#!/usr/bin/env python3
"""Falsadores de los pisos históricos de crédito
(ACTO GEN2-DIN-CREDITO-HISTORIA-1, P2): CALC-DIN-CREDITO-PISOS-ENIF2018-0001,
-ENIF2015-0001 y -ENIF2012-0001, un solo medidor byte a byte.

Tres bloques:

1. **Sintético (D-22), por ola.** Fabrica el payload con la FORMA de cada
   ola (CSV 2018 con columnas en minúsculas; pares DBF 2015 y 2012 con la
   cabecera real de campos) y corre `medir()` con los inputs REALES del repo
   (medidor sellado de -0003, tablas de identidad, tabla de comparabilidad
   v1.1, mapa de prerregistro). Prueba: las conductas emitidas son las que
   la tabla permite (K4/K7 no salen en 2015/2012; K7 no sale en 2018);
   2015/2012 no emiten formalidad; cada celda trae `-SOPORTE`; coherencia por
   eje cierra; K6-PR cuenta productos; toda conducta lleva `-MATIZ` y
   `-VEREDICTO-TEXTO`; el medidor PARA si la tabla dice CAMBIO-DE-INSTRUMENTO
   para una conducta que el mapa trae, y si el mapa no trae una conducta
   positiva. Los tres medidores son idénticos por bytes y cada spec.yaml
   declara exactamente los ids que el sintético produce.
2. **Oro (encargo §5 P2)** — sólo con corpus y `--oro`: el mismo punto de
   entrada con `ola = 2021` reproduce los 2 939 RESULT de #943 (tolerancia
   1e-10 en flotantes, exactos en enteros y texto), con los diagnósticos
   traducidos por rol (`TRADUCCION_2021`). El resultado se asienta en
   `forense/prereg-caja/DIN-CREDITO-PISOS-HISTORIA-oro-2021.json`.
3. **Sellado.** Si `resultados.json` existe en un CALC: su tabla de
   identidad coincide uno a uno con los `-P` por eje.

Corre standalone (`python3 tests/test_din_credito_pisos_historia.py [--oro]`)
y expone `corre()`.
"""
from __future__ import annotations

import hashlib
import io
import json
import struct
import sys
import tempfile
import types
import zipfile
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
CALCS = {ola: ROOT / f"data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF{ola}-0001" for ola in ("2018", "2015", "2012")}
CALC_ORO = ROOT / "data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF2021-0001"
SPEC_MD = ROOT / "forense/prereg-caja/DIN-CREDITO-PISOS-HISTORIA-spec-v1_0.md"
MAPA = ROOT / "forense/prereg-caja/DIN-CREDITO-PISOS-HISTORIA-mapa-v1_0.tsv"
ORO_JSON = ROOT / "forense/prereg-caja/DIN-CREDITO-PISOS-HISTORIA-oro-2021.json"
REPS = 120
CONDUCTAS_ESPERADAS = {
    "2018": 14,   # K1, K2×3, K3, K4×5, K5×2, K6×2
    "2015": 9,    # K1, K2×3, K3, K5×2, K6×2
    "2012": 9,
}
CELDAS = {"2018": 18, "2015": 15, "2012": 15}
# diagnósticos de #943 (nombres por variable) -> nombres por rol del medidor genérico
TRADUCCION_2021 = {
    "P6-2-INDEFINIDO-N": "TENENCIA-INDEFINIDO-N",
    "P6-15-FUERA-DE-CATALOGO-N": "K4-MOTIVO-FUERA-DE-CATALOGO-N",
    "P6-15-FUERA-DE-BASE-N": "K4-MOTIVO-FUERA-DE-BASE-N",
    "P6-17-FUERA-DE-CATALOGO-N": "K5-FUERA-DE-CATALOGO-N",
    "P6-7-NO-SABE-N": "K7-NO-SABE-N",
    "P6-7-BLANCO-EN-TENEDORES-N": "K7-BLANCO-EN-TENEDORES-N",
    "P6-7-FUERA-DE-BASE-N": "K7-FUERA-DE-BASE-N",
    "P6-4-NO-SABE-NO-RESPONDE-N": "K6-ATRASO-NO-SABE-NO-RESPONDE-N",
    "P6-4-BLANCO-EN-PRODUCTO-TENIDO-N": "K6-ATRASO-BLANCO-EN-PRODUCTO-TENIDO-N",
    "FORMALIDAD-EXCLUIDOS-P3-10-NO-SABE": "FORMALIDAD-EXCLUIDOS-NO-SABE",
    "FORMALIDAD-EXCLUIDOS-P3-10-BLANCO": "FORMALIDAD-EXCLUIDOS-BLANCO",
}


def _modulo(calc: Path):
    src = (calc / "medidor.py").read_bytes()
    mod = types.ModuleType("medidor_din_credito_historia")
    exec(compile(src, str(calc / "medidor.py"), "exec"), mod.__dict__)
    return mod


def _inputs_repo(spec: dict) -> dict:
    out = {}
    for ent in spec["inputs"]:
        if ent.get("origen") == "repo":
            p = ROOT / ent["ruta"]
            out[ent["id"]] = {"ruta_absoluta": str(p), "bytes": p.read_bytes()}
    return out


# ------------------------------------------------------------- sintéticos
def _dbf(campos: list[tuple[str, int]], filas: list[list[str]]) -> bytes:
    """DBF mínimo (dBase III): cabecera + descriptores C de ancho fijo."""
    r_len = 1 + sum(w for _, w in campos)
    h_len = 32 + 32 * len(campos) + 1
    head = bytearray(struct.pack("<BBBBIHH", 0x03, 24, 1, 1, len(filas), h_len, r_len)) + bytes(20)
    for nombre, w in campos:
        head += nombre.encode("ascii").ljust(11, b"\0") + b"C" + bytes(4) + bytes([w, 0]) + bytes(14)
    head += b"\x0d"
    body = bytearray()
    for f in filas:
        body += b" "
        for (nombre, w), v in zip(campos, f):
            body += v.encode("latin-1").ljust(w)[:w]
    return bytes(head) + bytes(body) + b"\x1a"


def _base(rng, n):
    """Columnas comunes inventadas por persona (diseño, ejes)."""
    filas = []
    for i in range(n):
        est = 1 + i % 12
        upm = est * 10 + int(rng.integers(0, 4))
        filas.append({
            "est": f"{est:03d}", "upm": f"{upm:05d}", "w": str(int(rng.integers(500, 5000))),
            "sexo": str(int(rng.integers(1, 3))), "edad": str(int(rng.integers(18, 71))),
            "tloc": str(int(rng.integers(1, 5))), "niv": f"{int(rng.integers(0, 10)):02d}",
        })
    return filas


def _credito(rng, k_items, atr_codes):
    """Filtro + batería + atraso con los saltos del cuestionario."""
    filtro = rng.random() < 0.38
    prod = ["1" if (filtro and rng.random() < p) else ("2" if filtro else "")
            for p in (0.20, 0.12, 0.06, 0.08, 0.02, 0.05, 0.02, 0.01)[:k_items]]
    if filtro and "1" not in prod and rng.random() < 0.9:
        prod[int(rng.integers(0, k_items))] = "1"
    atr = ["" if pk != "1" else str(rng.choice(atr_codes[0], p=atr_codes[1])) for pk in prod]
    return filtro, prod, atr


def payload_2018(n=2400, semilla=7) -> bytes:
    rng = np.random.default_rng(semilla)
    cols = (["upm", "viv_sel", "hogar", "n_ren", "sexo", "edad", "tloc", "niv", "p3_11", "p5_4", "p5_5",
             "p6_1_1", "p6_1_2", "p6_1_3", "p6_1_4", "p6_1_5", "p6_3", "p6_4", "p6_5", "p6_6"]
            + [f"p6_8_{k}" for k in range(1, 9)] + [f"p6_10_{k}" for k in range(1, 8)]
            + ["p6_18", "est_dis", "upm_dis", "fac_per", "relleno"])
    filas = []
    for b in _base(rng, n):
        filtro, prod, atr = _credito(rng, 8, (["1", "2", "8", "9"], [.25, .69, .03, .03]))
        p63 = "1" if (filtro and rng.random() < .85) else "2"
        p64 = "1" if (filtro and p63 == "2") else ("" if p63 == "1" else "2")
        p65 = "" if filtro else str(rng.choice(["1", "2"], p=[.3, .7]))
        p66 = str(int(rng.integers(1, 9))) if (not filtro and p65 == "2") else ""
        inf = [str(rng.choice(["1", "2"], p=[q, 1 - q])) for q in (.05, .04, .15, .2, .01)]
        p54 = str(rng.choice(["1", "2"], p=[.45, .55]))
        p55 = "" if p54 == "1" else str(rng.choice(["1", "2"], p=[.2, .8]))
        trabaja = rng.random() < 0.65
        p311 = str(rng.choice(list("1234569"), p=[.35, .05, .02, .03, .02, .5, .03])) if trabaja else ""
        filas.append([b["upm"], "01", "01", "01", b["sexo"], b["edad"], b["tloc"], b["niv"], p311, p54, p55]
                     + inf + [p63, p64, p65, p66] + prod + atr[:7]
                     + [str(rng.choice(["1", "2", "3"], p=[.12, .38, .5])), b["est"], b["upm"], b["w"], "x"])
    csv = ",".join(cols) + "\n" + "\n".join(",".join(f) for f in filas) + "\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("conjunto_de_datos_tmodulo_enif_2018/conjunto_de_datos/tmodulo.csv", csv.encode("utf-8"))
        zf.writestr("conjunto_de_datos_tmodulo2_enif_2018/conjunto_de_datos/conjunto_de_datos_tmodulo2_enif_2018.csv", "x\n")
    return buf.getvalue()


def payload_2015(n=2400, semilla=7) -> bytes:
    rng = np.random.default_rng(semilla)
    c1 = [("UPM", 7), ("VIV_SEL", 2), ("HOGAR", 2), ("R_SEL", 2), ("NIV", 1), ("P5_4", 1),
          ("P6_1_1", 1), ("P6_1_2", 1), ("P6_1_3", 1), ("P6_1_4", 1), ("P6_1_5", 1), ("P6_4", 1), ("P6_5", 1),
          ("TLOC", 1), ("EST_DIS", 3), ("UPM_DIS", 5), ("SEXO", 1), ("EDAD", 2), ("FAC_PER", 5)]
    c2 = ([("UPM", 7), ("VIV_SEL", 2), ("HOGAR", 2), ("R_SEL", 2)] + [(f"P6_9_{k}", 1) for k in range(1, 9)]
          + [(f"P6_13_{k}", 1) for k in range(1, 9)] + [("P6_20", 1)])
    f1, f2 = [], []
    for i, b in enumerate(_base(rng, n)):
        filtro, prod, atr = _credito(rng, 8, (["1", "2", "3", "8", "9"], [.15, .08, .71, .03, .03]))
        p64 = "1" if filtro else "2"
        p65 = "" if filtro else str(rng.choice(["1", "2"], p=[.3, .7]))
        inf = [str(rng.choice(["1", "2"], p=[q, 1 - q])) for q in (.2, .15, .05, .04, .01)]
        llave = [f"{i:07d}", "01", "01", "01"]
        f1.append(llave + [b["niv"][-1], str(rng.choice(["1", "2"], p=[.44, .56]))] + inf
                  + [p64, p65, b["tloc"], b["est"], b["upm"], b["sexo"], b["edad"], b["w"].zfill(5)])
        f2.append(llave + prod + atr + [str(rng.choice(["1", "2", "3"], p=[.12, .38, .5]))])
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("tmodulo1.DBF", _dbf(c1, f1))
        zf.writestr("tmodulo2.DBF", _dbf(c2, f2))
        zf.writestr("tsdem.DBF", _dbf([("UPM", 7)], []))
    return buf.getvalue()


def payload_2012(n=2400, semilla=7) -> bytes:
    rng = np.random.default_rng(semilla)
    c1 = ([("CONTROL", 6), ("VIV_SEL", 2), ("HOGAR", 1), ("N_INF", 2), ("R_SEL", 2), ("NIV", 2), ("P5_3", 1),
           ("P6_1_1", 1), ("P6_1_2", 1), ("P6_1_3", 1), ("P6_1_4", 1), ("P6_1_5", 1), ("P6_4", 1)]
          + [(f"P6_6_{k}", 1) for k in range(1, 9)] + [(f"P6_11_{k}", 1) for k in range(1, 9)]
          + [("P6_17", 1), ("TL", 1), ("EST_DIS", 2), ("UPM_DIS", 5), ("FAC_PER", 10)])
    cs = [("CONTROL", 6), ("VIV_SEL", 2), ("HOGAR", 1), ("N_REN", 2), ("SEXO", 1), ("EDAD", 2)]
    f1, fs = [], []
    for i, b in enumerate(_base(rng, n)):
        filtro, prod, atr = _credito(rng, 8, (["1", "2", "3", "8", "9"], [.15, .08, .71, .03, .03]))
        inf = [str(rng.choice(["1", "2"], p=[q, 1 - q])) for q in (.03, .05, .15, .2, .01)]
        llave = [f"{i:06d}", "01", "1"]
        f1.append(llave + ["01", "02", b["niv"], str(rng.choice(["1", "2"], p=[.35, .65]))] + inf
                  + ["1" if filtro else "2"] + prod + atr
                  + [str(rng.choice(["1", "2", "3"], p=[.12, .38, .5])), b["tloc"], b["est"][-2:], b["upm"],
                     b["w"].rjust(10)])
        if i % 50 != 7:                      # una de cada 50 sin pareja en TSDEM
            fs.append(llave + ["02", b["sexo"], b["edad"]])
        fs.append(llave + ["01", "1", "40"])  # el informante, otro renglón
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("stmodulo1_e2.dbf", _dbf(c1, f1))
        zf.writestr("stsdem_e2.dbf", _dbf(cs, fs))
    return buf.getvalue()


PAYLOADS = {"2018": ("enif2018_csv", payload_2018),
            "2015": ("enif_2015_enif_2015_bd_dbf", payload_2015),
            "2012": ("enif_2012_bases_enif2012_dbf", payload_2012)}


def _corre_sintetico(ola: str, errores: list[str]):
    calc = CALCS[ola]
    spec = yaml.safe_load((calc / "spec.yaml").read_text(encoding="utf-8"))
    mod = _modulo(calc)
    inputs = _inputs_repo(spec)
    pid, fabrica = PAYLOADS[ola]
    with tempfile.TemporaryDirectory() as td:
        z = Path(td) / f"enif{ola}_sintetico.zip"
        z.write_bytes(fabrica())
        inputs[pid] = {"ruta_absoluta": str(z), "bytes": None}
        contrato = {"parametros": {"bootstrap_replicas": REPS, "ola": ola}, "seed": {"valor": 42}}
        try:
            out = mod.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"{ola}: medir() sobre el sintético reventó: {exc!r}")
            return None, mod, spec
        # PARA si la tabla degrada una conducta que el mapa trae
        txt = inputs["CREDITO-COMPARABILIDAD-TEXTO"]["bytes"].decode("utf-8")
        lineas = txt.split("\n")
        cab = lineas[0].split("\t")
        ik, io_, iv = cab.index("conducta"), cab.index("ola"), cab.index("veredicto")
        rota = []
        for l in lineas:
            c = l.split("\t")
            if len(c) == len(cab) and c[ik] == "K5" and c[io_] == ola:
                c[iv] = "CAMBIO-DE-INSTRUMENTO"
            rota.append("\t".join(c))
        r = dict(inputs); r["CREDITO-COMPARABILIDAD-TEXTO"] = {"ruta_absoluta": "", "bytes": "\n".join(rota).encode("utf-8")}
        try:
            mod.medir(r, contrato)
            errores.append(f"{ola}: el medidor no PARÓ con K5 degradado a CAMBIO-DE-INSTRUMENTO en la tabla")
        except RuntimeError:
            pass
        # PARA si el mapa no trae una conducta positiva
        mtxt = inputs["MAPA"]["bytes"].decode("utf-8")
        mrota = "\n".join(("\t".join(c[:3] + [""] + c[4:]) if (c[0] == ola and c[1] == "k5") else l)
                          for l in mtxt.split("\n") for c in [l.split("\t")])
        r = dict(inputs); r["MAPA"] = {"ruta_absoluta": "", "bytes": mrota.encode("utf-8")}
        try:
            mod.medir(r, contrato)
            errores.append(f"{ola}: el medidor no PARÓ con el mapa sin la variable de K5")
        except RuntimeError:
            pass
    return out, mod, spec


def _falsa_sintetico(ola: str, out: dict, errores: list[str]) -> None:
    pref = f"RESULT-DIN-CREDITO-PISOS-ENIF{ola}"
    unidades = {k[len(pref) + 1:-7]: v for k, v in out.items() if k.startswith(pref) and k.endswith("-UNIDAD")}
    conductas = list(unidades)
    if len(conductas) != CONDUCTAS_ESPERADAS[ola]:
        errores.append(f"{ola}: {len(conductas)} conductas {conductas}, esperaba {CONDUCTAS_ESPERADAS[ola]}")
    if any(c.startswith("K7") for c in conductas):
        errores.append(f"{ola}: emite K7 (NO-ESTIMABLE)")
    if ola != "2018" and any(c.startswith("K4") for c in conductas):
        errores.append(f"{ola}: emite K4 (CAMBIO-DE-INSTRUMENTO)")
    puntos = [k for k in out if k.endswith("-P") and k.startswith(pref)]
    if len(puntos) != len(conductas) * CELDAS[ola]:
        errores.append(f"{ola}: {len(puntos)} celdas -P, esperaba {len(conductas) * CELDAS[ola]}")
    if ola != "2018" and any("-FORMALIDAD-" in k or "-UNIVERSO-" in k for k in puntos):
        errores.append(f"{ola}: emite celdas de formalidad sin eje construible")
    for k in puntos:
        base = k[:-2]
        for s in ("IC-LO", "IC-HI", "N", "DEN-W", "B-VALIDAS", "SOPORTE"):
            if f"{base}-{s}" not in out:
                errores.append(f"{base}-{s} ausente")
        n = out.get(f"{base}-N"); sop = out.get(f"{base}-SOPORTE")
        if isinstance(n, int) and sop not in (("OK",) if n >= 200 else ("BAJO-N-MENOR-200",)):
            errores.append(f"{base}: N={n} pero SOPORTE={sop!r}")
    ejes = ["SEXO", "EDAD", "ESCOLARIDAD", "LOCALIDAD", "CUENTA"] + (["FORMALIDAD"] if ola == "2018" else [])
    for c in conductas:
        for s in ("MATIZ", "VEREDICTO-TEXTO"):
            if not out.get(f"{pref}-{c}-{s}"):
                errores.append(f"{ola}: {c} sin -{s}")
        for e in ejes:
            for s in ("NUM", "DEN"):
                v = out.get(f"{pref}-{c}-COHERENCIA-{e}-DELTA-{s}-W")
                if v is None or abs(v) > 1e-6:
                    errores.append(f"{ola}: {c}×{e}: DELTA-{s}-W={v!r}")
    n_pr = out[f"{pref}-K6-PR-NACIONAL-TODOS-N"]; n_pt = out[f"{pref}-K6-P-TENEDORES-NACIONAL-TODOS-N"]
    if not (n_pr > n_pt > 0):
        errores.append(f"{ola}: K6-PR N={n_pr} debería superar a K6-P-TENEDORES N={n_pt}")
    if n_pr > out[f"{pref}-FILAS-PRODUCTO"]:
        errores.append(f"{ola}: K6-PR cuenta más filas que productos tenidos")
    if out[f"{pref}-K1-N-UNIVERSO"] <= out[f"{pref}-TENEDORES-N"]:
        errores.append(f"{ola}: K1 debería medirse sobre tenedores y no tenedores")
    if ola == "2018":
        if out[f"{pref}-K4A-AUTOEXCLUSION-N-UNIVERSO"] > out[f"{pref}-NUNCA-HA-TENIDO-N"]:
            errores.append("2018: K4 fuera de la base «nunca ha tenido»")
        if out[f"{pref}-K6-PRODUCTOS-TENIDOS-SIN-VARIABLE-DE-ATRASO-N"] <= 0:
            errores.append("2018: el ítem «Otro» tenido sin variable de atraso debería contarse")
    if ola == "2012" and out[f"{pref}-FILAS-SIN-SOCIODEMOGRAFICO-N"] <= 0:
        errores.append("2012: el join con TSDEM debería contar filas sin pareja")
    if ola == "2012" and out[f"{pref}-K3-VEREDICTO-TEXTO"] != "CAMBIO-MENOR":
        errores.append("2012: K3 debería entrar como CAMBIO-MENOR (sin caja)")


# ------------------------------------------------------------------- oro
def _oro(errores: list[str]) -> None:
    spec18 = yaml.safe_load((CALCS["2018"] / "spec.yaml").read_text(encoding="utf-8"))
    mod = _modulo(CALCS["2018"])
    inputs = _inputs_repo(spec18)
    z = ROOT / "data/raw/enif2021_csv.zip"
    if not z.exists():
        errores.append("oro: data/raw/enif2021_csv.zip no está montado")
        return
    inputs["enif2021_csv"] = {"ruta_absoluta": str(z), "bytes": None}
    spec21 = yaml.safe_load((CALC_ORO / "spec.yaml").read_text(encoding="utf-8"))
    contrato = {"parametros": {"bootstrap_replicas": int(spec21["parametros"]["bootstrap_replicas"]), "ola": "2021"},
                "seed": {"valor": int(spec21["seed"]["valor"])}}
    out = mod.medir(inputs, contrato)
    res = json.loads((CALC_ORO / "resultados.json").read_text(encoding="utf-8"))["resultados"]
    pref = "RESULT-DIN-CREDITO-PISOS-ENIF2021-"
    faltan, difs, maxd = [], [], 0.0
    for k, v in res.items():
        suf = k[len(pref):]
        kk = pref + TRADUCCION_2021.get(suf, suf)
        if kk not in out:
            faltan.append(k); continue
        o = out[kk]
        if isinstance(v, float) or isinstance(o, float):
            if v is None or o is None:
                if v is not o: difs.append(k)
            else:
                dd = abs(float(v) - float(o)); maxd = max(maxd, dd)
                if dd > 1e-10: difs.append(k)
        elif v != o:
            difs.append(k)
    resumen = {"calc_oro": CALC_ORO.name, "medidor_sha256": hashlib.sha256((CALCS["2018"] / "medidor.py").read_bytes()).hexdigest(),
               "result_en_943": len(res), "comparados": len(res) - len(faltan), "faltantes": faltan,
               "discordantes": difs, "max_abs_diff_flotantes": maxd, "extras_del_generico": sorted(set(out) - {pref + TRADUCCION_2021.get(k[len(pref):], k[len(pref):]) for k in res}),
               "veredicto": "REPRODUCE" if not faltan and not difs else "NO-REPRODUCE"}
    ORO_JSON.write_text(json.dumps(resumen, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if faltan or difs:
        errores.append(f"oro: {len(faltan)} RESULT faltantes, {len(difs)} discordantes (max |Δ|={maxd})")


def _falsa_sellado(ola: str, errores: list[str]) -> None:
    calc = CALCS[ola]
    rj = calc / "resultados.json"
    if not rj.exists():
        return
    res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    pref = f"RESULT-DIN-CREDITO-PISOS-ENIF{ola}"
    tabla = ROOT / f"forense/prereg-caja/DIN-CREDITO-PISOS-ENIF{ola}-metadatos-v1_0.tsv"
    if not tabla.exists():
        errores.append(f"{ola}: CALC sellado sin tabla de identidad {tabla.relative_to(ROOT)}")
        return
    with tabla.open(encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh if l.strip() and not l.startswith("#")]
    cab = lineas[0].split("\t")
    filas = [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]
    ids = {f["cell_id"] for f in filas}
    esperados = {k for k in res if k.startswith(pref) and k.endswith("-P") and "-NACIONAL-" not in k and "-UNIVERSO-" not in k}
    if ids != esperados:
        errores.append(f"{ola}: tabla de identidad: {len(ids - esperados)} sobran, {len(esperados - ids)} faltan")
    for f in filas:
        c = f["outcome"]
        if res.get(f"{pref}-{c}-UNIDAD") is None or not f["unit"].startswith(res[f"{pref}-{c}-UNIDAD"] + " "):
            errores.append(f"{f['cell_id']}: unit {f['unit']!r} vs {res.get(f'{pref}-{c}-UNIDAD')!r}")
        if (f["source_instrument"], f["source_edition"]) != ("ENIF", ola):
            errores.append(f"{f['cell_id']}: ola {f['source_edition']}")
    side = Path(str(tabla) + ".sha256")
    if not side.exists() or side.read_text().split()[0] != hashlib.sha256(tabla.read_bytes()).hexdigest():
        errores.append(f"{ola}: sidecar de la tabla de identidad ausente o discordante")


def corre(oro: bool = False) -> list[str]:
    errores: list[str] = []
    for p in [SPEC_MD, Path(str(SPEC_MD) + ".sha256"), MAPA, Path(str(MAPA) + ".sha256")] + \
             [c / f for c in CALCS.values() for f in ("medidor.py", "spec.yaml")]:
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    sha_md = hashlib.sha256(SPEC_MD.read_bytes()).hexdigest()
    if Path(str(SPEC_MD) + ".sha256").read_text().split()[0] != sha_md:
        errores.append("sidecar .sha256 de la spec humana discordante")
    if Path(str(MAPA) + ".sha256").read_text().split()[0] != hashlib.sha256(MAPA.read_bytes()).hexdigest():
        errores.append("sidecar .sha256 del mapa discordante")
    medidores = {hashlib.sha256((c / "medidor.py").read_bytes()).hexdigest() for c in CALCS.values()}
    if len(medidores) != 1:
        errores.append("los tres medidores no son idénticos por bytes")
    for ola, calc in CALCS.items():
        spec = yaml.safe_load((calc / "spec.yaml").read_text(encoding="utf-8"))
        if spec.get("spec_md_sha256") != sha_md:
            errores.append(f"{ola}: spec_md_sha256 del yaml no coincide con la spec humana")
        if str(spec.get("parametros", {}).get("ola")) != ola:
            errores.append(f"{ola}: parametros.ola = {spec.get('parametros', {}).get('ola')!r}")
        if any("milpa/" in str(e.get("ruta", "")) for e in spec["inputs"]):
            errores.append(f"{ola}: la spec declara un input bajo milpa/")
        mapa_sha = [e for e in spec["inputs"] if e.get("id") == "MAPA"]
        if not mapa_sha or mapa_sha[0].get("sha256") != hashlib.sha256(MAPA.read_bytes()).hexdigest():
            errores.append(f"{ola}: el input MAPA no declara el sha del mapa del árbol")
        out, mod, spec = _corre_sintetico(ola, errores)
        if out is not None:
            _falsa_sintetico(ola, out, errores)
            declarados = {r["id"] for r in spec.get("resultados") or []}
            if declarados != set(out):
                errores.append(f"{ola}: resultados declarados: {len(declarados - set(out))} sobran, {len(set(out) - declarados)} faltan")
        _falsa_sellado(ola, errores)
    if oro:
        _oro(errores)
    return errores


def main() -> int:
    oro = "--oro" in sys.argv
    errores = corre(oro=oro)
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_din_credito_pisos_historia.py (sintético D-22 × 3 olas; medidor único; ids declarados"
              + ("; ORO 2021 REPRODUCE #943" if oro else "") + ")")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
