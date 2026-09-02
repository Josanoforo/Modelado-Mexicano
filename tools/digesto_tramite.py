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

v1.1 — SECCIONES F Y G, Y LA TABLA DE FALSADORES DEL PIE.
`ACTO MAESTRA33-E3 · CABLEADO-COLA-DIGESTO`
(`forense/encargos/2026-08-31-MAESTRA33-E3-CABLEADO-COLA-DIGESTO.md`)
añade tres cosas a la v1.0, y las tres cierran un hueco por el que se
veía pasar el agua:

  · **F · Cola.** La cola del despachador (`forense/encargos/cola/`, de
    `ADR-240`) no estaba en ninguna de las cinco secciones de la v1.0 —
    `seccion_d` hace `glob` PLANO sobre `forense/encargos/*.md` y deja
    `cola/` fuera de su universo **a propósito**, para no tentar a la
    skill a marcar `CONSUMIDO` un encargo que todavía no se ejecutó. El
    efecto lateral era que la cola sólo se veía abriendo el directorio a
    mano. F la mira: los cuatro estados con su edad, la prueba de
    huérfano, y la línea de cola vacía.
  · **G · `PENDIENTE-DE-MESA`.** Lo que `milpa/*.yaml` deja nombrado como
    pendiente de mesa tampoco tenía sección.
  · **Pie · falsadores.** Cinco piezas de esta familia caducan «en un
    mes» y ninguna decía desde qué día. Ahora la fecha se deriva del
    propio archivo y el pie dice cuándo vence cada una.

Ninguna de las tres decide nada, igual que las cinco anteriores: F
nombra huérfanos y no los resetea, G nombra pendientes y no los
resuelve, el pie dice qué toca mirar y no lo mira.

v1.2 — VENCIMIENTOS, P2 de `ACTO MAESTRA33-E11 · CRITERIOS-Y-VENCIMIENTOS`
(`forense/encargos/2026-09-01-MAESTRA33-E11-CRITERIOS-Y-VENCIMIENTOS.md`).
Antes de la v1.2 ninguna fila del tablero podía traer una fecha límite:
"esa semana" quedaba flotando hasta que alguien se acordara (firma de
mesa 5, verbatim: "ponle fecha no quiero que se quede volando"). Ahora
`gatea` puede traer `vence: AAAA-MM-DD`, y el digesto ABRE (antes de la
sección A) con dos listas derivadas de esa fecha: `VENCIDAS` (ya pasó,
con los días de retraso) y `vencen esta semana` (próximos 7 días, hoy
incluido). Mismo principio que las demás secciones: nombra, no decide
ni resuelve. `tests/check.py::t22_firmas` (T22(a)/(c)) recibió el mismo
parseo, así que el WARN de cada corrida de la suite también trae los
días de retraso cuando aplica — la memoria mecánica no depende de que
alguien abra el digesto del día.

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

No es defensa hipotética, pero tampoco es lo que una primera versión de
este comentario afirmaba, y la diferencia importa. Medido el 31/ago/2026
contra `af41796`: de las 6 filas ABIERTA del tablero, `FP-179` trae los
rótulos pelados `E3`, `E2`, `E6`, `E10` y `FP-190` trae `E4` en su
texto. Con `--tope-texto 0` los cinco entran al digesto y los cinco se
neutralizan. Con el tope POR DEFECTO (220 caracteres) no entra ninguno:
el primero de `FP-179` empieza en el carácter **229** y el de `FP-190`
en el **486**. Es decir, la corrida por defecto de hoy se salva por
**nueve caracteres**, y se salva por accidente de dónde caen las letras
— no por ninguna garantía.

Decirlo con precisión: es FALSO que la corrida por defecto habría roto
`T25` el primer día. Lo cierto es que el peligro está vivo y latente, y
se materializa por tres vías ordinarias: alguien corre con
`--tope-texto 0` (bandera soportada y documentada en el runbook), el
texto de una fila se edita y el rótulo se corre hacia el principio, o
una fila nueva trae su rótulo dentro de los primeros 220 caracteres. Un
margen de nueve caracteres no es un mecanismo de seguridad; es una
casualidad que nadie eligió y que nadie vigila.

Lo que sí ocurrió, y es independiente del tope: `--verifica-marcadores`
atrapó DOS defectos reales de este mismo archivo mientras se escribía
—la prosa del digesto nombraba el marcador de ranura, y después nombraba
la constante de `tests/check.py` que lo contiene como subcadena—, los
dos con capacidad de romper `T22(b)` en producción.

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
# Un encargo que el arbol declara NO consumido -- el patron que la casa ya
# usa cuando mesa sustituye o devuelve un texto. Vive aqui porque el agente
# NO puede marcarlo CONSUMIDO sin escribir una falsedad, y ninguna
# derivacion por `git log` lo detecta: hay que LEER el archivo.
RE_NO_CONSUMIDO = re.compile(
    r"SUSTITUID[OA]|DEVUELT[OA]-POR-MESA|no ejecutado|no consumido|queda como historia",
    re.I)

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


def plural(n, sing, plur):
    return f"{n} {sing}" if n == 1 else f"{n} {plur}"


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


RE_VENCE = re.compile(r"vence:\s*(\d{4}-\d{2}-\d{2})")


def _vence_de(fila):
    """AAAA-MM-DD si la columna `gatea` trae `vence: AAAA-MM-DD`, si no None.
    Solo la columna `gatea` -- P2 de MAESTRA33-E11 la fija ahí a propósito,
    no en `qué_se_firma` (prosa libre, ya ocupada) ni en ninguna otra."""
    m = RE_VENCE.search(fila.get("gatea", ""))
    if not m:
        return None
    try:
        anio, mes, dia = (int(x) for x in m.group(1).split("-"))
        return datetime.date(anio, mes, dia)
    except ValueError:
        return None


def bloque_vencimientos(raiz, hoy, cuenta):
    """VENCIDAS / vencen esta semana -- P2 de `ACTO MAESTRA33-E11 ·
    CRITERIOS-Y-VENCIMIENTOS`. Abre el digesto, antes de la sección A:
    parsea `vence: AAAA-MM-DD` en la columna `gatea` de cada fila `ABIERTA`
    del tablero (misma fuente que A, mismo lector `lee_tablero`). No
    decide ni resuelve nada -- nombra, igual que el resto del digesto."""
    _, filas, _ = lee_tablero(raiz)
    out = ["## Vencimientos — filas del tablero con `vence:` en `gatea`", "",
           "Comando: lectura directa de `forense/firmas-pendientes.tsv` "
           "(columna `estado` == `ABIERTA`, `gatea` parseada con "
           "`vence:\\s*(\\d{4}-\\d{2}-\\d{2})`).", ""]
    if not filas:
        out += ["Tablero no encontrado o vacío — ver sección A.", ""]
        return out, 0, 0
    con_vence = []
    for f in filas:
        if f.get("estado") != "ABIERTA":
            continue
        v = _vence_de(f)
        if v is not None:
            con_vence.append((f, v))
    if not con_vence:
        out += [f"NINGUNA fila `ABIERTA` trae `vence:` en `gatea`. "
                f"Filas `ABIERTA` examinadas: "
                f"{sum(1 for f in filas if f.get('estado') == 'ABIERTA')} (A.13).", ""]
        return out, 0, 0
    vencidas = sorted((t for t in con_vence if t[1] < hoy), key=lambda t: t[1])
    vencen_semana = sorted((t for t in con_vence
                            if hoy <= t[1] <= hoy + datetime.timedelta(days=6)),
                           key=lambda t: t[1])
    if vencidas:
        out += [f"### VENCIDAS ({len(vencidas)})", ""]
        for f, v in vencidas:
            retraso = (hoy - v).days
            txt = neutraliza(una_linea(f.get("qué_se_firma", ""), 160), cuenta)
            out.append(f"- `{f.get('id', '?')}` — venció **{v.isoformat()}** "
                       f"({plural_dias(retraso)} de retraso): {txt}")
        out.append("")
    else:
        out += ["### VENCIDAS (0)", "", "NINGUNA.", ""]
    if vencen_semana:
        out += [f"### Vencen esta semana ({len(vencen_semana)})", "",
               f"Ventana: `{hoy.isoformat()}` a "
               f"`{(hoy + datetime.timedelta(days=6)).isoformat()}` (7 días, hoy incluido).",
               ""]
        for f, v in vencen_semana:
            faltan = (v - hoy).days
            txt = neutraliza(una_linea(f.get("qué_se_firma", ""), 160), cuenta)
            out.append(f"- `{f.get('id', '?')}` — vence **{v.isoformat()}** "
                       f"(en {plural_dias(faltan)}): {txt}")
        out.append("")
    else:
        out += ["### Vencen esta semana (0)", "", "NINGUNA.", ""]
    return out, len(vencidas), len(vencen_semana)


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
        return out, 0, [], fuente
    out += [f"{len(ramas)} de **{examinadas}** ramas remotas examinadas son distintas "
            f"de `main` (A.13):", ""]
    for r in ramas:
        out.append(f"- `{r}`")
    out += ["",
            "Una rama que sobrevive a su merge es trabajo perdido o trabajo sin "
            "fusionar; el digesto la nombra, no la borra — borrar es de mesa.", ""]
    return out, len(ramas), ramas, fuente


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

    # ── Dos banderas que la skill NECESITA para no escribir una falsedad ──
    #
    # La derivación por `git log --grep=<rótulo>` de la skill es ciega a dos
    # cosas, y las dos ya ocurrieron en este árbol:
    #
    #  (1) RÓTULO COMPARTIDO. `2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md` y
    #      `2026-08-30-MAESTRA32-E3-EXTRACTOR-DTA-v2.md` comparten rótulo; el
    #      grep da EXACTAMENTE un merge (`PR #400`) que toca los dos, así que
    #      el criterio "exactamente un candidato" se satisface para AMBOS.
    #      `forense/encargos/convencion.md` ya advierte esta colisión.
    #  (2) ENCARGO NO CONSUMIDO POR DECLARACIÓN. Ese mismo v1 dice, dentro del
    #      mismo PR: "SUSTITUIDO por v2 (dirección, 30/ago/2026): no ejecutado,
    #      no consumido; queda como historia." Marcarlo CONSUMIDO escribiría
    #      una falsedad que contradice por escrito una decisión de mesa.
    #
    # Ninguna de las dos se ve desde `git log`: hay que mirar los NOMBRES de
    # los otros encargos y LEER el contenido del archivo. El digesto las
    # deriva y las marca; la skill tiene prohibido tocar una fila marcada.
    def _rotulo(ruta):
        return re.sub(r"\.md$", "", os.path.basename(ruta)[11:])

    rot_todos = {p: _rotulo(p) for p in con_fecha}
    def _comparte_rotulo(p):
        r = rot_todos[p]
        return sorted(os.path.basename(q) for q, rq in rot_todos.items()
                      if q != p and (rq.startswith(r) or r.startswith(rq)))

    banderas = {}
    for p in frescos:
        motivos = []
        hermanos = _comparte_rotulo(p)
        if hermanos:
            motivos.append("rótulo compartido con " + ", ".join("`%s`" % h for h in hermanos))
        try:
            with open(p, encoding="utf-8") as fh:
                m = RE_NO_CONSUMIDO.search(fh.read())
            if m:
                motivos.append("el archivo se declara no consumido (`%s`)" % m.group(0))
        except OSError:
            motivos.append("no se pudo leer para verificar")
        if motivos:
            banderas[p] = motivos

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
                "digesto, no edición.",
                "",
                (f"**{len(banderas)} de estos {len(frescos)} van marcados ⚠️ NO MARCAR** "
                 f"— comparten rótulo con otro encargo (y entonces un mismo `PR` satisface "
                 f"la derivación para los dos), o el propio archivo se declara no "
                 f"consumido. La skill tiene prohibido tocarlos: son de mesa."
                 if banderas else
                 f"Ninguno de estos {len(frescos)} lleva bandera de rótulo compartido ni "
                 f"se declara no consumido ({len(frescos)} archivos examinados, A.13)."),
                ""]
        for p in mostrados:
            if p in banderas:
                out.append(f"- ⚠️ `forense/encargos/{os.path.basename(p)}` — **NO "
                           f"MARCAR**: " + "; ".join(banderas[p]))
            else:
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
# F · La cola  ·  G · PENDIENTE-DE-MESA  ·  falsadores del pie
#
# P2/P3 de `ACTO MAESTRA33-E3 · CABLEADO-COLA-DIGESTO`
# (`forense/encargos/2026-08-31-MAESTRA33-E3-CABLEADO-COLA-DIGESTO.md`).
#
# Por qué existen. Hasta v1.0 el digesto cubría A-E: tablero, suite, ramas,
# encargos sin marca, contadores. La COLA (`forense/encargos/cola/`, que el
# despachador de `ADR-240` consume) no estaba en ninguna de las cinco —
# `seccion_d` hace `glob` PLANO sobre `forense/encargos/*.md`, así que
# `cola/` queda fuera de su universo a propósito (lo dice su propia
# derivación declarada). El resultado era una cola que sólo se veía
# abriendo el directorio a mano: exactamente el hueco por el que se filtra
# el agua. F la mira. G mira lo que `milpa/` deja nombrado como pendiente
# de mesa, que tampoco tenía sección.
#
# QUIÉN LEE QUÉ, y por qué no es lo mismo. El DESPACHADOR lee la cola de
# `origin/main` — regla dura: lo que no está en `main` no cuenta, ni para
# ejecutar ni para bloquear. Este DIGESTO lee el ÁRBOL DE TRABAJO, por su
# propio contrato de determinismo (mismo árbol + misma `--fecha` → misma
# salida). Las dos lecturas coinciden en un clon limpio y sincronizado, y
# pueden no coincidir en uno sucio; por eso la sección DECLARA cuál usó.
# No se cambia una por la otra: el digesto que dependiera del remoto
# dejaría de ser determinista, y el despachador que leyera el árbol
# perdería la única compuerta que lo separa de ejecutar lo que le digan.
# ───────────────────────────────────────────────────────────────

RE_ESTADO = re.compile(r"^ESTADO:\s*(\S+)", re.M)
RE_ENTORNO = re.compile(r"^ENTORNO:\s*(\S+)", re.M)
RE_ENCOLADO = re.compile(r"^ENCOLADO:\s*(\d{4}-\d{2}-\d{2})", re.M)
# Renglon de bitacora: `- <fecha> · <ESTADO> · <que paso>`. Solo se ANADE,
# nunca se reescribe, asi que el ULTIMO renglon de un estado dado es la
# fecha en que ese estado empezo.
RE_BITACORA = re.compile(r"^-\s*(\d{4}-\d{2}-\d{2})\s*·\s*([A-Z-]+)\s*·\s*(.*)$", re.M)

ESTADOS_COLA = ("LISTO-NUBE", "EN-CURSO", "CONSUMIDO", "PARO-REPORTADO")


def _lee_item_cola(ruta):
    """Cabecera de un archivo de cola. Solo la cabecera: el cuerpo verbatim
    del encargo (A.3) no se interpreta ni se cita aquí. `^ESTADO:` anclado a
    principio de línea es unívoco por construcción — el cuerpo puede traer la
    cadena `ESTADO:` dentro de una línea, y de hecho el primer elemento de la
    cola la trae (`/acto · ESTADO: LISTO-NUBE`), pero nunca empezando línea."""
    try:
        with open(ruta, encoding="utf-8") as fh:
            s = fh.read()
    except OSError:
        return None
    m_e = RE_ESTADO.search(s)
    m_n = RE_ENTORNO.search(s)
    m_q = RE_ENCOLADO.search(s)
    bit = RE_BITACORA.findall(s)
    return {
        "ruta": ruta,
        "base": os.path.basename(ruta),
        # `codigo` es lo que el despachador usa para derivar su nombre de
        # rama (`claude/despacha-<CODIGO>`): basename sin prefijo de fecha
        # ni extension. Misma derivacion, o el cotejo de F.3 no valdria.
        "codigo": re.sub(r"\.md$", "", os.path.basename(ruta)[11:]),
        "estado": m_e.group(1) if m_e else None,
        "entorno": m_n.group(1) if m_n else None,
        "encolado": m_q.group(1) if m_q else None,
        "bitacora": bit,
    }


def _fecha_de_estado(item, estado):
    """Fecha del ÚLTIMO renglón de bitácora con ese estado; si no hay
    ninguno, la de `ENCOLADO:`; si tampoco, `None`. Nunca se inventa."""
    fechas = [f for f, e, _ in item["bitacora"] if e == estado]
    if fechas:
        return fechas[-1]
    return item["encolado"]


def seccion_f(raiz, hoy, ramas_remotas, fuente_ramas):
    """F · Cola de `forense/encargos/cola/`.

    Cuatro cubos por estado, más la línea de cola vacía. La regla de
    HUÉRFANO es la de `ADR-240` extendida por este acto y escrita en
    `forense/agente-despacho-v1_0.md` §0/P1: un `EN-CURSO` de **más de
    24 h** SIN rama remota propia está huérfano. El digesto lo NOMBRA; ni
    el digesto ni el despachador lo ejecutan ni lo resetean — resetear es
    juicio de mesa.
    """
    d = os.path.join(raiz, "forense", "encargos", "cola")
    out = ["## F · La cola (`forense/encargos/cola/`)", "",
           "Comando: lectura directa de `forense/encargos/cola/*.md` en el "
           "**árbol de trabajo** de este clon (cabecera únicamente: `^ESTADO:`, "
           "`^ENTORNO:`, `^ENCOLADO:` y los renglones de `BITACORA:`; el cuerpo "
           "verbatim del encargo no se interpreta ni se cita). Edad = `--fecha` − "
           "fecha del último renglón de `BITACORA:` con ese estado (o `ENCOLADO:` "
           "si no hay ninguno).", "",
           "⚠️ **El despachador NO lee esto.** Él lee la cola de `origin/main` "
           "(`git ls-tree origin/main -- forense/encargos/cola/`), porque su regla "
           "dura es que lo que no está en `main` no cuenta ni para ejecutar ni "
           "para bloquear. Este digesto lee el árbol para poder ser determinista "
           "(mismo árbol + misma `--fecha` → misma salida). En un clon limpio y "
           "sincronizado las dos lecturas coinciden; en uno sucio pueden no "
           "hacerlo, y entonces manda la del despachador.", ""]

    if not os.path.isdir(d):
        out += ["**COLA VACÍA — dirección debe redactar.** El directorio "
                "`forense/encargos/cola/` no existe en este árbol; archivos "
                "examinados: **0** (A.13). Que la cola no exista todavía no es un "
                "error: nace cuando mesa fusiona el PR que la crea.", ""]
        return out, {"listo_nube": 0, "esperando_caja": 0, "en_curso": 0,
                     "huerfanos": 0, "paro": 0, "total": 0}

    archivos = sorted(glob.glob(os.path.join(d, "*.md")))
    items = [x for x in (_lee_item_cola(p) for p in archivos) if x]
    out.append(f"Archivos `.md` examinados en `forense/encargos/cola/`: "
               f"**{len(archivos)}** (A.13){'' if len(items) == len(archivos) else f'; {len(archivos) - len(items)} no se pudieron leer'}.")

    sin_estado = [i for i in items if i["estado"] not in ESTADOS_COLA]
    if sin_estado:
        out += ["",
                f"⚠️ **{len(sin_estado)} archivo(s) sin una línea `^ESTADO:` de las "
                f"cuatro de la máquina de estados** ({', '.join('`%s`' % e for e in ESTADOS_COLA)}). "
                f"No se clasifican, se nombran: " +
                ", ".join(f"`{i['base']}` (`{i['estado'] or 'sin ESTADO'}`)" for i in sin_estado) +
                ". Un archivo de cola sin estado no lo arregla el digesto: es de mesa."]
    out.append("")

    def _edad(item, estado):
        f = _fecha_de_estado(item, estado)
        n = dias(f, hoy) if f else None
        return f, n

    def _tabla(titulo, filas, nota):
        blq = [f"### {titulo}", ""]
        if not filas:
            blq += [nota, ""]
            return blq
        blq += ["| encargo | desde | edad |", "|---|---|---|"] + filas + [""]
        return blq

    # ── F.1 · LISTO-NUBE en espera ──────────────────────────────
    listo_nube = [i for i in items if i["estado"] == "LISTO-NUBE"
                  and i["entorno"] == "NUBE"]
    filas = []
    for i in sorted(listo_nube, key=lambda x: x["base"]):
        f, n = _edad(i, "LISTO-NUBE")
        filas.append(f"| `{i['base']}` | {f or '?'} | "
                     f"{plural_dias(n) if n is not None else 'no derivable'} |")
    out += _tabla("F.1 · `LISTO-NUBE` · `ENTORNO: NUBE` — esperando turno",
                  filas,
                  f"NINGUNO. Archivos de cola examinados: {len(items)} (A.13).")
    if listo_nube:
        out += ["El primero de esa lista por nombre de archivo es el que tomará el "
                "siguiente tick del despachador: la selección es determinista y "
                "ordena por nombre, que empieza por la fecha.", ""]

    # ── F.2 · esperando CAJA ────────────────────────────────────
    caja = [i for i in items if i["entorno"] == "CAJA"
            and i["estado"] in ("LISTO-NUBE", "LISTO", "LISTO-CAJA")]
    filas = []
    for i in sorted(caja, key=lambda x: x["base"]):
        f, n = _edad(i, i["estado"])
        filas.append(f"| `{i['base']}` | {f or '?'} | "
                     f"{plural_dias(n) if n is not None else 'no derivable'} |")
    out += _tabla("F.2 · `ENTORNO: CAJA` — esperando caja, nadie en nube los toca",
                  filas,
                  f"NINGUNO. Archivos de cola examinados: {len(items)} (A.13).")
    if caja:
        out += ["Estos abren microdato y van a Ubuntu, sin excepción. El "
                "despachador de nube los lista y **no los toca**; que envejezcan es "
                "información de mesa, no un defecto del despachador.", ""]

    # ── F.3 · EN-CURSO, con la prueba de huérfano ───────────────
    #
    # La prueba tiene DOS mitades y solo una es derivable en este entorno:
    #  · RAMA: derivable. `claude/despacha-<CODIGO>` es invariante por
    #    encargo (no lleva la fecha de hoy) justo para que se pueda cotejar.
    #  · PR: NO derivable. `gh` no existe en la nube (medido 31/ago/2026 por
    #    el acto que instauro el despachador), y sin `gh` no hay forma de
    #    preguntar por PRs. Se declara, no se finge: un PR vivo implica una
    #    rama viva, asi que la rama es cota superior segura -- si no hay
    #    rama, tampoco hay PR abierto sobre ella.
    en_curso = [i for i in items if i["estado"] == "EN-CURSO"]
    ramas_set = set(ramas_remotas or [])
    huerfanos = []
    filas = []
    for i in sorted(en_curso, key=lambda x: x["base"]):
        f, n = _edad(i, "EN-CURSO")
        rama = f"claude/despacha-{i['codigo']}"
        tiene = rama in ramas_set
        # >24h = al menos un dia cumplido. La bitacora tiene granularidad de
        # DIA, asi que `n >= 1` es lo mas fino que el dato soporta; afinar mas
        # seria inventar horas que el archivo no trae.
        viejo = (n is not None and n >= 1)
        es_huerfano = viejo and not tiene
        if es_huerfano:
            huerfanos.append((i, f, n, rama))
        filas.append(
            f"| `{i['base']}` | {f or '?'} | "
            f"{plural_dias(n) if n is not None else 'no derivable'} | "
            f"{'sí' if tiene else 'NO'} (`{rama}`) | "
            f"{'**HUÉRFANO**' if es_huerfano else ('en vuelo' if tiene else 'reciente — aún no cumple 24 h')} |")
    out += ["### F.3 · `EN-CURSO` — con la prueba de huérfano", ""]
    if not en_curso:
        out += [f"NINGUNO. Archivos de cola examinados: {len(items)} (A.13). "
                f"Ninguna sesión de nube tiene un encargo en vuelo según el árbol.",
                ""]
    else:
        out += [f"Fuente de las ramas: {fuente_ramas}. Ramas remotas distintas de "
                f"`main` examinadas para este cotejo: **{len(ramas_set)}** (A.13).",
                "",
                "| encargo | `EN-CURSO` desde | edad | ¿rama propia en el remoto? | veredicto |",
                "|---|---|---|---|---|"] + filas + [""]
        out += ["La rama propia es `claude/despacha-<CÓDIGO>`, derivada del nombre "
                "del archivo **sin la fecha de hoy** — invariante por encargo, que "
                "es lo que la hace cotejable. **El PR no es derivable en este "
                "entorno**: `gh` no existe en la nube (medido el 31/ago/2026 por el "
                "acto que instauró el despachador), y sin `gh` no hay manera de "
                "preguntar por PRs. No se finge: la rama es cota superior segura, "
                "porque un PR abierto implica una rama viva.", ""]
    if huerfanos:
        out += [f"⚠️ **{plural(len(huerfanos), 'HUÉRFANO', 'HUÉRFANOS')}.** Un `EN-CURSO` de más de 24 h "
                f"sin rama remota propia es un encargo cuya sesión murió a media "
                f"ejecución: bloquea el candado de todos los ticks siguientes y no "
                f"hay nadie trabajándolo.", ""]
        for i, f, n, rama in huerfanos:
            out.append(f"- `{i['base']}` — `EN-CURSO` desde **{f}** "
                       f"(**{plural_dias(n)}**), sin `{rama}` en el remoto.")
        out += ["",
                "**Ni el digesto ni el despachador lo resetean.** Decidir que una "
                "sesión murió es juicio de mesa. El reset es un commit de una línea "
                "de mesa/dirección que devuelve la cabecera a `LISTO-NUBE` o a "
                "`PARO-REPORTADO` **con la razón**, y añade su renglón de "
                "`BITACORA:`. Hasta que eso ocurra, la cola sigue parada — que es el "
                "comportamiento correcto: preferimos parados que duplicados.", ""]
    elif en_curso:
        out += [f"Ninguno huérfano: los {len(en_curso)} `EN-CURSO` examinados tienen "
                f"rama propia viva o no cumplen todavía 24 h (A.13).", ""]

    # ── F.4 · PARO-REPORTADO sin triaje ─────────────────────────
    #
    # "Sin triaje" = el archivo NO trae ningun renglon de bitacora POSTERIOR
    # al que puso el PARO. Ese renglon posterior es la unica huella que deja
    # mesa cuando lo mira: reencolarlo escribe `LISTO-NUBE`, archivarlo
    # escribe lo que sea, pero SIEMPRE anade renglon (la bitacora solo se
    # anade). Un PARO cuyo ultimo renglon es el suyo propio es un PARO que
    # nadie ha mirado.
    paro = [i for i in items if i["estado"] == "PARO-REPORTADO"]
    sin_triaje = []
    for i in paro:
        est = [e for _, e, _ in i["bitacora"]]
        # ultimo renglon es el del propio PARO -> nadie escribio despues
        if not est or est[-1] == "PARO-REPORTADO":
            sin_triaje.append(i)
    out += ["### F.4 · `PARO-REPORTADO` sin triaje de mesa", ""]
    if not paro:
        out += [f"NINGUNO. Archivos de cola examinados: {len(items)} (A.13). "
                f"Ningún encargo de la cola está parado.", ""]
    else:
        out += [f"`PARO-REPORTADO` en la cola: **{len(paro)}** de {len(items)} "
                f"archivos examinados (A.13). **Sin triaje: {len(sin_triaje)}** — "
                f"«sin triaje» = el último renglón de su `BITACORA:` es el del "
                f"propio paro, así que nadie ha escrito nada después de él.", "",
                "| encargo | parado desde | edad | ¿triaje? |", "|---|---|---|---|"]
        for i in sorted(paro, key=lambda x: x["base"]):
            f, n = _edad(i, "PARO-REPORTADO")
            out.append(f"| `{i['base']}` | {f or '?'} | "
                       f"{plural_dias(n) if n is not None else 'no derivable'} | "
                       f"{'**NO**' if i in sin_triaje else 'sí'} |")
        out += ["",
                "Un `PARO-REPORTADO` **no se reintenta solo**: se queda parado hasta "
                "que mesa lo vuelva a encolar. Que aparezca aquí no pide acción del "
                "despachador — pide lectura de mesa. La razón verbatim del paro vive "
                "en el renglón de `BITACORA:` del propio archivo.", ""]

    # ── F.5 · la linea de cola vacia ────────────────────────────
    #
    # Se emite cuando no hay NINGUN LISTO, ni de nube ni de caja: es el unico
    # caso en que la cola no tiene trabajo autorizado de ninguna clase.
    # Un EN-CURSO o un PARO no son trabajo esperando; son trabajo atascado, y
    # eso ya lo dicen F.3 y F.4.
    if not listo_nube and not caja:
        out += ["### F.5 · Veredicto de cola", "",
                f"**COLA VACÍA — dirección debe redactar.** Ningún encargo `LISTO` "
                f"de ninguna clase: 0 en nube, 0 esperando caja, sobre "
                f"**{len(items)}** archivos de cola examinados (A.13). El "
                f"despachador terminará su próximo tick con cero commits, y hará "
                f"bien. Una cola vacía no es una avería del despachador: es "
                f"información de mesa — significa que dirección no ha encolado "
                f"nada.", ""]
    else:
        out += ["### F.5 · Veredicto de cola", "",
                f"Cola con trabajo: **{len(listo_nube)}** `LISTO-NUBE` en nube y "
                f"**{len(caja)}** esperando caja, sobre "
                f"{plural(len(items), 'archivo examinado', 'archivos examinados')} "
                f"(A.13).", ""]

    return out, {"listo_nube": len(listo_nube), "esperando_caja": len(caja),
                 "en_curso": len(en_curso), "huerfanos": len(huerfanos),
                 "paro": len(paro), "paro_sin_triaje": len(sin_triaje),
                 "total": len(items)}


# ───────────────────────────────────────────────────────────────
# G · PENDIENTE-DE-MESA en `milpa/*.yaml`
# ───────────────────────────────────────────────────────────────

# Clave estructurada que declararia un pendiente de mesa de forma
# inequivoca. Se busca aparte del patron en prosa porque una clave YAML es
# un compromiso del archivo, y una frase en un comentario es una pista.
RE_CLAVE_PENDIENTE = re.compile(
    r"^\s*(requiere_decision|pendiente_de_mesa|decision_de_mesa|"
    r"requiere_mesa|pendiente_mesa)\s*:\s*(\S+)", re.M)
RE_ID_YAML = re.compile(r"^\s*-?\s*id:\s*([A-Za-z0-9_.\-]+)")
RE_FECHA_ISO = re.compile(r"(\d{4}-\d{2}-\d{2})")
RE_FECHA_CASA = re.compile(r"(\d{1,2}/[a-z]{3}/\d{4})")


def seccion_g(raiz):
    """G · pendientes nombrados de mesa dentro de `milpa/*.yaml`.

    Dos rastreos sobre el mismo universo, y se reportan por separado
    porque no dicen lo mismo:

      · el patrón EN PROSA es `RE_MARCADOR_PENDIENTE`, **el mismo** que
        `T22(b)` de la suite persigue y que este archivo ya neutraliza al
        copiar texto. Reusarlo no es economía: si `milpa/` trae un
        positivo, ese texto es a la vez un pendiente de mesa y un riesgo
        vivo para la suite, y conviene que sea el mismo regex el que lo
        vea en los dos sitios.
      · el patrón ESTRUCTURADO son claves YAML (`requiere_decision:` y
        hermanas). Una clave es un compromiso del archivo; una frase en un
        comentario es una pista. No se mezclan.

    El `id` se atribuye al `- id:` inmediatamente anterior, y la fecha del
    acto de origen a la fecha más cercana hacia atrás dentro del mismo
    bloque. Las dos son atribuciones POSICIONALES y se declaran como
    tales: un YAML no lleva escrito de qué acto viene cada línea.
    """
    out = ["## G · `PENDIENTE-DE-MESA` en `milpa/*.yaml`", "",
           "Comando: dos rastreos línea a línea sobre `milpa/*.yaml` — (g.1) el "
           "patrón **en prosa** `RE_MARCADOR_PENDIENTE`, que es el mismo que "
           "persigue `T22(b)` de la suite; (g.2) el patrón **estructurado** de "
           "claves YAML (`requiere_decision:`, `pendiente_de_mesa:`, "
           "`decision_de_mesa:`, `requiere_mesa:`, `pendiente_mesa:`). Se reportan "
           "por separado: una clave es un compromiso del archivo, una frase en un "
           "comentario es una pista.", ""]

    archivos = sorted(glob.glob(os.path.join(raiz, "milpa", "*.yaml")))
    if not archivos:
        out += ["**NO-ENCONTRADO.** Archivos examinados en `milpa/*.yaml`: **0** "
                "(A.13) — el directorio no existe o no tiene `.yaml`.", ""]
        return out, 0

    n_lineas = 0
    hallazgos = []   # (archivo, linea, clase, id, fecha, texto)
    for p in archivos:
        try:
            with open(p, encoding="utf-8") as fh:
                lineas = fh.read().splitlines()
        except OSError:
            continue
        n_lineas += len(lineas)
        id_actual, fecha_actual = None, None
        for n, l in enumerate(lineas, 1):
            m_id = RE_ID_YAML.match(l)
            if m_id:
                id_actual, fecha_actual = m_id.group(1), None
            m_f = RE_FECHA_ISO.search(l) or RE_FECHA_CASA.search(l)
            if m_f:
                fecha_actual = m_f.group(1)
            clase = None
            if RE_CLAVE_PENDIENTE.match(l):
                clase = "clave"
            elif RE_MARCADOR_PENDIENTE.search(l):
                clase = "prosa"
            if clase:
                hallazgos.append((os.path.relpath(p, raiz), n, clase,
                                  id_actual, fecha_actual, l.strip()))

    universo = (f"Universo examinado: **{len(archivos)}** archivo(s) "
                f"`milpa/*.yaml`, **{n_lineas}** líneas en total (A.13): "
                + ", ".join(f"`{os.path.relpath(p, raiz)}`" for p in archivos) + ".")

    if not hallazgos:
        out += [universo, "",
                "**NO-ENCONTRADO — 0 pendientes de mesa.** Ninguna de las "
                f"{n_lineas} líneas examinadas coincide con el patrón en prosa ni "
                "con ninguna de las cinco claves estructuradas. Dicho con "
                "precisión, que es lo que un negativo debe decir: **`milpa/` no "
                "usa hoy ninguna de esas cinco claves** — no es que las traiga en "
                "`false`. Si mañana una regla necesita marcar un pendiente de "
                "mesa, la clave que esta sección leerá es `requiere_decision`, en "
                "positivo; hasta entonces este cero significa «no hay marcador», no "
                "«mesa no tiene nada pendiente en `milpa/`».", ""]
        return out, 0

    n_clave = sum(1 for h in hallazgos if h[2] == "clave")
    out += [universo, "",
            f"**{len(hallazgos)} coincidencia(s)**: {n_clave} por clave "
            f"estructurada, {len(hallazgos) - n_clave} por patrón en prosa.", "",
            "| archivo:línea | clase | `id` atribuido | fecha del acto de origen |",
            "|---|---|---|---|"]
    for arch, n, clase, idv, fecha, _ in hallazgos:
        out.append(f"| `{arch}:{n}` | {clase} | "
                   f"{('`%s`' % idv) if idv else '—'} | {fecha or 'no derivable'} |")
    out += ["",
            "**Las dos últimas columnas son atribuciones POSICIONALES**, y se "
            "declaran como tales: el `id` es el `- id:` inmediatamente anterior en "
            "el archivo, y la fecha es la más cercana hacia atrás dentro del mismo "
            "bloque. Un YAML no lleva escrito de qué acto viene cada línea; si el "
            "bloque no trae fecha, aquí dice `no derivable` en vez de inventarla. "
            "Ningún pendiente se resuelve aquí: resolverlo es de mesa.", ""]
    return out, len(hallazgos)


# ───────────────────────────────────────────────────────────────
# Falsadores vivos — para el pie
# ───────────────────────────────────────────────────────────────
#
# P3 del acto. Todos los falsadores de esta familia de piezas caducan "en
# un mes", y ninguno dice DE QUE DIA cuenta ese mes. Mientras la fecha
# viva solo en la cabeza de quien lo escribio, "en un mes" depende de que
# alguien se acuerde -- y nadie se acuerda. Aqui se DERIVA:
#
#   origen  = la fecha que el propio archivo declara (el prefijo de fecha
#             del encargo que cita, o la primera fecha de la casa de su
#             cabecera). NUNCA de memoria: si el archivo no la trae, la
#             fila dice NO-DERIVABLE y eso es el hallazgo.
#   revision= origen + 30 dias. Treinta, no "un mes de calendario": es lo
#             unico que no obliga a elegir entre 28 y 31, y la diferencia
#             no cambia ninguna decision de mesa.
FALSADORES = (
    ("`/acto`", ".claude/commands/acto.md",
     "no evita ni un acto perdido por compuerta · el tamaño mediano de encargo "
     "no baja 50% · un lote deja pasar un defecto que el formato largo habría "
     "atrapado"),
    ("agente de trámite", "forense/agente-tramite-v1_0.md",
     "un PR `[TRAMITE]` requiere retrabajo de mesa · un PR `[TRAMITE]` toca algo "
     "fuera de su perímetro de tres rutas"),
    ("`/tramite`", ".claude/commands/tramite.md",
     "hereda el falsador del runbook de trámite (§3)"),
    ("agente de despacho", "forense/agente-despacho-v1_0.md",
     "ejecuta algo fuera de la cola o fuera de `main` · dos sesiones de nube "
     "coinciden por su causa"),
    ("`/despacha`", ".claude/commands/despacha.md",
     "hereda el falsador del runbook de despacho (§3)"),
    ("`/revisa`", ".claude/commands/revisa.md",
     "hereda el falsador del runbook de revisión (§3)"),
    ("agente de revisión", "forense/agente-revisor-v1_0.md",
     "(a) falso negativo: mesa fusiona un PR con un defecto que la lista "
     "habría atrapado — se añade el punto, basta uno · (b) falso positivo: "
     "el agente bloquea en falso tres veces — se revisa la lista entera"),
)

MESES_CASA = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
              "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}


def _fecha_origen(texto):
    """(fecha ISO, cómo se derivó) o (None, motivo). Dos vías, en orden de
    fiabilidad: el prefijo de fecha del encargo que el archivo cita (es el
    nombre de un archivo del repo, no prosa), y si no, la primera fecha de
    la casa (`31/ago/2026`) de su cabecera."""
    m = re.search(r"forense/encargos/(\d{4}-\d{2}-\d{2})-", texto)
    if m:
        return m.group(1), "prefijo de fecha del encargo que el archivo cita"
    m = re.search(r"\b(\d{1,2})/([a-z]{3})/(\d{4})\b", texto[:4000])
    if m and m.group(2) in MESES_CASA:
        return ("%s-%02d-%02d" % (m.group(3), MESES_CASA[m.group(2)], int(m.group(1))),
                f"primera fecha de la casa de su cabecera (`{m.group(0)}`)")
    return None, "el archivo no declara ninguna fecha derivable"


def _falsador_vivo(texto):
    """¿El archivo declara todavía un falsador «a un mes»? Si alguien lo
    quita, esta sección deja de listarlo — y eso es correcto: un falsador
    borrado no es un falsador vencido."""
    return bool(re.search(r"en un mes", texto))


def bloque_falsadores(raiz, hoy):
    out = ["### Falsadores vivos y su fecha de revisión", "",
           "Comando: lectura de cada runbook/skill de la lista; la fecha de origen "
           "se **deriva del propio archivo** (el prefijo de fecha del encargo que "
           "cita, o la primera fecha de la casa de su cabecera), nunca de memoria; "
           "revisión = origen **+ 30 días**. Treinta y no «un mes de calendario» "
           "porque es lo único que no obliga a elegir entre 28 y 31, y la "
           "diferencia no cambia ninguna decisión de mesa.", "",
           "| pieza | archivo | falsador «a un mes» | origen | derivación del origen | revisión | estado |",
           "|---|---|---|---|---|---|---|"]
    vencidos, examinados = 0, 0
    for nombre, rel, criterio in FALSADORES:
        p = os.path.join(raiz, rel)
        examinados += 1
        if not os.path.exists(p):
            out.append(f"| {nombre} | `{rel}` | — | — | **NO-ENCONTRADO** — la ruta "
                       f"no existe (1 ruta examinada, A.13) | — | — |")
            continue
        with open(p, encoding="utf-8") as fh:
            s = fh.read()
        if not _falsador_vivo(s):
            out.append(f"| {nombre} | `{rel}` | — | — | el archivo ya no declara un "
                       f"falsador «en un mes» | — | retirado |")
            continue
        origen, como = _fecha_origen(s)
        if not origen:
            out.append(f"| {nombre} | `{rel}` | {criterio} | **NO-DERIVABLE** | "
                       f"{como} | — | ⚠️ sin fecha |")
            continue
        a, m, d = (int(x) for x in origen.split("-"))
        rev = datetime.date(a, m, d) + datetime.timedelta(days=30)
        n = (hoy - rev).days
        if n > 0:
            estado, vencidos = f"⚠️ **VENCIDO hace {plural_dias(n)}**", vencidos + 1
        elif n == 0:
            estado = "⚠️ **vence HOY**"
        else:
            estado = f"faltan {plural_dias(-n)}"
        out.append(f"| {nombre} | `{rel}` | {criterio} | {origen} | {como} | "
                   f"**{rev.isoformat()}** | {estado} |")

    # La lista FALSADORES es FIJA, y una lista fija se queda corta en
    # silencio -- que es justo la clase de hueco que este acto existe para
    # cerrar. El cotejo de abajo la audita contra el arbol: si aparece una
    # pieza nueva con falsador "en un mes" que nadie anadio a la lista, la
    # seccion lo DICE en vez de omitirla. No la anade sola: decidir que una
    # pieza nueva es de esta familia es juicio de mesa.
    universo = sorted(glob.glob(os.path.join(raiz, ".claude", "commands", "*.md")) +
                      glob.glob(os.path.join(raiz, "forense", "agente-*.md")))
    conocidos = {os.path.join(raiz, rel) for _, rel, _ in FALSADORES}
    huerfanas = []
    for q in universo:
        if q in conocidos:
            continue
        try:
            with open(q, encoding="utf-8") as fh:
                if _falsador_vivo(fh.read()):
                    huerfanas.append(os.path.relpath(q, raiz))
        except OSError:
            pass
    out.append("")
    if huerfanas:
        out += [f"⚠️ **{plural(len(huerfanas), 'pieza declara', 'piezas declaran')} un "
                f"falsador «en un mes» y no está en la tabla de arriba**, sobre "
                f"**{len(universo)}** archivo(s) examinado(s) en `.claude/commands/*.md` "
                f"y `forense/agente-*.md` (A.13): "
                + ", ".join(f"`{h}`" for h in huerfanas) +
                ". La tabla no se amplía sola: decidir que una pieza nueva pertenece a "
                "esta familia es de mesa. Mientras tanto, su falsador no tiene fecha.", ""]
    else:
        out += [f"Cotejo contra el árbol: ninguna otra pieza declara un falsador «en un "
                f"mes» fuera de la tabla, sobre **{len(universo)}** archivo(s) "
                f"examinado(s) en `.claude/commands/*.md` y `forense/agente-*.md` "
                f"(A.13). La tabla está completa hoy.", ""]
    if vencidos:
        out += [f"⚠️ **{plural(vencidos, 'falsador vencido', 'falsadores vencidos')}.** Vencer no significa "
                f"que la pieza haya fallado: significa que **toca mirarla**, con el "
                f"criterio que la propia fila cita. Mirarla y anotar el veredicto es "
                f"de mesa; este digesto solo se encarga de que la fecha no dependa "
                f"de que alguien se acuerde.", ""]
    else:
        out += [f"Ninguno vencido hoy. Piezas con falsador examinadas: "
                f"**{examinados}** (A.13).", ""]
    return out, vencidos


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

    venc, n_vencidas, n_vencen_semana = bloque_vencimientos(raiz, fecha, cuenta)
    a, n_ab = seccion_a(raiz, fecha, cuenta, tope_texto)
    b, _ = seccion_b(raiz, sin_suite)
    c, n_ramas, ramas, fuente_ramas = seccion_c(raiz)
    d, n_sin, det_d = seccion_d(raiz, piso, tope_lista)
    e, n_cont = seccion_e(raiz)
    f, res_f = seccion_f(raiz, fecha, ramas, fuente_ramas)
    g, n_pend = seccion_g(raiz)
    fals, n_venc = bloque_falsadores(raiz, fecha)

    pie = ["## Pie · falsadores vivos, neutralización de marcadores y A.13", "",
           ] + fals + [
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
           f"`milpa/procedencia.yaml` · `forense/encargos/cola/*.md` · "
           f"`milpa/*.yaml` · los runbooks y skills de la tabla de falsadores · "
           f"ramas del remoto `origin`. Fuera de ese "
           "universo este digesto no dice nada, y no debe leerse como si dijera.", ""]

    cuerpo = cab + venc + a + b + c + d + e + f + g + pie
    resumen = {"abiertas": n_ab, "ramas": n_ramas, "sin_consumido": n_sin,
               "contadores": n_cont, "neutralizaciones": cuenta.total(),
               "detalle_d": det_d, "sha": sha, "cola": res_f,
               "pendientes_mesa": n_pend, "falsadores_vencidos": n_venc,
               "vencidas": n_vencidas, "vencen_semana": n_vencen_semana}
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

    c = res["cola"]
    print(f"resumen: {res['abiertas']} ABIERTA · {res['ramas']} rama(s) ≠ main · "
          f"{res['sin_consumido']} encargo(s) sin CONSUMIDO · "
          f"cola {c['listo_nube']} LISTO-NUBE / {c['esperando_caja']} caja / "
          f"{c['en_curso']} EN-CURSO ({c['huerfanos']} huérfano(s)) / "
          f"{c['paro']} PARO · {res['pendientes_mesa']} pendiente(s) de mesa · "
          f"{res['falsadores_vencidos']} falsador(es) vencido(s) · "
          f"{res['vencidas']} vencida(s) · {res['vencen_semana']} vencen esta semana · "
          f"{res['neutralizaciones']} neutralización(es) · HEAD {res['sha']}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
