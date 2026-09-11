#!/usr/bin/env python3
"""Genera/verifica la lista cerrada de inputs de CALC-F5-REANALISIS-0001."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-F5-REANALISIS-0001"
DESTINO = CALC / "spec.yaml"
PLAN = Path("forense/prereg-duelo-v2/F5-completa-plan-v1_0.json")
UNIVERSO = Path("forense/prereg-duelo-v2/universo-triada-v1_4.tsv")
SNAPSHOT = Path("forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json")
TARJETAS = Path("forense/prereg-duelo-v2/F5-reanalisis-tarjetas-M-R-v1_0.tsv")
CONTRATO = Path("forense/prereg-duelo-v2/F5-evaluacion-sin-fugas-spec-v1_0.md")
CALCULADOR = Path("tools/calcula_f5_sin_fugas.py")


def sha(ruta: Path) -> str:
    return hashlib.sha256((ROOT / ruta).read_bytes()).hexdigest()


def entrada(iid: str, rol: str, ruta: Path, **campos) -> dict:
    return {
        "id": iid, "origen": "repo", "ruta": ruta.as_posix(),
        "sha256": sha(ruta), "rol": rol, **campos,
    }


def construir(ruta_linaje: Path) -> dict:
    plan = json.loads((ROOT / PLAN).read_text(encoding="utf-8"))
    with (ROOT / UNIVERSO).open(encoding="utf-8", newline="") as fh:
        universo = list(csv.DictReader(fh, delimiter="\t"))
    inputs = [
        entrada("IN-F5SF-CONTRATO", "contrato_estudio", CONTRATO),
        entrada("IN-F5SF-PLAN", "plan", PLAN),
        entrada("IN-F5SF-SNAPSHOT-M", "snapshot_m", SNAPSHOT),
        entrada("IN-F5SF-UNIVERSO-R", "universo_r", UNIVERSO),
        entrada("IN-F5SF-TARJETAS-MR", "tarjetas_mr", TARJETAS),
        entrada("IN-F5SF-CALCULADOR", "calculador", CALCULADOR),
        entrada("IN-F5SF-LINAJE", "linaje", ruta_linaje),
    ]
    for posicion in plan["posiciones"]:
        cid = posicion["id_celda"]
        variante = posicion["variante"]
        replica = int(posicion["replica"])
        iid = (f"IN-F5SF-L-{cid}-{variante}-{replica:02d}"
               .replace("+", "PLUS"))
        inputs.append(entrada(
            iid, "captura_l", Path(posicion["ruta"]), id_celda=cid,
            variante=variante, replica=replica,
        ))
    for fila in universo:
        cid = fila["id_celda"]
        ruta = Path(fila["fuente_R"]) / "resultados.json"
        datos = json.loads((ROOT / ruta).read_text(encoding="utf-8"))
        inputs.append(entrada(
            f"IN-F5SF-R-{cid}", "resultado_r", ruta, id_celda=cid,
            calc_id_esperado=datos["spec_id"],
            result_id_punto=f"RESULT-R-{cid}-PUNTO",
            result_id_estado=(f"RESULT-R-{cid}-ESTADO"
                               if f"RESULT-R-{cid}-ESTADO"
                               in datos.get("resultados", {}) else ""),
        ))

    def resultado(iid: str, tipo: str, unidad: str,
                  permite: bool = False) -> dict:
        fila = {"id": iid, "tipo": tipo, "unidad": unidad}
        if permite:
            fila["permite_no_estimable"] = True
        return fila

    resultados = [
        resultado("RESULT-F5SF-POSICIONES", "entero", "posiciones"),
        resultado("RESULT-F5SF-VALIDAS", "entero", "replicas"),
        resultado("RESULT-F5SF-ABSTENCIONES", "entero", "replicas"),
        resultado("RESULT-F5SF-MALFORMADAS", "entero", "replicas"),
        resultado("RESULT-F5SF-ERRORES-TECNICOS", "entero", "replicas"),
        resultado("RESULT-F5SF-ERRORES-IDENTIDAD", "entero", "replicas"),
        resultado("RESULT-F5SF-MARCO-N", "entero", "celdas"),
        resultado("RESULT-F5SF-U3-N", "entero", "celdas"),
        resultado("RESULT-F5SF-U3-IDS", "texto", "ids_de_celda"),
        resultado("RESULT-F5SF-COMPARACION-COMPROMETIDA", "texto", "categoria"),
        resultado("RESULT-F5SF-COBERTURA-L-SOLO", "entero", "celdas_con_punto"),
        resultado("RESULT-F5SF-COBERTURA-L-CORPUS", "entero", "celdas_con_punto"),
        resultado("RESULT-F5SF-COBERTURA-M-PUNTO", "entero", "celdas_con_punto"),
        resultado("RESULT-F5SF-COBERTURA-M-ELEGIBLE", "entero", "celdas_elegibles"),
        resultado("RESULT-F5SF-COBERTURA-R", "entero", "celdas_con_punto"),
        resultado("RESULT-F5SF-MAE-L-SOLO-PP", "flotante", "puntos_porcentuales", True),
        resultado("RESULT-F5SF-MAE-L-CORPUS-PP", "flotante", "puntos_porcentuales", True),
        resultado("RESULT-F5SF-MAE-M-PP", "flotante", "puntos_porcentuales", True),
        resultado("RESULT-F5SF-VEREDICTO-GLOBAL", "texto", "categoria"),
        resultado("RESULT-F5SF-DETALLE-CELDAS-JSON", "texto", "json_canonico"),
    ]
    for corto in ("LCORPUS-LSOLO", "M-LSOLO", "M-LCORPUS"):
        prefijo = f"RESULT-F5SF-DELTA-{corto}"
        resultados.extend([
            resultado(f"{prefijo}-PUNTO-PP", "flotante", "puntos_porcentuales", True),
            resultado(f"{prefijo}-IC95-LO-PP", "flotante", "puntos_porcentuales", True),
            resultado(f"{prefijo}-IC95-HI-PP", "flotante", "puntos_porcentuales", True),
            resultado(f"{prefijo}-VEREDICTO", "texto", "categoria"),
        ])

    return {
        "calc_id": "CALC-F5-REANALISIS-0001",
        "spec_md": "spec.md", "spec_md_sha256": sha(CALC.relative_to(ROOT) / "spec.md"),
        "script": "data/corrida0/CALC-F5-REANALISIS-0001/medidor.py",
        "etiquetas": {
            "generacion": "GEN2", "tipo": "F5-REANALISIS-SIN-FUGAS",
            "cuenta_gen2": "NO", "validacion_independiente": "NO-HECHA",
            "adopta_al_motor": "NO",
            "naturaleza": "REANALISIS-DIAGNOSTICO-PANEL-CONOCIDO",
        },
        "inputs": inputs, "dependencias_materiales": [],
        "universo": "Panel histórico fijo de 14 celdas; U3 congelado de CALC-TRIADA-0002.",
        "filtros": "Elegibilidad fail-closed por identidad, firewall, linaje, corte, estimando y punto; faltantes no se imputan.",
        "ponderador": "Peso igual por celda en U3; el diseño de cada R no se mezcla con el bootstrap de errores.",
        "transformacion": "Última línea L a proporción, mediana de réplicas válidas, error absoluto en pp y bootstrap pareado.",
        "estimando": "Diagnóstico retrospectivo de error frente a R en el panel conocido; no transferencia ni validación independiente.",
        "parametros": {
            "plan_version": plan["version"], "n_posiciones": 224,
            "k_replicas": 8,
            "variantes": {"L-solo": "L_SOLO", "L+corpus": "L_CORPUS"},
            "seleccion": "MEDIANA-DE-REPLICAS-VALIDAS",
            "bootstrap_replicas": 10000, "nivel_ic": 0.95,
            "delta_banda_pp": 0.5, "tolerancia_numerica_pp": 1.0e-9,
            "contendientes": ["L_SOLO", "L_CORPUS", "M"],
            "comparaciones": [["L_CORPUS", "L_SOLO"], ["M", "L_SOLO"], ["M", "L_CORPUS"]],
            "u3_congelado": [
                "CIV-M-01", "CIV-M-02", "CIV-M-04", "CIV-M-10",
                "CIV-M-12", "CIV-M-13", "FAM-M-01", "FAM-M-05",
                "FAM-M-06", "FAM-M-07", "TRA-M-02", "TRA-M-03",
            ],
            "proposito": "REANALISIS-DIAGNOSTICO-TRANSFERENCIA",
            "estado_firewall_apto": "LIMPIO-DE-OBJETIVO",
            "estado_m_apto": "EMITE", "comparabilidad_apta": "ACREDITADA",
            "cumple_corte_apto": "SI", "r_punto_apto": "SI",
            "regex_punto_l": r"^ESTIMACION_PUNTUAL=(\d+(?:[.,]\d+)?)%$",
            "estados_r_aptos": ["CALCULADO"],
        },
        "seed": {"aplica": True, "valor": 42, "rng": "random.Random"},
        "tolerancia": {"tipo": "flotante", "abs": 1.0e-9,
                        "razon": "Separada de la banda práctica de 0.5 pp."},
        "resultados": resultados, "variables": [],
    }


def serializar(datos: dict) -> str:
    return yaml.safe_dump(datos, allow_unicode=True, sort_keys=False,
                          width=100000)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--linaje", type=Path, required=True,
                    help="ruta repo-local del módulo común entregado por el acto 17")
    ap.add_argument("--verifica", action="store_true")
    args = ap.parse_args()
    esperado = serializar(construir(args.linaje))
    if args.verifica:
        real = DESTINO.read_text(encoding="utf-8") if DESTINO.exists() else ""
        if real != esperado:
            print(f"DISCORDA: {DESTINO.relative_to(ROOT)}")
            return 1
        print(f"COINCIDE: {DESTINO.relative_to(ROOT)}")
        return 0
    DESTINO.write_text(esperado, encoding="utf-8")
    print(f"ESCRITO: {DESTINO.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
