#!/usr/bin/env python3
"""CAL-CONF Fase B, posiciones 5 y 6 (03/ago/2026) -- computa las tablas de
`radio_confianza` (ENCUCI AP5_1_1/2/3) y `familismo_apoyo` (ENIF P9_9_1..6),
especificacion congelada en
forense/notas/2026-08-03-cal-conf-faseb-medicion-pos5-6.md §1.

Corre desde la raiz del repo: python3 tests/cal_conf_faseb_pos5_6.py
Requiere data/raw (symlink) -> BD_ENCUCI2020_dbf.zip, enif2024_csv.zip.

A diferencia de tests/cal_conf_faseb_ola2.py, este script NO hardcodea una
ruta de scratch de una sesion anterior: usa tempfile.mkdtemp() para que
corra igual en cualquier entorno que monte data/raw.
"""
import csv
import io
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

sys.path.insert(0, "tests")
import dbfmini  # noqa: E402
import svystat  # noqa: E402

RAW = "data/raw"


def tramo_edad_encuci(edad_str):
    if not edad_str:
        return None
    e = int(float(edad_str))
    if e in (97, 98, 99):
        return None
    if e == 96:
        e = 97
    if 18 <= e <= 29:
        return "18-29"
    if 30 <= e <= 44:
        return "30-44"
    if 45 <= e <= 59:
        return "45-59"
    if e >= 60:
        return "60+"
    return None


def tramo_edad_enif(edad_str):
    if not edad_str:
        return None
    e = int(float(edad_str))
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
    return f"n={n} p={fmt_pct(out['p_hat'])} se={fmt_pp(out['se'])} ic95=[{fmt_pct(out['ic95'][0])}, {fmt_pct(out['ic95'][1])}]"


print("=" * 70)
print("§2 -- validacion del estimador (caso conocido, re-corrida en este entorno, no heredada)")
print("=" * 70)
svystat._caso_conocido()

TMP = tempfile.mkdtemp(prefix="cal_conf_pos5_6_")

# ---------------------------------------------------------------------
# ENCUCI -- extraer y validar pipeline reproduciendo educacion (primera ola)
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("Validacion de pipeline ENCUCI -- reproduce educacion (primera ola) antes de tocar AP5_1_*")
print("=" * 70)

with zipfile.ZipFile(f"{RAW}/BD_ENCUCI2020_dbf.zip") as z:
    z.extract("ENCUCI_2020_SD.dbf", TMP)
    z.extract("ENCUCI_2020_SEC_4_5.dbf", TMP)

SD_PATH = f"{TMP}/ENCUCI_2020_SD.dbf"
SEC45_PATH = f"{TMP}/ENCUCI_2020_SEC_4_5.dbf"

sd = {}
for row in dbfmini.read_dbf(SD_PATH, wanted_fields=["UPM", "VIV_SEL", "N_REN", "EDAD", "AP3_15_4"]):
    key = (row["UPM"], row["VIV_SEL"], row["N_REN"])
    edad_raw = row["EDAD"].strip()
    edad = tramo_edad_encuci(edad_raw) if edad_raw else None
    sd[key] = (edad, row["AP3_15_4"].strip())


def cargar_sec45(campos_reactivo):
    n_filas = 0
    filas = []
    campos = ["UPM", "VIV_SEL", "R_SEL", "FAC_SEL", "EST_DIS", "UPM_DIS", "DOMINIO"] + campos_reactivo
    for row in dbfmini.read_dbf(SEC45_PATH, wanted_fields=campos):
        n_filas += 1
        key = (row["UPM"], row["VIV_SEL"], row["R_SEL"])
        sdinfo = sd.get(key)
        filas.append((row, sdinfo))
    return n_filas, filas


def codigo_num(v):
    v = v.strip()
    if not v:
        return None
    return int(float(v))


n_filas, filas = cargar_sec45(["AP5_2_6"])
no_resp = 0
sin_cruce = 0
cells = defaultdict(list)
for row, sdinfo in filas:
    code = codigo_num(row["AP5_2_6"])
    if code in (5, 9) or code is None:
        no_resp += 1
        continue
    if sdinfo is None or sdinfo[0] is None:
        sin_cruce += 1
        continue
    tramo, ap3154 = sdinfo
    if tramo is None:
        sin_cruce += 1
        continue
    formalidad = "Formal" if ap3154 == "1" else ("Informal" if ap3154 == "0" else None)
    if formalidad is None:
        continue
    y = 1 if code in (1, 2) else 0
    fac = float(row["FAC_SEL"].strip())
    cells[(formalidad, tramo)].append((row["EST_DIS"].strip(), row["UPM_DIS"].strip(), fac, y))

utiles = n_filas - no_resp - sin_cruce
print(f"n_filas={n_filas} no_respuesta={no_resp} sin_cruce={sin_cruce} utiles={utiles}")
print("(esperado, publicado en cal-conf-faseb-medicion.md y reproducido de nuevo por cal_conf_faseb_ola2.py: "
      "n_filas=21519 no_respuesta=1483 sin_cruce=1265 utiles=18771)")
assert n_filas == 21519 and no_resp == 1483 and sin_cruce == 1265, "pipeline ENCUCI NO reproduce la primera ola -- DETENTE"
for key in [("Formal", "18-29"), ("Formal", "30-44"), ("Formal", "45-59"), ("Formal", "60+"),
            ("Informal", "18-29"), ("Informal", "30-44"), ("Informal", "45-59"), ("Informal", "60+")]:
    data = cells[key]
    out = svystat.prop_ultimate_cluster(data)
    print(f"  {key}: {reporta_celda(len(data), out)}")
print("Pipeline ENCUCI verificado -- coincide exactamente con la primera ola/ola 2. Procede con AP5_1_*.")

# ---------------------------------------------------------------------
# §3.1 -- radio_confianza: ENCUCI AP5_1_1 / AP5_1_2 / AP5_1_3
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("§3.1 -- ENCUCI 2020, SEC_4_5 -- radio_confianza (AP5_1_1/2/3)")
print("=" * 70)

RADIO = [("AP5_1_1", "la mayoria de las personas"),
         ("AP5_1_2", "personas que conoce personalmente"),
         ("AP5_1_3", "vecinos de su colonia/localidad")]

campos_radio = [c for c, _ in RADIO]
n_filas_r, filas_r = cargar_sec45(campos_radio)


def codigo_ap5_1(v):
    v = v.strip()
    if not v:
        return None
    return int(v)  # campo tipo C, "00".."10","99"


for confid, nombre in RADIO:
    no_resp = 0
    sin_cruce = 0
    cells = defaultdict(list)
    cells_dom = defaultdict(list)
    for row, sdinfo in filas_r:
        code = codigo_ap5_1(row[confid])
        if code is None or code == 99:
            no_resp += 1
            continue
        if sdinfo is None or sdinfo[0] is None:
            sin_cruce += 1
            continue
        tramo, ap3154 = sdinfo
        formalidad = "Formal" if ap3154 == "1" else ("Informal" if ap3154 == "0" else None)
        y = 1 if code >= 6 else 0  # aprobatorio (>=6) vs no aprobatorio -- declarado en §1, escala "como en la escuela"
        fac = float(row["FAC_SEL"].strip())
        est, upm = row["EST_DIS"].strip(), row["UPM_DIS"].strip()
        if tramo is not None and formalidad is not None:
            cells[(formalidad, tramo)].append((est, upm, fac, y))
        dom = row["DOMINIO"].strip()
        cells_dom[dom].append((est, upm, fac, y))
    utiles = n_filas_r - no_resp - sin_cruce
    print()
    print(f"{nombre} (`{confid}`): n_filas={n_filas_r} no_respuesta(99)={no_resp} sin_cruce_edad={sin_cruce} utiles={utiles}")
    print("  Formalidad x Edad:")
    for formalidad in ["Formal", "Informal"]:
        for tramo in ["18-29", "30-44", "45-59", "60+"]:
            data = cells[(formalidad, tramo)]
            out = svystat.prop_ultimate_cluster(data) if data else None
            print(f"    {formalidad} {tramo}: {reporta_celda(len(data), out)}")
    print("  Dominio:")
    for dom, label in [("U", "Urbano"), ("C", "Complemento urbano"), ("R", "Rural")]:
        data = cells_dom.get(dom, [])
        out = svystat.prop_ultimate_cluster(data) if data else None
        print(f"    {label}: {reporta_celda(len(data), out)}")

# ---------------------------------------------------------------------
# ENIF -- extraer y validar pipeline reproduciendo financiera (primera ola)
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("Validacion de pipeline ENIF -- reproduce financiera (primera ola) antes de tocar P9_9_*")
print("=" * 70)

with zipfile.ZipFile(f"{RAW}/enif2024_csv.zip") as z:
    name = "conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/conjunto_de_datos_tmodulo_enif2024.csv"
    z.extract(name, TMP)

ENIF_PATH = f"{TMP}/{name}"

with open(ENIF_PATH, encoding="latin-1", newline="") as f:
    reader = csv.DictReader(f)
    enif_rows = list(reader)

print(f"TMODULO: {len(enif_rows)} filas totales")


def formalidad_enif(p3_13):
    p3_13 = p3_13.strip()
    if not p3_13:
        return None
    if p3_13 in ("1", "2", "3", "4", "5", "6"):
        return "Formal"
    if p3_13 == "7":
        return "Informal"
    return None  # 9 = no sabe, blanco = no trabaja


P11 = ["p11_1_1", "p11_1_2", "p11_1_3", "p11_1_4", "p11_1_5"]
n_sin_indice = 0
indice_cells = defaultdict(list)
for row in enif_rows:
    vals = []
    valido = True
    for c in P11:
        v = row[c].strip()
        if v not in ("1", "2"):
            valido = False
            break
        vals.append(1 if v == "1" else 0)
    if not valido:
        n_sin_indice += 1
        continue
    indice = sum(vals)
    tramo = tramo_edad_enif(row["edad_v"])
    formalidad = formalidad_enif(row["p3_13"])
    if tramo is None or formalidad is None:
        continue
    y = 1 if indice >= 3 else 0
    fac = float(row["fac_per"].strip())
    est, upm = row["est_dis"].strip(), row["upm_dis"].strip()
    indice_cells[(formalidad, tramo)].append((est, upm, fac, y))

print(f"n_filas={len(enif_rows)} sin_indice_valido={n_sin_indice}")
print("(esperado, publicado en cal-conf-faseb-medicion.md: n_filas=13502 sin_indice_valido=3238)")
assert len(enif_rows) == 13502 and n_sin_indice == 3238, "pipeline ENIF NO reproduce la primera ola -- DETENTE"
for key in [("Formal", "18-29"), ("Formal", "30-44"), ("Formal", "45-59"), ("Formal", "60+"),
            ("Informal", "18-29"), ("Informal", "30-44"), ("Informal", "45-59"), ("Informal", "60+")]:
    data = indice_cells[key]
    out = svystat.prop_ultimate_cluster(data) if data else None
    print(f"  {key}: {reporta_celda(len(data), out)}")
print("Pipeline ENIF verificado -- reproduce la primera ola. Procede con P9_9_*.")

# ---------------------------------------------------------------------
# §3.2 -- familismo_apoyo: ENIF P9_9_1..6, universo efectivo = filtro_s9_1=2
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("§3.2 -- ENIF 2024, TMODULO -- familismo_apoyo (P9_9_1..6, universo filtro_s9_1=2)")
print("=" * 70)

FAMILISMO = [("p9_9_1", "apoyos del gobierno para adultos mayores"),
             ("p9_9_2", "pension/jubilacion/Afore/plan privado"),
             ("p9_9_3", "venta o renta de bienes/propiedades"),
             ("p9_9_4", "dinero de esposa(o)/pareja/hijos/otros familiares  <-- C1 de familismo_apoyo"),
             ("p9_9_5", "seguir trabajando"),
             ("p9_9_6", "otro")]

n_71mas = sum(1 for row in enif_rows if row["filtro_s9_1"].strip() == "1")
n_menor71 = sum(1 for row in enif_rows if row["filtro_s9_1"].strip() == "2")
print(f"filtro_s9_1: 71+ (no aplica P9_9)={n_71mas} · <71 (universo efectivo)={n_menor71} · total={len(enif_rows)}")

for confid, nombre in FAMILISMO:
    no_resp = 0
    no_aplica_71mas = 0
    sin_cruce = 0
    cells = defaultdict(list)
    cells_marg = defaultdict(list)
    for row in enif_rows:
        if row["filtro_s9_1"].strip() == "1":
            no_aplica_71mas += 1
            continue
        v = row[confid].strip()
        if v in ("", "9"):
            no_resp += 1
            continue
        code = int(v)
        tramo = tramo_edad_enif(row["edad_v"])
        formalidad = formalidad_enif(row["p3_13"])
        y = 1 if code == 1 else 0
        fac = float(row["fac_per"].strip())
        est, upm = row["est_dis"].strip(), row["upm_dis"].strip()
        if tramo is not None and formalidad is not None:
            cells[(formalidad, tramo)].append((est, upm, fac, y))
        else:
            sin_cruce += 1
        tloc = row["tloc"].strip()
        cells_marg[tloc].append((est, upm, fac, y))
    utiles = len(enif_rows) - no_aplica_71mas - no_resp
    print()
    print(f"{nombre} (`{confid}`): no_aplica(71+)={no_aplica_71mas} no_respuesta(9/blanco)={no_resp} "
          f"utiles={utiles} sin_cruce_formalidad_edad={sin_cruce}")
    print("  Formalidad x Edad:")
    for formalidad in ["Formal", "Informal"]:
        for tramo in ["18-29", "30-44", "45-59", "60+"]:
            data = cells[(formalidad, tramo)]
            out = svystat.prop_ultimate_cluster(data) if data else None
            print(f"    {formalidad} {tramo}: {reporta_celda(len(data), out)}")
    print("  Urbanizacion (tloc):")
    for tl, label in [("1", "100k+"), ("2", "15k-99,999"), ("3", "2,500-14,999"), ("4", "<2,500")]:
        data = cells_marg.get(tl, [])
        out = svystat.prop_ultimate_cluster(data) if data else None
        print(f"    {label}: {reporta_celda(len(data), out)}")

print()
print("=" * 70)
print("Fin de la corrida.")
print("=" * 70)
