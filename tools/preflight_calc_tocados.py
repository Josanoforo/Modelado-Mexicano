#!/usr/bin/env python3
"""preflight sobre los CALC SIN SELLO que un cambio añade o toca.

ACTO GEN2-TUBERIA-PREFLIGHT-CI-1 (21/sep/2026). Defecto real que atrapa,
tres veces observado y contado por el PR que lo introdujo:

  · #781 (15/sep) — cuatro CALC sin `spec.md`; lo topó GEN2-MEDICION-DEMANDA-2
    el mismo día.
  · #903 (19/sep) — EMISIONES-0001 sin `seed`, sin tolerancia y sin
    resultados; lo topó la ejecución del día siguiente.
  · #926 (20/sep) — `spec_md:` escrito como ruta desde la raíz, que
    `preflight` resuelve relativa al directorio del CALC; lo topó
    GEN2-CELDA-D-PILOTO-3-COMMIT-2-3 esa noche.

Los tres son cableado: el CALC quedó fusionado en un estado en que el
runner no podría correrlo. Los tres se ven en segundos y sin corpus, porque
`corrida0 preflight` «no mide, no escribe, no arregla nada» y sin corpus
montado sólo hace sha256 de lo que hay.

LO QUE NO ES: un verificador de que el CALC esté listo para correr. Un CALC
puede estar legítimamente BLOQUEADO —spec congelada sin medidor todavía,
input que es el resultado de un hermano que aún no corre, corpus que el
runner nunca tiene— y eso NO pone rojo a nadie. Esa distinción es el objeto
de este archivo: ver `ESTADOS_LEGITIMOS`.

LA REGLA, y por qué está escrita al revés de lo que parece natural: la lista
cerrada es la de estados LEGÍTIMOS, y todo lo demás es FAIL. Así el chequeo
no se acopla a la evolución de `tools/corrida0.py`, que es de dirección: si
dirección añade un bloqueo nuevo, este chequeo lo trata como `preflight` lo
trata —bloquea— sin que nadie lo edite. Sólo un estado legítimo nuevo obliga
a tocar la lista, y eso sí debe ser una decisión visible (falsador §11 del
encargo).

D-23 · Esta herramienta NO muta el clon que verifica: no hace `fetch`, no
escribe archivos, y desactiva el bytecode para no ensuciar el árbol con
`__pycache__` —que `preflight` leería como `working_tree_dirty`—.

Uso:
    python3 tools/preflight_calc_tocados.py --base <ref> [--cabeza <ref>]

El árbol de trabajo debe estar en `<cabeza>`: `preflight` lee del disco.
Códigos de salida: 0 = sin FAIL · 1 = al menos un FAIL · 2 = error de uso.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Antes de importar `tools/corrida0.py`: un `__pycache__` recién escrito en
# el árbol que se verifica es exactamente lo que `preflight` reporta como
# `working_tree_dirty`, y sería un rojo fabricado por el propio chequeo.
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

RAIZ = Path(__file__).resolve().parents[1]
CORRIDAS_REL = "data/corrida0"

# Un CALC se da por SELLADO si existe cualquiera de estos dos. `preflight`
# entra a verificar sello por `sello.sha256`; dirección cuenta el universo
# por `sello.json`. En main 5a888bcb los dos conjuntos coinciden (153 y 153),
# así que la unión no cambia el universo hoy y cubre el desfase si un día
# llegaran separados.
ARCHIVOS_DE_SELLO = ("sello.json", "sello.sha256")

# LISTA CERRADA de estados legítimos: bloquean a `preflight` con razón, pero
# no son defecto del PR. Cada línea cita de dónde sale su legitimidad.
ESTADOS_LEGITIMOS: dict[str, str] = {
    "script_ausente":
        "spec congelada sin corrida todavía — "
        "forense/notas/2026-09-15-GEN2-SPECS-DEMANDA-1-mapa-19.md:324: "
        "«Es el estado correcto de una spec congelada sin corrida, no un defecto.»",
    "input_repo_ausente":
        "el input es el resultado de un CALC hermano que aún no corre "
        "(cadena) — p. ej. ADJUDICACION-0001 depende de "
        "EMISIONES-0002/resultados.json, que no existe hasta que ese corra",
    "input_repo_no_commiteado":
        "misma cadena: un resultado que todavía no nace no puede estar "
        "commiteado",
    "spec_md_sha256_discorda_origin_main":
        "el runner de CI no tiene `origin/main` en su clon superficial; si "
        "el token aparece, se reporta y no adjudica",
}

# Prefijos (el token lleva el estado pegado: `input_manifiesto_<estado>`).
PREFIJOS_LEGITIMOS: dict[str, str] = {
    "input_manifiesto_":
        "corpus que no está montado en el runner — el runner nunca tiene "
        "corpus, y eso es por diseño (A.2: todo acto que abre microdato va "
        "a caja, no a la nube)",
}

# Ni WARN ni FAIL: este chequeo no los adjudica.
FUERA_DE_ALCANCE: dict[str, str] = {
    "calc_ya_sellado":
        "un CALC sellado no entra al universo de este chequeo; si aparece, "
        "el que falló fue la derivación del universo",
    "sello_previo_incompatible":
        "igual que el anterior: es asunto del sello, no del PR",
    "working_tree_dirty":
        "si el árbol está sucio en CI, quien lo ensució es el propio "
        "chequeo: error del chequeo, no del PR",
}

WARN, FAIL, FUERA = "WARN", "FAIL", "FUERA-DE-ALCANCE"


def token(bloqueo: str) -> str:
    """El nombre del bloqueo, sin su carga. `preflight` los emite como
    `ausente=<ruta>`, `calc_id_discorda(spec=…, dir=…)` o pelados."""
    for corte in ("=", "("):
        i = bloqueo.find(corte)
        if i != -1:
            bloqueo = bloqueo[:i]
    return bloqueo.strip()


def clasifica(bloqueo: str) -> tuple[str, str]:
    """(clase, razón) de un bloqueo de `preflight`."""
    t = token(bloqueo)
    if t in ESTADOS_LEGITIMOS:
        return WARN, ESTADOS_LEGITIMOS[t]
    for pref, razon in PREFIJOS_LEGITIMOS.items():
        if t.startswith(pref):
            return WARN, razon
    if t in FUERA_DE_ALCANCE:
        return FUERA, FUERA_DE_ALCANCE[t]
    return FAIL, ("no está en la lista cerrada de estados legítimos: "
                  "`preflight` bloquea por esto y el runner no podría correr "
                  "este CALC")


def _git(*args: str, cwd: Path | None = None) -> tuple[int, str]:
    r = subprocess.run(["git", *args], cwd=str(cwd or RAIZ),
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def universo(base: str, cabeza: str = "HEAD", raiz: Path | None = None) -> list[str]:
    """Los CALC que el cambio añade o toca y que en `cabeza` no tienen sello.

    Se deriva del árbol de `cabeza` con `git ls-tree`, no del disco: así el
    universo es el mismo se corra donde se corra, y una supresión no deja un
    CALC fantasma en la lista.
    """
    raiz = raiz or RAIZ
    cod, salida = _git("diff", "--name-only", base, cabeza, "--",
                       CORRIDAS_REL, cwd=raiz)
    if cod != 0:
        raise SystemExit(
            f"BASE-NO-RESOLUBLE: `git diff {base} {cabeza}` salió {cod}. "
            "El job de CI debe traer la base en su propio clonado (D-23: no "
            "se hace fetch dentro del clon de otro job).")
    tocados: set[str] = set()
    for linea in salida.splitlines():
        partes = linea.strip().split("/")
        if len(partes) >= 3 and partes[0] == "data" and partes[1] == "corrida0":
            tocados.add(partes[2])
    vivos: list[str] = []
    for calc in sorted(tocados):
        cod, arbol = _git("ls-tree", "-r", "--name-only", cabeza, "--",
                          f"{CORRIDAS_REL}/{calc}/", cwd=raiz)
        nombres = {Path(l).name for l in arbol.splitlines()}
        if "spec.yaml" not in nombres:
            continue  # borrado en cabeza, o no es un CALC
        if nombres & set(ARCHIVOS_DE_SELLO):
            continue  # sellado: fuera del universo por definición
        vivos.append(calc)
    return vivos


def evalua(calc_ids: list[str], preflight=None) -> dict:
    """Corre `preflight` sobre cada CALC y clasifica sus bloqueos.

    `preflight` se inyecta para poder ejercitar la clasificación sin arrancar
    el runner entero; por omisión es el de `tools/corrida0.py`, importado sin
    modificarlo.
    """
    if preflight is None:
        sys.path.insert(0, str(RAIZ / "tools"))
        from corrida0 import preflight as preflight  # noqa: PLC0415

    filas = []
    for calc in calc_ids:
        try:
            res = preflight(calc, imprime=False)
            bloqueos = list(res.get("bloqueos") or [])
            veredicto = res.get("veredicto", "?")
        except Exception as e:  # noqa: BLE001
            # `_carga_spec` levanta BloqueoPreflight (spec_yaml_ausente,
            # spec_yaml_no_es_mapa). Un CALC que ni siquiera carga es el caso
            # más crudo del defecto, no una excepción a tratar aparte.
            bloqueos = [f"{type(e).__name__.lower()}={e}"]
            veredicto = "BLOQUEADO"
        clasificados = [(b, *clasifica(b)) for b in bloqueos]
        filas.append({
            "calc_id": calc, "veredicto": veredicto,
            "bloqueos": clasificados,
            "fail": [b for b, c, _ in clasificados if c == FAIL],
            "warn": [b for b, c, _ in clasificados if c == WARN],
            "fuera": [b for b, c, _ in clasificados if c == FUERA],
        })
    return {
        "filas": filas,
        "calc_fail": [f["calc_id"] for f in filas if f["fail"]],
        "calc_warn": [f["calc_id"] for f in filas if f["warn"] and not f["fail"]],
        "calc_limpio": [f["calc_id"] for f in filas
                        if not f["fail"] and not f["warn"]],
    }


def informe(res: dict, escribe=print) -> None:
    filas = res["filas"]
    if not filas:
        escribe("0 CALC sin sello tocados — nada que verificar. PASA.")
        return
    escribe(f"CALC sin sello tocados por este cambio: {len(filas)}")
    for f in filas:
        marca = "FAIL" if f["fail"] else ("WARN" if f["warn"] else "LIMPIO")
        escribe(f"\n  [{marca}] {f['calc_id']}   "
                f"(corrida0 preflight: {f['veredicto']})")
        for bloqueo, clase, razon in f["bloqueos"]:
            escribe(f"      {clase:<16} {bloqueo}")
            escribe(f"      {'':<16}   ↳ {razon}")
    escribe(f"\nRESUMEN · FAIL={len(res['calc_fail'])} "
            f"WARN={len(res['calc_warn'])} LIMPIO={len(res['calc_limpio'])}")
    if res["calc_fail"]:
        escribe("ROJO. Estos CALC quedarían en main en un estado en que el "
                "runner no podría correrlos: " + ", ".join(res["calc_fail"]))
        escribe("Un bloqueo marcado FAIL no se relaja: o se arregla el CALC, "
                "o el estado es legítimo y se añade a ESTADOS_LEGITIMOS con "
                "su razón, en un acto, visible.")
    else:
        escribe("PASA. Ningún bloqueo fuera de la lista cerrada de estados "
                "legítimos.")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", required=True,
                   help="ref contra la que se deriva qué CALC toca el cambio")
    p.add_argument("--cabeza", default="HEAD",
                   help="ref del cambio (por omisión HEAD)")
    a = p.parse_args(argv)

    print(f"PREFLIGHT-CALC-TOCADOS · base={a.base} cabeza={a.cabeza}")
    calcs = universo(a.base, a.cabeza)
    res = evalua(calcs)
    informe(res)
    return 1 if res["calc_fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
