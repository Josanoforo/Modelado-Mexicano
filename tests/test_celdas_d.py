#!/usr/bin/env python3
"""Validador de las celdas-D (data/curacion-registro/celdas-d/) contra el
contrato propuesta-motor-adaptativo-celda-v0_5.md §3 (con las adiciones H1/H2
de v0.3, la partición de `fuerza` de v0.4, y los cinco cambios de v0.5) y
contra el invariante de identidad de §2 ("celda-D =
(estimando) x (población objetivo). Dominio derivado; fuente y diseño nunca
en la clave, solo en candidatos").

DISENOS_DATOS gana un octavo valor, `experimento_aleatorizado_terceros`,
en ACTO PACK-NUBE2-CIERRE-R101 (2026-08-25, ADR-184), ejecutando la
PROPUESTA-SELLADA de FP-131 que FP-144 firmó implementar -- addendum
fechado de propuesta-motor-adaptativo-celda-v0_5.md §3, sin bumpear
versión ni tocar los cinco cambios que v0.5 ya declaró.

Encargo CABLEADO-100 (12/ago/2026), G4/TAREA 4.2: hoy hay 2 celdas-D
(G5.familismo_obligacion.actitud, G5.radio_confianza.encuci_vs_enbiare); el
piloto va a escribir 10-15 más. Este validador llega antes que ellas -- no
después, cuando ya haya 10 formas distintas de omitir un campo.

Qué valida (alcance del encargo, ampliado por CONTRATO-v0_5 -- ver ese
changelog para el porqué de cada campo nuevo):
  1. campos obligatorios de §3, a nivel celda_d y a nivel de cada candidato.
  2. rol de candidato en BASELINE | CHALLENGER | COMPLEMENTO |
     BASELINE_INGENUO | ENSAMBLE (§3, ampliado v0.5), que un candidato
     COMPLEMENTO declare resultado NO-APLICA (§3: "no compiten, no ganan ni
     pierden"), y variante_corredor en L-solo | L+corpus cuando el campo
     está presente (v0.5 -- opcional, no ata a un valor de rol porque L
     puede jugar BASELINE o CHALLENGER según la celda).
  3. tipo_adjudicacion en COMPARACION | FALSACION | CALIBRACION_CONJUNTA.
  4. escala/universo por candidato (H1): universo_instrumento no vacío por
     candidato; criterio_adjudicacion.escala y output_nativo.escala no
     vacíos a nivel celda (ambos nuevos en v0.3, el segundo obligatorio sin
     condición, el primero declarado explícito aun cuando no aplique -- así
     lo hacen las tres celdas ya selladas, con "NO-APLICA", no con ausencia).
  5. clave sin fuente (§2): celda_d no lleva fuente/fuentes/diseno/
     diseno_datos a su propio nivel -- esos campos existen SOLO dentro de
     cada candidato.
  6. estado_decidibilidad (v0.5, §3(b)): enum PUNTUADA | INDECIDIBLE |
     SKIP:<motivo> | CONTROL-MEMORIA | NO-APLICA, a nivel celda_d --
     OBLIGATORIO solo si vocabulario_version == 0.5. No se exige bajo
     vocabulario_version == 0.4 -- así es como las tres celdas existentes,
     que declaran 0.4 y no se editan por este acto, siguen validando
     (D-2/ADR-128: "el cambio se corrige, no las celdas").
  7. margen_material (v0.5, §3(c)): si está presente, número o el string
     literal "PENDIENTE-DERIVACION" -- nunca obligatorio.
  8. vocabulario_version (v0.5, §3(d)): si está presente, 0.4 o 0.5 -- nunca
     obligatorio (sigue siendo el único campo top-level opcional).

Qué NO valida (declarado, no es descuido): el valor libre de `resultado`
fuera del caso COMPLEMENTO -- exactamente la razón por la que v0.5 le abre
un campo hermano validado (`estado_decidibilidad`) en vez de apretar el
enum de `resultado` mismo. Las tres celdas ya selladas usan valores de
`resultado` fuera de cualquier enum terso, con razón declarada en su propio
YAML -- forzar aquí un enum estricto sobre `resultado` rompería los tres
archivos sellados que este validador debe aceptar. La consistencia entre
candidatos BASELINE/CHALLENGER de una misma celda (mismo estimando, escala
comparable, §3.1) tampoco se valida aquí -- es un chequeo entre celdas
relacionadas, no dentro de un solo archivo; queda para el acto de
consolidación cuando existan celdas suficientes para que aplique. Y, nuevo
en v0.5: si el valor de `estado_decidibilidad` elegido (`PUNTUADA` vs
`INDECIDIBLE`, etc.) respeta las dos condiciones verbatim de `ADV1-M3`
sobre el dato real de esa celda -- eso es un juicio sobre contenido, no
algo que un validador de esquema pueda comprobar; el esquema sólo exige
que el valor elegido sea uno de los cinco legales.
"""
import glob
import json
import os
import sys
import copy

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELDAS_DIR = os.path.join(ROOT, "data", "curacion-registro", "celdas-d")

TIPOS_ADJUDICACION = {"COMPARACION", "FALSACION", "CALIBRACION_CONJUNTA"}
DOMINIOS = {"FIN", "MIG", "TEC", "CAP", "CUL", "SAL", "SEG", "TRA", "EST", "TIE"}
UNIDADES_OBJETIVO = {"persona", "hogar", "establecimiento", "agregado_geografico", "evento"}
# `evento`: firma de mesa 21/sep/2026 (FP-393, GEN2-TRAMITE-FIRMAS-3 §2 4.2
# «a»), para estimandos cuyo denominador no es persona/hogar/establecimiento
# ni agregado geográfico, sino el propio evento (p. ej. ENCIG trámite,
# N_TRA=='01', ponderador FAC_TRA, llave (ID_TRA,NT_TIPO) sin deduplicar):
# quien hizo doce trámites contribuye doce veces.
ROLES = {"BASELINE", "CHALLENGER", "COMPLEMENTO", "BASELINE_INGENUO", "ENSAMBLE", "PISO"}
DISENOS_DATOS = {
    "panel", "pseudo_panel", "transversal", "registro_administrativo",
    "experimento_natural", "auditoria_campo", "enlace_ecologico",
    "experimento_aleatorizado_terceros",
}
# v0.5 §3(a): dos dietas de información del corredor L, campo hermano de
# `rol` -- no duplica el enum porque L puede jugar BASELINE o CHALLENGER
# según la celda; opcional, solo se valida el valor cuando está presente.
VARIANTES_CORREDOR = {"L-solo", "L+corpus"}

# v0.5 §3(b): veredicto de celda del piloto ADV-DUELO (D-4/M4/M5,
# ADR-128(e)). SKIP:<motivo> lleva sufijo libre -- se valida por prefijo,
# no por pertenencia al set (mismo patrón que PERDIO:<margen> en
# `resultado`, nunca cerrado a un catálogo de motivos).
ESTADOS_DECIDIBILIDAD = {"PUNTUADA", "INDECIDIBLE", "CONTROL-MEMORIA", "NO-APLICA"}

# v0.5 §3(d): las dos versiones que hoy tienen celdas reales -- 0.4 (las
# tres existentes) y 0.5 (lo que este contrato introduce). Comparación
# numérica: YAML parsea `0.4`/`0.5` sin comillas como float.
VOCABULARIO_VERSIONES = {0.4, 0.5, 0.6}
ESTRATEGIAS = {"pseudo_panel", "momentos", "composicion", "transversal_con_seleccion", "persistencia", "NO-APLICA"}
ESTADOS_OPERATIVOS = {"LISTO", "LEGACY", "PENDIENTE", "EXCLUIDO"}

# §2: "fuente y diseño nunca en la clave, solo en candidatos" -- estas claves
# solo pueden vivir dentro de un elemento de `candidatos`, nunca al nivel celda_d.
CLAVE_SIN_FUENTE = {"fuente", "fuentes", "diseno", "diseno_datos"}

# Las specs selladas declaran la identidad de segmento. Este mapa protege los
# dos pilotos ya emitidos sin convertir 8/12 en una regla para celdas futuras.
PILOTOS_POR_ID = {
    "DIN.ahorro_solo_informal.enif2024.localidad_x_edad": (
        "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001", "DIN-LXE8", "L", "E",
        {f"L{i}xE{j}" for i in (1, 2) for j in range(1, 5)}),
    "TRA.evade_norma.envipe2025.escolaridad_x_dominio": (
        "CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001", "TRA-SXD12", "S", "D",
        {f"S{i}xD{j}" for i in range(1, 5) for j in range(1, 4)}),
}

def _decision_adopcion_existe():
    ruta = os.path.join(ROOT, "data", "corrida0", "decisiones.tsv")
    with open(ruta, encoding="utf-8") as handle:
        return any(line.startswith("adopcion:piso-C2-20-celdas\t") and
                   "Se adoptan las 20 celdas" in line for line in handle)

REQUIRED_TOP_FIELDS = [
    "id", "estimando", "tipo_adjudicacion", "dominio", "poblacion_objetivo",
    "unidad_objetivo", "universo_candidatos", "candidatos", "criterio_adjudicacion",
    "momentos_holdout_refs", "champion_actual", "output_nativo", "incertidumbre",
    "supuesto_transporte", "fuerza_coeficiente", "procedencia_condicional", "calibrado",
    "estado_operativo", "requiere_decision_mesa", "fecha_declaracion", "commit_declaracion",
    "fecha_adjudicacion", "commit_adjudicacion", "relacion_complemento",
]
REQUIRED_CANDIDATO_FIELDS = [
    "rol", "fuentes", "edicion_periodo", "universo_instrumento", "diseno_datos",
    "estrategia", "regla_composicion", "production_spec_refs", "resultado",
]


def errors_for(celda_d, filename):
    errs = []

    if not isinstance(celda_d, dict):
        return [f"{filename}: 'celda_d' no es un mapeo"]

    for field in REQUIRED_TOP_FIELDS:
        if field not in celda_d:
            errs.append(f"{filename}: falta campo obligatorio '{field}' (v0.3 §3)")

    leaked = CLAVE_SIN_FUENTE & set(celda_d)
    if leaked:
        errs.append(
            f"{filename}: fuente/diseño en la clave, prohibido por contrato (§2 -- "
            f"solo van en candidatos): {sorted(leaked)}"
        )

    if "tipo_adjudicacion" in celda_d and celda_d["tipo_adjudicacion"] not in TIPOS_ADJUDICACION:
        errs.append(f"{filename}: tipo_adjudicacion inválido: {celda_d['tipo_adjudicacion']!r}")
    if "dominio" in celda_d and celda_d["dominio"] not in DOMINIOS:
        errs.append(f"{filename}: dominio inválido: {celda_d['dominio']!r}")
    if "unidad_objetivo" in celda_d and celda_d["unidad_objetivo"] not in UNIDADES_OBJETIVO:
        errs.append(f"{filename}: unidad_objetivo inválido: {celda_d['unidad_objetivo']!r}")
    if "estado_operativo" in celda_d and celda_d["estado_operativo"] not in ESTADOS_OPERATIVOS:
        errs.append(f"{filename}: estado_operativo inválido: {celda_d['estado_operativo']!r}")
    if "calibrado" in celda_d and not isinstance(celda_d["calibrado"], bool):
        errs.append(f"{filename}: calibrado debe ser booleano, no {celda_d['calibrado']!r}")
    if "requiere_decision_mesa" in celda_d and not isinstance(celda_d["requiere_decision_mesa"], bool):
        errs.append(f"{filename}: requiere_decision_mesa debe ser booleano, no {celda_d['requiere_decision_mesa']!r}")
    if "momentos_holdout_refs" in celda_d and not isinstance(celda_d["momentos_holdout_refs"], list):
        errs.append(f"{filename}: momentos_holdout_refs debe ser una lista")

    # v0.5 §3(d): vocabulario_version, si está presente, tiene que ser una
    # de las dos versiones que hoy tienen celdas reales.
    vocabulario_version = celda_d.get("vocabulario_version")
    if vocabulario_version is not None and vocabulario_version not in VOCABULARIO_VERSIONES:
        errs.append(
            f"{filename}: vocabulario_version inválida: {vocabulario_version!r} "
            f"(v0.5 §3(d): 0.4 o 0.5)"
        )

    # v0.5 §3(b): el valor, cuando está presente, siempre se valida contra
    # el enum; la OBLIGATORIEDAD está gateada por vocabulario_version == 0.5
    # -- las tres celdas selladas declaran 0.4 y no se editan por este acto
    # (D-2/ADR-128), así que exigir el campo sin esa compuerta las rompería.
    # El propio encargo lo dice: "si alguna falla, el cambio está mal
    # diseñado -- se corrige el cambio, no las celdas".
    estado_decid = celda_d.get("estado_decidibilidad")
    if estado_decid is None:
        if vocabulario_version == 0.5:
            errs.append(
                f"{filename}: falta 'estado_decidibilidad' (v0.5 §3(b), obligatorio "
                f"bajo vocabulario_version 0.5)"
            )
    elif estado_decid not in ESTADOS_DECIDIBILIDAD and not (
        isinstance(estado_decid, str) and estado_decid.startswith("SKIP:")
        and len(estado_decid) > len("SKIP:")
    ):
        errs.append(
            f"{filename}: estado_decidibilidad inválido: {estado_decid!r} (v0.5 §3(b): "
            f"PUNTUADA|INDECIDIBLE|SKIP:<motivo>|CONTROL-MEMORIA|NO-APLICA)"
        )

    # v0.5 §3(c): opcional siempre -- cuando existe, número (interpretado
    # sobre criterio_adjudicacion.escala) o el centinela explícito.
    margen = celda_d.get("margen_material")
    if margen is not None:
        es_numero = isinstance(margen, (int, float)) and not isinstance(margen, bool)
        if not es_numero and margen != "PENDIENTE-DERIVACION":
            errs.append(
                f"{filename}: margen_material inválido: {margen!r} (v0.5 §3(c): "
                f"número o PENDIENTE-DERIVACION)"
            )

    criterio = celda_d.get("criterio_adjudicacion")
    if not isinstance(criterio, dict) or not criterio.get("texto") or not criterio.get("escala"):
        errs.append(f"{filename}: criterio_adjudicacion.{{texto,escala}} obligatorios (escala: H1, v0.3 §3)")

    salida = celda_d.get("output_nativo")
    if not isinstance(salida, dict) or not salida.get("tipo") or not salida.get("escala") or not salida.get("valor_ref"):
        errs.append(f"{filename}: output_nativo.{{tipo,escala,valor_ref}} obligatorios (escala: H1, v0.3 §3)")

    incert = celda_d.get("incertidumbre")
    if not isinstance(incert, dict) or not incert.get("tipo") or not incert.get("ref"):
        errs.append(f"{filename}: incertidumbre.{{tipo,ref}} obligatorios")

    candidatos = celda_d.get("candidatos")
    if not isinstance(candidatos, list) or not candidatos:
        errs.append(f"{filename}: candidatos debe ser una lista no vacía")
        candidatos = []

    for i, cand in enumerate(candidatos):
        etiqueta = f"{filename}: candidatos[{i}]"
        if not isinstance(cand, dict):
            errs.append(f"{etiqueta}: no es un mapeo")
            continue
        for field in REQUIRED_CANDIDATO_FIELDS:
            if field not in cand:
                errs.append(f"{etiqueta}: falta campo obligatorio '{field}'")

        rol = cand.get("rol")
        if rol not in ROLES:
            errs.append(
                f"{etiqueta}: rol inválido: {rol!r} (v0.5 §3(a): BASELINE|CHALLENGER|"
                f"COMPLEMENTO|BASELINE_INGENUO|ENSAMBLE)"
            )

        # v0.5 §3(a): opcional siempre -- distingue la dieta de información
        # del corredor L sin duplicar el enum de rol.
        variante = cand.get("variante_corredor")
        if variante is not None and variante not in VARIANTES_CORREDOR:
            errs.append(
                f"{etiqueta}: variante_corredor inválida: {variante!r} (v0.5 §3(a): "
                f"L-solo|L+corpus)"
            )

        if not cand.get("universo_instrumento"):
            errs.append(f"{etiqueta}: universo_instrumento vacío (obligatorio, H1 v0.3 §3)")

        if not cand.get("fuentes"):
            errs.append(f"{etiqueta}: fuentes vacío -- sin fuente declarada, el candidato no es verificable")

        diseno = cand.get("diseno_datos")
        if diseno is not None and diseno not in DISENOS_DATOS:
            errs.append(f"{etiqueta}: diseno_datos inválido: {diseno!r}")

        estrategia = cand.get("estrategia")
        if estrategia is not None and estrategia not in ESTRATEGIAS:
            errs.append(f"{etiqueta}: estrategia inválida: {estrategia!r}")

        if rol == "COMPLEMENTO":
            resultado = str(cand.get("resultado", "")).strip()
            if resultado != "NO-APLICA":
                errs.append(
                    f"{etiqueta}: rol COMPLEMENTO exige resultado=NO-APLICA -- no compite, "
                    f"no gana ni pierde (v0.3 §3); trae {resultado!r}"
                )
        elif not cand.get("resultado"):
            errs.append(f"{etiqueta}: resultado vacío")

    # v0.6: un champion es un candidato, no una observación. Las condiciones
    # especiales sólo aplican cuando el campeón es un piso; una celda puede
    # seguir sin adjudicar o tener un campeón de otro rol admisible.
    champion = celda_d.get("champion_actual")
    if vocabulario_version == 0.6:
        ids = {c.get("id_candidato") for c in candidatos if isinstance(c, dict)}
        if champion == "NINGUNO":
            return errs
        if champion not in ids:
            errs.append(f"{filename}: champion_actual debe referir id_candidato bajo v0.6")
        else:
            ganador = next(c for c in candidatos if c.get("id_candidato") == champion)
            es_piso = ganador.get("rol") in {"PISO", "BASELINE_INGENUO"}
            if es_piso and estado_decid not in {"PUNTUADA", "INDECIDIBLE"}:
                errs.append(f"{filename}: piso adjudicado requiere estado_decidibilidad pertinente")
            if es_piso and celda_d.get("veredicto") != "SIN-CANDIDATO-SUPERIOR":
                errs.append(f"{filename}: piso adjudicado requiere veredicto SIN-CANDIDATO-SUPERIOR")
        por_celda = celda_d.get("adjudicacion_por_celda")
        if not isinstance(por_celda, dict) or not por_celda:
            errs.append(f"{filename}: falta adjudicacion_por_celda v0.6")
        else:
            piloto = PILOTOS_POR_ID.get(celda_d.get("id"))
            if piloto and set(por_celda) != piloto[4]:
                errs.append(f"{filename}: cobertura de segmentos no coincide con la spec sellada")
            vistos = set()
            for segmento, refs in por_celda.items():
                if not isinstance(refs, dict) or refs.get("id_candidato") != champion:
                    errs.append(f"{filename}: adjudicación inválida para {segmento}")
                elif not all(refs.get(k) for k in ("calc", "resultado_puntual", "ic95inf", "ic95sup", "decision_ref")):
                    errs.append(f"{filename}: referencias incompletas para {segmento}")
                else:
                    tripleta = (refs["resultado_puntual"], refs["ic95inf"], refs["ic95sup"])
                    if tripleta in vistos:
                        errs.append(f"{filename}: segmento duplicado o intercambio de referencias: {segmento}")
                    vistos.add(tripleta)
                    if piloto:
                        calc_esperado, prefijo, _, _, _ = piloto
                        esperado = {
                            "resultado_puntual": f"RESULT-{prefijo}-C2-P-{segmento}",
                            "ic95inf": f"RESULT-{prefijo}-C2-IC95INF-{segmento}",
                            "ic95sup": f"RESULT-{prefijo}-C2-IC95SUP-{segmento}",
                        }
                        if champion != "C2" or refs["id_candidato"] != "C2":
                            errs.append(f"{filename}: la firma de adopción y RESULT C2 exigen candidato C2")
                        if refs["calc"] != calc_esperado or any(refs[k] != v for k, v in esperado.items()):
                            errs.append(f"{filename}: identidad/función RESULT no corresponde a {segmento}")
                        if refs["decision_ref"] != "adopcion:piso-C2-20-celdas" or not _decision_adopcion_existe():
                            errs.append(f"{filename}: decisión de adopción inexistente o no pertinente para {segmento}")
                    calc = os.path.join(ROOT, "data", "corrida0", refs["calc"], "resultados.json")
                    try:
                        with open(calc, encoding="utf-8") as handle:
                            resultados = json.load(handle)["resultados"]
                    except (OSError, KeyError, json.JSONDecodeError) as exc:
                        errs.append(f"{filename}: CALC no legible para {segmento}: {exc}")
                    else:
                        if any(ref not in resultados for ref in tripleta):
                            errs.append(f"{filename}: referencias RESULT inexistentes para {segmento}")
                        if "P-REDERIVADO" in refs["resultado_puntual"] or "IC95" in refs["resultado_puntual"]:
                            errs.append(f"{filename}: el punto de {segmento} no es RESULT puntual primario")

    return errs


def main():
    paths = sorted(glob.glob(os.path.join(CELDAS_DIR, "*.yaml")))
    if not paths:
        print(f"ERROR: no se encontró ningún YAML en {os.path.relpath(CELDAS_DIR, ROOT)}", file=sys.stderr)
        return 1

    total_errors = []
    for path in paths:
        filename = os.path.basename(path)
        with open(path, encoding="utf-8") as handle:
            doc = yaml.safe_load(handle)
        if not isinstance(doc, dict) or "celda_d" not in doc:
            total_errors.append(f"{filename}: documento sin clave de nivel superior 'celda_d'")
            continue
        errs = errors_for(doc["celda_d"], filename)
        total_errors.extend(errs)
        etiqueta_id = doc["celda_d"].get("id", "?") if isinstance(doc["celda_d"], dict) else "?"
        estado = "FAIL" if errs else "ok"
        sufijo = f" -- {len(errs)} error(es)" if errs else ""
        print(f"{filename} [{etiqueta_id}]: {estado}{sufijo}")

    print()
    if total_errors:
        print(f"{len(total_errors)} error(es) contra el contrato v0.3 §3:")
        for e in total_errors:
            print(f"  {e}")
        return 1

    print(f"{len(paths)} archivo(s) de celda-D validan contra propuesta-motor-adaptativo-celda-v0_6.md §3.")
    return 0


def test_v06_rechaza_alteraciones_de_segmento():
    """Regresiones: la existencia de IDs no basta para una adjudicación."""
    ruta = os.path.join(CELDAS_DIR, "DIN.ahorro_solo_informal.enif2024.localidad_x_edad.yaml")
    with open(ruta, encoding="utf-8") as handle:
        base = yaml.safe_load(handle)["celda_d"]
    assert not errors_for(base, "fixture")
    a, b = "L1xE1", "L1xE2"
    casos = []
    x = copy.deepcopy(base); x["adjudicacion_por_celda"][a], x["adjudicacion_por_celda"][b] = x["adjudicacion_por_celda"][b], x["adjudicacion_por_celda"][a]; casos.append(x)
    x = copy.deepcopy(base); del x["adjudicacion_por_celda"][a]; casos.append(x)
    x = copy.deepcopy(base); x["adjudicacion_por_celda"][a]["ic95inf"], x["adjudicacion_por_celda"][a]["ic95sup"] = x["adjudicacion_por_celda"][a]["ic95sup"], x["adjudicacion_por_celda"][a]["ic95inf"]; casos.append(x)
    x = copy.deepcopy(base); x["adjudicacion_por_celda"][a]["decision_ref"] = "ADR-538"; casos.append(x)
    for caso in casos:
        assert errors_for(caso, "fixture")


def test_unidad_objetivo_evento_es_valida():
    """FP-393/GEN2-TRAMITE-FIRMAS-3 §2 4.2 (firma de mesa 21/sep/2026, 'a'):
    `evento` entra a UNIDADES_OBJETIVO para estimandos cuyo denominador no es
    persona/hogar/establecimiento/agregado_geografico sino el propio evento
    (ENCIG trámite: quien hizo doce trámites contribuye doce veces)."""
    ruta = os.path.join(CELDAS_DIR, "DIN.ahorro_solo_informal.enif2024.localidad_x_edad.yaml")
    with open(ruta, encoding="utf-8") as handle:
        base = yaml.safe_load(handle)["celda_d"]
    caso = copy.deepcopy(base)
    caso["unidad_objetivo"] = "evento"
    assert not errors_for(caso, "fixture")
    caso_invalido = copy.deepcopy(base)
    caso_invalido["unidad_objetivo"] = "tramite"
    assert errors_for(caso_invalido, "fixture")


def test_v06_rechaza_candidato_distinto_de_la_firma_c2():
    ruta = os.path.join(CELDAS_DIR, "DIN.ahorro_solo_informal.enif2024.localidad_x_edad.yaml")
    with open(ruta, encoding="utf-8") as handle:
        caso = yaml.safe_load(handle)["celda_d"]
    caso["champion_actual"] = "C1"
    for refs in caso["adjudicacion_por_celda"].values():
        refs["id_candidato"] = "C1"
    assert errors_for(caso, "fixture")


if __name__ == "__main__":
    raise SystemExit(main())
