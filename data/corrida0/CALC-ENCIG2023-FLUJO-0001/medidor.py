"""Clasifica el flujo de P8_4 sin atribuir marcas de tipo a cada evento."""
from __future__ import annotations

import csv
import io
import json
import math
import zipfile


ZIP_ID = "encig23_base_datos_csv"
P = "RESULT-ENCIG23-FLUJO-"
M_S7 = "encig2023_04_sec_7.csv"
M_S8 = "encig2023_05_sec_8.csv"
M_PERSONA = "encig2023_01_sec1_A_3_4_5_8_9_10.csv"
COLS_S7 = ["ID_VIV", "ID_PER", "ID_TRA", "N_TRA", "P7_3", "FAC_TRA"]
COLS_S8 = ["ID_VIV", "ID_PER", "ID_TRA", "N_TRA", "P8_4"]
COLS_PERSONA = ["ID_VIV", "ID_PER", "P8_3_1", "P8_3_2", "P8_3_3"]
CATEGORIAS = (
    "RESPUESTA_VALIDA_OBSERVADA",
    "SALTO_NEGATIVO_LOGICO",
    "FUERA_UNIVERSO_NO_APLICA",
    "ELEGIBILIDAD_NO_DETERMINABLE",
    "RESPUESTA_FALTANTE_APLICABLE",
    "CONTRADICCION",
)
GRUPOS = ("TOTAL", "PRE", "DIG", "OTRO", "CANAL_FALTANTE")


def _norm(col):
    return col.lstrip("\ufeff").lstrip("ï»¿").strip().strip('"').upper()


def _llave(valor):
    texto = "" if valor is None else str(valor).strip().strip('"')
    return texto or None


def _codigo(valor, blancos):
    texto = "" if valor is None else str(valor).strip().strip('"')
    if texto in blancos or texto.lower() in blancos:
        return None
    try:
        return int(texto)
    except ValueError:
        return "FUERA"


def _peso(valor):
    try:
        numero = float(str(valor).strip().replace(",", ""))
    except (TypeError, ValueError):
        return None
    return numero if math.isfinite(numero) and numero > 0 else None


def _abre(zf, miembro, columnas):
    with zf.open(miembro) as fh:
        lector = csv.reader(io.TextIOWrapper(fh, encoding="latin-1", newline=""))
        try:
            cabecera = [_norm(x) for x in next(lector)]
        except StopIteration:
            return [], list(columnas)
        indices = {c: cabecera.index(c) for c in columnas if c in cabecera}
        ausentes = [c for c in columnas if c not in indices]
        filas = []
        for fila in lector:
            if not fila:
                continue
            filas.append(tuple(
                fila[indices[c]] if c in indices and indices[c] < len(fila) else None
                for c in columnas
            ))
        return filas, ausentes


def _soporte(valores):
    cuenta = {}
    for valor in valores:
        k = "b" if valor is None else str(valor)
        cuenta[k] = cuenta.get(k, 0) + 1
    return ";".join(f"{k}:{cuenta[k]}" for k in sorted(cuenta))


def _canal(codigo):
    if codigo == 1:
        return "PRE"
    if codigo in {3, 4, 5}:
        return "DIG"
    if codigo in {2, 6, 7, 8, 9}:
        return "OTRO"
    if codigo is None:
        return "CANAL_FALTANTE"
    return None


def _categoria(p83, p84):
    if p84 == "FUERA" or any(x == "FUERA" for x in p83):
        return "CONTRADICCION"
    if 1 in p83:
        return (
            "RESPUESTA_VALIDA_OBSERVADA"
            if p84 in {0, 1}
            else "RESPUESTA_FALTANTE_APLICABLE"
        )
    if p84 in {0, 1}:
        return "CONTRADICCION"
    if all(x == 2 for x in p83):
        return "SALTO_NEGATIVO_LOGICO"
    return "ELEGIBILIDAD_NO_DETERMINABLE"


def _base_salida():
    salida = {
        P + "ESTADO": "NO-ESTIMABLE",
        P + "JOIN-ESTADO": "NO-EVALUADO",
        P + "JOIN-N-SEC7": 0,
        P + "JOIN-N-SEC8": 0,
        P + "JOIN-N-PERSONAS": 0,
        P + "JOIN-N-EVENTOS-PERSONA": 0,
        P + "JOIN-N-EVENTOS-SIN-PERSONA": 0,
        P + "N-PESO-INVALIDO": 0,
        P + "SOPORTE-P83-1": "NO-EVALUADO",
        P + "SOPORTE-P83-2": "NO-EVALUADO",
        P + "SOPORTE-P83-3": "NO-EVALUADO",
        P + "SOPORTE-P84": "NO-EVALUADO",
        P + "TABLA-CATEGORIAS-JSON": "[]",
        P + "CATEGORIAS-CIERRE-N": "NO-EVALUADO",
        P + "CATEGORIAS-CIERRE-MASA": "NO-EVALUADO",
        P + "PADRE-N-TOTAL": 0,
        P + "PADRE-MASA-TOTAL": None,
        P + "PADRE-N-OBSERVADO": 0,
        P + "PADRE-MASA-OBSERVADA": None,
        P + "PADRE-MASA-NUMERADOR": None,
        P + "PADRE-P-CONDICIONADO": None,
        P + "PADRE-N-P84-FALTANTE": 0,
        P + "PADRE-N-TIPOS-OBSERVADOS": 0,
        P + "PADRE-N-TIPOS-POSITIVOS": 0,
        P + "PADRE-N-TIPOS-POSITIVOS-REPETIDOS": 0,
        P + "PADRE-MAX-EVENTOS-POR-TIPO-POSITIVO": 0,
        P + "RECONCILIACION-PADRE": "NO-EVALUADA",
        P + "N-UNIVERSO": 0,
        P + "W-UNIVERSO": None,
        P + "N-POSITIVO-CONOCIDO": 0,
        P + "W-POSITIVO-CONOCIDO": 0.0,
        P + "N-NEGATIVO-CONOCIDO": 0,
        P + "W-NEGATIVO-CONOCIDO": 0.0,
        P + "N-DESCONOCIDO": 0,
        P + "W-DESCONOCIDO": 0.0,
        P + "N-POSITIVO-LIM-INF": 0,
        P + "N-POSITIVO-LIM-SUP": 0,
        P + "W-POSITIVO-LIM-INF": None,
        P + "W-POSITIVO-LIM-SUP": None,
        P + "P-LIM-INF": None,
        P + "P-LIM-SUP": None,
        P + "ESTIMANDO-ESTADO": "NO-EVALUADO",
        P + "CORRESPONDENCIA-RES-0007": "NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR",
        P + "CORRESPONDENCIA-RES-0008": "NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR",
        P + "PRECISION-MUESTRAL": "NO-CALCULADA",
    }
    return salida


def _paro(salida, razon):
    salida[P + "ESTADO"] = razon
    return salida


def medir(inputs, contrato):
    salida = _base_salida()
    parametros = contrato.get("parametros", {})
    blancos = {str(x) for x in parametros.get("blanco_literal", ["", "b", "NA"])}

    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as zf:
        nombres = set(zf.namelist())
        requeridos = (M_S7, M_S8, M_PERSONA)
        faltan = [m for m in requeridos if m not in nombres]
        if faltan:
            return _paro(salida, "NO-ESTIMABLE-MIEMBRO-AUSENTE:" + ",".join(faltan))
        s7, falta7 = _abre(zf, M_S7, COLS_S7)
        s8, falta8 = _abre(zf, M_S8, COLS_S8)
        personas, faltap = _abre(zf, M_PERSONA, COLS_PERSONA)

    salida[P + "JOIN-N-SEC7"] = len(s7)
    salida[P + "JOIN-N-SEC8"] = len(s8)
    salida[P + "JOIN-N-PERSONAS"] = len(personas)
    ausentes = (
        [f"{M_S7}:{x}" for x in falta7]
        + [f"{M_S8}:{x}" for x in falta8]
        + [f"{M_PERSONA}:{x}" for x in faltap]
    )
    if ausentes:
        return _paro(salida, "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ",".join(ausentes))

    i7 = {c: i for i, c in enumerate(COLS_S7)}
    i8 = {c: i for i, c in enumerate(COLS_S8)}
    ip = {c: i for i, c in enumerate(COLS_PERSONA)}

    tipos = {}
    for r in s8:
        k = _llave(r[i8["ID_TRA"]])
        if k is None or k in tipos:
            salida[P + "JOIN-ESTADO"] = "NO-ESTIMABLE-SEC8-ID_TRA-NO-UNICA"
            return _paro(salida, salida[P + "JOIN-ESTADO"])
        tipos[k] = r

    por_persona = {}
    for r in personas:
        k = (_llave(r[ip["ID_VIV"]]), _llave(r[ip["ID_PER"]]))
        if None in k or k in por_persona:
            salida[P + "JOIN-ESTADO"] = "NO-ESTIMABLE-PERSONA-NO-UNICA"
            return _paro(salida, salida[P + "JOIN-ESTADO"])
        por_persona[k] = r

    p83_soportes = [[], [], []]
    for r in personas:
        for j, col in enumerate(("P8_3_1", "P8_3_2", "P8_3_3")):
            p83_soportes[j].append(_codigo(r[ip[col]], blancos))
    for j in range(3):
        salida[P + f"SOPORTE-P83-{j + 1}"] = _soporte(p83_soportes[j])
    salida[P + "SOPORTE-P84"] = _soporte(
        [_codigo(r[i8["P8_4"]], blancos) for r in s8]
    )

    tabla = {g: {c: [0, 0.0] for c in CATEGORIAS} for g in GRUPOS}
    eventos = []
    n_peso_invalido = 0
    n_sin_persona = 0
    for r in s7:
        peso = _peso(r[i7["FAC_TRA"]])
        if peso is None:
            n_peso_invalido += 1
            continue
        id_tra = _llave(r[i7["ID_TRA"]])
        rt = tipos.get(id_tra)
        kp = (_llave(r[i7["ID_VIV"]]), _llave(r[i7["ID_PER"]]))
        rp = por_persona.get(kp)
        if rt is None:
            salida[P + "JOIN-ESTADO"] = "NO-ESTIMABLE-EVENTO-SIN-TIPO"
            return _paro(salida, salida[P + "JOIN-ESTADO"])
        control7 = (
            _llave(r[i7["ID_VIV"]]), _llave(r[i7["ID_PER"]]),
            _llave(r[i7["N_TRA"]]),
        )
        control8 = (
            _llave(rt[i8["ID_VIV"]]), _llave(rt[i8["ID_PER"]]),
            _llave(rt[i8["N_TRA"]]),
        )
        if control7 != control8:
            salida[P + "JOIN-ESTADO"] = "NO-ESTIMABLE-CONTROL-TIPO-DIFIERE"
            return _paro(salida, salida[P + "JOIN-ESTADO"])
        if rp is None:
            n_sin_persona += 1
            continue
        p83 = tuple(_codigo(rp[ip[c]], blancos) for c in ("P8_3_1", "P8_3_2", "P8_3_3"))
        p84 = _codigo(rt[i8["P8_4"]], blancos)
        canal_codigo = _codigo(r[i7["P7_3"]], blancos)
        canal = _canal(canal_codigo)
        if canal is None:
            return _paro(salida, "NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P7_3")
        categoria = _categoria(p83, p84)
        eventos.append({
            "id_tra": id_tra, "peso": peso, "p84": p84,
            "categoria": categoria, "canal": canal,
        })
        for grupo in ("TOTAL", canal):
            tabla[grupo][categoria][0] += 1
            tabla[grupo][categoria][1] += peso

    salida[P + "N-PESO-INVALIDO"] = n_peso_invalido
    salida[P + "JOIN-N-EVENTOS-SIN-PERSONA"] = n_sin_persona
    salida[P + "JOIN-N-EVENTOS-PERSONA"] = len(eventos)
    if n_peso_invalido:
        return _paro(salida, "NO-ESTIMABLE-PESO-INVALIDO")
    if n_sin_persona or len(eventos) != len(s7):
        salida[P + "JOIN-ESTADO"] = "NO-ESTIMABLE-COBERTURA-PERSONA-INCOMPLETA"
        return _paro(salida, salida[P + "JOIN-ESTADO"])
    salida[P + "JOIN-ESTADO"] = "JOIN-EXACTO-SIN-MULTIPLICACION"

    filas_tabla = []
    for grupo in GRUPOS:
        for categoria in CATEGORIAS:
            n, masa = tabla[grupo][categoria]
            filas_tabla.append({
                "grupo": grupo, "categoria": categoria,
                "n": n, "masa_fac_tra": masa,
            })
    salida[P + "TABLA-CATEGORIAS-JSON"] = json.dumps(
        filas_tabla, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    n_total = len(eventos)
    w_total = sum(x["peso"] for x in eventos)
    salida[P + "CATEGORIAS-CIERRE-N"] = (
        "CIERRA" if sum(tabla["TOTAL"][c][0] for c in CATEGORIAS) == n_total else "NO-CIERRA"
    )
    salida[P + "CATEGORIAS-CIERRE-MASA"] = (
        "CIERRA" if math.isclose(sum(tabla["TOTAL"][c][1] for c in CATEGORIAS), w_total, abs_tol=1e-9) else "NO-CIERRA"
    )

    observados = [x for x in eventos if x["p84"] in {0, 1}]
    positivos_marca = [x for x in observados if x["p84"] == 1]
    por_tipo = {}
    for x in eventos:
        por_tipo.setdefault(x["id_tra"], []).append(x)
    tipos_obs = {x["id_tra"] for x in observados}
    tipos_pos = {x["id_tra"] for x in positivos_marca}
    grupos_pos = [por_tipo[k] for k in tipos_pos]

    w_obs = sum(x["peso"] for x in observados)
    w_num = sum(x["peso"] for x in positivos_marca)
    salida[P + "PADRE-N-TOTAL"] = n_total
    salida[P + "PADRE-MASA-TOTAL"] = w_total
    salida[P + "PADRE-N-OBSERVADO"] = len(observados)
    salida[P + "PADRE-MASA-OBSERVADA"] = w_obs
    salida[P + "PADRE-MASA-NUMERADOR"] = w_num
    salida[P + "PADRE-P-CONDICIONADO"] = w_num / w_obs if w_obs else None
    salida[P + "PADRE-N-P84-FALTANTE"] = n_total - len(observados)
    salida[P + "PADRE-N-TIPOS-OBSERVADOS"] = len(tipos_obs)
    salida[P + "PADRE-N-TIPOS-POSITIVOS"] = len(tipos_pos)
    salida[P + "PADRE-N-TIPOS-POSITIVOS-REPETIDOS"] = sum(len(g) > 1 for g in grupos_pos)
    salida[P + "PADRE-MAX-EVENTOS-POR-TIPO-POSITIVO"] = max((len(g) for g in grupos_pos), default=0)

    esperado = parametros.get("esperado_padre", {})
    pares = {
        "n_total": n_total,
        "n_observado": len(observados),
        "w_observado": w_obs,
        "w_numerador": w_num,
    }
    concilia = all(
        k not in esperado or math.isclose(float(pares[k]), float(esperado[k]), abs_tol=1e-9)
        for k in pares
    )
    salida[P + "RECONCILIACION-PADRE"] = "CONCILIA" if concilia else "NO-CONCILIA"
    if not concilia:
        return _paro(salida, "NO-ESTIMABLE-NO-CONCILIA-PADRE")

    negativos = [
        x for x in eventos
        if x["categoria"] == "SALTO_NEGATIVO_LOGICO"
        or (x["categoria"] == "RESPUESTA_VALIDA_OBSERVADA" and x["p84"] == 0)
    ]
    positivos_conocidos = [g[0] for g in grupos_pos if len(g) == 1]
    n_neg = len(negativos)
    w_neg = sum(x["peso"] for x in negativos)
    n_pos_con = len(positivos_conocidos)
    w_pos_con = sum(x["peso"] for x in positivos_conocidos)
    n_universo = n_total
    w_universo = w_total
    n_desconocido = n_universo - n_neg - n_pos_con
    w_desconocido = w_universo - w_neg - w_pos_con
    n_lim_inf = len(grupos_pos)
    n_lim_sup = n_universo - n_neg
    w_lim_inf = sum(min(x["peso"] for x in grupo) for grupo in grupos_pos)
    w_lim_sup = w_universo - w_neg

    salida[P + "N-UNIVERSO"] = n_universo
    salida[P + "W-UNIVERSO"] = w_universo
    salida[P + "N-POSITIVO-CONOCIDO"] = n_pos_con
    salida[P + "W-POSITIVO-CONOCIDO"] = w_pos_con
    salida[P + "N-NEGATIVO-CONOCIDO"] = n_neg
    salida[P + "W-NEGATIVO-CONOCIDO"] = w_neg
    salida[P + "N-DESCONOCIDO"] = n_desconocido
    salida[P + "W-DESCONOCIDO"] = w_desconocido
    salida[P + "N-POSITIVO-LIM-INF"] = n_lim_inf
    salida[P + "N-POSITIVO-LIM-SUP"] = n_lim_sup
    salida[P + "W-POSITIVO-LIM-INF"] = w_lim_inf
    salida[P + "W-POSITIVO-LIM-SUP"] = w_lim_sup
    salida[P + "P-LIM-INF"] = w_lim_inf / w_universo if w_universo else None
    salida[P + "P-LIM-SUP"] = w_lim_sup / w_universo if w_universo else None
    salida[P + "ESTIMANDO-ESTADO"] = "CONJUNTO-IDENTIFICADO-CIRCUNSTANCIA-NO-PAGO"
    salida[P + "ESTADO"] = "CLASIFICADO-CON-INCERTIDUMBRE-DE-FLUJO"
    return salida
