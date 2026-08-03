#!/usr/bin/env python3
"""CAL-CONF Fase B, segunda ola (03/ago/2026) -- computa las tablas de
seguridad-FFAA / justicia-policia / electoral-partidos, especificacion
congelada en forense/notas/2026-08-03-cal-conf-faseb-medicion-ola2.md §1.

Corre desde la raiz del repo: python3 tests/cal_conf_faseb_ola2.py
Requiere data/raw (symlink) -> envipe2025_csv.zip, BD_ENCUCI2020_dbf.zip.
"""
import csv
import io
import sys
import zipfile
from collections import Counter, defaultdict

sys.path.insert(0, "tests")
import dbfmini  # noqa: E402
import svystat  # noqa: E402

RAW = "data/raw"


def tramo_edad_envipe(edad_str):
    if not edad_str:
        return None
    e = int(edad_str)
    if e == 98:
        return None  # no especificada
    if e == 97:
        e = 97  # "97 o mas" -- ya cae en 60+
    if 18 <= e <= 29:
        return "18-29"
    if 30 <= e <= 44:
        return "30-44"
    if 45 <= e <= 59:
        return "45-59"
    if e >= 60:
        return "60+"
    return None


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


def fmt_pct(x):
    return f"{x*100:.1f}%"


def fmt_pp(x):
    return f"{x*100:.2f}pp"


def reporta_celda(n, out):
    if n < 30:
        return f"| {n} | SIN SOPORTE | -- | -- |"
    return f"| {n} | {fmt_pct(out['p_hat'])} | {fmt_pp(out['se'])} | [{fmt_pct(out['ic95'][0])}, {fmt_pct(out['ic95'][1])}] |"


# ---------------------------------------------------------------------
# 0. Validar estimador (caso conocido)
# ---------------------------------------------------------------------
print("=" * 70)
print("§2 -- validacion del estimador")
print("=" * 70)
svystat._caso_conocido()

# ---------------------------------------------------------------------
# 0.b Validar el pipeline ENCUCI reproduciendo educacion (primera ola)
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("Validacion de pipeline -- reproduce educacion (primera ola) antes de tocar reactivos nuevos")
print("=" * 70)

with zipfile.ZipFile(f"{RAW}/BD_ENCUCI2020_dbf.zip") as z:
    z.extract("ENCUCI_2020_SD.dbf", "/tmp/claude-1000/-home-pc0/61e9e624-13c9-4a95-807b-5cd2c1d8c531/scratchpad/encuci_ola2")
    z.extract("ENCUCI_2020_SEC_4_5.dbf", "/tmp/claude-1000/-home-pc0/61e9e624-13c9-4a95-807b-5cd2c1d8c531/scratchpad/encuci_ola2")

SD_PATH = "/tmp/claude-1000/-home-pc0/61e9e624-13c9-4a95-807b-5cd2c1d8c531/scratchpad/encuci_ola2/ENCUCI_2020_SD.dbf"
SEC45_PATH = "/tmp/claude-1000/-home-pc0/61e9e624-13c9-4a95-807b-5cd2c1d8c531/scratchpad/encuci_ola2/ENCUCI_2020_SEC_4_5.dbf"

sd = {}
for row in dbfmini.read_dbf(SD_PATH, wanted_fields=["UPM", "VIV_SEL", "N_REN", "EDAD", "AP3_15_4"]):
    key = (row["UPM"], row["VIV_SEL"], row["N_REN"])
    edad_raw = row["EDAD"].strip()
    edad = tramo_edad_encuci(edad_raw) if edad_raw else None
    sd[key] = (edad, row["AP3_15_4"].strip())


def cargar_sec45(campos_reactivo):
    """Devuelve lista de dicts por fila util, con join a SD ya resuelto."""
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
print("(esperado de la primera ola: n_filas=21519 no_respuesta=1483 sin_cruce=1265 utiles=18771)")
assert n_filas == 21519 and no_resp == 1483 and sin_cruce == 1265, "pipeline NO reproduce la primera ola -- DETENTE"
for key in [("Formal", "18-29"), ("Formal", "30-44"), ("Formal", "45-59"), ("Formal", "60+"),
            ("Informal", "18-29"), ("Informal", "30-44"), ("Informal", "45-59"), ("Informal", "60+")]:
    data = cells[key]
    out = svystat.prop_ultimate_cluster(data)
    print(f"  {key}: n={len(data)} p={fmt_pct(out['p_hat'])} se={fmt_pp(out['se'])}")
print("Pipeline verificado -- coincide exactamente con la primera ola. Procede con los reactivos nuevos.")

# ---------------------------------------------------------------------
# 1. ENVIPE -- seguridad-FFAA y justicia-policia
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("§3.1-3.2 -- ENVIPE 2025, TPer_Vic1 (seguridad-FFAA, justicia-policia)")
print("=" * 70)

FFAA = [("AP5_4_04", "AP5_3_04", "Guardia Nacional"),
        ("AP5_4_08", "AP5_3_08", "Ejercito"),
        ("AP5_4_09", "AP5_3_09", "Fuerza Aerea"),
        ("AP5_4_10", "AP5_3_10", "Marina")]
JUSTICIA = [("AP5_4_01", "AP5_3_01", "Policia de Transito"),
            ("AP5_4_02", "AP5_3_02", "Policia Preventiva"),
            ("AP5_4_03", "AP5_3_03", "Policia Estatal"),
            ("AP5_4_05", "AP5_3_05", "Policia Ministerial/Judicial"),
            ("AP5_4_06", "AP5_3_06", "MP y Fiscalias Estatales"),
            ("AP5_4_07", "AP5_3_07", "FGR"),
            ("AP5_4_11", "AP5_3_11", "Jueces")]

wanted = ["EDAD", "DOMINIO", "FAC_ELE", "EST_DIS", "UPM_DIS"]
for confid, ident, _ in FFAA + JUSTICIA:
    wanted += [confid, ident]

envipe_rows = []
with zipfile.ZipFile(f"{RAW}/envipe2025_csv.zip") as z:
    name = "tper_vic1_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2025.csv"
    with z.open(name) as f:
        r = csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"))
        for row in r:
            envipe_rows.append(row)

print(f"TPer_Vic1: {len(envipe_rows)} filas totales")


def tabla_envipe(items, titulo):
    print()
    print(f"--- {titulo} ---")
    for confid, ident, nombre in items:
        n_total = len(envipe_rows)
        n_identifica = sum(1 for row in envipe_rows if row[ident] == "1")
        n_no_identifica = sum(1 for row in envipe_rows if row[ident] in ("2", "9"))
        n_ident_pero_sin_confid = 0
        cells = defaultdict(list)
        cells_dom = defaultdict(list)
        n_norespuesta_confid = 0
        for row in envipe_rows:
            if row[ident] != "1":
                continue
            v = row[confid]
            if v in ("", "9"):
                n_norespuesta_confid += 1
                continue
            code = int(v)
            y = 1 if code in (1, 2) else 0
            tramo = tramo_edad_envipe(row["EDAD"])
            fac = float(row["FAC_ELE"])
            est, upm = row["EST_DIS"], row["UPM_DIS"]
            if tramo is not None:
                cells[tramo].append((est, upm, fac, y))
            dom = row["DOMINIO"]
            cells_dom[dom].append((est, upm, fac, y))
        print(f"{nombre} (`{confid}`): identifica={n_identifica} ({n_identifica/n_total*100:.1f}%) "
              f"· no identifica/NS={n_no_identifica} · sin respuesta de confianza entre quienes identifican={n_norespuesta_confid}")
        print("  Edad | n | % confia | SE | IC95%")
        for tramo in ["18-29", "30-44", "45-59", "60+"]:
            data = cells[tramo]
            out = svystat.prop_ultimate_cluster(data) if data else None
            if not data or len(data) < 30:
                print(f"  {tramo} {reporta_celda(len(data), out)}")
            else:
                print(f"  {tramo} {reporta_celda(len(data), out)}")
        print("  Dominio | n | % confia | SE | IC95%")
        for dom, label in [("U", "Urbano"), ("C", "Complemento urbano"), ("R", "Rural")]:
            data = cells_dom.get(dom, [])
            out = svystat.prop_ultimate_cluster(data) if data else None
            print(f"  {label} {reporta_celda(len(data), out)}")


tabla_envipe(FFAA, "seguridad-FFAA")
tabla_envipe(JUSTICIA, "justicia-policia")

# ---------------------------------------------------------------------
# 2. ENCUCI -- electoral-partidos
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("§3.3 -- ENCUCI 2020, SEC_4_5 (electoral-partidos)")
print("=" * 70)

ELECTORAL = [("AP5_2_5", "Partidos politicos"),
             ("AP5_3_6", "Senadores y diputados federales"),
             ("AP5_3_7", "Diputados locales"),
             ("AP5_3_8", "Instituto Nacional Electoral")]

campos_elect = [c for c, _ in ELECTORAL]
n_filas_e, filas_e = cargar_sec45(campos_elect)

for confid, nombre in ELECTORAL:
    no_resp = 0
    sin_cruce = 0
    cells = defaultdict(list)
    cells_dom = defaultdict(list)
    for row, sdinfo in filas_e:
        code = codigo_num(row[confid])
        if code in (5, 9) or code is None:
            no_resp += 1
            continue
        if sdinfo is None or sdinfo[0] is None:
            sin_cruce += 1
            continue
        tramo, ap3154 = sdinfo
        formalidad = "Formal" if ap3154 == "1" else ("Informal" if ap3154 == "0" else None)
        y = 1 if code in (1, 2) else 0
        fac = float(row["FAC_SEL"].strip())
        est, upm = row["EST_DIS"].strip(), row["UPM_DIS"].strip()
        if tramo is not None and formalidad is not None:
            cells[(formalidad, tramo)].append((est, upm, fac, y))
        dom = row["DOMINIO"].strip()
        cells_dom[dom].append((est, upm, fac, y))
    utiles = n_filas_e - no_resp - sin_cruce
    print()
    print(f"{nombre} (`{confid}`): n_filas={n_filas_e} no_respuesta={no_resp} sin_cruce_edad={sin_cruce} utiles={utiles}")
    print("  Formalidad | Edad | n | % confia | SE | IC95%")
    for formalidad in ["Formal", "Informal"]:
        for tramo in ["18-29", "30-44", "45-59", "60+"]:
            data = cells[(formalidad, tramo)]
            out = svystat.prop_ultimate_cluster(data) if data else None
            print(f"  {formalidad} {tramo} {reporta_celda(len(data), out)}")
    print("  Dominio | n | % confia | SE | IC95%")
    for dom, label in [("U", "Urbano"), ("C", "Complemento urbano"), ("R", "Rural")]:
        data = cells_dom.get(dom, [])
        out = svystat.prop_ultimate_cluster(data) if data else None
        print(f"  {label} {reporta_celda(len(data), out)}")

print()
print("=" * 70)
print("Fin de la corrida.")
print("=" * 70)
