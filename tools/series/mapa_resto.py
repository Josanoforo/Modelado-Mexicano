#!/usr/bin/env python3
"""Fragmento RESTO del mapa de series (GEN2-DONDE-CAMBIO-EL-MEXICANO-1).

FAMILIA=RESTO: todo instrumento que no sea ENVIPE, ENCIG, ENIF, ENUT ni ENIGH:
Banxico, EDER, ENCUCI, ENNViH, ENSANUT, LAPOP, MOTRAL, enfih (catálogo), más ENOE,
ENDIREH y MOCIBA (evaluados aparte, ver abajo).

Regla dura de ceguera (B-bis, spec §0/§1): este script NUNCA lee ni imprime un
valor numérico de punto/IC/tau2/cobertura/error. Del catálogo sólo toma las
columnas 1-8 y 12-23 (posición 1-based); las columnas 9,10,11 (punto, ic95_inf,
ic95_sup) y 24 (oferta_valor_ic) jamás se leen. De resultados.json SOLO se leen
las LLAVES (nunca j['resultados'][id]).

stdlib únicamente. TSV vía split('\t')/join('\t'), NUNCA el módulo csv. Las
celdas vacías finales de cada fila se conservan (no se hace rstrip de tabs).
"""
import hashlib
import json
import os
import re
from urllib.parse import quote as _urlquote

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOGO = os.path.join(REPO, "canon", "catalogo-del-mexicano-v1_0.tsv")
CORRIDA0 = os.path.join(REPO, "data", "corrida0")
OUT = os.path.join(REPO, "forense", "analisis", "donde-cambio", "mapa", "resto.tsv")

# Columnas permitidas del catálogo: 1-based 1..8 y 12..23 (nunca 9,10,11,24,25).
ALLOW_1BASED = list(range(1, 9)) + list(range(12, 24))
ALLOW_0BASED = [i - 1 for i in ALLOW_1BASED]

HEADER = ("serie_id\tinstrumento\tdominio\tconducta\tconducta_texto\teje\tsegmento\t"
          "unidad\tola\tcalc\tresult_p\tresult_lo\tresult_hi\tpar_con_anterior\t"
          "cita_par\tmarca_2020\tnota")

INSTR_PAT = re.compile(r"(BANXICO|EDER|ENCUCI|ENNVIH|ENSANUT|LAPOP|MOTRAL|ENFIH)", re.I)


def leer_catalogo_filtrado():
    """Regresa filas crudas del catálogo cuyo instrumento_ola matche RESTO,
    restringidas por posición a las columnas permitidas (nunca 9,10,11,24,25)."""
    filas = []
    with open(CATALOGO, encoding="utf-8") as f:
        header_full = f.readline().rstrip("\n").split("\t")
        for ln in f:
            if not ln.strip():
                continue
            parts = ln.rstrip("\n").split("\t")
            instrumento_ola = parts[4] if len(parts) > 4 else ""
            if not INSTR_PAT.search(instrumento_ola):
                continue
            # sólo columnas permitidas, por posición 0-based
            sel = {header_full[i]: (parts[i] if i < len(parts) else "")
                   for i in ALLOW_0BASED if i < len(header_full)}
            filas.append(sel)
    return filas


def claves_calc(calc_id):
    """Regresa el set de LLAVES (nunca valores) de resultados.json de un CALC."""
    ruta = os.path.join(CORRIDA0, calc_id, "resultados.json")
    if not os.path.isfile(ruta):
        return None
    with open(ruta, encoding="utf-8") as f:
        j = json.load(f)
    r = j.get("resultados")
    if isinstance(r, dict):
        return set(r.keys())
    return set()


# ---------------------------------------------------------------------------
# Curaduría manual: el catálogo no separa eje/segmento de forma uniforme para
# estos instrumentos (columna "segmento" a veces repite la llave, a veces trae
# la ruta milpa). Se completa a mano por result_p, verificado en runtime contra
# el catálogo filtrado (arriba) y contra las llaves de resultados.json (abajo).
# instrumento, dominio_override(None=usa catálogo), conducta, conducta_texto,
# eje, segmento, ola, unidad, marca_2020
# ---------------------------------------------------------------------------
OVERRIDE = {
    "RESULT-BANXICO-2024-AUT-ATRASO-P": ("BANXICO", "ATRASO-DANO-POR-PRODUCTO",
        "atraso_y_dano_por_producto_banxico (auto)", "NACIONAL", "AUTO", "2024",
        "proporcion_persona_0_1", "NO"),
    "RESULT-BANXICO-2024-HIP-ATRASO-P": ("BANXICO", "ATRASO-DANO-POR-PRODUCTO",
        "atraso_y_dano_por_producto_banxico (hipotecario)", "NACIONAL", "HIPOTECARIO", "2024",
        "proporcion_persona_0_1", "NO"),
    "RESULT-BANXICO-2024-NOM-ATRASO-P": ("BANXICO", "ATRASO-DANO-POR-PRODUCTO",
        "atraso_y_dano_por_producto_banxico (nomina)", "NACIONAL", "NOMINA", "2024",
        "proporcion_persona_0_1", "NO"),
    "RESULT-BANXICO-2024-PER-ATRASO-P": ("BANXICO", "ATRASO-DANO-POR-PRODUCTO",
        "atraso_y_dano_por_producto_banxico (personal)", "NACIONAL", "PERSONAL", "2024",
        "proporcion_persona_0_1", "NO"),
    "RESULT-BANXICO-2024-TDC-ATRASO-P": ("BANXICO", "ATRASO-DANO-POR-PRODUCTO",
        "atraso_y_dano_por_producto_banxico (tarjeta de credito)", "NACIONAL", "TDC", "2024",
        "proporcion_persona_0_1", "NO"),
    "RESULT-CTX-2019-P-ALTO": ("LAPOP", "CONTEXTO-INSTITUCIONAL-ALTO",
        "contexto_institucional_victimas.lapop (indice ALTO)", "NACIONAL", "TOTAL", "2019",
        "proporcion_persona_0_1", "NO"),
    "RESULT-CTX-2021-P-ALTO": ("LAPOP", "CONTEXTO-INSTITUCIONAL-ALTO",
        "contexto_institucional_victimas.lapop (indice ALTO)", "NACIONAL", "TOTAL", "2021",
        "proporcion_persona_0_1", "NO"),
    "RESULT-CTX-2023-P-ALTO": ("LAPOP", "CONTEXTO-INSTITUCIONAL-ALTO",
        "contexto_institucional_victimas.lapop (indice ALTO)", "NACIONAL", "TOTAL", "2023",
        "proporcion_persona_0_1", "NO"),
    "RESULT-EDER-A-P": ("EDER", "CORRESIDENCIA-ADULTO-FAMILIAR",
        "familia.corresidencia.adulto_familiar", "NACIONAL", "TOTAL", "SN",
        "proporcion_persona_0_1", "NO"),
    "RESULT-EDER-UNION-A-P-DIRECTO": ("EDER", "UNION-PRIMERA-DIRECTO",
        "familia.union.libre :: matrimonio_directo", "NACIONAL", "TOTAL", "2017",
        "proporcion_persona_0_1", "NO"),
    "RESULT-EDER-UNION-A-P-LIBRE": ("EDER", "UNION-PRIMERA-LIBRE",
        "familia.union.libre :: union_libre", "NACIONAL", "TOTAL", "2017",
        "proporcion_persona_0_1", "NO"),
    "RESULT-ENCUCI-A-P-CUALQUIERA": ("ENCUCI", "MORDIDA-DISCRECIONAL-SOLICITUD-O-ENTREGA",
        "tramite.mordida.discrecional (AP5_17|AP5_18)", "NACIONAL", "TOTAL", "2020",
        "proporcion_persona_0_1", "SI"),
    "RESULT-ENCUCI-B-P-RUR-AGR": ("ENCUCI", "PROTESTA-ALGUNA-VEZ-CON-AGRAVIO",
        "civico.protesta.agravio_urbano_encuci2020", "RURAL", "TOTAL", "2020",
        "proporcion_persona_0_1", "SI"),
    "RESULT-ENCUCI-B-P-URB-AGR": ("ENCUCI", "PROTESTA-ALGUNA-VEZ-CON-AGRAVIO",
        "civico.protesta.agravio_urbano_encuci2020", "URBANO", "TOTAL", "2020",
        "proporcion_persona_0_1", "SI"),
    "RESULT-ENFIH-A-P": ("ENFIH", "PLANEACION-FORMAL-TIENE-AFORE",
        "dinero.planeacion.formal_estable :: tiene_afore", "NACIONAL", "TOTAL", "2019",
        "proporcion_hogar_0_1", "NO"),
    "RESULT-ENFIH-A-P-COMPLEMENTO": ("ENFIH", "PLANEACION-FORMAL-NO-TIENE-AFORE",
        "dinero.planeacion.formal_estable :: no_tiene_afore", "NACIONAL", "TOTAL", "2019",
        "proporcion_hogar_0_1", "NO"),
    "RESULT-ENSANUT-A-P-LOGISTICA": ("ENSANUT", "VACUNACION-RAZON-LOGISTICA",
        "salud.vacunacion.disponible_ensanut2024 :: razon_no_vacunacion_logistica", "NACIONAL",
        "TOTAL", "2024", "proporcion_mencion_0_1", "NO"),
    "RESULT-ENSANUT-A-P-NO-LOGISTICA": ("ENSANUT", "VACUNACION-RAZON-NO-LOGISTICA",
        "salud.vacunacion.disponible_ensanut2024 :: razon_no_vacunacion_no_logistica", "NACIONAL",
        "TOTAL", "2024", "proporcion_mencion_0_1", "NO"),
    "RESULT-MOTRAL15-ENOE-P17-CON-ACCESO-P": ("MOTRAL", "VALORACION-SEGURIDAD-SOCIAL-CON-ACCESO",
        "trabajo.prestaciones.valoracion_seguridad_social_motral (con acceso)", "NACIONAL",
        "TOTAL", "2015", "proporcion_persona_0_1", "NO"),
    "RESULT-MOTRAL15-ENOE-P17-SIN-ACCESO-P": ("MOTRAL", "VALORACION-SEGURIDAD-SOCIAL-SIN-ACCESO",
        "trabajo.prestaciones.valoracion_seguridad_social_motral (sin acceso)", "NACIONAL",
        "TOTAL", "2015", "proporcion_persona_0_1", "NO"),
    "RESULT-MOTRAL15-P17-TOTAL-P": ("MOTRAL", "VALORACION-SEGURIDAD-SOCIAL-TOTAL",
        "trabajo.prestaciones.valoracion_seguridad_social_motral (total)", "NACIONAL",
        "TOTAL", "2015", "proporcion_persona_0_1", "NO"),
    "RESULT-R-DIN-M-01-PUNTO": ("ENNVIH", "AHORRO-TIENE-AHORROS",
        "marco-M::DIN-M-01::R (cr27 TIENE AHORROS)", "NACIONAL", "DIN-M-01", "2002",
        "proporcion_persona_0_1", "NO"),
    "RESULT-R-TRA-M-02-PUNTO": ("ENCUCI", "MORDIDA-CONTACTO-MARCO-M",
        "marco-M::TRA-M-02::R (contacto AP5_16)", "NACIONAL", "TRA-M-02", "2020",
        "proporcion_persona_0_1", "SI"),
}


# ---------------------------------------------------------------------------
# Ampliación (mensaje del coordinador, post-entrega inicial): un RESULT-*-TABLA
# sellado es un RESULT sellado; sus celdas cuentan como fuente si son
# direccionables (traen punto e IC identificables por campo). Se verificó la
# ESTRUCTURA de estos tres blobs con un inspector que reemplaza todo número por
# '#' antes de imprimir (nunca se vio ni transmitió un valor numérico):
#   - ENOE (CALC-ENOE-PISOS-0003, RESULT-ENOE-PISOS-TABLA): lista de dicts con
#     campos conducta,eje,segmento,ola,era,unidad,calidad,punto,ic95_lo,ic95_hi
#     (nombres de campo separados, confirmado también en el medidor.py del
#     propio ENOE-PERSISTENCIA/PISOS: sólo se leyó código, no RESULT).
#   - ENDIREH (CALC-ENDIREH-PISOS-*): lista de dicts con resultado,eje,
#     categoria,estado,ic95(lista de 2),p — orden [lo,hi] confirmado leyendo
#     tools/dominios/.../medidor.py línea `"ic95": [float(lo), float(hi)]`.
#   - MOCIBA (CALC-MOCIBA-PISOS-2015/2016/2017): dict {"celdas":[...]} con
#     dominio,medida,estado,n,(punto,ic95 sólo si estado==ESTIMABLE). 2015 no
#     trae punto/ic95 en ninguna celda (estado NO-ESTIMABLE-SIN-EST_DIS): no
#     entra al mapa, se reporta como evidencia de estructura, no como fila.
#
# Direccionamiento de celda: result_p = "<RESULT-ID>#k1=v1&k2=v2&.../<campo>"
# donde k1..kn son los campos NO numéricos que identifican la celda de forma
# única dentro de la lista (conducta/eje/segmento/ola para ENOE; resultado/eje/
# categoria para ENDIREH; dominio/medida para MOCIBA). El script verifica la
# celda por EXISTENCIA de esa combinación de claves y por la PRESENCIA del
# campo (nunca por su valor) antes de emitir la fila.
# ---------------------------------------------------------------------------

# Gramática de la ruta de celda (para el medidor del coordinador):
#   <RESULT-ID>#k1=v1&k2=v2&.../<campo>
# - k1..kn: vocabulario FIJO de nombres de campo (conducta,eje,segmento,ola /
#   resultado,eje,categoria / dominio,medida) -- nunca se escapan, nunca
#   vienen de datos libres.
# - v1..vn: el valor crudo de esa clave, percent-encoded con
#   urllib.parse.quote(v, safe='') (RFC 3986: sólo A-Za-z0-9_.~ quedan
#   literales). Esto escapa '&', '=', '/', '%' y cualquier otro byte
#   reservado/no-ASCII dentro del VALOR, así que un valor jamás puede inyectar
#   un separador falso ni un '/' de límite de campo falso.
# - los pares k=v se unen con '&' literal.
# - el bloque de pares y el <campo> final se unen con un '/' literal que NUNCA
#   es ambiguo porque todo '/' dentro de un valor ya viene escapado a %2F.
# - <campo>: vocabulario FIJO y cerrado (nunca datos, nunca se escapa):
#     ENOE      -> punto | ic95_lo | ic95_hi
#     ENDIREH   -> p | ic95[0] | ic95[1]      (índice 0=lo, 1=hi, confirmado
#                  en el medidor.py fuente: "ic95": [float(lo), float(hi)])
#     MOCIBA    -> punto | ic95[0] | ic95[1]  (mismo orden [lo,hi])
# - para leer una ruta: split una vez en '#', luego el resto en '/' desde la
#   DERECHA (rsplit('/', 1)) para separar el <campo> final del bloque k=v
#   (válido porque el único '/' sin escapar en toda la ruta es ese separador);
#   el bloque k=v se parte por '&' y cada par por el primer '=' (split('=',1)),
#   y cada valor se decodifica con urllib.parse.unquote antes de comparar.
CELDA_PAT_ENOE = "conducta={conducta}&eje={eje}&segmento={segmento}&ola={ola}"
# ENDIREH: 'resultado' y 'ventana' son CONDICIONALES -- sólo entran a la ruta
# si la celda de esa tabla realmente trae ese campo (ver filas_endireh: no
# todas las tablas tienen 'resultado', y sólo algunas traen 'ventana', pero
# las celdas PUBLICABLE de UNA MISMA tabla son consistentes: todas o ninguna
# traen cada campo). Construida dinámicamente, nunca vía este patrón fijo
# (se deja documentado el orden canónico: resultado?, eje, categoria,
# ventana?).
CELDA_PAT_ENDIREH = "[resultado={resultado}&]eje={eje}&categoria={categoria}[&ventana={ventana}]"
CELDA_PAT_MOCIBA = "dominio={dominio}&medida={medida}"


def _q(v):
    """Percent-encoding RFC 3986 de un valor de celda (nunca del nombre de
    campo, que es vocabulario fijo). safe='' escapa también '/'."""
    return _urlquote(str(v), safe="")

ENOE_PERSISTENCIA_SPEC = "forense/prereg-caja/ENOE-PERSISTENCIA-spec-v1_0.md"
MOCIBA_SPEC = "forense/prereg-caja/MOCIBA-PISOS-spec-v1_0.md"


def _cargar_tabla(calc_id, tabla_result_id):
    ruta = os.path.join(CORRIDA0, calc_id, "resultados.json")
    with open(ruta, encoding="utf-8") as f:
        j = json.load(f)
    raw = j["resultados"][tabla_result_id]
    if isinstance(raw, str):
        return json.loads(raw)
    return raw


def filas_enoe():
    """ENOE: CALC-ENOE-PISOS-0003 / RESULT-ENOE-PISOS-TABLA. Sólo unidad=
    'proporcion' (excluye horas_ocupado e ingreso_ocupado_nominal, que no son
    proporción en (0,1) por definición -- se anota, no se incluyen). Pares
    SOLO dentro de la misma era (spec: 'separar_eras: true', 'Universo:
    Celdas agregadas selladas de 12 conductas comparables dentro de era');
    cruzar de era NO es un salto evaluable -- DONDE-CAMBIO-spec-v1_0.md §3:
    "ENOE sólo se evalúa dentro de era, con los pares que su spec sellada
    admite" -> NO-COMPARABLE (corrección del coordinador; no CAMBIO-
    DOCUMENTADO, que lo haría evaluable como salto). Nota
    SIN-COVARIANZA-LONGITUDINAL en cada fila (la spec sellada declara que el
    IC predictivo no es estimable por el panel rotatorio)."""
    calc_id = "CALC-ENOE-PISOS-0003"
    result_id = "RESULT-ENOE-PISOS-TABLA"
    tabla = _cargar_tabla(calc_id, result_id)
    excluidas = set()
    series = {}
    for cell in tabla:
        campos_ok = all(c in cell for c in
                         ("conducta", "eje", "segmento", "ola", "era", "unidad",
                          "punto", "ic95_lo", "ic95_hi"))
        if not campos_ok:
            continue
        if cell["unidad"] != "proporcion":
            excluidas.add((cell["conducta"], cell["unidad"]))
            continue
        key = (cell["conducta"], cell["eje"], cell["segmento"])
        series.setdefault(key, []).append(cell)

    filas = []
    for (conducta, eje, segmento), celdas in series.items():
        celdas.sort(key=lambda c: c["ola"])
        for i, c in enumerate(celdas):
            ruta = CELDA_PAT_ENOE.format(conducta=_q(conducta), eje=_q(eje), segmento=_q(segmento),
                                          ola=_q(c["ola"]))
            result_p = f"{result_id}#{ruta}/punto"
            result_lo = f"{result_id}#{ruta}/ic95_lo"
            result_hi = f"{result_id}#{ruta}/ic95_hi"
            serie_id = "-".join([slug("ENOE"), slug(conducta), slug(eje), slug(segmento)])
            if i == 0:
                par, cita = "PRIMERA", ""
            else:
                prev_era = celdas[i - 1]["era"]
                if c["era"] == prev_era:
                    par = "COMPARABLE"
                    cita = (f"{ENOE_PERSISTENCIA_SPEC} §universo: '12 conductas comparables "
                             f"dentro de era' (era={c['era']})")
                else:
                    # DONDE-CAMBIO-spec-v1_0.md §3: "ENOE sólo se evalúa dentro de
                    # era, con los pares que su spec sellada admite" -- un par que
                    # cruza frontera de era queda FUERA del tramo evaluable, no es
                    # un salto documentado dentro de él: NO-COMPARABLE (corrección
                    # del coordinador, no CAMBIO-DOCUMENTADO).
                    par = "NO-COMPARABLE"
                    cita = (f"{ENOE_PERSISTENCIA_SPEC} parametros.separar_eras=true: frontera "
                             f"de era {prev_era}->{c['era']} | forense/prereg-caja/"
                             "DONDE-CAMBIO-spec-v1_0.md §3: 'ENOE sólo se evalúa dentro de "
                             "era, con los pares que su spec sellada admite'")
            marca_2020 = "SI" if "2020" in c["ola"] else "NO"
            nota = f"CELDA-DE-TABLA | SIN-COVARIANZA-LONGITUDINAL | era={c['era']} calidad={c.get('calidad','')}"
            filas.append([
                serie_id, "ENOE", "trabajo", conducta, f"ENOE PISOS :: {conducta}",
                eje, segmento, "proporcion_0_1", c["ola"], calc_id,
                result_p, result_lo, result_hi, par, cita, marca_2020, nota,
            ])
    nota_excl = ["ENOE conducta/unidad excluida (no proporcion en (0,1)): "
                 f"{c}={u}" for c, u in sorted(excluidas)]
    return filas, nota_excl


# CALC ENDIREH-PISOS -> (ola, RESULT-id de la TABLA)
ENDIREH_CALCS = {
    "CALC-ENDIREH-PISOS-2006-MODULOS-0002": ("2006", "RESULT-ENDIREH2006-MOD-TABLA"),
    "CALC-ENDIREH-PISOS-2011-MODULOS-0001": ("2011", "RESULT-ENDIREH2011-MOD-TABLA"),
    "CALC-ENDIREH-PISOS-2016-DISCRIMINACION-0001": ("2016", "RESULT-ENDIREH2016-DIS-TABLA"),
    "CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002": ("2016", "RESULT-ENDIREH2016-PF-TABLA"),
    "CALC-ENDIREH-PISOS-2016-RESTANTES-0001": ("2016", "RESULT-ENDIREH2016-REST-TABLA"),
    "CALC-ENDIREH-PISOS-2021-AYUDA-0001": ("2021", "RESULT-ENDIREH2021-AYU-TABLA"),
    "CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001": ("2021", "RESULT-ENDIREH2021-COM-TABLA"),
    "CALC-ENDIREH-PISOS-2021-DECISIONES-0001": ("2021", "RESULT-ENDIREH2021-DEC-TABLA"),
    "CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001": ("2021", "RESULT-ENDIREH2021-DIS-TABLA"),
    "CALC-ENDIREH-PISOS-2021-ESCOLAR-0001": ("2021", "RESULT-ENDIREH2021-ESC-TABLA"),
    "CALC-ENDIREH-PISOS-2021-FAMILIAR-0001": ("2021", "RESULT-ENDIREH2021-FAM-TABLA"),
    "CALC-ENDIREH-PISOS-2021-LABORAL-0001": ("2021", "RESULT-ENDIREH2021-LAB-TABLA"),
    "CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001": ("2021", "RESULT-ENDIREH2021-NF-BC-TABLA"),
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0003": ("2021", "RESULT-ENDIREH2021-PF-TABLA"),
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0004": ("2021", "RESULT-ENDIREH2021-PF-TABLA"),
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-BC-0001": ("2021", "RESULT-ENDIREH2021-PF-BC-TABLA"),
}


# Defecto encontrado por el coordinador al resolver: algunas tablas ENDIREH
# no traen campo 'resultado' en ninguna celda PUBLICABLE (confirmado por
# inspección de estructura: 2016-PF, 2021-COM, 2021-ESC, 2021-FAM, 2021-LAB,
# 2021-PF x2, 2021-PF-BC). Cada uno de esos CALC mide UN solo módulo/conducta
# por construcción (su propio nombre lo declara), así que el "resultado" se
# deriva del nombre del CALC para las columnas de reporte (conducta/
# conducta_texto/serie_id) -- NUNCA se inventa como clave de dirección: la
# ruta de celda sólo usa campos que existen de verdad en el JSON de esa celda
# (eje,categoria[,ventana]), y el chequeo de unicidad (verifica_direcciones_
# endireh) confirma que esa combinación basta para resolver una sola celda
# dentro de la tabla de su propio CALC.
ENDIREH_RESULTADO_FALLBACK = {
    "CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002": "pareja_fisica",
    "CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001": "comunitaria",
    "CALC-ENDIREH-PISOS-2021-ESCOLAR-0001": "escolar",
    "CALC-ENDIREH-PISOS-2021-FAMILIAR-0001": "familiar",
    "CALC-ENDIREH-PISOS-2021-LABORAL-0001": "laboral",
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0003": "pareja_fisica",
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0004": "pareja_fisica",
    "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-BC-0001": "pareja_fisica_bc",
}


def _endireh_filtro_celda(cell, resultado_data, eje, categoria, ventana):
    """Recorre una lista de celdas de una tabla y cuenta cuántas matchean
    exactamente los mismos campos NO numéricos que se usaron para construir
    la ruta de esta celda (resultado SÓLO si viene del propio dato, nunca del
    fallback; eje; categoria; ventana SÓLO si la tabla la trae)."""
    if resultado_data is not None and cell.get("resultado") != resultado_data:
        return False
    if cell.get("eje") != eje or cell.get("categoria") != categoria:
        return False
    if ventana is not None and cell.get("ventana") != ventana:
        return False
    if ventana is None and "ventana" in cell:
        return False
    return True


def filas_endireh():
    """ENDIREH: 16 CALC-ENDIREH-PISOS-* (olas 2006/2011/2016/2021, un módulo
    por CALC). Sólo celdas con estado=='PUBLICABLE' (traen p + ic95=[lo,hi]).
    No se localizó ningún forense/prereg-caja/ENDIREH-PISOS-spec-v*.md (spec_md
    de cada CALC es un spec.md LOCAL junto al CALC, no un documento único de
    comparabilidad); no hay fuente de texto sellada que dictamine el par entre
    olas -> par_con_anterior = NO-DOCUMENTADO en todos los pares (spec §2: sin
    fuente no se presume comparable). Identidad de serie entre olas: SOLO
    coincidencia EXACTA de (resultado, eje, categoria, ventana) como cadena --
    regla mecánica, sin inferencia semántica entre módulos distintos.

    Corrección del coordinador: varias tablas (2016-PF, 2021-NF-BC, -LAB,
    -ESC, -PF, -COM, -PF-BC) tienen celdas PUBLICABLE con el mismo
    (resultado,eje,categoria) que sólo difieren en el campo 'ventana' -->
    'ventana' entra a la dirección Y a la identidad de serie (ventanas
    distintas = series distintas; se codifica en la columna 'segmento' como
    'categoria|VENTANA:<ventana>' para no añadir columna nueva al ESQUEMA).
    Verificado (ver verifica_direcciones_endireh): con ventana incluida, 0
    direcciones con 0 o >1 celdas en las 16 tablas."""
    series = {}
    for calc_id, (ola, tabla_id) in ENDIREH_CALCS.items():
        tabla = _cargar_tabla(calc_id, tabla_id)
        celdas = tabla["celdas"] if isinstance(tabla, dict) and "celdas" in tabla else tabla
        resultado_fallback = ENDIREH_RESULTADO_FALLBACK.get(calc_id)
        for cell in celdas:
            if cell.get("estado") != "PUBLICABLE":
                continue
            if not all(k in cell for k in ("eje", "categoria", "ic95", "p")):
                continue
            if not (isinstance(cell["ic95"], list) and len(cell["ic95"]) == 2):
                continue
            resultado_data = cell.get("resultado")
            if resultado_data is None and resultado_fallback is None:
                continue  # ni dato ni fallback: no se puede rotular, se omite
            resultado_reporte = resultado_data if resultado_data is not None else resultado_fallback
            ventana = cell.get("ventana")
            key = (resultado_reporte, cell["eje"], cell["categoria"], ventana)
            series.setdefault(key, []).append(
                (ola, calc_id, tabla_id, cell, resultado_data, ventana))

    filas = []
    direcciones_a_verificar = []  # (calc_id, tabla_id, resultado_data, eje, categoria, ventana)
    for (resultado_reporte, eje, categoria, ventana), entradas in series.items():
        entradas.sort(key=lambda t: (t[0], t[1]))
        # olas distintas en orden -- el índice de PAR/PRIMERA avanza por OLA,
        # no por entrada: dos CALC de la MISMA ola (p.ej. RESULT-ENDIREH2021-
        # PF-TABLA sale de CALC-...-PAREJA-FISICA-0003 Y de -0004) son
        # mediciones hermanas de la misma etapa, no un salto a otra ola.
        olas_distintas = sorted({e[0] for e in entradas})
        # ¿alguna ola tiene >1 CALC para esta (resultado,eje,categoria,ventana)?
        calcs_por_ola = {}
        for (ola, calc_id, *_r) in entradas:
            calcs_por_ola.setdefault(ola, set()).add(calc_id)
        for ola, cal_id, tabla_id, cell, resultado_data, vent in entradas:
            i = olas_distintas.index(ola)
            partes_ruta = [f"eje={_q(eje)}", f"categoria={_q(categoria)}"]
            if resultado_data is not None:
                partes_ruta.insert(0, f"resultado={_q(resultado_data)}")
            if vent is not None:
                partes_ruta.append(f"ventana={_q(vent)}")
            ruta = "&".join(partes_ruta)
            result_p = f"{tabla_id}#{ruta}/p"
            result_lo = f"{tabla_id}#{ruta}/ic95[0]"
            result_hi = f"{tabla_id}#{ruta}/ic95[1]"
            segmento = categoria if vent is None else f"{categoria}|VENTANA:{vent}"
            # dos CALC distintos midiendo la misma (resultado,eje,segmento,ola)
            # -- p.ej. RESULT-ENDIREH2021-PF-TABLA en CALC-...-0003 y -0004 --
            # son series DISTINTAS a efectos de (serie_id,ola) único; se
            # desambigua con el sufijo numérico del propio CALC.
            multi_calc_esta_ola = len(calcs_por_ola[ola]) > 1
            if multi_calc_esta_ola:
                sufijo_calc = cal_id.rsplit("-", 1)[-1]
                segmento_id = f"{segmento}|CALC-{sufijo_calc}"
            else:
                segmento_id = segmento
            serie_id = "-".join([slug("ENDIREH"), slug(resultado_reporte), slug(eje), slug(segmento_id)])
            if i == 0:
                par, cita = "PRIMERA", ""
            else:
                par = "NO-DOCUMENTADO"
                cita = ("sin-fuente-texto: no existe forense/prereg-caja/ENDIREH-PISOS-spec-"
                        "v*.md ni tabla data/*-comparabilidad-texto-v*.tsv para ENDIREH")
            nota_partes = ["CELDA-DE-TABLA"]
            if resultado_data is None:
                nota_partes.append(f"resultado-derivado-del-calc(sin campo 'resultado' en la "
                                    f"tabla; label='{resultado_reporte}' del nombre de {cal_id})")
            if multi_calc_esta_ola:
                nota_partes.append(f"RESULT-ID-COMPARTIDO-ENTRE-CALC: {tabla_id} también sale de "
                                    f"{sorted(calcs_por_ola[ola] - {cal_id})}; desambiguado por calc "
                                    "en serie_id y verificado por (calc,RESULT-ID) exacto en la columna calc")
            nota = " | ".join(nota_partes)
            filas.append([
                serie_id, "ENDIREH", "genero", resultado_reporte,
                f"ENDIREH PISOS :: {resultado_reporte}",
                eje, segmento, "proporcion_0_1", ola, cal_id,
                result_p, result_lo, result_hi, par, cita, "NO", nota,
            ])
            direcciones_a_verificar.append((cal_id, tabla_id, resultado_data, eje, categoria, vent))
    return filas, direcciones_a_verificar


def verifica_direcciones_endireh(direcciones):
    """Re-abre cada tabla ENDIREH ya cargada (mismo calc_id) y cuenta, SIN
    leer ningún valor numérico, cuántas celdas matchean exactamente los
    campos no numéricos de cada dirección emitida. Regresa (n_cero, n_multi)."""
    cache = {}
    n_cero = n_multi = 0
    for calc_id, tabla_id, resultado_data, eje, categoria, ventana in direcciones:
        if calc_id not in cache:
            tabla = _cargar_tabla(calc_id, tabla_id)
            cache[calc_id] = tabla["celdas"] if isinstance(tabla, dict) and "celdas" in tabla else tabla
        celdas = cache[calc_id]
        n = sum(1 for c in celdas
                if c.get("estado") == "PUBLICABLE"
                and _endireh_filtro_celda(c, resultado_data, eje, categoria, ventana))
        if n == 0:
            n_cero += 1
        elif n > 1:
            n_multi += 1
    return n_cero, n_multi


MOCIBA_CALCS = {
    "CALC-MOCIBA-PISOS-2015-0001": ("2015", "RESULT-MOCIBA-PISOS-2015-TABLA"),
    "CALC-MOCIBA-PISOS-2016-0001": ("2016", "RESULT-MOCIBA-PISOS-2016-TABLA"),
    "CALC-MOCIBA-PISOS-2017-0001": ("2017", "RESULT-MOCIBA-PISOS-2017-TABLA"),
}


def filas_mociba():
    """MOCIBA: 2015 NO trae punto/ic95 en ninguna celda (estado
    NO-ESTIMABLE-SIN-EST_DIS, el FD no documenta EST_DIS) -- no entra al mapa,
    se reporta la estructura como evidencia. 2016/2017 sí (estado==ESTIMABLE).
    La propia spec sellada (MOCIBA-PISOS-spec-v1_0.md) declara por texto que
    'el cambio de población en 2017 y las distintas redacciones/respuestas
    impiden calibrar una serie con estos tres puntos. Estado
    SIN-HISTORIA-PARA-CALIBRAR' -> cualquier par 2016->2017 es NO-COMPARABLE
    por esa fuente de texto sellada, no NO-DOCUMENTADO."""
    series = {}
    notas_2015 = []
    for calc_id, (ola, tabla_id) in MOCIBA_CALCS.items():
        tabla = _cargar_tabla(calc_id, tabla_id)
        celdas = tabla["celdas"] if isinstance(tabla, dict) else tabla
        for cell in celdas:
            if cell.get("estado") != "ESTIMABLE":
                if ola == "2015":
                    notas_2015.append(
                        f"MOCIBA 2015 celda dominio={cell.get('dominio')} "
                        f"medida={cell.get('medida')} estado={cell.get('estado')} "
                        "(sin punto/ic95 en la estructura -- no entra al mapa)")
                continue
            if not all(k in cell for k in ("dominio", "medida", "ic95", "punto")):
                continue
            if not (isinstance(cell["ic95"], list) and len(cell["ic95"]) == 2):
                continue
            key = (cell["dominio"], cell["medida"])
            series.setdefault(key, []).append((ola, calc_id, tabla_id, cell))

    filas = []
    for (dominio_cel, medida), entradas in series.items():
        entradas.sort(key=lambda t: t[0])
        for i, (ola, calc_id, tabla_id, cell) in enumerate(entradas):
            ruta = CELDA_PAT_MOCIBA.format(dominio=_q(dominio_cel), medida=_q(medida))
            result_p = f"{tabla_id}#{ruta}/punto"
            result_lo = f"{tabla_id}#{ruta}/ic95[0]"
            result_hi = f"{tabla_id}#{ruta}/ic95[1]"
            serie_id = "-".join([slug("MOCIBA"), slug(medida), slug("NACIONAL"), slug(dominio_cel)])
            if i == 0:
                par, cita = "PRIMERA", ""
            else:
                par = "NO-COMPARABLE"
                cita = f"{MOCIBA_SPEC}: 'impiden calibrar una serie ... SIN-HISTORIA-PARA-CALIBRAR'"
            nota = "CELDA-DE-TABLA"
            filas.append([
                serie_id, "MOCIBA", "tecnologia", medida, f"MOCIBA PISOS :: {medida}",
                "NACIONAL", dominio_cel, "proporcion_0_1", ola, calc_id,
                result_p, result_lo, result_hi, par, cita, "NO", nota,
            ])
    return filas, notas_2015


def slug(s):
    s = s.upper()
    s = re.sub(r"[^A-Z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def construir_filas():
    catalogo_filas = leer_catalogo_filtrado()
    por_result = {}
    for fila in catalogo_filas:
        rp = fila.get("result_punto", "")
        if rp:
            por_result[rp] = fila

    cache_claves = {}
    filas_out = []
    notas_generales = []

    series = {}  # (instrumento, conducta) -> lista de (ola, dict)
    for result_p, ov in OVERRIDE.items():
        (instrumento, conducta, conducta_texto, eje, segmento, ola, unidad,
         marca_2020) = ov
        cat_fila = por_result.get(result_p)
        if cat_fila is None:
            notas_generales.append(f"OMITIDO {result_p}: no está en el catálogo filtrado")
            continue
        calc = cat_fila.get("calc", "")
        result_lo = cat_fila.get("result_inf", "")
        result_hi = cat_fila.get("result_sup", "")
        dominio = cat_fila.get("dominio", "")

        claves = cache_claves.get(calc)
        if claves is None:
            claves = claves_calc(calc)
            cache_claves[calc] = claves
        nota = []
        if claves is None:
            nota.append(f"SIN-RESULTADOS-JSON({calc})")
        else:
            for etiqueta, rid in (("p", result_p), ("lo", result_lo), ("hi", result_hi)):
                if rid and rid not in claves:
                    nota.append(f"ID-NO-VERIFICADO({etiqueta}={rid})")

        key = (instrumento, conducta, eje, segmento)
        series.setdefault(key, []).append({
            "instrumento": instrumento, "dominio": dominio, "conducta": conducta,
            "conducta_texto": conducta_texto, "eje": eje, "segmento": segmento,
            "unidad": unidad, "ola": ola, "calc": calc, "result_p": result_p,
            "result_lo": result_lo, "result_hi": result_hi,
            "marca_2020": marca_2020, "nota_verif": ";".join(nota),
        })

    for key, olas in series.items():
        # orden por ola (texto lexicográfico salvo 'SN' que se manda al final)
        def ordkey(o):
            v = o["ola"]
            return (1, v) if v == "SN" else (0, v)
        olas.sort(key=ordkey)
        for i, o in enumerate(olas):
            serie_id = "-".join([
                slug(o["instrumento"]), slug(o["conducta"]), slug(o["eje"]), slug(o["segmento"]),
            ])
            if i == 0:
                par = "PRIMERA"
                cita = ""
            else:
                # RESTO: no hay tabla data/*comparabilidad-texto* que dictamine
                # ninguno de estos instrumentos (Banxico/EDER/ENCUCI/ENSANUT/
                # LAPOP/MOTRAL/ENFIH/ENNViH). Sin fuente -> NO-DOCUMENTADO (spec §2).
                par = "NO-DOCUMENTADO"
                cita = "sin-fuente-texto: no existe data/*-comparabilidad-texto-v*.tsv para este instrumento"
            nota_partes = []
            if o["nota_verif"]:
                nota_partes.append(o["nota_verif"])
            if o["ola"] == "SN":
                nota_partes.append("ola-no-declarada-en-catalogo(instrumento_ola='EDER')")
            nota = " | ".join(nota_partes)
            filas_out.append([
                serie_id, o["instrumento"], o["dominio"], o["conducta"], o["conducta_texto"],
                o["eje"], o["segmento"], o["unidad"], o["ola"], o["calc"],
                o["result_p"], o["result_lo"], o["result_hi"], par, cita, o["marca_2020"], nota,
            ])

    # --- ampliación: celdas de RESULT-*-TABLA de ENOE/ENDIREH/MOCIBA ---
    filas_enoe_, notas_enoe_excl = filas_enoe()
    filas_out.extend(filas_enoe_)
    filas_endireh_, direcciones_endireh = filas_endireh()
    filas_out.extend(filas_endireh_)
    filas_mociba_, notas_mociba_2015 = filas_mociba()
    filas_out.extend(filas_mociba_)
    notas_generales.extend(notas_enoe_excl)
    notas_generales.extend(notas_mociba_2015)

    filas_out.sort(key=lambda r: (r[0], r[8]))

    # --- chequeo propio (sin valores): cada dirección ENDIREH resuelve a
    # exactamente 1 celda dentro de la tabla de su propio calc; y ninguna
    # fila del fragmento completo repite (serie_id, ola). ---
    n_cero, n_multi = verifica_direcciones_endireh(direcciones_endireh)
    if n_cero or n_multi:
        notas_generales.append(
            f"VERIFICACION-DIRECCIONES-ENDIREH: {n_cero} direcciones con 0 celdas, "
            f"{n_multi} con >1 celdas (deben ser 0 y 0)")

    contador_serie_ola = {}
    for r in filas_out:
        k = (r[0], r[8])  # (serie_id, ola)
        contador_serie_ola[k] = contador_serie_ola.get(k, 0) + 1
    duplicados = [(k, v) for k, v in contador_serie_ola.items() if v > 1]
    if duplicados:
        notas_generales.append(
            f"DUPLICADOS (serie_id,ola): {len(duplicados)} combinaciones repetidas "
            f"(deben ser 0): {duplicados[:5]}{'...' if len(duplicados) > 5 else ''}")

    return filas_out, notas_generales, n_cero, n_multi, len(duplicados)


def main():
    filas, notas, n_cero, n_multi, n_dup = construir_filas()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(HEADER + "\n")
        for r in filas:
            f.write("\t".join(r) + "\n")
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"escrito {OUT} ({len(filas)} filas) sha256={sha}")
    for n in notas:
        print("NOTA:", n)
    print(f"VERIFICACION: direcciones ENDIREH con 0 celdas = {n_cero} "
          f"(debe ser 0); con >1 celdas = {n_multi} (debe ser 0)")
    print(f"VERIFICACION: (serie_id,ola) duplicados en el fragmento completo = {n_dup} (debe ser 0)")
    print("ENOE: incluido vía celdas de RESULT-ENOE-PISOS-TABLA (CALC-ENOE-PISOS-0003), "
          "direccionadas por conducta/eje/segmento/ola; sólo unidad=proporcion. "
          "CALC-ENOE-PERSISTENCIA-0001 sigue sin usarse (agregado, no por celda).")
    print("ENDIREH: incluido vía celdas PUBLICABLE de RESULT-ENDIREH*-TABLA "
          "(16 CALC-ENDIREH-PISOS-*, 2006/2011/2016/2021), direccionadas por "
          "resultado(si la tabla lo trae)/eje/categoria/ventana(si la tabla la trae). "
          "Sin spec de comparabilidad sellada localizada: todos los pares NO-DOCUMENTADO.")
    print("MOCIBA: incluido vía celdas ESTIMABLE de RESULT-MOCIBA-PISOS-*-TABLA "
          "(2016/2017 únicamente; 2015 no trae punto/ic95 -- ver notas). Pares "
          "2016->2017 dictaminados NO-COMPARABLE por MOCIBA-PISOS-spec-v1_0.md "
          "('SIN-HISTORIA-PARA-CALIBRAR').")


if __name__ == "__main__":
    main()
