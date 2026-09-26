#!/usr/bin/env python3
"""Hook PreToolUse (Bash|Read) que hace cumplir las reglas de lectura.

ACTO GEN2-TUBERIA-CABLEADO-SESIONES-1, P1. Las reglas viven en
canon/REGLAS-DE-LECTURA.md; este hook convierte cuatro de ellas en bloqueo
(salida 2, mensaje por stderr que Claude Code devuelve al modelo):

  (a) `cat`/`less`/`more` o `Read` sin rango sobre un archivo > UMBRAL líneas;
  (b) lectura completa (cat/less/more o Read sin limit) de un derivado;
  (c) `git log -p` / `--patch` sin ruta (`-- <ruta>`);
  (d) `pytest` sin `-q`.

Todo lo demás pasa. Escape declarado: la cadena `--permitir-lectura-completa`
en el comando Bash (p. ej. como comentario final `# --permitir-lectura-completa`)
deja pasar y REGISTRA el uso. `Read` no admite bandera: el escape de una
lectura completa legítima es Bash con la bandera.

Excepciones por ruta (flujo legítimo, declaradas): encargos y adendas en
forense/encargos/*.md y los adjuntos subidos (/root/.claude/uploads/), que
/acto debe leer completos para archivarlos verbatim.

D-23: el hook solo lee (cuenta saltos de línea, lo mismo que `wc -l`) y
escribe su registro forense/analisis/cableado/bloqueos.tsv (una fila por
bloqueo o escape; contador de cumplimiento, derivado, no se edita a mano).
Si el registro no se puede escribir, el hook sigue decidiendo igual.

Uso (lo invoca .claude/settings.json; JSON del evento por stdin):
  python3 tools/hook_lectura.py
"""
import datetime
import fnmatch
import json
import os
import re
import shlex
import sys

UMBRAL = 200
ESCAPE = "--permitir-lectura-completa"
DERIVADOS = (
    "data/corrida0/*.tsv",
    "data/corrida0/CALC-*/resultados.json",
    "data/manifiesto.yaml",
    "milpa/estimadores-*",
    "data/curacion-universo/*.tsv",
    "canon/L0/HISTORICO.md",
)
EXCEPCIONES = ("forense/encargos/*.md", "/root/.claude/uploads/*")
LECTORES = {"cat", "less", "more", "bat", "tac"}
REGISTRO = os.path.join("forense", "analisis", "cableado", "bloqueos.tsv")
CABECERA = "fecha\tsesion\therramienta\tdecision\tmotivo\tcomando\n"

SUGERENCIA = (
    "Usa `wc -l` y luego `head -n N`, `tail -n N`, `sed -n 'a,bp'` o Read con "
    "offset/limit; para derivados: `python3 tools/consulta.py "
    "result|corrida|celda|payload|fp|nc <id>`, `jq`, `yq` "
    "(canon/REGLAS-DE-LECTURA.md). Escape declarado y registrado: añade "
    "`# " + ESCAPE + "` al comando Bash."
)


def raiz():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def relativa(ruta, cwd):
    absr = os.path.normpath(os.path.join(cwd, ruta))
    base = os.path.normpath(raiz())
    if absr.startswith(base + os.sep):
        return os.path.relpath(absr, base), absr
    return absr, absr


def casa(rel, patrones):
    return any(fnmatch.fnmatch(rel, p) for p in patrones)


def lineas(absr):
    try:
        n = 0
        with open(absr, "rb") as f:
            for bloque in iter(lambda: f.read(1 << 20), b""):
                n += bloque.count(b"\n")
        return n
    except OSError:
        return None


def juzga_archivo(ruta, cwd):
    """Motivo de bloqueo para una lectura completa de `ruta`, o None."""
    rel, absr = relativa(ruta, cwd)
    if casa(rel, EXCEPCIONES) or casa(absr, EXCEPCIONES):
        return None
    if casa(rel, DERIVADOS):
        return "(b) lectura completa de derivado %s" % rel
    n = lineas(absr)
    if n is not None and n > UMBRAL:
        return "(a) lectura completa de %s (%d líneas > %d)" % (rel, n, UMBRAL)
    return None


def segmentos(cmd):
    """Parte un comando en segmentos simples por | ; && || y saltos de línea."""
    # quita heredocs: su cuerpo no es comando
    cmd = re.sub(r"<<-?\s*'?\"?(\w+)'?\"?.*?\n.*?\n\1\b", "", cmd, flags=re.S)
    for seg in re.split(r"\|\||&&|[|;\n]", cmd):
        try:
            toks = shlex.split(seg, comments=True)
        except ValueError:
            toks = seg.split()
        if toks:
            yield toks


def juzga_bash(cmd, cwd):
    motivos = []
    for toks in segmentos(cmd):
        while toks and re.match(r"^\w+=", toks[0]):
            toks = toks[1:]
        if toks and toks[0] in ("sudo", "time", "command", "nice"):
            toks = toks[1:]
        if not toks:
            continue
        prog = os.path.basename(toks[0])
        if prog in LECTORES:
            # tras una redirección de salida, el resto no es archivo leído
            limpios = []
            salto = False
            for t in toks[1:]:
                if salto:
                    salto = False
                    continue
                if t in (">", ">>", "2>", "&>"):
                    salto = True
                    continue
                if t.startswith((">", "2>", "&>")) or t.startswith("-"):
                    continue
                limpios.append(t)
            for a in limpios:
                m = juzga_archivo(a, cwd)
                if m:
                    motivos.append(m)
        elif prog == "git" and "log" in toks[1:3]:
            if any(t in ("-p", "--patch", "-u") for t in toks) and "--" not in toks:
                motivos.append("(c) git log -p sin ruta")
        es_pytest = prog in ("pytest", "py.test") or (
            prog.startswith("python") and "-m" in toks and "pytest" in toks
        )
        if es_pytest:
            quiet = any(t in ("--quiet",) or re.match(r"^-q+$", t) for t in toks)
            if not quiet:
                motivos.append("(d) pytest sin -q")
    return motivos


def registra(evento, herramienta, decision, motivo, comando):
    try:
        ruta = os.path.join(raiz(), REGISTRO)
        nuevo = not os.path.exists(ruta)
        fila = "\t".join(
            [
                datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                str(evento.get("session_id") or "SIN-SESION")[:40],
                herramienta,
                decision,
                motivo.replace("\t", " "),
                re.sub(r"\s+", " ", comando)[:160],
            ]
        )
        with open(ruta, "a", encoding="utf-8") as f:
            if nuevo:
                f.write(CABECERA)
            f.write(fila + "\n")
    except OSError:
        pass


def decide(evento):
    """(codigo_salida, mensaje). 0 = pasa, 2 = bloquea."""
    herramienta = evento.get("tool_name", "")
    entrada = evento.get("tool_input") or {}
    cwd = evento.get("cwd") or raiz()
    if herramienta == "Read":
        ruta = entrada.get("file_path", "")
        if entrada.get("limit") or entrada.get("offset") or entrada.get("pages"):
            return 0, ""
        m = juzga_archivo(ruta, cwd)
        comando = "Read " + ruta
        motivos = [m] if m else []
    elif herramienta == "Bash":
        comando = entrada.get("command", "")
        motivos = juzga_bash(comando, cwd)
    else:
        return 0, ""
    if not motivos:
        return 0, ""
    motivo = "; ".join(motivos)
    if herramienta == "Bash" and ESCAPE in comando:
        registra(evento, herramienta, "ESCAPE", motivo, comando)
        return 0, ""
    registra(evento, herramienta, "BLOQUEO", motivo, comando)
    return 2, "BLOQUEADO por reglas de lectura: %s. %s" % (motivo, SUGERENCIA)


def main():
    try:
        evento = json.load(sys.stdin)
    except ValueError:
        return 0
    codigo, mensaje = decide(evento)
    if mensaje:
        print(mensaje, file=sys.stderr)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
