"""Reconstrucción independiente de RESULT-ENCUCI-B-P-RUR-AGR (ENCUCI 2020).

Punto: paquete/encuci-rural-restaurado.md.
IC: paquete/residuales-p3-contrato-ic.md + residuales-p3-modulos-ic.md (firmados, R26).
Salida: paquete/CONTRATO-v3.md (firmado, R31).
Ejecutar desde el directorio de trabajo: python3 salida/codigo/reconstruye.py
"""
import csv
import hashlib
import json
import math
import os
import platform
import subprocess
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbf  # noqa: E402

PAQ = "paquete"
SAL = "salida"
F45 = os.path.join(PAQ, "datos", "ENCUCI_2020_SEC_4_5.dbf")
F678 = os.path.join(PAQ, "datos", "ENCUCI_2020_SEC_6_7_8.dbf")

IDENTIDAD = {
    "paquete": "encuci-0001",
    "version_entrada": "residuales-documentales-v2",
    "sha256_entrada": "1b7e98c5a2360cfa4f415340ba957227136fa15687d6ee4d5d28ed42fb278ce6",
}
FIRMADOS = {
    "residuales-p3-contrato-ic.md": "f09ffd47ee2bfbb80d210b4af0d2c29c1b0e7515f92ca85a051d3654ab9338bb",
    "residuales-p3-modulos-ic.md": "d360280cd34b7067ef35af8a42091c3c03a352910faba4be33659a41d0006c98",
    "CONTRATO-v3.md": "821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb",
}
B = 2000
SEMILLA = 20260923
Q_INF, Q_SUP = 0.025, 0.975
MARCA_SINGLETON = "IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA"

# Columnas autorizadas (y solo esas) por archivo.
COLS_678 = ["ID_PER", "AP7_3_5", "FAC_SEL", "EST_DIS", "UPM_DIS", "DOMINIO"]
COLS_45 = ["ID_PER", "AP4_3_2", "DOMINIO"]


def sha256_archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def r(x):
    return repr(float(x))


def quitar_relleno_dbf(s):
    """Retira solo el relleno de ancho fijo del formato DBF (espacios a la derecha)."""
    return s.rstrip(" ")


def codigo(s):
    """Normaliza un código numérico: 1 y 1.000000000000000 -> 1. Blanco -> None."""
    t = s.strip()
    if t == "":
        return None
    try:
        v = float(t)
    except ValueError:
        return "no-numerico"
    if not math.isfinite(v):
        return "no-finito"
    if v == 1.0:
        return 1
    if v == 2.0:
        return 2
    if v == 9.0:
        return 9
    return "otro"


def peso(s):
    t = s.strip()
    if t == "":
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    return v if (math.isfinite(v) and v > 0) else None


def cuantil_tipo7(ordenadas, q):
    n = len(ordenadas)
    a = (n - 1) * q
    j = math.floor(a)
    if j >= n - 1:
        return float(ordenadas[n - 1])
    return float((1 - a + j) * ordenadas[j] + (a - j) * ordenadas[j + 1])


def escribir_entorno():
    uname = subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()
    txt = (
        f"python {sys.version}\n"
        f"numpy {np.__version__}\n"
        f"pandas {pd.__version__}\n"
        "lector DBF: propio (salida/codigo/dbf.py); dbfread y pyreadstat no instalados\n"
        f"plataforma {platform.platform()}\n"
        f"uname -a: {uname}\n"
    )
    ruta = os.path.join(SAL, "entorno.txt")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(txt)
    return sha256_archivo(ruta)


def main():
    os.makedirs(SAL, exist_ok=True)
    hash_entorno = escribir_entorno()
    for nombre, esperado in FIRMADOS.items():
        obs = sha256_archivo(os.path.join(PAQ, nombre))
        if obs != esperado:
            raise SystemExit(f"sha256 de {nombre} no coincide con la firma: {obs}")

    with open(os.path.join(PAQ, "esquema-identidades.tsv"), encoding="utf-8", newline="") as f:
        esquema = list(csv.DictReader(f, delimiter="\t"))
    assert len(esquema) == 1 and esquema[0]["llave"] == "RESULT-ENCUCI-B-P-RUR-AGR"
    fila_esq = esquema[0]

    # --- Lectura (solo columnas autorizadas) ---
    c678, del678 = dbf.leer_columnas(F678, COLS_678)
    c45, del45 = dbf.leer_columnas(F45, COLS_45)
    n678, n45 = len(del678), len(del45)

    # --- Llaves únicas ---
    id678 = [quitar_relleno_dbf(x) for x in c678["ID_PER"]]
    id45 = [quitar_relleno_dbf(x) for x in c45["ID_PER"]]
    vivos45 = [id45[i] for i in range(n45) if not del45[i]]
    dup678 = n678 - len(set(id678))
    dup45 = len(vivos45) - len(set(vivos45))
    blancos_id = sum(1 for x in id678 if x.strip() == "") + sum(1 for x in vivos45 if x.strip() == "")
    join_ambiguo = dup678 > 0 or dup45 > 0 or blancos_id > 0
    mapa45 = {id45[i]: i for i in range(n45) if not del45[i]}

    # --- Construcción por fila de la tabla base SEC_6_7_8, en orden físico ---
    causas = [
        "registro_borrado_dbf",
        "peso_FAC_SEL_no_finito_o_no_positivo",
        "diseno_EST_DIS_UPM_DIS_ausente",
        "sin_pareja_en_SEC_4_5",
        "DOMINIO_fuera_de_UCR",
        "fuera_de_dominio_DOMINIO_U_o_C",
        "AP4_3_2_blanco_9_u_otro",
        "fuera_de_dominio_AP4_3_2_igual_2",
        "AP7_3_5_blanco_9_u_otro",
    ]
    excl_n = {c: 0 for c in causas}
    excl_w = {c: 0.0 for c in causas}
    marginal = {"AP7_3_5": {}, "AP4_3_2_pareados": {}, "DOMINIO_678": {}}
    dominio_discrepa = 0

    marco_filas = []  # (i, est, upm, w, dk, y)
    n_validos = 0
    for i in range(n678):
        if del678[i]:
            excl_n["registro_borrado_dbf"] += 1
            continue
        w = peso(c678["FAC_SEL"][i])
        if w is None:
            excl_n["peso_FAC_SEL_no_finito_o_no_positivo"] += 1
            continue
        est = quitar_relleno_dbf(c678["EST_DIS"][i])
        upm = quitar_relleno_dbf(c678["UPM_DIS"][i])
        if est.strip() == "" or upm.strip() == "":
            excl_n["diseno_EST_DIS_UPM_DIS_ausente"] += 1
            excl_w["diseno_EST_DIS_UPM_DIS_ausente"] += w
            continue
        a7 = codigo(c678["AP7_3_5"][i])
        dom = c678["DOMINIO"][i].strip()
        marginal["AP7_3_5"][str(a7)] = marginal["AP7_3_5"].get(str(a7), 0) + 1
        marginal["DOMINIO_678"][dom] = marginal["DOMINIO_678"].get(dom, 0) + 1
        j = mapa45.get(id678[i])
        causa = None
        a4 = None
        if j is None:
            causa = "sin_pareja_en_SEC_4_5"
        else:
            a4 = codigo(c45["AP4_3_2"][j])
            marginal["AP4_3_2_pareados"][str(a4)] = marginal["AP4_3_2_pareados"].get(str(a4), 0) + 1
            if c45["DOMINIO"][j].strip() != dom:
                dominio_discrepa += 1
            if dom not in ("U", "C", "R"):
                causa = "DOMINIO_fuera_de_UCR"
            elif dom != "R":
                causa = "fuera_de_dominio_DOMINIO_U_o_C"
            elif a4 not in (1, 2):
                causa = "AP4_3_2_blanco_9_u_otro"
            elif a4 == 2:
                causa = "fuera_de_dominio_AP4_3_2_igual_2"
            elif a7 not in (1, 2):
                causa = "AP7_3_5_blanco_9_u_otro"
        if causa is not None:
            excl_n[causa] += 1
            excl_w[causa] += w
            marco_filas.append((i, est, upm, w, 0, 0))
        else:
            n_validos += 1
            marco_filas.append((i, est, upm, w, 1, 1 if a7 == 1 else 0))

    sin_pareja_45 = len(set(mapa45) - set(id678))

    # --- Totales por par (estrato, UPM) en orden físico ---
    pares = {}
    for (_, est, upm, w, dk, y) in marco_filas:
        k = (est, upm)
        if k not in pares:
            pares[k] = [0.0, 0.0, 0]
        if dk:
            pares[k][0] += w * y
            pares[k][1] += w
            pares[k][2] += 1
    orden = sorted(pares)  # lexicográfico por puntos Unicode de (estrato, UPM)
    Xhu = np.array([pares[k][0] for k in orden], dtype=np.float64)
    Yhu = np.array([pares[k][1] for k in orden], dtype=np.float64)
    Nhu = np.array([pares[k][2] for k in orden], dtype=np.int64)
    X = 0.0
    Y = 0.0
    for a, b in zip(Xhu, Yhu):
        X += a
        Y += b
    # Diagnóstico: suma directa en orden físico de filas (no alimenta la salida).
    Xf = 0.0
    Yf = 0.0
    for (_, _, _, w, dk, y) in marco_filas:
        if dk:
            Xf += w * y
            Yf += w

    estratos = {}
    for idx, (est, _) in enumerate(orden):
        estratos.setdefault(est, []).append(idx)
    orden_estratos = sorted(estratos)
    n_singleton = sum(1 for h in orden_estratos if len(estratos[h]) == 1)
    n_upm_conocidos = int((Nhu > 0).sum())

    fila = {"llave": fila_esq["llave"], "unidad": fila_esq["unidad"]}
    diag_ic = {
        "llave": fila_esq["llave"], "tipo_incertidumbre": "", "se": "", "n_conocidos": n_validos,
        "n_upm_marco": len(orden), "n_upm_conocidos": n_upm_conocidos, "n_singleton": n_singleton,
        "n_replicas_no_estimables": "", "B": B, "semilla": SEMILLA,
        "RNG": "numpy.random.Generator(numpy.random.PCG64(20260923)); rng.choice(indices_ordenados,n_h,replace=True); replica->estrato lexicografico",
        "regla_marco": "pares distintos (EST_DIS,UPM_DIS) de SEC_6_7_8 con FAC_SEL finito>0 y diseno no vacio, antes de filtrar pareja/DOMINIO/AP4_3_2/AP7_3_5; incluye pares con X_hu=Y_hu=0",
        "cuantil": "tipo7 lineal; q=0.025,0.975",
        "hash_contrato": FIRMADOS["residuales-p3-contrato-ic.md"] + "+" + FIRMADOS["residuales-p3-modulos-ic.md"],
        "hash_entrada": IDENTIDAD["sha256_entrada"], "hash_entorno": hash_entorno,
    }
    publ = {}
    se = None
    ic = None
    n_no_est = None
    punto = None

    if join_ambiguo:
        fila.update({"estado": "NO-ESTIMABLE",
                     "motivo": f"NO-ESTIMABLE-DISENO: union por ID_PER ambigua (duplicados SEC_6_7_8={dup678}, SEC_4_5={dup45}, ID blancos={blancos_id})"})
    elif Y == 0.0:
        fila.update({"estado": "DENOMINADOR-CERO",
                     "motivo": "NO-ESTIMABLE-UNIVERSO-VACIO: suma de FAC_SEL en la celda valida (DOMINIO=R, AP4_3_2=1, AP7_3_5 en {1,2}) es cero"})
    else:
        punto = X / Y
        rng = np.random.Generator(np.random.PCG64(SEMILLA))
        t = np.empty(B, dtype=np.float64)
        estimable = np.ones(B, dtype=bool)
        for rep in range(B):
            M = np.zeros(len(orden), dtype=np.int64)
            for h in orden_estratos:
                ind = np.array(estratos[h], dtype=np.int64)
                sel = rng.choice(ind, len(ind), replace=True)
                np.add.at(M, sel, 1)
            Xr = 0.0
            Yr = 0.0
            for m, a, b in zip(M, Xhu, Yhu):
                if m:
                    Xr += float(m) * a
                    Yr += float(m) * b
            if Yr == 0.0:
                estimable[rep] = False
                t[rep] = np.nan
            else:
                t[rep] = Xr / Yr
        n_no_est = int((~estimable).sum() + (~np.isfinite(t[estimable])).sum())
        tipo = "bootstrap-percentil-UPM-no-reescalado-diagnostico"
        if n_singleton > 0:
            tipo += ";" + MARCA_SINGLETON
        diag_ic["tipo_incertidumbre"] = tipo
        diag_ic["n_replicas_no_estimables"] = n_no_est
        fila.update({"estado": "RECONSTRUIDO", "punto": r(punto)})
        if n_no_est > 0:
            fila.update({"estado_ic": "NO-IDENTIFICADA",
                         "motivo_ic": f"{n_no_est} replicas bootstrap no estimables (Y_r=0 o no finitas); el contrato P3 anula intervalo y SE"})
        else:
            ts = np.sort(t)
            ic = (cuantil_tipo7(ts, Q_INF), cuantil_tipo7(ts, Q_SUP))
            media = float(np.mean(t))
            se = math.sqrt(float(np.sum((t - media) ** 2)) / (B - 1))
            diag_ic["se"] = r(se)
            fila.update({"estado_ic": "CALCULADO", "ic95_inf": r(ic[0]), "ic95_sup": r(ic[1])})

    # --- Publicabilidad diagnóstica (proporciones) ---
    if punto is not None:
        crit = {"n_conocidos>=100": n_validos >= 100, "n_upm_conocidos>=5": n_upm_conocidos >= 5,
                "sin_replicas_no_estimables": n_no_est == 0}
        if ic is not None:
            crit["ancho<=0.20"] = bool((ic[1] - ic[0]) <= 0.20)
            if punto > 0:
                crit["CV<=0.30"] = bool((se / punto) <= 0.30)
            else:
                crit["CV<=0.30"] = "punto=0: se reporta separado, sin division"
        publ = {"criterios": crit,
                "ancho": r(ic[1] - ic[0]) if ic else None,
                "cv": r(se / punto) if (ic and punto > 0) else None,
                "publicable_diagnostico": bool(all(v is True for v in crit.values()) and ic is not None),
                "nota": "regla diagnostica del contrato P3; no acredita validez inferencial; no suprime la celda"}

    doc = {"version": 3, "identidad": IDENTIDAD, "filas": [fila]}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")

    cols = ["llave", "tipo_incertidumbre", "se", "n_conocidos", "n_upm_marco", "n_upm_conocidos",
            "n_singleton", "n_replicas_no_estimables", "B", "semilla", "RNG", "regla_marco", "cuantil",
            "hash_contrato", "hash_entrada", "hash_entorno"]
    with open(os.path.join(SAL, "diagnosticos-ic-v1.tsv"), "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter="\t", lineterminator="\n")
        wr.writerow(cols)
        wr.writerow([diag_ic[c] for c in cols])

    diag = {
        "llaves": {fila_esq["llave"]: {
            "celda": fila_esq["celda"], "segmento": fila_esq["segmento"], "unidad_observacion": "PERSONA",
            "n_registros_SEC_6_7_8": n678, "n_registros_SEC_4_5": n45,
            "duplicados_ID_PER": {"SEC_6_7_8": dup678, "SEC_4_5": dup45, "blancos": blancos_id},
            "n_valido": n_validos,
            "peso_denominador": r(Y), "peso_numerador": r(X),
            "punto_suma_directa_orden_fisico": r(Xf / Yf) if Yf else None,
            "exclusiones_en_cascada_no_ponderadas": excl_n,
            "exclusiones_en_cascada_ponderadas_FAC_SEL": {k: r(v) for k, v in excl_w.items()},
            "nota_exclusiones": "cascada en el orden listado; registros sin peso valido no tienen suma ponderada (0.0 por construccion); las causas 'fuera_de_dominio_*' son filtros de la identidad, no faltantes",
            "sin_pareja_SEC_4_5_sin_base": sin_pareja_45,
            "DOMINIO_discrepante_entre_tablas_pareadas": dominio_discrepa,
            "conteos_marginales_no_ponderados": marginal,
            "n_filas_marco": len(marco_filas), "n_upm_marco": len(orden), "n_estratos": len(orden_estratos),
            "n_upm_conocidos": n_upm_conocidos, "n_singleton": n_singleton,
            "publicabilidad": publ,
        }},
        "decisiones": DECISIONES,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diag, f, ensure_ascii=False, indent=2)
        f.write("\n")


DECISIONES = [
    {"decision": "Estado de salida para denominador cero: DENOMINADOR-CERO de v3 con motivo NO-ESTIMABLE-UNIVERSO-VACIO.",
     "frase": "Denominador cero produce NO-ESTIMABLE-UNIVERSO-VACIO. (encuci-rural-restaurado.md) / DENOMINADOR-CERO | ... Spec suficiente; dominio observado con denominador cero. (CONTRATO-v3.md)"},
    {"decision": "Formato de salida v3 con version=3, no v2, pese a que el punto remite a esquema-salida-v2.md.",
     "frase": "Salida comparada: documento y filas exactamente según `esquema-salida-v2.md` (encuci-rural-restaurado.md); instrucción de sesión: donde difieran, rige CONTRATO-v3.md."},
    {"decision": "Se calcula IC (estado_ic explícito) en lugar de SIN-IC, porque el contrato P3 está firmado (R26) con sha coincidente.",
     "frase": "IC solo bajo contrato P3. (encuci-rural-restaurado.md); «Apruebo la receta IC sucesora ... solo como reproducibilidad diagnóstica» (FIRMAS-Y-ACCESO.md)"},
    {"decision": "DOMINIO, FAC_SEL, EST_DIS y UPM_DIS se toman de SEC_6_7_8 (tabla base); de SEC_4_5 solo AP4_3_2 (DOMINIO de SEC_4_5 solo para contar discrepancias).",
     "frase": "Usar `FAC_SEL` de SEC_6_7_8 (encuci-rural-restaurado.md); EST_DIS/UPM_DIS de tabla base; B: SEC_6_7_8 base unida a SEC_4_5 (residuales-p3-modulos-ic.md)"},
    {"decision": "El marco de UPM se forma con todas las filas de SEC_6_7_8 con peso válido y diseño no vacío, incluidas las sin pareja en SEC_4_5 (contribuyen cero).",
     "frase": "marco completo personas15+ con diseño antes de contacto, agravio o rural (residuales-p3-modulos-ic.md); Marco: todos los pares distintos (estrato,UPM) del universo base con ponderador finito positivo y diseño válido, antes de filtrar dominio o respuesta (residuales-p3-contrato-ic.md)"},
    {"decision": "Diseño válido = EST_DIS y UPM_DIS no vacíos. Del valor crudo DBF solo se quita el relleno de ancho fijo a la derecha (campos C de 7 bytes para EST_DIS de 3); no se hace otro trim ni conversión a entero.",
     "frase": "conservar bytes y ceros iniciales, no convertir a enteros ni rellenar ... sin trim implícito (residuales-p3-contrato-ic.md)"},
    {"decision": "Exclusiones contadas en cascada: borrado DBF, peso, diseño, pareja, DOMINIO fuera de {U,C,R}, DOMINIO U/C, AP4_3_2 inválido, AP4_3_2=2, AP7_3_5 inválido. Se añaden conteos marginales.",
     "frase": "sin pareja quedan fuera y se cuentan ... blancos/9 quedan fuera y se cuentan (encuci-rural-restaurado.md)"},
    {"decision": "Códigos: se parsea el texto recortado como float; 1.0->1, 2.0->2; blanco, 9 y cualquier otro valor son inválidos.",
     "frase": "Normalizar los códigos numéricos de reactivos, aceptando 1 y 1.000000000000000 como 1. Exigir AP7_3_5 y AP4_3_2 en {1,2} (encuci-rural-restaurado.md)"},
    {"decision": "El punto se computa como (acumulación de X_hu en orden lexicográfico de pares)/(ídem Y_hu), con X_hu,Y_hu acumulados en orden físico de SEC_6_7_8; la suma directa por filas se reporta solo como diagnóstico.",
     "frase": "sumas float64, totales por par en ese orden y acumulación de pares ordenados (residuales-p3-contrato-ic.md)"},
    {"decision": "Réplica: X_r y Y_r como acumulación secuencial de float(M_rhu)*X_hu en orden lexicográfico de pares; M_rhu por conteo de índices sorteados.",
     "frase": "Multiplicidad M_rhu determina X_r=sum(M_rhu X_hu),Y_r=sum(M_rhu Y_hu) (residuales-p3-contrato-ic.md)"},
    {"decision": "Los estratos con una sola UPM (si existen) no bloquean el IC: estado_ic=CALCULADO y la marca IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA va en tipo_incertidumbre del TSV. Decidido antes de ver cifras.",
     "frase": "Singleton: se sortea a sí mismo, no se colapsa ni descarta ... Registrar cantidad y marcar IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA (residuales-p3-contrato-ic.md) vs. Un bloqueo de inferencia se representa con NO-IDENTIFICADA (CONTRATO-v3.md)"},
    {"decision": "Registros marcados como borrados en el DBF quedan fuera y se cuentan.",
     "frase": "Filas sin diseño salen contadas (residuales-p3-contrato-ic.md); el FD no documenta registros borrados."},
    {"decision": "Unión por ID_PER (no por UPM+VIV_SEL+R_SEL, llave primaria del FD). ID_PER = UPM+VIV_SEL+R_SEL según el FD; se leyó solo ID_PER.",
     "frase": "Unir `SEC_6_7_8` con `SEC_4_5` por `ID_PER`, con llaves únicas (encuci-rural-restaurado.md)"},
    {"decision": "hash_contrato = sha256 de residuales-p3-contrato-ic.md y residuales-p3-modulos-ic.md unidos por '+'; hash_entrada = sha256_entrada de la identidad; hash_entorno = sha256 de salida/entorno.txt.",
     "frase": "columnas ... hash_contrato, hash_entrada, hash_entorno (residuales-p3-contrato-ic.md) — sin definición de contenido."},
]

if __name__ == "__main__":
    main()
