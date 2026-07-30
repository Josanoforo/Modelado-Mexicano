#!/usr/bin/env python3
"""tests/bitacora.py — protocolo-sesion v1.0 §1/§2.

--abre    imprime el estado del repo, todo derivado en el momento.
--cierra  deriva y anexa un bloque a forense/bitacora.md.

Requisito duro (protocolo §1): todo lo impreso sale de git, de la suite,
o de un archivo. Ningún campo se teclea ni se rellena con placeholder;
si algo no se puede derivar, se omite y se reporta como omitido al final.

Única dependencia externa del proyecto: PyYAML, para leer/escribir
canon/cola.yaml (protocolo §5).
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sh(args, cwd=ROOT):
    """Corre un comando, devuelve (stdout.strip(), exit_code). Nunca lanza."""
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode


def git(*args):
    out, code = sh(["git", *args])
    return out if code == 0 else None


def leer(path):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────── --abre ──

def cmd_abre():
    faltantes = []
    print("=" * 72)
    print("  APERTURA DE SESIÓN — protocolo §1")
    print("=" * 72)

    head = git("rev-parse", "HEAD")
    origin_main = git("rev-parse", "origin/main")
    if head is None:
        faltantes.append("HEAD (git rev-parse no lo derivó)")
    if origin_main is None:
        faltantes.append("origin/main (sin remoto 'origin', o sin ref local; este comando no hace fetch)")
    print(f"\nHEAD:         {head or '(no derivable)'}")
    print(f"origin/main:  {origin_main or '(no derivable)'}  (ref local, sin fetch)")
    if head and origin_main:
        if head == origin_main:
            print("Divergencia:  ninguna — HEAD == origin/main")
        else:
            counts = git("rev-list", "--left-right", "--count", "origin/main...HEAD")
            print(f"Divergencia:  sí — {counts or '(no derivable)'} (izq=solo en origin/main · der=solo en HEAD)")

    rama = git("branch", "--show-current")
    ramas_raw = git("for-each-ref", "refs/heads",
                     "--format=%(refname:short)|%(objectname:short)|%(committerdate:short)")
    print(f"\nRama actual:  {rama or '(no derivable)'}")
    print("Ramas vivas (locales):")
    if ramas_raw:
        for l in ramas_raw.split("\n"):
            nombre, sha, fecha = (l.split("|") + ["?", "?"])[:3]
            print(f"  - {nombre}  {sha}  {fecha}")
    else:
        faltantes.append("ramas vivas (git for-each-ref no devolvió nada)")

    print("\n--- Estado de las dos suites ---")
    out, code = sh([sys.executable, os.path.join(ROOT, "tests", "check.py"), "--baseline"])
    veredicto = next((l.strip() for l in out.split("\n") if "LÍNEA BASE:" in l), None) if out else None
    print(f"check.py --baseline:        exit={code} · {veredicto or '(veredicto no encontrado en la salida)'}")
    out2, code2 = sh([sys.executable, os.path.join(ROOT, "tests", "validador_registro_ids.py")])
    print(f"validador_registro_ids.py:  exit={code2} · {out2 or '(sin salida)'}")

    print("\n--- Último bloque de forense/bitacora.md ---")
    bit = leer("forense/bitacora.md")
    if bit is None:
        print("(forense/bitacora.md no existe todavía — ninguna sesión lo ha cerrado aún)")
        faltantes.append("último bloque de bitácora (el archivo no existe)")
    else:
        bloques = [b for b in re.split(r"(?m)^## ", bit) if b.strip()]
        if bloques:
            print("## " + bloques[-1].rstrip())
        else:
            print("(forense/bitacora.md existe pero no tiene bloques con encabezado '## ')")
            faltantes.append("último bloque de bitácora (archivo sin bloques)")

    print("\n--- Cola abierta (canon/cola.yaml), por clase ---")
    cola_raw = leer("canon/cola.yaml")
    if cola_raw is None:
        print("(canon/cola.yaml no existe)")
        faltantes.append("cola (el archivo no existe)")
    else:
        entradas = yaml.safe_load(cola_raw) or []
        abiertas = [e for e in entradas if e.get("estado") in ("abierto", "en_curso")]
        if not abiertas:
            print("(sin entradas abiertas)")
        else:
            por_clase = {}
            for e in abiertas:
                por_clase.setdefault(e.get("clase", "sin_clase"), []).append(e)
            for clase in sorted(por_clase):
                print(f"  [{clase}]")
                for e in por_clase[clase]:
                    print(f"    {e.get('id', '?')} · {e.get('titulo', '?')} "
                          f"(casos={e.get('casos', '?')}, {e.get('estado', '?')})")

    print("\n--- Versión de instrucciones vigente ---")
    instr = leer("instrucciones-proyecto-v2.md")
    if instr is None:
        faltantes.append("versión de instrucciones (el archivo no existe)")
    else:
        primera = instr.split("\n", 1)[0]
        commit_instr = git("log", "-1", "--format=%h %ci", "--", "instrucciones-proyecto-v2.md")
        print(f"  {primera}")
        print(f"  último commit que la tocó: {commit_instr or '(no derivable)'}")

    if faltantes:
        print("\n--- Campos que NO se pudieron derivar (omitidos, no rellenados) ---")
        for f in faltantes:
            print(f"  - {f}")


# ────────────────────────────────────────────────────────────── --cierra ──

def cmd_cierra(decidido, bloqueado):
    if not decidido or not bloqueado:
        print("ERROR: --cierra exige --decidido y --bloqueado (las dos únicas líneas "
              "manuales del bloque, protocolo §2). No se rellenan con placeholder.")
        sys.exit(1)

    fecha = datetime.date.today().isoformat()
    origin_main = git("rev-parse", "origin/main")
    head = git("rev-parse", "HEAD")
    rama = git("branch", "--show-current")

    lineas = [f"## {fecha}", ""]
    lineas.append(
        f"**Fecha:** {fecha} · **Rama:** `{rama or '(no derivable)'}` · "
        f"**HEAD inicial (origin/main):** `{origin_main or '(no derivable)'}` · "
        f"**HEAD final:** `{head or '(no derivable)'}`"
    )
    lineas.append("")

    rango = "origin/main..HEAD"
    if origin_main and head and origin_main != head:
        log = git("log", rango, "--format=%H|%an|%(trailers:key=Co-Authored-By,valueonly)|%s")
        lineas.append("**Commits de la sesión:**")
        if log:
            for l in log.split("\n"):
                partes = l.split("|", 3)
                h = partes[0][:7] if len(partes) > 0 else "?"
                an = partes[1] if len(partes) > 1 else "?"
                co = partes[2].strip() if len(partes) > 2 else ""
                asunto = partes[3] if len(partes) > 3 else ""
                lineas.append(f"  - `{h}` · {an}" + (f" · co: {co}" if co else "") + f" · {asunto}")
        else:
            lineas.append("  (origin/main y HEAD difieren pero `git log` no devolvió commits)")

        archivos = git("diff", "--stat", rango)
        lineas.append("")
        lineas.append("**Archivos tocados:**")
        lineas.append("```")
        lineas.append(archivos or "(sin cambios de archivo)")
        lineas.append("```")

        diff_canon = git("diff", rango, "--", "canon/")
        adrs = re.findall(r"^\+\*\*(ADR-\d+)", diff_canon, re.M) if diff_canon else []
        lineas.append("")
        lineas.append(f"**ADRs añadidos:** {', '.join(adrs) if adrs else '(ninguno detectado)'}")

        versiones = re.findall(r"^\+.*?· \*\*v[\d._]+\*\*.*$", diff_canon, re.M) if diff_canon else []
        lineas.append(f"**Líneas de versión modificadas en canon/:** {len(versiones)}")
        for v in versiones[:10]:
            lineas.append(f"  - {v.lstrip('+').strip()}")
    else:
        lineas.append("**Commits de la sesión:** (HEAD == origin/main — nada nuevo que listar)")

    lineas.append("")
    lineas.append("**Delta de suite:**")
    antes_raw = git("show", "origin/main:tests/baseline.json") if origin_main else None
    if antes_raw:
        try:
            antes = json.loads(antes_raw)
            antes_txt = (f"{len(antes.get('fails', []))} FAIL · "
                          f"{len(antes.get('warns', []))} WARN (congelados en origin/main)")
        except Exception:
            antes_txt = "(tests/baseline.json en origin/main no se pudo parsear)"
    else:
        antes_txt = "(tests/baseline.json no existía en origin/main)"
    out, _ = sh([sys.executable, os.path.join(ROOT, "tests", "check.py")])
    m = re.search(r"(\d+)\s*FAIL\s*·\s*(\d+)\s*WARN", out or "")
    despues_txt = (f"{m.group(1)} FAIL · {m.group(2)} WARN (corrida real, sin --baseline)"
                   if m else "(no derivable de la corrida)")
    lineas.append(f"  - Antes: {antes_txt}")
    lineas.append(f"  - Después: {despues_txt}")

    lineas.append("")
    lineas.append("**Cola — IDs afectados en la sesión:**")
    cola_antes_raw = git("show", "origin/main:canon/cola.yaml") if origin_main else None
    ids_antes = set()
    if cola_antes_raw:
        try:
            ids_antes = {e["id"] for e in (yaml.safe_load(cola_antes_raw) or [])}
        except Exception:
            pass
    cola_despues_raw = leer("canon/cola.yaml")
    ids_despues, estado_despues = set(), {}
    if cola_despues_raw:
        try:
            entradas = yaml.safe_load(cola_despues_raw) or []
            ids_despues = {e["id"] for e in entradas}
            estado_despues = {e["id"]: e.get("estado") for e in entradas}
        except Exception:
            pass
    abiertos = sorted(ids_despues - ids_antes)
    cerrados = sorted(i for i in (ids_antes & ids_despues)
                       if estado_despues.get(i) in ("cerrado", "descartado"))
    lineas.append(f"  - Abiertos: {', '.join(abiertos) if abiertos else '(ninguno)'}")
    lineas.append(f"  - Cerrados: {', '.join(cerrados) if cerrados else '(ninguno)'}")

    lineas.append("")
    lineas.append(f"**Qué se decidió:** {decidido}")
    lineas.append(f"**Qué quedó bloqueado:** {bloqueado}")
    lineas.append("")
    lineas.append("---")
    lineas.append("")

    bloque = "\n".join(lineas)
    path = os.path.join(ROOT, "forense", "bitacora.md")
    existente = leer("forense/bitacora.md")
    if existente is None:
        existente = ("# Bitácora de sesión\n\n"
                     "*(Generado por `tests/bitacora.py --cierra`, protocolo §2. "
                     "No se edita a mano salvo las dos líneas declaradas en cada bloque.)*\n\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(existente + bloque + "\n")

    print(bloque)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--abre", action="store_true")
    g.add_argument("--cierra", action="store_true")
    ap.add_argument("--decidido", default=None, help="Línea manual: qué se decidió (solo --cierra)")
    ap.add_argument("--bloqueado", default=None, help="Línea manual: qué quedó bloqueado (solo --cierra)")
    a = ap.parse_args()
    if a.abre:
        cmd_abre()
    else:
        cmd_cierra(a.decidido, a.bloqueado)


if __name__ == "__main__":
    main()
