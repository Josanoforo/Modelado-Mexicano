"""Genera el contrato ejecutable de CALC-AMAI-NSE-ENIGH-2024-0001 (spec humana §5).

Los ids de `resultados:` salen de correr `medir()` sobre el zip sintético de
`tests/test_amai_enigh2024.py`, nunca a mano. El medidor se copia byte a byte.
Uso: python3 -m tools.dominios.amai.genera_spec_enigh2024
"""
from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

from tools.dominios.amai import enigh2024 as E
from tools.dominios.amai.genera_specs import _tipo

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests"))
from test_amai_enigh2024 import zip_sintetico  # noqa: E402

SPEC_MD = ROOT / "forense/prereg-caja/AMAI-NSE-ENIGH2024-spec-v1_0.md"
CID = "CALC-AMAI-NSE-ENIGH-2024-0001"
PAYLOAD = "enigh2024_nc_csv"
CODIGO = (
    ("AMAI-ENIGH2024", "tools/dominios/amai/enigh2024.py"),
    ("AMAI-AUDITORIA-ENIGH2024", "tools/dominios/amai/auditoria_enigh2024.py"),
    ("AMAI-REGLA", "tools/dominios/amai/regla.py"),
    ("AMAI-MEDIDOR-CLASE-AMAI-1", "tools/dominios/amai/medidor.py"),
    ("AMAI-COMPONENTES", "tools/dominios/amai/componentes.py"),
    ("AMAI-IMPUTACION", "tools/dominios/amai/imputacion.py"),
    ("DBFMINI", "tests/dbfmini.py"),
)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parametros(input_id: str) -> dict:
    return {"instrumento": "ENIGH", "ola": "2024", "input_id": input_id, "calc_id": CID,
            "columnas_leidas": E.lista_blanca(), "umbral_desvio_pp": 5.0, "n_min": 200,
            "referencia": "nota AMAI 2024 p.4 Figura 1 (ENIGH 2022)",
            "agrupacion": {"BAJO": ["E", "D", "D+"], "MEDIO": ["C-", "C"],
                           "ALTO": ["C+", "A/B"]},
            "firma": "C7 (FIRMAS-16, 24/sep/2026)"}


def genera() -> None:
    with tempfile.TemporaryDirectory() as t:
        z = zip_sintetico(Path(t) / "x.zip")
        raiz, E.RAIZ = E.RAIZ, Path(t)   # la tabla sintética no toca el CALC real
        try:
            out = E.medir({"P": {"ruta_absoluta": str(z)}},
                          {"parametros": parametros("P"), "seed": {"valor": 0}})
        finally:
            E.RAIZ = raiz
    carpeta = ROOT / "data/corrida0" / CID
    carpeta.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "tools/dominios/amai/enigh2024.py", carpeta / "medidor.py")
    resultados = []
    for k, v in out.items():
        tipo = _tipo(k, v)
        if k.endswith("-JSON"):
            tipo = {"tipo": "texto", "unidad": "REF a tablas/nse-enigh2024.json (JSON sin "
                                               "identificadores individuales)"}
        if k.endswith("-COLUMNAS-LEIDAS"):
            tipo = {"tipo": "texto", "unidad": "lista tabla.columna separada por comas"}
        resultados.append({"id": k, **tipo})
    spec = {
        "calc_id": CID,
        "spec_md": f"../../../forense/prereg-caja/{SPEC_MD.name}",
        "spec_md_sha256": sha(SPEC_MD),
        "script": f"data/corrida0/{CID}/medidor.py",
        "etiquetas": {"generacion": "GEN2", "tipo": "DISTRIBUCION-NSE-AMAI-RETROSPECTIVA",
                      "rotulo": "RETROSPECTIVA", "cuenta_gen2": "SI", "adopta": "NO",
                      "acto": "GEN2-CLASE-AMAI-2", "origen_numerico": "NUEVO"},
        "inputs": [{"id": PAYLOAD, "origen": "manifiesto"}] + [
            {"id": i, "origen": "repo", "funcion": "CODIGO", "ruta": r, "sha256": sha(ROOT / r)}
            for i, r in CODIGO],
        "variables": [{"archivo": c.split(".")[0], "variable": c.split(".")[1],
                       "rol": "columna autorizada por C7 (spec §2)"} for c in E.lista_blanca()],
        "universo": "ENIGH 2024 NS; hogares de concentradohogar; nacional",
        "filtros": "Hogar sin algún componente válido queda sin NSE (conteo reportado); "
                   "factor > 0",
        "ponderador": "factor",
        "transformacion": "regla AMAI 2024 (spec AMAI-NSE v1.0 §1); masa ponderada por nivel "
                          "y grupo NSE; supresión n<200",
        "estimando": "distribución NSE AMAI nacional de hogares, ENIGH 2024, y su desvío "
                     "contra la Figura 1 AMAI (ENIGH 2022)",
        "parametros": parametros(PAYLOAD),
        "seed": {"aplica": False},
        "dependencias_materiales": ["numpy", "pandas"],
        "tolerancia": {"tipo": "flotante", "abs": 1e-10,
                       "razon": "mismo payload y mismo orden de filas; sin azar"},
        "resultados": resultados,
    }
    (carpeta / "spec.yaml").write_text(
        "# El primer resultado que produzca este procedimiento es el que se reporta.\n"
        + yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(CID, len(resultados))


if __name__ == "__main__":
    genera()
