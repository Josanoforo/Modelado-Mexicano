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

# Cotejo documental fechado del sucesor. El estatus sellado del catálogo se
# conserva por separado; estas operaciones no son adopciones ni nuevos CALC.
CATALOGO_COTEJO = {
    "M01": ("ENCIG P8_3=solicitud, no pago ni discrecionalidad sin registro", "NO-EQUIVALENTE-PAGO; mesa fija pregunta de pago y estrato registro antes de CALC"),
    "M02": ("ENCIG P8_3/P8_4 no identifica pago normal con registro", "NO-EQUIVALENTE-PAGO; mesa fija pregunta y denominador de pago con registro"),
    "M03": ("R3.4: Banxico mide adopcion agregada CoDi; condicion B/C carece de riesgo fiscal separado de friccion", "PARCIAL-NO-EQUIVALENTE; mesa fija instrumento individual de adopcion, riesgo y friccion"),
    "M04": ("R3.4: Banxico SPEI mide uso agregado; ENIF 2024 uso declarado CoDi no mide utilidad sin coercion", "PARCIAL-NO-EQUIVALENTE; mesa fija reactivo de utilidad y ausencia de coercion en una persona"),
    "M06": ("modelo §3.1 exige puente personal, respaldo y adopcion coobservados; ENIGH 2022 sin reactivo acreditado", "mesa fija instrumento con las tres preguntas, universo y denominador; despues reserva y CALC"),
    "M07": ("modelo §3.1 cita ENSAFI 2023 y CNBV para CAT/mora/scoring; no es proporcion persona ENIGH 2022", "NO-EQUIVALENTE; mesa elige cartera auditada o respuesta individual sin fabricar conjunta"),
    "M08": ("CALC-ENVIPE-DENUNCIA-SEGURO-0001 mide robo total de vehiculo BPCOD=01 por delito, no persona general", "mesa decide acotar a delito y aceptar NO-REPRODUCE-GEN1, o buscar instrumento persona"),
    "M09": ("R1.4: ENNViH panel D/E sin marca y sustituto en acto de compra; D archivado", "HOLDOUT; requerir instrumento de compra pareada marca/sustituto y nueva reserva"),
    "M10": ("R2.1: HSOPS sin jerarquia familiar/plana y cuatro controles juntos; D archivado", "HOLDOUT; requerir microdato empleado con jerarquia, voz, canal, sector, tamano y escolaridad"),
    "M11": ("R2.2: sin Cheng/Farh junto a retencion y desempeno; D archivado", "HOLDOUT; requerir panel comparable de liderazgo y empleado"),
    "M12": ("R3.4: Banxico A medido, B/C sin fuente que separe riesgo fiscal y friccion; B archivada", "HOLDOUT; requerir identificacion individual o variacion exogena para B/C"),
    "M13": ("R7.1: falta serie municipal pareada y peso percibido del acto", "HOLDOUT; requerir mismo electorado concurrente/no concurrente y peso percibido"),
    "M14": ("R7.3: exige RDD Pension Bienestar sobre eleccion de voto independiente de aprobacion", "HOLDOUT; requerir RDD y no sustituir eleccion de voto por turnout"),
    "M15": ("R7.4: fuentes existentes no unen agravio, respuesta y entorno en un caso; D archivado", "HOLDOUT; requerir registro sistematico comun con entorno y forma de respuesta"),
    "M16": ("R7.5: mismo falsador R7.4, sin registro de autodefensa y protesta comparable; D archivado", "HOLDOUT; requerir mismo registro; no usar protesta como autodefensa"),
    "M17": ("R8.1: requiere contribucion >=2 anos sin sancion fuera de faena/tequio", "HOLDOUT; requerir inventario longitudinal de comites urbanos/mestizos y sanciones"),
    "M18": ("R8.2: apps conocidas carecen de tasa auditada entre desconocidos; B archivado", "HOLDOUT; requerir ROSCA entre desconocidos, dos ciclos y tasa auditada"),
    "M19": ("R8.3: abridor existente mide eje enforcement; A archivada con eje 3 en desacuerdo", "HOLDOUT; cotejar estimando y reservas del abridor antes de proponer CALC nuevo"),
    "M20": ("R10.1: ancla Tlaxcala universitarios, sin contraste superior/inferior fuera de muestra", "HOLDOUT; requerir rechazo codificado y asimetria de poder en muestra definida"),
    "M21": ("R10.2: falta exposicion publica/privada y rotacion/desempeno en panel; D archivado", "HOLDOUT; requerir panel con sector y exposicion"),
    "M22": ("R10.3: solo dato secundario publicado agregado; no recoleccion primaria en zona activa", "HOLDOUT; requerir pre/post proteccion efectiva y testimonio seguro; de otro modo D"),
}


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
        elif mid in CATALOGO_COTEJO:
            dependencia, operacion = CATALOGO_COTEJO[mid]
            dependencia += "; cotejo-documental-catalogo.md; catalogo sellado sigue " + m.estatus_disponibilidad
        else:
            raise AssertionError(f"momento sin cotejo documental: {mid}")
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
