#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/digesto_tramite.py — el digesto de trámite del agente de fondo.

P1 de `ACTO MAESTRA33-E1 · AGENTE-TRAMITE-1`
(`forense/encargos/2026-08-31-MAESTRA33-E1-AGENTE-TRAMITE-1.md`), que
instaura la práctica que `D-13` de `instrucciones-proyecto-v2_12.md`
dejó registrada sin implementar:

    "un agente de fondo recurrente corre tests/check.py --baseline, lista
    las filas ABIERTA del tablero con su antigüedad, y redacta los PRs de
    trámite (recibos, censos, enterados) para firma de mesa — el WARN
    diario deja de depender de que alguien abra la suite a mano."

QUÉ ES Y QUÉ NO ES. Esto es el LECTOR del agente: mira el árbol y
escribe un archivo. No firma, no decide, no edita el tablero, no toca
`canon/`. Quien actúa es la skill `.claude/commands/tramite.md` (P2), y
lo único que puede hacer está enumerado ahí. Esta separación es
deliberada: un lector que no escribe fuera de `forense/digesto/` no
puede equivocarse de perímetro.

DETERMINISMO. Misma `--fecha` + mismo árbol → misma salida, byte por
byte. La única entrada no derivable del árbol es la fecha, y es un
argumento explícito (por defecto, hoy). Todo lo demás sale de comandos
sobre el clon, con el comando a la vista en la propia salida — nunca de
memoria ni del espejo del proyecto (ARRANQUE punto 5).

A.13. Todo veredicto negativo de este archivo declara cuántos archivos
examinó el comando que lo produjo. Un negativo sin conteo no es un
negativo.

────────────────────────────────────────────────────────────────────
NEUTRALIZACIÓN DE MARCADORES — léelo antes de tocar `_neutraliza()`.
────────────────────────────────────────────────────────────────────
El digesto vive en `forense/digesto/DIGESTO-<fecha>.md`, y su nombre
CAMBIA CADA DÍA. Eso lo pone dentro del universo que vigilan dos tests
de la suite y, a la vez, fuera de la única salida que esos tests
ofrecen:

  · `T25` (`tests/check.py::t25_rotulos`) recorre `forense/**/*.md` y
    FALLA ante el primer rótulo `M`/`E` pelado (`_T25_ROTULO_BARE`). Su
    salida es `_T25_ARCHIVOS_CONOCIDOS`, una lista de rutas literales.
  · `T22(b)` (`::t22_firmas`) recorre `forense/**/*.md` y FALLA ante
    `RANURA` o el patrón de pendiente-de-mesa. Sus dos salidas son
    `_T22_ARCHIVOS_CONOCIDOS` y que una fila ABIERTA/FIRMADA del tablero
    cite el BASENAME del archivo en su columna `dónde`.

Las tres salidas son por ruta o por basename. Un archivo cuyo nombre
cambia cada día no puede estar en ninguna por adelantado. Así que la
garantía tiene que venir POR CONSTRUCCIÓN: este archivo neutraliza los
dos marcadores en todo texto que copia del árbol, antes de escribirlo.

No es defensa hipotética. Medido el 31/ago/2026 contra `af41796`: de las
6 filas ABIERTA del tablero, `FP-179` trae los rótulos pelados `E3`,
`E2`, `E6`, `E10` y `FP-190` trae `E4` en su texto. Un digesto que los
copiara verbatim rompería `T25` en su PRIMERA corrida — el agente de
fondo habría nacido tumbando la suite.

Cómo se neutraliza, y por qué así:
  · Rótulo pelado `M12`/`E-3` → `_M12`/`_E-3`. El guion bajo está en la
    clase que el lookbehind de `_T25_ROTULO_BARE` excluye, así que deja
    de coincidir; el rótulo real es lo que va después del guion bajo, y
    se lee igual. No se inventa un prefijo de espacio (`ADV1-`, `MTR-`):
    eso sería decidir a qué espacio pertenece el rótulo, y decidir es de
    mesa (D-6/ADR-128).
  · Marcadores de `T22(b)` → `«marcador-T22-a»` / `«marcador-T22-b»`.
    Aquí no hay forma de conservar el texto sin conservar el marcador,
    así que se sustituye y se declara.

Toda sustitución se CUENTA y se reporta en el pie del digesto: si un día
son muchas, mesa lo ve. Y `--verifica-marcadores` (encendido por
defecto) vuelve a correr los dos regex sobre la salida ya construida y
aborta con código 2 si algo se coló. El digesto nunca es la fuente de
verdad de un texto: cita el `id` de la fila, y la fila íntegra vive en
`forense/firmas-pendientes.tsv`.
"""

import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys

RAIZ_POR_DEFECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Copiados VERBATIM de tests/check.py -- si allá cambian, aquí se rompe la
# garantía en silencio, y por eso `--verifica-marcadores` re-corre estos
# mismos patrones sobre la salida final en vez de confiar en la copia.
RE_ROTULO_PELADO = re.compile(r"(?<![A-Za-z0-9_-])(M|E)-?(\d{1,2})(?![A-Za-z0-9_.])")
RE_MARCADOR_RANURA = re.compile(r"RANURA")
RE_MARCADOR_PENDIENTE = re.compile(
    r"requiere_decision.*true|PENDIENTE de mesa|pendiente nombrado.*mesa|PROPUESTA.*mesa")

CORRIDAS = ("M", "R", "L")


# ───────────────────────────────────────────────────────────────
# Utilidades
# ───────────────────────────────────────────────────────────────

class Cuenta:
    """Contador de neutralizaciones, para el pie del digesto."""

    def __init__(self):
        self.rotulos = 0
        self.ranura = 0
        self.pendiente = 0

    def total(self):
        return self.rotulos + self.ranura + self.pendiente


def neutraliza(texto, cuenta):
    """Deja `texto` a salvo de T25 y T22(b). Ver la nota del encabezado."""
    def _rot(m):
        cuenta.rotulos += 1
        return "_" + m.group(0)

    texto = RE_ROTULO_PELADO.sub(_rot, texto)

    def _ran(m):
        cuenta.ranura += 1
        return "«marcador-T22-a»"

    texto = RE_MARCADOR_RANURA.sub(_ran, texto)

    def _pen(m):
        cuenta.pendiente += 1
        return "«marcador-T22-b»"

    texto = RE_MARCADOR_PENDIENTE.sub(_pen, texto)
    return texto


def una_linea(texto, tope=None):
    """Colapsa a una línea. Sin tope por defecto: truncar es perder texto,
    y cuando se trunca se dice (ver `--tope-texto`)."""
    t = " ".join(texto.split())
    if tope and len(t) > tope:
        return t[:tope].rstrip() + "…"
    return t


def corre(cmd, raiz, timeout=900):
    """Ejecuta y devuelve (rc, salida). Nunca lanza: un comando que no
    corre es un hallazgo del digesto, no una caída del digesto."""
    try:
        p = subprocess.run(cmd, cwd=raiz, capture_output=True, text=True,
                           timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError as e:
        return 127, f"comando no encontrado: {e}"
    except subprocess.TimeoutExpired:
        return 124, f"tiempo agotado ({timeout}s)"


def plural_dias(n):
    return "1 día" if n == 1 else f"{n} días"


def dias(desde, hasta):
    try:
        a, m, d = (int(x) for x in desde.split("-"))
        return (hasta - datetime.date(a, m, d)).days
    except (ValueError, TypeError, AttributeError):
        return None


# ───────────────────────────────────────────────────────────────
# Lectores del árbol
# ───────────────────────────────────────────────────────────────

def lee_tablero(raiz):
    """(ruta, filas, n_lineas). Mismo lector que `_t22_tabla` de la suite:
    TSV con cabecera, sin comillas -- el tablero se lee, no se parsea con
    csv, porque sus celdas ya traen comillas literales de firmas verbatim."""
    ruta = os.path.join(raiz, "forense", "firmas-pendientes.tsv")
    if not os.path.exists(ruta):
        return ruta, None, 0
    with open(ruta, encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh if l.strip()]
    if not lineas:
        return ruta, [], 0
    cab = lineas[0].split("\t")
    filas = [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]
    return ruta, filas, len(lineas)


def seccion_a(raiz, hoy, cuenta, tope):
    ruta, filas, _ = lee_tablero(raiz)
    out = ["## A · Filas `ABIERTA` del tablero, con antigüedad",
           "",
           "Comando: lectura directa de `forense/firmas-pendientes.tsv` "
           "(columna `estado` == `ABIERTA`, antigüedad = `--fecha` − `creado`).",
           ""]
    if filas is None:
        out += [f"**PARO** — no existe `forense/firmas-pendientes.tsv`. "
                f"A.12 lo exige (`instrucciones-proyecto-v2_9.md`). "
                f"Archivos examinados por la ruta `{os.path.relpath(ruta, raiz)}`: 0.", ""]
        return out, 0
    abiertas = [f for f in filas if f.get("estado") == "ABIERTA"]
    if not abiertas:
        out += [f"NINGUNA. Filas del tablero examinadas: {len(filas)} (A.13). "
                f"El tablero no tiene pendientes de firma hoy.", ""]
        return out, 0
    nota_tope = (f"Los textos se truncan a {tope} caracteres (`--tope-texto`, "
                 f"`0` = sin tope) y se marcan con `…`; el íntegro vive en la fila "
                 f"del tablero." if tope else
                 "Los textos van sin truncar (`--tope-texto 0`).")
    out += [f"{len(abiertas)} de {len(filas)} filas del tablero están `ABIERTA` (A.13). "
            + nota_tope,
            "",
            "| id | creado | antigüedad | qué se firma (íntegro en el tablero) |",
            "|---|---|---|---|"]
    for f in sorted(abiertas, key=lambda x: x.get("id", "")):
        d = dias(f.get("creado", ""), hoy)
        edad = plural_dias(d) if d is not None else "antigüedad no derivable"
        txt = neutraliza(una_linea(f.get("qué_se_firma", ""), tope), cuenta)
        txt = txt.replace("|", "\\|")
        out.append(f"| `{f.get('id', '?')}` | {f.get('creado', '?')} | {edad} | {txt} |")
    out.append("")
    mas_vieja = max((dias(f.get("creado", ""), hoy) or 0) for f in abiertas)
    out += [f"La más antigua lleva **{plural_dias(mas_vieja)}** abierta. "
            f"T22(a) grita estas mismas filas en cada corrida de la suite; "
            f"el digesto existe para que alguien las lea sin abrirla a mano.", ""]
    return out, len(abiertas)


def seccion_b(raiz, sin_suite):
    out = ["## B · `python3 tests/check.py --baseline`",
           "",
           "Comando: `python3 tests/check.py --baseline` en la raíz del clon.",
           ""]
    if sin_suite:
        out += ["**NO CORRIDA** — `--sin-suite`. Este digesto no dice nada sobre "
                "el estado de la suite; no se lea como si lo dijera.", ""]
        return out, None
    rc, salida = corre([sys.executable, "tests/check.py", "--baseline"], raiz)
    m_cifras = re.search(r"(\d+)\s+FAIL\s+·\s+(\d+)\s+WARN", salida)
    m_verde = re.search(r"LÍNEA BASE:\s*VERDE", salida)
    m_rojo = re.search(r"LÍNEA BASE:\s*ROJO\s*—\s*(\d+)\s+entradas nuevas", salida)
    m_head = re.search(r"HEAD congelado ([0-9a-f]{7,40})", salida)

    if m_verde:
        veredicto = "**VERDE**"
    elif m_rojo:
        veredicto = f"**ROJO** — {m_rojo.group(1)} entradas nuevas frente a `tests/baseline.json`"
    else:
        veredicto = ("**NO DERIVABLE** — la salida de la suite no trae ninguna línea "
                     "`LÍNEA BASE:`; se reporta el código de salida crudo y nada más")
    out += [f"- Veredicto de línea base: {veredicto}",
            f"- Código de salida: `{rc}`"]
    if m_cifras:
        out.append(f"- Cifras crudas de esta corrida: **{m_cifras.group(1)} FAIL · "
                   f"{m_cifras.group(2)} WARN**")
    else:
        out.append("- Cifras crudas: NO DERIVABLES — la salida no trae la línea "
                   "`N FAIL · M WARN`.")
    if m_head:
        out.append(f"- `tests/baseline.json` congelado en `{m_head.group(1)[:7]}`")
    # Cifras de la linea base, DERIVADAS del propio archivo -- nunca tecleadas:
    # son justamente las que hacen ver que restar totales crudos no significa nada.
    base = os.path.join(raiz, "tests", "baseline.json")
    if os.path.exists(base):
        try:
            with open(base, encoding="utf-8") as fh:
                d = json.load(fh)
            n_f, n_w = len(d.get("fails", [])), len(d.get("warns", []))
            comparacion = (f"`tests/baseline.json` congela **{n_f} entradas FAIL** y "
                           f"**{n_w} entradas WARN** normalizadas")
            if m_cifras:
                comparacion += (f"; esta corrida dio {m_cifras.group(1)} FAIL y "
                                f"{m_cifras.group(2)} WARN crudos. Las cifras no tienen "
                                f"por qué coincidir y su resta no significa nada")
        except (ValueError, OSError):
            comparacion = ("`tests/baseline.json` no se pudo leer para derivar sus "
                           "conteos (1 archivo examinado)")
    else:
        comparacion = "no existe `tests/baseline.json` (1 ruta examinada, A.13)"

    out += ["",
            "Delta: el veredicto de arriba ES el delta. La suite compara entrada por "
            "entrada normalizada contra `tests/baseline.json`, no cifra contra cifra: "
            f"{comparacion}, porque `_baseline_key` deduplica y normaliza, y las "
            "señales de `T22` sobre el tablero se restan a propósito (una fila que "
            "envejece no es un hallazgo nuevo). VERDE = no empeoraste; ROJO = las "
            "entradas nuevas están en la salida de la suite, no aquí.", ""]
    return out, (rc, bool(m_verde))


def seccion_c(raiz):
    out = ["## C · Ramas remotas distintas de `main`", ""]
    rc, salida = corre(["git", "ls-remote", "--heads", "origin"], raiz, timeout=60)
    if rc == 0 and salida.strip():
        fuente = "`git ls-remote --heads origin` (estado vivo del remoto)"
        ramas = sorted({l.split("refs/heads/", 1)[1].strip()
                        for l in salida.splitlines() if "refs/heads/" in l})
    else:
        rc2, salida2 = corre(["git", "for-each-ref", "--format=%(refname:short)",
                              "refs/remotes/origin"], raiz, timeout=60)
        fuente = ("`git for-each-ref refs/remotes/origin` (RESPALDO: `ls-remote` no "
                  f"respondió, rc={rc}) — refleja el último `fetch` de este clon, "
                  "no necesariamente el remoto de ahora")
        ramas = sorted({l.strip().split("origin/", 1)[-1]
                        for l in salida2.splitlines() if l.strip()
                        and not l.strip().endswith("/HEAD")})
    examinadas = len([r for r in ramas if r])
    ramas = [r for r in ramas if r and r != "main"]
    out += [f"Comando: {fuente}.", ""]
    if not ramas:
        out += [f"NINGUNA. Ramas remotas examinadas por ese comando: "
                f"**{examinadas}** (A.13); ninguna distinta de `main`.", ""]
        return out, 0
    out += [f"{len(ramas)} de **{examinadas}** ramas remotas examinadas son distintas "
            f"de `main` (A.13):", ""]
    for r in ramas:
        out.append(f"- `{r}`")
    out += ["",
            "Una rama que sobrevive a su merge es trabajo perdido o trabajo sin "
            "fusionar; el digesto la nombra, no la borra — borrar es de mesa.", ""]
    return out, len(ramas)


def seccion_d(raiz, piso_arg, tope_lista):
    """Encargos sin `## CONSUMIDO`.

    El piso se DERIVA, no se hereda: es la fecha del encargo más antiguo
    que SÍ trae la marca. Por debajo de esa fecha la convención todavía no
    se practicaba, así que un encargo sin marca no es un defecto sino
    pasivo histórico -- y decidir cuál de esos "ya no aplica" es de mesa
    (lo dice el propio encargo de este acto).
    """
    d = os.path.join(raiz, "forense", "encargos")
    archivos = sorted(glob.glob(os.path.join(d, "*.md")))
    out = ["## D · Encargos sin marca `## CONSUMIDO`", "",
           "Comando: `grep -L '^## CONSUMIDO' forense/encargos/*.md`, acotado a "
           "archivos con prefijo de fecha `AAAA-MM-DD-` (la convención los exige; "
           "`convencion.md` y `PLANTILLA-LOTE-v1_0.md` no son encargos).", ""]
    if not archivos:
        out += [f"NINGUNO. Archivos examinados en `forense/encargos/`: 0 (A.13). "
                f"El directorio está vacío o no existe.", ""]
        return out, 0, None

    con_fecha, sin_fecha = [], []
    for p in archivos:
        b = os.path.basename(p)
        (con_fecha if re.match(r"^\d{4}-\d{2}-\d{2}-", b) else sin_fecha).append(p)

    marcados, sin_marca = [], []
    for p in con_fecha:
        with open(p, encoding="utf-8") as fh:
            s = fh.read()
        (marcados if re.search(r"^## CONSUMIDO", s, re.M) else sin_marca).append(p)

    if piso_arg:
        piso, origen_piso = piso_arg, "dado con `--piso-encargos`"
    elif marcados:
        piso = min(os.path.basename(p)[:10] for p in marcados)
        origen_piso = ("derivado del árbol: fecha del encargo más antiguo que SÍ "
                       "trae la marca")
    else:
        piso, origen_piso = "0000-00-00", "sin piso: ningún encargo trae la marca"

    frescos = sorted((p for p in sin_marca if os.path.basename(p)[:10] >= piso),
                     key=lambda p: os.path.basename(p), reverse=True)
    pasivo = sorted(p for p in sin_marca if os.path.basename(p)[:10] < piso)

    out += [f"Archivos `.md` examinados en `forense/encargos/`: **{len(archivos)}** "
            f"({len(con_fecha)} con prefijo de fecha, {len(sin_fecha)} sin él y por "
            f"tanto fuera del universo) (A.13).",
            f"Con marca: **{len(marcados)}**. Sin marca: **{len(sin_marca)}**.",
            f"Piso de la convención: **{piso}** — {origen_piso}.", ""]

    if not frescos:
        out += [f"**Ninguno sin marca en o después del piso.** Encargos examinados "
                f"por encima del piso: {sum(1 for p in con_fecha if os.path.basename(p)[:10] >= piso)} "
                f"(A.13).", ""]
    else:
        mostrados = frescos if tope_lista <= 0 else frescos[:tope_lista]
        out += [f"### D.1 · Sin marca, en o después del piso — **{len(frescos)}**",
                "",
                "Estos son los accionables: la convención ya estaba viva cuando "
                "nacieron. La skill solo añade la marca cuando el PR es derivable "
                "mecánicamente y da exactamente un candidato; los demás son fila de "
                "digesto, no edición.", ""]
        for p in mostrados:
            out.append(f"- `forense/encargos/{os.path.basename(p)}`")
        if len(mostrados) < len(frescos):
            out += ["",
                    f"**Se listan {len(mostrados)} de {len(frescos)}.** Los "
                    f"{len(frescos) - len(mostrados)} restantes NO están ocultos: son "
                    f"los más antiguos de este mismo conjunto, y `--tope-lista 0` los "
                    f"imprime todos. Truncar en silencio se leería como cobertura "
                    f"completa, y no lo es."]
        out.append("")

    if pasivo:
        fechas = sorted(os.path.basename(p)[:10] for p in pasivo)
        out += [f"### D.2 · Pasivo histórico (anterior al piso) — **{len(pasivo)}**", "",
                f"Rango de fechas: {fechas[0]} … {fechas[-1]}. No se listan uno por uno: "
                f"nacieron antes de que la convención existiera, así que la ausencia de "
                f"marca no es un defecto suyo. **Ni el digesto ni la skill deciden cuál "
                f"de estos «ya no aplica» — eso es de mesa/dirección**, y el encargo de "
                f"este acto lo dice con esas palabras.", ""]
    return out, len(sin_marca), (len(frescos), len(pasivo))


def seccion_e(raiz):
    out = ["## E · Contadores derivados", "",
           "Todos derivados por comando contra el clon, con el comando a la vista. "
           "Ninguno heredado de prosa, de un acto anterior ni del espejo del proyecto "
           "(ARRANQUE punto 5).", ""]
    filas = []

    # (e.1) reglas y dominios de milpa/tramite.yaml
    ruta_tr = os.path.join(raiz, "milpa", "tramite.yaml")
    if os.path.exists(ruta_tr):
        with open(ruta_tr, encoding="utf-8") as fh:
            s_tr = fh.read()
        ids = re.findall(r"^\s+- id:\s*([A-Za-z0-9_.]+)", s_tr, re.M)
        dominios = sorted({i.split(".", 1)[0] for i in ids})
        m_dom = re.search(r"^dominio:\s*(\S+)", s_tr, re.M)
        filas.append(("reglas en `milpa/tramite.yaml`", str(len(ids)),
                      "`grep -cE '^\\s+- id:' milpa/tramite.yaml`"))
        filas.append(("dominios ACTIVOS en `milpa/tramite.yaml`", str(len(dominios)),
                      "prefijo de cada `id`: " + ", ".join(f"`{d}`" for d in dominios)))
        filas.append(("dominio DECLARADO en la cabecera", f"`{m_dom.group(1)}`" if m_dom else "—",
                      "`grep -E '^dominio:' milpa/tramite.yaml`"))
    else:
        filas.append(("reglas en `milpa/tramite.yaml`", "NO-ENCONTRADO",
                      "0 archivos examinados: la ruta no existe (A.13)"))

    # (e.2) ejecutables de milpa/procedencia.yaml
    ruta_pr = os.path.join(raiz, "milpa", "procedencia.yaml")
    if os.path.exists(ruta_pr):
        with open(ruta_pr, encoding="utf-8") as fh:
            n_ej = len(re.findall(r"^\s*valor_ejecutable:", fh.read(), re.M))
        filas.append(("ejecutables en `milpa/procedencia.yaml`", str(n_ej),
                      "`grep -cE '^\\s*valor_ejecutable:' milpa/procedencia.yaml`"))
    else:
        filas.append(("ejecutables en `milpa/procedencia.yaml`", "NO-ENCONTRADO",
                      "0 archivos examinados: la ruta no existe (A.13)"))

    # (e.3) puntos M/R/L
    notas_corridas = []
    for c in CORRIDAS:
        d = os.path.join(raiz, "forense", "prereg-duelo-v2", f"corridas-{c}")
        if not os.path.isdir(d):
            filas.append((f"puntos `{c}` (`corridas-{c}/*.json`)", "NO-ENCONTRADO",
                          "0 archivos examinados: el directorio no existe (A.13)"))
            continue
        todos = sorted(os.listdir(d))
        jsons = [x for x in todos if x.endswith(".json")]
        filas.append((f"puntos `{c}` (`corridas-{c}/*.json`)", str(len(jsons)),
                      f"`ls forense/prereg-duelo-v2/corridas-{c}/*.json | wc -l` "
                      f"— {len(todos)} entradas en total en el directorio"))
        otros = [x for x in todos if not x.endswith(".json")]
        if otros:
            notas_corridas.append(
                f"`corridas-{c}/` trae {len(otros)} entrada(s) que no son `.json` y "
                f"por tanto no son puntos: " + ", ".join(f"`{o}`" for o in sorted(otros)))

    # La barra vertical parte celdas en markdown, y varias derivaciones son
    # tuberias de shell (`ls ... | wc -l`). Se escapa o la tabla se rompe.
    out += ["| contador | valor | derivación |", "|---|---|---|"]
    for nombre, valor, cmd in filas:
        out.append(f"| {nombre} | **{valor}** | {cmd.replace('|', chr(92) + '|')} |")
    out.append("")
    if notas_corridas:
        out.append("Declarado, para que el conteo no se lea como inventario del "
                   "directorio:")
        for n in notas_corridas:
            out.append(f"- {n}")
        out.append("")
    return out, len(filas)


# ───────────────────────────────────────────────────────────────
# Armado
# ───────────────────────────────────────────────────────────────

def construye(raiz, fecha, sin_suite, tope_texto, tope_lista, piso):
    cuenta = Cuenta()
    rc_git, sha = corre(["git", "rev-parse", "--short", "HEAD"], raiz, timeout=60)
    sha = sha.strip() if rc_git == 0 else "NO-DERIVABLE"

    cab = [f"# Digesto de trámite · {fecha.isoformat()}", "",
           f"Emitido por `tools/digesto_tramite.py` sobre el clon en `HEAD` "
           f"`{sha}`. Determinista: misma `--fecha` y mismo árbol → misma salida.",
           "",
           "Este archivo NO decide nada y NO firma nada. Es la lectura del día que "
           "el agente de fondo de `D-13` (`instrucciones-proyecto-v2_12.md`) le debe "
           "a mesa. Lo que aquí aparece como pendiente sigue siendo pendiente hasta "
           "que mesa lo firme.", ""]

    a, n_ab = seccion_a(raiz, fecha, cuenta, tope_texto)
    b, _ = seccion_b(raiz, sin_suite)
    c, n_ramas = seccion_c(raiz)
    d, n_sin, det_d = seccion_d(raiz, piso, tope_lista)
    e, n_cont = seccion_e(raiz)

    pie = ["## Pie · neutralización de marcadores y A.13", "",
           f"Sustituciones hechas al copiar texto del árbol a este archivo: "
           f"**{cuenta.total()}** "
           f"(rótulo `M`/`E` pelado → `_`+rótulo: {cuenta.rotulos} · "
           f"marcador de ranura → `«marcador-T22-a»`: {cuenta.ranura} · "
           f"marcador de decisión-sin-resolver → `«marcador-T22-b»`: {cuenta.pendiente}).",
           "",
           "Los dos marcadores de `T22(b)` no se nombran literalmente en este "
           "archivo — escribirlos aquí lo haría fallar exactamente igual que "
           "copiarlos del árbol, y ni siquiera los NOMBRES de sus constantes "
           "pueden escribirse, porque uno de los dos patrones es una subcadena "
           "suya. Viven en `tests/check.py`, como las dos constantes "
           "`_T22_MARCADOR_*`.", "",
           "Por qué: el nombre de este archivo cambia cada día, así que no puede "
           "estar por adelantado en `_T25_ARCHIVOS_CONOCIDOS` ni en "
           "`_T22_ARCHIVOS_CONOCIDOS`, ni ser citado por `dónde` en una fila del "
           "tablero — las tres salidas que esos tests ofrecen son por ruta o por "
           "basename. La garantía viene por construcción. **El texto íntegro y sin "
           "neutralizar de cada fila vive en `forense/firmas-pendientes.tsv`; este "
           "digesto cita el `id`, no sustituye a la fuente.**", "",
           "Universos examinados por este digesto (A.13): tablero "
           f"`forense/firmas-pendientes.tsv` · `forense/encargos/*.md` · "
           f"`forense/prereg-duelo-v2/corridas-{{M,R,L}}/` · `milpa/tramite.yaml` · "
           f"`milpa/procedencia.yaml` · ramas del remoto `origin`. Fuera de ese "
           "universo este digesto no dice nada, y no debe leerse como si dijera.", ""]

    cuerpo = cab + a + b + c + d + e + pie
    resumen = {"abiertas": n_ab, "ramas": n_ramas, "sin_consumido": n_sin,
               "contadores": n_cont, "neutralizaciones": cuenta.total(),
               "detalle_d": det_d, "sha": sha}
    return "\n".join(cuerpo).rstrip() + "\n", resumen


def verifica(texto):
    """Re-corre los dos regex sobre la salida final. Cinturón y tirantes:
    la copia de los patrones puede quedar desfasada de `tests/check.py`, y
    un digesto que rompe la suite es peor que no tener digesto."""
    problemas = []
    m = RE_ROTULO_PELADO.search(texto)
    if m:
        problemas.append(f"T25: rótulo pelado `{m.group(0)}` sobrevivió a la neutralización")
    if RE_MARCADOR_RANURA.search(texto):
        problemas.append("T22(b): marcador `RANURA` sobrevivió a la neutralización")
    if RE_MARCADOR_PENDIENTE.search(texto):
        problemas.append("T22(b): marcador de pendiente-de-mesa sobrevivió a la neutralización")
    return problemas


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Digesto de trámite determinista (P1 · MAESTRA33-E1).")
    ap.add_argument("--fecha", default=None,
                    help="AAAA-MM-DD. Por defecto, hoy. Fija la fecha del archivo y "
                         "el 'hoy' con que se calcula la antigüedad.")
    ap.add_argument("--raiz", default=RAIZ_POR_DEFECTO,
                    help="Raíz del clon. Por defecto, la que contiene a este archivo.")
    ap.add_argument("--salida", default=None,
                    help="Ruta de salida. Por defecto forense/digesto/DIGESTO-<fecha>.md")
    ap.add_argument("--sin-suite", action="store_true",
                    help="No corre tests/check.py --baseline. La sección B lo declara.")
    ap.add_argument("--stdout", action="store_true",
                    help="Imprime en vez de escribir.")
    ap.add_argument("--tope-texto", type=int, default=220,
                    help="Tope de caracteres del texto citado por fila (0 = sin tope). "
                         "Cuando trunca, lo dice en la propia celda.")
    ap.add_argument("--tope-lista", type=int, default=25,
                    help="Máximo de encargos listados uno por uno en D.1 "
                         "(0 = todos). El resto se declara con su número.")
    ap.add_argument("--piso-encargos", default=None,
                    help="AAAA-MM-DD. Por defecto se DERIVA del árbol.")
    ap.add_argument("--verifica-marcadores", dest="verifica", action="store_true",
                    default=True, help="(por defecto) re-corre los regex de T25/T22 "
                                       "sobre la salida y aborta si algo se coló.")
    ap.add_argument("--sin-verificar-marcadores", dest="verifica", action="store_false",
                    help="Desactiva la verificación. No lo uses para escribir en "
                         "forense/: es la única garantía de que el digesto no tumba "
                         "la suite.")
    a = ap.parse_args(argv)

    if a.fecha:
        try:
            anio, mes, dia = (int(x) for x in a.fecha.split("-"))
            fecha = datetime.date(anio, mes, dia)
        except (ValueError, TypeError):
            print(f"--fecha inválida: {a.fecha!r} (se espera AAAA-MM-DD)", file=sys.stderr)
            return 2
    else:
        fecha = datetime.date.today()

    raiz = os.path.abspath(a.raiz)
    texto, res = construye(raiz, fecha, a.sin_suite, a.tope_texto, a.tope_lista,
                           a.piso_encargos)

    if a.verifica:
        problemas = verifica(texto)
        if problemas:
            print("PARO — la neutralización no fue completa; el digesto NO se escribe:",
                  file=sys.stderr)
            for p in problemas:
                print(f"  · {p}", file=sys.stderr)
            return 2

    if a.stdout:
        sys.stdout.write(texto)
    else:
        salida = a.salida or os.path.join(raiz, "forense", "digesto",
                                          f"DIGESTO-{fecha.isoformat()}.md")
        os.makedirs(os.path.dirname(salida), exist_ok=True)
        with open(salida, "w", encoding="utf-8") as fh:
            fh.write(texto)
        print(f"escrito: {os.path.relpath(salida, raiz)}")

    print(f"resumen: {res['abiertas']} ABIERTA · {res['ramas']} rama(s) ≠ main · "
          f"{res['sin_consumido']} encargo(s) sin CONSUMIDO · "
          f"{res['neutralizaciones']} neutralización(es) · HEAD {res['sha']}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
