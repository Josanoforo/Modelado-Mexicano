#!/usr/bin/env python3
"""Escenarios prospectivos; no estiman variación temporal ni evalúan R futura.

Los índices compartidos son de una misma ola histórica, nunca pares entre olas.
El IC primario mantiene p0 fijo y solo usa error muestral histórico centrado.
tau añade un shock común hipotético al cambio, sin ensanchar ese IC primario.
Los singleton invalidan inferencia: los números quedan como diagnóstico.
"""
import argparse
import json
from pathlib import Path

import numpy as np

FAMILIAS = ("DENUNCIA_U4", "EVASION_NORMA")
SEMILLA = 20260926
N_DRAWS = 10000
BANDA = 0.02
DELTAS = (0.0, -0.01, 0.01, -0.02, 0.02, -0.04, 0.04, -0.06, 0.06)
TAUS = (0.0, 0.01, 0.02)
ESTADOS = ("COMPATIBLE", "INDETERMINADO", "DESVIO")


def clasificar(cambio, limites):
    """IC cerrado: contacto con la frontera no basta para declarar desvío."""
    inferior = cambio + limites[0]
    superior = cambio + limites[1]
    compatible = (inferior >= -BANDA) & (superior <= BANDA)
    material = (inferior > BANDA) | (superior < -BANDA)
    return np.where(compatible, 0, np.where(material, 2, 1))


def probabilidades(estados, autorizado):
    probs = {nombre: float(np.mean(estados == i))
             for i, nombre in enumerate(ESTADOS)}
    informativa = probs["COMPATIBLE"] + probs["DESVIO"]
    return {
        "estado_inferencia": ("ESCENARIO-CONDICIONAL" if autorizado else
                               "DIAGNOSTICO-NO-VALIDO-PARA-INFERENCIA"),
        "probabilidades": probs,
        "probabilidad_conclusion_informativa_diagnostica": informativa,
        "probabilidad_conclusion_informativa_autorizada": (
            informativa if autorizado else 0.0),
    }


def correlacion(x):
    if np.any(np.std(x, axis=0) == 0):
        return None
    return float(np.corrcoef(x.T)[0, 1])


def ejecutar(replicas, diagnostico):
    familias = diagnostico["familias"]
    puntos = np.array([float(familias[k]["punto"]) for k in FAMILIAS])
    if not np.all(np.isfinite(puntos)) or np.any((puntos < 0) | (puntos > 1)):
        raise ValueError("puntos fuera de [0,1] o no finitos")
    arrays = [np.asarray(replicas[k], dtype=float) for k in FAMILIAS]
    if any(a.shape != (2000,) for a in arrays):
        raise ValueError("se exigen exactamente 2000 réplicas por familia")
    x = np.column_stack(arrays)
    if not np.all(np.isfinite(x)) or np.any((x < 0) | (x > 1)):
        raise ValueError("réplicas fuera de [0,1] o no finitas")
    singleton = [bool(familias[k].get("singleton_marco", diagnostico.get(
        "diseno", {}).get("singleton_marco", False))) for k in FAMILIAS]
    if any("soporte" not in familias[k] for k in FAMILIAS):
        raise ValueError("falta diagnóstico de soporte por familia")
    autorizado = [not s for s in singleton]
    # Centrar por la media bootstrap no modifica ni reestima el p0 primario.
    centradas = x - np.mean(x, axis=0)
    limites = np.quantile(centradas, [0.025, 0.975], axis=0)
    rng = np.random.default_rng(SEMILLA)
    indices = rng.integers(0, len(x), N_DRAWS)
    error = centradas[indices]
    shock = rng.normal(size=N_DRAWS)
    salida = {
        "metodo": "bootstrap centrado conjunto de una ola, IC percentil de errores centrados 95%, p0 fijo",
        "semilla": SEMILLA, "draws": N_DRAWS, "replicas": len(x),
        "banda_absoluta": BANDA, "deltas": DELTAS, "taus": TAUS,
        "supuestos": {
            "temporal": "ESCENARIO-NO-ESTIMACION: shock común normal(0,tau²)",
            "muestreo": "error de la ola histórica como escenario de precisión futura",
            "dependencia": "índice conjunto en una misma ola; ningún pairing entre olas",
            "ic": "tau no entra al IC primario; p0 sin incertidumbre histórica propagada",
            "cambios": "delta igual en ambas familias; sin truncar errores en [0,1]",
            "mde": "rejilla 0.001, primer delta con P(DESVIO)>=0.80; no monotonicidad impuesta",
        },
        "correlacion_replicas": correlacion(x),
        "familias": {}, "escenarios": [], "mde": [],
    }
    for j, k in enumerate(FAMILIAS):
        salida["familias"][k] = {
            "p0": float(puntos[j]), "singleton_marco": singleton[j],
            "soporte": familias[k]["soporte"],
            "error_muestral_sd": float(np.std(centradas[:, j], ddof=1)),
            "error_cuantiles_95": limites[:, j].tolist(),
            "estado_inferencia": ("ESCENARIO-CONDICIONAL" if autorizado[j] else
                                   "DIAGNOSTICO-NO-VALIDO-PARA-INFERENCIA"),
        }
    for tau in TAUS:
        ruido = error + tau * shock[:, None]
        for delta in DELTAS:
            estados = clasificar(delta + ruido, limites)
            fila = {"delta": delta, "tau": tau,
                    "poblacion_hipotetica_en_0_1": bool(np.all(
                        (puntos + delta >= 0) & (puntos + delta <= 1))),
                    "correlacion_error_con_shock": correlacion(ruido),
                    "familias": {k: probabilidades(estados[:, j], autorizado[j])
                                 for j, k in enumerate(FAMILIAS)}}
            conjunta = {
                f"{a}|{b}": float(np.mean((estados[:, 0] == i) &
                                         (estados[:, 1] == j)))
                for i, a in enumerate(ESTADOS) for j, b in enumerate(ESTADOS)}
            ambas = float(np.mean(np.all(estados != 1, axis=1)))
            fila["conjunta"] = {
                "estado_inferencia": ("ESCENARIO-CONDICIONAL" if all(autorizado)
                    else "DIAGNOSTICO-NO-VALIDO-PARA-INFERENCIA"),
                "probabilidades": conjunta,
                "probabilidad_ambas_informativas_diagnostica": ambas,
                "probabilidad_ambas_informativas_autorizada": ambas if all(autorizado) else 0.0,
            }
            # En delta=0, declarar DESVIO es el error relevante bajo este escenario.
            if delta == 0:
                fila["error_relevante_delta_cero"] = {
                    k: float(np.mean(estados[:, j] == 2))
                    for j, k in enumerate(FAMILIAS)}
            salida["escenarios"].append(fila)
        for j, k in enumerate(FAMILIAS):
            for signo in (-1, 1):
                maximo = puntos[j] if signo < 0 else 1 - puntos[j]
                encontrado = None
                prob = None
                for paso in range(1, int(np.floor(maximo / 0.001)) + 1):
                    delta = signo * paso * 0.001
                    estados = clasificar(delta + ruido[:, j], limites[:, j])
                    p = float(np.mean(estados == 2))
                    if p >= 0.8:
                        encontrado, prob = delta, p
                        break
                salida["mde"].append({
                    "familia": k, "tau": tau, "direccion": signo,
                    "maximo_delta_factible": float(maximo),
                    "delta_diagnostico": encontrado,
                    "probabilidad_desvio_diagnostica": prob,
                    "delta_inferencial_autorizado": encontrado if autorizado[j] else None,
                    "estado": ("DIAGNOSTICO-NO-VALIDO-PARA-INFERENCIA" if not autorizado[j]
                               else "ALCANZA-80" if encontrado is not None else "NO-ALCANZA-80"),
                })
    return salida


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicas", type=Path, required=True)
    parser.add_argument("--diagnostico", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    diagnostico = json.loads(args.diagnostico.read_text(encoding="utf-8"))
    with np.load(args.replicas, allow_pickle=False) as replicas:
        resultado = ejecutar(replicas, diagnostico)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2,
                                    allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
