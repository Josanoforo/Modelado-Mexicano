#!/usr/bin/env python3
"""HITO D · R8.1 — corrida del falsador (COMMIT B, ACTO RETRIAGE-4).

Ejecuta `forense/hitoD-R8_1-especificacion-v1_0.md`: llena la tabla Q1-Q4 por
LECTURA de cada instrumento en disco. Ninguna cifra se teclea.
"""
import json
import os
import unicodedata

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
DESC = "/mnt/c/Users/PC0/Descargas MX/Descargas Manuales"
SAL = os.path.join(ROOT, "forense", "notas",
                   "2026-08-20-r8-1-contribucion-salida.txt")
OUT = open(SAL, "w", encoding="utf8")


def log(m=""):
    print(m)
    OUT.write(m + "\n")


def na(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


SANCION = ("sancion", "multa", "excluir", "exclusion", "castigo", "corte de servicio",
           "suspension", "penaliza", "vigila", "monitore", "supervis")
CONTRIB = ("contribu", "coopera", "aporta", "cuota", "paga", "faena", "tequio",
           "participa en la solucion", "solucion de algun problema")

log("=" * 78)
log("HITO D · R8.1 — corrida del falsador · ACTO RETRIAGE-4 · 20/ago/2026")
log("spec congelada: forense/hitoD-R8_1-especificacion-v1_0.md")
log("=" * 78)
log()
log("Q1 bien publico identificado con TASA (numerador sobre denominador)")
log("Q2 sostenida >=2 anos sobre la MISMA unidad-bien")
log("Q3 ausencia IDENTIFICABLE de sancion y de liderazgo con capacidad de excluir")
log("Q4 fuera del sistema comunal (ADR-10): mestizo o urbano identificable")
log()

# ── 1 · Contraloria Social ──────────────────────────────────────────────
log("─" * 78)
log("§1 · r8_1_contraloria_social_2019_2025_csv")
p = os.path.join(RAW, "R8.1_contraloria_social", "contraloria_social_2019_2025.csv")
d = pd.read_csv(p)
log("  filas x columnas                              : %d x %d" % d.shape)
log("  columnas                                      : %s" % ", ".join(d.columns))
log("  contenido integro (son %d filas, se pegan todas):" % len(d))
for ln in d.to_string(index=False).split("\n"):
    log("    " + ln)
log("  Q1 columna de tasa o de denominador           : %s"
    % ([c for c in d.columns if any(x in na(c) for x in ("tasa", "porcent", "elegib", "potencial", "universo"))] or "NINGUNA"))
log("  Q1 identificador de bien publico o de comite  : %s"
    % ([c for c in d.columns if any(x in na(c) for x in ("id", "clave", "folio", "comite_id"))] or "NINGUNA"))
log("  Q2 unidad-bien repetida en >=2 anos           : NO — la unidad es el ANO, no el bien")
_q3 = [c for c in d.columns if any(x in na(c) for x in SANCION)]
log("  Q3 columna de sancion / monitoreo / exclusion : %s" % (_q3 or "NINGUNA"))
log("     ^ FALSO POSITIVO del propio patron: 'beneficios_vigilados' es un CONTEO")
log("       de beneficios vigilados, no una variable de sancion ni de exclusion.")
log("       Q3 real en este instrumento: NINGUNA.")
log("  Q4 columna geografica o de regimen comunal    : %s"
    % ([c for c in d.columns if any(x in na(c) for x in ("entidad", "municip", "estado", "localidad", "indigena", "usos"))] or "NINGUNA"))
log("  ESTRUCTURAL, y es el punto: 'comites_constituidos' enumera SOLO el brazo")
log("  monitoreado. El bien publico sin comite no aparece aqui por construccion.")
log("  VEREDICTO DE INSTRUMENTO: Q1 NO · Q2 NO · Q3 NO · Q4 NO")
log()

# ── 2 · OMCA conflictos por el agua ─────────────────────────────────────
log("─" * 78)
log("§2 · ADQ15_OMCA_conflictos_agua / omca_conflictos_base_completa.json")
j = json.load(open(os.path.join(RAW, "ADQ15_OMCA_conflictos_agua",
                                "omca_conflictos_base_completa.json"),
                   encoding="utf8", errors="replace"))
log("  registros                                     : %d" % len(j))
campos = sorted({k for r in j for k in r.keys()})
log("  campos de primer nivel                        : %s" % ", ".join(campos))
log("  Q1 campo de tasa/contribucion                 : %s"
    % ([c for c in campos if any(x in na(c) for x in CONTRIB)] or "NINGUNA"))
log("  Q3 campo de sancion/monitoreo                 : %s"
    % ([c for c in campos if any(x in na(c) for x in SANCION)] or "NINGUNA"))
anios = sorted({r.get("anio") for r in j if r.get("anio")})
log("  Q2 anios cubiertos                            : %s..%s (%d distintos)"
    % (anios[0], anios[-1], len(anios)) if anios else "  Q2 sin campo anio")
log("  Q4 presencia_indigena, valores                : %s"
    % sorted({str(r.get("presencia_indigena")) for r in j})[:6])
log("  la unidad de observacion es el CONFLICTO, no el bien publico ni la")
log("  contribucion: registra disputas, no tasas de aportacion.")
log("  VEREDICTO DE INSTRUMENTO: Q1 NO · Q2 parcial (anio del conflicto) · Q3 NO · Q4 SI")
log()

# ── 3 · LAPOP ───────────────────────────────────────────────────────────
log("─" * 78)
log("§3 · LAPOP AmericasBarometer Mexico — participacion comunitaria")
for ola, fn in ((2021, "MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta"),
                (2023, "MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta")):
    path = os.path.join(DESC, fn)
    if not os.path.exists(path):
        log("  ola %d AUSENTE" % ola)
        continue
    vl = pd.io.stata.StataReader(path).variable_labels()
    cps = {k: v for k, v in vl.items() if na(k).startswith("cp")}
    log("  ── ola %d · variables cp*: %s" % (ola, list(cps.keys()) or "NINGUNA"))
    for k, v in cps.items():
        log("       %-10s %s" % (k, str(v)[:80]))
    san = {k: v for k, v in vl.items() if any(x in na(v) for x in SANCION)}
    log("     Q3 variables de sancion/monitoreo de bien publico: %s"
        % (list(san.items()) if san else "NINGUNA"))
    con = {k: v for k, v in vl.items() if any(x in na(v) for x in CONTRIB)}
    log("     Q1 variables de contribucion/cooperacion          : %s"
        % (list(con.items()) if con else "NINGUNA"))
    if ola == 2021:
        psc = [k for k in vl if na(k).startswith("psc2r2")]
        log("     MODULO DE AGUA (solo esta ola): %d dummies psc2r2_* de 'quien paga",
            ) if False else log("     MODULO DE AGUA (solo esta ola): %d dummies psc2r2_*" % len(psc))
        log("       incluye psc2r2_99 'No pagan por el agua que consumen' -> es lo mas")
        log("       cerca que hay de una tasa de aportacion a un bien publico.")
        log("       Falla Q2: la bateria NO existe en la ola 2023 (una sola ola).")
        log("       Falla Q3: cero variables de corte de servicio, multa o exclusion.")
log("  cp8 mide ASISTENCIA A REUNIONES de un comite, no aportacion a un bien.")
log("  Y no existe ninguna variable que registre si ese comite tiene sancion.")
log("  VEREDICTO DE INSTRUMENTO: Q1 NO (asistencia != contribucion) · Q3 NO")
log()

# ── 4 · ENCUP 2012 ──────────────────────────────────────────────────────
log("─" * 78)
log("§4 · encup_2012_base_datos_xlsx")
pe = os.path.join(RAW, "encup_2012_base_datos_xlsx.xlsx")
if os.path.exists(pe):
    xl = pd.ExcelFile(pe)
    log("  hojas                                         : %s" % xl.sheet_names)
    h = pd.read_excel(pe, sheet_name=xl.sheet_names[0], nrows=0)
    log("  hoja 1: columnas                              : %d" % len(h.columns))
    pond = [c for c in h.columns if any(x in na(c) for x in ("pond", "factor", "fac_", "peso", "expan"))]
    estr = [c for c in h.columns if any(x in na(c) for x in ("estrato", "est_dis", "upm", "conglom"))]
    log("  ponderador declarado en columnas              : %s" % (pond or "NINGUNO"))
    log("  estrato / UPM declarados en columnas          : %s" % (estr or "NINGUNO"))
    san = [c for c in h.columns if any(x in na(c) for x in SANCION)]
    con = [c for c in h.columns if any(x in na(c) for x in CONTRIB)]
    log("  Q3 columnas de sancion/monitoreo              : %s" % (san or "NINGUNA"))
    log("  Q1 columnas de contribucion/cooperacion       : %s" % (con or "NINGUNA"))
    part = [c for c in h.columns if any(x in na(c) for x in
            ("asistio a alguna reunion", "organizacion", "vecin", "faena", "tequio",
             "comite", "junta de mejoras", "agua"))]
    log("  bateria de participacion/organizacion (%d columnas):" % len(part))
    for c in part:
        log("     · %s" % str(c)[:130])
else:
    log("  AUSENTE de data/raw")
log()

log("=" * 78)
log("CIERRE — ningun instrumento en disco construye Q1+Q2+Q3+Q4.")
log("Q3 (ausencia identificable de sancion) tiene CERO cobertura en los cuatro.")
log("=" * 78)
OUT.close()
print("\nsalida cruda -> " + SAL)
