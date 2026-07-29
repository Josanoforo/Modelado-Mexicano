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
    """El archivo vigente de un artefacto versionado. Falla si hay más de uno."""
    hits = sorted(glob.glob(os.path.join(ROOT, pattern)))
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
def t03_dangling_refs():
    """Un documento que cita un archivo inexistente no obliga a nada."""
    existing = {os.path.basename(p) for p in
                glob.glob(os.path.join(ROOT, "**", "*.*"), recursive=True)}
    for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if ".git" in p:
            continue
        for i, l in enumerate(read(p).split("\n"), 1):
            for m in re.findall(r"`([A-Za-z0-9_\-áéíóúñÁÉÍÓÚÑ.]+\.(?:md|yaml))`", l):
                if m in existing:
                    continue
                if re.search(r"borrad|BORRAD|REEMPLAZA|elimin|~~|superced|supersede|v1, borrado|fusionad", l, re.I):
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
    ]
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
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
