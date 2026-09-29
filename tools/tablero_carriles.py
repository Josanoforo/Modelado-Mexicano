#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tablero_carriles.py -- TABLERO DE CARRILES: un carril por report del
mexicano (los 31 de `corpus/reports/`), derivado por comando y sin una cifra
a mano (ACTO GEN2-TABLERO-CARRILES-1, 28/sep/2026).

Uso (desde la raíz del clon):
    python3 tools/tablero_carriles.py                 # markdown del bloque a stdout
    python3 tools/tablero_carriles.py --json          # los mismos datos, JSON
    python3 tools/tablero_carriles.py --actualiza     # reescribe el bloque derivado de
        forense/tablero/TABLERO-CARRILES.md y docs/tablero-carriles.html
    python3 tools/tablero_carriles.py --crosswalk     # escribe canon/crosswalk-carriles-v1_0.tsv
    python3 tools/tablero_carriles.py --verifica      # 0 si crosswalk, md y html casan con la derivación

Qué NO hace: no mide, no adopta, no descarga, no cierra stoppers; los muestra
con su sucesor. No decide nada (§2 del encargo: «el tablero no decide nada»).

Determinismo: la salida es función del CONTENIDO de los archivos fuente (no de
HEAD, ni de la fecha, ni de la rama). Por eso no hay guardián de origin/main
como en `tablero_programa.py`: correrlo en una rama y en el canal da lo mismo
sobre el mismo árbol. La procedencia se imprime como blob git de cada fuente
(`git hash-object`), que identifica el contenido que se leyó.

Fuera del bloque `<!-- TABLERO-DERIVADO:BEGIN/END -->` el md conserva lo que
tenga (título y «Lectura de dirección», el único texto que un humano teclea,
rotulado como opinión y fechado). `derivados_protegidos.py --solo-derivados`
acepta un [deriva] que sólo cambie dentro del bloque.

─────────────────────────── REGLAS DECLARADAS ───────────────────────────
(las constantes viven sólo aquí; el tablero las imprime en «Cómo leer»)

UNIÓN report ↔ dominio (P1). Dominios del carril = `dominio` de sus filas en
  `canon/mapa-dominios-v1_1.tsv`, con peso = afirmaciones del dominio / total
  del carril. NÚCLEO = dominios con peso ≥ NUCLEO_PESO_MIN, más siempre el (los)
  de mayor peso.
UNIÓN report ↔ instrumento. Un instrumento es un token del VOCABULARIO citado
  como palabra (sensible a mayúsculas; o por ALIAS) en `instrumento_ola` o
  `programa_id` de la afirmación. VOCABULARIO = programas de
  `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` ∪ `instrumento` del
  catálogo v1.3 ∪ `programa_id` del mapa ∪ EXTRA, menos NO_INSTRUMENTO.
UNIÓN report ↔ catálogo. El catálogo no trae `report`: la unión pasa por
  dominio (y el instrumento se marca con * si el carril lo cita).
UNIÓN report ↔ regla. Basename de `fuentes` en `canon/reglas-contrastadas-v1_0.tsv`
  (v1 y v2 son homónimos). `origen` NO nombra el report (dice TABLA-C3-1 /
  REPORT-V1 / REPORT-V2). Filas cuyo `texto` empieza con «#» son encabezados
  de sección, no reglas, y se excluyen (se cuentan aparte).
UNIÓN report ↔ familia 2027. La familia alimenta al carril si su instrumento
  (prefijo del nombre de familia) está entre los instrumentos que cita.

SEMÁFORO (se evalúa en este orden):
  GRIS     = dominio principal ∈ DOMINIOS_FIREWALL, o la fracción de afirmaciones
             NO-MEDIBLE-POR-DISEÑO es > GRIS_NO_MEDIBLE_MIN (lo que el mapa marca).
  ROJO     = ningún dominio NÚCLEO tiene cifra adoptada en el catálogo v1.3.
  VERDE    = todo dominio NÚCLEO tiene ≥ 1 cifra adoptada y la fracción de reglas
             con dictamen distinto de SIN-CIFRA-GEN2 es ≥ VERDE_REGLAS_MIN
             (0 reglas cuenta como fracción 0).
  AMARILLO = el resto: hay cifra adoptada pero reglas mayoritariamente sin cifra,
             o reglas con dictamen pero algún NÚCLEO sin cifra.
  «Cifra adoptada» = fila del catálogo con estado_adopcion ADOPTADO o
  ADOPTADO-CON-RESERVA-DE-ANCHO; SUSPENDIDA-POR-FIRMA no cuenta.

INSTRUMENTOS DEL NÚCLEO = los citados por afirmaciones de dominios NÚCLEO. Los
  stoppers de firma, reserva, NC, CALC y en vuelo, y la validación ciega, casan
  contra ellos (un instrumento citado una vez en un dominio secundario no mueve
  el carril). Dentro de cada categoría los stoppers se ordenan por relevancia
  (afirmaciones del carril que citan lo casado) y luego por id.
STOPPERS y precedencia de la SIGUIENTE ACCIÓN (PRECEDENCIA):
  FIRMA > RESERVA > ADQUISICION > NC-PARO > CALC > EDITORIAL. Actos en vuelo se
  muestran pero no generan acción (ya están en manos de un acto).
  FIRMA       fila ABIERTA de firmas-pendientes cuyo texto nombra un instrumento
              del núcleo o un dominio NÚCLEO (palabra, mayúsculas).
  RESERVA     (a) ola reservada de un instrumento del carril —tabla-final
              `olas_reservadas_al_entrar` o `estado_reserva` del manifiesto (id →
              programa por token)— cuyo año cita alguna afirmación del carril;
              (b) afirmaciones con `reserva_v1_1` no vacía.
  ADQUISICION afirmaciones MEDIBLE-CON-ADQUISICIÓN clasificadas en este orden:
              EN-MANIFIESTO (un id de `datos_id_estado` está en el manifiesto: no
              es stopper, falta medir) · PROGRAMA-OBTENIDO-EN-COLA (la cola tiene
              una fila OBTENIDO del programa; ola no verificada: no es stopper) ·
              COLA-PENDIENTE (hay filas del programa y ninguna OBTENIDO: stopper
              con su estado A4/A5 tal cual) · SIN-FILA-EN-COLA (instrumento
              reconocido sin fila: stopper) · SIN-UNION (ningún instrumento del
              vocabulario: stopper; sucesor = `propietario` del mapa).
  NC-PARO     NC ABIERTA con razón PARO-PREMISA* o PARO-ENTORNO que nombra un
              instrumento del carril.
  CALC        fila de demanda-dictamen con dictamen SIN-BASE-GEN2 o ESPERA-* que
              nombra un instrumento del carril.
  EDITORIAL   fila del INDICE ausente, estado distinto de EN-MAIN, o sin recibo.
  EN-VUELO    encargo de forense/encargos/ sin «## CONSUMIDO» cuyo nombre de
              archivo contiene un instrumento o un dominio NÚCLEO.
QUIÉN PIDE una fuente de la cola (QUIEN_PIDE, por prefijo del estado A4/A5).
"""
from __future__ import annotations

import csv
import glob
import hashlib
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict

csv.field_size_limit(sys.maxsize)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Umbrales: único sitio (el tablero los imprime) ──────────────────────────
NUCLEO_PESO_MIN = 0.20
VERDE_REGLAS_MIN = 0.50
GRIS_NO_MEDIBLE_MIN = 0.50
DOMINIOS_FIREWALL = ("GENETICA", "GENOMICA")
PRECEDENCIA = ("FIRMA", "RESERVA", "ADQUISICION", "NC-PARO", "CALC", "EDITORIAL")
ESTADOS_ADOPTADOS = ("ADOPTADO", "ADOPTADO-CON-RESERVA-DE-ANCHO")
MAX_ITEMS = 5  # stoppers listados por categoría en una tarjeta (el resto se cuenta)

# ── Vocabulario de instrumentos ─────────────────────────────────────────────
# EXTRA: tokens de primera posición de `fuente_canonica` en la cola de
# adquisición que los 31 reports citan como palabra en `instrumento_ola`, y que
# no están en tabla-final ni en el catálogo (derivado en este acto, 28/sep, con
# el recorrido documentado en la nota). Fijo aquí para que el crosswalk dependa
# sólo de tablas versionadas; el tablero audita en vivo si la cola trae tokens
# citados que falten (línea «vocabulario» de Adquisición global).
EXTRA = ("CONDUSEF", "CSES", "ECCO", "ENAFI", "ENCOVID", "ENCUP", "ENEM", "ENNVIH",
         "IECM", "MCPS", "OECD", "PISA", "SESNSP", "SHF", "TEPJF")
# Instituciones o palabras, no instrumentos (evidencia: aparecen como primera
# palabra en la cola o como programa genérico en tabla-final).
NO_INSTRUMENTO = ("INEGI", "INE", "IMSS", "SEGOB", "SHCP", "DGIS", "REPORTE",
                  "SALUD", "MIGRACION", "INVESTIGACION", "MORTALIDAD", "NATALIDAD",
                  "NUPCIALIDAD", "ACCIDENTES", "ADICCIONES", "MUSEOS",
                  "INSTRUMENTO-NO-IDENTIFICADO")
# ALIAS: patrón (regex) → instrumento canónico.
ALIAS = (
    (r"(?<![A-Za-z0-9])EMOVI(?![A-Za-z0-9])", "CEEY_EMOVI"),
    (r"Latinobar[óo]metro|LATINOBAR[ÓO]METRO", "LATINOBAROMETRO"),
    (r"AmericasBarometer", "LAPOP"),
    (r"World Values Survey", "WVS"),
    (r"(?<![A-Za-z0-9])OCDE(?![A-Za-z0-9])", "OECD"),
)
# Quién pide una fuente, por prefijo del estado A4/A5 de la cola (orden importa).
QUIEN_PIDE = (
    ("OBTENIDO-PARCIAL", "caja (completa el payload)"),
    ("OBTENIDO", "nadie (obtenido)"),
    ("SOLICITUD-PREPARADA", "mesa con identidad (solicitud preparada)"),
    ("NO-ACCESIBLE", "mesa con identidad (acceso/registro)"),
    ("NO-ADQUIRIDA-POR-COSTO", "mesa (costo)"),
    ("NO-OBTENIDO-POR-ESTE-AGENTE", "acto de nube (reintento) o caja"),
    ("SIN-FETCH", "acto de nube (abrir la fuente)"),
    ("NO-ENCONTRADO", "acto de nube (/sonda)"),
    ("DIFERIDO-A", "nadie (diferida)"),
    ("SUPERADA-POR", "nadie (superada)"),
    ("CERRADA", "nadie (cerrada)"),
)

# ── Fuentes (clave de procedencia → archivo) ────────────────────────────────
FUENTES = {
    "F1": "canon/mapa-dominios-v1_1.tsv",
    "F2": "canon/catalogo-del-mexicano-v1_3.tsv",
    "F3": "canon/reglas-contrastadas-v1_0.tsv",
    "F4": "corpus/reports-v2/INDICE.md",
    "F5": "data/cola-adquisicion-v1_0.tsv",
    "F6": "data/manifiesto.yaml",
    "F7": "forense/firmas-pendientes.tsv",
    "F8": "forense/no-corrido.tsv",
    "F9": "data/corrida0/demanda-dictamen-v1_0.tsv",
    "F10": "data/corrida0/validaciones-independientes.tsv",
    "F11": "forense/analisis/familias-2027/familias-2027-estado-v1_1.tsv",
    "F12": "forense/analisis/corpus-completo/tabla-final-v1_0.tsv",
    "F13": "forense/encargos/*.md",
    "F14": "canon/crosswalk-carriles-v1_0.tsv",
    "F15": "data/corrida0/aperturas-pendientes-v1_0.tsv",  # GEN2-APERTURAS-PREREGISTRADAS-1
}
LECTOR = {
    "F1": "lee_tsv (csv.DictReader), filas con report corpus/reports/*",
    "F2": "lee_tsv, agrega por (dominio, instrumento, estado_adopcion)",
    "F3": "lee_tsv, report = basename(fuentes)",
    "F4": "indice(): filas de la tabla markdown",
    "F5": "lee_tsv (salta líneas #)",
    "F6": "manifiesto(): campos id y estado_reserva por línea",
    "F7": "lee_tsv, estado ABIERTA*",
    "F8": "lee_tsv, estado ABIERTA*, razón PARO-PREMISA*/PARO-ENTORNO*",
    "F9": "lee_tsv, dictamen SIN-BASE-GEN2 / ESPERA-*",
    "F10": "lee_tsv, join resultado_id → catálogo.result_id",
    "F11": "lee_tsv",
    "F12": "lee_tsv, programa y olas_reservadas_al_entrar",
    "F13": "glob; en vuelo = sin línea «## CONSUMIDO»",
    "F14": "crosswalk() (misma derivación; --verifica compara con el archivo)",
    "F15": "lee_tsv, (programa, año de ola) -> expediente y qué la abre",
}
CMD = "python3 tools/tablero_carriles.py --json"

MD_SALIDA = "forense/tablero/TABLERO-CARRILES.md"
HTML_SALIDA = "docs/tablero-carriles.html"
CROSSWALK = "canon/crosswalk-carriles-v1_0.tsv"
MARCAS = ("<!-- TABLERO-DERIVADO:BEGIN -->", "<!-- TABLERO-DERIVADO:END -->")
ICONO = {"VERDE": "🟢", "AMARILLO": "🟡", "ROJO": "🔴", "GRIS": "⚪"}
ORDEN_SEMAFORO = ("ROJO", "AMARILLO", "VERDE", "GRIS")
TAG = re.compile(r"⟨((?:F\d+|S)(?: (?:F\d+|S))*)⟩")


# ── lectura ─────────────────────────────────────────────────────────────────
def ruta(rel: str) -> str:
    return os.path.join(RAIZ, rel)


def lee_tsv(rel: str) -> list[dict]:
    with open(ruta(rel), encoding="utf-8", errors="replace") as f:
        lineas = [ln for ln in f if not ln.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


def blob(rel: str) -> str:
    """sha1 de blob git del contenido (== `git hash-object <rel>`)."""
    if "*" in rel:
        h = hashlib.sha1()
        for p in sorted(glob.glob(ruta(rel))):
            h.update(os.path.basename(p).encode() + b"\0" + str(_consumido(p)).encode() + b"\n")
        return h.hexdigest()[:12] + " (lista)"
    with open(ruta(rel), "rb") as f:
        d = f.read()
    return hashlib.sha1(b"blob %d\0" % len(d) + d).hexdigest()[:12]


def manifiesto() -> tuple[set, list[tuple[str, str]]]:
    """ids y (id, estado_reserva) leyendo las dos claves por línea; PyYAML puro
    tarda ~9 s sobre 7 198 entradas y el canal lo corre por trozo. El test
    compara este lector contra yaml.safe_load."""
    ids, reservas, actual = set(), [], None
    rid = re.compile(r"^- id:\s*['\"]?([^'\"\s]+)")
    rres = re.compile(r"^\s+estado_reserva:\s*['\"]?(.*?)['\"]?\s*$")
    with open(ruta(FUENTES["F6"]), encoding="utf-8", errors="replace") as f:
        for ln in f:
            m = rid.match(ln)
            if m:
                actual = m.group(1)
                ids.add(actual)
                continue
            m = rres.match(ln)
            if m and actual and m.group(1) and m.group(1) not in ("null", "~"):
                reservas.append((actual, m.group(1)))
    return ids, reservas


def _consumido(p: str) -> bool:
    with open(p, encoding="utf-8", errors="replace") as f:
        return any(ln.startswith("## CONSUMIDO") for ln in f)


def indice() -> dict:
    """Filas de la tabla del INDICE v2 por basename del original v1."""
    out = {}
    with open(ruta(FUENTES["F4"]), encoding="utf-8") as f:
        for ln in f:
            if not ln.startswith("| [") or "../reports/" not in ln:
                continue
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            m = re.search(r"\(\.\./reports/([^)]+\.md)\)", c[0])
            if not m or len(c) < 9:
                continue
            rec = re.search(r"\[([^\]]+)\]\(", c[5])
            out[m.group(1)] = {
                "cmrs": c[3], "estado": c[4],
                "recibo": rec.group(1) if rec else "",
                "regla_adoptada": c[7], "reserva_material": re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", c[8]),
            }
    return out


# ── vocabulario y unión por instrumento ─────────────────────────────────────
def norm_instr(n: str) -> str:
    return re.sub(r"-\d+$", "", n.strip())


def vocabulario(mapa, catalogo_instr, tabla_final) -> list[str]:
    v = {x["programa"] for x in tabla_final}
    v |= {norm_instr(i) for i in catalogo_instr}
    v |= {x["programa_id"] for x in mapa if x["programa_id"]}
    v |= set(EXTRA)
    v -= set(NO_INSTRUMENTO)
    return sorted(t for t in v if len(t) >= 3)


def patrones(vocab):
    pats = [(re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])"), t) for t in vocab]
    pats += [(re.compile(p), t) for p, t in ALIAS]
    return pats


def instrumentos_en(texto: str, pats) -> list[str]:
    return sorted({t for p, t in pats if p.search(texto)})


def tokens_en(texto: str, tokens) -> list[str]:
    return sorted({t for t in tokens if re.search(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", texto)})


def programa_de_id(pid: str, vocab_set) -> str:
    for t in pid.split("_"):
        u = re.sub(r"\d+$", "", t).upper()
        if u in vocab_set:
            return u
    return ""


def programa_cola(fuente: str, pats) -> str:
    primera = re.split(r"[_\-\s.]", fuente)[0]
    hits = instrumentos_en(primera, pats) or instrumentos_en(fuente.split("_")[0], pats)
    return hits[0] if hits else ""


def quien_pide(estado: str) -> str:
    for pref, q in QUIEN_PIDE:
        if estado.startswith(pref):
            return q
    return "SIN-REGLA (estado fuera de QUIEN_PIDE)"


def estado_token(estado: str) -> str:
    return re.split(r"[\s(:]", estado.strip())[0] if estado.strip() else "(vacío)"


# ── semáforo (puro; probado en tests/test_tablero_carriles.py) ───────────────
def semaforo(dominio_principal: str, frac_no_medible: float, nucleo_con_cifra: int,
             nucleo_total: int, frac_reglas_con_dictamen: float) -> tuple[str, str]:
    if dominio_principal in DOMINIOS_FIREWALL:
        return "GRIS", f"dominio {dominio_principal} fuera por firewall genético"
    if frac_no_medible > GRIS_NO_MEDIBLE_MIN:
        return "GRIS", f"NO-MEDIBLE-POR-DISEÑO {frac_no_medible:.0%} > {GRIS_NO_MEDIBLE_MIN:.0%}"
    if nucleo_con_cifra == 0:
        return "ROJO", f"núcleo con cifra adoptada 0/{nucleo_total}"
    if nucleo_con_cifra == nucleo_total and frac_reglas_con_dictamen >= VERDE_REGLAS_MIN:
        return "VERDE", (f"núcleo con cifra {nucleo_con_cifra}/{nucleo_total}; reglas con dictamen "
                         f"{frac_reglas_con_dictamen:.0%} ≥ {VERDE_REGLAS_MIN:.0%}")
    return "AMARILLO", (f"núcleo con cifra {nucleo_con_cifra}/{nucleo_total}; reglas con dictamen "
                        f"{frac_reglas_con_dictamen:.0%} (umbral {VERDE_REGLAS_MIN:.0%})")


def nucleo(pesos: Counter) -> list[str]:
    n = sum(pesos.values())
    if not n:
        return []
    top = max(pesos.values())
    return sorted(d for d, k in pesos.items() if k / n >= NUCLEO_PESO_MIN or k == top)


def titulo(basename: str) -> str:
    t = basename[:-3] if basename.endswith(".md") else basename
    return re.sub(r"\s+", " ", t.replace("__", " · ").replace("_", " ")).strip()


# ── derivación ──────────────────────────────────────────────────────────────
def derivar() -> dict:
    mapa_all = lee_tsv(FUENTES["F1"])
    mapa = [x for x in mapa_all if x["report"].startswith("corpus/reports/")]
    cat = lee_tsv(FUENTES["F2"])
    reglas = lee_tsv(FUENTES["F3"])
    cola = lee_tsv(FUENTES["F5"])
    ids_man, reservas_man = manifiesto()
    firmas = lee_tsv(FUENTES["F7"])
    ncs = lee_tsv(FUENTES["F8"])
    demanda = lee_tsv(FUENTES["F9"])
    valid = lee_tsv(FUENTES["F10"])
    familias = lee_tsv(FUENTES["F11"])
    tfinal = lee_tsv(FUENTES["F12"])
    idx = indice()
    encargos = sorted(p for p in glob.glob(ruta(FUENTES["F13"])) if "-ADENDA-" not in os.path.basename(p))
    en_vuelo = [os.path.basename(p) for p in encargos if not _consumido(p)]

    vocab = vocabulario(mapa, {x["instrumento"] for x in cat}, tfinal)
    vset = set(vocab)
    pats = patrones(vocab)
    filas_leidas = {"F1": len(mapa_all), "F2": len(cat), "F3": len(reglas), "F4": len(idx),
                    "F5": len(cola), "F6": len(ids_man), "F7": len(firmas), "F8": len(ncs),
                    "F9": len(demanda), "F10": len(valid), "F11": len(familias),
                    "F12": len(tfinal), "F13": len(encargos)}

    # catálogo agregado
    cat_agg = defaultdict(Counter)          # (dominio, instr) -> estado -> n
    cat_acot = Counter()                    # (dominio, instr) -> acotadas por validación ciega
    res_a = {}                              # result_id -> (dominio, instr)
    for x in cat:
        k = (x["dominio"], norm_instr(x["instrumento"]))
        cat_agg[k][x["estado_adopcion"]] += 1
        if x["validacion_ciega"].startswith("ACOTADA"):
            cat_acot[k] += 1
        if x["result_id"]:
            res_a[x["result_id"]] = k
    dom_con_cifra = {d for (d, _), c in cat_agg.items() if sum(c[e] for e in ESTADOS_ADOPTADOS)}

    # cola por programa
    cola_prog = defaultdict(list)
    for x in cola:
        p = programa_cola(x["fuente_canonica"], pats)
        if p:
            cola_prog[p].append(x)

    # reservas: programa -> [(ola, fuente, detalle)]
    reservas = defaultdict(list)
    for x in tfinal:
        for ola in [o.strip() for o in x["olas_reservadas_al_entrar"].split(";") if o.strip()]:
            reservas[x["programa"]].append((ola, "F12", "tabla-final olas_reservadas_al_entrar"))
    man_res = defaultdict(Counter)
    for pid, est in reservas_man:
        p = programa_de_id(pid, vset)
        anio = re.search(r"(?:19|20)\d\d", pid)
        if p:
            man_res[(p, anio.group(0) if anio else "sin-año")][est[:40]] += 1
    for (p, anio), c in man_res.items():
        det = "; ".join(f"{e} ×{n}" for e, n in sorted(c.items()))
        reservas[p].append((anio, "F6", f"manifiesto estado_reserva: {det}"))

    # familias por instrumento
    fam_por_instr = defaultdict(list)
    for x in familias:
        fam_por_instr[x["familia"].split("-")[0]].append(x)

    # reglas por report
    reglas_por = defaultdict(list)
    for x in reglas:
        b = os.path.basename(x["fuentes"].split(":")[0])
        reglas_por[b].append(x)

    firmas_ab = [x for x in firmas if x["estado"].startswith("ABIERTA")]
    nc_paro = [x for x in ncs if x["estado"].startswith("ABIERTA")
               and (x["razon"].startswith("PARO-PREMISA") or x["razon"].startswith("PARO-ENTORNO"))]
    calc_pend = [x for x in demanda if x["dictamen"] == "SIN-BASE-GEN2" or x["dictamen"].startswith("ESPERA-")]
    # validaciones: -> (dominio, instr)
    val_rows = []
    for x in valid:
        k = res_a.get(x["resultado_id"])
        if k is None:
            ins = instrumentos_en(x["spec_id"] + " " + x["resultado_id"], pats)
            k = ("", ins[0] if ins else "")
        val_rows.append((k, x["validacion_independiente"]))

    # afirmaciones por report
    por_report = defaultdict(list)
    for x in mapa:
        por_report[x["report"]].append(x)

    carriles = []
    for i, rep in enumerate(sorted(por_report), start=1):
        filas = por_report[rep]
        base = os.path.basename(rep)
        n = len(filas)
        clase = Counter(x["dictamen"] for x in filas)
        pesos = Counter(x["dominio"] for x in filas)
        nuc = nucleo(pesos)
        principal = sorted(pesos.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        ins_por_fila = [instrumentos_en(x["instrumento_ola"] + " " + x["programa_id"], pats) for x in filas]
        instr = Counter(t for s in ins_por_fila for t in s)
        instr_nuc = Counter(t for x, s in zip(filas, ins_por_fila) if x["dominio"] in nuc for t in s)
        gen2_cita = sum(1 for x in filas if re.search(r"(CALC|RESULT)-[A-Z0-9]", x["gen2_existente"]))

        # cifras del catálogo por dominio
        cifras = {}
        for d in sorted(pesos):
            por_i = {ins: c for (dd, ins), c in cat_agg.items() if dd == d}
            if not por_i:
                continue
            cifras[d] = {
                "adoptadas": sum(c["ADOPTADO"] for c in por_i.values()),
                "con_reserva_de_ancho": sum(c["ADOPTADO-CON-RESERVA-DE-ANCHO"] for c in por_i.values()),
                "suspendidas": sum(c["SUSPENDIDA-POR-FIRMA"] for c in por_i.values()),
                "acotadas_validacion": sum(cat_acot[(d, ins)] for ins in por_i),
                "por_instrumento": {ins: sum(c[e] for e in ESTADOS_ADOPTADOS)
                                    for ins, c in sorted(por_i.items())},
            }
        nucleo_con_cifra = sum(1 for d in nuc if d in dom_con_cifra)

        rg = reglas_por.get(base, [])
        rg_enc = [x for x in rg if x["texto"].lstrip().startswith("#")]
        rg_ok = [x for x in rg if not x["texto"].lstrip().startswith("#")]
        rg_dict = Counter(x["dictamen"] for x in rg_ok)
        frac_rg = (sum(v for k, v in rg_dict.items() if k != "SIN-CIFRA-GEN2") / len(rg_ok)) if rg_ok else 0.0

        vc = Counter(v for (d, ins), v in val_rows if (d and d in nuc) or (ins and ins in instr_nuc))
        frac_nm = clase["NO-MEDIBLE-POR-DISEÑO"] / n
        sem, razon = semaforo(principal, frac_nm, nucleo_con_cifra, len(nuc), frac_rg)

        ed = idx.get(base)

        # ── stoppers ──
        st = {k: [] for k in PRECEDENCIA}
        tokens_carril = sorted(set(instr_nuc) | set(nuc))

        def relevancia(hit):
            return sum(instr_nuc.get(t, 0) for t in hit) + sum(pesos.get(t, 0) for t in hit)

        for x in firmas_ab:
            texto = " ".join(x[k] for k in ("qué_se_firma", "gatea", "dónde", "encargo"))
            hit = tokens_en(texto, tokens_carril)
            if hit:
                plazo = re.search(r"PLAZO (\d{4}-\d{2}-\d{2})", x["gatea"])
                st["FIRMA"].append({"id": x["id"], "por": hit, "rel": relevancia(hit), "texto": x["qué_se_firma"][:110],
                                    "sucesor": "mesa firma" + (f" (plazo {plazo.group(1)})" if plazo else "")
                                    + (f"; encargo {os.path.basename(x['encargo'])}" if x["encargo"] else "")})
        # reservas citadas (F15: expediente de apertura por programa × año, GEN2-APERTURAS-PREREGISTRADAS-1)
        aper = {(x["programa"], x["ola"][:4]): x for x in (lee_tsv(FUENTES["F15"]) if os.path.exists(ruta(FUENTES["F15"])) else [])}
        for ins in sorted(instr_nuc):
            for ola, fk, det in reservas.get(ins, []):
                anio = re.match(r"(?:19|20)\d\d", ola)
                if not anio:
                    continue
                citan = sum(1 for x, s in zip(filas, ins_por_fila)
                            if ins in s and anio.group(0) in (x["instrumento_ola"] + " " + x["ola_v1_1"]))
                if citan:
                    fam = [f["familia"] for f in fam_por_instr.get(ins, [])]
                    st["RESERVA"].append({"id": f"{ins} {ola}", "fuente": fk, "rel": citan, "texto": f"{det}; afirmaciones que la citan: {citan}",
                                          "sucesor": (("familia 2027 " + ", ".join(fam)) if fam else
                                          "E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito")
                                          + (lambda a: f"; expediente {a['expediente']} ({a['que_la_abre'][:40]})" if a else "")(
                                              aper.get((ins.upper(), anio.group(0))))})
        res_map = Counter(x["reserva_v1_1"][:90] for x in filas if x["reserva_v1_1"])
        for t, k in sorted(res_map.items()):
            st["RESERVA"].append({"id": "mapa:reserva_v1_1", "fuente": "F1", "rel": k, "texto": f"{t} (afirmaciones: {k})",
                                  "sucesor": "E.6 (reserva declarada en el mapa)"})
        # adquisición
        adq = Counter()
        adq_pend = defaultdict(lambda: {"n": 0})
        sin_union_prop = Counter()
        for x, s in zip(filas, ins_por_fila):
            if x["dictamen"] != "MEDIBLE-CON-ADQUISICIÓN":
                continue
            ids = re.findall(r"[a-z0-9][a-z0-9_]+", x["datos_id_estado"])
            if any(t in ids_man for t in ids):
                adq["EN-MANIFIESTO"] += 1
                continue
            if not s:
                adq["SIN-UNION"] += 1
                sin_union_prop[x["propietario"] or "(sin propietario)"] += 1
                continue
            filas_cola = [c for t in s for c in cola_prog.get(t, [])]
            if any(c["estado_A4A5"] == "OBTENIDO" for c in filas_cola):
                adq["PROGRAMA-OBTENIDO-EN-COLA"] += 1
            elif filas_cola:
                adq["COLA-PENDIENTE"] += 1
                for c in filas_cola:
                    e = adq_pend[c["fuente_canonica"]]
                    e["n"] += 1
                    e.update(estado=c["estado_A4A5"], prioridad=c["prioridad"], origen=c["origen"][:60])
            else:
                adq["SIN-FILA-EN-COLA"] += 1
                e = adq_pend["SIN-FILA-EN-COLA:" + "+".join(s)]
                e["n"] += 1
                e.update(estado="SIN-FILA-EN-COLA", prioridad="", origen="")
        for f, e in sorted(adq_pend.items(), key=lambda kv: (-kv[1]["n"], kv[0])):
            st["ADQUISICION"].append({"id": f, "rel": e["n"], "texto": f"estado {e['estado']}; prioridad {e['prioridad'] or '—'}; "
                                      f"afirmaciones {e['n']}" + (f"; origen {e['origen']}" if e["origen"] else ""),
                                      "sucesor": quien_pide(e["estado"]) if not f.startswith("SIN-FILA")
                                      else "dirección da de alta la fila en la cola (/adquiere)"})
        if adq["SIN-UNION"]:
            props = ", ".join(f"{p} ×{k}" for p, k in sin_union_prop.most_common(3))
            st["ADQUISICION"].append({"id": "SIN-UNION", "rel": adq["SIN-UNION"], "texto": f"afirmaciones {adq['SIN-UNION']} sin instrumento del vocabulario",
                                      "sucesor": f"propietario en el mapa: {props}"})
        for x in nc_paro:
            hit = tokens_en(" ".join(x[k] for k in ("pieza", "que_no_se_corrio", "impacto")), sorted(instr_nuc))
            if hit:
                st["NC-PARO"].append({"id": x["id"], "por": hit, "rel": relevancia(hit), "texto": x["razon"].split()[0][:40] + " · " + x["pieza"][:80],
                                      "sucesor": x["sucesor"][:90] or "SIN-ASIGNAR"})
        for x in calc_pend:
            hit = tokens_en(" ".join(x[k] for k in ("corrida_id", "resultado_id", "cita")), sorted(instr_nuc))
            if hit:
                st["CALC"].append({"id": x["resultado_id"] if x["resultado_id"] not in ("", "CORRIDA") else x["corrida_id"],
                                   "por": hit, "rel": relevancia(hit), "texto": x["dictamen"], "sucesor": x["sucesor"][:90] or "SIN-ASIGNAR"})
        if ed is None:
            st["EDITORIAL"].append({"id": "INDICE", "rel": 0, "texto": "sin fila en el INDICE v2", "sucesor": "C3 (INDICE)"})
        elif ed["estado"] != "EN-MAIN" or not ed["recibo"]:
            st["EDITORIAL"].append({"id": "INDICE", "rel": 0, "texto": f"estado {ed['estado']}; recibo {ed['recibo'] or 'AUSENTE'}",
                                    "sucesor": "C3 (recibo de Claude por SHA)"})
        vuelo_tok = [t.replace("_", "-") for t in tokens_carril]
        vuelo = [e for e in en_vuelo if any(re.search(r"(?<![A-Z0-9])" + re.escape(t) + r"(?![A-Z0-9])", e) for t in vuelo_tok)]

        for k in st:
            st[k].sort(key=lambda it: (-it["rel"], it["id"]))
        fam = [f for ins in sorted(instr) for f in fam_por_instr.get(ins, [])]
        # siguiente acción
        sig = None
        for cat_ in PRECEDENCIA:
            if st[cat_]:
                it = st[cat_][0]
                sig = {"categoria": cat_, "id": it["id"], "sucesor": it["sucesor"], "fuente": it.get("fuente", FK_ST[cat_])}
                break
        if sig is None:
            if fam:
                f0 = fam[0]
                sig = {"categoria": "2027", "id": f0["familia"],
                       "sucesor": f"esperando ola 2027 (familia {f0['familia']}, gate {f0['gate_faltante'][:60]})"}
            else:
                sig = {"categoria": "LISTO", "id": "", "sucesor": "listo para catálogo v1.4"}

        carriles.append({
            "carril": f"CARRIL-{i:02d}", "report": rep, "titulo": titulo(base),
            "report_sha256": filas[0]["report_sha256"], "afirmaciones": n,
            "clase": dict(sorted(clase.items())), "gen2_citado": gen2_cita,
            "dominios": dict(sorted(pesos.items(), key=lambda kv: (-kv[1], kv[0]))),
            "nucleo": nuc, "principal": principal, "instrumentos_nucleo": dict(sorted(instr_nuc.items(), key=lambda kv: (-kv[1], kv[0]))), "instrumentos": dict(sorted(instr.items(), key=lambda kv: (-kv[1], kv[0]))),
            "afirmaciones_sin_instrumento": sum(1 for s in ins_por_fila if not s),
            "cifras": cifras, "nucleo_con_cifra": nucleo_con_cifra,
            "reglas": dict(sorted(rg_dict.items())), "reglas_total": len(rg_ok), "reglas_encabezado": len(rg_enc),
            "frac_reglas_con_dictamen": frac_rg, "validacion": dict(sorted(vc.items())),
            "editorial": ed, "semaforo": sem, "razon": razon, "frac_no_medible": frac_nm,
            "stoppers": st, "adquisicion": dict(sorted(adq.items())), "en_vuelo": vuelo,
            "familias": [{"familia": f["familia"], "estado": f["estado"], "gate": f["gate_faltante"][:80],
                          "firma": f["firma_que_lo_abre"][:80]} for f in fam],
            "siguiente": sig,
        })

    # global de adquisición
    tok_cola_citados = set()
    for x in cola:
        t = re.split(r"[_\-\s.]", x["fuente_canonica"])[0]
        if re.fullmatch(r"[A-Z][A-Z0-9]{2,}", t) and any(
                re.search(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", y["instrumento_ola"]) for y in mapa):
            tok_cola_citados.add(t)
    fuera_vocab = sorted(tok_cola_citados - vset - set(NO_INSTRUMENTO) - {"EMOVI"})
    licencias = Counter()
    lic_sin = 0
    with open(ruta(FUENTES["F6"]), encoding="utf-8", errors="replace") as f:
        cur_lic, en_entrada = None, False
        for ln in f:
            if ln.startswith("- id:"):
                if en_entrada and (cur_lic is None or cur_lic.startswith("NO-DECLARADA")):
                    lic_sin += 1
                en_entrada, cur_lic = True, None
            m = re.match(r"^\s+licencia:\s*['\"]?(.*?)['\"]?\s*$", ln)
            if m and en_entrada:
                cur_lic = m.group(1) if m.group(1) not in ("", "null", "~") else None
        if en_entrada and (cur_lic is None or cur_lic.startswith("NO-DECLARADA")):
            lic_sin += 1
    glob_adq = {
        "cola_por_estado": dict(sorted(Counter(estado_token(x["estado_A4A5"]) for x in cola).items(),
                                       key=lambda kv: (-kv[1], kv[0]))),
        "cola_filas": len(cola),
        "cola_pendientes": [{"fuente": x["fuente_canonica"], "estado": x["estado_A4A5"][:50], "prioridad": x["prioridad"],
                             "quien": quien_pide(x["estado_A4A5"])}
                            for x in cola if estado_token(x["estado_A4A5"]) in
                            ("SOLICITUD-PREPARADA", "NO-ACCESIBLE", "NO-ENCONTRADO", "OBTENIDO-PARCIAL",
                             "NO-OBTENIDO-POR-ESTE-AGENTE", "SIN-FETCH", "NO-ADQUIRIDA-POR-COSTO")
                            or x["estado_A4A5"].startswith("NO-OBTENIDO-POR-ESTE-AGENTE")],
        "manifiesto_payloads": len(ids_man),
        "manifiesto_por_reserva": dict(sorted(Counter(e for _, e in reservas_man).items(), key=lambda kv: (-kv[1], kv[0]))),
        "manifiesto_licencia_sin_resolver": lic_sin,
        "vocabulario": len(vocab), "cola_tokens_citados_fuera_de_vocabulario": fuera_vocab,
    }
    return {
        "carriles": carriles, "adquisicion_global": glob_adq, "familias": familias,
        "procedencia": {k: {"archivo": v, "blob": blob(v), "lector": LECTOR[k], "filas": filas_leidas.get(k)}
                        for k, v in FUENTES.items() if k != "F14"},
        "vocabulario": vocab, "en_vuelo_total": len(en_vuelo),
    }


# ── crosswalk (P1) ──────────────────────────────────────────────────────────
CW_COLS = ("carril", "report_v1", "report_sha256", "titulo", "afirmaciones", "dominios_mapa",
           "dominios_nucleo", "dominios_en_catalogo", "instrumentos_citados", "instrumentos_nucleo",
           "instrumentos_en_catalogo",
           "familias_2027", "report_v2")


def crosswalk_texto(D: dict) -> str:
    cat_dom = set()
    cat_ins = set()
    for x in lee_tsv(FUENTES["F2"]):
        cat_dom.add(x["dominio"])
        cat_ins.add(norm_instr(x["instrumento"]))
    lineas = [
        "# canon/crosswalk-carriles-v1_0.tsv · ACTO GEN2-TABLERO-CARRILES-1 · derivado por "
        "`python3 tools/tablero_carriles.py --crosswalk` (--verifica compara byte a byte). Nunca a mano.",
        "# Regla de unión: dominios = columna `dominio` del mapa v1.1 (peso = afirmaciones del dominio / total del report);"
        f" núcleo = peso ≥ {NUCLEO_PESO_MIN} más el de mayor peso. Instrumentos = tokens del vocabulario (tabla-final ∪ "
        "catálogo v1.3 ∪ programa_id del mapa ∪ EXTRA − NO_INSTRUMENTO, más ALIAS) citados como palabra en "
        "`instrumento_ola`/`programa_id`; n = afirmaciones que lo citan. Catálogo sin `report`: la unión pasa por "
        "dominio × instrumento. Familias 2027: prefijo de la familia ∈ instrumentos citados.",
        "# Celda sin unión: SIN-UNION (razón). Ninguna celda vacía.",
        "\t".join(CW_COLS),
    ]
    for c in D["carriles"]:
        dom = "|".join(f"{d}:{k}" for d, k in c["dominios"].items())
        dcat = "|".join(d for d in c["dominios"] if d in cat_dom) or "SIN-UNION (ningún dominio del report tiene filas en el catálogo v1.3)"
        ins = "|".join(f"{i}:{k}" for i, k in c["instrumentos"].items()) or \
            "SIN-UNION (ninguna afirmación cita un instrumento del vocabulario)"
        inuc = "|".join(f"{i}:{k}" for i, k in c["instrumentos_nucleo"].items()) or \
            "SIN-UNION (ninguna afirmación de un dominio núcleo cita un instrumento del vocabulario)"
        icat = "|".join(i for i in c["instrumentos"] if i in cat_ins) or \
            "SIN-UNION (ningún instrumento citado está en el catálogo v1.3)"
        fam = "|".join(f["familia"] for f in c["familias"]) or \
            "SIN-UNION (ningún instrumento citado es instrumento de una familia 2027)"
        v2 = "corpus/reports-v2/" + os.path.basename(c["report"])
        v2 = v2 if os.path.exists(ruta(v2)) else "SIN-UNION (sin homónimo v2 en el árbol)"
        fila = (c["carril"], c["report"], c["report_sha256"], c["titulo"], str(c["afirmaciones"]), dom,
                "|".join(c["nucleo"]), dcat, ins, inuc, icat, fam, v2)
        lineas.append("\t".join(fila))
    return "\n".join(lineas) + "\n"


# ── render markdown ─────────────────────────────────────────────────────────
def pct(x: float) -> str:
    return f"{x:.0%}"


def lista_items(items, fk):
    out = []
    for it in items[:MAX_ITEMS]:
        f = it.get("fuente", fk)
        por = f" (por {', '.join(it['por'])})" if it.get("por") else ""
        out.append(f"  - `{it['id']}`{por} — {it['texto']} → {it['sucesor']} ⟨{f}⟩")
    if len(items) > MAX_ITEMS:
        out.append(f"  - … y {len(items) - MAX_ITEMS} más (`{CMD}`) ⟨{fk}⟩")
    return out


FK_ST = {"FIRMA": "F7", "RESERVA": "F12 F6 F15", "ADQUISICION": "F1 F5 F6", "NC-PARO": "F8", "CALC": "F9", "EDITORIAL": "F4"}


def tarjeta(c: dict) -> list[str]:
    L = [f"### {ICONO[c['semaforo']]} {c['carril']} · {c['titulo']} ⟨F1 F14⟩", ""]
    L.append(f"- **Semáforo {c['semaforo']}** — {c['razon']} ⟨F1 F2 F3 S⟩")
    cl = c["clase"]
    L.append(f"- **Afirmaciones {c['afirmaciones']}**: medible en corpus {cl.get('MEDIBLE-EN-CORPUS', 0)} · con adquisición "
             f"{cl.get('MEDIBLE-CON-ADQUISICIÓN', 0)} · no medible por diseño {cl.get('NO-MEDIBLE-POR-DISEÑO', 0)} · "
             f"no construible {cl.get('NO-CONSTRUIBLE-EN-CORPUS', 0)}; citan un CALC/RESULT en `gen2_existente`: "
             f"{c['gen2_citado']} ⟨F1⟩")
    tot = c["afirmaciones"]
    doms = " · ".join(f"{d} {k} ({k / tot:.0%}){' núcleo' if d in c['nucleo'] else ''}" for d, k in c["dominios"].items())
    L.append(f"- **Dominios**: {doms} ⟨F1 S⟩")
    ins = " · ".join(f"{i} {k}" for i, k in c["instrumentos"].items()) or "ninguno del vocabulario"
    L.append(f"- **Instrumentos citados** (afirmaciones): {ins}; sin instrumento reconocido: {c['afirmaciones_sin_instrumento']} ⟨F1 F12 S⟩")
    inu = " · ".join(f"{i} {k}" for i, k in c["instrumentos_nucleo"].items()) or "ninguno"
    L.append(f"- **Instrumentos del núcleo** (casan stoppers y validación): {inu} ⟨F1 F12 S⟩")
    if c["cifras"]:
        L.append(f"- **Cifras del catálogo v1.3 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩")
        sec = []
        for d, v in c["cifras"].items():
            if d not in c["nucleo"]:
                sec.append(f"{d} {v['adoptadas'] + v['con_reserva_de_ancho']}")
                continue
            pi = ", ".join(f"{i}{'*' if i in c['instrumentos'] else ''} {n}" for i, n in v["por_instrumento"].items())
            L.append(f"  - {d} (núcleo): {v['adoptadas']} · {v['con_reserva_de_ancho']} · "
                     f"{v['suspendidas']} · {v['acotadas_validacion']} — por instrumento (* = el carril lo cita): {pi} ⟨F2⟩")
        faltan = [d for d in c["nucleo"] if d not in c["cifras"]]
        if faltan:
            L.append(f"  - núcleo sin filas en el catálogo: {', '.join(faltan)} ⟨F2⟩")
        if sec:
            L.append(f"  - dominios secundarios con cifra (adoptadas + con reserva de ancho): {' · '.join(sec)} ⟨F2⟩")
    else:
        L.append("- **Cifras del catálogo v1.3**: ningún dominio del carril tiene filas en el catálogo ⟨F2⟩")
    rg = " · ".join(f"{k} {v}" for k, v in c["reglas"].items()) or "ninguna"
    L.append(f"- **Reglas del report** ({c['reglas_total']}; encabezados excluidos {c['reglas_encabezado']}): {rg}; "
             f"con dictamen distinto de SIN-CIFRA-GEN2 {pct(c['frac_reglas_con_dictamen'])} ⟨F3⟩")
    vv = " · ".join(f"{k} {v}" for k, v in c["validacion"].items()) or "ningún RESULT de sus instrumentos o núcleo"
    L.append(f"- **Validación ciega**: {vv} ⟨F10 F2⟩")
    ed = c["editorial"]
    if ed:
        L.append(f"- **Editorial v2** (C/M/R/S {ed['cmrs']}): {ed['estado']} · recibo {ed['recibo'] or 'AUSENTE'} · "
                 f"regla adoptada: {ed['regla_adoptada']} · reserva material: {ed['reserva_material'][:120]} ⟨F4⟩")
    a = c["adquisicion"]
    if a:
        L.append("- **Adquisición del carril** (afirmaciones con adquisición): "
                 + " · ".join(f"{k} {v}" for k, v in a.items()) + " ⟨F1 F5 F6⟩")
    nst = sum(len(v) for v in c["stoppers"].values())
    if nst:
        fks = " ".join(sorted({f for k in PRECEDENCIA if c["stoppers"][k] for f in FK_ST[k].split()}, key=lambda x: int(x[1:])))
        L.append(f"- **Stoppers** ({nst}): ⟨{fks}⟩")
        for cat_ in PRECEDENCIA:
            its = c["stoppers"][cat_]
            if its:
                L.append(f"  - **{cat_}** ({len(its)}) ⟨{FK_ST[cat_]}⟩")
                L.extend("  " + x for x in lista_items(its, FK_ST[cat_]))
    else:
        L.append("- **Stoppers**: ninguno ⟨F7 F8 F9 F4 F5 F12⟩")
    if c["en_vuelo"]:
        L.append(f"- **Actos en vuelo** (sin CONSUMIDO, por nombre): " + ", ".join(f"`{e}`" for e in c["en_vuelo"][:MAX_ITEMS])
                 + (f" … y {len(c['en_vuelo']) - MAX_ITEMS} más" if len(c["en_vuelo"]) > MAX_ITEMS else "") + " ⟨F13⟩")
    if c["familias"]:
        L.append("- **Frente 2027**: " + " · ".join(f"{f['familia']} ({f['estado']}; gate {f['gate']})" for f in c["familias"]) + " ⟨F11⟩")
    else:
        L.append("- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩")
    s = c["siguiente"]
    fk = s.get("fuente") or FK_ST.get(s["categoria"], "F11" if s["categoria"] == "2027" else "S")
    L.append(f"- **Siguiente acción** [{s['categoria']}]: " + (f"`{s['id']}` → " if s["id"] else "") + f"{s['sucesor']} ⟨{fk}⟩")
    L.append("")
    return L


def render_md(D: dict) -> str:
    C = D["carriles"]
    orden = sorted(C, key=lambda c: (ORDEN_SEMAFORO.index(c["semaforo"]), -c["afirmaciones"], c["carril"]))
    L = ["## Cómo leer", ""]
    L.append(f"Umbrales (único sitio: cabecera de `tools/tablero_carriles.py`): núcleo = dominio con peso ≥ {NUCLEO_PESO_MIN} "
             f"(más el de mayor peso) · VERDE exige cifra adoptada en todo el núcleo y reglas con dictamen ≥ {VERDE_REGLAS_MIN} · "
             f"GRIS = dominio principal en {', '.join(DOMINIOS_FIREWALL)} o NO-MEDIBLE-POR-DISEÑO > {GRIS_NO_MEDIBLE_MIN} · "
             f"a lo más {MAX_ITEMS} stoppers listados por categoría ⟨S⟩")
    L.append("")
    L.append("Precedencia de la siguiente acción: " + " > ".join(PRECEDENCIA) + ". Cada línea con un número lleva "
             "`⟨F…⟩`: el archivo del que sale, con su blob y su lector en «Cadena de procedencia». `S` = regla del script. "
             "El catálogo no trae `report`: la unión carril ↔ cifra pasa por dominio × instrumento. Firmas, reservas, NC, CALC, "
             "actos en vuelo y validación casan con los instrumentos del núcleo y se ordenan por relevancia. ⟨S⟩")
    L.append("")
    cnt = Counter(c["semaforo"] for c in C)
    L.append("## Resumen")
    L.append("")
    L.append(f"Carriles {len(C)}: " + " · ".join(f"{ICONO[s]} {s} {cnt.get(s, 0)}" for s in ORDEN_SEMAFORO) + " ⟨F1 F2 F3 S⟩")
    L.append("")
    L.append("| carril | report | semáforo | afirm. | núcleo con cifra | reglas con dictamen | stoppers | siguiente acción | ⟨⟩ |")
    L.append("|---|---|---|---:|---:|---:|---:|---|---|")
    for c in orden:
        s = c["siguiente"]
        nst = sum(len(v) for v in c["stoppers"].values())
        sig = f"{s['categoria']}: " + (f"`{s['id']}`" if s["id"] else s["sucesor"])
        L.append(f"| {c['carril']} | {c['titulo'][:60]} | {ICONO[c['semaforo']]} {c['semaforo']} | {c['afirmaciones']} | "
                 f"{c['nucleo_con_cifra']}/{len(c['nucleo'])} | {pct(c['frac_reglas_con_dictamen'])} de {c['reglas_total']} | "
                 f"{nst} | {sig} | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |")
    L.append("")

    G = D["adquisicion_global"]
    L.append("## Adquisición — global")
    L.append("")
    L.append(f"Cola de adquisición: {G['cola_filas']} filas; por estado A4/A5 (primer token, tal cual): "
             + " · ".join(f"{k} {v}" for k, v in G["cola_por_estado"].items()) + " ⟨F5⟩")
    L.append("")
    L.append(f"Manifiesto: {G['manifiesto_payloads']} payloads; con `estado_reserva`: "
             + (" · ".join(f"{k} {v}" for k, v in G["manifiesto_por_reserva"].items()) or "ninguno")
             + f"; licencia ausente o NO-DECLARADA: {G['manifiesto_licencia_sin_resolver']} ⟨F6⟩")
    L.append("")
    fv = G["cola_tokens_citados_fuera_de_vocabulario"]
    L.append(f"Vocabulario de instrumentos: {G['vocabulario']} tokens; tokens de la cola citados por los reports y fuera del "
             f"vocabulario: {', '.join(fv) if fv else 'ninguno'} ⟨F12 F2 F1 F5 S⟩")
    L.append("")
    L.append("Fuentes pendientes en la cola (quién la pide, por la regla QUIEN_PIDE):")
    L.append("")
    L.append("| fuente | estado A4/A5 | prioridad | quién la pide | ⟨F5⟩ |")
    L.append("|---|---|---|---|---|")
    for x in G["cola_pendientes"]:
        L.append(f"| `{x['fuente'][:60]}` | {x['estado']} | {x['prioridad'] or '—'} | {x['quien']} | ⟨F5 S⟩ |")
    L.append("")

    L.append("## Frente 2027 ⟨F11⟩")
    L.append("")
    L.append("| familia | ola | estado | gate faltante | firma que lo abre | carriles que alimenta | ⟨⟩ |")
    L.append("|---|---|---|---|---|---|---|")
    for f in D["familias"]:
        cs = [c["carril"] for c in C if any(x["familia"] == f["familia"] for x in c["familias"])]
        L.append(f"| {f['familia']} | {f['ola_objetivo']} | {f['estado'][:60]} | {f['gate_faltante'][:90]} | "
                 f"{f['firma_que_lo_abre'][:70]} | {', '.join(cs) or 'SIN-UNION'} | ⟨F11 F1⟩ |")
    L.append("")

    L.append("## Carriles")
    L.append("")
    for c in orden:
        L.extend(tarjeta(c))

    L.append("## Cadena de procedencia")
    L.append("")
    L.append(f"Todo número de arriba sale de estos archivos por `{CMD}`; «blob» es el `git hash-object` del contenido leído "
             "(la salida no depende de HEAD ni de la fecha). El crosswalk F14 se escribe con `--crosswalk` y `--verifica` lo compara.")
    L.append("")
    L.append("| clave | archivo | blob | lector | filas leídas |")
    L.append("|---|---|---|---|---:|")
    for k, v in D["procedencia"].items():
        L.append(f"| {k} | `{v['archivo']}` | `{v['blob']}` | {v['lector']} | {v['filas'] if v['filas'] is not None else '—'} |")
    L.append(f"| F14 | `{FUENTES['F14']}` | `{blob(FUENTES['F14']) if os.path.exists(ruta(FUENTES['F14'])) else 'AUSENTE'}` | {LECTOR['F14']} | {len(C)} |")
    L.append(f"| S | `tools/tablero_carriles.py` | `{blob('tools/tablero_carriles.py')}` | constantes de la cabecera | — |")
    L.append("")
    return "\n".join(L)


# ── render HTML (misma data: el md renderizado) ─────────────────────────────
def _inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])_([^_\n]+)_(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = TAG.sub(lambda m: f'<span class="dd">⟨{m.group(1)}⟩</span>', t)
    return t


def md_a_html(md: str) -> str:
    out, i, lineas = [], 0, md.split("\n")
    lista = 0

    def cierra_listas(hasta=0):
        nonlocal lista
        while lista > hasta:
            out.append("</li></ul>")
            lista -= 1

    while i < len(lineas):
        ln = lineas[i]
        if ln.startswith("<!--"):
            i += 1
            continue
        if ln.startswith("|"):
            cierra_listas()
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                filas.append([x.strip() for x in lineas[i].strip().strip("|").split("|")])
                i += 1
            out.append('<div class="tabla"><table>')
            out.append("<thead><tr>" + "".join(f"<th>{_inline(x)}</th>" for x in filas[0]) + "</tr></thead><tbody>")
            for f in filas[2:]:
                out.append("<tr>" + "".join(f"<td>{_inline(x)}</td>" for x in f) + "</tr>")
            out.append("</tbody></table></div>")
            continue
        m = re.match(r"^(#{1,4}) (.*)$", ln)
        if m:
            cierra_listas()
            n = len(m.group(1))
            cls = ""
            for s, ic in ICONO.items():
                if m.group(2).startswith(ic):
                    cls = f' class="carril {s.lower()}"'
            out.append(f"<h{n}{cls}>{_inline(m.group(2))}</h{n}>")
            i += 1
            continue
        m = re.match(r"^( *)- (.*)$", ln)
        if m:
            nivel = len(m.group(1)) // 2 + 1
            if nivel > lista:
                while lista < nivel:
                    out.append("<ul><li>" if lista < nivel - 1 else "<ul><li>")
                    lista += 1
            else:
                cierra_listas(nivel)
                out.append("</li><li>")
            out.append(_inline(m.group(2)))
            i += 1
            continue
        cierra_listas()
        if ln.strip():
            out.append(f"<p>{_inline(ln)}</p>")
        i += 1
    cierra_listas()
    return "\n".join(out)


HTML_MARCO = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tablero por carriles</title>
<style>
:root{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6960;--line:#e3e0d8;--card:#ffffff;--code:#f1efe9;
--verde:#2e7d4f;--amarillo:#b7860b;--rojo:#b23a2e;--gris:#7a7a7a}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#161614;--fg:#ecebe6;--mut:#a3a197;
--line:#34332f;--card:#1f1f1c;--code:#2a2926;--verde:#5fbf86;--amarillo:#e0b43c;--rojo:#e47464;--gris:#a0a0a0}}
:root[data-theme="dark"]{--bg:#161614;--fg:#ecebe6;--mut:#a3a197;--line:#34332f;--card:#1f1f1c;--code:#2a2926;
--verde:#5fbf86;--amarillo:#e0b43c;--rojo:#e47464;--gris:#a0a0a0}
html,body{margin:0;background:var(--bg);color:var(--fg)}
body{font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;max-width:1100px;margin:0 auto;padding:16px;
overflow-wrap:anywhere}
h1{font-size:1.6rem;margin:.5rem 0}h2{border-bottom:1px solid var(--line);padding-bottom:.2rem;margin-top:2rem}
h3.carril{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--gris);padding:.5rem .7rem;
border-radius:6px;font-size:1.05rem;margin-top:1.6rem}
h3.verde{border-left-color:var(--verde)}h3.amarillo{border-left-color:var(--amarillo)}h3.rojo{border-left-color:var(--rojo)}
code{background:var(--code);padding:0 .25rem;border-radius:3px;font-size:.88em;word-break:break-all}
.dd{color:var(--mut);font-size:.8em;white-space:nowrap}
.tabla{overflow-x:auto;max-width:100%}table{border-collapse:collapse;font-size:.88rem;width:100%;min-width:760px}
th,td{overflow-wrap:normal}
td:first-child{white-space:nowrap;overflow-wrap:normal}.intro{color:var(--mut)}
th,td{border:1px solid var(--line);padding:.25rem .45rem;vertical-align:top;text-align:left}
th{background:var(--code)}ul{padding-left:1.2rem}li{margin:.15rem 0}
a{color:inherit}
</style>
</head>
<body>
<h1>Tablero por carriles · los 31 reports del mexicano</h1>
<p class="intro">Un carril por report: cómo está, qué lo detiene y cuál es la siguiente acción. Lo escribe
<code>python3 tools/tablero_carriles.py --actualiza</code> y lo publica el canal en cada push a <code>main</code>.
Misma data que <a href="https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/tablero/TABLERO-CARRILES.md">TABLERO-CARRILES.md</a>.</p>
<!-- TABLERO-DERIVADO:BEGIN -->
<!-- TABLERO-DERIVADO:END -->
</body>
</html>
"""

MD_MARCO = """# Tablero por carriles · los 31 reports del mexicano

Un carril por report de `corpus/reports/`: cómo está (evidencia), qué lo detiene (stoppers) y cuál es la siguiente acción. Todo lo que está entre las marcas `TABLERO-DERIVADO` lo escribe `python3 tools/tablero_carriles.py --actualiza` (el canal lo regenera en cada push a `main`); no se edita a mano. Versión web: [docs/tablero-carriles.html](../../docs/tablero-carriles.html). Tablero del programa (GEN1→GEN2): [TABLERO-PROGRAMA.md](TABLERO-PROGRAMA.md).

## Lectura de dirección

<!-- LECTURA-DIRECCION: única sección tecleada por un humano; opinión, fechada. -->
_Opinión de dirección, sin fecha todavía._

<!-- TABLERO-DERIVADO:BEGIN -->
<!-- TABLERO-DERIVADO:END -->
"""


def reemplaza_bloque(texto: str, cuerpo: str) -> str:
    ini, fin = MARCAS
    a, b = texto.find(ini), texto.find(fin)
    if a < 0 or b < a or texto.count(ini) != 1 or texto.count(fin) != 1:
        raise SystemExit(f"error: el archivo no trae exactamente un par de marcas {ini} / {fin}")
    return texto[:a + len(ini)] + "\n" + cuerpo.rstrip("\n") + "\n" + texto[b:]


def genera(D: dict | None = None) -> tuple[str, str]:
    """(md, html) completos, a partir de los archivos actuales (o marcos si faltan)."""
    D = D or derivar()
    p_md, p_html = ruta(MD_SALIDA), ruta(HTML_SALIDA)
    md0 = open(p_md, encoding="utf-8").read() if os.path.exists(p_md) else MD_MARCO
    md = reemplaza_bloque(md0, render_md(D))
    h0 = open(p_html, encoding="utf-8").read() if os.path.exists(p_html) else HTML_MARCO
    # El HTML lleva su propio encabezado: se renderiza el md desde «Lectura de dirección».
    k = md.find("## Lectura de dirección")
    h = reemplaza_bloque(h0, md_a_html(md[k:] if k >= 0 else md))
    return md, h


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--crosswalk" in argv:
        D = derivar()
        with open(ruta(CROSSWALK), "w", encoding="utf-8") as f:
            f.write(crosswalk_texto(D))
        print(f"escrito {CROSSWALK}: {len(D['carriles'])} filas")
        return 0
    if "--verifica" in argv:
        D = derivar()
        md, h = genera(D)
        ok = True
        for rel, esperado in ((CROSSWALK, crosswalk_texto(D)), (MD_SALIDA, md), (HTML_SALIDA, h)):
            actual = open(ruta(rel), encoding="utf-8").read() if os.path.exists(ruta(rel)) else None
            casa = actual == esperado
            ok &= casa
            print(f"{rel}: {'CASA' if casa else 'NO-CASA'}")
        return 0 if ok else 1
    if "--actualiza" in argv:
        D = derivar()
        md, h = genera(D)
        os.makedirs(os.path.dirname(ruta(MD_SALIDA)), exist_ok=True)
        for rel, t in ((MD_SALIDA, md), (HTML_SALIDA, h)):
            with open(ruta(rel), "w", encoding="utf-8") as f:
                f.write(t)
        cnt = Counter(c["semaforo"] for c in D["carriles"])
        print(f"tablero-carriles: {len(D['carriles'])} carriles · " + " · ".join(f"{s} {cnt.get(s, 0)}" for s in ORDEN_SEMAFORO))
        return 0
    D = derivar()
    if "--json" in argv:
        print(json.dumps(D, ensure_ascii=False, indent=1, default=str))
        return 0
    print(render_md(D))
    return 0


if __name__ == "__main__":
    sys.exit(main())
