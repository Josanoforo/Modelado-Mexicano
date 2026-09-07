#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/test_corrida0.py` -- unidad de `preflight` / `verify` / `spec-check`
/ `negativo` con fixtures pequenos y SIN CORPUS.

ACTO GEN2-E3 · AUTOMATIZA-GEN2-1. Lo llama `tests/check.py` (T32 · T-CORRIDA0).

Estos tests no abren microdato, no tocan la red y no escriben fuera de un
directorio temporal. Los unicos archivos reales que leen son los TRES
inventarios canonicos vigentes -- que es justo lo que el caso de prueba
obligatorio del encargo exige comprobar contra el arbol de verdad.

Nota sobre `preflight` en un test: el arbol de trabajo esta sucio mientras
la suite corre, asi que `preflight` siempre devuelve BLOQUEADO aqui. Por eso
los tests afirman sobre los BLOQUEOS CONCRETOS (que aparezca el que toca y
que NO aparezca el que no toca), no sobre un VERDE global que en este
contexto seria imposible y cuya ausencia no probaria nada.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
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
        valores, code, err = C._ejecuta({"script": rel, "parametros": {}, "inputs": []})
        _afirma(code == 1 and "boom" in err, caso, f"code={code} err={err}")
        _afirma(valores == {}, caso, "devolvio valores tras reventar")
    finally:
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
