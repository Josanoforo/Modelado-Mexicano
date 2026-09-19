#!/usr/bin/env python3
"""Regresiones del handoff redundante y la salud mecánica ADQ."""
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
sys.path.insert(0, str(RAIZ / "tests"))
import adq_doctor as D  # noqa: E402
import adq_handoff as H  # noqa: E402
import check as C  # noqa: E402

FALLOS = []


def afirma(condicion, mensaje):
    if not condicion:
        FALLOS.append(mensaje)


def _raiz_fixture():
    td = tempfile.TemporaryDirectory()
    raiz = Path(td.name)
    (raiz / "tools").mkdir()
    shutil.copy2(RAIZ / "tools" / "adq-resultado.schema.json",
                 raiz / "tools" / "adq-resultado.schema.json")
    (raiz / "data" / "curacion-registro" / "investigacion-estado").mkdir(
        parents=True)
    (raiz / "data" / "raw").mkdir()
    (raiz / "data" / "manifiesto.yaml").write_text("[]\n", encoding="utf-8")
    (raiz / "data" / "curacion-registro" /
     "cola-adquisicion-registro.tsv").write_text(
        "fuente_canonica\testado_A4A5\tnota\n", encoding="utf-8")
    (raiz / "forense").mkdir()
    return td, raiz


def _seleccion():
    return {"corte": "2026-09-17", "maximo": 5,
            "elegidos": [], "excluidos": []}


def _seleccion_inv(ids=()):
    return {"corte": "2026-09-17", "maximo": 3,
            "elegidos": [{"id": x, "version_pregunta": "v1"} for x in ids],
            "excluidos": []}


def _suficiencia(uso="INCOMPATIBLE", conceptual="NO_ACREDITADA"):
    return {
        "identidad": "NO_ACREDITADA", "conceptual": conceptual,
        "poblacional": "NO_ACREDITADA",
        "seleccion_no_respuesta": "NO_ACREDITADA",
        "unidad": "NO_ACREDITADA", "temporalidad": "NO_ACREDITADA",
        "diseno": "NO_ACREDITADA", "identificacion": "NO_APLICA",
        "uso_habilitado": uso, "pregunta_original": "ABIERTA",
    }


def _investigacion(ident, evidencia, *, candidata_nueva=False,
                   uso="INCOMPATIBLE", conceptual="NO_ACREDITADA"):
    candidatas = ([{
        "id": f"C-{ident}", "url": "https://example.org/candidato",
        "objeto": "objeto candidato", "verificacion_contenido": "revisado",
        "nuevo_respecto_corpus": True, "cobertura": "parcial",
        "acceso": "público", "siguiente_accion": "revisar",
    }] if candidata_nueva else [])
    return {
        "necesidad_id": ident, "version_pregunta": "v1",
        "estado": "continua", "modos_ejecutados": ["CONSTRUCTO"],
        "consultas": [{"mecanismo": "buscador", "consulta": f"consulta {ident}",
                       "resultado": "resultado verificable"}],
        "candidatas": candidatas, "evidencias": [evidencia],
        "frontera_no_examinada": "ruta siguiente",
        "cursor_continuacion": "página 2", "proxima_revision": "2026-09-18",
        "suficiencia": _suficiencia(uso, conceptual),
    }


def _resultado(ids=(), evidencia="forense/evidencia.md", resumen="fixture"):
    return {
        "ejecutor": "codex",
        "seleccion": {"calculada": True, "corte": "modelo", "maximo": 0,
                      "elegidos": [], "excluidos_con_causa": []},
        "seleccion_investigacion": {
            "calculada": True, "corte": "modelo", "maximo": 0,
            "elegidos": [], "excluidos_con_causa": []},
        "investigaciones": [_investigacion(x, evidencia) for x in ids],
        "resultado_sustantivo": ("descubrimiento_documentado" if ids
                                  else "cola_vacia"),
        "resultados_por_objeto": [],
        "publicacion_trabajo": ({
            "estado": "publicada", "referencias": [{
                "ref": "refs/heads/adq/fixture", "commit": "a" * 40}]}
            if ids else {"estado": "no_aplica", "referencias": []}),
        "resumen": resumen,
    }


def _prepara_investigaciones(raiz, ids):
    evidencia = raiz / "forense" / "evidencia.md"
    evidencia.write_text("evidencia\n", encoding="utf-8")
    for ident in ids:
        (raiz / "data" / "curacion-registro" / "investigacion-estado" /
         f"{ident}.json").write_text(json.dumps({
             "version_pregunta": "v1", "evidencias": ["forense/evidencia.md"],
             "suficiencia": _suficiencia(),
         }), encoding="utf-8")


def _escribe(ruta, dato):
    ruta.write_text(json.dumps(dato), encoding="utf-8")


def prueba_1_last_message_valido_handoff_ausente():
    td, raiz = _raiz_fixture()
    try:
        last, handoff = raiz / "last.json", raiz / "handoff.json"
        _escribe(last, _resultado())
        informe, aceptado = H.selecciona_resultado(
            [("last-message", last), ("handoff", handoff)], _seleccion(),
            _seleccion_inv(), raiz=raiz, comprobar_remoto=False)
        afirma(informe["resultado_origen"] == "last-message" and aceptado,
               f"last-message único válido no cerró normal: {informe}")
    finally:
        td.cleanup()


def prueba_2_handoff_valido_last_null_tres_investigaciones_cero_bytes():
    td, raiz = _raiz_fixture()
    try:
        ids = ("N1", "N2", "N3")
        _prepara_investigaciones(raiz, ids)
        last, handoff = raiz / "last.json", raiz / "handoff.json"
        _escribe(last, None)
        _escribe(handoff, _resultado(ids))
        informe, aceptado = H.selecciona_resultado(
            [("last-message", last), ("handoff", handoff)], _seleccion(),
            _seleccion_inv(ids), raiz=raiz, comprobar_remoto=False)
        metricas = H.metricas_resultado(
            aceptado, H.captura_estado_antes(_seleccion_inv(ids), raiz), raiz)
        afirma(informe["resultado_origen"] == "handoff" and
               len(aceptado["investigaciones"]) == 3 and
               metricas["objetos_adquiridos"] == metricas["bytes_nuevos"] == 0,
               f"handoff con 3 investigaciones/0 bytes no se recuperó: {informe}")
    finally:
        td.cleanup()


def prueba_3_ambos_validos_iguales_sin_doble_conteo():
    td, raiz = _raiz_fixture()
    try:
        last, handoff = raiz / "last.json", raiz / "handoff.json"
        dato = _resultado()
        _escribe(last, dato); _escribe(handoff, dato)
        informe, aceptado = H.selecciona_resultado(
            [("last-message", last), ("handoff", handoff)], _seleccion(),
            _seleccion_inv(), raiz=raiz, comprobar_remoto=False)
        afirma(informe["causa"] == "candidatos_validos_iguales" and
               aceptado["resultados_por_objeto"] == [],
               f"dos copias iguales no cerraron una vez: {informe}")
    finally:
        td.cleanup()


def prueba_4_ambos_validos_distintos_conflicto():
    td, raiz = _raiz_fixture()
    try:
        last, handoff = raiz / "last.json", raiz / "handoff.json"
        _escribe(last, _resultado(resumen="A"))
        _escribe(handoff, _resultado(resumen="B"))
        informe, aceptado = H.selecciona_resultado(
            [("last-message", last), ("handoff", handoff)], _seleccion(),
            _seleccion_inv(), raiz=raiz, comprobar_remoto=False)
        afirma(informe["resultado_origen"] == "conflicto" and
               informe["codigo"] == 67 and aceptado is None,
               f"candidatos divergentes no fallaron cerrado: {informe}")
    finally:
        td.cleanup()


def prueba_5_ausentes_o_invalidos_exit_65():
    td, raiz = _raiz_fixture()
    try:
        last, handoff = raiz / "last.json", raiz / "handoff.json"
        last.write_text("null\n", encoding="utf-8")
        handoff.write_text("{roto", encoding="utf-8")
        informe, aceptado = H.selecciona_resultado(
            [("last-message", last), ("handoff", handoff)], _seleccion(),
            _seleccion_inv(), raiz=raiz, comprobar_remoto=False)
        afirma(informe["resultado_origen"] == "ninguno" and
               informe["codigo"] == 65 and aceptado is None,
               f"ausencia de JSON válido no preservó exit 65: {informe}")
    finally:
        td.cleanup()


def prueba_6_rama_o_nota_no_reconstruyen_json():
    td, raiz = _raiz_fixture()
    try:
        (raiz / "forense" / "nota.md").write_text("tres investigaciones\n")
        (raiz / ".git-ref-simulada").write_text("refs/heads/adq/fixture\n")
        informe, aceptado = H.selecciona_resultado(
            [("last-message", raiz / "ausente-1"),
             ("handoff", raiz / "ausente-2")], _seleccion(),
            _seleccion_inv(), raiz=raiz, comprobar_remoto=False)
        afirma(informe["codigo"] == 65 and aceptado is None,
               "nota/rama sustituyó indebidamente el JSON ausente")
    finally:
        td.cleanup()


def prueba_7_publicacion_ref_sha_incorrectos_falla():
    td, raiz = _raiz_fixture()
    try:
        ids = ("N1",); _prepara_investigaciones(raiz, ids)
        last, handoff = raiz / "last.json", raiz / "handoff.json"
        _escribe(last, _resultado(ids))
        with mock.patch.object(D, "_corre", return_value=(
                0, f"{'b' * 40}\trefs/heads/adq/fixture\n", "")):
            informe, aceptado = H.selecciona_resultado(
                [("last-message", last), ("handoff", handoff)], _seleccion(),
                _seleccion_inv(ids), raiz=raiz, comprobar_remoto=True)
        afirma(informe["codigo"] == 65 and aceptado is None,
               f"SHA remoto incorrecto acreditó publicación: {informe}")
    finally:
        td.cleanup()


def prueba_8_evidencia_nueva_cero_descargas_no_es_sin_evidencia():
    td, raiz = _raiz_fixture()
    try:
        _prepara_investigaciones(raiz, ("N1",))
        antes = H.captura_estado_antes(_seleccion_inv(("N1",)), raiz)
        nuevo = raiz / "forense" / "nueva.md"
        nuevo.write_text("hallazgo nuevo\n", encoding="utf-8")
        resultado = _resultado(("N1",), evidencia="forense/nueva.md")
        resultado["investigaciones"][0]["candidatas"] = [{
            "id": "C-N1", "url": "https://example.org/c",
            "objeto": "candidata", "verificacion_contenido": "verificada",
            "nuevo_respecto_corpus": True, "cobertura": "parcial",
            "acceso": "público", "siguiente_accion": "continuar"}]
        m = H.metricas_resultado(resultado, antes, raiz)
        afirma(m["salud_trabajo"] == "EVIDENCIA_NUEVA_SIN_REDUCCION" and
               m["objetos_adquiridos"] == m["bytes_nuevos"] == 0,
               f"evidencia nueva sin descarga se perdió: {m}")
    finally:
        td.cleanup()


def prueba_9_fecha_cursor_no_reducen_brecha():
    td, raiz = _raiz_fixture()
    try:
        _prepara_investigaciones(raiz, ("N1",))
        antes = H.captura_estado_antes(_seleccion_inv(("N1",)), raiz)
        resultado = _resultado(("N1",))
        resultado["investigaciones"][0]["cursor_continuacion"] = "página 99"
        resultado["investigaciones"][0]["proxima_revision"] = "2027-01-01"
        m = H.metricas_resultado(resultado, antes, raiz)
        afirma(m["investigaciones_reduccion_brecha"] == 0 and
               m["salud_trabajo"] == "EJECUCION_SIN_EVIDENCIA_NUEVA",
               f"fecha/cursor se presentaron como reducción: {m}")
    finally:
        td.cleanup()


def prueba_10_data_raw_montado_es_evidencia_local_valida():
    td, raiz = _raiz_fixture()
    try:
        corpus = raiz / "corpus"; corpus.mkdir()
        (corpus / "existente.pdf").write_bytes(b"PDF")
        (raiz / "data" / "raw").rmdir()
        (raiz / "data" / "raw").symlink_to(corpus, target_is_directory=True)
        real, permitido = D._ruta_evidencia_local(
            "data/raw/existente.pdf", str(raiz))
        afirma(permitido and os.path.exists(real),
               "data/raw montado fue rechazado pese a existir en el corpus")
    finally:
        td.cleanup()


def prueba_11_vigilante_distingue_evidencia_sin_bytes():
    import datetime
    linea = (
        "[ADQ] 2026-09-17 09:30: invocado=si motivo=- exit=0 "
        "resultado=descubrimiento_documentado resultado_origen=handoff "
        "resultado_causa=handoff_unico_valido "
        "salud_trabajo=EVIDENCIA_NUEVA_SIN_REDUCCION "
        "investigaciones_evidencia_nueva=1 "
        "investigaciones_reduccion_brecha=0 objetos_nuevos=0 bytes_nuevos=0 "
        "publicacion=OK run_id=RUN-EVIDENCIA\n")
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 17), {"[ADQ]"}, linea)
    afirma(estado == "EVIDENCIA-NUEVA-SIN-REDUCCION" and
           "bytes_nuevos=0" in detalle,
           f"vigilante confundió cero bytes con cero evidencia: {estado} {detalle}")


def prueba_12_runner_conserva_canales_y_publica_origen():
    fuente = (RAIZ / "tools" / "adquiere_cron.sh").read_text(encoding="utf-8")
    afirma("--output-schema" in fuente and "--output-last-message" in fuente,
           "el handoff reemplazó un canal primario de Codex")
    afirma("HANDOFF REDUNDANTE OBLIGATORIO" in fuente and
           "os.replace" in fuente and "--selecciona-resultado" in fuente,
           "la ruta redundante no llega literal/atómica al prompt y selector")
    afirma("preentrega-validacion.json" in fuente and
           "intentos[].resultado debe aparecer VERBATIM" in fuente and
           "investigaciones sin adquiridos=descubrimiento_documentado" in fuente,
           "el productor no recibe prevalidación, evidencia literal y clasificación mecánica")
    afirma("resultado_origen=${RESULTADO_ORIGEN}" in fuente and
           "resultado_causa=${RESULTADO_CAUSA}" in fuente,
           "la huella no publica origen y causa breve")


def prueba_13_vigilante_nombra_resultado_invalido():
    import datetime
    linea = (
        "[ADQ] 2026-09-17 09:31: invocado=si motivo=- exit=65 "
        "resultado=resultado_invalido resultado_origen=ninguno "
        "resultado_causa=sin_candidato_valido salud_trabajo=RESULTADO_INVALIDO "
        "publicacion=OK run_id=RUN-INVALIDO\n")
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 17), {"[ADQ]"}, linea)
    afirma(estado == "RESULTADO-INVALIDO" and
           "sin_candidato_valido" in detalle,
           f"vigilante ocultó causa del resultado inválido: {estado} {detalle}")


def main():
    pruebas = [v for k, v in sorted(globals().items())
               if k.startswith("prueba_")]
    for prueba in pruebas:
        try:
            prueba()
        except Exception as e:
            FALLOS.append(f"{prueba.__name__}: {type(e).__name__}: {e}")
    for fallo in FALLOS:
        print("FAIL", fallo)
    print(f"\n{len(pruebas)} pruebas, {len(FALLOS)} fallos")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    raise SystemExit(main())
