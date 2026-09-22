"""RETROSPECTIVA-MECÁNICA del duelo prospectivo ENIGH 2024, P4.

ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1. Lo genérico está fuera, propio de este
acto (NO es tools/duelo/, que está ajeno al perímetro):
`tools/enigh_duelo_nacional.py` — C-PISO/C-T2/C-T3/C-TS/C-MEDIA, origen
móvil, chequeo de coincidencias. Su sha256 se emite como RESULT en esta
misma corrida (mismo patrón que CALC-DUELO-ORIGEN-MOVIL-0001 de ENVIPE con
tools/duelo/tendencia_nacional.py).

Corre sobre la serie SELLADA de `remesas>0` (RESULT-B-ENIGH-{ola}-* de
CALC-B-0001, citado como input con hash) -- cero microdato de ENIGH 2024,
cero microdato de ninguna ola: los cuatro puntos son proporciones y IC95 ya
publicados por un CALC ajeno sellado antes de este acto.

Interfaz estable: medir(inputs, contrato) -> {"RESULT-...": valor}.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys


def _carga_modulo(ruta_absoluta):
    spec = importlib.util.spec_from_file_location("enigh_duelo_nacional", ruta_absoluta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _sha256_archivo(ruta):
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()


def _canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def medir(inputs, contrato):
    par = contrato["parametros"]
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    ruta_modulo = os.path.join(raiz, "tools", "enigh_duelo_nacional.py")
    m = _carga_modulo(ruta_modulo)
    sha_modulo = _sha256_archivo(ruta_modulo)

    padre = json.loads(inputs["IN-CALC-B-0001-RESULTADOS"]["bytes"].decode("utf-8"))["resultados"]
    olas = par["olas_ventana"]
    serie = []
    for ola in olas:
        pre = f"RESULT-B-ENIGH-{ola}-"
        p = padre[pre + "P"]
        lo = padre[pre + "IC-LO"]
        hi = padre[pre + "IC-HI"]
        serie.append(m.Punto(ola, float(p), float(lo), float(hi)))

    om = m.origen_movil(serie)

    coinc_por_ola = {ola: m.coincidencias(serie, ola) for ola in olas}
    coincidencias_planas = []
    for ola, c in coinc_por_ola.items():
        for a, b, val in c["coincidencias_exactas"]:
            coincidencias_planas.append({"ola": ola, "a": a, "b": b, "valor": val})

    resumen_json = _canon(om["resumen"])
    por_ola_json = _canon({str(k): v for k, v in om["por_ola"].items()})
    coincidencias_json = _canon(coincidencias_planas)

    salida = {
        "RESULT-ENIGHDM-MODULO-SHA256": sha_modulo,
        "RESULT-ENIGHDM-SERIE-OLAS-JSON": _canon(olas),
        "RESULT-ENIGHDM-VENTANA-COMUN-JSON": _canon(om["ventana_comun"]),
        "RESULT-ENIGHDM-RESUMEN-JSON": resumen_json,
        "RESULT-ENIGHDM-RESUMEN-SHA256": hashlib.sha256(resumen_json.encode()).hexdigest(),
        "RESULT-ENIGHDM-POR-OLA-JSON": por_ola_json,
        "RESULT-ENIGHDM-COINCIDENCIAS-JSON": coincidencias_json,
    }
    for cid in m.CONTENDIENTES:
        r = om["resumen"][cid]["todas"]
        clave = cid.replace("-", "")
        salida[f"RESULT-ENIGHDM-{clave}-N-OLAS"] = r["n_olas"]
        salida[f"RESULT-ENIGHDM-{clave}-MAE-PP"] = r["mae_pp"]
        salida[f"RESULT-ENIGHDM-{clave}-SESGO-PP"] = r["sesgo_pp"]
        salida[f"RESULT-ENIGHDM-{clave}-COBERTURA-R-EN-IC-CAND"] = r["cobertura_R_en_ic_cand"]
    return salida
