#!/usr/bin/env python3
"""HITO D · R10.1 — corrida del falsador (COMMIT B, ACTO RETRIAGE-4).

Ejecuta `forense/hitoD-R10_1-especificacion-v1_0.md`: cuenta los rechazos
MEXICANOS del corpus Brasdefer por brazo de poder y los codifica por directez
con la regla congelada en COMMIT A §4.1.

Imprime las 12 transcripciones integras a la salida cruda para que la
codificacion sea auditable a mano por cualquiera, no creible bajo palabra.
"""
import html
import os
import re

from scipy import stats as sps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "data", "raw", "ADQ15_Brasdefer_corpus_pragmatico")
SAL = os.path.join(ROOT, "forense", "notas",
                   "2026-08-20-r10-1-rechazo-poder-salida.txt")
OUT = open(SAL, "w", encoding="utf8")

# Operacionalizacion lexica de "negacion explicita" (COMMIT A §4.1). Lista
# CERRADA, declarada aqui: si el turno de quien rechaza contiene una de estas
# cabezas, el rechazo se cuenta DIRECTO; si no, INDIRECTO.
CABEZAS = [r"\bno puedo\b", r"\bno voy a\b", r"\bno quiero\b", r"\bno me interesa\b",
           r"\bno gracias\b", r"\bno, no\b", r"\bimposible\b", r"\bme niego\b",
           r"\bno podr[eé]\b", r"\bno va a poder\b", r"\bno cuentes conmigo\b",
           r"\bno voy\b", r"\bno la voy\b", r"\bno lo voy\b"]
RX_CAB = re.compile("|".join(CABEZAS), re.I)
UMBRAL_PP = 15.0


def log(m=""):
    print(m)
    OUT.write(m + "\n")


def plano(fn):
    t = open(os.path.join(DIR, fn), encoding="utf8", errors="replace").read()
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S | re.I)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    t = re.sub(r"[ \t]+", " ", t)
    return [l.strip() for l in t.split("\n") if l.strip()]


log("=" * 78)
log("HITO D · R10.1 — rechazo indirecto por asimetria de poder · RETRIAGE-4")
log("spec congelada: forense/hitoD-R10_1-especificacion-v1_0.md")
log("=" * 78)
log()
log("Regla de directez congelada en COMMIT A §4.1, operacionalizada aqui como")
log("lista CERRADA de cabezas de negacion explicita:")
log("  " + " · ".join(c.replace("\\b", "").replace("\\", "") for c in CABEZAS))
log()

# ── localizar la seccion de rechazos y sus bloques por pais ─────────────
lineas = plano("actos_de_habla.html")
i0 = next(n for n, l in enumerate(lineas) if l == "Rechazos")
sig = [n for n, l in enumerate(lineas)
       if n > i0 and l in ("Peticiones", "Invitaciones", "Cumplidos", "Quejas", "Consejos")]
fin = sig[0] if sig else len(lineas)
blk = lineas[i0:fin]
log("§1 · UNIVERSO")
log("  seccion 'Rechazos' de actos_de_habla.html: lineas %d..%d (%d lineas)"
    % (i0, fin, len(blk)))

paises = [(n, l.split(":")[0].strip()) for n, l in enumerate(blk)
          if re.match(r"^[A-ZÁÉÍÓÚÑ][\wáéíóúñ ]{2,30}: Transcripci", l)]
log("  paises con bloque de rechazos: %s" % ", ".join(p for _, p in paises))

# limites del bloque de Mexico
mx = [n for n, p in paises if p == "México"]
if not mx:
    log("  MEXICO AUSENTE de la seccion de rechazos -> rama 3")
    OUT.close()
    raise SystemExit
ini = mx[0]
sigs = [n for n, _ in paises if n > ini]
fim = sigs[0] if sigs else len(blk)
mxblk = blk[ini:fim]
log("  bloque de MEXICO: %d lineas" % len(mxblk))
log()

# ── escenarios: 'Rechazos N-M' seguido de descripcion con codigo ────────
esc = []
for n, l in enumerate(mxblk):
    if re.match(r"^Rechazos?\s*\d+\s*[-–y]\s*\d+\s*$", l) or re.match(r"^Rechazos?\s*\d+\s*[-–]\s*\d+", l):
        desc = mxblk[n + 1] if n + 1 < len(mxblk) else ""
        m = re.search(r"\(\s*([+=-])\s*D\s*,\s*([+=-])\s*P\s*\)", desc)
        if not m:
            m = re.search(r"\(\s*([+=-])\s*[Dd]istancia\s*,\s*([+=-])\s*[Pp]oder\s*\)", desc)
        esc.append((n, l, desc, m.group(2) if m else None))

log("§2 · ESCENARIOS MEXICANOS Y SU CODIGO DE PODER (del propio corpus)")
for n, rot, desc, pod in esc:
    log("  %-16s poder=%s | %s" % (rot, pod or "SIN CODIGO", desc.lstrip(": ")[:95]))
log()

# ── transcripciones: 'Rechazo N:' dentro de cada escenario ──────────────
marcas = [(n, l) for n, l in enumerate(mxblk) if re.match(r"^Rechazo\s*\d+\s*:", l)]
log("§3 · TRANSCRIPCIONES MEXICANAS")
log("  total de transcripciones 'Rechazo N:' en el bloque de Mexico: %d" % len(marcas))

def poder_de(idx):
    prev = [e for e in esc if e[0] < idx]
    return prev[-1][3] if prev else None

items = []
for k, (n, rot) in enumerate(marcas):
    fin_t = marcas[k + 1][0] if k + 1 < len(marcas) else len(mxblk)
    cuerpo = mxblk[n + 1:fin_t]
    items.append({"rot": rot, "poder": poder_de(n), "cuerpo": cuerpo,
                  "esc": [e for e in esc if e[0] < n][-1][1]})

por_brazo = {}
for it in items:
    por_brazo.setdefault(it["poder"], []).append(it)
for p, v in sorted(por_brazo.items(), key=lambda x: str(x[0])):
    log("    brazo poder=%-4s -> %d transcripciones" % (p, len(v)))
log()

# ── codificacion de directez ────────────────────────────────────────────
log("§4 · CODIFICACION DE DIRECTEZ (regla congelada, aplicada linea por linea)")
for it in items:
    texto = " ".join(it["cuerpo"])
    hit = RX_CAB.search(texto)
    it["directo"] = bool(hit)
    it["marca"] = hit.group(0) if hit else ""
    log("  %-14s escenario=%-16s poder=%-3s -> %-9s %s"
        % (it["rot"].rstrip(":"), it["esc"], it["poder"] or "?",
           "DIRECTO" if it["directo"] else "INDIRECTO",
           ("cabeza: '%s'" % it["marca"]) if it["directo"] else ""))
log()

# ── tasas por brazo ─────────────────────────────────────────────────────
log("§5 · TASAS POR BRAZO")
res = {}
for p in ("+", "-"):
    v = [it for it in items if it["poder"] == p]
    if not v:
        log("  brazo poder=%s : VACIO" % p)
        continue
    ind = sum(1 for it in v if not it["directo"])
    res[p] = (ind, len(v))
    lo, hi = sps.beta.ppf([0.025, 0.975], ind + 0.5, len(v) - ind + 0.5)
    log("  brazo poder=%s : indirectos %d de %d = %.2f pp   IC95%% Jeffreys [%.2f, %.2f]"
        % (p, ind, len(v), 100.0 * ind / len(v), 100 * lo, 100 * hi))

log()
log("§6 · DECISION contra el Umbral (|dif| < %.0f pp)" % UMBRAL_PP)
if "+" in res and "-" in res:
    (i1, n1), (i0_, n0) = res["+"], res["-"]
    d = 100.0 * (i1 / n1 - i0_ / n0)
    tab = [[i1, n1 - i1], [i0_, n0 - i0_]]
    odds, p = sps.fisher_exact(tab)
    se = 100.0 * ((i1 / n1 * (1 - i1 / n1) / n1 + i0_ / n0 * (1 - i0_ / n0) / n0) ** 0.5)
    log("  tasa(+P) = %.2f pp   tasa(-P) = %.2f pp" % (100.0 * i1 / n1, 100.0 * i0_ / n0))
    log("  diferencia (+P menos -P)                      : %.2f pp" % d)
    log("  EE de la diferencia (Wald, muestra no probabilistica): %.2f pp" % se)
    log("  IC95%% Wald                                    : [%.2f, %.2f]"
        % (d - 1.96 * se, d + 1.96 * se))
    log("  Fisher exacto 2x2, p = %.4f" % p)
    log("  tabla 2x2 [indirecto, directo] por brazo      : +P %s / -P %s" % (tab[0], tab[1]))
    cruza = (d - 1.96 * se) < UMBRAL_PP < (d + 1.96 * se)
    if abs(d) < UMBRAL_PP and not cruza:
        log("  RAMA 1 -> fila A")
    elif abs(d) >= UMBRAL_PP and not cruza:
        log("  RAMA 2 -> fila B")
    else:
        log("  RAMA 4 -> NO ADJUDICA: el IC95%% cruza el umbral de %.0f pp" % UMBRAL_PP)
else:
    log("  RAMA 3 -> fila D: al menos un brazo vacio")
log()

# ── control: las otras dos paginas ──────────────────────────────────────
log("§7 · CONTROL — las otras dos paginas del corpus Brasdefer")
for fn in ("encuentros_de_servicio.html", "convelic_conversaciones.html"):
    ls = plano(fn)
    r = [l for l in ls if re.match(r"^Rechazos?\s*\d", l)]
    log("  %-32s lineas=%-5d marcas 'Rechazo N'=%d" % (fn, len(ls), len(r)))
log("  control positivo del mismo patron sobre actos_de_habla.html: %d marcas"
    % len([l for l in lineas if re.match(r"^Rechazos?\s*\d", l)]))
log()

# ── transcripciones integras, para auditar la codificacion a mano ───────
log("=" * 78)
log("§8 · LAS %d TRANSCRIPCIONES MEXICANAS, INTEGRAS" % len(items))
log("=" * 78)
for it in items:
    log()
    log("── %s | escenario %s | poder %s | codificado %s"
        % (it["rot"].rstrip(":"), it["esc"], it["poder"],
           "DIRECTO" if it["directo"] else "INDIRECTO"))
    for l in it["cuerpo"]:
        log("   " + l)
log()
log("=" * 78)
OUT.close()
print("\nsalida cruda -> " + SAL)
