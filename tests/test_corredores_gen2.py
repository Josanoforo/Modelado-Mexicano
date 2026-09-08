#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/test_corredores_gen2.py` -- un test por wrapper GEN2 del marcador,
sobre FIXTURES, mas los casos del Go/No-Go.

ACTO GEN2-E7 · READINESS-2 · Pieza A (tests) + Pieza B.

Estos tests no abren microdato, no llaman a ningun modelo, no tocan la red y
no escriben fuera de un directorio temporal. Mismo arnes que
`tests/test_corrida0.py`: `corre()` devuelve la lista de fallos y
`tests/check.py` la consume.

Los fixtures son marcos y specs REDUCIDOS construidos en el test (dos o tres
celdas), no copias del arbol: un test que corre sobre el arbol completo mide
el arbol, no el wrapper. Las dos excepciones declaradas son (a) el marco
vigente real, que es lo que `MARCO-VIGENTE-UNICO` tiene que leer para decir
algo, y (b) `L-spec-v1_2.json`, cuyo conteo de 14 celdas es exactamente el
invariante que `L-SPEC-v1_2` afirma.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

CALC_M = RAIZ / "data/corrida0/CALC-M-marco-M-sorteado-v1_3"
CALC_AGG = RAIZ / "data/corrida0/CALC-AGG-marco-M-sorteado-v1_3"
MARCO_REL = "forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv"

FALLOS: list[str] = []


def _falla(caso: str, msg: str) -> None:
    FALLOS.append(f"{caso}: {msg}")


def _carga(ruta: Path, nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def _entrada(iid: str, crudo: bytes, **extra) -> dict:
    return {"id": iid, "origen": "repo", "bytes": crudo,
            "sha256": hashlib.sha256(crudo).hexdigest(),
            "estado": "COINCIDE", **extra}


def _entrada_de(iid: str, rel: str) -> dict:
    return _entrada(iid, (RAIZ / rel).read_bytes(), ruta=rel)


def _marco_fixture(ids: list[str]) -> bytes:
    """Sub-marco con SOLO las celdas pedidas, mismas columnas que el vigente.
    Se recorta el real en vez de teclear filas: teclear una fila a mano seria
    inventar valores de calibracion que el emisor va a leer."""
    texto = (RAIZ / MARCO_REL).read_text(encoding="utf-8")
    filas = list(csv.DictReader(io.StringIO(texto), delimiter="\t"))
    campos = filas[0].keys()
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(campos), delimiter="\t",
                       lineterminator="\n")
    w.writeheader()
    for fila in filas:
        if fila["id"] in ids:
            w.writerow(fila)
    return buf.getvalue().encode("utf-8")


# ── A1 · wrapper M ─────────────────────────────────────────────────────────

def t_m_emite_solo_las_celdas_del_marco_que_recibe() -> None:
    """El marco es INPUT, no cableado: un marco de dos celdas produce dos
    celdas. Es la diferencia contra `emite_m.camina()`, que siempre camina
    `marco-M-sorteado-v1_1.tsv` pase lo que pase."""
    mod = _carga(CALC_M / "medidor.py", "med_m_t1")
    inputs = {
        "IN-MARCO-M-SORTEADO-V1-3": _entrada(
            "IN-MARCO-M-SORTEADO-V1-3", _marco_fixture(["CIV-M-01", "TRA-M-03"])),
        "IN-EMITE-M": _entrada_de("IN-EMITE-M", "tools/emite_m.py"),
    }
    v = mod.medir(inputs, {"parametros": {"fuente_acto": "TEST"}})
    if v["RESULT-M-N-CELDAS"] != 2:
        _falla("t_m_emite_solo_las_celdas_del_marco_que_recibe",
               f"N-CELDAS={v['RESULT-M-N-CELDAS']}, esperaba 2")
    if v["RESULT-M-N-EMITIDAS"] != 2:
        _falla("t_m_emite_solo_las_celdas_del_marco_que_recibe",
               f"N-EMITIDAS={v['RESULT-M-N-EMITIDAS']}, esperaba 2")
    faltan = [k for k in ("RESULT-M-CIV-M-01-P", "RESULT-M-TRA-M-03-P")
              if k not in v]
    if faltan:
        _falla("t_m_emite_solo_las_celdas_del_marco_que_recibe",
               f"faltan resultados: {faltan}")
    sobra = [k for k in v if k.startswith("RESULT-M-FAM-")]
    if sobra:
        _falla("t_m_emite_solo_las_celdas_del_marco_que_recibe",
               f"emitio celdas fuera del marco recibido: {sobra}")


def t_m_es_determinista_sobre_el_mismo_marco() -> None:
    """Dos corridas del wrapper sobre los MISMOS bytes dan los mismos valores.
    Es la precondicion de que `verify` pueda dar REPRODUCE/IDENTICO."""
    mod = _carga(CALC_M / "medidor.py", "med_m_t2")
    crudo = _marco_fixture(["CIV-M-01", "FAM-M-05"])
    def corrida():
        return mod.medir({
            "IN-MARCO-M-SORTEADO-V1-3": _entrada("IN-MARCO-M-SORTEADO-V1-3", crudo),
            "IN-EMITE-M": _entrada_de("IN-EMITE-M", "tools/emite_m.py"),
        }, {"parametros": {"fuente_acto": "TEST"}})
    a, b = corrida(), corrida()
    # `RESULT-M-CIEGO-A-R` cuenta aperturas del proceso y puede variar con el
    # cacheo de imports: se compara aparte, por su forma, no por su cifra.
    clave = "RESULT-M-CIEGO-A-R"
    if {k: v for k, v in a.items() if k != clave} != \
            {k: v for k, v in b.items() if k != clave}:
        _falla("t_m_es_determinista_sobre_el_mismo_marco",
               "dos corridas del wrapper difieren")
    for salida in (a[clave], b[clave]):
        if not salida.startswith("VERIFICADO-POR-AUDITHOOK:"):
            _falla("t_m_es_determinista_sobre_el_mismo_marco",
                   f"ciego_a_R no viene del hook: {salida[:60]!r}")


def t_m_levanta_si_abre_legado_gen1() -> None:
    """El audithook no es decorativo: si algo abre `corridas-M/` dentro de la
    ventana de emision, el medidor levanta y `run` no sella. Se prueba
    inyectando la apertura -- sin inyeccion, un test verde no distingue
    'el hook funciona' de 'no habia nada que atrapar'."""
    mod = _carga(CALC_M / "medidor.py", "med_m_t3")
    auditor = mod._Auditor()
    auditor.activo = True
    ruta = str(RAIZ / "forense/prereg-duelo-v2/corridas-M/M-CIV-M-01.json")
    auditor("open", (ruta, "r", 0))
    if not auditor.prohibidas:
        _falla("t_m_levanta_si_abre_legado_gen1",
               "el auditor no marco una apertura bajo corridas-M/")
    auditor2 = mod._Auditor()
    auditor2.activo = True
    auditor2("open", (str(RAIZ / MARCO_REL), "r", 0))
    if auditor2.prohibidas:
        _falla("t_m_levanta_si_abre_legado_gen1",
               "el auditor marco el marco vigente como legado")
    if auditor2.aperturas != 1:
        _falla("t_m_levanta_si_abre_legado_gen1",
               f"no conto la apertura legitima: {auditor2.aperturas}")


# ── A2 · adaptador R ───────────────────────────────────────────────────────

def t_r_resuelve_por_payload_id_exacto() -> None:
    """Un payload_id, no una lista de candidatos."""
    mod = _carga(RAIZ / "tools/arbitra_gen2.py", "arb2_t1")
    r = mod.resuelve_celda("CIV-08")
    if r["payload_id"] != "envipe2023_csv":
        _falla("t_r_resuelve_por_payload_id_exacto",
               f"payload_id={r['payload_id']!r}, esperaba 'envipe2023_csv'")
    if "candidatos" in json.dumps(r).lower():
        _falla("t_r_resuelve_por_payload_id_exacto",
               "la resolucion devuelve candidatos (plural)")
    if r["resuelto_por"] != "tests/payload_resolver.resolver_payload":
        _falla("t_r_resuelve_por_payload_id_exacto",
               f"resuelto_por={r['resuelto_por']!r}")


def t_r_sin_fila_de_codificacion_levanta_no_adivina() -> None:
    """La celda sin `payload_id` declarado no obtiene 'el mas parecido'."""
    mod = _carga(RAIZ / "tools/arbitra_gen2.py", "arb2_t2")
    tabla = {"CIV-08": {"id": "CIV-08", "payload_id": "envipe2023_csv"},
             "SIN-PAYLOAD": {"id": "SIN-PAYLOAD", "payload_id": "  "}}
    for id_celda in ("NO-EXISTE", "SIN-PAYLOAD"):
        try:
            mod.payload_id_de(id_celda, tabla)
        except mod.SinPayloadDeclarado:
            pass
        else:
            _falla("t_r_sin_fila_de_codificacion_levanta_no_adivina",
                   f"{id_celda}: devolvio un payload_id en vez de levantar")


def t_r_spec_declara_el_payload_como_input_de_manifiesto() -> None:
    mod = _carga(RAIZ / "tools/arbitra_gen2.py", "arb2_t3")
    spec = mod.spec_de_celda("CIV-08", MARCO_REL)
    manif = [i for i in spec["inputs"] if i.get("origen") == "manifiesto"]
    if len(manif) != 1 or manif[0]["id"] != "envipe2023_csv":
        _falla("t_r_spec_declara_el_payload_como_input_de_manifiesto",
               f"inputs de manifiesto: {manif}")
    if spec["calc_id"] != "CALC-R-CIV-08":
        _falla("t_r_spec_declara_el_payload_como_input_de_manifiesto",
               f"calc_id={spec['calc_id']!r}")
    for campo in ("variables", "universo", "filtros", "ponderador",
                  "transformacion", "estimando", "parametros", "seed",
                  "dependencias_materiales", "resultados", "tolerancia"):
        if campo not in spec:
            _falla("t_r_spec_declara_el_payload_como_input_de_manifiesto",
                   f"dimension sustantiva ausente: {campo}")


def t_r_se_abstiene_si_el_payload_no_coincide() -> None:
    """`medir` no calcula sobre un archivo cuya identidad no cuadra: se
    abstiene con motivo. Es el camino que este entorno (sin corpus) ejerce."""
    mod = _carga(RAIZ / "tools/arbitra_gen2.py", "arb2_t4")
    v = mod.medir({"p": {"id": "envipe2023_csv", "origen": "manifiesto",
                         "estado": "AUSENTE"}},
                  {"parametros": {"id_celda": "CIV-08"}})
    if v["RESULT-R-CIV-08-PUNTO"] is not None:
        _falla("t_r_se_abstiene_si_el_payload_no_coincide",
               "produjo un punto con el payload AUSENTE")
    if "ABSTENCION" not in v["RESULT-R-CIV-08-ESTADO"]:
        _falla("t_r_se_abstiene_si_el_payload_no_coincide",
               f"estado={v['RESULT-R-CIV-08-ESTADO']!r}")


# ── A3 · corredor L sucesor ────────────────────────────────────────────────

def t_l_cubre_las_14_celdas_x_2_variantes_x_k8() -> None:
    mod = _carga(RAIZ / "forense/prereg-duelo-v2/corredor_l_v1_2.py", "corl_t1")
    plan = mod.plan()
    if len(plan) != 14 * 2 * 8:
        _falla("t_l_cubre_las_14_celdas_x_2_variantes_x_k8",
               f"plan de {len(plan)} corridas, esperaba 224")
    rutas = {mod.ruta_salida(c["id"], v, k) for c, v, k in plan}
    if len(rutas) != len(plan):
        _falla("t_l_cubre_las_14_celdas_x_2_variantes_x_k8",
               f"{len(plan) - len(rutas)} rutas colisionan")


def t_l_no_escribe_en_corridas_l_gen1() -> None:
    mod = _carga(RAIZ / "forense/prereg-duelo-v2/corredor_l_v1_2.py", "corl_t2")
    for celda, variante, k in mod.plan():
        plana = str(mod.ruta_salida(celda["id"], variante, k)).replace("\\", "/")
        if "/corridas-L/" in plana:
            _falla("t_l_no_escribe_en_corridas_l_gen1",
                   f"ruta bajo legado GEN1: {plana}")
            return


def t_l_toma_el_prompt_verbatim_de_la_spec() -> None:
    """El prompt es `pregunta_L` tal cual; la variante `L+corpus` antepone el
    encabezado y NO reescribe la pregunta."""
    mod = _carga(RAIZ / "forense/prereg-duelo-v2/corredor_l_v1_2.py", "corl_t3")
    celda = mod.cargar_celdas()[0]
    if mod.prompt_de(celda, "L-solo") != celda["pregunta_L"]:
        _falla("t_l_toma_el_prompt_verbatim_de_la_spec",
               "L-solo no es pregunta_L verbatim")
    con_corpus = mod.prompt_de(celda, "L+corpus")
    if not con_corpus.endswith(celda["pregunta_L"]):
        _falla("t_l_toma_el_prompt_verbatim_de_la_spec",
               "L+corpus reescribio la pregunta en vez de anteponer")


def t_l_levanta_si_el_universo_no_es_de_14() -> None:
    """El corredor declara 14 celdas. Si la spec cambia de universo bajo sus
    pies, para -- no corre sobre un universo que no declaro."""
    mod = _carga(RAIZ / "forense/prereg-duelo-v2/corredor_l_v1_2.py", "corl_t4")
    datos = json.loads((RAIZ / "forense/prereg-duelo-v2/L-spec-v1_2.json")
                       .read_text(encoding="utf-8"))
    datos["celdas"] = datos["celdas"][:3]
    with tempfile.TemporaryDirectory() as tmp:
        falso = Path(tmp) / "L-spec-v1_2.json"
        falso.write_text(json.dumps(datos), encoding="utf-8")
        original = mod.L_SPEC_JSON
        mod.L_SPEC_JSON = falso
        try:
            mod.cargar_celdas()
        except mod.UniversoInesperado:
            pass
        else:
            _falla("t_l_levanta_si_el_universo_no_es_de_14",
                   "acepto un universo de 3 celdas")
        finally:
            mod.L_SPEC_JSON = original


# ── A4 · agregado derivado ─────────────────────────────────────────────────

def t_agg_consume_solo_results_y_declara_los_ejes_ausentes() -> None:
    """Sin RESULT-R ni RESULT-L, los ejes salen NO-ESTIMABLE con motivo -- no
    se rellenan con la cifra GEN1 de `agregado-v1_3-resultado.json`."""
    mod = _carga(CALC_AGG / "medidor.py", "med_agg_t1")
    marco = _marco_fixture(["CIV-M-01", "TRA-M-03"])
    res_m = json.dumps({"spec_id": "CALC-M-x", "resultados": {
        "RESULT-M-CIV-M-01-P": 0.25, "RESULT-M-TRA-M-03-P": 0.5,
    }}).encode("utf-8")
    v = mod.medir({
        "IN-MARCO-M-SORTEADO-V1-3": _entrada("IN-MARCO-M-SORTEADO-V1-3", marco,
                                             ruta=MARCO_REL),
        "IN-CALC-M-RESULTADOS": _entrada("IN-CALC-M-RESULTADOS", res_m,
                                         ruta="data/corrida0/x/resultados.json"),
    }, {"parametros": {}})
    if (v["RESULT-AGG-N-CELDAS"], v["RESULT-AGG-N-CON-M"]) != (2, 2):
        _falla("t_agg_consume_solo_results_y_declara_los_ejes_ausentes",
               f"conteos={v['RESULT-AGG-N-CELDAS']}/{v['RESULT-AGG-N-CON-M']}")
    if v["RESULT-AGG-N-CON-R"] != 0 or v["RESULT-AGG-N-CON-L"] != 0:
        _falla("t_agg_consume_solo_results_y_declara_los_ejes_ausentes",
               "conto insumos R/L que no existen")
    for clave in ("RESULT-AGG-EJE-M-VS-R", "RESULT-AGG-EJE-M-VS-L"):
        if not v[clave].startswith("NO-ESTIMABLE"):
            _falla("t_agg_consume_solo_results_y_declara_los_ejes_ausentes",
                   f"{clave}={v[clave]!r}")
    if v["RESULT-AGG-M-P-MEDIANA"] != 0.375:
        _falla("t_agg_consume_solo_results_y_declara_los_ejes_ausentes",
               f"mediana={v['RESULT-AGG-M-P-MEDIANA']}")


def t_agg_entra_R_y_L_cuando_existen_sin_tocar_el_medidor() -> None:
    """El dia que haya CALC-R/CALC-L, entran por la spec. Se prueba ahora para
    que el hueco no se descubra el dia que importe."""
    mod = _carga(CALC_AGG / "medidor.py", "med_agg_t2")
    marco = _marco_fixture(["CIV-M-01", "TRA-M-03"])
    def res(prefijo, clave):
        return json.dumps({"resultados": {
            f"RESULT-{prefijo}-CIV-M-01-{clave}": 0.2}}).encode("utf-8")
    v = mod.medir({
        "IN-MARCO-M-SORTEADO-V1-3": _entrada("IN-MARCO-M-SORTEADO-V1-3", marco),
        "IN-CALC-M-RESULTADOS": _entrada("IN-CALC-M-RESULTADOS", res("M", "P")),
        "IN-CALC-R-RESULTADOS": _entrada("IN-CALC-R-RESULTADOS", res("R", "PUNTO")),
        "IN-CALC-L-RESULTADOS": _entrada("IN-CALC-L-RESULTADOS", res("L", "PUNTO")),
    }, {"parametros": {}})
    if (v["RESULT-AGG-N-CON-R"], v["RESULT-AGG-N-CON-L"]) != (1, 1):
        _falla("t_agg_entra_R_y_L_cuando_existen_sin_tocar_el_medidor",
               f"R={v['RESULT-AGG-N-CON-R']} L={v['RESULT-AGG-N-CON-L']}")
    if v["RESULT-AGG-EJE-M-VS-R"] != "ESTIMABLE":
        _falla("t_agg_entra_R_y_L_cuando_existen_sin_tocar_el_medidor",
               f"eje M-vs-R sigue en {v['RESULT-AGG-EJE-M-VS-R']!r}")


# ── Pieza B · Go/No-Go ─────────────────────────────────────────────────────

def t_gonogo_los_seis_checks_existen_y_corren() -> None:
    mod = _carga(RAIZ / "tests/gonogo_marcador.py", "gonogo_t1")
    nombres = [n for n, _ in mod.CHECKS]
    esperados = ["MARCO-VIGENTE-UNICO", "M-DESDE-CONTRATO", "R-SIN-HEURISTICA",
                 "L-SPEC-v1_2", "AGREGADO-DERIVADO", "LEGACY-NO-LEIDO"]
    if nombres != esperados:
        _falla("t_gonogo_los_seis_checks_existen_y_corren",
               f"checks={nombres}")


def t_gonogo_ast_ignora_la_prosa_y_ve_las_llamadas() -> None:
    """El falsador del propio Go/No-Go: un modulo que solo MENCIONA
    `localiza_payload` en un docstring esta limpio; uno que la LLAMA no.
    Sin este caso, `R-SIN-HEURISTICA` podria estar midiendo comentarios."""
    mod = _carga(RAIZ / "tests/gonogo_marcador.py", "gonogo_t2")
    limpio = '"""Este modulo no usa localiza_payload."""\nx = 1\n'
    sucio = "import arbitra\ny = arbitra.localiza_payload(1, 2, 3)\n"
    if "localiza_payload" in mod.identificadores(limpio):
        _falla("t_gonogo_ast_ignora_la_prosa_y_ve_las_llamadas",
               "conto una mencion de docstring como uso")
    if "localiza_payload" not in mod.identificadores(sucio):
        _falla("t_gonogo_ast_ignora_la_prosa_y_ve_las_llamadas",
               "no vio una llamada real")


def t_gonogo_ve_la_constante_armada_con_barra() -> None:
    """`L_SPEC_JSON = DIR / "L-spec-v1_2.json"` es un BinOp. Una version previa
    de `constantes_str` solo miraba `NOMBRE = "literal"` y no veia esta linea
    -- exactamente la que `L-SPEC-v1_2` necesita leer."""
    mod = _carga(RAIZ / "tests/gonogo_marcador.py", "gonogo_t3")
    consts = mod.constantes_str('DIR = "x"\nL_SPEC_JSON = DIR / "L-spec-v1_2.json"\n')
    if "L-spec-v1_2.json" not in consts.get("L_SPEC_JSON", []):
        _falla("t_gonogo_ve_la_constante_armada_con_barra",
               f"no leyo la constante: {consts}")


def t_gonogo_marco_vigente_unico_atrapa_dos_marcos() -> None:
    mod = _carga(RAIZ / "tests/gonogo_marcador.py", "gonogo_t4")
    consts = mod.constantes_str(
        'A = "forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv"\n')
    encontrados = [m for vals in consts.values() for v in vals
                   for m in mod._RE_MARCO.findall(v)]
    if encontrados != ["marco-M-sorteado-v1_1.tsv"]:
        _falla("t_gonogo_marco_vigente_unico_atrapa_dos_marcos",
               f"el detector de marcos no vio v1_1: {encontrados}")


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def corre() -> list[str]:
    """Devuelve la lista de fallos (vacia = verde). La llama `tests/check.py`."""
    FALLOS.clear()
    for fn in TESTS:
        try:
            fn()
        except Exception as exc:  # un test que revienta es un fallo, no un hueco
            _falla(fn.__name__, f"EXCEPCION {type(exc).__name__}: {exc}")
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    print(f"tests/test_corredores_gen2.py · {len(TESTS)} casos · "
          f"{len(TESTS) - len({f.split(':')[0] for f in fallos})} ok · "
          f"{len(fallos)} FALLOS")
    for f in fallos:
        print(f"  FAIL  {f}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
