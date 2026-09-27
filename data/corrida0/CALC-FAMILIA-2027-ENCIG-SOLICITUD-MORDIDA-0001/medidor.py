"""Emisión del punto histórico fijo; no recibe ZIP ni R futura."""
import hashlib
import json


def medir(inputs, contrato):
    if set(inputs) != {"IN-ENCIG-PISOS"}:
        raise PermissionError("GUARDIA-INPUTS-EMISION")
    source = inputs["IN-ENCIG-PISOS"]
    data = source["bytes"]
    if hashlib.sha256(data).hexdigest() != source["sha256"]:
        raise PermissionError("PISO-HASH")
    floors = json.loads(data)
    par = contrato["parametros"]
    piso = floors["familias"][par["familia"]]
    if piso["result_id"] != par["result_origen"]:
        raise PermissionError("PISO-RESULT")
    return {par["result_emision"]: piso["p0"],
            par["result_emision"] + "-FUENTE": piso["result_id"],
            par["result_emision"] + "-ESTADO": "SELLADO-INTERNAMENTE-SIN-R-FUTURA"}
