"""Emisiones (COMMIT-2) del duelo prospectivo ENIGH 2024 — PREVISTO, no
corrido por ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1 (PARO (a) del encargo: no
abre, lista ni deriva de enigh2024*). Congelado en COMMIT-1 (D-18, enmienda
de cableado) para que la sesión que sí abra la ola sólo tenga que correr
`corrida0 run` -- todo el procedimiento, incluida la guardia, ya está aquí.

Único código autorizado a llamar `emite_bajo_reserva()` sobre la ola
reservada (E.6, ver tools/enigh_duelo_guardian.py). Emite el punto de 2024
Y las predicciones de los cinco contendientes (C-PISO/C-T2/C-T3/C-TS/
C-MEDIA, tools/enigh_duelo_nacional.py) sobre la serie 2016-2022 -- las
predicciones NO usan el dato de 2024 (origen móvil ya midió su error en
CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001; aquí sólo se re-emiten para que
COMMIT-3 no tenga que releer ese CALC). No adjudica: eso es COMMIT-3.

Interfaz estable: medir(inputs, contrato) -> {"RESULT-...": valor}.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys


def _carga_modulo(nombre, ruta_absoluta):
    spec = importlib.util.spec_from_file_location(nombre, ruta_absoluta)
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
    guardian = _carga_modulo("enigh_duelo_guardian", os.path.join(raiz, "tools", "enigh_duelo_guardian.py"))
    nacional_mod = _carga_modulo("enigh_duelo_nacional", os.path.join(raiz, "tools", "enigh_duelo_nacional.py"))

    ruta_zip = inputs[par["zip_id"]]["ruta_absoluta"]
    marco = guardian.carga_hogares(ruta_zip, par["miembro_concentradohogar"], reservada=True)
    r = guardian.emite_bajo_reserva(marco, autoriza=True)

    padre = json.loads(inputs["IN-CALC-B-0001-RESULTADOS"]["bytes"].decode("utf-8"))["resultados"]
    olas_previas = par["olas_previas"]
    serie = []
    for ola in olas_previas:
        pre = f"RESULT-B-ENIGH-{ola}-"
        serie.append(nacional_mod.Punto(ola, float(padre[pre + "P"]),
                                        float(padre[pre + "IC-LO"]), float(padre[pre + "IC-HI"])))

    ola_nueva = int(par["ola_nueva"])
    predicciones = {}
    for cid in nacional_mod.CONTENDIENTES:
        pr = nacional_mod.predice(serie, ola_nueva, cid)
        predicciones[cid] = {
            "p": pr.p, "ic95": list(pr.ic95) if pr.ic95 else None,
            "estado": pr.estado, "olas_usadas": list(pr.olas_usadas),
        }
    pred_json = _canon(predicciones)

    salida = {
        "RESULT-ENIGHEM-GUARDIAN-SHA256": _sha256_archivo(os.path.join(raiz, "tools", "enigh_duelo_guardian.py")),
        "RESULT-ENIGHEM-MODULO-NACIONAL-SHA256": _sha256_archivo(os.path.join(raiz, "tools", "enigh_duelo_nacional.py")),
        "RESULT-ENIGHEM-OLA-NUEVA": ola_nueva,
        "RESULT-ENIGHEM-R-ESTADO": r["estado"],
        "RESULT-ENIGHEM-R-P": r["p"],
        "RESULT-ENIGHEM-R-IC95-JSON": _canon(r["ic95"]) if r["ic95"] else None,
        "RESULT-ENIGHEM-R-N-VALIDOS": r["n_validos"],
        "RESULT-ENIGHEM-R-N-PESO-INVALIDO": r["n_peso_invalido"],
        "RESULT-ENIGHEM-R-N-REMESAS-INVALIDO": r["n_remesas_invalido"],
        "RESULT-ENIGHEM-R-MARCO-HUELLA": marco.huella,
        "RESULT-ENIGHEM-PREDICCIONES-JSON": pred_json,
        "RESULT-ENIGHEM-PREDICCIONES-SHA256": hashlib.sha256(pred_json.encode()).hexdigest(),
    }
    return salida
