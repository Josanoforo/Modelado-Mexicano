#!/usr/bin/env python3
"""CAL-G3 · Fase C — estimación descriptiva sobre el panel ENNViH/MxFLS.

Ficha: `forense/hitoD-preregistro-v2_0.md`, Nota 7 + Adenda 1.
Alcance de esta corrida (decisiones de mesa, ver la nota fechada de Fase C):
  · Olas 2 (2005-06) y 3 (2009-12) únicamente. Ola 1 fuera (D-10, opción 1).
  · Entregable DESCRIPTIVO: sin veredicto de falsación, sin celda CAL, sin
    entrada al conteo de corridas (D-09, opción 3).
  · NO calibra el -0.60. `milpa/procedencia.yaml` no se toca.

TODA cifra que salga de aquí lleva pegada la ventana 2005-2012.

Insumos: los .zip de ENNViH bajo `data/raw/ennvih/` (no versionados). Sólo se
abren las tablas declaradas (CRH, TB) más las instrumentales que el primario
necesita y que la ficha no nombró — ver la sección "lecturas instrumentales"
de la nota. Sin dependencias: el entorno no tiene pandas, numpy ni pip.

Uso:  python3 tests/calg3_fasec.py [--salida RUTA]
"""
import argparse
import io
import math
import os
import struct
import sys
import zipfile
from collections import Counter

VENTANA = '2005-2012'
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, 'data', 'raw', 'ennvih')


# ===========================================================================
# 1 · Lector de Stata .dta, formatos 113/114 (Stata 8-10)
# ===========================================================================
class Dta:
    """Los missing de Stata se devuelven como None."""

    _MAXV = {251: 100, 252: 32740, 253: 2147483620,
             254: 1.701e38, 255: 8.9884656743e307}
    _FMT = {251: 'b', 252: 'h', 253: 'i', 254: 'f', 255: 'd'}

    def __init__(self, buf):
        self.buf = buf
        self.p = 0
        self._header()
        self._descriptors()
        self._expansion()
        self._data()

    def _take(self, n):
        b = self.buf[self.p:self.p + n]
        self.p += n
        return b

    def _u(self, fmt):
        return struct.unpack(self.bo + fmt, self._take(struct.calcsize(fmt)))[0]

    @staticmethod
    def _s(b):
        i = b.find(b'\x00')
        return (b[:i] if i >= 0 else b).decode('latin-1').strip()

    def _header(self):
        self.ver = self.buf[0]
        if self.ver not in (113, 114):
            raise ValueError('formato dta %d no soportado' % self.ver)
        self.bo = '>' if self.buf[1] == 1 else '<'
        self.p = 4
        self.nvar = self._u('h')
        self.nobs = self._u('i')
        self._s(self._take(81))
        self._s(self._take(18))

    def _descriptors(self):
        self.typlist = list(self._take(self.nvar))
        self.varlist = [self._s(self._take(33)) for _ in range(self.nvar)]
        self._take(2 * (self.nvar + 1))
        flen = 12 if self.ver == 113 else 49
        [self._s(self._take(flen)) for _ in range(self.nvar)]
        [self._s(self._take(33)) for _ in range(self.nvar)]
        self.varlabels = [self._s(self._take(81)) for _ in range(self.nvar)]

    def _expansion(self):
        while True:
            dt = self._u('b')
            ln = self._u('i')
            if dt == 0 and ln == 0:
                break
            self._take(ln)

    def _data(self):
        rows = []
        for _ in range(self.nobs):
            row = []
            for t in self.typlist:
                if t <= 244:
                    row.append(self._s(self._take(t)))
                else:
                    v = self._u(self._FMT[t])
                    row.append(None if v > self._MAXV[t] else v)
            rows.append(row)
        self.rows = rows

    def dicts(self):
        for r in self.rows:
            yield dict(zip(self.varlist, r))

    def col(self, name):
        i = self.varlist.index(name)
        return [r[i] for r in self.rows]


def abrir(zip_nombre, sufijo):
    """Abre por sufijo el único .dta que coincide dentro del zip."""
    ruta = os.path.join(DATOS, zip_nombre)
    if not os.path.exists(ruta):
        sys.exit('FALTA el insumo %s (los microdatos no se versionan)' % ruta)
    with zipfile.ZipFile(ruta) as zf:
        cand = [n for n in zf.namelist() if n.endswith(sufijo)]
        if len(cand) != 1:
            sys.exit('%s: %d coincidencias para %s' %
                     (zip_nombre, len(cand), sufijo))
        return Dta(zf.read(cand[0]))


# ===========================================================================
# 2 · Llaves de enlace entre olas
# ===========================================================================
# Esquema documentado en `guia_de_usuario_ennvih-3.pdf` §5.2.1 (pp. 41-46):
#   folio ola 3 (10) = base6 + [7] ronda de apertura (A=2002, B=2005, C=2009)
#                            + [8] P (miembro panel) / H (miembro nuevo)
#                            + [9-10] LS del miembro que se desprendió
#                              ("00" en hogares panel)
#   pid_link (12)    = folio del PRIMER hogar donde se registró la persona,
#                      más su LS original; "nunca cambia entre las rondas".
# En los archivos de la ola 2 el folio se graba con 8 dígitos, sin el bloque
# de dos letras: quitarlo reconstruye la llave de la ola 2.
#
# FILTRO OBLIGADO: un pid_link de ronda "C" identifica a alguien registrado por
# primera vez en 2009 — no puede tener registro en la ola 2. Sin el filtro, la
# normalización lo emparejaría por coincidencia de dígitos con una persona
# distinta (falso enlace).
RONDAS_ENLAZABLES = ('A', 'B')

norm_pid = {'w2': lambda p: p, 'w3': lambda p: p[:6] + p[8:12]}
norm_folio = {'w2': lambda f: f, 'w3': lambda f: f[:6] + f[8:10]}

FUENTES = {
    'w2': dict(datos='ehh05dta_all.zip', peso='ehh05lw_all.zip',
               crh='ehh05dta_b2/ii_crh.dta', tb='ehh05dta_b3a/iiia_tb.dta',
               port='ehh05dta_b3a/iiia_portad.dta', ls='ehh05dta_bc/c_ls.dta',
               wh='ehh05_lw_b2.dta', wi='ehh05_lw_b3a.dta',
               fh='fac_2l', fi='fac_3al'),
    'w3': dict(datos='ehh09dta_all.zip', peso='ehh09lw_all.zip',
               crh='ehh09dta_b2/ii_crh.dta', tb='ehh09dta_b3a/iiia_tb.dta',
               port='ehh09dta_b3a/iiia_portad.dta', ls='ehh09dta_bc/c_ls.dta',
               wh='ehh09_lw_b2.dta', wi='ehh09_lw_b3a.dta',
               fh='fac_2l', fi='fac_3al'),
}


# ===========================================================================
# 3 · Desenlace y exposición
# ===========================================================================
# CRH01 es multi-selección ("CIRCULE TODAS LAS QUE APLIQUEN", Adenda 1 a): el
# instrumento graba el número de opción si fue seleccionada y missing si no.
FORMAL_BASE = ['crh01_1b', 'crh01_1h']              # Banco (2), afores vol.(8)
BLOQUE_CAJAS = ['crh01_1c', 'crh01_1d', 'crh01_1i']  # coop.(3), caja(4), sol.(9)
INFORMAL_RESTO = ['crh01_1e', 'crh01_1f', 'crh01_1g', 'crh01_1j']
NINGUNO, OTRO = 'crh01_1a', 'crh01_1k'
TODAS = [NINGUNO] + FORMAL_BASE + BLOQUE_CAJAS + INFORMAL_RESTO + [OTRO]


def estado_ahorro(row, sens=False):
    """(estado de 4 categorías, indicador de algún acceso formal) o (None,None).

    Cuatro estados con el molde del ENIF (Adenda 1 b). `sens=True` aplica la
    ÚNICA sensibilidad admitida (Adenda 1 d): el bloque cooperativa + caja de
    ahorro + cajas solidarias pasa completo a formal.
    """
    formales = FORMAL_BASE + (BLOQUE_CAJAS if sens else [])
    informales = [v for v in BLOQUE_CAJAS + INFORMAL_RESTO if v not in formales]
    sel = {v: row.get(v) is not None for v in TODAS}
    if not any(sel.values()):
        return None, None                  # ninguna opción marcada: sin dato
    if sel[OTRO]:
        return None, None                  # Adenda 1 (c): faltante, no se imputa
    f = any(sel[v] for v in formales)
    i = any(sel[v] for v in informales)
    if f and i:
        return 'mixto', 1
    if f:
        return 'solo_formal', 1
    if i:
        return 'solo_informal', 0
    return ('ninguno', 0) if sel[NINGUNO] else (None, None)


def formalidad(row):
    """'formal' | 'informal' | 'ninguna' | None (sin TB33 respondido).

    FORMAL = tb33p_a ∨ tb33p_b ∨ tb33p_d. El "tb33p_d categorías 1-2" del
    punto (4) es un desliz de nombre ya registrado (Nota 8, `cola` D-10):
    tb33p_* es una batería de binarias, una por opción de respuesta.
    INFORMAL = contrato verbal sin IMSS, literal del punto (4).
    """
    if any(row.get(v) is not None for v in ('tb33p_a', 'tb33p_b', 'tb33p_d')):
        return 'formal'
    if row.get('tb33p_c') is not None:
        return 'informal'
    if any(row.get(v) is not None for v in
           ('tb33p_e', 'tb33p_f', 'tb33p_g', 'tb33p_h', 'tb33p_i')):
        return 'ninguna'
    return None


# ===========================================================================
# 4 · Estimadores (forma cerrada exacta para T=2)
# ===========================================================================
# * Probabilidad lineal con efectos fijos de hogar  ==  MCO en primeras
#   diferencias: dY = a + b·dX + e, donde "a" absorbe el efecto común de
#   periodo. EE robusto HC1 (cada hogar aporta una observación).
# * Logit condicional (Chamberlain): condicionando en que la unidad cambie de
#   desenlace, la verosimilitud condicional colapsa a un logit binario sobre
#   las unidades DISCORDANTES, P(Y sube) = L(g + b·dX). Newton-Raphson, VCE
#   sandwich.
Z = 1.959963984540054


def _solve(A, b):
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-14:
            raise ZeroDivisionError('matriz singular')
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [M[r][k] - f * M[c][k] for k in range(n + 1)]
    return [M[i][n] for i in range(n)]


def _inv(A):
    n = len(A)
    cols = [_solve(A, [1.0 if i == j else 0.0 for i in range(n)])
            for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def _sandwich(A, B):
    k = len(A)
    Ai = _inv(A)
    return [[sum(Ai[a][p] * B[p][q] * Ai[q][b]
                 for p in range(k) for q in range(k)) for b in range(k)]
            for a in range(k)]


def mco_hc1(X, y, w=None):
    n, k = len(X), len(X[0])
    w = w or [1.0] * n
    A = [[sum(w[i] * X[i][a] * X[i][b] for i in range(n)) for b in range(k)]
         for a in range(k)]
    beta = _solve(A, [sum(w[i] * X[i][a] * y[i] for i in range(n))
                      for a in range(k)])
    e = [y[i] - sum(beta[a] * X[i][a] for a in range(k)) for i in range(n)]
    B = [[sum((w[i] ** 2) * (e[i] ** 2) * X[i][a] * X[i][b] for i in range(n))
          for b in range(k)] for a in range(k)]
    V = _sandwich(A, B)
    c = n / (n - k) if n > k else 1.0
    return beta, [math.sqrt(c * V[a][a]) for a in range(k)]


def logit(X, y, w=None, iters=100, tol=1e-10):
    n, k = len(X), len(X[0])
    w = w or [1.0] * n
    beta = [0.0] * k
    p, S = [], []
    for _ in range(iters):
        p, S, g = [], [], [0.0] * k
        for i in range(n):
            eta = max(-30.0, min(30.0, sum(beta[a] * X[i][a]
                                           for a in range(k))))
            pi = 1.0 / (1.0 + math.exp(-eta))
            p.append(pi)
            S.append(w[i] * pi * (1 - pi))
            for a in range(k):
                g[a] += w[i] * (y[i] - pi) * X[i][a]
        H = [[sum(S[i] * X[i][a] * X[i][b] for i in range(n))
              for b in range(k)] for a in range(k)]
        step = _solve(H, g)
        beta = [beta[a] + step[a] for a in range(k)]
        if max(abs(s) for s in step) < tol:
            break
    A = [[sum(S[i] * X[i][a] * X[i][b] for i in range(n)) for b in range(k)]
         for a in range(k)]
    B = [[sum((w[i] ** 2) * ((y[i] - p[i]) ** 2) * X[i][a] * X[i][b]
              for i in range(n)) for b in range(k)] for a in range(k)]
    V = _sandwich(A, B)
    return beta, [math.sqrt(V[a][a]) for a in range(k)]


def lpm_fe(dx, dy, w=None):
    beta, se = mco_hc1([[1.0, d] for d in dx], [float(v) for v in dy], w)
    return dict(n=len(dx), beta=beta[1], se=se[1],
                ic=(beta[1] - Z * se[1], beta[1] + Z * se[1]))


def clogit_fe(dx, dy, w=None):
    idx = [i for i, d in enumerate(dy) if d != 0]
    if not idx:
        return dict(n_disc=0, error='sin unidades discordantes')
    xs = [dx[i] for i in idx]
    ys = [1.0 if dy[i] > 0 else 0.0 for i in idx]
    ws = [w[i] for i in idx] if w else None
    n_inf = sum(1 for v in xs if v != 0)
    if n_inf == 0 or len(set(xs)) < 2:
        return dict(n_disc=len(idx), n_informativas=n_inf,
                    error='sin variación de exposición entre discordantes')
    try:
        beta, se = logit([[1.0, v] for v in xs], ys, ws)
    except (ZeroDivisionError, OverflowError) as exc:
        return dict(n_disc=len(idx), n_informativas=n_inf, error=str(exc))
    lo, hi = beta[1] - Z * se[1], beta[1] + Z * se[1]
    return dict(n_disc=len(idx), n_informativas=n_inf, or_=math.exp(beta[1]),
                or_ic=(math.exp(lo), math.exp(hi)))


def autoprueba():
    """Los dos estimadores contra resultados de forma cerrada conocidos."""
    X, y = [], []
    for xv, (s, f) in [(1, (30, 20)), (0, (10, 40))]:
        X += [[1.0, float(xv)]] * (s + f)
        y += [1.0] * s + [0.0] * f
    b, se = logit(X, y)
    lor = math.log((30 / 20) / (10 / 40))
    woolf = math.sqrt(1 / 30 + 1 / 20 + 1 / 10 + 1 / 40)
    assert abs(b[1] - lor) < 1e-12, 'logit != log odds-ratio 2x2'
    assert abs(se[1] - woolf) < 1e-12, 'EE sandwich != Woolf en tabla saturada'
    b, _ = mco_hc1([[1.0, float(i)] for i in range(10)],
                   [1 + 2 * i for i in range(10)])
    assert abs(b[0] - 1) < 1e-9 and abs(b[1] - 2) < 1e-9, 'MCO exacto falla'
    ba, _ = mco_hc1([[1., 0.], [1., 1.], [1., 2.]], [1., 3., 4.], [1., 2., 3.])
    bb, _ = mco_hc1([[1., 0.], [1., 1.], [1., 1.], [1., 2.], [1., 2.], [1., 2.]],
                    [1., 3., 3., 4., 4., 4.])
    assert all(abs(x - y) < 1e-9 for x, y in zip(ba, bb)), 'ponderación falla'
    return 'autoprueba de estimadores: OK (logit=log-OR, EE=Woolf, MCO exacto,' \
           ' ponderado==replicado)'


# ===========================================================================
# 5 · Ensamblado del panel
# ===========================================================================
def cargar_ola(tag):
    F = FUENTES[tag]
    w = {'crh': {}, 'roster': {}, 'tb': {}, 'port': {}, 'tb_folio': {}}
    for r in abrir(F['datos'], F['crh']).dicts():
        w['crh'][r['folio']] = r
    for r in abrir(F['datos'], F['ls']).dicts():
        w['roster'][(r['folio'], r['ls'])] = r
    for r in abrir(F['datos'], F['tb']).dicts():
        w['tb'][(r['folio'], r['ls'])] = r
        w['tb_folio'].setdefault(r['folio'], []).append(r)
    for r in abrir(F['datos'], F['port']).dicts():
        w['port'][(r['folio'], r['ls'])] = r
    d = abrir(F['peso'], F['wh'])
    w['w_h'] = dict(zip(d.col('folio'), d.col(F['fh'])))
    d = abrir(F['peso'], F['wi'])
    w['w_i'] = {(f, l): v for f, l, v in
                zip(d.col('folio'), d.col('ls'), d.col(F['fi']))}
    return w


def jefes(w, tag):
    res, desc, dup = {}, Counter(), set()
    for (folio, ls), r in w['roster'].items():
        if r.get('ls05_1') != 1.0:               # parentesco con el jefe
            continue
        pid = r.get('pid_link')
        if not pid:
            desc['sin_pid_link'] += 1
            continue
        if tag == 'w3' and (len(pid) < 7 or pid[6] not in RONDAS_ENLAZABLES):
            desc['ronda_C_no_enlazable'] += 1
            continue
        k = norm_pid[tag](pid)
        if k in res:
            dup.add(k)
            desc['clave_duplicada'] += 1
            continue
        res[k] = dict(folio=folio, ls=ls, ros=r)
    for k in dup:
        res.pop(k, None)
    return res, desc


def _sin_entidad(w, folio, ls):
    """Único marcador de levantamiento fuera de México dentro de lo leído.

    La portada del Libro IIIA graba `ent` (entidad federativa). Una
    observación levantada en EE.UU. no puede traerla. Es COTA INFERIOR: el
    punto (6) de la ficha no nombró la variable con la que se identifica la
    diáspora, y este script no abre el módulo de migración.
    """
    p = w['port'].get((folio, ls))
    return p is not None and p.get('ent') is None


def algun_miembro_formal(w, folio):
    hay = False
    for r in w['tb_folio'].get(folio, []):
        if formalidad(r) == 'formal':
            return True
        hay = True
    return False if hay else None


def ensamblar():
    W = {t: cargar_ola(t) for t in ('w2', 'w3')}
    j2, _ = jefes(W['w2'], 'w2')
    j3, d3 = jefes(W['w3'], 'w3')
    comunes = set(j2) & set(j3)
    flujo = Counter(jefes_ola2=len(j2), jefes_ola3=len(j3),
                    ola3_ronda_C_no_enlazable=d3['ronda_C_no_enlazable'],
                    jefes_en_ambas_olas=len(comunes))
    filas, basal = [], []
    for pid in sorted(j2):
        d = j2[pid]
        r2 = W['w2']['tb'].get((d['folio'], d['ls']))
        f2 = formalidad(r2) if r2 else None
        h2 = W['w2']['crh'].get(d['folio'])
        e2, y2 = estado_ahorro(h2) if h2 else (None, None)
        elegible = f2 is not None and y2 is not None
        reg = dict(pid=pid, f2=f2, e2=e2, y2=y2, elegible=elegible,
                   sexo=d['ros'].get('ls04'), edu=d['ros'].get('ls14'),
                   edad=d['ros'].get('ls02_2'))
        basal.append(reg)
        if not elegible:
            continue
        if pid not in comunes:
            flujo['elegible_sin_jefatura_o_ausente_en_ola3'] += 1
            continue
        d3r = j3[pid]
        if (_sin_entidad(W['w2'], d['folio'], d['ls']) or
                _sin_entidad(W['w3'], d3r['folio'], d3r['ls'])):
            flujo['excluidos_sin_entidad_federativa'] += 1
            continue
        r3 = W['w3']['tb'].get((d3r['folio'], d3r['ls']))
        f3 = formalidad(r3) if r3 else None
        if f3 is None:
            flujo['sin_TB33_en_ola3'] += 1
            continue
        h3 = W['w3']['crh'].get(d3r['folio'])
        if h3 is None:
            flujo['sin_CRH_en_ola3'] += 1
            continue
        e3, y3 = estado_ahorro(h3)
        if y3 is None:
            flujo['composicion_no_construible_ola3'] += 1
            continue
        _, y2s = estado_ahorro(h2, sens=True)
        _, y3s = estado_ahorro(h3, sens=True)
        reg = dict(reg, f3=f3, e3=e3, y3=y3, y2s=y2s, y3s=y3s,
                   a2=algun_miembro_formal(W['w2'], d['folio']),
                   a3=algun_miembro_formal(W['w3'], d3r['folio']),
                   w_h_o2=W['w2']['w_h'].get(d['folio']),
                   w_h_o3=W['w3']['w_h'].get(d['folio']),
                   w_i_o2=W['w2']['w_i'].get((d['folio'], d['ls'])),
                   w_i_o3=W['w3']['w_i'].get((d3r['folio'], d3r['ls'])))
        filas.append(reg)
    flujo['elegibles_basal_ola2'] = sum(1 for b in basal if b['elegible'])
    flujo['muestra_analitica'] = len(filas)
    return filas, basal, flujo, W


# ===========================================================================
# 6 · Especificaciones y reporte
# ===========================================================================
EXPOSICIONES = [
    ('jefe-literal', 'formalidad del jefe, definición literal del punto (4): '
     'FORMAL = contrato escrito o IMSS; INFORMAL = contrato verbal sin IMSS; '
     '"ninguna de las anteriores" queda FUERA del contraste'),
    ('jefe-binaria', 'formalidad del jefe, lectura binaria: FORMAL vs '
     'NO-FORMAL (conserva "ninguna de las anteriores" en el grupo de '
     'comparación)'),
    ('algun-miembro', 'sensibilidad pre-registrada del punto (4): expuesto = '
     'algún miembro del hogar es FORMAL'),
]
DESENLACES = [
    ('base', 'algún acceso formal = Banco o cuentas voluntarias de afores '
     '(Adenda 1 c/e)'),
    ('sens-cajas', 'única sensibilidad admitida (Adenda 1 d): cooperativa + '
     'caja de ahorro + cajas solidarias pasan a FORMAL'),
]
PONDERADORES = [
    ('sin ponderar', None),
    ('fac_2l ola 2  (long., Libro II, hogar)', 'w_h_o2'),
    ('fac_2l ola 3  (long., Libro II, hogar)', 'w_h_o3'),
    ('fac_3al ola 2 (long., Libro IIIA, indiv.)', 'w_i_o2'),
    ('fac_3al ola 3 (long., Libro IIIA, indiv.)', 'w_i_o3'),
]


def expo(r, modo):
    if modo == 'jefe-literal':
        m = {'formal': 1, 'informal': 0}
        if r['f2'] not in m or r['f3'] not in m:
            return None
        return m[r['f2']], m[r['f3']]
    if modo == 'jefe-binaria':
        return int(r['f2'] == 'formal'), int(r['f3'] == 'formal')
    if r['a2'] is None or r['a3'] is None:
        return None
    return int(r['a2']), int(r['a3'])


def desenlace(r, modo):
    if modo == 'base':
        return r['y2'], r['y3']
    a, b = r.get('y2s'), r.get('y3s')
    return (a, b) if a is not None and b is not None else None


def subconjunto(filas, e_modo, d_modo, w_key):
    dx, dy, w = [], [], []
    for r in filas:
        x, y = expo(r, e_modo), desenlace(r, d_modo)
        if x is None or y is None:
            continue
        if w_key is not None:
            wv = r.get(w_key)
            if wv is None or wv <= 0:
                continue
            w.append(float(wv))
        dx.append(float(x[1] - x[0]))
        dy.append(y[1] - y[0])
    return dx, dy, (w if w_key is not None else None)


def reporte(filas, basal, flujo, W):
    out = []
    A = out.append
    A('CAL-G3 · FASE C · ESTIMACIÓN DESCRIPTIVA · VENTANA %s' % VENTANA)
    A('=' * 78)
    A('')
    A('Panel ENNViH/MxFLS, olas 2 (2005-06) y 3 (2009-12). La ola 1 queda')
    A('FUERA (D-10, opción 1): su módulo TB no es comparable y el instrumento')
    A('fabrica transiciones. Entregable DESCRIPTIVO (D-09, opción 3): sin')
    A('veredicto de falsación, sin celda CAL, sin entrada al conteo de')
    A('corridas. No calibra el -0.60 (ficha, punto 2, opción b).')
    A('')
    A('El módulo OC de la ola 3 no está en el manual de codificación, así que')
    A('el confundidor de OFERTA queda sin descartar y aplica la degradación')
    A('pre-registrada: NINGUNA cifra de este documento se lee como preferencia')
    A('temporal. Se lee como conducta bajo restricción de oferta.')
    A('')
    A('TODA cifra de este documento pertenece a la ventana %s.' % VENTANA)
    A('')
    A(autoprueba())
    A('')
    A('-' * 78)
    A('1 · FLUJO DE MUESTRA')
    A('-' * 78)
    for k in ['jefes_ola2', 'jefes_ola3', 'ola3_ronda_C_no_enlazable',
              'jefes_en_ambas_olas', 'elegibles_basal_ola2',
              'elegible_sin_jefatura_o_ausente_en_ola3',
              'excluidos_sin_entidad_federativa', 'sin_TB33_en_ola3',
              'sin_CRH_en_ola3', 'composicion_no_construible_ola3',
              'muestra_analitica']:
        A('  %-46s %6d' % (k, flujo[k]))
    eleg, ana = flujo['elegibles_basal_ola2'], flujo['muestra_analitica']
    A('')
    A('  Atrición efectiva sobre elegibles basales: %d de %d = %.1f%%'
      % (eleg - ana, eleg, 100.0 * (eleg - ana) / eleg))
    A('')
    A('  Observaciones excluidas por levantamiento fuera de entidad federativa')
    A('  mexicana: %d. El marcador es COTA INFERIOR — ver la nota.'
      % flujo['excluidos_sin_entidad_federativa'])
    A('')
    A('  Incidencia de "Otro" (crh01_1k), tratado como faltante para el estado')
    A('  de composición (Adenda 1 c), sobre el módulo CRH completo:')
    for t, et in (('w2', '2 (2005-06)'), ('w3', '3 (2009-12)')):
        n = len(W[t]['crh'])
        k = sum(1 for r in W[t]['crh'].values()
                if r.get('crh01_1k') is not None)
        A('    ola %s: %d de %d hogares = %.2f%%' % (et, k, n, 100.0 * k / n))

    A('')
    A('-' * 78)
    A('2 · COMPOSICIÓN BASAL (ola 2): PERDIDOS vs RETENIDOS')
    A('-' * 78)
    ret = {r['pid'] for r in filas}
    eleg_l = [b for b in basal if b['elegible']]
    sexo_lab = {1.0: 'hombre', 3.0: 'mujer', None: 's/d'}   # ENNViH usa 1/3

    def dist(g, campo, lab=None):
        c = Counter(b[campo] for b in g)
        n = sum(c.values())
        return ', '.join('%s=%.1f%%' % (lab.get(k, k) if lab else k,
                                        100.0 * c[k] / n)
                         for k in sorted(c, key=lambda x: (x is None, x)))

    for nom, g in (('retenidos', [b for b in eleg_l if b['pid'] in ret]),
                   ('perdidos', [b for b in eleg_l if b['pid'] not in ret])):
        ed = [b['edad'] for b in g if b['edad'] is not None]
        A('  %s (n=%d)' % (nom, len(g)))
        A('    sexo del jefe:       %s' % dist(g, 'sexo', sexo_lab))
        A('    formalidad basal:    %s' % dist(g, 'f2'))
        A('    acceso formal basal: %.1f%%'
          % (100.0 * sum(b['y2'] for b in g) / len(g)))
        A('    edad media:          %.1f (n con dato=%d)'
          % (sum(ed) / len(ed), len(ed)))
        A('    nivel educativo ls14: %s' % dist(g, 'edu'))
        A('')
    A('  Dirección del sesgo, declarada ANTES de medir (ficha, punto 6): si')
    A('  los perdidos son sistemáticamente más informales, el sesgo va CONTRA')
    A('  encontrar el efecto. Las cifras de arriba permiten verificarlo.')

    A('')
    A('-' * 78)
    A('3 · TRANSICIÓN DE LOS CUATRO ESTADOS (Adenda 1 b), muestra analítica')
    A('-' * 78)
    orden = ['ninguno', 'solo_informal', 'mixto', 'solo_formal']
    tr = Counter((r['e2'], r['e3']) for r in filas)
    A('  filas = estado del hogar en 2005-06 · columnas = en 2009-12')
    A('  %-16s %9s %14s %7s %12s %8s'
      % ('', 'ninguno', 'solo_informal', 'mixto', 'solo_formal', 'total'))
    for a in orden:
        f = [tr[(a, b)] for b in orden]
        A('  %-16s %9d %14d %7d %12d %8d' % tuple([a] + f + [sum(f)]))
    A('  %-16s %9d %14d %7d %12d %8d' % tuple(
        ['total'] + [sum(tr[(a, b)] for a in orden) for b in orden]
        + [sum(tr.values())]))
    A('')
    A('  "Algún acceso formal" (mixto o solo formal), %s:' % VENTANA)
    A('    ola 2: %.2f%%   ola 3: %.2f%%   (n=%d)'
      % (100.0 * sum(r['y2'] for r in filas) / len(filas),
         100.0 * sum(r['y3'] for r in filas) / len(filas), len(filas)))
    A('')
    A('  Transición de formalidad del jefe:')
    for k, v in sorted(Counter((r['f2'], r['f3']) for r in filas).items()):
        A('    %-24s %5d' % ('%s -> %s' % k, v))

    A('')
    A('-' * 78)
    A('4 · EFECTOS FIJOS DE HOGAR SOBRE LA TRANSICIÓN 2005-06 -> 2009-12')
    A('-' * 78)
    A('  beta(pp): probabilidad lineal con EF de hogar (== MCO en primeras')
    A('  diferencias); efecto sobre P(algún acceso formal) en puntos')
    A('  porcentuales; EE robusto HC1.')
    A('  OR: logit condicional de Chamberlain. n.disc = hogares que cambian de')
    A('  desenlace; n.inf = de ésos, los que ADEMÁS cambian de exposición —')
    A('  los únicos que identifican el coeficiente.')
    for e_modo, e_desc in EXPOSICIONES:
        A('')
        A('=' * 78)
        A('EXPOSICIÓN: %s' % e_modo)
        A('  %s' % e_desc)
        A('=' * 78)
        for d_modo, d_desc in DESENLACES:
            A('')
            A('  DESENLACE: %s — %s' % (d_modo, d_desc))
            A('')
            A('  %-42s %6s %9s %8s %-20s'
              % ('ponderador', 'n', 'beta(pp)', 'EE', 'IC95%'))
            A('  ' + '-' * 74)
            for pn, pk in PONDERADORES:
                dx, dy, w = subconjunto(filas, e_modo, d_modo, pk)
                if len(dx) < 3:
                    A('  %-42s %6d  (insuficiente)' % (pn, len(dx)))
                    continue
                m = lpm_fe(dx, dy, w)
                A('  %-42s %6d %9.2f %8.2f [%.2f, %.2f]'
                  % (pn, m['n'], 100 * m['beta'], 100 * m['se'],
                     100 * m['ic'][0], 100 * m['ic'][1]))
            A('')
            A('  %-42s %6s %6s %8s %-20s'
              % ('logit condicional', 'n.disc', 'n.inf', 'OR', 'IC95% del OR'))
            A('  ' + '-' * 74)
            for pn, pk in PONDERADORES:
                dx, dy, w = subconjunto(filas, e_modo, d_modo, pk)
                if len(dx) < 3:
                    A('  %-42s  (insuficiente)' % pn)
                    continue
                c = clogit_fe(dx, dy, w)
                if 'error' in c:
                    A('  %-42s %6d %6s  NO ESTIMABLE: %s'
                      % (pn, c.get('n_disc', 0),
                         c.get('n_informativas', '-'), c['error']))
                    continue
                A('  %-42s %6d %6d %8.3f [%.3f, %.3f]'
                  % (pn, c['n_disc'], c['n_informativas'], c['or_'],
                     c['or_ic'][0], c['or_ic'][1]))
    A('')
    A('=' * 78)
    A('Toda cifra de este documento pertenece a la ventana %s. Sin ese' % VENTANA)
    A('calificador pegado, la cifra se degrada al citarse.')
    A('=' * 78)
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--salida', help='ruta donde escribir el reporte')
    args = ap.parse_args()
    txt = reporte(*ensamblar())
    if args.salida:
        with io.open(args.salida, 'w', encoding='utf-8') as fh:
            fh.write(txt)
    sys.stdout.write(txt)


if __name__ == '__main__':
    main()
