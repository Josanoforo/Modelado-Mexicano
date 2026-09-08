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

v1.3 — DIGESTO INCREMENTAL DE H, P1-P3 de `ACTO AUTO-DIGESTO-1 ·
CAMBIOS-DESDE-EL-ULTIMO-CORTE`
(`forense/encargos/2026-09-08-digesto-incremental-reservas.md`). La
sección H (`ACTO GEN2-T8`) volcaba todo `forense/no-corrido.tsv` cada
corrida, como si todo fuera novedad. Ahora compara por `id` contra el
último digesto versionado en `forense/digesto/`, localizado UNA SOLA VEZ
por su historial de `git log` (nunca por fecha de modificación del
sistema de archivos) y recuperado por el SHA de árbol que ese digesto
declaró — nunca por lo que "hoy daría" el TSV en el árbol de trabajo.
DETERMINISMO DE H, explícito (extiende el párrafo de arriba): misma
`--fecha` + mismo árbol de entrada + misma referencia de comparación →
mismo diff, byte por byte; la referencia se fija una vez al empezar y
no se re-consulta a mitad de la comparación. Cada corte deja una marca
`<!-- H-REF sha_arbol=… nc_sha256=… -->` (invisible en Markdown, no
volátil: ambos valores derivan del árbol, nunca del reloj) para que el
siguiente la recupere. Sin referencia recuperable —primera emisión, TSV
ausente en ese árbol, SHA no resoluble— se declara `SIN-BASE-COMPARABLE`
con la causa, nunca "todo es nuevo". Ver el docstring de `seccion_h()`
para el contrato completo.

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
import csv
import datetime
import glob
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile

import estado_comun as EC

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

# ACTO GEN2-E7 pieza D (D1): el libro GEN1 se cerro con un rotulo mecanico
# (`tools/cierra_libro_gen1.py`). Un encargo asi rotulado NO es un pendiente
# -- es historia declarada -- y §D deja de LISTARLO para pasar a CONTARLO en
# una linea. Listar sesenta archivos que nadie va a abrir es ruido que tapa
# los que si importan.
RE_HISTORICO_GEN1 = re.compile(r"^## HIST[OÓ]RICO-GEN1", re.M)

# Un encargo puede traer una marca que NO es `## CONSUMIDO` y aun asi estar
# cerrado: `## SUSTITUIDO` (mesa lo reemplazo) o `## HISTÓRICO` (quedo como
# historia). Antes de GEN2-E7 pieza D el digesto solo miraba `## CONSUMIDO`,
# asi que esos dos casos se contaban como "sin marca" -- una inexactitud
# medida: los DOS que sobrevivian al cierre del libro son exactamente esos.
# Se cuentan aparte, con su nombre.
RE_MARCA_OTRA = re.compile(r"^## (SUSTITUIDO|HIST[OÓ]RICO)(?!-GEN1)", re.M)

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

# lee_tablero() y _es_abierta() migraron a tools/estado_comun.py (ACTO
# AUTOMATIZA-1-E2 · ESTADO-COMUN, 7/sep/2026) -- primitivas compartidas con
# tools/tablero_programa.py y tests/check.py (T22). Este archivo usa
# EC.lee_tablero/EC.es_abierta; los nombres locales de abajo quedan como
# wrappers para no reescribir cada sitio de llamada de esta sección.
lee_tablero = EC.lee_tablero


def _es_abierta(fila):
    """`estado` es `ABIERTA` con o sin glosa (`ABIERTA -- pendiente de...`).
    Comparar con `==` es ciego a la glosa y subcuenta las filas `ABIERTA`
    del tablero -- defecto real, medido: DIGESTO-2026-09-05 reportó 1 de
    299 cuando por prefijo eran 5. Delega en `estado_comun.es_abierta()`
    (ACTO AUTOMATIZA-1-E2): misma regla `^ABIERTA(\\s|$)`, ahora compartida
    con `tools/tablero_programa.py` y `tests/check.py` (T22)."""
    return EC.es_abierta(fila.get("estado", ""))


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
        if not _es_abierta(f):
            continue
        v = _vence_de(f)
        if v is not None:
            con_vence.append((f, v))
    if not con_vence:
        out += [f"NINGUNA fila `ABIERTA` trae `vence:` en `gatea`. "
                f"Filas `ABIERTA` examinadas: "
                f"{sum(1 for f in filas if _es_abierta(f))} (A.13).", ""]
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
    abiertas = [f for f in filas if _es_abierta(f)]
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
    # Estrategia (ls-remote + respaldo for-each-ref) migrada a
    # estado_comun.ramas_remotas_presentes() (ACTO AUTOMATIZA-1-E2):
    # devuelve TODAS las ramas presentes, sin filtrar `main` -- ese filtro
    # es específico de esta sección y se conserva aquí.
    ramas, fuente = EC.ramas_remotas_presentes(raiz)
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

    marcados, sin_marca, historicos_gen1, marca_otra = [], [], [], []
    for p in con_fecha:
        with open(p, encoding="utf-8") as fh:
            s = fh.read()
        if re.search(r"^## CONSUMIDO", s, re.M):
            marcados.append(p)
        elif RE_HISTORICO_GEN1.search(s):
            # D1: rotulado al cierre de GEN1. No se lista; se cuenta.
            historicos_gen1.append(p)
        elif RE_MARCA_OTRA.search(s):
            marca_otra.append(p)
        else:
            sin_marca.append(p)

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
            f"`HISTÓRICO-GEN1`: **{len(historicos_gen1)}** — rotulados al cierre "
            f"de GEN1 (7/sep/2026, `PR #597`) por `tools/cierra_libro_gen1.py` "
            f"(`ACTO GEN2-E7` pieza D, `D13`). **No se listan**: son historia "
            f"declarada, no pendientes, y GEN2 deriva su perímetro de "
            f"consumidores activos (`E.2`), no de encargos.",
            f"Con otra marca de cierre (`## SUSTITUIDO` / `## HISTÓRICO`): "
            f"**{len(marca_otra)}**" +
            (" — " + ", ".join("`%s`" % os.path.basename(q) for q in marca_otra)
             if marca_otra else "") + ".",
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


def seccion_i(raiz, fecha):
    """I · Rutinas (últimos 7 días) -- `ACTO GEN2-E7` pieza D (D5a).

    Derivada de `forense/rutinas.tsv`, donde cada rutina apenda UNA línea
    por tick. Existe porque un tick que termina en `NADA-QUE-HACER` y un
    tick **que no corrió** se ven idénticos desde fuera —cero commits,
    cero PR— y esa ambigüedad impide saber si una rutina sigue viva.

    La ventana es de 7 días y se declara: una rutina SIN líneas en ese
    plazo no se reporta como "sana y ociosa", se reporta como **SIN
    HUELLA**, que es lo que de verdad se midió."""
    ruta = os.path.join(raiz, "forense", "rutinas.tsv")
    out = ["## I · Rutinas (últimos 7 días)", "",
           "Comando: lectura de `forense/rutinas.tsv` (append-only), acotada a "
           "las líneas con `fecha` en los 7 días previos a la de este digesto. "
           "Cada rutina apenda una línea por tick, incluidos los ticks que no "
           "hicieron nada -- ese es el punto.", ""]
    if not os.path.exists(ruta):
        out += ["**NO-ENCONTRADO.** `forense/rutinas.tsv` no existe (A.13). "
                "Ninguna rutina ha dejado huella todavía.", ""]
        return out, {}
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        filas = [f for f in csv.DictReader(
            (l for l in fh if not l.startswith("#")), delimiter="\t")
            if f.get("fecha")]
    try:
        hoy = fecha if isinstance(fecha, datetime.date) else datetime.date.fromisoformat(fecha)
    except (ValueError, TypeError):
        hoy = datetime.date.today()
    piso = (hoy - datetime.timedelta(days=7)).isoformat()
    ventana = [f for f in filas if f["fecha"] >= piso]

    RUTINAS_VIVAS = ("despacha", "revisa", "tramite")
    por_rutina = {}
    for f in ventana:
        por_rutina.setdefault(f.get("rutina", "(sin rutina)"), []).append(f)

    out += [f"Ventana: **{piso}** a **{hoy.isoformat()}**. Líneas en el "
            f"archivo: **{len(filas)}**; en la ventana: **{len(ventana)}** "
            f"(A.13).", ""]
    out += ["| rutina | ticks | resultados |", "|---|---|---|"]
    for nombre in RUTINAS_VIVAS:
        fs = por_rutina.get(nombre, [])
        if not fs:
            out.append(f"| `{nombre}` | **0** | **SIN HUELLA en la ventana** — "
                       f"no se midió que corriera; no se afirma que no corriera |")
            continue
        res = " · ".join(f"`{x.get('resultado', '?')}`" for x in fs)
        out.append(f"| `{nombre}` | {len(fs)} | {res} |")
    otras = sorted(set(por_rutina) - set(RUTINAS_VIVAS))
    for nombre in otras:
        fs = por_rutina[nombre]
        res = " · ".join(f"`{x.get('resultado', '?')}`" for x in fs)
        out.append(f"| `{nombre}` (no es una de las tres) | {len(fs)} | {res} |")
    out.append("")
    sin_huella = [n for n in RUTINAS_VIVAS if not por_rutina.get(n)]
    if sin_huella:
        out += [f"**{len(sin_huella)} rutina(s) sin huella en la ventana**: "
                + ", ".join(f"`{n}`" for n in sin_huella) +
                ". Una rutina sin huella no es una rutina sana: es una rutina "
                "de la que no se sabe nada.", ""]
    return out, por_rutina


def seccion_j(raiz, fecha, ramas_remotas, fuente_ramas):
    """J · Revisiones -- `ACTO GEN2-E7` pieza D (D5b).

    Los PR `[REVISA]` abiertos o fusionados en la ventana. `gh` no existe
    en este entorno (medido 31/ago/2026), así que el PR no es derivable
    directamente: se deriva por sus DOS huellas en el árbol, y se declara
    que son huellas y no el PR.
    """
    out = ["## J · Revisiones (`[REVISA]`)", "",
           "Comando: `gh` no existe en este entorno, así que un PR no se lee "
           "directamente. Se derivan sus **dos huellas**: las notas "
           "`forense/notas/*-revisa-*.md` (que es lo que un PR `[REVISA]` "
           "post-hoc contiene) y las ramas remotas `claude/revisa-*`. Es una "
           "cota, no el conjunto de PR: un `/revisa` en línea deja su "
           "veredicto como comentario de GitHub y **no** deja huella aquí.", ""]
    dir_notas = os.path.join(raiz, "forense", "notas")
    notas = sorted(glob.glob(os.path.join(dir_notas, "*revisa*.md")))
    try:
        hoy = fecha if isinstance(fecha, datetime.date) else datetime.date.fromisoformat(fecha)
    except (ValueError, TypeError):
        hoy = datetime.date.today()
    piso = (hoy - datetime.timedelta(days=7)).isoformat()
    recientes = [n for n in notas if os.path.basename(n)[:10] >= piso]
    ramas_revisa = [r for r in (ramas_remotas or []) if "revisa" in r]

    out += [f"Notas de revisión en `forense/notas/`: **{len(notas)}** total, "
            f"**{len(recientes)}** desde {piso} (A.13).", ""]
    if recientes:
        for n in recientes:
            out.append(f"- `forense/notas/{os.path.basename(n)}`")
    else:
        out.append("- Ninguna nota de revisión en la ventana.")
    out += ["", f"Ramas remotas `claude/revisa-*`: **{len(ramas_revisa)}** "
            f"(fuente de ramas: {fuente_ramas}).", ""]
    for r in ramas_revisa:
        out.append(f"- `{r}`")
    if not ramas_revisa:
        out.append("- Ninguna.")
    out.append("")
    return out, {"notas": len(recientes), "ramas": len(ramas_revisa)}


# ───────────────────────────────────────────────────────────────
# H · P1/P2 (`ACTO AUTO-DIGESTO-1 · CAMBIOS-DESDE-EL-ULTIMO-CORTE`,
# 8/sep/2026, `forense/encargos/2026-09-08-digesto-incremental-reservas.md`)
# -- contrato de referencia y de comparación del digesto incremental de
# `forense/no-corrido.tsv`. Ver el docstring de `seccion_h()` para el
# resumen operativo; las funciones de abajo son las piezas mecánicas.
# ───────────────────────────────────────────────────────────────

# Marca invisible en Markdown (comentario HTML) que un digesto nuevo deja
# para que el SIGUIENTE la recupere sin ambigüedad. No es metadato volátil:
# `sha_arbol` y `nc_sha256` son ambos derivados del árbol, no del reloj ni
# de un UUID (P1.7). `nc_sha256` puede ser `AUSENTE` cuando el TSV no
# existía en ese árbol (p. ej. antes de `ACTO GEN2-T8`).
RE_H_REF = re.compile(
    r"<!-- H-REF sha_arbol=([0-9a-f]{40}) nc_sha256=([0-9a-f]{64}|AUSENTE) -->")

# Fallback para digestos anteriores a esta pieza: todos declaran su HEAD
# corto en la cabecera (`construye()`), y ADMITIR el SHA corto ahí es
# exactamente lo que P1.3 autoriza -- "únicamente si resuelve de forma
# inequívoca" (se resuelve con `git rev-parse`, nunca a ojo).
RE_HEAD_CABECERA = re.compile(r"sobre el clon en `HEAD` `([0-9a-fA-F]{4,40}|NO-DERIVABLE)`")

_NC_RUTA_REL = os.path.join("forense", "no-corrido.tsv")


def _hash_tsv(texto):
    """sha256 normalizando BOM y finales de línea (P1.1/P2: solo transporte,
    nunca contenido). No usar para nada que exija integridad criptográfica
    fuerte -- es una firma de identidad de corte, no una firma de seguridad."""
    t = texto.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def _git_rev_parse(raiz, ref):
    """Resuelve `ref` a un SHA completo de commit, con argumentos
    estructurados -- nunca interpolación de shell (P1.5). `None` si no
    resuelve (ref inexistente, historial superficial, etc.)."""
    rc, salida = corre(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
                       raiz, timeout=30)
    if rc != 0:
        return None
    sha = salida.strip().splitlines()[0].strip() if salida.strip() else ""
    return sha if re.fullmatch(r"[0-9a-f]{40}", sha) else None


def _git_muestra_archivo(raiz, sha, ruta_rel):
    """`git show <sha>:<ruta_rel>`, o `None` si el objeto no existe en ese
    árbol (el archivo aún no existía, o el SHA no es recuperable)."""
    rc, salida = corre(["git", "show", f"{sha}:{ruta_rel}"], raiz, timeout=30)
    return salida if rc == 0 else None


def _git_arbol_sucio(raiz, ruta_rel):
    """`True` si `ruta_rel` tiene cambios sin commitear frente a `HEAD`
    (P1.6). `git status --porcelain` sobre esa ruta exacta."""
    rc, salida = corre(["git", "status", "--porcelain", "--", ruta_rel], raiz, timeout=30)
    return rc == 0 and bool(salida.strip())


def _localiza_ultimo_digesto(raiz):
    """El último digesto COMPLETADO y VERSIONADO en el historial del
    destino de salida (`forense/digesto/`), anterior a esta emisión
    (P1.2). Se resuelve UNA VEZ por el propio historial de `git log`
    -- nunca por fecha de modificación del sistema de archivos -- y se
    fija durante toda la generación (el resultado se pasa hacia abajo,
    nunca se re-consulta a mitad de la comparación).

    Devuelve (commit_sha, ruta_rel, texto) del digesto más reciente, o
    (None, None, None) si `forense/digesto/` no tiene ningún commit
    (primera vez que se publica cualquier digesto)."""
    rc, salida = corre(["git", "log", "--format=%H", "-n", "1", "--",
                        "forense/digesto/"], raiz, timeout=30)
    if rc != 0 or not salida.strip():
        return None, None, None
    sha = salida.strip().splitlines()[0].strip()
    rc2, listado = corre(["git", "show", "--name-only", "--format=",
                          sha, "--", "forense/digesto/"], raiz, timeout=30)
    if rc2 != 0:
        return sha, None, None
    candidatos = sorted(l.strip() for l in listado.splitlines()
                        if l.strip().endswith(".md"))
    if not candidatos:
        return sha, None, None
    ruta_rel = candidatos[-1]  # el más reciente por nombre (DIGESTO-<fecha>)
    texto = _git_muestra_archivo(raiz, sha, ruta_rel)
    return sha, ruta_rel, texto


def _parse_referencia_h(raiz, texto_digesto):
    """Extrae del texto de un digesto anterior la referencia que declaró
    para SU PROPIO corte de entrada: (sha_arbol_completo, nc_sha256_o_None,
    via). `via` documenta de dónde salió, para el A.13 de la sección H.

    Dos formatos, en orden de preferencia:
      1. La marca `H-REF` de esta misma pieza (digestos emitidos por esta
         versión del generador).
      2. La cabecera `HEAD <sha-corto>` que TODO digesto declara desde
         `construye()` -- válida como referencia de árbol para digestos
         más antiguos que no traen `H-REF` todavía; se resuelve con
         `git rev-parse` para admitir el corto SOLO si es inequívoco."""
    if texto_digesto is None:
        return None, None, ("no existe ningún digesto anterior versionado en "
                            "`forense/digesto/` (esta seria la primera emisión)")
    m = RE_H_REF.search(texto_digesto)
    if m:
        sha_arbol = m.group(1)
        nc_sha = None if m.group(2) == "AUSENTE" else m.group(2)
        return sha_arbol, nc_sha, "marca H-REF"
    m2 = RE_HEAD_CABECERA.search(texto_digesto)
    if m2 and m2.group(1) != "NO-DERIVABLE":
        resuelto = _git_rev_parse(raiz, m2.group(1))
        if resuelto:
            return resuelto, None, f"cabecera HEAD corto `{m2.group(1)}` (digesto anterior a H-REF)"
        return None, None, f"cabecera HEAD corto `{m2.group(1)}` no resuelve de forma inequívoca"
    return None, None, "el digesto anterior no declara ninguna referencia de árbol"


def _cruza_no_corrido_abiertas(raiz, n_local):
    """P3: "Usar el conteo de `corrida0 status` cuando el contexto permita
    derivarlo sobre el mismo árbol; contrastarlo en la verificación." Si
    `tools/corrida0.py status --json` no corre (dependencia ausente,
    tiempo agotado, etc.) se declara una lectura local del TSV, sin
    anunciar una corroboración inexistente -- nunca se calla el motivo."""
    rc, salida = corre(["python3", os.path.join(raiz, "tools", "corrida0.py"),
                        "status", "--json"], raiz, timeout=60)
    if rc != 0:
        return (f"`no_corrido_abiertas` **{n_local}** — lectura local del TSV; "
                f"`tools/corrida0.py status --json` no corrió (código {rc}), sin "
                f"corroboración cruzada.")
    try:
        remoto = json.loads(salida).get("no_corrido_abiertas")
    except (json.JSONDecodeError, AttributeError):
        return (f"`no_corrido_abiertas` **{n_local}** — lectura local del TSV; "
                f"la salida de `tools/corrida0.py status --json` no se pudo parsear, "
                f"sin corroboración cruzada.")
    if remoto == n_local:
        return (f"`no_corrido_abiertas` **{n_local}** — coincide con "
                f"`tools/corrida0.py status` sobre el mismo árbol.")
    return (f"`no_corrido_abiertas` **{n_local}** (lectura local del TSV) vs. "
            f"**{remoto}** de `tools/corrida0.py status` — **discrepancia**, "
            f"señalada y no resuelta aquí.")


def _lee_tsv_texto(texto):
    """Parsea un TSV de `no-corrido.tsv` desde una cadena (misma norma de
    lectura que el archivo real: `utf-8-sig`, `\\t`). Lanza `ValueError`
    con un mensaje explícito ante ID duplicado o fila sin `id` -- P2:
    "ID duplicado, TSV inválido o esquema incompatible: error explícito;
    no emitir un diff aparentemente válido"."""
    t = texto.lstrip("﻿")
    filas = list(csv.DictReader(io.StringIO(t), delimiter="\t"))
    vistos = {}
    for i, f in enumerate(filas):
        rid = (f.get("id") or "").strip()
        if not rid:
            raise ValueError(f"fila {i + 1} sin `id` -- TSV inválido")
        if rid in vistos:
            raise ValueError(f"`id` duplicado: `{rid}` (filas {vistos[rid] + 1} y {i + 1})")
        vistos[rid] = i
    return filas


_CAMPOS_IDENTIDAD = ("id",)
_CAMPO_ESTADO = "estado"


def _compara_cortes(filas_antes, filas_ahora):
    """P2: compara dos cortes por `id`, campo por campo (todos los del
    TSV, no solo los que la tabla visible muestra). Orden determinista
    por `id`. Devuelve un dict con las cinco categorías + metadatos de
    esquema, o lanza `ValueError` si el esquema cambiado ya no permite
    comparar identidad/estado con seguridad."""
    idx_antes = {f["id"].strip(): f for f in filas_antes}
    idx_ahora = {f["id"].strip(): f for f in filas_ahora}

    cols_antes = set(filas_antes[0].keys()) if filas_antes else set()
    cols_ahora = set(filas_ahora[0].keys()) if filas_ahora else set()
    agregadas = sorted(cols_ahora - cols_antes)
    retiradas = sorted(cols_antes - cols_ahora)
    if cols_antes and cols_ahora:
        for c in _CAMPOS_IDENTIDAD + (_CAMPO_ESTADO,):
            if c in cols_antes and c not in cols_ahora:
                raise ValueError(
                    f"columna `{c}` (identidad/estado) desapareció del esquema -- "
                    f"no se puede comparar identidad ni estado con seguridad")

    campos_comunes = sorted((cols_antes & cols_ahora) or cols_ahora) or ["id", "estado"]

    nuevas, cambios_estado, modificadas, ausentes, sin_cambio = [], [], [], [], []
    todos_ids = sorted(set(idx_antes) | set(idx_ahora))
    for rid in todos_ids:
        antes = idx_antes.get(rid)
        ahora = idx_ahora.get(rid)
        if antes is None:
            nuevas.append((rid, ahora))
            continue
        if ahora is None:
            ausentes.append((rid, antes))
            continue
        cambio_estado = (antes.get(_CAMPO_ESTADO) or "") != (ahora.get(_CAMPO_ESTADO) or "")
        campos_distintos = sorted(
            c for c in campos_comunes
            if c != _CAMPO_ESTADO and (antes.get(c) or "") != (ahora.get(c) or ""))
        if not cambio_estado and not campos_distintos:
            sin_cambio.append(rid)
            continue
        tags = []
        if cambio_estado:
            tags.append("CAMBIO-DE-ESTADO")
            cambios_estado.append((rid, antes, ahora))
        if campos_distintos:
            tags.append("MODIFICADA")
            modificadas.append((rid, antes, ahora, campos_distintos))

    afectados = sorted({rid for rid, *_ in nuevas} | {rid for rid, *_ in cambios_estado}
                       | {rid for rid, *_ in modificadas} | {rid for rid, *_ in ausentes})
    return {
        "nuevas": nuevas, "cambios_estado": cambios_estado, "modificadas": modificadas,
        "ausentes": ausentes, "sin_cambio": sin_cambio, "afectados": afectados,
        "columnas_agregadas": agregadas, "columnas_retiradas": retiradas,
    }


def seccion_h(raiz, fecha, base_nc_ref=None, tope_filas=25):
    """H · A.14 -- digesto INCREMENTAL de `forense/no-corrido.tsv`
    (P1-P3 de `ACTO AUTO-DIGESTO-1 · CAMBIOS-DESDE-EL-ULTIMO-CORTE`,
    8/sep/2026). Reemplaza el volcado completo de la v1 de esta sección
    (`ACTO GEN2-T8`) por un diff contra el último corte publicado.

    Referencia (P1): se localiza UNA VEZ el último digesto versionado en
    `forense/digesto/` (o, con `--base-nc-ref`, una referencia explícita
    de diagnóstico -- resuelta con `git`, nunca interpolación de shell),
    se recupera el `no-corrido.tsv` que declaró, y se compara contra el
    corte actual por `id` (P2). Sin referencia recuperable, se declara
    `SIN-BASE-COMPARABLE` -- nunca se afirma que todo es nuevo.

    Devuelve (líneas, dict-resumen) igual que las demás secciones;
    `dict-resumen["no_corrido_abiertas"]` es el conteo vigente de
    abiertas (se preserva aunque la comparación no sea posible) y
    `dict-resumen["h_error"]` (str o None) señala una referencia
    explícita inválida -- la única condición de esta sección que debe
    abortar la escritura del digesto completo (P1.5)."""
    ruta = os.path.join(raiz, _NC_RUTA_REL)
    resumen = {"no_corrido_abiertas": 0, "h_error": None}
    out = ["## H · `NO-CORRIDO / RESERVAS` — digesto incremental (A.14)", "",
           "Comando: diff por `id` de `forense/no-corrido.tsv` contra el último "
           "digesto versionado en `forense/digesto/` (P1/P2 de "
           "`forense/encargos/2026-09-08-digesto-incremental-reservas.md`).", ""]

    if not os.path.exists(ruta):
        out += ["**NO-ENCONTRADO.** `forense/no-corrido.tsv` no existe (A.13).", ""]
        return out, resumen

    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        texto_actual = fh.read()
    try:
        filas_ahora = _lee_tsv_texto(texto_actual)
    except ValueError as exc:
        out += [f"**ERROR** — `forense/no-corrido.tsv` no es un TSV válido: {exc}. "
                f"No se emite un diff aparentemente válido sobre datos inválidos (P2).", ""]
        resumen["h_error"] = f"TSV actual inválido: {exc}"
        return out, resumen

    abiertas = [f for f in filas_ahora if (f.get("estado") or "").strip() == "ABIERTA"]
    resumen["no_corrido_abiertas"] = len(abiertas)

    rc_sha, sha_actual = corre(["git", "rev-parse", "HEAD"], raiz, timeout=30)
    sha_arbol_actual = sha_actual.strip() if rc_sha == 0 else None
    nc_sha256_actual = _hash_tsv(texto_actual)
    sucio = _git_arbol_sucio(raiz, _NC_RUTA_REL)

    # Referencia: explícita (diagnóstico) o auto-seleccionada (P1.2/P1.5).
    if base_nc_ref:
        sha_ref = _git_rev_parse(raiz, base_nc_ref)
        if not sha_ref:
            out += [f"**ERROR** — `--base-nc-ref {base_nc_ref}` no resuelve a un commit "
                    f"real (`git rev-parse --verify`). Una referencia explícita inválida "
                    f"es error; no se sustituye silenciosamente por otra (P1.5).", ""]
            resumen["h_error"] = f"--base-nc-ref inválido: {base_nc_ref!r}"
            return out, resumen
        via_ref = f"explícita (`--base-nc-ref {base_nc_ref}` → `{sha_ref}`)"
        texto_ref_tsv = _git_muestra_archivo(raiz, sha_ref, _NC_RUTA_REL)
        origen_digesto = None
        nc_sha256_ref = None  # diagnóstico: no hay digesto que declare un hash que cotejar
    else:
        sha_digesto, ruta_digesto, texto_digesto = _localiza_ultimo_digesto(raiz)
        origen_digesto = ruta_digesto
        sha_ref, nc_sha256_ref, via_ref = _parse_referencia_h(raiz, texto_digesto)
        texto_ref_tsv = _git_muestra_archivo(raiz, sha_ref, _NC_RUTA_REL) if sha_ref else None

    marca_ref = (f"<!-- H-REF sha_arbol={sha_arbol_actual or '0' * 40} "
                f"nc_sha256={nc_sha256_actual} -->")

    if sha_ref is None or texto_ref_tsv is None:
        causa = (via_ref if sha_ref is None else
                 f"`{_NC_RUTA_REL}` no existe en el árbol `{sha_ref}` "
                 f"({via_ref}) -- probablemente anterior a `ACTO GEN2-T8` (8/sep/2026, "
                 f"introdujo el archivo)")
        out += ["**SIN-BASE-COMPARABLE.**", "",
                f"Motivo: {causa}.", "",
                f"Corte actual: árbol `{sha_arbol_actual or 'NO-DERIVABLE'}`"
                + (" (TSV con cambios locales sin commitear — ver nota abajo)"
                   if sucio else "") + f", `no-corrido.tsv` `sha256:{nc_sha256_actual}`. "
                f"**{len(filas_ahora)}** fila(s) total, **{len(abiertas)}** `ABIERTA`.", "",
                "No se afirma que todas las filas son nuevas ni que no hubo cambios: "
                "esta ejecución solo establece una referencia utilizable para la "
                "siguiente (P1.4).", "", marca_ref, ""]
        return out, resumen

    try:
        filas_antes = _lee_tsv_texto(texto_ref_tsv)
    except ValueError as exc:
        out += [f"**ERROR** — el TSV de referencia (`{sha_ref}`) no es válido: {exc}. "
                f"No se emite un diff sobre una referencia inválida.", "", marca_ref, ""]
        resumen["h_error"] = f"TSV de referencia inválido: {exc}"
        return out, resumen

    if nc_sha256_ref:
        integridad = ("coincide" if _hash_tsv(texto_ref_tsv) == nc_sha256_ref
                      else "NO coincide con la declarada por ese digesto (A.13: "
                           "se compara igual, con esta discrepancia señalada)")
    else:
        integridad = "no declarada por el digesto de referencia (formato anterior a H-REF)"

    try:
        cmp = _compara_cortes(filas_antes, filas_ahora)
    except ValueError as exc:
        out += [f"**ERROR** — esquema incompatible entre el corte de referencia y el "
                f"actual: {exc}.", "", marca_ref, ""]
        resumen["h_error"] = f"esquema incompatible: {exc}"
        return out, resumen

    out += [f"Referencia anterior: árbol `{sha_ref}` (`{via_ref}`"
            + (f", vía `{origen_digesto}`" if origen_digesto else "") + f"); "
            f"hash de su `no-corrido.tsv`: {integridad}.",
            f"Corte actual: árbol `{sha_arbol_actual or 'NO-DERIVABLE'}`"
            + (" — **TSV con cambios locales sin commitear** (esta comparación es "
               "una vista previa; no constituye referencia publicada, ver P1.6)"
               if sucio else "") + f", `no-corrido.tsv` `sha256:{nc_sha256_actual}`.",
            "Comparabilidad: **BASE-COMPARABLE**.", ""]

    if cmp["columnas_agregadas"] or cmp["columnas_retiradas"]:
        out += [f"Cambio de esquema: columnas añadidas: "
                f"{', '.join(f'`{c}`' for c in cmp['columnas_agregadas']) or '(ninguna)'}"
                f"; retiradas: "
                f"{', '.join(f'`{c}`' for c in cmp['columnas_retiradas']) or '(ninguna)'}. "
                f"Comparación limitada a las columnas comunes.", ""]

    n_nuevas, n_ce, n_mod, n_aus = (len(cmp["nuevas"]), len(cmp["cambios_estado"]),
                                     len(cmp["modificadas"]), len(cmp["ausentes"]))
    n_afectados = len(cmp["afectados"])
    if n_nuevas == n_ce == n_mod == n_aus == 0:
        out += [f"**SIN-CAMBIOS.** Cero IDs afectados desde la referencia. Total vigente "
                f"de abiertas: **{len(abiertas)}**.", ""]
    else:
        out += [f"**{n_nuevas}** nueva(s) · **{n_ce}** con cambio de estado · "
                f"**{n_mod}** modificada(s) · **{n_aus}** ausente(s) en el corte actual "
                f"-- **{n_afectados}** ID(s) afectado(s) en total, sin duplicar "
                f"(una fila con cambio de estado Y de contenido cuenta una sola vez "
                f"en este total).", ""]
        filas_tabla = []
        cambio_de = {rid: (a, b) for rid, a, b in cmp["cambios_estado"]}
        mod_de = {rid: (a, b, campos) for rid, a, b, campos in cmp["modificadas"]}
        nueva_de = {rid: f for rid, f in cmp["nuevas"]}
        aus_de = {rid: f for rid, f in cmp["ausentes"]}
        for rid in cmp["afectados"]:
            if rid in nueva_de:
                f = nueva_de[rid]
                filas_tabla.append((rid, "NUEVA", "—",
                                    f.get("estado", "—"), f.get("sucesor") or "—"))
            elif rid in aus_de:
                f = aus_de[rid]
                filas_tabla.append((rid, "AUSENTE-EN-CORTE-ACTUAL", f.get("estado", "—"),
                                    "—", f.get("sucesor") or "—"))
            else:
                tags = []
                antes_estado = ahora_estado = "—"
                sucesor = "—"
                if rid in cambio_de:
                    a, b = cambio_de[rid]
                    tags.append("CAMBIO-DE-ESTADO")
                    antes_estado, ahora_estado = a.get("estado", "—"), b.get("estado", "—")
                    sucesor = b.get("sucesor") or "—"
                if rid in mod_de:
                    a, b, campos = mod_de[rid]
                    tags.append(f"MODIFICADA ({', '.join(campos)})")
                    if antes_estado == "—":
                        antes_estado, ahora_estado = a.get("estado", "—"), b.get("estado", "—")
                    sucesor = b.get("sucesor") or sucesor
                filas_tabla.append((rid, " + ".join(tags), antes_estado, ahora_estado, sucesor))
        tope = tope_filas if tope_filas else len(filas_tabla)
        out += ["| `id` | cambio | antes | después | sucesor |", "|---|---|---|---|---|"]
        for rid, cambio, antes_e, despues_e, sucesor in filas_tabla[:tope]:
            out.append(f"| `{rid}` | {cambio} | {antes_e} | {despues_e} | {sucesor} |")
        if len(filas_tabla) > tope:
            out.append(f"| … | **{len(filas_tabla) - tope} fila(s) más, omitidas por el "
                       f"tope de presentación (`--tope-lista`)** | | | |")
        out.append("")
        out += [f"Total vigente de abiertas (corte actual, sin duplicar): **{len(abiertas)}**.", ""]

    corroboracion = _cruza_no_corrido_abiertas(raiz, len(abiertas))
    out += [f"Inventario completo: `forense/no-corrido.tsv` (**{len(filas_ahora)}** fila(s) "
            f"total). {corroboracion}", "", marca_ref, ""]
    return out, resumen


def construye(raiz, fecha, sin_suite, tope_texto, tope_lista, piso, base_nc_ref=None):
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
    h, res_h = seccion_h(raiz, fecha, base_nc_ref=base_nc_ref, tope_filas=tope_lista)
    n_nc_abiertas = res_h["no_corrido_abiertas"]
    i, res_i = seccion_i(raiz, fecha)
    j, res_j = seccion_j(raiz, fecha, ramas, fuente_ramas)
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
           f"`milpa/*.yaml` · `forense/no-corrido.tsv` · `forense/rutinas.tsv` · "
           f"`forense/notas/*revisa*.md` · los runbooks y skills de "
           f"la tabla de falsadores · ramas del remoto `origin`. Fuera de ese "
           "universo este digesto no dice nada, y no debe leerse como si dijera.", ""]

    cuerpo = cab + venc + a + b + c + d + e + f + g + h + i + j + pie
    resumen = {"abiertas": n_ab, "ramas": n_ramas, "sin_consumido": n_sin,
               "contadores": n_cont, "neutralizaciones": cuenta.total(),
               "detalle_d": det_d, "sha": sha, "cola": res_f,
               "rutinas": res_i, "revisiones": res_j,
               "pendientes_mesa": n_pend, "falsadores_vencidos": n_venc,
               "vencidas": n_vencidas, "vencen_semana": n_vencen_semana,
               "no_corrido_abiertas": n_nc_abiertas, "h_error": res_h["h_error"]}
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
    ap.add_argument("--base-nc-ref", default=None,
                    help="Diagnóstico (P1.5): SHA/ref explícito contra el que comparar "
                         "`forense/no-corrido.tsv`, en vez de auto-seleccionar el último "
                         "digesto versionado. Se resuelve con `git rev-parse --verify`; "
                         "una ref inválida es error, nunca se sustituye por otra.")
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

    # P1.6: en modo publicación (escribe archivo), un `no-corrido.tsv` con
    # cambios locales sin commitear no puede atribuirse a ningún SHA -- se
    # detiene y se exige versionarlo primero. `--stdout` sigue siendo vista
    # previa: puede mostrarlo (seccion_h ya lo declara como tal).
    if not a.stdout and _git_arbol_sucio(raiz, _NC_RUTA_REL):
        print("PARO — `forense/no-corrido.tsv` tiene cambios locales sin commitear. "
              "El digesto de archivo no puede atribuir ese contenido a ningún SHA "
              "(P1.6). Commitea el corte primero, o usa `--stdout` para una vista "
              "previa que declare su hash sin publicarlo.", file=sys.stderr)
        return 2

    texto, res = construye(raiz, fecha, a.sin_suite, a.tope_texto, a.tope_lista,
                           a.piso_encargos, base_nc_ref=a.base_nc_ref)

    if res.get("h_error"):
        print(f"PARO — sección H (P1/P2): {res['h_error']}. El digesto NO se escribe.",
              file=sys.stderr)
        return 2

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
        # Escritura atómica (P3): valida todo el contenido arriba (verifica
        # de marcadores + h_error) antes de tocar el archivo final; escribe
        # a un temporal en el mismo directorio y `os.replace` -- si algo
        # falla a mitad, el digesto anterior queda intacto.
        fd, tmp_path = tempfile.mkstemp(prefix=".digesto-tmp-",
                                        dir=os.path.dirname(salida))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(texto)
            os.replace(tmp_path, salida)
        except BaseException:
            try:
                os.remove(tmp_path)
            except OSError:
                pass
            raise
        print(f"escrito: {os.path.relpath(salida, raiz)}")

    c = res["cola"]
    print(f"resumen: {res['abiertas']} ABIERTA · {res['ramas']} rama(s) ≠ main · "
          f"{res['sin_consumido']} encargo(s) sin CONSUMIDO · "
          f"cola {c['listo_nube']} LISTO-NUBE / {c['esperando_caja']} caja / "
          f"{c['en_curso']} EN-CURSO ({c['huerfanos']} huérfano(s)) / "
          f"{c['paro']} PARO · {res['pendientes_mesa']} pendiente(s) de mesa · "
          f"{res['falsadores_vencidos']} falsador(es) vencido(s) · "
          f"{res['vencidas']} vencida(s) · {res['vencen_semana']} vencen esta semana · "
          f"{res['neutralizaciones']} neutralización(es) · "
          f"no_corrido_abiertas {res['no_corrido_abiertas']} · HEAD {res['sha']}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
