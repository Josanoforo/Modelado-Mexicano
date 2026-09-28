#!/usr/bin/env python3
"""
Recalculo independiente -- ENDIREH-PISOS-2021-DISCRIMINACION, spec humana v2.0.

Implementa EXACTAMENTE el procedimiento descrito en:
  forense/prereg-caja/ENDIREH-PISOS-2021-DISCRIMINACION-spec-v2_0.md

Emite SOLO las 23 llaves que forense/validacion-independiente/pisos-y-adendas-1/
protocolo-recalculo-v1_0.md Sec.1 lista para este CALC:
  #5 #6 #7 #8      (prueba_ingreso x escolaridad {ninguno,basica,media_superior,superior})
  #56 #57 #58      (prueba_continuidad x escolaridad {basica,media_superior,superior})
  #105 #106 #107 #108 (prueba_alguna x escolaridad {ninguno,basica,media_superior,superior})
  #156 #157 #158   (despido_embarazo x escolaridad {basica,media_superior,superior})
  #206 #207 #208   (no_renovacion_embarazo x escolaridad {...})
  #256 #257 #258   (reduccion_embarazo x escolaridad {...})
  #306 #307 #308   (perjuicio_embarazo_alguno x escolaridad {...})

El marco (S2) se construye completo (todas las mujeres elegibles), porque el
bootstrap (S5.3) usa el marco de conglomerados COMPLETO, no solo la celda;
solo se EMITEN las llaves de arriba.

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


# ---------------------------------------------------------------------------
# Lectura del ZIP (miembros por nombre base exacto, latin-1, CSV con encabezado)
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
    """Lee solo las columnas pedidas (por nombre exacto de encabezado);
    devuelve lista de tuplas alineadas con wanted_cols, en orden de archivo."""
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
        n = len(col_idx)
        rows = []
        for row in reader:
            rows.append(tuple(row[i] for i in col_idx))
        return rows


# ---------------------------------------------------------------------------
# Ejes / categorias (S4)
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
PAREJAS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

EJES = [
    ('nacional', ['MX']),
    ('edad', ['15-29', '30-44', '45-59', '60+']),
    ('escolaridad', ['ninguno', 'basica', 'media_superior', 'superior']),
    ('localidad', LOCALIDADES),
    ('pareja', PAREJAS),
    ('entidad', ENTIDADES),
]

DESENLACES = [
    'prueba_ingreso', 'prueba_continuidad', 'prueba_alguna',
    'despido_embarazo', 'no_renovacion_embarazo', 'reduccion_embarazo',
    'perjuicio_embarazo_alguno',
]


def enumerate_keys():
    """[(k, desenlace, eje, categoria)] en el orden de S6 de la spec."""
    out = []
    k = 0
    for des in DESENLACES:
        for eje, cats in EJES:
            for cat in cats:
                out.append((k, des, eje, cat))
                k += 1
    return out


# Llaves requeridas por el protocolo P4 Sec.1 para este CALC (23)
REQUERIDAS = [
    5, 6, 7, 8,
    56, 57, 58,
    105, 106, 107, 108,
    156, 157, 158,
    206, 207, 208,
    256, 257, 258,
    306, 307, 308,
]


# ---------------------------------------------------------------------------
# Clasificadores de desenlace (S3) -- codigos comparados TRAS recortar espacios
# ---------------------------------------------------------------------------

def _simple_10(code_raw):
    c = code_raw.strip()
    if c == '1':
        return 1
    if c == '2':
        return 0
    return None  # desconocido


def _embarazo_item(code_raw):
    c = code_raw.strip()
    if c == '3':
        return None  # no estuvo embarazada -> desconocido (inelegible, no negativo)
    if c == '1':
        return 1
    if c == '2':
        return 0
    return None


def _perjuicio_alguno(c1_raw, c2_raw, c3_raw):
    cs = [c1_raw.strip(), c2_raw.strip(), c3_raw.strip()]
    if all(c == '3' for c in cs):
        return None
    if any(c == '1' for c in cs):
        return 1
    if all(c == '2' for c in cs):
        return 0
    return None


def _union_alguna(a, b):
    if a == 1 or b == 1:
        return 1
    if a == 0 and b == 0:
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
            id_map[idp] = (edad, niv)  # ultima fila leida gana

    cols_viii = [
        'ID_PER', 'DOMINIO', 'CVE_ENT', 'T_INSTRUM',
        'P8_2', 'P8_3_1_1', 'P8_3_1_2', 'P8_3_2_1', 'P8_3_2_2', 'P8_3_2_3',
        'FAC_MUJ', 'EST_DIS', 'UPM_DIS',
    ]
    viii = read_columns(zf, 'TB_SEC_VIII.csv', cols_viii)

    marco = []
    for (idp, dominio, cve_ent, t_instrum,
         p8_2, p8_3_1_1, p8_3_1_2, p8_3_2_1, p8_3_2_2, p8_3_2_3,
         fac_muj, est_dis, upm_dis) in viii:

        # 1. P8_2 exactamente '1' (texto crudo, sin recortar)
        if p8_2 != '1':
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

        # 4. EST_DIS, UPM_DIS no vacios (texto crudo)
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

        p_ingreso = _simple_10(p8_3_1_1)
        p_continuidad = _simple_10(p8_3_1_2)
        p_alguna = _union_alguna(p_ingreso, p_continuidad)
        d_embarazo = _embarazo_item(p8_3_2_1)
        nr_embarazo = _embarazo_item(p8_3_2_2)
        r_embarazo = _embarazo_item(p8_3_2_3)
        perj_alguno = _perjuicio_alguno(p8_3_2_1, p8_3_2_2, p8_3_2_3)

        desenlaces_fila = {
            'prueba_ingreso': p_ingreso,
            'prueba_continuidad': p_continuidad,
            'prueba_alguna': p_alguna,
            'despido_embarazo': d_embarazo,
            'no_renovacion_embarazo': nr_embarazo,
            'reduccion_embarazo': r_embarazo,
            'perjuicio_embarazo_alguno': perj_alguno,
        }

        marco.append(Fila(fac, est_dis, upm_dis, ejes_fila, desenlaces_fila))

    return marco


def construir_marco_de_conglomerados(marco):
    """Todos los pares (EST_DIS, UPM_DIS) del marco completo, en orden de
    primera aparicion recorriendo las filas en el orden del archivo (S5.3)."""
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

    filas_out = []
    for k in REQUERIDAS:
        des, eje, cat = mapa_k[k]
        r = calcular_celda(des, eje, cat, marco, n_clusters, estratos_order,
                            estrato_cluster_arrays, R_REPLICAS)
        llave = f"RESULT-ENDIREH2021-DIS-TABLA#{k}"

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
