#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de verificación del corpus · Psicología del Mexicano Contemporáneo

Consolida los checks que se escribieron sueltos durante la sesión del 28/jul/2026.
Cada test corresponde a un ADR o a un defecto documentado.

    python3 tests/check.py           # corre todo
    python3 tests/check.py --strict  # los WARN también fallan

Filosofía: cada ADR que declara un principio necesita un test que FALLE
visiblemente si no se cumple. "Principio declarado sin requisito de salida"
es el patrón que explica casi todos los fallos del programa.
"""
import io, os, re, sys, glob, hashlib, unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRICT = "--strict" in sys.argv
BASELINE_MODE = "--baseline" in sys.argv
FREEZE_MODE = "--freeze" in sys.argv
BASELINE_PATH = os.path.join(ROOT, "tests", "baseline.json")
FAILS, WARNS = [], []

def read(p):
    return io.open(p, encoding="utf-8").read()

def rel(p):
    return os.path.relpath(p, ROOT)

def fail(test, msg):
    FAILS.append((test, msg))

def warn(test, msg):
    (FAILS if STRICT else WARNS).append((test, msg))

def newest(pattern):
    """El archivo vigente de un artefacto versionado. Ordena por versión
    semántica extraída del nombre (v<major>[._]<minor>), no por orden
    lexicográfico de string -- lexicográfico rompe en cuanto una versión
    llega a dos dígitos (`v1_10` ordena antes que `v1_9` como texto, no
    como versión). Un archivo sin versión en el nombre queda al final del
    empate, ordenado por nombre. (Hoy cada patrón que llama a esta función
    resuelve a un único archivo -- verificado -- así que este cambio no
    mueve ningún resultado vigente; es endurecimiento contra el próximo
    salto de versión de dos dígitos, no una corrección de un bug visto.)"""
    hits = glob.glob(os.path.join(ROOT, pattern))
    def _version_key(h):
        m = re.search(r"v(\d+)[._](\d+)", os.path.basename(h))
        version = (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
        return (version, os.path.basename(h))
    hits.sort(key=_version_key)
    return hits[-1] if hits else None

def reports():
    return sorted(glob.glob(os.path.join(ROOT, "corpus", "reports", "*.md")))

def motor_section():
    m = newest("canon/modelo-decision-v*.md")
    if not m:
        return None, ""
    s = read(m)
    try:
        return m, s[s.index("### 3.B"): s.index("## 4 · Protocolo de uso")]
    except ValueError:
        return m, ""

def motor_rules():
    _, sec = motor_section()
    return [l for l in sec.split("\n") if l.startswith("- **SI**")]

def rule_tier(line):
    body = re.split(r"\*\(v[23]", line)[0]
    t = re.findall(r"`\[[^\]]*\]`", body)
    return t[0] if t else None


# ───────────────────────────────────────────────────────────────
# T01 · Fuente única de verdad
# ───────────────────────────────────────────────────────────────
def t01_single_source():
    """gobernanza: 'duplicar la fuente de verdad es el defecto'."""
    for name, pat in [("modelo", "canon/modelo-decision-v*.md"),
                      ("glosario", "canon/glosario-v*.md"),
                      ("gobernanza", "canon/gobernanza-v*.md"),
                      ("estado", "canon/estado-programa-v*.md")]:
        hits = glob.glob(os.path.join(ROOT, pat))
        if len(hits) == 0:
            fail("T01", f"falta el artefacto canónico `{name}`")
        elif len(hits) > 1:
            fail("T01", f"`{name}` tiene {len(hits)} versiones a la vez: "
                        + ", ".join(sorted(os.path.basename(h) for h in hits)))


# ───────────────────────────────────────────────────────────────
# T02 · Duplicados por nombre normalizado y por contenido
# ───────────────────────────────────────────────────────────────
def t02_duplicates():
    def norm(n):
        n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
        return re.sub(r"[^a-z0-9]", "", n)
    by_name, by_hash = defaultdict(list), defaultdict(list)
    for p in glob.glob(os.path.join(ROOT, "**", "*.*"), recursive=True):
        if ".git" in p or "/tests/" in p:
            continue
        by_name[norm(os.path.basename(p))].append(rel(p))
        by_hash[hashlib.md5(io.open(p, "rb").read()).hexdigest()].append(rel(p))
    for k, v in by_name.items():
        if len(v) > 1:
            fail("T02", "nombre normalizado colisiona: " + " · ".join(v))
    for k, v in by_hash.items():
        if len(v) > 1:
            fail("T02", "contenido idéntico bajo nombres distintos: " + " · ".join(v))


# ───────────────────────────────────────────────────────────────
# T03 · Referencias colgantes
# ───────────────────────────────────────────────────────────────

# Nombres declarados como borrados/superados en `forense/curaduria-archivos.md`
# §1 (SE VA), §2.2 (ADR transitorios) y §4, y en `canon/gobernanza-v*.md` §2
# (Registro de artefactos) — leídos de esos dos documentos, no de memoria.
# Un nombre aquí es un archivo cuya ausencia ya fue decidida y registrada,
# no una referencia colgante sin explicar. Añadir un nombre nuevo a esta
# lista es el costo deliberado de declarar un borrado — es el mismo que
# `curaduria-archivos.md` ya paga a mano.
HISTORICOS = {
    # forense/curaduria-archivos.md §1 "SE VA"
    "estado-proyecto-psicologia-mexicano.md",
    "glosario-corregido-v2.md",
    "glosario-v3.md",
    "glosario-v4.md",
    # forense/curaduria-archivos.md §2.2 "ADR sin incorporar" (transitorios)
    "ADR-26-27-28.md",
    "ADR-29.md",
    # forense/curaduria-archivos.md §4 "SE AÑADE" / orden de ejecución
    "hito2-modelo-fantasma.md",   # nunca se subió
    "auditoria-glosario-v4.md",   # declarado "no subir": andamiaje, no artefacto
    # canon/gobernanza-v*.md §2, Registro de artefactos
    "ficha-canonica-modelo.md",
    "CHECKPOINT-v2.md",
    "mapa-y-roadmap.md",
    "inventario-corpus.md",
    "ADR-30.md",
    "modelo-decisiones-mexicano.md",
    # canon/gobernanza-v*.md §2, Registro de artefactos — declarados 29/jul/2026
    # (sesión de correcciones): nombres pre-ADR-36 que forense/curaduria-archivos.md
    # cita como vigentes el 27/jul y ningún documento declaraba renombrados/borrados.
    "gobernanza-programa.md",       # renombrado bajo ADR-36 a la serie gobernanza-v1.X.md
    "glosario-v5.md",               # renombrado bajo ADR-36 a la serie glosario-v5.X.md
    "CHECKPOINT-programa-psicologia-mexicano.md",  # probable antecesor de CHECKPOINT-v2.md (certeza media)
}

def _normalize_version_dots(name):
    """ADR-36: la plataforma convierte el punto en guion bajo al subir
    (`...-v3.0.md` -> `...-v3_0.md`). Una cita con la convención canónica
    (punto) contra un archivo que existe con guion bajo es cosmética, no
    una referencia colgante: normaliza el segmento de versión antes de
    decidir que el archivo no existe."""
    stem, dot, ext = name.rpartition(".")
    if not dot:
        return name
    stem = re.sub(r"(\d)\.(\d)", r"\1_\2", stem)
    return f"{stem}.{ext}"

def t03_dangling_refs():
    """Un documento que cita un archivo inexistente no obliga a nada."""
    existing = {os.path.basename(p) for p in
                glob.glob(os.path.join(ROOT, "**", "*.*"), recursive=True)}
    for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if ".git" in p:
            continue
        for i, l in enumerate(read(p).split("\n"), 1):
            for m in re.findall(r"`([A-Za-z0-9_\-áéíóúñÁÉÍÓÚÑ.]+\.(?:md|yaml))`", l):
                if m in existing or _normalize_version_dots(m) in existing or m in HISTORICOS:
                    continue
                if re.search(r"borrad|BORRAD|REEMPLAZA|elimin|~~|superced|supersede|v1, borrado|fusionad|renombr", l, re.I):
                    continue
                warn("T03", f"{rel(p)}:{i} cita `{m}`, que no existe")


# ───────────────────────────────────────────────────────────────
# T04 · ADR-33 — prohibida la diagonal en el ENTONCES
# ───────────────────────────────────────────────────────────────
def t04_adr33_diagonal():
    for l in motor_rules():
        m = re.search(r"\*\*ENTONCES\*\*(.*?)—\s*PORQUE", l) or \
            re.search(r"\*\*ENTONCES\*\*(.*?)—", l)
        if not m:
            continue
        cons = re.sub(r"\*|`", "", m.group(1))
        if re.search(r"\s/\s", cons):
            fail("T04", "consecuente con diagonal: " + cons.strip()[:110])


# ───────────────────────────────────────────────────────────────
# T05 · ADR-32.c — todo constructo del PORQUE existe en el glosario
# ───────────────────────────────────────────────────────────────
CONSTRUCTOS = [
    "G1", "G2", "G3", "G4", "G5", "G6",
    "familismo_apoyo", "familismo_obligacion", "simpatía", "machismo",
    "marianis", "face", "trampa social", "bandwidth", "transferencia directa",
    "turnout buying", "vote-choice", "confianza personalizada",
    "interruptor formal", "default es aceptación",
]
def t05_adr32c_constructs():
    g = newest("canon/glosario-v*.md")
    if not g:
        return
    gl = read(g).lower()
    for c in CONSTRUCTOS:
        if c.lower() not in gl:
            fail("T05", f"constructo `{c}` usado por el motor y ausente del glosario")


# ───────────────────────────────────────────────────────────────
# T06 · Consistencia numérica entre reports  (el que faltaba)
# ───────────────────────────────────────────────────────────────
def t06_numeric_consistency():
    """Cuatro valores de Gini y cuatro de confianza interpersonal (T-02, T-03)."""
    checks = [
        ("Gini", r"[Gg]ini[^.\n]{0,80}?(0\.\d{2,3}|\b4\d\.\d\b)"),
        ("confianza interpersonal", r"confian\w+ interpersonal[^.\n]{0,90}?(\d{1,2}(?:\.\d)?)\s?%"),
    ]
    for label, pat in checks:
        found = defaultdict(list)
        for p in reports() + glob.glob(os.path.join(ROOT, "corpus", "forense", "*.md")):
            for i, l in enumerate(read(p).split("\n"), 1):
                for m in re.finditer(pat, l):
                    found[m.group(1)].append(f"{os.path.basename(p)[:28]}:{i}")
        if len(found) > 1:
            det = " · ".join(f"{k} ({len(v)}x)" for k, v in sorted(found.items()))
            fail("T06", f"{len(found)} valores distintos de **{label}** en el corpus: {det}")


# ───────────────────────────────────────────────────────────────
# T07 · Vocabulario de tiers  (T-05: cuatro vocabularios incompatibles)
# ───────────────────────────────────────────────────────────────
CANONICO = {"FUERTE", "MEDIA", "MEDIA-FUERTE", "HIPÓTESIS"}
def t07_tier_vocabulary():
    ajenos = Counter()
    pat = r"\[(SÓLIDO|MEDIO|HIPÓTESIS RAZONABLE)\]|Calificación:\s*([A-ZÁÉÍÓÚ\- ]{4,25})|\*\*(Moderada|Moderada-Fuerte|Narrativa exagerada|Débil)\*\*"
    for p in reports():
        for i, l in enumerate(read(p).split("\n"), 1):
            for m in re.finditer(pat, l):
                tok = next(g for g in m.groups() if g)
                if tok.strip().upper() not in CANONICO:
                    ajenos[tok.strip()] += 1
    if ajenos:
        det = " · ".join(f"`{k}` ×{v}" for k, v in ajenos.most_common(8))
        fail("T07", f"{len(ajenos)} vocabularios de tier ajenos al Bloque A: {det}")


# ───────────────────────────────────────────────────────────────
# T08 · Todo report tiene mapa de evidencia  (A-01, R-01)
# ───────────────────────────────────────────────────────────────
def t08_evidence_map():
    sin = []
    for p in reports():
        s = read(p)
        if not re.search(r"^#+.*mapa de evidencia", s, re.I | re.M):
            sin.append(os.path.basename(p)[:46])
    if sin:
        fail("T08", f"{len(sin)} reports sin mapa de evidencia — todo constructo suyo es "
                    f"DERIVADO, no LEÍDO: " + " · ".join(sorted(sin)[:8])
                    + (" …" if len(sin) > 8 else ""))


# ───────────────────────────────────────────────────────────────
# T09 · Marcos importados (c) usados como causa  (A-04/05/06, C-02..C-05)
# ───────────────────────────────────────────────────────────────
CAUSAL = r"\b(explica|produce|genera|causa|hace que|se manifiesta en|implica|predice)\b"
def t09_imported_as_cause():
    for p in reports():
        for i, l in enumerate(read(p).split("\n"), 1):
            if "Hofstede" not in l and not re.search(r"\b(PDI|UAI|IDV)\b|Indulgencia \d|Individualismo de", l):
                continue
            if "(c)" in l or re.search(r"correlat|co-var|no causa|CORREGIDO|corregido", l, re.I):
                continue
            if re.search(CAUSAL, l, re.I):
                fail("T09", f"{os.path.basename(p)[:30]}:{i} marco importado como CAUSA sin (c): "
                            + re.sub(r"\s+", " ", l.strip())[:95])


# ───────────────────────────────────────────────────────────────
# T10 · Muestra de diáspora (b) sin marcar  (A-07..A-09, R-03..R-05, T-04)
# ───────────────────────────────────────────────────────────────
DIASPORA = ["Arciniega", "HCHS/SOL", "Nuñez", "Acevedo", "Castillo et al., 2010",
            "Lugo Steidel", "Sabogal", "Zeiders", "Knight", "mexicano-american",
            "mexicoamerican", "latinos en Estados Unidos", "US-Latin"]
def t10_diaspora_unmarked():
    for p in reports():
        for i, l in enumerate(read(p).split("\n"), 1):
            if not any(d.lower() in l.lower() for d in DIASPORA):
                continue
            if "(b)" in l or re.search(r"diáspora|no es evidencia sobre México", l, re.I):
                continue
            warn("T10", f"{os.path.basename(p)[:30]}:{i} muestra de diáspora sin (b): "
                        + re.sub(r"\s+", " ", l.strip())[:90])


# ───────────────────────────────────────────────────────────────
# T11 · Afirmaciones de estado sin verificar  (defecto #1, 5 de 5 falsas)
# ───────────────────────────────────────────────────────────────
ABSOLUTOS = r"\b(únicas?|únicos?|todas las|todos los|ninguna otra|completo|exhaustiv\w+)\b"
def t11_state_claims():
    for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if ".git" in p:
            continue
        for i, l in enumerate(read(p).split("\n"), 1):
            if re.search(r"[Vv]erificado contra el texto|se registró como aplicad|parchado en la fuente", l):
                if re.search(ABSOLUTOS, l, re.I):
                    fail("T11", f"{rel(p)}:{i} afirmación de estado con cuantificador absoluto "
                                f"(5 de 5 comprobadas resultaron falsas): "
                                + re.sub(r"\s+", " ", l.strip())[:95])


# ───────────────────────────────────────────────────────────────
# T12 · Conteos del motor coherentes entre canónicos
# ───────────────────────────────────────────────────────────────
def t12_counts():
    rules = motor_rules()
    n = len(rules)
    if n == 0:
        fail("T12", "no se pudo leer §3.B del modelo")
        return
    tiers = Counter(rule_tier(l) for l in rules)
    fuerte = tiers.get("`[FUERTE]`", 0)
    for name, pat in [("modelo", "canon/modelo-decision-v*.md"),
                      ("gobernanza", "canon/gobernanza-v*.md"),
                      ("estado", "canon/estado-programa-v*.md")]:
        f = newest(pat)
        if not f:
            continue
        s = read(f)
        if re.search(r"\b\d+ reglas\b", s):
            declarados = {int(x) for x in re.findall(r"\b(\d+) reglas\b", s)}
            if n not in declarados and not (declarados & {n - 1, n + 1}):
                warn("T12", f"{name} declara {sorted(declarados)} reglas; el motor tiene {n}")
    print(f"       motor: {n} reglas · {fuerte} [FUERTE] · " +
          " · ".join(f"{v}{k}" for k, v in tiers.most_common() if k))


# ───────────────────────────────────────────────────────────────
# T13 · Cabecera de versión obligatoria  (ADR-36)
# ───────────────────────────────────────────────────────────────
def t13_version_header():
    for p in glob.glob(os.path.join(ROOT, "canon", "*.md")) + \
             glob.glob(os.path.join(ROOT, "milpa", "*.md")):
        s = read(p)[:2500]
        if "**ARCHIVO**" not in s or "**NOMBRE ESTABLE**" not in s:
            warn("T13", f"{rel(p)} sin bloque de cabecera ARCHIVO/NOMBRE ESTABLE (ADR-36)")


# ───────────────────────────────────────────────────────────────
# T14 · T-INVENTARIO — cifras de inventario derivadas, no tecleadas
#   (sesión de tests, 29/jul/2026 · censo-integridad-v1_0.md C1-01, C1-08)
# ───────────────────────────────────────────────────────────────
def _inventory_section():
    """Texto de `## 1 · Inventario verificado` de `estado`, con la línea de
    archivo (1-indexado) donde empieza -- para anclar hallazgos a línea real
    en vez de re-buscar la posición dos veces."""
    p = newest("canon/estado-programa-v*.md")
    if not p:
        return None, "", 0
    s = read(p)
    m = re.search(r"^## 1 ·[^\n]*\n", s, re.M)
    if not m:
        return p, "", 0
    start = m.end()
    nxt = re.search(r"^## \d", s[start:], re.M)
    end = start + nxt.start() if nxt else len(s)
    start_line = s[:start].count("\n") + 1
    return p, s[start:end], start_line

def t14_inventario():
    """La suma de la tabla de `estado §1` debe igualar su propio encabezado
    (C1-01: decía 56, la tabla suma 59), y las dos filas que son un glob
    real -- reports, validaciones forenses -- deben igualar el disco. Las
    otras seis filas de la tabla son listas curadas (nombres específicos,
    no un glob), no se re-derivan aquí: hacerlo exigiría mantener a mano un
    segundo inventario tan frágil como el que este test reemplaza. También
    cubre C1-08: el mismo hecho (conteo de reports) citado en `integrador`."""
    p, sec, start_line = _inventory_section()
    if p is None or not sec:
        fail("T14", "no se pudo leer `## 1 · Inventario verificado` de estado")
        return
    m = re.search(r"\*\*(\d+)\s*archivos\*\*", sec)
    if not m:
        fail("T14", f"{rel(p)} §1: no se encontró el encabezado '**N archivos**'")
        return
    declarado = int(m.group(1))
    header_line = start_line + sec[:m.start()].count("\n")
    filas = []
    for i, l in enumerate(sec.split("\n")):
        fm = re.match(r"\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|\s*\*{0,2}(\d+)\*{0,2}\s*\|", l)
        if fm and fm.group(1).strip() != "Bloque":
            filas.append((fm.group(1).strip(), int(fm.group(2)), start_line + i))
    if not filas:
        fail("T14", f"{rel(p)} §1: no se encontraron filas de tabla con cuenta numérica")
        return
    suma = sum(c for _, c, _ in filas)
    if suma != declarado:
        detalle = "+".join(str(c) for _, c, _ in filas)
        fail("T14", f"{rel(p)}:{header_line} encabezado dice **{declarado} archivos**, "
                    f"la tabla suma {suma} ({detalle})")
    real_reports = len(reports())
    real_forense = len(glob.glob(os.path.join(ROOT, "corpus", "forense", "*.md")))
    for nombre, cuenta, ln in filas:
        n = nombre.lower()
        if "report" in n and cuenta != real_reports:
            fail("T14", f"{rel(p)}:{ln} fila '{nombre}' declara {cuenta}, "
                        f"`ls corpus/reports/*.md` da {real_reports}")
        if "forense" in n and "proceso" not in n and cuenta != real_forense:
            fail("T14", f"{rel(p)}:{ln} fila '{nombre}' declara {cuenta}, "
                        f"`ls corpus/forense/*.md` da {real_forense}")
    integ = newest("canon/integrador-*.md")
    if integ:
        # Sitios curados, no un escaneo genérico de "los N reports": el
        # documento también dice "los 5 reports de la Ronda 3" (línea 52),
        # un subconjunto real que NO debe compararse contra el total del
        # corpus -- un regex genérico ahí produce el mismo defecto que T07
        # (falso positivo por vocabulario libre, no acotado).
        s = read(integ)
        for pat in (r"contradicen los (\d+) reports", r"comparten los (\d+) reports"):
            for im in re.finditer(pat, s):
                n = int(im.group(1))
                if n != real_reports:
                    ln = s[:im.start()].count("\n") + 1
                    fail("T14", f"{rel(integ)}:{ln} dice 'los {n} reports', "
                                f"disco tiene {real_reports}")


# ───────────────────────────────────────────────────────────────
# T15 · T-ADR-COUNT — el número de ADR citado en canon/ debe igualar los
#   ADR únicos de `gobernanza`, sin huecos en la secuencia.
#   (sesión de tests, 29/jul/2026 · censo-integridad-v1_0.md C1-02: 32 vs 37)
# ───────────────────────────────────────────────────────────────
def t15_adr_count():
    g = newest("canon/gobernanza-v*.md")
    if not g:
        fail("T15", "no se pudo leer `canon/gobernanza-v*.md`")
        return
    nums = [int(n) for n in re.findall(r"^\*\*ADR-(\d+)", read(g), re.M)]
    if not nums:
        fail("T15", f"{rel(g)}: no se encontró ningún `**ADR-N`")
        return
    real = len(set(nums))
    dup = sorted(n for n, c in Counter(nums).items() if c > 1)
    if dup:
        fail("T15", f"{rel(g)}: ADR repetido(s), mismo número dos veces: {dup}")
    huecos = sorted(set(range(1, max(nums) + 1)) - set(nums))
    if huecos:
        fail("T15", f"{rel(g)}: huecos en la secuencia de ADR: {huecos}")
    for p in glob.glob(os.path.join(ROOT, "canon", "*.md")):
        for i, l in enumerate(read(p).split("\n"), 1):
            for m in re.finditer(r"(\d+)\s*ADR\b", l):
                n = int(m.group(1))
                if n != real:
                    fail("T15", f"{rel(p)}:{i} cita {n} ADR; gobernanza tiene {real} únicos")


# ───────────────────────────────────────────────────────────────
# T16 · T-SUITE-SELF-CHECK — ninguna afirmación VIGENTE sobre FAIL/WARN en
#   un canónico puede contradecir la corrida real.
#   (sesión de tests, 29/jul/2026 · censo-integridad-v1_0.md C1-06/C1-07,
#   el hallazgo de mayor severidad de todo el censo: 107 vigente cuando la
#   corrida real daba 111, y el propio mensaje del commit ya sabía 111.)
#
#   Juicio explícito de esta sesión: una cifra fechada dentro de un
#   changelog histórico (`> **v1.8 — 29/jul.** ...`) NO es un defecto -- era
#   correcta cuando se escribió, y perseguirla degradaría un registro
#   correcto a falso positivo (exactamente lo que este archivo, en su
#   propio §0, ya distingue a mano). El único marcador mecánico confiable
#   que encontramos para "esto es historia, no estado vigente" es esa
#   combinación cita-de-bloque + versión + fecha, porque es la única forma
#   en que ESTE documento narra un cambio pasado (ver v1.1/v1.6/v1.7/v1.8
#   en `estado §0`). Si algún día un canónico declara un FAIL/WARN histórico
#   con una forma distinta, este test no lo reconocerá como historia y lo
#   marcará FAIL por error -- limitación declarada, no descubierta a mano.
# ───────────────────────────────────────────────────────────────
_CAMBIO_FECHADO = re.compile(r"^>\s*\*\*v\d+[._]\d+\s*[—-]\s*\d{1,2}/")

def _suite_real():
    """Corrida independiente en subproceso, sin --strict/--baseline/--freeze
    y sin volver a correr T16 (variable de entorno) -- correr la suite
    completa para preguntarle 'cuál es tu resultado real' mientras todavía
    está corriendo es un problema de punto fijo, no una pregunta con
    respuesta. El subproceso excluye T16 de sí mismo: la cifra contra la
    que este test compara es 'todo lo demás', no 'todo incluido yo mismo'."""
    import subprocess
    env = dict(os.environ, CHECK_SELFCHECK_CHILD="1")
    try:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tests", "check.py")],
                            cwd=ROOT, capture_output=True, text=True, env=env, timeout=60)
    except Exception as e:
        return None, None, str(e)
    m = re.search(r"(\d+)\s*FAIL\s*·\s*(\d+)\s*WARN", r.stdout)
    if not m:
        return None, None, r.stdout[-300:]
    return int(m.group(1)), int(m.group(2)), None

def t16_suite_self_check():
    """Ninguna afirmación VIGENTE de FAIL/WARN en canon/ puede contradecir
    la corrida real (subproceso independiente, ver `_suite_real`).

    LÍMITE DECLARADO -- léelo antes de tocar este test: el único marcador
    mecánico que reconoce "esto es historia, no estado vigente" es
    `_CAMBIO_FECHADO`, que exige el formato literal `> **vX.Y — DD/mon.**`
    al INICIO de la línea (el patrón que `estado §0` ya usa para v1.1,
    v1.6, v1.7, v1.8). Si un canónico narra un cambio pasado con cualquier
    otra forma -- una tabla, una nota sin blockquote, una fecha en otro
    lugar de la oración -- este test NO lo reconocerá como histórico y
    marcará FAIL un registro que en realidad es correcto. Verificado en la
    sesión de tests (29/jul/2026): quitarle el `>` a una entrada histórica
    real basta para que empiece a fallar -- la exención es real, pero es
    tan angosta como el formato que sabe reconocer. Antes de ampliar el
    universo de documentos o de patrones que este test vigila, hay que
    ampliar `_CAMBIO_FECHADO` en la misma medida, o se repite exactamente
    el defecto de T07 (cobertura más angosta que el fenómeno que declara
    medir)."""
    real_fail, real_warn, err = _suite_real()
    if real_fail is None:
        fail("T16", f"no se pudo derivar el resultado real de la suite (subproceso): {err}")
        return
    for p in glob.glob(os.path.join(ROOT, "canon", "*.md")):
        for i, l in enumerate(read(p).split("\n"), 1):
            historico = bool(_CAMBIO_FECHADO.match(l))
            m1 = re.search(r"\*\*(\d+)\s*FAIL\s*·\s*(\d+)\s*WARN\*\*", l)
            if m1 and not historico:
                fd, wd = int(m1.group(1)), int(m1.group(2))
                if (fd, wd) != (real_fail, real_warn):
                    fail("T16", f"{rel(p)}:{i} declara {fd} FAIL · {wd} WARN vigente; "
                                f"la corrida real da {real_fail} FAIL · {real_warn} WARN")
            m2 = re.search(r"total de WARN de la suite es\s*\*{0,2}(\d+)", l)
            if m2 and not historico:
                wd = int(m2.group(1))
                if wd != real_warn:
                    fail("T16", f"{rel(p)}:{i} declara {wd} WARN vigente; "
                                f"la corrida real da {real_warn} WARN")


# ───────────────────────────────────────────────────────────────
# T17 · T-FICHAS-COUNT — el conteo de fichas de `hitoD-preregistro`
#   declarado en la declaración canónica de `estado §4·S2` debe igualar
#   los encabezados `## R` reales del propio pre-registro.
#   (sesión de tests, 29/jul/2026 · consolidación tras `b28b144`, que
#   dejó 3 menciones sueltas del mismo hecho en `estado` -- 111/171/214
#   -- por corregir una a la vez cada vez que cambia el conteo real.)
# ───────────────────────────────────────────────────────────────
def t17_fichas_count():
    """Una sola fuente para 'cuántas fichas tiene el pre-registro', y un
    test que la compara contra el disco -- para que la próxima ficha que
    se escriba (o se retire) no deje la declaración de estado stale como
    pasó con R3.2 (el propio motivo de esta sesión: T14/T15/T16 taparon
    3 de los 7 puntos de escritura manual; este era uno de los que no
    tenían test propio).

    Ampliado (29/jul/2026, sesión de canon). Hallazgo previo: el patrón
    original solo escaneaba `canon/estado-programa`, nunca el propio
    `hitoD-preregistro` -- así que la autodeclaración falsa de su propia
    cabecera ("VERIFICAS ASÍ: contiene **27 fichas**", línea 8, ya
    autoseñalada como falsa por su Nota 2) nunca entró al radar de este
    test, con verbo "tiene" o sin él. La causa raíz no era el verbo -- era
    el alcance. Se corrige ampliando a DOS fuentes de declaración vigente:

    (1) `estado`, citando al pre-registro por su nombre estable
        (`hitoD-preregistro\\``) seguido, a distancia corta y con
        CUALQUIER verbo o frase intermedia, de `**N fichas**` -- cubre
        "tiene", "contiene", "incluye", "declara", etc. Cubre la familia
        "hitoD-preregistro\\` <lo que sea> **N fichas**"; NO cubre una
        declaración que nombre el archivo por su nombre de archivo en vez
        del nombre estable, ni una que ponga más de ~30 caracteres entre
        el nombre y la cifra.

    (2) El propio `hitoD-preregistro`, que no se nombra a sí mismo --
        cualquier `**N fichas**` en su CUERPO VIGENTE, definido como todo
        el texto antes de `## Notas fechadas` (el propio archivo declara
        esa sección "append-only... se agregan al final" -- todo lo que
        vive ahí es historia narrada o citada, nunca declaración fresca).
        Es una exención ESTRUCTURAL, no un regex de fecha por nota: las
        Notas 1-7 usan el formato "### Nota N · fecha", que `_CAMBIO_FECHADO`
        no reconoce (exige `> **vX.Y — DD/mon.**`, el formato de `estado §0`)
        -- ampliar el universo sin ampliar la exención habría repetido el
        defecto de T07 que este mismo test ya advertía evitar. Cubre
        "contiene **N fichas**", "tiene **N fichas**", cualquier frase que
        preceda a la cifra entre corchetes dobles; NO cubre una declaración
        que hable de cobertura sin la palabra "fichas" pegada al número
        (p. ej. `hitoD-preregistro:13`, "v2.0 completa el perímetro: **27
        de 27**", queda fuera -- no dice "fichas").

    Hereda de T16 la exención de historia fechada para la fuente (1)
    (`_CAMBIO_FECHADO`); la fuente (2) usa su propia exención estructural,
    descrita arriba, en vez de heredarla."""
    h = newest("forense/hitoD-preregistro-v*.md")
    if not h:
        fail("T17", "no se pudo leer `forense/hitoD-preregistro-v*.md`")
        return
    texto_h = read(h)
    real = len(re.findall(r"^## R\d", texto_h, re.M))

    vigentes = []

    p = newest("canon/estado-programa-v*.md")
    if not p:
        fail("T17", "no se pudo leer `canon/estado-programa-v*.md`")
        return
    s = read(p)
    pat_ext = re.compile(r"hitoD-preregistro`[^\n]{0,30}\*\*(\d+)\s*fichas\*\*")
    for i, l in enumerate(s.split("\n"), 1):
        m = pat_ext.search(l)
        if not m or _CAMBIO_FECHADO.match(l):
            continue
        vigentes.append((rel(p), i, int(m.group(1))))

    marcador = "## Notas fechadas"
    corte = texto_h.find(marcador)
    cuerpo_vigente = texto_h if corte == -1 else texto_h[:corte]
    pat_int = re.compile(r"\*\*(\d+)\s*fichas\*\*")
    for i, l in enumerate(cuerpo_vigente.split("\n"), 1):
        m = pat_int.search(l)
        if not m:
            continue
        vigentes.append((rel(h), i, int(m.group(1))))

    if not vigentes:
        fail("T17", "no se encontró ninguna declaración vigente de cobertura del "
                     "pre-registro (ni en `canon/estado-programa` citando el nombre "
                     "estable, ni en el cuerpo vigente -- antes de `## Notas fechadas` "
                     "-- del propio pre-registro)")
        return
    distintos = sorted(set(n for _, _, n in vigentes))
    if len(distintos) > 1 or distintos[0] != real:
        detalle = " · ".join(f"{a}:{i}={n}" for a, i, n in vigentes)
        fail("T17", f"declaraciones de cobertura del pre-registro no cuadran con "
                     f"{rel(h)} ({real} encabezados `## R`): {detalle}")


# ───────────────────────────────────────────────────────────────
# T18 · T-PASO2-EJECUCION — aprobado y registrado 29/jul/2026, tras dos
#   rechazos y dos rediseños el mismo día:
#   1) el primer T18 derivaba su "real" leyendo `estado` y lo comparaba
#      contra el contador declarado en el MISMO archivo -- no cruzaba
#      frontera de archivo, el mismo alcance autorreferencial que T05.
#   2) el segundo T18 movió la forma canónica a `hitoD-preregistro` pero
#      la buscaba en CUALQUIER prosa del archivo -- no distinguía emitir
#      de citar/hipotetizar. El primer borrador de la propia Nota 5 que
#      archivaba el veredicto de R1.1 disparó su propio patrón al citar
#      la narración vieja de `estado`.
#   ADR-40 fija el diseño final: los veredictos viven en un bloque
#   designado, append-only, al final de `hitoD-preregistro`
#   (`## Registro de veredictos archivados`) -- la ÚNICA sección que este
#   test lee. Fuera de ese bloque, la forma canónica es cita o hipótesis
#   y no se cuenta, sea cual sea su forma.
# ───────────────────────────────────────────────────────────────
_VEREDICTO_CANONICO = re.compile(r"`(R\d+\.\d+)`\s*→\s*veredicto\s*`([A-D])`")
# Letra en mayúscula exacta (sin heredar re.I de "veredicto"): con re.I
# sobre todo el patrón, [ABCD] también matchea la preposición "a" -- ya
# verificado como falso positivo real antes de esta versión.
_VEREDICTO_SOSPECHOSO = re.compile(r"`(R\d+\.\d+)`[^\n`]{0,20}(?i:veredicto)[^\n]{0,15}\b([A-D])\b")

def _bloque_veredictos(texto):
    """Extrae SOLO el contenido de '## Registro de veredictos archivados'
    hasta el final del archivo (ADR-40: bloque designado, append-only,
    debe ser la última sección). Fuera de ese bloque no se lee nada --
    es la garantía de que citar o hipotetizar en cualquier otra prosa del
    documento no puede producir un match."""
    m = re.search(r"^## Registro de veredictos archivados.*$", texto, re.M)
    if not m:
        return None
    return texto[m.end():]

def t18_paso2_ejecucion():
    """`hitoD-preregistro` es, desde ADR-40, el registro canónico de
    veredictos archivados -- pero SOLO dentro de su bloque designado
    ('## Registro de veredictos archivados', al final del archivo).
    Deriva el conteo real de ese bloque (forma canónica:
    '`RX.Y` → veredicto `Z`') y lo compara contra el contador declarado en
    `estado:192` ('Paso 2 — EN CURSO. N de 27 corrida.'). También escanea
    el MISMO bloque en busca de líneas con forma de veredicto que no
    cumplan la forma exacta -- un ID de regla entre backticks seguido, a
    poca distancia, de la palabra 'veredicto' y una letra A-D -- para que
    una variante no se archive invisible. Nada fuera del bloque se lee:
    una hipótesis o una cita en cualquier otra parte del documento, con
    la forma que sea, no cuenta."""
    h = newest("forense/hitoD-preregistro-v*.md")
    if not h:
        fail("T18", "no se pudo leer `forense/hitoD-preregistro-v*.md`")
        return
    completo = read(h)
    bloque = _bloque_veredictos(completo)
    if bloque is None:
        fail("T18", f"{rel(h)}: no se encontró el bloque "
                    f"'## Registro de veredictos archivados' (ADR-40)")
        return
    offset_lineas = completo[:completo.index(bloque)].count("\n")
    reales = set()
    for i, l in enumerate(bloque.split("\n"), 1):
        m = _VEREDICTO_CANONICO.search(l)
        if m:
            reales.add(m.group(1))
            continue
        ms = _VEREDICTO_SOSPECHOSO.search(l)
        if ms:
            fail("T18", f"{rel(h)}:{offset_lineas + i} tiene forma de veredicto para "
                        f"`{ms.group(1)}` que no cumple la forma canónica "
                        f"('`RX.Y` → veredicto `Z`', ADR-40), dentro del bloque de registro: "
                        + re.sub(r"\s+", " ", l.strip())[:110])
    real = len(reales)

    p = newest("canon/estado-programa-v*.md")
    if not p:
        fail("T18", "no se pudo leer `canon/estado-programa-v*.md`")
        return
    s2 = read(p)
    pat = re.compile(r"Paso 2\s*—\s*EN CURSO\.\s*(\d+)\s*de\s*27\s*corrida")
    vigentes = []
    for i, l in enumerate(s2.split("\n"), 1):
        m = pat.search(l)
        if not m or _CAMBIO_FECHADO.match(l):
            continue
        vigentes.append((i, int(m.group(1))))
    if not vigentes:
        fail("T18", f"{rel(p)}: no se encontró el contador vigente de ejecución de Paso 2 "
                    f"('Paso 2 — EN CURSO. N de 27 corrida' en §7, fuera de historia fechada)")
        return
    distintos = sorted(set(n for _, n in vigentes))
    if len(distintos) > 1:
        detalle = " · ".join(f"{rel(p)}:{i}={n}" for i, n in vigentes)
        fail("T18", f"{rel(p)}: {len(vigentes)} contadores de ejecución vigentes, "
                    f"no todos iguales: {detalle}")
        return
    declarado = distintos[0]
    if declarado != real:
        ln = vigentes[0][0]
        fail("T18", f"{rel(p)}:{ln} declara {declarado} de 27 corrida; "
                    f"{rel(h)} tiene {real} veredictos archivados en forma canónica "
                    f"(patrón `` `RX.Y` → veredicto `Z` ``)")


# ───────────────────────────────────────────────────────────────
# Modo línea base · congela el estado conocido, no lo mueve por defecto
# ───────────────────────────────────────────────────────────────
#   --freeze     escribe tests/baseline.json con el estado actual (acto
#                deliberado, con rastro en el diff — nunca automático)
#   --baseline   compara la corrida actual contra tests/baseline.json:
#                verde si no hay entradas NUEVAS, rojo si las hay
#
# La clave NO es (test, mensaje) completo: T03/T09/T10/T11 incrustan el
# número de línea en el mensaje, y cualquier edición cosmética por encima
# de la línea citada lo desplaza — probado: una sola línea insertada sin
# relación con el contenido cambia el mensaje de 3 de 3 hallazgos en el
# mismo archivo. Tampoco es (test, archivo) a secas: de 39 pares
# (test, archivo) que produce este corpus, 22 agrupan más de un mensaje
# distinto (hasta 15 en un solo archivo) — con esa clave, un hallazgo
# nuevo en un archivo ya conocido no se distinguiría de uno viejo.
# La clave es (test, mensaje con el número de línea quitado): sobre el
# corpus real hoy, 107 entradas producen 106 claves únicas — 1 colisión,
# entre dos citas idénticas al mismo archivo histórico en líneas
# distintas del mismo censo, que es inocua (perder una no oculta un
# defecto nuevo, solo un duplicado del mismo ya sabido).
def _baseline_key(msg):
    return re.sub(r":\d+ ", ": ", msg, count=1)

def _git_head():
    try:
        import subprocess
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return None

# ───────────────────────────────────────────────────────────────
# Nota de composición · "congelar no es aceptar" (29/jul/2026)
# ───────────────────────────────────────────────────────────────
# Congelar una cifra no dice qué es. Sin esto, dentro de dos meses 83
# WARN se lee como deuda técnica homogénea del corpus, cuando parte es
# deuda del propio instrumento de medición (T03 con cobertura angosta) y
# solo parte es deuda real ya identificada. Los buckets son patrones
# vistos y explicados a mano en forense/censo-integridad-v1_1.md — no una
# regla general recalculable; lo que no cae en ninguno queda "sin_clasificar",
# explícito, en vez de asumido como una cosa o la otra.
_FRAGMENTOS_EJEMPLO = {"-v3.2.md", "-v3_2.md", "...-v3.0.md", "...-v3_0.md"}
_HISTORIA_RECIENTE_NO_DECLARADA = {
    "estado-programa-v1_8.md", "gobernanza-v1_8.md", "modelo-decision-v3_2.md",
    "estado-programa-v1_7.md", "v1_9.md", "gobernanza-v1_9.md",
}
_GOBERNANZA_STALE_C5_02 = {"glosario-v5.5.md", "modelo-decision-v3.0.md", "estado-programa-v1.1.md"}
_NOMBRADOS_SIN_BORRADO_DECLARADO = {
    # Dormante desde 29/jul/2026 (sesión de correcciones): los 3 nombres se
    # declararon en gobernanza-v1_9.md §2 y se movieron a HISTORICOS (arriba),
    # así que t03_dangling_refs ya no los agrega a WARNS -- este bucket nunca
    # vuelve a poblarse a menos que se retire alguno de HISTORICOS. Se
    # conserva el set (no el código muerto) porque tests/baseline.json
    # congelado antes de esa sesión todavía puede citar este bucket.
    "gobernanza-programa.md", "CHECKPOINT-programa-psicologia-mexicano.md", "glosario-v5.md",
}

def _classify(test, msg):
    if test == "T03":
        m = re.search(r"cita `([^`]+)`", msg)
        name = m.group(1) if m else None
        if name in _FRAGMENTOS_EJEMPLO and "TRANSFER-maestra-9.md" in msg:
            return ("T03_TRANSFER-9_cita_ilustrativa_del_propio_falso_positivo"
                     "__mismo_patron_benigno_ya_reconocido")
        if name in _FRAGMENTOS_EJEMPLO:
            return "T03_fragmento_de_ejemplo_no_es_archivo_real__deuda_del_test"
        if name in _HISTORIA_RECIENTE_NO_DECLARADA:
            return "T03_historia_real_no_cubierta_por_HISTORICOS__deuda_de_mantener_la_lista"
        if name in _GOBERNANZA_STALE_C5_02:
            return "T03_defecto_real_gobernanza_S2_tabla_stale__deuda_real_del_corpus_C5-02"
        if name in _NOMBRADOS_SIN_BORRADO_DECLARADO:
            return "T03_nombrado_sin_borrado_explicito_en_ninguna_fuente__gap_de_documentacion"
        return "T03_sin_clasificar"
    if test == "T13":
        return "T13_integrador_sin_cabecera__deuda_real_del_corpus_C5-01"
    if test == "T10":
        return "T10_no_triado_instancia_por_instancia_en_esta_sesion__pendiente_C7"
    return f"{test}_sin_clasificar"

def _freeze_note():
    # Clasifica sobre el conjunto ya deduplicado por _baseline_key (mismo
    # criterio que se congela), no sobre WARNS crudo — si no, el total del
    # desglose no cuadra contra "warns" y el propio archivo se contradice.
    warn_keys = sorted({(t, _baseline_key(m)) for t, m in WARNS})
    buckets = Counter(_classify(t, m) for t, m in warn_keys)
    for t, m in FAILS:
        if t == "T17":
            buckets["T17_autodeclaracion_falsa_conocida__protegida_por_append-only__pendiente_de_ADR"] += 1
        else:
            buckets[f"{t}_FAIL_no_re-analizado_en_P1__ver_censo-integridad_para_detalle"] += 1
    return {
        "principio": ("Congelar no es aceptar. La cifra congelada mezcla deuda real del "
                      "corpus con ruido de medición conocido del propio T03 (cobertura "
                      "angosta); ver forense/censo-integridad-v1_1.md §1 para la derivación "
                      "completa de cada bucket. Bajada de 89 a 83 WARN el 29/jul/2026 "
                      "(sesión de correcciones, ver mensaje de commit) sin tocar ningún FAIL."),
        "fecha_de_clasificacion": "2026-07-29",
        "conteo_por_bucket": dict(sorted(buckets.items())),
    }

def _freeze_baseline():
    import json
    data = {
        "head": _git_head(),
        "fails": sorted({(t, _baseline_key(m)) for t, m in FAILS}),
        "warns": sorted({(t, _baseline_key(m)) for t, m in WARNS}),
        "nota": _freeze_note(),
    }
    with open(BASELINE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"\n[--freeze] escrito {rel(BASELINE_PATH)} — HEAD {data['head']} · "
          f"{len(data['fails'])} fail · {len(data['warns'])} warn congelados")

def _baseline_compare():
    import json
    if not os.path.exists(BASELINE_PATH):
        print(f"\n[--baseline] no existe {rel(BASELINE_PATH)} — corre con --freeze primero.")
        return 1
    with open(BASELINE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    known = {tuple(e) for e in data["fails"]} | {tuple(e) for e in data["warns"]}
    current = {(t, _baseline_key(m)) for t, m in FAILS} | {(t, _baseline_key(m)) for t, m in WARNS}
    nuevos = current - known
    resueltos = known - current
    print("\n" + "─" * 72)
    if nuevos:
        print(f"  LÍNEA BASE: ROJO — {len(nuevos)} entradas nuevas frente a {rel(BASELINE_PATH)} "
              f"(HEAD congelado {data.get('head')})")
        for t, k in sorted(nuevos):
            print(f"  · {t}: {k[:110]}")
    else:
        print(f"  LÍNEA BASE: VERDE — nada nuevo frente a {rel(BASELINE_PATH)} "
              f"(HEAD congelado {data.get('head')})")
    if resueltos:
        print(f"  ({len(resueltos)} entradas de la línea base ya no aparecen — mejora, no bloquea, "
              f"no baja la cifra congelada sin --freeze explícito)")
    print("─" * 72)
    return 1 if nuevos else 0


def main():
    tests = [
        ("T01 fuente única de verdad",            t01_single_source),
        ("T02 duplicados nombre/contenido",       t02_duplicates),
        ("T03 referencias colgantes",             t03_dangling_refs),
        ("T04 ADR-33 diagonal en ENTONCES",       t04_adr33_diagonal),
        ("T05 ADR-32.c constructos en glosario",  t05_adr32c_constructs),
        ("T06 consistencia numérica",             t06_numeric_consistency),
        ("T07 vocabulario de tiers",              t07_tier_vocabulary),
        ("T08 mapa de evidencia por report",      t08_evidence_map),
        ("T09 marco (c) usado como causa",        t09_imported_as_cause),
        ("T10 diáspora (b) sin marcar",           t10_diaspora_unmarked),
        ("T11 afirmaciones de estado absolutas",  t11_state_claims),
        ("T12 conteos del motor",                 t12_counts),
        ("T13 cabecera de versión ADR-36",        t13_version_header),
        ("T14 T-INVENTARIO",                      t14_inventario),
        ("T15 T-ADR-COUNT",                       t15_adr_count),
        ("T17 T-FICHAS-COUNT",                    t17_fichas_count),
        ("T18 T-PASO2-EJECUCION",                 t18_paso2_ejecucion),
    ]
    if not os.environ.get("CHECK_SELFCHECK_CHILD"):
        tests.append(("T16 T-SUITE-SELF-CHECK", t16_suite_self_check))
    print("═" * 72)
    print("  VERIFICACIÓN DEL CORPUS" + ("   [--strict]" if STRICT else ""))
    print("═" * 72)
    for name, fn in tests:
        before_f, before_w = len(FAILS), len(WARNS)
        fn()
        df, dw = len(FAILS) - before_f, len(WARNS) - before_w
        mark = "FAIL" if df else ("warn" if dw else " ok ")
        extra = f"  ({df} fail" + (f", {dw} warn)" if dw else ")") if df else (f"  ({dw} warn)" if dw else "")
        print(f"  [{mark}]  {name}{extra}")

    if WARNS:
        print("\n" + "─" * 72 + f"\n  WARN ({len(WARNS)})\n" + "─" * 72)
        agg = Counter(t for t, _ in WARNS)
        for t, n in agg.most_common():
            print(f"  · {t}: {n}")
            for tt, m in [w for w in WARNS if w[0] == t][:3]:
                print(f"      {m}")
            if n > 3:
                print(f"      … y {n-3} más")

    if FAILS:
        print("\n" + "─" * 72 + f"\n  FAIL ({len(FAILS)})\n" + "─" * 72)
        agg = Counter(t for t, _ in FAILS)
        for t, n in agg.most_common():
            print(f"  · {t}: {n}")
            for tt, m in [f for f in FAILS if f[0] == t][:4]:
                print(f"      {m}")
            if n > 4:
                print(f"      … y {n-4} más")

    print("\n" + "═" * 72)
    print(f"  {len(FAILS)} FAIL · {len(WARNS)} WARN")
    print("═" * 72)

    if FREEZE_MODE:
        _freeze_baseline()
        return 0
    if BASELINE_MODE:
        return _baseline_compare()

    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
