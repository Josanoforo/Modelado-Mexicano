#!/usr/bin/env python3
"""Construye forense/analisis/donde-cambio/mapa/enigh.tsv (fragmento ENIGH
del mapa de series de DONDE-CAMBIO-spec-v1_0 §1-2, ver ESQUEMA.md).

REGLA DURA DE CEGUERA (B-bis): nunca se leen valores numéricos de
punto/IC/tau2/cobertura/error. Del catálogo sólo se usan las columnas de
texto/ids (1-8,12-23, saltando 9,10,11,24). De resultados.json sólo se usan
las LLAVES del dict `resultados`.

Fuentes:
- canon/catalogo-del-mexicano-v1_0.tsv (filas instrumento_ola ~ ENIGH *)
- data/enigh-comparabilidad-texto-v1_0.tsv: veredicto POR VARIABLE contra el
  ancla 2022 (no por conducta, no por par consecutivo)
- forense/prereg-caja/ENIGH-SERIE-OLAS-ABIERTAS-spec-v1_0.md §2-3: fuente de
  TEXTO equivalente y más fuerte para los pares consecutivos 2016-2018 y
  2018-2020 (no cubiertos por la tabla de variables, que sólo compara contra
  2022): declara que los 9 CALC de 2016/2018/2020 son "el mismo procedimiento
  estadístico" del sellado 2022, "parametrizado por ola" (mismo universo,
  filtros, ponderador, transformación, categorías, método, semilla y
  tolerancia), y que el oro-check reproduce 2022 byte-exacto desde el mismo
  medidor.py congelado -- es decir, el procedimiento es literalmente el mismo
  entre las cuatro olas, no sólo cada una contra 2022.
- data/corrida0/CALC-ENIGH<ola>-*-0001/resultados.json (sólo llaves)

Series que entran (§1 universo, filtro por definición de proporción):
- ENIGH-INTENSIDAD-REMESAS: 4 conductas con unidad_escala == "proporcion"
  (participacion agregada, participacion ge50, participacion media hogar,
  prevalencia), cada una con 4 olas (2016,2018,2020,2022). "remesas media" y
  "remesas mediana" están en PESOS, no son proporción por definición ->
  EXCLUIDAS (anotado).
- Filas de una sola ola (recibe_remesas/no_recibe_remesas, sólo ENIGH 2022;
  R/FAM-M-05..07, cada una en una sola ola con segmento distinto) -> listadas
  con par_con_anterior=PRIMERA en su única fila (§1: "una sola ola" no se
  dictamina SIN-SERIE con más lectura en esta tabla -- eso es el estado del
  CALC-<INST>-SERIE-DICTAMEN, no de este mapa; aquí basta con que el mapa las
  liste, k=1, una sola fila).
"""
import json
import os
import sys
from collections import defaultdict

REPO = "/home/pc0/mm-gen2-donde-cambio-el-mexicano-1"
CATALOGO = os.path.join(REPO, "canon/catalogo-del-mexicano-v1_0.tsv")
CORRIDA0 = os.path.join(REPO, "data/corrida0")
OUT = os.path.join(REPO, "forense/analisis/donde-cambio/mapa/enigh.tsv")
CITA_SPEC = "forense/prereg-caja/ENIGH-SERIE-OLAS-ABIERTAS-spec-v1_0.md:§2-§3"

HEADER = [
    "serie_id", "instrumento", "dominio", "conducta", "conducta_texto", "eje",
    "segmento", "unidad", "ola", "calc", "result_p", "result_lo", "result_hi",
    "par_con_anterior", "cita_par", "marca_2020", "nota",
]

CAT_SAFE_COLS = list(range(1, 9)) + list(range(12, 24))
CAT_FIELDS = [
    "area_consulta", "llave", "dominio", "conducta", "instrumento_ola",
    "segmento", "universo_denominador", "unidad_escala", "naturaleza_ic",
    "estado_adopcion", "firma", "temporalidad", "result_punto", "result_inf",
    "result_sup", "calc", "sha256_resultados", "sha256_sello", "uso",
    "oferta_compatible",
]

OLA_NUM = {"ENIGH 2016": 2016, "ENIGH 2018": 2018, "ENIGH 2020": 2020, "ENIGH 2022": 2022}

REMINT_PROPORCION = {
    "participacion agregada de remesas",
    "participacion ge50 de remesas",
    "participacion media hogar de remesas",
    "prevalencia de remesas",
}
REMINT_EXCLUIDA = {"remesas media de remesas", "remesas mediana de remesas"}


def leer_tsv_seguro(path, cols_1idx):
    with open(path, encoding="utf-8") as f:
        filas = [l.rstrip("\n").split("\t") for l in f]
    header = filas[0]
    idx = [i - 1 for i in cols_1idx]
    out = []
    for fila in filas[1:]:
        while len(fila) < len(header):
            fila.append("")
        out.append([fila[i] for i in idx])
    return out


def llaves_result(calc):
    path = os.path.join(CORRIDA0, calc, "resultados.json")
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    r = d.get("resultados")
    if isinstance(r, dict):
        return set(r.keys())
    return set()


def main():
    cat_raw = leer_tsv_seguro(CATALOGO, CAT_SAFE_COLS)
    rows = [dict(zip(CAT_FIELDS, r)) for r in cat_raw]
    enigh_rows = [r for r in rows if r["instrumento_ola"].startswith("ENIGH ")]

    calc_keys_cache = {}

    def keys_de(calc):
        if calc not in calc_keys_cache:
            calc_keys_cache[calc] = llaves_result(calc)
        return calc_keys_cache[calc]

    # --- REMINT: agrupa por conducta (texto exacto), las 5 conductas ---
    # Ninguna fila se excluye por escala (corrección de mesa): remesas
    # media/mediana están en PESOS, no proporción -- se listan igual con
    # nota FUERA-DE-ESCALA-(0,1); el CALC de dictamen las resuelve SIN-SERIE
    # por spec §2 (k cuenta sólo olas con p,lo,hi en (0,1)).
    remint = [r for r in enigh_rows if r["uso"] == "ENIGH-INTENSIDAD-REMESAS"]
    series_remint = defaultdict(list)  # conducta -> [(ola_num, row)]
    fuera_escala_n = 0
    for r in remint:
        if r["conducta"] in REMINT_EXCLUIDA:
            fuera_escala_n += 1
        series_remint[r["conducta"]].append((OLA_NUM[r["instrumento_ola"]], r))

    out_rows = []
    n_series = 0
    for conducta, items in series_remint.items():
        items.sort(key=lambda t: t[0])
        n_series += 1
        for i, (ola_num, r) in enumerate(items):
            keys = keys_de(r["calc"])
            rp = r["result_punto"] if r["result_punto"] in keys else ""
            rlo = r["result_inf"] if r["result_inf"] and r["result_inf"] in keys else ""
            rhi = r["result_sup"] if r["result_sup"] and r["result_sup"] in keys else ""
            nota_falta = "" if rp or not r["result_punto"] else " result_punto NO está en resultados.json del CALC (declarado)."
            nota_escala = " FUERA-DE-ESCALA-(0,1)." if r["conducta"] in REMINT_EXCLUIDA else ""
            marca_2020 = "SI" if ola_num == 2020 else "NO"
            if i > 0 and items[i - 1][0] == 2020:
                marca_2020 = "SI"

            if i == 0:
                par, cita, nota = "PRIMERA", "", "Primera ola de la serie." + nota_escala + nota_falta
            else:
                ola_ant = items[i - 1][0]
                par = "COMPARABLE"
                cita = CITA_SPEC
                nota = (("Par (%d,%d): %s declara que los CALC de 2016/2018/2020 son el mismo "
                         "procedimiento estadístico del sellado 2022, byte-exacto por oro-check "
                         "(mismo universo/filtros/ponderador/metodo/semilla/tolerancia)."
                         ) % (ola_ant, ola_num, CITA_SPEC)) + nota_escala + nota_falta

            serie_id = "ENIGH-REMINT-NACIONAL-%s" % (conducta.upper().replace(" ", "_"))
            out_rows.append([
                serie_id, "ENIGH", r["dominio"], conducta, r["universo_denominador"][:2000],
                "NACIONAL", "TOTAL", r["unidad_escala"], str(ola_num), r["calc"], rp, rlo, rhi,
                par, cita, marca_2020, nota,
            ])

    # --- filas de una sola ola (SIN-SERIE en el dictamen, pero se listan
    #     aquí con k=1, PRIMERA, tal como exige §1: toda conducta con RESULT
    #     en el catálogo entra al universo) ---
    resto = [r for r in enigh_rows if r["uso"] != "ENIGH-INTENSIDAD-REMESAS"]
    conteo_por_llave_conducta = defaultdict(list)
    for r in resto:
        # serie_id por (conducta, segmento): cada FAM-M-xx es un segmento
        # distinto (identidad de llave, no de rótulo), y recibe/no_recibe
        # remesas sólo tienen ENIGH 2022 en el catálogo.
        conteo_por_llave_conducta[(r["conducta"], r["segmento"])].append(r)

    n_unicas = 0
    for (conducta, segmento), items in conteo_por_llave_conducta.items():
        # cada conducta/segmento de "resto" aparece en una sola ola en el
        # catálogo -- se verifica, no se presume
        olas = sorted(set(OLA_NUM[r["instrumento_ola"]] for r in items))
        if len(olas) != 1:
            print("AVISO: %s/%s tiene %d olas, revisar manualmente: %s" % (
                conducta, segmento, len(olas), olas), file=sys.stderr)
        for r in items:
            n_unicas += 1
            ola_num = OLA_NUM[r["instrumento_ola"]]
            keys = keys_de(r["calc"])
            rp = r["result_punto"] if r["result_punto"] in keys else ""
            rlo = r["result_inf"] if r["result_inf"] and r["result_inf"] in keys else ""
            rhi = r["result_sup"] if r["result_sup"] and r["result_sup"] in keys else ""
            nota_falta = "" if rp or not r["result_punto"] else " result_punto NO está en resultados.json del CALC (declarado)."
            marca_2020 = "SI" if ola_num == 2020 else "NO"
            serie_id = "ENIGH-%s-NACIONAL-%s" % (
                conducta.upper().replace(" ", "_"), segmento.upper().replace(" ", "_").replace(";", "").replace(",", ""))
            out_rows.append([
                serie_id, "ENIGH", r["dominio"], conducta, r["universo_denominador"][:2000],
                "NACIONAL", segmento, r["unidad_escala"], str(ola_num), r["calc"], rp, rlo, rhi,
                "PRIMERA", "", marca_2020,
                "Única ola con RESULT para esta serie en el catálogo (k=1)." + nota_falta,
            ])

    out_rows.sort(key=lambda row: (row[0], int(row[8])))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\t".join(HEADER) + "\n")
        for row in out_rows:
            f.write("\t".join(row) + "\n")

    print("ENIGH: %d filas (%d REMINT en %d series + %d de una sola ola), %d filas REMINT FUERA-DE-ESCALA-(0,1) (listadas igual)" % (
        len(out_rows), sum(len(v) for v in series_remint.values()), n_series, n_unicas, fuera_escala_n), file=sys.stderr)


if __name__ == "__main__":
    main()
