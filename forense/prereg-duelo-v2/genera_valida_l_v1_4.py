#!/usr/bin/env python3
"""Genera, valida y hace dry-run del contrato sucesor L v1.4.

No abre resultados R/M/TRIADA, no interpreta capturas y no invoca modelos.
La fuente humana es L-estimandos-v1_4.tsv. Las tres celdas sin cambio material
conservan literalmente su entrada v1.3; las restantes reciben universo y evento
explícitos de la target card.
"""
from __future__ import annotations

import argparse
import copy
import csv
import importlib.util
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[1]
TARGETS = DIR / "L-estimandos-v1_4.tsv"
SPEC_ANTERIOR = DIR / "L-spec-v1_3.json"
SPEC_NUEVA = DIR / "L-spec-v1_4.json"
MARCO = DIR / "marco-M-sorteado-v1_3.tsv"
DIAGNOSTICO = DIR / "diagnostico-corpus-L-v1_4.tsv"
RUNNER = DIR / "runner_l_cli.py"

COLUMNAS = {
    "id", "encuesta", "ola", "unidad_observacion", "universo_L",
    "evento_L", "escala", "fuente_definicion", "cambio_vs_v1_3",
    "requiere_recaptura",
}
PROHIBIDO_UNIVERSO = "NO ESTIMADO EN ESTE ACTO"
ALIAS_TRA_PROHIBIDO = "paga_mordida_encig2025"
K = 8
VARIANTES = ("L-solo", "L+corpus")


def leer_tsv(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def pregunta(row: dict[str, str]) -> str:
    return (
        f'En la encuesta {row["encuesta"]} (ola {row["ola"]}), para el universo '
        f'"{row["universo_L"]}", ¿cuál es tu estimación de la proporción del '
        f'universo para la que se cumple el evento "{row["evento_L"]}"? '
        f'Unidad de observación: {row["unidad_observacion"]}. Escala de respuesta: '
        f'{row["escala"]}. Da tu mejor estimación puntual y, si no conoces el '
        "dato, dilo explícitamente -- no inventes una cifra plausible."
    )


def construir() -> dict:
    rows = leer_tsv(TARGETS)
    anterior = json.loads(SPEC_ANTERIOR.read_text(encoding="utf-8"))
    por_id_anterior = {x["id"]: x for x in anterior["celdas"]}
    celdas = []
    for row in rows:
        if row["requiere_recaptura"] == "NO":
            celda = dict(por_id_anterior[row["id"]])
            celda["unidad_observacion"] = row["unidad_observacion"]
            celda["evento_L"] = row["evento_L"]
            celda["fuente_definicion"] = row["fuente_definicion"]
            celda["cambio_vs_v1_3"] = row["cambio_vs_v1_3"]
            celda["requiere_recaptura"] = "NO"
        else:
            celda = {
                "conducta": row["evento_L"],
                "encuesta": row["encuesta"],
                "escala": row["escala"],
                "evento_L": row["evento_L"],
                "fuente_definicion": row["fuente_definicion"],
                "id": row["id"],
                "ola": row["ola"],
                "pregunta_L": pregunta(row),
                "unidad_observacion": row["unidad_observacion"],
                "universo": row["universo_L"],
                "cambio_vs_v1_3": row["cambio_vs_v1_3"],
                "requiere_recaptura": "SI",
            }
        celdas.append(celda)
    return {
        "acto": "GEN2-F5-L-ESTIMANDO-V1-4 · L-SPEC-v1_4",
        "celdas": celdas,
        "declaracion": (
            "Contrato sucesor prospectivo de 14 celdas. Entrega a L la definición "
            "humana del mismo estimando primario que arbitra R, nunca la respuesta "
            "de R. No contiene puntos, errores, intervalos, resultados M/TRIADA ni "
            "conteos de sí/no. Las capturas v1.3 permanecen históricas e intactas."
        ),
        "derivacion": (
            "L-estimandos-v1_4.tsv es la fuente humana. Las filas con cambio material "
            "se transforman mediante pregunta(); FAM-M-05/06/07 conservan literalmente "
            "la pregunta v1.3 porque P1 confirmó que ya estaba alineada."
        ),
        "fecha": "2026-09-10",
        "fuente_marco_ids": "forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv",
        "fuente_target_card": "forense/prereg-duelo-v2/L-estimandos-v1_4.tsv",
        "k_corridas": K,
        "n_celdas": len(celdas),
        "n_celdas_recaptura": sum(x["requiere_recaptura"] == "SI" for x in celdas),
        "n_invocaciones_futuras": sum(x["requiere_recaptura"] == "SI" for x in celdas) * len(VARIANTES) * K,
        "plantilla_honestidad": "Da tu mejor estimación puntual y, si no conoces el dato, dilo explícitamente -- no inventes una cifra plausible.",
        "version": "v1_4",
    }


def ids_marco() -> list[str]:
    return [r["id"] for r in leer_tsv(MARCO) if r.get("elegible_v1_1") == "SI"]


def validar(spec: dict) -> None:
    targets = leer_tsv(TARGETS)
    assert targets and COLUMNAS <= set(targets[0]), "faltan columnas obligatorias en target card"
    ids = [x["id"] for x in spec["celdas"]]
    assert len(ids) == 14 and len(set(ids)) == 14, "L-spec-v1_4 debe contener exactamente 14 ids únicos"
    assert ids == ids_marco(), "los ids o su orden difieren del marco congelado 14/14"
    assert ids == [x["id"] for x in targets], "target card y spec difieren en ids u orden"
    for target, celda in zip(targets, spec["celdas"]):
        assert celda.get("universo", "").strip(), f'{celda["id"]}: falta universo explícito'
        assert celda.get("evento_L", "").strip(), f'{celda["id"]}: falta evento explícito'
        assert PROHIBIDO_UNIVERSO not in celda["universo"], f'{celda["id"]}: universo-placeholder prohibido'
        definicion = " ".join(str(celda.get(k, "")) for k in ("conducta", "evento_L", "pregunta_L"))
        if celda["id"].startswith("TRA-"):
            assert ALIAS_TRA_PROHIBIDO not in definicion, f'{celda["id"]}: alias de consumidor usado como definición'
        material = target["cambio_vs_v1_3"] != "SIN-CAMBIO-MATERIAL"
        assert target["requiere_recaptura"] == ("SI" if material else "NO"), f'{celda["id"]}: recaptura no deriva del cambio material'
        assert celda["requiere_recaptura"] == target["requiere_recaptura"]
        assert "mejor estimación puntual" in celda["pregunta_L"]
        assert "no inventes una cifra plausible" in celda["pregunta_L"]
    assert spec["n_celdas_recaptura"] == 11
    assert spec["n_invocaciones_futuras"] == 176


def autoprobar_guardias(spec: dict) -> None:
    """Falsadores mínimos de los cinco defectos que P4 exige rechazar."""
    casos = []
    mutado = copy.deepcopy(spec)
    mutado["celdas"][0]["universo"] = PROHIBIDO_UNIVERSO
    casos.append(("universo-placeholder", mutado))
    mutado = copy.deepcopy(spec)
    tra = next(x for x in mutado["celdas"] if x["id"] == "TRA-M-02")
    tra["evento_L"] = ALIAS_TRA_PROHIBIDO
    casos.append(("alias-TRA", mutado))
    mutado = copy.deepcopy(spec)
    mutado["celdas"][0]["evento_L"] = ""
    casos.append(("evento-vacío", mutado))
    mutado = copy.deepcopy(spec)
    mutado["celdas"].pop()
    casos.append(("cardinalidad", mutado))
    mutado = copy.deepcopy(spec)
    mutado["celdas"][0]["id"] = "ID-AJENO-AL-MARCO"
    casos.append(("ids-marco", mutado))
    for nombre, caso in casos:
        try:
            validar(caso)
        except AssertionError:
            continue
        raise AssertionError(f"la guardia {nombre} no rechazó su falsador")


def cargar_runner():
    module_spec = importlib.util.spec_from_file_location("runner_l_cli_v14_base", RUNNER)
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    return module


def validar_diagnostico(runner) -> None:
    diag = {r["id"]: r for r in leer_tsv(DIAGNOSTICO)}
    recaptura = [r for r in leer_tsv(TARGETS) if r["requiere_recaptura"] == "SI"]
    assert set(diag) == {r["id"] for r in recaptura}, "diagnóstico no cubre exactamente la recaptura"
    for row in recaptura:
        texto, meta = runner.cargar_contexto_corpus(row["id"])
        d = diag[row["id"]]
        assert int(d["documentos_disponibles"]) == meta["documentos_disponibles"]
        assert int(d["documentos_incluidos_antes_limite"]) == len(meta["documentos_incluidos"])
        assert int(d["chars_incluidos"]) == meta["chars_incluidos"]
        assert d["truncado"] == ("SI" if meta["truncado"] else "NO")
        encuesta = "ENNViH" if row["id"] == "DIN-M-01" else row["encuesta"]
        menciona_encuesta = encuesta.casefold() in texto.casefold()
        ola_simple = row["ola"].split()[0]
        assert d["menciona_encuesta"] == ("SI" if menciona_encuesta else "NO")
        conjunta = menciona_encuesta and ola_simple in texto
        assert d["menciona_encuesta_y_ola"] == ("SI" if conjunta else "NO")
        assert d["evidencia_directa_evento"] in {"SI", "NO", "DUDOSA"}


def dry_run(spec: dict) -> None:
    runner = cargar_runner()
    runner._CARGA.L_SPEC_JSON = SPEC_NUEVA
    validar_diagnostico(runner)
    recaptura = [x for x in spec["celdas"] if x["requiere_recaptura"] == "SI"]
    rutas: set[Path] = set()
    prompts = 0
    for celda in recaptura:
        obj = runner.celda_a_spec(celda)
        for variante in VARIANTES:
            contexto = ""
            if variante == "L+corpus":
                contexto, _ = runner.cargar_contexto_corpus(celda["id"])
            params = runner._CARGA.construir_params(variante, "paquete-corpus-F5-v1_0" if variante == "L+corpus" else None)
            prompt = runner.construir_prompt(obj, params, contexto)
            assert prompt and celda["universo"] in prompt and celda["evento_L"] in prompt
            prompts += 1
            for indice in range(1, K + 1):
                ruta = DIR / "corridas-L" / f'L-{celda["id"]}-M__{variante}__{indice:02d}__v1_4.json'
                assert ruta not in rutas and not ruta.exists(), f"ruta ocupada o repetida: {ruta}"
                rutas.add(ruta)
    assert len(rutas) == 176 and prompts == 22
    print("OK -- target card y L-spec-v1_4: 14/14 ids; 11 recapturas mecánicas")
    print("OK -- 22 prompts y 176 rutas futuras v1_4 construidas; cero invocaciones de modelo")
    print("OK -- diagnóstico L+corpus recompuesto con paquete-corpus-F5-v1_0 y límite 600000 intacto")


def diff_semantico(spec: dict) -> None:
    anterior = {x["id"]: x for x in json.loads(SPEC_ANTERIOR.read_text(encoding="utf-8"))["celdas"]}
    for celda in spec["celdas"]:
        campos = [k for k in ("universo", "conducta", "pregunta_L") if celda.get(k) != anterior[celda["id"]].get(k)]
        print(f'{celda["id"]}\t{celda["cambio_vs_v1_3"]}\t{",".join(campos) if campos else "SIN-DIFF"}\tRECAPTURA={celda["requiere_recaptura"]}')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--escribe", action="store_true")
    ap.add_argument("--valida", action="store_true")
    ap.add_argument("--diff-semantico", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not any(vars(args).values()):
        ap.error("elige al menos una acción")
    esperado = construir()
    if args.escribe:
        SPEC_NUEVA.write_text(json.dumps(esperado, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    spec = json.loads(SPEC_NUEVA.read_text(encoding="utf-8"))
    assert spec == esperado, "L-spec-v1_4.json no coincide con su derivación mecánica"
    validar(spec)
    if args.valida:
        autoprobar_guardias(spec)
        print("OK -- validación 14/14 y 5/5 falsadores de guardias rechazados")
    if args.diff_semantico:
        diff_semantico(spec)
    if args.dry_run:
        dry_run(spec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
