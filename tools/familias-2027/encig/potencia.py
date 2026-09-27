#!/usr/bin/env python3
"""Escenarios prospectivos ENCIG; consume auxiliares agregados, nunca microdato."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

FAMILIAS = ("PAGO-DIGITAL", "SOLICITUD-MORDIDA")
BANDA = .02
SEMILLA = 26092603
SIMULACIONES = 10000


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalized(document):
    return {key.removeprefix("ENCIG-"): value
            for key, value in document["familias"].items()}


def classify(center, error, quantiles, p0):
    # Intervalo percentil futuro: cuantiles de R + residual bootstrap, p0 fijo.
    estimate = np.clip(center + error, 0, 1)
    low = np.clip(estimate + quantiles[0], 0, 1)
    high = np.clip(estimate + quantiles[1], 0, 1)
    # Comparar extremos en escala original evita cancelación de p0 en fronteras.
    compatible = (low >= p0 - BANDA) & (high <= p0 + BANDA)
    deviation = (low > p0 + BANDA) | (high < p0 - BANDA)
    return np.where(compatible, 0, np.where(deviation, 2, 1))


def probabilities(states):
    result = {name: float(np.mean(states == index)) for index, name in
              enumerate(("COMPATIBLE", "INDETERMINADO", "DESVIO"))}
    result["informativa"] = 1 - result["INDETERMINADO"]
    return result


def calculate(replicas, pisos):
    if replicas.get("joint_design") is not True:
        raise ValueError("Se exige joint_design=true: réplicas conjuntas de una misma ola")
    families, floors = normalized(replicas), normalized(pisos)
    arrays, p0 = [], []
    for family in FAMILIAS:
        source = families[family]
        arr = np.asarray(source["replicas"], dtype=float)
        baseline = float(source["p"])
        floor = floors[family]
        fixed = float(floor["p0"])
        if not floor.get("result_id") or len(floor.get("source_sha256", "")) != 64:
            raise ValueError("Piso sin RESULT y hash de fuente")
        if arr.ndim != 1 or len(arr) < 100 or not np.isfinite(arr).all():
            raise ValueError("Réplicas inválidas o insuficientes")
        if np.any((arr < 0) | (arr > 1)) or not 0 <= baseline <= 1 or not 0 <= fixed <= 1:
            raise ValueError("Proporciones fuera de [0,1]")
        arrays.append(arr - baseline)
        p0.append(fixed)
    if len(arrays[0]) != len(arrays[1]):
        raise ValueError("Réplicas conjuntas deben conservar índices alineados")
    residuals = np.column_stack(arrays)
    if np.any(np.std(residuals, axis=0, ddof=1) == 0):
        raise ValueError("Varianza empírica cero: potencia no identificable por este auxiliar")
    p0 = np.asarray(p0)
    rng = np.random.default_rng(SEMILLA)
    sampled = residuals[rng.integers(0, len(residuals), SIMULACIONES)]
    temporal = rng.normal(size=(SIMULACIONES, 1))
    shifts = [0] + [sign * magnitude for magnitude in (.01, .02, .03, .05)
                    for sign in (-1, 1)]
    scenarios, mdes = [], []
    for scale in (.5, 1., 2.):
        quantiles = np.quantile(residuals * scale, (.025, .975), axis=0)
        for temporal_sd in (0., .01, .02):
            error = sampled * scale + temporal * temporal_sd
            for shift in shifts:
                states = classify(p0 + shift, error, quantiles, p0)
                scenarios.append({"shift": shift, "escala_ee": scale,
                    "sd_temporal_comun": temporal_sd,
                    "familias": {family: probabilities(states[:, i])
                                 for i, family in enumerate(FAMILIAS)},
                    "conjunta": {"ambas_compatibles": float(np.mean(np.all(states == 0, axis=1))),
                        "al_menos_un_desvio": float(np.mean(np.any(states == 2, axis=1))),
                        "ambas_informativas": float(np.mean(np.all(states != 1, axis=1)))}})
            for i, family in enumerate(FAMILIAS):
                for direction in (-1, 1):
                    crossing = None
                    for magnitude in np.arange(1, 401) * .0005:
                        if not 0 <= p0[i] + direction * magnitude <= 1:
                            break
                        states = classify(p0[i] + direction * magnitude, error[:, i],
                                          quantiles[:, i], p0[i])
                        prob = probabilities(states)
                        if prob["DESVIO"] >= .8:
                            crossing = {"cambio": float(direction * magnitude), **prob}
                            break
                    mdes.append({"familia": family, "escala_ee": scale,
                        "sd_temporal_comun": temporal_sd, "direccion": direction,
                        "mde": crossing, "max_rejilla": .2, "paso": .0005})
    return {"estado": "ESCENARIOS-NO-EVALUACION-FUTURA", "semilla": SEMILLA,
        "simulaciones": SIMULACIONES, "replicas": len(residuals), "banda": BANDA,
        "correlacion_residual": float(np.corrcoef(residuals.T)[0, 1]),
        "pisos": floors, "escenarios": scenarios, "mde": mdes}


def markdown(result):
    lines = ["# Potencia ENCIG · escenarios", "",
        "EJECUTADO sobre réplicas históricas agregadas. No evalúa ola futura ni valida cobertura.", "",
        "El primario mantiene p0 fijo y banda ±2 pp. El ruido temporal es escenario común, no parámetro estimado.", "",
        "| Familia | Cambio pp | Compatible | Indeterminado | Desvío | Informativa |",
        "|---|---:|---:|---:|---:|---:|"]
    for scenario in result["escenarios"]:
        if scenario["escala_ee"] != 1 or scenario["sd_temporal_comun"] != 0:
            continue
        for family, probability in scenario["familias"].items():
            values = " | ".join(f"{100 * probability[name]:.2f}%" for name in
                                ("COMPATIBLE", "INDETERMINADO", "DESVIO", "informativa"))
            lines.append(f"| {family} | {100 * scenario['shift']:+.0f} | {values} |")
    lines += ["", "DESVÍO con cambio cero es el error relevante bajo igualdad al piso; no equivale a error de cobertura.",
              "", "| Familia | Escala EE | SD temporal | Dirección | MDE pp | P informativa al MDE |",
              "|---|---:|---:|---:|---:|---:|"]
    for item in result["mde"]:
        mde = item["mde"]
        value = f"{100*mde['cambio']:+.2f}" if mde else "No alcanza 80% hasta límite"
        info = f"{100*mde['informativa']:.2f}%" if mde else "—"
        lines.append(f"| {item['familia']} | {item['escala_ee']} | {item['sd_temporal_comun']} | {item['direccion']:+d} | {value} | {info} |")
    lines += ["", "Sensibilidad completa y probabilidades conjuntas: potencia.json (81 escenarios).",
              "MDE es descriptivo, sin selección de familias ni modificación de umbrales.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicas", required=True)
    parser.add_argument("--pisos", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = calculate(json.loads(Path(args.replicas).read_text()),
                       json.loads(Path(args.pisos).read_text()))
    result["fuentes"] = {"replicas_sha256": sha(args.replicas), "pisos_sha256": sha(args.pisos),
                         "codigo_sha256": sha(__file__)}
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "potencia.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    (output / "potencia.md").write_text(markdown(result))
    print(json.dumps({"estado": result["estado"], "escenarios": len(result["escenarios"]),
                      "mde": len(result["mde"]), "replicas": result["replicas"]}))


if __name__ == "__main__":
    main()
