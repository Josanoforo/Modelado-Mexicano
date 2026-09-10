"""`CALC-DUELO-0001` -- ACTO GEN2-F5-DUELO-CALC, P2 (el computo).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-...": v}`.

Ejecuta, sobre las 6 celdas CIV-M con arbitro R (CIV-M-01/02/04/10/12/13),
la escala B-bis pre-declarada por
`forense/prereg-duelo-v2/F5-duelo-contemporaneo-spec-v1_0.md` (COMMIT-1 de
`ACTO GEN2-F5-RECAPTURA-L`): pareada primaria TRANSFERENCIA sobre
`dif_abs_pareada = |z_LCORPUS| - |z_LSOLO|`, bootstrap sellado
(`seed=42`, `replicas=10000`, `nivel_ic=0.95`, `delta=0.5`), reutilizando
SIN EDITAR el agregado por mediana (`pipeline-L-adv1-m2.py::agregar_continua`)
y el motor de bootstrap (`scoring-adv1-m3.py::generar_indices_bootstrap` /
`derivar_seed_scope`).

HALLAZGO MEDIDO EN ESTE ACTO, declarado antes de adoptar ningun veredicto de
banda (A.13): el unico extractor de `valor_extraido` que existe en el repo
para prosa libre de `corridas-L/` (`tools/extrae_l_v1_1.py`, sellado por
`MAESTRA33-E21` contra las 176 capturas v1.1) busca un encabezado Markdown
que contenga "estimaci" y, si NINGUNA linea del documento lo trae, cae a
buscar el primer numero en TODO el texto. Las 96 capturas reales de las 6
celdas CIV-M (formato real-corpus de `RECAPTURA-L`, prosa sin encabezados)
tienen CERO encabezados de ese tipo -- 0/96, medido por este medidor sobre
las 96 capturas declaradas como input -- por lo que el 100% de las
extracciones de esas celdas cae al *fallback* de documento completo. Leidas
tres a mano (citadas en `RESULT-DUELO-DIAGNOSTICO-EJEMPLO-*`), el numero que
el fallback captura es, en los tres casos, una cifra de CONTEXTO que el
propio modelo dice explicitamente que NO es su estimacion del reactivo (la
"cifra negra" ~90-93% de la ENVIPE, o una cifra de otra encuesta citada como
analogia) -- nunca la respuesta al reactivo pedido. Este medidor SI calcula
el numero que el procedimiento sellado produciria aplicando el extractor tal
cual (transparencia, "el primer resultado que produzca este procedimiento es
el que se reporta"), pero NO lo adopta como veredicto: `RESULT-DUELO-
PAREADA-VEREDICTO-ADOPTADO` queda `INCONCLUSO` con razon
`INSTRUMENTO-DE-EXTRACCION-NO-VALIDADO-PARA-FORMATO-REAL-DE-CORPUS`, una
ENMIENDA fechada a la escala de `F5-duelo-contemporaneo-spec-v1_0.md` §5 (que
no preveia esta clase de hueco), no una enmienda a esa spec en si -- la spec
no se edita (P1 de este mismo acto la copia, congelada).

NADA se recalcula de las capturas mas alla de leerlas: este medidor no abre
`data/raw`, no re-corre L, no toca `corridas-R/`.
"""
from __future__ import annotations

import importlib.util
import math
import statistics
import sys
import types

CELDAS_R = ["CIV-M-01", "CIV-M-02", "CIV-M-04", "CIV-M-10", "CIV-M-12", "CIV-M-13"]
VARIANTES = ("L-solo", "L+corpus")
K = 8
SEED = 42
REPLICAS = 10000
DELTA = 0.5
NIVEL_IC = 0.95


def _exec_modulo_desde_bytes(nombre: str, crudo: bytes, ruta_declarada: str) -> types.ModuleType:
    """Ejecuta el CONTENIDO ya resuelto por `_resuelve_inputs` (mismos bytes
    que el sha256 verificado identifica) como modulo -- no se reabre el
    archivo por una segunda vez (P1, GEN2-E3-1-1)."""
    mod = types.ModuleType(nombre)
    mod.__file__ = ruta_declarada
    sys.modules[nombre] = mod
    codigo = compile(crudo.decode("utf-8"), ruta_declarada, "exec")
    exec(codigo, mod.__dict__)
    return mod


def _json_bytes(inputs: dict, iid: str):
    import json
    return json.loads(inputs[iid]["bytes"].decode("utf-8"))


def _cuantil_7(ordenados: list[float], probabilidad: float) -> float:
    if len(ordenados) == 1:
        return float(ordenados[0])
    posicion = (len(ordenados) - 1) * probabilidad
    inferior, superior = math.floor(posicion), math.ceil(posicion)
    if inferior == superior:
        return float(ordenados[inferior])
    peso = posicion - inferior
    return float(ordenados[inferior] * (1 - peso) + ordenados[superior] * peso)


def _id_captura(cid: str, variante: str, k: int) -> str:
    return f"cap_{cid}_{variante.replace('+', 'p').replace('-', '_')}_{k:02d}"


def medir(inputs: dict, contrato: dict) -> dict:
    extrae = _exec_modulo_desde_bytes(
        "extrae_l_v1_1_calc_duelo", inputs["extrae_l_v1_1_py"]["bytes"],
        "tools/extrae_l_v1_1.py")
    pipeline = _exec_modulo_desde_bytes(
        "pipeline_l_adv1_m2_calc_duelo", inputs["pipeline_l_adv1_m2_py"]["bytes"],
        "forense/prereg-duelo-v2/pipeline-L-adv1-m2.py")
    motor = _exec_modulo_desde_bytes(
        "scoring_adv1_m3_calc_duelo", inputs["scoring_adv1_m3_py"]["bytes"],
        "forense/prereg-duelo-v2/scoring-adv1-m3.py")

    resultados: dict = {}

    m_ids = {
        "CIV-M-01": "m_CIV-M-01", "CIV-M-02": "m_CIV-M-02", "CIV-M-04": "m_CIV-M-04",
        "CIV-M-10": "m_CIV-M-10", "CIV-M-12": "m_CIV-M-12", "CIV-M-13": "m_CIV-M-13",
    }

    n_examinadas_diag = 0
    n_sin_encabezado_diag = 0
    n_extraible_fallback_diag = 0
    ejemplos_diag: list[dict] = []

    pares_z: list[tuple[float, float]] = []
    ids_pareados: list[str] = []

    for cid in CELDAS_R:
        p = cid.replace("-", "_")
        r_datos = _json_bytes(inputs, f"calc_r_{cid}")["resultados"]
        R = r_datos[f"RESULT-R-{cid}-PUNTO"]
        EE_R = r_datos[f"RESULT-R-{cid}-EE"]
        m_datos = _json_bytes(inputs, m_ids[cid])
        M = m_datos.get("valor_punto")

        resultados[f"RESULT-DUELO-{p}-R"] = R
        resultados[f"RESULT-DUELO-{p}-EE-R"] = EE_R
        resultados[f"RESULT-DUELO-{p}-M"] = M
        resultados[f"RESULT-DUELO-{p}-Z-M"] = (M - R) / EE_R if (M is not None and EE_R) else None

        n_sin_encabezado_celda = 0
        agregados = {}
        for variante, clave in (("L-solo", "L_SOLO"), ("L+corpus", "L_CORPUS")):
            valores = []
            for k in range(1, K + 1):
                iid = _id_captura(cid, variante, k)
                d = _json_bytes(inputs, iid)
                assert d["id_celda"] == cid and d["variante"] == variante, (
                    f"{iid}: id_celda/variante inesperados en la captura")
                texto = d["texto_crudo"]
                n_examinadas_diag += 1
                tiene_encabezado = any(
                    "estimaci" in extrae._sin_acentos(m.group(2)).lower()
                    for m in extrae.RE_ENCABEZADO.finditer(texto))
                if not tiene_encabezado:
                    n_sin_encabezado_diag += 1
                    n_sin_encabezado_celda += 1
                ext = extrae.extraer_valor(texto)
                if ext.estado == "EXTRAIBLE":
                    valores.append(ext.valor)
                    if not tiene_encabezado:
                        n_extraible_fallback_diag += 1
                        texto_plano = extrae._sin_acentos(texto).lower()
                        es_refuso_explicito = (
                            "no proporcionada" in texto_plano
                            or "no es una estimaci" in texto_plano)
                        if len(ejemplos_diag) < 3 and es_refuso_explicito:
                            ejemplos_diag.append({
                                "iid": iid, "cid": cid, "variante": variante, "k": k,
                                "valor_capturado": ext.valor,
                                "fragmento": ext.fragmento_citado,
                            })
            agg = pipeline.agregar_continua(valores)
            agregados[clave] = agg
            resultados[f"RESULT-DUELO-{p}-N-EXTRAIBLE-{clave.replace('_', '-')}"] = len(valores)
            resultados[f"RESULT-DUELO-{p}-{clave.replace('_', '-')}-MEDIANA"] = agg["mediana"]

        resultados[f"RESULT-DUELO-{p}-N-SIN-ENCABEZADO-ESTIMACION"] = n_sin_encabezado_celda

        z_solo = ((agregados["L_SOLO"]["mediana"] - R) / EE_R
                  if agregados["L_SOLO"]["mediana"] is not None else None)
        z_corpus = ((agregados["L_CORPUS"]["mediana"] - R) / EE_R
                    if agregados["L_CORPUS"]["mediana"] is not None else None)
        resultados[f"RESULT-DUELO-{p}-Z-L-SOLO"] = z_solo
        resultados[f"RESULT-DUELO-{p}-Z-L-CORPUS"] = z_corpus
        if z_solo is not None and z_corpus is not None:
            dif = abs(z_corpus) - abs(z_solo)
            resultados[f"RESULT-DUELO-{p}-DIF-ABS-PAREADA"] = dif
            pares_z.append((abs(z_corpus), abs(z_solo)))
            ids_pareados.append(cid)
        else:
            resultados[f"RESULT-DUELO-{p}-DIF-ABS-PAREADA"] = None

    # -- comparacion pareada primaria (bootstrap sellado, reutilizado) ------
    n = len(pares_z)
    if n == 0:
        punto = ic_lo = ic_hi = None
        veredicto_banda_bruto = "SIN_CELDAS_PAREADAS"
    else:
        seed_scope = motor.derivar_seed_scope(SEED, "F5-DUELO-CALC-transferencia-pareada")
        indices = motor.generar_indices_bootstrap(n, REPLICAS, seed_scope)
        difs = [a - b for a, b in pares_z]
        punto = statistics.fmean(difs)
        replicas_dif = [sum(difs[i] for i in rep) / n for rep in indices]
        ordenadas = sorted(replicas_dif)
        cola = (1.0 - NIVEL_IC) / 2.0
        ic_lo = _cuantil_7(ordenadas, cola)
        ic_hi = _cuantil_7(ordenadas, 1.0 - cola)
        if n < 3:
            veredicto_banda_bruto = "INCONCLUSO_POR_CONSTRUCCION_N_MENOR_3"
        elif ic_hi < -DELTA:
            veredicto_banda_bruto = "GANA_L_CORPUS"
        elif ic_lo > DELTA:
            veredicto_banda_bruto = "PIERDE_L_CORPUS"
        elif ic_lo >= -DELTA and ic_hi <= DELTA:
            veredicto_banda_bruto = "EMPATE"
        else:
            veredicto_banda_bruto = "INCONCLUSO"

    resultados["RESULT-DUELO-PAREADA-N-CELDAS"] = n
    resultados["RESULT-DUELO-PAREADA-PUNTO"] = punto
    resultados["RESULT-DUELO-PAREADA-IC-LO"] = ic_lo
    resultados["RESULT-DUELO-PAREADA-IC-HI"] = ic_hi
    resultados["RESULT-DUELO-PAREADA-VEREDICTO-BANDA-BRUTO"] = veredicto_banda_bruto
    resultados["RESULT-DUELO-PAREADA-VEREDICTO-ADOPTADO"] = "INCONCLUSO"
    resultados["RESULT-DUELO-PAREADA-RAZON-VEREDICTO-ADOPTADO"] = (
        "INSTRUMENTO-DE-EXTRACCION-NO-VALIDADO-PARA-FORMATO-REAL-DE-CORPUS")

    # -- diagnostico del instrumento -----------------------------------------
    resultados["RESULT-DUELO-DIAGNOSTICO-N-CAPTURAS-EXAMINADAS"] = n_examinadas_diag
    resultados["RESULT-DUELO-DIAGNOSTICO-N-SIN-ENCABEZADO-ESTIMACION"] = n_sin_encabezado_diag
    resultados["RESULT-DUELO-DIAGNOSTICO-N-EXTRAIBLE-VIA-FALLBACK"] = n_extraible_fallback_diag
    for i in range(3):
        idx = i + 1
        if i < len(ejemplos_diag):
            ej = ejemplos_diag[i]
            iid = ej["iid"]
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-ID"] = (
                f"{ej['cid']}__{ej['variante']}__{ej['k']:02d}")
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-SHA256"] = inputs[iid]["sha256"]
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-VALOR-CAPTURADO-INDEBIDAMENTE"] = (
                ej["valor_capturado"])
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-FRAGMENTO"] = ej["fragmento"]
        else:
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-ID"] = "SIN-EJEMPLO"
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-SHA256"] = "SIN-EJEMPLO"
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-VALOR-CAPTURADO-INDEBIDAMENTE"] = "SIN-EJEMPLO"
            resultados[f"RESULT-DUELO-DIAGNOSTICO-EJEMPLO-{idx}-FRAGMENTO"] = "SIN-EJEMPLO"

    # -- cobertura por brazo, TODO el marco de 14 celdas -- CITADA, no       --
    # -- recalculada: el embudo ya lo sello RECAPTURA-L (manifiesto P3).    --
    manifiesto = _json_bytes(inputs, "manifiesto_capturas_p3_json")
    resultados["RESULT-DUELO-COBERTURA-TOTAL-CAPTURAS-MARCO"] = manifiesto["total_capturas"]
    resultados["RESULT-DUELO-COBERTURA-OK"] = manifiesto["embudo"]["estados"].get("OK", 0)
    resultados["RESULT-DUELO-COBERTURA-RECHAZADAS"] = (
        manifiesto["embudo"]["estados"].get("RECHAZADO_TRAS_REINTENTOS", 0))

    # -- secundaria (b): USO DOCUMENTAL, acotada a las 6 celdas con arbitro --
    # -- (el panel de este acto -- no se extiende a las 8 celdas sin R).    --
    n_fuente_citada = 0
    n_l_corpus_examinadas = 0
    for cid in CELDAS_R:
        for k in range(1, K + 1):
            iid = _id_captura(cid, "L+corpus", k)
            d = _json_bytes(inputs, iid)
            n_l_corpus_examinadas += 1
            if d.get("fuente_citada"):
                n_fuente_citada += 1
    resultados["RESULT-DUELO-SECUNDARIA-USO-DOCUMENTAL-N-EXAMINADAS"] = n_l_corpus_examinadas
    resultados["RESULT-DUELO-SECUNDARIA-USO-DOCUMENTAL-N-FUENTE-CITADA-CAMPO-POBLADO"] = n_fuente_citada
    resultados["RESULT-DUELO-SECUNDARIA-USO-DOCUMENTAL-VEREDICTO"] = (
        "CAMPO-ESTRUCTURADO-VACIO-LECTURA-CUALITATIVA-EN-NOTA"
        if n_fuente_citada == 0 else "CAMPO-ESTRUCTURADO-PARCIALMENTE-POBLADO")

    resultados["RESULT-DUELO-SECUNDARIA-PP-VEREDICTO"] = (
        "NO-COMPUTABLE-MISMO-INSTRUMENTO-QUE-LA-PRIMARIA")

    return resultados
