#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_cierre_acto.py -- prueba mínima de `tools/cierre_acto.py`
(ACTO AUTOMATIZA-1-E3 · CIERRE-MECANICO, 7/sep/2026; tercer contador --
la fila `gobernanza` de la tabla de nombres estables -- añadido por
`ACTO AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR`, 7/sep/2026).

P-B (`ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`, 21/sep/2026): los TRES
contadores mecánicos quedaron HISTÓRICOS -- `--aplica` DEJÓ DE
ESCRIBIRLOS. Los casos B/C/G/F de antes (que probaban la reconciliación
todo-o-nada de las tres cifras) se reemplazan por los que prueban que
`--aplica` YA NO las toca, pase lo que pase en sus anclas; `inspeccion_gobernanza`
(la lectura de Fase A) sigue viva sin cambios -- sigue siendo la que
reporta las anclas rotas/duplicadas a un humano, sólo dejó de gatear una
escritura.

Casos: (A) dry-run sigue reportando las TRES cifras (cabecera/L0/tabla)
3 vs 4 real, sin escribir nada -- es sólo lectura. (B) `--aplica` NO
escribe ninguno de los tres archivos de gobierno, aunque estén
desreconciliados -- sólo corre la cola y reporta el real por
`EC.adr_max`. (C/G) `inspeccion_gobernanza` sigue detectando ancla L0 y
de tabla rotas/duplicadas para un humano, aun cuando `--aplica` ya no usa
eso para decidir si escribe. (D) segunda corrida es igual de inerte que
la primera -- no hay estado que reconciliar. (E) rótulo ausente se
reporta sin escribir `registro-rotulos.tsv`. (H) unicidad de L0 con
duplicado/ausente/cita histórica -- sigue viva, es lectura pura.

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


def _fixture(tmp, adr_reales, cabecera_declara, l0_declara, tabla_declara=None):
    """Construye un mini-árbol con canon/gobernanza-v1_15.md (N ADR reales,
    cabecera declarando `cabecera_declara`) y canon/estado-programa-v1_17.md
    (L0 declarando `l0_declara`, tabla de nombres estables declarando
    `tabla_declara` -- default: igual a `l0_declara`, para no tener que
    tocar cada llamada existente). Sin git real -- cierre_acto sólo
    necesita los archivos de canon/ para la reconciliación de conteos."""
    if tabla_declara is None:
        tabla_declara = l0_declara
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
        "# Estado del programa\n\n"
        "## 0 · Nomenclatura\n\n"
        "| Nombre estable | Archivo vigente | Qué es |\n"
        "|---|---|---|\n"
        "| **`modelo`** | `modelo-decision-v4.0.md` | CANÓNICO OPERATIVO |\n"
        f"| **`gobernanza`** | `gobernanza-v1.15.md` | {tabla_declara} ADR, protocolo de cambio |\n"
        "| **`estado`** | `estado-programa-v1.12.md` | Este archivo |\n\n"
        + "cabecera de estado\n\n" * 55 +  # empuja L0 más allá de la línea 1, no crítico
        f"**L0 · Gobierno — completo y al día.** {l0_declara} ADR *(`ADR-{l0_declara}` (anotación previa) · texto)*\n"
    )
    with open(os.path.join(canon, "estado-programa-v1_17.md"), "w", encoding="utf-8") as f:
        f.write(estado)

    return tmp


def prueba_a_dry_run_reconcilia():
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3, tabla_declara=3)
        gob = CA.inspeccion_gobernanza(CA.EC.adr_max(tmp), raiz=tmp)
        afirma(gob["adr_real"] == 4, gob)
        afirma(gob["cabecera_declara"] == 3, gob)
        afirma(gob["l0_declara"] == 3, gob)
        afirma(gob["tabla_declara"] == 3, gob)
        afirma(gob["cabecera_anclas"] == 1 and gob["l0_anclas"] == 1 and gob["tabla_anclas"] == 1, gob)


def prueba_b_aplica_ya_no_escribe_los_tres():
    """P-B: `--aplica` deja de reconciliar cabecera/L0/tabla -- aunque estén
    desreconciliadas (3 declarado, 4 real), ninguno de los dos archivos de
    gobierno se toca. El criterio de "hecho" 4 del encargo: verificable con
    `git status` tras correrlo -- aquí, con una comparación byte a byte."""
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3, tabla_declara=3)
        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(CA._ruta_estado(tmp))

        import io
        import contextlib
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = CA.fase_b_aplica(raiz=tmp)
        afirma(codigo == 0, f"--aplica debe salir 0, salió {codigo}")

        gob_despues = CA._leer(CA._ruta_gobernanza(tmp))
        est_despues = CA._leer(CA._ruta_estado(tmp))
        afirma(gob_despues == gob_antes,
               "P-B: gobernanza no debe cambiar -- el contador quedó HISTÓRICO")
        afirma(est_despues == est_antes,
               "P-B: estado-programa (L0 y tabla) no debe cambiar -- quedaron HISTÓRICOS")
        afirma("HISTÓRICOS" in salida.getvalue(),
               f"el mensaje debe declarar que los contadores son históricos: {salida.getvalue()!r}")

        # Ningún temporal huérfano: --aplica no preparó ningún rename sobre
        # estos dos archivos.
        sobrantes = [n for n in os.listdir(os.path.join(tmp, "canon")) if n.endswith(".tmp")]
        afirma(sobrantes == [], f"no deben quedar temporales tras --aplica: {sobrantes}")


def prueba_c_ancla_l0_rota_sigue_siendo_lectura():
    """`inspeccion_gobernanza` (Fase A, sólo lectura) sigue detectando el
    ancla L0 rota para un humano; `--aplica` (Fase B) ya no la usa para
    decidir si escribe -- P-B la volvió irrelevante para la escritura, no
    para el reporte."""
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3)
        ruta_est = CA._ruta_estado(tmp)
        contenido = CA._leer(ruta_est)
        with open(ruta_est, "w", encoding="utf-8") as f:
            f.write(contenido + "\n" + contenido)

        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(ruta_est)

        rep = CA.inspeccion_gobernanza(CA.EC.adr_max(tmp), raiz=tmp)
        afirma(rep["l0_anclas"] == 2 and rep["l0_declara"] is None,
               f"Fase A debe seguir viendo el ancla L0 duplicada: {rep}")

        codigo = CA.fase_b_aplica(raiz=tmp)
        afirma(codigo == 0, f"--aplica ya no aborta por esto, sale 0, fue {codigo}")
        afirma(CA._leer(CA._ruta_gobernanza(tmp)) == gob_antes,
               "gobernanza no debe cambiar -- --aplica no la toca")
        afirma(CA._leer(ruta_est) == est_antes,
               "estado-programa no debe cambiar, ni siquiera con el ancla rota")


def prueba_g_ancla_tabla_rota_sigue_siendo_lectura():
    """Misma idea que prueba_c pero con la fila de tabla duplicada."""
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3, tabla_declara=3)
        ruta_est = CA._ruta_estado(tmp)
        contenido = CA._leer(ruta_est)
        fila_tabla = "| **`gobernanza`** | `gobernanza-v1.15.md` | 3 ADR, protocolo de cambio |\n"
        afirma(contenido.count(fila_tabla) == 1, "precondición: la fila aparece una sola vez")
        contenido_roto = contenido + "\n" + fila_tabla
        with open(ruta_est, "w", encoding="utf-8") as f:
            f.write(contenido_roto)

        est_antes = CA._leer(ruta_est)
        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))

        rep = CA.inspeccion_gobernanza(CA.EC.adr_max(tmp), raiz=tmp)
        afirma(rep["tabla_anclas"] == 2 and rep["tabla_declara"] is None,
               f"Fase A debe seguir viendo la fila de tabla duplicada: {rep}")

        codigo = CA.fase_b_aplica(raiz=tmp)
        afirma(codigo == 0, f"--aplica ya no aborta por esto, sale 0, fue {codigo}")
        afirma(CA._leer(CA._ruta_gobernanza(tmp)) == gob_antes,
               "gobernanza no debe cambiar")
        afirma(CA._leer(ruta_est) == est_antes,
               "estado-programa no debe cambiar, ni siquiera con la fila de tabla rota")


def prueba_h_unicidad_l0_uno_duplicado_ausente_y_cita_historica():
    """NC-0148: la regla compartida distingue 1/2/0 anclas aun cuando el
    duplicado declara la misma cifra. Una cita literal fuera del canónico es
    historia, no otra ancla viva."""
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=4, l0_declara=4)
        forense = os.path.join(tmp, "forense", "encargos")
        os.makedirs(forense, exist_ok=True)
        with open(os.path.join(forense, "historico.md"), "w", encoding="utf-8") as f:
            f.write("Cita histórica literal: **L0 · Gobierno — completo y al día.** 4 ADR\n")

        uno = CA.inspeccion_gobernanza(4, raiz=tmp)
        afirma(uno["l0_anclas"] == 1,
               f"una cita histórica fuera del canónico produjo falso fallo: {uno}")

        ruta_est = CA._ruta_estado(tmp)
        original = CA._leer(ruta_est)
        ancla = CA.L0_ADR_RE.search(original)
        afirma(ancla is not None, "precondición: falta el ancla L0 del fixture")
        if ancla is None:
            return
        with open(ruta_est, "w", encoding="utf-8") as f:
            f.write(original + "\n" + ancla.group(0) + " *(duplicado con igual cifra)*\n")
        duplicado = CA.inspeccion_gobernanza(4, raiz=tmp)
        afirma(duplicado["l0_anclas"] == 2 and duplicado["l0_declara"] is None,
               f"el duplicado con cifra coincidente no fue detectado: {duplicado}")

        with open(ruta_est, "w", encoding="utf-8") as f:
            f.write(CA.L0_ADR_RE.sub("L0 ausente", original))
        ausente = CA.inspeccion_gobernanza(4, raiz=tmp)
        afirma(ausente["l0_anclas"] == 0 and ausente["l0_declara"] is None,
               f"el ancla ausente no fue detectada: {ausente}")


def prueba_d_segunda_corrida_igual_de_inerte():
    """Ya no hay estado de conteo que reconciliar -- correr dos veces
    seguidas es igual de inerte la primera vez que la segunda."""
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=4, l0_declara=4)
        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(CA._ruta_estado(tmp))

        for _ in range(2):
            import io
            import contextlib
            salida = io.StringIO()
            with contextlib.redirect_stdout(salida):
                codigo = CA.fase_b_aplica(raiz=tmp)
            afirma(codigo == 0, codigo)
            afirma("sin cambios" in salida.getvalue(), salida.getvalue())
            afirma(CA._leer(CA._ruta_gobernanza(tmp)) == gob_antes, "no debe reescribir nunca")
            afirma(CA._leer(CA._ruta_estado(tmp)) == est_antes, "no debe reescribir nunca")


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
    prueba_b_aplica_ya_no_escribe_los_tres()
    prueba_c_ancla_l0_rota_sigue_siendo_lectura()
    prueba_g_ancla_tabla_rota_sigue_siendo_lectura()
    prueba_h_unicidad_l0_uno_duplicado_ausente_y_cita_historica()
    prueba_d_segunda_corrida_igual_de_inerte()
    prueba_e_rotulo_ausente_no_escribe_registro()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_cierre_acto.py: 7 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
