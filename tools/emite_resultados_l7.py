#!/usr/bin/env python3
"""ACTO MAESTRA35-L7 · corre los cuatro medidores congelados y emite
`data/l7-resultados-v1_0.json` -- la salida cruda de COMMIT-2, para no
transcribir a mano los números que van a `milpa/tramite-ola5-propuesta-v0.yaml`.
No recalcula nada: importa y llama a `main()` de cada medidor ya congelado.
"""
import io
import json
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def celda_a_dict(c):
    return {k: v for k, v in c.items()}


def eje_a_dict(r):
    return {
        "eje": r["eje"], "cobertura": r["cobertura"],
        "veredicto": r["veredicto"], "monotonia": r["monotonia"],
        "signo": r["signo"], "nota": r["nota"],
        "celdas": [celda_a_dict(c) for c in r["celdas"]],
    }


def corre(modulo):
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod = __import__(modulo)
        salida = mod.main()
    return salida, buf.getvalue()


def main():
    resultado = {}

    salida_a, log_a = corre("medidor_denuncia_seguro_envipe25")
    resultado["pieza_a_civico_denuncia"] = {
        "eje": eje_a_dict(salida_a["eje"]),
        "universo_n": salida_a["universo_n"],
    }

    salida_b, log_b = corre("medidor_union_libre")
    resultado["pieza_b_familia_union"] = {
        "eder": eje_a_dict(salida_b["eder"]),
        "enadid": eje_a_dict(salida_b["enadid"]),
        "enadid_prevalencia_bruta": salida_b["enadid_prevalencia_bruta"],
    }

    salida_c, log_c = corre("medidor_cuidado_enut")
    resultado["pieza_c_familia_cuidado"] = {
        "d1_sexo_edad": eje_a_dict(salida_c["d1_sexo_edad"]),
        "d2_razon_todos_los_hogares": salida_c["d2_razon_todos"],
        "d2_razon_hogares_con_carga": salida_c["d2_razon_con_carga"],
    }

    salida_d, log_d = corre("medidor_horizonte_enif24")
    resultado["pieza_d_dinero_ahorro"] = {
        etiqueta: eje_a_dict(r) for etiqueta, r in salida_d.items()
    }

    ruta = os.path.join(RAIZ, "data", "l7-resultados-v1_0.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"Escrito: {ruta}")

    for etiqueta, log in [("a", log_a), ("b", log_b), ("c", log_c), ("d", log_d)]:
        ruta_log = os.path.join(RAIZ, "data", f"l7-log-pieza-{etiqueta}.txt")
        with open(ruta_log, "w", encoding="utf-8") as f:
            f.write(log)
        print(f"Escrito: {ruta_log}")

    return resultado


if __name__ == "__main__":
    main()
