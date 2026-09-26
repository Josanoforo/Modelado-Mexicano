"""Emisión congelada, sin R futura y sin retador."""
import json

def medir(inputs, contrato):
    if set(inputs) != {'CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1'}:
        raise PermissionError("input ajeno a piso")
    res = json.loads(inputs['CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1']["bytes"].decode())
    res = res.get("resultados", res)
    return {'RESULT-FAMILIA-ENIF-HORIZONTE-AHORRO-PISO-P': res['RESULT-HVD-A-AMBAS-VIAS']}
