#!/usr/bin/env python3
"""tablero_programa.py -- deriva los indicadores del TABLERO DEL PROGRAMA desde el
arbol del repo. Cero cifras tecleadas: todo sale de archivos o de git.

Uso (desde la raiz del clon, con origin/main recien traido):
    python3 tools/tablero_programa.py            # markdown a stdout
    python3 tools/tablero_programa.py --json     # mismo contenido, JSON

Reglas que este script respeta (instrucciones v2.12):
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
    for f in sorted(glob.glob("forense/encargos/cola/*.md")):
        tt = leer(f)
        cola[os.path.basename(f)] = "CONSUMIDO" if "## CONSUMIDO" in tt else ("LISTO" if "LISTO-" in tt else "GATED")
    put("cola_encargos", cola, "forense/encargos/cola/*.md: '## CONSUMIDO' / 'LISTO-' / otro=GATED")
    put("skills", sorted(os.path.basename(f)[:-3] for f in glob.glob(".claude/commands/*.md")), "ls .claude/commands/")
    vers = sorted(int(m) for m in re.findall(r"instrucciones-proyecto-v2_(\d+)\.md", " ".join(glob.glob("instrucciones-proyecto-v2_*.md"))))
    put("instrucciones_vigentes", f"v2.{vers[-1]}" if vers else None, "ls instrucciones-proyecto-v2_*.md | version maxima numerica")
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

    return I


def _v(I, k):
    return I[k]["valor"] if k in I else None


def render_bloque_vivo(I: dict[str, dict]) -> str:
    """Construye el bloque factual committeado a partir del dict de derivar_indicadores().

    Solo hechos mecanicos y estables entre corridas -- sin cifras efimeras
    (edad en dias de FP, ramas remotas presentes), que siguen disponibles en
    la salida interactiva normal (markdown/--json) pero no aqui.
    """
    fp_ids = ", ".join(a["id"] for a in (_v(I, "fp_abiertas") or [])) or "(ninguna)"
    cola = _v(I, "cola_encargos") or {}
    cola_txt = "\n".join(f"  - `{k}`: {v}" for k, v in cola.items()) or "  (vacía)"

    partes = []
    partes.append(MARCA_INICIO)
    partes.append("## Estado vivo derivado")
    partes.append("")
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
        f"- **Corredor.** marco vigente `marco-M-{_v(I, 'marco_vigente_sorteado')}` sorteado / "
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
        f"cola de encargos:\n{cola_txt}"
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
    partes.append(
        f"- **GEN2 · medición vs. adopción (ACTO GEN2-PRE-E5 · P3).** "
        f"sellados `{_v(I, 'gen2_N_resultados_gen2_sellados')}` · "
        f"pendientes de adopción (citados en la propuesta, ningún consumidor activo aún) "
        f"`{_v(I, 'gen2_N_resultados_gen2_pendientes_adopcion')}` · "
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
