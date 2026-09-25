#!/usr/bin/env python3
"""Genera forense/analisis/donde-cambio/mapa/encig.tsv (fragmento ENCIG del
MAPA DE SERIES, DONDE-CAMBIO §1-2 / ESQUEMA.md).

REGLA DURA DE CEGUERA (B-bis): este script NUNCA lee valores numéricos.
Sólo verifica existencia de llaves RESULT-* en resultados.json (por 'in',
sin indexar el valor) y copia ids de llave, tal cual, a las columnas
result_p/result_lo/result_hi.

Fuente única de series ENCIG con proporción observada por ola + IC:
CALC-ENCIG-SERIE-CANAL-{2015,2017,2019,2021,2023} (conducta C-LUZ-DIGITAL,
spec forense/prereg-caja/ENCIG-SERIE-CANAL-spec-v1_0.md). Se EXCLUYE
CALC-ENCIG-ORIGEN-MOVIL-0001: sus llaves son predicciones/errores de piso
(PERSISTENCIA/TENDENCIA-*), no proporción observada.

Comparabilidad de par: sólo por texto de
data/encig-canal-comparabilidad-texto-v1_0.tsv (regla ESQUEMA.md §2, spec
ENCIG-SERIE-CANAL-spec-v1_0.md §4: 2017,2019 = MISMO-INSTRUMENTO;
2015,2023 = CAMBIO-MENOR; todas contra ancla 2021).
"""
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORRIDA0 = os.path.join(REPO, "data", "corrida0")
COMPARA_TSV = os.path.join(REPO, "data", "encig-canal-comparabilidad-texto-v1_0.tsv")
OUT = os.path.join(REPO, "forense", "analisis", "donde-cambio", "mapa", "encig.tsv")

OLAS = ["2015", "2017", "2019", "2021", "2023"]
INSTRUMENTO = "ENCIG"
DOMINIO = "Trámites y Estado"
CONDUCTA = "C-LUZ-DIGITAL"
UNIDAD = "TRAMITE"

# Celdas del medidor CALC-ENCIG-SERIE-CANAL-<ola>: sufijo de la llave RESULT
# tras 'RESULT-ENCIG-SERIE-<ola>-DIGITAL-' -> (eje, segmento).
# eje usa los mismos nombres que RESULT-ENCIGPIC-DIGITAL-<EJE>-TAU2-FINAL
# (EDAD, ESCOLARIDAD, SEXO); sin eje -> NACIONAL/TOTAL (regla del encargo).
CELDAS = [
    ("ALL-ALL", "NACIONAL", "TOTAL"),
    ("SEXO-1", "SEXO", "1"),
    ("SEXO-2", "SEXO", "2"),
    ("EDAD-18-29", "EDAD", "18-29"),
    ("EDAD-30-44", "EDAD", "30-44"),
    ("EDAD-45-59", "EDAD", "45-59"),
    ("EDAD-60-MAS", "EDAD", "60-MAS"),
    ("ESCOLARIDAD-HASTA-PRIMARIA", "ESCOLARIDAD", "HASTA-PRIMARIA"),
    ("ESCOLARIDAD-SECUNDARIA", "ESCOLARIDAD", "SECUNDARIA"),
    ("ESCOLARIDAD-MEDIA-SUPERIOR", "ESCOLARIDAD", "MEDIA-SUPERIOR"),
    ("ESCOLARIDAD-SUPERIOR", "ESCOLARIDAD", "SUPERIOR"),
]

HEADER = [
    "serie_id", "instrumento", "dominio", "conducta", "conducta_texto",
    "eje", "segmento", "unidad", "ola", "calc",
    "result_p", "result_lo", "result_hi",
    "par_con_anterior", "cita_par", "marca_2020", "nota",
]


def cargar_resultados_keyset(ola):
    """Devuelve el set de LLAVES (nunca valores) de resultados.json de la ola."""
    calc = f"CALC-ENCIG-SERIE-CANAL-{ola}"
    ruta = os.path.join(CORRIDA0, calc, "resultados.json")
    with open(ruta, "r", encoding="utf-8") as f:
        doc = json.load(f)
    return calc, set(doc["resultados"].keys())


def cargar_conducta_texto():
    """Lee sólo la columna conducta_texto de la fila 2021 (ancla) del TSV de
    comparabilidad; es texto descriptivo, no un valor de resultado."""
    with open(COMPARA_TSV, "r", encoding="utf-8") as f:
        filas = [ln.split("\t") for ln in f.read().split("\n") if ln]
    cab = filas[0]
    idx_ola = cab.index("ola")
    idx_texto = cab.index("conducta_texto")
    for fila in filas[1:]:
        if fila[idx_ola] == "2021":
            return fila[idx_texto]
    return ""


def cargar_veredictos_vs_ancla():
    """ola -> veredicto contra el ancla (2021), y la fila del TSV (para cita)."""
    with open(COMPARA_TSV, "r", encoding="utf-8") as f:
        lineas = [ln for ln in f.read().split("\n") if ln]
    filas = [ln.split("\t") for ln in lineas]
    cab = filas[0]
    idx_ola = cab.index("ola")
    idx_ver = cab.index("veredicto")
    out = {}
    n = 1  # fila de cabecera cuenta como 1; primer dato es fila 2
    for i, fila in enumerate(filas[1:], start=2):
        out[fila[idx_ola]] = {"veredicto": fila[idx_ver], "fila_tsv": i}
    return out


ORDEN_ESTADO = {
    "NO-COMPARABLE": 3,
    "NO-DOCUMENTADO": 2,
    "CAMBIO-DOCUMENTADO": 1,
    "COMPARABLE": 0,
}

VS_ANCLA_A_ESTADO = {
    "MISMO-INSTRUMENTO": "OK",
    "CAMBIO-MENOR": "OK",
    "CAMBIO-DE-INSTRUMENTO": "CAMBIO-DOCUMENTADO",
    "NO-COMPARABLE": "NO-COMPARABLE",
}


def estado_par(ola_a, ola_b, veredictos):
    """Regla ESQUEMA.md §2 aplicada contra el ancla 2021 (spec
    ENCIG-SERIE-CANAL-spec-v1_0.md §4: única fuente de comparabilidad
    disponible para C-LUZ-DIGITAL es el TSV de veredictos vs ancla)."""
    va = veredictos.get(ola_a)
    vb = veredictos.get(ola_b)
    if va is None or vb is None:
        return "NO-DOCUMENTADO", f"{os.path.basename(COMPARA_TSV)}: sin fila para {ola_a} o {ola_b}"
    ea = VS_ANCLA_A_ESTADO.get(va["veredicto"], "NO-DOCUMENTADO")
    eb = VS_ANCLA_A_ESTADO.get(vb["veredicto"], "NO-DOCUMENTADO")
    if ea == "NO-COMPARABLE" or eb == "NO-COMPARABLE":
        estado = "NO-COMPARABLE"
    elif ea == "OK" and eb == "OK":
        estado = "COMPARABLE"
    else:
        estado = "NO-DOCUMENTADO"
    cita = (
        f"{os.path.basename(COMPARA_TSV)}: filas {va['fila_tsv']} (ola {ola_a}, "
        f"veredicto {va['veredicto']}) y {vb['fila_tsv']} (ola {ola_b}, "
        f"veredicto {vb['veredicto']}) contra ancla 2021"
    )
    return estado, cita


def marca_2020(ola_a, ola_b):
    # Ninguna ola de la serie ENCIG-C-LUZ-DIGITAL es 2020 ni el texto
    # sellado la refiere como periodo de referencia (cada ola pregunta
    # "durante este año (<ola>)"); SI sólo si a o b == '2020'.
    return "SI" if ola_a == "2020" or ola_b == "2020" else "NO"


def main():
    conducta_texto = cargar_conducta_texto()
    veredictos = cargar_veredictos_vs_ancla()

    keysets = {}
    calc_por_ola = {}
    for ola in OLAS:
        calc, keys = cargar_resultados_keyset(ola)
        calc_por_ola[ola] = calc
        keysets[ola] = keys

    filas = []
    for sufijo, eje, segmento in CELDAS:
        serie_id = f"{INSTRUMENTO}-{CONDUCTA}-{eje}-{segmento}".upper()
        for i, ola in enumerate(OLAS):
            pref = f"RESULT-ENCIG-SERIE-{ola}-DIGITAL-{sufijo}"
            id_p = f"{pref}-P"
            id_lo = f"{pref}-IC-LO"
            id_hi = f"{pref}-IC-HI"
            keys = keysets[ola]
            result_p = id_p if id_p in keys else ""
            result_lo = id_lo if id_lo in keys else ""
            result_hi = id_hi if id_hi in keys else ""

            if i == 0:
                par_con_anterior = "PRIMERA"
                cita_par = ""
                marca = "NO"
            else:
                ola_a = OLAS[i - 1]
                par_con_anterior, cita_par = estado_par(ola_a, ola, veredictos)
                marca = marca_2020(ola_a, ola)

            nota = ""
            if not result_p:
                nota = "sin RESULT-P para esta celda/ola"

            filas.append([
                serie_id, INSTRUMENTO, DOMINIO, CONDUCTA, conducta_texto,
                eje, segmento, UNIDAD, ola, calc_por_ola[ola],
                result_p, result_lo, result_hi,
                par_con_anterior, cita_par, marca, nota,
            ])

    filas.sort(key=lambda r: (r[0], r[8]))

    lineas = ["\t".join(HEADER)]
    for fila in filas:
        lineas.append("\t".join(fila))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print(f"escrito {OUT}: {len(filas)} filas, {len(CELDAS)} series")


if __name__ == "__main__":
    main()
