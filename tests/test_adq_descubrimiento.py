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


def prueba_necesidad_nueva_llega_a_sonda_sin_lista_manual():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        (raiz / "forense").mkdir(parents=True)
        (raiz / "forense" / "no-corrido.tsv").write_text(
            "id\tacto\tpieza\tque_no_se_corrio\trazon\timpacto\tsucesor\testado\n"
            "NC-NUEVA\tACTO-X\tP1\tbuscar fuente pública con variable X\t"
            "EVIDENCIA-INSUFICIENTE\tarchivo obtenido no cubre X\t"
            "localizar microdato público con X\tABIERTA\n"
            "NC-DIF\tACTO-X\tP2\tbuscar fuente Y\tDIFERIDO-A:OTRO\t"
            "espera explícita\tOTRO\tABIERTA\n",
            encoding="utf-8")
        cfg = {
            "version": "GEN2-ADQ-INVESTIGACION-V1",
            "fuente_necesidades": "forense/no-corrido.tsv",
            "estado_dir": "estado", "reservas_runtime_dir": "reservas",
            "reserva_minutos": 75, "necesidades": [],
        }
        seleccion = I.selecciona(
            cfg, dt.date(2026, 9, 12), 3, raiz=raiz,
            ahora=dt.datetime(2026, 9, 12, tzinfo=dt.timezone.utc))
        afirma([x["id"] for x in seleccion["elegidos"]] == ["NC-NUEVA"],
               f"una brecha nueva verificable debe llegar automáticamente: {seleccion}")
        elegida = seleccion["elegidos"][0]
        afirma(elegida["contrato_operativo"] == "DESCRIPCION_MINIMA_DERIVADA",
               "la necesidad nueva debe recibir contrato mínimo reproducible")
        afirma(bool(elegida["responsable"] and elegida["siguiente_accion"]),
               "el contrato derivado debe tener responsable y siguiente acción")
        afirma(any(x["id"] == "NC-DIF" for x in seleccion["excluidos"]),
               "un diferido explícito no debe reactivarse automáticamente")


def prueba_demanda_explica_todo_elemento_gen2_vigente():
    cfg = I.cargar_config()
    demanda = I.proyecta_demanda(cfg, dt.date(2026, 9, 11))
    elementos = demanda["elementos_gen2"]
    usos = [x for x in I._tsv(RAIZ / cfg["fuente_usos"])
            if x.get("activo") == "SI"]
    abiertas = {i for i, x in I.necesidades_canonicas(cfg).items()
                if x.get("estado") == "ABIERTA"}
    afirma(len(elementos) == len(usos),
           "la proyección debe conservar exactamente el alcance activo de usos.tsv")
    afirma(demanda["total_activas"] == len(abiertas),
           "la proyección debe conservar exactamente las NC abiertas canónicas")
    afirma(demanda["contrato_cientifico_completo"] +
           demanda["contrato_cientifico_incompleto"] <= demanda["total_activas"],
           "los contratos operativos no deben contarse como científicos")
    afirma(all(x["situacion"] and x["siguiente_accion"] for x in elementos),
           "cada elemento vigente requiere situación y siguiente acción")
    afirma(all(x["contrato_id"] and x["identidad_contrato"] and
               x["ejecutor_siguiente"] for x in elementos),
           "toda obligación debe conservar contrato, identidad y ejecutor")
    afirma(all("GEN1_ES_SOLO_ANTECEDENTE" in x["adopcion"] for x in elementos
               if not x["resultado_id"]),
           "GEN1 no debe reactivarse por entrar al inventario")
    consumidores_horizonte = {
        vinculo["consumidor"] for necesidad in cfg["necesidades"]
        if necesidad["id"] == "NC-0126"
        for vinculo in necesidad["vinculos_consulta"]}
    horizonte = [x for x in elementos
                 if x["consumidor"] in consumidores_horizonte]
    afirma(len(horizonte) == len(consumidores_horizonte) and
           all(x["situacion"] == "PENDIENTE_DATOS_O_DECISION_DE_USO" and
               not x["uso_disponible_hoy"] for x in horizonte),
           "las tres salidas de horizonte deben conservar NO_COVERAGE")
    afirma("cero tareas elegibles" in demanda["advertencia_suficiencia"],
           "la proyección debe negar suficiencia general por cola vacía")
    afirma(not demanda["seleccion_siguiente"]["elegidos"] and
           {x["id"] for x in demanda["seleccion_siguiente"]["excluidos"]} == abiertas,
           "el mapa debe publicar la selección siguiente y todas sus causas")
    por_id = {x["elemento_id"]: x for x in elementos}
    complemento = por_id["RES-0028"]
    afirma(complemento["situacion"] == "PENDIENTE_ADOPCION" and
           complemento["necesidades_nc_abiertas"] == ["NC-0085"] and
           complemento["ofertas_conciliadas"][0]["resultado_id"] ==
           "RESULT-ENVIPE-DEN-P-C2-U4",
           "RES-0028 debe enlazar el complemento U4 exacto sin fingir adopción")
    seguro = por_id["RES-0039"]
    afirma(seguro["situacion"] == "PENDIENTE_DECISION_CIENTIFICA" and
           seguro["ofertas_conciliadas"][0].get("resultado_id") is None,
           "RES-0039..42 deben exponer propuesta no ejecutada, no un cálculo")
    for ident in ("RES-0063", "RES-0064"):
        afirma(por_id[ident]["medicion_disponible_hoy"] and
               not por_id[ident]["uso_disponible_hoy"] and
               por_id[ident]["primer_faltante"] == "REGISTRO_CORRIDA0",
               f"{ident} está medido/adoptado, pero GEN2 aún requiere registro")
    r_civ = por_id["RES-0095"]
    afirma(r_civ["situacion"] == "EVALUACION_GEN2_DISPONIBLE" and
           r_civ["ofertas_conciliadas"][0]["resultado_id"] ==
           "RESULT-R-CIV-M-01-PUNTO" and r_civ["advertencias"],
           "R debe consumirse como árbitro de evaluación, nunca como M")
    r_din = por_id["RES-0125"]
    afirma("FP-371" in r_din["incertidumbre_pendiente"] and
           r_din["uso_disponible_hoy"],
           "DIN debe conservar el punto y separar la incertidumbre FP-371")
    tecnicas = [x for x in demanda["necesidades"]
                if x["naturaleza_necesidad"].startswith("OPERATIVA_")]
    afirma(tecnicas and all(not x["aplica_contrato_cientifico"] for x in tecnicas),
           "las necesidades técnicas/acceso no deben fabricar contrato científico")


def prueba_conciliacion_exige_identidad_y_compatibilidad_documentada():
    with tempfile.TemporaryDirectory() as td:
        ruta = Path(td) / "cfg.yaml"
        ruta.write_text(yaml.safe_dump({
            "version": "GEN2-ADQ-INVESTIGACION-V1",
            "conciliacion_elementos": [{
                "elementos": ["RES-X"],
                "ofertas": [{"oferta_id": "O-SIN-CAMPOS"}],
            }],
        }), encoding="utf-8")
        try:
            I.cargar_config(ruta)
        except ValueError:
            paso = True
        else:
            paso = False
        afirma(paso, "una oferta sin población/unidad/propósito debe rechazarse")


def prueba_reanudacion_estructurada_y_barrera_humana():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        (raiz / "forense").mkdir(parents=True)
        (raiz / "forense" / "no-corrido.tsv").write_text(
            "id\tque_no_se_corrio\timpacto\testado\n"
            "NC-W\tbuscar fuente X\tfalta X\tABIERTA\n"
            "NC-H\tbuscar fuente Y\tfalta Y\tABIERTA\n", encoding="utf-8")
        base = {"version": "GEN2-ADQ-INVESTIGACION-V1",
                "fuente_necesidades": "forense/no-corrido.tsv",
                "estado_dir": "estado", "reservas_runtime_dir": "reservas",
                "reserva_minutos": 75, "necesidades": [
                    {"id": "NC-W", "version_pregunta": "v1", "lista": True,
                     "estado_ruteo": "ESPERA_NUEVA_PISTA",
                     "proxima_revision": "2026-10-11", "prioridad_consumidor": 1,
                     "bloqueo_material": 1, "asignacion": "servicio-gen2-38"},
                    {"id": "NC-H", "version_pregunta": "v1", "lista": True,
                     "estado_ruteo": "ESPERA_ACCESO_HUMANO",
                     "proxima_revision": "2026-09-01", "prioridad_consumidor": 0,
                     "bloqueo_material": 2, "asignacion": "servicio-gen2-38"},
                ]}
        antes = I.selecciona(base, dt.date(2026, 10, 10), 3, raiz=raiz)
        afirma(not antes["elegidos"], "la espera no vencida no debe reanudarse")
        vencida = I.selecciona(base, dt.date(2026, 10, 11), 3, raiz=raiz)
        afirma([x["id"] for x in vencida["elegidos"]] == ["NC-W"],
               f"la fecha vencida debe reanudar NC-W sin liberar NC-H: {vencida}")
        forzada = I.selecciona(
            base, dt.date(2026, 10, 11), 3, nombradas={"NC-H"}, raiz=raiz)
        afirma(all(x["id"] != "NC-H" for x in forzada["elegidos"]),
               "ni la selección nominal debe atravesar una barrera humana")
        (raiz / "estado").mkdir()
        (raiz / "estado" / "NC-W.json").write_text(json.dumps({
            "necesidad_id": "NC-W", "version_pregunta": "v1",
            "proxima_revision": "2026-10-11",
            "evidencia_nueva_identificada": {
                "identificada": True, "necesidad_id": "NC-W",
                "version_pregunta": "v1", "evidencias": ["FUENTE-NUEVA"]},
        }), encoding="utf-8")
        nueva = I.selecciona(base, dt.date(2026, 9, 12), 3, raiz=raiz)
        afirma([x["id"] for x in nueva["elegidos"]] == ["NC-W"],
               "evidencia nueva exacta debe reanudar antes de la fecha")


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
    esquema = json.loads(
        (RAIZ / "tools" / "adq-resultado.schema.json").read_text(encoding="utf-8"))
    pendientes = [("$", esquema)]
    while pendientes:
        ruta, nodo = pendientes.pop()
        if isinstance(nodo, dict):
            if "enum" in nodo or "const" in nodo:
                afirma("type" in nodo,
                       f"Structured Outputs exige type junto a enum/const: {ruta}")
            pendientes.extend((f"{ruta}.{k}", v) for k, v in nodo.items())
        elif isinstance(nodo, list):
            pendientes.extend((f"{ruta}[{i}]", v) for i, v in enumerate(nodo))


def main() -> int:
    prueba_autorizacion_json_gana_a_historia_y_detecta_errores()
    prueba_intento_explicito_sin_fecha_no_es_ausencia()
    prueba_seleccion_reanudacion_reserva_y_version()
    prueba_necesidad_nueva_llega_a_sonda_sin_lista_manual()
    prueba_demanda_explica_todo_elemento_gen2_vigente()
    prueba_conciliacion_exige_identidad_y_compatibilidad_documentada()
    prueba_reanudacion_estructurada_y_barrera_humana()
    prueba_altas_concurrentes_no_pierden_fila_y_vista_converge()
    prueba_cableado_y_calendario_de_produccion()
    if FALLOS:
        print(f"FALLÓ ({len(FALLOS)}):")
        for fallo in FALLOS:
            print("  ·", fallo)
        return 1
    print("OK -- test_adq_descubrimiento.py: 9 grupos, 0 fallos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
