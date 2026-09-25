"""Genera los seis contratos ejecutables AMAI-NSE (spec humana §4).

Los ids de `resultados:` salen de correr `medir()` sobre payloads sintéticos
(`sintetico.py`), nunca a mano. El medidor se copia byte a byte a cada CALC.
Uso: python3 -m tools.dominios.amai.genera_specs
"""
from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
from pathlib import Path

import yaml

from tools.dominios.amai import medidor as M
from tools.dominios.amai import sintetico as S

ROOT = Path(__file__).resolve().parents[3]
SPEC_MD = ROOT / "forense/prereg-caja/AMAI-NSE-spec-v1_0.md"
SEMILLA = 20260924
CALCS = {
    ("ENIGH", "2022"): ("enigh2022_nc_csv", None, "hogar", "factor"),
    ("ENIF", "2021"): ("enif_2021_enif_2021_bd_csv", None, "hogar (sin pisos)", "FAC_HOG"),
    ("ENIF", "2024"): ("enif_2024_enif_2024_bd_csv", None, "persona elegida 18+", "FAC_PER"),
    ("ENDUTIH", "2023"): ("endutih_2023_endutih2023_bd_dbf", "enigh2022_nc_csv",
                          "persona 6+", "FAC_PER"),
    ("ENDUTIH", "2024"): ("endutih2024_bd_dbf_zip", "enigh2022_nc_csv", "persona 6+", "FAC_PER"),
    ("ENDUTIH", "2025"): ("endutih_2025_endutih2025_bd_dbf", "enigh2022_nc_csv",
                          "persona 6+", "FAC_PER"),
}
CODIGO = (
    ("AMAI-REGLA", "tools/dominios/amai/regla.py"),
    ("AMAI-COMPONENTES", "tools/dominios/amai/componentes.py"),
    ("AMAI-IMPUTACION", "tools/dominios/amai/imputacion.py"),
    ("REGION-ESTADISTICA", "tools/astra/region/estadistica.py"),
    ("REPLICAS-COMPARTIDAS", "tools/celda_d/marginales_reproduccion.py"),
    ("DBFMINI", "tests/dbfmini.py"),
)
CODIGO_ENIF = (
    ("REGION-ENIF-PORTAFOLIO", "tools/astra/region/enif_portafolio.py"),
    ("REGION-ENIF-CONDICIONALES", "tools/astra/region/enif_condicionales.py"),
    ("REGION-ENIF-NO-TRABAJA", "tools/astra/region/enif_no_trabaja.py"),
    ("REGION-MEDIDOR-CSV", "tools/astra/region/medidor.py"),
)
CODIGO_ENDUTIH = (("ENDUTIH-PISOS-MEDIDOR", "tools/dominios/endutih/pisos.py"),)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def calc_id(inst: str, ola: str) -> str:
    return f"CALC-AMAI-NSE-{inst}-{ola}-0001"


def parametros(inst, ola, payload, donante):
    par = {"instrumento": inst, "ola": ola, "input_id": payload,
           "conductas": list(M.CONDUCTAS[(inst, ola)]), "bootstrap_replicas": 1000,
           "n_min": 200, "umbral_desvio_pp": 5.0, "tolerancia_reproduce_pp": 0.15,
           "agrupacion": {"BAJO": ["E", "D", "D+"], "MEDIO": ["C-", "C"],
                          "ALTO": ["C+", "A/B"]}}
    if donante:
        par["input_donante"] = donante
    return par


def corrida_sintetica(inst, ola, rama="normal", replicas=40, n=1200):
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        don = S.enigh2022(t / "enigh.zip", n=n, rama="normal")
        if inst == "ENIGH":
            ruta = S.enigh2022(t / "x.zip", n=n, rama=rama)
        elif inst == "ENIF":
            ruta = S.enif(t / "x.zip", ola, n=n, rama=rama)
        else:
            ruta = S.endutih(t / "x.zip", ola, n=n, rama=rama)
        par = parametros(inst, ola, "PAYLOAD", "DONANTE" if inst == "ENDUTIH" else None)
        par["bootstrap_replicas"] = replicas
        inputs = {"PAYLOAD": {"ruta_absoluta": str(ruta)},
                  "DONANTE": {"ruta_absoluta": str(don)}}
        return M.medir(inputs, {"parametros": par, "seed": {"valor": SEMILLA}})


def _tipo(rid: str, valor) -> dict:
    if rid.endswith("-JSON"):
        return {"tipo": "texto", "unidad": "JSON sin identificadores individuales"}
    if rid.endswith("-ESTADO"):
        return {"tipo": "texto", "unidad": "estado de publicación o de validación"}
    if re.search(r"-(N|N-HOGARES-CON-NSE|N-HOGARES-SIN-NSE)$", rid):
        return {"tipo": "entero", "unidad": "conteo no ponderado"}
    if rid.endswith("-PP"):
        return {"tipo": "flotante", "unidad": "puntos porcentuales", "permite_no_estimable": True}
    uni = ("límite inferior IC95" if rid.endswith("-IC-LO") else
           "límite superior IC95" if rid.endswith("-IC-HI") else "proporción [0,1]")
    return {"tipo": "proporcion", "unidad": uni, "permite_no_estimable": True}


def genera():
    md_sha = sha(SPEC_MD)
    for (inst, ola), (payload, donante, unidad, factor) in CALCS.items():
        cid = calc_id(inst, ola)
        carpeta = ROOT / "data/corrida0" / cid
        carpeta.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "tools/dominios/amai/medidor.py", carpeta / "medidor.py")
        out = corrida_sintetica(inst, ola)
        resultados = [{"id": k, **_tipo(k, v)} for k, v in out.items()]
        codigo = CODIGO + (CODIGO_ENIF if inst == "ENIF" else ()) + (
            CODIGO_ENDUTIH if inst == "ENDUTIH" else ())
        inputs = [{"id": payload, "origen": "manifiesto"}]
        if donante:
            inputs.append({"id": donante, "origen": "manifiesto"})
        inputs += [{"id": i, "origen": "repo", "funcion": "CODIGO", "ruta": r,
                    "sha256": sha(ROOT / r)} for i, r in codigo]
        spec = {
            "calc_id": cid,
            "spec_md": f"../../../forense/prereg-caja/{SPEC_MD.name}",
            "spec_md_sha256": md_sha,
            "script": f"data/corrida0/{cid}/medidor.py",
            "etiquetas": {"generacion": "GEN2", "tipo": "PISO-NSE-AMAI-RETROSPECTIVO",
                          "rotulo": "RETROSPECTIVA", "cuenta_gen2": "SI", "adopta": "NO",
                          "acto": "GEN2-CLASE-AMAI-1", "origen_numerico": "NUEVO"},
            "inputs": inputs,
            "variables": [{"archivo": "microdato de la spec humana §4", "variable": v, "rol": r}
                          for v, r in ((factor, "factor de expansión"),
                                       ("EST_DIS/est_dis", "estrato de diseño"),
                                       ("UPM_DIS/upm", "UPM de diseño"))],
            "universo": f"{inst} {ola}; NSE por hogar; pisos en unidad {unidad}",
            "filtros": "Hogar sin algún componente válido queda sin NSE; conductas con su "
                       "denominador sellado; no se filtra el marco antes de las réplicas",
            "ponderador": factor,
            "transformacion": "regla AMAI 2024 (spec §1-§4); razón de masas ponderadas por "
                              "grupo NSE; IC percentil de réplicas UPM compartidas; supresión n<200",
            "estimando": f"distribución NSE de hogares y proporción de cada conducta por grupo "
                         f"NSE (BAJO/MEDIO/ALTO), {inst} {ola}",
            "parametros": parametros(inst, ola, payload, donante),
            "seed": {"aplica": True, "valor": SEMILLA, "rng": "numpy.PCG64"},
            "dependencias_materiales": ["numpy", "pandas"],
            "tolerancia": {"tipo": "flotante", "abs": 1e-10,
                           "razon": "mismo payload, mismo orden de filas y semilla"},
            "resultados": resultados,
        }
        (carpeta / "spec.yaml").write_text(
            "# El primer resultado que produzca este procedimiento es el que se reporta.\n"
            + yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(cid, len(resultados))


if __name__ == "__main__":
    genera()
