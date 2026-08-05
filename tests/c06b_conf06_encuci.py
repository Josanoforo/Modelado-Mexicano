#!/usr/bin/env python3
"""ACTO C-06b (05/ago/2026) -- conf.06 contra ENCUCI, corte >=8/10 vs >=6/10.

Especificacion congelada en
forense/notas/2026-08-05-c06b-conf06-encuci-corte.md §1, escrita y
commiteada antes de correr este script.

Corre desde la raiz del repo: python3 tests/c06b_conf06_encuci.py
Requiere data/raw (symlink) -> BD_ENCUCI2020_dbf.zip.

No modifica tests/svystat.py ni tests/dbfmini.py. A diferencia de
tests/cal_conf_faseb_pos5_6.py, este script NO hace join a
ENCUCI_2020_SD -- el estimando es un agregado nacional sin condicionar
(no requiere formalidad/edad), y FAC_SEL/EST_DIS/UPM_DIS viven en
SEC_4_5 mismo (verificado contra FD_ENCUCI2020.pdf p.32 en la ficha,
§0/§1.2/§1.4).
"""
import sys
import tempfile
import zipfile

sys.path.insert(0, "tests")
import dbfmini  # noqa: E402
import svystat  # noqa: E402

RAW = "data/raw"

RADIO = [("AP5_1_1", "la mayoria de las personas"),
         ("AP5_1_2", "personas que conoce personalmente"),
         ("AP5_1_3", "vecinos de su colonia/localidad")]

CORTES = [6, 8]

# (etiqueta, valor, item(s) candidato(s) declarados por C-06a §5, nota)
CORPUS_CIFRAS = [
    ("21.8%", 0.218, "AP5_1_1", "candidata C-06a §5"),
    ("32.1%", 0.321, "AP5_1_1 o AP5_1_3", "candidata C-06a §5 -- ambiguo, decide el propio resultado (§1.8 de la ficha)"),
    ("62.1%", 0.621, "AP5_1_2", "candidata C-06a §5"),
]

NO_RESP_ESPERADO = {"AP5_1_1": 110, "AP5_1_2": 74, "AP5_1_3": 116}


def fmt_pct(x):
    return f"{x*100:.1f}%"


def fmt_pp(x):
    return f"{x*100:.2f}pp"


def reporta_celda(n, out):
    if n < 30 or out is None:
        return f"n={n} SIN SOPORTE"
    return (f"n={n} p={fmt_pct(out['p_hat'])} se={fmt_pp(out['se'])} "
            f"ic95=[{fmt_pct(out['ic95'][0])}, {fmt_pct(out['ic95'][1])}]")


def codigo_ap5_1(v):
    v = v.strip()
    if not v:
        return None
    return int(v)  # campo tipo C, "00".."10","99"


print("=" * 70)
print("§0 -- validacion del estimador (caso conocido, re-corrida en este entorno)")
print("=" * 70)
svystat._caso_conocido()

TMP = tempfile.mkdtemp(prefix="c06b_conf06_")

print()
print("=" * 70)
print("Extraccion ENCUCI_2020_SEC_4_5 -- sin join a SD (agregado nacional, ficha §1.2)")
print("=" * 70)

with zipfile.ZipFile(f"{RAW}/BD_ENCUCI2020_dbf.zip") as z:
    z.extract("ENCUCI_2020_SEC_4_5.dbf", TMP)

SEC45_PATH = f"{TMP}/ENCUCI_2020_SEC_4_5.dbf"

campos = ["FAC_SEL", "EST_DIS", "UPM_DIS"] + [c for c, _ in RADIO]
filas = list(dbfmini.read_dbf(SEC45_PATH, wanted_fields=campos))
n_filas = len(filas)

# ---------------------------------------------------------------------
# Guardia de pipeline (ficha §1.10) -- assert duro antes de tocar el
# corte >=8/10
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("Guardia de pipeline -- reproduce no_respuesta(99) ya publicado antes de calcular algo nuevo")
print("=" * 70)

no_resp_obs = {confid: 0 for confid, _ in RADIO}
for row in filas:
    for confid, _ in RADIO:
        code = codigo_ap5_1(row[confid])
        if code is None or code == 99:
            no_resp_obs[confid] += 1

print(f"n_filas={n_filas} (esperado 21519)")
for confid, _ in RADIO:
    print(f"  no_respuesta(99) {confid} = {no_resp_obs[confid]} (esperado {NO_RESP_ESPERADO[confid]})")

assert n_filas == 21519, f"n_filas NO reproduce -- DETENTE (obtenido {n_filas})"
for confid, _ in RADIO:
    assert no_resp_obs[confid] == NO_RESP_ESPERADO[confid], (
        f"no_respuesta({confid}) NO reproduce -- DETENTE "
        f"(obtenido {no_resp_obs[confid]}, esperado {NO_RESP_ESPERADO[confid]})")
print("Guardia de pipeline verificada -- coincide exacto con lo publicado. Procede con la matriz item x corte.")

# ---------------------------------------------------------------------
# Matriz completa item x corte (ficha §1.6-§1.7)
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("Matriz completa: 3 items x 2 cortes -- agregado nacional, sin condicionar")
print("=" * 70)

resultados = {}  # (confid, corte) -> (n, out|None)

for confid, nombre in RADIO:
    print()
    print(f"{nombre} (`{confid}`):")
    for corte in CORTES:
        rows = []
        for row in filas:
            code = codigo_ap5_1(row[confid])
            if code is None or code == 99:
                continue
            y = 1 if code >= corte else 0
            fac = float(row["FAC_SEL"].strip())
            est = row["EST_DIS"].strip()
            upm = row["UPM_DIS"].strip()
            rows.append((est, upm, fac, y))
        out = svystat.prop_ultimate_cluster(rows) if rows else None
        resultados[(confid, corte)] = (len(rows), out)
        extra = f" n_estratos={out['n_estratos']} singleton={out['n_estratos_singleton']}" if out else ""
        print(f"  corte >={corte}/10: {reporta_celda(len(rows), out)}{extra}")

# ---------------------------------------------------------------------
# Comparacion contra las tres cifras del corpus (ficha §1.8) -- criterio
# fijado antes de ver esto: contenida en IC95%, no cercania puntual
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("Comparacion contra las tres cifras de conf.06 -- ¿cae dentro del IC95%? (criterio de §1.8, no cercania)")
print("=" * 70)

for etiqueta, valor, candidata, nota in CORPUS_CIFRAS:
    print()
    print(f"{etiqueta} ({nota}; item(s) candidato(s): {candidata}):")
    for confid, _ in RADIO:
        for corte in CORTES:
            n, out = resultados[(confid, corte)]
            if out is None:
                print(f"  {confid} >={corte}/10: SIN SOPORTE")
                continue
            lo, hi = out["ic95"]
            contiene = lo <= valor <= hi
            marca = "SI -- REPRODUCE" if contiene else "no"
            print(f"  {confid} >={corte}/10: p={fmt_pct(out['p_hat'])} ic95=[{fmt_pct(lo)}, {fmt_pct(hi)}] -- ¿contiene {etiqueta}? {marca}")

print()
print("=" * 70)
print("Fin de la corrida.")
print("=" * 70)
