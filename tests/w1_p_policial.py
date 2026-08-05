#!/usr/bin/env python3
"""ENCARGO W1-P: radio_confianza (ENCUCI AP5_1_1/2/3) x tramite.mordida.discrecional,
estrato policial (AP5_16_1='1') vs no-policial (resto del universo de contacto),
especificacion congelada en forense/notas/2026-08-04-w1-p-policial.md ANTES de
correr este script.

Corre desde la raiz del repo: python3 tests/w1_p_policial.py
Requiere data/raw (symlink) -> BD_ENCUCI2020_dbf.zip.

Reusa sin modificar tests/svystat.py::prop_ultimate_cluster y tests/dbfmini.py.
"""
import math
import sys
import tempfile
import zipfile

sys.path.insert(0, "tests")
import dbfmini  # noqa: E402
import svystat  # noqa: E402

RAW = "data/raw"
Z = 1.959963985
N_MIN = 30  # n_min por celda, heredado de X1 (misma vara que toda Fase B)

AP16 = [f"AP5_16_{i}" for i in range(1, 11)]
THETA = [("AP5_1_1", "la mayoria de las personas"),
         ("AP5_1_2", "personas que conoce personalmente"),
         ("AP5_1_3", "vecinos de su colonia/localidad")]


def fmt_pct(x):
    return f"{x*100:.2f}%"


def fmt_pp(x):
    return f"{x*100:.2f}pp"


def num16(v):
    v = v.strip()
    if not v:
        return None
    return int(float(v))  # AP5_16_* son Numerico -- texto tipo "1.000000000000000"


def codigo_ap5_1(v):
    v = v.strip()
    if not v:
        return None
    return int(v)  # AP5_1_* son Caracter, "00".."10","99" (mismo parseo que cal_conf_faseb_pos5_6.py)


def mordida(v17, v18):
    v17, v18 = v17.strip(), v18.strip()
    if v17 == "1" or v18 == "1":
        return 1
    if v17 == "2" and v18 == "2":
        return 0
    return None  # blanco (sin contacto) o algun '9' que no permite decidir


def prevalencia_estrato(filas):
    data = []
    for row in filas:
        y = mordida(row["AP5_17"], row["AP5_18"])
        if y is None:
            continue
        fac = float(row["FAC_SEL"].strip())
        data.append((row["EST_DIS"].strip(), row["UPM_DIS"].strip(), fac, y))
    out = svystat.prop_ultimate_cluster(data)
    return len(data), out


def celda(filas, colname, nivel_confia):
    data = []
    for row in filas:
        code = codigo_ap5_1(row[colname])
        if code is None or code == 99:
            continue
        confia = 1 if code >= 6 else 0
        if confia != nivel_confia:
            continue
        y = mordida(row["AP5_17"], row["AP5_18"])
        if y is None:
            continue
        fac = float(row["FAC_SEL"].strip())
        data.append((row["EST_DIS"].strip(), row["UPM_DIS"].strip(), fac, y))
    n = len(data)
    if n < N_MIN:
        return n, None
    return n, svystat.prop_ultimate_cluster(data)


def beta_de(out1, out0):
    beta = out1["p_hat"] - out0["p_hat"]
    se = math.sqrt(out1["se"] ** 2 + out0["se"] ** 2)
    return beta, se, (beta - Z * se, beta + Z * se)


def rr_de(out1, out0):
    p1, p0 = out1["p_hat"], out0["p_hat"]
    if p0 == 0:
        return None, None, "no definido (p0=0)"
    if p1 == 0:
        return 0.0, None, "IC no calculable via log (p1=0)"
    rr = p1 / p0
    se_ln = math.sqrt((out1["se"] / p1) ** 2 + (out0["se"] / p0) ** 2)
    ci = (math.exp(math.log(rr) - Z * se_ln), math.exp(math.log(rr) + Z * se_ln))
    return rr, ci, None


print("=" * 70)
print("Validacion del estimador (caso conocido, re-corrida en este entorno)")
print("=" * 70)
svystat._caso_conocido()

TMP = tempfile.mkdtemp(prefix="w1_p_policial_")
with zipfile.ZipFile(f"{RAW}/BD_ENCUCI2020_dbf.zip") as z:
    z.extract("ENCUCI_2020_SEC_4_5.dbf", TMP)
PATH = f"{TMP}/ENCUCI_2020_SEC_4_5.dbf"

campos = ["FAC_SEL", "EST_DIS", "UPM_DIS", "AP5_17", "AP5_18"] + AP16 + [c for c, _ in THETA]
rows = list(dbfmini.read_dbf(PATH, wanted_fields=campos))
print()
print(f"ENCUCI_2020_SEC_4_5.dbf: {len(rows)} filas leidas")

# ---------------------------------------------------------------------
# Guarda de reproduccion: el universo de contacto ya se verifico en
# 2026-08-04-w-coeficientes-generador-paso1.md SS1.1 (13435 de 21519).
# Si esto no coincide, la lectura de AP5_16_1..10 esta mal -- DETENTE
# antes de construir nada sobre ella.
# ---------------------------------------------------------------------
universo = []
for row in rows:
    vals16 = {f: num16(row[f]) for f in AP16}
    if any(v == 1 for v in vals16.values()):
        universo.append((row, vals16))

print(f"universo de contacto (>=1 '1' en AP5_16_1..10) = {len(universo)} de {len(rows)}")
assert len(universo) == 13435, "el universo de contacto NO reproduce el 13435 ya verificado -- DETENTE"
print("Coincide con el 13435 ya verificado. Pipeline de AP5_16_* confirmado.")

# ---------------------------------------------------------------------
# Particion policial / no-policial (ficha SS2)
# ---------------------------------------------------------------------
policial_rows = [row for row, v in universo if v["AP5_16_1"] == 1]
nopolicial_rows = [row for row, v in universo if v["AP5_16_1"] != 1]
assert len(policial_rows) + len(nopolicial_rows) == len(universo)

mixto = sum(1 for row, v in universo
            if v["AP5_16_1"] == 1 and any(vv == 1 for k, vv in v.items() if k != "AP5_16_1"))
print()
print(f"ESTRATO POLICIAL (AP5_16_1==1): n={len(policial_rows)}")
print(f"  con contacto mixto (>=1 otro item de AP5_16 tambien =1): {mixto} "
      f"({mixto/len(policial_rows)*100:.1f}% de policial)")
print(f"ESTRATO NO-POLICIAL (resto del universo, AP5_16_1 in {{2,9}}): n={len(nopolicial_rows)}")

n_prev_p, prev_p = prevalencia_estrato(policial_rows)
n_prev_np, prev_np = prevalencia_estrato(nopolicial_rows)
print()
print("Prevalencia de tramite.mordida.discrecional, agrupada sobre confia (referencia estable):")
print(f"  POLICIAL:    n={n_prev_p}  p={fmt_pct(prev_p['p_hat'])} ic95=[{fmt_pct(prev_p['ic95'][0])}, {fmt_pct(prev_p['ic95'][1])}]")
print(f"  NO-POLICIAL: n={n_prev_np}  p={fmt_pct(prev_np['p_hat'])} ic95=[{fmt_pct(prev_np['ic95'][0])}, {fmt_pct(prev_np['ic95'][1])}]")

# ---------------------------------------------------------------------
# Celdas: 3 items x 2 estratos x 2 niveles de confia
# ---------------------------------------------------------------------
resultados = {}  # (item, estrato) -> dict
veredicto_item = {}

for colname, nombre in THETA:
    print()
    print("=" * 70)
    print(f"{nombre} (`{colname}`)")
    print("=" * 70)
    fila = {}
    for estrato, filas in [("policial", policial_rows), ("no_policial", nopolicial_rows)]:
        n1, out1 = celda(filas, colname, 1)
        n0, out0 = celda(filas, colname, 0)
        sin_soporte = out1 is None or out0 is None
        print(f"  [{estrato}] confia=1: n={n1}" + (" SIN SOPORTE" if out1 is None else f" p={fmt_pct(out1['p_hat'])}"))
        print(f"  [{estrato}] confia=0: n={n0}" + (" SIN SOPORTE" if out0 is None else f" p={fmt_pct(out0['p_hat'])}"))
        if sin_soporte:
            fila[estrato] = {"sin_soporte": True, "n1": n1, "n0": n0}
            print(f"  [{estrato}] beta_hat: SIN SOPORTE (n minimo=30 no alcanzado en algun grupo)")
            continue
        beta, se, ci = beta_de(out1, out0)
        rr, ci_rr, rr_nota = rr_de(out1, out0)
        fila[estrato] = {"sin_soporte": False, "n1": n1, "n0": n0, "beta": beta, "se": se, "ci": ci,
                          "rr": rr, "ci_rr": ci_rr, "rr_nota": rr_nota}
        sig = "significativo (95%)" if (ci[0] > 0 or ci[1] < 0) else "no distinguible de cero"
        print(f"  [{estrato}] beta_hat={fmt_pp(beta)}  ic95=[{fmt_pp(ci[0])}, {fmt_pp(ci[1])}]  ({sig})")
        if rr_nota:
            print(f"  [{estrato}] RR: {rr_nota}")
        else:
            print(f"  [{estrato}] RR={rr:.3f}  ic95=[{ci_rr[0]:.3f}, {ci_rr[1]:.3f}]")
    resultados[colname] = fila

    # -- Falsador SS5: clasificacion DISCREPANTE / ESTABLE, o sin veredicto por n --
    if fila["policial"]["sin_soporte"] or fila["no_policial"]["sin_soporte"]:
        veredicto_item[colname] = "SIN_SOPORTE"
        print("  -> item sin veredicto: al menos una celda SIN SOPORTE")
        continue
    bp, cip = fila["policial"]["beta"], fila["policial"]["ci"]
    bn, cin = fila["no_policial"]["beta"], fila["no_policial"]["ci"]
    signos_opuestos = (bp > 0 and bn < 0) or (bp < 0 and bn > 0)
    sig_p = cip[0] > 0 or cip[1] < 0
    sig_n = cin[0] > 0 or cin[1] < 0
    discrepante = signos_opuestos and (sig_p or sig_n)
    veredicto_item[colname] = "DISCREPANTE" if discrepante else "ESTABLE"
    print(f"  -> {veredicto_item[colname]} "
          f"(signos {'opuestos' if signos_opuestos else 'iguales'}; "
          f"policial {'sig.' if sig_p else 'n.s.'}, no_policial {'sig.' if sig_n else 'n.s.'})")

# ---------------------------------------------------------------------
# Veredicto agregado -- regla de precedencia de la ficha SS5
# ---------------------------------------------------------------------
n_sin_soporte = sum(1 for v in veredicto_item.values() if v == "SIN_SOPORTE")
n_discrepante = sum(1 for v in veredicto_item.values() if v == "DISCREPANTE")
n_estable = sum(1 for v in veredicto_item.values() if v == "ESTABLE")

print()
print("=" * 70)
print("VEREDICTO (regla de precedencia, ficha SS5)")
print("=" * 70)
print(f"items SIN_SOPORTE={n_sin_soporte}  DISCREPANTE={n_discrepante}  ESTABLE={n_estable}  (de 3)")

if n_sin_soporte >= 2:
    veredicto = "INEJECUTABLE POR N"
elif n_discrepante >= 2:
    veredicto = "COMPOSICION POLICIAL CONFIRMADA"
elif n_estable >= 2:
    veredicto = "COMPOSICION POLICIAL DESCARTADA"
else:
    veredicto = "ACOTADA"

print(f"-> {veredicto}")
print()
print("Fin de la corrida.")
