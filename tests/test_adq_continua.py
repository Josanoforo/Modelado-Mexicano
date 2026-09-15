#!/usr/bin/env python3
"""Regresiones mínimas del servicio conectado a demanda efectiva."""
from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import adq_investigacion as I  # noqa: E402

FALLOS = []


def afirma(condicion, mensaje):
    if not condicion:
        FALLOS.append(mensaje)


def _contrato(ident="DEM-X"):
    return {
        "id": ident, "vigente": True, "version_pregunta": "v1",
        "pregunta": "buscar variable X", "consumidor": "modelo:x",
        "uso": "descriptivo", "prioridad_consumidor": 1,
        "bloqueo_material": 2, "lista": True,
        "estado_ruteo": "LISTA_SONDA", "asignacion": "servicio-gen2-38",
        "modos": ["CONSTRUCTO"], "poblacion": "México", "unidad": "persona",
        "periodo": "2026", "variables": "X",
        "evidencia_disponible": "ninguna compatible", "brecha": "falta X",
        "investigacion_previa": "ruta A agotada", "frontera_previa": "ruta B",
        "siguiente_accion": "examinar ruta B", "etapa_faltante": "FUENTE_O_VARIABLE",
        "antecedentes_nc": ["NC-X"], "opciones_decision": ["usar proxy X0"],
    }


def _cfg(raiz):
    (raiz / "forense").mkdir()
    (raiz / "forense/no-corrido.tsv").write_text(
        "id\tque_no_se_corrio\timpacto\testado\n"
        "NC-X\tbrecha histórica\timpacto\tCERRADA\n"
        "NC-Y\tbuscar Y\tfalta Y\tABIERTA\n", encoding="utf-8")
    return {
        "version": "GEN2-ADQ-INVESTIGACION-V1",
        "fuente_necesidades": "forense/no-corrido.tsv",
        "estado_dir": "estado", "reservas_runtime_dir": "reservas",
        "presupuesto_runtime_dir": "runtime", "reserva_minutos": 10,
        "presupuesto_diario": {"necesidades": 3, "objetos": 5,
                                "segundos_ejecutor": 3900},
        "necesidades": [], "demandas_instrumento": [_contrato()],
    }


def prueba_cierre_nc_no_borra_demanda_y_reserva_vence():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        ahora = dt.datetime(2026, 9, 15, tzinfo=dt.timezone.utc)
        seleccion = I.selecciona(cfg, dt.date(2026, 9, 15), raiz=raiz, ahora=ahora)
        afirma("DEM-X" in [x["id"] for x in seleccion["elegidos"]],
               "cerrar la NC antecedente borró la demanda independiente")
        I.reserva_seleccion(seleccion, "RUN-VIEJO", cfg, raiz, ahora)
        tras_vencer = I.selecciona(
            cfg, dt.date(2026, 9, 15), raiz=raiz,
            ahora=ahora + dt.timedelta(minutes=11))
        afirma("DEM-X" in [x["id"] for x in tras_vencer["elegidos"]],
               "una reserva terminada mantuvo exclusión eterna")


def prueba_continuacion_y_alerta_dos_ciclos():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        base = {
            "seleccion_investigacion": {"corte": "2026-09-15"},
            "investigaciones": [{
                "necesidad_id": "DEM-X", "version_pregunta": "v1",
                "estado": "continua", "candidatas": [],
                "proxima_revision": "2026-10-15", "cursor_continuacion": "ruta B/página 2",
                "frontera_no_examinada": "ruta B/página 2", "evidencias": ["nota"],
                "suficiencia": {"uso_habilitado": "INCOMPATIBLE"},
            }],
        }
        p = raiz / "resultado.json"
        p.write_text(json.dumps(base), encoding="utf-8")
        I.actualiza_desde_resultados(p, cfg, raiz)
        estado = json.loads((raiz / "estado/DEM-X.json").read_text())
        afirma(estado["proxima_revision"] == "2026-09-16" and
               estado["continuacion_pendiente"],
               "una frontera concreta quedó congelada treinta días")
        antes = I.selecciona(cfg, dt.date(2026, 9, 15), raiz=raiz)
        despues = I.selecciona(
            cfg, dt.date(2026, 9, 15), raiz=raiz,
            cambios_materiales={"DEM-X"})
        afirma("DEM-X" not in [x["id"] for x in antes["elegidos"]] and
               "DEM-X" in [x["id"] for x in despues["elegidos"]],
               "un cambio material del consumidor no replanificó su agenda")
        base["seleccion_investigacion"]["corte"] = "2026-09-16"
        p.write_text(json.dumps(base), encoding="utf-8")
        I.actualiza_desde_resultados(p, cfg, raiz)
        estado2 = json.loads((raiz / "estado/DEM-X.json").read_text())
        afirma(estado2["alternativa_requerida"] and estado2["alternativas"],
               "dos ciclos sin avance no produjeron alternativa concreta")


def prueba_presupuesto_diario_es_agregado_e_idempotente():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        fecha = dt.date(2026, 9, 15)
        uno = I.reserva_presupuesto(cfg, fecha, "RUN-1", 2, 3, 3900, raiz)
        dos = I.reserva_presupuesto(cfg, fecha, "RUN-1", 2, 3, 3900, raiz)
        afirma(uno["usado"] == dos["usado"] == {
            "necesidades": 2, "objetos": 3, "segundos_ejecutor": 3900},
            "reintentar el mismo run_id duplicó el consumo")
        try:
            I.reserva_presupuesto(cfg, fecha, "RUN-2", 1, 1, 1, raiz)
        except RuntimeError:
            paso = True
        else:
            paso = False
        afirma(paso, "una segunda activación excedió el techo agregado diario")
        comprobacion = raiz / "forense/adq-log/estado/comprobacion.json"
        comprobacion.parent.mkdir(parents=True)
        comprobacion.write_text(json.dumps({"presupuesto": {"obsoleto": True}}),
                                 encoding="utf-8")
        ciclo = I.registra_ciclo(cfg, fecha, "RUN-1", raiz)
        afirma(ciclo["presupuesto"]["disponible"] == {
            "necesidades": 1, "objetos": 2, "segundos_ejecutor": 0},
            "el cierre persistió el presupuesto anterior a la reserva")


def main():
    prueba_cierre_nc_no_borra_demanda_y_reserva_vence()
    prueba_continuacion_y_alerta_dos_ciclos()
    prueba_presupuesto_diario_es_agregado_e_idempotente()
    if FALLOS:
        print(f"FALLÓ ({len(FALLOS)}):")
        for fallo in FALLOS:
            print("  ·", fallo)
        return 1
    print("OK -- test_adq_continua.py: 3 grupos, 0 fallos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
