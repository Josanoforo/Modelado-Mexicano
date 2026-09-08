#!/usr/bin/env python3
"""Go/No-Go del marcador -- ACTO GEN2-E7 · READINESS-2 · Pieza B.

Seis checks MECANICOS sobre los artefactos GEN2 del marcador. No opina, no
mide, no arregla: imprime `GO-MARCADOR` o la lista de fallos, y su codigo de
salida es 0 solo en el primer caso.

    python3 tests/gonogo_marcador.py

## Por que AST y audithook, y no `grep`

La primera version de este archivo escaneaba el TEXTO de los artefactos. Fue
un fracaso instructivo: marcaba como violacion la linea del docstring que
dice *"este corredor no abre `corridas-L/`"* y la constante
`LEGADO_PROHIBIDO` que existe precisamente para prohibirlo. Un check que
castiga a la defensa por nombrar al atacante no mide nada.

Lo que se mide aqui son dos propiedades distintas, con la herramienta que
corresponde a cada una:

  · **Que el corredor no LLAME a la API del legado** -> AST. Se recolectan
    los identificadores REALES del modulo (`Name.id`, `Attribute.attr`, los
    modulos importados y el argumento de `spec_from_file_location`). La prosa
    de un docstring no es un identificador y no cuenta; una llamada si.

  · **Que el corredor no ABRA archivos del legado** -> `sys.addaudithook`
    sobre el evento `open`, alrededor de la ejecucion real de cada corredor
    en su modo de readiness. Un `open()` con la ruta armada por concatenacion
    -- que ningun escaneo estatico atrapa -- si aparece aqui.

    MARCO-VIGENTE-UNICO   una sola fuente del marco entre codigo y specs
    M-DESDE-CONTRATO      el corredor M toma su marco del snapshot de inputs,
                          no del `RUTA_MARCO_V1_1` cableado de emite_m, y no
                          llama `camina()` (el `regenera_todos()` historico)
    R-SIN-HEURISTICA      el adaptador R no llama `localiza_payload` y si usa
                          `resolver_payload` sobre un `payload_id` exacto
    L-SPEC-v1_2           el corredor L consume L-spec-v1_2.json (14 celdas) y
                          no importa `carga_l_v1_1` ni `runner_l_cli`
    AGREGADO-DERIVADO     el agregado consume solo RESULT-* de CALC-*, no
                          `corridas-*/` ni `agregado-v1_3-resultado.json`
    LEGACY-NO-LEIDO       ningun corredor abre corridas-R/M/L ni
                          agregado_v1_3 al correr -- salvo un input declarado
                          `valor_legacy` (el delta contra GEN1, unico uso que
                          el encargo permite)
"""
from __future__ import annotations

import ast
import csv
import hashlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

MARCO_VIGENTE_REL = "forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv"
MARCO_VIGENTE = Path(MARCO_VIGENTE_REL).name

CALC_M = "data/corrida0/CALC-M-marco-M-sorteado-v1_3"
CALC_AGG = "data/corrida0/CALC-AGG-marco-M-sorteado-v1_3"

ARTEFACTOS = {
    "M":   f"{CALC_M}/medidor.py",
    "R":   "tools/arbitra_gen2.py",
    "L":   "forense/prereg-duelo-v2/corredor_l_v1_2.py",
    "AGG": f"{CALC_AGG}/medidor.py",
}

# Fragmentos de ruta del legado GEN1. Una apertura cuya ruta contenga
# cualquiera de estos es una lectura de legado.
LEGADO_RUTAS = ("/corridas-R/", "/corridas-M/", "/corridas-L/",
                "agregado_v1_3.py", "agregado-v1_3-resultado.json")

# La marca que exime: un input declarado `valor_legacy` es la lectura de la
# cifra GEN1 para reportar un delta contra ella -- el unico uso permitido.
MARCA_EXENTA = "valor_legacy"

_RE_MARCO = re.compile(r"marco-M-sorteado-v1_\d+\.tsv")


# ── utilidades ─────────────────────────────────────────────────────────────

def _lee(rel: str) -> str | None:
    try:
        return (RAIZ / rel).read_text(encoding="utf-8")
    except OSError:
        return None


def identificadores(texto: str) -> set[str]:
    """Los nombres que el modulo REALMENTE usa: variables, atributos, modulos
    importados y el nombre logico de todo `spec_from_file_location`. Un
    docstring que menciona `camina()` no aporta un identificador; una llamada
    `emite_m.camina()` aporta `camina`."""
    arbol = ast.parse(texto)
    fuera: set[str] = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Name):
            fuera.add(nodo.id)
        elif isinstance(nodo, ast.Attribute):
            fuera.add(nodo.attr)
        elif isinstance(nodo, ast.Import):
            for a in nodo.names:
                fuera.add(a.name.split(".")[0])
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.module:
                fuera.add(nodo.module.split(".")[0])
            for a in nodo.names:
                fuera.add(a.name)
        elif isinstance(nodo, ast.Call):
            fn = nodo.func
            nombre = fn.attr if isinstance(fn, ast.Attribute) else \
                     (fn.id if isinstance(fn, ast.Name) else "")
            if nombre == "spec_from_file_location":
                for arg in nodo.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        fuera.add(arg.value)
    return fuera


def constantes_str(texto: str) -> dict[str, list[str]]:
    """`{NOMBRE: [literales de texto que aparecen en su valor]}` para las
    asignaciones de modulo. Se camina el VALOR entero, no solo el caso
    `NOMBRE = "literal"`: un corredor declara su spec como
    `L_SPEC_JSON = DIR / "L-spec-v1_2.json"`, que es un `BinOp` y no un
    `Constant`. Mirar solo el caso simple dejaba fuera precisamente la linea
    que este check existe para leer."""
    fuera: dict[str, list[str]] = {}
    for nodo in ast.parse(texto).body:
        if not (isinstance(nodo, ast.Assign) and len(nodo.targets) == 1
                and isinstance(nodo.targets[0], ast.Name)):
            continue
        literales = [n.value for n in ast.walk(nodo.value)
                     if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        if literales:
            fuera[nodo.targets[0].id] = literales
    return fuera


def _todos_los_literales(consts: dict[str, list[str]]) -> set[str]:
    return {v for vals in consts.values() for v in vals}


def _carga(rel: str, nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def _entrada_repo(iid: str, rel: str) -> dict:
    crudo = (RAIZ / rel).read_bytes()
    return {"id": iid, "origen": "repo", "ruta": rel, "bytes": crudo,
            "sha256": hashlib.sha256(crudo).hexdigest(), "estado": "COINCIDE"}


class _Auditor:
    """Acumula aperturas; no decide. Quien juzga es el check."""

    def __init__(self) -> None:
        self.activo = False
        self.total = 0
        self.legado: list[str] = []

    def __call__(self, evento: str, args) -> None:
        if not self.activo or evento != "open":
            return
        crudo = args[0]
        if isinstance(crudo, (bytes, bytearray)):
            crudo = crudo.decode("utf-8", "replace")
        if not isinstance(crudo, str):
            return
        self.total += 1
        plana = crudo.replace("\\", "/")
        for frag in LEGADO_RUTAS:
            if frag in plana:
                self.legado.append(plana)
                return


_AUDITOR = _Auditor()
sys.addaudithook(_AUDITOR)


# ── los seis checks ────────────────────────────────────────────────────────

def check_marco_vigente_unico() -> list[str]:
    """El marco que el codigo RESUELVE (constantes de modulo) y el que las
    specs DECLARAN (input `origen: repo`) tienen que ser uno y el mismo. La
    prosa que compara contra `v1_1` para explicar la diferencia no cuenta:
    solo se miran constantes y specs."""
    fallos, vistos = [], {}
    for etiqueta, rel in ARTEFACTOS.items():
        texto = _lee(rel)
        if texto is None:
            fallos.append(f"artefacto ausente: {rel} ({etiqueta})")
            continue
        for nombre, valores in constantes_str(texto).items():
            if "PROHIBID" in nombre or "LEGADO" in nombre:
                continue  # lista de lo prohibido: nombra para prohibir
            for valor in valores:
                for m in _RE_MARCO.findall(valor):
                    vistos.setdefault(m, set()).add(f"{rel}:{nombre}")
    for rel in (f"{CALC_M}/spec.yaml", f"{CALC_AGG}/spec.yaml"):
        texto = _lee(rel)
        if texto is None:
            fallos.append(f"spec ausente: {rel}")
            continue
        for ruta in re.findall(r"^\s*ruta:\s*(\S+)\s*$", texto, re.M):
            for m in _RE_MARCO.findall(ruta):
                vistos.setdefault(m, set()).add(f"{rel}:inputs")
    for nombre in sorted(set(vistos) - {MARCO_VIGENTE}):
        fallos.append(f"marco no vigente {nombre} (vigente: {MARCO_VIGENTE}) "
                      f"en {', '.join(sorted(vistos[nombre]))}")
    if MARCO_VIGENTE not in vistos and not fallos:
        fallos.append(f"ningun artefacto ni spec resuelve {MARCO_VIGENTE}")
    return fallos


def check_m_desde_contrato() -> list[str]:
    fallos = []
    rel = ARTEFACTOS["M"]
    texto = _lee(rel)
    if texto is None:
        return [f"ausente {rel}"]
    ids = identificadores(texto)
    for prohibido in ("RUTA_MARCO_V1_1", "RUTA_MARCO_V1_0", "camina",
                      "regenera_todos"):
        if prohibido in ids:
            fallos.append(f"{rel} usa `{prohibido}` -- el marco (o la caminata) "
                          f"vendria cableado de emite_m, no del contrato")
    if 'inputs["IN-MARCO-M-SORTEADO-V1-3"]' not in texto:
        fallos.append(f"{rel} no lee el marco del snapshot de inputs")
    if "emite_celda" not in ids:
        fallos.append(f"{rel} no llama `emite_celda` -- no envuelve la emision")
    spec = _lee(f"{CALC_M}/spec.yaml")
    if spec is None:
        fallos.append(f"ausente {CALC_M}/spec.yaml")
    elif not re.search(r"ruta:\s*" + re.escape(MARCO_VIGENTE_REL), spec):
        fallos.append("la spec de CALC-M no declara el marco vigente como "
                      "input `origen: repo`")
    return fallos


def check_r_sin_heuristica() -> list[str]:
    fallos = []
    rel = ARTEFACTOS["R"]
    texto = _lee(rel)
    if texto is None:
        return [f"ausente {rel}"]
    ids = identificadores(texto)
    if "localiza_payload" in ids:
        fallos.append(f"{rel} llama `localiza_payload` -- la heuristica de "
                      f"substring de arbitra.py")
    if "resolver_payload" not in ids:
        fallos.append(f"{rel} no usa `resolver_payload`")
    if "payload_id_de" not in ids:
        fallos.append(f"{rel} no toma el payload_id exacto de la tabla de "
                      f"codificacion")
    # Comprobacion de conducta: una celda conocida resuelve a UN payload_id,
    # no a una lista de candidatos.
    try:
        mod = _carga(rel, "arbitra_gen2_gonogo")
        r = mod.resuelve_celda("CIV-08")
    except Exception as exc:
        fallos.append(f"{rel}: resuelve_celda levanto {type(exc).__name__}: {exc}")
    else:
        if not isinstance(r.get("payload_id"), str) or not r["payload_id"]:
            fallos.append(f"{rel}: resuelve_celda no devolvio un payload_id "
                          f"unico: {r.get('payload_id')!r}")
    return fallos


def check_l_spec_v1_2() -> list[str]:
    fallos = []
    rel = ARTEFACTOS["L"]
    texto = _lee(rel)
    if texto is None:
        return [f"ausente {rel}"]
    ids = identificadores(texto)
    for prohibido in ("carga_l_v1_1", "runner_l_cli", "cargar_celdas_l_spec",
                      "celda_a_spec"):
        if prohibido in ids:
            fallos.append(f"{rel} depende de `{prohibido}` (cadena del "
                          f"universo v1.1)")
    # Se mira LA constante que resuelve la spec de entrada, no el conjunto de
    # literales del modulo: la lista `LEGADO_PROHIBIDO` nombra
    # `L-spec-v1_1.json` para prohibirlo, y contarla seria castigar la defensa.
    consts = constantes_str(texto)
    spec_declarada = consts.get("L_SPEC_JSON")
    if spec_declarada is None:
        fallos.append(f"{rel} no declara una constante L_SPEC_JSON")
    elif "L-spec-v1_2.json" not in spec_declarada:
        fallos.append(f"{rel}: L_SPEC_JSON resuelve {spec_declarada}, "
                      f"no L-spec-v1_2.json")
    spec = RAIZ / "forense/prereg-duelo-v2/L-spec-v1_2.json"
    try:
        n_celdas = len(json.loads(spec.read_text(encoding="utf-8"))["celdas"])
    except (OSError, KeyError, ValueError) as exc:
        return fallos + [f"no se pudo contar celdas de {spec.name}: {exc}"]
    if n_celdas != 14:
        fallos.append(f"{spec.name} trae {n_celdas} celdas, el marcador declara 14")
    try:
        mod = _carga(rel, "corredor_l_gonogo")
        if mod.N_CELDAS_ESPERADAS != n_celdas:
            fallos.append(f"{rel} declara N_CELDAS_ESPERADAS="
                          f"{mod.N_CELDAS_ESPERADAS} y la spec trae {n_celdas}")
        if len(mod.plan()) != n_celdas * len(mod.VARIANTES) * mod.K_CORRIDAS_SELLADO:
            fallos.append(f"{rel}: el plan no cubre celdas x variantes x k")
    except Exception as exc:
        fallos.append(f"{rel}: {type(exc).__name__}: {exc}")
    return fallos


def check_agregado_derivado() -> list[str]:
    fallos = []
    rel = ARTEFACTOS["AGG"]
    if _lee(rel) is None:
        return [f"ausente {rel}"]
    spec = _lee(f"{CALC_AGG}/spec.yaml")
    if spec is None:
        return [f"ausente {CALC_AGG}/spec.yaml"]
    rutas = re.findall(r"^\s*ruta:\s*(\S+)\s*$", spec, re.M)
    if not rutas:
        fallos.append("la spec no declara ningun input `origen: repo`")
    for ruta in rutas:
        if any(f in ruta for f in LEGADO_RUTAS) or "agregado_v1_3" in ruta:
            fallos.append(f"input de legado GEN1 en la spec: {ruta}")
        elif not (ruta.startswith("data/corrida0/CALC-")
                  or ruta == MARCO_VIGENTE_REL):
            fallos.append(f"input que no es RESULT de un CALC ni el marco: {ruta}")
    if not any(r.endswith("resultados.json") for r in rutas):
        fallos.append("la spec no consume ningun resultados.json de otro CALC")
    return fallos


def check_legacy_no_leido() -> list[str]:
    """Conducta, no texto: se corre cada corredor en su modo de readiness con
    el audithook encendido y se cuentan las aperturas bajo el legado."""
    fallos = []

    # M -- emision completa sobre el marco vigente.
    try:
        mod = _carga(ARTEFACTOS["M"], "medidor_m_gonogo")
        entradas = {
            "IN-MARCO-M-SORTEADO-V1-3": _entrada_repo(
                "IN-MARCO-M-SORTEADO-V1-3", MARCO_VIGENTE_REL),
            "IN-EMITE-M": _entrada_repo("IN-EMITE-M", "tools/emite_m.py"),
        }
        _AUDITOR.legado.clear()
        _AUDITOR.activo = True
        try:
            mod.medir(entradas, {"parametros": {"fuente_acto": "GO/NO-GO"}})
        finally:
            _AUDITOR.activo = False
        for ruta in sorted(set(_AUDITOR.legado)):
            fallos.append(f"corredor M abrio legado: {ruta}")
    except Exception as exc:
        fallos.append(f"corredor M: {type(exc).__name__}: {exc}")

    # L -- dry-run completo (224 corridas planificadas, cero llamadas).
    try:
        mod = _carga(ARTEFACTOS["L"], "corredor_l_gonogo_legacy")
        _AUDITOR.legado.clear()
        _AUDITOR.activo = True
        try:
            mod.plan()
        finally:
            _AUDITOR.activo = False
        for ruta in sorted(set(_AUDITOR.legado)):
            fallos.append(f"corredor L abrio legado: {ruta}")
        if "/corridas-L/" in str(mod.SALIDA).replace("\\", "/"):
            fallos.append(f"corredor L escribiria en legado GEN1: {mod.SALIDA}")
    except Exception as exc:
        fallos.append(f"corredor L: {type(exc).__name__}: {exc}")

    # R -- resolucion de las celdas del marco vigente (no abre microdato).
    try:
        mod = _carga(ARTEFACTOS["R"], "arbitra_gen2_gonogo_legacy")
        marco = list(csv.DictReader(
            io.StringIO((RAIZ / MARCO_VIGENTE_REL).read_text(encoding="utf-8")),
            delimiter="\t"))
        tabla = mod.lee_codificacion()
        _AUDITOR.legado.clear()
        _AUDITOR.activo = True
        try:
            for fila in marco:
                try:
                    mod.resuelve_celda(fila["id"], tabla)
                except mod.SinPayloadDeclarado:
                    pass  # celda sin insumo declarado: es un hecho, no legado
        finally:
            _AUDITOR.activo = False
        for ruta in sorted(set(_AUDITOR.legado)):
            fallos.append(f"adaptador R abrio legado: {ruta}")
    except Exception as exc:
        fallos.append(f"adaptador R: {type(exc).__name__}: {exc}")

    # AGG -- solo si su spec ya esta depositada (es la ultima en existir:
    # declara el sha del resultados.json de CALC-M, que nace de una corrida).
    spec = _lee(f"{CALC_AGG}/spec.yaml")
    res_m = RAIZ / CALC_M / "resultados.json"
    if spec is None or not res_m.exists():
        fallos.append(f"agregado: {CALC_AGG}/spec.yaml o el resultados.json de "
                      f"CALC-M aun no existen -- no se puede ejercer el check")
    else:
        try:
            mod = _carga(ARTEFACTOS["AGG"], "medidor_agg_gonogo")
            entradas = {
                "IN-MARCO-M-SORTEADO-V1-3": _entrada_repo(
                    "IN-MARCO-M-SORTEADO-V1-3", MARCO_VIGENTE_REL),
                "IN-CALC-M-RESULTADOS": _entrada_repo(
                    "IN-CALC-M-RESULTADOS", f"{CALC_M}/resultados.json"),
            }
            _AUDITOR.legado.clear()
            _AUDITOR.activo = True
            try:
                mod.medir(entradas, {"parametros": {}})
            finally:
                _AUDITOR.activo = False
            for ruta in sorted(set(_AUDITOR.legado)):
                fallos.append(f"agregado abrio legado: {ruta}")
        except Exception as exc:
            fallos.append(f"agregado: {type(exc).__name__}: {exc}")

    # La exencion declarada: un input marcado `valor_legacy` en una spec es
    # lectura permitida. Hoy ninguna spec la usa; se comprueba para que el
    # dia que se use quede dicho en la salida y no pase inadvertida.
    for rel in (f"{CALC_M}/spec.yaml", f"{CALC_AGG}/spec.yaml"):
        texto = _lee(rel)
        if texto and MARCA_EXENTA in texto:
            print(f"  [AVISO] {rel} declara un input `{MARCA_EXENTA}` -- "
                  f"lectura de legado PERMITIDA para delta contra GEN1")
    return fallos


CHECKS = (
    ("MARCO-VIGENTE-UNICO", check_marco_vigente_unico),
    ("M-DESDE-CONTRATO", check_m_desde_contrato),
    ("R-SIN-HEURISTICA", check_r_sin_heuristica),
    ("L-SPEC-v1_2", check_l_spec_v1_2),
    ("AGREGADO-DERIVADO", check_agregado_derivado),
    ("LEGACY-NO-LEIDO", check_legacy_no_leido),
)


def evalua() -> dict[str, list[str]]:
    return {nombre: fn() for nombre, fn in CHECKS}


def main() -> int:
    print("=== Go/No-Go del marcador · ACTO GEN2-E7 · READINESS-2 · Pieza B ===\n")
    resultado = evalua()
    for nombre, _fn in CHECKS:
        fallos = resultado[nombre]
        print(f"  [{'PASA' if not fallos else 'FALLA'}] {nombre}")
        for f in fallos:
            print(f"           - {f}")
    todos = [(n, f) for n, fs in resultado.items() for f in fs]
    if todos:
        print(f"\nNO-GO -- {len(todos)} fallo(s):")
        for n, f in todos:
            print(f"  - {n}: {f}")
        return 1
    print("\nGO-MARCADOR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
