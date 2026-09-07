#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_cierre_acto.py -- prueba mínima de `tools/cierre_acto.py`
(ACTO AUTOMATIZA-1-E3 · CIERRE-MECANICO, 7/sep/2026).

Cinco casos, todos sobre un fixture mínimo en `tempfile.TemporaryDirectory`
(nunca sobre el árbol real): (A) dry-run reconcilia 3→4, (B) `--aplica`
escribe sólo los dígitos previstos, (C) ancla L0 rota aborta todo-o-nada,
(D) segunda corrida ya reconciliada no cambia nada, (E) rótulo ausente se
reporta sin escribir `registro-rotulos.tsv`.

Corre sola:
    python3 tests/test_cierre_acto.py
"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import cierre_acto as CA  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def _fixture(tmp, adr_reales, cabecera_declara, l0_declara):
    """Construye un mini-árbol con canon/gobernanza-v1_15.md (N ADR reales,
    cabecera declarando `cabecera_declara`) y canon/estado-programa-v1_12.md
    (L0 declarando `l0_declara`). Sin git real -- cierre_acto sólo necesita
    los archivos de canon/ para la reconciliación de conteos."""
    canon = os.path.join(tmp, "canon")
    os.makedirs(canon, exist_ok=True)

    entradas_adr = "\n\n".join(
        f"**ADR-{n} (texto) · ACTO X**, 7/sep/2026, texto de la entrada."
        for n in range(1, adr_reales + 1)
    )
    gobernanza = (
        f"# Gobernanza\n"
        f"### `gobernanza` · **v1.15** · 30 de julio de 2026 · **{cabecera_declara} ADR**\n\n"
        f"{entradas_adr}\n"
    )
    with open(os.path.join(canon, "gobernanza-v1_15.md"), "w", encoding="utf-8") as f:
        f.write(gobernanza)

    estado = (
        "cabecera de estado\n\n" * 55 +  # empuja L0 más allá de la línea 1, no crítico
        f"**L0 · Gobierno — completo y al día.** {l0_declara} ADR *(`ADR-{l0_declara}` (anotación previa) · texto)*\n"
    )
    with open(os.path.join(canon, "estado-programa-v1_12.md"), "w", encoding="utf-8") as f:
        f.write(estado)

    return tmp


def prueba_a_dry_run_reconcilia():
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3)
        gob = CA.inspeccion_gobernanza(CA.EC.adr_max(tmp), raiz=tmp)
        afirma(gob["adr_real"] == 4, gob)
        afirma(gob["cabecera_declara"] == 3, gob)
        afirma(gob["l0_declara"] == 3, gob)
        afirma(gob["cabecera_anclas"] == 1 and gob["l0_anclas"] == 1, gob)


def prueba_b_aplica_actualiza_ambos():
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3)
        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(CA._ruta_estado(tmp))

        codigo = CA.fase_b_aplica(raiz=tmp)
        afirma(codigo == 0, f"--aplica debe salir 0, salió {codigo}")

        gob_despues = CA._leer(CA._ruta_gobernanza(tmp))
        est_despues = CA._leer(CA._ruta_estado(tmp))

        afirma("**4 ADR**" in gob_despues, "cabecera debe declarar 4 tras aplicar")
        afirma("**3 ADR**" not in gob_despues, "cabecera no debe seguir declarando 3")
        afirma("día.** 4 ADR" in est_despues, "L0 debe declarar 4 tras aplicar")

        # Sólo los dígitos previstos cambiaron -- todo lo demás es idéntico.
        afirma(CA._solo_digitos_cambiaron(gob_antes, gob_despues, CA.CABECERA_ADR_RE),
               "el cambio en gobernanza debe limitarse a los dígitos del conteo")
        afirma(CA._solo_digitos_cambiaron(est_antes, est_despues, CA.L0_ADR_RE),
               "el cambio en L0 debe limitarse a los dígitos del conteo")
        # La anotación previa de L0 (ajena al conteo) no se toca.
        afirma("(anotación previa)" in est_despues, "la anotación existente de L0 no debe alterarse")


def prueba_c_ancla_rota_aborta_todo_o_nada():
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3)
        # Rompe el ancla de L0 (dos ocurrencias en vez de una).
        ruta_est = CA._ruta_estado(tmp)
        contenido = CA._leer(ruta_est)
        with open(ruta_est, "w", encoding="utf-8") as f:
            f.write(contenido + "\n" + contenido)

        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(ruta_est)

        import io
        import contextlib
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = CA.fase_b_aplica(raiz=tmp)

        afirma(codigo == 1, f"ancla rota debe abortar con código 1, fue {codigo}")
        afirma("APLICACION_ABORTADA" in salida.getvalue(), salida.getvalue())
        afirma("0 archivos escritos" in salida.getvalue(), salida.getvalue())
        afirma(CA._leer(CA._ruta_gobernanza(tmp)) == gob_antes,
               "gobernanza no debe cambiar cuando L0 aborta -- todo o nada")
        afirma(CA._leer(ruta_est) == est_antes,
               "L0 no debe cambiar cuando su propia ancla está rota")


def prueba_d_ya_reconciliado_no_cambia():
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=4, l0_declara=4)
        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(CA._ruta_estado(tmp))

        import io
        import contextlib
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = CA.fase_b_aplica(raiz=tmp)

        afirma(codigo == 0, codigo)
        afirma("sin cambios" in salida.getvalue(), salida.getvalue())
        afirma(CA._leer(CA._ruta_gobernanza(tmp)) == gob_antes, "no debe reescribir si ya coincide")
        afirma(CA._leer(CA._ruta_estado(tmp)) == est_antes, "no debe reescribir si ya coincide")


def prueba_e_rotulo_ausente_no_escribe_registro():
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=4, l0_declara=4)
        ruta_registro = CA._ruta_registro_rotulos(tmp)
        afirma(not os.path.exists(ruta_registro), "precondición: no existe aún")

        info = CA.inspeccion_rotulo(raiz=tmp)
        afirma(info["ya_censado"] is False, info)

        afirma(not os.path.exists(ruta_registro),
               "inspeccion_rotulo() es de sólo lectura -- nunca debe crear registro-rotulos.tsv")


def main():
    prueba_a_dry_run_reconcilia()
    prueba_b_aplica_actualiza_ambos()
    prueba_c_ancla_rota_aborta_todo_o_nada()
    prueba_d_ya_reconciliado_no_cambia()
    prueba_e_rotulo_ausente_no_escribe_registro()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_cierre_acto.py: 5 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
