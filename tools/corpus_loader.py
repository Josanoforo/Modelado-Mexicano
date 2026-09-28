#!/usr/bin/env python3
"""`tools/corpus_loader.py` -- caché columnar (Parquet) del corpus y su cargador único.

ACTO GEN2-CORPUS-CACHE-PARQUET-1
(`forense/encargos/2026-09-28-GEN2-CORPUS-CACHE-PARQUET-1.md`).

Defecto que ataca (D-14, transfer 26/sep §6): cada CALC lee el miembro CSV
entero del zip, lo decodifica y lo pasa a pandas con `dtype=str`; un miembro
de 230 MB cuesta varios GB de memoria y la caja (24 GB) quedó topada en dos
sesiones pesadas a la vez.

Dos mitades que no se mezclan:

1. `cargar(id, tabla, columnas=[...])` -- LECTURA, nunca escribe (D-23).
   Lee `<raíz de caché>/<id>/<tabla>.parquet` con proyección de columnas,
   después de verificar su sha256 contra `data/cache/constancias.tsv`. Si no
   hay caché, lee el miembro original del payload como TEXTO CRUDO y lo dice
   (aviso en stderr y `df.attrs["fuente"]`). Los medidores sellados no lo
   usan (E.3): lo que ya midió sigue midiendo del CSV.

2. CLI -- ESCRITURA de la caché, por comando:
     python3 tools/corpus_loader.py universo            # P1: qué entra
     python3 tools/corpus_loader.py convierte <id>...   # P2 (o --todos)
     python3 tools/corpus_loader.py verifica [<id>...]  # sha256 de cada Parquet
   `convierte` extrae cada miembro tabular del zip en streaming (memoria
   acotada por bloque), toma los tipos DECLARADOS -- diccionario de datos
   del zip para CSV, descriptor de campo para DBF, metadato del archivo para
   DTA/SAV -- y nunca los infiere; una columna sin tipo declarado, o cuyo
   soporte no cabe en el tipo declarado, queda como TEXTO y se cuenta. Cada
   miembro se lee dos veces (dos sha256 del miembro, A.7) y el Parquet una
   tercera: filas, columnas y, por columna, huella (texto) o suma exacta y
   no-nulos (numérico) contra el original. Sólo si todo casa se registra la
   constancia (id · miembro · sha256_origen · sha256_parquet · filas ·
   columnas · fecha · versión del conversor).

Olas reservadas (E.6, PARO a del encargo): `universo` y `convierte` se niegan
a tocar un id del conjunto `ids_reservados()` -- ver su docstring.

La caché es derivado del payload (mismo id), no entrada del manifiesto
(D-22(4)): este módulo nunca escribe `data/manifiesto.yaml`.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import hashlib
import importlib.util
import io
import json
import os
import re
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO / "data" / "cache"
UNIVERSO = CACHE_DIR / "universo-p1.tsv"


def _registro() -> Path:
    """Dónde viven constancias.tsv y verificacion.tsv: `data/cache/`, o
    `MM_CACHE_REGISTRO` (lo usa el test sintético para no escribir el árbol)."""
    return Path(os.environ.get("MM_CACHE_REGISTRO") or CACHE_DIR)


def _constancias() -> Path:
    return _registro() / "constancias.tsv"


def _verificacion() -> Path:
    return _registro() / "verificacion.tsv"
MANIFIESTO = REPO / "data" / "manifiesto.yaml"

VERSION_CONVERSOR = "corpus_loader-1.0"
COLS_CONSTANCIA = ["id", "miembro", "sha256_origen", "sha256_parquet", "filas",
                   "columnas", "fecha", "version_conversor"]
COLS_VERIFICACION = ["id", "miembro", "tabla", "sha256_zip", "sha256_origen_1",
                     "sha256_origen_2", "encoding", "filas_origen", "filas_parquet",
                     "cols_origen", "cols_parquet", "cols_valor_igual",
                     "cols_texto_sin_tipo_declarado", "cols_texto_soporte_no_numerico",
                     "cols_numericas", "huella_columnas", "veredicto"]

EXT_TABULAR = (".csv", ".dbf", ".dta", ".sav")
UMBRAL_YA_PEQUENO = 100_000_000  # bytes tabulares descomprimidos
BLOQUE_CSV = 1 << 26              # 64 MiB por lote de lectura
FILAS_LOTE = 200_000              # DBF / DTA / SAV

# --------------------------------------------------------------------------
# utilidades comunes (sin pyarrow: la lectura de constancias no lo necesita)
# --------------------------------------------------------------------------


def sha256_archivo(ruta, buf=1 << 22) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        while True:
            b = f.read(buf)
            if not b:
                return h.hexdigest()
            h.update(b)


def tabla_de(miembro: str) -> str:
    """Nombre de tabla (y del .parquet) derivado del miembro, determinista y sin
    contexto: tallo del archivo, precedido de su carpeta inmediata salvo que
    ésta sea la raíz o `conjunto_de_datos/` (patrón INEGI). Zip anidado:
    `externo.zip!carpeta/interno.csv` -> `externo__carpeta__interno`.
    (Con sólo el tallo, `edr2015_2019` -- cinco carpetas por año con los
    mismos `CAPGPO.dbf` -- se pisaba: lo atrapó `verifica`.)"""
    partes = miembro.split("!")
    out = []
    for i, p in enumerate(partes):
        segs = p.split("/")
        tallo = os.path.splitext(segs[-1])[0]
        if i < len(partes) - 1:
            out.append(tallo)
            continue
        padre = segs[-2] if len(segs) > 1 else ""
        if padre and padre.lower() != "conjunto_de_datos":
            out.append(padre)
        out.append(tallo)
    return re.sub(r"[^A-Za-z0-9_.-]", "_", "__".join(out))


def raiz_cache() -> Path:
    """Raíz física de la caché: `MM_CACHE_RAIZ`, o `cache:` de
    `data/raices.local.yaml`, o junto al corpus (`<realpath(data/raw)>/../cache`),
    o `data/cache/` del propio árbol si `data/raw` no existe."""
    env = os.environ.get("MM_CACHE_RAIZ")
    if env:
        return Path(env)
    loc = REPO / "data" / "raices.local.yaml"
    if loc.exists():
        for linea in loc.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^cache:\s*(\S.*)$", linea)
            if m:
                return Path(m.group(1).strip().strip("'\""))
    raw = REPO / "data" / "raw"
    if raw.exists():
        return Path(os.path.realpath(raw)).parent / "cache"
    return CACHE_DIR


def ruta_parquet(pid: str, tabla: str) -> Path:
    local = CACHE_DIR / pid / f"{tabla}.parquet"
    if local.exists() and not os.environ.get("MM_CACHE_RAIZ"):
        return local
    return raiz_cache() / pid / f"{tabla}.parquet"


def _lee_tsv(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []
    lineas = [l.rstrip("\n") for l in ruta.read_text(encoding="utf-8").splitlines()
              if l and not l.startswith("#")]
    if not lineas:
        return []
    cab = lineas[0].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def leer_constancias() -> dict[tuple[str, str], dict]:
    return {(r["id"], tabla_de(r["miembro"])): r for r in _lee_tsv(_constancias())}


def _anexa_tsv(ruta: Path, cols: list[str], fila: dict) -> None:
    # Sin el módulo csv (entrecomilla y corrompe TSV): tabulador pelado.
    nuevo = not ruta.exists()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "a", encoding="utf-8") as f:
        if nuevo:
            f.write("\t".join(cols) + "\n")
        vals = [str(fila.get(c, "")).replace("\t", " ").replace("\n", " ") for c in cols]
        f.write("\t".join(vals) + "\n")


def _manifiesto_mod():
    spec = importlib.util.spec_from_file_location("_mm_manifiesto", REPO / "tests" / "manifiesto.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_MAN_CACHE: dict | None = None


def manifiesto() -> dict[str, dict]:
    global _MAN_CACHE
    if _MAN_CACHE is None:
        import yaml
        loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
        with open(MANIFIESTO, encoding="utf-8") as f:
            _MAN_CACHE = {e["id"]: e for e in yaml.load(f, Loader=loader)}
    return _MAN_CACHE


def ruta_payload(pid: str) -> Path:
    e = manifiesto().get(pid)
    if e is None:
        raise KeyError(f"{pid}: no está en data/manifiesto.yaml")
    mm = _manifiesto_mod()
    nombre, _ = mm.resolver_raiz_declarada(e)
    base = mm.resolver_raiz(nombre, str(REPO), str(REPO / "data" / "raw"))
    if base is None:
        raise FileNotFoundError(f"{pid}: raíz '{nombre}' no configurada en esta máquina")
    return Path(base) / e["archivo"]


# --------------------------------------------------------------------------
# P1 · universo y reservas
# --------------------------------------------------------------------------

# Olas cuya reserva está declarada fuera del campo `estado_reserva` del
# manifiesto. Unión conservadora; ninguna se convierte.
#  (h) hoja consolidada «reserva sin decidir»
#      (forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md:22-31)
#  (m) régimen vigente, canon/MEMORIA-OPERATIVA.md §1 «Reservas» (E.6: «toda ola
#      nueva de una encuesta con historia nace RESERVADA»; firma sobre ENIGH 2024, #964)
RESERVA_FUERA_DEL_MANIFIESTO = [
    (r"encrige.*2020", "h: ENCRIGE 2020"),
    (r"(^|_)(oe1_)?enve.*2024", "h: ENVE 2024"),
    (r"cses.*(m5|modulo_?5|module_?5|2018)", "h: CSES Módulo 5"),
    (r"endutih.*2025", "h: ENDUTIH 2025"),
    (r"enif.*2024", "h: ENIF 2024 (reservas por módulo; módulo 7)"),
    (r"envipe.*2026", "m: ENVIPE 2026"),
    (r"enigh.*2024", "m: ENIGH 2024"),
    (r"(^|_)enco(_|$)", "m: ENCO"),
]


def motivo_reserva(pid: str, entrada: dict | None) -> str:
    """'' si el id no está reservado; si lo está, de dónde sale la reserva."""
    if entrada and str(entrada.get("estado_reserva", "")).startswith("RESERVADA"):
        return f"manifiesto: {entrada['estado_reserva']}"
    for patron, motivo in RESERVA_FUERA_DEL_MANIFIESTO:
        if re.search(patron, pid.lower()):
            return motivo
    return ""


def ids_citados() -> dict[str, set[str]]:
    """id -> fuentes que lo citan: inputs `origen: manifiesto` de
    data/corrida0/*/spec.yaml (sellados o no; familias 2027 aparte), ids de
    `payload_ids` en data/corrida0/demanda-corridas.tsv, e ids del manifiesto
    citados literalmente en forense/analisis/familias-2027/."""
    import yaml
    man = manifiesto()
    cita: dict[str, set[str]] = {}
    for sp in sorted(glob.glob(str(REPO / "data" / "corrida0" / "*" / "spec.yaml"))):
        calc = Path(sp).parent.name
        sellado = (Path(sp).parent / "sello.json").exists()
        try:
            y = yaml.safe_load(open(sp, encoding="utf-8")) or {}
        except Exception:
            continue
        for inp in y.get("inputs") or []:
            if isinstance(inp, dict) and inp.get("origen") == "manifiesto" and inp.get("id"):
                fam = "FAMILIA-2027" in calc or "FAMILIAS-2027" in calc
                src = "familia2027" if fam else ("calc-sellado" if sellado else "calc-sin-sello")
                cita.setdefault(inp["id"], set()).add(f"{src}:{calc}")
    dem = REPO / "data" / "corrida0" / "demanda-corridas.tsv"
    for r in _lee_tsv(dem):
        for tok in (r.get("payload_ids") or "").split(";"):
            m = re.match(r"^\s*(?:ola\d=|peso=)?([a-z0-9_]+)\s*$", tok)
            if m and m.group(1) in man:
                cita.setdefault(m.group(1), set()).add(f"demanda:{r['corrida_id']}")
    for f in glob.glob(str(REPO / "forense" / "analisis" / "familias-2027" / "**" / "*"), recursive=True):
        if not os.path.isfile(f):
            continue
        txt = open(f, encoding="utf-8", errors="ignore").read()
        for tok in set(re.findall(r"[a-z][a-z0-9_]{5,}", txt)):
            if tok in man:
                cita.setdefault(tok, set()).add("familia2027-analisis:" + Path(f).relative_to(REPO).parts[3])
    return cita


def _es_datos(nombre: str, todos: list[str]) -> bool:
    n = nombre.lower()
    if not n.endswith(EXT_TABULAR):
        return False
    if any("/conjunto_de_datos/" in "/" + t.lower() for t in todos):
        return "/conjunto_de_datos/" in "/" + n
    return not re.search(r"(^|/)(catalogos?|diccionario[^/]*|metadatos)/", n)


def miembros_tabulares(ruta: Path) -> list[tuple[str, int]]:
    """(miembro, bytes) de los miembros de datos; un nivel de zip anidado
    como `externo.zip!interno.csv`. Sólo directorio central (no abre dato)."""
    import zipfile_deflate64  # noqa: F401  (registra deflate64 en zipfile)
    s = str(ruta).lower()
    if s.endswith(EXT_TABULAR):
        return [(ruta.name, ruta.stat().st_size)]
    if not s.endswith(".zip"):
        return []
    out = []
    with zipfile.ZipFile(ruta) as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        nombres = [i.filename for i in infos]
        for i in infos:
            if _es_datos(i.filename, nombres):
                out.append((i.filename, i.file_size))
            elif i.filename.lower().endswith(".zip"):
                with z.open(i) as fz, zipfile.ZipFile(io.BytesIO(fz.read())) as zi:
                    inn = [j for j in zi.infolist() if not j.is_dir()]
                    nn = [j.filename for j in inn]
                    out += [(f"{i.filename}!{j.filename}", j.file_size) for j in inn
                            if _es_datos(j.filename, nn)]
    return out


def universo(escribe: bool = True) -> list[dict]:
    man = manifiesto()
    filas = []
    for pid, fuentes in sorted(ids_citados().items()):
        e = man.get(pid)
        fila = {"id": pid, "archivo": (e or {}).get("archivo", ""),
                "formato": "", "tamano_bytes": (e or {}).get("tamano_bytes", ""),
                "bytes_tabulares": "", "n_miembros": "", "decision": "", "motivo": "",
                "citado_por": ",".join(sorted({f.split(":")[0] for f in fuentes})),
                "n_citas": len(fuentes)}
        if e is None:
            fila.update(decision="NO-SE-CONVIERTE", motivo="NO-EN-MANIFIESTO")
            filas.append(fila)
            continue
        ext = os.path.splitext(e.get("archivo", ""))[1].lower()
        fila["formato"] = ext.lstrip(".")
        res = motivo_reserva(pid, e)
        if res:
            # La reserva se decide ANTES de mirar el zip: ni su directorio central.
            fila.update(decision="NO-SE-CONVIERTE", motivo=f"RESERVADA ({res})")
            filas.append(fila)
            continue
        try:
            ruta = ruta_payload(pid)
            miembros = miembros_tabulares(ruta) if ruta.exists() else None
        except Exception as ex:  # raíz no configurada, zip roto
            miembros, fila["motivo"] = None, f"NO-LEGIBLE-AQUI ({type(ex).__name__})"
        if miembros is None:
            fila.update(decision="NO-SE-CONVIERTE", motivo=fila["motivo"] or "NO-LEGIBLE-AQUI (payload ausente)")
        elif not miembros:
            fila.update(decision="NO-SE-CONVIERTE", motivo="FORMATO-NO-TABULAR")
        else:
            tb = sum(b for _, b in miembros)
            exts = sorted({os.path.splitext(m.split("!")[-1])[1].lower().lstrip(".") for m, _ in miembros})
            fila.update(formato="+".join(exts), bytes_tabulares=tb, n_miembros=len(miembros))
            if tb < UMBRAL_YA_PEQUENO:
                fila.update(decision="NO-SE-CONVIERTE", motivo=f"YA-PEQUEÑO (<{UMBRAL_YA_PEQUENO // 10**6} MB tabulares)")
            else:
                fila.update(decision="SE-CONVIERTE", motivo="")
        filas.append(fila)
    if escribe:
        cols = ["id", "archivo", "formato", "tamano_bytes", "bytes_tabulares", "n_miembros",
                "decision", "motivo", "citado_por", "n_citas"]
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(UNIVERSO, "w", encoding="utf-8") as f:
            f.write("# DERIVADO por `python3 tools/corpus_loader.py universo` -- no editar a mano\n")
            f.write("\t".join(cols) + "\n")
            for r in filas:
                f.write("\t".join(str(r[c]) for c in cols) + "\n")
    return filas


# --------------------------------------------------------------------------
# Lectores en streaming -> lotes Arrow de TEXTO CRUDO
# --------------------------------------------------------------------------


class _Hasheador(io.RawIOBase):
    """Envuelve un flujo de lectura y lleva su sha256 (A.7: huella del miembro)."""

    def __init__(self, f):
        self.f, self.h, self.n = f, hashlib.sha256(), 0

    def readable(self):
        return True

    def readinto(self, b):
        d = self.f.read(len(b))
        n = len(d)
        b[:n] = d
        self.h.update(d)
        self.n += n
        return n

    def agota(self):
        while self.read(1 << 22):
            pass
        return self.h.hexdigest()


def _abre_miembro(ruta_zip: Path, miembro: str):
    """Flujo binario del miembro (un nivel de anidamiento). El llamador cierra."""
    import zipfile_deflate64  # noqa: F401
    if not str(ruta_zip).lower().endswith(".zip"):
        return open(ruta_zip, "rb"), []
    z = zipfile.ZipFile(ruta_zip)
    partes = miembro.split("!")
    if len(partes) == 1:
        return z.open(partes[0]), [z]
    zi = zipfile.ZipFile(io.BytesIO(z.read(partes[0])))
    return zi.open(partes[1]), [z, zi]


def _nombres_zip(ruta_zip: Path, miembro: str) -> list[str]:
    import zipfile_deflate64  # noqa: F401
    if not str(ruta_zip).lower().endswith(".zip"):
        return []
    with zipfile.ZipFile(ruta_zip) as z:
        if "!" not in miembro:
            return z.namelist()
        return zipfile.ZipFile(io.BytesIO(z.read(miembro.split("!")[0]))).namelist()


def _cabecera_csv(ruta_zip, miembro, forzado=None):
    """(encoding, delimitador, nombres crudos) leyendo sólo el primer MiB.
    `forzado="latin1"` cuando el UTF-8 falla más allá del primer MiB."""
    import csv as _csv
    f, cierra = _abre_miembro(ruta_zip, miembro)
    try:
        cab = f.read(1 << 20)
    finally:
        f.close()
        for c in cierra:
            c.close()
    try:
        if forzado == "latin1":
            raise UnicodeDecodeError("utf-8", b"", 0, 1, "forzado")
        texto, enc = cab.decode("utf-8-sig"), "utf8"
    except UnicodeDecodeError as ex:
        if forzado == "latin1":
            ex = UnicodeDecodeError("utf-8", cab, 0, 1, "forzado")
        # un corte de secuencia multibyte al final del MiB no es latin-1
        try:
            texto, enc = cab[:ex.start].decode("utf-8-sig"), "utf8"
            if ex.start < len(cab) - 4:
                raise UnicodeDecodeError("utf-8", cab, ex.start, ex.end, "interno")
        except UnicodeDecodeError:
            texto, enc = cab.decode("latin-1"), "latin1"
    linea = re.split(r"\r\n|\r|\n", texto, maxsplit=1)[0]  # hay CSV con fin de línea \r solo
    delim = max([",", ";", "|", "\t"], key=linea.count)
    nombres = next(_csv.reader([linea], delimiter=delim))
    return enc, delim, nombres


def _lotes_csv(flujo, enc, delim, nombres):
    import pyarrow as pa
    import pyarrow.csv as pcsv
    r = pcsv.open_csv(
        flujo,
        read_options=pcsv.ReadOptions(block_size=BLOQUE_CSV, encoding=enc),
        parse_options=pcsv.ParseOptions(delimiter=delim, newlines_in_values=True),
        convert_options=pcsv.ConvertOptions(
            column_types={n: pa.string() for n in nombres},
            strings_can_be_null=False, quoted_strings_can_be_null=False))
    for lote in r:
        yield lote


def _campos_dbf(cab: bytes):
    campos, pos = [], 32
    while pos + 32 <= len(cab) and cab[pos:pos + 1] != b"\x0d":
        d = cab[pos:pos + 32]
        campos.append((d[0:11].split(b"\x00")[0].decode("latin-1"), d[11:12].decode("latin-1"), d[16], d[17]))
        pos += 32
    return campos


def _lotes_dbf(flujo):
    """Lotes de texto crudo de un DBF (latin-1, con strip, como tests/dbfmini.py).
    Devuelve primero la lista de campos (nombre, tipo, ancho, decimales)."""
    import numpy as np
    import pyarrow as pa
    h = flujo.read(32)
    nreg = struct.unpack("<I", h[4:8])[0]
    hsize = struct.unpack("<H", h[8:10])[0]
    rsize = struct.unpack("<H", h[10:12])[0]
    resto = flujo.read(hsize - 32)
    campos = _campos_dbf(h + resto)
    yield campos
    dt = np.dtype([("_borrado", "S1")] + [(f"f{i}", f"S{c[2]}") for i, c in enumerate(campos)])
    if dt.itemsize != rsize:
        raise ValueError(f"DBF: ancho de registro {rsize} != suma de campos {dt.itemsize}")
    leidos = 0
    while leidos < nreg:
        k = min(FILAS_LOTE, nreg - leidos)
        buf = flujo.read(k * rsize)
        k = len(buf) // rsize
        if k == 0:
            break
        leidos += k
        arr = np.frombuffer(buf[:k * rsize], dtype=dt)
        arr = arr[arr["_borrado"] != b"*"]
        cols = [pa.array(np.char.strip(np.char.decode(arr[f"f{i}"], "latin-1")).tolist(), type=pa.string())
                for i in range(len(campos))]
        yield pa.RecordBatch.from_arrays(cols, names=[c[0] for c in campos])


# --------------------------------------------------------------------------
# Tipos declarados
# --------------------------------------------------------------------------


def _tipo_declarado(t: str):
    t = (t or "").strip().upper()
    t = t.replace("É", "E").replace("Á", "A").replace("Ú", "U").replace("�", "")
    if not t:
        return None
    if t.startswith(("N", "ENT", "DEC", "FLOAT", "INT", "DOUBLE", "REAL")):
        return "N"
    if t.startswith(("C", "A", "T", "S", "CHAR", "STR")):
        return "C"
    return None


def diccionario_csv(ruta_zip: Path, miembro: str) -> dict[str, str] | None:
    """{columna(MAYÚS): 'N'|'C'|'?'} del diccionario_de_datos hermano del miembro,
    o None si el zip no trae un diccionario legible por máquina para él."""
    import csv as _csv
    nombres = _nombres_zip(ruta_zip, miembro)
    interno = miembro.split("!")[-1]
    if "/conjunto_de_datos/" not in "/" + interno.lower():
        return None
    carpeta = interno[: ("/" + interno).lower().index("/conjunto_de_datos/")]
    dic = [n for n in nombres if n.lower().endswith(".csv") and "/diccionario" in "/" + n.lower()
           and n.startswith(carpeta)]
    if len(dic) != 1:
        return None
    pref = miembro.split("!")[0] + "!" if "!" in miembro else ""
    f, cierra = _abre_miembro(ruta_zip, pref + dic[0])
    try:
        raw = f.read()
    finally:
        f.close()
        for c in cierra:
            c.close()
    try:
        texto = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = raw.decode("latin-1")
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")  # hay diccionarios con fin de línea \r solo
    filas = list(_csv.reader(io.StringIO(texto)))
    for i, fila in enumerate(filas):
        up = [c.strip().upper() for c in fila]
        it = next((j for j, c in enumerate(up) if c == "TIPO"), None)
        iv = next((j for j, c in enumerate(up) if re.sub(r"[^A-Z]", "", c) in ("NEMONICO", "NEMNICO", "VARIABLE")), None)
        if it is None or iv is None:
            continue
        out = {}
        for f2 in filas[i + 1:]:
            if len(f2) <= max(it, iv) or not f2[iv].strip():
                continue
            out[f2[iv].strip().upper()] = _tipo_declarado(f2[it]) or "?"
        return out or None
    return None


# --------------------------------------------------------------------------
# Huellas por columna (misma función sobre origen y sobre Parquet)
# --------------------------------------------------------------------------


class _Col:
    __slots__ = ("h", "hl", "n", "vacios", "es_int", "es_float", "suma_hi", "suma_lo", "no_nulos")

    def __init__(self):
        # dos flujos (bytes y longitudes): concatenaciones, luego no dependen del corte en lotes
        self.h, self.hl = hashlib.sha256(), hashlib.sha256()
        self.n = self.vacios = self.no_nulos = self.suma_hi = self.suma_lo = 0
        self.es_int = self.es_float = True


RE_INT = r"^-?\d{1,18}$"
RE_FLOAT = r"^-?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$"


def _huella_texto(c, arr):
    import numpy as np
    import pyarrow as pa
    if arr.null_count:
        arr = arr.fill_null("")
    if pa.types.is_large_string(arr.type):
        dt = np.int64
    else:
        arr = arr.cast(pa.string()) if not pa.types.is_string(arr.type) else arr
        dt = np.int32
    buf = arr.buffers()
    offs = np.frombuffer(buf[1], dtype=dt)[arr.offset: arr.offset + len(arr) + 1]
    c.hl.update(np.diff(offs).astype("<i8").tobytes())
    if len(offs) and buf[2] is not None:
        c.h.update(memoryview(buf[2])[int(offs[0]):int(offs[-1])])


def _suma_entera(c: _Col, arr):
    import numpy as np
    v = arr.drop_null().to_numpy(zero_copy_only=False).astype(np.int64)
    c.suma_hi += int((v >> 32).sum())
    c.suma_lo += int((v & 0xFFFFFFFF).sum())
    c.no_nulos += len(v)


def _suma_flotante(c: _Col, arr):
    """Huella de los float64 (bytes de valor + máscara de nulos): una fsum por
    lote no es independiente del corte en lotes; una concatenación sí."""
    import numpy as np
    import pyarrow as pa
    arr = arr.cast(pa.float64())
    c.hl.update(arr.is_null().to_numpy(zero_copy_only=False).astype(np.uint8).tobytes())
    c.h.update(arr.fill_null(0.0).to_numpy(zero_copy_only=False).astype("<f8").tobytes())
    c.no_nulos += len(arr) - arr.null_count


def _estado_texto(c: _Col) -> str:
    return f"T:{c.n}:{hashlib.sha256((c.h.hexdigest() + c.hl.hexdigest()).encode()).hexdigest()}"


def _estado_int(c: _Col) -> str:
    return f"I:{c.no_nulos}:{(c.suma_hi << 32) + c.suma_lo}"


def _estado_float(c: _Col) -> str:
    return f"F:{c.no_nulos}:{hashlib.sha256((c.h.hexdigest() + c.hl.hexdigest()).encode()).hexdigest()}"


# --------------------------------------------------------------------------
# P2 · conversión de un miembro
# --------------------------------------------------------------------------


def _fecha():
    try:
        from zoneinfo import ZoneInfo
        return _dt.datetime.now(ZoneInfo("America/Mexico_City")).date().isoformat()
    except Exception:
        return _dt.date.today().isoformat()


def _convierte_texto_tabular(pid, ruta, miembro, sha_zip, destino: Path, formato):
    """CSV o DBF: pasada 1 (sha1 + huellas + tipos), pasada 2 (sha2 + escritura),
    pasada 3 (Parquet -> huellas). Devuelve (constancia, verificacion) o lanza."""
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    forzado = {"enc": None}

    def lotes():
        f, cierra = _abre_miembro(ruta, miembro)
        hsh = _Hasheador(f)
        flujo = io.BufferedReader(hsh, buffer_size=1 << 22)
        try:
            if formato == "csv":
                enc, delim, nombres = _cabecera_csv(ruta, miembro, forzado["enc"])
                meta = {"encoding": enc, "delim": delim, "nombres": nombres}
                return hsh, flujo, cierra, meta, _lotes_csv(flujo, enc, delim, nombres)
            gen = _lotes_dbf(flujo)
            campos = next(gen)
            meta = {"encoding": "latin1", "campos": campos, "nombres": [c[0] for c in campos]}
            return hsh, flujo, cierra, meta, gen
        except Exception:
            flujo.close()
            for c in cierra:
                c.close()
            raise

    # ---- pasada 1 (reintenta en latin-1 si el UTF-8 cae después del primer MiB)
    def pasada1():
        hsh, flujo, cierra, meta, gen = lotes()
        if formato == "csv":
            dic = diccionario_csv(ruta, miembro)
            declarado = {n: (dic or {}).get(n.strip().upper()) for n in meta["nombres"]}
        else:
            declarado = {c[0]: ("N" if c[1] in "NFBI" else "C") for c in meta["campos"]}
        stats = {n: _Col() for n in meta["nombres"]}
        filas = 0
        try:
            for lote in gen:
                if lote.schema.names != meta["nombres"] or any(t != pa.string() for t in lote.schema.types):
                    raise ValueError("el lector no devolvió exactamente las columnas de la cabecera como texto")
                filas += lote.num_rows
                for n, arr in zip(lote.schema.names, lote.columns):
                    c = stats[n]
                    c.n += len(arr)
                    _huella_texto(c, arr)
                    if declarado.get(n) == "N" and (c.es_int or c.es_float):
                        nov = arr.filter(pc.not_equal(arr, ""))
                        if len(nov) == 0:
                            continue
                        if c.es_int and not pc.all(pc.match_substring_regex(nov, RE_INT)).as_py():
                            c.es_int = False
                        if c.es_float and not pc.all(pc.match_substring_regex(nov, RE_FLOAT)).as_py():
                            c.es_float = False
            return meta, declarado, stats, filas, hsh.agota()
        finally:
            flujo.close()
            for cc in cierra:
                cc.close()

    try:
        meta, declarado, stats, filas, sha1 = pasada1()
    except pa.ArrowInvalid as ex:
        if formato != "csv" or "invalid UTF8" not in str(ex):
            raise
        forzado["enc"] = "latin1"
        meta, declarado, stats, filas, sha1 = pasada1()

    # ---- tipos decididos (declarados, nunca inferidos)
    tipos, sin_decl, soporte_no_num = {}, 0, 0
    for n in meta["nombres"]:
        d, c = declarado.get(n), stats[n]
        if d == "N" and c.es_int:
            tipos[n] = pa.int64()
        elif d == "N" and c.es_float:
            tipos[n] = pa.float64()
        else:
            tipos[n] = pa.string()
            if d == "N":
                soporte_no_num += 1
            elif d is None or d == "?":
                sin_decl += 1
    nombres_limpios = [n.strip() for n in meta["nombres"]]
    if len(set(nombres_limpios)) != len(nombres_limpios):
        raise ValueError("columnas duplicadas tras strip del nombre")
    ref = {}
    for n in meta["nombres"]:
        t = tipos[n]
        ref[n] = _estado_texto(stats[n]) if t == pa.string() else None

    # ---- pasada 2: escritura (y sha2, y referencias numéricas desde el texto)
    esquema = pa.schema([pa.field(nl, tipos[n]) for n, nl in zip(meta["nombres"], nombres_limpios)])
    tipos_fuente = {nl: {"declarado": declarado.get(n) or "SIN-DECLARAR", "parquet": str(tipos[n])}
                    for n, nl in zip(meta["nombres"], nombres_limpios)}
    md = {"mm.id": pid, "mm.miembro": miembro, "mm.sha256_origen": sha1, "mm.sha256_zip": sha_zip,
          "mm.encoding": meta["encoding"], "mm.conversor": VERSION_CONVERSOR,
          "mm.tipos": json.dumps(tipos_fuente, ensure_ascii=False, sort_keys=True)}
    esquema = esquema.with_metadata(md)
    tmp = destino.with_suffix(".parquet.tmp")
    destino.parent.mkdir(parents=True, exist_ok=True)
    num = {n: _Col() for n in meta["nombres"] if tipos[n] != pa.string()}
    hsh, flujo, cierra, meta2, gen = lotes()
    filas2 = 0
    try:
        with pq.ParquetWriter(tmp, esquema, compression="zstd", compression_level=3) as w:
            for lote in gen:
                filas2 += lote.num_rows
                cols = []
                for n, arr in zip(lote.schema.names, lote.columns):
                    t = tipos[n]
                    if t == pa.string():
                        cols.append(arr)
                        continue
                    arr = pc.if_else(pc.equal(arr, ""), pa.scalar(None, pa.string()), arr)
                    v = pc.cast(arr, t)
                    (_suma_entera if t == pa.int64() else _suma_flotante)(num[n], v)
                    cols.append(v)
                w.write_batch(pa.RecordBatch.from_arrays(cols, schema=esquema))
        sha2 = hsh.agota()
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise
    finally:
        flujo.close()
        for cc in cierra:
            cc.close()
    for n, c in num.items():
        ref[n] = _estado_int(c) if tipos[n] == pa.int64() else _estado_float(c)
    return _verifica_y_sella(pid, ruta, miembro, sha_zip, destino, tmp, sha1, sha2, filas, filas2,
                             meta["nombres"], nombres_limpios, ref, tipos, sin_decl, soporte_no_num,
                             meta["encoding"])


def _convierte_readstat(pid, ruta, miembro, sha_zip, destino: Path, formato, tmpdir):
    """DTA/SAV: extracción a temporal (sha1), re-hash del temporal (sha2),
    tipos del metadato del archivo, lectura por bloques con pyreadstat. Si los
    strings no son válidos en la codificación declarada, reintenta en latin-1
    (biyectiva sobre bytes) y lo deja en `mm.encoding`."""
    import pyreadstat
    f, cierra = _abre_miembro(ruta, miembro)
    hsh = _Hasheador(f)
    with tempfile.NamedTemporaryFile(suffix="." + formato, dir=tmpdir, delete=False) as t:
        tmpsrc = t.name
        try:
            while True:
                b = hsh.read(1 << 22)
                if not b:
                    break
                t.write(b)
        finally:
            f.close()
            for c in cierra:
                c.close()
    sha1 = hsh.h.hexdigest()
    try:
        sha2 = sha256_archivo(tmpsrc)
        try:
            return _escribe_readstat(pid, ruta, miembro, sha_zip, destino, formato, tmpsrc, sha1, sha2, {})
        except pyreadstat.ReadstatError as ex:
            if "encoding" not in str(ex):
                raise
            return _escribe_readstat(pid, ruta, miembro, sha_zip, destino, formato, tmpsrc, sha1, sha2,
                                     {"encoding": "latin1"})
    finally:
        os.unlink(tmpsrc)
        parcial = destino.with_suffix(".parquet.tmp")
        if parcial.exists():
            parcial.unlink()


def _escribe_readstat(pid, ruta, miembro, sha_zip, destino, formato, tmpsrc, sha1, sha2, kw):
    import numpy as np
    import pyarrow as pa
    import pyarrow.parquet as pq
    import pyreadstat
    lector = pyreadstat.read_dta if formato == "dta" else pyreadstat.read_sav
    _, m = lector(tmpsrc, metadataonly=True, **kw)
    nombres = list(m.column_names)
    rt = m.readstat_variable_types
    tipos = {}
    for n in nombres:
        v = rt.get(n, "")
        tipos[n] = pa.string() if v == "string" else (pa.int64() if v.startswith("int") else pa.float64())
    tipos_fuente = {n: {"declarado": rt.get(n, "SIN-DECLARAR"), "parquet": str(tipos[n])} for n in nombres}
    enc = "latin1-forzado" if kw else (getattr(m, "file_encoding", "") or "")
    md = {"mm.id": pid, "mm.miembro": miembro, "mm.sha256_origen": sha1, "mm.sha256_zip": sha_zip,
          "mm.encoding": enc, "mm.conversor": VERSION_CONVERSOR,
          "mm.tipos": json.dumps(tipos_fuente, ensure_ascii=False, sort_keys=True)}
    esquema = pa.schema([pa.field(n, tipos[n]) for n in nombres]).with_metadata(md)
    stats = {n: _Col() for n in nombres}
    bloque = max(5_000, min(FILAS_LOTE, 20_000_000 // max(1, len(nombres))))
    tmp = destino.with_suffix(".parquet.tmp")
    destino.parent.mkdir(parents=True, exist_ok=True)
    filas = 0
    with pq.ParquetWriter(tmp, esquema, compression="zstd", compression_level=3) as w:
        # bloques a mano: read_file_in_chunks relee el metadato sin `encoding`
        desde = 0
        while True:
            df, _ = lector(tmpsrc, row_offset=desde, row_limit=bloque,
                           disable_datetime_conversion=True, **kw)
            if len(df) == 0:
                break
            desde += len(df)
            filas += len(df)
            cols = []
            for n in nombres:
                s, t = df[n], tipos[n]
                c = stats[n]
                if t == pa.string():
                    a = pa.array(s.astype(object).where(s.notna(), "").astype(str).tolist(), type=pa.string())
                    c.n += len(a)
                    _huella_texto(c, a)
                else:
                    a = pa.array(np.asarray(s, dtype="float64"), from_pandas=True)
                    if t == pa.int64():
                        a = a.cast(pa.int64())  # safe: falla si hay fracción
                        _suma_entera(c, a)
                    else:
                        _suma_flotante(c, a)
                cols.append(a)
            w.write_batch(pa.RecordBatch.from_arrays(cols, schema=esquema))
    ref = {n: (_estado_texto(stats[n]) if tipos[n] == pa.string() else
               _estado_int(stats[n]) if tipos[n] == pa.int64() else _estado_float(stats[n]))
           for n in nombres}
    return _verifica_y_sella(pid, ruta, miembro, sha_zip, destino, tmp, sha1, sha2, filas, filas,
                             nombres, nombres, ref, tipos, 0, 0, enc)


def huellas_parquet(ruta: Path) -> tuple[int, list[str], dict[str, str]]:
    """(filas, columnas, {columna: huella}) leyendo el Parquet por lotes."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    pf = pq.ParquetFile(ruta)
    nombres = pf.schema_arrow.names
    st = {n: _Col() for n in nombres}
    filas = 0
    for lote in pf.iter_batches(batch_size=FILAS_LOTE):
        filas += lote.num_rows
        for n, arr in zip(nombres, lote.columns):
            c = st[n]
            if pa.types.is_string(arr.type) or pa.types.is_large_string(arr.type):
                c.n += len(arr)
                _huella_texto(c, arr)
            elif pa.types.is_integer(arr.type):
                _suma_entera(c, arr)
            else:
                _suma_flotante(c, arr)
    out = {}
    for n in nombres:
        t = pf.schema_arrow.field(n).type
        out[n] = (_estado_texto(st[n]) if pa.types.is_string(t) or pa.types.is_large_string(t) else
                  _estado_int(st[n]) if pa.types.is_integer(t) else _estado_float(st[n]))
    return filas, nombres, out


def _verifica_y_sella(pid, ruta, miembro, sha_zip, destino, tmp, sha1, sha2, filas1, filas2,
                      nombres, nombres_limpios, ref, tipos, sin_decl, soporte_no_num, enc):
    import pyarrow as pa
    fp, cols_p, huellas = huellas_parquet(tmp)
    iguales = sum(1 for n, nl in zip(nombres, nombres_limpios) if huellas.get(nl) == ref[n])
    n_num = sum(1 for n in nombres if tipos[n] != pa.string())
    ok = (sha1 == sha2 and filas1 == filas2 == fp and cols_p == nombres_limpios
          and iguales == len(nombres))
    huella_cols = hashlib.sha256("\n".join(f"{nl}\t{huellas.get(nl)}" for nl in nombres_limpios)
                                 .encode()).hexdigest()
    verif = {"id": pid, "miembro": miembro, "tabla": tabla_de(miembro), "sha256_zip": sha_zip,
             "sha256_origen_1": sha1, "sha256_origen_2": sha2, "encoding": enc,
             "filas_origen": filas1, "filas_parquet": fp, "cols_origen": len(nombres),
             "cols_parquet": len(cols_p), "cols_valor_igual": iguales,
             "cols_texto_sin_tipo_declarado": sin_decl, "cols_texto_soporte_no_numerico": soporte_no_num,
             "cols_numericas": n_num, "huella_columnas": huella_cols,
             "veredicto": "IGUAL" if ok else "DISCORDANTE"}
    if not ok:
        tmp.unlink()
        return None, verif
    os.replace(tmp, destino)
    cons = {"id": pid, "miembro": miembro, "sha256_origen": sha1,
            "sha256_parquet": sha256_archivo(destino), "filas": fp, "columnas": len(cols_p),
            "fecha": _fecha(), "version_conversor": VERSION_CONVERSOR}
    return cons, verif


def convierte(pid: str, tmpdir: str | None = None, log=print) -> dict:
    """Convierte todos los miembros de datos de `pid`. Idempotente: un miembro
    con constancia y Parquet cuyo sha casa no se vuelve a convertir."""
    man = manifiesto()
    e = man.get(pid)
    if e is None:
        raise KeyError(pid)
    res = motivo_reserva(pid, e)
    if res:
        raise PermissionError(f"PARO-a: {pid} está RESERVADA ({res}); no se convierte")
    ruta = ruta_payload(pid)
    sha_zip = sha256_archivo(ruta)
    if sha_zip != e.get("sha256"):
        log(f"PARA-CONVERSION {pid}: A.1 hash-discordante zip={sha_zip} manifiesto={e.get('sha256')}")
        return {"id": pid, "estado": "HASH-DISCORDANTE"}
    hechas = leer_constancias()
    resumen = {"id": pid, "estado": "OK", "miembros": 0, "convertidos": 0, "ya": 0, "fallos": []}
    miembros = [m for m, _ in miembros_tabulares(ruta)]
    dup = [t for t, n in __import__("collections").Counter(map(tabla_de, miembros)).items() if n > 1]
    if dup:
        raise ValueError(f"{pid}: dos miembros comparten nombre de tabla {dup[:3]}")
    for miembro in miembros:
        resumen["miembros"] += 1
        tabla = tabla_de(miembro)
        destino = raiz_cache() / pid / f"{tabla}.parquet"
        prev = hechas.get((pid, tabla))
        if prev and destino.exists() and prev["sha256_parquet"] == sha256_archivo(destino):
            resumen["ya"] += 1
            continue
        fmt = os.path.splitext(miembro.split("!")[-1])[1].lower().lstrip(".")
        try:
            if fmt in ("csv", "dbf"):
                cons, verif = _convierte_texto_tabular(pid, ruta, miembro, sha_zip, destino, fmt)
            else:
                cons, verif = _convierte_readstat(pid, ruta, miembro, sha_zip, destino, fmt,
                                                  tmpdir or tempfile.gettempdir())
        except Exception as ex:
            msg = f"{type(ex).__name__}: {str(ex)[:300]}"
            resumen["fallos"].append((miembro, msg))
            _anexa_tsv(_verificacion(), COLS_VERIFICACION,
                       {"id": pid, "miembro": miembro, "tabla": tabla, "sha256_zip": sha_zip,
                        "veredicto": "ERROR " + msg})
            log(f"  ERROR {pid} {miembro}: {msg}")
            continue
        _anexa_tsv(_verificacion(), COLS_VERIFICACION, verif)
        if cons is None:
            resumen["fallos"].append((miembro, "DISCORDANTE"))
            log(f"  DISCORDANTE {pid} {miembro}: {verif}")
            continue
        _anexa_tsv(_constancias(), COLS_CONSTANCIA, cons)
        resumen["convertidos"] += 1
        log(f"  OK {pid} {miembro} filas={cons['filas']} cols={cons['columnas']} "
            f"num={verif['cols_numericas']} sin_decl={verif['cols_texto_sin_tipo_declarado']} "
            f"sop_no_num={verif['cols_texto_soporte_no_numerico']}")
    if resumen["fallos"]:
        resumen["estado"] = "PARCIAL" if resumen["convertidos"] + resumen["ya"] else "FALLO"
    return resumen


# --------------------------------------------------------------------------
# P3 · cargador (nunca escribe)
# --------------------------------------------------------------------------


def _a_pandas(tabla, como):
    import pandas as pd
    import pyarrow as pa
    if como == "arrow":
        return tabla
    mapa = {pa.string(): pd.StringDtype("pyarrow"), pa.large_string(): pd.StringDtype("pyarrow"),
            pa.int64(): pd.Int64Dtype(), pa.int32(): pd.Int64Dtype()}
    return tabla.to_pandas(types_mapper=mapa.get, self_destruct=True, split_blocks=True)


def cargar(id: str, tabla: str, columnas: list[str] | None = None, como: str = "pandas"):
    """Lee `tabla` del payload `id`, con proyección a `columnas`.

    Con caché: verifica el sha256 del Parquet contra `data/cache/constancias.tsv`
    ANTES de leer (discordancia -> ValueError) y devuelve los tipos declarados
    (texto como `string[pyarrow]`, enteros como `Int64`). Sin caché: lee el
    miembro original del payload como texto crudo y lo avisa por stderr.
    `df.attrs["fuente"]` dice cuál de las dos fue. `como="arrow"` devuelve la
    `pyarrow.Table`. Nunca escribe."""
    import pyarrow.parquet as pq
    cons = leer_constancias().get((id, tabla))
    ruta = ruta_parquet(id, tabla)
    if cons is not None and ruta.exists():
        sha = sha256_archivo(ruta)
        if sha != cons["sha256_parquet"]:
            raise ValueError(f"CACHE-DISCORDANTE {id}/{tabla}: sha256 {sha} != constancia {cons['sha256_parquet']}")
        t = pq.read_table(ruta, columns=columnas)
        out = _a_pandas(t, como)
        fuente = f"PARQUET:{id}/{tabla}.parquet:{sha}"
    else:
        print(f"AVISO corpus_loader: {id}/{tabla} sin caché con constancia -> leo el original como TEXTO CRUDO",
              file=sys.stderr)
        t = _lee_original(id, tabla, columnas)
        out = _a_pandas(t, como)
        fuente = f"ORIGINAL-TEXTO-CRUDO:{id}:{tabla}"
    if como != "arrow":
        out.attrs["fuente"] = fuente
    return out


def _lee_original(pid: str, tabla: str, columnas):
    import pyarrow as pa
    ruta = ruta_payload(pid)
    cands = [m for m, _ in miembros_tabulares(ruta) if tabla_de(m) == tabla]
    if len(cands) != 1:
        raise KeyError(f"{pid}: tabla '{tabla}' no identifica un miembro único ({cands})")
    miembro = cands[0]
    fmt = os.path.splitext(miembro.split("!")[-1])[1].lower().lstrip(".")
    if fmt in ("dta", "sav"):
        import pyreadstat
        with tempfile.TemporaryDirectory() as d:
            f, cierra = _abre_miembro(ruta, miembro)
            p = os.path.join(d, "m." + fmt)
            with open(p, "wb") as o:
                while True:
                    b = f.read(1 << 22)
                    if not b:
                        break
                    o.write(b)
            f.close()
            for c in cierra:
                c.close()
            lector = pyreadstat.read_dta if fmt == "dta" else pyreadstat.read_sav
            df, _ = lector(p, usecols=columnas, disable_datetime_conversion=True)
        return pa.Table.from_pandas(df, preserve_index=False)
    f, cierra = _abre_miembro(ruta, miembro)
    flujo = io.BufferedReader(_Hasheador(f), buffer_size=1 << 22)
    try:
        if fmt == "csv":
            enc, delim, nombres = _cabecera_csv(ruta, miembro)
            gen = _lotes_csv(flujo, enc, delim, nombres)
        else:
            gen = _lotes_dbf(flujo)
            next(gen)
        lotes = []
        for lote in gen:
            lote = lote.rename_columns([n.strip() for n in lote.schema.names])
            lotes.append(lote.select(columnas) if columnas else lote)
        return pa.Table.from_batches(lotes)
    finally:
        flujo.close()
        for c in cierra:
            c.close()


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def compacta_verificacion() -> None:
    """Deja una fila por (id, miembro): la última. Un ERROR transitorio (disco
    lleno) que un reintento resolvió no debe quedar como estado."""
    filas = _lee_tsv(_verificacion())
    if not filas:
        return
    ult = {}
    for r in filas:
        ult[(r["id"], r["miembro"])] = r
    tmp = _verificacion().with_suffix(".tsv.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\t".join(COLS_VERIFICACION) + "\n")
        for (pid, m) in sorted(ult):
            f.write("\t".join(ult[(pid, m)].get(c, "") for c in COLS_VERIFICACION) + "\n")
    os.replace(tmp, _verificacion())


def _cmd_verifica(ids):
    malos = 0
    filas = [r for r in _lee_tsv(_constancias()) if not ids or r["id"] in ids]
    for r in filas:
        p = ruta_parquet(r["id"], tabla_de(r["miembro"]))
        sha = sha256_archivo(p) if p.exists() else "AUSENTE"
        ok = sha == r["sha256_parquet"]
        malos += not ok
        print(f"{'OK' if ok else 'DISCORDANTE'}\t{r['id']}\t{r['miembro']}\t{sha}")
    print(f"VERIFICA · {len(filas)} constancias examinadas · {malos} discordantes")
    return 1 if malos else 0


# P4 · medida de carga: la función de carga del medidor SELLADO, importada sin
# modificarla, contra cargar() con proyección. Un proceso por medida.
P4_CALC = "CALC-PISOS-ENCIG2023-EJES-0002"
P4_ID = "encig23_base_datos_csv"
P4_ESCENARIOS = {
    # S1: exactamente lo que carga medir() de P4_CALC (spec.yaml `variables`)
    "S1": [("encig2023_04_sec_7.csv", ["N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS", "ID_PER"]),
           ("encig2023_02_residentes_sec_2.csv", ["ID_PER", "SEXO", "EDAD", "NIV"])],
    # S2: el mismo patrón de carga sobre el miembro más grande del payload
    "S2": [("encig2023_05_sec_8.csv", ["ID_TRA", "P8_4"])],
}


def mide_carga(modo: str, escenario: str) -> dict:
    import resource
    import time
    t0 = time.perf_counter()
    filas = []
    if modo == "csv":
        ruta_med = REPO / "data" / "corrida0" / P4_CALC / "medidor.py"
        spec = importlib.util.spec_from_file_location("_p4_medidor_sellado", ruta_med)
        med = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(med)
        zipp = ruta_payload(P4_ID)
        for miembro, cols in P4_ESCENARIOS[escenario]:
            filas.append(len(med._csv(zipp, miembro, cols)))
        extra = {"medidor_sha256": sha256_archivo(ruta_med)}
    else:
        for miembro, cols in P4_ESCENARIOS[escenario]:
            df = cargar(P4_ID, tabla_de(miembro), cols)
            filas.append(len(df))
        extra = {"fuente": df.attrs.get("fuente", "")}
    seg = time.perf_counter() - t0
    pico_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {"modo": modo, "escenario": escenario, "filas": filas, "segundos": round(seg, 3),
            "pico_rss_mb": round(pico_kb / 1024, 1), **extra}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("universo", help="P1: deriva data/cache/universo-p1.tsv")
    c = sub.add_parser("convierte", help="P2: convierte ids (o --todos los SE-CONVIERTE)")
    c.add_argument("ids", nargs="*")
    c.add_argument("--todos", action="store_true")
    c.add_argument("--tmpdir")
    v = sub.add_parser("verifica", help="sha256 de cada Parquet contra su constancia")
    v.add_argument("ids", nargs="*")
    m = sub.add_parser("mide-carga", help="P4: pico de memoria y tiempo de una carga (un proceso)")
    m.add_argument("--modo", choices=["csv", "parquet"], required=True)
    m.add_argument("--escenario", choices=sorted(P4_ESCENARIOS), required=True)
    a = ap.parse_args(argv)
    if a.cmd == "mide-carga":
        print(json.dumps(mide_carga(a.modo, a.escenario), ensure_ascii=False))
        return 0
    if a.cmd == "universo":
        filas = universo()
        from collections import Counter
        cnt = Counter(f["decision"] + " " + f["motivo"].split(" (")[0] for f in filas)
        for k, n in sorted(cnt.items()):
            print(f"{n}\t{k}")
        print(f"UNIVERSO · {len(filas)} ids -> {UNIVERSO.relative_to(REPO)}")
        return 0
    if a.cmd == "verifica":
        return _cmd_verifica(set(a.ids))
    ids = list(a.ids)
    if a.todos:
        ids += [r["id"] for r in _lee_tsv(UNIVERSO) if r["decision"] == "SE-CONVIERTE"]
    rc = 0
    # temporales (DTA/SAV extraídos, hasta GB) en disco junto a la caché, nunca en /tmp (tmpfs)
    tmpdir = a.tmpdir or str(raiz_cache() / ".tmp")
    os.makedirs(tmpdir, exist_ok=True)
    try:
        for pid in dict.fromkeys(ids):
            print(f"== {pid}", flush=True)
            r = convierte(pid, tmpdir, log=lambda s: print(s, flush=True))
            print(f"RESUMEN {json.dumps(r, ensure_ascii=False)}", flush=True)
            rc |= r["estado"] not in ("OK",)
    finally:
        compacta_verificacion()
    return rc


if __name__ == "__main__":
    sys.exit(main())
