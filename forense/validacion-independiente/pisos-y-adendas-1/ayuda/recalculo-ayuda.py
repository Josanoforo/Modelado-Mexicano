#!/usr/bin/env python3
"""
Recalculo independiente -- ENDIREH-PISOS-2021-AYUDA, spec humana v2.0.

Implementa EXACTAMENTE el procedimiento descrito en:
  forense/prereg-caja/ENDIREH-PISOS-2021-AYUDA-spec-v2_0.md

Emite SOLO la llave que forense/validacion-independiente/pisos-y-adendas-1/
protocolo-recalculo-v1_0.md Sec.1 lista para este CALC:
  #115 (razon_14 x nacional) = "No sabia que existian leyes para sancionar
  la violencia" (P14_22_14, casilla 14 de 14.22, FD 2021 p.632).

`razon_14` solo tiene celda nacional y solo depende de: violencia (clasificador
sobre los 38 actos de 14.1), ayuda (P14_7_1) y denuncia (P14_7_2) -- ambas solo
si violencia=1 -- y, si ayuda=0 y denuncia=0, de P14_22_14 de TB_SEC_XIV_2.csv
enlazado por ID_PER. El enumerador de indices SI construye los 117 slots
completos (ayuda, denuncia, institucion_*, razon_*) para verificar que la
identidad de la llave requerida coincide con la que declara el protocolo.

Uso: python3 recalculo.py <ruta_zip> <salida.tsv>
"""
import sys
import zipfile
import csv
import io
import math

import numpy as np

SEMILLA_BASE = 20260923
R_REPLICAS = 500

AB_ACTS = {23, 24, 35, 36, 37, 38}


def field_p14_1(i):
    return f'P14_1_{i}AB' if i in AB_ACTS else f'P14_1_{i}'


# ---------------------------------------------------------------------------
# Lectura del ZIP
# ---------------------------------------------------------------------------

def find_member(zf, basename):
    matches = [n for n in zf.namelist() if n.rsplit('/', 1)[-1] == basename]
    if len(matches) != 1:
        raise SystemExit(
            f"esperaba exactamente un miembro llamado {basename!r} en el zip, "
            f"hallados: {matches}"
        )
    return matches[0]


def read_columns(zf, basename, wanted_cols):
    member = find_member(zf, basename)
    with zf.open(member) as f:
        wrapper = io.TextIOWrapper(f, encoding='latin-1', newline='')
        reader = csv.reader(wrapper)
        header = next(reader)
        idx = {name: i for i, name in enumerate(header)}
        for w in wanted_cols:
            if w not in idx:
                raise SystemExit(f"columna {w!r} no encontrada en {basename}")
        col_idx = [idx[w] for w in wanted_cols]
        rows = []
        for row in reader:
            rows.append(tuple(row[i] for i in col_idx))
        return rows


# ---------------------------------------------------------------------------
# Ejes / categorias (S4) -- solo se usan para el enumerador de indices
# (la llave requerida, #115, es nacional-only y no necesita las demas)
# ---------------------------------------------------------------------------

ENTIDADES = [f'{i:02d}' for i in range(1, 33)]
LOCALIDADES = ['U', 'C', 'R']
PAREJAS = ['A1', 'A2']

EJES = [
    ('nacional', ['MX']),
    ('edad', ['15-29', '30-44', '45-59', '60+']),
    ('escolaridad', ['ninguno', 'basica', 'media_superior', 'superior']),
    ('localidad', LOCALIDADES),
    ('pareja', PAREJAS),
    ('entidad', ENTIDADES),
]


def enumerate_keys():
    """[(k, desenlace, eje, categoria)] en el orden de S6 (117 slots: 0-116)."""
    out = []
    k = 0
    for des in ('ayuda', 'denuncia'):
        for eje, cats in EJES:
            for cat in cats:
                out.append((k, des, eje, cat))
                k += 1
    for i in range(1, 11):
        out.append((k, f'institucion_{i:02d}', 'nacional', 'MX'))
        k += 1
    for i in range(1, 16):
        out.append((k, f'razon_{i:02d}', 'nacional', 'MX'))
        k += 1
    return out


# Llave requerida por el protocolo P4 Sec.1 para este CALC (1)
REQUERIDAS = [115]


# ---------------------------------------------------------------------------
# Clasificadores (S3)
# ---------------------------------------------------------------------------

def clasificador_actos(valores):
    if any(v in ('1', '2', '3') for v in valores):
        return 1
    if len(valores) > 0 and all(v == '4' for v in valores):
        return 0
    return None


def _simple_10(code_raw):
    c = code_raw.strip()
    if c == '1':
        return 1
    if c == '2':
        return 0
    return None


def _razon_item(code_raw):
    c = code_raw.strip()
    if c == '1':
        return 1
    if c == '0':
        return 0
    return None


# ---------------------------------------------------------------------------
# Marco (S2) + derivados por fila
# ---------------------------------------------------------------------------

class Fila:
    __slots__ = ('fac', 'est', 'upm', 'ejes', 'desenlaces', 'cluster_idx')

    def __init__(self, fac, est, upm, ejes, desenlaces):
        self.fac = fac
        self.est = est
        self.upm = upm
        self.ejes = ejes
        self.desenlaces = desenlaces
        self.cluster_idx = None


def construir_marco(zf):
    id_map_edad = {}
    for idp, edad in read_columns(zf, 'TSDem.csv', ['ID_PER', 'EDAD']):
        if idp != '':
            id_map_edad[idp] = edad

    id_map_razon14 = {}
    for idp, r14 in read_columns(zf, 'TB_SEC_XIV_2.csv', ['ID_PER', 'P14_22_14']):
        if idp != '':
            id_map_razon14[idp] = r14

    campos_p14_1 = [field_p14_1(i) for i in range(1, 39)]  # 38 columnas
    cols_xiv = ['ID_PER', 'T_INSTRUM', 'FAC_MUJ', 'EST_DIS', 'UPM_DIS',
                'P14_7_1', 'P14_7_2'] + campos_p14_1
    xiv = read_columns(zf, 'TB_SEC_XIV.csv', cols_xiv)
    n_fijos = 7

    marco = []
    for row in xiv:
        (idp, t_instrum, fac_muj, est_dis, upm_dis,
         p14_7_1, p14_7_2) = row[:n_fijos]
        p14_1_vals = row[n_fijos:]

        # 1. T_INSTRUM (texto crudo) en {A1,A2}
        if t_instrum not in ('A1', 'A2'):
            continue

        # 2. Edad via enlace ID_PER -> TSDem
        edad_raw = id_map_edad.get(idp)
        if edad_raw is None:
            continue
        try:
            edad_int = int(edad_raw)
        except (ValueError, TypeError):
            continue
        if not (15 <= edad_int <= 120):
            continue

        # 3. FAC_MUJ real, finito, > 0
        try:
            fac = float(fac_muj)
        except (ValueError, TypeError):
            continue
        if not math.isfinite(fac) or fac <= 0:
            continue

        # 4. EST_DIS, UPM_DIS no vacios
        if est_dis == '' or upm_dis == '':
            continue

        ejes_fila = {'nacional': 'MX'}

        # violencia: clasificador sobre los 38 actos de 14.1 (nunca C1 aqui,
        # el marco solo admite A1/A2, pero se respeta la omision general)
        acts = list(range(1, 39))
        if t_instrum == 'C1':
            acts = [a for a in acts if a not in AB_ACTS]
        valores_violencia = [p14_1_vals[a - 1].strip() for a in acts]
        violencia = clasificador_actos(valores_violencia)

        if violencia == 1:
            ayuda = _simple_10(p14_7_1)
            denuncia = _simple_10(p14_7_2)
        else:
            ayuda = None
            denuncia = None

        if ayuda == 0 and denuncia == 0:
            r14_raw = id_map_razon14.get(idp)
            razon_14 = _razon_item(r14_raw) if r14_raw is not None else None
        else:
            razon_14 = None

        desenlaces_fila = {
            'ayuda': ayuda,
            'denuncia': denuncia,
            'razon_14': razon_14,
        }

        marco.append(Fila(fac, est_dis, upm_dis, ejes_fila, desenlaces_fila))

    return marco


def construir_marco_de_conglomerados(marco):
    clusters_order = []
    cluster_index = {}
    estratos_order = []
    estrato_clusters = {}

    for fila in marco:
        par = (fila.est, fila.upm)
        ci = cluster_index.get(par)
        if ci is None:
            ci = len(clusters_order)
            cluster_index[par] = ci
            clusters_order.append(par)
            if fila.est not in estrato_clusters:
                estrato_clusters[fila.est] = []
                estratos_order.append(fila.est)
            estrato_clusters[fila.est].append(ci)
        fila.cluster_idx = ci

    estrato_cluster_arrays = {
        est: np.array(idxs, dtype=np.int64) for est, idxs in estrato_clusters.items()
    }
    return clusters_order, estratos_order, estrato_cluster_arrays


# ---------------------------------------------------------------------------
# Estimacion por celda (S5)
# ---------------------------------------------------------------------------

def calcular_celda(des, eje, cat, marco, n_clusters, estratos_order,
                    estrato_cluster_arrays, R, texto_semilla):
    num = np.zeros(n_clusters, dtype=np.float64)
    den = np.zeros(n_clusters, dtype=np.float64)
    n = 0
    upm_set = set()

    for fila in marco:
        if eje != 'nacional' and fila.ejes.get(eje) != cat:
            continue
        val = fila.desenlaces[des]
        if val is None:
            continue
        n += 1
        ci = fila.cluster_idx
        upm_set.add(ci)
        num[ci] += fila.fac * val
        den[ci] += fila.fac

    upm = len(upm_set)

    resultado = dict(estado=None, causa=None, n=n, upm=upm,
                      punto=None, ic_inf=None, ic_sup=None, se=None)

    if n < 100 or upm < 5:
        resultado['estado'] = 'SUPRIMIDA'
        resultado['causa'] = 'soporte'
        return resultado

    total_den = den.sum()
    p = num.sum() / total_den

    s = SEMILLA_BASE + sum(ord(c) for c in texto_semilla)
    rng = np.random.default_rng(s)

    replicas = np.empty(R, dtype=np.float64)
    for r in range(R):
        snum = 0.0
        sden = 0.0
        for est in estratos_order:
            idxs_arr = estrato_cluster_arrays[est]
            m = idxs_arr.shape[0]
            draws = rng.integers(0, m, m)
            elegidos = idxs_arr[draws]
            snum += num[elegidos].sum()
            sden += den[elegidos].sum()
        if sden != 0.0 and math.isfinite(snum) and math.isfinite(sden):
            replicas[r] = snum / sden
        else:
            replicas[r] = math.nan

    if not np.all(np.isfinite(replicas)):
        resultado['estado'] = 'SUPRIMIDA'
        resultado['causa'] = 'replicas'
        return resultado

    ic_inf, ic_sup = np.quantile(replicas, [0.025, 0.975])
    se = replicas.std(ddof=1)

    if (ic_sup - ic_inf) > 0.20 or (p > 0 and se / p > 0.30):
        resultado['estado'] = 'SUPRIMIDA'
        resultado['causa'] = 'precision'
        return resultado

    resultado['estado'] = 'PUBLICABLE'
    resultado['causa'] = ''
    resultado['punto'] = p
    resultado['ic_inf'] = ic_inf
    resultado['ic_sup'] = ic_sup
    resultado['se'] = se
    return resultado


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        raise SystemExit("uso: python3 recalculo.py <ruta_zip> <salida.tsv>")
    ruta_zip, ruta_salida = sys.argv[1], sys.argv[2]

    with zipfile.ZipFile(ruta_zip) as zf:
        marco = construir_marco(zf)

    n_elegibles = len(marco)
    clusters_order, estratos_order, estrato_cluster_arrays = construir_marco_de_conglomerados(marco)
    n_clusters = len(clusters_order)

    todas = enumerate_keys()
    mapa_k = {k: (des, eje, cat) for (k, des, eje, cat) in todas}
    assert len(todas) == 117, f"se esperaban 117 slots, hubo {len(todas)}"

    filas_out = []
    for k in REQUERIDAS:
        des, eje, cat = mapa_k[k]
        # institucion_*/razon_*: semilla = solo el nombre del desenlace (S5.5)
        if des.startswith('institucion_') or des.startswith('razon_'):
            texto_semilla = des
        else:
            texto_semilla = des + eje + cat
        r = calcular_celda(des, eje, cat, marco, n_clusters, estratos_order,
                            estrato_cluster_arrays, R_REPLICAS, texto_semilla)
        llave = f"RESULT-ENDIREH2021-AYU-TABLA#{k}"

        def fmt(x):
            return '' if x is None else repr(float(x))

        filas_out.append([
            llave, des, eje, cat, r['estado'], r['causa'],
            str(r['n']), str(r['upm']),
            fmt(r['punto']), fmt(r['ic_inf']), fmt(r['ic_sup']), fmt(r['se']),
        ])

    with open(ruta_salida, 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['llave', 'desenlace', 'eje', 'categoria', 'estado', 'causa',
                    'n', 'upm', 'punto', 'ic95_inf', 'ic95_sup', 'se'])
        for row in filas_out:
            w.writerow(row)

    print(f"N-ELEGIBLES (marco): {n_elegibles}")
    print(f"clusters (marco de conglomerados): {n_clusters}, estratos: {len(estratos_order)}")
    print(f"llaves emitidas: {len(filas_out)} -> {ruta_salida}")
    for row in filas_out:
        print('\t'.join(row))


if __name__ == '__main__':
    main()
