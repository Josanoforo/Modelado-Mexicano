"""Complementos q=1-p de un padre sellado único (clase iii-DERIVADO-DE-GEN2).

Interfaz del runner GEN2: ``medir(inputs, contrato) -> dict``. No abre
microdatos ni escribe archivos. Verifica los bytes de la cadena sellada del
padre antes de transformar cada punto y su intervalo.
"""
from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal


def _bytes(inputs: dict, iid: str) -> bytes:
    entrada = inputs[iid]
    crudo = entrada.get("bytes")
    if crudo is not None:
        return crudo
    with open(entrada["ruta_absoluta"], "rb") as fh:
        return fh.read()


def _sha(crudo: bytes) -> str:
    return hashlib.sha256(crudo).hexdigest()


def _verifica_cadena_sellada(inputs: dict, padre: dict) -> dict:
    ids = padre["inputs"]
    resultados_b = _bytes(inputs, ids["resultados"])
    spec_b = _bytes(inputs, ids["spec"])
    sello_b = _bytes(inputs, ids["sello"])
    sidecar_b = _bytes(inputs, ids["sello_sha256"])
    try:
        sello = json.loads(sello_b.decode("utf-8"))
        sidecar = sidecar_b.decode("utf-8").split()[0]
        resultados = json.loads(resultados_b.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, IndexError) as exc:
        raise RuntimeError(f"PADRE-NO-ESTIMABLE-CADENA-ILEGIBLE: {exc}") from exc
    if sidecar != _sha(sello_b):
        raise RuntimeError("PADRE-NO-ESTIMABLE-SELLO-SIDECAR-NO-COINCIDE")
    for nombre, real in (("resultados.json", _sha(resultados_b)),
                         ("spec.yaml", _sha(spec_b))):
        if sello.get(nombre) != real:
            raise RuntimeError(
                f"PADRE-NO-ESTIMABLE-SELLO-NO-CUBRE-{nombre}: "
                f"declarado={sello.get(nombre)!r} real={real}")
    if resultados.get("spec_id") != padre["calc_id"]:
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


def _complemento(valor: float) -> float:
    """Resta decimal sobre la representación publicada en JSON."""
    return float(Decimal("1") - Decimal(str(valor)))


def medir(inputs: dict, contrato: dict) -> dict:
    parametros = contrato.get("parametros") or {}
    padre = parametros["padre"]
    valores = _verifica_cadena_sellada(inputs, padre)
    tolerancia = float(parametros["tolerancia_legacy"])
    salida: dict = {}
    for par in parametros["complementos"]:
        pre = par["prefijo"]
        veredicto = valores.get(par["veredicto_id"])
        if veredicto != "TASA-REPORTADA":
            raise RuntimeError(f"PADRE-NO-ESTIMABLE-VEREDICTO:{pre}:{veredicto!r}")
        metodo = valores.get(par["metodo_ic_id"])
        if not isinstance(metodo, str) or metodo.startswith("NO-ESTIMABLE"):
            raise RuntimeError(f"PADRE-NO-ESTIMABLE-METODO-IC:{pre}:{metodo!r}")
        p = _numero(valores, par["p_id"])
        lo = _numero(valores, par["ic_lo_id"])
        hi = _numero(valores, par["ic_hi_id"])
        if not (0.0 <= lo <= p <= hi <= 1.0):
            raise RuntimeError(
                f"PADRE-NO-ESTIMABLE-LIMITES-INVERTIDOS-O-FUERA-DE-ESCALA:{pre}: "
                f"lo={lo!r} p={p!r} hi={hi!r}")
        q = _complemento(p)
        legado_raw = par["valor_legacy"]
        delta = float(Decimal(str(q)) - Decimal(str(legado_raw)))
        salida.update({
            pre + "P-PADRE": p,
            pre + "Q": q,
            pre + "IC-LO-Q": _complemento(hi),
            pre + "IC-HI-Q": _complemento(lo),
            pre + "SUMA-P-Q": p + q,
            pre + "METODO-IC-HEREDADO": metodo,
            pre + "DELTA-VS-LEGACY": delta,
            pre + "COMPATIBILIDAD-LEGACY": (
                "COINCIDE-AL-GRANO" if abs(delta) <= tolerancia
                else "NO-COINCIDE-AL-GRANO"),
        })
    salida[parametros["veredicto_id"]] = (
        "DERIVADO-DE-PADRE-SELLADO-SIN-INFORMACION-MUESTRAL-INDEPENDIENTE")
    return salida
