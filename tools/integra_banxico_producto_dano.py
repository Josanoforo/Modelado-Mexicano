#!/usr/bin/env python3
"""Actualiza sólo la relación Banxico de N34 con la medición sellada."""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from curador_registro.tsv_crudo import leer_lineas, upsert_fila  # noqa: E402


REL_ID = "REL-defde50a805b668d2f395b84"
CALC = "CALC-BANXICO-PRODUCTO-DANO-0001"
CALC_DIR = f"data/corrida0/{CALC}"
OUT_DIR = "data/banxico-producto-dano-medicion"
NOTE = "forense/notas/2026-09-12-GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO-cierre.md"
REG = ROOT / "data" / "curacion-registro"


def fields(path: Path) -> list[str]:
    return leer_lineas(path)[0].split("\t")


def row_for(path: Path, key: str, value: str) -> dict[str, str]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row[key] == value]
    if len(rows) != 1:
        raise ValueError(f"{path}: {key}={value} resuelve {len(rows)} filas")
    return rows[0]


def main() -> None:
    relations = REG / "relaciones.tsv"
    utility = REG / "utilidad-modelo.tsv"
    evidence = REG / "evidencias.tsv"

    rel = row_for(relations, "relacion_id", REL_ID)
    rel.update({
        "evidencia_ref": f"MAIN:forense/notas/2026-09-11-GEN2-N34-DATOS-PRODUCTO-Y-DANO-cierre.md;{CALC_DIR}/resultados.json;{OUT_DIR}/estimandos.csv;{NOTE}",
        "evidencia_textual_breve": "Medicion sellada 2019-2024 por cinco productos: pago, atraso/imposibilidad, problemas, reclamacion filtrada y conjunta costo percibido-pago; 2024 dano combinado 4.25% TDC, 18.68% hipotecario, 8.57% personal, 10.35% nomina y 4.31% automotriz.",
        "nota": "Relacion confirmada y medida para descripcion/asociacion mexicana por producto y ola. CALC-BANXICO-PRODUCTO-DANO-0001 REPRODUCE y control independiente COINCIDE. Categoria de producto, no institucion; costo percibido 0-10, no tasa ni CAT; sin UPM/estrato acreditados no hay EE/IC; sin asignacion exogena; universo 18-70 en localidades de 50 mil o mas. Cero adopcion; NC-0164 sigue abierta.",
    })
    upsert_fila(relations, rel, fields(relations), clave="relacion_id")

    util = row_for(utility, "relacion_id", REL_ID)
    util.update({
        "uso_actual": "Medicion descriptiva/asociativa sellada por producto y ola para N34/R1.7; cero parametro adoptado.",
        "evidencia_disponible": f"{CALC_DIR}/resultados.json; {OUT_DIR}/estimandos.csv, conjunta-costo-pago.csv, costo-dano-2024.csv y ficha ficha-consumo-banxico.md; control independiente COINCIDE.",
        "reserva": "No causal; costo subjetivo no equivale a CAT; producto es categoria; universo excluye localidades menores de 50 mil; sin EE/IC por diseno no acreditado; celdas de costo frecuentemente pequenas.",
        "verificacion_requerida": "Completada: spec previa, 35/35 RESULT reproducen, control independiente de cociente/filtro/no-levantado/cobertura/hashes coincide.",
        "siguiente_accion": "Consumir sólo como descripcion/asociacion en N34/R1.7; mantener NC-0164 abierta y buscar producto/lender mexicano exacto, costo objetivo e identificacion causal.",
        "evidencia_ref": f"{CALC_DIR}/resultados.json;{NOTE}",
    })
    upsert_fila(utility, util, fields(utility), clave="relacion_id")

    prov_id = "PROV-" + hashlib.sha256(f"{REL_ID}|{CALC}".encode()).hexdigest()[:24]
    new_evidence = {
        "procedencia_id": prov_id,
        "relacion_id": REL_ID,
        "necesidad_id": "N34",
        "fuente_canonica_normalizada": "BANXICO_SATISFACCION_USUARIOS_2019_2024",
        "objeto_evidencia_id_canonico": "OE-080f605caa1d07c7558b3d89",
        "procedencia_necesidad_id": "N34",
        "procedencia_fuente": "BANXICO_SATISFACCION_USUARIOS_2019_2024",
        "procedencia_objeto_evidencia_id": CALC,
        "accion_normalizacion": "MEDICION_NUEVA_MISMA_RELACION",
        "clasificacion_relacion": "CONFIRMADA",
        "tipo_evidencia": "CALC_SELLADO_Y_AGREGADOS",
        "evidencia_ref": f"{CALC_DIR}/resultados.json",
        "evidencia_localizador": f"{OUT_DIR}/estimandos.csv;{OUT_DIR}/conjunta-costo-pago.csv;{OUT_DIR}/costo-dano-2024.csv",
        "variable_reactivo_tabla": "fecha;ponderador;tdc|hip|per|nom|aut_filtro;*_intereses;*_comp_pago;*_problemas;*_reclamacion",
        "texto_evidencia": "Puntos ponderados auditables 2019-2024; 2024 union atraso/imposibilidad: TDC 4.25%, hipotecario 18.68%, personal 8.57%, nomina 10.35%, automotriz 4.31%.",
        "unidad_observacion": "PERSONA-OLA-PRODUCTO",
        "periodo": "2019-2024",
        "universo_muestra": "12,408 filas; personas mexicanas de 18-70 con producto financiero en localidades de 50 mil habitantes o mas; olas transversales; productos no excluyentes.",
        "codificacion": "Pago valido 1-4; TDC atraso=3/impago=4; otros atraso=2|3/imposibilidad=4; costo 0-10; problemas/reclamacion 1|2; reclamacion condicionada a problema=1; faltantes separados.",
        "parte_necesidad_cubierta": "Descripcion y asociacion mexicana entre categoria de producto, costo percibido, pago y problemas/reclamacion en la misma fila.",
        "parte_necesidad_no_cubierta": "Lender o BNPL mexicano exacto, CAT/tasa/friccion objetiva, diseno para EE/IC e identificacion causal.",
        "uso_potencial_modelo": "Contexto descriptivo/asociativo para N34/R1.7 y encargo 40; no calibrar ni adoptar probabilidad.",
        "transformacion_requerida": "Ninguna adicional para tablas publicadas; conservar denominadores, producto, ola, escala 0-10 y codigos originales.",
        "incertidumbre": "Sin EE/IC porque no se acreditaron UPM/estratos/procedimiento; 37/55 celdas costo-dano 2024 tienen n<30; seleccion, autorreporte y confusion.",
        "siguiente_accion": "Consumir como descripcion/asociacion; mantener NC-0164 abierta para evidencia mexicana objetiva y causal.",
        "objeto_modelo_origen": "dinero.credito.baja_friccion_usura_dano_downstream",
        "objeto_modelo_origen_ref": "MAIN:data/curacion-registro/necesidad-objeto-modelo.tsv:N34",
    }
    upsert_fila(evidence, new_evidence, fields(evidence), clave="procedencia_id")
    print(f"integracion Banxico aplicada: {REL_ID}; evidencia={prov_id}; SHED/CFPB/NC-0164 intactas")


if __name__ == "__main__":
    main()
