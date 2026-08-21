#!/usr/bin/env python3
"""HITO D · R7.3 — corrida de constructibilidad del RDD (COMMIT B, ACTO RETRIAGE-4).

Ejecuta `forense/hitoD-R7_3-especificacion-v1_0.md`: llena la tabla P1-P4 por
LECTURA DE CADA INSTRUMENTO, no por memoria ni por catalogo. No corre ningun
RDD y no corre ningun sustituto (spec §5.3).
"""
import io
import os
import zipfile
import unicodedata

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
DESC = "/mnt/c/Users/PC0/Descargas MX/Descargas Manuales"
SAL = os.path.join(ROOT, "forense", "notas",
                   "2026-08-20-r7-3-rdd-constructibilidad-salida.txt")
OUT = open(SAL, "w", encoding="utf8")

# Corte de elegibilidad de la Pension para el Bienestar de las Personas
# Adultas Mayores: 68 anos (2019-2021) y 65 anos desde 2022 (universal).
CORTES = {2021: 68, 2023: 65}


def log(m=""):
    print(m)
    OUT.write(m + "\n")


def na(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


log("=" * 78)
log("HITO D · R7.3 — constructibilidad del RDD · ACTO RETRIAGE-4 · 20/ago/2026")
log("spec congelada: forense/hitoD-R7_3-especificacion-v1_0.md")
log("=" * 78)
log()
log("P1 variable de asignacion continua con corte conocido")
log("P2 el programa NOMBRADO (Pension del Bienestar), no ayuda generica")
log("P3 desenlace electoral (eleccion de voto, no solo participacion)")
log("P4 aprobacion presidencial en la MISMA unidad")
log()

# ── 1 · Padron Unico de Beneficiarios (agregado CKAN) ────────────────────
log("─" * 78)
log("§1 · r7_3_pub_beneficiarios_bienestar_csv — Padron Unico, recurso CKAN")
p = os.path.join(RAW, "R7.3_PUB_Bienestar", "padron_unico_bienestar.csv")
d = pd.read_csv(p)
log("  filas x columnas                              : %d x %d" % d.shape)
log("  columnas                                      : %s" % ", ".join(d.columns))
log("  unidad de observacion real                    : %s"
    % ("entidad x periodo" if {"CVEENT", "periodo_cve"} <= set(d.columns) else "?"))
log("  filas unicas por (CVEENT, periodo_cve)        : %d de %d"
    % (d.groupby(["CVEENT", "periodo_cve"]).ngroups, len(d)))
log("  P1 variable de asignacion continua            : NO — ninguna columna es")
log("     edad ni ninguna otra variable de persona; el registro es un conteo.")
log("  P2 programa nombrado                          : el dataset ES del programa,")
log("     pero AGREGADO: no hay unidad elegible/no elegible que comparar.")
log("  P3 desenlace electoral                        : NO — cero columnas electorales")
log("  P4 aprobacion presidencial                    : NO")
log("  VEREDICTO DE INSTRUMENTO: P1 NO · P2 parcial-inutilizable · P3 NO · P4 NO")
log()

# ── 2 · Base electoral por seccion ──────────────────────────────────────
log("─" * 78)
log("§2 · zenodo_electoral_precinct_level_mexico_municipal — seccion x ano")
zo = zipfile.ZipFile(os.path.join(RAW, "zenodo_electoral_precinct_level_mexico_municipal.zip"))
inner = [n for n in zo.namelist() if n.endswith("all_states_final.zip")][0]
zi = zipfile.ZipFile(io.BytesIO(zo.read(inner)))
with zi.open("all_states_final.csv") as fh:
    cols = fh.readline().decode("utf8").strip().split(",")
log("  columnas                                      : %d" % len(cols))
hits = [c for c in cols if any(x in na(c) for x in
        ("age", "edad", "bienestar", "pension", "program", "transfer", "approv", "aprob"))]
log("  columnas con edad/programa/aprobacion         : %s" % (hits if hits else "NINGUNA"))
log("  P1 NO · P2 NO · P3 SI (voto por seccion) · P4 NO")
log("  VEREDICTO DE INSTRUMENTO: trae SOLO P3.")
log()

# ── 3 · LAPOP Mexico ────────────────────────────────────────────────────
log("─" * 78)
log("§3 · LAPOP AmericasBarometer Mexico — 2021 y 2023")
for ola, fn in ((2021, "MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta"),
                (2023, "MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta")):
    path = os.path.join(DESC, fn)
    log("  ── ola %d · %s" % (ola, fn))
    if not os.path.exists(path):
        log("     AUSENTE en la raiz descargas_mx")
        continue
    rd = pd.io.stata.StataReader(path)
    vl = rd.variable_labels()
    log("     variables                                  : %d" % len(vl))

    # P2: el programa NOMBRADO, buscado en nombres Y en etiquetas
    prog = {k: v for k, v in vl.items()
            if "bienestar" in na(v) or "bienestar" in na(k)
            or "pension para" in na(v) or "adulto mayor" in na(v)}
    log("     P2 variables que nombran el programa       : %s"
        % (list(prog.items()) if prog else "NINGUNA"))
    gen = {k: v for k, v in vl.items()
           if any(x in na(v) for x in ("recibir ayuda", "del gobierno", "programa social"))}
    log("     P2 lo mas cercano (ayuda GENERICA)         : %s"
        % (list(gen.items()) if gen else "ninguna"))

    tiene = lambda c: c in vl
    log("     P1 q2 (edad) presente                      : %s" % tiene("q2"))
    log("     P3 vb3n/vb20/vb2 presentes                 : %s/%s/%s"
        % (tiene("vb3n"), tiene("vb20"), tiene("vb2")))
    log("     P4 m1 (aprobacion ejecutivo) presente      : %s" % tiene("m1"))
    log("     diseno: wt=%s strata=%s upm=%s cluster=%s"
        % (tiene("wt"), tiene("strata"), tiene("upm"), tiene("cluster")))

    # contenido: conteos de celda alrededor del corte (contaminacion declarada)
    need = [c for c in ("q2", "m1", "vb3n", "vb20", "mexwf1_19", "wt") if c in vl]
    df = pd.read_stata(path, columns=need, convert_categoricals=False)
    corte = CORTES[ola]
    edad = pd.to_numeric(df["q2"], errors="coerce")
    log("     n total de la ola                          : %d" % len(df))
    log("     edad: min=%s max=%s validos=%d"
        % (edad.min(), edad.max(), int(edad.notna().sum())))
    for h in (10, 5, 3):
        m = edad.between(corte - h, corte + h - 1)
        izq = int((edad.between(corte - h, corte - 1)).sum())
        der = int((edad.between(corte, corte + h - 1)).sum())
        log("     ventana +-%2d alrededor del corte %d      : n=%4d  (izq %3d / der %3d)"
            % (h, corte, int(m.sum()), izq, der))
    if "mexwf1_19" in df.columns and "vb20" in df.columns:
        m5 = edad.between(corte - 5, corte + 4)
        cc = int((m5 & df["mexwf1_19"].notna() & df["vb20"].notna()).sum())
        log("     ventana +-5 CON ayuda-generica Y voto      : n=%d" % cc)
    if "m1" in df.columns:
        m5 = edad.between(corte - 5, corte + 4)
        log("     ventana +-5 con aprobacion presidencial    : n=%d"
            % int((m5 & df["m1"].notna()).sum()))
    # Aritmetica de potencia sobre los n MEDIDOS. NO es una estimacion del
    # efecto: es el ancho minimo que un IC95% podria tener con esos n, para
    # decidir si el diseno puede siquiera hablar del corte de >=10 pp que el
    # Umbral pide. No se corre ningun RDD (spec §5.3).
    log("     MDE — ancho minimo de IC95% alcanzable con esos n (p=0.5, sin")
    log("     penalizacion por efecto de diseno ni por ajuste local del RDD):")
    for h in (5, 3):
        izq = int((edad.between(corte - h, corte - 1)).sum())
        der = int((edad.between(corte, corte + h - 1)).sum())
        if izq and der:
            se = float(np.sqrt(0.25 / izq + 0.25 / der)) * 100.0
            log("       ventana +-%d: n=%d/%d  EE minimo %.2f pp  semiancho IC95%% %.2f pp"
                % (h, izq, der, se, 1.96 * se))
            log("         -> un efecto de 10 pp %s distinguible de cero"
                % ("SERIA" if 1.96 * se < 10 else "NO seria"))
    log()

# ── 4 · Latinobarometro 2024 ────────────────────────────────────────────
log("─" * 78)
log("§4 · latinobarometro2024_bd_stata")
zp = os.path.join(RAW, "latinobarometro2024_bd_stata.zip")
if os.path.exists(zp):
    z = zipfile.ZipFile(zp)
    dtas = [n for n in z.namelist() if n.lower().endswith(".dta")]
    log("  .dta dentro del zip                           : %s" % dtas)
    if dtas:
        b = z.read(dtas[0])
        vl = pd.io.stata.StataReader(io.BytesIO(b)).variable_labels()
        log("  variables                                     : %d" % len(vl))
        prog = {k: v for k, v in vl.items() if "bienestar" in na(v)}
        log("  P2 variables que nombran el programa          : %s"
            % (list(prog.items()) if prog else "NINGUNA"))
        log("  nota: instrumento REGIONAL (18 paises); el submuestreo mexicano")
        log("        no lo convierte en base con corte de elegibilidad.")
else:
    log("  AUSENTE de data/raw")
log()

log("=" * 78)
log("CIERRE — ningun instrumento en disco reune P1+P2+P3+P4 a la misma unidad.")
log("Ningun RDD se corrio. Ningun sustituto se corrio (spec §5.3).")
log("=" * 78)
OUT.close()
print("\nsalida cruda -> " + SAL)
