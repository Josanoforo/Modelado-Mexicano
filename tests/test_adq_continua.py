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


def prueba_reserva_liquidacion_y_segunda_activacion():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        fecha = dt.date(2026, 9, 15)
        I.reserva_presupuesto(cfg, fecha, "RUN-1", 1, 5, 3900, raiz)
        uno = I.liquida_presupuesto(
            cfg, fecha, "RUN-1", 1, 0, 250, raiz,
            evidencia="fixture aceptación 1/0/250")
        dos = I.liquida_presupuesto(
            cfg, fecha, "RUN-1", 1, 0, 250, raiz,
            evidencia="reintento idempotente")
        esperado = {"necesidades": 2, "objetos": 5,
                    "segundos_ejecutor": 3650}
        afirma(uno["disponible"] == dos["disponible"] == esperado,
               "liquidar 1/0/250 no devolvió 0/5/3650 exactamente una vez")
        afirma(uno["consumido"] == {"necesidades": 1, "objetos": 0,
                                     "segundos_ejecutor": 250},
               "el ledger no separó consumo consolidado de reserva")
        I.reserva_presupuesto(cfg, fecha, "RUN-2", 1, 2, 100, raiz)
        tres = I.liquida_presupuesto(cfg, fecha, "RUN-2", 1, 1, 40, raiz)
        afirma(tres["consumido"] == {"necesidades": 2, "objetos": 1,
                                      "segundos_ejecutor": 290},
               "la segunda activación no compartió el consumo del día")


def prueba_checkpoints_fallos_timeout_y_publicacion():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        fecha = dt.date(2026, 9, 15)
        # Fallo antes de arrancar: todo vuelve.
        I.reserva_presupuesto(cfg, fecha, "NO-ARRANCO", 1, 2, 100, raiz)
        fallo = I.liquida_presupuesto(cfg, fecha, "NO-ARRANCO", 0, 0, 0, raiz)
        afirma(fallo["disponible"] == {"necesidades": 3, "objetos": 5,
                                        "segundos_ejecutor": 3900},
               "un arranque fallido retuvo capacidad no usada")

        # Un resultado incompleto conserva intentos por checkpoint y cobra al
        # menos la investigación cuyo ejecutor el wrapper sí inició.
        I.reserva_presupuesto(cfg, fecha, "TIMEOUT", 2, 3, 300, raiz)
        I.checkpoint_presupuesto(cfg, fecha, "TIMEOUT", "ejecutor", "proceso", raiz)
        I.checkpoint_presupuesto(cfg, fecha, "TIMEOUT", "objetos", "OBJ-X", raiz)
        I.checkpoint_presupuesto(cfg, fecha, "TIMEOUT", "objetos", "OBJ-X", raiz)
        timeout = I.liquida_presupuesto(
            cfg, fecha, "TIMEOUT", 0, 0, 300, raiz,
            asegurar_investigacion_iniciada=True, evidencia="timeout")
        afirma(timeout["consumido"] == {"necesidades": 1, "objetos": 1,
                                         "segundos_ejecutor": 300},
               "timeout perdió el trabajo iniciado o duplicó checkpoint")

        # Publicar después no reabre ni vuelve a cobrar el trabajo.
        repetida = I.liquida_presupuesto(
            cfg, fecha, "TIMEOUT", 2, 3, 300, raiz,
            asegurar_investigacion_iniciada=True,
            evidencia="publicación reintentada")
        afirma(repetida["consumido"] == timeout["consumido"],
               "reintentar publicación alteró el consumo consolidado")


def prueba_huerfanas_y_dimensiones_independientes():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        fecha = dt.date(2026, 9, 15)
        # Una reserva cuyo proceso sigue vivo no se toca ni con lock declarado.
        I.reserva_presupuesto(cfg, fecha, "VIVA", 1, 1, 100, raiz)
        viva = I.recupera_reservas_huerfanas(cfg, fecha, "OTRA", True, raiz)
        rv = next(r for r in viva["reservas"] if r["run_id"] == "VIVA")
        afirma(rv["estado"] == "activa", "se liberó una reserva de proceso vivo")
        I.liquida_presupuesto(cfg, fecha, "VIVA", 0, 0, 0, raiz)

        # PID/starttime incompatibles prueban orfandad pre-arranque: vuelve todo.
        I.reserva_presupuesto(cfg, fecha, "HUERFANA", 1, 1, 100, raiz)
        ledger = raiz / "runtime/presupuesto-2026-09-15.json"
        dato = json.loads(ledger.read_text())
        rh = next(r for r in dato["reservas"] if r["run_id"] == "HUERFANA")
        rh["pid"] = 99999999
        rh["proceso_inicio"] = "no-existe"
        ledger.write_text(json.dumps(dato), encoding="utf-8")
        recuperado = I.recupera_reservas_huerfanas(
            cfg, fecha, "SIGUIENTE", True, raiz)
        rh2 = next(r for r in recuperado["reservas"] if r["run_id"] == "HUERFANA")
        afirma(rh2["estado"] == "liquidada" and
               rh2["consumido"] == {"necesidades": 0, "objetos": 0,
                                     "segundos_ejecutor": 0},
               "la reserva huérfana pre-arranque no se recuperó con evidencia")

        # Agotar objetos no paraliza investigación; cada run conserva tiempo.
        I.reserva_presupuesto(cfg, fecha, "OBJETOS", 0, 5, 100, raiz)
        I.liquida_presupuesto(cfg, fecha, "OBJETOS", 0, 5, 100, raiz)
        tras_objetos = I.reserva_presupuesto(
            cfg, fecha, "SOLO-INVESTIGA", 1, 0, 50, raiz)
        afirma(tras_objetos["reservado_activo"]["necesidades"] == 1 and
               tras_objetos["disponible"]["objetos"] == 0,
               "agotar objetos paralizó una investigación independiente")


def prueba_migracion_legacy_con_evidencia_no_inventa_credito():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        fecha = dt.date(2026, 9, 15)
        ledger = raiz / "runtime/presupuesto-2026-09-15.json"
        ledger.parent.mkdir(parents=True)
        ledger.write_text(json.dumps({
            "fecha": "2026-09-15",
            "usado": {"necesidades": 1, "objetos": 5,
                      "segundos_ejecutor": 3900},
            "reservas": [{
                "run_id": "2026-09-15T104704-88296",
                "necesidades": 1, "objetos": 5,
                "segundos_ejecutor": 3900,
            }],
        }), encoding="utf-8")
        incierto = I.recupera_reservas_huerfanas(
            cfg, fecha, "SIGUIENTE", True, raiz)
        afirma(incierto["recuperacion_pendiente"] == [
            "2026-09-15T104704-88296"],
            "una reserva legacy incierta se liberó sin logs/eventos")
        migrado = I.liquida_presupuesto(
            cfg, fecha, "2026-09-15T104704-88296", 1, 0, 227, raiz,
            evidencia="límites del hijo en log histórico")
        afirma(migrado["consumido"] == {
            "necesidades": 1, "objetos": 0, "segundos_ejecutor": 227} and
               migrado["disponible"] == {
                   "necesidades": 2, "objetos": 5,
                   "segundos_ejecutor": 3673},
               "migrar el ledger legacy no produjo 1/0/227 y 2/5/3673")
        repetido = I.liquida_presupuesto(
            cfg, fecha, "2026-09-15T104704-88296", 0, 0, 0, raiz)
        afirma(repetido["consumido"] == migrado["consumido"],
               "repetir la migración legacy devolvió o cobró dos veces")


def prueba_checkpoint_runtime_no_repite_rama_sin_fusionar():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _cfg(raiz)
        fecha = dt.date(2026, 9, 15)
        resultado = raiz / "resultado.json"
        resultado.write_text(json.dumps({"investigaciones": [{
            "necesidad_id": "DEM-X", "version_pregunta": "v1",
            "estado": "continua", "proxima_revision": "2026-09-16",
        }]}), encoding="utf-8")
        ciclo = I.registra_ciclo(
            cfg, fecha, "RUN-PUBLICADO-SIN-MERGE", raiz, resultado)
        marca = ciclo["investigaciones_atendidas"]["DEM-X"]
        afirma(marca["run_id"] == "RUN-PUBLICADO-SIN-MERGE" and
               marca["proxima_revision"] == "2026-09-16",
               "el cierre no preservó la investigación publicada sin merge")
        seleccion = {"elegidos": [{"id": "DEM-X", "version_pregunta": "v1"}],
                     "excluidos": []}
        filtrada = I._excluye_atendidas_runtime(
            seleccion, ciclo, fecha, set())
        afirma(not filtrada["elegidos"] and
               "RUN-PUBLICADO-SIN-MERGE" in filtrada["excluidos"][0]["razon"],
               "la segunda activación repetiría la misma versión antes del merge")
        reactivada = I._excluye_atendidas_runtime(
            {"elegidos": [{"id": "DEM-X", "version_pregunta": "v1"}],
             "excluidos": []}, ciclo, fecha, {"DEM-X"})
        afirma(len(reactivada["elegidos"]) == 1,
               "un cambio material no reactivó la investigación atendida")


def main():
    prueba_cierre_nc_no_borra_demanda_y_reserva_vence()
    prueba_continuacion_y_alerta_dos_ciclos()
    prueba_presupuesto_diario_es_agregado_e_idempotente()
    prueba_reserva_liquidacion_y_segunda_activacion()
    prueba_checkpoints_fallos_timeout_y_publicacion()
    prueba_huerfanas_y_dimensiones_independientes()
    prueba_migracion_legacy_con_evidencia_no_inventa_credito()
    prueba_checkpoint_runtime_no_repite_rama_sin_fusionar()
    if FALLOS:
        print(f"FALLÓ ({len(FALLOS)}):")
        for fallo in FALLOS:
            print("  ·", fallo)
        return 1
    print("OK -- test_adq_continua.py: 8 grupos, 0 fallos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
