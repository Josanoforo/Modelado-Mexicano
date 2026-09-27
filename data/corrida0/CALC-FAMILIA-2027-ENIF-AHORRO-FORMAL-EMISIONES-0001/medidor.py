"""Emisión congelada, sin R futura y sin retador."""
import json

def medir(inputs, contrato):
    if set(inputs) != {'CALC-ENIF-0001'}:
        raise PermissionError("input ajeno a piso")
    res = json.loads(inputs['CALC-ENIF-0001']["bytes"].decode())
    res = res.get("resultados", res)
    return {'RESULT-FAMILIA-ENIF-AHORRO-FORMAL-PISO-P': res['RESULT-ENIF-AHO-B-P-FORMAL-P']}
