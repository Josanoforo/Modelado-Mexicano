#!/usr/bin/env python3
"""Construye forense/analisis/donde-cambio/mapa/enut.tsv (fragmento ENUT del
mapa de series de DONDE-CAMBIO-spec-v1_0 §1-2, ver ESQUEMA.md).

REGLA DURA DE CEGUERA (B-bis): este script NUNCA lee valores numéricos de
punto/IC/tau2/cobertura/error. Del catálogo sólo se usan las columnas de
texto/ids (1-8,12-23, es decir, se saltan 9,10,11 [punto,ic95_inf,ic95_sup]
y 24 [oferta_valor_ic]). De resultados.json sólo se usan las LLAVES del
dict `resultados` (nunca sus valores).

Fuentes (ids/texto únicamente):
- canon/catalogo-del-mexicano-v1_0.tsv (filas instrumento_ola ~ ENUT *)
- data/enut-comparabilidad-texto-v1_0.tsv (veredictos por ola contra ancla
  2024, columna `veredicto`; NUNCA valores)
- data/corrida0/<calc>/resultados.json (sólo llaves de `resultados`, para
  verificar que result_p/lo/hi existen)

Reglas de agrupación (derivadas del propio patrón de las llaves RESULT, que
codifica variante-eje-categoria; verificado contra
data/enut-comparabilidad-texto-v1_0.tsv, conductas C1..C5/E):
  CONCP  = C1 (definición 2024, sólo existe en ENUT 2024)
  NUCLEO = C2 (núcleo común 2014/2019/2024; no construible en 2009 -- lo
           declara la fila C4/2009 de la tabla de comparabilidad)
  MIN    = C3 (núcleo mínimo, las 4 olas 2009/2014/2019/2024)
  RAZON-<variante> = C4 (razón reparto_hogar sobre la variante dada)
  RESULT-ENUT-A-R = fila suelta de CALC-ENUT-0001 (misma familia C1/C4 pero
           llave distinta; se trata como su propia serie, por identidad de
           llave, no por rótulo -- sólo tiene ola 2024)

Escala (0,1): NINGUNA fila se excluye del mapa por su escala -- la tabla
final exige una fila por (conducta, segmento) con dictamen (el CALC de
dictamen decide SIN-SERIE por spec §2, que cuenta sólo olas con p,lo,hi en
(0,1)). MIN/NUCLEO/CONCP miden horas/semana (unidad_escala explícita en el
catálogo, no [0,1]/(0,1)): se listan igual, con nota `FUERA-DE-ESCALA-(0,1)`.
Las RAZON declaran "[0,1]" explícito en unidad_escala.

par_con_anterior (regla del ESQUEMA.md, literal): "las dos olas del par con
MISMO-INSTRUMENTO o CAMBIO-MENOR contra el ancla (el ancla misma cuenta como
MISMO) -> COMPARABLE; alguna de las dos con CAMBIO-DE-INSTRUMENTO -> CAMBIO-
DOCUMENTADO". data/enut-comparabilidad-texto-v1_0.tsv dictamina cada ola
CONTRA EL ANCLA 2024 -- exactamente lo que esa regla consume para CUALQUIER
par consecutivo (a,b): se leen las dos filas (código, a) y (código, b) de la
tabla (ambas contra el ancla 2024) y se aplica la regla tal cual. Sólo sale
NO-DOCUMENTADO cuando falta la fila de esa ola/objeto en la tabla.
"""
import json
import os
import sys
from collections import OrderedDict, defaultdict

REPO = "/home/pc0/mm-gen2-donde-cambio-el-mexicano-1"
CATALOGO = os.path.join(REPO, "canon/catalogo-del-mexicano-v1_0.tsv")
COMPARABILIDAD = os.path.join(REPO, "data/enut-comparabilidad-texto-v1_0.tsv")
CORRIDA0 = os.path.join(REPO, "data/corrida0")
OUT = os.path.join(REPO, "forense/analisis/donde-cambio/mapa/enut.tsv")

HEADER = [
    "serie_id", "instrumento", "dominio", "conducta", "conducta_texto", "eje",
    "segmento", "unidad", "ola", "calc", "result_p", "result_lo", "result_hi",
    "par_con_anterior", "cita_par", "marca_2020", "nota",
]

# columnas seguras del catálogo: 1-8 y 12-23 (1-indexed), saltando 9,10,11,24
CAT_SAFE_COLS = list(range(1, 9)) + list(range(12, 24))
CAT_FIELDS = [
    "area_consulta", "llave", "dominio", "conducta", "instrumento_ola",
    "segmento", "universo_denominador", "unidad_escala", "naturaleza_ic",
    "estado_adopcion", "firma", "temporalidad", "result_punto", "result_inf",
    "result_sup", "calc", "sha256_resultados", "sha256_sello", "uso",
    "oferta_compatible",
]


def leer_tsv_seguro(path, cols_1idx):
    """Lee un TSV con split('\\t') (nunca el módulo csv), conservando celdas
    vacías finales, y sólo se queda con las columnas 1-indexadas dadas."""
    with open(path, encoding="utf-8") as f:
        filas = [l.rstrip("\n").split("\t") for l in f]
    header = filas[0]
    out = []
    idx = [i - 1 for i in cols_1idx]
    for fila in filas[1:]:
        # tolera filas más cortas por celdas vacías finales recortadas
        while len(fila) < len(header):
            fila.append("")
        out.append([fila[i] for i in idx])
    return out


def leer_tsv_completo(path):
    with open(path, encoding="utf-8") as f:
        filas = [l.rstrip("\n").split("\t") for l in f]
    header = filas[0]
    rows = []
    for fila in filas[1:]:
        while len(fila) < len(header):
            fila.append("")
        rows.append(dict(zip(header, fila)))
    return rows


def llaves_result(calc):
    """Sólo LLAVES del dict resultados de resultados.json (nunca valores)."""
    path = os.path.join(CORRIDA0, calc, "resultados.json")
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    r = d.get("resultados")
    if isinstance(r, dict):
        return set(r.keys())
    return set()


OLA_NUM = {"ENUT 2009": 2009, "ENUT 2014": 2014, "ENUT 2019": 2019, "ENUT 2024": 2024}


def clasifica_llave(llave, ola_txt):
    """Deriva (variante, eje, categoria) de la llave RESULT-ENUTyyyy-... .
    Devuelve None si la llave no matchea el patrón esperado (se reporta)."""
    if llave == "RESULT-ENUT-A-R":
        return ("A", "NACIONAL", "TOTAL")
    anio = str(OLA_NUM[ola_txt])
    prefijo = "RESULT-ENUT" + anio + "-"
    if not llave.startswith(prefijo):
        return None
    resto = llave[len(prefijo):]
    if resto.endswith("-P"):
        resto = resto[:-2]
    else:
        return None
    partes = resto.split("-")
    # RAZON-<variante>-NACIONAL
    if partes[0] == "RAZON":
        variante = "RAZON-" + partes[1]
        return (variante, "NACIONAL", "TOTAL")
    variante = partes[0]
    resto2 = partes[1:]
    if resto2 and resto2[0] == "NACIONAL":
        return (variante, "NACIONAL", "TOTAL")
    if resto2 and resto2[0] == "EDAD":
        return (variante, "EDAD", "-".join(resto2[1:]))
    if resto2 and resto2[0] == "ESCOLARIDAD":
        return (variante, "ESCOLARIDAD", "-".join(resto2[1:]))
    if resto2 and resto2[0] == "LOCALIDAD":
        return (variante, "LOCALIDAD", "-".join(resto2[1:]))
    if resto2 and resto2[0] == "SEXO":
        return (variante, "SEXO", "-".join(resto2[1:]))
    return None


def main():
    cat_raw = leer_tsv_seguro(CATALOGO, CAT_SAFE_COLS)
    rows = [dict(zip(CAT_FIELDS, r)) for r in cat_raw]
    enut_rows = [r for r in rows if r["instrumento_ola"].startswith("ENUT ")]

    comp_rows = leer_tsv_completo(COMPARABILIDAD)
    # index: (conducta_code, ola) -> veredicto  (conducta_code = C1..C5/E)
    veredicto_por_ola = defaultdict(dict)
    conducta_texto_de = {}
    for r in comp_rows:
        veredicto_por_ola[r["conducta"]][r["ola"]] = (r["veredicto"], r["alcance_del_veredicto"])
        conducta_texto_de[r["conducta"]] = r["conducta_texto"]

    # variante -> código de comparabilidad-texto (C1..C4); sólo comparabilidad
    # de la conducta base entra (la RAZON hereda el peor entre su propio
    # código C4 y el de la variante que razona, por la regla del "peor
    # estado" de §2 cuando la conducta combina objetos).
    VARIANTE_A_CODIGO = {"CONCP": "C1", "NUCLEO": "C2", "MIN": "C3", "A": "C1"}
    RAZON_BASE = {"RAZON-CONCP": "CONCP", "RAZON-NUCLEO": "NUCLEO", "RAZON-MIN": "MIN"}

    def fuera_de_escala(unidad_escala):
        u = unidad_escala.replace(" ", "")
        return not ("[0,1]" in u or "(0,1)" in u)

    # agrupa filas del catálogo por serie (variante, eje, segmento) -- NINGUNA
    # fila se excluye por escala (corrección de mesa); se anota FUERA-DE-ESCALA
    series = defaultdict(list)  # (variante,eje,seg) -> [(ola_num, catrow)]
    fuera_escala_n = 0
    no_clasificadas = []
    for r in enut_rows:
        cl = clasifica_llave(r["llave"], r["instrumento_ola"])
        if cl is None:
            no_clasificadas.append(r["llave"])
            continue
        variante, eje, seg = cl
        if fuera_de_escala(r["unidad_escala"]):
            fuera_escala_n += 1
        ola_num = OLA_NUM[r["instrumento_ola"]]
        series[(variante, eje, seg)].append((ola_num, r))

    calc_keys_cache = {}

    def keys_de(calc):
        if calc not in calc_keys_cache:
            calc_keys_cache[calc] = llaves_result(calc)
        return calc_keys_cache[calc]

    out_rows = []
    n_series = 0
    for (variante, eje, seg), items in series.items():
        items.sort(key=lambda t: t[0])
        n_series += 1
        prev_ola = None
        for i, (ola_num, r) in enumerate(items):
            keys = keys_de(r["calc"])
            rp = r["result_punto"] if r["result_punto"] in keys else ""
            rlo = r["result_inf"] if r["result_inf"] and r["result_inf"] in keys else ""
            rhi = r["result_sup"] if r["result_sup"] and r["result_sup"] in keys else ""
            if r["result_punto"] and not rp:
                nota_falta = " result_punto NO está en resultados.json del CALC (declarado)."
            else:
                nota_falta = ""

            marca_2020 = "NO"  # ENUT no tiene olas 2020

            nota_escala = " FUERA-DE-ESCALA-(0,1)." if fuera_de_escala(r["unidad_escala"]) else ""

            if i == 0:
                par = "PRIMERA"
                cita = ""
                nota = "Primera ola de la serie." + nota_escala + nota_falta
            else:
                ola_ant = items[i - 1][0]
                # regla del ESQUEMA.md literal: para cada objeto (código de
                # comparabilidad-texto) se leen sus DOS filas contra el ancla
                # 2024 -- (codigo, ola_ant) y (codigo, ola_num) -- y "las dos
                # olas del par con MISMO-INSTRUMENTO o CAMBIO-MENOR contra el
                # ancla -> COMPARABLE; alguna con CAMBIO-DE-INSTRUMENTO ->
                # CAMBIO-DOCUMENTADO". El ancla contra sí misma cuenta como
                # MISMO (fila ancla, veredicto MISMO-INSTRUMENTO).
                orden_peor = {"NO-COMPARABLE": 3, "NO-DOCUMENTADO": 2, "CAMBIO-DE-INSTRUMENTO": 1, "CAMBIO-MENOR": 0, "MISMO-INSTRUMENTO": 0}

                def estado_objeto(codigo):
                    """Devuelve (nivel, citas[], texto) para un objeto (código)
                    sobre el par (ola_ant, ola_num), leyendo sus DOS filas
                    contra el ancla 2024."""
                    va = veredicto_por_ola.get(codigo, {}).get(str(ola_ant))
                    vb = veredicto_por_ola.get(codigo, {}).get(str(ola_num))
                    citas = []
                    faltan = []
                    niveles = []
                    if va is not None:
                        citas.append("data/enut-comparabilidad-texto-v1_0.tsv:%s:%s" % (codigo, ola_ant))
                        niveles.append(orden_peor.get(va[0], 2))
                    else:
                        faltan.append(str(ola_ant))
                    if vb is not None:
                        citas.append("data/enut-comparabilidad-texto-v1_0.tsv:%s:%s" % (codigo, ola_num))
                        niveles.append(orden_peor.get(vb[0], 2))
                    else:
                        faltan.append(str(ola_num))
                    if faltan:
                        return (2, citas, "falta fila %s/%s para %s" % ("-".join(faltan), codigo, "-".join(faltan)))
                    nivel = max(niveles)
                    txt = "%s:%s=%s,%s:%s=%s" % (codigo, ola_ant, va[0], codigo, ola_num, vb[0])
                    return (nivel, citas, txt)

                codigo = VARIANTE_A_CODIGO.get(variante) or ("C4" if variante.startswith("RAZON") else None)
                objetos = []
                if codigo is not None:
                    objetos.append(codigo)
                if variante.startswith("RAZON"):
                    base_var = RAZON_BASE.get(variante)
                    base_cod = VARIANTE_A_CODIGO.get(base_var)
                    if base_cod is not None:
                        objetos.append(base_cod)

                if not objetos:
                    par, cita, nota = "NO-DOCUMENTADO", "", "Variante sin código de comparabilidad-texto mapeado." + nota_escala + nota_falta
                else:
                    resultados_obj = [estado_objeto(c) for c in objetos]
                    nivel_peor = max(r0[0] for r0 in resultados_obj)
                    citas = []
                    for r0 in resultados_obj:
                        citas.extend(r0[1])
                    cita = ";".join(citas)
                    textos = [r0[2] for r0 in resultados_obj]
                    if nivel_peor == 0:
                        par = "COMPARABLE"
                    elif nivel_peor == 1:
                        par = "CAMBIO-DOCUMENTADO"
                    else:
                        par = "NO-DOCUMENTADO"
                    nota = ("Par (%s,%s), objeto(s) %s: %s." % (ola_ant, ola_num, "/".join(objetos), "; ".join(textos))) + nota_escala + nota_falta

            serie_id = "ENUT-%s-%s-%s" % (variante, eje, seg)
            out_rows.append([
                serie_id, "ENUT", r["dominio"], variante, conducta_texto_de.get(
                    VARIANTE_A_CODIGO.get(variante, "C4" if variante.startswith("RAZON") else ""), r["conducta"])[:2000],
                eje, seg, r["unidad_escala"], str(ola_num), r["calc"], rp, rlo, rhi,
                par, cita, marca_2020, nota,
            ])

    out_rows.sort(key=lambda row: (row[0], int(row[8])))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\t".join(HEADER) + "\n")
        for row in out_rows:
            f.write("\t".join(row) + "\n")

    print("ENUT: %d filas, %d series, %d filas FUERA-DE-ESCALA-(0,1) (listadas igual), %d llaves sin clasificar" % (
        len(out_rows), n_series, fuera_escala_n, len(no_clasificadas)), file=sys.stderr)
    if no_clasificadas:
        print("  sin clasificar: %s" % no_clasificadas[:10], file=sys.stderr)


if __name__ == "__main__":
    main()
