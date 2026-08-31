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
import csv, io, os, re, sys, glob, hashlib, unicodedata, datetime
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRICT = "--strict" in sys.argv
BASELINE_MODE = "--baseline" in sys.argv
FREEZE_MODE = "--freeze" in sys.argv
REQUIRE_CABLEADO = "--require-cableado" in sys.argv
BASELINE_PATH = os.path.join(ROOT, "tests", "baseline.json")
FAILS, WARNS = [], []
SENAL = []

def read(p):
    return io.open(p, encoding="utf-8").read()

def rel(p):
    return os.path.relpath(p, ROOT)

def fail(test, msg):
    FAILS.append((test, msg))

def warn(test, msg):
    (FAILS if STRICT else WARNS).append((test, msg))

def senal(test, msg):
    """WARN de vigía: dispara por diseño en cada corrida, así que por
    construcción no puede ser un detector de regresiones. Se imprime
    igual —A.12 le encarga justamente gritar hasta que alguien atienda—
    y queda fuera de la comparación de línea base."""
    (FAILS if STRICT else WARNS).append((test, msg))
    SENAL.append((test, _baseline_key(msg)))

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
    # Grupos cuyos miembros caen TODOS bajo estos tres prefijos son
    # nomenclatura por-run/por-expediente que colisiona por diseño del
    # pipeline de curación semántica del barrido: cada unidad de trabajo
    # (SEMRUN-*, ESP-OPACA-*, la integración) reusa el mismo puñado de
    # nombres genéricos (particiones.tsv, hashes.json, resumen.json,
    # analisis-reproducible.py...). Mismo razonamiento que la excepción de
    # data/raw arriba: colisión por diseño de nomenclatura, no defecto del
    # corpus. Es a nivel de GRUPO, no de archivo individual (a diferencia de
    # data/raw, que se excluye del índice por completo): si un solo miembro
    # de un grupo cae fuera de estos tres prefijos, el grupo entero se sigue
    # reportando -- una colisión real que cruce el límite no se tapa.
    EXCEPTED_PREFIXES = (
        "data/curacion-registro/ejecucion-semantica/runs/",
        "data/curacion-registro/expedientes-produccion/",
        "data/curacion-registro/integracion-barrido/",
        # forense/rescate/curador-untracked-20260807/: rescate verbatim
        # (DIRECTIVA de cierre de RESCATE-CURADOR, FP-55) del untracked de
        # Modelado-Mexicano-curador -- worker-N-*.tsv/json repetidos entre
        # multi{1,2}-staging/ y su propio integrado/ es el mismo patrón
        # por-worker/por-integración que las tres excepciones de arriba, un
        # prototipo anterior (6-7/ago) del mismo pipeline. Archivo, no vivo.
        "forense/rescate/curador-untracked-20260807/",
        # forense/rescate/barrido-completo-untracked-20260807/: rescate verbatim
        # (FP-59, ACTO LIMPIA-CAJA) del untracked de
        # Modelado-Mexicano-barrido-completo -- son literalmente archivos bajo
        # `data/curacion-registro/ejecucion-semantica/runs/`, el PRIMER prefijo
        # exceptuado de arriba, movidos bajo forense/rescate/ al archivarlos:
        # SEMTSK-*.json repetidos entre contratos/ y reportes-worker/, TCUR-*.json
        # entre inputs/ e inputs-curador/. Misma nomenclatura por-run, mismo
        # pipeline, misma corrida (SEMRUN-1d73f40d/354ccb9d, 07/ago). Archivo, no
        # vivo. Mismo mecanismo de grupo que el rescate del curador (PR #274).
        "forense/rescate/barrido-completo-untracked-20260807/",
    )
    def all_excepted(paths):
        return all(p.startswith(EXCEPTED_PREFIXES) for p in paths)
    # Grupos por-contenido exceptuados uno a uno, no por prefijo: pares donde
    # el segundo archivo es deliberadamente una copia byte a byte del primero
    # -- un CONGELADO (compromiso criptográfico), no una duplicación
    # accidental. `ADR-179`, `ACTO CONGELA-SORTEA`, 25/ago/2026: el marco de
    # candidatas del piloto y su congelado deben coincidir byte a byte por
    # diseño (`cmp` verificado al crear el congelado; `CONGELADO-v1_0.sha256`
    # registra el pin) -- mismo patrón de censo mecánico que `ADR-177`/`ADR-178`.
    EXCEPTED_HASH_GROUPS = (
        frozenset({
            "forense/marco-candidatas-piloto-v1_0.tsv",
            "forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv",
        }),
        # ACTO MAESTRA32-E14 · MARCO-M-SORTEA (ACTO B′), 31/ago/2026: regla
        # de tamaño de forense/notas/2026-08-31-marco-M-spec.md §e -- con
        # N_elegibles=2 < 15 el "sorteo" es la identidad (todas las filas
        # elegibles entran, sin PRNG), así que el sorteado debe coincidir
        # byte a byte con el congelado que lo origina. Mismo patrón que el
        # grupo de arriba (compromiso criptográfico, no duplicación
        # accidental).
        frozenset({
            "forense/prereg-duelo-v2/marco-M-congelado-v1_0.tsv",
            "forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv",
        }),
    )
    by_name, by_hash = defaultdict(list), defaultdict(list)
    for p in glob.glob(os.path.join(ROOT, "**", "*.*"), recursive=True):
        if ".git" in p or "/tests/" in p or "/data/raw" in p:
            # data/raw: INEGI empaqueta conjunto_de_datos.csv/diccionario_datos.csv
            # en casi todos sus zips de microdato — by_name colisiona por diseño
            # de nomenclatura del portal, no por defecto del corpus. by_hash ya
            # lo cubre mejor tests/manifiesto.py --verifica (dedup por sha256
            # declarado, sin rehashear el corpus completo en cada corrida).
            continue
        if not os.path.isfile(p):
            continue
        by_name[norm(os.path.basename(p))].append(rel(p))
        by_hash[hashlib.md5(io.open(p, "rb").read()).hexdigest()].append(rel(p))
    for k, v in by_name.items():
        if len(v) > 1 and not all_excepted(v):
            fail("T02", "nombre normalizado colisiona: " + " · ".join(sorted(v)))
    for k, v in by_hash.items():
        if len(v) > 1 and not all_excepted(v) and frozenset(v) not in EXCEPTED_HASH_GROUPS:
            fail("T02", "contenido idéntico bajo nombres distintos: " + " · ".join(sorted(v)))


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
    # canon/gobernanza-v*.md §2 — declarado 30/jul/2026 por ADR-48 (R0):
    # la cola del canon se congeló como `forense/hallazgos-congelados-2026-07-30.yaml`.
    # Las citas vivas del canon están reapuntadas; las que quedan viven en
    # artefactos que no se reescriben (pre-registros, bitácora append-only,
    # documentos recogidos verbatim) y esta línea es lo que cuesta declararlo.
    "cola.yaml",
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

# Marca explícita de cita ilustrativa (cola I-01, cerrada por ADR-48).
# Se escribe pegada a la cita que exime, no en cualquier parte de la línea:
#
#     La FASE 5 propone `LICENSE-CORPUS.md` {cita-ilustrativa}, que no se creará.
#
# Exime SOLO la cita inmediatamente anterior — una línea con tres citas y una
# marca deja las otras dos vigiladas. Es deliberado: el defecto que I-01
# registró es que documentar un falso positivo genera otro, y la respuesta a
# eso es una exención estrecha y visible en el texto, no una lista paralela de
# excepciones que nadie mantiene (el costo que ya paga HISTORICOS).
MARCA_ILUSTRATIVA = r"\s*\{cita-ilustrativa\}"

def t03_dangling_refs():
    """Un documento que cita un archivo inexistente no obliga a nada."""
    existing = {os.path.basename(p) for p in
                glob.glob(os.path.join(ROOT, "**", "*.*"), recursive=True)}
    for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if ".git" in p:
            continue
        for i, l in enumerate(read(p).split("\n"), 1):
            for mo in re.finditer(r"`([A-Za-z0-9_\-áéíóúñÁÉÍÓÚÑ.]+\.(?:md|yaml))`", l):
                m = mo.group(1)
                if m in existing or _normalize_version_dots(m) in existing or m in HISTORICOS:
                    continue
                if re.match(MARCA_ILUSTRATIVA, l[mo.end():]):
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
# Bloque A (canónico): fuerte · media · hipótesis razonable · narrativa
# popular -- `HIPÓTESIS` es la forma corta de "hipótesis razonable", ya en
# uso antes de este acto. CANONICO admite esos cuatro más sus
# equivalencias, mapeo sellado por mesa (`ADR-93(c)`/`FP-30`, ejecutado por
# `ADR-94`): SÓLIDO→fuerte · MEDIO/MODERADA→media · HIPÓTESIS RAZONABLE→
# hipótesis razonable · NARRATIVA EXAGERADA→narrativa popular ·
# MODERADA-FUERTE→media-fuerte. `MEDIA-FUERTE` no es del Bloque A pero se
# retiene como quinta categoría, declarado en `ADR-94`: el test la usa
# desde antes de este acto, el corpus la usa una vez, y retirarla rompería
# sin ganancia -- es el único punto de este conjunto que ADR-94 decide de
# nuevo; el resto ya estaba sellado por FP-30.
CANONICO = {
    "FUERTE", "SÓLIDO",
    "MEDIA", "MEDIO", "MODERADA",
    "HIPÓTESIS", "HIPÓTESIS RAZONABLE",
    "NARRATIVA POPULAR", "NARRATIVA EXAGERADA",
    "MEDIA-FUERTE", "MODERADA-FUERTE",
}
def t07_tier_vocabulary():
    ajenos = Counter()
    pat = r"\[(SÓLIDO|MEDIO|HIPÓTESIS RAZONABLE)\]|Calificación:\s*([A-ZÁÉÍÓÚ\- ]{4,25})|\*\*(Moderada|Moderada-Fuerte|Narrativa exagerada|Débil)\*\*"
    for p in reports():
        for i, l in enumerate(read(p).split("\n"), 1):
            for m in re.finditer(pat, l):
                tok = next(g for g in m.groups() if g)
                # ADR-94/FP-41: contar sobre la misma forma normalizada que
                # decide el chequeo -- antes se comparaba con `.upper()` pero
                # se contaba con `tok.strip()` sin mayusculizar, así que
                # "Moderada" y "MODERADA" salían como dos vocabularios.
                normalizado = tok.strip().upper()
                if normalizado not in CANONICO:
                    ajenos[normalizado] += 1
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
#
#   Marca de cita histórica (ADR-72, 13/ago/2026). Mismo mecanismo que
#   MARCA_ILUSTRATIVA de T03 (línea ~208), aplicado aquí porque T15 tenía
#   el mismo punto ciego que motivó esa marca: ADR-71 narra su propia saga
#   de renumeración ("Cascada — historia completa de la numeración") y
#   cita, correctamente, el conteo que tenía en ESE momento — `71 ADR`.
#   Sellar el siguiente ADR vuelve esa cita histórica, correcta, indistinguible
#   de una afirmación vigente para el regex de siempre. A diferencia de T16
#   (que exime bloques `> **vX.Y — DD/mon.**`, el único formato en que
#   `estado §0` narra un cambio pasado), T15 no tenía ningún mecanismo
#   equivalente porque, hasta ADR-71, ningún ADR había necesitado citar un
#   dígito de conteo dentro de su propia prosa ya sellada — ADR-44 a ADR-70
#   dicen "conteo de ADR vía receta T15" sin dígito, precisamente evitando
#   esta trampa. La marca exime SOLO la cita inmediatamente anterior, igual
#   que T03: una línea con dos citas y una marca deja la otra vigilada.
# ───────────────────────────────────────────────────────────────
#   La cita que motiva esta marca vive entre backticks (`` `71 ADR` ``,
#   markdown estándar de este repo para un valor citado) — el regex de
#   arriba (`(\d+)\s*ADR\b`) no incluye el backtick de cierre en el match,
#   así que la marca debe tolerar un backtick opcional antes de sí misma.
MARCA_HISTORICA = r"`?\s*\{cita-historica\}"

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
                if n == real:
                    continue
                if re.match(MARCA_HISTORICA, l[m.end():]):
                    continue
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
    que este test compara es 'todo lo demás', no 'todo incluido yo mismo'.

    Punto fijo verificado, no asumido (ACTO CI-CATEGORIA, 18/ago/2026,
    contra 997482b). Como T16 nunca corre dentro de este subproceso, el
    par (real_fail, real_warn) que devuelve NUNCA incluye la contribución
    de T16 -- es estructuralmente estable frente a cuántas citas de
    gobernanza estén desincronizadas (0, 1, 2 o 3), no una coincidencia de
    esta corrida en particular. Confirmado por prueba directa (editada y
    revertida, no commiteada): fijar una sola cita vigente
    (`gobernanza:1658`) al valor esperado bajó el FAIL de la corrida
    completa de 22 a 21 -- un T16 menos -- y este subproceso siguió dando
    exactamente 19 FAIL · 132 WARN, sin moverse un dígito. La trampa que
    esto previene: quien resincronice `gobernanza:1106`, `:1136` o
    `:1658` copiando el total impreso al pie de la corrida (22 FAIL) en
    vez del que este test acepta (19 FAIL, el 'núcleo' sin T16) deja esas
    líneas rojas para siempre -- ningún `declara` hace cerrar la
    comparación contra 22, porque este subproceso jamás calcula 22.

    Las tres citas que hoy no matchean el núcleo (`gobernanza:1106`,
    `:1136`, `:1658`) no se reescriben aquí: las tres narran un estado
    PASADO de un ADR ya sellado (ADR-76(f)/ADR-77/ADR-94 respectivamente),
    sin el formato de blockquote que `_CAMBIO_FECHADO` exige para
    reconocerlas como histórico -- límite ya declarado en el docstring de
    `t16_suite_self_check`. Sobreescribirlas con el núcleo vigente
    falsearía lo que esos ADR midieron al sellarse -- `gobernanza:1106`
    lo dice verbatim: "nunca debe seguir al real". Quedan protegidas por
    el mecanismo que ya existe: `_T16_REAL_SUFIJO` normaliza el sufijo
    volátil ('la corrida real da…') de la clave de línea base para las
    tres por igual -- el regex no está acotado a `:1106`/`:1136` -- así
    que ninguna necesita recongelarse cada vez que el WARN real se mueve
    por una causa ajena a gobernanza."""
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

    LÍMITE DECLARADO -- léelo antes de tocar este test: dos marcadores
    mecánicos reconocen "esto es historia, no estado vigente". El primero,
    `_CAMBIO_FECHADO`, exige el formato literal `> **vX.Y — DD/mon.**` al
    INICIO de la línea (el patrón que `estado §0` ya usa para v1.1, v1.6,
    v1.7, v1.8). El segundo, `MARCA_HISTORICA` (ACTO T16-HISTÓRICAS,
    18/ago/2026 -- mismo mecanismo `{cita-historica}` que T15 ya usa desde
    ADR-72), exime SOLO la cita inmediatamente anterior a la marca: una
    línea con dos citas y una marca deja la otra vigilada. Si un canónico
    narra un cambio pasado con cualquier otra forma -- una tabla, una nota
    sin blockquote ni marca, una fecha en otro lugar de la oración -- este
    test NO lo reconocerá como histórico y marcará FAIL un registro que en
    realidad es correcto. Verificado en la sesión de tests (29/jul/2026):
    quitarle el `>` a una entrada histórica real basta para que empiece a
    fallar -- la exención es real, pero es tan angosta como los dos
    formatos que sabe reconocer. Antes de ampliar el universo de
    documentos o de patrones que este test vigila, hay que ampliar ambos
    marcadores en la misma medida, o se repite exactamente el defecto de
    T07 (cobertura más angosta que el fenómeno que declara medir)."""
    real_fail, real_warn, err = _suite_real()
    if real_fail is None:
        fail("T16", f"no se pudo derivar el resultado real de la suite (subproceso): {err}")
        return
    for p in glob.glob(os.path.join(ROOT, "canon", "*.md")):
        for i, l in enumerate(read(p).split("\n"), 1):
            historico = bool(_CAMBIO_FECHADO.match(l))
            for m in re.finditer(r"\*\*(\d+)\s*FAIL\s*·\s*(\d+)\s*WARN\*\*", l):
                if historico or re.match(MARCA_HISTORICA, l[m.end():]):
                    continue
                fd, wd = int(m.group(1)), int(m.group(2))
                if (fd, wd) != (real_fail, real_warn):
                    fail("T16", f"{rel(p)}:{i} declara {fd} FAIL · {wd} WARN vigente; "
                                f"la corrida real da {real_fail} FAIL · {real_warn} WARN")
            for m in re.finditer(r"total de WARN de la suite es\s*\*{0,2}(\d+)", l):
                if historico or re.match(MARCA_HISTORICA, l[m.end():]):
                    continue
                wd = int(m.group(1))
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
# ADR-58 (4/ago/2026) extiende la escala con la fila E (corroboración
# prospectiva) -- excepción acotada aplicada aquí a `R1.2` (inciso d).
# El rango pasa de A-D a A-E; sin este cambio, la línea `R1.2` →
# veredicto `E` del bloque append-only quedaría invisible para este
# parser (ni canónica ni sospechosa) y el contador declarado (11) no
# cuadraría contra el real (10).
_VEREDICTO_CANONICO = re.compile(r"`(R\d+\.\d+)`\s*→\s*veredicto\s*`([A-E])`")
# Letra en mayúscula exacta (sin heredar re.I de "veredicto"): con re.I
# sobre todo el patrón, [ABCDE] también matchea la preposición "a" -- ya
# verificado como falso positivo real antes de esta versión.
_VEREDICTO_SOSPECHOSO = re.compile(r"`(R\d+\.\d+)`[^\n`]{0,20}(?i:veredicto)[^\n]{0,15}\b([A-E])\b")

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
    poca distancia, de la palabra 'veredicto' y una letra A-E -- para que
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
# T19a · T-CABECERA-CRUZADA (estado → modelo) — Acto 1, 4/ago/2026.
#   La fila VERIFICAS ASÍ de `estado` cita la versión de `modelo` que
#   hay que tener abierta para verificarla. Esa cita puede desincronizarse
#   sin que ningún test lo note: `modelo` subió de v3.4 a v4.0 (Encargo A,
#   3/ago/2026) y `estado` siguió citando v3.4 en su cabecera un acto
#   entero, mientras su propio §0 ya listaba v4.0 -- exactamente la clase
#   de defecto que I-12 nombró para `gobernanza` (versión del cuerpo
#   distinta de la de su cabecera), aquí aplicada a una cita cruzada
#   entre dos canónicos en vez de a la cabecera de uno solo. Seis
#   apariciones documentadas antes de este test: I-12 ×2, `estado` ×2
#   (esta y la de `modelo` en su propia cabecera, ver T19b), `modelo` ×2.
# ───────────────────────────────────────────────────────────────
def t19a_estado_cita_modelo_vigente():
    """`estado` VERIFICAS ASÍ debe citar la versión de `modelo` que
    `newest()` resuelve hoy -- ni más vieja (Encargo A) ni cualquier
    otra. Solo mira las primeras líneas (cabecera, no el cuerpo): una
    cita histórica de `modelo` en prosa fechada no es este defecto."""
    e = newest("canon/estado-programa-v*.md")
    m = newest("canon/modelo-decision-v*.md")
    if not e or not m:
        fail("T19a", "no se pudo leer `canon/estado-programa-v*.md` o `canon/modelo-decision-v*.md`")
        return
    vm = re.search(r"v(\d+)[._](\d+)", os.path.basename(m))
    if not vm:
        fail("T19a", f"{rel(m)}: no se pudo derivar la versión de su propio nombre de archivo")
        return
    real = f"{vm.group(1)}.{vm.group(2)}"
    cabecera = read(e)[:1500]
    citas = re.findall(r"`modelo`\s+en\s+\*\*v(\d+)[._](\d+)\*\*", cabecera)
    if not citas:
        fail("T19a", f"{rel(e)}: la cabecera no cita ninguna versión de `modelo` en la forma "
                     f"'`modelo` en **vX.Y**' -- VERIFICAS ASÍ debe declarar qué versión verifica")
        return
    for maj, minr in citas:
        if f"{maj}.{minr}" != real:
            fail("T19a", f"{rel(e)}: cabecera VERIFICAS ASÍ cita `modelo` v{maj}.{minr}; "
                         f"la vigente es v{real} ({rel(m)})")


# ───────────────────────────────────────────────────────────────
# T19b · T-CONTADOR-14-CRUZADO — Acto 1, 4/ago/2026.
#   El caso que lo motiva: `modelo §1.1.F`/§6.1/§7 subieron de "8 de 14"
#   a "9 de 14" (Encargo K, 4/ago/2026) pero la cabecera del propio
#   documento (el párrafo de changelog "v4.0 -- 3/ago/2026") se quedó en
#   "8 de 14" -- un acto entero corrigió tres apariciones del mismo
#   contador y dejó la cuarta, más visible, intacta. Cruza tres fuentes:
#   la cabecera, §6.1 (la sección que deriva el denominador) y el
#   conteo real de `procedencia.yaml` -- para que las tres no puedan
#   volver a divergir sin que algo falle.
# ───────────────────────────────────────────────────────────────
# Denominador 14 -> 15 el 13/ago/2026 (ACTO PROC-11, ejecutando ADR-75(b)): entra
# `obligación_medida` como condicional nueva, ver `modelo §1.1.F` Paso 6. El NOMBRE
# de la constante se conserva -- es el identificador del test (T-CONTADOR-14-CRUZADO)
# y renombrarlo rompería la trazabilidad de ADR-51/Encargo K sin ganar nada; lo que
# cambia es el denominador que vigila, no qué vigila.
#
# OJO -- ESTA CONSTANTE NO ES EL ÚNICO SITIO. T19c (abajo) tiene su propia regex
# gemela para el mismo contador, leída sobre README.md en vez de sobre `modelo`.
# ACTO PROC-11 encontró el hueco de la forma cara: su encargo declaraba perímetro
# "SOLO la constante _CONTADOR_14" y, de haberse ejecutado así, README.md habría
# quedado en "9 de 15" con T19c todavía buscando "de 14" -- suite ROJA por un
# perímetro que no podía satisfacer su propio criterio de cierre. Si alguien vuelve
# a mover este denominador, tiene que mover LAS DOS.
#
# NUMERADOR -- séptima clase, 13/ago/2026 (`ACTO PROC-10-bis`, ADR-79(a)):
# `milpa/procedencia.yaml` ganó `MEDIDO·NACIONAL` (marginales medidas sin eje,
# x = ∅) además de `MEDIDO·PARCIAL(x)`. Este predicado, y su gemelo de T19c
# abajo, contaban SOLO `MEDIDO·PARCIAL` -- una subcadena literal que no
# reconoce la clase nueva. El numerador subió de 9 a 10 en `procedencia.yaml`
# (entra `norma_de_género`) pero el conteo mecánico se quedó en 9: suite ROJA
# declarada por `PROC-10-bis` (`forense/notas/2026-08-13-proc-10-bis.md` §4),
# corregida aquí. Mismo criterio que el hueco del párrafo de arriba: quien
# mueva el numerador con una clase nueva tiene que sumarla aquí Y en T19c.
_CONTADOR_14 = re.compile(r"condicionales medidas sobre atributos:\s*(?:~~\d+~~\s*)?(\d+)\s*de\s*15", re.I)

def t19b_modelo_contador_14():
    """La cabecera de `modelo` ('condicionales medidas sobre atributos:
    N de 14', en el párrafo de changelog de la versión vigente) debe
    coincidir con la misma frase dentro de §6.1, y con el conteo real
    de `clase: "MEDIDO·PARCIAL` en `milpa/procedencia.yaml`."""
    m = newest("canon/modelo-decision-v*.md")
    if not m:
        fail("T19b", "no se pudo leer `canon/modelo-decision-v*.md`")
        return
    s = read(m)
    mc = _CONTADOR_14.search(s[:2000])
    if not mc:
        fail("T19b", f"{rel(m)}: la cabecera (primeros 2000 caracteres) no declara "
                     f"'condicionales medidas sobre atributos: N de 14'")
        return
    declarado_cabecera = int(mc.group(1))

    sec = re.search(r"^### 6\.1[^\n]*\n(.*?)(?=^## |\Z)", s, re.M | re.S)
    if not sec:
        fail("T19b", f"{rel(m)}: no se encontró la sección §6.1")
        return
    ms = _CONTADOR_14.search(sec.group(1))
    if not ms:
        fail("T19b", f"{rel(m)} §6.1: no declara 'condicionales medidas sobre atributos: N de 14'")
        return
    declarado_61 = int(ms.group(1))
    if declarado_cabecera != declarado_61:
        fail("T19b", f"{rel(m)}: cabecera declara {declarado_cabecera} de 14; "
                    f"§6.1 declara {declarado_61} de 14")

    proc = os.path.join(ROOT, "milpa", "procedencia.yaml")
    if not os.path.exists(proc):
        fail("T19b", "no se pudo leer `milpa/procedencia.yaml`")
        return
    ptxt = read(proc)
    real = ptxt.count('clase: "MEDIDO·PARCIAL') + ptxt.count('clase: "MEDIDO·NACIONAL')
    if declarado_cabecera != real:
        fail("T19b", f"{rel(m)}: cabecera declara {declarado_cabecera} de 14; "
                    f"`grep -c 'clase: \"MEDIDO·PARCIAL\\|MEDIDO·NACIONAL' {rel(proc)}` da {real}")


# ───────────────────────────────────────────────────────────────
# T19c · T-PORTADA-DERIVADA — Acto 1, 4/ago/2026. Cierra I-06 ("nadie
#   vigila las cifras de README.md contra el árbol") e I-07 (una cifra
#   corregida en la portada sobrevivió sin sincronizar al canon, porque
#   el encargo nombró un archivo y no una afirmación). Cruza las tres
#   cifras derivadas que este acto puso en README `## Estado del
#   modelo` contra su fuente real: fichas del bloque append-only de
#   `hitoD-preregistro` (mismo parser canónico que T18, `_VEREDICTO_
#   CANONICO`, aplicado SOLO al bloque designado), `MEDIDO·PARCIAL` de
#   `procedencia.yaml`, y coeficientes en escala (0 de 15 mientras
#   `procedencia.yaml` no promueva ninguno de ASIGNADO a medido en la
#   escala del modelo -- ADR-57(a) excluye los tres β̂ marginales).
# ───────────────────────────────────────────────────────────────
def t19c_readme_derivadas():
    r = os.path.join(ROOT, "README.md")
    if not os.path.exists(r):
        fail("T19c", "no se pudo leer `README.md`")
        return
    s = read(r)
    m = re.search(r"^## Estado del modelo\b.*?(?=^## |\Z)", s, re.M | re.S)
    if not m:
        fail("T19c", "README.md: no se encontró la sección `## Estado del modelo`")
        return
    bloque = m.group(0)

    h = newest("forense/hitoD-preregistro-v*.md")
    if not h:
        fail("T19c", "no se pudo leer `forense/hitoD-preregistro-v*.md`")
    else:
        vb = _bloque_veredictos(read(h))
        if vb is None:
            fail("T19c", f"{rel(h)}: no se encontró '## Registro de veredictos archivados' (ADR-40)")
        else:
            fichas = {}
            for l in vb.split("\n"):
                mv = _VEREDICTO_CANONICO.search(l)
                if mv:
                    fichas[mv.group(1)] = mv.group(2)
            real_n = len(fichas)
            letras = Counter(fichas.values())

            mn = re.search(r"\*\*(\d+)\s*de\s*27\*\*\s*corridas del Hito D", bloque)
            if not mn:
                fail("T19c", "README.md, `## Estado del modelo`: no se encontró "
                             "'**N de 27** corridas del Hito D'")
            elif int(mn.group(1)) != real_n:
                fail("T19c", f"README.md declara {mn.group(1)} de 27 corridas del Hito D; "
                            f"el bloque append-only de {rel(h)} tiene {real_n} fichas con veredicto")

            md = re.search(r"—\s*\*\*([\dA-E·\s]+)\*\*", bloque)
            if not md:
                fail("T19c", "README.md, `## Estado del modelo`: no se encontró el desglose por letra "
                             "(forma '**NLETRA·...**' tras un guion largo)")
            else:
                declarado = dict((letra, int(n)) for n, letra in
                                  re.findall(r"(\d+)([A-E])", md.group(1)))
                derivado = {k: v for k, v in letras.items() if v}
                if declarado != derivado:
                    fail("T19c", f"README.md declara desglose {declarado}; "
                                f"derivado del bloque append-only: {derivado}")

    proc = os.path.join(ROOT, "milpa", "procedencia.yaml")
    if not os.path.exists(proc):
        fail("T19c", "no se pudo leer `milpa/procedencia.yaml`")
        return
    ptxt = read(proc)
    real_medidas = ptxt.count('clase: "MEDIDO·PARCIAL') + ptxt.count('clase: "MEDIDO·NACIONAL')
    # Regex GEMELA de `_CONTADOR_14` (línea ~869), sobre README en vez de `modelo`.
    # Denominador 14 -> 15 el 13/ago/2026, ACTO PROC-11 -- ver el comentario largo
    # junto a esa constante: las dos se mueven juntas o la suite se pone roja.
    # NUMERADOR -- séptima clase, 13/ago/2026 (`ACTO PROC-10-bis`, ADR-79(a)):
    # `MEDIDO·NACIONAL` entra a la cuenta junto con `MEDIDO·PARCIAL(x)`; ver el
    # comentario largo junto a `_CONTADOR_14` -- las dos regex se corrigen juntas
    # o la suite se pone roja otra vez.
    mcond = re.search(r"[Cc]ondicionales medidas\s*(\d+)\s*de\s*15", bloque)
    if not mcond:
        fail("T19c", "README.md, `## Estado del modelo`: no se encontró "
                     "'condicionales medidas N de 15'")
    elif int(mcond.group(1)) != real_medidas:
        fail("T19c", f"README.md declara condicionales medidas {mcond.group(1)} de 15; "
                    f"`grep -c 'clase: \"MEDIDO·PARCIAL\\|MEDIDO·NACIONAL' {rel(proc)}` da {real_medidas}")

    promovido = re.search(r"magnitud:\s*medid", ptxt, re.I) is not None
    mcoef = re.search(r"[Cc]oeficientes en escala del modelo\s*(\d+)\s*de\s*15", bloque)
    if not mcoef:
        fail("T19c", "README.md, `## Estado del modelo`: no se encontró "
                     "'coeficientes en escala del modelo N de 15'")
    elif int(mcoef.group(1)) != 0 or promovido:
        fail("T19c", f"README.md declara {mcoef.group(1)} de 15 coeficientes en escala; "
                    + ("`milpa/procedencia.yaml` promueve alguno a medido -- la cifra debe subir de 0"
                       if promovido else
                       "`milpa/procedencia.yaml` no sostiene un valor distinto de 0"))


# ───────────────────────────────────────────────────────────────
# T20 · T-CASCADA-MARCADA — Encargo CU, 5/ago/2026. Cierra (parcialmente)
#   el requisito de salida de ADR-45 (`gobernanza:362`, I-07): "ninguna
#   afirmación de conteo de veredictos... existe en `canon/` fuera de su
#   bloque de fuente única sin decir cuál de las tres poblaciones cita y
#   con qué denominador".
#
#   Hallazgo que lo motiva: con T18 vigilando un solo sitio vigente
#   (`estado:196`) y T19c otro (`README:36`), la cascada de ADR-55/56/58/60
#   se ejecutó completa cada vez, pero el perímetro ACOTADO de ADR-63
#   (R1.3→E, 12→13) dejó fuera `gobernanza:358` y `:810` -- declarado
#   como deuda por el propio ADR-63 (`gobernanza:786`) -- Y ADEMÁS
#   `modelo-decision:64` y `:636`, que ninguna nota de deuda anterior
#   había nombrado nunca. Los cuatro declaraban "12 de 27" con la suite
#   completa en VERDE, porque ningún test los leía. Encargo CU corrigió
#   los cuatro con cascada completa (no acotada) y marca los ocho sitios
#   vigentes de canon/README que sí hacen la afirmación DIRECTA de
#   "corridas archivadas" -- para que la próxima cascada acotada no
#   vuelva a dejar un sitio invisible atrás.
#
#   Convención de marcado (extiende la que `README.md` ya usa para sus
#   propias cifras de portada, p. ej. líneas 34/37 -- receta de derivación
#   en un comentario HTML junto a la cifra): un comentario
#   `<!-- T20:HITO-D pob=reglas -->` en cualquier punto de la MISMA línea
#   física que la cifra vigente. `pob=reglas` declara que la cifra cuenta
#   REGLAS distintas con veredicto archivado -- el denominador de
#   T18/T19c y de `_bloque_veredictos` (el diccionario `fichas` colapsa
#   por ID de regla: `R4.3` se archiva en dos mitades y cuenta 1, no 2).
#   El test toma la PRIMERA cifra en forma "N de 27" que aparezca en esa
#   línea -- verificado contra los ocho sitios marcados en este acto: en
#   todos, la afirmación vigente antecede a cualquier mención histórica
#   de transición ("N de 27 → M de 27") que pueda venir después en la
#   misma línea, dentro de la cola fechada de correcciones.
#
#   LÍMITE DECLARADO -- léelo antes de asumir que esto cierra I-07 por
#   completo. T20 vigila los sitios MARCADOS. Un contador vigente nuevo
#   que nadie marque sigue siendo invisible para la suite; la marca es
#   obligación de quien escribe la cifra, no algo que este test pueda
#   descubrir por sí solo. Tampoco entiende una cifra en forma
#   COMPLEMENTO ("N de 27 SIN corrida"): `estado-programa:122` declara
#   vigente "14 de 27 sin corrida" (27-13=14, correcto hoy) pero se deja
#   SIN MARCAR a propósito -- marcarla con la etiqueta de hoy produciría
#   un FAIL falso, porque T20 compara la cifra encontrada directo contra
#   `real` sin restar de 27. Extender la etiqueta a `forma=complemento`
#   queda fuera de este acto.
#
#   No duplica a T18 ni a T19c -- ambos siguen como están, verdes y
#   verificados, y no se borran. `README:36` y `estado:196` sí llevan
#   también la marca de T20 (para que la cascada vigilada cubra todo el
#   universo declarado, no solo lo que quedó fuera de T18/T19c) -- eso
#   vuelve a T20 redundante con T18 en `estado:196` y con T19c en
#   `README:36`. Redundancia observada y anotada aquí para mesa, no
#   removida: decidir si T18/T19c se retiran queda fuera de este acto.
# ───────────────────────────────────────────────────────────────
_MARCA_T20_HITO_D = re.compile(r"T20:HITO-D\s+pob=(\S+?)\s*-->")
_CONTADOR_DE_27 = re.compile(r"(\d+)\s*de\s*27\b")

def t20_cascada_marcada():
    """Cada sitio de `README.md`/`canon/*.md` marcado `<!-- T20:HITO-D
    pob=reglas -->` debe declarar, en la misma línea, la misma cifra de
    'N de 27' que produce `_bloque_veredictos` + `_VEREDICTO_CANONICO`
    sobre el bloque append-only de `hitoD-preregistro` (el mismo parser
    canónico que usan T18/T19c). No inspecciona nada sin marca -- ver
    límite declarado arriba."""
    h = newest("forense/hitoD-preregistro-v*.md")
    if not h:
        fail("T20", "no se pudo leer `forense/hitoD-preregistro-v*.md`")
        return
    bloque = _bloque_veredictos(read(h))
    if bloque is None:
        fail("T20", f"{rel(h)}: no se encontró el bloque "
                    f"'## Registro de veredictos archivados' (ADR-40)")
        return
    fichas = {}
    for l in bloque.split("\n"):
        m = _VEREDICTO_CANONICO.search(l)
        if m:
            fichas[m.group(1)] = m.group(2)
    real = len(fichas)

    archivos = [os.path.join(ROOT, "README.md")] + sorted(glob.glob(os.path.join(ROOT, "canon", "*.md")))
    marcados = 0
    for p in archivos:
        if not os.path.exists(p):
            continue
        for i, l in enumerate(read(p).split("\n"), 1):
            mm = _MARCA_T20_HITO_D.search(l)
            if not mm:
                continue
            marcados += 1
            pob = mm.group(1)
            if pob != "reglas":
                fail("T20", f"{rel(p)}:{i} marcador T20:HITO-D declara población "
                            f"'{pob}' -- este test solo sabe verificar 'reglas'")
                continue
            mn = _CONTADOR_DE_27.search(l)
            if not mn:
                fail("T20", f"{rel(p)}:{i} tiene marcador T20:HITO-D pero no se "
                            f"encontró ninguna cifra en forma 'N de 27' en la misma línea")
                continue
            declarado = int(mn.group(1))
            if declarado != real:
                fail("T20", f"{rel(p)}:{i} declara {declarado} de 27 corridas archivadas "
                            f"(marcado T20:HITO-D, pob=reglas); el bloque append-only de "
                            f"{rel(h)} tiene {real} veredictos archivados en forma canónica "
                            f"(`_VEREDICTO_CANONICO`)")
    if marcados == 0:
        warn("T20", "ningún sitio con marcador `T20:HITO-D` encontrado en "
                     "README.md/canon/*.md -- ¿se perdió el marcado?")


# ───────────────────────────────────────────────────────────────
# T22 · T-FIRMAS — el tablero de firmas pendientes se deriva, no se
#   recuerda (A.12, `instrucciones-proyecto-v2_9.md` · ACTO TABLERO-FIRMAS,
#   14/ago/2026). Firma de mesa que motiva el mecanismo, verbatim: "está
#   bien que yo tenga que sellar; el maldito problema viene cuando ya ni
#   nos acordamos que tengo que sellar y se quedan en el limbo como
#   muchas otras cosas."
#
#   (a) WARN por cada fila `ABIERTA` de `forense/firmas-pendientes.tsv`,
#   con sus días de antigüedad -- la memoria mecánica: no depende de que
#   alguien se acuerde, grita en cada corrida de la suite, en cada acto,
#   para siempre.
#
#   (b) FAIL si un archivo NUEVO de `canon/`/`forense/` trae un marcador
#   de ranura de firma o de decisión de mesa sin resolver (las mismas dos
#   expresiones que sembraron el tablero: `grep -rn "RANURA"` y
#   `grep -rn "requiere_decision.*true\|PENDIENTE de mesa\|pendiente
#   nombrado.*mesa\|PROPUESTA.*mesa"`) sin que ninguna fila del tablero lo
#   cite en `dónde` -- el mecanismo se auto-protege desde su propio primer
#   commit.
#
#   (c) WARN por cada fila `FIRMADA` con `ejecutada_en` vacío, con sus
#   días de antigüedad (ADR-94, columnas `ejecutada_en`/`encargo`
#   añadidas al tablero en ese mismo acto). `estado` solo distinguía
#   ABIERTA de FIRMADA -- ninguno de los cuatro valores significaba
#   "firmada y sin ejecutar", que es distinto de "firmada" a secas: una
#   firma resuelve la pregunta de mesa, no escribe el archivo. Mismo
#   mecanismo que (a), sobre la columna nueva.
#
#   LÍMITE DECLARADO -- léelo antes de tocar este test. (b) tiene
#   granularidad de ARCHIVO, no de línea: un archivo ya conocido (el
#   snapshot de abajo, verificado al sellar T-FIRMAS) puede ganar una
#   mención nueva del marcador sin volver a fallar. Granularidad de línea
#   sería más fina pero más frágil -- el propio ACTO TABLERO-FIRMAS vio
#   números de línea correrse varias veces por ediciones ajenas dentro de
#   una sola sesión (`forense/notas/2026-08-14-tablero-firmas.md`). La
#   protección real de (b) es contra la clase de defecto que motivó todo
#   el acto -- un documento NUEVO (encargo, nota, ADR) que crea una
#   ranura o deja una decisión sin resolver y nadie lo sube al tablero --
#   no contra cada edición de un archivo que ya está vigilado.
# ───────────────────────────────────────────────────────────────
_T22_MARCADOR_RANURA = re.compile(r"RANURA")
_T22_MARCADOR_PENDIENTE = re.compile(
    r"requiere_decision.*true|PENDIENTE de mesa|pendiente nombrado.*mesa|PROPUESTA.*mesa")

# Snapshot verificado por los dos grep del propio encargo (`grep -rl
# "RANURA" canon/ forense/` + `grep -rl` con el patrón de arriba) al
# sellar T22 -- ACTO TABLERO-FIRMAS, 14/ago/2026. Cada archivo de esta
# lista ya se revisó contra `forense/firmas-pendientes.tsv` (fila con
# estado real, o exclusión razonada -- ver `forense/notas/2026-08-14-
# tablero-firmas.md`). Un archivo NUEVO que no esté aquí y traiga
# cualquiera de los dos marcadores es exactamente el defecto que (b)
# existe para atrapar.
_T22_ARCHIVOS_CONOCIDOS = {
    # forense/encargos/2026-08-26-MAESTRA31-E2-REGISTRA-PENDIENTES.md --
    # encargo verbatim (A.3) que pide abrir fila de tablero para siete
    # pendientes heredados de mesa (P1-P7). Verificado por el propio acto
    # que lo ejecuto: los siete ya estaban resueltos o vigentes en el
    # arbol (P1=PR #381, P2=FP-166 FIRMADA, P3=FP-169 en paralelo, P4 ya
    # citado en hitoD-preregistro-v2_0.md, P5 verbatim en FP-165 FIRMADA,
    # P6/P7 politica y regla vigentes) -- dirección, consultada con el
    # hallazgo, ordenó no abrir ninguna fila (ver ADR-211 y
    # forense/notas/2026-08-26-registra-pendientes-cierre.md). El
    # marcador que T22 detecta es del encargo pedido, no de una decisión
    # de mesa nueva sin registrar.
    "forense/encargos/2026-08-26-MAESTRA31-E2-REGISTRA-PENDIENTES.md",
    # forense/notas/2026-08-25-sella-e.md -- discute cinco letras de mesa
    # (L1-L5) y FP-24, todas ya rastreadas en firmas-pendientes.tsv
    # (FP-127..FP-130, FP-63, FP-24) o explícitamente reportadas como sin
    # ruling verbatim en el repo -- ninguna es un marcador nuevo. Extensión
    # mínima de perímetro por desviación mecánica, mismo precedente que
    # ADR-147(c)/ADR-149(f)/ADR-151 -- ACTO SELLA-AGO25-E, 25/ago/2026.
    "forense/notas/2026-08-25-sella-e.md",
    # forense/notas/2026-08-25-sella-f.md y su encargo -- discuten ocho letras
    # de mesa (L1-L8) y FP-118, todas ya rastreadas en firmas-pendientes.tsv
    # (FP-127..FP-132, FP-63, FP-24, FP-118) o explícitamente reportadas como
    # sin ruling verbatim en el repo -- ninguna es un marcador nuevo. Misma
    # extensión mínima de perímetro por desviación mecánica que ADR-147(c)/
    # ADR-149(f)/ADR-151/ADR-164 -- ACTO SELLA-AGO25-F, 25/ago/2026.
    "forense/notas/2026-08-25-sella-f.md",
    # forense/notas/2026-08-26-prereg-corrida-cierre.md -- discute RANURA 1
    # y RANURA 2 de ACTO PREREG-CORRIDA, ambas ya rastreadas: RANURA 1 es
    # FP-161 (FIRMADA, ADR-194) y RANURA 2 queda adoptada en el mismo ADR
    # sin fila propia (no pide firma de mesa). No es un marcador nuevo.
    "forense/notas/2026-08-26-prereg-corrida-cierre.md",
    # forense/encargos/2026-08-25-SELLA-A1-CODI.md -- encargo archivado
    # verbatim (convencion de forense/encargos/, A.3), incluye la RANURA
    # de firma de mesa tal como se lanzo. La firma que esa ranura pedia
    # ya esta capturada: FP-104 en firmas-pendientes.tsv paso a FIRMADA
    # con el verbatim exacto y ADR-177 la sella -- no es un marcador
    # nuevo sin dueno, es la copia fiel de uno ya resuelto. Extension
    # minima de perimetro por desviacion mecanica, mismo precedente que
    # ADR-147(c)/ADR-149(f)/ADR-151/ADR-164 -- ACTO SELLA-A1-CODI,
    # 25/ago/2026 (PR #350, CI del propio acto).
    "forense/encargos/2026-08-25-SELLA-A1-CODI.md",
    "forense/encargos/2026-08-25-SELLA-AGO25-F.md",
    # forense/encargos/2026-08-26-PREREG-CORRIDA.md -- encargo archivado
    # verbatim (convencion de forense/encargos/, A.3), incluye las dos
    # RANURAS de firma de mesa tal como se lanzaron. RANURA 1 (cual-L) ya
    # esta capturada: FP-161 en firmas-pendientes.tsv nace FIRMADA con el
    # verbatim exacto y ADR-194 la sella; RANURA 2 (D-iii) queda adoptada
    # en el mismo ADR sin fila propia (no pide firma de mesa, designa un
    # patron ya vigente en pipeline-L-adv1-m2.py). No es un marcador nuevo
    # sin dueno, es la copia fiel de uno ya resuelto y otro ya adoptado.
    "forense/encargos/2026-08-26-PREREG-CORRIDA.md",
    # forense/encargos/2026-08-26-E1-CIERRA-FP157.md y su nota -- encargo
    # archivado verbatim (convencion de forense/encargos/, A.3), incluye la
    # RANURA de firma de mesa (FIRMA M-FP157) tal como se lanzo. La firma que
    # esa ranura pedia ya esta capturada: FP-157 en firmas-pendientes.tsv pasa
    # a FIRMADA con el verbatim exacto y ADR-201 la sella (renumerado de
    # ADR-200 al fusionar segundo -- ADR-200 lo tomo ACTO E2-PREP-L-RUN,
    # PR #371) -- no es un marcador nuevo sin dueno. Mismo precedente que
    # SELLA-A1-CODI/PREREG-CORRIDA -- ACTO CIERRA-FP157, 26/ago/2026.
    "forense/encargos/2026-08-26-E1-CIERRA-FP157.md",
    "forense/notas/2026-08-26-cierra-fp157-cierre.md",
    # forense/prereg-duelo-v2/lanzamiento-L-v1_0.md, su nota de cierre y su
    # encargo archivado (ACTO E2-PREP-L-RUN, 26/ago/2026) -- citan "RANURA
    # DE MESA" (el modelo del corredor L, ya precargado por el encargo y
    # dejado tal cual, F2(a) del prereg) y "RANURA 1"/"RANURA 2" de
    # PREREG-CORRIDA, ambas ya resueltas: RANURA 1 es FP-162 (FIRMADA,
    # ADR-197) y RANURA 2 queda adoptada en el mismo ADR sin fila propia.
    # Ninguna de las tres cita un marcador nuevo sin dueño -- extensión
    # mínima de perímetro por desviación mecánica, mismo precedente que
    # ADR-147(c)/ADR-149(f)/ADR-151/ADR-164/ADR-197.
    "forense/prereg-duelo-v2/lanzamiento-L-v1_0.md",
    "forense/notas/2026-08-26-prep-l-run-cierre.md",
    "forense/encargos/2026-08-26-E2-PREP-L-RUN.md",
    # forense/notas/2026-08-25-sella-f-hoja.md y su encargo -- continuación de
    # SELLA-AGO25-F, ejecuta las diez letras de mesa (L1-L10) ya resueltas y
    # abre seis actos sucesores declarados (FP-135..FP-140), todos ya con fila
    # propia en firmas-pendientes.tsv -- ninguna es un marcador nuevo sin
    # rastro. Misma extensión mínima de perímetro que ADR-164/ADR-165 --
    # ACTO SELLA-AGO25-F (continuación), 25/ago/2026.
    "forense/notas/2026-08-25-sella-f-hoja.md",
    "forense/encargos/2026-08-25-SELLA-AGO25-F-HOJA.md",
    # forense/notas/2026-08-20-emisor-m-verificacion-premisas.md:26 -- "⊕ sigue
    # PROPUESTA sin sellar (mesa-pendientes §3)" es una referencia de solo
    # lectura a un pendiente YA existente y ya rastreado en `mesa-pendientes.md`
    # (§3), no un marcador nuevo que necesite fila propia en firmas-pendientes.tsv
    # -- ACTO LANDING-EMISOR-M1, 21/ago/2026.
    "forense/notas/2026-08-20-emisor-m-verificacion-premisas.md",
    "canon/gobernanza-v1_15.md",
    "forense/encargos/2026-08-11-A-renglon-llaves.md",
    "forense/encargos/2026-08-12-E4c-commit4.md",
    "forense/encargos/2026-08-12-E4c-paso3-corrida.md",
    "forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo-p-lote1.md",
    "forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md",
    "forense/encargos/2026-08-12-veredicto-pr185-mapeo-universo-map-a.md",
    "forense/encargos/2026-08-12-veredicto-pr185-mapeo-universo-map-b.md",
    "forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md",
    "forense/encargos/2026-08-13-RP-reconcilia-puertas.md",
    "forense/ficha-id-g3-v1_0.md",
    "forense/firmas-pendientes.tsv",
    "forense/hallazgos.md",
    "forense/notas/2026-08-05-s2-idg3-sello.md",
    "forense/notas/2026-08-11-e4b-sello-b-corrida-b.md",
    "forense/notas/2026-08-11-e4c-r5-1-d2-commit3-ajuste-preejecucion.md",
    "forense/notas/2026-08-12-acto-m-adq-ensafi-enfih.md",
    "forense/notas/2026-08-12-e4c-r5-1-d2-commit4-diseno-resuelto.md",
    "forense/notas/2026-08-12-u1-e4b-prime-recorrida.md",
    "forense/notas/2026-08-13-enasic-split-verificacion.md",
    "forense/notas/2026-08-13-proc-11.md",
    "forense/notas/2026-08-13-res-reserva.md",
    "forense/notas/2026-08-13-sella-3.md",
    "forense/notas/2026-08-14-sanea-mapeo.md",
    "forense/notas/2026-08-14-tablero-firmas.md",
    "forense/notas/2026-08-14-t-firmas.md",
    # Sumados en ACTO TABLERO-FIRMAS COMMIT 3 -- origin/main avanzó con
    # ENLACE-2/MOTOR-3-E0/RECONCILIA-SPEC (PR #236-238) mientras este acto
    # investigaba; ver forense/notas/2026-08-14-tablero-firmas-commit3.md.
    "forense/encargos/2026-08-14-ENLACE-2-adjudicacion-68-y-19.md",  # cita FP-24 (RANURA c) y los M1-M6 ya cubiertos por FP-01..FP-06
    "forense/notas/2026-08-14-enlace2-68-mas-19.md",                # fuente primaria de FP-24
    "forense/notas/2026-08-14-enlace2-clase-limbo.md",              # fuente primaria de FP-24, §4
    "forense/encargos/2026-08-14-MOTOR-3-E0-autocontenido.md",      # solo referencia M1-M6, ya cubiertos por FP-01..FP-06
    "forense/notas/2026-08-14-tablero-firmas-commit3.md",            # esta misma nota cita los marcadores verbatim al documentarlos -- mismo autocaptura que ya tuvo el commit 2
    "forense/notas/2026-08-14-tablero-firmas-commit4-freeze.md",     # ídem, tercera vez
    "forense/notas/2026-08-14-tablero-firmas-commit5-colision-adr84.md",  # ídem, cuarta vez
    # Sumado en ACTO CI-CATEGORIA, 18/ago/2026 -- la nota documenta, por
    # nombre, el control C2 del commit 1 (que crea a propósito un archivo
    # con el marcador RANURA para probar la protección de (b)); la cita es
    # verbatim al describir el control, no una ranura real sin fila --
    # mismo autocaptura ya visto en las notas de TABLERO-FIRMAS arriba.
    # (El encargo archivado del mismo acto, 2026-08-18-CI-CATEGORIA-
    # devolver-significado-ci.md, no lleva ninguno de los dos marcadores
    # -- verificado, no supuesto -- así que no se añade aquí.)
    "forense/notas/2026-08-18-ci-categoria.md",
    # Sumado en ACTO SELLO-FICHA-G3, 18/ago/2026 -- dispara
    # `_T22_MARCADOR_PENDIENTE` (`PROPUESTA.*mesa`) por coincidencia de dos
    # citas ajenas en la misma línea del Estado: "PROPUESTA DE SELLO
    # COMPLETA" (cita el estado ya existente de FP-11, `firmas-
    # pendientes.tsv:12`) y "...que mesa firmó" (cita verbatim el gate del
    # propio encargo). No crea ninguna decisión nueva sin registrar: FP-11
    # ya tiene su fila, ya es `FIRMADA-CONDICIONAL`, y este acto no le
    # cambió el estado -- verificado, no supuesto, y explicado en la propia
    # nota (§6). Mismo criterio de autocaptura verbatim que las notas de
    # TABLERO-FIRMAS/CI-CATEGORIA ya usaron.
    "forense/notas/2026-08-18-sello-ficha-g3-gate-e0e5-no-cumplido.md",
    # Sumado en ACTO SELLO-FICHA-G3-V2, 19/ago/2026 -- cita el estado viejo
    # de la ficha ("PROPUESTA DE SELLO COMPLETA... mesa eligió"), dos
    # términos sin relación, mismo patrón que la línea de arriba -- ver
    # esa misma nota, §7.
    "forense/notas/2026-08-19-sello-ficha-g3-v2-adjudica-idx.md",
    # Sumados en ACTO NOTAS-P3, 18/ago/2026 -- ejecuta CONSOLIDA-17AGO
    # §PARTE 3 (el barrido de firmas-pendientes.tsv en sí). El encargo
    # reproduce verbatim (A.3) el patrón de dirección, que cita "RANURA"
    # y "Pendiente de mesa" como sus propios ejemplos/controles positivos;
    # la nota del acto documenta esos mismos hallazgos citándolos -- mismo
    # autocaptura ya visto arriba en TABLERO-FIRMAS y CI-CATEGORIA, no una
    # ranura real sin fila. Los tres `FILA` que este acto sí abre (FP-54,
    # FP-55, FP-56) están citados en `forense/firmas-pendientes.tsv` desde
    # el mismo commit -- eso es lo que (b) protege, y sigue protegido.
    "forense/encargos/2026-08-18-NOTAS-P3.md",
    "forense/notas/2026-08-18-p3-barrido-final.md",
    # Sumados en ACTO REPARA-T22, 21/ago/2026 -- ambos citan verbatim el
    # bloque de patrones de la Parte 3 de CONSOLIDA-17AGO como sus propios
    # ejemplos ("queda (a|para) mesa | pendiente de mesa | decisión de
    # mesa pendiente | ..."), no un pendiente real sin registrar. Ya
    # diagnosticado el mismo día en la propia nota, que dejó el ajuste a
    # `_T22_ARCHIVOS_CONOCIDOS` para un acto sucesor con `tests/**` en su
    # perímetro (`forense/notas/2026-08-17-consolida.md`, entrada `T22`).
    "forense/encargos/2026-08-17-CONSOLIDA-17AGO.md",
    "forense/notas/2026-08-17-consolida.md",
    # Descubiertos por el acotamiento de (b) a filas ABIERTA/FIRMADA del
    # mismo ACTO REPARA-T22 -- antes exentos por una fila CERRADA de otro
    # archivo que citaba su nombre; verificados uno por uno, mismo
    # mecanismo de autocaptura verbatim que las entradas de arriba, no un
    # pendiente sin registrar:
    #  - EDEC cita el propio comando `grep -n "pendiente nombrado\|queda
    #    para mesa\|sigue en mesa"` que corre contra `gobernanza-v1_15.md`
    #    ("hits sin fila" -- describe el resultado del grep, no crea uno).
    #  - la nota de fuente-única lo reproduce verbatim y lo declara: "Los
    #    dos archivos nuevos de este acto disparan el marcador por
    #    construcción" (línea 233 propia).
    #  - LANE-A-E0-E5 usa "RANURAS DEL SELLO" como nombre de sección del
    #    propio encargo (a llenar con firmas de ADR-100 ya existentes),
    #    no una ranura nueva sin fila.
    "forense/encargos/2026-08-17-EDEC-fuente-unica-decisiones.md",
    "forense/notas/2026-08-17-fuente-unica-decisiones.md",
    "forense/encargos/2026-08-18-LANE-A-E0-E5.md",
    # El propio encargo de este acto, archivado verbatim (A.3): reproduce
    # citas literales del bloque T22 (RANURA/PENDIENTE de mesa/PROPUESTA)
    # como parte de su propia descripción del defecto que repara -- mismo
    # autocaptura, no un pendiente real sin fila.
    "forense/encargos/2026-08-21-REPARA-T22.md",
    "forense/notas/2026-08-21-repara-t22-cierre.md",  # ídem, cita verbatim las mismas fuentes al documentarlas -- mismo autocaptura
    # Sumados en ACTO COMMIT-DOC-COERCION, 24/ago/2026 -- disparan
    # `_T22_MARCADOR_PENDIENTE` (`PROPUESTA.*mesa`) por la cabecera nueva
    # que el propio acto rotula, verbatim, en el documento que commitea:
    # "PROPUESTA (no sellada) -- adjunto de mesa 24/ago". No es una
    # decisión nueva sin registrar -- es exactamente lo que `FP-113` ya
    # rastrea, y este mismo acto cierra esa fila a `FIRMADA` en el mismo
    # commit. El documento y su encargo/nota citan el rótulo verbatim al
    # describirlo -- mismo autocaptura ya visto arriba.
    "forense/COERCION-Y-ADOPCION-rediseno-2026-08-20.md",
    "forense/encargos/2026-08-24-ACTO-COMMIT-DOC-COERCION.md",
    "forense/notas/2026-08-24-commit-doc-coercion.md",
    # forense/encargos/2026-08-25-SELLA-SORTEO-V2.md -- encargo archivado
    # verbatim (convencion de forense/encargos/, A.3), incluye la RANURA
    # de firma de mesa tal como se lanzo. La firma que esa ranura pedia
    # ya esta capturada: FP-150 en firmas-pendientes.tsv paso a FIRMADA
    # con el verbatim exacto y ADR-178 la sella -- no es un marcador
    # nuevo sin dueno, es la copia fiel de uno ya resuelto. Su nota de
    # cierre cita el mismo verbatim al documentarlo -- mismo autocaptura.
    # Extension minima de perimetro por desviacion mecanica, mismo
    # precedente que ADR-147(c)/ADR-149(f)/ADR-151/ADR-164/ADR-177 --
    # ACTO SELLA-SORTEO-V2, 25/ago/2026 (PR #351, CI del propio acto).
    "forense/encargos/2026-08-25-SELLA-SORTEO-V2.md",
    "forense/notas/2026-08-25-sella-sorteo-v2-cierre.md",
    # forense/encargos/2026-08-26-E5-SELLA-FP164-OCTAVA.md -- encargo
    # archivado verbatim (A.3), incluye la RANURA de firma de mesa tal
    # como se lanzo. La firma que esa ranura pedia ya esta capturada:
    # FP-164 en firmas-pendientes.tsv paso a FIRMADA con el verbatim
    # exacto y ADR-204 la ejecuta -- no es un marcador nuevo sin dueno.
    # Su nota de cierre cita el mismo verbatim al documentarlo -- mismo
    # autocaptura visto arriba. Extension minima de perimetro por
    # desviacion mecanica, mismo precedente que ADR-177/ADR-201/ADR-203
    # -- ACTO E5-SELLA-FP164-OCTAVA, 26/ago/2026.
    "forense/encargos/2026-08-26-E5-SELLA-FP164-OCTAVA.md",
    "forense/notas/2026-08-26-sella-fp164-cierre.md",
    # forense/notas/2026-08-30-propaga-firmas-cierre.md -- nota de cierre
    # de ACTO MAESTRA32-E5 · PROPAGA-FIRMAS-Y-COLA. Discute las cuatro
    # RANURAS opcionales del encargo (R-168, R-AGREGA, R-169,
    # R-ENTERADOS) y la RANURA M-EXTRACTOR de MAESTRA32-E3 -- todas ya
    # rastreadas en firmas-pendientes.tsv (FP-168/170/169/171/172/173/
    # 174/175/178, mas la fila-grito FP-179 nueva) antes de que esta nota
    # existiera. Ninguna es un marcador nuevo sin dueno. Extension minima
    # de perimetro por desviacion mecanica -- el encargo de este acto
    # (Bloque PERIMETRO) solo listaba _T25_ARCHIVOS_CONOCIDOS para
    # tests/check.py, sin anticipar que discutir ranuras ya tablero-
    # izadas dispara tambien T22; mismo precedente y misma logica que
    # ADR-147(c)/ADR-149(f)/ADR-151/ADR-164/ADR-177 aplicados aqui a la
    # constante hermana. Declarado en la propia nota de cierre.
    "forense/notas/2026-08-30-propaga-firmas-cierre.md",
}

def _t22_tabla():
    """Lee forense/firmas-pendientes.tsv como lista de dicts (una por fila,
    en el orden del archivo). (None, []) si el archivo no existe."""
    p = os.path.join(ROOT, "forense", "firmas-pendientes.tsv")
    if not os.path.exists(p):
        return None, []
    lineas = read(p).split("\n")
    if not lineas or not lineas[0].strip():
        return p, []
    cabecera = lineas[0].split("\t")
    filas = []
    for l in lineas[1:]:
        if not l.strip():
            continue
        campos = l.split("\t")
        if len(campos) != len(cabecera):
            continue
        filas.append(dict(zip(cabecera, campos)))
    return p, filas

def t22_firmas():
    p, filas = _t22_tabla()
    if p is None:
        fail("T22", "no existe `forense/firmas-pendientes.tsv` -- A.12 "
                     "(`instrucciones-proyecto-v2_9.md`) lo exige")
        return

    # (a) WARN por cada fila ABIERTA, con antigüedad -- la memoria mecánica.
    hoy = datetime.date.today()
    for f in filas:
        if f.get("estado") != "ABIERTA":
            continue
        edad_txt = "antigüedad no derivable"
        try:
            anio, mes, dia = (int(x) for x in f.get("creado", "").split("-"))
            edad_txt = f"{(hoy - datetime.date(anio, mes, dia)).days} días"
        except (ValueError, TypeError):
            pass
        senal("T22", f"{f.get('id', '?')} ABIERTA desde {f.get('creado', '?')} "
                     f"({edad_txt}): {f.get('qué_se_firma', '')[:100]}")

    # (c) WARN por cada fila FIRMADA con `ejecutada_en` vacío -- una firma
    # de mesa no es lo mismo que una firma ejecutada, y `estado` solo
    # distinguía ABIERTA de FIRMADA (ADR-94, arreglo (a): defecto real que
    # atrapó -- FP-30 firmada, T07 siguió fallando, nació FP-41, y mesa fue
    # consultada dos veces sobre el mismo asunto).
    for f in filas:
        if f.get("estado") != "FIRMADA":
            continue
        if f.get("ejecutada_en", "").strip():
            continue
        edad_txt = "antigüedad no derivable"
        try:
            anio, mes, dia = (int(x) for x in f.get("creado", "").split("-"))
            edad_txt = f"{(hoy - datetime.date(anio, mes, dia)).days} días"
        except (ValueError, TypeError):
            pass
        senal("T22", f"{f.get('id', '?')} FIRMADA sin ejecutar desde {f.get('creado', '?')} "
                     f"({edad_txt}): {f.get('qué_se_firma', '')[:100]}")

    # (b) auto-protección: archivo nuevo de canon/forense con marcador de
    # ranura o de pendiente-de-mesa, sin fila que lo cite en `dónde`.
    # Acotado a filas ABIERTA/FIRMADA -- ACTO REPARA-T22, 21/ago/2026.
    # Antes, cualquier fila (incluida CERRADA) exentaba el archivo entero
    # para siempre; una fila ya cerrada no puede blindar contra un
    # pendiente nuevo que el mismo archivo traiga después. Medido antes de
    # commitear: 21 archivos dejan de estar exentos, 3 FAIL nuevos (dentro
    # del límite de 3 acordado con mesa) -- ver nota del acto.
    citados = set()
    for f in filas:
        if f.get("estado") not in ("ABIERTA", "FIRMADA"):
            continue
        for m in re.finditer(r"[\w./-]+\.(?:md|tsv|yaml|json)", f.get("dónde", "")):
            citados.add(os.path.basename(m.group(0)))

    archivos = (glob.glob(os.path.join(ROOT, "canon", "*.md")) +
                glob.glob(os.path.join(ROOT, "forense", "**", "*.md"), recursive=True) +
                glob.glob(os.path.join(ROOT, "forense", "**", "*.tsv"), recursive=True))
    for a in sorted(set(archivos)):
        r = rel(a)
        if r in _T22_ARCHIVOS_CONOCIDOS:
            continue
        s = read(a)
        if not (_T22_MARCADOR_RANURA.search(s) or _T22_MARCADOR_PENDIENTE.search(s)):
            continue
        if os.path.basename(a) in citados:
            continue
        fail("T22", f"{r} trae un marcador de ranura/pendiente-de-mesa nuevo y "
                     f"ninguna fila de `forense/firmas-pendientes.tsv` lo cita -- "
                     f"añade la fila (A.12), o explica la exclusión en la nota del acto "
                     f"y súmalo a `_T22_ARCHIVOS_CONOCIDOS`")


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
# Deriva de fecha, corregida por ACTO T22-DERIVA (ADR-88, 17/ago/2026).
# T22 incrusta la ANTIGÜEDAD de la fila en su propio mensaje (`(3 días)`), y
# esa cifra cambia sola cada medianoche: la misma fila `ABIERTA`, sobre el
# mismo árbol, sin un byte de diferencia, produce una clave distinta cada
# día. Consecuencia medida y no concebida: la corrida de CI sobre `f3873c2`
# fue SUCCESS el 14/ago/2026 (run 31772585548) y ese mismo commit da exit 1
# el 17/ago -- y las tres PR abiertas ese día (A10-ESTAMPA, BARRIDO-2,
# E-HIG) estaban rojas por lo mismo. Recongelar sin esto compra un solo día:
# a la mañana siguiente las 19 claves vuelven a no coincidir.
#
# El remedio es de la CLAVE, no del mensaje, y la distinción es el punto:
# el WARN sigue imprimiendo los días en cada corrida -- ésa es justamente la
# función que `A.12` le encarga, gritar la antigüedad hasta que alguien la
# atienda --, y solo la clave que decide "¿es esto una regresión NUEVA?"
# los ignora. Una fila `ABIERTA` que envejece no es un hallazgo nuevo; una
# fila `ABIERTA` que aparece, sí, y su `id` y su fecha `creado` -- ambos
# estables -- la siguen distinguiendo.
_T22_EDAD_VARIABLE = re.compile(r"\(\d+ días\)")

# Segundo punto ciego de la misma familia, corregido por ACTO CI-BASELINE-T16
# (ADR-90, 17/ago/2026) -- mismo género de defecto que _T22_EDAD_VARIABLE
# (arriba), esta vez del propio T16. Las dos entradas "permanentes" que T16
# emite contra `gobernanza:1106`/`:1136` (una cita histórica congelada, p.ej.
# `18 FAIL · 104 WARN`, que nunca debe seguir al real) incrustan en su
# mensaje el `real_fail`/`real_warn` VIGENTE ("...la corrida real da {N} FAIL
# · {M} WARN"). Ese sufijo es tan volátil como la antigüedad de T22 -- cambia
# cada vez que CUALQUIER test mueve su WARN, por cualquier motivo, sin que el
# archivo citado cambie un byte -- pero no estaba normalizado: `ADR-89`
# (`FP-13` -> `FIRMADA`, WARN real 131->130) lo expuso, ROJO sin regresión de
# contenido. La cita que SÍ importa (`declara {fd} FAIL · {wd} WARN vigente`,
# el valor histórico congelado) no se toca -- solo el sufijo que describe la
# corrida de hoy, que por definición nunca es parte de la identidad del
# hallazgo.
_T16_REAL_SUFIJO = re.compile(r"la corrida real da (\d+ FAIL · )?\d+ WARN")

def _baseline_key(msg):
    msg = re.sub(r":\d+ ", ": ", msg, count=1)
    msg = _T22_EDAD_VARIABLE.sub("(N días)", msg)
    return _T16_REAL_SUFIJO.sub("la corrida real da N WARN", msg)

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
        if name == "LICENSE-CORPUS.md" and "revision-publicacion-2026-07-30" in msg:
            # Refreeze tras el merge del PR #1 (30/jul/2026): la revisión de
            # publicación cita, como propuesta de su FASE 5, un artefacto que
            # su propia Nota de reconciliación declara descartado (D-05, se
            # mantuvo el LICENSE dual único). Patrón I-01 (forense/hallazgos-congelados-2026-07-30.yaml):
            # T03 no distingue mención de referencia — mismo patrón benigno
            # ya reconocido en los T03 de TRANSFER-8/9.
            return ("T03_revision-publicacion_cita_ilustrativa_de_artefacto_"
                     "descartado_D-05__patron_I-01_mismo_que_TRANSFER-8-9")
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
        if name == "v2_6.md" and "A8LAND-instrucciones" in msg:
            # ACTO A8-LAND, 13/ago/2026 (ADR-78): el encargo archivado
            # (forense/encargos/2026-08-13-A8LAND-instrucciones-v2_7.md) cita
            # "v2_6.md" sin el prefijo "instrucciones-proyecto-" tres veces,
            # verbatim -- forense/encargos/convencion.md exige archivar el
            # encargo tal como se lanzó, no editado, así que la cita corta
            # queda. El archivo real (instrucciones-proyecto-v2_6.md) existe;
            # T03 compara por nombre exacto y no lo reconoce. Mismo patrón que
            # 2026-08-12-M6-sello.md, ya congelado.
            return "T03_encargo_archivado_cita_nombre_corto_verbatim__A.3_prohibe_editar__patron_M6-sello"
        if name in {"compass-1-7edaceda.md", "compass-2-8b198c56.md", "compass-3-d72e6a97.md",
                     "red-team-A_auditoria-adversarial.md", "red_team_A_auditoria.md"}:
            # ACTO PROC-10-bis, 13/ago/2026: el encargo de MOTOR-1 (§3, archivado
            # verbatim en forense/encargos/2026-08-13-PROC-10-BIS-clase-septima-y-anexos.md
            # por A.3) exige que "el lanzador suba a la sesión" estos cinco archivos --
            # nunca llegaron. MOTOR-1 se declaró bloqueado (PARA) precisamente por su
            # ausencia; T03 la confirma, no es un defecto nuevo. Desaparece cuando
            # MOTOR-1 corra con los archivos en mano, o si alguien retira la cita.
            return "T03_encargo_MOTOR-1_cita_archivos_nunca_entregados_a_la_sesion__PROC-10-bis_declara_PARA"
        if name == "propuesta-motor-matriz-v0_2.md":
            # ACTO PROC-10-bis, 13/ago/2026: el encargo original (archivado verbatim,
            # §3 PERÍMETRO de MOTOR-1) cita "propuesta-motor-matriz-v0_2.md" -- solo
            # existe "propuesta-motor-matriz-v0_1.md" en el árbol. Error del encargo tal
            # como se lanzó (A.3 prohíbe editarlo), repetido una vez más en la nota propia
            # al citarlo para explicar el hallazgo. No se corrige ninguna de las dos citas.
            return "T03_encargo_verbatim_cita_v0_2_inexistente__solo_existe_v0_1__error_del_encargo_PROC-10-bis"
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
        elif t == "T16":
            if "gobernanza-v1_15.md:1104" in m or "gobernanza-v1_15.md:1134" in m:
                # ACTO A8-LAND, 13/ago/2026 (ADR-78): gobernanza:1104 (ADR-76(f))
                # y gobernanza:1134 (ADR-77, su propia Cascada -- corrida en
                # :1132 al sellarse; el número de línea se movió por edits
                # ajenos entre entonces y este refreeze, el texto no) declaran
                # "104 WARN", exacto contra su propia base al sellarse --
                # correctos como historia, no como estado vigente. Consecuencia
                # aritmética del T03 de este mismo refreeze (el encargo
                # archivado sube el WARN real de 104 a 107), no un defecto de
                # ninguno de los dos ADR. T16 no distingue "lo que ese ADR
                # midió" de "lo que es vigente hoy" -- limite documentado en
                # su propio docstring (_CAMBIO_FECHADO solo reconoce blockquote
                # de changelog). Editarlas falsearía el registro de dos
                # decisiones ya selladas.
                buckets["T16_cifra_historica_de_ADR_ya_sellado__consecuencia_aritmetica_"
                        "del_T03_de_A8LAND__no_defecto_de_ese_ADR__ver_ADR-78"] += 1
            elif ("gobernanza-v1_15.md:764" in m or "gobernanza-v1_15.md:856" in m or
                  "estado-programa-v1_10.md:129" in m or "estado-programa-v1_10.md:221" in m):
                # ACTO PROC-10-bis, 13/ago/2026: estas cuatro citas declaran "107
                # WARN" (o "18 FAIL · 107 WARN"), exacto contra su propia base al
                # escribirse (ACTO A8-LAND ya había subido 104 a 107) -- correctas
                # como historia. Consecuencia aritmética de este mismo refreeze: el
                # encargo de MOTOR-1 archivado por A.3 (forense/encargos/2026-08-13-
                # PROC-10-BIS-clase-septima-y-anexos.md) cita cinco archivos nunca
                # entregados a la sesión más un "v0_2" inexistente, subiendo el WARN
                # real de 107 a 119 -- ver forense/notas/2026-08-13-proc-10-bis.md
                # §4. No es un defecto de ninguna de las cuatro citas ni del propio
                # encargo archivado (A.3 prohíbe editarlo).
                buckets["T16_cifra_historica_declarada_107_WARN__consecuencia_aritmetica_"
                        "del_T03_de_PROC-10-bis__no_defecto_independiente"] += 1
            else:
                # Los T16 del refreeze del 30/jul/2026 son consecuencia aritmética
                # del T03 de revision-publicacion (3 citas ilustrativas suben el
                # total de WARN y desfasan la declaración de estado), no defectos
                # independientes: desaparecen cuando A1 resuelva I-01.
                buckets["T16_consecuencia_aritmetica_del_T03_de_revision-publicacion"
                        "__no_defecto_independiente__desaparece_cuando_A1_resuelva_I-01"] += 1
        else:
            buckets[f"{t}_FAIL_no_re-analizado_en_P1__ver_censo-integridad_para_detalle"] += 1
    return {
        "principio": ("Congelar no es aceptar. La cifra congelada mezcla deuda real del "
                      "corpus con ruido de medición conocido del propio T03 (cobertura "
                      "angosta); ver forense/censo-integridad-v1_1.md §1 para la derivación "
                      "completa de cada bucket. Bajada de 89 a 83 WARN el 29/jul/2026 "
                      "(sesión de correcciones, ver mensaje de commit) sin tocar ningún FAIL. "
                      "Re-congelada el 30/jul/2026 tras el merge del PR #1 (main 22a7d9d): "
                      "3 entradas nuevas, cada una con bucket propio — 1 T03 (cita "
                      "ilustrativa de LICENSE-CORPUS, artefacto propuesto y descartado por "
                      "D-05, patrón I-01) y 2 T16 que son su consecuencia aritmética. "
                      "Re-congelada el 13/ago/2026, ACTO A8-LAND (ADR-78), autorizado "
                      "explícitamente por mesa en el hilo de la sesión tras que el ejecutor "
                      "reportara los hallazgos y preguntara si congelar — mismo mecanismo de "
                      "autorización que ya usó ENCARGO ADR-PROVISIONALIDAD §9 (PR #199): 3 "
                      "entradas nuevas — 1 T03 (forense/encargos/2026-08-13-A8LAND-"
                      "instrucciones-v2_7.md cita \"v2_6.md\" sin prefijo, verbatim, tres "
                      "veces, patrón M6-sello) y 2 T16 (gobernanza:1104/ADR-76(f) y "
                      "gobernanza:1132/ADR-77, cada uno correcto contra lo que su propio ADR "
                      "midió al sellarse, consecuencia aritmética del T03 de este mismo "
                      "refreeze — ninguno de los dos ADR está mal, el WARN real se movió "
                      "después de que ambos sellaran). "
                      "Re-congelada el 13/ago/2026, ACTO PROC-10-bis (ADR-79(a)), autorizado "
                      "explícitamente por el usuario en la sesión ('pull and solve CI', tras "
                      "reportarle el fallo de CI de PR #227 y el hallazgo verificado) — mismo "
                      "mecanismo de autorización que ya usó ACTO A8-LAND. Corrige la causa raíz "
                      "declarada por PROC-10-bis (T19b/T19c contaban solo `MEDIDO·PARCIAL`, no "
                      "reconocían la séptima clase `MEDIDO·NACIONAL` que ese acto selló — "
                      "corregido en ambas regex, `tests/check.py` líneas ~918/~1001) y congela "
                      "el residuo esperado: 7 T03 (los cinco archivos de MOTOR-1 nunca "
                      "entregados a la sesión, más dos citas del propio encargo verbatim a "
                      "`propuesta-motor-matriz-v0_2.md`, que no existe — solo `v0_1` — error "
                      "del encargo original, no de este acto) y 6 T16 (cuatro citas históricas "
                      "de \"107 WARN\"/\"18 FAIL · 107 WARN\" en gobernanza:764,856 y "
                      "estado-programa:129,221, correctas cuando se escribieron, más las dos ya "
                      "clasificadas de A8-LAND cuyo número de línea real se corrió de :1132 a "
                      ":1134 por edits ajenos entre sesiones — consecuencia aritmética de subir "
                      "el WARN real, ninguna cita está mal). Detalle completo: "
                      "forense/notas/2026-08-13-proc-10-bis.md §4. "
                      "Re-congelada el 17/ago/2026, ACTO T22-DERIVA (ADR-88), autorizada por "
                      "mesa en la sesión mediante pregunta estructurada que citó ADR-76(f) "
                      "verbatim y describió qué cambia y qué no con cada opción — mismo "
                      "mecanismo de autorización que ya usó ADR-86, y misma honestidad de "
                      "procedencia: no es cita verbatim de texto libre. Este recongelado NO "
                      "absorbe deuda nueva del corpus: reescribe las 19 claves de T22 bajo la "
                      "normalización nueva de `_baseline_key`, que deja de meter la antigüedad "
                      "variable ('(N días)') en la clave. Sin esa corrección el recongelado "
                      "duraba un solo día — probado contra el propio CI, no supuesto: el run "
                      "31772585548 sobre f3873c2 fue SUCCESS el 14/ago y ese mismo commit da "
                      "exit 1 el 17/ago. La suite cruda no se mueve y T22 sigue emitiendo sus "
                      "19 WARN en cada corrida: cambia qué cuenta como regresión nueva, no qué "
                      "reporta la suite. Detalle completo: "
                      "forense/notas/2026-08-17-t22-deriva.md."),
        "fecha_de_clasificacion": "2026-08-17",
        "conteo_por_bucket": dict(sorted(buckets.items())),
    }

def _freeze_baseline():
    import json
    data = {
        "head": _git_head(),
        "fails": sorted({(t, _baseline_key(m)) for t, m in FAILS} - set(SENAL)),
        "warns": sorted({(t, _baseline_key(m)) for t, m in WARNS} - set(SENAL)),
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
    current = ({(t, _baseline_key(m)) for t, m in FAILS} |
               {(t, _baseline_key(m)) for t, m in WARNS}) - set(SENAL)
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


# ───────────────────────────────────────────────────────────────
# T21 · Biyección capa2 ↔ capa3 en relaciones.tsv
# ───────────────────────────────────────────────────────────────

# La correspondencia que el registro cumple sin una sola excepción desde que
# CAPA3-RECONCILIA (PR #202) la reparó — 19 desacuerdos → 0. No es cosmética:
# `capa3_disco_real` afirma el estado del payload EN DISCO, así que una fila
# `SI`|`SI_O_PARCIAL` dice a la vez "verificado íntegro" y "quizá parcial".
# Nadie vigilaba esto: hasta este test, `grep -c "capa2\|capa3" tests/check.py`
# daba 0, y por eso el defecto de `via_capa2.py --escribe` (que escribía capa2
# y dejaba capa3 atrás) pudo vivir callado hasta que ENLACE-2 lo midió con 8
# filas rotas en un solo comando (PR 236).
CAPA2_CAPA3 = {
    "SI":                "EXISTE;COINCIDE;INTEGRO",
    "SI_O_REFERENCIADO": "SI_O_PARCIAL",
    "NO_REFERENCIADO":   "NO_REFERENCIADO",
}

def t21_capa2_capa3():
    """Cada fila de `relaciones.tsv` debe llevar el `capa3_disco_real` que su
    `capa2_manifiesto` exige. Un valor de capa2 fuera de la correspondencia no
    es un fallo — es un aviso para que quien lo introduzca declare aquí qué
    capa3 le toca."""
    p = os.path.join(ROOT, "data", "curacion-registro", "relaciones.tsv")
    if not os.path.exists(p):
        fail("T21", "no se pudo leer `data/curacion-registro/relaciones.tsv`")
        return
    lineas = read(p).split("\n")
    cab = lineas[0].split("\t")
    if "capa2_manifiesto" not in cab or "capa3_disco_real" not in cab:
        fail("T21", "relaciones.tsv no trae capa2_manifiesto y/o capa3_disco_real")
        return
    i2, i3 = cab.index("capa2_manifiesto"), cab.index("capa3_disco_real")
    desacuerdos, desconocidos = {}, {}
    for n, l in enumerate(lineas[1:], 2):
        if not l.strip():
            continue
        c = l.split("\t")
        if len(c) <= max(i2, i3):
            continue
        esperado = CAPA2_CAPA3.get(c[i2])
        if esperado is None:
            desconocidos.setdefault(c[i2], []).append(n)
        elif c[i3] != esperado:
            desacuerdos.setdefault((c[i2], c[i3]), []).append(n)
    for (c2, c3), filas in sorted(desacuerdos.items()):
        fail("T21", f"relaciones.tsv: {len(filas)} fila(s) con capa2={c2} y capa3={c3}; "
                    f"capa2={c2} exige capa3={CAPA2_CAPA3[c2]} "
                    f"(primera en la línea {filas[0]})")
    for c2, filas in sorted(desconocidos.items()):
        warn("T21", f"relaciones.tsv: capa2={c2} no está en la correspondencia que declara "
                    f"este test ({len(filas)} fila(s), primera en la línea {filas[0]}) -- "
                    f"si es un valor nuevo legítimo, añádelo a CAPA2_CAPA3 con su capa3")


# ───────────────────────────────────────────────────────────────
# T23 · T-CABLEADO -- nace inactivo, activado por --require-cableado
#
# Espec única: `forense/notas/2026-08-17-b2-derivaciones-c4.md` §4, que a su
# vez deriva del encargo madre §21/§22. ACTO T23-INTEGRADOR-CABLEADO,
# 18/ago/2026 (ADR-98). `T-CABLEADO` no conoce los 20 IDs históricos, ni
# denominadores, ni cuotas -- la validación es fila por fila.
#
# Sin `--require-cableado` y sin `data/cableado-universo-v1_0.tsv`: T23 no
# emite nada (ni FAIL ni WARN) -- el producto no existe todavía (C6, sin
# empezar). Con `--require-cableado` y sin producto: FAIL, únicamente por
# archivo inexistente. Con producto presente (con o sin la bandera): las 19
# condiciones rigen siempre.
#
# Rutas fijadas por este acto (§4: "no tienen ruta fijada en ningún sitio" es
# el defecto que desbloquea dos de las 19 condiciones) bajo
# `data/curacion-registro/ejecucion-semantica/barrido2/`, versionadas (§24
# «Versionable»: propuestas depuradas, decisiones, cableado).
# ───────────────────────────────────────────────────────────────
CABLEADO_CABECERA = [
    "payload_id", "representacion_id", "sha256_12", "sha256", "fuente_canonica",
    "objeto_logico_id", "necesidad_id", "reactivo_id", "texto_reactivo_recortado",
    "grado_inspeccion", "afirmacion_tipo", "veredicto_a4", "evidencia",
    "frontera_inspeccion", "reporte_neutral_ref", "propuesta_id", "relacion_id",
    "semrun_id", "requiere_decision_mesa", "decision_mesa_id", "dependencia_fp24",
    "razon_gate", "estado_integracion", "cegamiento_roto", "fecha", "razon",
]
_T23_TEXTO_160 = {"texto_reactivo_recortado", "razon_gate", "evidencia", "frontera_inspeccion", "razon"}
_T23_SENTINELS = {"", "NO-APLICA", "NO-DETERMINADO", "[REDACTADO-PRIVACIDAD]"}
_T23_NO_INTEGRADA_TERMINAL_OK = {"INTEGRADA", "NO_APLICA_TERMINAL"}


def _t23_leer_tsv(path):
    """None si el archivo no existe -- distinto de [], que es 'existe y está vacío'."""
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _t23_fila(n, row, ctx):
    """Devuelve lista de mensajes FAIL para una fila de cableado. `n` es el
    número de línea (2-based, la 1 es cabecera)."""
    problemas = []
    def f(msg):
        problemas.append(f"cableado-universo:{n} {msg}")

    payload_id = row.get("payload_id", "")
    representacion_id = row.get("representacion_id", "")
    sha = row.get("sha256", "")
    sha12 = row.get("sha256_12", "")
    veredicto = row.get("veredicto_a4", "")
    evidencia = row.get("evidencia", "")
    frontera = row.get("frontera_inspeccion", "")
    reporte_ref = row.get("reporte_neutral_ref", "")
    relacion_id = row.get("relacion_id", "")
    propuesta_id = row.get("propuesta_id", "")
    estado_integracion = row.get("estado_integracion", "")
    grado = row.get("grado_inspeccion", "")
    requiere_mesa = row.get("requiere_decision_mesa", "")
    decision_mesa = row.get("decision_mesa_id", "")
    fp24 = row.get("dependencia_fp24", "")

    # 3 · payload_id ausente
    if not payload_id:
        f("payload_id ausente")
    # 4 · representacion_id ausente
    if not representacion_id:
        f("representacion_id ausente")
    # 5 · SHA inválido
    if not re.fullmatch(r"[0-9a-f]{64}", sha or ""):
        f(f"sha256 inválido ({sha!r})")
    # 6 · sha256_12 incorrecto
    elif sha12 != sha[:12]:
        f(f"sha256_12 ({sha12!r}) no es prefijo de sha256")
    # 7 · celda vacía (resto de las 26, payload_id/representacion_id ya cubiertas arriba)
    for col in CABLEADO_CABECERA:
        if col in ("payload_id", "representacion_id"):
            continue
        if row.get(col, "") == "":
            f(f"celda vacía en `{col}`")
    # 8 · texto >160 (solo las 5 columnas de texto durable)
    for col in _T23_TEXTO_160:
        valor = row.get(col, "")
        if len(valor) > 160:
            f(f"`{col}` excede 160 caracteres ({len(valor)})")
    # 9 · evidencia requerida ausente
    if veredicto in ("EXISTE-SATISFACE", "EXISTE-NO-SATISFACE") and evidencia in _T23_SENTINELS:
        f(f"veredicto_a4={veredicto} exige evidencia real, trae {evidencia!r}")
    # 10 · reporte neutral no dereferenciable -- límite declarado (§4): el
    # índice E2 privado no vive en un clon limpio; se exige forma
    # dereferenciable (`id:sha256`), no resolución contra el índice.
    if reporte_ref not in _T23_SENTINELS and not re.fullmatch(r"[^:\s]+:[0-9a-f]{64}", reporte_ref):
        f(f"reporte_neutral_ref no tiene forma dereferenciable ({reporte_ref!r})")
    # 11 · negativo sin frontera
    if veredicto == "EXISTE-NO-SATISFACE" and frontera in _T23_SENTINELS:
        f("veredicto_a4=EXISTE-NO-SATISFACE sin frontera_inspeccion declarada")
    # 12 · SIN-DEMANDA-CONFIRMADO sin E2 -- no tiene columna propia (§4);
    # búsqueda de token en la fila, a mano.
    if any("SIN-DEMANDA-CONFIRMADO" in (row.get(col, "") or "") for col in CABLEADO_CABECERA) and grado != "E2":
        f("SIN-DEMANDA-CONFIRMADO exige E2 completo (grado_inspeccion=E2)")
    # 13 · INTEGRADA con relacion_id inexistente
    if estado_integracion == "INTEGRADA" and relacion_id not in ctx["relaciones"]:
        f(f"INTEGRADA cita relacion_id inexistente en relaciones.tsv ({relacion_id!r})")
    # 14 · INTEGRADA sin decisión verificable de integrate.py
    if estado_integracion == "INTEGRADA":
        decision = ctx["decisiones"].get(propuesta_id) if ctx["decisiones"] is not None else None
        if decision is None:
            f(f"INTEGRADA sin decisión verificable en decisiones-integracion-barrido2.tsv (propuesta_id={propuesta_id!r})")
        elif decision.get("estado_integracion") != "INTEGRADA":
            f(f"INTEGRADA en el cableado pero decisiones-integracion-barrido2.tsv dice "
              f"{decision.get('estado_integracion')!r} para {propuesta_id!r}")
    # 15 · propuesta/reporte/tarea sin join
    if propuesta_id not in _T23_SENTINELS:
        propuesta = ctx["propuestas"].get(propuesta_id) if ctx["propuestas"] is not None else None
        if propuesta is None:
            f(f"propuesta_id sin fila en propuestas-barrido2.tsv ({propuesta_id!r})")
        elif ctx["tareas"] is None or propuesta.get("tarea_id") not in ctx["tareas"]:
            f(f"propuesta {propuesta_id!r} sin join a tarea semántica verificable")
    # 16 · físico no declarado con payload_id inventado
    if payload_id not in _T23_SENTINELS and payload_id not in ctx["payload_ids"]:
        f(f"payload_id {payload_id!r} no corresponde a ningún payload conocido -- inventado")
    # 17 · inconsistencia entre requiere_decision_mesa, decision_mesa_id y dependencia_fp24
    if fp24 == "SI" and (requiere_mesa != "SI" or decision_mesa != "FP-24"):
        f(f"dependencia_fp24=SI exige requiere_decision_mesa=SI y decision_mesa_id=FP-24, "
          f"trae {requiere_mesa!r}/{decision_mesa!r}")
    if fp24 == "NO" and (requiere_mesa != "NO" or decision_mesa != "NO-APLICA"):
        f(f"dependencia_fp24=NO exige requiere_decision_mesa=NO y decision_mesa_id=NO-APLICA, "
          f"trae {requiere_mesa!r}/{decision_mesa!r}")
    # 18 · dependencia_fp24=SI e INTEGRADA mientras FP-24 esté abierta -- este
    # acto no adjudica FP-24 caso por caso (fuera de perímetro, ADR-93/ADR-95);
    # la regla fail-closed es incondicional, igual que el schema congelado.
    if fp24 == "SI" and estado_integracion == "INTEGRADA":
        f("dependencia_fp24=SI no puede quedar INTEGRADA mientras FP-24 esté abierta")
    return problemas


def t23_cableado():
    cableado_path = os.path.join(ROOT, "data", "cableado-universo-v1_0.tsv")
    rows = _t23_leer_tsv(cableado_path)
    if rows is None:
        if REQUIRE_CABLEADO:
            fail("T23", "`data/cableado-universo-v1_0.tsv` no existe bajo --require-cableado")
        return  # T-CABLEADO normal queda inactivo antes de existir el producto (§22)
    if not rows:
        fail("T23", "`data/cableado-universo-v1_0.tsv` trae solo cabecera, cero filas")
        return

    relaciones = {r["relacion_id"] for r in (_t23_leer_tsv(os.path.join(ROOT, "data/curacion-registro/relaciones.tsv")) or [])}
    b2 = os.path.join(ROOT, "data/curacion-registro/ejecucion-semantica/barrido2")
    propuestas_rows = _t23_leer_tsv(os.path.join(b2, "propuestas-barrido2.tsv"))
    tareas_rows = _t23_leer_tsv(os.path.join(b2, "tareas-semanticas-barrido2.tsv"))
    decisiones_rows = _t23_leer_tsv(os.path.join(b2, "decisiones-integracion-barrido2.tsv"))
    ctx = {
        "relaciones": relaciones,
        "propuestas": ({r["propuesta_id"]: r for r in propuestas_rows} if propuestas_rows is not None else None),
        "tareas": ({r["tarea_id"] for r in tareas_rows}) if tareas_rows is not None else None,
        "decisiones": ({r["propuesta_id"]: r for r in decisiones_rows}) if decisiones_rows is not None else None,
        "payload_ids": ({r.get("payload_id", "") for r in tareas_rows}) if tareas_rows is not None else set(),
    }

    conteos = Counter()
    for n, row in enumerate(rows, 2):
        for msg in _t23_fila(n, row, ctx):
            fail("T23", msg)
        conteos[row.get("estado_integracion", "")] += 1

    # WARN únicamente por conteos -- nunca por tener 0/5/20/30 FP-24 (§22).
    for estado in ("CONFLICTO_MATERIAL", "NO_DETERMINADO", "REQUIERE_DECISION_FP24"):
        if conteos[estado]:
            warn("T23", f"cableado-universo: {conteos[estado]} fila(s) en estado {estado}")
    no_integradas = sum(c for e, c in conteos.items() if e not in _T23_NO_INTEGRADA_TERMINAL_OK)
    if no_integradas:
        warn("T23", f"cableado-universo: {no_integradas} propuesta(s) no integrada(s)")

    # 19 · aperturas absorbidas -- la única de las 19 que se evalúa contra el
    # registro (relaciones.tsv/lista-apertura), no contra celdas del
    # cableado (§4). `capa3_disco_real` que empieza en EXISTE es la señal de
    # payload observado que ya vive en el registro -- no reinventa una
    # segunda fuente de verdad para "en disco".
    apertura_path = os.path.join(ROOT, "data", "lista-apertura-enlace2-2026-08-14.tsv")
    apertura_rows = _t23_leer_tsv(apertura_path)
    relaciones_completas = _t23_leer_tsv(os.path.join(ROOT, "data/curacion-registro/relaciones.tsv"))
    if apertura_rows is not None and relaciones_completas is not None:
        rel_by_id = {r["relacion_id"]: r for r in relaciones_completas}
        for r in apertura_rows:
            if r.get("destino") != "APERTURA-PENDIENTE":
                continue
            rel = rel_by_id.get(r["relacion_id"])
            if rel is None:
                continue
            if (rel.get("capa4_apertura_mapeo") == "INDEXADO-NO-DESCARGADO"
                    and rel.get("capa3_disco_real", "").startswith("EXISTE")):
                fail("T23", f"apertura absorbida {r['relacion_id']} conserva "
                            f"INDEXADO-NO-DESCARGADO con payload observado (capa3_disco_real="
                            f"{rel.get('capa3_disco_real')!r})")


# ───────────────────────────────────────────────────────────────
# T24 · T-LLAVES-EJERCIDAS — Encargo T20-LLAVES, 18/ago/2026. Cierra
#   `FP-18` (firma de mesa `ADR-91`, `PR #246`): instrumenta el vigía
#   sobre la población "llaves de identificación ejercidas" que
#   `ADR-67(c)` abrió (`gobernanza:868`) -- distinta del denominador 27
#   de Hito D, distinta de `9 de 14`, distinta de `15 coeficientes, cero
#   medidos`.
#
#   El vigía OBSERVA el contador, no lo mueve (mismo límite que el
#   propio encargo declara): deriva la cifra con la receta congelada de
#   `forense/registro-llaves-identificacion-v*.md` §4 -- acota el conteo
#   a `## 3 · Tabla de llaves`, extrae la columna `estado` (sexta tras
#   dividir por `|`) de cada fila de datos, cuenta las que empiezan con
#   `EJERCIDA_` -- y la cruza contra la cita vigente de
#   `canon/estado-programa-v*.md` ("Llaves de identificación ejercidas:
#   `N` de `M`."). Mismo defecto de cascada que T19b/T19c ya vigilan
#   para sus propios contadores: una cifra que se desincroniza de su
#   fuente sin que ninguna corrida lo note.
#
#   Hoy el registro trae `1` de `2` (ACTO ADJ-4, 13/ago/2026) y
#   `estado-programa:99` ya cita esa misma cifra -- este marcador nace
#   en verde, no dispara sobre estado no-regresivo, y por eso no exige
#   `SENAL` (precedente `ADR-96`/`ADR-101(c)`/`FP-51`): no hay disparo
#   que declarar.
# ───────────────────────────────────────────────────────────────
def t24_llaves_ejercidas():
    r = newest("forense/registro-llaves-identificacion-v*.md")
    if not r:
        fail("T24", "no se pudo leer `forense/registro-llaves-identificacion-v*.md`")
        return
    texto = read(r)
    m = re.search(r"^## 3 · Tabla de llaves\n(.*?)(?=^## )", texto, re.S | re.M)
    if not m:
        fail("T24", f"{rel(r)}: no se encontró la sección `## 3 · Tabla de llaves`")
        return
    filas = [l for l in m.group(1).split("\n") if l.startswith("| `")]
    if not filas:
        fail("T24", f"{rel(r)}: `## 3 · Tabla de llaves` no trae filas de datos")
        return

    # `ADQ-ENOE-PRE2019` T3 (`ADR-144`): el indice 5 estaba tecleado aqui, y la
    # receta congelada de §4 del registro lo tiene tecleado tambien (`awk
    # -F'|' '{print $6}'`). Las dos se mueven juntas si alguien altera las
    # columnas de la tabla, y ninguna se queja. Medido sobre la tabla real al
    # escribir esto: el indice 6 (`veredicto`) contiene `EJERCIDA_` en 2 de 3
    # filas, exactamente igual que `estado` -- asi que QUITAR una columna
    # antes de `estado` desplaza `veredicto` al indice 5 y el vigia sigue
    # derivando `2 de 3`, **en verde, contando la columna equivocada**.
    # Insertar una columna da el modo benigno (falla, pero culpando a
    # `estado-programa` de una discrepancia que no es suya). Se deriva la
    # posicion del encabezado y se cruza contra la que la receta congela: si
    # divergen, hay que reescribir §4, y esto lo dice en vez de contar mal.
    POS_RECETA = 5
    cab = next((l for l in m.group(1).split("\n")
                if l.startswith("| llave_id")), None)
    if cab is None:
        fail("T24", f"{rel(r)}: `## 3 · Tabla de llaves` no trae encabezado "
                     f"`| llave_id | …`")
        return
    campos = [c.strip() for c in cab.split("|")]
    if "estado" not in campos:
        fail("T24", f"{rel(r)}: el encabezado de `## 3 · Tabla de llaves` no "
                     f"declara una columna `estado`: {campos}")
        return
    pos = campos.index("estado")
    if pos != POS_RECETA:
        fail("T24", f"{rel(r)}: la columna `estado` esta en la posicion {pos} "
                     f"del encabezado, pero la receta congelada de §4 lee la "
                     f"{POS_RECETA} (`awk -F'|' '{{print ${POS_RECETA+1}}}'`). "
                     f"Se {'insertó' if pos > POS_RECETA else 'quitó'} "
                     f"{abs(pos - POS_RECETA)} columna(s) antes de `estado`: "
                     f"reescribe §4 del registro y esta constante en el mismo "
                     f"acto, o el conteo sale de la columna equivocada")
        return
    anchos = {len(l.split("|")) for l in filas}
    if len(anchos) != 1:
        fail("T24", f"{rel(r)}: las filas de `## 3 · Tabla de llaves` no tienen "
                     f"el mismo número de columnas ({sorted(anchos)}) — alguna "
                     f"fila trae un `|` sin escapar y la columna `estado` no "
                     f"cae en el mismo sitio en todas")
        return
    estados = [l.split("|")[pos].strip() for l in filas]
    ejercidas = sum(1 for e in estados if "EJERCIDA_" in e)
    total = len(filas)

    e = newest("canon/estado-programa-v*.md")
    if not e:
        fail("T24", "no se pudo leer `canon/estado-programa-v*.md`")
        return
    dm = re.search(r"Llaves de identificaci[oó]n ejercidas:\s*`(\d+)`\s*de\s*`(\d+)`", read(e))
    if not dm:
        fail("T24", f"{rel(e)}: no se encontró la cita 'Llaves de identificación "
                     f"ejercidas: `N` de `M`.'")
        return
    declarado_num, declarado_den = int(dm.group(1)), int(dm.group(2))
    if (declarado_num, declarado_den) != (ejercidas, total):
        fail("T24", f"{rel(e)} declara {declarado_num} de {declarado_den} llaves "
                     f"ejercidas; {rel(r)} (receta §4) deriva {ejercidas} de {total}")


# ───────────────────────────────────────────────────────────────
# T25 · T-ROTULOS — D-6 (`ADR-128`, `ACTO SELLA-ADV`, 20/ago/2026):
#   lo que ya está en uso se registra (`canon/registro-rotulos.tsv`), no se
#   renombra; ningún rótulo NUEVO puede ser letra+número pelado desde hoy.
#   Motivado por la colisión medida el mismo día: `M5` con cuatro
#   habitantes distintos (`forense/RONDA-M-...:61`, `forense/hallazgos.md:65`,
#   `ADR-100`, y desde hoy `ADV1-M5`) y siete rótulos `E<n>` distintos en el
#   rango `E0`-`E5`, uno de ellos citado por nombre en la fila `FP-26`
#   (`ABIERTA`) del tablero.
#
#   FAIL si un archivo `.md` NUEVO de `canon/` o `forense/` trae un rótulo
#   pelado de las dos familias que colisionan hoy — `M<n>` o `E<n>`/`E-<n>`
#   sin prefijo de espacio delante (p.ej. `ADV1-M5`, no `M5` a secas) — y
#   ese archivo no está en el snapshot conocido de abajo.
#
#   LÍMITE DECLARADO — léelo antes de tocar este test, mismo patrón que
#   T22(b). (1) Granularidad de ARCHIVO, no de rótulo ni de línea: protege
#   contra la clase de defecto real — un documento NUEVO que inventa o
#   repite `M<n>`/`E<n>` pelado sin que nadie lo registre —, no contra cada
#   mención nueva dentro de un archivo ya vigilado. (2) Solo cubre las DOS
#   familias medidas colisionando hoy (`M`, `E`); no intenta detectar
#   cualquier espacio de rótulo que alguien pueda inventar a futuro
#   (`K3`, `P7`, …) — un regex general para "cualquier letra+número nuevo"
#   se ahoga en falsos positivos de prosa (149 de los ~380 `.md` de
#   `canon/`+`forense/` ya usan `M`/`E`+dígito de forma legítima; extender
#   el patrón a todo el alfabeto multiplicaría ese ruido sin acotar nada
#   nuevo). `canon/registro-rotulos.tsv` documenta el censo humano de las
#   dos colisiones reales; este test es la mitad mecánica, no todo D-6.
#   Falsador y caducidad: mismo criterio que A.3/A.8/A.9/A.10/A.12 — si en
#   tres meses `T-ROTULOS` nunca dispara y ninguna colisión nueva se evita,
#   se retira y se anota.
# ───────────────────────────────────────────────────────────────
_T25_ROTULO_BARE = re.compile(r"(?<![A-Za-z0-9_-])(M|E)-?(\d{1,2})(?![A-Za-z0-9_.])")

# Snapshot verificado por `python3 -c` sobre `canon/**/*.md` + `forense/**/*.md`
# al sellar T25 — `ACTO SELLA-ADV`, 20/ago/2026, contra `5a60e98` + lo que
# el propio acto escribió (T1/T4/T6). Cada archivo de esta lista ya trae
# `M<n>` o `E<n>` pelado hoy, de forma ya conocida (censada en
# `canon/registro-rotulos.tsv` para los casos que colisionan de verdad).
# Un archivo NUEVO que no esté aquí y traiga el patrón es exactamente el
# defecto que este test existe para atrapar.
_T25_ARCHIVOS_CONOCIDOS = {
    # ACTO MAESTRA31-E2 · REGISTRA-PENDIENTES, 26/ago/2026: encargo
    # archivado VERBATIM (A.3). Direccion lo lanzo rotulado "ENCARGO E2",
    # y "E2" pelado colisiona con el habitante ya censado del espacio E
    # (pipeline de barrido semantico, FP-65). D-6 aplicado donde se puede
    # aplicar: el acto se declara ACTO MAESTRA31-E2 en todo archivo que
    # escribe y queda censado en canon/registro-rotulos.tsv; el encargo
    # NO se edita, porque A.3 pide el texto de direccion verbatim. Mismo
    # movimiento y misma razon que MAESTRA31-E1, E4, E5, E6, E7 y
    # MAESTRA30-E10, seis entradas de esta misma lista.
    "forense/encargos/2026-08-26-MAESTRA31-E2-REGISTRA-PENDIENTES.md",
    # forense/notas/2026-08-26-registra-pendientes-cierre.md -- nota de
    # cierre de ACTO MAESTRA31-E2 que discute tres rotulos bare (E1, E9,
    # E2) al citar habitantes ya censados del espacio E (MAESTRA31-E1,
    # el habitante E9=ACTO MAESTRA30-E9, y el habitante E2=FP-65) --
    # ninguno es un marcador nuevo. Extension minima de perimetro por
    # desviacion mecanica, mismo precedente que ADR-147(c)/ADR-149(f)/
    # ADR-151/sella-e.md/sella-f.md.
    "forense/notas/2026-08-26-registra-pendientes-cierre.md",
    # ACTO MAESTRA31-E3 · PERIMETRO-ALCANZABLE, 26/ago/2026 (ADR-212,
    # renumerado desde ADR-211 al resolver PR #384 contra PR #383/
    # ACTO MAESTRA31-E2, que fusiono primero y se quedo con ADR-211):
    # encargo archivado VERBATIM (A.3) y su nota de cierre. Direccion lo
    # lanzo rotulado "ENCARGO E3", y "E3" pelado colisiona con el
    # habitante previo E3-TRIAGE y con los demas habitantes ya censados
    # del espacio E. D-6 aplicado donde se puede aplicar: el acto se
    # declara ACTO MAESTRA31-E3 en todo archivo que escribe y queda
    # censado en canon/registro-rotulos.tsv; el encargo NO se edita,
    # porque A.3 pide el texto de direccion verbatim, y la nota de
    # cierre menciona el rotulo "E3" al narrar el propio hallazgo de T25
    # sobre el encargo (misma situacion que ya cubren otras notas de
    # esta lista: la mencion de un rotulo dentro de un documento que
    # narra el hallazgo no es su uso, pero el regex no distingue, asi
    # que se censa aqui en vez de editar la narracion). El entregable
    # propio del acto, forense/perimetro-alcanzable-v1_0.md, NO necesita
    # esta lista (no trae ningun rotulo pelado, verificado por comando
    # antes de cerrar). Mismo movimiento y misma razon que E4, E5, E6,
    # E7, MAESTRA30-E10 y MAESTRA31-E1/E2, siete entradas de esta misma
    # lista.
    "forense/encargos/2026-08-26-MAESTRA31-E3-PERIMETRO-ALCANZABLE.md",
    # ACTO MAESTRA32-E3 · EXTRACTOR-DTA v2, 30/ago/2026: encargo archivado
    # VERBATIM (A.3) rotulado "ENCARGO E3" por direccion, y su nota de
    # COMMIT-1 y su nota de cierre citan el rotulo bare "E4" al nombrar
    # el sucesor declarado MAESTRA32-E4 · RE-EMPAREJA. "E3" colisiona con
    # E3-TRIAGE/MAESTRA30-E1..E4/MAESTRA31-E3 y demas habitantes del
    # espacio E; "E4" colisiona con E4 (DISENO-ENSAFI)/MAESTRA30-E1..E4.
    # D-6 aplicado donde se puede aplicar: el acto se declara ACTO
    # MAESTRA32-E3 en todo archivo que escribe y queda censado en
    # canon/registro-rotulos.tsv; el encargo NO se edita porque A.3 pide
    # el texto de direccion verbatim, y las notas de COMMIT-1/cierre
    # citan el rotulo del sucesor al narrar su propia especificacion --
    # mismo patron que las demas entradas de esta lista.
    "forense/encargos/2026-08-30-MAESTRA32-E3-EXTRACTOR-DTA-v2.md",
    "forense/notas/2026-08-30-extractor-ext-spec.md",
    "forense/notas/2026-08-30-extractor-ext-cierre.md",
    # ACTO MAESTRA32-E12 · EXTRACTOR-FD, 31/ago/2026: encargo archivado
    # VERBATIM (A.3) rotulado "ENCARGO E12" por direccion, que cita los
    # rotulos bare "E3" (cierre de la rama (a) previa, ADR-228) y "E4"
    # (sucesor declarado MAESTRA32-E4 · RE-EMPAREJA en carril nube) al
    # narrar la secuencia FP-175/FP-179. "E3" colisiona con
    # E3-TRIAGE/MAESTRA30-E1..E4/MAESTRA31-E3/MAESTRA32-E3 y demas
    # habitantes del espacio E; "E4" colisiona con E4 (DISENO-ENSAFI)/
    # MAESTRA30-E1..E4. D-6 aplicado donde se puede aplicar: el acto se
    # declara ACTO MAESTRA32-E12 en todo archivo que escribe y queda
    # censado en canon/registro-rotulos.tsv; el encargo NO se edita
    # porque A.3 pide el texto de direccion verbatim -- mismo patron que
    # las demas entradas de esta lista.
    "forense/encargos/2026-08-30-MAESTRA32-E12-EXTRACTOR-FD.md",
    "forense/notas/2026-08-26-perimetro-alcanzable-cierre.md",
    # ACTO MAESTRA31-E1 · RELOJ-CRUCE, 26/ago/2026 (ADR-210): encargo
    # archivado VERBATIM (A.3). Direccion lo lanzo rotulado "ENCARGO E1",
    # y "E1" pelado colisiona con los habitantes ya censados del espacio E.
    # D-6 aplicado donde se puede aplicar: el acto se declara ACTO
    # MAESTRA31-E1 en todo archivo que escribe y queda censado en
    # canon/registro-rotulos.tsv; el encargo NO se edita, porque A.3 pide
    # el texto de direccion verbatim. Mismo movimiento y misma razon que
    # E4, E5, E6, E7 y MAESTRA30-E10, cinco entradas de esta misma lista.
    "forense/encargos/2026-08-26-MAESTRA31-E1-RELOJ-CRUCE.md",
    # ACTO MAESTRA30-E10 · R21-ADJUDICA, 26/ago/2026 (ADR-208): encargo
    # archivado VERBATIM (A.3) y su nota de cierre. Direccion lo lanzo
    # rotulado "ENCARGO E10", y "E10" pelado colisiona con la referencia
    # previa "E10 · EL SIMULADOR" de forense/encargos/2026-08-14-ENLACE-2-
    # adjudicacion-68-y-19.md:51 -- un referente distinto, no un espacio
    # nuevo. D-6 aplicado donde se puede aplicar: el acto se declara ACTO
    # MAESTRA30-E10 en todo archivo que escribe y queda censado en
    # canon/registro-rotulos.tsv; el encargo NO se edita, porque A.3 pide
    # el texto de direccion verbatim. Mismo movimiento y misma razon que
    # E4, E5, E6 y E7, cuatro entradas de esta misma lista.
    "forense/encargos/2026-08-26-E10-R21-ADJUDICA.md",
    "forense/notas/2026-08-26-e10-r21-adjudica-cierre.md",
    # ACTO E7 · R-SCORING, 26/ago/2026 (ADR-207): encargo archivado VERBATIM
    # (A.3) y su nota de cierre. Direccion lo lanzo rotulado "ENCARGO E7", y
    # "E7" pelado colisiona con los habitantes ya censados del espacio E.
    # D-6 aplicado donde se puede aplicar: el acto se declara ACTO E7 ·
    # R-SCORING en todo archivo que escribe y queda censado en
    # canon/registro-rotulos.tsv; el encargo NO se edita, porque A.3 pide el
    # texto de direccion verbatim. Mismo movimiento y misma razon que E4, E5
    # y E6, tres entradas de esta misma lista.
    "forense/encargos/2026-08-26-E7-R-SCORING.md",
    "forense/notas/2026-08-26-r-scoring-cierre.md",
    # ACTO MAESTRA30-E9 · SCORING-V2, 26/ago/2026 (ADR-209): encargo
    # archivado VERBATIM (A.3) y su nota de cierre, mas dos documentos
    # propios (procedimiento congelado y marcador v1.1) que citan "E7" en
    # prosa al comparar el nuevo blindaje contra el de E7/v1.0. "E9" pelado
    # resulto tener DOS habitantes reales al censarlo (ver
    # canon/registro-rotulos.tsv): ICH E9(R1), guia regulatoria ya citada en
    # forense/red_team_A_auditoria.md y forense/auditoria_adversarial_
    # benchmarks.md, y este acto. D-6 aplicado donde se puede aplicar: el
    # acto se declara ACTO MAESTRA30-E9 en todo archivo que escribe; el
    # encargo NO se edita, porque A.3 pide el texto de direccion verbatim.
    # Mismo movimiento y misma razon que E3, E4, E5, E6, E7 y E10.
    "forense/encargos/2026-08-26-E9-SCORING-V2.md",
    "forense/notas/2026-08-26-e9-scoring-v2-cierre.md",
    "forense/prereg-duelo-v2/procedimiento-scoring-v1_0.md",
    "forense/prereg-duelo-v2/marcador-piloto-v1_1.md",
    # SELLA-AGO25-F (continuación), 25/ago/2026 (ADR-166): la nota cita
    # verbatim, entre comillas, la firma ya sellada de FP-46/ADR-109 ("la
    # condicion literal de ADR-93 sobre material E2") -- el "E2" pelado es
    # el rotulo del propio ACTO ENLACE-2/B2-SEMANTICO, no un espacio nuevo
    # de este acto. Cita, no declaracion.
    "forense/notas/2026-08-25-sella-f-hoja.md",
    # misma razon que la entrada de abajo: esta nota cita por nombre la fila
    # `E3-TRIAGE` del propio canon/registro-rotulos.tsv al narrar el hallazgo
    # de T25 sobre el encargo. Cita de un habitante YA censado, no declaracion
    # de uno nuevo -- el acto se declara MAESTRA30-E3 y no reclama el token
    # bare. Mismo patron exacto que forense/notas/2026-08-24-adq-corre-
    # r74r75-cierre.md, que esta en esta lista por citar "E-3" en prosa.
    "forense/notas/2026-08-26-ejerce-llave-compartamos-cierre.md",
    # MAESTRA30-E3 / EJERCE-LLAVE-COMPARTAMOS, 26/ago/2026 (ADR-203):
    # encargo archivado VERBATIM (A.3 + convencion de forense/encargos/).
    # Direccion lo lanzo rotulado "ENCARGO E3", y "E3" pelado ya tiene dos
    # habitantes censados en canon/registro-rotulos.tsv (E3-TRIAGE y el
    # Encargo E-3 de tests/svystat.py) -- este seria un tercero, que es
    # exactamente la colision que D-6 existe para evitar. Resuelto donde
    # se puede resolver: el acto se declara MAESTRA30-E3 en TODOS los
    # archivos que escribe (resultado, nota, registro de llaves, ADR-203,
    # estado-programa) y asi queda censado; el encargo archivado NO se
    # edita, porque A.3 pide el texto de direccion verbatim y el texto de
    # direccion no se edita para complacer a un test. Mismo movimiento y
    # misma razon que PREREG-CORRIDA, SELLA-AGO24-C-v2 y ADQ-CORRE-R74R75.
    # Extension minima de perimetro por desviacion mecanica, declarada en
    # la nota del acto (SS 8) -- una linea de snapshot, cero cambios de logica.
    "forense/encargos/2026-08-26-E3-EJERCE-LLAVE-COMPARTAMOS.md",
    # PREREG-CORRIDA, 26/ago/2026 (ADR-194): encargo archivado VERBATIM
    # (convencion de forense/encargos/: "el texto completo del encargo tal
    # como se lanzo"). Su `M2` pelado es ADV1-M2, ya censado en
    # canon/registro-rotulos.tsv; el texto de direccion no se edita para
    # complacer a un test. Mismo movimiento y misma razon que ACT-PIL-2/
    # SELLA-AGO24-C-v2.
    "forense/encargos/2026-08-26-PREREG-CORRIDA.md",
    # CIERRA-FP157, 26/ago/2026 (ADR-201, renumerado de ADR-200 al fusionar
    # segundo -- ADR-200 lo tomo ACTO E2-PREP-L-RUN, PR #371): encargo
    # archivado VERBATIM (convencion de forense/encargos/), y la nota de
    # cierre que lo narra. Su `E1` pelado es el rotulo del propio acto
    # (Encargo E1, dirección maestra-30), no un espacio de rotulos nuevo --
    # ya censado en canon/registro-rotulos.tsv. El texto de direccion no se
    # edita para complacer a un test.
    "forense/encargos/2026-08-26-E1-CIERRA-FP157.md",
    "forense/notas/2026-08-26-cierra-fp157-cierre.md",
    # E2-PREP-L-RUN, 26/ago/2026 (ADR-200): "E2" pelado es el nombre propio
    # del acto (ENCARGO E2 · PREP-L-RUN, tal como direccion lo lanzo), no
    # una cita al espacio ADV1-E2/ADV1-M2 de la escala del duelo -- el
    # encargo se archiva VERBATIM (convencion de forense/encargos/) y la
    # nota/lanzamiento lo citan por el mismo nombre de acto al describirlo.
    # Ningun espacio de la escala se declara de nuevo; el texto de direccion
    # no se edita para complacer a un test. Mismo movimiento que
    # SELLA-AGO25-F-HOJA/PREREG-CORRIDA.
    "forense/prereg-duelo-v2/lanzamiento-L-v1_0.md",
    "forense/notas/2026-08-26-prep-l-run-cierre.md",
    "forense/encargos/2026-08-26-E2-PREP-L-RUN.md",
    # SELLA-AGO24-C-v2, 24/ago/2026 (ADR-155): encargo archivado VERBATIM
    # (convencion de forense/encargos/: "el texto completo del encargo tal
    # como se lanzo"). Su `M5` pelado es ADV1-M5, ya censado en
    # canon/registro-rotulos.tsv; el texto de direccion no se edita para
    # complacer a un test. Mismo movimiento y misma razon que ACT-PIL-2.
    "forense/encargos/2026-08-24-SELLA-AGO24-C-v2.md",
    # ADQ-CORRE-R74R75, 24/ago/2026 (ADR-158): encargo archivado VERBATIM,
    # misma convencion. Su `E-3` pelado ("E-3 espera a este", linea ORDEN)
    # es el Encargo E-3 real del 4/ago/2026 (tests/svystat.py, PR #97,
    # forense/hallazgos.md:106/:138 -- ese archivo ya esta en esta misma
    # lista), citado por nombre, no declarado de nuevo; censado tambien en
    # canon/registro-rotulos.tsv. El texto de direccion no se edita para
    # complacer a un test.
    "forense/encargos/2026-08-24-ADQ-CORRE-R74R75.md",
    # misma razon que la entrada de arriba: esta nota cita "E-3" en prosa al
    # narrar el propio hallazgo de T25 sobre el encargo.
    "forense/notas/2026-08-24-adq-corre-r74r75-cierre.md",
    # ACTO SELLA-A1-CODI, 25/ago/2026 (ADR-177, PR #350): adjunto de mesa
    # aterrizado verbatim (ADR-151, cero ediciones). Su `§E5` pelado cita
    # por nombre el espacio real de forense/EDGE-CASES-y-literatura-
    # reciente.md §E5 (linea 39, "## E5 - Invariancia de medicion"), ya
    # existente y censado -- no declara un espacio nuevo. Mismo patron que
    # benchmark-enlace-invarianza. Extension minima de perimetro por
    # desviacion mecanica (CI del propio acto, PR #350).
    "forense/benchmark-unidad-homogenea-codi-spei-v1_0.md",
    "forense/BENCHMARK-INTERVALO-CORREDOR-M-2026-08-20.md",
    "forense/encargos/2026-08-21-emisor-m1b.md",
    "canon/APERTURA-FASE-CALCULO-v1_2.md",
    "canon/PLAN-CALCULO-TOTAL-v1_1.md",
    "canon/estado-programa-v1_10.md",
    "canon/gobernanza-v1_15.md",
    "canon/modelo-decision-v4_0.md",
    "canon/protocolo-sesion-v1_0.md",
    "forense/ADR-MOTOR-2-esqueleto-2026-08-14.md",
    "forense/adv-duelo/ADV-1_demolicion_duelo_L_vs_M.md",
    "forense/BENCHMARKS-metodologicos-D-ABC.md",
    "forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md",
    "forense/CAREO-benchmarks-4RT-archivo-proyecto.md",
    "forense/CASCADA-M1-2026-08-14.md",
    "forense/EDGE-CASES-y-literatura-reciente.md",
    "forense/RONDA-M-motor-matriz-veredicto-opus-2026-08-13-v1_0.md",
    "forense/RONDA1-motor-adaptativo-celda-adjudicacion-v1_0.md",
    "forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md",
    "forense/auditoria_adversarial_benchmarks.md",
    "forense/bbis-radio-confianza-enbiare-v1_0.md",
    "forense/benchmark-enlace-invarianza-v1_0.md",
    "forense/bitacora.md",
    "forense/adv-duelo/compass-5-d3f09137-estado-arte-duelo-2026.md",
    "forense/encargos/2026-08-05-m1-ensanut.md",
    "forense/encargos/2026-08-05-m4bis-encup-lapop-latinobarometro.md",
    "forense/encargos/2026-08-05-m5bis-cierre-inventarios-catalogo-cruce.md",
    "forense/encargos/2026-08-11-E4b.md",
    # ACT-PIL-2, 20/ago/2026: encargo archivado VERBATIM (convencion de
    # forense/encargos/: "el texto completo del encargo tal como se lanzo").
    # Sus `M1` pelados son ADV1-M1, ya censados en canon/registro-rotulos.tsv
    # filas 12-13, que fijan justo esta regla: el documento fuente queda
    # verbatim sin prefijo, es la CITA la que se prefija -- y las citas de
    # este acto (ADR-130, nota) van todas con ADV1-.
    "forense/encargos/2026-08-20-ACT-PIL-2.md",
    # TRIAGE-UNIVERSO-12, 24/ago/2026: mismo precedente que ACT-PIL-2 --
    # encargo archivado VERBATIM (convencion de forense/encargos/: "el texto
    # completo del encargo tal como se lanzo"). Su `E-0` pelado cita el acto
    # previo `ACTO E-0`/`SELLA-AGO24`, ya censado; el documento fuente queda
    # sin prefijo, la cita del propio triaje (forense/notas/2026-08-24-
    # triaje-universo-12.md) no repite el rotulo pelado.
    "forense/encargos/2026-08-24-TRIAGE-UNIVERSO-12.md",
    "forense/encargos/2026-08-12-C-universo-minimo.md",
    "forense/encargos/2026-08-12-E4a.md",
    "forense/encargos/2026-08-12-E4c-paso3-corrida.md",
    "forense/encargos/2026-08-12-M6-sello.md",
    "forense/encargos/2026-08-12-S-svystat-4celdas.md",
    "forense/encargos/2026-08-12-V-vocabulario-celda-d.md",
    "forense/encargos/2026-08-13-AI-apertura-issp.md",
    "forense/encargos/2026-08-13-FIRMAS2-carril-caja.md",
    "forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md",
    "forense/encargos/2026-08-13-PROC-10-BIS-clase-septima-y-anexos.md",
    "forense/encargos/2026-08-13-VP-verifica-puertas.md",
    "forense/encargos/2026-08-13-censo-v1_1.md",
    "forense/encargos/2026-08-13-r5-1-d3.md",
    "forense/encargos/2026-08-14-B2-mantenimiento-via-capa3.md",
    "forense/encargos/2026-08-14-ENLACE-2-adjudicacion-68-y-19.md",
    "forense/encargos/2026-08-14-MOTOR-1-consolidado.md",
    "forense/encargos/2026-08-14-MOTOR-3-E0-autocontenido.md",
    "forense/encargos/2026-08-14-RECONCILIA-SPEC-encargo.md",
    "forense/encargos/2026-08-17-B2-RELEVO-recuperar-barrido2-desde-c4.md",
    "forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md",
    "forense/encargos/2026-08-17-EDEC-fuente-unica-decisiones.md",
    "forense/encargos/2026-08-17-REGISTRA-17AGO.md",
    "forense/encargos/2026-08-18-B2-SEMANTICO-C4-C5-C6.md",
    "forense/encargos/2026-08-18-B2-V7-generacion-v7-y-tres-cifras.md",
    "forense/encargos/2026-08-18-E3-TRIAGE.md",
    "forense/encargos/2026-08-18-E5-entrada-5-registro-recalculo.md",
    "forense/encargos/2026-08-18-LANE-A-E0-E5.md",
    "forense/encargos/2026-08-18-MESA-18AGO-nueve-firmas.md",
    "forense/encargos/2026-08-18-NOTAS-P3.md",
    "forense/encargos/2026-08-20-SELLA-ADV.md",
    "forense/encargos/2026-08-20-T-SELLO.md",
    # RETRIAGE-4, 20/ago/2026: encargo archivado VERBATIM (misma convencion
    # que ACT-PIL-2 arriba). Su `E3` pelado es la cita del acto E3-TRIAGE,
    # cuyo propio encargo ya esta censado en esta misma lista.
    "forense/encargos/2026-08-20-RETRIAGE-4.md",
    # RETRIAGE-4, 20/ago/2026: la nota del acto cita E3-TRIAGE (precedente de
    # escala B-bis) y ACT-PIL-2 (precedente de censo). Mismos `E3` pelados que
    # el encargo, misma razon: es cita del acto, no rotulo nuevo.
    "forense/notas/2026-08-20-retriage-4-cierre.md",
    "forense/TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md",
    "forense/hallazgos.md",
    "forense/historico/TRANSFER-maestra-7.md",
    "forense/hitoD-R1_1-bbis-triage-v1_0.md",
    "forense/hitoD-R1_3-especificacion-v1_0.md",
    "forense/hitoD-R3_1-especificacion-v1_0.md",
    "forense/hitoD-R4_1-bbis-triage-v1_0.md",
    "forense/hitoD-R4_2-bbis-triage-v1_0.md",
    "forense/hitoD-R4_3-bbis-triage-v1_0.md",
    "forense/hitoD-R7_2-bbis-triage-v1_0.md",
    "forense/hitoD-R9_1-bbis-triage-v1_0.md",
    "forense/hitoD-R9_2-bbis-triage-v1_0.md",
    "forense/hitoD-preregistro-v2_0.md",
    "forense/hitoE-campana-medicion-v2_0.md",
    "forense/adv-duelo/informe_ADV2_estado_del_arte_y_rubrica.md",
    "forense/notas/2026-07-30-verificacion-premisas-hitoE.md",
    "forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md",
    "forense/notas/2026-08-03-cbis-deferencia-externas.md",
    "forense/notas/2026-08-04-d2-descargas-endutih-mociba-enasem.md",
    "forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md",
    "forense/notas/2026-08-04-encup-certificado-fijado.md",
    "forense/notas/2026-08-04-encup-paso1-deferencia.md",
    "forense/notas/2026-08-04-encup-paso2-deferencia.md",
    "forense/notas/2026-08-04-m1-adjudicacion-r3-1-adr-60.md",
    "forense/notas/2026-08-04-m1-adjudicacion-r3-1-paro.md",
    "forense/notas/2026-08-04-m2-adjudicacion-adr-61.md",
    "forense/notas/2026-08-04-p3-lca-segmentacion.md",
    "forense/notas/2026-08-04-svystat-casos-referencia.md",
    "forense/notas/2026-08-04-w1-p-policial.md",
    "forense/notas/2026-08-05-a5-portada-publica-falsas.md",
    "forense/notas/2026-08-05-conf17-fetch-corrida-A.md",
    "forense/notas/2026-08-05-conf17-fetch-corrida-B.md",
    "forense/notas/2026-08-05-desc1-descarga.md",
    "forense/notas/2026-08-05-e-encig-bloqueos.md",
    "forense/notas/2026-08-05-m1-ensanut-mapa.md",
    "forense/notas/2026-08-05-m2-incognitas.md",
    "forense/notas/2026-08-05-m3-lote-b3-diez-reactivos.md",
    "forense/notas/2026-08-05-m4-adjudicacion-adr-63.md",
    "forense/notas/2026-08-05-m4bis-encup-lapop-latinobarometro-bloqueo.md",
    "forense/notas/2026-08-05-m5-adr64-conf06.md",
    "forense/notas/2026-08-05-p2-cierre-documental.md",
    "forense/notas/2026-08-05-p3-r8-1-contradiccion-inventario.md",
    "forense/notas/2026-08-06-map2-cruce.md",
    "forense/notas/2026-08-08-explora2.md",
    "forense/notas/2026-08-11-e4b-sello-b-corrida-b.md",
    "forense/notas/2026-08-11-e4c-r5-1-d2-especificacion.md",
    "forense/notas/2026-08-12-acto-v-vocabulario-celda-d.md",
    "forense/notas/2026-08-12-e4a-radio-celda-d.md",
    "forense/notas/2026-08-12-e4c-r5-1-d2-commit6-reconciliacion-fila-e.md",
    "forense/notas/2026-08-12-j-alcance-folioviv.md",
    "forense/notas/2026-08-13-alias-p-motor-diag.md",
    "forense/notas/2026-08-13-apertura-issp.md",
    "forense/notas/2026-08-13-benchmark-enlace-invarianza.md",
    "forense/notas/2026-08-13-e2-cierre.md",
    "forense/notas/2026-08-13-firmas-2.md",
    "forense/notas/2026-08-13-invarianza-encuci-enbiare.md",
    "forense/notas/2026-08-13-proc-10.md",
    "forense/notas/2026-08-13-proc-11.md",
    "forense/notas/2026-08-13-reapertura-52a-54-commit2-barrido.md",
    "forense/notas/2026-08-13-res-reserva.md",
    "forense/notas/2026-08-13-sella-3.md",
    "forense/notas/2026-08-13-sella-mesa.md",
    "forense/notas/2026-08-14-acto-b2-via-capa3.md",
    "forense/notas/2026-08-14-motor-1.md",
    "forense/notas/2026-08-14-motor3-plan.md",
    "forense/notas/2026-08-14-reconcilia-spec.md",
    "forense/notas/2026-08-14-tablero-firmas-commit3.md",
    "forense/notas/2026-08-14-tablero-firmas-commit4-freeze.md",
    "forense/notas/2026-08-14-tablero-firmas.md",
    "forense/notas/2026-08-17-b2-derivaciones-c4.md",
    "forense/notas/2026-08-17-b2-recupera.md",
    "forense/notas/2026-08-17-b2-relevo.md",
    "forense/notas/2026-08-17-celda-d-complemento.md",
    "forense/notas/2026-08-17-consolida.md",
    "forense/notas/2026-08-17-fuente-unica-decisiones.md",
    "forense/notas/2026-08-17-higiene-vivos.md",
    "forense/notas/2026-08-17-registra-17ago-comandos.md",
    "forense/notas/2026-08-17-t22-deriva.md",
    "forense/notas/2026-08-18-b2-semantico.md",
    "forense/notas/2026-08-18-b2-transfer.md",
    "forense/notas/2026-08-18-b2-v7.md",
    "forense/notas/2026-08-18-entrada3-triage-hitoD.md",
    "forense/notas/2026-08-18-estado-split-clausula-por-linea.md",
    "forense/notas/2026-08-18-gate-durable-v7.md",
    "forense/notas/2026-08-18-integrate-t23.md",
    "forense/notas/2026-08-18-mesa-18ago.md",
    "forense/notas/2026-08-18-mesa-19ago-seis-firmas.md",
    "forense/notas/2026-08-18-motor3-con-sello-y-entrada-5.md",
    "forense/notas/2026-08-18-p3-barrido-final.md",
    "forense/notas/2026-08-18-sello-ficha-g3-gate-e0e5-no-cumplido.md",
    "forense/notas/2026-08-19-coef-universo-cierre.md",
    "forense/notas/2026-08-20-sella-adv-cierre.md",
    "forense/p3-lca-preregistro-v1_0.md",
    "forense/r5-1-diseno-por-regla-preregistro-v1_0.md",
    "forense/red-team-A_auditoria-adversarial.md",
    "forense/red-team-auditoria-benchmarks.md",
    "forense/red_team_A_auditoria.md",
    "forense/notas/2026-08-20-lote-retriage-cierre.md",
    "forense/notas/2026-08-20-lote-motor2-reverificacion.md",
    "forense/encargos/2026-08-20-LOTE-MOTOR2.md",
    "forense/registro-recalculo-v1_0.md",
    "forense/notas/nota-2026-08-25-propaga-330-337.md",
    # ACTO DISENO-ENSAFI, 26/ago/2026: encargo archivado VERBATIM (convencion
    # de forense/encargos/) y su nota de cierre. El `E4` pelado es el nombre
    # que direccion (maestra-30) le dio a este mismo encargo; queda censado en
    # canon/registro-rotulos.tsv como HABITANTE adicional del espacio E, con
    # su colision declarada contra E4a/E4b/E4c (que son las partes a/b/c de la
    # entrada 4 del motor, referente distinto). La nota de cierre entra por la
    # misma razon que 2026-08-24-adq-corre-r74r75-cierre.md: narra el hallazgo
    # de T25 y al narrarlo vuelve a escribir el token. El texto de direccion no
    # se edita para complacer a un test. Extension minima de perimetro por
    # desviacion mecanica (CI del propio acto), declarada en la nota de cierre.
    "forense/encargos/2026-08-26-E4-DISENO-ENSAFI.md",
    "forense/notas/2026-08-26-diseno-ensafi-cierre.md",
    # ACTO E5-SELLA-FP164-OCTAVA, 26/ago/2026: encargo archivado VERBATIM
    # (convencion de forense/encargos/) y su nota de cierre. El `E5` pelado
    # es el nombre que direccion (maestra-30) le dio a este mismo encargo;
    # queda censado en canon/registro-rotulos.tsv como HABITANTE adicional
    # del espacio E, con su colision declarada contra E4x/E4/E-3/E3-TRIAGE/
    # MAESTRA30-E1..E4 (referentes distintos, ninguno gana, mismo patron
    # que M5). El texto de direccion no se edita para complacer a un test.
    # Extension minima de perimetro por desviacion mecanica (CI del propio
    # acto), declarada en la nota de cierre.
    "forense/encargos/2026-08-26-E5-SELLA-FP164-OCTAVA.md",
    "forense/notas/2026-08-26-sella-fp164-cierre.md",
    # ACTO E6 L-RUN, 26/ago/2026 (ADR-206): encargo archivado VERBATIM
    # (A.3 + convencion de forense/encargos/) y su nota de cierre. El `E6`
    # pelado es el nombre que direccion (maestra-30) le dio a este mismo
    # encargo -- sexto de la serie --, no una fase E6 de ningun motor; queda
    # censado en canon/registro-rotulos.tsv como HABITANTE adicional del
    # espacio E, con su colision declarada contra E0/E2/E3-TRIAGE/E4a/E4b/
    # E4c/E5/E-3/E1/E4/MAESTRA30-E1..E4 (referentes distintos, ninguno gana,
    # mismo patron que M5). La nota entra por la misma razon que
    # 2026-08-26-sella-fp164-cierre.md: narra el hallazgo de T25 y al
    # narrarlo vuelve a escribir el token. El texto de direccion no se edita
    # para complacer a un test. Extension minima de perimetro por desviacion
    # mecanica (CI del propio acto), declarada en la nota de cierre.
    "forense/encargos/2026-08-26-E6-L-RUN.md",
    "forense/notas/2026-08-26-l-run-cierre.md",
    # ACTO MAESTRA30-E8 M-EMITE-Y-RESELLO, 26/ago/2026 (ADR-208): encargo
    # archivado VERBATIM (A.3 + convencion de forense/encargos/), su nota
    # de cierre y el enlace M que narra el hallazgo de E7 al citarlo. Los
    # `E7`/`E8`/`E9` pelados son los nombres que direccion (maestra-30) le
    # dio a los actos de esta misma serie -- septimo, octavo y noveno --,
    # no fases de ningun motor; quedan censados en canon/registro-rotulos.tsv
    # como HABITANTES adicionales del espacio E, con su colision declarada
    # contra E0/E2/E3-TRIAGE/E4a/E4b/E4c/E5/E-3/E1/E4/E6/MAESTRA30-E1..E7
    # (referentes distintos, ninguno gana, mismo patron que M5). El texto de
    # direccion no se edita para complacer a un test. Extension minima de
    # perimetro por desviacion mecanica (CI del propio acto), declarada en
    # la nota de cierre.
    "forense/encargos/2026-08-26-E8-M-EMITE-Y-RESELLO.md",
    "forense/notas/2026-08-26-e8-m-emite-cierre.md",
    "forense/prereg-duelo-v2/enlace-M-v1_0.md",
    # ACTO MAESTRA31-E4 · ORDEN-SUPERIOR, 27/ago/2026 (ADR-213): encargo
    # archivado VERBATIM (A.3), su spec de COMMIT-1 y su nota de cierre.
    # Direccion lo lanzo rotulado "ENCARGO E4", y "E4" pelado colisiona con
    # los habitantes ya censados E4a/E4b/E4c y con el habitante previo E4
    # (ACTO DISENO-ENSAFI, maestra-30, forense/encargos/2026-08-26-E4-
    # DISENO-ENSAFI.md) -- cinco referentes reales distintos, ninguno gana,
    # mismo patron que M5. La spec de COMMIT-1 menciona de paso "el
    # emparejador de E5" (el acto sucesor que emparejaria este inventario
    # contra el motor, fuera del perimetro de este acto) -- "E5" pelado
    # colisiona con los habitantes ya censados del espacio E. La nota de
    # cierre cita textualmente la lista de siete actos del encargo de
    # direccion ("E1, R34-ENSAFI-CENSA, ...") -- "E1" pelado es la mencion
    # de un habitante ya censado (ACTO MAESTRA31-E1), no un marcador nuevo.
    # D-6 aplicado donde se puede aplicar: el acto se declara ACTO
    # MAESTRA31-E4 en todo archivo que escribe y queda censado en
    # canon/registro-rotulos.tsv; el texto de direccion no se edita para
    # complacer a un test.
    "forense/encargos/2026-08-26-MAESTRA31-E4-ORDEN-SUPERIOR.md",
    "forense/notas/2026-08-26-orden-superior-spec.md",
    "forense/notas/2026-08-26-orden-superior-cierre.md",
    # ACTO MAESTRA31-E5 · CRUCE-INVERSO, 27/ago/2026 (ADR-214): encargo
    # archivado VERBATIM (A.3), su spec de COMMIT-1 y su nota de cierre.
    # Direccion lo lanzo rotulado "ENCARGO E5", titulo que el propio
    # encargo abre con "E5" pelado ("ENCARGO E5 · CRUCE-INVERSO..."),
    # colisionando con los habitantes ya censados del espacio E -- se
    # censa, no se reclama, tal como el propio encargo instruye ("Token
    # pelado E5 colisiona; se censa, no se reclama"). La spec y la nota de
    # cierre citan `E1` al listar el residual de falsos positivos de forma
    # de la propia regex (el token literal `E1` que aparece en
    # `milpa/procedencia.yaml:996`, metadata interna del archivo, no un
    # marcador de acto) -- mismo patron que las notas de E2/E4 arriba. D-6
    # aplicado donde se puede aplicar: el acto se declara ACTO MAESTRA31-E5
    # en todo archivo que escribe y queda censado en
    # canon/registro-rotulos.tsv; el texto de direccion no se edita para
    # complacer a un test.
    "forense/encargos/2026-08-27-MAESTRA31-E5-CRUCE-INVERSO.md",
    "forense/notas/2026-08-27-cruce-inverso-spec.md",
    "forense/notas/2026-08-27-cruce-inverso-cierre.md",
    # ACTO MAESTRA31-E6 · DICCIONARIOS-FD, 27/ago/2026 (ADR-215, candidateado
    # ADR-214 y renumerado al fusionar en segundo lugar contra PR #386/
    # ACTO MAESTRA31-E5 · CRUCE-INVERSO, que fusiono primero y se quedo con
    # ADR-214 -- ver la entrada de arriba, mismo patron de concurrencia
    # NUBE/UBUNTU que el propio encargo de este acto ya declaraba antes de
    # arrancar): encargo archivado VERBATIM (A.3), su nota de cierre.
    # Direccion lo lanzo rotulado "ENCARGO E6", y "E6" pelado colisiona con
    # el habitante ya censado del espacio E (ACTO E6 L-RUN, maestra-30,
    # forense/encargos/2026-08-26-E6-L-RUN.md) -- token pelado E6, se
    # censa, no se reclama, tal como el propio encargo lo declara. El
    # encargo y la nota tambien citan en prosa "E4" (ACTO MAESTRA31-E4, el
    # acto anterior cuyo hueco este acto extiende) y "E5" (ACTO MAESTRA31-E5
    # · CRUCE-INVERSO, concurrente en NUBE, y el acto sucesor que
    # emparejaria el texto extraido contra el motor) -- las dos son mencion
    # de habitantes ya censados del espacio E, no marcadores nuevos.
    # Colision declarada contra E0/E2/E3-TRIAGE/E4a/E4b/E4c/E5/E-3/E1/E4/
    # E6/E7/E9/E10/MAESTRA30-E1..E4/MAESTRA31-E1..E5 (referentes distintos,
    # ninguno gana, mismo patron que M5). D-6 aplicado donde se puede
    # aplicar: el acto se declara ACTO MAESTRA31-E6 en todo archivo que
    # escribe y queda censado en canon/registro-rotulos.tsv; el texto de
    # direccion no se edita para complacer a un test.
    "forense/encargos/2026-08-27-MAESTRA31-E6-DICCIONARIOS-FD.md",
    "forense/notas/2026-08-27-diccionarios-fd-cierre.md",
    # ACTO MAESTRA31-E7 · ETIQUETA, 27/ago/2026 (ADR-216): encargo
    # archivado VERBATIM (A.3) y su nota de cierre. Direccion lo lanzo
    # rotulado "ENCARGO E7", y "E7" pelado colisiona con la referencia
    # previa ACTO E7 R-SCORING (maestra-30, ADR-207) y con los demas
    # habitantes ya censados del espacio E. D-6 aplicado donde se puede
    # aplicar: el acto se declara ACTO MAESTRA31-E7 en todo archivo que
    # escribe y queda censado en canon/registro-rotulos.tsv; el encargo
    # NO se edita, porque A.3 pide el texto de direccion verbatim, y la
    # nota de cierre y la nota de regla congelada citan el rotulo "E7" al
    # narrar el propio hallazgo -- ninguno es un marcador nuevo.
    "forense/encargos/2026-08-27-MAESTRA31-E7-ETIQUETA.md",
    "forense/notas/2026-08-27-etiqueta-regla.md",
    "forense/notas/2026-08-27-etiqueta-cierre.md",
    # ACTO MAESTRA31-E8 · LOS-388, 27/ago/2026: encargo archivado VERBATIM
    # (A.3), su spec de COMMIT-1 y su nota de cierre. Direccion lo lanzo
    # rotulado "ENCARGO E8", titulo que el propio encargo abre con "E8"
    # pelado ("ENCARGO E8 · LOS 388...") y que menciona de nuevo al declarar
    # "Rotulo: ACTO MAESTRA31-E8 (D-6). Token pelado E8 colisiona; se censa,
    # no se reclama" -- colisiona con el habitante ya censado del espacio E
    # (ACTO E8-M-EMITE-Y-RESELLO, maestra-30,
    # forense/encargos/2026-08-26-E8-M-EMITE-Y-RESELLO.md, ya en esta misma
    # lista arriba), tal como el propio encargo instruye: se censa, no se
    # reclama. La spec de COMMIT-1 y la nota de cierre citan en prosa "E7"
    # al declarar que `E7 · ETIQUETA` (FP-174, concurrente en NUBE) no
    # habia fusionado a origin/main a la hora de arrancar -- mencion de un
    # habitante ya censado del espacio E, no un marcador nuevo, mismo
    # patron que las notas de E4/E5/E6 arriba. D-6 aplicado donde se puede
    # aplicar: el acto se declara ACTO MAESTRA31-E8 en todo archivo que
    # escribe y queda censado en canon/registro-rotulos.tsv; el texto de
    # direccion no se edita para complacer a un test.
    "forense/encargos/2026-08-27-MAESTRA31-E8-LOS-388.md",
    "forense/notas/2026-08-27-los-388-commit1-escala.md",
    "forense/notas/2026-08-27-los-388-cierre.md",
    # ACTO MAESTRA31-E9 · ESTIMA-RUTAC, 27/ago/2026: encargo archivado
    # VERBATIM (A.3). Direccion lo lanzo rotulado "ENCARGO E9 ·
    # ESTIMA-RUTAC", titulo que el propio encargo abre con "E9" pelado
    # y que ademas declara en su ARRANQUE: "Rotulo: ACTO MAESTRA31-E9
    # (D-6). Token pelado E9 colisiona con MAESTRA30-E9 · SCORING-V2;
    # se censa, no se reclama" -- colisiona con el habitante ya censado
    # del espacio E (fila E9 = ACTO MAESTRA30-E9 SCORING-V2,
    # canon/registro-rotulos.tsv), tal como el propio encargo instruye:
    # se censa, no se reclama. D-6 aplicado donde se puede aplicar: el
    # acto se declara ACTO MAESTRA31-E9 en todo archivo que escribe y
    # queda censado en canon/registro-rotulos.tsv; el texto de direccion
    # no se edita para complacer a un test. La spec de COMMIT-1
    # (forense/notas/2026-08-27-estima-rutac-spec.md) y la nota de
    # cierre (forense/notas/2026-08-27-estima-rutac-cierre.md) NO traen
    # ningun rotulo pelado nuevo (verificado con el mismo regex de este
    # test, sin match en ninguno de los dos) -- solo el encargo se
    # censa aqui, no los tres.
    "forense/encargos/2026-08-27-MAESTRA31-E9-ESTIMA-RUTAC.md",
    # ACTO MAESTRA31-E10 · RECONCILIA-MOTOR, 27/ago/2026: encargo archivado
    # VERBATIM (A.3). Direccion lo lanzo rotulado "ENCARGO E10 ·
    # RECONCILIA-MOTOR", titulo que el propio encargo abre con "E10" pelado
    # y que ademas declara en su ARRANQUE: "Rotulo: ACTO MAESTRA31-E10
    # (D-6). Token pelado E10 colisiona con MAESTRA30-E10 · R21-ADJUDICA;
    # se censa, no se reclama" -- colisiona con el habitante ya censado
    # del espacio E (fila MAESTRA30-E10 = ACTO MAESTRA30-E10 R21-ADJUDICA,
    # canon/registro-rotulos.tsv), tal como el propio encargo instruye:
    # se censa, no se reclama. D-6 aplicado donde se puede aplicar: el
    # acto se declara ACTO MAESTRA31-E10 en todo archivo que escribe y
    # queda censado en canon/registro-rotulos.tsv; el texto de direccion
    # no se edita para complacer a un test. forense/estado-motor-v1_0.md
    # y forense/notas/2026-08-27-reconcilia-motor-cierre.md NO traen
    # ningun rotulo pelado nuevo (verificado con el mismo regex de este
    # test, corrido en vivo sobre el arbol -- sin match en ninguno de los
    # dos) -- solo el encargo se censa aqui.
    "forense/encargos/2026-08-27-MAESTRA31-E10-RECONCILIA-MOTOR.md",
    # ACTO MAESTRA32-E1 · SELLA-ENLACE, 28/ago/2026 (ADR-220): encargo
    # archivado VERBATIM (A.3). Direccion lo lanzo rotulado "ACTO
    # MAESTRA32-E1 · SELLA-ENLACE", titulo que el propio encargo abre con
    # "E1" pelado y que ademas declara en su cabecera: "Token pelado E1
    # colisiona con los habitantes ya censados del espacio E (E1 ·
    # CIERRA-FP157, maestra-30; MAESTRA31-E1 · RELOJ-CRUCE) -- se censa, no
    # se reclama" -- colisiona con esos dos habitantes ya censados de
    # canon/registro-rotulos.tsv, tal como el propio encargo instruye. D-6
    # aplicado donde se puede aplicar: el acto se declara ACTO MAESTRA32-E1
    # en todo archivo que escribe y queda censado en
    # canon/registro-rotulos.tsv; el texto de direccion no se edita para
    # complacer a un test. forense/notas/2026-08-28-sella-enlace-cierre.md
    # NO trae ningun rotulo pelado nuevo (verificado con el mismo regex de
    # este test, corrido en vivo sobre el arbol -- sin match) -- solo el
    # encargo se censa aqui.
    "forense/encargos/2026-08-28-MAESTRA32-E1-SELLA-ENLACE.md",
    # ACTO MAESTRA32-E2 · EMPAREJA-MOTOR-TEXTO, 28/ago/2026: encargo
    # archivado VERBATIM (A.3). Direccion lo lanzo rotulado "ACTO
    # MAESTRA32-E2 · EMPAREJA-MOTOR-TEXTO" y el propio texto trae, sin
    # prefijo de espacio, la mencion "cuando E3 amplie" (sucesor
    # MAESTRA32-E3, verificado con el mismo regex de este test, corrido
    # en vivo sobre el archivo -- un solo match, `E3`). "E2" pelado
    # colisiona con los habitantes ya censados del espacio E (E2 ·
    # pipeline de barrido semantico, FP-65; MAESTRA31-E2 ·
    # REGISTRA-PENDIENTES) -- se censa, no se reclama, mismo patron que
    # los actos anteriores de esta serie. D-6 aplicado donde se puede
    # aplicar: el acto se declara ACTO MAESTRA32-E2 en todo archivo que
    # escribe y queda censado en canon/registro-rotulos.tsv; el texto de
    # direccion no se edita para complacer a un test.
    # forense/notas/2026-08-28-empareja-spec.md NO trae ningun rotulo
    # pelado nuevo (verificado con el mismo regex, corrido en vivo sobre
    # el archivo -- sin match).
    # forense/notas/2026-08-28-empareja-cierre.md SI trae rotulos pelados
    # (verificado con el mismo regex, corrido en vivo -- varios match:
    # E1/E5/E6, todos referencias narrativas a actos previos ya censados
    # -- "lo que E1 escribio", "abierta por E6, no por E5" -- no rotulos
    # nuevos que este acto reclame). Se censa aqui en vez de reescribir
    # cada referencia con prefijo, mismo patron que el propio test ofrece
    # como alternativa valida en su mensaje de fail.
    "forense/encargos/2026-08-28-MAESTRA32-E2-EMPAREJA-MOTOR-TEXTO.md",
    "forense/notas/2026-08-28-empareja-cierre.md",
    # ACTO MAESTRA32-E5 · PROPAGA-FIRMAS-Y-COLA, 30/ago/2026 (ADR-222):
    # encargo archivado VERBATIM (A.3). El titulo abre con "ACTO
    # MAESTRA32-E5" (hifenado, no pelado) pero el cuerpo trae, en prosa,
    # bare E4 ("El numero E4 queda reservado"), E2/E3 ("cierres de
    # E2/E3"), E1/E2 ("solo E1 y E2, listado completo") y E5 ("E5/ADR-214
    # corrio"; el rotulo del propio acto en la linea de registro-rotulos)
    # -- verificado con el mismo regex de este test, corrido en vivo
    # sobre el archivo. Todos son referencias narrativas a habitantes ya
    # censados o al propio acto declarandose (D-6), ninguno reclama un
    # rotulo nuevo sin censar. D-6 aplicado donde se puede aplicar: el
    # acto se declara ACTO MAESTRA32-E5 en todo archivo que escribe y
    # queda censado en canon/registro-rotulos.tsv (token pelado E5
    # colisiona con tres habitantes previos: "entrada 5, registro de
    # recalculo" 18/ago; ACTO E5 - SELLA-FP164-OCTAVA, maestra-30;
    # MAESTRA31-E5 - CRUCE-INVERSO); el texto de direccion no se edita
    # para complacer a un test.
    "forense/encargos/2026-08-30-MAESTRA32-E5-PROPAGA-FIRMAS-Y-COLA.md",
    # ACTO MAESTRA32-E3 · EXTRACTOR-DTA, redactado 28/ago/2026 por
    # direccion, archivado 30/ago/2026 por ACTO MAESTRA32-E5 (repara la
    # grieta A.3: el texto vivio solo en la conversacion de lanzamiento
    # de E3 hasta hoy). Cuerpo verbatim (verificado byte a byte contra
    # el original cargado por direccion), con una cabecera anadida
    # resolviendo su RANURA M-EXTRACTOR -- la cabecera no trae rotulos
    # pelados nuevos. El cuerpo trae bare E2 ("resultado de E2", "arbol
    # ya fusionado con E2", "veredictos de E2"), E4/E6 ("precedente
    # E4/E6"), E6 ("patron", "estilo E6") y E8 ("misma regla del propio
    # E8") -- verificado con el mismo regex, corrido en vivo sobre el
    # archivo -- todas referencias narrativas de direccion a actos ya
    # censados (MAESTRA31-E6, MAESTRA31-E8, MAESTRA31-E4, MAESTRA32-E2),
    # ninguna reclama un rotulo nuevo. El texto de direccion no se edita
    # para complacer a un test.
    "forense/encargos/2026-08-28-MAESTRA32-E3-EXTRACTOR-DTA.md",
    # forense/notas/2026-08-30-propaga-firmas-cierre.md -- nota de cierre
    # de ACTO MAESTRA32-E5 que discute los rotulos bare E1-E8 al citar,
    # en prosa, por que los dos archivos de arriba necesitaron esta
    # misma lista -- ninguna es un rotulo nuevo que este acto reclame.
    # Extension minima de perimetro por desviacion mecanica, mismo
    # precedente que las notas de cierre de MAESTRA31-E2/E7/E8 y
    # MAESTRA32-E2 ya listadas arriba.
    "forense/notas/2026-08-30-propaga-firmas-cierre.md",
    # ACTO MAESTRA32-E6 · ETIQUETA-v1_2, 31/ago/2026 (ADR-223): encargo
    # archivado VERBATIM (A.3). El titulo abre con "ACTO MAESTRA32-E6"
    # (hifenado, no pelado) pero el cuerpo trae bare E6 ("E6 (este)"),
    # E7 ("E7 - CANDIDATOS-MARCO-M", "el mismo dia que E7"), E3/E8
    # (carril CAJA), E2 (spec congelada de E2) -- verificado con el
    # mismo regex de este test, corrido en vivo sobre el archivo. Todas
    # son referencias narrativas de direccion a actos ya censados o al
    # propio acto declarandose, ninguna reclama un rotulo nuevo sin
    # censar. El texto de direccion no se edita para complacer a un
    # test.
    "forense/encargos/2026-08-30-MAESTRA32-E6-ETIQUETA-v1_2.md",
    # forense/notas/2026-08-30-etiqueta-v1_2-spec.md -- COMMIT-1 de
    # ACTO MAESTRA32-E6. Trae bare E2 ("editar la spec de E2") y E5/E7/E2
    # ("mismo cierre que E5/E7/E2") al citar, en prosa, precedentes ya
    # censados -- ninguno es un rotulo nuevo.
    "forense/notas/2026-08-30-etiqueta-v1_2-spec.md",
    # forense/notas/2026-08-30-etiqueta-v1_2-cierre.md -- nota de cierre
    # de ACTO MAESTRA32-E6. Trae bare E2/E5 ("ACTO MAESTRA32-E2/E5 ya
    # dieron", "no-discrepante que E2/E5 ya reportaron") y E6/E7
    # ("Rotulo E6/E7 intercambiado") al citar, en prosa, precedentes ya
    # censados o el propio acto -- ninguno reclama un rotulo nuevo.
    # Extension minima de perimetro por desviacion mecanica, mismo
    # precedente que las notas de cierre ya listadas arriba.
    "forense/notas/2026-08-30-etiqueta-v1_2-cierre.md",
    # ACTO MAESTRA32-E10 · COBERTURA-15, 31/ago/2026: encargo archivado
    # VERBATIM (A.3), cerrado por hallazgo antes de COMMIT-1 (el propio
    # ARRANQUE del encargo, no un descubrimiento tardio). El titulo abre
    # con "ACTO MAESTRA32-E10" (hifenado, no pelado) pero el cuerpo trae
    # bare E9 ("carril NUBE = `E9 -> E10`", "registrada por E9", "3 (+1
    # con E9, +2 con E8)"), E10 ("carril NUBE = `E9 -> E10 (este)`",
    # "token pelado `E10` colisiona"), E3/E8 (carril CAJA, mismo patron
    # narrativo que MAESTRA32-E6/E5 ya listados arriba) -- verificado con
    # el mismo regex de este test, corrido en vivo sobre el archivo (9
    # coincidencias, ninguna reclama un rotulo nuevo sin censar: E9/E10
    # ya censados en canon/registro-rotulos.tsv, E3/E8 cubiertos por el
    # mismo precedente narrativo que MAESTRA32-E6). El texto de direccion
    # no se edita para complacer a un test.
    "forense/encargos/2026-08-30-MAESTRA32-E10-COBERTURA-15.md",
    # forense/notas/2026-08-30-cobertura-15-cierre.md -- nota de cierre de
    # ACTO MAESTRA32-E10. Narra, en prosa, por que el propio encargo (arriba)
    # necesito esta misma lista, y cita el gate incumplido con los mismos
    # rotulos bare (E9/E10/E3/E8) -- ninguno es un rotulo nuevo. Extension
    # minima de perimetro por desviacion mecanica, mismo precedente que las
    # notas de cierre de MAESTRA32-E5/E6 ya listadas arriba.
    "forense/notas/2026-08-30-cobertura-15-cierre.md",
    # ACTO MAESTRA32-E9 · PROPAGA-2, 30/ago/2026 (ADR-225, renumerado de
    # ADR-224 al fusionar: ACTO MAESTRA32-E10 arriba fusionó primero y se
    # quedó con ADR-224): encargo archivado VERBATIM (A.3). El titulo abre
    # con "ACTO MAESTRA32-E9" (hifenado, no pelado) pero el cuerpo trae
    # bare E9 ("E9 (este)", "entre E9 y E8", "E9 añade UNA entrada",
    # "token pelado E9 colisiona"), E10 ("E10 lo ejecuta", "E10
    # habiliten"), E8 ("E8 añade campos", "no lanza E3 ni E8"), E3 ("E3
    # archivado", "E3 <- FP-178"), E7 ("E7 - CANDIDATOS-MARCO-M", "retiro
    # de E7"), E6 ("el cierre de E6", "le paso a direccion en E6"), E4
    # ("E4 - RE-EMPAREJA") y E2 ("mediciones que E2/E6/E10 habiliten") --
    # verificado con el mismo regex de este test, corrido en vivo sobre
    # el archivo. Todas son referencias narrativas de direccion a actos
    # ya censados o al propio acto declarandose, ninguna reclama un
    # rotulo nuevo sin censar. El texto de direccion no se edita para
    # complacer a un test.
    "forense/encargos/2026-08-30-MAESTRA32-E9-PROPAGA-2.md",
    # forense/notas/2026-08-30-propaga-2-cierre.md -- nota de cierre de
    # ACTO MAESTRA32-E9 · PROPAGA-2. Discute, en prosa, los mismos
    # rotulos bare que el encargo (E9/E10/E8/E3/E7/E6/E4/E2) al citar
    # por que este acto necesito la misma lista de arriba -- ninguno es
    # un rotulo nuevo. Extension minima de perimetro por desviacion
    # mecanica, mismo precedente que las notas de cierre ya listadas
    # arriba.
    "forense/notas/2026-08-30-propaga-2-cierre.md",
    # ACTO MAESTRA32-E8 · MEDICION-COMPUESTA, 30/ago/2026 (ADR pendiente
    # de numero, M-AGREGA=a'): encargo archivado VERBATIM (A.3), su spec
    # congelada (COMMIT-1) y su nota de cierre (COMMIT-2). Direccion lo
    # lanzo rotulado "ENCARGO E8", y "E8" pelado colisiona con el
    # habitante ya censado MAESTRA31-E8; ademas la cabecera del encargo
    # y ambas notas citan "MAESTRA32-E3 . EXTRACTOR-DTA" (compuerta
    # levantada in situ el mismo 30/ago), cuyo "E3" pelado colisiona con
    # MAESTRA31-E3/E3-TRIAGE. D-6 aplicado donde se puede aplicar: el
    # acto se declara ACTO MAESTRA32-E8 en todo archivo que escribe y
    # queda censado en canon/registro-rotulos.tsv; el encargo NO se
    # edita, porque A.3 pide el texto de direccion verbatim, y la spec/
    # la nota de cierre repiten ese mismo texto verbatim en su §0 (input
    # de direccion que levanta la compuerta) por instruccion explicita
    # de direccion -- misma situacion que ya cubren las notas de la
    # lista de arriba: citar un rotulo al narrar una decision no es
    # reclamarlo, pero el regex no distingue, asi que se censa aqui en
    # vez de editar la narracion. Mismo movimiento y misma razon que
    # MAESTRA31-E1..E7, MAESTRA30-E10 y MAESTRA32-E9/E10, ya listadas
    # arriba.
    "forense/encargos/2026-08-30-MAESTRA32-E8-MEDICION-COMPUESTA.md",
    "forense/notas/2026-08-30-compuesta-spec.md",
    "forense/notas/2026-08-30-compuesta-cierre.md",
    # ACTO MAESTRA32-E11 · COBERTURA-15, 31/ago/2026 (ADR-227, renumerado
    # de ADR-226 al fusionar: ACTO MAESTRA32-E8 arriba fusiono primero y
    # se quedo con ADR-226; re-emision de MAESTRA32-E10/ADR-224 con
    # compuerta ya cumplida por MAESTRA32-E9/ADR-225): encargo archivado
    # VERBATIM (A.3). El titulo
    # abre con "ACTO MAESTRA32-E11" (hifenado, no pelado) pero el cuerpo
    # trae bare E10 ("re-emision de E10", "E10 queda consumido",
    # "verificado por el propio E10", "el intento E10", "el cierre de
    # E10", "re-emision de E10 (ADR-224)"), E9 ("su compuerta era E9
    # fusionado", "registrada por ADR-225 (E9)", "redactar y fusionar
    # E9", "E9 ya fusiono"), E11 ("carril NUBE = E11 (este)", "token
    # pelado E11"), E3/E8 (carril CAJA, mismo patron narrativo que
    # MAESTRA32-E6/E9/E10 ya listados arriba) y E4 ("E4 sigue
    # reservado") -- verificado con el mismo regex de este test, corrido
    # en vivo sobre el archivo. Todas son referencias narrativas de
    # direccion a actos ya censados o al propio acto declarandose,
    # ninguna reclama un rotulo nuevo sin censar. El texto de direccion
    # no se edita para complacer a un test.
    "forense/encargos/2026-08-30-MAESTRA32-E11-COBERTURA-15.md",
    # forense/notas/2026-08-30-cobertura-15-cierre-E11.md -- nota de
    # cierre de ACTO MAESTRA32-E11 · COBERTURA-15. Trae bare E10 tres
    # veces, todas narrativas: el titulo ("re-emision de E10"), la cita
    # al cierre de E10 como obra previa ("cierre de E10, obra previa
    # citada"), y la cita al encargo original de E10 ("encargo original
    # de E10, para heredar la definicion de FP-183/FP-184") -- ninguno
    # es un rotulo nuevo, E10 ya esta censado en canon/registro-rotulos.
    # tsv. Extension minima de perimetro por desviacion mecanica, mismo
    # precedente que las notas de cierre ya listadas arriba.
    "forense/notas/2026-08-30-cobertura-15-cierre-E11.md",
    # ACTO MAESTRA32-E4 · RE-EMPAREJA, 30/ago/2026 (re-corre la spec
    # congelada de MAESTRA32-E2 verbatim sobre el universo ampliado
    # v1_2 UNION ext-v1_0): encargo archivado VERBATIM (A.3). El titulo
    # abre con "ACTO MAESTRA32-E4" (hifenado, no pelado) pero el cuerpo
    # trae bare E2/E3/E6/E12/E4 en prosa narrativa de direccion (citas a
    # actos previos ya censados -- E2/EMPAREJA-MOTOR-TEXTO, E3/E6 ya
    # censados arriba -- y al carril CAJA declarado, E12, y al propio
    # rotulo reservado "E4 (este)"/"su rotulo estaba reservado") --
    # verificado con el mismo regex de este test, corrido en vivo sobre
    # el archivo. Ninguna es un rotulo nuevo sin censar; E12 no se censa
    # aqui porque no es un habitante de este acto (carril CAJA ajeno,
    # declarado solo por concurrencia). El texto de direccion no se
    # edita para complacer a un test.
    "forense/encargos/2026-08-30-MAESTRA32-E4-RE-EMPAREJA.md",
    # forense/notas/2026-08-30-reempareja-spec.md -- COMMIT-1 de este
    # acto. Trae bare E2 (cita repetida a la spec/criterios congelados
    # de MAESTRA32-E2) y E6 (cita al bloque de re-corrida elevado desde
    # MAESTRA32-E6) en prosa narrativa -- ambos ya censados, ninguno
    # nuevo. Extension minima de perimetro por desviacion mecanica,
    # mismo precedente que las notas de cierre ya listadas arriba.
    "forense/notas/2026-08-30-reempareja-spec.md",
    # forense/notas/2026-08-30-reempareja-cierre.md -- COMMIT-2 (nota de
    # cierre) de este acto. Trae bare E6 (cita a la nota de origen del
    # codigo elevado) y E2 (cita a la spec congelada) en prosa
    # narrativa -- ambos ya censados, ninguno nuevo.
    "forense/notas/2026-08-30-reempareja-cierre.md",
    # ACTO MAESTRA32-E13 · MARCO-M-CONGELA (ACTO A') + PROPAGA-3, 31/ago/2026:
    # encargo archivado VERBATIM (A.3). El texto de dirección cita F1
    # verbatim ("FP-180 (E6)", "cobertura-15-v1_0.tsv (E11)") y la NOTA DE
    # ARRANQUE cita "mientras E4 corra" -- E4/E6/E11 son habitantes del
    # espacio E ya censados (MAESTRA32-E4/E6/E11), ninguno nuevo.
    "forense/encargos/2026-08-31-MAESTRA32-E13-MARCO-M-CONGELA.md",
    # forense/notas/2026-08-31-marco-M-cierre.md -- COMMIT-2 (nota de
    # cierre) de este acto. Trae bare E4/E6/E11 al listar los rótulos ya
    # conocidos que _T25_ARCHIVOS_CONOCIDOS censa (cita en prosa narrativa
    # sobre el propio mecanismo de este test), ninguno nuevo.
    "forense/notas/2026-08-31-marco-M-cierre.md",
    # ACTO MAESTRA32-E14 · MARCO-M-SORTEA (ACTO B′), 31/ago/2026: encargo
    # archivado VERBATIM (A.3). El texto de dirección cita "MAESTRA32-E13"
    # con prefijo (no bare) pero también el bare "E13" en varios puntos de
    # prosa narrativa (p.ej. "SHA de este merge... protocolo ADR-178/FP-150",
    # "ACTO B′ = MAESTRA32-E14" con "E13" citado como habitante ya censado
    # en canon/registro-rotulos.tsv) -- E13 ya está censado por
    # MAESTRA32-E13, ninguno nuevo.
    "forense/encargos/2026-08-31-MAESTRA32-E14-MARCO-M-SORTEA.md",
    # forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_0.md -- COMMIT-1
    # + COMMIT-2 de este acto. Cita bare E13 al declarar SHA_A ("merge de
    # E13") -- habitante ya censado (MAESTRA32-E13), ninguno nuevo.
    "forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_0.md",
    # ACTO MAESTRA32-E16 · MEDIDOR-FAMILISMO-APOYO, 31/ago/2026: encargo
    # archivado VERBATIM (A.3). Trae rótulo pelado nuevo `E16` (D-6/ADR-128)
    # -- censado aquí y en canon/registro-rotulos.tsv, no reclamado: el
    # acto se declara ACTO MAESTRA32-E16 en todo archivo que escribe.
    "forense/encargos/2026-08-31-MAESTRA32-E16-MEDIDOR-FAMILISMO.md",
}


def t25_rotulos():
    reg = os.path.join(ROOT, "canon", "registro-rotulos.tsv")
    if not os.path.exists(reg):
        fail("T25", "no existe `canon/registro-rotulos.tsv` -- D-6/ADR-128 lo exige "
                     "como registro de rótulos ya en uso")
        return
    for base in ("canon", "forense"):
        for p in glob.glob(os.path.join(ROOT, base, "**", "*.md"), recursive=True):
            relp = rel(p)
            if relp in _T25_ARCHIVOS_CONOCIDOS:
                continue
            m = _T25_ROTULO_BARE.search(read(p))
            if m:
                fail("T25", f"{relp}: trae rótulo pelado nuevo `{m.group(0)}` sin "
                             f"prefijo de espacio (D-6/ADR-128) -- dale prefijo "
                             f"(p.ej. `ADV1-{m.group(0)}`) o, si ya estaba en uso "
                             f"y solo faltaba censarlo, añádelo a `_T25_ARCHIVOS_"
                             f"CONOCIDOS` y a `canon/registro-rotulos.tsv`")


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
        ("T19a cabecera cruzada estado→modelo",   t19a_estado_cita_modelo_vigente),
        ("T19b contador 14 cruzado (modelo)",     t19b_modelo_contador_14),
        ("T19c portada derivada (README)",        t19c_readme_derivadas),
        ("T20 T-CASCADA-MARCADA",                 t20_cascada_marcada),
        ("T21 T-CAPA2-CAPA3",                     t21_capa2_capa3),
        ("T22 T-FIRMAS",                          t22_firmas),
        ("T23 T-CABLEADO",                        t23_cableado),
        ("T24 T-LLAVES-EJERCIDAS",                t24_llaves_ejercidas),
        ("T25 T-ROTULOS",                         t25_rotulos),
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
