#!/usr/bin/env python3
"""Casos dirigidos de GEN2-ADQUISICION-CIERRE-VERIFICABLE-Y-PRODUCCION."""
import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
sys.path.insert(0, str(RAIZ / "tests"))
import adq_doctor as D  # noqa: E402
import check as C  # noqa: E402

FALLOS = []


def afirma(condicion, mensaje):
    if not condicion:
        FALLOS.append(mensaje)


def _seleccion(ids):
    return {"corte": "2026-09-11", "maximo": 5,
            "elegidos": [{"id": x, "estado": "PENDIENTE", "prioridad": "1",
                           "intento_efectivo": None, "razon": "sin intento previo registrado"}
                          for x in ids],
            "excluidos": []}


def _resultado(ids, estado="intentos_documentados", resultados=None,
               publicacion="publicada"):
    return {
        "ejecutor": "codex",
        "seleccion": {"calculada": True, "corte": "2026-09-11", "maximo": 5,
                      "elegidos": ids, "excluidos_con_causa": []},
        "seleccion_investigacion": {
            "calculada": True, "corte": "2026-09-11", "maximo": 0,
            "elegidos": [], "excluidos_con_causa": []},
        "investigaciones": [],
        "resultado_sustantivo": estado,
        "resultados_por_objeto": resultados or [],
        "publicacion_trabajo": {
            "estado": publicacion,
            "referencias": ([{"ref": "refs/heads/adq/fixture",
                              "commit": "a" * 40}]
                             if publicacion == "publicada" else []),
        },
        "resumen": "fixture",
    }


def _raiz_fixture():
    td = tempfile.TemporaryDirectory()
    raiz = Path(td.name)
    (raiz / "tools").mkdir()
    shutil.copy2(RAIZ / "tools" / "adq-resultado.schema.json",
                 raiz / "tools" / "adq-resultado.schema.json")
    (raiz / "data" / "curacion-registro").mkdir(parents=True)
    (raiz / "data" / "raw").mkdir()
    (raiz / "forense").mkdir()
    return td, raiz


def prueba_h2_rechaza_tres_falsos_positivos():
    td, raiz = _raiz_fixture()
    try:
        (raiz / "data" / "manifiesto.yaml").write_text("[]\n", encoding="utf-8")
        (raiz / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv").write_text(
            "fuente_canonica\testado_A4A5\tnota\nOBJ\tPENDIENTE\t\n", encoding="utf-8")
        seleccion = _seleccion(["OBJ"])
        casos = [
            _resultado(["OBJ"], estado="cola_vacia", publicacion="no_aplica"),
            _resultado(["OBJ"], estado="adquisicion_obtenida"),
            _resultado(["OBJ"], estado="intentos_documentados"),
        ]
        for i, caso in enumerate(casos, 1):
            r = D.valida_resultado_adquisicion(caso, seleccion,
                                                comprobar_remoto=False, raiz=raiz)
            afirma(not r["valido"], f"H2 caso {i}: respuesta incoherente fue aceptada: {r}")
    finally:
        td.cleanup()


def prueba_resultado_parcial_y_publicacion_separada():
    td, raiz = _raiz_fixture()
    try:
        evidencia = raiz / "forense" / "recetas.md"
        evidencia.write_text("OBJ: curl 60 TLS roto\n", encoding="utf-8")
        (raiz / "data" / "manifiesto.yaml").write_text("[]\n", encoding="utf-8")
        (raiz / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv").write_text(
            "fuente_canonica\testado_A4A5\tnota\n"
            "OBJ\tNO-OBTENIDO-POR-ESTE-AGENTE(1 intentos)\tintento efectivo 2026-09-11: curl 60 TLS roto\n",
            encoding="utf-8")
        por_objeto = [{"objeto_id": "OBJ", "desenlace": "intento_documentado",
                       "evidencias": ["forense/recetas.md"],
                       "intentos": [{"via": "URL directa", "resultado": "curl 60 TLS roto"}],
                       "archivos": [], "ids_manifiesto": []}]
        caso = _resultado(["OBJ"], estado="fallo", resultados=por_objeto,
                          publicacion="fallida")
        r = D.valida_resultado_adquisicion(caso, _seleccion(["OBJ"]),
                                            comprobar_remoto=False, raiz=raiz)
        afirma(r["valido"] and not r["cierre_exitoso"],
               f"resultado parcial válido debe conservarse sin fingir publicación: {r}")
        afirma(r["resultado_trabajo"] == "intentos_documentados"
               and r["publicacion_trabajo"] == "fallida",
               f"trabajo y publicación deben quedar separados: {r}")
    finally:
        td.cleanup()


def prueba_adquisicion_exige_archivo_manifiesto_pertinente():
    td, raiz = _raiz_fixture()
    try:
        payload = raiz / "data" / "raw" / "obj.zip"
        payload.write_bytes(b"PK fixture")
        (raiz / "data" / "manifiesto.yaml").write_text(
            "- id: obj_2026\n  usado_para: OBJ\n  archivo: obj.zip\n", encoding="utf-8")
        (raiz / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv").write_text(
            "fuente_canonica\testado_A4A5\tnota\nOBJ\tOBTENIDO\tregistrado\n", encoding="utf-8")
        por_objeto = [{"objeto_id": "OBJ", "desenlace": "adquirido",
                       "evidencias": ["data/manifiesto.yaml"], "intentos": [],
                       "archivos": ["data/raw/obj.zip"], "ids_manifiesto": ["obj_2026"]}]
        caso = _resultado(["OBJ"], estado="adquisicion_obtenida", resultados=por_objeto)
        r = D.valida_resultado_adquisicion(caso, _seleccion(["OBJ"]),
                                            comprobar_remoto=False, raiz=raiz)
        afirma(r["valido"] and r["cierre_exitoso"], f"adquisición acreditada fue rechazada: {r}")
        caso["resultados_por_objeto"][0]["ids_manifiesto"] = []
        r2 = D.valida_resultado_adquisicion(caso, _seleccion(["OBJ"]),
                                             comprobar_remoto=False, raiz=raiz)
        afirma(not r2["valido"], f"adquisición sin manifiesto fue aceptada: {r2}")
    finally:
        td.cleanup()


def prueba_cola_vacia_mecanica_valida():
    td, raiz = _raiz_fixture()
    try:
        (raiz / "data" / "manifiesto.yaml").write_text("[]\n", encoding="utf-8")
        (raiz / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv").write_text(
            "fuente_canonica\testado_A4A5\tnota\n", encoding="utf-8")
        caso = _resultado([], estado="cola_vacia", publicacion="no_aplica")
        r = D.valida_resultado_adquisicion(caso, _seleccion([]),
                                            comprobar_remoto=False, raiz=raiz)
        afirma(r["valido"] and r["cierre_exitoso"], f"cola vacía coherente fue rechazada: {r}")
    finally:
        td.cleanup()


def prueba_cola_descargas_vacia_con_investigacion_exige_evidencia():
    td, raiz = _raiz_fixture()
    try:
        evidencia = raiz / "forense" / "sonda.md"
        evidencia.write_text("consulta web y frontera verificables\n", encoding="utf-8")
        estado_dir = raiz / "data" / "curacion-registro" / "investigacion-estado"
        estado_dir.mkdir()
        (estado_dir / "NC-X.json").write_text(json.dumps({
            "version_pregunta": "v1", "evidencias": ["forense/sonda.md"]}), encoding="utf-8")
        (raiz / "data" / "manifiesto.yaml").write_text("[]\n", encoding="utf-8")
        (raiz / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv").write_text(
            "fuente_canonica\testado_A4A5\tnota\n", encoding="utf-8")
        sel_inv = {"corte": "2026-09-11", "maximo": 3,
                   "elegidos": [{"id": "NC-X", "version_pregunta": "v1"}],
                   "excluidos": []}
        caso = _resultado([], estado="descubrimiento_documentado", publicacion="publicada")
        caso["seleccion_investigacion"] = {
            "calculada": True, "corte": "2026-09-11", "maximo": 3,
            "elegidos": ["NC-X"], "excluidos_con_causa": []}
        caso["investigaciones"] = [{
            "necesidad_id": "NC-X", "version_pregunta": "v1",
            "estado": "sin_hallazgo_acotado", "modos_ejecutados": ["CONSTRUCTO"],
            "consultas": [{"mecanismo": "web_search", "consulta": "objeto X México",
                           "resultado": "sin candidato exacto"}],
            "candidatas": [], "evidencias": ["forense/sonda.md"],
            "frontera_no_examinada": "repositorios con acceso institucional",
            "cursor_continuacion": "reanudar ante nueva edición", "proxima_revision": "2026-10-11",
            "suficiencia": {"identidad": "NO_ACREDITADA", "conceptual": "NO_ACREDITADA",
                            "poblacional": "NO_ACREDITADA", "seleccion_no_respuesta": "NO_ACREDITADA",
                            "unidad": "NO_ACREDITADA", "temporalidad": "NO_ACREDITADA",
                            "diseno": "NO_ACREDITADA", "identificacion": "NO_APLICA",
                            "uso_habilitado": "INCOMPATIBLE", "pregunta_original": "ABIERTA"},
        }]
        r = D.valida_resultado_adquisicion(caso, _seleccion([]), sel_inv,
                                            comprobar_remoto=False, raiz=raiz)
        afirma(r["valido"] and r["resultado_trabajo"] == "descubrimiento_documentado",
               f"investigación real con cola de bytes vacía fue rechazada: {r}")
    finally:
        td.cleanup()


def prueba_wrapper_normaliza_selecciones_sin_redecidir_hallazgos():
    seleccion = _seleccion([])
    seleccion["excluidos"] = [{
        "id": "OBJ-X", "estado": "OBTENIDO",
        "razon": "A.8 ya resuelto"}]
    seleccion_inv = {
        "corte": "2026-09-11", "maximo": 3,
        "elegidos": [{"id": "NC-X", "version_pregunta": "v1"}],
        "excluidos": [{"id": "NC-Y", "razon": "reserva vigente"}],
    }
    caso = _resultado([], estado="descubrimiento_documentado",
                      publicacion="no_aplica")
    caso["resumen"] = "hallazgo que no debe cambiar"
    caso["seleccion"]["excluidos_con_causa"] = ["resumen del modelo"]
    caso["seleccion_investigacion"]["elegidos"] = []
    normalizado = D.normaliza_selecciones_resultado(
        caso, seleccion, seleccion_inv)
    afirma(normalizado["seleccion"]["excluidos_con_causa"] == [
        "OBJ-X [OBTENIDO] — A.8 ya resuelto"],
        f"no se insertó la exclusión autoritativa: {normalizado['seleccion']}")
    afirma(normalizado["seleccion_investigacion"]["elegidos"] == ["NC-X"]
           and normalizado["seleccion_investigacion"]["excluidos_con_causa"] == [
               "NC-Y — reserva vigente"],
           "no se insertó la selección de investigación autoritativa")
    afirma(normalizado["resumen"] == caso["resumen"],
           "normalizar selecciones alteró el hallazgo del ejecutor")


def prueba_vigilante_acredita_cola_vacia_sin_llm():
    linea = ("[ADQ] 2026-09-11 17:10: invocado=no motivo=COLA-VACIA exit=0 "
             "resultado=cola_vacia resultado_trabajo=cola_vacia "
             "publicacion_trabajo=no_aplica publicacion=OK "
             "disparador=puesta-en-marcha-programada run_id=RUN-VACIO\n")
    estado, detalle = C.t_cron_estado(__import__("datetime").date(2026, 9, 11),
                                      {"[ADQ]"}, linea)
    afirma(estado == "COMPLETO" and "invocado=no" in detalle,
           f"vigilante no acreditó el cierre mecánico publicado: {estado} {detalle}")
    fallo = linea.replace("publicacion=OK", "publicacion=FALLIDA(1)")
    estado2, _ = C.t_cron_estado(__import__("datetime").date(2026, 9, 11),
                                  {"[ADQ]"}, fallo)
    afirma(estado2 == "COLA-VACIA-PUBLICACION-FALLIDA",
           f"cola vacía sin publicación no debe acreditar: {estado2}")


def _launcher_fixture(raiz):
    (raiz / "tools").mkdir()
    shutil.copy2(RAIZ / "tools" / "adquiere_launcher.sh", raiz / "tools" / "adquiere_launcher.sh")
    bindir = raiz / "bin"
    bindir.mkdir()
    git = bindir / "git"
    git.write_text(
        "#!/usr/bin/env bash\n"
        "if [ \"$1\" = rev-parse ]; then printf '%040d\\n' 1; exit 0; fi\n"
        "if [ \"$1\" = fetch ]; then echo fetch roto >&2; exit 128; fi\n"
        "exit 0\n", encoding="utf-8")
    git.chmod(0o755)
    return bindir


def prueba_h3_fetch_128_deja_identidad_y_cierre():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        bindir = _launcher_fixture(raiz)
        env = dict(os.environ, PATH=f"{bindir}:{os.environ['PATH']}",
                   ADQ_DISPARADOR="fixture")
        r = subprocess.run(["bash", str(raiz / "tools" / "adquiere_launcher.sh")],
                           env=env, capture_output=True, text=True, timeout=20)
        hb = json.loads((raiz / "forense" / "adq-log" / "estado" / "heartbeat.json").read_text())
        afirma(r.returncode == 128, f"H3: fetch roto debe preservar exit 128, dio {r.returncode}")
        afirma(hb["estado"] == "FAILED" and hb["fase"] == "LAUNCHER-FETCH",
               f"H3: heartbeat debe localizar el fallo en launcher/fetch: {hb}")
        afirma(hb["run_id"] and hb["motivo"] == "git-fetch-origin-main"
               and hb["codigo_salida"] == 128,
               f"H3: faltan identidad/motivo/código original: {hb}")


def prueba_launcher_rechazado_no_pisa_heartbeat():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        bindir = _launcher_fixture(raiz)
        estado = raiz / "forense" / "adq-log" / "estado"
        estado.mkdir(parents=True)
        hb = estado / "heartbeat.json"
        hb.write_text('{"run_id":"DUEÑO","estado":"EN-CURSO"}\n', encoding="utf-8")
        with open(estado / "adquiere_cron.lock", "w") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            env = dict(os.environ, PATH=f"{bindir}:{os.environ['PATH']}")
            r = subprocess.run(["bash", str(raiz / "tools" / "adquiere_launcher.sh")],
                               env=env, capture_output=True, text=True, timeout=20)
        afirma(r.returncode == 3, f"launcher rechazado debe salir 3, dio {r.returncode}")
        afirma(json.loads(hb.read_text())["run_id"] == "DUEÑO",
               "launcher rechazado pisó el heartbeat del dueño")


def main():
    prueba_h2_rechaza_tres_falsos_positivos()
    prueba_resultado_parcial_y_publicacion_separada()
    prueba_adquisicion_exige_archivo_manifiesto_pertinente()
    prueba_cola_vacia_mecanica_valida()
    prueba_cola_descargas_vacia_con_investigacion_exige_evidencia()
    prueba_wrapper_normaliza_selecciones_sin_redecidir_hallazgos()
    prueba_vigilante_acredita_cola_vacia_sin_llm()
    prueba_h3_fetch_128_deja_identidad_y_cierre()
    prueba_launcher_rechazado_no_pisa_heartbeat()
    if FALLOS:
        print(f"FALLÓ ({len(FALLOS)}):")
        for fallo in FALLOS:
            print(f"  · {fallo}")
        return 1
    print("OK -- test_adq_cierre_verificable.py: 9 casos, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
