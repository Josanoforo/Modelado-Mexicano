#!/usr/bin/env python3
"""tablero_programa.py -- deriva los indicadores del TABLERO DEL PROGRAMA desde el
arbol del repo. Cero cifras tecleadas: todo sale de archivos o de git.

Uso (desde la raiz del clon, con origin/main recien traido):
    python3 tools/tablero_programa.py            # markdown a stdout
    python3 tools/tablero_programa.py --json     # mismo contenido, JSON

Reglas que este script respeta (instrucciones v2.15):
  * A.13 -- cada negativo declara cuantos archivos examino.
  * v2.1 -- ninguna cifra esperada vive aqui; el script solo mide.
  * A.10 -- imprime el SHA contra el que derivo; sin SHA no hay tablero.
Dependencias: libreria estandar + PyYAML (requirements.txt).
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
import subprocess
import sys

# ACTO GEN2-DIN-CREDITO-PISOS-ENIF2021-1 (PR #943): `resultados_ids` de una corrida con
# 2 939 RESULT mide 209 856 bytes y revienta el tope de 131 072 del modulo csv.
# El tope es del lector, no del dato: se sube antes de leer cualquier vista.
csv.field_size_limit(sys.maxsize)
import tempfile
from collections import Counter
from datetime import date

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

import estado_comun as EC
import limpia_arbol as LA  # ACTO GEN2-T9 · P4(v)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
PD = "forense/prereg-duelo-v2/"


def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True).stdout.decode("utf-8", "replace").strip()


def leer(path: str) -> str:
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def tsv_rows(path: str):
    return [r for r in csv.reader(open(path, encoding="utf-8", errors="replace"), delimiter="\t")
            if r and not r[0].startswith("#")]


_ESTADO_CABECERA = re.compile(r"(?m)^ESTADO:\s*(\S+)")


def _estado_cola(texto: str) -> str:
    """Clasifica un archivo de `forense/encargos/cola/` para el tablero.

    NC-0252 (medido por `ACTO GEN2-VIGENCIA-DEUDA-1`, corregido por `ACTO
    GEN2-MANTENIMIENTO-3`): el vocabulario real es el de la cabecera
    `ESTADO:` (`.claude/commands/despacha.md`) -- CONSUMIDO / LISTO-<ENTORNO>
    / EN-CURSO / GATEADO / PARO-REPORTADO / INDICE-DE-COLA -- no el substring
    literal `"## CONSUMIDO"` en el cuerpo crudo, que un renglon de BITACORA
    que solo *menciona* un estado anterior (p.ej. "seguia LISTO-CAJA con el
    PR ya fusionado") puede falsear. Los archivos en formato viejo (pre
    patron 2-ter, sin cabecera `ESTADO:`) caen al heuristico anterior.
    """
    m = _ESTADO_CABECERA.search(texto)
    if m:
        estado = m.group(1).rstrip(".,;:")
        if estado.startswith("CONSUMIDO"):
            return "CONSUMIDO"
        if estado.startswith("LISTO"):
            return "LISTO"
        return "GATED"
    return "CONSUMIDO" if "## CONSUMIDO" in texto else ("LISTO" if "LISTO-" in texto else "GATED")


_NC_TOKENS_A14 = (
    "PARO-ENTORNO", "PARO-PREMISA", "FUERA-DE-PERÍMETRO", "SUSTITUIDO-POR:",
    "DIFERIDO-A:", "NO-VERIFICABLE-AQUÍ", "DECISIÓN-DE-MESA-PENDIENTE",
)


def _nc_por_razon() -> dict:
    """Censa `forense/no-corrido.tsv`, filas `estado == ABIERTA`, por el
    TOKEN DE A.14 que abre su columna `razon` -- prefijo exacto (A.16), no
    un corte por espacio y dos puntos (el defecto real: un parser que corta
    por ' ' o ':' pierde `DIFERIDO-A:E7` y `NO-VERIFICABLE-AQUÍ` contadas
    como prosa cuando sí llevan token)."""
    ruta = "forense/no-corrido.tsv"
    if not os.path.exists(ruta):
        return {"abiertas": 0, "por_token": {}, "prosa": 0}
    filas = [r for r in csv.reader(open(ruta, encoding="utf-8", errors="replace"),
                                    delimiter="\t", quoting=csv.QUOTE_NONE)
             if r and not r[0].startswith("#")]
    if not filas:
        return {"abiertas": 0, "por_token": {}, "prosa": 0}
    cab = filas[0]
    i_estado = cab.index("estado")
    i_razon = cab.index("razon")
    abiertas = [r for r in filas[1:] if len(r) > i_estado and r[i_estado] == "ABIERTA"]
    por_token = Counter()
    prosa = 0
    for r in abiertas:
        razon = r[i_razon] if len(r) > i_razon else ""
        token = next((t.rstrip(":") for t in _NC_TOKENS_A14 if razon.startswith(t)), None)
        if token:
            por_token[token] += 1
        else:
            prosa += 1
    return {"abiertas": len(abiertas), "por_token": dict(por_token), "prosa": prosa}


def _marcador_segmento_resumen() -> dict:
    """Filas de `data/corrida0/marcador-segmento.tsv` por `estado`, más
    `emision = EMITIDA-SIN-EVALUAR`, cruzadas con `tools/marcador_segmento.py
    --json` (`cobertura_de_piso`, `valor_anadido/evaluadas`,
    `veto_pisos_activo`). Cada número con su denominador (P1, lección 9.6:
    dos contadores que parecen fracción y no lo son)."""
    ruta = "data/corrida0/marcador-segmento.tsv"
    if not os.path.exists(ruta):
        return {"error": f"AUSENTE: {ruta}"}
    filas = tsv_rows(ruta)
    cab, cuerpo = filas[0], filas[1:]
    i_estado = cab.index("estado")
    i_emision = cab.index("emision")
    por_estado = dict(Counter(r[i_estado] for r in cuerpo))
    emitida_sin_evaluar = sum(1 for r in cuerpo if r[i_emision] == "EMITIDA-SIN-EVALUAR")
    try:
        j = json.loads(sh("python3 tools/marcador_segmento.py --json"))
    except Exception as exc:  # noqa: BLE001
        j = {"error": f"{type(exc).__name__}: {exc}"}
    return {
        "total_filas": len(cuerpo),
        "por_estado": por_estado,
        "emitida_sin_evaluar": f"{emitida_sin_evaluar} / {len(cuerpo)}",
        "cobertura_de_piso": f"{j.get('cobertura_de_piso')} / {len(cuerpo)}" if "error" not in j else j["error"],
        "valor_anadido_sobre_evaluadas": f"{j.get('valor_anadido')} / {j.get('evaluadas')}" if "error" not in j else j["error"],
        "veto_pisos_activo": j.get("veto_pisos_activo") if "error" not in j else j["error"],
    }


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
    if not os.path.exists(ruta):
        return {"error": f"AUSENTE: {ruta}"}
    filas = tsv_rows(ruta)
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
    cruces = _celdas_d_adjudicadas()
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
    n_cruce = sum(c.get("n_celdas") or 0 for c in cruces if c.get("cuenta"))

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
    if os.path.exists(pt):
        t = json.load(open(pt, encoding="utf-8")).get("resultados", {})
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
        if not c.get("cuenta"):
            continue
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


def _corridas_pendientes_de_contar() -> dict:
    """`corridas.tsv`: filas `estado == SELLADA` repartidas por
    `cuenta_gen2`, más el detalle de `PENDIENTE-DE-MESA` con su
    `resultado_replay` (P1)."""
    ruta = "data/corrida0/corridas.tsv"
    if not os.path.exists(ruta):
        return {"error": f"AUSENTE: {ruta}"}
    filas = tsv_rows(ruta)
    cab, cuerpo = filas[0], filas[1:]
    i_estado = cab.index("estado")
    i_cuenta = cab.index("cuenta_gen2")
    i_id = cab.index("corrida_id")
    i_replay = cab.index("resultado_replay")
    selladas = [r for r in cuerpo if r[i_estado] == "SELLADA"]
    por_cuenta = dict(Counter(r[i_cuenta] for r in selladas))
    pendientes_mesa = [{"corrida_id": r[i_id], "resultado_replay": r[i_replay]}
                       for r in selladas if r[i_cuenta] == "PENDIENTE-DE-MESA"]
    return {
        "selladas_total": len(selladas),
        "por_cuenta_gen2": por_cuenta,
        "pendientes_de_mesa": pendientes_mesa,
    }


def find_rules(o):
    if isinstance(o, dict):
        for v in o.values():
            r = find_rules(v)
            if r:
                return r
    if isinstance(o, list) and o and isinstance(o[0], dict) and "id" in o[0] and "entonces" in o[0]:
        return o
    return None


MARCA_INICIO = "<!-- TABLERO-DERIVADO:BEGIN -->"
MARCA_FIN = "<!-- TABLERO-DERIVADO:END -->"


def _marco_vigente(familia: str) -> tuple[str, str]:
    """(version, ruta) del marco `familia` de version maxima en el arbol.
    Deriva; no clava una version en el codigo (ACTO GEN2-E6)."""
    patron = re.compile(rf"marco-M-{familia}-v(\d+)_(\d+)\.tsv$")
    hallados = []
    for f in glob.glob(PD + f"marco-M-{familia}-v*.tsv"):
        m = patron.search(f)
        if m:
            hallados.append(((int(m.group(1)), int(m.group(2))), f))
    if not hallados:
        return "NO-ENCONTRADO", ""
    (mayor, menor), ruta = max(hallados)
    return f"v{mayor}_{menor}", ruta


def _contadores_gen2() -> tuple[dict, str]:
    """Los contadores GEN2 (§9 del plan v2.0) LEIDOS DE `corrida0 status`.

    El tablero no los recalcula por su cuenta: `corrida0.py` es la unica
    fuente y este script solo la muestra. Si `status` no puede derivar
    (falta la demanda, una validacion PARA), se declara el motivo -- nunca
    se rellena con ceros que aparentarian un programa sano.
    """
    try:
        import importlib.util
        ruta = os.path.join(RAIZ, "tools", "corrida0.py")
        spec = importlib.util.spec_from_file_location("corrida0_para_tablero", ruta)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        return mod.status(imprime=False), "python3 tools/corrida0.py status"
    except Exception as exc:  # noqa: BLE001 -- el tablero informa, no revienta
        return ({"error": f"{type(exc).__name__}: {exc}"},
                "python3 tools/corrida0.py status (no derivable en este arbol)")


def derivar_indicadores() -> dict[str, dict]:
    I: dict[str, dict] = {}

    def put(clave, valor, comando, nota=""):
        I[clave] = {"valor": valor, "comando": comando, "nota": nota}

    # ── 0 · procedencia ────────────────────────────────────────────────
    sha = sh("git rev-parse --short HEAD")
    put("sha", sha, "git rev-parse --short HEAD")
    put("fecha_commit", sh("git log -1 --format=%ad --date=short HEAD"), "git log -1 --format=%ad --date=short HEAD")
    put("es_origin_main", sh("git rev-parse HEAD") == sh("git rev-parse origin/main"),
        "git rev-parse HEAD == git rev-parse origin/main", "si False, el tablero no se deriva de main")
    _ramas_presentes, _fuente_ramas = EC.ramas_remotas_presentes(RAIZ)
    put("ramas_remotas_vivas", [r for r in _ramas_presentes if r != "main"],
        f"tools/estado_comun.py::ramas_remotas_presentes() -- {_fuente_ramas.replace(chr(96), chr(39))}",
        "'vivas' es historico del nombre de esta clave -- son ramas PRESENTES en origin "
        "(ACTO AUTOMATIZA-1-E2), no necesariamente PR abierto ni trabajo sin fusionar: "
        "una rama puede existir sin haber redactado aun su ADR")
    _ramas_detalle, _fuente_ramas_detalle = EC.ramas_remotas_detalle(RAIZ)
    put("ramas_remotas_detalle", _ramas_detalle,
        f"tools/estado_comun.py::ramas_remotas_detalle() -- {_fuente_ramas_detalle}",
        "nombre + commits delante/detras de origin/main + fecha del ultimo commit, "
        "por cada rama presente en origin distinta de main (P1, GEN2-TABLERO-SENAL-1)")

    # ACTO GEN2-T9 · P4(v): `NO-VERIFICABLE-SIN-GH` es un ESTADO, no un cero.
    # `tools/limpia_arbol.py` ya lo distinguia y el tablero no lo leia: sin
    # `gh` en el entorno, la politica de cero ramas (A.14) queda SIN VERIFICAR,
    # y un tablero que publicara `0` ahi estaria afirmando que se cumple. Los
    # tres estados posibles se publican con ese nombre -- `VERIFICADO`,
    # `NO-VERIFICABLE-SIN-GH`, `ERROR` -- porque colapsarlos a un numero es
    # justo como un negativo no examinado se lee como positivo (A.13).
    try:
        _pol = LA.ramas_fuera_de_politica()
        _estado_pol = "VERIFICADO" if _pol.get("verificable") else "NO-VERIFICABLE-SIN-GH"
        _n_pol = _pol.get("n")
        _detalle_pol = _pol.get("detalle") or []
        _nota_pol = _pol.get("nota") or ""
        _cmd_pol = _pol.get("comando", "")
    except Exception as _exc:      # el tablero no revienta por un tool auxiliar
        _estado_pol, _n_pol, _detalle_pol = "ERROR", None, []
        _nota_pol = f"{type(_exc).__name__}: {_exc}"
        _cmd_pol = "tools/limpia_arbol.py::ramas_fuera_de_politica()"
    put("ramas_fuera_de_politica_estado", _estado_pol,
        f"tools/limpia_arbol.py::ramas_fuera_de_politica() -- {_cmd_pol}",
        _nota_pol or "VERIFICADO: se consultaron los PR abiertos de verdad")
    put("ramas_fuera_de_politica_n", _n_pol,
        f"tools/limpia_arbol.py::ramas_fuera_de_politica() -- {_cmd_pol}",
        "null cuando el estado NO es VERIFICADO -- un null declarado, nunca un 0 "
        "que se leeria como 'la politica se cumple'")
    put("ramas_fuera_de_politica_detalle", _detalle_pol,
        f"tools/limpia_arbol.py::ramas_fuera_de_politica() -- {_cmd_pol}",
        "vacio cuando no es verificable; no distingue por si solo -- se lee "
        "junto a `ramas_fuera_de_politica_estado`")

    # ── 1 · motor ─────────────────────────────────────────────────────
    t = leer("milpa/tramite.yaml")
    ids = re.findall(r"^  - id: (\S+)", t, re.M)
    put("motor_reglas", len(ids), "grep -cE '^  - id: ' milpa/tramite.yaml")
    put("motor_clase_asignado_lineas", int(sh("grep -c 'clase: ASIGNADO' milpa/tramite.yaml") or 0),
        "grep -c 'clase: ASIGNADO' milpa/tramite.yaml", "incluye las conservadas como historia (refutadas/sustituidas)")
    put("motor_conductas_medido", int(sh("grep -c 'MEDIDO·' milpa/tramite.yaml") or 0), "grep -c 'MEDIDO·' milpa/tramite.yaml")
    if yaml:
        R = find_rules(yaml.safe_load(t)) or []
        sin_dato, con_dato, tiers = [], [], Counter()
        for r in R:
            clases = [str(c.get("clase", "")) for c in r.get("entonces", []) if isinstance(c, dict)]
            (con_dato if any(x.startswith("MEDIDO") for x in clases) else sin_dato).append(r["id"])
            tiers[str(r.get("tier"))] += 1
        put("motor_reglas_con_dato", len(con_dato), "python: reglas con >=1 conducta clase MEDIDO*")
        put("motor_reglas_sin_dato", sin_dato, "python: reglas cuyas conductas son todas ASIGNADO",
            "sin instrumento: 0 aciertos de e.firma vigente en 350 832 filas (FP-329 (e), 6/sep); "
            "gobierna FP-273 (3/sep): conservar. Razon derivada (ACTO MAESTRA38-SELLO-3, 7/sep/2026), "
            "no 'sin acto asignado' -- MAESTRA35-L6/MAESTRA38-LOTE-CRUCE (COERCITIVO) ya corrieron contra "
            "esta regla y volvieron con negativo de universo, no con la fuente.")
        put("motor_tiers", dict(tiers), "python: Counter(tier) sobre milpa/tramite.yaml")
    put("modelo_reglas_canon", sh("python3 tests/validador_registro_ids.py 2>/dev/null | tail -1"),
        "python3 tests/validador_registro_ids.py | tail -1", "las 49 del modelo-decision; el motor implementa un subconjunto")

    # ── 2 · propuesta (acumulador) ─────────────────────────────────────
    p = leer("milpa/tramite-ola5-propuesta-v0.yaml")
    put("propuesta_entradas", len(re.findall(r"^  - id: ", p, re.M)), "grep -cE '^  - id: ' milpa/tramite-ola5-propuesta-v0.yaml")
    for k in ("PENDIENTE-DE-MESA", "SELLADA", "MEDIA", "FUERTE"):
        put(f"propuesta_tier_{k}", len(re.findall(rf"^    tier: {k}", p, re.M)), f"grep -cE '^    tier: {k}' milpa/tramite-ola5-propuesta-v0.yaml",
            "cuenta por entrada (indentacion 4, una por bloque `- id:`), no por linea: la 51a `tier:` del archivo vive a indentacion 6, anidada dentro de la propia entrada `con_registro_encig2025`")
    put("propuesta_situacion_refutada", len(re.findall(r"^\s+situacion: REFUTADA", p, re.M)), "grep -cE '^\\s+situacion: REFUTADA' milpa/tramite-ola5-propuesta-v0.yaml")
    put("propuesta_celdas_por_ejes", len(re.findall(r"^\s+- \{celda: ", p, re.M)), "grep -cE '^\\s+- \\{celda: ' milpa/tramite-ola5-propuesta-v0.yaml",
        "celdas con IC por ejes (entradas *_ejes_*)")

    # ── 3 · procedencia (coeficientes) ─────────────────────────────────
    if yaml:
        d = yaml.safe_load(leer("milpa/procedencia.yaml"))
        put("coef_generador_sellados", len(d.get("coeficientes_generador_sellados", [])), "yaml: len(coeficientes_generador_sellados)")
        put("asignados_probabilidad", len(d.get("asignados_probabilidad", [])), "yaml: len(asignados_probabilidad)", "reglas del modelo con p ASIGNADO fuera del motor")
        put("rutas_coeficiente", d.get("rutas_estimabilidad_coeficiente", {}).get("reparto"), "yaml: rutas_estimabilidad_coeficiente.reparto")

    # ── 4 · corredor (duelo M/L vs R) ──────────────────────────────────
    # El marco vigente se DERIVA (version maxima presente en el arbol), no se
    # fija a mano: hasta ACTO GEN2-E6 (8/sep/2026) estas dos lineas apuntaban
    # a `v1_2` mientras el marco vigente ya era `v1_3` -- un tablero que mide
    # un marco superado informa de un programa que ya no existe.
    v_sort, sorteado = _marco_vigente("sorteado")
    v_cong, congelado = _marco_vigente("congelado")
    put("marco_vigente_sorteado", v_sort, "max(version) de forense/prereg-duelo-v2/marco-M-sorteado-v1_*.tsv")
    put("marco_vigente_congelado", v_cong, "max(version) de forense/prereg-duelo-v2/marco-M-congelado-v1_*.tsv",
        "asimetria REAL del arbol, no un error de este script: el sorteado llego a v1_3 y el congelado se quedo en v1_2")
    sort = [r[0] for r in tsv_rows(sorteado) if r[0] != "id"]
    cong = [r[0] for r in tsv_rows(congelado) if r[0] != "id"]
    Rc = [i for i in sort if os.path.exists(PD + f"corridas-R/{i}.json")]
    Mc = [i for i in sort if glob.glob(PD + f"corridas-M/M-{i}*.json")]
    Lc = [i for i in sort if glob.glob(PD + f"corridas-L/L-{i}-M__*.json")]
    lmr = [i for i in sort if i in Rc and i in Mc and i in Lc]
    put("marco_congelado", len(cong), f"filas de {os.path.basename(congelado)} sin '#'")
    put("marco_sorteado", len(sort), f"filas de {os.path.basename(sorteado)} sin '#'",
        "clave renombrada desde `marco_v1_2_sorteado` (ACTO GEN2-E6): el nombre "
        "ya no clava una version en el indicador")
    put("celdas_con_R", len(Rc), "ls corridas-R/<id>.json por id sorteado")
    put("celdas_con_M", len(Mc), "ls corridas-M/M-<id>*.json por id sorteado")
    put("celdas_con_L", len(Lc), "ls corridas-L/L-<id>-M__*.json por id sorteado")
    put("celdas_puntuables_LMR", len(lmr), "interseccion R∩M∩L sobre el sorteado", "LA SEÑAL: celdas puntuadas")
    put("celdas_sin_LMR", sorted(set(sort) - set(lmr)), "sorteado − (R∩M∩L)")
    put("dominios_sorteado", {k: sum(1 for i in sort if i.startswith(k)) for k in ("TRA", "CIV", "DIN", "FAM")}, "prefijo de id")
    put("L_capturas_total", len(glob.glob(PD + "corridas-L/L-*.json")), "ls corridas-L/L-*.json | wc -l")
    put("L_capturas_v1_2", int(sh(f"grep -l sha256_prompt {PD}corridas-L/L-*.json | wc -l") or 0), "grep -l sha256_prompt corridas-L/L-*.json | wc -l")
    put("scoreboards", sorted(os.path.basename(f) for f in glob.glob(PD + "scoreboard*")), "ls scoreboard*", "v1_2 aparece cuando N3 cierra")

    # ── 5 · corpus ────────────────────────────────────────────────────
    put("manifiesto_ids", int(sh("grep -c '^- id: ' data/manifiesto.yaml") or 0), "grep -c '^- id: ' data/manifiesto.yaml")
    put("payloads_verificados_ultimo_registro", sh("grep -rhoE 'data_raw: coincide=[0-9]+[^|]{0,40}' forense/notas/2026-09-0*.md | tail -1"),
        "grep -rhoE 'data_raw: coincide=...' forense/notas/2026-09-0*.md | tail -1", "solo se re-mide en caja con corpus (tests/manifiesto.py --verifica)")
    rows = tsv_rows("data/cola-adquisicion-v1_0.tsv")
    put("cola_adquisicion_estados", dict(Counter(r[1].split(" REL-")[0] for r in rows[1:])), "columna 2 de data/cola-adquisicion-v1_0.tsv")
    put("registro_curador_filas", int(sh("grep -vc '^#' data/curacion-registro/cola-adquisicion-registro.tsv") or 0), "grep -vc '^#' data/curacion-registro/cola-adquisicion-registro.tsv")
    put("relaciones_filas", int(sh("grep -vc '^#' data/curacion-registro/relaciones.tsv") or 0), "grep -vc '^#' data/curacion-registro/relaciones.tsv")
    put("inventario_reactivos_v1_2", int(sh("grep -vc '^#' data/inventario-reactivos-v1_2.tsv") or 0), "grep -vc '^#' data/inventario-reactivos-v1_2.tsv")

    # ── 6 · gobernanza y aparato ───────────────────────────────────────
    put("adr_max", EC.adr_max(RAIZ),
        "tools/estado_comun.py::adr_max() -- equivalente a "
        "grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1")
    put("fp_max", EC.fp_max(RAIZ),
        "tools/estado_comun.py::fp_max() -- equivalente a "
        "grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | grep -oE '[0-9]+' | sort -n | tail -1")
    hoy = date.today()
    abiertas = []
    for r in csv.reader(open("forense/firmas-pendientes.tsv", encoding="utf-8", errors="replace"), delimiter="\t"):
        if len(r) > 5 and EC.es_abierta(r[5]):
            try:
                edad = (hoy - date.fromisoformat(r[3][:10])).days
            except Exception:
                edad = None
            abiertas.append({"id": r[0], "creado": r[3][:10], "dias": edad, "que": r[1][:140]})
    put("fp_abiertas", abiertas,
        "tools/estado_comun.py::es_abierta() sobre columna 6 -- ABIERTA con o sin glosa "
        "(ACTO AUTOMATIZA-1-E2; antes comparaba columna==ABIERTA a secas, ciego a la glosa)",
        "WARN de T-FIRMAS en cada corrida")
    enc = glob.glob("forense/encargos/*.md")
    cons = sum(1 for f in enc if "## CONSUMIDO" in leer(f))
    put("encargos_archivados", len(enc), "ls forense/encargos/*.md | wc -l")
    put("encargos_consumidos", cons, "grep -l '## CONSUMIDO' forense/encargos/*.md | wc -l")
    cola = {}
    # ACTO GEN2-DOCS-ALINEACION-2, 14/sep/2026: el glob plano no recorria
    # los subdirectorios de paquetes (p.ej. forense/encargos/cola/2026-09-11-
    # GEN2-POST-693/*.md) -- se corrige SOLO esa omision (recursive=True +
    # clave por ruta relativa, para no colisionar basenames entre paquetes),
    # cero refactorizacion del resto de la funcion.
    for f in sorted(glob.glob("forense/encargos/cola/**/*.md", recursive=True)):
        tt = leer(f)
        clave = os.path.relpath(f, "forense/encargos/cola")
        cola[clave] = _estado_cola(tt)
    put("cola_encargos", cola, "forense/encargos/cola/**/*.md (recursivo): cabecera 'ESTADO:' real "
        "(CONSUMIDO / LISTO-* / EN-CURSO / GATEADO / PARO-REPORTADO), y solo si el archivo no trae "
        "esa cabecera (formato viejo, pre patron 2-ter) cae al heuristico por substring "
        "'## CONSUMIDO' / 'LISTO-' / otro=GATED -- NC-0252, ACTO GEN2-MANTENIMIENTO-3")
    put("skills", sorted(os.path.basename(f)[:-3] for f in glob.glob(".claude/commands/*.md")), "ls .claude/commands/")
    # P2 (GEN2-TABLERO-SENAL-1): version maxima presente en el arbol, de
    # CUALQUIER familia `instrucciones-proyecto-v<mayor>[_<menor>].md`, sin
    # sufijo `-HISTORIA`/`-DELTA` (el propio patron de nombre ya los excluye:
    # `v2_14-HISTORIA.md` no calza `v(\d+)(?:_(\d+))?\.md$`). El cuerpo
    # curado deja de escribir la version a mano -- cita esta clave.
    _ivig = re.compile(r"instrucciones-proyecto-v(\d+)(?:_(\d+))?\.md$")
    _ivers = []
    for f in glob.glob("instrucciones-proyecto-v*.md"):
        m = _ivig.search(os.path.basename(f))
        if m:
            _ivers.append((int(m.group(1)), int(m.group(2) or 0)))
    put("instrucciones_vigentes", f"v{max(_ivers)[0]}.{max(_ivers)[1]}" if _ivers else None,
        "ls instrucciones-proyecto-v*.md | version maxima (mayor, menor), sin sufijo -HISTORIA/-DELTA")
    put("para_v2_13_entradas", int(sh("grep -c 'PARA-v2.13' forense/hallazgos.md") or 0), "grep -c 'PARA-v2.13' forense/hallazgos.md", "v2.13 se entrega con >=3")
    put("hallazgos_entradas", int(sh("grep -c '^- \\*\\*2026' forense/hallazgos.md") or 0), "grep -c '^- **2026' forense/hallazgos.md")
    put("reports_tematicos", len(glob.glob("corpus/reports/*.md")), "ls corpus/reports/*.md | wc -l")
    put("forenses", len(glob.glob("corpus/forense/*.md")), "ls corpus/forense/*.md | wc -l")
    dig = sorted(glob.glob("forense/digesto/DIGESTO-*.md"))
    put("digesto_ultimo", os.path.basename(dig[-1]) if dig else None, "ls forense/digesto/DIGESTO-*.md | tail -1")
    # `hito_d_historico` RETIRADO (ACTO GEN2-E6, 8/sep/2026). Era una tarjeta
    # narrada con la receta rota: apuntaba a `canon/estado-programa-v1_10.md`,
    # luego a `v1_11`, y las dos versiones estan fuera del arbol (`T01`,
    # `ADR-339`), asi que el `grep` devolvia cadena vacia sin avisar --
    # un negativo de un comando que examino CERO archivos, que es justo lo
    # que A.13 prohibe tratar como resultado. Defecto ya asentado como `B22`
    # y `§7·D5` en `forense/tablero/TABLERO-PROGRAMA.md`. No se "arregla" la
    # ruta: el propio indicador declaraba "NO es la señal", y la cifra que
    # perseguia vive en `canon/modelo-decision-v4_0.md`.
    put("commits", int(sh("git rev-list --count HEAD") or 0), "git rev-list --count HEAD")
    put("prs_fusionados", int(sh("git log --merges --format=%s HEAD | grep -c 'pull request'") or 0), "git log --merges --format=%s HEAD | grep -c 'pull request'")
    put("suite", "correr: python3 tests/check.py --baseline | tail -6 (no se corre aqui: tarda; pega la salida cruda)", "python3 tests/check.py --baseline")

    # ── 7 · GEN2 (derivado de `corrida0 status`) ───────────────────────
    # ACTO GEN2-E6 · AUTOMATIZA-GEN2-2: el tablero deja de contar GEN2 a
    # ojo y lo lee del CLI. `0 / N` explicito es la lectura CORRECTA hoy --
    # el aparato existe antes que las corridas, y un tablero que ocultara
    # el cero estaria informando de un avance que nadie midio.
    gen2, comando_gen2 = _contadores_gen2()
    for clave, valor in gen2.items():
        put(f"gen2_{clave}", valor, comando_gen2)

    # ── 8 · MÉTRICA RECTORA + marcador por segmento y corridas pendientes ──
    # `celdas_validadas` es la métrica rectora del programa por firma de mesa
    # del 20/sep/2026, y por eso va PRIMERA en el bloque derivado (ACTO
    # GEN2-SENAL-1 · P1). Se deriva del marcador y de tres CALC sellados.
    put("celdas_validadas", _celdas_validadas(),
        "data/corrida0/marcador-segmento.tsv + CALC-{DIN-AHORRO-SOLO-INFORMAL,TRA-EVADE-NORMA-SXD}-ARBITRO-CRUCE-0001 "
        "+ CALC-TRIADA-0002 (resultados.json sellados)",
        "métrica rectora (firma de mesa 20/sep/2026); tres clases que NO se funden: "
        "cruce vs R, persistencia t-1 vs R, duelo de tres nacional")
    put("marcador_segmento", _marcador_segmento_resumen(),
        "tools/marcador_segmento.py --json + data/corrida0/marcador-segmento.tsv (columnas estado/emision)")
    put("corridas_pendientes_de_contar", _corridas_pendientes_de_contar(),
        "data/corrida0/corridas.tsv: SELLADA por cuenta_gen2, y detalle de PENDIENTE-DE-MESA")

    # ── 9 · NC por razon, token de A.14 (P5) ────────────────────────────
    put("nc_por_razon", _nc_por_razon(),
        "forense/no-corrido.tsv: filas ABIERTA por token de A.14 (prefijo exacto, A.16)")

    return I


def _v(I, k):
    return I[k]["valor"] if k in I else None


def _linea_celdas_validadas(cv: dict) -> str:
    """Primera línea del bloque derivado: la MÉTRICA RECTORA (firma de mesa
    20/sep/2026). Las tres clases se imprimen POR SEPARADO y cada una lleva su
    instrumento y su brecha temporal al lado; no hay un solo error promedio,
    porque promediar brechas de 1, 2 y 3 años y escalas distintas sería
    exactamente la lectura que esta línea existe para impedir."""
    if not cv or "error" in cv:
        return f"- **Celdas validadas (métrica rectora).** {cv.get('error', '(no derivable)')}"
    d = cv["desglose_por_clase"]
    L = [f"- **Celdas validadas (métrica rectora, firma de mesa 20/sep/2026).** "
         f"`{cv['total_celdas_validadas']}` celdas con predicción emitida antes de ver el dato "
         f"y error sellado contra R "
         f"(cruce `{d['cruce_vs_R']}` + persistencia `{d['persistencia_t_menos_1_vs_R']}`). "
         f"**No es «N aciertos»: es N celdas con error CONOCIDO.** Tres clases, sin fundir:"]

    for c in cv["clase_1_cruce_vs_R"]:
        if "estado" in c:
            L.append(f"  - *cruce vs R* · `{c['celda_d']}`: {c['estado']}")
            continue
        L.append(
            f"  - *cruce vs R* · `{c['celda_d']}` · n `{c['n_celdas']}` · champion `{c['champion']}` · "
            f"error mediano `{c['error_mediano_pp']}` pp (máx `{c['error_max_pp']}` pp) · "
            f"brecha `{c['brecha_anios']}` años (misma ola) · escala cruda del CALC "
            f"`{c['escala_cruda']}` · `{c['fuente']}`")

    for p in cv["clase_2_persistencia_vs_R"]:
        L.append(
            f"  - *persistencia t−1 vs R* · `{p['instrumento']}` · n `{p['n_celdas']}` · "
            f"error mediano `{p['error_mediano_pp']}` pp (máx `{p['error_max_pp']}` pp) · "
            f"**brecha `{p['brecha_anios']}` años** · PERSISTE `{p['PERSISTE']}` / CAMBIA `{p['CAMBIA']}`")

    t = cv["clase_3_duelo_tres_nacional"]
    if "estado" in t:
        L.append(f"  - *duelo de tres, nacional* · {t['estado']}")
    else:
        L.append(
            f"  - *duelo de tres, nacional* · n `{t['n_celdas']}` · "
            f"MAE `M` `{t['MAE_M_pp']}` pp · `L_SOLO` `{t['MAE_L_SOLO_pp']}` pp · "
            f"`L_CORPUS` `{t['MAE_L_CORPUS_pp']}` pp · veredicto `{t['veredicto']}` · "
            f"NO se suma a las otras dos clases (otro universo, otro estimando) · `{t['fuente']}`")

    dn = cv["dominio_dinero"]
    L.append(
        f"  - *sub-cifra del dominio DINERO* · cruce n `{dn['cruce_n']}` (error mediano "
        f"`{dn['cruce_error_mediano_pp']}` pp) · persistencia n `{dn['persistencia_n']}` "
        f"(error mediano `{dn['persistencia_error_mediano_pp']}` pp) · {dn['nota']}")

    nc = cv["NO_CUENTAN"]
    L.append(
        f"  - *NO cuentan* · `{nc['identico_emisor_igual_arbitro']}` filas `IDENTICO` "
        f"(M == R porque `EMISOR=ARBITRO`: el mismo número copiado, no una predicción contrastada) · "
        f"`{nc['formalidad_con_piso_sin_error']}` celdas de `formalidad` con piso y sin "
        f"`error_piso_pp` (su error es un CALC sucesor) · universo examinado: {cv['universo_examinado']}")
    return "\n".join(L)


def render_bloque_vivo(I: dict[str, dict]) -> str:
    """Construye el bloque factual committeado a partir del dict de derivar_indicadores().

    Solo hechos mecanicos y estables entre corridas -- sin cifras efimeras
    (edad en dias de FP, ramas remotas presentes), que siguen disponibles en
    la salida interactiva normal (markdown/--json) pero no aqui.
    """
    fp_ids = ", ".join(a["id"] for a in (_v(I, "fp_abiertas") or [])) or "(ninguna)"
    # P3 (GEN2-TABLERO-SENAL-1): la cola deja de listar las 64 lineas de
    # CONSUMIDO -- solo los estados != CONSUMIDO, mas el conteo de consumidos.
    cola = _v(I, "cola_encargos") or {}
    cola_no_consumidos = {k: v for k, v in cola.items() if v != "CONSUMIDO"}
    cola_n_consumidos = sum(1 for v in cola.values() if v == "CONSUMIDO")
    cola_txt = "\n".join(f"  - `{k}`: {v}" for k, v in cola_no_consumidos.items()) or "  (vacía)"

    ms = _v(I, "marcador_segmento") or {}
    ms_estado = ms.get("por_estado", {})
    ms_estado_txt = " · ".join(f"{k} `{v}`" for k, v in sorted(ms_estado.items())) or "(sin filas)"

    cpc = _v(I, "corridas_pendientes_de_contar") or {}
    cpc_cuenta = cpc.get("por_cuenta_gen2", {})
    cpc_cuenta_txt = " · ".join(f"`{k}` {v}" for k, v in sorted(cpc_cuenta.items())) or "(sin filas)"
    cpc_pend_txt = "\n".join(
        f"  - `{p['corrida_id']}`: `{p['resultado_replay']}`"
        for p in cpc.get("pendientes_de_mesa", [])
    ) or "  (ninguna)"

    ramas_detalle = _v(I, "ramas_remotas_detalle") or []
    ramas_n = len(ramas_detalle)
    ramas_txt = "\n".join(
        f"  - `{r['nombre']}`: {r['delante_de_main']} delante / {r['detras_de_main']} detrás de main · "
        f"último commit `{r['fecha_ultimo_commit']}`"
        for r in ramas_detalle
    ) or "  (ninguna)"
    if ramas_n > 0:
        ramas_cabecera = f"**{ramas_n} rama(s) presente(s) en origin (política de cero)**"
    else:
        ramas_cabecera = "0 ramas presentes en origin (política de cero cumplida)"

    partes = []
    partes.append(MARCA_INICIO)
    partes.append("## Estado vivo derivado")
    partes.append("")
    partes.append(_linea_celdas_validadas(_v(I, "celdas_validadas") or {}))
    partes.append(
        f"- **Procedencia.** SHA `{_v(I, 'sha')}` · fecha del commit `{_v(I, 'fecha_commit')}` · "
        f"¿árbol == origin/main? `{_v(I, 'es_origin_main')}`."
    )
    partes.append(
        f"- **Motor.** reglas totales `{_v(I, 'motor_reglas')}` · "
        f"reglas con dato (>=1 conducta MEDIDO*) `{_v(I, 'motor_reglas_con_dato')}` · "
        f"reglas sin dato `{len(_v(I, 'motor_reglas_sin_dato') or [])}` · "
        f"conductas MEDIDO* `{_v(I, 'motor_conductas_medido')}` · "
        f"tiers `{_v(I, 'motor_tiers')}`."
    )
    partes.append(
        f"- **Marcador por segmento.** filas por estado: {ms_estado_txt} (total `{ms.get('total_filas')}`) · "
        f"cobertura de piso `{ms.get('cobertura_de_piso')}` · "
        f"valor añadido / evaluadas `{ms.get('valor_anadido_sobre_evaluadas')}` · "
        f"celdas `emision = EMITIDA-SIN-EVALUAR` `{ms.get('emitida_sin_evaluar')}` · "
        f"`veto_pisos_activo` `{ms.get('veto_pisos_activo')}`."
    )
    partes.append(
        f"- **Corridas selladas que no cuentan todavía.** por `cuenta_gen2`: {cpc_cuenta_txt} "
        f"(selladas total `{cpc.get('selladas_total')}`) · `PENDIENTE-DE-MESA`:\n{cpc_pend_txt}"
    )
    partes.append(
        f"- **Ramas presentes en origin.** {ramas_cabecera}:\n{ramas_txt}"
    )
    partes.append(
        f"- **Corredor LEGACY (eje x = ∅, GO-MARCADOR).** el marcador por segmento es la línea de arriba. "
        f"marco vigente `marco-M-{_v(I, 'marco_vigente_sorteado')}` sorteado / "
        f"`marco-M-{_v(I, 'marco_vigente_congelado')}` congelado (derivado del árbol) · "
        f"celdas sorteadas `{_v(I, 'marco_sorteado')}` · "
        f"celdas con M `{_v(I, 'celdas_con_M')}` · con R `{_v(I, 'celdas_con_R')}` · con L `{_v(I, 'celdas_con_L')}` · "
        f"celdas puntuables (M∩R∩L) `{_v(I, 'celdas_puntuables_LMR')}` · "
        f"celdas sin cobertura completa `{len(_v(I, 'celdas_sin_LMR') or [])}`."
    )
    partes.append(
        f"- **Corpus lógico.** entradas del manifiesto `{_v(I, 'manifiesto_ids')}` · "
        f"filas de registro de curación `{_v(I, 'registro_curador_filas')}` · "
        f"filas de relaciones `{_v(I, 'relaciones_filas')}` · "
        f"filas del inventario de reactivos v1.2 `{_v(I, 'inventario_reactivos_v1_2')}`."
    )
    partes.append(
        f"- **Gobernanza operativa.** ADR máximo `{_v(I, 'adr_max')}` · FP máximo `{_v(I, 'fp_max')}` · "
        f"FP abiertas: {fp_ids} · "
        f"encargos archivados `{_v(I, 'encargos_archivados')}` (consumidos `{_v(I, 'encargos_consumidos')}`) · "
        f"instrucciones vigentes `{_v(I, 'instrucciones_vigentes')}` · "
        f"cola de encargos (solo estados != CONSUMIDO; consumidos `{cola_n_consumidos}`):\n{cola_txt}"
    )
    nc = _v(I, "nc_por_razon") or {}
    nc_tok_txt = " · ".join(f"`{k}` {v}" for k, v in sorted(nc.get("por_token", {}).items())) or "(ninguno)"
    partes.append(
        f"- **NC abiertas por razón (token A.14, prefijo exacto).** abiertas `{nc.get('abiertas')}` · "
        f"por token: {nc_tok_txt} · prosa (sin token reconocible) `{nc.get('prosa')}`."
    )
    partes.append(
        f"- **GEN2 (derivado de `corrida0 status`).** corridas selladas "
        f"`{_v(I, 'gen2_N_corridas_selladas')}` / requeridas `{_v(I, 'gen2_N_corridas_requeridas')}` · "
        f"resultados sellados `{_v(I, 'gen2_N_resultados_sellados')}` / activos "
        f"`{_v(I, 'gen2_N_resultados_activos')}` · pendientes `{_v(I, 'gen2_N_resultados_pendientes')}` · "
        f"dependencias numéricas legacy activas `{_v(I, 'gen2_dependencias_numericas_legacy_activas')}` · "
        f"validación independiente `{_v(I, 'gen2_resultados_con_validacion_independiente')}` · "
        f"diferencias materiales `{_v(I, 'gen2_diferencias_materiales')}` · "
        f"NC- abiertas `{_v(I, 'gen2_no_corrido_abiertas')}` · "
        f"replays LEGACY-GEN1 sellados `{_v(I, 'gen2_replays_legacy_sellados')}` (no cuentan). "
        f"El `0 / N` es la lectura correcta: el aparato se construyó antes que las corridas."
    )
    # ACTO GEN2-RELEVO-RECONCILIA-1 · P4 (la mitad que faltaba: el encargo
    # pide el desglose en `status` Y en el tablero). Las claves llegan solas
    # con prefijo `gen2_` desde `corrida0 status`, así que esta línea sólo
    # las RINDE: no recalcula nada y no puede discrepar del contador.
    # Aditiva: las sub-cifras suman el total de la línea de arriba, que no
    # cambia de nombre ni de valor. `T45 T-LEGACY-DESGLOSE-SUMA` exige la
    # suma; si una clase falta aquí, se imprime como `(sin desglose)` en vez
    # de mentir por omisión.
    _CLASES_LEGACY = ("motor", "procedencia", "catalogo_de_momentos",
                      "marco_del_duelo", "celdas_D", "otro")
    _desg = [(c, _v(I, f"gen2_legacy_activas_por_consumidor__{c}"))
             for c in _CLASES_LEGACY]
    if all(v is not None for _, v in _desg):
        _txt = " · ".join(f"{c.replace('_', ' ')} `{v}`" for c, v in _desg)
        _suma = sum(int(v) for _, v in _desg)
        partes.append(
            f"- **Legacy activas por consumidor (desglose aditivo del contador "
            f"de arriba).** {_txt} — suman `{_suma}`, el total. Los cinco "
            f"consumidores son RELEVABLES: ninguno se declara fuera del "
            f"contador. Cuántos de ellos ya tienen medición GEN2 sellada que "
            f"la vista no enlaza se deriva en "
            f"`forense/analisis/relevo-reconcilia-1/reconcilia-173-v1_0.tsv`."
        )
    else:
        partes.append(
            "- **Legacy activas por consumidor.** (sin desglose: "
            "`corrida0 status` no entregó las seis clases)."
        )
    # ACTO GEN2-RELEVO-TANDA-3 · P7. La firma 4.1 cierra con «El contador
    # muestra las clases sin fundirlas»: una sola cifra de "relevadas"
    # borraría la diferencia entre medir desde crudo (i) y leer una conducta
    # que ya es GEN2 (ii). Se RINDE lo que `status` deriva; aquí no se
    # recalcula nada.
    _vi = _v(I, "gen2_relevadas_por_pin_de_mesa__i_CRUDO")
    _vii = _v(I, "gen2_relevadas_por_pin_de_mesa__ii_CONDUCTA_GEN2")
    _mp = _v(I, "gen2_legacy_marco_M_celdas_M_pendientes")
    if _vi is not None and _vii is not None:
        _campos = " · ".join(
            f"{c} `{_v(I, f'gen2_legacy_marco_M_por_campo__{c}')}`"
            for c in ("R", "M", "L", "AGREGADO"))
        partes.append(
            f"- **Relevadas por pin de mesa, por vía (firma 4.1, 21/sep/2026 — "
            f"las clases NO se funden).** vía (i) desde insumo crudo con hash "
            f"`{_vi}` · vía (ii) lectura de una conducta ya GEN2 `{_vii}`. "
            f"Marco del duelo, lo que sigue legacy por campo: {_campos}. "
            f"Celdas M todavía legacy, **nombradas**: `{_mp}` — `DIN-M-01` es "
            f"el recordatorio de que `tiene_ahorros` espera el acceso a "
            f"ENNViH. El canal vive en `data/corrida0/pines-de-mesa.tsv` y "
            f"cada fila pasa las cuatro guardas de 4.1 antes de mover el "
            f"contador (`T32-quater T-PINES-MESA`)."
        )
    else:
        partes.append(
            "- **Relevadas por pin de mesa.** (sin desglose: `corrida0 status` "
            "no entregó las dos vías)."
        )
    partes.append(
        f"- **GEN2 · medición vs. adopción (ACTO GEN2-PRE-E5 · P3).** "
        f"sellados `{_v(I, 'gen2_N_resultados_gen2_sellados')}` · "
        f"pendientes de adopción (citados en la propuesta, ningún consumidor activo aún) "
        f"`{_v(I, 'gen2_N_resultados_gen2_pendientes_adopcion')}` · "
        f"vetados por decisión vigente (sellados, pero una firma prohíbe adoptarlos: "
        f"no son cola) `{_v(I, 'gen2_N_resultados_gen2_vetados_por_decision')}` · "
        f"adoptados por un consumidor activo `{_v(I, 'gen2_N_resultados_gen2_adoptados_activos')}`. "
        f"Sellar un RESULT no mueve `dependencias_numericas_legacy_activas` por sí solo: "
        f"solo el consumidor activo que lo adopta la baja."
    )
    partes.append(
        "- **Fuentes.** `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`, `milpa/procedencia.yaml`, "
        "`forense/prereg-duelo-v2/` (marcos y corridas M/R/L), `data/manifiesto.yaml`, "
        "`data/curacion-registro/cola-adquisicion-registro.tsv`, `data/curacion-registro/relaciones.tsv`, "
        "`data/inventario-reactivos-v1_2.tsv`, `canon/gobernanza-v1_15.md`, `forense/firmas-pendientes.tsv`, "
        "`forense/encargos/*.md`, `forense/encargos/cola/*.md`."
    )
    partes.append("")
    partes.append("**Protocolo vigente.** La actualización factual de este bloque se hace con:")
    partes.append("")
    partes.append("```")
    partes.append("git fetch origin")
    partes.append("python3 tools/tablero_programa.py --actualiza")
    partes.append("python3 tests/check.py --baseline")
    partes.append("```")
    partes.append("")
    partes.append(
        "El humano solo actualiza la interpretación (las tablas curadas §2.1-2.5 y la narrativa) cuando hay "
        "una decisión o un hallazgo que valga la pena registrar. Las recetas antiguas del snapshot histórico "
        "(p. ej. `git branch -r` o `awk '$6==\"ABIERTA\"'`) NO gobiernan esta actualización -- son historia, "
        "no el mecanismo vigente."
    )
    partes.append("")
    partes.append(MARCA_FIN)
    return "\n".join(partes)


def _actualiza_tablero(ruta: str, I: dict[str, dict]) -> int:
    if not os.path.exists(ruta):
        print(f"error: no existe {ruta}", file=sys.stderr)
        return 1
    texto = leer(ruta)
    n_begin = texto.count(MARCA_INICIO)
    n_end = texto.count(MARCA_FIN)
    if n_begin != 1 or n_end != 1:
        print(
            f"error: se esperaba exactamente 1 marcador BEGIN y 1 END en {ruta} "
            f"(encontrados BEGIN={n_begin} END={n_end})",
            file=sys.stderr,
        )
        return 1
    i_begin = texto.index(MARCA_INICIO)
    i_end = texto.index(MARCA_FIN)
    if i_begin >= i_end:
        print(f"error: BEGIN debe preceder a END en {ruta}", file=sys.stderr)
        return 1
    nuevo_bloque = render_bloque_vivo(I)
    fin_bloque = i_end + len(MARCA_FIN)
    nuevo_texto = texto[:i_begin] + nuevo_bloque + texto[fin_bloque:]
    if nuevo_texto == texto:
        return 0
    dir_destino = os.path.dirname(os.path.abspath(ruta))
    fd, tmp = tempfile.mkstemp(dir=dir_destino, prefix=".tablero-tmp-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(nuevo_texto.encode("utf-8"))
        os.replace(tmp, ruta)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return 0


def main() -> None:
    I = derivar_indicadores()

    if "--actualiza" in sys.argv:
        rc = _actualiza_tablero("forense/tablero/TABLERO-PROGRAMA.md", I)
        sys.exit(rc)

    if "--json" in sys.argv:
        print(json.dumps(I, ensure_ascii=False, indent=2, default=str))
        return
    print(f"# Indicadores derivados · HEAD {I['sha']['valor']} · {I['fecha_commit']['valor']} · origin/main={I['es_origin_main']['valor']}\n")
    print("| indicador | valor | comando / receta | nota |")
    print("|---|---|---|---|")
    for k, v in I.items():
        val = json.dumps(v["valor"], ensure_ascii=False, default=str)
        if len(val) > 160:
            val = val[:157] + "…"
        print(f"| `{k}` | {val} | `{v['comando']}` | {v['nota']} |")


if __name__ == "__main__":
    main()
