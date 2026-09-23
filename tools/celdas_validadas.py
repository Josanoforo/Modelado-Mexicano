#!/usr/bin/env python3
"""celdas_validadas.py -- MÉTRICA RECTORA del programa: una sola derivación
importable, movida desde `tablero_programa.py` (ACTO
GEN2-TUBERIA-METRICA-RECTORA-1, firma de mesa 20/sep/2026, plan de
aceleración P2). Antes de este acto la función vivía sólo en
`tablero_programa.py`; hoy es la fuente única que importan `corrida0
status`, `digesto_tramite --mesa`, el tablero y el inventario.

Uso:
    python3 tools/celdas_validadas.py --json     # diccionario completo
    python3 tools/celdas_validadas.py --linea     # una sola línea de resumen

Reglas que este módulo respeta (instrucciones v2.16):
  * §4 -- PROSPECTIVA y RETROSPECTIVA no se suman en una sola cifra.
  * A.13 -- todo negativo declara cuántos archivos examinó.
  * D-16 -- ninguna cifra sale sin su SHA (bloque `universo`).
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# Mismo tope que tablero_programa.py: un `resultados_ids` grande revienta el
# tope de 131072 del lector csv por defecto. El tope es del lector, no del dato.
csv.field_size_limit(sys.maxsize)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, cwd=RAIZ
                           ).stdout.decode("utf-8", "replace").strip()


def tsv_rows(path: str):
    return [r for r in csv.reader(open(path, encoding="utf-8", errors="replace"), delimiter="\t")
            if r and not r[0].startswith("#")]


#: Sufijos de RESULT con los que una corrida de adjudicación nombra el ERROR
#: POR CELDA del piso C2 contra R. Son dos convenciones vivas, no una
#: preferencia: los pilotos 1 y 2 emitieron `...-ARB-D-C2-<celda>` y el piloto 3
#: `...-<celda>-C2-D-PP`. La escala NO se teclea: se deriva abajo contra el
#: `margen_material` sellado de la propia celda-D.
_PATRONES_ERROR_C2 = (
    ("-C2-D-PP", "sufijo"),      # piloto 3 (GOB): ya en puntos porcentuales
    ("-ARB-D-C2-", "prefijo"),   # pilotos 1 y 2 (DIN, TRA)
)


def _celdas_d_adjudicadas() -> list[dict]:
    """Las celdas-D con VEREDICTO SELLADO, con su n de celdas y su error.

    ACTO GEN2-MARCADOR-E-INFORME-1 · P1. Antes de este acto la clase 1 de la
    métrica rectora era una lista de DOS celdas-D escritas a mano en este
    archivo, con su CALC y su escala tecleados al lado. El piloto 3 adjudicó 15
    celdas en un tercer dominio y la métrica no se movió, porque nadie había
    añadido la tercera línea. Una métrica rectora que hay que editar a mano cada
    vez que el programa avanza mide al editor, no al programa.

    VALIDADA NO QUIERE DECIR ACERTADA. Una celda cuenta si su predicción se
    emitió antes de ver el dato y se comparó contra R con error sellado. El
    VEREDICTO de la celda-D -- `SIN-CANDIDATO-SUPERIOR` («nadie vence»),
    `FALSADOR-DEBIL`, o el día que lo haya, uno que vence -- NO entra en el
    conteo: un piloto que falsa una hipótesis validó exactamente tantas celdas
    como uno que la corrobora. Lo único que se exige es que el veredicto EXISTA
    y esté sellado, porque un veredicto ausente significa que nadie comparó.

    LA ESCALA SE DERIVA, NO SE TECLEA (§4.3, y el defecto es de factor 100: DIN
    emite en proporción y TRA/GOB en puntos porcentuales). El `margen_material`
    de la celda-D es el MAE del piso C2 en pp, sellado en el YAML. Se prueba el
    factor 1 y el factor 100 contra él y se adopta el que casa. Si NINGUNO casa,
    la celda-D NO cuenta y se declara con su motivo: preferimos una métrica que
    no sube a una que sube por una escala adivinada (PARO (d) del encargo).
    """
    salida = []
    if yaml is None:
        return salida
    for ruta in sorted(glob.glob(os.path.join(
            RAIZ, "data", "curacion-registro", "celdas-d", "*.yaml"))):
        try:
            with open(ruta, encoding="utf-8") as fh:
                d = (yaml.safe_load(fh) or {}).get("celda_d") or {}
        except (OSError, ValueError):
            continue
        rel = os.path.relpath(ruta, RAIZ)
        cid = d.get("id") or os.path.basename(ruta)
        veredicto = d.get("veredicto")
        if d.get("estado_decidibilidad") != "PUNTUADA" or not veredicto:
            salida.append({
                "celda_d": cid, "n_celdas": 0, "cuenta": False,
                "motivo": (f"estado_decidibilidad="
                           f"{d.get('estado_decidibilidad')!r}, veredicto="
                           f"{veredicto!r} -- sin veredicto sellado no hubo "
                           "comparación contra R"),
                "fuente": rel,
            })
            continue

        errores, calc_usado, soportes = {}, "", {}
        for ref in (d.get("momentos_holdout_refs") or []):
            if not isinstance(ref, str) or not ref.startswith("CALC-"):
                continue
            calc_id = ref.split("--", 1)[0]
            p = os.path.join(RAIZ, "data", "corrida0", calc_id, "resultados.json")
            if not os.path.exists(p):
                continue
            try:
                with open(p, encoding="utf-8") as fh:
                    res = json.load(fh).get("resultados", {})
            except (OSError, ValueError):
                continue
            for patron, modo in _PATRONES_ERROR_C2:
                if modo == "sufijo":
                    hit = {k[:-len(patron)]: v for k, v in res.items()
                           if k.endswith(patron) and isinstance(v, (int, float))}
                else:
                    hit = {k.split(patron, 1)[1]: v for k, v in res.items()
                           if patron in k and isinstance(v, (int, float))}
                if hit:
                    errores, calc_usado = hit, calc_id
                    soportes = {k[:-len("-SOPORTE")]: v for k, v in res.items()
                                if k.endswith("-SOPORTE")}
                    break
            if errores:
                break

        if not errores:
            salida.append({
                "celda_d": cid, "n_celdas": 0, "cuenta": False,
                "veredicto": veredicto,
                "motivo": ("veredicto sellado pero ningún RESULT de error por "
                           "celda localizado en sus momentos_holdout_refs "
                           f"({_PATRONES_ERROR_C2[0][0]} / "
                           f"{_PATRONES_ERROR_C2[1][0]})"),
                "fuente": rel,
            })
            continue

        # Las celdas FUERA-DE-SOPORTE declaradas ex ante no se comparan contra
        # nada: el árbitro las marca y aquí no cuentan.
        vivos = {k: v for k, v in errores.items()
                 if soportes.get(k, "PUNTUADA") == "PUNTUADA"}
        margen = d.get("margen_material")
        escala, factor = None, None
        if isinstance(margen, (int, float)) and vivos:
            mae = sum(vivos.values()) / len(vivos)
            for f, nombre in ((1.0, "PUNTOS-PORCENTUALES"), (100.0, "PROPORCION")):
                if abs(mae * f - margen) <= 1e-5:
                    escala, factor = nombre, f
                    break
        if factor is None:
            salida.append({
                "celda_d": cid, "n_celdas": 0, "cuenta": False,
                "veredicto": veredicto,
                "motivo": ("la escala no se derivó: ni el factor 1 ni el 100 "
                           f"reproducen margen_material={margen!r} desde "
                           f"{calc_usado}"),
                "fuente": rel,
            })
            continue

        e_pp = sorted(v * factor for v in vivos.values())
        n = len(e_pp)
        salida.append({
            "celda_d": cid,
            "n_celdas": n,
            "cuenta": True,
            "veredicto": veredicto,
            "champion_actual": d.get("champion_actual"),
            "dominio": d.get("dominio"),
            "unidad_objetivo": d.get("unidad_objetivo"),
            "error_mediano_pp": round(
                e_pp[n // 2] if n % 2 else (e_pp[n // 2 - 1] + e_pp[n // 2]) / 2, 3),
            "error_max_pp": round(max(e_pp), 3),
            "MAE_pp": round(sum(e_pp) / n, 3),
            "escala_cruda": escala,
            "escala_verificada_contra": f"margen_material={margen} (sellado en {rel})",
            "fuera_de_soporte": len(errores) - n,
            "brecha_anios": 0,
            "fuente": f"data/corrida0/{calc_usado}/resultados.json",
        })
    return salida


def _celdas_validadas() -> dict:
    """MÉTRICA RECTORA (firma de mesa 20/sep/2026): celdas cuya predicción se
    emitió ANTES de ver el dato y se comparó contra R con error sellado.

    TRES CLASES QUE NO SE FUNDEN EN UNA CIFRA (§4.3/§4.4: escalas y universos
    distintos no se promedian). Cada una con su n, su error mediano en pp, su
    instrumento y su BRECHA TEMPORAL al lado -- las brechas de 1, 2 y 3 años NO
    se promedian entre sí.

    LO QUE NO CUENTA, y por qué (el defecto que esta métrica existe para evitar
    es leer «N validadas» como «N aciertos»):
      * las filas `IDENTICO` del marcador (89) tienen M y R porque
        `emisor_vs_arbitro = EMISOR=ARBITRO` -- M y R son EL MISMO NÚMERO
        copiado, no una predicción contrastada. Cero de ellas es validación.
      * las 6 celdas de `formalidad` con piso y SIN `error_piso_pp`:
        CALC-PISO-PERSISTENCIA-ERROR-0001 se selló antes de que existieran. Su
        error es un CALC sucesor, no de este acto.
    """
    ruta = "data/corrida0/marcador-segmento.tsv"
    if not os.path.exists(os.path.join(RAIZ, ruta)):
        return {"error": f"AUSENTE: {ruta}"}
    filas = tsv_rows(os.path.join(RAIZ, ruta))
    cab, cuerpo = filas[0], filas[1:]
    ix = {k: cab.index(k) for k in cab}
    R = [dict(zip(cab, r)) for r in cuerpo]

    def mediana(v):
        v = sorted(v)
        n = len(v)
        if not n:
            return None
        return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2

    def anio(s):
        m = re.findall(r"(19|20)\d{2}", s or "")
        return int(re.findall(r"(?:19|20)\d{2}", s)[0]) if m else None

    # ── clase 1 · CRUCE vs R (pilotos 1 y 2, adoptados por firma) ──────────
    # El marcador trae M pero NO trae R para estas filas: el error por celda
    # vive en el CALC del árbitro del cruce, sellado. Se lee de ahí, con su
    # ESCALA DECLARADA -- DIN emite en PROPORCIÓN y TRA en PUNTOS PORCENTUALES;
    # confundirlas da un factor 100. La escala se verifica contra el
    # `margen_material` sellado del YAML de cada celda-D, no se teclea.
    # `clase_1_cruce_vs_R` publica SÓLO las celdas-D que cuentan: es un contrato
    # que ya tiene consumidor (`tests/test_celdas_validadas.py` recorre la lista
    # y lee `error_mediano_pp` de cada entrada), y una celda-D sin veredicto no
    # tiene esa clave. Las que NO cuentan no se callan -- salen en
    # `clase_1_celdas_d_sin_contar` con su motivo, que es lo que §2 pide: un
    # negativo con universo declarado, no un silencio.
    todas_las_celdas_d = _celdas_d_adjudicadas()
    cruces = [c for c in todas_las_celdas_d if c.get("cuenta")]
    sin_contar = [c for c in todas_las_celdas_d if not c.get("cuenta")]
    for c in cruces:
        inst = [r for r in R if r["celda_id"].startswith(f"CRUCE::{c['celda_d']}::")]
        c["n_adoptadas_en_marcador"] = sum(
            1 for r in inst if r["estado"] == "ADOPTADO-POR-FIRMA")
        # Una celda-D adjudicada puede NO tener filas en el marcador: el
        # derivador sólo publica cruces con `champion_actual: C2`, y el piloto 3
        # cerró en `NINGUNO`. La celda cuenta igual (se emitió antes y se comparó
        # después); lo que falta es su fila en la vista, que es
        # DECISIÓN-DE-MESA-PENDIENTE heredada de #961, no un hueco de conteo.
        c["instrumento"] = inst[0]["instrumento"] if inst else (
            f"celda-D {c['celda_d']} · SIN-FILA-EN-MARCADOR "
            f"(champion_actual={c.get('champion_actual')!r})")
    n_cruce = sum(c.get("n_celdas") or 0 for c in cruces)

    # ── clase 2 · PERSISTENCIA t-1 vs R (filas con error_piso_pp) ──────────
    ep = [r for r in R if r["error_piso_pp"]]
    por_inst: dict[str, list] = {}
    for r in ep:
        por_inst.setdefault(r["instrumento"], []).append(r)
    persist = []
    for inst, rs in sorted(por_inst.items()):
        e = [float(r["error_piso_pp"]) for r in rs]
        a_obj, a_piso = anio(inst), anio(rs[0]["piso_fuente"])
        persist.append({
            "instrumento": inst,
            "n_celdas": len(rs),
            "error_mediano_pp": round(mediana(e), 3),
            "error_max_pp": round(max(e), 3),
            "brecha_anios": (a_obj - a_piso) if (a_obj and a_piso) else None,
            "PERSISTE": sum(1 for r in rs if r["clase_persistencia"] == "PERSISTE"),
            "CAMBIA": sum(1 for r in rs if r["clase_persistencia"] == "CAMBIA"),
        })
    n_persist = len(ep)

    # Las 6 de formalidad: piso SIN error. No cuentan. Se declaran con universo.
    sin_error = [r for r in R
                 if r["piso"] and not r["error_piso_pp"] and "::formalidad::" in r["celda_id"]]

    # ── clase 3 · DUELO DE TRES, NACIONAL (CALC-TRIADA-0002) ───────────────
    pt = "data/corrida0/CALC-TRIADA-0002/resultados.json"
    triada = {"estado": f"AUSENTE: {pt}"}
    if os.path.exists(os.path.join(RAIZ, pt)):
        t = json.load(open(os.path.join(RAIZ, pt), encoding="utf-8")).get("resultados", {})
        def g(k):
            for kk, vv in t.items():
                if kk.endswith(k):
                    return vv
            return None
        def r3(x):
            return round(x, 3) if isinstance(x, (int, float)) else x
        triada = {
            "n_celdas": g("U3-N"),
            "MAE_M_pp": r3(g("MAE-M-PP")),
            "MAE_L_SOLO_pp": r3(g("MAE-L-SOLO-PP")),
            "MAE_L_CORPUS_pp": r3(g("MAE-L-CORPUS-PP")),
            "veredicto": g("VEREDICTO-GLOBAL"),
            "fuente": "CALC-TRIADA-0002/resultados.json",
        }

    # ── sub-cifra del dominio DINERO (la firma la exige explícitamente) ────
    din_cruce = next((c for c in cruces if c["celda_d"].startswith("DIN.")), {})
    din_persist = [p for p in persist if "ENIF" in p["instrumento"]]
    dinero = {
        "cruce_n": din_cruce.get("n_celdas"),
        "cruce_error_mediano_pp": din_cruce.get("error_mediano_pp"),
        "persistencia_n": sum(p["n_celdas"] for p in din_persist),
        "persistencia_error_mediano_pp": (
            round(mediana([float(r["error_piso_pp"]) for r in ep if "ENIF" in r["instrumento"]]), 3)
            if any("ENIF" in r["instrumento"] for r in ep) else None),
        "nota": "ENIF 2024; la brecha de persistencia es de 3 años y no se promedia "
                "con las de 1 y 2 años de ENVIPE/ENCIG",
    }

    # ── P1 · desglose por INSTRUMENTO y por TIPO (cruce / marginal) ────────
    # Conteos, no promedios: los errores de instrumentos distintos no se
    # promedian entre sí (§4.3) y aquí no se promedia ninguno.
    por_instrumento: dict[str, dict] = {}
    for c in cruces:
        k = c.get("instrumento") or "(sin fila en el marcador)"
        por_instrumento.setdefault(k, {"cruce": 0, "marginal": 0})["cruce"] += \
            c["n_celdas"]
    for r in ep:
        k = r["instrumento"]
        por_instrumento.setdefault(k, {"cruce": 0, "marginal": 0})["marginal"] += 1

    # ── P2 · el rótulo PROSPECTIVA/RETROSPECTIVA del marcador, sin sumar ───
    prosp = Counter(r.get("prospectividad", "(columna ausente)") for r in R)

    return {
        "total_celdas_validadas": n_cruce + n_persist,
        "desglose_por_clase": {
            "cruce_vs_R": n_cruce,
            "persistencia_t_menos_1_vs_R": n_persist,
            "duelo_tres_nacional": triada.get("n_celdas"),
        },
        "desglose_por_tipo": {
            "cruce": n_cruce,
            "marginal": n_persist,
            "nota": "un cruce y una marginal no son la misma unidad de trabajo; "
                    "el total de arriba las suma porque ambas son celdas "
                    "validadas, y este desglose existe para poder deshacer la suma",
        },
        "desglose_por_instrumento": por_instrumento,
        "prospectividad_del_marcador": {
            **dict(prosp),
            "nota": "columna derivada por tools/prospectividad.py desde los sellos. "
                    "PROSPECTIVA y RETROSPECTIVA NO se suman en una sola cifra "
                    "(firma de mesa 21/sep/2026); este bloque no trae total.",
        },
        "clase_1_cruce_vs_R": cruces,
        "clase_1_celdas_d_sin_contar": sin_contar,
        "clase_2_persistencia_vs_R": persist,
        "clase_3_duelo_tres_nacional": triada,
        "dominio_dinero": dinero,
        "NO_CUENTAN": {
            "identico_emisor_igual_arbitro": sum(1 for r in R if r["estado"] == "IDENTICO"),
            "formalidad_con_piso_sin_error": len(sin_error),
            "por_que": "IDENTICO tiene M == R por EMISOR=ARBITRO (mismo número copiado, "
                       "no predicción contrastada). Las de formalidad tienen piso pero su "
                       "error de persistencia no está medido: CALC sucesor.",
        },
        "universo_examinado": f"{len(cuerpo)} filas de {ruta} + 3 CALC sellados",
    }


#: Archivos que la derivación lee, para el bloque `universo` de `--json`
#: (D-16: ninguna cifra sale sin su SHA). No es una lista de dependencias de
#: import -- es el universo de DATO que la función recorre.
_ARCHIVOS_LEIDOS = (
    "data/corrida0/marcador-segmento.tsv",
    "data/curacion-registro/celdas-d/*.yaml",
    "data/corrida0/CALC-*/resultados.json (referidos desde las celdas-d y "
    "desde CALC-TRIADA-0002)",
)


def _universo() -> dict:
    sha = _sh("git rev-parse HEAD") or "NO-DERIVABLE"
    return {
        "sha": sha,
        "archivos_leidos": list(_ARCHIVOS_LEIDOS),
    }


def prospectividad_sub_cifras(cv: dict) -> tuple[int, int]:
    """PROSPECTIVA y RETROSPECTIVA del marcador, SIN sumarlas entre sí (firma
    de mesa 21/sep/2026). Devuelve el par (prospectiva, retrospectiva); las
    otras tres claves de `prospectividad_del_marcador`
    (`IDENTICO-EMISOR-ES-ARBITRO`, `SIN-EMISION`, `EMITIDA-SIN-R`) no entran
    en `celdas_validadas` -- son estado del marcador, no de la métrica."""
    p = cv.get("prospectividad_del_marcador", {})
    return int(p.get("PROSPECTIVA", 0) or 0), int(p.get("RETROSPECTIVA", 0) or 0)


def emitidas_sin_r(cv: dict) -> int:
    """Demanda: emisiones que esperan su R. No cuenta como validada."""
    p = cv.get("prospectividad_del_marcador", {})
    return int(p.get("EMITIDA-SIN-R", 0) or 0)


def linea(cv: dict | None = None) -> str:
    """La línea de una sola fila que imprime `--linea` y que abre
    `digesto_tramite.py --mesa`."""
    cv = cv if cv is not None else _celdas_validadas()
    prosp, retro = prospectividad_sub_cifras(cv)
    u = _universo()
    n = cv.get("total_celdas_validadas")
    return (f"celdas_validadas {n} (prospectiva {prosp} · retrospectiva {retro}) "
            f"@ {u['sha'][:8]}")


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="imprime el diccionario completo")
    ap.add_argument("--linea", action="store_true", help="imprime la línea de una sola fila")
    a = ap.parse_args(argv)

    cv = _celdas_validadas()
    if a.linea:
        print(linea(cv))
        return 0
    salida = dict(cv)
    salida["universo"] = _universo()
    print(json.dumps(salida, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
