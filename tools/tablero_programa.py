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


# `_celdas_validadas`, `_celdas_d_adjudicadas` y `_PATRONES_ERROR_C2` viven
# ahora en tools/celdas_validadas.py (ACTO GEN2-TUBERIA-METRICA-RECTORA-1):
# una sola derivación importable, con su CLI propia y su bloque `universo`.
from celdas_validadas import _celdas_validadas  # noqa: E402


def _celdas_d_adoptadas_activas(directorio: str | None = None) -> dict:
    """Cuenta las celdas-D con `champion_actual` NO vacío y distinto de
    `NINGUNO` -- el contador `adoptados_activos` que el trámite #981
    (hallazgo P3, firma de mesa sobre TANDA-5) pidió mover en la misma
    derivación en que una celda-D adopta (NC-...-3619-01/-02).

    Se deriva directo de `data/curacion-registro/celdas-d/*.yaml`, sin pasar
    por el marcador: adoptar es un hecho de la celda-D (`champion_actual` en
    su YAML, firma de mesa citada ahí mismo), no un efecto de que el
    marcador ya se haya re-derivado. Esto es intencional: el par de
    `marcador-segmento.tsv` puede seguir `RESERVADA` por diseño de
    `tools/marcador_segmento.py` (NC-...-3619-01, ajeno a este acto, §9) sin
    que ese contador quede ciego a la adopción ya firmada.

    `directorio` es un parámetro de prueba (T-CELDAS-D-ADOPTADAS sintético);
    en producción se deriva siempre de `data/curacion-registro/celdas-d/`.
    """
    base = directorio or os.path.join(RAIZ, "data", "curacion-registro", "celdas-d")
    rutas = sorted(glob.glob(os.path.join(base, "*.yaml")))
    if yaml is None:
        return {"error": "PyYAML no disponible", "universo_examinado": len(rutas)}
    adoptadas, sin_adoptar, ilegibles = [], [], []
    for ruta in rutas:
        try:
            with open(ruta, encoding="utf-8") as fh:
                d = (yaml.safe_load(fh) or {}).get("celda_d") or {}
        except (OSError, ValueError):
            ilegibles.append(os.path.relpath(ruta, RAIZ))
            continue
        champ = d.get("champion_actual")
        cid = d.get("id") or os.path.basename(ruta)
        if champ and str(champ).strip().upper() not in ("NINGUNO", ""):
            adoptadas.append({"celda_d": cid, "champion_actual": champ,
                               "fuente": os.path.relpath(ruta, RAIZ)})
        else:
            sin_adoptar.append(cid)
    return {
        "total_adoptadas_activas": len(adoptadas),
        "detalle": adoptadas,
        "celdas_d_sin_adoptar": sin_adoptar,
        "celdas_d_ilegibles": ilegibles,
        "universo_examinado": f"{len(rutas)} archivos en "
                               f"{os.path.relpath(base, RAIZ) if os.path.isabs(base) else base}",
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


def _compara_head_origin_main(head: str, remoto: str) -> tuple[bool, str]:
    """P2 (ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1): ¿HEAD es exactamente
    `origin/main`? Puro -- recibe los dos SHA ya resueltos, para que el test
    no dependa del estado de git real. `remoto` vacío es NO-RESUELTO (un
    checkout que no trae el ref, no una coincidencia por default -- A.13:
    un negativo que no examinó nada no es negativo, y un `==` contra cadena
    vacía sería justo ese negativo fabricado)."""
    if not remoto:
        return False, "origin/main no resoluble (falta `git fetch origin main` antes de --actualiza)"
    if head != remoto:
        return False, f"HEAD ({head}) != origin/main ({remoto})"
    return True, ""


# ADENDA-1 P2: "o el árbol está sucio". Se exceptúan los derivados que el
# propio canal escribe ANTES del tablero (mismo `git add` de verify.yml): en
# CI ya están modificados cuando corre `--actualiza` y son justo lo que viaja.
DERIVADOS_DEL_CANAL = (
    "data/corrida0/corridas.tsv", "data/corrida0/resultados.tsv",
    "data/corrida0/pines-sellados-resueltos.tsv", "data/corrida0/usos.tsv",
    "data/corrida0/marcador-segmento.tsv", "milpa/estimadores-por-segmento.yaml",
    "forense/tablero/TABLERO-PROGRAMA.md", "docs/tablero.md",
)


def _sucios_ajenos(porcelain: str) -> list[str]:
    """Rutas modificadas (sin contar no rastreados) que NO son derivados del canal. Puro."""
    rutas = [ln.split(maxsplit=1)[1] for ln in porcelain.splitlines() if ln.strip()]
    # VISTA-NORMALIZADA-4: `data/corrida0/<CALC>/valores-vista/*` también lo escribe el canal.
    return sorted(r for r in rutas if r not in DERIVADOS_DEL_CANAL and "/valores-vista/" not in r)


def _es_origin_main_limpio() -> tuple[bool, str]:
    ok, motivo = _compara_head_origin_main(sh("git rev-parse HEAD"), sh("git rev-parse -q --verify origin/main"))
    if not ok:
        return ok, motivo
    sucios = _sucios_ajenos(sh("git status --porcelain --untracked-files=no"))
    if sucios:
        return False, f"árbol sucio fuera de los derivados del canal: {', '.join(sucios[:5])}"
    return True, ""


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
    # NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-04: el espacio NUMERICO quedo CERRADO
    # (D-2, ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1). Estos dos maximos describen ese
    # espacio cerrado, NO el ultimo id acuñado: los de raiz de acto se cuentan aparte.
    put("adr_max_espacio_cerrado", EC.adr_max(RAIZ),
        "tools/estado_comun.py::adr_max() -- equivalente a "
        "grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1",
        "espacio NUMERICO cerrado (D-2): no es el ultimo id acuñado")
    put("fp_max_espacio_cerrado", EC.fp_max(RAIZ),
        "tools/estado_comun.py::fp_max() -- equivalente a "
        "grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | grep -oE '[0-9]+' | sort -n | tail -1",
        "espacio NUMERICO cerrado (D-2): no es el ultimo id acuñado")
    put("ids_raiz_de_acto", {
        "ADR": int(sh("grep -coE '^\\*\\*ADR-[0-9]{6}-' canon/gobernanza-v1_15.md") or 0),
        "FP": int(sh("grep -coE '^FP-[0-9]{6}-' forense/firmas-pendientes.tsv") or 0),
        "NC": int(sh("grep -coE '^NC-[0-9]{6}-' forense/no-corrido.tsv") or 0)},
        "grep -coE '^<PREFIJO>-[0-9]{6}-' sobre gobernanza/firmas-pendientes/no-corrido",
        "epoca vigente: ids con raiz de acto, que nunca se renumeran")
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
    # ADENDA-1 P5: los contadores GEN2 se leen de las vistas EN ÁRBOL. Esta
    # lista dice cuáles difieren de HEAD (en CI: las recién derivadas que
    # viajan en el PR [deriva]; en una sesión local, lo que re-derivó sin
    # publicar). Vacía = el valor en árbol es el publicado.
    put("vistas_arbol_distintas_de_head",
        [r for r in DERIVADOS_DEL_CANAL[:5]
         if subprocess.run(["git", "diff", "--quiet", "HEAD", "--", r]).returncode != 0],
        "git diff --quiet HEAD -- <vista> por cada vista de data/corrida0 que escribe el canal")
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
    put("celdas_d_adoptadas_activas", _celdas_d_adoptadas_activas(),
        "data/curacion-registro/celdas-d/*.yaml: champion_actual no vacío y != NINGUNO",
        "P5 GEN2-TUBERIA-EFICIENCIA-1 / trámite #981: adoptar una celda-D mueve este "
        "contador en la misma derivación que celdas_validadas, sin depender de que "
        "el marcador ya haya salido de RESERVADA (NC-...-3619-01, ajeno a este acto)")
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
            f"  - *cruce vs R* · `{c['celda_d']}` · n `{c['n_celdas']}` · champion `{c.get('champion_actual')}` · "
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


def render_bloque_vivo(I: dict[str, dict], no_es_origin_main: bool = False) -> str:
    """Construye el bloque factual committeado a partir del dict de derivar_indicadores().

    Solo hechos mecanicos y estables entre corridas -- sin cifras efimeras
    (edad en dias de FP, ramas remotas presentes), que siguen disponibles en
    la salida interactiva normal (markdown/--json) pero no aqui.

    `no_es_origin_main` (P2, ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1): True solo
    cuando `--actualiza --permitir-rama` corrió fuera de `origin/main`.
    Antepone el rótulo `NO-ES-ORIGIN-MAIN` -- `docs/PROTOCOLO-TABLERO.md`
    dice que una conversación lo ignora.
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

    partes = []
    partes.append(MARCA_INICIO)
    if no_es_origin_main:
        partes.append(
            "**NO-ES-ORIGIN-MAIN** -- generado con `--permitir-rama` fuera de "
            "`origin/main`. El único productor del canal es el job `guardias` "
            "de CI (`.github/workflows/verify.yml`) sobre `origin/main`; una "
            "conversación de mesa lo ignora (`docs/PROTOCOLO-TABLERO.md`)."
        )
        partes.append("")
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
    # "Ramas presentes en origin" NO va en este bloque committeado (P4, ACTO
    # GEN2-TUBERIA-TABLERO-EN-CANAL-1): `ramas_remotas_detalle` corre `git
    # ls-remote`/`git fetch` en vivo contra un repo compartido con sesiones
    # concurrentes -- dos derivaciones sobre el MISMO HEAD, minutos aparte,
    # ya difieren aquí (medido: 3→4 ramas en dos corridas seguidas de este
    # acto). Coincide con lo que el docstring de esta función ya prometía
    # ("sin cifras efímeras... ramas remotas presentes") y que el bloque no
    # cumplía. Sigue disponible sin cambios en `--json` y en `tools/
    # tablero_vista.py` -- el indicador no se borra, solo sale del committeado.
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
        f"- **Gobernanza operativa.** ADR máximo del espacio numérico CERRADO "
        f"`{_v(I, 'adr_max_espacio_cerrado')}` · FP máximo del mismo espacio "
        f"`{_v(I, 'fp_max_espacio_cerrado')}` · ids con raíz de acto (época vigente) "
        f"`{_v(I, 'ids_raiz_de_acto')}` · "
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
        f"- **GEN2 (derivado de `corrida0 status`, valores EN ÁRBOL; vistas del árbol "
        f"distintas de HEAD: `{', '.join(_v(I, 'vistas_arbol_distintas_de_head') or []) or 'ninguna'}`).** "
        f"adoptados activos `{_v(I, 'gen2_N_resultados_gen2_adoptados_activos')}` · "
        f"pendientes de adopción `{_v(I, 'gen2_N_resultados_gen2_pendientes_adopcion')}` · corridas selladas "
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


def _actualiza_tablero(ruta: str, I: dict[str, dict], no_es_origin_main: bool = False) -> int:
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
    nuevo_bloque = render_bloque_vivo(I, no_es_origin_main=no_es_origin_main)
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
    if "--actualiza" in sys.argv:
        # P2 (ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1): único productor sobre
        # `origin/main`. Defecto real que corrige (evidencia en el encargo):
        # `/tramite` T0 regeneró el bloque desde una rama (commit `78f79c80`,
        # SHA del bloque `8a867a04`, ¿árbol==origin/main? False) mientras el
        # job de CI producía otro bloque distinto (SHA `3423b498`, True) --
        # dos productores, dos resultados. `--permitir-rama` es la única
        # salida y rotula el bloque `NO-ES-ORIGIN-MAIN` (nunca silenciosa).
        permitir_rama = "--permitir-rama" in sys.argv
        ok, motivo = _es_origin_main_limpio()
        if not ok and not permitir_rama:
            print(
                f"error: --actualiza se niega -- {motivo}. El único productor "
                "del canal es el job `guardias` de CI sobre origin/main "
                "(.github/workflows/verify.yml); usa --permitir-rama para "
                "forzarlo de todos modos -- rotula el bloque NO-ES-ORIGIN-MAIN.",
                file=sys.stderr,
            )
            sys.exit(1)
        no_es_origin_main = not ok
        I = derivar_indicadores()
        rc = _actualiza_tablero("forense/tablero/TABLERO-PROGRAMA.md", I, no_es_origin_main=no_es_origin_main)
        if rc == 0 and os.path.exists("docs/tablero.md"):
            # P3: misma derivación, misma función ya probada
            # (idempotencia/preservación) -- una segunda salida, no un
            # segundo productor.
            rc = _actualiza_tablero("docs/tablero.md", I, no_es_origin_main=no_es_origin_main)
        sys.exit(rc)

    I = derivar_indicadores()

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
