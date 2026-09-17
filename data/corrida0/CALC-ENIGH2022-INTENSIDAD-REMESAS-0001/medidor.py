"""Monto e intensidad contable de remesas entre hogares receptores, ENIGH 2022.

Interfaz estable: ``medir(inputs, contrato) -> {"RESULT-...": valor}``.
El medidor abre un solo miembro estadistico del ZIP declarado. Los IC usan el
marco completo y contribuciones cero fuera del dominio de participacion.
"""
from __future__ import annotations

import csv
import io
import zipfile

import numpy as np


ZIP_ID = "enigh2022_nc_csv"
P = "RESULT-ENIGH22-REMINT-"
MIEMBRO = (
    "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/"
    "conjunto_de_datos_concentradohogar_enigh2022_ns.csv"
)
COLUMNAS = [
    "folioviv", "foliohog", "factor", "remesas", "ing_cor", "est_dis", "upm"
]


def _norm(celda):
    return str(celda).lstrip("\ufeff").lstrip("ï»¿").strip().strip('"').lower()


def _texto(valor):
    if valor is None:
        return None
    texto = str(valor).strip().strip('"')
    return texto or None


def _numero(valor):
    texto = _texto(valor)
    if texto is None:
        return None
    try:
        numero = float(texto.replace(",", ""))
    except ValueError:
        return None
    return numero if np.isfinite(numero) else None


def _abre(zf):
    with zf.open(MIEMBRO) as fh:
        texto = io.TextIOWrapper(fh, encoding="latin-1", newline="")
        lector = csv.reader(texto)
        try:
            cabecera = [_norm(c) for c in next(lector)]
        except StopIteration:
            return [], list(COLUMNAS), 0
        indices = {c: cabecera.index(c) for c in COLUMNAS if c in cabecera}
        ausentes = [c for c in COLUMNAS if c not in indices]
        filas = []
        for fila in lector:
            if not fila:
                continue
            filas.append({
                c: fila[indices[c]] if c in indices and indices[c] < len(fila) else None
                for c in COLUMNAS
            })
        return filas, ausentes, len(cabecera)


def mediana_ponderada(valores, pesos):
    """Inversa izquierda de la CDF: menor valor con acumulada >= 0.5."""
    pares = sorted((float(v), float(w)) for v, w in zip(valores, pesos))
    if not pares:
        return None
    total = float(sum(w for _, w in pares))
    if total <= 0:
        return None
    acumulada = 0.0
    mitad = total / 2.0
    for valor, peso in pares:
        acumulada += peso
        if acumulada >= mitad:
            return valor
    return pares[-1][0]


def _percentiles(valores):
    arreglo = np.asarray(valores, dtype=float)
    finitos = arreglo[np.isfinite(arreglo)]
    if finitos.size == 0:
        return None, None, int(arreglo.size)
    return (
        float(np.percentile(finitos, 2.5)),
        float(np.percentile(finitos, 97.5)),
        int(arreglo.size - finitos.size),
    )


def _bootstrap_marco(filas, replicas, seed):
    """Remuestrea UPM en estrato sobre todo el marco; fuera de dominio = cero."""
    conglomerados = {}
    n_sin_diseno = 0
    for fila in filas:
        estrato = fila["est_dis"]
        upm = fila["upm"]
        if estrato is None or upm is None:
            n_sin_diseno += 1
            continue
        bloque = conglomerados.setdefault((estrato, upm), np.zeros(5, dtype=float))
        bloque += fila["contrib"]

    base = {
        "n_filas_marco": len(filas),
        "n_sin_diseno": n_sin_diseno,
        "n_estratos": 0,
        "n_upm": 0,
        "n_unica": 0,
        "metodo": "NO-ESTIMABLE-DISENO-INCOMPLETO",
        "media_lo": None, "media_hi": None, "media_noest": replicas,
        "agregada_lo": None, "agregada_hi": None, "agregada_noest": replicas,
        "ge50_lo": None, "ge50_hi": None, "ge50_noest": replicas,
    }
    # El contrato exige el marco completo, no una aproximacion que descarte filas.
    if n_sin_diseno or not conglomerados:
        return base

    estratos = {}
    for (estrato, _upm), contrib in conglomerados.items():
        estratos.setdefault(estrato, []).append(contrib)
    bloques = [np.asarray(estratos[e], dtype=float) for e in sorted(estratos)]
    base["n_estratos"] = len(bloques)
    base["n_upm"] = len(conglomerados)
    base["n_unica"] = sum(len(b) == 1 for b in bloques)

    rng = np.random.Generator(np.random.PCG64(seed))
    media = np.full(replicas, np.nan)
    agregada = np.full(replicas, np.nan)
    ge50 = np.full(replicas, np.nan)
    for replica in range(replicas):
        total = np.zeros(5, dtype=float)
        for bloque in bloques:
            k = bloque.shape[0]
            total += bloque[rng.integers(0, k, size=k)].sum(axis=0)
        # den_w, num_media, num_r, den_y, num_ge50
        if total[0] > 0:
            media[replica] = total[1] / total[0]
            ge50[replica] = total[4] / total[0]
        if total[3] > 0:
            agregada[replica] = total[2] / total[3]

    base["media_lo"], base["media_hi"], base["media_noest"] = _percentiles(media)
    base["agregada_lo"], base["agregada_hi"], base["agregada_noest"] = _percentiles(agregada)
    base["ge50_lo"], base["ge50_hi"], base["ge50_noest"] = _percentiles(ge50)
    if all(base[k] is not None for k in ("media_lo", "agregada_lo", "ge50_lo")):
        base["metodo"] = (
            "BOOTSTRAP-UPM-EN-ESTRATO-CON-UPM-UNICA"
            if base["n_unica"] else "BOOTSTRAP-UPM-EN-ESTRATO"
        )
    else:
        base["metodo"] = "NO-ESTIMABLE-REPLICAS"
    return base


def _vacios():
    salida = {
        P + "ESTADO": "NO-ESTIMABLE",
        P + "N-FILAS": 0,
        P + "N-COLUMNAS": 0,
        P + "LLAVE-HOGAR-UNICA": "NO-EVALUADO",
        P + "N-PESO-INVALIDO": 0,
        P + "N-REMESAS-AUSENTE-NOFINITA": 0,
        P + "N-REMESAS-NEGATIVA": 0,
        P + "UNIVERSO-VALIDO-N": 0,
        P + "UNIVERSO-VALIDO-MASA": None,
        P + "RECEPTORES-N": 0,
        P + "RECEPTORES-MASA": None,
        P + "PREVALENCIA": None,
        P + "PREVALENCIA-DELTA-PADRE": None,
        P + "PREVALENCIA-CONTROL-PADRE": "NO-EVALUADO",
        P + "REMESAS-MEDIA": None,
        P + "REMESAS-MEDIANA": None,
        P + "PARTICIPACION-N": 0,
        P + "PARTICIPACION-MASA": None,
        P + "EXCL-INGCOR-AUSENTE-NOFINITA-N": 0,
        P + "EXCL-INGCOR-AUSENTE-NOFINITA-MASA": 0.0,
        P + "EXCL-INGCOR-CERO-N": 0,
        P + "EXCL-INGCOR-CERO-MASA": 0.0,
        P + "EXCL-INGCOR-NEGATIVO-N": 0,
        P + "EXCL-INGCOR-NEGATIVO-MASA": 0.0,
        P + "R-MAYOR-Y-N": 0,
        P + "R-MAYOR-Y-MASA": 0.0,
        P + "R-MAYOR-Y-MAX-EXCESO": 0.0,
        P + "PARTICIPACION-MEDIA-HOGAR": None,
        P + "PARTICIPACION-AGREGADA": None,
        P + "PARTICIPACION-GE50": None,
        P + "PARTICIPACION-MEDIA-HOGAR-IC-LO": None,
        P + "PARTICIPACION-MEDIA-HOGAR-IC-HI": None,
        P + "PARTICIPACION-AGREGADA-IC-LO": None,
        P + "PARTICIPACION-AGREGADA-IC-HI": None,
        P + "PARTICIPACION-GE50-IC-LO": None,
        P + "PARTICIPACION-GE50-IC-HI": None,
        P + "DISENO-N-FILAS-MARCO": 0,
        P + "DISENO-N-SIN-DISENO": 0,
        P + "DISENO-N-ESTRATOS": 0,
        P + "DISENO-N-UPM": 0,
        P + "DISENO-N-ESTRATOS-UPM-UNICA": 0,
        P + "IC-N-REPLICAS-NOEST-MEDIA": 0,
        P + "IC-N-REPLICAS-NOEST-AGREGADA": 0,
        P + "IC-N-REPLICAS-NOEST-GE50": 0,
        P + "METODO-IC": "NO-EVALUADO",
    }
    return salida


def medir(inputs, contrato):
    salida = _vacios()
    parametros = contrato["parametros"]
    replicas = int(parametros["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    tolerancia_monetaria = float(parametros["tolerancia_componente_pesos"])
    referencia = float(parametros["prevalencia_padre"])
    tolerancia_prevalencia = float(parametros["tolerancia_prevalencia"])

    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as zf:
        if MIEMBRO not in set(zf.namelist()):
            salida[P + "ESTADO"] = "NO-ESTIMABLE-MIEMBRO-AUSENTE"
            return salida
        filas, ausentes, n_columnas = _abre(zf)

    salida[P + "N-FILAS"] = len(filas)
    salida[P + "N-COLUMNAS"] = n_columnas
    if ausentes:
        salida[P + "ESTADO"] = "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ",".join(ausentes)
        return salida

    llaves = [(_texto(f["folioviv"]), _texto(f["foliohog"])) for f in filas]
    if any(a is None or b is None for a, b in llaves):
        salida[P + "LLAVE-HOGAR-UNICA"] = "NO-LLAVE-INCOMPLETA"
        salida[P + "ESTADO"] = "NO-ESTIMABLE-LLAVE-INCOMPLETA"
        return salida
    if len(set(llaves)) != len(llaves):
        salida[P + "LLAVE-HOGAR-UNICA"] = "NO-DUPLICADA"
        salida[P + "ESTADO"] = "NO-ESTIMABLE-LLAVE-NO-UNICA"
        return salida
    salida[P + "LLAVE-HOGAR-UNICA"] = "SI"

    validos = []
    receptores = []
    marco_boot = []
    n_peso_invalido = n_r_falta = n_r_neg = 0
    exclusiones = {
        "AUSENTE-NOFINITA": [0, 0.0],
        "CERO": [0, 0.0],
        "NEGATIVO": [0, 0.0],
    }
    excepciones = []
    participacion = []

    for llave, fila in zip(llaves, filas):
        est = _texto(fila["est_dis"])
        upm = _texto(fila["upm"])
        contrib = np.zeros(5, dtype=float)
        marco_boot.append({"est_dis": est, "upm": upm, "contrib": contrib})

        peso = _numero(fila["factor"])
        if peso is None or peso <= 0:
            n_peso_invalido += 1
            continue
        remesa = _numero(fila["remesas"])
        if remesa is None:
            n_r_falta += 1
            continue
        if remesa < 0:
            n_r_neg += 1
            continue
        validos.append((llave, peso, remesa))
        if remesa == 0:
            continue
        receptores.append((llave, peso, remesa))

        ingreso = _numero(fila["ing_cor"])
        if ingreso is None:
            motivo = "AUSENTE-NOFINITA"
        elif ingreso == 0:
            motivo = "CERO"
        elif ingreso < 0:
            motivo = "NEGATIVO"
        else:
            motivo = None
        if motivo is not None:
            exclusiones[motivo][0] += 1
            exclusiones[motivo][1] += peso
            continue

        razon = remesa / ingreso
        participacion.append((llave, peso, remesa, ingreso, razon))
        contrib[:] = [
            peso,
            peso * razon,
            peso * remesa,
            peso * ingreso,
            peso if razon >= 0.5 else 0.0,
        ]
        if remesa > ingreso + tolerancia_monetaria:
            excepciones.append((peso, remesa - ingreso))

    salida[P + "N-PESO-INVALIDO"] = n_peso_invalido
    salida[P + "N-REMESAS-AUSENTE-NOFINITA"] = n_r_falta
    salida[P + "N-REMESAS-NEGATIVA"] = n_r_neg
    salida[P + "UNIVERSO-VALIDO-N"] = len(validos)
    salida[P + "UNIVERSO-VALIDO-MASA"] = float(sum(x[1] for x in validos)) if validos else None
    salida[P + "RECEPTORES-N"] = len(receptores)
    salida[P + "RECEPTORES-MASA"] = float(sum(x[1] for x in receptores)) if receptores else None

    if validos:
        masa_u = float(sum(x[1] for x in validos))
        masa_r = float(sum(x[1] for x in receptores))
        prevalencia = masa_r / masa_u
        delta = prevalencia - referencia
        salida[P + "PREVALENCIA"] = prevalencia
        salida[P + "PREVALENCIA-DELTA-PADRE"] = delta
        salida[P + "PREVALENCIA-CONTROL-PADRE"] = (
            "REPLICA-RESULTADO" if abs(delta) <= tolerancia_prevalencia else "NO-REPLICA"
        )

    if receptores:
        masa_r = float(sum(x[1] for x in receptores))
        salida[P + "REMESAS-MEDIA"] = float(sum(x[1] * x[2] for x in receptores) / masa_r)
        salida[P + "REMESAS-MEDIANA"] = mediana_ponderada(
            [x[2] for x in receptores], [x[1] for x in receptores]
        )

    for motivo, sufijo in (
        ("AUSENTE-NOFINITA", "AUSENTE-NOFINITA"),
        ("CERO", "CERO"),
        ("NEGATIVO", "NEGATIVO"),
    ):
        salida[P + f"EXCL-INGCOR-{sufijo}-N"] = exclusiones[motivo][0]
        salida[P + f"EXCL-INGCOR-{sufijo}-MASA"] = float(exclusiones[motivo][1])

    salida[P + "PARTICIPACION-N"] = len(participacion)
    salida[P + "PARTICIPACION-MASA"] = (
        float(sum(x[1] for x in participacion)) if participacion else None
    )
    salida[P + "R-MAYOR-Y-N"] = len(excepciones)
    salida[P + "R-MAYOR-Y-MASA"] = float(sum(x[0] for x in excepciones))
    salida[P + "R-MAYOR-Y-MAX-EXCESO"] = (
        float(max((x[1] for x in excepciones), default=0.0))
    )

    if participacion:
        den_w = float(sum(x[1] for x in participacion))
        salida[P + "PARTICIPACION-MEDIA-HOGAR"] = float(
            sum(x[1] * x[4] for x in participacion) / den_w
        )
        salida[P + "PARTICIPACION-AGREGADA"] = float(
            sum(x[1] * x[2] for x in participacion)
            / sum(x[1] * x[3] for x in participacion)
        )
        salida[P + "PARTICIPACION-GE50"] = float(
            sum(x[1] for x in participacion if x[4] >= 0.5) / den_w
        )

    boot = _bootstrap_marco(marco_boot, replicas, seed)
    salida[P + "PARTICIPACION-MEDIA-HOGAR-IC-LO"] = boot["media_lo"]
    salida[P + "PARTICIPACION-MEDIA-HOGAR-IC-HI"] = boot["media_hi"]
    salida[P + "PARTICIPACION-AGREGADA-IC-LO"] = boot["agregada_lo"]
    salida[P + "PARTICIPACION-AGREGADA-IC-HI"] = boot["agregada_hi"]
    salida[P + "PARTICIPACION-GE50-IC-LO"] = boot["ge50_lo"]
    salida[P + "PARTICIPACION-GE50-IC-HI"] = boot["ge50_hi"]
    salida[P + "DISENO-N-FILAS-MARCO"] = boot["n_filas_marco"]
    salida[P + "DISENO-N-SIN-DISENO"] = boot["n_sin_diseno"]
    salida[P + "DISENO-N-ESTRATOS"] = boot["n_estratos"]
    salida[P + "DISENO-N-UPM"] = boot["n_upm"]
    salida[P + "DISENO-N-ESTRATOS-UPM-UNICA"] = boot["n_unica"]
    salida[P + "IC-N-REPLICAS-NOEST-MEDIA"] = boot["media_noest"]
    salida[P + "IC-N-REPLICAS-NOEST-AGREGADA"] = boot["agregada_noest"]
    salida[P + "IC-N-REPLICAS-NOEST-GE50"] = boot["ge50_noest"]
    salida[P + "METODO-IC"] = boot["metodo"]

    if not receptores:
        salida[P + "ESTADO"] = "NO-ESTIMABLE-SIN-RECEPTORES"
    elif not participacion:
        salida[P + "ESTADO"] = "MONTOS-REPORTADOS-SIN-DOMINIO-PARTICIPACION"
    elif excepciones:
        salida[P + "ESTADO"] = "REPORTADO-CON-INCOMPATIBILIDAD-R-MAYOR-Y"
    elif n_peso_invalido or n_r_falta or n_r_neg or any(v[0] for v in exclusiones.values()):
        salida[P + "ESTADO"] = "REPORTADO-CON-EXCLUSIONES"
    else:
        salida[P + "ESTADO"] = "REPORTADO"
    return salida
