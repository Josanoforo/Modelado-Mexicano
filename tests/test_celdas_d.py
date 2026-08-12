#!/usr/bin/env python3
"""Validador de las celdas-D (data/curacion-registro/celdas-d/) contra el
contrato propuesta-motor-adaptativo-celda-v0_3.md §3 (con las adiciones H1/H2
de esa misma versión) y contra el invariante de identidad de §2 ("celda-D =
(estimando) x (población objetivo). Dominio derivado; fuente y diseño nunca
en la clave, solo en candidatos").

Encargo CABLEADO-100 (12/ago/2026), G4/TAREA 4.2: hoy hay 2 celdas-D
(G5.familismo_obligacion.actitud, G5.radio_confianza.encuci_vs_enbiare); el
piloto va a escribir 10-15 más. Este validador llega antes que ellas -- no
después, cuando ya haya 10 formas distintas de omitir un campo.

Qué valida (alcance del encargo):
  1. campos obligatorios de §3, a nivel celda_d y a nivel de cada candidato.
  2. rol de candidato en BASELINE | CHALLENGER | COMPLEMENTO (§3), y que un
     candidato COMPLEMENTO declare resultado NO-APLICA (§3: "no compiten, no
     ganan ni pierden").
  3. tipo_adjudicacion en COMPARACION | FALSACION | CALIBRACION_CONJUNTA.
  4. escala/universo por candidato (H1): universo_instrumento no vacío por
     candidato; criterio_adjudicacion.escala y output_nativo.escala no
     vacíos a nivel celda (ambos nuevos en v0.3, el segundo obligatorio sin
     condición, el primero declarado explícito aun cuando no aplique -- así
     lo hacen las dos celdas ya selladas, con "NO-APLICA", no con ausencia).
  5. clave sin fuente (§2): celda_d no lleva fuente/fuentes/diseno/
     diseno_datos a su propio nivel -- esos campos existen SOLO dentro de
     cada candidato.

Qué NO valida (declarado, no es descuido): el valor libre de `resultado` y
de `fuerza` fuera del caso COMPLEMENTO. Las dos celdas ya selladas usan
valores fuera del enum terso de §3 ("vigente", "NO_DETERMINADO",
"MEDIDO·PARCIAL(x)") con razón declarada en su propio YAML -- v0.3 §4-bis
ya ejemplifica "vigente" en su propio caso trabajado, y el encabezado de
ambos archivos invoca la regla "§3/§4 difieren -- §4 manda". Forzar aquí un
enum más estricto que el que la propia propuesta ejemplifica rompería los
dos archivos sellados que este validador debe aceptar. La consistencia
entre candidatos BASELINE/CHALLENGER de una misma celda (mismo estimando,
escala comparable, §3.1) tampoco se valida aquí -- es un chequeo entre
celdas relacionadas, no dentro de un solo archivo; queda para el acto de
consolidación cuando existan celdas suficientes para que aplique.
"""
import glob
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELDAS_DIR = os.path.join(ROOT, "data", "curacion-registro", "celdas-d")

TIPOS_ADJUDICACION = {"COMPARACION", "FALSACION", "CALIBRACION_CONJUNTA"}
DOMINIOS = {"FIN", "MIG", "TEC", "CAP", "CUL", "SAL", "SEG", "TRA", "EST", "TIE"}
UNIDADES_OBJETIVO = {"persona", "hogar", "establecimiento", "agregado_geografico"}
ROLES = {"BASELINE", "CHALLENGER", "COMPLEMENTO"}
DISENOS_DATOS = {
    "panel", "pseudo_panel", "transversal", "registro_administrativo",
    "experimento_natural", "auditoria_campo", "enlace_ecologico",
}
ESTRATEGIAS = {"pseudo_panel", "momentos", "composicion", "transversal_con_seleccion", "NO-APLICA"}
ESTADOS_OPERATIVOS = {"LISTO", "LEGACY", "PENDIENTE", "EXCLUIDO"}

# §2: "fuente y diseño nunca en la clave, solo en candidatos" -- estas claves
# solo pueden vivir dentro de un elemento de `candidatos`, nunca al nivel celda_d.
CLAVE_SIN_FUENTE = {"fuente", "fuentes", "diseno", "diseno_datos"}

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
            errs.append(f"{etiqueta}: rol inválido: {rol!r} (v0.3 §3: BASELINE|CHALLENGER|COMPLEMENTO)")

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

    print(f"{len(paths)} archivo(s) de celda-D validan contra propuesta-motor-adaptativo-celda-v0_3.md §3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
