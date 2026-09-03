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
from collections import Counter
from datetime import date

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

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


def main() -> None:
    I: dict[str, dict] = {}

    def put(clave, valor, comando, nota=""):
        I[clave] = {"valor": valor, "comando": comando, "nota": nota}

    # ── 0 · procedencia ────────────────────────────────────────────────
    sha = sh("git rev-parse --short HEAD")
    put("sha", sha, "git rev-parse --short HEAD")
    put("fecha_commit", sh("git log -1 --format=%ad --date=short HEAD"), "git log -1 --format=%ad --date=short HEAD")
    put("es_origin_main", sh("git rev-parse HEAD") == sh("git rev-parse origin/main"),
        "git rev-parse HEAD == git rev-parse origin/main", "si False, el tablero no se deriva de main")
    put("ramas_remotas_vivas", [b.strip() for b in sh("git branch -r | grep -v HEAD | grep -v 'origin/main$'").splitlines() if b.strip()],
        "git branch -r | grep -v HEAD | grep -v 'origin/main$'", "PR abiertos = actos que aun no fusionan")

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
        put("motor_reglas_sin_dato", sin_dato, "python: reglas cuyas conductas son todas ASIGNADO", "LA SEÑAL: meta = []")
        put("motor_tiers", dict(tiers), "python: Counter(tier) sobre milpa/tramite.yaml")
    put("modelo_reglas_canon", sh("python3 tests/validador_registro_ids.py 2>/dev/null | tail -1"),
        "python3 tests/validador_registro_ids.py | tail -1", "las 49 del modelo-decision; el motor implementa un subconjunto")

    # ── 2 · propuesta (acumulador) ─────────────────────────────────────
    p = leer("milpa/tramite-ola5-propuesta-v0.yaml")
    put("propuesta_entradas", len(re.findall(r"^  - id: ", p, re.M)), "grep -cE '^  - id: ' milpa/tramite-ola5-propuesta-v0.yaml")
    for k in ("PENDIENTE-DE-MESA", "SELLADA", "MEDIA", "FUERTE"):
        put(f"propuesta_tier_{k}", len(re.findall(rf"^\s+tier: {k}", p, re.M)), f"grep -cE '^\\s+tier: {k}' milpa/tramite-ola5-propuesta-v0.yaml")
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
    sort = [r[0] for r in tsv_rows(PD + "marco-M-sorteado-v1_2.tsv") if r[0] != "id"]
    cong = [r[0] for r in tsv_rows(PD + "marco-M-congelado-v1_2.tsv") if r[0] != "id"]
    Rc = [i for i in sort if os.path.exists(PD + f"corridas-R/{i}.json")]
    Mc = [i for i in sort if glob.glob(PD + f"corridas-M/M-{i}*.json")]
    Lc = [i for i in sort if glob.glob(PD + f"corridas-L/L-{i}-M__*.json")]
    lmr = [i for i in sort if i in Rc and i in Mc and i in Lc]
    put("marco_v1_2_congelado", len(cong), "filas de marco-M-congelado-v1_2.tsv sin '#'")
    put("marco_v1_2_sorteado", len(sort), "filas de marco-M-sorteado-v1_2.tsv sin '#'")
    put("celdas_con_R", len(Rc), "ls corridas-R/<id>.json por id sorteado")
    put("celdas_con_M", len(Mc), "ls corridas-M/M-<id>*.json por id sorteado")
    put("celdas_con_L", len(Lc), "ls corridas-L/L-<id>-M__*.json por id sorteado")
    put("celdas_puntuables_LMR", len(lmr), "interseccion R∩M∩L sobre el sorteado", "LA SEÑAL: celdas puntuadas")
    put("celdas_sin_LMR", sorted(set(sort) - set(lmr)), "sorteado − (R∩M∩L)")
    put("dominios_sorteado", {k: sum(1 for i in sort if i.startswith(k)) for k in ("TRA", "CIV", "DIN", "FAM")}, "prefijo de id")
    put("L_capturas_total", len(glob.glob(PD + "corridas-L/L-*.json")), "ls corridas-L/L-*.json | wc -l")
    put("L_capturas_v1_2", int(sh(f"grep -l sha256_prompt {PD}corridas-L/L-*.json | wc -l") or 0), "grep -l sha256_prompt corridas-L/L-*.json | wc -l")
    put("scoreboards", sorted(os.path.basename(f) for f in glob.glob(PD + "scoreboard*")), "ls scoreboard*", "v1_2 aparece cuando N3 cierra")
    put("dominios_activos", 4, "ADR-265 (MAESTRA33-E14): tramite, civico, dinero, familia; Ola 6 NO abierta", "cambia solo por firma de mesa (N5)")

    # ── 5 · corpus ────────────────────────────────────────────────────
    put("manifiesto_ids", int(sh("grep -c '^- id: ' data/manifiesto.yaml") or 0), "grep -c '^- id: ' data/manifiesto.yaml")
    put("payloads_verificados_ultimo_registro", sh("grep -rhoE 'data_raw: coincide=[0-9]+[^|]{0,40}' forense/notas/2026-09-0*.md | tail -1"),
        "grep -rhoE 'data_raw: coincide=...' forense/notas/2026-09-0*.md | tail -1", "solo se re-mide en caja con corpus (tests/manifiesto.py --verifica)")
    rows = tsv_rows("data/cola-adquisicion-v1_0.tsv")
    put("cola_adquisicion_estados", dict(Counter(r[1].split("(")[0] for r in rows[1:])), "columna 2 de data/cola-adquisicion-v1_0.tsv")
    put("registro_curador_filas", int(sh("grep -vc '^#' data/curacion-registro/cola-adquisicion-registro.tsv") or 0), "grep -vc '^#' data/curacion-registro/cola-adquisicion-registro.tsv")
    put("relaciones_filas", int(sh("grep -vc '^#' data/curacion-registro/relaciones.tsv") or 0), "grep -vc '^#' data/curacion-registro/relaciones.tsv")
    put("inventario_reactivos_v1_2", int(sh("grep -vc '^#' data/inventario-reactivos-v1_2.tsv") or 0), "grep -vc '^#' data/inventario-reactivos-v1_2.tsv")

    # ── 6 · gobernanza y aparato ───────────────────────────────────────
    put("adr_max", int(sh("grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1") or 0),
        "grep -oE '^\\*\\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1")
    put("fp_max", int(sh("grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | grep -oE '[0-9]+' | sort -n | tail -1") or 0),
        "grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | grep -oE '[0-9]+' | sort -n | tail -1")
    hoy = date.today()
    abiertas = []
    for r in csv.reader(open("forense/firmas-pendientes.tsv", encoding="utf-8", errors="replace"), delimiter="\t"):
        if len(r) > 5 and r[5] == "ABIERTA":
            try:
                edad = (hoy - date.fromisoformat(r[3][:10])).days
            except Exception:
                edad = None
            abiertas.append({"id": r[0], "creado": r[3][:10], "dias": edad, "que": r[1][:140]})
    put("fp_abiertas", abiertas, "awk -F'\\t' '$6==\"ABIERTA\"' forense/firmas-pendientes.tsv", "WARN de T-FIRMAS en cada corrida")
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
    put("hito_d_historico", sh("grep -oE '[0-9]+ de 27 corridas archivadas' canon/estado-programa-v1_11.md | head -1"),
        "grep -oE '[0-9]+ de 27 corridas archivadas' canon/estado-programa-v1_11.md", "historico (transfer §6): NO es la señal")
    put("commits", int(sh("git rev-list --count HEAD") or 0), "git rev-list --count HEAD")
    put("prs_fusionados", int(sh("git log --merges --format=%s HEAD | grep -c 'pull request'") or 0), "git log --merges --format=%s HEAD | grep -c 'pull request'")
    put("suite", "correr: python3 tests/check.py --baseline | tail -6 (no se corre aqui: tarda; pega la salida cruda)", "python3 tests/check.py --baseline")

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
