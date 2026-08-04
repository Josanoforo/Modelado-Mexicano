#!/usr/bin/env python3
"""R5.1 -- Volatilidad + ausencia de Estado -> familia como seguro.

Falsador: tras la universalizacion de la Pension del Bienestar, ¿retrocede
el seguro familiar (corresidencia intergeneracional / transferencias
intrafamiliares hacia mayores) en hogares beneficiarios frente a no
beneficiarios comparables?

Pipeline reproducible sobre las 6 olas ENIGH (2012, 2014, 2016, 2018, 2020,
2022) leidas directamente de los zips en data/raw/ (sin extraer a disco).
No usa pandas/numpy (no estan instalados en este entorno) -- solo csv y
zipfile de la libreria estandar, mas tests/svystat.py (estimador de
conglomerado ultimo ya validado en ese archivo contra un caso SRS conocido).

Variable de beneficiario: tabla `ingresos`, columna `clave`.
  2012, 2014: P044 = "Beneficio del programa 70 y mas"
  2016, 2018: P044 = "Beneficio del programa 65 y mas"
  2020, 2022: P104 = "Programa para el Bienestar de las Personas Adultas Mayores"
(mismo codigo de columna en las 6 olas; el catalogo de `clave` renombra el
programa -- verificado leyendo ingresos_cat.csv / ingreso.csv de cada ola,
no supuesto).

No se usa `bene_gob` (concentradohogar): agrega P043,P045,P048,P101..P108 --
mezcla la pension de adultos mayores con becas juveniles y otros programas,
confirmado leyendo su formula en el diccionario de datos. Usar `bene_gob`
como proxy de "recibe Pension del Bienestar" habria sido el mismo error que
el hallazgo I-18/ADR-30 ya registrado en el corpus para otras fuentes.

Transferencia intrafamiliar hacia mayores: tabla `ingresos`, clave P040
("Donativos en dinero provenientes de otros hogares"), restringido a
receptores con edad >= 65 (tabla `poblacion`, join por folioviv+foliohog+numren).
P040 no distingue si el donante es familiar o no -- limite documentado, no
resuelto por el instrumento (misma naturaleza de reserva que `redsoc` en la
nota de segmentacion, aunque aqui la clave si es monetaria y aislable, cosa
que `redsoc` no es).

Corresidencia intergeneracional: `concentradohogar.clase_hog` en
{3 Ampliado, 4 Compuesto} (definicion identica y estable en las 6 olas,
verificado contra el diccionario de datos de 2012 y de 2022 palabra por
palabra).

Universo de analisis: hogares con concentradohogar.p65mas >= 1 (al menos un
integrante de 65 anios o mas).
"""
import csv
import io
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svystat import prop_ultimate_cluster  # noqa: E402

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

WAVES = {
    2012: dict(
        zip_name="enigh2012_nc_csv.zip",
        ch="concentradohogar_enigh2012ncv/conjunto_de_datos/concentradohogar.csv",
        pob="poblacion_enigh2012ncv/conjunto_de_datos/poblacion.csv",
        ing="ingresos_enigh2012ncv/conjunto_de_datos/ingresos.csv",
        weight_col="factor_hog",
        design_in_ingresos=False,
        pension_claves={"P044"},
        pension_label="Beneficio del programa 70 y mas",
    ),
    2014: dict(
        zip_name="enigh2014_nc_csv.zip",
        ch="concentradohogar_enigh2014ncv/conjunto_de_datos/concentradohogar.csv",
        pob="poblacion_enigh2014ncv/conjunto_de_datos/poblacion.csv",
        ing="ingresos_enigh2014ncv/conjunto_de_datos/ingresos.csv",
        weight_col="factor_hog",
        design_in_ingresos=False,
        pension_claves={"P044"},
        pension_label="Beneficio del programa 70 y mas",
    ),
    2016: dict(
        zip_name="enigh2016_nc_csv.zip",
        ch="conjunto_de_datos_concentradohogar_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2016_ns.csv",
        pob="conjunto_de_datos_poblacion_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh_2016_ns.csv",
        ing="conjunto_de_datos_ingresos_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh_2016_ns.csv",
        weight_col="factor",
        design_in_ingresos=True,
        pension_claves={"P044"},
        pension_label="Beneficio del programa 65 y mas",
    ),
    2018: dict(
        zip_name="enigh2018_nc_csv.zip",
        ch="conjunto_de_datos_concentradohogar_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2018_ns.csv",
        pob="conjunto_de_datos_poblacion_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh_2018_ns.csv",
        ing="conjunto_de_datos_ingresos_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh_2018_ns.csv",
        weight_col="factor",
        design_in_ingresos=True,
        pension_claves={"P044"},
        pension_label="Beneficio del programa 65 y mas",
    ),
    2020: dict(
        zip_name="enigh2020_nc_csv.zip",
        ch="conjunto_de_datos_concentradohogar_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh_2020_ns.csv",
        pob="conjunto_de_datos_poblacion_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh_2020_ns.csv",
        ing="conjunto_de_datos_ingresos_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh_2020_ns.csv",
        weight_col="factor",
        design_in_ingresos=True,
        pension_claves={"P104"},
        pension_label="Programa para el Bienestar de las Personas Adultas Mayores",
    ),
    2022: dict(
        zip_name="enigh2022_nc_csv.zip",
        ch="conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2022_ns.csv",
        pob="conjunto_de_datos_poblacion_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh2022_ns.csv",
        ing="conjunto_de_datos_ingresos_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh2022_ns.csv",
        weight_col="factor",
        design_in_ingresos=True,
        pension_claves={"P104"},
        pension_label="Programa para el Bienestar de las Personas Adultas Mayores",
    ),
}

TRANSFER_CLAVE = "P040"
CORRESIDENCIA_CLASES = {"3", "4"}  # Ampliado, Compuesto
EDAD_MAYOR = 65


def _reader(z, path):
    with z.open(path) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace")
        yield from csv.DictReader(text)


def procesar_ola(year):
    cfg = WAVES[year]
    zpath = RAW / cfg["zip_name"]
    z = zipfile.ZipFile(zpath)

    hogares = {}
    for row in _reader(z, cfg["ch"]):
        key = (row["folioviv"], row["foliohog"])
        hogares[key] = {
            "est_dis": row["est_dis"],
            "upm": row["upm"],
            "factor": float(row[cfg["weight_col"]]),
            "clase_hog": row["clase_hog"],
            "tam_loc": row["tam_loc"],
            "ing_cor": float(row["ing_cor"]),
            "ingtrab": float(row["ingtrab"]),
            "gasto_mon": float(row["gasto_mon"]),
            "tot_integ": int(row["tot_integ"]),
            "p65mas": int(row["p65mas"]),
            "beneficiario": False,
            "monto_pension_tri": 0.0,
            "transferencia_mayor": False,
            "monto_transferencia_mayor_tri": 0.0,
        }

    # edad por persona, solo necesaria para atribuir receptor de P040 a mayor/no-mayor
    edad_persona = {}
    for row in _reader(z, cfg["pob"]):
        key = (row["folioviv"], row["foliohog"], row["numren"])
        try:
            edad_persona[key] = int(row["edad"])
        except (ValueError, KeyError):
            pass

    for row in _reader(z, cfg["ing"]):
        hkey = (row["folioviv"], row["foliohog"])
        hh = hogares.get(hkey)
        if hh is None:
            continue
        clave = row["clave"]
        try:
            ing_tri = float(row["ing_tri"])
        except ValueError:
            ing_tri = 0.0
        if ing_tri <= 0:
            continue
        if clave in cfg["pension_claves"]:
            hh["beneficiario"] = True
            hh["monto_pension_tri"] += ing_tri
        elif clave == TRANSFER_CLAVE:
            pkey = (row["folioviv"], row["foliohog"], row["numren"])
            edad = edad_persona.get(pkey)
            if edad is not None and edad >= EDAD_MAYOR:
                hh["transferencia_mayor"] = True
                hh["monto_transferencia_mayor_tri"] += ing_tri

    return hogares


def _prop(rows_iter, cond):
    rows = [
        (hh["est_dis"], hh["upm"], hh["factor"], 1 if cond(hh) else 0)
        for hh in rows_iter
    ]
    if not rows:
        return None
    return prop_ultimate_cluster(rows)


def validar_contra_publicado():
    """Valida el pipeline de lectura+ponderacion contra cifras publicadas por
    el INEGI en el Comunicado de Prensa 420/23 (26/jul/2023, ENIGH 2022),
    Cuadro 1 y Cuadro de composicion de ingresos -- no el caso sintetico SRS
    que ya trae tests/svystat.py (eso valida la formula de varianza; esto
    valida que el join de folioviv+foliohog, la columna de peso y los campos
    leidos son los correctos contra un numero real, publicado, reproducible).
    """
    cfg = WAVES[2022]
    z = zipfile.ZipFile(RAW / cfg["zip_name"])
    n = 0
    sum_factor = sum_bene_gob = sum_donativos = sum_jubilacion = 0.0
    for row in _reader(z, cfg["ch"]):
        w = float(row["factor"])
        sum_factor += w
        sum_bene_gob += w * float(row["bene_gob"])
        sum_donativos += w * float(row["donativos"])
        sum_jubilacion += w * float(row["jubilacion"])
        n += 1

    casos = [
        ("Total de hogares (sum factor)", sum_factor, 37_560_123),
        ("bene_gob promedio ponderado", sum_bene_gob / sum_factor, 1_777),
        ("donativos promedio ponderado", sum_donativos / sum_factor, 1_271),
        ("jubilacion promedio ponderado", sum_jubilacion / sum_factor, 5_169),
    ]
    print(f"n hogares ENIGH 2022 sin ponderar = {n}")
    ok = True
    for nombre, calc, publicado in casos:
        rel = abs(calc - publicado) / publicado
        estado = "OK" if rel < 0.001 else "FALLA"
        if estado == "FALLA":
            ok = False
        print(f"  {estado} -- {nombre}: calculado={calc:,.1f} publicado={publicado:,} (dif rel {rel*100:.3f}%)")
    print("Fuente: INEGI, Comunicado de Prensa Num. 420/23, 26/jul/2023, Cuadro 1 y cuadro de composicion de ingreso corriente.")
    if not ok:
        raise SystemExit("Validacion contra cifra publicada FALLO -- no usar el pipeline sin corregir.")
    print("Validado contra caso conocido publicado.")


def resumen_ola(year):
    hogares = procesar_ola(year)
    universo = [hh for hh in hogares.values() if hh["p65mas"] >= 1]
    benef = [hh for hh in universo if hh["beneficiario"]]
    no_benef = [hh for hh in universo if not hh["beneficiario"]]

    out = {
        "year": year,
        "pension_clave": sorted(WAVES[year]["pension_claves"]),
        "pension_label": WAVES[year]["pension_label"],
        "n_hogares_total_sin_ponderar": len(hogares),
        "n_hogares_con_mayor_sin_ponderar": len(universo),
        "n_hogares_con_mayor_ponderado": sum(hh["factor"] for hh in universo),
        "n_benef_sin_ponderar": len(benef),
        "n_benef_ponderado": sum(hh["factor"] for hh in benef),
        "n_no_benef_sin_ponderar": len(no_benef),
        "n_no_benef_ponderado": sum(hh["factor"] for hh in no_benef),
        "corresidencia_benef": _prop(benef, lambda h: h["clase_hog"] in CORRESIDENCIA_CLASES),
        "corresidencia_no_benef": _prop(no_benef, lambda h: h["clase_hog"] in CORRESIDENCIA_CLASES),
        "transferencia_benef": _prop(benef, lambda h: h["transferencia_mayor"]),
        "transferencia_no_benef": _prop(no_benef, lambda h: h["transferencia_mayor"]),
        "monto_pension_tri_prom": (
            sum(h["monto_pension_tri"] * h["factor"] for h in benef)
            / sum(h["factor"] for h in benef)
            if benef
            else None
        ),
        "ing_cor_prom_benef": (
            sum(h["ing_cor"] * h["factor"] for h in benef) / sum(h["factor"] for h in benef)
            if benef
            else None
        ),
        "ing_cor_prom_no_benef": (
            sum(h["ing_cor"] * h["factor"] for h in no_benef) / sum(h["factor"] for h in no_benef)
            if no_benef
            else None
        ),
        "ingtrab_prom_benef": (
            sum(h["ingtrab"] * h["factor"] for h in benef) / sum(h["factor"] for h in benef)
            if benef
            else None
        ),
        "ingtrab_prom_no_benef": (
            sum(h["ingtrab"] * h["factor"] for h in no_benef) / sum(h["factor"] for h in no_benef)
            if no_benef
            else None
        ),
    }
    return out


def _weighted_tercile_cuts(rows):
    """rows: list de (factor, valor). Devuelve (corte1, corte2) ponderados."""
    rows = sorted(rows, key=lambda r: r[1])
    total = sum(w for w, _ in rows)
    targets = [total / 3, 2 * total / 3]
    cuts = []
    acc = 0.0
    ti = 0
    for w, v in rows:
        acc += w
        while ti < len(targets) and acc >= targets[ti]:
            cuts.append(v)
            ti += 1
    while len(cuts) < 2:
        cuts.append(rows[-1][1] if rows else 0.0)
    return cuts[0], cuts[1]


def resumen_ola_estratificado(year):
    """Comparacion beneficiario/no-beneficiario dentro de terciles de ingtrab
    PER CAPITA (ingtrab / tot_integ), no del total del hogar -- el total del
    hogar esta mecanicamente inflado en hogares Ampliado/Compuesto (mas
    integrantes = mas perceptores potenciales = mayor ingtrab total), lo que
    confundiria la propia variable de control con el desenlace de corresidencia.
    Verificado en una corrida previa de este script: estratificar por ingtrab
    total producia una asociacion corresidencia~tercil casi mecanica (15% en
    T1 a 70%+ en T3) que es en gran parte composicion de hogar, no ingreso.
    Per capita es el control de comparabilidad declarado en el acto (PP-3/2.5).
    """
    hogares = procesar_ola(year)
    universo = [hh for hh in hogares.values() if hh["p65mas"] >= 1]
    for hh in universo:
        hh["ingtrab_pc"] = hh["ingtrab"] / hh["tot_integ"] if hh["tot_integ"] else 0.0
    c1, c2 = _weighted_tercile_cuts([(hh["factor"], hh["ingtrab_pc"]) for hh in universo])

    def tercil(hh):
        if hh["ingtrab_pc"] <= c1:
            return "T1 (bajo)"
        if hh["ingtrab_pc"] <= c2:
            return "T2 (medio)"
        return "T3 (alto)"

    out = {"year": year, "cortes_ingtrab_tri": (c1, c2), "estratos": {}}
    for nombre in ["T1 (bajo)", "T2 (medio)", "T3 (alto)"]:
        sub = [hh for hh in universo if tercil(hh) == nombre]
        benef = [hh for hh in sub if hh["beneficiario"]]
        no_benef = [hh for hh in sub if not hh["beneficiario"]]
        out["estratos"][nombre] = {
            "n_benef": len(benef),
            "n_no_benef": len(no_benef),
            "corresidencia_benef": _prop(benef, lambda h: h["clase_hog"] in CORRESIDENCIA_CLASES),
            "corresidencia_no_benef": _prop(no_benef, lambda h: h["clase_hog"] in CORRESIDENCIA_CLASES),
            "transferencia_benef": _prop(benef, lambda h: h["transferencia_mayor"]),
            "transferencia_no_benef": _prop(no_benef, lambda h: h["transferencia_mayor"]),
        }
    return out


def _fmt_prop(p):
    if p is None:
        return "NA"
    lo, hi = p["ic95"]
    return f"{p['p_hat']*100:.1f}% (n_upm={p['n_upm_total']}, IC95 [{lo*100:.1f},{hi*100:.1f}])"


if __name__ == "__main__":
    if "--validar" in sys.argv:
        validar_contra_publicado()
        sys.exit(0)
    args = [a for a in sys.argv[1:] if a != "--estratos"]
    years = [int(a) for a in args] or sorted(WAVES)
    for y in years:
        r = resumen_ola(y)
        print(f"\n=== ENIGH {y} -- clave {r['pension_clave']} ({r['pension_label']}) ===")
        print(f"hogares totales (sin ponderar): {r['n_hogares_total_sin_ponderar']}")
        print(
            f"hogares con >=1 integrante 65+ : {r['n_hogares_con_mayor_sin_ponderar']} sin ponderar"
            f" / {r['n_hogares_con_mayor_ponderado']:,.0f} ponderado"
        )
        print(
            f"  beneficiarios    : {r['n_benef_sin_ponderar']} sin ponderar / {r['n_benef_ponderado']:,.0f} ponderado"
        )
        print(
            f"  no beneficiarios : {r['n_no_benef_sin_ponderar']} sin ponderar / {r['n_no_benef_ponderado']:,.0f} ponderado"
        )
        print(f"corresidencia (Ampliado+Compuesto) -- beneficiarios   : {_fmt_prop(r['corresidencia_benef'])}")
        print(f"corresidencia (Ampliado+Compuesto) -- no beneficiarios: {_fmt_prop(r['corresidencia_no_benef'])}")
        print(f"transferencia P040 hacia mayor -- beneficiarios       : {_fmt_prop(r['transferencia_benef'])}")
        print(f"transferencia P040 hacia mayor -- no beneficiarios    : {_fmt_prop(r['transferencia_no_benef'])}")
        if r["monto_pension_tri_prom"] is not None:
            print(f"monto pension trimestral promedio (beneficiarios): ${r['monto_pension_tri_prom']:,.0f}")
        print(f"ing_cor promedio -- beneficiarios: ${r['ing_cor_prom_benef']:,.0f} | no beneficiarios: ${r['ing_cor_prom_no_benef']:,.0f}")
        print(f"ingtrab promedio -- beneficiarios: ${r['ingtrab_prom_benef']:,.0f} | no beneficiarios: ${r['ingtrab_prom_no_benef']:,.0f}")

        if "--estratos" in sys.argv or len(sys.argv) == 1:
            e = resumen_ola_estratificado(y)
            c1, c2 = e["cortes_ingtrab_tri"]
            print(f"-- estratificado por tercil de ingtrab trimestral (cortes ${c1:,.0f} / ${c2:,.0f}) --")
            for nombre, d in e["estratos"].items():
                print(f"  {nombre}: n_benef={d['n_benef']} n_no_benef={d['n_no_benef']}")
                print(f"    corresidencia benef={_fmt_prop(d['corresidencia_benef'])} | no_benef={_fmt_prop(d['corresidencia_no_benef'])}")
                print(f"    transferencia benef={_fmt_prop(d['transferencia_benef'])} | no_benef={_fmt_prop(d['transferencia_no_benef'])}")
