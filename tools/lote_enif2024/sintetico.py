#!/usr/bin/env python3
"""Fabrica olas SINTÉTICAS de ENIF (2021 y 2024) con la forma de los payloads
reales, para el ensayo de sellabilidad (D-22 ampliada) y los tests del lote.

ACTO `GEN2-DIN-LOTE-ENIF2024-COMMIT-1`. Nada de aquí es dato: son filas
sorteadas con `numpy.random.PCG64(seed)` sobre la rejilla del árbitro, con
los nemónicos de cada ola (2021: `P3_1_1`, `P3_10`, `P5_7_k`, `FAC_ELE`,
`EDAD`; 2024: `NIV`, `P3_13`, `P5_6_k`, `FAC_PER`, `EDAD_V`) y los miembros de
zip que el medidor busca por sufijo. Sirve para ejercitar CADA rama terminal:
`vaciar` quita categorías enteras de una ola (celda rara: n = 0 en una ola),
`n_por_estrato` chico deja estratos con una sola UPM, `masa_cero` deja una
categoría de un eje sin filas (marginal con masa cero).
"""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np

MIEMBRO = {
    "2021": "conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/conjunto_de_datos_tmodulo_enif_2021.csv",
    "2024": "conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/conjunto_de_datos_tmodulo_enif2024.csv",
}
CATALOGO_2021 = ("conjunto_de_datos_tmodulo_enif_2021/catalogos/p3_1_1.csv",
                 "cve,descrip\n0,Ninguno\n1,Preescolar o kínder\n2,Primaria\n3,Secundaria\n"
                 "4,Estudios técnicos con secundaria terminada\n5,Normal básica\n"
                 "6,Preparatoria o bachillerato\n7,Estudios técnicos con preparatoria terminada\n"
                 "8,Licenciatura o ingeniería (profesional)\n9,Maestría o doctorado\n99,No sabe\n")

ESC_2021 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
ESC_2024 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]


def _fila(rng, ola: str, prob: dict, vaciar: set) -> dict | None:
    sexo = str(rng.integers(1, 3))
    edad = int(rng.integers(18, 90))
    if rng.random() < prob.get("edad_98", 0.01):
        edad = 98
    tloc = str(rng.integers(1, 5))
    esc = rng.choice(ESC_2021 if ola == "2021" else ESC_2024)
    if rng.random() < prob.get("esc_99", 0.005):
        esc = "99"
    trabaja = rng.random() < 0.69
    if ola == "2021":
        form = str(rng.integers(1, 7)) if trabaja else ""
    else:
        form = str(rng.integers(1, 8)) if trabaja else ""
    if rng.random() < 0.004 and trabaja:
        form = "9"
    tiene = (rng.random(9) < 0.25).astype(int)
    cuentas = ["1" if t else "2" for t in tiene]
    # la propensión al ahorro informal depende de los ejes: hay interacción
    z = -0.4 + 0.5 * (tloc in ("3", "4")) - 0.02 * (edad - 40) / 10 \
        + 0.3 * (sexo == "2") - 0.4 * (int(esc) >= 8 if esc != "99" else 0) \
        + prob.get("interaccion", 0.6) * ((tloc in ("3", "4")) and edad < 30)
    p_inf = 1.0 / (1.0 + np.exp(-z))
    inf = ["1" if rng.random() < p_inf / 2.5 else "2" for _ in range(6)]
    formal = []
    for k in range(9):
        if cuentas[k] == "1":
            formal.append("1" if rng.random() < 0.35 else "2")
        else:
            formal.append("")                       # blanco por secuencia
    celda = {"sexo": sexo, "tloc": tloc, "esc": esc}
    for eje, cats in vaciar.items():
        if celda.get(eje) in cats:
            return None
    fila = {"SEXO": sexo, "TLOC": tloc}
    if ola == "2021":
        fila.update({"EDAD": str(edad), "P3_1_1": esc, "P3_10": form})
        fila.update({f"P5_7_{k + 1}": formal[k] for k in range(9)})
    else:
        fila.update({"EDAD_V": str(edad), "NIV": esc, "P3_13": form})
        fila.update({f"P5_6_{k + 1}": formal[k] for k in range(9)})
    fila.update({f"P5_4_{k + 1}": cuentas[k] for k in range(9)})
    fila.update({f"P5_1_{k + 1}": inf[k] for k in range(6)})
    return fila


def fabrica_zip(destino: Path, ola: str, n: int = 900, seed: int = 0,
                n_estratos: int = 12, upm_por_estrato: int = 6,
                vaciar: dict | None = None, prob: dict | None = None,
                minusculas: bool | None = None) -> Path:
    """Escribe el zip sintético de la ola. `vaciar` = {"tloc": {"3"}, ...}
    quita filas de esas categorías (celdas raras). Devuelve la ruta."""
    ola = str(ola)
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    vaciar = {k: set(v) for k, v in (vaciar or {}).items()}
    prob = dict(prob or {})
    filas = []
    intentos = 0
    while len(filas) < n and intentos < 20 * n:
        intentos += 1
        f = _fila(rng, ola, prob, vaciar)
        if f is None:
            continue
        e = int(rng.integers(1, n_estratos + 1))
        u = (e - 1) * upm_por_estrato + int(rng.integers(1, upm_por_estrato + 1))
        f["EST_DIS"] = f"{e:03d}"
        f["UPM_DIS"] = f"{u:05d}" if ola == "2024" else f"{u:07d}"
        w = float(rng.integers(500, 20000))
        if ola == "2021":
            f["FAC_ELE"] = f"{w:.0f}"
        else:
            f["FAC_PER"] = f"{w:.0f}"
        filas.append(f)
    cols = list(filas[0].keys())
    if minusculas is None:
        minusculas = ola == "2024"
    cab = [c.lower() if minusculas else c for c in cols]
    buf = io.StringIO()
    buf.write(",".join(cab) + "\n")
    for f in filas:
        buf.write(",".join(f[c] for c in cols) + "\n")
    destino = Path(destino)
    with zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MIEMBRO[ola], buf.getvalue().encode("utf-8"))
        if ola == "2021":
            zf.writestr(CATALOGO_2021[0], CATALOGO_2021[1].encode("latin-1"))
    return destino
