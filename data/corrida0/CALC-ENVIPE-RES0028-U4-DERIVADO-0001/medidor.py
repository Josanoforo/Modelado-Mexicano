"""Complemento U4 de RES-0028 sobre el RESULT sellado de CALC-ENVIPE-0001.

Interfaz del runner GEN2: ``medir(inputs, contrato) -> dict``. La función no
abre microdatos ni escribe archivos. Verifica los bytes de la cadena sellada
del padre antes de transformar el punto y el intervalo.
"""
from __future__ import annotations

import hashlib
import json
import math


IN_RESULTADOS = "IN-ENVIPE-0001-RESULTADOS"
IN_SPEC = "IN-ENVIPE-0001-SPEC"
IN_SELLO = "IN-ENVIPE-0001-SELLO"
IN_SELLO_SHA = "IN-ENVIPE-0001-SELLO-SHA256"
PREFIX = "RESULT-ENVIPE-RES0028-"


def _bytes(inputs: dict, iid: str) -> bytes:
    entrada = inputs[iid]
    crudo = entrada.get("bytes")
    if crudo is not None:
        return crudo
    with open(entrada["ruta_absoluta"], "rb") as fh:
        return fh.read()


def _sha(crudo: bytes) -> str:
    return hashlib.sha256(crudo).hexdigest()


def _verifica_cadena_sellada(inputs: dict) -> dict:
    resultados_b = _bytes(inputs, IN_RESULTADOS)
    spec_b = _bytes(inputs, IN_SPEC)
    sello_b = _bytes(inputs, IN_SELLO)
    sidecar_b = _bytes(inputs, IN_SELLO_SHA)

    try:
        sello = json.loads(sello_b.decode("utf-8"))
        sidecar = sidecar_b.decode("utf-8").split()[0]
        resultados = json.loads(resultados_b.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, IndexError) as exc:
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-CADENA-ILEGIBLE: {exc}") from exc

    esperados = {
        "resultados.json": _sha(resultados_b),
        "spec.yaml": _sha(spec_b),
    }
    if sidecar != _sha(sello_b):
        raise RuntimeError("PADRE-NO-ESTIMABLE-SELLO-SIDECAR-NO-COINCIDE")
    for nombre, real in esperados.items():
        if sello.get(nombre) != real:
            raise RuntimeError(
                f"PADRE-NO-ESTIMABLE-SELLO-NO-CUBRE-{nombre}: "
                f"declarado={sello.get(nombre)!r} real={real}"
            )
    if resultados.get("spec_id") != "CALC-ENVIPE-0001":
        raise RuntimeError("PADRE-NO-ESTIMABLE-SPEC-ID-INCORRECTO")
    valores = resultados.get("resultados")
    if not isinstance(valores, dict):
        raise RuntimeError("PADRE-NO-ESTIMABLE-RESULTADOS-AUSENTES")
    return valores


def _numero(valores: dict, rid: str) -> float:
    valor = valores.get(rid)
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-RESULTADO-NO-NUMERICO:{rid}={valor!r}")
    valor = float(valor)
    if not math.isfinite(valor):
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-RESULTADO-NO-FINITO:{rid}")
    return valor


def _contrato_padre(contrato: dict) -> dict:
    padre = (contrato.get("parametros") or {}).get("padre") or {}
    ids = [padre.get(k, "") for k in ("p_id", "ic_lo_id", "ic_hi_id")]
    if padre.get("unidad") != "persona" or padre.get("poblacion") != "U4":
        raise RuntimeError("PADRE-NO-ESTIMABLE-UNIDAD-O-POBLACION-NO-U4-PERSONA")
    if any("U1" in rid or not rid.endswith("-U4") for rid in ids):
        raise RuntimeError("PADRE-NO-ESTIMABLE-REFERENCIA-U1-O-NO-U4")
    return padre


def medir(inputs: dict, contrato: dict) -> dict:
    padre = _contrato_padre(contrato)
    valores = _verifica_cadena_sellada(inputs)

    veredicto_padre = valores.get(padre["veredicto_id"])
    if veredicto_padre != "TASA-REPORTADA":
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-VEREDICTO:{veredicto_padre!r}")

    p = _numero(valores, padre["p_id"])
    lo = _numero(valores, padre["ic_lo_id"])
    hi = _numero(valores, padre["ic_hi_id"])
    masa = _numero(valores, padre["masa_id"])
    n_raw = valores.get(padre["n_id"])
    if isinstance(n_raw, bool) or not isinstance(n_raw, int) or n_raw <= 0:
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-DENOMINADOR:{n_raw!r}")
    if not (0.0 <= lo <= p <= hi <= 1.0):
        raise RuntimeError(
            f"PADRE-NO-ESTIMABLE-LIMITES-INVERTIDOS-O-FUERA-DE-ESCALA: "
            f"lo={lo!r} p={p!r} hi={hi!r}"
        )
    if masa <= 0:
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-MASA:{masa!r}")

    metodo = valores.get(padre["metodo_ic_id"])
    if not isinstance(metodo, str) or metodo.startswith("NO-ESTIMABLE"):
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-METODO-IC:{metodo!r}")

    q = 1.0 - p
    q_lo = 1.0 - hi
    q_hi = 1.0 - lo
    suma = p + q
    legado = float((contrato.get("parametros") or {})["valor_legacy_res0028"])
    delta = q - legado
    tolerancia = float((contrato.get("parametros") or {})["tolerancia_legacy"])

    return {
        PREFIX + "P-PADRE-C2-U4": p,
        PREFIX + "Q-C2-U4": q,
        PREFIX + "IC-LO-Q-C2-U4": q_lo,
        PREFIX + "IC-HI-Q-C2-U4": q_hi,
        PREFIX + "SUMA-P-Q-C2-U4": suma,
        PREFIX + "N-PERSONAS-U4": n_raw,
        PREFIX + "MASA-FAC-ELE-U4": masa,
        PREFIX + "METODO-IC-HEREDADO": metodo,
        PREFIX + "DELTA-VS-LEGACY-RES0028": delta,
        PREFIX + "COMPATIBILIDAD-RES0028": (
            "COINCIDE-AL-GRANO-U4" if abs(delta) <= tolerancia
            else "NO-COINCIDE-AL-GRANO-U4"
        ),
        PREFIX + "VEREDICTO":
            "DERIVADO-DE-PADRE-SELLADO-SIN-INFORMACION-MUESTRAL-INDEPENDIENTE",
    }
