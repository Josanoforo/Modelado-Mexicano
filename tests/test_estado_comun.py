#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_estado_comun.py -- prueba mínima de `tools/estado_comun.py`
(ACTO AUTOMATIZA-1-E2 · ESTADO-COMUN, 7/sep/2026).

Sin tests por métrica del tablero (eso variaría con el árbol real): esta
prueba fija fixtures mínimos y verifica las primitivas en aislamiento.

Corre sola:
    python3 tests/test_estado_comun.py
"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import estado_comun as EC  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_es_abierta_tabla():
    casos = [
        ("ABIERTA", True),
        ("ABIERTA -- pendiente", True),
        ("ABIERTA-RECIBO", False),
        ("FIRMADA", False),
        ("FIRMADA-POR-MERGE", False),
        ("", False),
    ]
    for estado, esperado in casos:
        afirma(EC.es_abierta(estado) is esperado,
               f"es_abierta({estado!r}) debería ser {esperado}, fue {EC.es_abierta(estado)!r}")


def prueba_lee_tablero_con_glosa():
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "forense"))
        ruta = os.path.join(tmp, "forense", "firmas-pendientes.tsv")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("id\tqué_se_firma\testado\n")
            f.write('FP-01\tuna glosa con "comillas" literales\tABIERTA -- pendiente de mesa\n')
            f.write("FP-02\tsin glosa\tFIRMADA\n")
        ruta_leida, filas, n_registros = EC.lee_tablero(tmp)
        afirma(ruta_leida == ruta, f"ruta esperada {ruta}, fue {ruta_leida}")
        afirma(n_registros == 2, f"2 REGISTROS lógicos (la cabecera no cuenta), fueron {n_registros}")
        afirma(len(filas) == 2, f"2 filas de dato, fueron {len(filas)}")
        afirma(filas[0]["id"] == "FP-01", filas[0])
        afirma('"comillas"' in filas[0]["qué_se_firma"],
               f"las comillas literales de la celda no deben perderse: {filas[0]!r}")
        afirma(EC.es_abierta(filas[0]["estado"]) is True, filas[0])
        afirma(EC.es_abierta(filas[1]["estado"]) is False, filas[1])


def prueba_lee_tablero_ausente():
    with tempfile.TemporaryDirectory() as tmp:
        ruta, filas, n_registros = EC.lee_tablero(tmp)
        afirma(filas is None, f"tablero ausente debe devolver filas=None, fue {filas!r}")
        afirma(n_registros == 0, n_registros)


def prueba_lee_tablero_salto_de_linea_incrustado():
    """H2 (hoja NC-DECISIONES-1, 28/sep/2026): caso sintético con el defecto
    real -- una firma verbatim con un salto de línea literal dentro de la
    celda, que una lectura por línea física partiría en dos."""
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "forense"))
        ruta = os.path.join(tmp, "forense", "firmas-pendientes.tsv")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("id\tqué_se_firma\testado\n")
            f.write('FP-01\t"firmado\npor mesa el 21/sep"\tFIRMADA\n')
            f.write("FP-02\tsin salto\tABIERTA\n")
        ruta_leida, filas, n_registros = EC.lee_tablero(tmp)
        afirma(n_registros == 2,
               f"el salto de línea incrustado no debe partir la fila en dos: "
               f"2 registros esperados, fueron {n_registros}")
        afirma(len(filas) == 2, f"2 filas de dato, fueron {len(filas)}")
        afirma(filas[0]["id"] == "FP-01", filas[0])
        afirma("\n" in filas[0]["qué_se_firma"],
               f"el salto de línea literal debe preservarse dentro de la celda: {filas[0]!r}")
        afirma(filas[1]["id"] == "FP-02", filas[1])
        afirma(EC.es_abierta(filas[1]["estado"]) is True, filas[1])


def prueba_adr_max():
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "canon"))
        ruta = os.path.join(tmp, "canon", "gobernanza-v1_15.md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("### `gobernanza` · **v1.15** · **5 ADR**\n\n")
            f.write("**ADR-3 (derivado...) · ACTO X**, texto.\n\n")
            f.write("**ADR-5 (derivado...) · ACTO Y**, texto.\n\n")
            f.write("**ADR-4 (derivado...) · ACTO Z**, texto.\n\n")
        afirma(EC.adr_max(tmp) == 5, f"máximo debe ser 5 (no el último en aparecer), fue {EC.adr_max(tmp)}")

    with tempfile.TemporaryDirectory() as tmp_vacio:
        afirma(EC.adr_max(tmp_vacio) == 0, "sin canon/gobernanza-v1_15.md, adr_max debe ser 0")


def prueba_adr_max_dos_epocas():
    """P-C.3 (`ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`, 21/sep/2026): una
    raíz de acto conviviendo con ADR numéricos no se lee como un ADR
    numérico fantasma (el defecto de backtracking: `260921-GEN2-…` se
    leía como `260921`, o retrocediendo, `26092`)."""
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "canon"))
        ruta = os.path.join(tmp, "canon", "gobernanza-v1_15.md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("### `gobernanza` · **v1.15** · **5 ADR**\n\n")
            f.write("**ADR-260921-GEN2-X-1-6e60-01** — entrada de raíz\n\n")
            f.write("**ADR-3 (derivado...) · ACTO X**, texto.\n\n")
            f.write("**ADR-5 (derivado...) · ACTO Y**, texto.\n\n")
            f.write("**ADR-4 (derivado...) · ACTO Z**, texto.\n\n")
        afirma(EC.adr_max(tmp) == 5,
               f"la raíz de acto no debe mover el máximo numérico, fue {EC.adr_max(tmp)}")


def prueba_adr_raiz_candidato():
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "canon"))
        import datetime
        hoy = datetime.date(2026, 9, 21)
        c1 = EC.adr_raiz_candidato(tmp, "GEN2-X-1", "27078f65c28459a", hoy=hoy)
        afirma(c1 == "ADR-260921-GEN2-X-1-2707-01", f"primer candidato inesperado: {c1}")

        ruta = os.path.join(tmp, "canon", "gobernanza-v1_15.md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(f"### `gobernanza` · **v1.15** · **1 ADR**\n\n**{c1}** — ya acuñada\n")
        c2 = EC.adr_raiz_candidato(tmp, "GEN2-X-1", "27078f65c28459a", hoy=hoy)
        afirma(c2 == "ADR-260921-GEN2-X-1-2707-02",
               f"segunda debe incrementar NN sobre el mismo prefijo, fue {c2}")

        import re as _re
        afirma(_re.fullmatch(EC.RE_ADR_NUEVA, c1) is not None,
               f"el candidato debe casar la gramática de raíz nueva: {c1}")


def prueba_fp_max():
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "forense"))
        ruta = os.path.join(tmp, "forense", "firmas-pendientes.tsv")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("id\tqué_se_firma\testado\n")
            f.write("FP-07\tx\tFIRMADA\n")
            f.write("FP-12\ty\tABIERTA\n")
            f.write("FP-09\tz\tABIERTA\n")
        afirma(EC.fp_max(tmp) == 12, f"máximo debe ser 12, fue {EC.fp_max(tmp)}")

    with tempfile.TemporaryDirectory() as tmp_vacio:
        afirma(EC.fp_max(tmp_vacio) == 0, "sin forense/firmas-pendientes.tsv, fp_max debe ser 0")


def prueba_ramas_remotas_presentes_respaldo():
    """Simula `git ls-remote` sin responder (rc != 0) para ejercitar la
    fuente de respaldo (`for-each-ref`) sin depender de la red ni del
    remoto real -- mismo patrón que `tests/test_t_cron.py`."""
    llamadas = []
    corre_original = EC._corre

    def corre_falso(cmd, raiz, timeout=60):
        llamadas.append(cmd[:2])
        if cmd[:2] == ["git", "ls-remote"]:
            return 1, ""
        if cmd[:2] == ["git", "for-each-ref"]:
            return 0, "origin/main\norigin/acto/x\norigin/HEAD\n"
        return corre_original(cmd, raiz, timeout)

    EC._corre = corre_falso
    try:
        ramas, fuente = EC.ramas_remotas_presentes(".")
    finally:
        EC._corre = corre_original

    afirma(ramas == ["acto/x", "main"], f"ramas esperadas ['acto/x', 'main'] (HEAD excluida), fueron {ramas}")
    afirma("for-each-ref" in fuente, f"la fuente debe declarar el respaldo usado: {fuente!r}")
    afirma(["git", "ls-remote"] in llamadas, "debió intentar ls-remote primero")


def main():
    prueba_es_abierta_tabla()
    prueba_lee_tablero_con_glosa()
    prueba_lee_tablero_ausente()
    prueba_lee_tablero_salto_de_linea_incrustado()
    prueba_adr_max()
    prueba_adr_max_dos_epocas()
    prueba_adr_raiz_candidato()
    prueba_fp_max()
    prueba_ramas_remotas_presentes_respaldo()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_estado_comun.py: 8 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
