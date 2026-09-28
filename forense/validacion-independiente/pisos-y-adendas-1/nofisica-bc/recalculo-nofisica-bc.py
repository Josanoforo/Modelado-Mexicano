#!/usr/bin/env python3
"""
Recalculo independiente -- ENDIREH-PISOS-2021-NOFISICA-BC, spec humana v2.0.

Implementa EXACTAMENTE el procedimiento descrito en:
  forense/prereg-caja/ENDIREH-PISOS-2021-NOFISICA-BC-spec-v2_0.md

Emite SOLO las 8 llaves que forense/validacion-independiente/pisos-y-adendas-1/
protocolo-recalculo-v1_0.md Sec.1 lista para este CALC:
  #495 #496 #497 #498 (ayuda_bc x escolaridad {ninguno,basica,media_superior,superior})
  #544 #545 #546 #547 (denuncia_bc x escolaridad {ninguno,basica,media_superior,superior})

`ayuda_bc`/`denuncia_bc` dependen solo de la "violencia" (clasificador sobre
TODOS los actos 1-38 de 14.1, S3 parrafo "Ayuda y denuncia B/C"), no de los
diez desenlaces de grupo (emocional_control, sexual, ...); por eso el marco
de conglomerados se construye completo (S5.3) pero solo se computan los
desenlaces ayuda_bc/denuncia_bc por fila. El enumerador de indices SI incluye
los 613 slots completos (grupos x ventanas, ayuda_bc, denuncia_bc,
institucion_bc_*, razon_bc_*) para verificar que la identidad de cada llave
requerida coincide con la que declara el protocolo.

Uso: python3 recalculo.py <ruta_zip> <salida.tsv>
"""
import sys
import zipfile
import csv
import io
import math

import numpy as np

SEMILLA_BASE = 20260923
R_REPLICAS = 200

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
# Ejes / categorias (S4) -- pareja tiene 5 categorias en esta spec (sin C2)
# ---------------------------------------------------------------------------

NIV_A_ESCOLARIDAD = {
    0: 'ninguno',
    1: 'basica', 2: 'basica', 3: 'basica', 5: 'basica', 6: 'basica',
    4: 'media_superior', 7: 'media_superior', 8: 'media_superior',
    9: 'superior', 10: 'superior', 11: 'superior',
}


def escolaridad_de_niv(niv_texto):
    try:
        n = int(niv_texto)
    except (ValueError, TypeError):
        return None
    return NIV_A_ESCOLARIDAD.get(n)


def edad_a_bucket(edad_int):
    if 15 <= edad_int <= 29:
        return '15-29'
    if 30 <= edad_int <= 44:
        return '30-44'
    if 45 <= edad_int <= 59:
        return '45-59'
    if 60 <= edad_int <= 120:
        return '60+'
    return None


ENTIDADES = [f'{i:02d}' for i in range(1, 33)]
LOCALIDADES = ['U', 'C', 'R']
PAREJAS = ['A1', 'A2', 'B1', 'B2', 'C1']  # sin C2 (S2 la excluye del marco)

EJES = [
    ('nacional', ['MX']),
    ('edad', ['15-29', '30-44', '45-59', '60+']),
    ('escolaridad', ['ninguno', 'basica', 'media_superior', 'superior']),
    ('localidad', LOCALIDADES),
    ('pareja', PAREJAS),
    ('entidad', ENTIDADES),
]

GRUPOS = ['emocional_control', 'sexual', 'digital', 'economica_patrimonial', 'no_fisica_alguna']
VENTANAS = ['vida_relacion', 'desde_octubre_2020']


def enumerate_keys():
    """[(k, desenlace, eje, categoria)] en el orden de S6 (613 slots: 0-612).
    Solo los desenlaces ayuda_bc/denuncia_bc llevan valores computados; el
    resto de las etiquetas se generan igual para que el indice k sea fiel a
    la spec y se pueda verificar la identidad de las llaves requeridas."""
    out = []
    k = 0
    for grupo in GRUPOS:
        for ventana in VENTANAS:
            des = f'{grupo}__{ventana}'
            for eje, cats in EJES:
                for cat in cats:
                    out.append((k, des, eje, cat))
                    k += 1
    for eje, cats in EJES:
        for cat in cats:
            out.append((k, 'ayuda_bc', eje, cat))
            k += 1
    for eje, cats in EJES:
        for cat in cats:
            out.append((k, 'denuncia_bc', eje, cat))
            k += 1
    for i in range(1, 11):
        out.append((k, f'institucion_bc_{i:02d}', 'nacional', 'MX'))
        k += 1
    for i in range(1, 16):
        out.append((k, f'razon_bc_{i:02d}', 'nacional', 'MX'))
        k += 1
    return out


# Llaves requeridas por el protocolo P4 Sec.1 para este CALC (8)
REQUERIDAS = [495, 496, 497, 498, 544, 545, 546, 547]


# ---------------------------------------------------------------------------
# Clasificador de actos (S3) y violencia B/C
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
    cols_tsdem = ['ID_PER', 'EDAD', 'NIV']
    tsdem = read_columns(zf, 'TSDem.csv', cols_tsdem)
    id_map = {}
    for idp, edad, niv in tsdem:
        if idp != '':
            id_map[idp] = (edad, niv)

    campos_p14_1 = [field_p14_1(i) for i in range(1, 39)]  # 38 columnas
    cols_xiv = (
        ['ID_PER', 'DOMINIO', 'CVE_ENT', 'T_INSTRUM',
         'FAC_MUJ', 'EST_DIS', 'UPM_DIS', 'P14_7_1', 'P14_7_2']
        + campos_p14_1
    )
    xiv = read_columns(zf, 'TB_SEC_XIV.csv', cols_xiv)
    n_fijos = 9  # cuantas columnas fijas van antes de los P14_1_*

    marco = []
    for row in xiv:
        (idp, dominio, cve_ent, t_instrum,
         fac_muj, est_dis, upm_dis, p14_7_1, p14_7_2) = row[:n_fijos]
        p14_1_vals = row[n_fijos:]  # alineado con campos_p14_1 / range(1,39)

        # 1. T_INSTRUM (texto crudo) en {A1,A2,B1,B2,C1}
        if t_instrum not in ('A1', 'A2', 'B1', 'B2', 'C1'):
            continue

        # 2. Edad via enlace ID_PER -> TSDem
        ed = id_map.get(idp)
        if ed is None:
            continue
        try:
            edad_int = int(ed[0])
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

        niv_texto = ed[1]
        ejes_fila = {
            'nacional': 'MX',
            'edad': edad_a_bucket(edad_int),
            'escolaridad': escolaridad_de_niv(niv_texto),
            'localidad': dominio if dominio in LOCALIDADES else None,
            'pareja': t_instrum if t_instrum in PAREJAS else None,
            'entidad': cve_ent if cve_ent in ENTIDADES else None,
        }

        # violencia: clasificador sobre TODOS los actos 1-38 de 14.1
        # (fisicos 1-9 incluidos; para C1 sin los seis AB)
        acts = list(range(1, 39))
        if t_instrum == 'C1':
            acts = [a for a in acts if a not in AB_ACTS]
        valores_violencia = [p14_1_vals[a - 1].strip() for a in acts]
        violencia = clasificador_actos(valores_violencia)

        if t_instrum in ('B1', 'B2', 'C1') and violencia == 1:
            ayuda_bc = _simple_10(p14_7_1)
            denuncia_bc = _simple_10(p14_7_2)
        else:
            ayuda_bc = None
            denuncia_bc = None

        desenlaces_fila = {
            'ayuda_bc': ayuda_bc,
            'denuncia_bc': denuncia_bc,
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
                    estrato_cluster_arrays, R):
    num = np.zeros(n_clusters, dtype=np.float64)
    den = np.zeros(n_clusters, dtype=np.float64)
    n = 0
    upm_set = set()

    for fila in marco:
        if eje != 'nacional' and fila.ejes[eje] != cat:
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

    # texto de semilla: desenlace + eje + categoria (ayuda_bc/denuncia_bc
    # NO son ni desenlaces de grupo ni institucion_bc_*/razon_bc_*, asi que
    # llevan el tratamiento normal, S5.5)
    texto_semilla = des + eje + cat
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
    assert len(todas) == 613, f"se esperaban 613 slots, hubo {len(todas)}"

    filas_out = []
    for k in REQUERIDAS:
        des, eje, cat = mapa_k[k]
        r = calcular_celda(des, eje, cat, marco, n_clusters, estratos_order,
                            estrato_cluster_arrays, R_REPLICAS)
        llave = f"RESULT-ENDIREH2021-NF-BC-TABLA#{k}"

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
