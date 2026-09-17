"""Agregado condicional ENCIG 2023 para RES-0007/0008.

Unidad: evento de tramite de sec_7, sin deduplicar. El desenlace P8_4 se
incorpora desde sec_8 por ID_TRA, con la llave de control heredada. El punto
usa FAC_TRA de sec_7. Los IC remuestrean UPM_DIS dentro de EST_DIS y vuelven a
calcular el cociente completo en cada replica.
"""
from __future__ import annotations

import csv
import io
import zipfile

import numpy as np


ZIP_ID = "encig23_base_datos_csv"
P = "RESULT-ENCIG23-AGCOND-"
M_S7 = "encig2023_04_sec_7.csv"
M_S8 = "encig2023_05_sec_8.csv"
COLS_S7 = [
    "ID_TRA", "NT_TIPO", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS",
    "UPM_DIS", "CVE_ENT", "UPM", "V_SEL", "R_ELE", "ID_VIV", "ID_PER",
]
COLS_S8 = ["ID_TRA", "P8_4", "ID_VIV", "ID_PER", "N_TRA", "FAC_P18"]
MAPA_P73 = set(range(1, 10))
MAPA_P84 = {0, 1}
GRUPOS = ("PRE", "DIG", "OTRO", "FALTANTE")


def _norm(col: str) -> str:
    return col.lstrip("\ufeff").lstrip("ï»¿").strip().strip('"').upper()


def _codigo(valor, blancos):
    if valor is None:
        return None
    texto = str(valor).strip().strip('"')
    if texto in blancos or texto.lower() in blancos:
        return None
    try:
        return int(texto)
    except ValueError:
        return "FUERA"


def _peso(valor):
    if valor is None:
        return None
    texto = str(valor).strip().replace(",", "")
    if not texto:
        return None
    try:
        numero = float(texto)
    except ValueError:
        return None
    if not np.isfinite(numero) or numero <= 0:
        return None
    return numero


def _llave(valor):
    if valor is None:
        return None
    texto = str(valor).strip().strip('"')
    return texto or None


def _abre(zf, miembro, columnas):
    """Lee solo columnas declaradas y conserva el orden original."""
    with zf.open(miembro) as fh:
        texto = io.TextIOWrapper(fh, encoding="latin-1", newline="")
        lector = csv.reader(texto)
        try:
            cabecera = [_norm(c) for c in next(lector)]
        except StopIteration:
            return [], list(columnas), 0
        indices = {c: cabecera.index(c) for c in columnas if c in cabecera}
        ausentes = [c for c in columnas if c not in indices]
        filas = []
        for fila in lector:
            if not fila:
                continue
            filas.append(tuple(
                fila[indices[c]] if c in indices and indices[c] < len(fila) else None
                for c in columnas
            ))
        return filas, ausentes, len(cabecera)


def _clasifica_canal(codigo, pre, dig):
    if codigo in pre:
        return "PRE"
    if codigo in dig:
        return "DIG"
    if codigo is None:
        return "FALTANTE"
    return "OTRO"


def _resumen(filas):
    """Devuelve n, masas de denominador/numerador y p/q directos."""
    n = len(filas)
    den = float(sum(f[0] for f in filas))
    num = float(sum(f[0] for f in filas if f[1] == 1))
    num_q = float(sum(f[0] for f in filas if f[1] == 0))
    p = num / den if den > 0 else None
    q = num_q / den if den > 0 else None
    return {"n": n, "den": den, "num": num, "num_q": num_q, "p": p, "q": q}


def _bootstrap_cociente(filas, replicas, seed):
    """Bootstrap de conglomerados dentro de estrato; cociente por replica."""
    conglomerados = {}
    n_sin_diseno = 0
    for peso, desenlace, _canal, estrato, upm in filas:
        if estrato is None or upm is None:
            n_sin_diseno += 1
            continue
        bloque = conglomerados.setdefault((estrato, upm), [0.0, 0.0])
        bloque[0] += peso
        if desenlace == 1:
            bloque[1] += peso
    if not conglomerados:
        return {
            "lo": None, "hi": None, "n_estratos": 0, "n_upm": 0,
            "n_unica": 0, "n_no_estimables": replicas,
            "n_sin_diseno": n_sin_diseno,
            "metodo": "NO-ESTIMABLE-DISENO-INCOMPLETO",
        }

    estratos = {}
    for (estrato, _upm), masas in conglomerados.items():
        estratos.setdefault(estrato, []).append(masas)
    bloques = [np.asarray(estratos[e], dtype=float) for e in sorted(estratos)]
    n_unica = sum(len(b) == 1 for b in bloques)
    rng = np.random.Generator(np.random.PCG64(seed))
    valores = np.empty(replicas, dtype=float)
    for replica in range(replicas):
        den = 0.0
        num = 0.0
        for bloque in bloques:
            k = bloque.shape[0]
            muestra = bloque[rng.integers(0, k, size=k)]
            den += float(muestra[:, 0].sum())
            num += float(muestra[:, 1].sum())
        valores[replica] = num / den if den > 0 else np.nan
    finitos = valores[np.isfinite(valores)]
    no_estimables = int(replicas - finitos.size)
    if finitos.size == 0:
        lo = hi = None
        metodo = "NO-ESTIMABLE-REPLICAS"
    else:
        lo = float(np.percentile(finitos, 2.5))
        hi = float(np.percentile(finitos, 97.5))
        metodo = (
            "BOOTSTRAP-UPM-EN-ESTRATO-CON-UPM-UNICA"
            if n_unica else "BOOTSTRAP-UPM-EN-ESTRATO"
        )
    return {
        "lo": lo, "hi": hi, "n_estratos": len(bloques),
        "n_upm": len(conglomerados), "n_unica": n_unica,
        "n_no_estimables": no_estimables, "n_sin_diseno": n_sin_diseno,
        "metodo": metodo,
    }


def _vacios():
    salida = {
        P + "ESTADO": "NO-ESTIMABLE",
        P + "JOIN-ESTADO": "NO-EVALUADO",
        P + "JOIN-N-SEC7": 0,
        P + "JOIN-N-SEC8": 0,
        P + "JOIN-N-EMPAREJADOS": 0,
        P + "JOIN-N-SIN-PAREJA": 0,
        P + "JOIN-COBERTURA-N": None,
        P + "JOIN-COBERTURA-MASA": None,
        P + "DESENLACE-N-OBSERVADO": 0,
        P + "DESENLACE-N-FALTANTE": 0,
        P + "DESENLACE-COBERTURA-N": None,
        P + "DESENLACE-COBERTURA-MASA": None,
        P + "N-PESO-INVALIDO": 0,
        P + "SOPORTE-P73": "NO-EVALUADO",
        P + "SOPORTE-P84": "NO-EVALUADO",
    }
    for universo in ("PRIMARIO", "PREDIG"):
        salida.update({
            P + f"{universo}-N": 0,
            P + f"{universo}-MASA-DEN": None,
            P + f"{universo}-MASA-NUM": None,
            P + f"{universo}-P": None,
            P + f"{universo}-Q": None,
            P + f"{universo}-IC-P-LO": None,
            P + f"{universo}-IC-P-HI": None,
            P + f"{universo}-IC-Q-LO": None,
            P + f"{universo}-IC-Q-HI": None,
            P + f"{universo}-N-ESTRATOS": 0,
            P + f"{universo}-N-UPM": 0,
            P + f"{universo}-N-ESTRATOS-UPM-UNICA": 0,
            P + f"{universo}-N-REPLICAS-NO-ESTIMABLES": 0,
            P + f"{universo}-N-SIN-DISENO": 0,
            P + f"{universo}-METODO-IC": "NO-EVALUADO",
        })
    for grupo in GRUPOS:
        salida.update({
            P + f"CANAL-{grupo}-N": 0,
            P + f"CANAL-{grupo}-MASA-DEN": 0.0,
            P + f"CANAL-{grupo}-MASA-NUM": 0.0,
            P + f"CANAL-{grupo}-P": None,
            P + f"CANAL-{grupo}-Q": None,
        })
    return salida


def _soporte(valores):
    conteos = {}
    for valor in valores:
        clave = "b" if valor is None else str(valor)
        conteos[clave] = conteos.get(clave, 0) + 1
    return ";".join(
        f"{k}:{conteos[k]}"
        for k in sorted(conteos, key=lambda x: (x == "b", x == "FUERA", x))
    )


def medir(inputs, contrato):
    salida = _vacios()
    parametros = contrato["parametros"]
    blancos = {str(x) for x in parametros["blanco_literal"]}
    pre = {int(x) for x in parametros["canal_pre"]}
    dig = {int(x) for x in parametros["canal_dig"]}
    replicas = int(parametros["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])

    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as zf:
        nombres = set(zf.namelist())
        faltan_miembros = [m for m in (M_S7, M_S8) if m not in nombres]
        if faltan_miembros:
            salida[P + "ESTADO"] = "NO-ESTIMABLE-MIEMBRO-AUSENTE:" + ",".join(faltan_miembros)
            return salida
        s7, falta7, _ = _abre(zf, M_S7, COLS_S7)
        s8, falta8, _ = _abre(zf, M_S8, COLS_S8)

    salida[P + "JOIN-N-SEC7"] = len(s7)
    salida[P + "JOIN-N-SEC8"] = len(s8)
    ausentes = [f"{M_S7}:{c}" for c in falta7] + [f"{M_S8}:{c}" for c in falta8]
    if ausentes:
        salida[P + "ESTADO"] = "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ",".join(ausentes)
        return salida

    i7 = {c: i for i, c in enumerate(COLS_S7)}
    i8 = {c: i for i, c in enumerate(COLS_S8)}
    ids8 = [_llave(r[i8["ID_TRA"]]) for r in s8]
    if len(set(ids8)) != len(ids8):
        salida[P + "JOIN-ESTADO"] = "NO-ESTIMABLE-LLAVE-NO-UNICA:SEC8-ID_TRA"
        salida[P + "ESTADO"] = salida[P + "JOIN-ESTADO"]
        return salida

    p84 = {k: _codigo(r[i8["P8_4"]], blancos) for k, r in zip(ids8, s8)}
    codigos84 = [p84[k] for k in ids8]
    codigos73 = [_codigo(r[i7["P7_3"]], blancos) for r in s7]
    salida[P + "SOPORTE-P84"] = _soporte(codigos84)
    salida[P + "SOPORTE-P73"] = _soporte(codigos73)
    if any(c == "FUERA" or (c is not None and c not in MAPA_P84) for c in codigos84):
        salida[P + "ESTADO"] = "NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P8_4"
        return salida
    if any(c == "FUERA" or (c is not None and c not in MAPA_P73) for c in codigos73):
        salida[P + "ESTADO"] = "NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P7_3"
        return salida

    ctrl8 = {
        (_llave(r[i8["ID_VIV"]]), _llave(r[i8["ID_PER"]]),
         _llave(r[i8["ID_TRA"]]), _llave(r[i8["N_TRA"]]))
        for r in s8
    }
    emp_prim = {
        n for n, r in enumerate(s7) if _llave(r[i7["ID_TRA"]]) in p84
    }
    emp_ctrl = {
        n for n, r in enumerate(s7)
        if (_llave(r[i7["ID_VIV"]]), _llave(r[i7["ID_PER"]]),
            _llave(r[i7["ID_TRA"]]), _llave(r[i7["N_TRA"]])) in ctrl8
    }
    if emp_prim != emp_ctrl:
        salida[P + "JOIN-ESTADO"] = f"NO-ESTIMABLE-JOIN-CONTROL-DIFIERE:{len(emp_prim)}/{len(emp_ctrl)}"
        salida[P + "ESTADO"] = salida[P + "JOIN-ESTADO"]
        return salida

    salida[P + "JOIN-ESTADO"] = "JOIN-EXACTO"
    salida[P + "JOIN-N-EMPAREJADOS"] = len(emp_prim)
    salida[P + "JOIN-N-SIN-PAREJA"] = len(s7) - len(emp_prim)
    salida[P + "JOIN-COBERTURA-N"] = len(emp_prim) / len(s7) if s7 else None

    masa_sec7 = 0.0
    masa_emparejada = 0.0
    n_base_obs = n_obs = n_falta = n_peso_invalido = 0
    masa_base_obs = masa_obs = 0.0
    filas = []  # peso, desenlace, grupo_canal, estrato, upm
    for numero, r in enumerate(s7):
        peso = _peso(r[i7["FAC_TRA"]])
        if peso is None:
            n_peso_invalido += 1
            continue
        masa_sec7 += peso
        if numero not in emp_prim:
            continue
        masa_emparejada += peso
        n_base_obs += 1
        masa_base_obs += peso
        desenlace = p84[_llave(r[i7["ID_TRA"]])]
        if desenlace is None:
            n_falta += 1
            continue
        n_obs += 1
        masa_obs += peso
        canal = _clasifica_canal(_codigo(r[i7["P7_3"]], blancos), pre, dig)
        filas.append((
            peso, int(desenlace), canal,
            _llave(r[i7["EST_DIS"]]), _llave(r[i7["UPM_DIS"]]),
        ))

    salida[P + "N-PESO-INVALIDO"] = n_peso_invalido
    salida[P + "JOIN-COBERTURA-MASA"] = masa_emparejada / masa_sec7 if masa_sec7 > 0 else None
    salida[P + "DESENLACE-N-OBSERVADO"] = n_obs
    salida[P + "DESENLACE-N-FALTANTE"] = n_falta
    salida[P + "DESENLACE-COBERTURA-N"] = n_obs / n_base_obs if n_base_obs else None
    salida[P + "DESENLACE-COBERTURA-MASA"] = masa_obs / masa_base_obs if masa_base_obs > 0 else None

    if not filas:
        salida[P + "ESTADO"] = "NO-ESTIMABLE-UNIVERSO-VACIO"
        return salida

    por_grupo = {g: [f for f in filas if f[2] == g] for g in GRUPOS}
    for grupo, seleccion in por_grupo.items():
        resumen = _resumen(seleccion)
        salida[P + f"CANAL-{grupo}-N"] = resumen["n"]
        salida[P + f"CANAL-{grupo}-MASA-DEN"] = resumen["den"]
        salida[P + f"CANAL-{grupo}-MASA-NUM"] = resumen["num"]
        salida[P + f"CANAL-{grupo}-P"] = resumen["p"]
        salida[P + f"CANAL-{grupo}-Q"] = resumen["q"]

    universos = {
        "PRIMARIO": filas,
        "PREDIG": por_grupo["PRE"] + por_grupo["DIG"],
    }
    for universo, seleccion in universos.items():
        resumen = _resumen(seleccion)
        salida[P + f"{universo}-N"] = resumen["n"]
        salida[P + f"{universo}-MASA-DEN"] = resumen["den"] if seleccion else None
        salida[P + f"{universo}-MASA-NUM"] = resumen["num"] if seleccion else None
        salida[P + f"{universo}-P"] = resumen["p"]
        salida[P + f"{universo}-Q"] = resumen["q"]
        ic = _bootstrap_cociente(seleccion, replicas, seed)
        salida[P + f"{universo}-IC-P-LO"] = ic["lo"]
        salida[P + f"{universo}-IC-P-HI"] = ic["hi"]
        # Transformacion monotona decreciente: extremos invertidos.
        salida[P + f"{universo}-IC-Q-LO"] = None if ic["hi"] is None else 1.0 - ic["hi"]
        salida[P + f"{universo}-IC-Q-HI"] = None if ic["lo"] is None else 1.0 - ic["lo"]
        salida[P + f"{universo}-N-ESTRATOS"] = ic["n_estratos"]
        salida[P + f"{universo}-N-UPM"] = ic["n_upm"]
        salida[P + f"{universo}-N-ESTRATOS-UPM-UNICA"] = ic["n_unica"]
        salida[P + f"{universo}-N-REPLICAS-NO-ESTIMABLES"] = ic["n_no_estimables"]
        salida[P + f"{universo}-N-SIN-DISENO"] = ic["n_sin_diseno"]
        salida[P + f"{universo}-METODO-IC"] = ic["metodo"]

    salida[P + "ESTADO"] = "TASA-REPORTADA-CON-RESERVA"
    return salida
