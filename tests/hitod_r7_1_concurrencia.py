#!/usr/bin/env python3
"""HITO D · R7.1 — corrida del falsador (COMMIT B de ACTO RETRIAGE-4).

Ejecuta al pie de la letra `forense/hitoD-R7_1-especificacion-v1_0.md`:
participacion por seccion electoral en elecciones municipales concurrentes
(ano federal) contra no concurrentes, pareando por la MISMA seccion.

No se teclea ninguna cifra: todo sale de este script. Salida cruda completa
a `forense/notas/2026-08-20-r7-1-concurrencia-salida.txt`.

Instrumento (solo lectura, nunca se escribe en data/raw):
  data/raw/zenodo_electoral_precinct_level_mexico_municipal.zip
    -> Final Data/all_states_final.zip -> all_states_final.csv
"""
import io
import os
import sys
import zipfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(ROOT, "data", "raw",
                   "zenodo_electoral_precinct_level_mexico_municipal.zip")

# Anos de eleccion federal en Mexico (diputados cada 3 anos). Identidad
# equivalente y auditable en una linea: year % 3 == 2.
FEDERALES = [1994, 1997, 2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2024]
assert all(y % 3 == 2 for y in FEDERALES)

UMBRAL_PP = 15.0
NOPARSE = {}

EDO = {1:"Aguascalientes",2:"Baja California",3:"Baja California Sur",4:"Campeche",
       5:"Coahuila",6:"Colima",7:"Chiapas",8:"Chihuahua",9:"Ciudad de Mexico",
       10:"Durango",11:"Guanajuato",12:"Guerrero",13:"Hidalgo",14:"Jalisco",
       15:"Mexico",16:"Michoacan",17:"Morelos",18:"Nayarit",19:"Nuevo Leon",
       20:"Oaxaca",21:"Puebla",22:"Queretaro",23:"Quintana Roo",24:"San Luis Potosi",
       25:"Sinaloa",26:"Sonora",27:"Tabasco",28:"Tamaulipas",29:"Tlaxcala",
       30:"Veracruz",31:"Yucatan",32:"Zacatecas"}


def log(msg=""):
    print(msg)
    OUT.write(msg + "\n")


# ── carga ────────────────────────────────────────────────────────────────
def carga():
    zo = zipfile.ZipFile(ZIP)
    inner = [n for n in zo.namelist() if n.endswith("all_states_final.zip")][0]
    zi = zipfile.ZipFile(io.BytesIO(zo.read(inner)))
    import csv
    with zi.open("all_states_final.csv") as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding="utf8", errors="replace"))
        hdr = next(rd)
        ix = {c: i for i, c in enumerate(hdr)}
        need = ("state_code", "mun_code", "year", "precinct",
                "registered_voters", "total", "turnout")
        for c in need:
            if c not in ix:
                sys.exit("columna ausente en el instrumento: " + c)
        crudas = 0
        st, mu, yr, pr, rv, to, tu = [], [], [], [], [], [], []
        for row in rd:
            crudas += 1
            try:
                s = int(row[ix["state_code"]]); m = int(row[ix["mun_code"]])
                y = int(row[ix["year"]]);       p = row[ix["precinct"]].strip()
                r = float(row[ix["registered_voters"]])
                t = float(row[ix["total"]])
            except (ValueError, IndexError):
                for c, lbl in (("state_code", "state_code"), ("mun_code", "mun_code"),
                               ("year", "year"), ("registered_voters", "registered_voters"),
                               ("total", "total")):
                    try:
                        float(row[ix[c]])
                    except (ValueError, IndexError):
                        NOPARSE[lbl] = NOPARSE.get(lbl, 0) + 1
                continue
            v = row[ix["turnout"]].strip()
            try:
                tt = float(v)
            except ValueError:
                tt = np.nan
            st.append(s); mu.append(m); yr.append(y); pr.append(p)
            rv.append(r); to.append(t); tu.append(tt)
    return (crudas, np.array(st, np.int32), np.array(mu, np.int32),
            np.array(yr, np.int32), np.array(pr, dtype=object),
            np.array(rv), np.array(to), np.array(tu))


# ── estimadores ──────────────────────────────────────────────────────────
def media_cluster(vals, clus):
    """Media de `vals` con EE cluster-robusto (CR1) por `clus`, e IC95% con
    t de G-1 grados de libertad. Es la regresion de vals sobre una constante."""
    from scipy import stats as sps
    n = len(vals)
    m = float(vals.mean())
    u = vals - m
    gs = np.unique(clus)
    G = len(gs)
    meat = 0.0
    for g in gs:
        meat += float(u[clus == g].sum()) ** 2
    c = (G / (G - 1.0)) * ((n - 1.0) / (n - 1.0))          # K=1
    var = c * meat / (n ** 2)
    se = float(np.sqrt(var))
    tcrit = float(sps.t.ppf(0.975, G - 1))
    return m, se, m - tcrit * se, m + tcrit * se, n, G


def dif_medias_cluster(y, w, clus):
    """b de y = a + b*w con EE cluster-robusto CR1 por `clus`. Con w binaria,
    b = media(y|w=1) - media(y|w=0)."""
    from scipy import stats as sps
    n = len(y)
    X = np.column_stack([np.ones(n), w.astype(float)])
    XtX = X.T @ X
    XtXi = np.linalg.inv(XtX)
    beta = XtXi @ (X.T @ y)
    u = y - X @ beta
    gs = np.unique(clus)
    G = len(gs)
    meat = np.zeros((2, 2))
    for g in gs:
        sel = clus == g
        Xg = X[sel]; ug = u[sel]
        sg = Xg.T @ ug
        meat += np.outer(sg, sg)
    c = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))          # K=2
    V = c * (XtXi @ meat @ XtXi)
    se = float(np.sqrt(V[1, 1]))
    b = float(beta[1])
    tcrit = float(sps.t.ppf(0.975, G - 1))
    return b, se, b - tcrit * se, b + tcrit * se, n, G


def parea(keys, y, w, st, min_por_brazo=1):
    """Delta_i por llave de electorado. Devuelve (deltas, cluster_estado, n_llaves)."""
    orden = np.argsort(keys, kind="stable")
    k = keys[orden]; yy = y[orden]; ww = w[orden]; ss = st[orden]
    bordes = np.flatnonzero(np.r_[True, k[1:] != k[:-1], True])
    d, cl = [], []
    for a, b in zip(bordes[:-1], bordes[1:]):
        m1 = ww[a:b] == 1
        n1 = int(m1.sum()); n0 = (b - a) - n1
        if n1 < min_por_brazo or n0 < min_por_brazo:
            continue
        d.append(yy[a:b][m1].mean() - yy[a:b][~m1].mean())
        cl.append(ss[a])
    return np.array(d), np.array(cl), len(d)


def linea(rot, r):
    m, se, lo, hi, n, G = r
    log("  %-46s %8.4f pp   EE %6.4f   IC95%% [%8.4f, %8.4f]   n=%-8d G=%d"
        % (rot, m, se, lo, hi, n, G))
    return m, se, lo, hi, n, G


# ── main ─────────────────────────────────────────────────────────────────
SAL = os.path.join(ROOT, "forense", "notas",
                   "2026-08-20-r7-1-concurrencia-salida.txt")
OUT = open(SAL, "w", encoding="utf8")

log("=" * 78)
log("HITO D · R7.1 — corrida del falsador · ACTO RETRIAGE-4 · 20/ago/2026")
log("spec congelada: forense/hitoD-R7_1-especificacion-v1_0.md")
log("=" * 78)
log()

crudas, st, mu, yr, pr, rv, to, tu = carga()
log("§1 · UNIVERSO")
log("  filas crudas del CSV                          : %d" % crudas)
log("  filas parseables                              : %d" % len(st))
log("  filas NO parseables                           : %d" % (crudas - len(st)))
for kk, vv in sorted(NOPARSE.items(), key=lambda x: -x[1]):
    log("      campo no numerico: %-22s %d" % (kk, vv))

# universo pre-registrado (spec §4)
ok = (rv > 0) & np.isfinite(to) & (pr != "") & (pr != "NA")
log("  excluidas por registered_voters<=0            : %d" % int((rv <= 0).sum()))
log("  excluidas por total ausente                   : %d" % int((~np.isfinite(to)).sum()))
log("  excluidas por precinct ausente                : %d" % int(((pr == "") | (pr == "NA")).sum()))
st, mu, yr, pr, rv, to, tu = (a[ok] for a in (st, mu, yr, pr, rv, to, tu))
log("  UNIVERSO REAL (filas)                         : %d" % len(st))
log("  anos presentes                                : %d..%d (%d distintos)"
    % (yr.min(), yr.max(), len(np.unique(yr))))
log("  estados                                       : %d" % len(np.unique(st)))

y = 100.0 * to / rv
w = (yr % 3 == 2).astype(np.int8)
log("  filas concurrentes (year%%3==2)                : %d" % int(w.sum()))
log("  filas no concurrentes                         : %d" % int((1 - w).sum()))
log("  anos concurrentes observados                  : %s"
    % sorted(set(int(v) for v in np.unique(yr[w == 1]))))
log("  anos NO concurrentes observados               : %s"
    % sorted(set(int(v) for v in np.unique(yr[w == 0]))))
log()

log("§2 · CONTROL DE CANALIZACION — turnout recalculado vs. publicado")
fin = np.isfinite(tu)
dif = np.abs(y[fin] / 100.0 - tu[fin])
log("  filas con turnout publicado                   : %d" % int(fin.sum()))
log("  |recalculado - publicado| max                 : %.10f" % float(dif.max()))
log("  filas con diferencia > 1e-6                   : %d" % int((dif > 1e-6).sum()))
log("  -> la columna publicada ES total/registered_voters: %s"
    % ("SI" if dif.max() < 1e-5 else "NO"))
log()

# outliers de participacion imposible
imp = int((y > 100.0).sum())
log("  filas con participacion > 100%%                : %d" % imp)
log()

llave_sec = np.array(["%02d|%05d|%s" % (a, b, c) for a, b, c in zip(st, mu, pr)], dtype=object)
llave_mun = np.array(["%02d|%05d" % (a, b) for a, b in zip(st, mu)], dtype=object)

log("§3 · PRIMARIO — diferencia pareada dentro de SECCION (spec §5.1)")
d, cl, nk = parea(llave_sec, y, w, st, 1)
if nk == 0:
    log("  CERO secciones con ambos brazos -> rama 4 de la spec (fila C)")
    prim = None
else:
    prim = linea("Delta pareado (concurrente - no concurrente)",
                 media_cluster(d, cl))
    log("  secciones pareadas                            : %d" % nk)
    log("  estados que aportan secciones pareadas        : %d" % len(np.unique(cl)))
log()

log("§4 · MARGINAL — diferencia de medias sin parear (spec §5.2, obligatorio)")
marg = linea("Delta marginal (concurrente - no concurrente)",
             dif_medias_cluster(y, w, st))
log("  media participacion, concurrentes             : %.4f pp" % float(y[w == 1].mean()))
log("  media participacion, NO concurrentes          : %.4f pp" % float(y[w == 0].mean()))
log()

log("§5 · SENSIBILIDADES PRE-DECLARADAS (spec §7)")
log("  S2 · misma prueba con la unidad agregada a MUNICIPIO")
ym = {}
for k, vy, vw, vs in zip(llave_mun, y, w, st):
    a = ym.setdefault((k, int(vw)), [0.0, 0, int(vs)])
    a[0] += vy; a[1] += 1
km = np.array([k for (k, _) in ym.keys()], dtype=object)
wm = np.array([v for (_, v) in ym.keys()], dtype=np.int8)
yv = np.array([a[0] / a[1] for a in ym.values()])
sm = np.array([a[2] for a in ym.values()], np.int32)
dm, clm, nm = parea(km, yv, wm, sm, 1)
if nm:
    s2 = linea("S2 Delta pareado por municipio", media_cluster(dm, clm))
    log("      municipios pareados                       : %d" % nm)
else:
    s2 = None
    log("      CERO municipios con ambos brazos")

log("  S3 · secciones con >=2 observaciones en CADA brazo")
d3, cl3, n3 = parea(llave_sec, y, w, st, 2)
s3 = linea("S3 Delta pareado (>=2 por brazo)", media_cluster(d3, cl3)) if n3 else None
if n3:
    log("      secciones                                 : %d" % n3)
else:
    log("      CERO secciones cumplen >=2 por brazo")

log("  S4 · solo observaciones de 2015 en adelante (alineacion post-reforma)")
m4 = yr >= 2015
if m4.sum():
    d4, cl4, n4 = parea(llave_sec[m4], y[m4], w[m4], st[m4], 1)
    s4 = linea("S4 Delta pareado (>=2015)", media_cluster(d4, cl4)) if n4 else None
    if n4:
        log("      secciones                                 : %d" % n4)
    else:
        log("      CERO secciones con ambos brazos desde 2015")
else:
    s4 = None
    log("      sin observaciones desde 2015")

log("  S5 · par de anos mas cercano, separado por <=6 anos")
orden = np.argsort(llave_sec, kind="stable")
k5 = llave_sec[orden]; y5 = y[orden]; w5 = w[orden]; s5s = st[orden]; yr5 = yr[orden]
b5 = np.flatnonzero(np.r_[True, k5[1:] != k5[:-1], True])
d5, cl5 = [], []
for a, b in zip(b5[:-1], b5[1:]):
    m1 = w5[a:b] == 1
    if not m1.any() or m1.all():
        continue
    yc = yr5[a:b][m1]; vc = y5[a:b][m1]
    yn = yr5[a:b][~m1]; vn = y5[a:b][~m1]
    gap = np.abs(yc[:, None] - yn[None, :])
    i, j = np.unravel_index(np.argmin(gap), gap.shape)
    if gap[i, j] <= 6:
        d5.append(vc[i] - vn[j]); cl5.append(s5s[a])
d5 = np.array(d5); cl5 = np.array(cl5)
s5 = linea("S5 Delta par mas cercano (<=6 anos)", media_cluster(d5, cl5)) if len(d5) else None
if len(d5):
    log("      secciones                                 : %d" % len(d5))
else:
    log("      CERO secciones con par a <=6 anos")
log()

log("§6 · A-bis r4 — el universo del pareado NO es el universo completo")
pares_ok = set()
orden6 = np.argsort(llave_sec, kind="stable")
k6 = llave_sec[orden6]; w6 = w[orden6]
b6 = np.flatnonzero(np.r_[True, k6[1:] != k6[:-1], True])
for a, b in zip(b6[:-1], b6[1:]):
    m1 = w6[a:b] == 1
    if m1.any() and not m1.all():
        pares_ok.add(k6[a])
enpar = np.array([k in pares_ok for k in llave_sec])
log("  filas del universo completo                   : %d" % len(y))
log("  filas dentro de secciones pareadas            : %d" % int(enpar.sum()))
pres = sorted(set(int(v) for v in np.unique(st)))
falt = [c for c in range(1, 33) if c not in pres]
log("  estados del universo completo (%d)             : %s" % (len(pres), pres))
log("  estado(s) AUSENTE(s) del instrumento          : %s"
    % ", ".join("%d %s" % (c, EDO[c]) for c in falt))
ppar = sorted(set(int(v) for v in np.unique(st[enpar])))
log("  estados que aportan secciones pareadas (%d)    : %s"
    % (len(ppar), ", ".join("%d %s" % (c, EDO[c]) for c in ppar)))
log("  estados SIN variacion de regimen (%d)          : %s"
    % (len(pres) - len(ppar),
       ", ".join("%d %s" % (c, EDO[c]) for c in pres if c not in ppar)))
log("  -> el pareado esta ACOTADO a esa subpoblacion; A-bis r4 exige recalcular")
log("     el marginal SOBRE EL MISMO UNIVERSO, y no compararlo contra el nacional.")
margR = linea("Marginal RECALCULADO sobre el universo pareado",
              dif_medias_cluster(y[enpar], w[enpar], st[enpar]))
log()

log("§6-bis · DIAGNOSTICO POST-HOC, NO PRE-REGISTRADO — participacion > 100%%")
log("  La spec no anticipo filas con total > registered_voters. Se reportan")
log("  por separado y NO sustituyen al primario (la spec no se corrige hacia atras).")
val = y <= 100.0
log("  filas excluidas por y>100pp                   : %d (%.3f%% del universo)"
    % (int((~val).sum()), 100.0 * float((~val).sum()) / len(y)))
dph, clph, nph = parea(llave_sec[val], y[val], w[val], st[val], 1)
if nph:
    linea("POST-HOC Delta pareado (y<=100pp)", media_cluster(dph, clph))
    log("      secciones                                 : %d" % nph)
log()

log("§7 · DECISION contra el Umbral (<%.0f pp) — arbol de la spec §5.4" % UMBRAL_PP)
if prim is None:
    log("  RAMA 4 -> fila C")
else:
    m, se, lo, hi, n, G = prim
    log("  Delta primario  = %.4f pp    IC95%% [%.4f, %.4f]" % (m, lo, hi))
    if hi < UMBRAL_PP:
        log("  RAMA 1 -> fila A  (IC95%% ENTERO por debajo de %.0f pp)" % UMBRAL_PP)
    elif lo > UMBRAL_PP:
        log("  RAMA 2 -> fila B  (IC95%% ENTERO por encima de %.0f pp)" % UMBRAL_PP)
    else:
        log("  RAMA 3 -> NO ADJUDICA (el IC95%% cruza %.0f pp)" % UMBRAL_PP)
    log("  Discordancia marginal vs. pareado: marginal=%.4f pp, pareado=%.4f pp, "
        "brecha=%.4f pp" % (marg[0], m, marg[0] - m))
log()

log("§8 · VERIFICACION INDEPENDIENTE DEL EE — bootstrap por conglomerado (estado)")
log("  No pre-registrado: control adversarial del EE cluster-robusto de §3.")
rng = np.random.default_rng(20260820)
gs = np.unique(cl)
idx = {g: np.flatnonzero(cl == g) for g in gs}
reps = []
for _ in range(2000):
    pick = rng.choice(gs, size=len(gs), replace=True)
    reps.append(float(np.concatenate([d[idx[g]] for g in pick]).mean()))
reps = np.array(reps)
log("  bootstrap 2000 reps, semilla 20260820, remuestreo de %d estados" % len(gs))
log("  EE bootstrap                                  : %.4f pp  (CR1 dio %.4f)"
    % (float(reps.std(ddof=1)), prim[1]))
log("  IC95%% percentil                               : [%.4f, %.4f]"
    % (float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))))
log("  reps con Delta >= %.0f pp                        : %d de 2000"
    % (UMBRAL_PP, int((reps >= UMBRAL_PP).sum())))
log()
log("=" * 78)
OUT.close()
print("\nsalida cruda -> " + SAL)
