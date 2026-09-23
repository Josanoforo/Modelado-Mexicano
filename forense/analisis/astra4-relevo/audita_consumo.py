#!/usr/bin/env python3
"""Contrasta las 40 filas de procedencia y 23 momentos con sus lectores reales."""
from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from milpa.src import matriz, motor, momentos, procedencia  # noqa: E402

OUT = Path(__file__).resolve().parent
INV = list(csv.DictReader((OUT / "inventario-operativo.tsv").open(), delimiter="\t"))


def write(name, fields, rows):
    with (OUT / name).open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def procedencia_rows():
    proc = procedencia.cargar()
    B = matriz.cargar_B(proc)
    result = motor.correr()
    assert len(B.celdas) == 15 and len(result["resultados"]) == 21
    rows = []
    for row in INV:
        if not row["consumidor"].startswith("milpa/procedencia.yaml:"):
            continue
        typ = row["tipo_uso"]
        suffix = row["consumidor"].split(":", 2)[-1]
        if typ == "coeficiente_ejecutable":
            gen, coef = suffix.split(".", 1)
            val = B.celdas[(gen, coef)].valor
            assert abs(val - float(row["valor_actual"])) < 1e-9
            consulta = "B_CARGA_VALOR"
            emision = "NO-EMITE-MAGNITUD-E0"
            evidence = "milpa/src/matriz.py:cargar_B; milpa/src/motor.py:correr/evaluar"
            next_op = "COTEJAR-RESULT-ORIGEN-Y-CALC; escritor-procedencia propio solo con firma; conservar reserva asociacion"
        elif typ == "coeficiente_asignado":
            gen, coef = suffix.split(".", 1)
            cell = B.celdas[(gen, coef)]
            # Estos ocho son el fallback efectivo; ninguno fue sustituido por sellado.
            if isinstance(cell, matriz.CoeficienteSinMagnitud):
                assert row["valor_actual"].strip("'") == cell.literal
                consulta = "B_CARGA_SIN_MAGNITUD"
            else:
                assert cell.valor == float(row["valor_actual"])
                consulta = "B_CARGA_FALLBACK_ASIGNADO"
            emision = "NO-EMITE-MAGNITUD-E0"
            evidence = "milpa/src/matriz.py:cargar_B; milpa/src/motor.py:correr/evaluar"
            next_op = "DISEÑAR-CALC-COEFICIENTE-POR-PAR; comprobar identificabilidad y reserva; escritor-procedencia con firma"
        elif typ == "asignado_probabilidad":
            key = suffix
            assert any(x.get("regla") == key for x in proc.crudo["asignados_probabilidad"])
            consulta = "YAML_CARGADO_SIN_LECTURA_NUMERICA_DEL_MOTOR"
            emision = "NO-EMITE-MAGNITUD-E0"
            evidence = "milpa/src/procedencia.py:cargar; milpa/src/motor.py:correr; milpa/src/emisor.py:apagar_generador"
            next_op = "COTEJAR-REGLA-Y-ESTIMANDO; CALC-POR-CONDICION-O-DICTAMEN-HISTORICO; firma antes de reclasificar"
        else:
            assert typ == "condicional_theta"
            assert any(x.ruta_yaml == tuple(suffix.split("/")) for x in proc.entradas)
            consulta = "ENTRADA_CONSUMIBLE_SIN_THETA_NUMERICA"
            emision = "NO-EMITE-MAGNITUD-E0"
            evidence = "milpa/src/procedencia.py:consumibles; milpa/src/theta.py:valor; milpa/src/motor.py:correr"
            next_op = "COTEJAR-EJE-Y-ESTIMANDO; CALC-CONDICIONAL-O-DICTAMEN-HISTORICO; Theta.valor lanza"
        rows.append(dict(slot=row["slot"], consumidor=row["consumidor"], tipo=typ,
                         valor_legacy=row["valor_actual"], consulta_efectiva=consulta,
                         emision=emision, prueba=evidence, dictamen="NO-HISTORICO-SIN-FIRMA",
                         siguiente_operacion=next_op))
    assert len(rows) == 40
    return rows


def catalogo_rows():
    cat = momentos.cargar_catalogo()
    by_id = {x.id_momento: x for x in cat.momentos}
    rows = []
    for row in INV:
        if row["tipo_uso"] != "momento":
            continue
        mid = row["consumidor"].split(":")[-1]
        m = by_id[mid]
        if mid == "M05":
            dependencia = "reserva de cruce 2025 ya consumida; arbitro y emisiones sellados, champion NINGUNO"
            operacion = "cotejar RESULT de CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001 y EMISIONES-0001 con estimando; decidir nueva reserva antes de otro CALC"
        elif mid == "M23":
            dependencia = "HOLDOUT de evaluación 2024 ya consumido; champion NINGUNO; lectura de valor prohibida en E0"
            operacion = "conservar sello de CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001 y EMISIONES-0001; pedir nuevo diseño y reserva para otra evaluación"
        elif m.rol_calibracion == "HOLDOUT":
            dependencia = f"ficha {m.objeto_modelo} sin instrumento/universo declarado en catálogo; muro HOLDOUT E0"
            operacion = f"localizar ficha {m.objeto_modelo} de forense/hitoD-preregistro-v2_0.md; fijar instrumento, universo, umbral y reserva en acto prospectivo; CALC solo tras apertura autorizada"
        else:
            dependencia = "universo de búsqueda POR DECLARAR; identidad instrumento-regla y reserva sin acreditar"
            operacion = f"cotejar reactivo y FD del instrumento para {m.objeto_modelo}; fijar universo/denominador y reserva; congelar CALC-RELEVO antes del dato"
        rows.append(dict(slot=row["slot"], momento=mid, objeto=m.objeto_modelo,
                         rol=m.rol_calibracion, estatus=m.estatus_disponibilidad,
                         plan_fechado="2026-09-23: decisión de secuencia, sin fecha ficticia de entrega",
                         dependencia=dependencia, operacion=operacion,
                         consumo_efectivo="METADATOS; valor_de() bloquea HOLDOUT o AJUSTE no implementado"))
    assert len(rows) == 23 and len(by_id) == 23
    return rows


if __name__ == "__main__":
    write("uso-efectivo-procedencia.tsv", ["slot", "consumidor", "tipo", "valor_legacy",
          "consulta_efectiva", "emision", "prueba", "dictamen", "siguiente_operacion"], procedencia_rows())
    write("plan-catalogo-23.tsv", ["slot", "momento", "objeto", "rol", "estatus",
          "plan_fechado", "dependencia", "operacion", "consumo_efectivo"], catalogo_rows())
    print("procedencia=40; catalogo=23")
