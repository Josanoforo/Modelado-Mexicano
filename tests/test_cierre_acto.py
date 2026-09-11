#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_cierre_acto.py -- prueba mínima de `tools/cierre_acto.py`
(ACTO AUTOMATIZA-1-E3 · CIERRE-MECANICO, 7/sep/2026; tercer contador --
la fila `gobernanza` de la tabla de nombres estables -- añadido por
`ACTO AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR`, 7/sep/2026).

Todos los casos sobre un fixture mínimo en `tempfile.TemporaryDirectory`
(nunca sobre el árbol real): (A) dry-run reconcilia las TRES cifras
(cabecera/L0/tabla) 3→4, (B) `--aplica` escribe sólo los dígitos previstos
en las tres, (C) ancla L0 rota aborta todo-o-nada, (D) segunda corrida ya
reconciliada no cambia nada, (E) rótulo ausente se reporta sin escribir
`registro-rotulos.tsv`, (F) fallo del segundo `os.replace()` no miente
"0 archivos escritos", (G) ancla de tabla rota (duplicada) aborta
todo-o-nada igual que L0.

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
    cabecera declarando `cabecera_declara`) y canon/estado-programa-v1_12.md
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
    with open(os.path.join(canon, "estado-programa-v1_12.md"), "w", encoding="utf-8") as f:
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


def prueba_b_aplica_actualiza_los_tres():
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3, tabla_declara=3)
        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(CA._ruta_estado(tmp))

        codigo = CA.fase_b_aplica(raiz=tmp)
        afirma(codigo == 0, f"--aplica debe salir 0, salió {codigo}")

        gob_despues = CA._leer(CA._ruta_gobernanza(tmp))
        est_despues = CA._leer(CA._ruta_estado(tmp))

        afirma("**4 ADR**" in gob_despues, "cabecera debe declarar 4 tras aplicar")
        afirma("**3 ADR**" not in gob_despues, "cabecera no debe seguir declarando 3")
        afirma("día.** 4 ADR" in est_despues, "L0 debe declarar 4 tras aplicar")
        afirma("`gobernanza-v1.15.md` | 4 ADR, protocolo de cambio |" in est_despues,
               "tabla estado debe declarar 4 tras aplicar")
        afirma("`gobernanza-v1.15.md` | 3 ADR, protocolo de cambio |" not in est_despues,
               "tabla estado no debe seguir declarando 3")

        # Sólo los dígitos previstos cambiaron -- todo lo demás es idéntico.
        # `estado-programa` trae DOS anclas propias (L0 y tabla) en el mismo
        # archivo, así que `_solo_digitos_cambiaron` (pensada para un solo
        # patrón) no basta por sí sola para comparar antes/después de las
        # dos correcciones juntas: se neutralizan ambos dígitos en las dos
        # copias del texto y se compara lo que queda.
        afirma(CA._solo_digitos_cambiaron(gob_antes, gob_despues, CA.CABECERA_ADR_RE),
               "el cambio en gobernanza debe limitarse a los dígitos del conteo")
        est_antes_neutro = CA.L0_ADR_RE.sub(r"\g<1>N\g<3>", est_antes)
        est_antes_neutro = CA.TABLA_ADR_RE.sub(r"\g<1>N\g<3>", est_antes_neutro)
        est_despues_neutro = CA.L0_ADR_RE.sub(r"\g<1>N\g<3>", est_despues)
        est_despues_neutro = CA.TABLA_ADR_RE.sub(r"\g<1>N\g<3>", est_despues_neutro)
        afirma(est_antes_neutro == est_despues_neutro,
               "el cambio en estado-programa debe limitarse a los dígitos de L0 y de la tabla, nada más")
        # La anotación previa de L0 (ajena al conteo) no se toca.
        afirma("(anotación previa)" in est_despues, "la anotación existente de L0 no debe alterarse")
        # El resto de la tabla (otras filas) tampoco se toca.
        afirma("| **`modelo`** | `modelo-decision-v4.0.md` | CANÓNICO OPERATIVO |" in est_despues,
               "otras filas de la tabla no deben alterarse")

        # canon/estado-programa-v1_12.md se lee y se escribe UNA sola vez:
        # las dos correcciones (L0 y tabla) llegan en el mismo archivo, no
        # en dos escrituras independientes -- verificado indirectamente por
        # el hecho de que ambos cambios ya están presentes en un solo
        # _leer() posterior a una sola corrida de fase_b_aplica.

        # Escritura atómica (tempfile + os.replace): no debe quedar ningún
        # temporal huérfano en el directorio tras una corrida exitosa.
        sobrantes = [n for n in os.listdir(os.path.join(tmp, "canon")) if n.endswith(".tmp")]
        afirma(sobrantes == [], f"no deben quedar temporales tras --aplica: {sobrantes}")


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


def prueba_g_ancla_tabla_rota_aborta_todo_o_nada():
    """Misma forma que prueba_c pero rompiendo SÓLO el ancla de la tabla
    (fila `gobernanza` duplicada) dejando L0 intacta con una sola
    ocurrencia -- caso distinto: aquí es la tabla la que aborta, no L0."""
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3, tabla_declara=3)
        ruta_est = CA._ruta_estado(tmp)
        contenido = CA._leer(ruta_est)
        fila_tabla = "| **`gobernanza`** | `gobernanza-v1.15.md` | 3 ADR, protocolo de cambio |\n"
        afirma(contenido.count(fila_tabla) == 1, "precondición: la fila aparece una sola vez")
        # Duplica solo la fila de la tabla, en otro punto del archivo --
        # L0 sigue teniendo exactamente una ancla.
        contenido_roto = contenido + "\n" + fila_tabla
        with open(ruta_est, "w", encoding="utf-8") as f:
            f.write(contenido_roto)

        anclas_l0_precheck = list(CA.L0_ADR_RE.finditer(contenido_roto))
        afirma(len(anclas_l0_precheck) == 1, "precondición: L0 sigue teniendo una sola ancla")

        gob_antes = CA._leer(CA._ruta_gobernanza(tmp))
        est_antes = CA._leer(ruta_est)

        import io
        import contextlib
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = CA.fase_b_aplica(raiz=tmp)

        afirma(codigo == 1, f"ancla de tabla rota debe abortar con código 1, fue {codigo}")
        texto = salida.getvalue()
        afirma("APLICACION_ABORTADA" in texto, texto)
        afirma("0 archivos escritos" in texto, texto)
        afirma("tabla" in texto.lower(), f"el mensaje debe nombrar la tabla como causa: {texto!r}")
        afirma(CA._leer(CA._ruta_gobernanza(tmp)) == gob_antes,
               "gobernanza no debe cambiar cuando la tabla aborta -- todo o nada")
        afirma(CA._leer(ruta_est) == est_antes,
               "estado-programa no debe cambiar cuando su propia ancla de tabla está rota")


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


def prueba_f_fallo_de_confirmacion_no_miente():
    """Si el segundo `os.replace` falla DESPUÉS de que el primero ya
    confirmó, el mensaje de error no debe decir "0 archivos escritos" --
    eso sería falso. Simulado: el primer archivo objetivo (gobernanza, se
    procesa primero) se reemplaza con normalidad; el segundo (L0) falla."""
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, adr_reales=4, cabecera_declara=3, l0_declara=3)
        ruta_est = CA._ruta_estado(tmp)

        reemplazo_original = CA._confirma_temp
        llamadas = []

        def reemplazo_falso(ruta_tmp, ruta):
            llamadas.append(ruta)
            if ruta == ruta_est:
                raise OSError("simulado: falla el segundo rename")
            return reemplazo_original(ruta_tmp, ruta)

        CA._confirma_temp = reemplazo_falso
        import io
        import contextlib
        salida = io.StringIO()
        try:
            with contextlib.redirect_stdout(salida):
                codigo = CA.fase_b_aplica(raiz=tmp)
        finally:
            CA._confirma_temp = reemplazo_original

        afirma(codigo == 1, codigo)
        texto = salida.getvalue()
        afirma("0 archivos" not in texto,
               f"gobernanza SÍ se escribió antes de que L0 fallara -- el mensaje no debe decir '0 archivos': {texto!r}")
        afirma(CA._ruta_gobernanza(tmp) in llamadas and ruta_est in llamadas,
               "ambos renames deben haberse intentado")
        gob_despues = CA._leer(CA._ruta_gobernanza(tmp))
        afirma("**4 ADR**" in gob_despues,
               "gobernanza debe haber quedado escrita aunque L0 fallara despues")


def main():
    prueba_a_dry_run_reconcilia()
    prueba_b_aplica_actualiza_los_tres()
    prueba_c_ancla_rota_aborta_todo_o_nada()
    prueba_g_ancla_tabla_rota_aborta_todo_o_nada()
    prueba_h_unicidad_l0_uno_duplicado_ausente_y_cita_historica()
    prueba_d_ya_reconciliado_no_cambia()
    prueba_e_rotulo_ausente_no_escribe_registro()
    prueba_f_fallo_de_confirmacion_no_miente()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_cierre_acto.py: 8 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
