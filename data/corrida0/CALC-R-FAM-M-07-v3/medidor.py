"""Medidor R GEN2 para una celda del marco de 14.

La identidad sustantiva sale exclusivamente de codificacion-R-v1_2.tsv,
sucesora vigente que conserva el estimando y separa la reserva inferencial de DIN-M-01. No abre corridas-L, corridas-M,
CALC TRIADA ni los JSON R legados. El control positivo ocurre fuera de este
medidor y despues del sello.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[3]
CODIFICACION = RAIZ / "forense/prereg-duelo-v2/codificacion-R-v1_2.tsv"


def _carga_arbitra():
    spec = importlib.util.spec_from_file_location(
        "arbitra_r_marco", RAIZ / "tools/arbitra.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _masa_de_llamada(filas, col_y, uno, cero, col_w, filtro, codifica, num):
    masa = 0.0
    for f in filas:
        if filtro and not filtro(f):
            continue
        if codifica is None:
            v = str(f.get(col_y, "")).strip()
            if v not in uno and v not in cero:
                continue
        elif codifica(f) is None:
            continue
        w = num(f.get(col_w))
        if w is not None and w > 0:
            masa += w
    return masa


def medir(inputs, contrato):
    celda = str(contrato["parametros"]["id_celda"])
    prefijo = f"RESULT-R-{celda}-"
    arbitra = _carga_arbitra()
    corredor = arbitra._correr_r()
    tabla = arbitra.lee_codificacion(str(CODIFICACION))
    manifiesto = arbitra.carga_manifiesto()

    # Instrumenta la misma llamada del corredor para obtener la masa sin
    # cambiar estima(): materializa exactamente las filas que el corredor ya
    # iba a consumir, lo ejecuta, y suma el mismo ponderador sobre las mismas
    # inclusiones. La aritmetica del punto/EE permanece en correr-R.py.
    original = corredor.estima
    trazas = []

    def estima_con_masa(filas, col_y, uno, cero, col_w, col_est, col_upm,
                        filtro=None, codifica=None):
        material = list(filas)
        res, conteos = original(iter(material), col_y, uno, cero, col_w,
                                col_est, col_upm, filtro=filtro,
                                codifica=codifica)
        trazas.append(_masa_de_llamada(material, col_y, uno, cero, col_w,
                                       filtro, codifica, corredor.num))
        return res, conteos

    corredor.estima = estima_con_masa
    calculo, motivo, _advertencias = arbitra.calcula_desde_tabla(
        celda, tabla, manifiesto, corredor)

    sufijos = [
        "PUNTO", "EE", "IC-LO", "IC-HI", "N", "MASA-PONDERADA",
        "N-FILAS-TABLA", "N-FALTANTES-EXCLUIDOS", "N-CODIGO-EXCLUIDO",
        "N-FUERA-UNIVERSO", "N-SIN-PONDERADOR", "N-ESTRATOS", "N-UPM",
        "N-ESTRATOS-UPM-UNICA", "METODO-IC", "ESTADO",
    ]
    if calculo is None:
        out = {prefijo + s: None for s in sufijos}
        out[prefijo + "METODO-IC"] = "NO-ESTIMABLE"
        out[prefijo + "ESTADO"] = "ABSTENCION: " + str(motivo)
        return out

    r, c, fila = calculo
    if r is None:
        out = {prefijo + s: None for s in sufijos}
        out[prefijo + "METODO-IC"] = "NO-ESTIMABLE"
        out[prefijo + "ESTADO"] = "ABSTENCION: UNIVERSO-VACIO"
        return out

    extra = fila.get("_extra") or {}
    if extra.get("diseno") == "DISENO-APROXIMADO":
        metodo = "IC-DISENO-APROXIMADO-COTA-INFERIOR"
    elif r["n_estratos_singleton"]:
        metodo = "IC-CON-ESTRATOS-DE-UPM-UNICA"
    else:
        metodo = "IC-ULTIMATE-CLUSTER"
    excl = (int(c["n_fuera_de_universo"]) + int(c["n_codigo_no_valido"])
            + int(c["n_sin_ponderador"]))
    return {
        prefijo + "PUNTO": float(r["p_hat"]),
        prefijo + "EE": float(r["se"]),
        prefijo + "IC-LO": float(r["ic95"][0]),
        prefijo + "IC-HI": float(r["ic95"][1]),
        prefijo + "N": int(c["n_efectivo"]),
        prefijo + "MASA-PONDERADA": float(trazas[0]),
        prefijo + "N-FILAS-TABLA": int(c["n_filas_leidas"]),
        prefijo + "N-FALTANTES-EXCLUIDOS": excl,
        prefijo + "N-CODIGO-EXCLUIDO": int(c["n_codigo_no_valido"]),
        prefijo + "N-FUERA-UNIVERSO": int(c["n_fuera_de_universo"]),
        prefijo + "N-SIN-PONDERADOR": int(c["n_sin_ponderador"]),
        prefijo + "N-ESTRATOS": int(r["n_estratos"]),
        prefijo + "N-UPM": int(r["n_upm_total"]),
        prefijo + "N-ESTRATOS-UPM-UNICA": int(r["n_estratos_singleton"]),
        prefijo + "METODO-IC": metodo,
        prefijo + "ESTADO": "CALCULADO",
    }
