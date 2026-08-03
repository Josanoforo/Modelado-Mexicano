#!/usr/bin/env python3
"""CAL-CONF Fase B -- posicion 4 (04/ago/2026) -- computa exposicion_violencia
(G4, C1), especificacion congelada en
forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md §1.

Corre desde la raiz del repo: python3 tests/cal_conf_faseb_pos4.py
Requiere data/raw (symlink) -> envipe2025_csv.zip.
"""
import csv
import io
import sys
import zipfile
from collections import defaultdict

sys.path.insert(0, "tests")
import svystat  # noqa: E402

RAW = "data/raw"
TRAMOS = ["18-29", "30-44", "45-59", "60+"]


def tramo_edad(edad_str):
    edad_str = edad_str.strip()
    if edad_str == "98" or edad_str == "":
        return None
    e = 97 if edad_str == "97" else int(edad_str)
    if 18 <= e <= 29:
        return "18-29"
    if 30 <= e <= 44:
        return "30-44"
    if 45 <= e <= 59:
        return "45-59"
    if e >= 60:
        return "60+"
    return None


def fmt_pct(x):
    return f"{x*100:.1f}%"


def fmt_pp(x):
    return f"{x*100:.2f}pp"


def reporta_celda(n, out):
    if n < 30 or out is None:
        return f"n={n} SIN SOPORTE"
    return f"n={n} p={fmt_pct(out['p_hat'])} se={fmt_pp(out['se'])} ic95=[{fmt_pct(out['ic95'][0])},{fmt_pct(out['ic95'][1])}]"


# ---------------------------------------------------------------------
# §2.1 -- validar estimador (caso sintetico conocido)
# ---------------------------------------------------------------------
print("=" * 70)
print("§2, caso 1 -- validacion del estimador (sintetico)")
print("=" * 70)
svystat._caso_conocido()

# ---------------------------------------------------------------------
# §2.2 -- validar pipeline reproduciendo TPer_Vic1 / Guardia Nacional (ola 2)
#         antes de tocar TMod_Vic, que ninguna sesion anterior habia leido.
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("§2, caso 2 -- reproduce Guardia Nacional (ola 2, TPer_Vic1) con dato real")
print("=" * 70)

with zipfile.ZipFile(f"{RAW}/envipe2025_csv.zip") as z:
    name1 = "tper_vic1_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2025.csv"
    with z.open(name1) as f:
        tper_vic1_rows = list(csv.DictReader(io.TextIOWrapper(f, encoding="latin-1")))

print(f"n_filas_tabla = {len(tper_vic1_rows)}")
n_identifica = sum(1 for r in tper_vic1_rows if r["AP5_3_04"] == "1")
n_no_identifica = sum(1 for r in tper_vic1_rows if r["AP5_3_04"] != "1")
cells_gn = defaultdict(list)
n_sin_resp = 0
for r in tper_vic1_rows:
    if r["AP5_3_04"] != "1":
        continue
    v = r["AP5_4_04"].strip()
    if v in ("", "9"):
        n_sin_resp += 1
        continue
    tramo = tramo_edad(r["EDAD"])
    if tramo is None:
        continue
    y = 1 if v in ("1", "2") else 0
    cells_gn[tramo].append((r["EST_DIS"], r["UPM_DIS"], float(r["FAC_ELE"]), y))

print(f"Identifica: {n_identifica} -- no identifica/NS: {n_no_identifica} -- sin respuesta: {n_sin_resp}")
assert len(tper_vic1_rows) == 91182, "TPer_Vic1 no tiene el n de filas esperado -- DETENTE"
assert n_identifica == 71742 and n_no_identifica == 19440 and n_sin_resp == 911, \
    "pipeline NO reproduce la ola 2 (Guardia Nacional) -- DETENTE"
esperado_gn = {"18-29": (16620, 82.2), "30-44": (23905, 80.2), "45-59": (17659, 79.6), "60+": (12352, 81.8)}
for tramo in TRAMOS:
    data = cells_gn[tramo]
    out = svystat.prop_ultimate_cluster(data)
    n_esp, p_esp = esperado_gn[tramo]
    print(f"  {tramo}: {reporta_celda(len(data), out)}  (esperado n={n_esp} p={p_esp}%)")
    assert len(data) == n_esp, f"n no coincide en {tramo}"
    assert abs(out["p_hat"] * 100 - p_esp) < 0.05, f"p no coincide en {tramo}"
print("Pipeline verificado contra la ola 2 -- coincide exactamente. Procede con TMod_Vic.")

# ---------------------------------------------------------------------
# §0.2/§3 -- TMod_Vic: BP1_20 / BP1_23 / BP1_28
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("§0.2/§3 -- ENVIPE 2025, TMod_Vic (exposicion_violencia)")
print("=" * 70)

with zipfile.ZipFile(f"{RAW}/envipe2025_csv.zip") as z:
    name2 = "tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv"
    with z.open(name2) as f:
        rows = list(csv.DictReader(io.TextIOWrapper(f, encoding="latin-1")))

n_total = len(rows)
print(f"n_filas_TMod_Vic = {n_total}")
assert n_total == 40280, "TMod_Vic no tiene el n de filas esperado -- DETENTE"

fac_del_sum = sum(float(r["FAC_DEL"]) for r in rows)
print(f"suma FAC_DEL (sin filtro) = {fac_del_sum:,.0f}")

n_si = sum(1 for r in rows if r["BP1_20"] == "1")
n_no = sum(1 for r in rows if r["BP1_20"] == "2")
n_23_filled_no = sum(1 for r in rows if r["BP1_20"] == "2" and r["BP1_23"].strip() != "")
n_reversa_no = sum(1 for r in rows if r["BP1_20"] == "2" and r["BP1_23"].strip() == "" and r["BP1_28"].strip() != "")
n_ninguno_no = sum(1 for r in rows if r["BP1_20"] == "2" and r["BP1_23"].strip() == "" and r["BP1_28"].strip() == "")
print(f"BP1_20=Si: {n_si} · BP1_20=No: {n_no} (de estos: BP1_23 valido={n_23_filled_no}, "
      f"reversa/BP1_28 en vez de BP1_23={n_reversa_no}, ninguno={n_ninguno_no})")
assert n_si == 4110 and n_no == 36170 and n_23_filled_no == 36040 and n_reversa_no == 32 and n_ninguno_no == 98

print()
print("--- BP1_20 (denuncio), conjunto primario edad ---")
by_edad = {t: [] for t in TRAMOS}
excl_edad = 0
for r in rows:
    t = tramo_edad(r["EDAD"])
    if t is None:
        excl_edad += 1
        continue
    y = 1 if r["BP1_20"] == "1" else 0
    by_edad[t].append((r["EST_DIS"], r["UPM_DIS"], float(r["FAC_DEL"]), y))
print(f"excluidos por EDAD=98: {excl_edad}")
for t in TRAMOS:
    out = svystat.prop_ultimate_cluster(by_edad[t])
    print(f"  {t}: {reporta_celda(len(by_edad[t]), out)}")

print()
print("--- BP1_20 marginal por DOMINIO ---")
by_dom = defaultdict(list)
for r in rows:
    y = 1 if r["BP1_20"] == "1" else 0
    by_dom[r["DOMINIO"]].append((r["EST_DIS"], r["UPM_DIS"], float(r["FAC_DEL"]), y))
for d, label in [("U", "Urbano"), ("C", "Complemento urbano"), ("R", "Rural")]:
    out = svystat.prop_ultimate_cluster(by_dom[d])
    print(f"  {label}: {reporta_celda(len(by_dom[d]), out)}")

CODS_23 = {
    "01": "Miedo al/a la agresor(a)", "02": "Miedo a extorsion", "03": "Delito de poca importancia",
    "04": "Perdida de tiempo", "05": "Tramites largos y dificiles", "06": "Desconfianza en la autoridad",
    "07": "No tenia pruebas", "08": "Actitud hostil de la autoridad", "09": "Otra", "99": "No sabe/no responde",
}
print()
print("--- BP1_23 (razon de no denuncia), universo BP1_20=No con codigo valido ---")
universo_23 = [r for r in rows if r["BP1_20"] == "2" and r["BP1_23"].strip() in CODS_23]
print(f"n universo = {len(universo_23)}")
for cod, label in CODS_23.items():
    cell = [(r["EST_DIS"], r["UPM_DIS"], float(r["FAC_DEL"]), 1 if r["BP1_23"] == cod else 0) for r in universo_23]
    out = svystat.prop_ultimate_cluster(cell)
    n_cod = sum(c[3] for c in cell)
    print(f"  {cod} {label}: {reporta_celda(n_cod, out) if n_cod >= 30 else f'n={n_cod} SIN SOPORTE'}")

CODS_28 = {
    "1": "Por el seguro", "2": "Recuperar sus cosas", "3": "Castigo al delincuente",
    "4": "Reparacion del dano", "5": "Deslindar responsabilidades", "6": "Otra", "9": "No sabe/no responde",
}
print()
print("--- BP1_28 (razon de si denuncio), universo BP1_20=Si con codigo valido ---")
universo_28 = [r for r in rows if r["BP1_20"] == "1" and r["BP1_28"].strip() in CODS_28]
print(f"n universo = {len(universo_28)}")
for cod, label in CODS_28.items():
    cell = [(r["EST_DIS"], r["UPM_DIS"], float(r["FAC_DEL"]), 1 if r["BP1_28"] == cod else 0) for r in universo_28]
    out = svystat.prop_ultimate_cluster(cell)
    n_cod = sum(c[3] for c in cell)
    flag = "" if n_cod >= 30 else " SIN SOPORTE"
    print(f"  {cod} {label}: n={n_cod} p={fmt_pct(out['p_hat'])} se={fmt_pp(out['se'])}{flag}")

print()
print("=" * 70)
print("Fin de la corrida.")
print("=" * 70)
