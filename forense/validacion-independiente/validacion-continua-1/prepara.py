#!/usr/bin/env python3
"""ACTO GEN2-VALIDACION-Y-2027-1 · P1 · arma un paquete de validación ciega (C1, opción A)
desde su configuración `paquetes/<paq>.json`, sin abrir ningún valor sellado.

Por paquete:
  <REC>/<paq>/paquete/   docs/ (spec humana + documentación no numérica) · datos/ (miembros
                         autorizados, extraídos byte a byte sin parsear) · esquema-identidades.tsv
                         (llave, unidad y descriptores del catálogo v1.3; ningún valor) ·
                         CONTRATO-v3.md · FIRMAS-Y-ACCESO.md
  <REC>/<paq>/salida/    vacío
  <repo>/…/validacion-continua-1/<paq>/entrada/<paq>--{allowlist.json, allowlist.canon.sha256,
                         identidad.json, prompt.md, FIRMAS-Y-ACCESO.md}

Tolerancia: la sellada en el spec.yaml de cada CALC (flotante abs 1e-10); su traducción v2 es
`catalogo-1-lote3/endireh-pisos-2016-pareja-fisica-0002/entrada/tolerancia-v2.json` (mismos bytes).
Uso: prepara.py <REC> <paq> [<paq> ...]
"""
import csv
import hashlib
import io
import json
import shutil
import sys
import zipfile
from pathlib import Path

import yaml

try:  # CCPV 2010: miembros deflate64 (entidades 15 y 20); zipfile solo no los abre
    import zipfile_deflate64  # noqa: F401
except ImportError:
    pass

SITE = Path.home() / ".local/lib/python3.14/site-packages"
LECTORES = ("pyreadstat", "dbfread", "narwhals")  # bibliotecas de lectura de terceros, no método

R = Path(__file__).resolve().parents[3]
AQUI = Path(__file__).resolve().parent
CONTRATO = R / "forense/validacion-independiente/catalogo-1-ejecutor-v3/CONTRATO-v3.md"
CONTRATO_SHA = "821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb"
CAT = R / "canon/catalogo-del-mexicano-v1_3.tsv"
DESCRIPTORES = ["llave", "unidad", "instrumento", "ola", "conducta", "eje", "segmento", "dominio"]
FIRMA_P1 = ("«Adelante, sigue corriendo el encargo, lo quiero completo, cualquier cosa de firmas o settings "
            "lo ajustamos» (mesa, chat del acto, 28/sep/2026), sobre la pregunta «Tomo tu mensaje como firma de "
            "mesa del acceso C1 para los 14 paquetes de P1 (olas abiertas)», sin objeción. Texto por paquete: "
            "«Autorizo el acceso C1 del paquete {calc}: lectura por la reconstructora sin historial de los inputs "
            "DATO de su spec.yaml, solo las columnas que nombre su spec humana, con los cuatro gates y la receta de "
            "LANZAMIENTO-LOTE3. No adopta cifras.»")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


_SHA = {}


def copia(src, miembro, destino, sha_esperado=None):
    s = R / src
    if sha_esperado:
        if s not in _SHA:
            _SHA[s] = sha(s)
        if _SHA[s] != sha_esperado:
            raise SystemExit(f"PARO · sha discorda: {src}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not miembro:
        shutil.copyfile(s, destino)
        return
    # «a.zip!b.dbf»: zips anidados (ENSU); cada nivel se abre en memoria, sin parsear el miembro final
    niveles = miembro.split("!")
    z = zipfile.ZipFile(s)
    for m in niveles[:-1]:
        z = zipfile.ZipFile(io.BytesIO(z.read(m)))
    with z.open(niveles[-1]) as a, open(destino, "wb") as b:
        shutil.copyfileobj(a, b)


def esquema(calc, destino):
    n = 0
    with open(CAT, encoding="utf-8", newline="") as fh, open(destino, "w", encoding="utf-8") as out:
        out.write("\t".join(DESCRIPTORES) + "\n")
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["calc"] == calc:
                out.write("\t".join(r[c].replace("\t", " ") for c in DESCRIPTORES) + "\n")
                n += 1
    return n


def firmas(calc, spec_md, spec_sha):
    return f"""# Registro de firmas y acceso · {calc}

Fecha de todas las firmas: 28/sep/2026.

| FP | Objeto | sha256 del objeto | Texto de firma (verbatim) |
|---|---|---|---|
| FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01 (R31) | `CONTRATO-v3.md` | `{CONTRATO_SHA}` | «Mesa firma CONTRATO-v3.md con sha256 {CONTRATO_SHA} como contrato de estados de C1. Esta firma no acredita contexto nuevo ni autoriza acceso: cualquier C1 real exige además CONTEXTO-NUEVO-ACREDITADO y ACCESO-AUTORIZADO por paquete. Una corrección material se hace en una versión sucesora con sello nuevo.» |
| FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01 (R23) | protocolo inferencial de C1 | — | «Apruebo el protocolo como contrato DIAGNÓSTICO de reproducción de IC para intentos futuros; no es estimador de IC adoptable ni recertifica IC históricos.» |
| FP-260928-GEN2-VALIDACION-Y-2027-1-f926-01 | acceso C1 al paquete | spec humana `{spec_md}` `{spec_sha}` | {FIRMA_P1.format(calc=calc)} |
"""


def prompt(paq, cfg, ident, n):
    campos = "\n".join(f"- `{m}`: {', '.join(f'`{c}`' for c in cs)}." for m, cs in cfg["campos"].items())
    filtro = f"\nFiltro de filas que pide la spec: {cfg['filtro_filas']}.\n" if cfg.get("filtro_filas") else ""
    return f"""Eres una sesión de reconstrucción independiente. No tienes historial ni memoria, y no debes buscarlos. Tu único insumo es el directorio `./paquete/`, de solo lectura. Escribes únicamente en `./salida/`.

## Objetivo

Recalcula el punto y, donde la spec lo defina, el IC95 de cada una de las {n} llaves de `paquete/esquema-identidades.tsv`. Implementa tú mismo el método de la spec humana `paquete/docs/spec-humana.md`, apoyándote en la documentación de `paquete/docs/`, en Python 3 (numpy, pandas). Para leer `.sav` o `.dbf` tienes `pyreadstat` y `dbfread` en `paquete/lib/` (`sys.path.insert(0, "paquete/lib")`); son lectores de terceros, sin método del programa. `.dta` se lee con `pandas.read_stata`. La spec menciona funciones de un código previo: no existe en el paquete, no debes buscarlo, y su comportamiento solo vale en la medida en que la spec lo describe en prosa. Las columnas `conducta`, `eje`, `segmento` y `ola` del esquema dicen qué estima cada llave.

- Formato de salida: `CONTRATO-v3.md` (`version` = 3).
- `FIRMAS-Y-ACCESO.md` registra qué firmó mesa y el alcance de tu acceso.

## Límites de acceso (autorización delimitada)

Del microdato puedes leer la fila de encabezados (o la lista de variables) completa, y de las filas solo estas columnas; en pandas usa `usecols` / `columns`:
{campos}
{filtro}
Si el método exige una columna que no está en esta lista, no la leas: marca las llaves afectadas con `BLOQUEADO-POR-ACCESO` y escribe el `motivo`. No imprimas filas de microdato; conteos y agregados sí. No uses la red ni leas nada fuera de `./paquete/`.

## Qué entregar en `./salida/`

1. `salida/resultado.json`: exactamente el documento de `CONTRATO-v3.md`; `version` = 3; `identidad` = `{json.dumps(ident, ensure_ascii=False)}`; una fila por llave del esquema, con `llave` y `unidad` literales. Con estimación: `estado: "RECONSTRUIDO"`, `punto` y `estado_ic` explícito (`CALCULADO` con `ic95_inf`/`ic95_sup`, `SIN-IC` si la spec no define IC para esa llave, o `NO-IDENTIFICADA` con `motivo_ic`). Sin estimación: el estado del contrato que corresponda, con `motivo`. Números como strings `repr(float(x))`, sin redondear. No suprimas celdas por publicabilidad.
2. `salida/diagnostico.json`: por llave, n válido y exclusiones por causa; y las decisiones de implementación que tomaste donde la spec admitía más de una lectura, cada una con la frase que la motiva.
3. `salida/codigo/`: todo tu código; `python3 salida/codigo/reconstruye.py`, desde el directorio de trabajo, regenera los archivos 1–2 desde `paquete/`.
4. `salida/entorno.txt`: versiones de python, numpy, pandas y de cualquier lector usado, y `uname -a`.
5. `salida/archivos-leidos.txt`: cada ruta que abriste, una por línea.
6. `salida/insuficiencias.md`: lo que la spec humana no alcanzó a fijar, por llave o grupo; «Ninguna.» si nada.

## Reglas

- Si falta método, acceso o un dato, informa el faltante sin adivinar (`NO-RECALCULABLE-DESDE-SPEC` con `motivo`).
- El primer resultado completo que produzca tu código es el que se entrega. No tienes valores esperados y no debes buscarlos.
- Trabaja por lotes si el esquema es grande; no dejes llaves sin fila.
- Al terminar, escribe el sha256 de cada archivo de `salida/` en `salida/SELLO.txt` y no modifiques nada después.
- La última línea de tu respuesta final es `RECONSTRUCCION-TERMINADA sha256(resultado.json)=<hex>`.
"""


def prepara(REC, paq):
    cfg = json.loads((AQUI / "paquetes" / f"{paq}.json").read_text(encoding="utf-8"))
    calc = cfg["calc"]
    y = yaml.safe_load(open(R / "data/corrida0" / calc / "spec.yaml", encoding="utf-8"))
    base = REC / paq
    if base.exists():
        raise SystemExit(f"PARO · ya existe {base}: no se sobrescribe")
    pk = base / "paquete"
    pk.mkdir(parents=True)
    (base / "salida").mkdir()
    for d in cfg["docs"]:
        copia(d["src"], d.get("miembro"), pk / d["dst"])
    spec_md = (R / "data/corrida0" / calc / y["spec_md"]).resolve()
    if sha(pk / "docs/spec-humana.md") != y["spec_md_sha256"]:
        raise SystemExit(f"PARO · docs/spec-humana.md no casa con spec_md_sha256 de {calc}")
    shas_dato = {i["sha256"] for i in y["inputs"] if i.get("funcion") == "DATO"}
    for d in cfg["datos"]:
        if d["sha256"] not in shas_dato:
            raise SystemExit(f"PARO · {d['src']} no es input DATO de {calc}")
        copia(d["src"], d.get("miembro"), pk / d["dst"], d["sha256"])
    faltan = set(cfg["campos"]) - {d["dst"] for d in cfg["datos"]}
    if faltan:
        raise SystemExit(f"PARO · campos sin archivo: {faltan}")
    n = esquema(calc, pk / "esquema-identidades.tsv")
    if n == 0:
        raise SystemExit(f"PARO · {calc} sin llaves en el catálogo v1.3")
    for lib in LECTORES:
        shutil.copytree(SITE / lib, pk / "lib" / lib, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copyfile(CONTRATO, pk / "CONTRATO-v3.md")
    if sha(pk / "CONTRATO-v3.md") != CONTRATO_SHA:
        raise SystemExit("PARO · sha de CONTRATO-v3.md")
    (pk / "FIRMAS-Y-ACCESO.md").write_text(firmas(calc, spec_md.relative_to(R), y["spec_md_sha256"]), encoding="utf-8")
    files = sorted(p for p in pk.rglob("*") if p.is_file())
    entrada = [{"path": str(p.relative_to(base)), "sha256": sha(p)} for p in files]
    ident = {"paquete": paq, "version_entrada": "validacion-continua-1",
             "sha256_entrada": hashlib.sha256(json.dumps(entrada, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}
    allow = {"paquete": paq, "calc": calc, "identidad": ident, "fuente_datos": cfg["datos"],
             "campos_autorizados": cfg["campos"], "filtro_filas": cfg.get("filtro_filas"),
             "herramientas": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"],
             "autorizacion": ["FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01", "FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02",
                              "FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-03", "FP-260928-GEN2-VALIDACION-Y-2027-1-f926-01"],
             "tolerancia_sellada": y["tolerancia"], "input_files": entrada}
    canon = json.dumps(allow, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    ent = AQUI / paq / "entrada"
    ent.mkdir(parents=True, exist_ok=True)
    (ent / f"{paq}--allowlist.json").write_text(json.dumps(allow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ent / f"{paq}--allowlist.canon.sha256").write_text(hashlib.sha256(canon.encode()).hexdigest() + "\n")
    (ent / f"{paq}--identidad.json").write_text(json.dumps(ident, ensure_ascii=False, sort_keys=True) + "\n")
    shutil.copyfile(pk / "FIRMAS-Y-ACCESO.md", ent / f"{paq}--FIRMAS-Y-ACCESO.md")
    pr = prompt(paq, cfg, ident, n)
    (ent / f"{paq}--prompt.md").write_text(pr, encoding="utf-8")
    (REC / f"{paq}.prompt").write_text(pr, encoding="utf-8")
    for p in pk.rglob("*"):
        p.chmod(0o555 if p.is_dir() else 0o444)
    pk.chmod(0o555)
    print(paq, n, "llaves ·", len(files), "archivos · entrada", ident["sha256_entrada"][:12])


if __name__ == "__main__":
    REC = Path(sys.argv[1])
    for paq in sys.argv[2:]:
        prepara(REC, paq)
