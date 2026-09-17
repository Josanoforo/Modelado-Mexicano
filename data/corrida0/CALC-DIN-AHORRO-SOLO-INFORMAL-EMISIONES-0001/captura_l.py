#!/usr/bin/env python3
"""`C3` del piloto celda-D: captura de `L` sobre las 8 celdas de cruce.

ACTO `GEN2-CELDA-D-PILOTO-1`, `COMMIT-2`. Este script **captura**; no mide, no
puntúa y no adjudica. El medidor (`medidor.py`) sólo LEE las capturas que este
script escribe, para que `verify` pueda reejecutar la medición sin volver a
llamar a ningún modelo — una corrida sellada no puede depender de una llamada
de red que no se repite igual.

**Nada de `forense/prereg-duelo-v2/` se edita.** `runner_l_cli.py`,
`pipeline-L-adv1-m2.py` y `carga_l_v1_1.py` se IMPORTAN por ruta y se reusan
verbatim: de ahí salen el comando exacto del CLI, el prompt de sistema mínimo,
el alias de modelo, el constructor de prompt, los reintentos acotados y la
permutación determinista del orden de captura. Lo único propio de este archivo
son las 8 `SpecCelda` del piloto y la ruta de salida.

Perímetro: escribe SÓLO en `forense/prereg-duelo-v2/corridas-L/`, con un prefijo
(`CD-DIN-…`) elegido para **no** colisionar con ningún glob ya existente —
`corridas-L/L-*.json` (`tools/tablero_programa.py`), `L-<id>-M__*.json`
(`tools/corrida0.py`), `*-M-*.json` (`tools/extrae_l_v1_1.py`), `*__v1_3.json`
(`tools/extrae_l_v1_3.py`) y `<id_celda>__L-*__*.json`
(`tools/score_marco_m.py`) siguen contando exactamente lo que contaban.

Uso:
    python3 …/captura_l.py --dry-run    # construye los 64 prompts, no llama
    python3 …/captura_l.py --correr     # MODO REAL; reanudable (salta lo escrito)
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREREG = ROOT / "forense" / "prereg-duelo-v2"
CORRIDAS_L = PREREG / "corridas-L"
# Sufijo de spec que gobierna las capturas NUEVAS. `v1_0` (siete tipos de
# cuenta) quedó SUPERADO-POR-SPEC por la ENMIENDA a FP-379 (mesa, 16/sep/2026):
# rige `D9`, los NUEVE tipos. Las 18 capturas `…__celda-d-piloto-v1_0.json` NO
# se borran ni se editan -- son historia auditable, marcadas en
# `corridas-L/CD-DIN-MANIFIESTO-SUPERADAS-v1_0.json`. Este script conserva los
# DOS textos para que cualquiera pueda reconstruir el prompt exacto de cada
# tanda; `--spec-version` elige, y el valor por omisión es el vigente.
SPEC_SUFIJO_POR_DEFECTO = "celda-d-piloto-v1_2"
SPEC_SUFIJO = SPEC_SUFIJO_POR_DEFECTO


def _importa(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


_PIPE = _importa("pipeline_l_adv1_m2", PREREG / "pipeline-L-adv1-m2.py")
_RUNNER = _importa("runner_l_cli", PREREG / "runner_l_cli.py")

SpecCelda = _PIPE.SpecCelda
ParametrosCorredorL = _PIPE.ParametrosCorredorL
construir_prompt = _PIPE.construir_prompt

# Invariantes sellados -- se TOMAN del runner, no se re-declaran con otro valor.
MODELO_ALIAS = _RUNNER.MODELO_ALIAS              # "opus"
SISTEMA_MINIMO = _RUNNER.SISTEMA_MINIMO
MAX_REINTENTOS = _RUNNER.MAX_REINTENTOS          # 2
SEMILLA_ORDEN = _RUNNER.SEMILLA_ORDEN            # 42
orden_captura = _RUNNER.orden_captura
ejecutar_corrida = _RUNNER.ejecutar_corrida

K_CORRIDAS = 8                                   # PAQUETE-L-v1_1 §2, sin cambio
FECHA_CONGELACION = "2026-09-16"
TEMPERATURA = 1.0

ENCUESTA = "Encuesta Nacional de Inclusion Financiera (ENIF), INEGI, Mexico"
OLA = "2024"
ESTIMADOR = "proporcion ponderada por el factor de expansion de persona (FAC_PER)"
ESCALA = ("continua: proporcion en [0,1]. Declara ademas un intervalo "
          "subjetivo al 80 % en la forma [inferior, superior].")
# Texto de la tanda SUPERADA (siete tipos) -- se conserva verbatim para poder
# reconstruir el prompt de las 18 capturas `…__celda-d-piloto-v1_0.json`.
VARIABLE_V1_0_SIETE = (
    "ahorra_solo_informal: la persona ahorro por alguna via informal en los "
    "ultimos 12 meses (presto dinero, compro animales o bienes, guardo dinero "
    "en una caja de ahorro del trabajo o de personas conocidas, guardo dinero "
    "con familiares o personas conocidas, participo en una tanda, o guardo "
    "dinero en su casa) Y NO guardo ni ahorro en ninguna de estas siete "
    "cuentas formales: nomina, pension, apoyos de gobierno, cuenta de ahorro, "
    "cuenta de cheques, cuenta contratada por Internet o aplicacion, u otra "
    "cuenta"
)

# VIGENTE (ENMIENDA a FP-379): los NUEVE tipos de cuenta, redactados desde el
# FD de ENIF 2024 (`enif_2024_fd.xlsx`, hoja TMODULO, filas 384-442, reactivos
# P5_6_1..P5_6_9), que es el mismo constructo que P5_7_1..P5_7_9 en 2021.
VARIABLE = (
    "ahorra_solo_informal: la persona ahorro por alguna via informal en los "
    "ultimos 12 meses (presto dinero, compro animales o bienes, guardo dinero "
    "en una caja de ahorro del trabajo o de personas conocidas, guardo dinero "
    "con familiares o personas conocidas, participo en una tanda, o guardo "
    "dinero en su casa) Y NO guardo ni ahorro en ninguna de estas nueve "
    "cuentas formales: cuenta o tarjeta de nomina, cuenta o tarjeta de "
    "pension, cuenta o tarjeta para recibir apoyos de gobierno, cuenta de "
    "ahorro, cuenta de cheques, deposito a plazo fijo, fondo de inversion, "
    "cuenta contratada por Internet o aplicacion, u otro tipo de cuenta"
)

LOCALIDAD = {
    "L1": "localidades de MENOS de 15 000 habitantes (tamano de localidad 3 o 4)",
    "L2": "localidades de 15 000 habitantes O MAS (tamano de localidad 1 o 2)",
}
EDAD = {
    "E1": "de 18 a 29 anos cumplidos",
    "E2": "de 30 a 44 anos cumplidos",
    "E3": "de 45 a 59 anos cumplidos",
    "E4": "de 60 anos cumplidos o mas",
}
CELDAS = [f"{l}x{e}" for l in ("L1", "L2") for e in ("E1", "E2", "E3", "E4")]


VARIABLE_POR_SPEC = {
    "celda-d-piloto-v1_0": VARIABLE_V1_0_SIETE,   # SUPERADO-POR-SPEC
    "celda-d-piloto-v1_2": VARIABLE,              # vigente
}


def spec_de(celda: str, sufijo: str = SPEC_SUFIJO_POR_DEFECTO) -> SpecCelda:
    loc, ed = celda.split("x")
    return SpecCelda(
        id=f"CD-DIN-{celda}",
        encuesta=ENCUESTA,
        ola=OLA,
        universo=(f"personas elegidas de 18 anos y mas que viven en "
                  f"{LOCALIDAD[loc]} y tienen {EDAD[ed]}"),
        variable=VARIABLE_POR_SPEC[sufijo],
        estimador=ESTIMADOR,
        escala=ESCALA,
        frase_discriminacion="NO-APLICA",
    )


def params_de(variante: str) -> ParametrosCorredorL:
    return ParametrosCorredorL(
        modelo_id=MODELO_ALIAS,
        version_declarada="derivada por corrida del campo `model` del JSON del CLI",
        fecha_congelacion=FECHA_CONGELACION,
        temperatura=TEMPERATURA,
        k_corridas=K_CORRIDAS,
        variante=variante,
    )


def ruta_salida(celda: str, variante: str, indice: int,
                sufijo: str = SPEC_SUFIJO_POR_DEFECTO) -> Path:
    return CORRIDAS_L / f"CD-DIN-{celda}__{variante}__{indice:02d}__{sufijo}.json"


def plan(variante: str = "L-solo") -> list[tuple]:
    tuplas = [(c, variante, i) for c in CELDAS for i in range(1, K_CORRIDAS + 1)]
    return orden_captura(tuplas)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--correr", action="store_true")
    ap.add_argument("--variante", default="L-solo", choices=["L-solo", "L+corpus"])
    ap.add_argument("--spec-version", default=SPEC_SUFIJO_POR_DEFECTO,
                    choices=sorted(VARIABLE_POR_SPEC))
    args = ap.parse_args()
    if args.variante == "L+corpus":
        print("L+corpus: DIFERIDO-A-SUCESOR (ENMIENDA a FP-379, mesa 16/sep/2026). "
              "Esta en el perimetro y en la spec; la razon es costo/tiempo, y ademas "
              "`paquete-corpus-F5-v1_0/manifiesto.json` no tiene entrada para ninguna "
              "de las 8 celdas (14 celdas del marco-M, ninguna de este piloto). La "
              "dieta viva de C3 es L-solo. No se captura.", file=sys.stderr)
        return 2

    sufijo = args.spec_version
    tuplas = plan(args.variante)
    params = params_de(args.variante)
    print(f"plan: {len(tuplas)} capturas · variante={args.variante} · spec={sufijo} · "
          f"k={K_CORRIDAS} · modelo={MODELO_ALIAS} · orden semilla={SEMILLA_ORDEN}")
    if args.dry_run or not args.correr:
        muestra = construir_prompt(spec_de(tuplas[0][0], sufijo), params)
        print(f"primera tupla: {tuplas[0]}")
        print(f"sha256_prompt: {hashlib.sha256(muestra.encode('utf-8')).hexdigest()}")
        print(f"comando: {_RUNNER.construir_comando_cli()}")
        print("--- prompt ---")
        print(muestra)
        return 0

    CORRIDAS_L.mkdir(parents=True, exist_ok=True)
    escritas, saltadas, rechazos = 0, 0, 0
    for n, (celda, variante, indice) in enumerate(tuplas, 1):
        destino = ruta_salida(celda, variante, indice, sufijo)
        if destino.exists():
            saltadas += 1
            continue
        spec = spec_de(celda, sufijo)
        prompt = construir_prompt(spec, params)
        reg = ejecutar_corrida(spec, variante, prompt, spec.id, indice, params, None)
        reg["spec_piloto"] = sufijo
        reg["celda_cruce"] = celda
        reg["spec_celda"] = asdict(spec)
        destino.write_text(json.dumps(reg, ensure_ascii=False, indent=1,
                                      sort_keys=True) + "\n", encoding="utf-8")
        escritas += 1
        if reg.get("estado_captura") != "OK":
            rechazos += 1
        print(f"[{n}/{len(tuplas)}] {destino.name} · {reg.get('estado_captura')} "
              f"· modelo_real={reg.get('modelo_real')}", flush=True)
    print(f"escritas={escritas} saltadas={saltadas} rechazos={rechazos}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
