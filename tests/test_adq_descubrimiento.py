#!/usr/bin/env python3
"""Pruebas dirigidas del ciclo descubrimiento→adquisición GEN2-38."""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
sys.path.insert(0, str(RAIZ / "tools" / "curador_registro"))
import adq_autorizacion as A  # noqa: E402
import adq_doctor as D  # noqa: E402
import adq_investigacion as I  # noqa: E402
import adq_suficiencia as S  # noqa: E402
import tsv_crudo  # noqa: E402
import vista_cola_adquisicion as V  # noqa: E402

FALLOS: list[str] = []


def afirma(condicion, mensaje):
    if not condicion:
        FALLOS.append(mensaje)


def prueba_autorizacion_json_gana_a_historia_y_detecta_errores():
    meta = {"autoridad": "AUTORIZADA-POR-ALCANCE:Jonas/2026-09-12/GEN2-38/OBJ"}
    nota = "RESIDUAL-ADQ-V1=" + json.dumps(meta, separators=(",", ":"))
    nota += " || SONDA-LATERAL-RECOMENDADA; sin autorización individual histórica"
    afirma(A.esta_autorizada(nota, "OBJ", dt.date(2026, 9, 12)),
           "la metadata vigente debe ganar a la recomendación histórica")
    for autoridad in (
        "AUTORIZADA-POR-ALCANCE:Jonas/2026-13-40/GEN2-38/OBJ",
        "AUTORIZADA-POR-ALCANCE:Jonas/2026-09-12/GEN2-38/OTRO",
        "NO-AUTORIZADA",
    ):
        n = "RESIDUAL-ADQ-V1=" + json.dumps({"autoridad": autoridad})
        afirma(not A.esta_autorizada(n, "OBJ", dt.date(2026, 9, 12)),
               f"autoridad inválida fue aceptada: {autoridad}")


def prueba_intento_explicito_sin_fecha_no_es_ausencia():
    valor = D.fecha_intento_efectivo("intento efectivo pendiente de conciliar")
    afirma(valor is D.FECHA_INDETERMINADA,
           f"intento explícito sin fecha debe ir a conciliación, dio {valor!r}")


def _fixture_investigacion(raiz: Path) -> dict:
    (raiz / "forense").mkdir(parents=True)
    (raiz / "forense" / "no-corrido.tsv").write_text(
        "id\tque_no_se_corrio\timpacto\testado\n"
        "NC-A\tpregunta A\timpacto A\tABIERTA\n"
        "NC-B\tpregunta B\timpacto B\tABIERTA\n"
        "NC-C\tpregunta C\timpacto C\tCERRADA\n", encoding="utf-8")
    cfg = {
        "version": "GEN2-ADQ-INVESTIGACION-V1",
        "fuente_necesidades": "forense/no-corrido.tsv",
        "estado_dir": "estado", "reservas_runtime_dir": "reservas",
        "reserva_minutos": 75,
        "necesidades": [
            {"id": "NC-A", "version_pregunta": "v1", "lista": True,
             "prioridad_consumidor": 2, "bloqueo_material": 3,
             "proxima_revision": "2026-09-11", "asignacion": "servicio-gen2-38"},
            {"id": "NC-B", "version_pregunta": "v1", "lista": True,
             "prioridad_consumidor": 1, "bloqueo_material": 1,
             "proxima_revision": "2026-10-01", "asignacion": "servicio-gen2-38"},
            {"id": "NC-C", "version_pregunta": "v1", "lista": True,
             "prioridad_consumidor": 0, "bloqueo_material": 3,
             "proxima_revision": "2026-09-11", "asignacion": "servicio-gen2-38"},
        ],
    }
    return cfg


def prueba_seleccion_reanudacion_reserva_y_version():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        cfg = _fixture_investigacion(raiz)
        r = I.selecciona(cfg, dt.date(2026, 9, 12), maximo=3, raiz=raiz,
                         ahora=dt.datetime(2026, 9, 12, tzinfo=dt.timezone.utc))
        afirma([x["id"] for x in r["elegidos"]] == ["NC-A"],
               f"debe elegir sólo necesidad abierta y vencida: {r}")
        I.reserva_seleccion(r, "RUN-1", cfg, raiz,
                            dt.datetime(2026, 9, 12, tzinfo=dt.timezone.utc))
        r2 = I.selecciona(cfg, dt.date(2026, 9, 12), 3, raiz=raiz,
                          ahora=dt.datetime(2026, 9, 12, 0, 1, tzinfo=dt.timezone.utc))
        afirma(not r2["elegidos"] and any("RUN-1" in x["razon"] for x in r2["excluidos"]),
               f"reserva vigente no evitó dueño duplicado: {r2}")
        I.libera("RUN-1", cfg, raiz)
        afirma(not list((raiz / "reservas").glob("*.json")), "la reserva no se liberó")


CAMPOS = ["fila_origen", "fuente_canonica", "fuente_canonica_normalizada",
          "discordancia_alias", "estado_A4A5", "prioridad", "url_conocida",
          "ids_manifiesto", "origen", "nota"]


def prueba_altas_concurrentes_no_pierden_fila_y_vista_converge():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        registro, vista = raiz / "registro.tsv", raiz / "vista.tsv"
        registro.write_text("\t".join(CAMPOS) + "\n", encoding="utf-8")
        programa = r'''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import tsv_crudo
sys.path.insert(0, sys.argv[2])
import vista_cola_adquisicion as V
campos = sys.argv[5].split(",")
ident = sys.argv[3]
fila = {c: "" for c in campos}
fila.update({"fila_origen": "residual:" + ident, "fuente_canonica": ident,
             "fuente_canonica_normalizada": ident, "estado_A4A5": "PENDIENTE",
             "prioridad": "1", "origen": "fixture"})
tsv_crudo.upsert_fila(Path(sys.argv[4]), fila, campos, clave="fuente_canonica")
V.regenera(Path(sys.argv[4]), Path(sys.argv[6]))
'''
        procesos = [subprocess.Popen(
            [sys.executable, "-c", programa,
             str(RAIZ / "tools" / "curador_registro"), str(RAIZ / "tools"),
             ident, str(registro), ",".join(CAMPOS), str(vista)])
            for ident in ("OBJ-A", "OBJ-B")]
        for p in procesos:
            afirma(p.wait(timeout=10) == 0, "proceso concurrente falló")
        filas = {x["fuente_canonica"] for x in tsv_crudo.leer_dicts(registro)}
        afirma(filas == {"OBJ-A", "OBJ-B"}, f"alta concurrente perdió una fila: {filas}")
        afirma(vista.read_text(encoding="utf-8") == V.build(registro),
               "la vista final no converge al registro después de concurrencia")


def prueba_cableado_y_calendario_de_produccion():
    runner = (RAIZ / "tools" / "adquiere_cron.sh").read_text(encoding="utf-8")
    cfg = yaml.safe_load((RAIZ / "data" / "adq-config.yaml").read_text(encoding="utf-8"))
    afirma("NUM_INVESTIGACIONES" in runner and "standalone_web_search" in runner,
           "runner no conecta selección de investigación con búsqueda web real")
    tramo_prompt = runner.split('PROMPT_EFECTIVO="', 1)[1].split(
        '"\n\n# set +e/-e:', 1)[0]
    afirma("\\`python3 tools/adq_investigacion.py" in tramo_prompt,
           "el prompt dinámico ejecutaría accidentalmente el comando entre backticks")
    afirma(len(cfg["calendario"]["dias_semana"]) == 7,
           "cadencia final debe ser diaria")
    afirma(cfg["descubrimiento_maximo_necesidades"] == 3 and cfg["maximo_filas"] == 5,
           "límites autorizados 3/5 no están configurados")
    proxy = S.proyecta("NC-0122")
    incompatible = S.proyecta("NC-0126")
    afirma(proxy["accion_consumidor"] == "SOLO_EMITIR_ALCANCE_MENOR_ROTULADO",
           "ENIF no debe cerrar el canal del producto fintech exacto")
    afirma(incompatible["accion_consumidor"] == "NO_EMITIR_RESULTADO_SOLICITADO",
           "la categoría colapsada no debe emitir el horizonte solicitado")


def main() -> int:
    prueba_autorizacion_json_gana_a_historia_y_detecta_errores()
    prueba_intento_explicito_sin_fecha_no_es_ausencia()
    prueba_seleccion_reanudacion_reserva_y_version()
    prueba_altas_concurrentes_no_pierden_fila_y_vista_converge()
    prueba_cableado_y_calendario_de_produccion()
    if FALLOS:
        print(f"FALLÓ ({len(FALLOS)}):")
        for fallo in FALLOS:
            print("  ·", fallo)
        return 1
    print("OK -- test_adq_descubrimiento.py: 5 grupos, 0 fallos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
