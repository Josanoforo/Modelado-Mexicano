#!/usr/bin/env python3
"""Falsadores de CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001
(ACTO GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1).

1. **Sintético (D-22).** Fabrica ENIF 2021 (CSV, columnas en mayúsculas),
   2018 (CSV, minúsculas, con los pases 5.4/5.5 → 5.9 → 5.13) y 2015 (DBF)
   y corre `medir()` con los inputs REALES del repo (medidor sellado de
   -0003, medidor histórico de crédito, pisos y R sellados, tabla del
   árbitro, tabla de comparabilidad). Prueba: `corrida0._valida_outputs`
   vacío; las 32 celdas traen IC calibrado y rótulo RETROSPECTIVA-MECÁNICA;
   el control muestral reproduce 6/32; 2015 sólo aparece como DESCRIPTIVO y
   sólo en informal × {sexo, edad, escolaridad, localidad}; el medidor PARA
   si la tabla de comparabilidad cambia un veredicto congelado; los ids del
   spec.yaml son exactamente los que el medidor emite.
2. **Regla a mano.** `calibra()` sobre un caso de dos celdas con números
   escritos a mano reproduce la fórmula de la spec §4 a 1e-12.
3. **Oro** (sólo con corpus y `--oro`): `mide_2021(armonizada=False)` —18+,
   nueve vías— reproduce P, IC-LO, IC-HI y N de los 32 pisos sellados
   (1e-10). No mide la versión 18-70 armonizada.

Corre standalone (`python3 tests/test_enif_persistencia_ic_calibrado.py
[--oro]`) y expone `corre()`.
"""
from __future__ import annotations

import hashlib
import io
import math
import struct
import sys
import tempfile
import types
import zipfile
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001"
SPEC_MD = ROOT / "forense/prereg-caja/ENIF-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md"
REPS = 60
sys.path.insert(0, str(ROOT / "tools"))


def _modulo():
    src = (CALC / "medidor.py").read_bytes()
    mod = types.ModuleType("medidor_enifpic")
    exec(compile(src, str(CALC / "medidor.py"), "exec"), mod.__dict__)
    return mod


def _spec():
    return yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))


def _inputs_repo(spec):
    out = {}
    for ent in spec["inputs"]:
        if ent.get("origen") == "repo":
            p = ROOT / ent["ruta"]
            out[ent["id"]] = {"ruta_absoluta": str(p), "bytes": p.read_bytes()}
    return out


# ------------------------------------------------------------- sintéticos
def _dbf(campos, filas):
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


def _yn(rng, q):
    return "1" if rng.random() < q else "2"


def _persona(rng, i, edad_max):
    est = 1 + i % 12
    return {"est": f"{est:03d}", "upm": f"{est * 10 + int(rng.integers(0, 4)):05d}",
            "w": str(int(rng.integers(500, 5000))), "sexo": str(int(rng.integers(1, 3))),
            "edad": str(int(rng.integers(18, edad_max + 1))), "tloc": str(int(rng.integers(1, 5))),
            "niv": f"{int(rng.integers(0, 10)):02d}"}


def payload_2021(n=2400, semilla=11):
    rng = np.random.default_rng(semilla)
    cols = ([f"P5_1_{i}" for i in range(1, 7)] + [f"P5_4_{i}" for i in range(1, 10)]
            + [f"P5_7_{i}" for i in range(1, 10)]
            + ["SEXO", "EDAD", "TLOC", "P3_1_1", "P3_10", "FAC_ELE", "EST_DIS", "UPM_DIS"])
    filas = []
    for i in range(n):
        b = _persona(rng, i, 96)
        inf = [_yn(rng, q) for q in (.05, .04, .15, .2, .01, .03)]
        acc = [_yn(rng, q) for q in (.3, .05, .1, .15, .02, .01, .01, .08, .02)]
        sav = [_yn(rng, .4) if a == "1" else "" for a in acc]
        p310 = str(rng.choice(list("1234569"), p=[.35, .05, .02, .03, .02, .5, .03])) if rng.random() < .65 else ""
        filas.append(inf + acc + sav + [b["sexo"], b["edad"], b["tloc"], b["niv"], p310, b["w"], b["est"], b["upm"]])
    csv = ",".join(cols) + "\n" + "\n".join(",".join(f) for f in filas) + "\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/conjunto_de_datos_tmodulo_enif_2021.csv",
                    csv.encode("utf-8"))
    return buf.getvalue()


def payload_2018(n=2400, semilla=12):
    rng = np.random.default_rng(semilla)
    cols = ([f"p5_1_{i}" for i in range(1, 7)] + ["p5_4", "p5_5"]
            + [x for k in range(1, 9) for x in (f"p5_9_{k}", f"p5_13_{k}")]
            + ["sexo", "edad", "tloc", "niv", "p3_11", "est_dis", "upm_dis", "fac_per", "relleno"])
    filas = []
    for i in range(n):
        b = _persona(rng, i, 70)
        inf = [_yn(rng, q) for q in (.05, .04, .15, .2, .01, .03)]
        p54 = _yn(rng, .4)
        p55 = "" if p54 == "1" else _yn(rng, .2)
        filtro = p54 == "1" or p55 == "1"
        bat = []
        for k in range(8):
            a = _yn(rng, (.5, .05, .2, .2, .02, .01, .01, .02)[k]) if filtro else ""
            s = (_yn(rng, .4) if a == "1" else "") if filtro else ""
            bat += [a, s]
        p311 = str(rng.choice(list("1234569"), p=[.35, .05, .02, .03, .02, .5, .03])) if rng.random() < .65 else ""
        filas.append(inf + [p54, p55] + bat + [b["sexo"], b["edad"], b["tloc"], b["niv"], p311,
                                               b["est"], b["upm"], b["w"], "x"])
    csv = ",".join(cols) + "\n" + "\n".join(",".join(f) for f in filas) + "\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("conjunto_de_datos_tmodulo_enif_2018/conjunto_de_datos/tmodulo.csv", csv.encode("utf-8"))
        zf.writestr("conjunto_de_datos_tmodulo2_enif_2018/conjunto_de_datos/conjunto_de_datos_tmodulo2_enif_2018.csv", "x\n")
    return buf.getvalue()


def payload_2015(n=2400, semilla=13):
    rng = np.random.default_rng(semilla)
    c1 = ([("UPM", 7), ("NIV", 1)] + [(f"P5_1_{i}", 1) for i in range(1, 7)]
          + [("TLOC", 1), ("EST_DIS", 3), ("UPM_DIS", 5), ("SEXO", 1), ("EDAD", 2), ("FAC_PER", 5)])
    f1 = []
    for i in range(n):
        b = _persona(rng, i, 70)
        f1.append([f"{i:07d}", b["niv"][-1]] + [_yn(rng, q) for q in (.2, .15, .05, .04, .01, .03)]
                  + [b["tloc"], b["est"], b["upm"], b["sexo"], b["edad"], b["w"].zfill(5)])
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("tmodulo1.DBF", _dbf(c1, f1))
        zf.writestr("tmodulo2.DBF", _dbf([("UPM", 7)], []))
    return buf.getvalue()


def corre_sintetico(errores):
    spec = _spec()
    mod = _modulo()
    inputs = _inputs_repo(spec)
    with tempfile.TemporaryDirectory() as td:
        for pid, fab in (("enif2021_csv", payload_2021), ("enif2018_csv", payload_2018),
                         ("enif_2015_enif_2015_bd_dbf", payload_2015)):
            z = Path(td) / f"{pid}.zip"
            z.write_bytes(fab())
            inputs[pid] = {"ruta_absoluta": str(z), "bytes": None}
        contrato = {"parametros": {"bootstrap_replicas": REPS}, "seed": {"valor": 42}}
        try:
            out = mod.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"medir() sobre el sintético reventó: {exc!r}")
            return None
        # PARA si la tabla de comparabilidad cambia un veredicto congelado
        txt = inputs["AHORRO-COMPARABILIDAD-TEXTO"]["bytes"].decode("utf-8").split("\n")
        cab = txt[0].split("\t"); io_, iv, iob = cab.index("ola"), cab.index("veredicto"), cab.index("objeto")
        rota = []
        for l in txt:
            c = l.split("\t")
            if len(c) == len(cab) and c[iob] == "E-FOR" and c[io_] == "2018":
                c[iv] = "CAMBIO-DE-INSTRUMENTO"
            rota.append("\t".join(c))
        r = dict(inputs); r["AHORRO-COMPARABILIDAD-TEXTO"] = {"ruta_absoluta": "", "bytes": "\n".join(rota).encode("utf-8")}
        try:
            mod.medir(r, contrato)
            errores.append("el medidor no PARÓ con E-FOR·2018 degradado en la tabla de comparabilidad")
        except RuntimeError:
            pass
    return out


def falsa_sintetico(out, spec, errores):
    import corrida0  # noqa: E402
    probs = corrida0._valida_outputs(spec, out)
    if probs:
        errores.append(f"_valida_outputs: {probs[:5]} (+{max(0, len(probs) - 5)})")
    P = "RESULT-ENIFPIC"
    claves = sorted({k[len(P) + 1:-len("-IC-CALIBRADO-INF")] for k in out
                     if k.endswith("-IC-CALIBRADO-INF")})
    if len(claves) != 32:
        errores.append(f"celdas con IC calibrado: {len(claves)} (esperadas 32)")
    for k in claves:
        b = f"{P}-{k}"
        if out[f"{b}-ROTULO"] != "RETROSPECTIVA-MECÁNICA":
            errores.append(f"{k}: rótulo {out[f'{b}-ROTULO']!r}")
        if out[f"{b}-TIPO-INCERTIDUMBRE"] != "muestral + cambio-entre-olas":
            errores.append(f"{k}: tipo_incertidumbre")
        lo, hi = out[f"{b}-IC-CALIBRADO-INF"], out[f"{b}-IC-CALIBRADO-SUP"]
        if lo is not None and not (lo <= out[f"{b}-PISO-P"] <= hi):
            errores.append(f"{k}: el piso no está dentro de su IC calibrado")
        if lo is not None and not (lo <= out[f"{b}-PISO-IC-LO"] + 1e-12 and out[f"{b}-PISO-IC-HI"] - 1e-12 <= hi):
            # el calibrado contiene al muestral salvo por la asimetría del percentil en logit
            pass
    g = f"{P}-AGG-GLOBAL"
    if out.get(f"{g}-CONTROL-MUESTRAL-N-DENTRO") != 6 or out.get(f"{g}-CONTROL-MUESTRAL-COTEJO") != "COINCIDE":
        errores.append(f"control muestral: {out.get(f'{g}-CONTROL-MUESTRAL-N-DENTRO')} (esperado 6/32)")
    if out.get(f"{g}-N-CONGLOMERADOS") != 12:
        errores.append(f"conglomerados: {out.get(f'{g}-N-CONGLOMERADOS')}")
    d15 = sorted(k for k in out if k.endswith("-DESCRIPTIVO-H2015-P"))
    ok15 = all(k.startswith(f"{P}-INFORMAL-CUALQUIERA-") and any(
        f"-{e}-" in k for e in ("SEXO", "EDAD", "ESCOLARIDAD", "LOCALIDAD")) for k in d15)
    if len(d15) != 12 or not ok15:
        errores.append(f"2015 descriptivo fuera de su perímetro: {len(d15)} celdas")
    if any("2015" in k and "DESCRIPTIVO" not in k and "DIAG-2015" not in k for k in out):
        errores.append("2015 aparece fuera de DESCRIPTIVO/DIAG")
    declarados = {r["id"] for r in spec.get("resultados") or []}
    if declarados != set(out):
        errores.append(f"resultados declarados: {len(declarados - set(out))} sobran, {len(set(out) - declarados)} faltan")
    # D-22: rama terminal degenerada — ninguna celda calibrable (sin Δ en
    # ningún grupo): nulos permitidos, cobertura NO-EVALUABLE, mismo conjunto de ids.
    mod = _modulo()
    inputs = _inputs_repo(spec)
    celdas = mod.celdas_arbitro(inputs)
    piso = dict(mod._json_resultados(inputs, "PISO-ENIF2021-EJES"))
    piso.update(mod._json_resultados(inputs, "PISO-ENIF2021-FORMALIDAD"))
    R = mod._json_resultados(inputs, "R-ENIF2024")
    vacio = mod.calibra(celdas, piso, R, {}, {}, {})
    deg = dict(out); deg.update(vacio)
    if set(deg) != set(out):
        errores.append("rama sin celdas calibrables emite otro conjunto de ids")
    probs = corrida0._valida_outputs(spec, deg)
    if probs:
        errores.append(f"_valida_outputs en la rama sin celdas calibrables: {probs[:3]}")
    if deg.get(f"{P}-REGLA-X-LECTURA-MECANICA") != "NO-EVALUABLE" or deg.get(f"{g}-N-NO-CALIBRABLE") != 32:
        errores.append("rama sin celdas calibrables: lectura o conteo NO-CALIBRABLE")


def falsa_regla_a_mano(errores):
    mod = _modulo()
    Z = 1.959964
    lg = lambda p: math.log(p / (1 - p))  # noqa: E731
    ex = lambda x: 1 / (1 + math.exp(-x))  # noqa: E731
    celdas = [{"clave": f"D9-SEXO-{s}", "des": "D9", "eje": "sexo", "cat": s,
               "rid": f"RESULT-ARBITRO-ENIF2024-D9-SEXO-{s}-P", "pid": f"RESULT-X-D9-SEXO-{s}-P",
               "calc_piso": "X", "grupo": "D9-SEXO"} for s in ("1", "2")]
    piso = {"RESULT-X-D9-SEXO-1-P": .20, "RESULT-X-D9-SEXO-1-IC-LO": .18, "RESULT-X-D9-SEXO-1-IC-HI": .22,
            "RESULT-X-D9-SEXO-2-P": .30, "RESULT-X-D9-SEXO-2-IC-LO": .27, "RESULT-X-D9-SEXO-2-IC-HI": .33}
    R = {"RESULT-ARBITRO-ENIF2024-D9-SEXO-1-P": .17, "RESULT-ARBITRO-ENIF2024-D9-SEXO-2-P": .40}
    h18 = {"D9-SEXO-1": {"P": .25, "LO": .23, "HI": .27, "N": 900}, "D9-SEXO-2": {"P": .28, "LO": .26, "HI": .30, "N": 1100}}
    h21 = {"D9-SEXO-1": {"P": .21, "LO": .19, "HI": .23, "N": 950}, "D9-SEXO-2": {"P": .31, "LO": .29, "HI": .33, "N": 1150}}
    out = mod.calibra(celdas, piso, R, h18, h21)
    d1, d2 = lg(.21) - lg(.25), lg(.31) - lg(.28)
    tau2 = (d1 * d1 + d2 * d2) / 2
    for s, p, lo, hi, r in (("1", .20, .18, .22, .17), ("2", .30, .27, .33, .40)):
        ee = (lg(hi) - lg(lo)) / (2 * Z)
        c = math.sqrt(ee * ee + tau2)
        inf, sup = ex(lg(p) - Z * c), ex(lg(p) + Z * c)
        b = f"RESULT-ENIFPIC-D9-SEXO-{s}"
        if abs(out[f"{b}-IC-CALIBRADO-INF"] - inf) > 1e-12 or abs(out[f"{b}-IC-CALIBRADO-SUP"] - sup) > 1e-12:
            errores.append(f"regla a mano: celda {s} no reproduce la fórmula de la spec §4")
        esperado = "DENTRO" if inf <= r <= sup else "FUERA"
        if out[f"{b}-R-EN-IC-CALIBRADO"] != esperado:
            errores.append(f"regla a mano: celda {s} {out[f'{b}-R-EN-IC-CALIBRADO']} != {esperado}")
    if abs(out["RESULT-ENIFPIC-G-D9-SEXO-TAU2-LOGIT"] - tau2) > 1e-15:
        errores.append("regla a mano: τ² del grupo")
    # τ² sin centrar: un cambio uniforme (misma Δ en todas las celdas) NO se anula
    h21u = {k: {**v, "P": ex(lg(h18[k]["P"]) + .3)} for k, v in h18.items()}
    outu = mod.calibra(celdas, piso, R, h18, h21u)
    if abs(outu["RESULT-ENIFPIC-G-D9-SEXO-TAU2-LOGIT"] - .09) > 1e-12:
        errores.append("regla a mano: τ² se centró (un cambio uniforme debe dar τ² = Δ²)")
    # lectura mecánica de X
    lx = mod._lectura_x
    if (lx(.85, .55), lx(.85, .45), lx(.6, .3), lx(.4, .2)) != (
            "CUMPLE", "CUMPLE-CON-RESERVA", "NO-CUMPLE", "NO-CUMPLE-PERSISTENCIA-TRIENAL-NO-ES-PISO"):
        errores.append("regla a mano: lectura mecánica de X")


def falsa_oro(errores):
    spec = _spec()
    mod = _modulo()
    z = ROOT / "data/raw/enif2021_csv.zip"
    if not z.exists():
        errores.append("oro: data/raw/enif2021_csv.zip no está montado")
        return None
    inputs = _inputs_repo(spec)
    inputs["enif2021_csv"] = {"ruta_absoluta": str(z), "bytes": None}
    m = mod._modulo(inputs, "MEDIDOR-EJES-0003", "medidor_ejes_0003")
    celdas = mod.celdas_arbitro(inputs)
    piso = dict(mod._json_resultados(inputs, "PISO-ENIF2021-EJES"))
    piso.update(mod._json_resultados(inputs, "PISO-ENIF2021-FORMALIDAD"))
    est, _diag = mod.mide_2021(m, inputs, celdas, int(spec["parametros"]["bootstrap_replicas"]),
                               int(spec["seed"]["valor"]), armonizada=False)
    if any(k.startswith("RESULT-H2021") for k in est):
        errores.append("oro: se midió la versión armonizada 18-70 (no debía)")
    maxd, disc = mod.oro(celdas, est, piso)
    print(f"ORO 2021 (18+, nueve vías) contra los 32 pisos sellados: max|Δ| = {maxd:.3e}, discordes = {disc}")
    if disc:
        errores.append(f"oro: {disc} valores discordantes (max |Δ| = {maxd})")
    return maxd, disc


def corre(oro=False):
    errores = []
    for p in (SPEC_MD, Path(str(SPEC_MD) + ".sha256"), CALC / "medidor.py", CALC / "spec.yaml"):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    spec = _spec()
    sha_md = hashlib.sha256(SPEC_MD.read_bytes()).hexdigest()
    if Path(str(SPEC_MD) + ".sha256").read_text().split()[0] != sha_md:
        errores.append("sidecar .sha256 de la spec humana discordante")
    if spec.get("spec_md_sha256") != sha_md:
        errores.append("spec_md_sha256 del yaml no coincide con la spec humana")
    for ent in spec["inputs"]:
        if ent.get("origen") == "repo":
            if hashlib.sha256((ROOT / ent["ruta"]).read_bytes()).hexdigest() != ent.get("sha256"):
                errores.append(f"input {ent['id']}: sha256 declarado no coincide con el árbol")
        if "milpa/" in str(ent.get("ruta", "")):
            errores.append(f"input bajo milpa/: {ent['id']}")
    falsa_regla_a_mano(errores)
    out = corre_sintetico(errores)
    if out is not None:
        falsa_sintetico(out, spec, errores)
    if oro:
        falsa_oro(errores)
    return errores


def main():
    oro = "--oro" in sys.argv
    errores = corre(oro=oro)
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_enif_persistencia_ic_calibrado.py (sintético D-22 × 3 olas; regla a mano; "
              "guardia de comparabilidad; ids declarados" + ("; ORO 2021 reproduce los 32 pisos" if oro else "") + ")")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
