#!/usr/bin/env python3
"""Reconstrucción independiente CALC-PEW-RELIGION-2024-0001 desde paquete/docs/spec-humana.md.

Ejecutar desde el directorio de trabajo: python3 salida/codigo/reconstruye.py
Lee solo las columnas autorizadas de paquete/datos/pew2024.sav; escribe salida/resultado.json
y salida/diagnostico.json.
"""
import csv
import json
import os
import sys

sys.path.insert(0, "paquete/lib")
import numpy as np
import pandas as pd
import pyreadstat

SAV = "paquete/datos/pew2024.sav"
ESQUEMA = "paquete/esquema-identidades.tsv"
COLUMNAS = ["country", "weight", "age", "gender", "d_educ_mexico",
            "religion_combined", "religion_christian", "religion_switch", "god"]
IDENTIDAD = {"paquete": "pew-religion-2024-0001",
             "version_entrada": "validacion-continua-1",
             "sha256_entrada": "e54f9c296d234cdc2867bcd3a2d508bb462edc98cfb64aeaf6b942e64408149e"}

PAIS = 35
EDAD_MIN, EDAD_MAX = 18, 97
SEMILLA = 20261002
REPLICAS = 2000
BLOQUE = 50

EDAD_CORTES = {"18-29": (18, 29), "30-44": (30, 44), "45-59": (45, 59), "60-MAS": (60, 97)}
ESCOL = {"HASTA-PRIMARIA": (1, 2, 3), "SECUNDARIA": (4, 5),
         "MEDIA-SUPERIOR": (6, 7, 8, 9), "SUPERIOR": (10, 11, 12)}
SEXO = {"HOMBRE": 1, "MUJER": 2}

RC_VALIDOS = (1, 2, 3, 4, 5, 6, 7, 99)


def lee():
    df, _ = pyreadstat.read_sav(SAV, usecols=COLUMNAS)
    return df


def conducta(df, nombre):
    """Devuelve (valido, uno) como arrays booleanos (sección 2 de la spec)."""
    rc = df["religion_combined"]
    if nombre == "catolico":
        v = rc.isin(RC_VALIDOS)
        u = v & (df["religion_christian"] == 1)
    elif nombre == "sin-religion":
        v = rc.isin(RC_VALIDOS)
        u = v & (rc == 7)
    elif nombre == "cambio-de-religion":
        s = df["religion_switch"]
        v = s.isin((1, 2))
        u = s == 1
    elif nombre == "cree-en-dios":
        g = df["god"]
        v = g.isin((1, 2))
        u = g == 1
    else:
        raise ValueError(nombre)
    return v.to_numpy(), u.to_numpy()


def segmento(df, eje, seg):
    """Devuelve (en_segmento, codigo_eje_valido) sobre el universo."""
    if eje == "TOTAL":
        t = np.ones(len(df), dtype=bool)
        return t, t
    if eje == "SEXO":
        g = df["gender"]
        return (g == SEXO[seg]).to_numpy(), g.isin((1, 2)).to_numpy()
    if eje == "EDAD":
        a = df["age"]
        lo, hi = EDAD_CORTES[seg]
        return ((a >= lo) & (a <= hi)).to_numpy(), ((a >= 18) & (a <= 97)).to_numpy()
    if eje == "ESCOLARIDAD":
        e = df["d_educ_mexico"]
        return e.isin(ESCOL[seg]).to_numpy(), e.isin(range(1, 13)).to_numpy()
    raise ValueError(eje)


def conteos_bootstrap(n):
    """Matriz (REPLICAS x n) de multiplicidades: remuestreo con reemplazo de n entrevistas,
    PCG64(SEMILLA), generado en bloques de BLOQUE réplicas."""
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    out = np.empty((REPLICAS, n), dtype=np.float64)
    for b0 in range(0, REPLICAS, BLOQUE):
        b = min(BLOQUE, REPLICAS - b0)
        idx = rng.integers(0, n, size=(b, n))
        for j in range(b):
            out[b0 + j] = np.bincount(idx[j], minlength=n)
    return out


def fnum(x):
    return repr(float(x))


def main():
    df = lee()
    n_archivo = len(df)
    mx = df[df["country"] == PAIS].reset_index(drop=True)
    n_pais = len(mx)
    w_raw = mx["weight"].to_numpy(dtype=float)
    peso_ok = np.isfinite(w_raw) & (w_raw > 0)
    diseno = mx[peso_ok].reset_index(drop=True)
    w = diseno["weight"].to_numpy(dtype=float)
    n_dis = len(diseno)
    a = diseno["age"]
    univ = ((a >= EDAD_MIN) & (a <= EDAD_MAX)).to_numpy()
    fuera_univ = {
        "age_nan": int(a.isna().sum()),
        "age_menor_18": int((a < 18).sum()),
        "age_98_no_sabe": int((a == 98).sum()),
        "age_99_rechaza": int((a == 99).sum()),
        "age_otro_fuera": int(((a > 97) & ~a.isin((98, 99))).sum()),
    }

    C = conteos_bootstrap(n_dis)

    with open(ESQUEMA, newline="", encoding="utf-8") as f:
        esquema = list(csv.DictReader(f, delimiter="\t"))

    filas, diag_llaves = [], []
    for r in esquema:
        llave, unidad = r["llave"], r["unidad"]
        cond, eje, seg = r["conducta"], r["eje"], r["segmento"]
        v, u = conducta(diseno, cond)
        enseg, eje_ok = segmento(diseno, eje, seg)
        dom = univ & enseg
        den_ind = (dom & v).astype(float)
        num_ind = (dom & v & u).astype(float)
        d = {
            "llave": llave, "conducta": cond, "eje": eje, "segmento": seg,
            "n_filas_pais": int(n_pais),
            "excl_peso_no_valido": int((~peso_ok).sum()),
            "n_diseno": int(n_dis),
            "excl_fuera_universo_edad": int((~univ).sum()),
            "excl_fuera_universo_detalle": fuera_univ,
            "excl_eje_codigo_no_valido_en_universo": int((univ & ~eje_ok).sum()),
            "excl_otro_segmento_en_universo": int((univ & eje_ok & ~enseg).sum()),
            "n_dominio": int(dom.sum()),
            "excl_conducta_no_valida_en_dominio": int((dom & ~v).sum()),
            "n_valido": int(den_ind.sum()),
            "n_uno": int(num_ind.sum()),
            "suma_pesos_valido": fnum((w * den_ind).sum()),
        }
        fila = {"llave": llave, "unidad": unidad}
        S = (w * den_ind).sum()
        if den_ind.sum() == 0 or S <= 0:
            fila.update(estado="DENOMINADOR-CERO",
                        motivo="dominio observado sin entrevistas válidas (Σw del denominador = 0) bajo spec suficiente")
            d["replicas_degeneradas"] = None
        else:
            p = (w * num_ind).sum() / S
            nb = C @ (w * num_ind)
            db = C @ (w * den_ind)
            deg = int((~(db > 0)).sum())
            d["replicas_degeneradas"] = deg
            fila.update(estado="RECONSTRUIDO", punto=fnum(p))
            if deg > 0:
                fila.update(estado_ic="NO-IDENTIFICADA",
                            motivo_ic=f"{deg} de {REPLICAS} réplicas bootstrap con denominador cero; contrato conservador de la spec §4: una réplica degenerada → sin EE ni IC")
            else:
                rb = nb / db
                lo, hi = np.percentile(rb, [2.5, 97.5])
                fila.update(estado_ic="CALCULADO", ic95_inf=fnum(lo), ic95_sup=fnum(hi))
                d["ee_bootstrap"] = fnum(rb.std(ddof=1))
        filas.append(fila)
        diag_llaves.append(d)

    resultado = {"version": 3, "identidad": IDENTIDAD, "filas": filas}

    decisiones = [
        {"decision": "Unidad de remuestreo = cada entrevista del diseño válido (México, peso finito > 0), incluidas las fuera de universo de edad; el universo 18–97 y el segmento se aplican como indicadores de dominio dentro de cada réplica (estimación por subpoblación, no condicionando el remuestreo).",
         "frase": "Válido para el diseño: peso finito > 0 (`M.prepara_diseno`); la validez de universo (18+) se aplica aparte, sobre el diseño ya válido."},
        {"decision": "Bootstrap ponderado = remuestreo con reemplazo de n de n entrevistas (sin estratos), multiplicidades aplicadas sobre el peso original; réplica = Σ c·w·y / Σ c·w·v. Sin reescalado tipo Rao-Wu (n-1).",
         "frase": "bootstrap ponderado de entrevistas (sin UPM: cada fila su propia unidad de remuestreo"},
        {"decision": "Generador numpy.random.Generator(numpy.random.PCG64(20261002)); índices con rng.integers(0, n, size=(50, n)) por bloque, 40 bloques = 2000 réplicas. Una misma matriz de réplicas (una sola semilla) se usa para las 44 llaves (equivale a re-sembrar por llave).",
         "frase": "`numpy.PCG64(20261002)`, 2000 réplicas, bloques de 50"},
        {"decision": "IC95 = percentiles 2.5 y 97.5 de las réplicas con numpy.percentile (interpolación lineal por defecto).",
         "frase": "percentiles 2.5/97.5"},
        {"decision": "Réplica degenerada = réplica con denominador ponderado Σ c·w·v = 0 (razón indefinida). Si hay al menos una, la llave queda RECONSTRUIDO con estado_ic NO-IDENTIFICADA. Réplicas con varianza cero (p=0 o 1) no se consideran degeneradas.",
         "frase": "contrato conservador (una réplica degenerada → sin EE ni IC)"},
        {"decision": "CATOLICO y SIN-RELIGION: denominador = religion_combined en {1..7, 99}; religion_christian ausente (no cristianos) cuenta como CERO si el denominador es válido.",
         "frase": "sobre filas con `religion_combined` en código válido (1–7, 99; ...), UNO si además `religion_christian` = 1"},
        {"decision": "CAMBIO-DE-RELIGION: válido solo códigos 1/2; cualquier otro valor o ausente fuera (ni UNO ni CERO).",
         "frase": "| CAMBIO-DE-RELIGION | `religion_switch` ... | 1 | 2 |"},
        {"decision": "Eje SEXO/ESCOLARIDAD: filas del universo con código fuera de catálogo (p.ej. 98/99 escolaridad) no pertenecen a ningún segmento; no se excluyen del universo en el eje TOTAL.",
         "frase": "Un eje a la vez; nunca cruces."},
        {"decision": "EDAD 60-MAS = 60..97 (97 = «97 o más»).",
         "frase": "cortes fijos del motor 18-29, 30-44, 45-59, 60-MAS — 98/99 fuera del universo"},
        {"decision": "No se aplica umbral de soporte mínimo ni supresión: la spec no fija valor numérico de soporte y el encargo prohíbe suprimir por publicabilidad.",
         "frase": "todas las ramas terminales — con soporte, sin soporte, categoría vacía, ..."},
        {"decision": "Los NaN de pyreadstat (celdas sistema-missing) se tratan como fuera de cualquier código válido.",
         "frase": "Códigos 8/9 (`god`) y cualquier código fuera de 1–7/99 (`religion_combined`) quedan fuera por diseño (ni UNO ni CERO)"},
    ]
    diagnostico = {
        "identidad": IDENTIDAD,
        "n_filas_archivo": int(n_archivo),
        "n_filas_pais_35": int(n_pais),
        "n_excl_peso_no_valido": int((~peso_ok).sum()),
        "n_diseno_valido": int(n_dis),
        "n_universo_18_97": int(univ.sum()),
        "fuera_universo": fuera_univ,
        "parametros": {"semilla": SEMILLA, "replicas": REPLICAS, "bloque": BLOQUE,
                       "percentiles": [2.5, 97.5], "diseno": "MAS-PONDERADO-SIN-ESTRATO"},
        "decisiones": decisiones,
        "llaves": diag_llaves,
    }

    os.makedirs("salida", exist_ok=True)
    with open("salida/resultado.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open("salida/diagnostico.json", "w", encoding="utf-8") as f:
        json.dump(diagnostico, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
