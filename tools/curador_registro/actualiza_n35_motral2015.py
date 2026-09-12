#!/usr/bin/env python3
"""Actualiza por clave las tres vistas acopladas de la relación N35/MOTRAL."""
from __future__ import annotations

import csv
import json
import shutil
import tempfile
from pathlib import Path

try:
    from .baseline import ARCHIVOS_TSV, validar_baseline
    from .integrate_barrido2 import _replace_with_rollback
    from .sync_bootstrap import _freeze_manifest
    from .tsv_crudo import upsert_fila
except ImportError:
    from baseline import ARCHIVOS_TSV, validar_baseline
    from integrate_barrido2 import _replace_with_rollback
    from sync_bootstrap import _freeze_manifest
    from tsv_crudo import upsert_fila


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data/curacion-registro"
RELATION_ID = "REL-31a794c27eca54d8d773df15"
REF = "forense/notas/2026-09-11-GEN2-N35-PREFERENCIAS-LABORALES-Y-FUENTES-cierre.md"


def read_one(path: Path, key: str, value: str) -> tuple[list[str], dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = [row for row in reader if row[key] == value]
        fields = list(reader.fieldnames or [])
    if len(rows) != 1:
        raise ValueError(f"{path.name}:{key}={value}: esperado 1, observado {len(rows)}")
    return fields, rows[0]


def main() -> int:
    template = json.loads((REGISTRY / "baseline.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="actualiza-n35-", dir=REGISTRY.parent) as temporary:
        candidate = Path(temporary) / "registro"
        candidate.mkdir()
        for filename in [*ARCHIVOS_TSV.values(), "baseline.json"]:
            shutil.copy2(REGISTRY / filename, candidate / filename)

        relation_fields, relation = read_one(candidate / "relaciones.tsv", "relacion_id", RELATION_ID)
        relation.update({
            "id_manifiesto": "motral2015_bases_datos_dbf",
            "sha256_fuente": "e86e4e6b350914276bd57a8354f145364c999f35c08c041ee4c5559f9c82741d",
            "capa4_apertura_mapeo": "EXISTE-NO-SATISFACE",
            "reason_code": "APERTURA_POSITIVA_EXPLICITA",
            "evidencia_ref": REF,
            "evidencia_textual_breve": "MOTRAL 2015 P16 ordena cinco prestaciones y P17 valora empleo con seguridad social aun pagando; CALC ejecutado; sin salarios alternativos explícitos",
            "nota": "Enmienda 2026-09-11: se conserva la evidencia histórica 2012 y se corrige únicamente el descarte de 2015. P16/P17 fueron acreditadas y medidas por CALC-MOTRAL2015-VALORACION-SS-0001; P17 no compara dos salarios, por lo que R2.3 estricta permanece EXISTE-NO-SATISFACE. Sin adopción ni cambio de tier.",
        })
        upsert_fila(candidate / "relaciones.tsv", relation, relation_fields, clave="relacion_id")

        evidence_fields, evidence = read_one(candidate / "evidencias.tsv", "relacion_id", RELATION_ID)
        evidence.update({
            "procedencia_fuente": "MOTRAL2012_BD_DBF;MOTRAL2015_BASES_DATOS_DBF;MOTRAL2015_CUESTIONARIO;MOTRAL2015_ESTRUCTURA_BD;MOTRAL2015_DOCUMENTO_METODOLOGICO;ENOE_2015_TRIM2_DBF",
            "tipo_evidencia": "APERTURA_DIRECTA;MEDICION_SELLADA",
            "evidencia_ref": REF,
            "evidencia_localizador": "motral2015_bases_datos_dbf.zip:motral2015_cuestionario.dbf[P16_1..P16_5,P17,FAC_MOTRAL];SDEMT215.DBF[CLASE2,SEG_SOC];CALC-MOTRAL2015-VALORACION-SS-0001",
            "variable_reactivo_tabla": "P16_1..P16_5={rangos 1..5 de servicio médico, vida, accidentes, pensión, vivienda};P17={1 sí,2 no};FAC_MOTRAL;SEG_SOC={1 acceso,2 sin acceso,3 no especificado}",
            "texto_evidencia": "EXISTE-NO-SATISFACE para R2.3 estricta; sí existe valoración declarada 2015: P17 afirmativa ponderada=0.823626705331 y distribución P16 publicada en 32 estimandos",
            "unidad_observacion": "persona seleccionada MOTRAL; cruce persona con empleo actual ENOE",
            "periodo": "2015; ENOE 2015-T2",
            "universo_muestra": "MOTRAL urbano, 18-54 con experiencia laboral y entrevista completa; n elegible=5704; FAC_MOTRAL",
            "codificacion": "P17 1=Sí 2=No; P16 exige primer lugar único entre cinco rangos; unión CD_A+ENT+CON+V_SEL+N_HOG+H_MUD+N_REN uno-a-uno",
            "parte_necesidad_cubierta": "Valoración declarada de seguridad social aun pagando; prioridad ordinal de cinco prestaciones; corte descriptivo por cobertura actual",
            "parte_necesidad_no_cubierta": "Comparación estricta prestaciones frente a alternativas con salarios explícitos y regla generalizable/adoptable",
            "uso_potencial_modelo": "Capa descriptiva y antecedente para diseñar una regla futura; no calibra ni sustituye R2.3",
            "transformacion_requerida": "Para R2.3 futura: definir prospectivamente contraste salarial/prestación y regla de transporte; no derivarlo de P17",
            "incertidumbre": "Puntos, n, masas, EE e IC sellados; control independiente valida P17 total, rankings y join, no todos los cortes ni la inferencia; experimento DCE sólo transcrito sin microdato público",
            "siguiente_accion": "Mesa decide si abre regla sucesora basada en DCE; antes obtener Appendix C, bloques, microdato anonimizado y código del estudio mexicano",
        })
        upsert_fila(candidate / "evidencias.tsv", evidence, evidence_fields, clave="relacion_id")

        utility_fields, utility = read_one(candidate / "utilidad-modelo.tsv", "relacion_id", RELATION_ID)
        utility.update({
            "estado_productivo": "MEDICION_DISPONIBLE_NO_PARAMETRO",
            "uso_actual": "Exploración/medición descriptiva según reserva; no parámetro definitivo",
            "evidencia_disponible": "SI",
            "reserva": "P17 no contiene salarios alternativos; DCE publicado sin paquete reproducible; ninguna adopción",
            "verificacion_requerida": "No aplica para conservar la medición descriptiva; cualquier parámetro exige regla y spec sucesora",
            "requiere_decision": "NO",
            "decision_id": "NO_APLICA",
            "siguiente_accion": "Entregar CALC/RESULT a 40; mesa puede abrir después una regla DCE explícita sin reemplazar R2.3",
            "evidencia_ref": REF,
        })
        upsert_fila(candidate / "utilidad-modelo.tsv", utility, utility_fields, clave="relacion_id")

        _freeze_manifest(candidate, template)
        validation = validar_baseline(candidate)
        if not validation["ok"]:
            raise ValueError("BASELINE_CANDIDATO_INVALIDO:" + ";".join(validation["errores"]))
        changed = ("relaciones.tsv", "evidencias.tsv", "utilidad-modelo.tsv", "baseline.json")
        outputs = {REGISTRY / name: (candidate / name).read_bytes() for name in changed}
        _replace_with_rollback(outputs, REGISTRY)
    print(f"ACTUALIZADA {RELATION_ID} por clave; baseline válido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
