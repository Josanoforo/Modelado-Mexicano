#!/usr/bin/env python3
"""Genera los spec.yaml de los cuatro CALC de GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.

Se corre UNA vez, en el COMMIT-1, antes de abrir microdato: toma el sha256 de cada payload del
manifiesto (por id), el de la receta, el motor y la spec humana del árbol, y la lista
`resultados:` de `esquema_resultados()` del medidor. No lee ningún dato.

    python3 tools/dominios/confianza/genera_spec_yaml.py
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
RECETA = "tools/dominios/salud/pisos_diseno.py"
MOTOR = "tools/dominios/confianza/motor_pisos.py"
ACTO = "GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1"
ENCARGO = "forense/encargos/2026-09-25-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.md"

CALCS = {
    "CALC-WVS-PISOS-2018-0001": dict(
        spec="CONFIANZA-WVS-PISOS-spec-v1_0.md", seed=20260925, ola="2018",
        universo="Persona 18+ (Q262>=18), WVS 2018 Mexico; W_WEIGHT>0 e I_PSU no vacia.",
        ponderador="W_WEIGHT", disenio="UPM I_PSU; sin estrato en el archivo publico (estrato unico)",
        estimando="Pisos por segmento WVS 2018 de 32 conductas/escalas con IC de conglomerados; ola unica",
        nota_ola="WVS 2018 (unica ola en corpus; se abre, E.6)"),
    "CALC-LATINOBAROMETRO-PISOS-2023-0001": dict(
        spec="CONFIANZA-LATINOBAROMETRO-PISOS-spec-v1_0.md", seed=20260926, ola="2023",
        universo="Persona 18+ (edad>=18) de Mexico (idenpa=484), Latinobarometro 2023; wt>0.",
        ponderador="wt", disenio="sin estrato ni UPM en el archivo: bootstrap ponderado de entrevistas (MAS-PONDERADO)",
        estimando="Pisos por segmento Latinobarometro 2023 Mexico de 21 conductas; 2024 RESERVADA",
        nota_ola="2023 abierta; 2024 RESERVADA (E.6), no es input"),
    "CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001": dict(
        spec="CONFIANZA-PEW-PISOS-spec-v1_0.md", seed=20260927, ola="2013,2015,2017,2018,2023,2024",
        universo="Persona 18+ de Mexico (pais por ola), PEW Global Attitudes 2013-2024; peso>0.",
        ponderador="WEIGHT/weight por ola", disenio="por ola: STRATUM_MEX/PSU(_MEX) donde existen; si la UPM falta en alguna fila, sin conglomerados",
        estimando="Pisos por segmento PEW Mexico de 7 conductas en 6 olas; IC calibrado de persistencia en 4 series; 2025 RESERVADA",
        nota_ola="2013-2024 abiertas; 2025 RESERVADA (E.6), no es input"),
    "CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001": dict(
        spec="CONFIANZA-LAPOP-PISOS-spec-v1_0.md", seed=20260928, ola="2004,2006,2019",
        universo="Persona 18+ (q2>=18), LAPOP Mexico 2004/2006/2019; peso>0, estrato y UPM no vacios.",
        ponderador="1 (2004, 2006) / wt (2019)", disenio="el de LAPOP-PISOS-OLAS-spec-v1_0.md por ola",
        estimando="Pisos por segmento LAPOP de 20 conductas en 3 olas; sin serie (FIRMAS-15 T); 2023 RESERVADA, 2021 fuera",
        nota_ola="2004/2006/2019 abiertas; 2023 RESERVADA para estos reactivos (E.6); 2021 fuera"),
}


# Miembro de datos de cada ZIP (lista de miembros = envoltura, A.7): `archivo` cita el miembro
# exacto para que `corrida0 spec-check` verifique las columnas.
MIEMBROS = {
    "f00013084_wvs_wave_7_mexico_stata_v5_1": "WVS_Wave_7_Mexico_Stata_v5.1.dta",
    "latinobarometro2023_bd_stata_zip": "Latinobarometro_2023_Esp_Stata_v1_0.dta",
    "pew_gas_spring2013": "Pew Research Global Attitudes Project Spring 2013 Dataset for web.sav",
    "pew_gas_spring2015": "Pew Research Global Attitudes Spring 2015 Dataset for Web FINAL.sav",
    "pew_gas_spring2017": "Pew Research Global Attitudes Spring 2017 Dataset WEB FINAL.sav",
    "pew_gas_spring2018": "Pew Research Global Attitudes Spring 2018 Dataset WEB FINAL.sav",
    "pew_gas_spring2023": "Pew Research Center Global Attitudes Spring 2023 Dataset CORRECTED.sav",
    "pew_gas_spring2024": "Pew Research Center Global Attitudes Spring 2024 Dataset.sav",
}


def archivo(pid, man):
    return MIEMBROS.get(pid) or Path(man[pid].get("archivo", pid)).name


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def manifiesto():
    with open(ROOT / "data/manifiesto.yaml") as f:
        m = yaml.safe_load(f)
    ents = m if isinstance(m, list) else next(v for v in m.values() if isinstance(v, list))
    return {e["id"]: e for e in ents if isinstance(e, dict) and "id" in e}


def carga(calc):
    s = importlib.util.spec_from_file_location(f"m_{calc}", ROOT / "data/corrida0" / calc / "medidor.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def payloads(m):
    return [m.PAY] if hasattr(m, "PAY") else list(m.PAYS.values())


def variables(m, man):
    out = []
    if hasattr(m, "CONDUCTAS"):
        arch = archivo(m.PAY, man)
        for c in m.columnas():
            out.append({"archivo": arch, "variable": c, "rol": "reactivo o diseno"})
        return out
    for ola, t in m.OLAS.items():
        arch = archivo(m.PAYS[ola], man)
        if len(t) == 8:  # PEW
            pais, peso, est, upm, sexo, edad, educ, cond = t
            cols = [pais[0]] + [c for c in (peso, est, upm, sexo, edad, educ) if c] + [r[1] for r in cond.values()]
        else:  # LAPOP
            peso, est, upm, cond = t
            ups = (upm,) if isinstance(upm, str) else tuple(upm)
            cols = [c for c in (peso, est) if c] + list(ups) + ["q1", "q2", "ed", "ur"] + [r[1] for r in cond.values()]
        # LAPOP 2006 guarda los nombres en MAYÚSCULAS: se citan como están en el archivo (el
        # lector del motor no distingue mayúsculas).
        caso = str.upper if (len(t) == 4 and ola == "2006") else (lambda x: x)
        for c in dict.fromkeys(cols):
            out.append({"archivo": arch, "variable": caso(c), "rol": f"reactivo o diseno ({ola})"})
    return out


def main():
    man = manifiesto()
    for calc, d in CALCS.items():
        m = carga(calc)
        spec_md = f"forense/prereg-caja/{d['spec']}"
        inputs = [{"id": p, "origen": "manifiesto", "sha256": man[p]["sha256"], "funcion": "DATO",
                   "nota": Path(man[p].get("archivo", p)).name} for p in payloads(m)]
        inputs += [
            {"id": "receta_pisos_salud", "origen": "repo", "ruta": RECETA, "sha256": sha(RECETA),
             "funcion": "CODIGO", "nota": "marginales, bootstrap, resumen, persistencia, ic_calibrado (GEN2-SALUD-Y-BIENESTAR-PISOS-1) ejecutados desde estos bytes"},
            {"id": "motor_pisos_confianza", "origen": "repo", "ruta": MOTOR, "sha256": sha(MOTOR),
             "funcion": "CODIGO", "nota": "lectura con filtro de pais, recodificacion, ejes, diseno, ids (este acto) ejecutados desde estos bytes"},
        ]
        spec = {
            "calc_id": calc,
            "spec_md": f"../../../{spec_md}",
            "spec_md_sha256": sha(spec_md),
            "script": f"data/corrida0/{calc}/medidor.py",
            "dependencias_materiales": ["numpy", "pandas", "pyreadstat"],
            "etiquetas": {
                "generacion": "GEN2", "uso_motor": "NO-ADOPTA-NADA", "cuenta_gen2": "SI", "adopta": "NO",
                "cuenta_gen2_nota": f"CONTADOR del encargo {ACTO} (cuenta_gen2: SI, adopta: NO)",
                "fuente_acto": ACTO, "encargo": ENCARGO, "tipo": "PISO-POR-SEGMENTO-DESDE-MICRODATO",
                "agrupacion": "UNA-SOLA-VARIABLE",
                "marca": "DESCRIPTIVO -- pisos por segmento; RETROSPECTIVO; nada se evalua contra R en este CALC",
                "firmas": "F-ASTRA-5-4, regla 6, E.6, FIRMAS-15 T, A3 (encargo §2, verbatim)",
                "unidad_transferencia": "PERSONA", "olas": d["nota_ola"],
            },
            "inputs": inputs,
            "variables": variables(m, man),
            "universo": d["universo"],
            "filtros": "Un eje a la vez; nunca cruces. Recodificacion por texto: lista-cerrada-P1.md §2-§3.",
            "ponderador": d["ponderador"],
            "transformacion": "bin(col, UNO, CERO) / media(col, lo, hi); todo otro codigo fuera (lista-cerrada-P1.md §2).",
            "estimando": d["estimando"],
            "seed": {"aplica": True, "valor": d["seed"], "rng": "numpy.PCG64"},
            "parametros": {
                "bootstrap_replicas": 2000,
                "metodo_ic": "bootstrap UPM con reposicion dentro de estrato; singleton de certeza; percentiles 2.5/97.5; bloques de 50; contrato conservador",
                "diseno": d["disenio"],
                "ola": d["ola"],
            },
            "tolerancia": {"tipo": "flotante", "abs": 1.0e-10,
                           "razon": "bootstrap determinista por semilla; mismo payload y sumas float64"},
            "resultados": m.esquema_resultados(),
        }
        cab = (f"# {calc} -- contrato ejecutable de la spec humana (D-15). COMMIT-1, antes de abrir microdato.\n"
               "# El primer resultado que produzca este procedimiento es el que se reporta.\n")
        (ROOT / "data/corrida0" / calc / "spec.yaml").write_text(
            cab + yaml.safe_dump(spec, allow_unicode=True, sort_keys=False, width=100))
        print(calc, len(spec["resultados"]), "RESULT")


if __name__ == "__main__":
    main()
