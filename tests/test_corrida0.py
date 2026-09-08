#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/test_corrida0.py` -- unidad de `preflight` / `verify` / `spec-check`
/ `negativo` con fixtures pequenos y SIN CORPUS.

ACTO GEN2-E3 · AUTOMATIZA-GEN2-1 (nucleo) + ACTO GEN2-E3-1 ·
READINESS-DEL-RUNNER (P1-P6: resolver unico de payload, contrato ejecutable,
outputs validados, inmutabilidad y sello completo, verify en dos ejes).
Lo llama `tests/check.py` (T32 · T-CORRIDA0).

Estos tests no abren microdato, no tocan la red y no escriben fuera de un
directorio temporal. Los unicos archivos reales que leen son los TRES
inventarios canonicos vigentes -- que es justo lo que el caso de prueba
obligatorio del encargo exige comprobar contra el arbol de verdad.

Nota sobre `preflight` en un test: el arbol de trabajo esta sucio mientras
la suite corre, asi que `preflight` siempre devuelve BLOQUEADO aqui. Por eso
los tests afirman sobre los BLOQUEOS CONCRETOS (que aparezca el que toca y
que NO aparezca el que no toca), no sobre un VERDE global que en este
contexto seria imposible y cuya ausencia no probaria nada.

Misma nota, extendida (GEN2-E3-1): `run()` real tampoco puede completar
punta a punta aqui -- exige `preflight` VERDE, que a su vez exige que
`spec.yaml`/`spec.md` esten COMMITEADOS (`git ls-files`), y un `spec.yaml`
de fixture vive en un directorio temporal FUERA del repo. Los catorce casos
de P6 que dependen de lo que `run`/`verify` escriben prueban las piezas que
`run`/`verify` factorizan para eso (`_fallas_run`, `_construye_ejecucion`,
`_construye_sello`, `_evalua_contexto`, `_verifica_sello`) en vez de invocar
`run()` de punta a punta -- mismo patron que ya usan `t_ejecuta_reporta_el_
fallo_como_hecho`/`t_tolerancia_*` para `_ejecuta`/`_compara`. La unica
excepcion real es T-SELLADO-NO-SOBRESCRIBE: la inmutabilidad se comprueba
ANTES de llamar a `preflight`, asi que `run()` si se invoca completo.
"""
from __future__ import annotations

import csv
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import contextlib
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("corrida0_bajo_prueba",
                                               RAIZ / "tools" / "corrida0.py")
C = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = C
_spec.loader.exec_module(C)

FALLOS: list[str] = []


def _falla(caso: str, msg: str) -> None:
    FALLOS.append(f"{caso}: {msg}")


def _afirma(cond, caso: str, msg: str) -> None:
    if not cond:
        _falla(caso, msg)


@contextlib.contextmanager
def _calc_temporal(spec: dict, spec_md: str = "# spec de prueba\n"):
    """Un CALC completo en un directorio temporal. `C.CORRIDAS` se re-apunta
    ahi y se restaura siempre -- ningun test escribe en `data/corrida0/`."""
    tmp = Path(tempfile.mkdtemp(prefix="calc-test-"))
    calc_id = spec.get("calc_id", "CALC-TEST-0000")
    d = tmp / calc_id
    d.mkdir(parents=True)
    (d / "spec.md").write_text(spec_md, encoding="utf-8")
    import yaml
    (d / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True),
                                 encoding="utf-8")
    previo = C.CORRIDAS
    C.CORRIDAS = tmp
    try:
        yield d, calc_id
    finally:
        C.CORRIDAS = previo
        shutil.rmtree(tmp, ignore_errors=True)


def _silencioso(fn, *a, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = fn(*a, **kw)
    return r, buf.getvalue()


def _sha(ruta: Path) -> str:
    import hashlib
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


# ── 1 · spec-check: el caso de prueba OBLIGATORIO del encargo ──────────────

def t_spec_check_hs02g_dos_archivos():
    """`iiib_hs.dta::hs02g` y `p_hs.dta::hs02g` existen los dos, y traen
    ETIQUETAS DISTINTAS. El check tiene que resolver cada uno contra SU
    archivo -- que la variable exista en el otro archivo del mismo
    instrumento no la da por hallada."""
    caso = "spec-check hs02g (iiib_hs.dta vs p_hs.dta)"
    with _calc_temporal({
            "calc_id": "CALC-TEST-HS", "spec_md": "spec.md",
            "variables": [{"archivo": "iiib_hs.dta", "variable": "hs02g"},
                          {"archivo": "p_hs.dta", "variable": "hs02g"}]}) as (_d, cid):
        r, salida = _silencioso(C.spec_check, cid)

    _afirma(r["n_fail"] == 0, caso,
            f"ambos pares deberian existir en los inventarios vigentes; n_fail={r['n_fail']}")
    _afirma(r["filas_examinadas"] > 0, caso,
            "A.13: un check que examino 0 filas no es un check")

    etiquetas = {}
    for item in r["items"]:
        e = item.get("etiqueta")
        etiquetas[item["archivo"]] = set(e) if isinstance(e, list) else {e}
    _afirma(set(etiquetas) == {"iiib_hs.dta", "p_hs.dta"}, caso,
            f"faltan pares en el resultado: {sorted(etiquetas)}")
    if set(etiquetas) == {"iiib_hs.dta", "p_hs.dta"}:
        _afirma(etiquetas["iiib_hs.dta"] != etiquetas["p_hs.dta"], caso,
                "ETIQUETAS DISTINTAS no detectadas: el check estaria colapsando "
                "dos archivos con la misma variable en uno solo -- que es "
                f"exactamente el defecto que persigue. {etiquetas}")
    _afirma("filas del archivo en inventario" in salida, caso,
            "la salida no declara cuantas filas del archivo examino (A.13)")
    _afirma("secciones del instrumento" in salida, caso,
            "la salida no lista las secciones del instrumento presentes en el inventario")


def t_spec_check_imms_warn():
    """`IMMS` no existe: FAIL, con WARN «¿IMSS?» a distancia <= 2. La
    sugerencia NO se da por hallada (sigue siendo FAIL) ni edita la spec."""
    caso = "spec-check IMMS -> WARN ¿IMSS?"
    cab = "payload_id\tsha256_12\tinstrumento\tola\tarchivo_miembro\tvariable_id\ttexto_reactivo\tmetodo\tuniverso_declarado\n"
    filas = ("P1\tabc\tENCUESTA-X\tNO_DETERMINADO\tmod/afil.dta\tIMSS\t¿ESTA AFILIADO AL IMSS?\tm\tu\n"
             "P1\tabc\tENCUESTA-X\tNO_DETERMINADO\tmod/afil.dta\tissste\t¿ESTA AFILIADO AL ISSSTE?\tm\tu\n")
    tmp = Path(tempfile.mkdtemp(prefix="inv-test-"))
    inv = tmp / "inventario-falso.tsv"
    inv.write_text(cab + filas, encoding="utf-8")
    try:
        with _calc_temporal({
                "calc_id": "CALC-TEST-IMMS", "spec_md": "spec.md",
                "variables": [{"archivo": "mod/afil.dta", "variable": "IMMS"}]}) as (_d, cid):
            r, salida = _silencioso(C.spec_check, cid, universo=[inv])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    _afirma(r["n_fail"] == 1, caso, f"IMMS no existe: deberia ser FAIL. n_fail={r['n_fail']}")
    item = r["items"][0]
    _afirma("IMSS" in (item.get("sugerencias_warn") or []), caso,
            f"no se sugirio IMSS a distancia <=2; sugerencias={item.get('sugerencias_warn')}")
    _afirma("[WARN] ¿IMSS?" in salida, caso,
            "la sugerencia no salio como WARN literal en la salida")
    _afirma(item["estado"] == "FAIL", caso,
            "la sugerencia dio el par por hallado -- una sugerencia NUNCA cierra un FAIL")
    _afirma("issste" not in (item.get("sugerencias_warn") or []), caso,
            "se sugirio una variable a distancia > 2")


def t_distancia_edicion():
    caso = "distancia de edicion"
    _afirma(C._distancia_edicion("IMMS", "IMSS") == 1, caso,
            "IMMS/IMSS es una sustitucion (M->S en la 3a): distancia 1")
    _afirma(C._distancia_edicion("hs02g", "hs20g") == 2, caso,
            "una transposicion cuesta 2 en Levenshtein -- sigue dentro del "
            "umbral <=2, que es justo por lo que el umbral es 2 y no 1")
    _afirma(C._distancia_edicion("hs02g", "hs02g") == 0, caso, "identicas != 0")
    _afirma(C._distancia_edicion("a", "abcde") == 4, caso, "longitudes distintas")


def t_mismo_archivo_es_por_ruta():
    caso = "_mismo_archivo corta por separador de ruta"
    _afirma(C._mismo_archivo("ehh05dta_b3b/iiib_hs.dta", "iiib_hs.dta"), caso,
            "un sufijo de ruta valido no caso")
    _afirma(C._mismo_archivo("a/b/iiib_hs.dta", "b/iiib_hs.dta"), caso,
            "sufijo de dos segmentos no caso")
    _afirma(not C._mismo_archivo("x/aiiib_hs.dta", "iiib_hs.dta"), caso,
            "COINCIDENCIA PARCIAL DE NOMBRE aceptada: `aiiib_hs.dta` no es "
            "`iiib_hs.dta` y tratarlos igual inventaria un hallazgo")
    _afirma(not C._mismo_archivo("x/iiib_hs.dta", ""), caso,
            "un archivo vacio en la spec casaria con todo")


# ── 2 · negativo ───────────────────────────────────────────────────────────

def t_negativo_declara_lo_examinado():
    """A.13: un negativo producido por un comando que no examino archivos no
    es un negativo."""
    caso = "negativo declara universo examinado"
    r, salida = _silencioso(C.negativo, r"NO_EXISTE_ESTE_VOCABULARIO_ZZZ")
    _afirma(r["veredicto"] == "SIN-COBERTURA", caso, f"veredicto={r['veredicto']}")
    _afirma(r["filas_examinadas"] > 1000, caso,
            f"solo examino {r['filas_examinadas']} filas de los inventarios vigentes")
    _afirma(r["archivos_examinados"] > 0, caso, "archivos_examinados = 0")
    for token in ("filas examinadas", "archivos examinados",
                  "LINEA PARA EL RECIBO"):
        _afirma(token in salida, caso, f"la salida no trae `{token}`")
    _afirma("filas_examinadas=" in r["linea_recibo"], caso,
            "la linea del recibo no declara las filas examinadas")


def t_negativo_filtra_por_archivo():
    caso = "negativo --archivos filtra el universo"
    todo, _ = _silencioso(C.negativo, r"INTERNADO")
    sub, _ = _silencioso(C.negativo, r"INTERNADO", "iiib_hs")
    _afirma(sub["filas_examinadas"] < todo["filas_examinadas"], caso,
            "el filtro no redujo el universo")
    _afirma(sub["aciertos"] <= todo["aciertos"], caso,
            "el filtro produjo MAS aciertos que el universo completo")
    _afirma(sub["aciertos"] > 0, caso,
            "fixture rota: `INTERNADO` deberia acertar en iiib_hs")


# ── 3 · preflight ──────────────────────────────────────────────────────────

_SPEC_BASE = {
    "calc_id": "CALC-TEST-PRE", "spec_md": "spec.md", "spec_md_sha256": "",
    "script": "tools/entorno.py", "inputs": [], "parametros": {"a": 1},
    "seed": 42, "tolerancia": {"tipo": "flotante", "abs": 1e-10},
    "resultados": [{"id": "RESULT-A"}, {"id": "RESULT-B"}],
}


def _preflight_de(spec: dict, spec_md: str = "# x\n"):
    with _calc_temporal(spec, spec_md) as (d, cid):
        # el sha del md se declara sobre el md real, salvo que el test lo fije
        if spec.get("spec_md_sha256") == "":
            import yaml
            spec = dict(spec, spec_md_sha256=_sha(d / "spec.md"))
            (d / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True),
                                         encoding="utf-8")
        return _silencioso(C.preflight, cid)


def t_preflight_ids_duplicados():
    caso = "preflight ids duplicados"
    spec = dict(_SPEC_BASE, resultados=[{"id": "RESULT-A"}, {"id": "RESULT-A"}])
    r, _s = _preflight_de(spec)
    _afirma(any("ids_resultados_duplicados" in b for b in r["bloqueos"]), caso,
            f"no bloqueo por ids duplicados: {r['bloqueos']}")


def t_preflight_ids_unicos_no_bloquean():
    caso = "preflight ids unicos"
    r, _s = _preflight_de(dict(_SPEC_BASE))
    _afirma(not any("ids_resultados_duplicados" in b for b in r["bloqueos"]), caso,
            f"bloqueo por duplicados con ids unicos: {r['bloqueos']}")


def t_preflight_campos_obligatorios():
    caso = "preflight campos obligatorios"
    for campo in ("script", "parametros", "resultados"):
        spec = {k: v for k, v in _SPEC_BASE.items() if k != campo}
        r, _s = _preflight_de(spec)
        _afirma(f"spec_sin_{campo}" in r["bloqueos"], caso,
                f"no bloqueo al faltar `{campo}`: {r['bloqueos']}")
    spec = {k: v for k, v in _SPEC_BASE.items() if k != "seed"}
    r, _s = _preflight_de(spec)
    _afirma("seed_no_declarado" in r["bloqueos"] or "spec_sin_seed" in r["bloqueos"],
            caso, f"no bloqueo al faltar `seed`: {r['bloqueos']}")


def t_preflight_sha_del_md():
    """El sha del md que la spec cita tiene que ser el del md real. Si no,
    alguien movio la spec bajo los pies de la corrida."""
    caso = "preflight sha del spec.md"
    ok, _s = _preflight_de(dict(_SPEC_BASE))
    _afirma("spec_md_sha256_discorda_arbol" not in ok["bloqueos"], caso,
            f"sha correcto marcado como discordante: {ok['bloqueos']}")
    _afirma(ok["spec_md_estado"] in ("NO-EN-MAIN", "EN-MAIN-COINCIDE"), caso,
            f"estado inesperado: {ok['spec_md_estado']}")

    malo, _s = _preflight_de(dict(_SPEC_BASE, spec_md_sha256="0" * 64))
    _afirma("spec_md_sha256_discorda_arbol" in malo["bloqueos"], caso,
            f"sha falso NO bloqueo: {malo['bloqueos']}")
    _afirma(malo["spec_md_estado"] == "ARBOL-DISCORDA", caso,
            f"estado={malo['spec_md_estado']}")


def t_preflight_script_ausente():
    caso = "preflight script ausente"
    r, _s = _preflight_de(dict(_SPEC_BASE, script="tools/no_existe_zzz.py"))
    _afirma(any(b.startswith("script_ausente") for b in r["bloqueos"]), caso,
            f"no bloqueo por script ausente: {r['bloqueos']}")


def t_preflight_input_repo_sha():
    caso = "preflight input repo con sha"
    ruta = "tools/entorno.py"
    bueno = _sha(RAIZ / ruta)
    r, _s = _preflight_de(dict(_SPEC_BASE, inputs=[
        {"id": "IN-A", "origen": "repo", "ruta": ruta, "sha256": bueno}]))
    _afirma("input_repo_sha_discorda=IN-A" not in r["bloqueos"], caso,
            f"sha correcto marcado discordante: {r['bloqueos']}")
    malo, _s = _preflight_de(dict(_SPEC_BASE, inputs=[
        {"id": "IN-A", "origen": "repo", "ruta": ruta, "sha256": "0" * 64}]))
    _afirma("input_repo_sha_discorda=IN-A" in malo["bloqueos"], caso,
            f"sha falso NO bloqueo: {malo['bloqueos']}")
    aus, _s = _preflight_de(dict(_SPEC_BASE, inputs=[
        {"id": "IN-A", "origen": "repo", "ruta": "tools/no_existe_zzz.py",
         "sha256": "0" * 64}]))
    _afirma(any(b.startswith("input_repo_ausente") for b in aus["bloqueos"]), caso,
            f"input ausente NO bloqueo: {aus['bloqueos']}")


def t_preflight_no_commiteado():
    """Un CALC temporal no esta en el indice de git: eso ES un bloqueo, y el
    test lo afirma en vez de esconderlo."""
    caso = "preflight exige spec commiteada"
    r, salida = _preflight_de(dict(_SPEC_BASE))
    _afirma(any(b.startswith("no_commiteado=") for b in r["bloqueos"]), caso,
            f"una spec fuera del indice deberia bloquear: {r['bloqueos']}")
    _afirma(r["veredicto"] == "BLOQUEADO", caso, "veredicto no fue BLOQUEADO")
    _afirma("PRE-FLIGHT: BLOQUEADO" in salida, caso,
            "la salida no imprime el rotulo `PRE-FLIGHT: BLOQUEADO`")


def t_preflight_arbol_sucio_es_bloqueo():
    """`working_tree_dirty=SI` con el rotulo exacto del encargo."""
    caso = "preflight working_tree_dirty"
    r, salida = _preflight_de(dict(_SPEC_BASE))
    limpio = C._git_salida("status", "--porcelain")[1].strip() == ""
    if limpio:
        _afirma("working_tree_dirty=SI" not in r["bloqueos"], caso,
                "arbol limpio reportado como sucio")
    else:
        _afirma("working_tree_dirty=SI" in r["bloqueos"], caso,
                f"arbol sucio NO bloqueo: {r['bloqueos']}")
        _afirma("working_tree_dirty=SI" in salida, caso,
                "el rotulo exacto del encargo no salio en la salida")


# ── 4 · verify / tolerancias ───────────────────────────────────────────────

def t_tolerancia_flotante():
    caso = "tolerancia flotante"
    tol = {"tipo": "flotante", "abs": 1e-10}
    ok, d = C._compara(1.0, 1.0 + 3e-15, tol)
    _afirma(ok, caso, f"3e-15 deberia caer dentro de 1e-10 (delta={d})")
    ok, d = C._compara(1.0, 1.0 + 1e-6, tol)
    _afirma(not ok, caso, f"1e-6 deberia caer FUERA de 1e-10 (delta={d})")
    _afirma(abs(d - 1e-6) < 1e-12, caso, f"delta mal calculado: {d}")


def t_tolerancia_entero_es_exacta():
    caso = "tolerancia entero exacta"
    tol = {"tipo": "entero"}
    _afirma(C._compara(14, 14, tol)[0], caso, "14 == 14 fallo")
    _afirma(not C._compara(14, 15, tol)[0], caso,
            "un entero distinto paso: los enteros se comparan EXACTO")
    # y con tolerancia de flotante declarada, un entero distinto por 1 no pasa
    _afirma(not C._compara(14, 15, {"tipo": "flotante", "abs": 1e-10})[0], caso,
            "delta 1.0 paso una tolerancia de 1e-10")


def t_tolerancia_bootstrap():
    caso = "tolerancia bootstrap"
    exacta = {"tipo": "bootstrap", "exacto_por_seed": True}
    _afirma(not C._compara(1.0, 1.0 + 3e-15, exacta)[0], caso,
            "con seed+RNG+codigo fijados el bootstrap se compara EXACTO")
    laxa = {"tipo": "bootstrap", "abs": 1e-10}
    _afirma(C._compara(1.0, 1.0 + 3e-15, laxa)[0], caso,
            "sin `exacto_por_seed` cae a la tolerancia absoluta declarada")


def t_tolerancia_estructuras():
    caso = "tolerancia sobre dict/list"
    tol = {"tipo": "flotante", "abs": 1e-10}
    _afirma(C._compara({"a": 1.0}, {"a": 1.0 + 1e-15}, tol)[0], caso, "dict igual fallo")
    _afirma(not C._compara({"a": 1.0}, {"b": 1.0}, tol)[0], caso,
            "claves distintas pasaron")
    _afirma(not C._compara([1.0, 2.0], [1.0], tol)[0], caso,
            "listas de distinta longitud pasaron")
    _afirma(not C._compara(True, 1, tol)[0] is False, caso, "bool vs int")


def t_verify_sin_corrida_es_no_ejecutable():
    """Sin `ejecucion.json` no hay NO-REPRODUCE que dar: es NO-EJECUTABLE, y
    los tres veredictos no se colapsan."""
    caso = "verify sin corrida sellada"
    with _calc_temporal(dict(_SPEC_BASE)) as (_d, cid):
        r, _s = _silencioso(C.verify, cid)
    _afirma(r["veredicto"] == "NO-EJECUTABLE", caso, f"veredicto={r['veredicto']}")
    _afirma("razon" in r, caso, "NO-EJECUTABLE sin razon declarada")


def t_run_bloqueado_no_escribe():
    """Un `run` sobre un preflight BLOQUEADO no deja artefacto: la corrida
    que este CLI existe para no volver a producir."""
    caso = "run con preflight bloqueado no escribe"
    spec = dict(_SPEC_BASE, resultados=[{"id": "R"}, {"id": "R"}])
    with _calc_temporal(spec) as (d, cid):
        r, salida = _silencioso(C.run, cid)
        escritos = [p.name for p in d.iterdir()]
    _afirma(r["veredicto"] == "NO-EJECUTADO", caso, f"veredicto={r['veredicto']}")
    _afirma("ejecucion.json" not in escritos, caso,
            f"escribio pese al bloqueo: {escritos}")
    _afirma("RUN: NO-EJECUTADO" in salida, caso, "no imprimio el rotulo")


# ── 5 · medidor sin interfaz estable ───────────────────────────────────────

def t_medidor_sin_medir_es_error():
    caso = "interfaz estable medir(inputs, params)"
    tmp = Path(tempfile.mkdtemp(prefix="med-test-"))
    try:
        s = tmp / "sin_medir.py"
        s.write_text("def otra_cosa():\n    return {}\n", encoding="utf-8")
        try:
            C._carga_medidor(s)
        except RuntimeError as exc:
            _afirma("medir" in str(exc), caso, f"mensaje poco claro: {exc}")
        else:
            _falla(caso, "un medidor sin `medir()` fue aceptado")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_ejecuta_reporta_el_fallo_como_hecho():
    caso = "un medidor que revienta es un HECHO de la corrida"
    tmp = Path(tempfile.mkdtemp(prefix="med-test-"))
    try:
        s = tmp / "revienta.py"
        s.write_text("def medir(inputs, params):\n    raise ValueError('boom')\n",
                     encoding="utf-8")
        rel = os.path.relpath(s, RAIZ)
        spec = {"script": rel, "parametros": {}, "inputs": []}
        valores, code, err = C._ejecuta(spec, C._resuelve_inputs(spec))
        _afirma(code == 1 and "boom" in err, caso, f"code={code} err={err}")
        _afirma(valores == {}, caso, "devolvio valores tras reventar")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ── 6 · decisiones.tsv / FP-339 (D9/D10, ACTO GEN2-T7) ─────────────────────

def t_decisiones_tsv_se_lee():
    caso = "decisiones.tsv (D9/D10 · FP-339) se lee y trae las 7 filas"
    decisiones = C._lee_decisiones()
    _afirma(len(decisiones) == 7, caso, f"se esperaban 7 objetos, hay {len(decisiones)}")
    for objeto in ("TRA-M-02", "TRA-M-03", "TRA-M-07"):
        _afirma(decisiones.get(objeto) == "M_vivo=__v1_3", caso,
                f"{objeto} deberia decidir M_vivo=__v1_3, trae {decisiones.get(objeto)!r}")
    for objeto in (
            "milpa/tramite.yaml:dinero.ahorro.tiene_ahorros:tiene_ahorros",
            "milpa/tramite.yaml:dinero.ahorro.tiene_ahorros:no_tiene_ahorros",
            "milpa/tramite.yaml:familia.apoyo.recibe_dinero_familiares:"
            "recibe_dinero_familiares_para_vejez",
            "milpa/tramite.yaml:familia.apoyo.recibe_dinero_familiares:"
            "no_recibe_dinero_familiares_para_vejez"):
        _afirma(decisiones.get(objeto) == "receta_legacy=SIN-RECETA", caso,
                f"{objeto} deberia decidir receta_legacy=SIN-RECETA, "
                f"trae {decisiones.get(objeto)!r}")


def t_cmd_demanda_aplica_fp339():
    """`cmd_demanda` real (arbol de trabajo, no fixture): los 7 casos de
    FP-339 dejan de listarse como ambiguos por `stderr` porque mesa ya los
    decidio en `decisiones.tsv`, y las filas de las celdas TRA-M usan el M
    `__v1_3` mientras las de DIN/FAM quedan SIN-RECETA."""
    caso = "cmd_demanda aplica D9/D10 · FP-339"
    buf_out, buf_err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        codigo = C.cmd_demanda(None)
    _afirma(codigo == 0, caso, f"cmd_demanda devolvio {codigo}")
    salida_err = buf_err.getvalue()
    salida_out = buf_out.getvalue()
    _afirma("decisiones_aplicadas (FP-339) = 7" in salida_out, caso,
            f"no se declaro la aplicacion de las 7 decisiones: {salida_out!r}")
    for fragmento in ("TRA-M-02", "TRA-M-03", "TRA-M-07",
                      "dinero.ahorro.tiene_ahorros",
                      "familia.apoyo.recibe_dinero_familiares"):
        _afirma(fragmento not in salida_err, caso,
                f"{fragmento} sigue listado como ambiguo pese a FP-339: {salida_err!r}")

    with (C.SALIDA / "demanda-resultados.tsv").open(encoding="utf-8") as fh:
        fh.readline()  # "# DERIVADO -- NO EDITAR"
        resultados = list(csv.DictReader(fh, delimiter="\t"))
    por_consumidor = {f["consumidor"]: f for f in resultados}
    for sufijo in ("tiene_ahorros", "no_tiene_ahorros"):
        cons = f"milpa/tramite.yaml:dinero.ahorro.tiene_ahorros:{sufijo}"
        fila = por_consumidor.get(cons)
        _afirma(fila is not None, caso, f"falta la fila de {cons}")
        _afirma(fila and fila["receta_legacy"] == "SIN-RECETA", caso,
                f"{cons} deberia ser SIN-RECETA, es {fila and fila['receta_legacy']!r}")
    for sufijo in ("recibe_dinero_familiares_para_vejez",
                   "no_recibe_dinero_familiares_para_vejez"):
        cons = f"milpa/tramite.yaml:familia.apoyo.recibe_dinero_familiares:{sufijo}"
        fila = por_consumidor.get(cons)
        _afirma(fila is not None, caso, f"falta la fila de {cons}")
        _afirma(fila and fila["receta_legacy"] == "SIN-RECETA", caso,
                f"{cons} deberia ser SIN-RECETA, es {fila and fila['receta_legacy']!r}")
    for cid in ("TRA-M-02", "TRA-M-03", "TRA-M-07"):
        cons = f"forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:{cid}:M"
        fila = por_consumidor.get(cons)
        _afirma(fila is not None, caso, f"falta la fila M de {cid}")
        ruta_m = C._m_vigente(cid)
        _afirma(ruta_m is not None and ruta_m.name == f"M-{cid}__v1_3.json", caso,
                f"el M vivo de {cid} deberia ser __v1_3, resolvio {ruta_m}")


# ── 7 · GEN2-E3-1 · READINESS-DEL-RUNNER (P1-P6, catorce casos) ────────────

_ID_MANIFIESTO_REAL = "encig23_base_datos_csv"  # entrada real con payload,
# usada solo para RESOLUCION (nunca abre el archivo -- data/raw no existe
# en este entorno de prueba; el estado esperado es AUSENTE).


def t_sellado_no_sobrescribe():
    """T-SELLADO-NO-SOBRESCRIBE. P4: un CALC sellado no se reescribe. Es el
    UNICO de los catorce que invoca `run()` completo -- la inmutabilidad se
    decide ANTES de llamar a `preflight`, asi que no le afecta que este
    entorno de prueba nunca pueda dejarlo VERDE."""
    caso = "T-SELLADO-NO-SOBRESCRIBE"
    with _calc_temporal(dict(_SPEC_BASE)) as (d, cid):
        C._escribe_json(d / "ejecucion.json", {"marca": "original"})
        C._escribe_json(d / "resultados.json", {"spec_id": cid, "resultados": {}})
        sello = {"ejecucion.json": C._sha256_archivo(d / "ejecucion.json"),
                 "resultados.json": C._sha256_archivo(d / "resultados.json")}
        C._escribe_json(d / "sello.json", sello)
        subprocess.run([sys.executable, str(C.SELLA_PY), str(d / "sello.json")],
                       check=True, capture_output=True)
        antes = {p.name: p.read_bytes() for p in d.iterdir()}
        r, salida = _silencioso(C.run, cid)
        despues = {p.name: p.read_bytes() for p in d.iterdir()}
    _afirma(r["veredicto"] == "CALC-INMUTABLE", caso, f"veredicto={r['veredicto']}")
    _afirma("YA-SELLADO" in salida, caso, f"no imprimio YA-SELLADO: {salida!r}")
    _afirma(antes == despues, caso, "los bytes del CALC cambiaron pese al sello valido")


def t_manifiesto_ausente_bloquea():
    """T-MANIFIESTO-AUSENTE-BLOQUEA. Un input `origen: manifiesto` cuyo id
    no existe en `data/manifiesto.yaml` resuelve AUSENTE y bloquea preflight
    -- `preflight` VERDE solo si TODOS los inputs activos estan COINCIDE."""
    caso = "T-MANIFIESTO-AUSENTE-BLOQUEA"
    spec = dict(_SPEC_BASE, inputs=[{"id": "IN-NO-EXISTE-ZZZ-TEST", "origen": "manifiesto"}])
    r, _s = _preflight_de(spec)
    _afirma(any(b == "input_manifiesto_AUSENTE=IN-NO-EXISTE-ZZZ-TEST" for b in r["bloqueos"]),
            caso, f"no bloqueo por payload ausente: {r['bloqueos']}")
    _afirma(r["veredicto"] == "BLOQUEADO", caso, "veredicto no fue BLOQUEADO")


def t_manifiesto_ruta_al_medidor():
    """T-MANIFIESTO-RUTA-AL-MEDIDOR. El objeto que resolvio el payload
    (P1) alimenta al medidor: `ruta_absoluta`/`raiz_logica` viajan, ningun
    medidor busca su propio archivo por su cuenta."""
    caso = "T-MANIFIESTO-RUTA-AL-MEDIDOR"
    spec = {"inputs": [{"id": _ID_MANIFIESTO_REAL, "origen": "manifiesto"}]}
    # P1 (GEN2-E3-1-1): el medidor recibe el SNAPSHOT ya resuelto; ya no
    # existe una firma que le permita resolver por su cuenta.
    inputs = C._inputs_para_medidor(spec, C._resuelve_inputs(spec))
    _afirma(_ID_MANIFIESTO_REAL in inputs, caso, "el input no llego al medidor")
    entrada = inputs[_ID_MANIFIESTO_REAL]
    _afirma(bool(entrada.get("ruta_absoluta")), caso,
            f"ruta_absoluta vacia -- el medidor no sabe donde esta su input: {entrada}")
    _afirma(entrada.get("raiz_logica") == "data_raw", caso,
            f"raiz_logica inesperada: {entrada.get('raiz_logica')!r}")


def t_sha_manifiesto_congelado():
    """T-SHA-MANIFIESTO-CONGELADO. `ejecucion.json.input_sha256[id]` se
    rellena del MISMO objeto que resolvio el payload -- nunca vacio, nunca
    tecleado."""
    caso = "T-SHA-MANIFIESTO-CONGELADO"
    spec = {"inputs": [{"id": _ID_MANIFIESTO_REAL, "origen": "manifiesto"}]}
    detalle = C._resuelve_inputs(spec)
    ent = next((e for e in detalle if e["id"] == _ID_MANIFIESTO_REAL), None)
    _afirma(ent is not None, caso, "el input no aparece en el detalle de preflight")
    r = C._PR.resolver_payload(_ID_MANIFIESTO_REAL)
    esperado = r["sha256_actual"] or r["sha256_esperado"]
    _afirma(bool(esperado), caso, "la entrada real del manifiesto no trae sha256 -- fixture rota")
    _afirma(ent["sha256"] == esperado, caso,
            f"sha256 no viene de resolver_payload: {ent['sha256']!r} vs {esperado!r}")


def t_spec_yaml_sellada():
    """T-SPEC-YAML-SELLADA. `ejecucion.json` trae `spec_yaml_sha256` y
    `spec_md_sha256` reales (nunca copiados de la spec); `sello.json` cubre
    `spec.yaml` (ademas de `ejecucion.json`/`resultados.json`)."""
    caso = "T-SPEC-YAML-SELLADA"
    with _calc_temporal(dict(_SPEC_BASE)) as (d, cid):
        pre = _silencioso(C.preflight, cid)[0]
        ejec = C._construye_ejecucion(cid, dict(_SPEC_BASE), d, pre, "deadbeef",
                                      {"RESULT-A": 1, "RESULT-B": 2}, 0, "")
        _afirma(ejec["spec_yaml_sha256"] == _sha(d / "spec.yaml"), caso,
                "spec_yaml_sha256 no coincide con el archivo real")
        _afirma(ejec["spec_md_sha256"] == _sha(d / "spec.md"), caso,
                "spec_md_sha256 no coincide con el archivo real")
        C._escribe_json(d / "ejecucion.json", ejec)
        C._escribe_json(d / "resultados.json",
                        {"spec_id": cid, "resultados": {"RESULT-A": 1, "RESULT-B": 2}})
        sello = C._construye_sello(d, dict(_SPEC_BASE))
    _afirma("spec.yaml" in sello, caso, f"sello no cubre spec.yaml: {sorted(sello)}")
    _afirma("ejecucion.json" in sello and "resultados.json" in sello, caso,
            f"sello incompleto: {sorted(sello)}")


def t_seed_llega_al_medidor():
    """T-SEED-LLEGA-AL-MEDIDOR. El medidor recibe `contrato["seed"]["valor"]`
    -- retrocompatible con un `seed` suelto (formato de `CALC-SMOKE-0001`,
    que este acto no toca)."""
    caso = "T-SEED-LLEGA-AL-MEDIDOR"
    _afirma(C.contrato_ejecutable({"seed": 42})["seed"] == {"aplica": True, "valor": 42},
            caso, "un seed suelto (retrocompat) no se normalizo")
    contrato_explicito = {"aplica": True, "valor": 7, "rng": "numpy.PCG64"}
    _afirma(C.contrato_ejecutable({"seed": contrato_explicito})["seed"] == contrato_explicito,
            caso, "un seed ya en forma de contrato se reescribio")

    tmp = Path(tempfile.mkdtemp(prefix="med-seed-"))
    try:
        s = tmp / "medidor_seed.py"
        s.write_text("def medir(inputs, contrato):\n"
                      "    return {'RESULT-SEED': contrato['seed']['valor']}\n",
                      encoding="utf-8")
        rel = os.path.relpath(s, RAIZ)
        spec = {"script": rel, "seed": 99, "inputs": []}
        valores, code, err = C._ejecuta(spec, C._resuelve_inputs(spec))
        _afirma(code == 0, caso, f"medidor revento: {err}")
        _afirma(valores.get("RESULT-SEED") == 99, caso,
                f"el seed no llego al medidor via el contrato: {valores}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def t_seed_no_aplica():
    """T-SEED-NO-APLICA. `seed: {aplica: false}` es una declaracion valida
    -- no se inventan semillas para calculos deterministas, y no bloquea
    preflight (a diferencia de `seed` ausente/null)."""
    caso = "T-SEED-NO-APLICA"
    _afirma(C.contrato_ejecutable({"seed": {"aplica": False}})["seed"] == {"aplica": False},
            caso, "aplica:false no se preservo")
    spec = dict(_SPEC_BASE, seed={"aplica": False})
    r, _s = _preflight_de(spec)
    _afirma("seed_no_declarado" not in r["bloqueos"], caso,
            f"aplica:false bloqueo como si no hubiera seed: {r['bloqueos']}")
    _afirma(not any(b.startswith("seed_") for b in r["bloqueos"]), caso,
            f"aplica:false disparo un bloqueo de seed: {r['bloqueos']}")


def t_outputs_exactos():
    """T-OUTPUTS-EXACTOS. `set(resultado.keys()) == set(outputs_declarados)`
    EXACTO -- ni faltan, ni sobran."""
    caso = "T-OUTPUTS-EXACTOS"
    spec = {"resultados": [{"id": "RESULT-A", "tipo": "entero", "unidad": "u"},
                           {"id": "RESULT-B", "tipo": "entero", "unidad": "u"}]}
    completo = C._valida_outputs(spec, {"RESULT-A": 1, "RESULT-B": 2})
    _afirma(completo == [], caso, f"outputs exactos y validos dieron problemas: {completo}")

    faltante = C._valida_outputs(spec, {"RESULT-A": 1})
    _afirma(any("outputs_faltantes" in p for p in faltante), caso,
            f"un output faltante no se detecto: {faltante}")

    sobrante = C._valida_outputs(spec, {"RESULT-A": 1, "RESULT-B": 2, "RESULT-999": 3})
    _afirma(any("outputs_no_declarados" in p for p in sobrante), caso,
            f"un RESULT-999 no declarado no se detecto: {sobrante}")


def t_tipo_result():
    """T-TIPO-RESULT. Cada output declara `tipo` y se valida: finitud,
    rango de `proporcion`, y el tipo de Python que corresponde."""
    caso = "T-TIPO-RESULT"

    def _un_output(tipo, unidad="u", **extra):
        return {"resultados": [dict({"id": "RESULT-X", "tipo": tipo, "unidad": unidad}, **extra)]}

    _afirma(C._valida_outputs(_un_output("entero"), {"RESULT-X": 3}) == [], caso,
            "entero valido reporto problema")
    _afirma(C._valida_outputs(_un_output("entero"), {"RESULT-X": 3.5}) != [], caso,
            "un flotante paso como entero")
    _afirma(C._valida_outputs(_un_output("flotante"), {"RESULT-X": 1.5}) == [], caso,
            "flotante valido reporto problema")
    _afirma(C._valida_outputs(_un_output("flotante"), {"RESULT-X": float("nan")}) != [], caso,
            "NaN paso como flotante valido")
    _afirma(C._valida_outputs(_un_output("flotante"), {"RESULT-X": float("inf")}) != [], caso,
            "infinito paso como flotante valido")
    _afirma(C._valida_outputs(_un_output("proporcion"), {"RESULT-X": 0.5}) == [], caso,
            "proporcion valida reporto problema")
    _afirma(C._valida_outputs(_un_output("proporcion"), {"RESULT-X": 1.5}) != [], caso,
            "proporcion fuera de [0,1] paso")
    _afirma(C._valida_outputs(_un_output("texto"), {"RESULT-X": "ok"}) == [], caso,
            "texto valido reporto problema")
    _afirma(C._valida_outputs(_un_output("texto"), {"RESULT-X": 3}) != [], caso,
            "un entero paso como texto")
    _afirma(C._valida_outputs(_un_output("entero", permite_no_estimable=True),
                              {"RESULT-X": None}) == [], caso,
            "null con permite_no_estimable=true deberia pasar")
    _afirma(C._valida_outputs(_un_output("entero"), {"RESULT-X": None}) != [], caso,
            "null sin permite_no_estimable paso")


def t_run_fallo_no_sella():
    """T-RUN-FALLO-NO-SELLA. Fallo antes de outputs validos -> ningun
    archivo se escribe. `_fallas_run` es el guard que `run()` consulta
    antes de escribir cualquier cosa."""
    caso = "T-RUN-FALLO-NO-SELLA"
    _afirma(C._fallas_run({}, {}, 1, "boom") == ["medidor_fallo:boom"], caso,
            "un medidor que revento no se marco como fallo")
    spec = {"resultados": [{"id": "R", "tipo": "entero", "unidad": "u"}]}
    _afirma(C._fallas_run(spec, {"R": 1}, 0, "") == [], caso,
            "outputs validos con exit_code=0 no deberian fallar")
    _afirma(C._fallas_run(spec, {}, 0, "") != [], caso,
            "outputs faltantes con exit_code=0 deberian fallar igual")


def t_verify_valida_sello():
    """T-VERIFY-VALIDA-SELLO. `_verifica_sello` valida el sidecar Y que
    cada archivo que `sello.json` declara cubrir siga coincidiendo -- un
    `sello.json` reescrito a mano con hashes frescos no basta."""
    caso = "T-VERIFY-VALIDA-SELLO"
    tmp = Path(tempfile.mkdtemp(prefix="sello-test-"))
    try:
        (tmp / "ejecucion.json").write_text('{"a": 1}\n', encoding="utf-8")
        (tmp / "resultados.json").write_text('{"b": 2}\n', encoding="utf-8")
        sello = {"ejecucion.json": C._sha256_archivo(tmp / "ejecucion.json"),
                 "resultados.json": C._sha256_archivo(tmp / "resultados.json")}
        C._escribe_json(tmp / "sello.json", sello)
        subprocess.run([sys.executable, str(C.SELLA_PY), str(tmp / "sello.json")],
                       check=True, capture_output=True)
        estado_ok, _r = C._verifica_sello(tmp)
        _afirma(estado_ok == "COINCIDE", caso, f"sello valido reporto {estado_ok}")

        (tmp / "ejecucion.json").write_text('{"a": 999}\n', encoding="utf-8")
        estado_alterado, razon = C._verifica_sello(tmp)
        _afirma(estado_alterado == "NO-COINCIDE", caso,
                f"un archivo cubierto alterado sin re-sellar dio {estado_alterado}")
        _afirma("ejecucion.json" in razon, caso, f"la razon no nombra el archivo: {razon}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    tmp2 = Path(tempfile.mkdtemp(prefix="sello-ausente-"))
    try:
        estado_ausente, _r = C._verifica_sello(tmp2)
        _afirma(estado_ausente == "AUSENTE", caso,
                f"sin sello.sha256 deberia ser AUSENTE, fue {estado_ausente}")
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)


def _construye_calc_sellado(d: Path, cid: str, parametros_spec, parametros_ejec, seed=42):
    """Un CALC REAL -- medidor.py DENTRO del CALC, spec.yaml apuntando a el,
    sello completo -- para ejercer `verify()` de punta a punta sin pasar por
    `preflight` (que `verify` no llama). `parametros_ejec` puede declarar,
    a proposito, un valor DISTINTO al de `parametros_spec` -- asi se simula
    una corrida sellada bajo parametros que la spec ya no trae."""
    import yaml
    medidor = d / "medidor.py"
    medidor.write_text("def medir(inputs, contrato):\n    return {'RESULT-X': 1}\n",
                       encoding="utf-8")
    spec = dict(_SPEC_BASE, calc_id=cid, script=os.path.relpath(medidor, RAIZ),
               parametros=parametros_spec, seed=seed,
               resultados=[{"id": "RESULT-X", "tipo": "entero", "unidad": "u"}])
    spec["spec_md_sha256"] = _sha(d / "spec.md")
    (d / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")

    _cod, commit = C._git_salida("rev-parse", "HEAD")
    ejec = {
        "git_commit": commit.strip(), "script_path": spec["script"],
        "script_blob_sha256": C._sha256_archivo(medidor),
        "spec_yaml_sha256": C._sha256_archivo(d / "spec.yaml"),
        "spec_md_sha256": spec["spec_md_sha256"],
        "input_ids": [], "input_sha256": {},
        "parametros": parametros_ejec, "seed": seed,
        "dependencias_materiales_calc": C._dependencias_materiales_calc(spec),
    }
    C._escribe_json(d / "ejecucion.json", ejec)
    C._escribe_json(d / "resultados.json", {"spec_id": cid, "resultados": {"RESULT-X": 1}})
    sello = C._construye_sello(d, spec)
    C._escribe_json(d / "sello.json", sello)
    subprocess.run([sys.executable, str(C.SELLA_PY), str(d / "sello.json")],
                   check=True, capture_output=True)
    return spec, ejec


def t_verify_contexto():
    """T-VERIFY-CONTEXTO. `CONTEXTO ∈ {IDENTICO, DISTINTO, NO-VERIFICABLE}`
    con razon -- aqui, identico cuando la spec y el recibo coinciden, y
    DISTINTO (con `parametros_distintos` en la razon) cuando la corrida
    sellada quedo bajo parametros que la spec ya no trae."""
    caso = "T-VERIFY-CONTEXTO"
    with _calc_temporal(dict(_SPEC_BASE, calc_id="CALC-TEST-CTX-A")) as (d, cid):
        spec, ejec = _construye_calc_sellado(d, cid, {"a": 1}, {"a": 1})
        contexto, razones = C._evalua_contexto(d, spec, ejec)
    _afirma(contexto == "IDENTICO", caso, f"contexto={contexto} razones={razones}")

    with _calc_temporal(dict(_SPEC_BASE, calc_id="CALC-TEST-CTX-B")) as (d, cid):
        spec, ejec = _construye_calc_sellado(d, cid, {"a": 1}, {"a": 999})
        contexto2, razones2 = C._evalua_contexto(d, spec, ejec)
    _afirma(contexto2 == "DISTINTO", caso, f"contexto={contexto2} razones={razones2}")
    _afirma("parametros_distintos" in razones2, caso, f"razones={razones2}")


def _listado_canonico(d: Path) -> list[str]:
    """Nombres de archivo en `d`, excluyendo `__pycache__` -- efecto
    colateral del propio interprete al importar `medidor.py` via
    `importlib` (ni un artefacto canonico de `corrida0`, ni algo que
    `verify` decida escribir)."""
    return sorted(p.name for p in d.iterdir() if p.name != "__pycache__")


def t_verify_no_escribe():
    """T-VERIFY-NO-ESCRIBE. `verify` no escribe ningun artefacto canonico
    -- ni con corrida sellada ni sin ella."""
    caso = "T-VERIFY-NO-ESCRIBE"
    with _calc_temporal(dict(_SPEC_BASE, calc_id="CALC-TEST-NOESCRIBE-1")) as (d, cid):
        antes = _listado_canonico(d)
        _silencioso(C.verify, cid)
        despues = _listado_canonico(d)
    _afirma(antes == despues, caso,
            f"verify escribio sin corrida sellada: antes={antes} despues={despues}")

    with _calc_temporal(dict(_SPEC_BASE, calc_id="CALC-TEST-NOESCRIBE-2")) as (d, cid):
        _construye_calc_sellado(d, cid, {"a": 1}, {"a": 1})
        antes = _listado_canonico(d)
        _silencioso(C.verify, cid)
        despues = _listado_canonico(d)
    _afirma(antes == despues, caso,
            f"verify escribio con corrida sellada: antes={antes} despues={despues}")


def t_entorno_una_vez():
    """T-ENTORNO-UNA-VEZ. `_firma_entorno()` se llama UNA sola vez por
    construccion de `ejecucion.json` -- antes se llamaba dos (una para
    `dependencias_materiales`, otra para `firma_entorno`)."""
    caso = "T-ENTORNO-UNA-VEZ"
    llamadas = []
    original = C._firma_entorno

    def _contador():
        llamadas.append(1)
        return original()

    C._firma_entorno = _contador
    try:
        with _calc_temporal(dict(_SPEC_BASE)) as (d, cid):
            pre = _silencioso(C.preflight, cid)[0]
            C._construye_ejecucion(cid, dict(_SPEC_BASE), d, pre, "deadbeef",
                                   {"RESULT-A": 1, "RESULT-B": 2}, 0, "")
    finally:
        C._firma_entorno = original
    _afirma(len(llamadas) == 1, caso,
            f"_firma_entorno se llamo {len(llamadas)} veces, se esperaba 1")


# ══════════ ACTO GEN2-E3-1-1 · CABLEADO-FINAL-DEL-RUNNER (P5) ═════════════
# Cuatro casos, uno por cada uno de los cuatro defectos materiales que el
# acto cierra. No se anaden casos para anomalias que no protejan a uno de
# esos cuatro.

# Una spec del ESQUEMA ENDURECIDO: declara TODA dimension sustantiva. Es lo
# que P2 exige a cualquier CALC nuevo, y la base de los casos de abajo.
_SPEC_ENDURECIDA = {
    "calc_id": "CALC-TEST-DURA", "spec_md": "spec.md", "spec_md_sha256": "",
    "script": "tools/entorno.py",
    "inputs": [], "variables": [], "universo": "NO-APLICA",
    "filtros": "NO-APLICA", "ponderador": "NO-APLICA",
    "transformacion": "NO-APLICA", "estimando": "NO-APLICA",
    "parametros": {"a": 1}, "seed": {"aplica": False},
    "dependencias_materiales": [],
    "tolerancia": {"tipo": "flotante", "abs": 1e-10},
    "resultados": [{"id": "RESULT-A", "tipo": "entero", "unidad": "u"}],
}


def t_snapshot_input_unico():
    """T-SNAPSHOT-INPUT-UNICO (D1). El payload se resuelve UNA sola vez por
    input y por intento de corrida, y ese MISMO sha/ruta llega al medidor y a
    `ejecucion.json`.

    El mock devuelve A en la primera llamada y B en la segunda a proposito:
    si existiera una segunda resolucion, el medidor mediria B mientras el
    recibo registraria A -- que es literalmente el defecto D1. El test afirma
    que la segunda llamada NO EXISTE."""
    caso = "T-SNAPSHOT-INPUT-UNICO"
    iid = "IN-FALSO-SNAPSHOT"
    llamadas = []
    respuestas = [
        {"id": iid, "raiz_logica": "data_raw", "ruta_absoluta": "/ruta/A",
         "sha256_esperado": "aaa", "sha256_actual": "aaa", "tamano": 1,
         "estado": "COINCIDE"},
        {"id": iid, "raiz_logica": "data_raw", "ruta_absoluta": "/ruta/B",
         "sha256_esperado": "bbb", "sha256_actual": "bbb", "tamano": 2,
         "estado": "COINCIDE"},
    ]

    def _mock(payload_id, **kw):
        llamadas.append(payload_id)
        return respuestas[min(len(llamadas) - 1, len(respuestas) - 1)]

    original = C._PR.resolver_payload
    C._PR.resolver_payload = _mock
    try:
        spec = dict(_SPEC_ENDURECIDA, calc_id="CALC-TEST-SNAP",
                    inputs=[{"id": iid, "origen": "manifiesto"}])
        with _calc_temporal(spec) as (d, cid):
            import yaml
            spec = dict(spec, spec_md_sha256=_sha(d / "spec.md"))
            (d / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True),
                                         encoding="utf-8")
            pre = _silencioso(C.preflight, cid)[0]
            n_tras_preflight = len(llamadas)
            inputs_medidor = C._inputs_para_medidor(spec, pre["inputs_resueltos"])
            ejec = C._construye_ejecucion(cid, spec, d, pre, "deadbeef",
                                          {"RESULT-A": 1}, 0, "")
    finally:
        C._PR.resolver_payload = original

    _afirma(n_tras_preflight == 1, caso,
            f"preflight resolvio el payload {n_tras_preflight} veces, se esperaba 1")
    _afirma(len(llamadas) == 1, caso,
            f"hubo una segunda resolucion tras preflight: {len(llamadas)} llamadas "
            f"-- el medidor y el recibo pueden discordar (defecto D1)")
    _afirma(pre["inputs_resueltos"][0]["sha256"] == "aaa", caso,
            f"snapshot de preflight: {pre['inputs_resueltos'][0]}")
    _afirma(inputs_medidor[iid]["sha256"] == "aaa"
            and inputs_medidor[iid]["ruta_absoluta"] == "/ruta/A", caso,
            f"al medidor no llego el snapshot de preflight: {inputs_medidor[iid]}")
    _afirma(ejec["input_sha256"][iid] == "aaa", caso,
            f"ejecucion.json no salio del mismo snapshot: {ejec['input_sha256']}")


def t_snapshot_repo_trae_los_bytes():
    """T-SNAPSHOT-INPUT-UNICO (D1, cara `origen: repo`). Para un insumo
    versionado el snapshot se queda con los MISMOS bytes que el SHA
    verificado identifica -- el medidor no reabre el archivo."""
    caso = "T-SNAPSHOT-INPUT-UNICO/repo"
    ruta_rel = "tools/entorno.py"
    spec = {"inputs": [{"id": "IN-ENTORNO", "origen": "repo", "ruta": ruta_rel,
                        "sha256": _sha(RAIZ / ruta_rel)}]}
    snapshot = C._resuelve_inputs(spec)
    ent = snapshot[0]
    _afirma(ent["estado"] == "COINCIDE", caso, f"estado={ent['estado']}")
    _afirma(ent["bytes"] == (RAIZ / ruta_rel).read_bytes(), caso,
            "el snapshot no trae los bytes del insumo versionado")
    import hashlib as _h
    _afirma(_h.sha256(ent["bytes"]).hexdigest() == ent["sha256"], caso,
            "los bytes del snapshot no son los que su sha256 identifica")
    _afirma(C._inputs_para_medidor(spec, snapshot)["IN-ENTORNO"]["bytes"]
            == ent["bytes"], caso, "los bytes no llegaron al medidor")


def t_spec_no_aplica_explicito():
    """T-SPEC-NO-APLICA-EXPLICITO (D2). `ponderador: NO-APLICA` es una
    declaracion valida; `ponderador` AUSENTE es un campo olvidado y bloquea.
    Antes de este acto ambos casos eran indistinguibles: el runner rellenaba
    con `"NO-APLICA"` por omision.

    El bloqueo se comprueba dimension por dimension en un solo bucle -- el
    mecanismo es uno (`DIMENSIONES_SUSTANTIVAS`), no un test por campo."""
    caso = "T-SPEC-NO-APLICA-EXPLICITO"
    r, _s = _preflight_de(dict(_SPEC_ENDURECIDA))
    _afirma(not any(b.startswith("campo_sustantivo_ausente") for b in r["bloqueos"]),
            caso, f"una spec que declara TODO bloqueo igual: {r['bloqueos']}")

    for campo in C.DIMENSIONES_SUSTANTIVAS:
        spec = {k: v for k, v in _SPEC_ENDURECIDA.items() if k != campo}
        r, _s = _preflight_de(spec)
        _afirma(f"campo_sustantivo_ausente={campo}" in r["bloqueos"], caso,
                f"`{campo}` ausente no bloqueo: {r['bloqueos']}")

    # `NO-APLICA` DECLARADO y `[]` DECLARADO son ambos declaraciones validas.
    r, _s = _preflight_de(dict(_SPEC_ENDURECIDA, ponderador="NO-APLICA",
                               variables=[], dependencias_materiales=[]))
    _afirma(not any(b.startswith("campo_sustantivo_ausente") for b in r["bloqueos"]),
            caso, f"un vacio DECLARADO se leyo como ausente: {r['bloqueos']}")

    # El esquema legado (las dos specs selladas) queda exento por su propia
    # etiqueta, no por olvido.
    legado = {k: v for k, v in _SPEC_ENDURECIDA.items() if k != "ponderador"}
    legado["etiquetas"] = {"generacion": C.GENERACION_LEGADO}
    r, _s = _preflight_de(legado)
    _afirma(not any(b.startswith("campo_sustantivo_ausente") for b in r["bloqueos"]),
            caso, f"el esquema LEGACY-GEN1 se endurecio: {r['bloqueos']}")


def t_seed_rng_obligatorio():
    """T-SPEC-NO-APLICA-EXPLICITO (D2, cara `seed`). `aplica: true` exige
    `valor` Y `rng`. No se inventa un RNG por omision."""
    caso = "T-SEED-RNG-OBLIGATORIO"
    r, _s = _preflight_de(dict(_SPEC_ENDURECIDA, seed={"aplica": True, "valor": 42}))
    _afirma("seed_aplica_sin_rng" in r["bloqueos"], caso,
            f"`aplica: true` sin `rng` no bloqueo: {r['bloqueos']}")

    r, _s = _preflight_de(dict(_SPEC_ENDURECIDA, seed={"aplica": True,
                                                       "rng": "numpy.PCG64"}))
    _afirma("seed_aplica_sin_valor" in r["bloqueos"], caso,
            f"`aplica: true` sin `valor` no bloqueo: {r['bloqueos']}")

    completo = {"aplica": True, "valor": 42, "rng": "numpy.PCG64"}
    r, _s = _preflight_de(dict(_SPEC_ENDURECIDA, seed=completo))
    _afirma(not any(b.startswith("seed_") for b in r["bloqueos"]), caso,
            f"un seed completo bloqueo: {r['bloqueos']}")

    # `{aplica: false}` sigue siendo declaracion valida (no exige rng).
    r, _s = _preflight_de(dict(_SPEC_ENDURECIDA, seed={"aplica": False}))
    _afirma(not any(b.startswith("seed_") for b in r["bloqueos"]), caso,
            f"`aplica: false` bloqueo: {r['bloqueos']}")


def t_preflight_valida_schema_de_resultados():
    """T-SPEC-NO-APLICA-EXPLICITO (D2, cara `resultados`). ANTES de abrir
    microdato, `preflight` valida la DECLARACION de outputs: id no vacio,
    tipo permitido, unidad no vacia, `permite_no_estimable` booleano."""
    caso = "T-PREFLIGHT-SCHEMA-RESULTADOS"
    for res, esperado in (
            ([{"id": "", "tipo": "entero", "unidad": "u"}], "resultado_sin_id"),
            ([{"id": "RESULT-A", "tipo": "raro", "unidad": "u"}],
             "resultado_tipo_invalido"),
            ([{"id": "RESULT-A", "tipo": "entero"}], "resultado_sin_unidad"),
            ([{"id": "RESULT-A", "tipo": "entero", "unidad": "u",
               "permite_no_estimable": "si"}],
             "resultado_permite_no_estimable_no_booleano")):
        r, _s = _preflight_de(dict(_SPEC_ENDURECIDA, resultados=res))
        _afirma(any(b.startswith(esperado) for b in r["bloqueos"]), caso,
                f"{esperado} no bloqueo con resultados={res}: {r['bloqueos']}")

    r, _s = _preflight_de(dict(_SPEC_ENDURECIDA, resultados=[
        {"id": "RESULT-A", "tipo": "proporcion", "unidad": "p",
         "permite_no_estimable": True}]))
    _afirma(not any(b.startswith("resultado_") for b in r["bloqueos"]), caso,
            f"un schema de outputs valido bloqueo: {r['bloqueos']}")


def _calc_para_verify(d: Path, cid: str, resultados_decl, sellados, replay,
                      tolerancia):
    """Un CALC sellado cuyo medidor devuelve `replay` mientras el recibo trae
    `sellados` -- para ejercer el eje RESULTADO de `verify` sin corpus."""
    import yaml
    medidor = d / "medidor.py"
    medidor.write_text("def medir(inputs, contrato):\n"
                       f"    return {replay!r}\n", encoding="utf-8")
    spec = dict(_SPEC_ENDURECIDA, calc_id=cid,
                script=os.path.relpath(medidor, RAIZ),
                resultados=resultados_decl, tolerancia=tolerancia)
    spec["spec_md_sha256"] = _sha(d / "spec.md")
    (d / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True),
                                 encoding="utf-8")
    _cod, commit = C._git_salida("rev-parse", "HEAD")
    ejec = {"git_commit": commit.strip(), "script_path": spec["script"],
            "script_blob_sha256": C._sha256_archivo(medidor),
            "spec_yaml_sha256": C._sha256_archivo(d / "spec.yaml"),
            "spec_md_sha256": spec["spec_md_sha256"],
            "input_ids": [], "input_sha256": {},
            "parametros": spec["parametros"], "seed": spec["seed"],
            "dependencias_materiales_calc": C._dependencias_materiales_calc(spec)}
    C._escribe_json(d / "ejecucion.json", ejec)
    C._escribe_json(d / "resultados.json", {"spec_id": cid, "resultados": sellados})
    C._escribe_json(d / "sello.json", C._construye_sello(d, spec))
    subprocess.run([sys.executable, str(C.SELLA_PY), str(d / "sello.json")],
                   check=True, capture_output=True)
    return spec


def t_verify_tipo_por_result():
    """T-VERIFY-TIPO-POR-RESULT (D3). Con `tolerancia: {tipo: flotante, abs:
    1e-10}` GLOBAL y un RESULT declarado `entero`, un replay que devuelve
    `1.0` contra un `1` sellado NO reproduce: el tipo autoritativo es el del
    RESULT, no el de la tolerancia. Antes de este acto `_compara` leia
    `tolerancia["tipo"]`, caia en la rama numerica y `1.0 == 1` dentro de
    1e-10 reproducia -- el cambio de tipo quedaba invisible."""
    caso = "T-VERIFY-TIPO-POR-RESULT"
    tol = {"tipo": "flotante", "abs": 1e-10}

    # (a) entero declarado, replay flotante -> NO reproduce.
    with _calc_temporal(dict(_SPEC_ENDURECIDA, calc_id="CALC-TEST-TIPO-N")) as (d, cid):
        _calc_para_verify(d, cid,
                          [{"id": "RESULT-N", "tipo": "entero", "unidad": "u"}],
                          {"RESULT-N": 1}, {"RESULT-N": 1.0}, tol)
        r = _silencioso(C.verify, cid)[0]
    _afirma(r["resultado"] != "REPRODUCE", caso,
            f"1.0 contra 1 sellado reprodujo como entero valido: {r}")

    # El comparador, aislado: la tolerancia global no puede decidir el tipo.
    ok, _delta = C._compara_result(1, 1.0, {"tipo": "entero"}, tol)
    _afirma(not ok, caso, "_compara_result acepto 1.0 para un RESULT `entero`")
    ok_viejo, _d = C._compara(1, 1.0, tol)
    _afirma(ok_viejo, caso,
            "premisa del caso rota: el comparador global ya no aceptaba 1.0 "
            "-- si esto falla, el defecto D3 se corrigio en otro sitio")

    # (b) flotante DENTRO de tolerancia -> si reproduce.
    with _calc_temporal(dict(_SPEC_ENDURECIDA, calc_id="CALC-TEST-TIPO-F")) as (d, cid):
        _calc_para_verify(d, cid,
                          [{"id": "RESULT-F", "tipo": "flotante", "unidad": "z"}],
                          {"RESULT-F": 1.0}, {"RESULT-F": 1.0 + 1e-15}, tol)
        r = _silencioso(C.verify, cid)[0]
    _afirma(r["resultado"] == "REPRODUCE", caso,
            f"un flotante dentro de tolerancia no reprodujo: {r}")

    # (c) los outputs del REPLAY pasan `_valida_outputs` antes de comparar:
    # una proporcion fuera de [0,1] es NO-EJECUTABLE, nunca REPRODUCE.
    with _calc_temporal(dict(_SPEC_ENDURECIDA, calc_id="CALC-TEST-TIPO-P")) as (d, cid):
        _calc_para_verify(d, cid,
                          [{"id": "RESULT-P", "tipo": "proporcion", "unidad": "p"}],
                          {"RESULT-P": 7.0}, {"RESULT-P": 7.0}, tol)
        r = _silencioso(C.verify, cid)[0]
    _afirma(r["resultado"] == "NO-EJECUTABLE", caso,
            f"un replay que viola el contrato no fue NO-EJECUTABLE: {r}")
    _afirma(r["veredicto"] != "REPRODUCE", caso,
            f"veredicto REPRODUCE sobre outputs invalidos: {r['veredicto']}")
    _afirma(any("proporcion_fuera_de_rango" in pb for pb in r["problemas_replay"]),
            caso, f"no se reporto el problema del replay: {r['problemas_replay']}")


def t_sellador_falla_no_ejecutado():
    """T-SELLADOR-FALLA-NO-EJECUTADO (D4). Medidor OK + outputs OK +
    `sella_sha256.py` con `returncode != 0` -> el veredicto NO puede ser
    `EJECUTADO`, y el CALC no queda sellado ni inmutable. Antes de este acto
    el veredicto salia del `exit_code` del MEDIDOR y el del sellador se
    imprimia sin consecuencia."""
    caso = "T-SELLADOR-FALLA-NO-EJECUTADO"
    original = subprocess.run

    class _Falla:
        returncode, stdout, stderr = 3, "", "sellador simulado: fallo"

    def _run_mock(cmd, *a, **kw):
        # solo el sellador cuando SELLA (no cuando --verifica): todo lo demas
        # (git, entorno) corre de verdad.
        if (len(cmd) > 1 and str(cmd[1]) == str(C.SELLA_PY)
                and "--verifica" not in [str(x) for x in cmd]):
            return _Falla()
        return original(cmd, *a, **kw)

    with _calc_temporal(dict(_SPEC_ENDURECIDA, calc_id="CALC-TEST-SELLO")) as (d, cid):
        medidor = d / "medidor.py"
        medidor.write_text("def medir(inputs, contrato):\n"
                           "    return {'RESULT-A': 1}\n", encoding="utf-8")
        import yaml
        spec = dict(_SPEC_ENDURECIDA, calc_id=cid,
                    script=os.path.relpath(medidor, RAIZ),
                    spec_md_sha256=_sha(d / "spec.md"))
        (d / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True),
                                     encoding="utf-8")
        # `preflight` no puede quedar VERDE con un fixture fuera del repo
        # (arbol sucio, spec.yaml no commiteado), asi que se ejerce `run` a
        # partir del punto que este caso mide: el tramo posterior al medidor.
        pre = _silencioso(C.preflight, cid)[0]
        pre["veredicto"] = "VERDE"
        original_pre = C.preflight
        C.preflight = lambda calc_id, imprime=True: pre
        C.subprocess.run = _run_mock
        try:
            r = _silencioso(C.run, cid)[0]
        finally:
            C.preflight = original_pre
            C.subprocess.run = original
        _afirma(r["veredicto"] != "EJECUTADO", caso,
                f"veredicto EJECUTADO con el sellador en fallo: {r['veredicto']}")
        _afirma(r["veredicto"] == "FALLO-SELLADO", caso,
                f"veredicto inesperado: {r['veredicto']}")
        _afirma(not C._calc_ya_sellado(d), caso,
                "el CALC quedo sellado/inmutable pese al fallo del sellador")


# ── ACTO GEN2-E6 · AUTOMATIZA-GEN2-2: `registro` y `status` ───────────────
#
# Punta a punta sobre FIXTURES, no sobre `data/corrida0/`: la demanda, la
# oferta y hasta el `tramite.yaml` que declara `corrida0_resultado_id` viven
# en un temporal, y `corrida0` se re-apunta ahi. Dos consecuencias que el
# encargo pide explicitamente: estos casos NO exigen arbol limpio (no pasan
# por `preflight`) y no escriben una sola linea en el arbol de verdad.

_SPEC_REGISTRO_BASE = {
    "spec_md": "spec.md",
    "inputs": [],
    "parametros": {"a": 1},
    "seed": {"aplica": False},
    "tolerancia": {"tipo": "flotante", "abs": 1.0e-10},
}


def _fila_demanda(rid: str, consumidor: str, corrida: str, **kw) -> dict:
    fila = {c: C.NO_DECLARADO for c in C.COLS_RESULTADOS}
    fila.update({"resultado_id": rid, "consumidor": consumidor, "tipo": "conducta_p_medido",
                 "valor_legacy": "0.5", "receta_legacy": "OK", "depende_de": "",
                 "corrida_natural": corrida, "estado": "PENDIENTE",
                 "vigencia": "PENDIENTE", "validacion_independiente": "NO-HECHA"})
    fila.update(kw)
    return fila


def _fila_corrida(cid: str, rids: list[str], **kw) -> dict:
    fila = {c: C.NO_DECLARADO for c in C.COLS_CORRIDAS}
    fila.update({"corrida_id": cid, "instrumento": "FIXTURE", "payload_ids": "",
                 "medidor_o_spec_candidato": "SIN-RECETA", "n_resultados": len(rids),
                 "resultados_ids": ",".join(rids), "entorno_requerido": "NUBE",
                 "receta": "OK", "orden_causal": 1})
    fila.update(kw)
    return fila


def _sella_calc_fixture(d: Path, cid: str, valores: dict, etiquetas: dict,
                        decl_res=None, sin_sello=False, sin_hash=None,
                        repite_de=None) -> None:
    """Un CALC de fixture con su sello real (`sella_sha256.py`, no un sidecar
    escrito a mano). `sin_sello` deja `resultados.json` sin respaldo y
    `sin_hash` borra un campo del recibo -- las dos son las condiciones que
    `registro` debe atrapar, no adornos."""
    import yaml
    d.mkdir(parents=True, exist_ok=True)
    (d / "spec.md").write_text("# fixture\n", encoding="utf-8")
    medidor = d / "medidor.py"
    medidor.write_text("def medir(inputs, contrato):\n    return {}\n", encoding="utf-8")
    spec = dict(_SPEC_REGISTRO_BASE, calc_id=cid, etiquetas=etiquetas,
                script=os.path.relpath(medidor, RAIZ),
                resultados=decl_res or [{"id": r, "tipo": "flotante", "unidad": "u"}
                                        for r in valores])
    if repite_de:
        spec["repite_de"] = repite_de
    spec["spec_md_sha256"] = _sha(d / "spec.md")
    (d / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")
    ejec = {"corrida_id": f"{cid}--fixture", "spec_id": cid,
            "git_commit": "0" * 40, "script_path": spec["script"],
            "script_blob_sha256": C._sha256_archivo(medidor),
            "spec_yaml_sha256": C._sha256_archivo(d / "spec.yaml"),
            "input_ids": [], "input_sha256": {}, "exit_code": 0,
            "fecha": "2026-09-08T00:00:00Z", "parametros": spec["parametros"],
            "seed": spec["seed"], "resultado_ids": sorted(valores)}
    if sin_hash:
        ejec.pop(sin_hash, None)
    C._escribe_json(d / "ejecucion.json", ejec)
    C._escribe_json(d / "resultados.json", {"spec_id": cid, "resultados": valores})
    if sin_sello:
        return
    C._escribe_json(d / "sello.json", C._construye_sello(d, spec))
    subprocess.run([sys.executable, str(C.SELLA_PY), str(d / "sello.json")],
                   check=True, capture_output=True)


@contextlib.contextmanager
def _arbol_registro(res=None, corr=None, calcs=(), tramite=None, propuesta=None):
    """Monta demanda + oferta en un temporal y re-apunta `corrida0` ahi.
    Restaura SIEMPRE: ningun caso escribe en `data/corrida0/`."""
    import yaml
    tmp = Path(tempfile.mkdtemp(prefix="registro-test-"))
    previos = {k: getattr(C, k) for k in
               ("CORRIDAS", "DEMANDA_RESULTADOS", "DEMANDA_CORRIDAS",
                "NO_CORRIDO_TSV", "TRAMITE", "PROCEDENCIA", "PROPUESTA")}
    C.CORRIDAS = tmp
    C.DEMANDA_RESULTADOS = tmp / "demanda-resultados.tsv"
    C.DEMANDA_CORRIDAS = tmp / "demanda-corridas.tsv"
    C.NO_CORRIDO_TSV = tmp / "no-corrido.tsv"
    C.TRAMITE = tmp / "tramite.yaml"
    C.PROCEDENCIA = tmp / "procedencia-ausente.yaml"
    C.PROPUESTA = tmp / "propuesta-ausente.yaml"
    C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS, res or [])
    C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS, corr or [])
    C.TRAMITE.write_text(yaml.safe_dump(tramite or {"reglas": []},
                                        allow_unicode=True), encoding="utf-8")
    if propuesta is not None:
        C.PROPUESTA = tmp / "tramite-ola5-propuesta-v0.yaml"
        C.PROPUESTA.write_text(yaml.safe_dump(propuesta, allow_unicode=True),
                               encoding="utf-8")
    for c in calcs:
        _sella_calc_fixture(tmp / c["calc_id"], c["calc_id"], c.get("valores", {}),
                            c.get("etiquetas", {}), c.get("decl_res"),
                            c.get("sin_sello", False), c.get("sin_hash"),
                            c.get("repite_de"))
    try:
        yield tmp
    finally:
        for k, v in previos.items():
            setattr(C, k, v)
        shutil.rmtree(tmp, ignore_errors=True)


def _paro_de(**kw) -> str:
    """Corre `registro` sobre el fixture y devuelve el texto del PARO (o ''
    si no paro). Ningun caso escribe vistas: `escribe=False`."""
    with _arbol_registro(**kw):
        try:
            C.registro(escribe=False, imprime=False)
        except C.ParoRegistro as exc:
            return str(exc)
    return ""


def t_registro_punta_a_punta():
    """T-REGISTRO-E2E. Demanda + oferta -> tres vistas, con la cabecera
    `# DERIVADO — NO EDITAR`, las columnas declaradas y bytes IDENTICOS en
    dos derivaciones seguidas (mismo criterio que `cmd_demanda`)."""
    caso = "T-REGISTRO-E2E"
    res = [_fila_demanda("RES-0001", "milpa/tramite.yaml:r.uno:c1", "CORR-0001")]
    corr = [_fila_corrida("CORR-0001", ["RES-0001"])]
    calcs = [{"calc_id": "CALC-FIX-0001", "valores": {"RESULT-A": 1.5},
              "etiquetas": {"generacion": "GEN2", "cuenta_gen2": "SI"}}]
    with _arbol_registro(res=res, corr=corr, calcs=calcs) as tmp:
        C.VISTA_CORRIDAS = tmp / "corridas.tsv"
        C.VISTA_RESULTADOS = tmp / "resultados.tsv"
        C.VISTA_USOS = tmp / "usos.tsv"
        try:
            v = C.registro(escribe=True, imprime=False)
            primeros = {p.name: p.read_bytes() for p in
                        (C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS)}
            C.registro(escribe=True, imprime=False)
            segundos = {p.name: p.read_bytes() for p in
                        (C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS)}
            _afirma(primeros == segundos, caso,
                    "dos derivaciones seguidas no dieron bytes identicos")
            texto = C.VISTA_CORRIDAS.read_text(encoding="utf-8").splitlines()
            _afirma(texto[0] == C.CABECERA_DERIVADO, caso,
                    f"cabecera inesperada: {texto[0]!r}")
            _afirma(texto[1].split("\t") == C.COLS_VISTA_CORRIDAS, caso,
                    "las columnas de corridas.tsv no son las declaradas")
        finally:
            C.VISTA_CORRIDAS = C.CORRIDAS / "corridas.tsv"
            C.VISTA_RESULTADOS = C.CORRIDAS / "resultados.tsv"
            C.VISTA_USOS = C.CORRIDAS / "usos.tsv"
    _afirma(len(v["corridas"]) == 2 and len(v["resultados"]) == 2, caso,
            f"vistas con tamano inesperado: {len(v['corridas'])}/{len(v['resultados'])}")
    _afirma(len(v["usos"]) == 1, caso, f"usos={len(v['usos'])}")


def t_registro_para_id_duplicado():
    """T-REGISTRO-PARA-DUPLICADO. Dos filas con el mismo id PARAN; el mismo
    RESULT en una cadena `repite_de` NO -- repetir ids es lo que significa
    replicar, y confundir las dos cosas volveria imposible todo replay."""
    caso = "T-REGISTRO-PARA-DUPLICADO"
    res = [_fila_demanda("RES-0001", "c:uno:a", "CORR-0001"),
           _fila_demanda("RES-0001", "c:dos:b", "CORR-0001")]
    corr = [_fila_corrida("CORR-0001", ["RES-0001"])]
    p = _paro_de(res=res, corr=corr)
    _afirma("ID-DUPLICADO" in p, caso, f"no paro por id duplicado: {p!r}")

    calcs = [{"calc_id": "CALC-FIX-A", "valores": {"RESULT-A": 1.0},
              "etiquetas": {"cuenta_gen2": "NO", "generacion": "LEGACY-GEN1"}},
             {"calc_id": "CALC-FIX-B", "valores": {"RESULT-A": 1.0},
              "etiquetas": {"cuenta_gen2": "NO", "generacion": "LEGACY-GEN1"},
              "repite_de": "CALC-FIX-A"}]
    p2 = _paro_de(calcs=calcs)
    _afirma(p2 == "", caso, f"un replay declarado paro por id repetido: {p2!r}")


def t_registro_para_cadena_rota():
    """T-REGISTRO-PARA-CADENA. Las validaciones bloqueantes del plan §5 que
    describen una cadena rota: RESULT sin CALC, CALC sin spec, RESULT sin
    sello, hash ausente en un CALC que CUENTA, y ciclo."""
    caso = "T-REGISTRO-PARA-CADENA"
    p = _paro_de(res=[_fila_demanda("RES-0001", "c:uno:a", "CORR-FANTASMA")],
                 corr=[_fila_corrida("CORR-0001", ["RES-0001"])])
    _afirma("RESULT-SIN-CALC" in p, caso, f"RESULT sin CALC no paro: {p!r}")

    with _arbol_registro() as tmp:
        (tmp / "CALC-FIX-SINSPEC").mkdir()
        try:
            C.registro(escribe=False, imprime=False)
            _falla(caso, "un CALC sin spec.yaml no paro")
        except C.ParoRegistro as exc:
            _afirma("CALC-SIN-SPEC" in str(exc), caso, f"paro inesperado: {exc}")

    p = _paro_de(calcs=[{"calc_id": "CALC-FIX-NS", "valores": {"RESULT-A": 1.0},
                         "etiquetas": {"cuenta_gen2": "SI"}, "sin_sello": True}])
    _afirma("RESULT-SIN-SELLO" in p, caso, f"RESULT sin sello no paro: {p!r}")

    p = _paro_de(calcs=[{"calc_id": "CALC-FIX-SH", "valores": {"RESULT-A": 1.0},
                         "etiquetas": {"cuenta_gen2": "SI"},
                         "sin_hash": "spec_yaml_sha256"}])
    _afirma("HASH-AUSENTE" in p, caso, f"hash ausente no paro: {p!r}")

    # El mismo hueco en un replay LEGACY-GEN1 AVISA y no para: es el caso
    # real de `CALC-SMOKE-0001`, sellado antes del esquema endurecido.
    p = _paro_de(calcs=[{"calc_id": "CALC-FIX-LEG", "valores": {"RESULT-A": 1.0},
                         "etiquetas": {"cuenta_gen2": "NO",
                                       "generacion": "LEGACY-GEN1"},
                         "sin_hash": "spec_yaml_sha256"}])
    _afirma(p == "", caso, f"un legado sin hash paro en vez de avisar: {p!r}")

    ciclo = [_fila_demanda("RES-0001", "c:uno:a", "CORR-0001", depende_de="RES-0002"),
             _fila_demanda("RES-0002", "c:dos:b", "CORR-0001", depende_de="RES-0001")]
    p = _paro_de(res=ciclo, corr=[_fila_corrida("CORR-0001", ["RES-0001", "RES-0002"])])
    _afirma("CICLO" in p, caso, f"el ciclo no paro: {p!r}")


def _tramite_con_marca(regla: str, conducta: str, rid: str, valor):
    return {"reglas": [{"id": regla, "entonces": [
        {"conducta": conducta, "p": valor, "corrida0_resultado_id": rid}]}]}


def t_registro_para_consumidor_gen2_roto():
    """T-REGISTRO-PARA-CONSUMIDOR. Un consumidor que ya declara
    `corrida0_resultado_id` y apunta a un RESULT inexistente, o a uno
    LEGACY-GEN1, PARA. Es la puerta por la que se colaria una cifra GEN1
    con rotulo de nueva."""
    caso = "T-REGISTRO-PARA-CONSUMIDOR"
    with _arbol_registro(tramite=_tramite_con_marca("r.uno", "c1", "RESULT-FANTASMA", 0.5)) as tmp:
        consumidor = f"{C._rel(C.TRAMITE)}:r.uno:c1"
        C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
                   [_fila_demanda("RES-0001", consumidor, "CORR-0001")])
        C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
                   [_fila_corrida("CORR-0001", ["RES-0001"])])
        try:
            C.registro(escribe=False, imprime=False)
            _falla(caso, "un corrida0_resultado_id inexistente no paro")
        except C.ParoRegistro as exc:
            _afirma("USO-A-RESULT-INEXISTENTE" in str(exc), caso, f"paro: {exc}")

    calcs = [{"calc_id": "CALC-FIX-LEG", "valores": {"RESULT-L": 1.0},
              "etiquetas": {"cuenta_gen2": "NO", "generacion": "LEGACY-GEN1"}}]
    with _arbol_registro(calcs=calcs,
                         tramite=_tramite_con_marca("r.uno", "c1", "RESULT-L", 1.0)) as tmp:
        consumidor = f"{C._rel(C.TRAMITE)}:r.uno:c1"
        C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
                   [_fila_demanda("RES-0001", consumidor, "CORR-0001")])
        C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
                   [_fila_corrida("CORR-0001", ["RES-0001"])])
        try:
            C.registro(escribe=False, imprime=False)
            _falla(caso, "un consumidor activo apuntando a LEGACY no paro")
        except C.ParoRegistro as exc:
            _afirma("CONSUMIDOR-ACTIVO-A-LEGACY" in str(exc), caso, f"paro: {exc}")


def t_registro_avisa_sin_parar():
    """T-REGISTRO-AVISA. Los tres avisos del plan §5 avisan y NO paran:
    un RESULT sin consumidor, un CALC sellado que nadie cita, y un legado
    sin sucesor que alguien SI lee."""
    caso = "T-REGISTRO-AVISA"
    calcs = [{"calc_id": "CALC-FIX-0001", "valores": {"RESULT-A": 1.0},
              "etiquetas": {"generacion": "GEN2", "cuenta_gen2": "SI"}}]
    with _arbol_registro(calcs=calcs):
        v = C.registro(escribe=False, imprime=False)
    avisos = " · ".join(v["avisos"])
    _afirma("RESULT-SIN-CONSUMIDOR" in avisos, caso, f"avisos={avisos}")
    _afirma("CALC-SIN-CONSUMIDOR-ACTIVO" in avisos, caso, f"avisos={avisos}")


def t_registro_estado_superado():
    """T-REGISTRO-SUPERADO. `repite_de` produce `SUPERADO→<sucesor>` en la
    corrida vieja y deja la nueva SELLADA -- el campo `estado` del encargo."""
    caso = "T-REGISTRO-SUPERADO"
    calcs = [{"calc_id": "CALC-FIX-A", "valores": {"RESULT-A": 1.0},
              "etiquetas": {"cuenta_gen2": "SI", "generacion": "GEN2"}},
             {"calc_id": "CALC-FIX-B", "valores": {"RESULT-A": 1.0},
              "etiquetas": {"cuenta_gen2": "SI", "generacion": "GEN2"},
              "repite_de": "CALC-FIX-A"}]
    with _arbol_registro(calcs=calcs):
        v = C.registro(escribe=False, imprime=False)
    por_spec = {f["spec_id"]: f for f in v["corridas"] if f["origen"] == "OFERTA"}
    _afirma(por_spec["CALC-FIX-A"]["estado"] == "SUPERADO→CALC-FIX-B", caso,
            f"estado={por_spec['CALC-FIX-A']['estado']}")
    _afirma(por_spec["CALC-FIX-B"]["estado"] == "SELLADA", caso,
            f"estado={por_spec['CALC-FIX-B']['estado']}")


def t_status_cifras_derivadas():
    """T-STATUS. Los contadores de §9 salen de las vistas, no de un TSV en
    disco, y un replay LEGACY-GEN1 NUNCA incrementa `N_resultados_sellados`
    (regla explicita del plan)."""
    caso = "T-STATUS"
    res = [_fila_demanda(f"RES-000{i}", f"c:r{i}:x", "CORR-0001") for i in (1, 2, 3)]
    corr = [_fila_corrida("CORR-0001", ["RES-0001", "RES-0002", "RES-0003"])]
    calcs = [{"calc_id": "CALC-FIX-SMOKE", "valores": {"RESULT-S": 1.0},
              "etiquetas": {"cuenta_gen2": "NO", "generacion": "LEGACY-GEN1"}},
             {"calc_id": "CALC-FIX-GEN2", "valores": {"RESULT-G1": 1.0, "RESULT-G2": 2.0},
              "etiquetas": {"cuenta_gen2": "SI", "generacion": "GEN2"}}]
    with _arbol_registro(res=res, corr=corr, calcs=calcs):
        c = C.status(imprime=False)
    esperado = {"N_corridas_requeridas": 1, "N_corridas_selladas": 1,
                "N_resultados_activos": 3, "N_resultados_sellados": 2,
                "N_resultados_pendientes": 3,
                "dependencias_numericas_legacy_activas": 3,
                "resultados_con_validacion_independiente": 0,
                "diferencias_materiales": 0, "no_corrido_abiertas": 0,
                "replays_legacy_sellados": 1}
    for k, v in esperado.items():
        _afirma(c[k] == v, caso, f"{k}={c[k]}, esperado {v}")


def t_status_arbol_real_no_cuenta_smokes():
    """T-STATUS-SMOKES. Sobre el arbol DE VERDAD: los dos replays sellados
    existen, estan contados aparte, y no suben ni una unidad de GEN2. Es la
    cifra que el encargo declara -- `0 / N` es correcto, no un error."""
    caso = "T-STATUS-SMOKES"
    c = C.status(imprime=False)
    _afirma(c["replays_legacy_sellados"] >= 2, caso,
            f"replays sellados={c['replays_legacy_sellados']} (se esperaban >=2)")
    _afirma(c["N_corridas_selladas"] == 0, caso,
            f"N_corridas_selladas={c['N_corridas_selladas']}: un replay GEN1 conto como GEN2")
    _afirma(c["N_resultados_sellados"] == 0, caso,
            f"N_resultados_sellados={c['N_resultados_sellados']}: un replay GEN1 conto como GEN2")
    _afirma(c["N_resultados_activos"] == c["dependencias_numericas_legacy_activas"], caso,
            "hoy toda dependencia activa es legacy: ningun consumidor declara "
            "corrida0_resultado_id todavia")


def t_repro_atrapa_valor_movido():
    """T-REPRO-ATRAPA. El test de `check.py` es de AVISO, no de adorno: si
    alguien mueve la cifra materializada sin mover el RESULT, `registro`
    resuelve la cadena y la comparacion POR TIPO da distinto. Sin este caso,
    `T35` seria un test que no puede fallar."""
    caso = "T-REPRO-ATRAPA"
    calcs = [{"calc_id": "CALC-FIX-G", "valores": {"RESULT-G": 0.5},
              "etiquetas": {"cuenta_gen2": "SI", "generacion": "GEN2"}}]
    for valor, espera_igual in ((0.5, True), (0.9, False)):
        with _arbol_registro(calcs=calcs,
                             tramite=_tramite_con_marca("r.uno", "c1", "RESULT-G", valor)):
            consumidor = f"{C._rel(C.TRAMITE)}:r.uno:c1"
            C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
                       [_fila_demanda("RES-0001", consumidor, "CORR-0001")])
            C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
                       [_fila_corrida("CORR-0001", ["RES-0001"])])
            v = C.registro(escribe=False, imprime=False)
        uso = [u for u in v["usos"] if u["corrida0_resultado_id"] == "RESULT-G"]
        _afirma(len(uso) == 1, caso, f"el uso GEN2 no se derivo: {uso}")
        destino = [f for f in v["resultados"] if f["resultado_id"] == "RESULT-G"][0]
        igual, delta = C._compara_result(destino["valor"], uso[0]["valor_materializado"],
                                         {"tipo": destino["tipo"]},
                                         json.loads(destino["tolerancia"]))
        _afirma(igual is espera_igual, caso,
                f"valor materializado {valor}: igual={igual} delta={delta}")


# ── ACTO GEN2-PRE-E5 · CABLEADO-Y-AUTOMATIZACION-FINAL ────────────────────

def _carga_check():
    ruta = RAIZ / "tests" / "check.py"
    spec = importlib.util.spec_from_file_location("check_bajo_prueba_t35", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _carga_verificador():
    ruta = RAIZ / "tools" / "verifica_encargos_gen2.py"
    spec = importlib.util.spec_from_file_location(
        "verifica_encargos_gen2_bajo_prueba", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def t_estado_calc_derivado():
    """T-ESTADO-CALC-DERIVADO (P1, cierra NC-0010). Los cinco estados de
    `estado_calc()`, cada uno de un artefacto real distinto -- y que
    `registro` (via `_lee_oferta`) reusa la MISMA función en vez de
    mantener una segunda máquina de estados."""
    caso = "T-ESTADO-CALC-DERIVADO"
    tmp = Path(tempfile.mkdtemp(prefix="estado-calc-test-"))
    previa = C.CORRIDAS
    C.CORRIDAS = tmp
    try:
        r = C.estado_calc("CALC-NO-EXISTE")
        _afirma(r["estado"] == "BORRADOR", caso, f"sin carpeta: {r}")

        d = tmp / "CALC-FIX-ESTADO"
        d.mkdir()
        (d / "spec.yaml").write_text("calc_id: CALC-FIX-ESTADO\n", encoding="utf-8")
        r = C.estado_calc("CALC-FIX-ESTADO")
        _afirma(r["estado"] == "SPEC-FIJADA", caso, f"spec sin ejecutar: {r}")

        # PRE-FLIGHT-VERDE se aisla de `preflight()` (probado aparte, y
        # documentado como siempre BLOQUEADO en este arnés por árbol
        # sucio) con un doble -- mismo patrón que ya usan los casos de
        # `run()` más arriba.
        original_pre = C.preflight
        try:
            C.preflight = lambda cid, imprime=False: {"veredicto": "VERDE"}
            r = C.estado_calc("CALC-FIX-ESTADO", evalua_preflight=True)
            _afirma(r["estado"] == "PRE-FLIGHT-VERDE", caso, f"preflight VERDE: {r}")
            C.preflight = lambda cid, imprime=False: {"veredicto": "BLOQUEADO"}
            r = C.estado_calc("CALC-FIX-ESTADO", evalua_preflight=True)
            _afirma(r["estado"] == "SPEC-FIJADA", caso,
                    f"preflight BLOQUEADO no debe subir el estado: {r}")
        finally:
            C.preflight = original_pre
        r = C.estado_calc("CALC-FIX-ESTADO")
        _afirma(r["estado"] == "SPEC-FIJADA", caso,
                f"sin evalua_preflight se queda en SPEC-FIJADA: {r}")

        d2 = tmp / "CALC-FIX-EJEC"
        d2.mkdir()
        (d2 / "spec.yaml").write_text("calc_id: CALC-FIX-EJEC\n", encoding="utf-8")
        C._escribe_json(d2 / "ejecucion.json", {"corrida_id": "x"})
        C._escribe_json(d2 / "resultados.json", {"resultados": {"RESULT-A": 1.0}})
        r = C.estado_calc("CALC-FIX-EJEC")
        _afirma(r["estado"] == "EJECUTADA-NO-SELLADA", caso, f"sin sello: {r}")

        d3 = tmp / "CALC-FIX-SELLADA"
        _sella_calc_fixture(d3, "CALC-FIX-SELLADA", {"RESULT-A": 1.0},
                            {"cuenta_gen2": "SI", "generacion": "GEN2"})
        r = C.estado_calc("CALC-FIX-SELLADA")
        _afirma(r["estado"] == "SELLADA", caso, f"sellado: {r}")
    finally:
        C.CORRIDAS = previa
        shutil.rmtree(tmp, ignore_errors=True)

    # `registro` (vía `_lee_oferta`) reusa la MISMA máquina: no una segunda
    # implementación que pueda divergir de `estado_calc`.
    calcs = [{"calc_id": "CALC-FIX-SELLADA2", "valores": {"RESULT-A": 1.0},
              "etiquetas": {"cuenta_gen2": "SI", "generacion": "GEN2"}}]
    with _arbol_registro(calcs=calcs):
        v = C.registro(escribe=False, imprime=False)
    fila = next(f for f in v["corridas"]
                if f["origen"] == "OFERTA" and f["spec_id"] == "CALC-FIX-SELLADA2")
    _afirma(fila["estado"] == "SELLADA", caso,
            f"`registro` diverge de `estado_calc`: {fila['estado']}")


def t_gen2_sin_resultado_id_avisa():
    """T-GEN2-SIN-RESULTADO-ID (P2/P6). Un consumidor que declara
    `corrida0_generacion: GEN2` sin `corrida0_resultado_id` es un número
    huérfano -- T35 (`tests/check.py`) DEBE avisar. Obligatorio porque el
    mecanismo anterior no podía construir el caso que decía detectar: GEN2
    se leía de la mera presencia de la marca."""
    caso = "T-GEN2-SIN-RESULTADO-ID"
    chk = _carga_check()
    tramite = {"reglas": [{"id": "r.uno", "entonces": [
        {"conducta": "c1", "p": 0.5, "corrida0_generacion": "GEN2"}]}]}
    with _arbol_registro(tramite=tramite):
        consumidor = f"{C._rel(C.TRAMITE)}:r.uno:c1"
        C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
                   [_fila_demanda("RES-0001", consumidor, "CORR-0001")])
        C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
                   [_fila_corrida("CORR-0001", ["RES-0001"])])
        chk.WARNS.clear()
        chk.FAILS.clear()
        chk.t35_repro(modulo=C)
    avisos = " · ".join(m for _, m in chk.WARNS)
    _afirma("(d)" in avisos and "corrida0_generacion: GEN2" in avisos, caso,
            f"T35 no avisó del número huérfano: {avisos!r}")


def t_resultado_id_sin_generacion_avisa():
    """T-RESULTADO-ID-SIN-GENERACION (P2/P6). Un consumidor que cita
    `corrida0_resultado_id` sin declarar `corrida0_generacion: GEN2` tiene
    una cadena incompleta por el otro lado -- T35 debe avisar."""
    caso = "T-RESULTADO-ID-SIN-GENERACION"
    chk = _carga_check()
    calcs = [{"calc_id": "CALC-FIX-RG", "valores": {"RESULT-RG": 1.0},
              "etiquetas": {"cuenta_gen2": "SI", "generacion": "GEN2"}}]
    with _arbol_registro(calcs=calcs,
                         tramite=_tramite_con_marca("r.dos", "c2", "RESULT-RG", 1.0)):
        consumidor = f"{C._rel(C.TRAMITE)}:r.dos:c2"
        C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
                   [_fila_demanda("RES-0002", consumidor, "CORR-0002")])
        C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
                   [_fila_corrida("CORR-0002", ["RES-0002"])])
        chk.WARNS.clear()
        chk.FAILS.clear()
        chk.t35_repro(modulo=C)
    avisos = " · ".join(m for _, m in chk.WARNS)
    _afirma("(e)" in avisos and "cadena incompleta" in avisos, caso,
            f"T35 no avisó de la cadena incompleta: {avisos!r}")


def t_status_mide_no_adopta():
    """T-STATUS-MIDE-NO-ADOPTA (P3/P6). Sellar un RESULT GEN2 y que la
    propuesta PENDIENTE-DE-MESA lo cite no lo adopta: el consumidor activo
    sigue leyendo LEGACY hasta que el mismo declara `corrida0_generacion:
    GEN2` + `corrida0_resultado_id` -- entonces, y solo entonces, pendiente
    baja y adoptado sube."""
    caso = "T-STATUS-MIDE-NO-ADOPTA"
    calcs = [{"calc_id": "CALC-FIX-ADOPCION", "valores": {"RESULT-X": 1.0},
              "etiquetas": {"cuenta_gen2": "SI", "generacion": "GEN2"}}]
    propuesta = {"reglas_propuestas": [{"id": "civico.x", "entonces": [
        {"conducta": "c", "p": 1.0, "corrida0_resultado_id": "RESULT-X"}]}]}

    with _arbol_registro(calcs=calcs, propuesta=propuesta,
                         tramite={"reglas": [{"id": "r.tres", "entonces": [
                             {"conducta": "c3", "p": 0.2}]}]}):
        consumidor = f"{C._rel(C.TRAMITE)}:r.tres:c3"
        C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
                   [_fila_demanda("RES-0003", consumidor, "CORR-0003")])
        C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
                   [_fila_corrida("CORR-0003", ["RES-0003"])])
        c = C.status(imprime=False)
    _afirma(c["N_resultados_gen2_sellados"] == 1, caso,
            f"sellados={c['N_resultados_gen2_sellados']}")
    _afirma(c["N_resultados_gen2_pendientes_adopcion"] == 1, caso,
            f"pendientes={c['N_resultados_gen2_pendientes_adopcion']}")
    _afirma(c["N_resultados_gen2_adoptados_activos"] == 0, caso,
            f"adoptados={c['N_resultados_gen2_adoptados_activos']}")
    _afirma(c["dependencias_numericas_legacy_activas"] == 1, caso,
            f"legacy_activas={c['dependencias_numericas_legacy_activas']}")

    with _arbol_registro(calcs=calcs, propuesta=propuesta,
                         tramite={"reglas": [{"id": "r.tres", "entonces": [
                             {"conducta": "c3", "p": 1.0,
                              "corrida0_generacion": "GEN2",
                              "corrida0_resultado_id": "RESULT-X"}]}]}):
        consumidor = f"{C._rel(C.TRAMITE)}:r.tres:c3"
        C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
                   [_fila_demanda("RES-0003", consumidor, "CORR-0003")])
        C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
                   [_fila_corrida("CORR-0003", ["RES-0003"])])
        c = C.status(imprime=False)
    _afirma(c["N_resultados_gen2_pendientes_adopcion"] == 0, caso,
            f"pendientes tras adoptar={c['N_resultados_gen2_pendientes_adopcion']}")
    _afirma(c["N_resultados_gen2_adoptados_activos"] == 1, caso,
            f"adoptados tras adoptar={c['N_resultados_gen2_adoptados_activos']}")
    _afirma(c["dependencias_numericas_legacy_activas"] == 0, caso,
            f"legacy_activas tras adoptar={c['dependencias_numericas_legacy_activas']}")


def t_encargo_gen2_desfasado():
    """T-ENCARGO-GEN2-DESFASADO (P4/P6). Una diferencia de UN byte entre el
    cuerpo de un encargo GEN2 activo en cola y la sección que le
    corresponde de la versión maestra debe hacer fallar `--verifica` -- es
    el defecto que ya ocurrió una vez (dirección emitió v1.5 y la cola se
    quedó con el cuerpo anterior)."""
    caso = "T-ENCARGO-GEN2-DESFASADO"
    V = _carga_verificador()
    tmp = Path(tempfile.mkdtemp(prefix="verifica-encargos-test-"))
    previos = {k: getattr(V, k) for k in ("RAIZ", "COLA", "NOTAS")}
    try:
        V.RAIZ = tmp
        V.NOTAS = tmp / "forense" / "notas"
        V.COLA = tmp / "forense" / "encargos" / "cola"
        V.NOTAS.mkdir(parents=True)
        V.COLA.mkdir(parents=True)
        cuerpo = ("## E9 · ACTO GEN2-E9 · FIXTURE — falsador de prueba\n\n"
                  "Cabecera: fixture.\n"
                  "Contador: cero.")
        (V.NOTAS / "ENCARGOS-GEN2-v1_0-fixture.md").write_text(
            f"# fixture\n\n---\n\n{cuerpo}\n", encoding="utf-8")
        cola = V.COLA / "2026-01-01-GEN2-E9-FIXTURE.md"
        cola.write_text(
            "ESTADO: GATEADO\nENTORNO: NUBE\nENCOLADO: fixture\nBITACORA:\n- fixture\n\n"
            "──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────\n\n"
            f"{cuerpo}\n", encoding="utf-8")

        _, salida = _silencioso(V.verifica)
        _afirma(salida.strip().startswith("OK ·"), caso,
                f"un encargo idéntico no debe fallar --verifica: {salida!r}")

        # una diferencia de UN byte (una coma por un punto) debe bastar.
        cola.write_text(cola.read_text(encoding="utf-8").replace("cero.", "cero,"),
                        encoding="utf-8")
        buf_err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(buf_err):
            codigo = V.verifica()
        _afirma(codigo == 1, caso,
                "una diferencia de un byte no hizo fallar --verifica")
        _afirma("ENCARGO-GEN2-DESFASADO" in buf_err.getvalue(), caso,
                f"no reportó el PARO esperado: {buf_err.getvalue()!r}")
    finally:
        for k, v in previos.items():
            setattr(V, k, v)
        shutil.rmtree(tmp, ignore_errors=True)


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
    print(f"tests/test_corrida0.py · {len(TESTS)} casos · "
          f"{len(TESTS) - len({f.split(':')[0] for f in fallos})} ok · {len(fallos)} FALLOS")
    for f in fallos:
        print(f"  FAIL  {f}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
