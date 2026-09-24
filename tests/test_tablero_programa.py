#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_tablero_programa.py -- prueba mínima del bloque vivo committeado
de `tools/tablero_programa.py` (ACTO AUTOMATIZA-*, TABLERO-VIVO).

Usa un FIXTURE PEQUEÑO en `tempfile.TemporaryDirectory()` -- nunca el archivo
real de 90KB. Verifica, en aislamiento: idempotencia (dos pasadas de
--actualiza sobre el mismo archivo producen diff vacío en la segunda),
preservación byte a byte de todo lo que está fuera de los marcadores, y que
un ancla inválida (0 marcadores, o 2+ BEGIN) aborta sin escribir.

Corre sola:
    python3 tests/test_tablero_programa.py
"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import tablero_programa as TP  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def _indicadores_fixture():
    return {
        "sha": {"valor": "abc1234", "comando": "-", "nota": ""},
        "fecha_commit": {"valor": "2026-01-01", "comando": "-", "nota": ""},
        "es_origin_main": {"valor": True, "comando": "-", "nota": ""},
        "motor_reglas": {"valor": 1, "comando": "-", "nota": ""},
        "motor_reglas_con_dato": {"valor": 1, "comando": "-", "nota": ""},
        "motor_reglas_sin_dato": {"valor": [], "comando": "-", "nota": ""},
        "motor_conductas_medido": {"valor": 1, "comando": "-", "nota": ""},
        "motor_tiers": {"valor": {"FUERTE": 1}, "comando": "-", "nota": ""},
        "marco_v1_2_sorteado": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_con_M": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_con_R": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_con_L": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_puntuables_LMR": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_sin_LMR": {"valor": [], "comando": "-", "nota": ""},
        "manifiesto_ids": {"valor": 1, "comando": "-", "nota": ""},
        "registro_curador_filas": {"valor": 1, "comando": "-", "nota": ""},
        "relaciones_filas": {"valor": 1, "comando": "-", "nota": ""},
        "inventario_reactivos_v1_2": {"valor": 1, "comando": "-", "nota": ""},
        "adr_max": {"valor": 1, "comando": "-", "nota": ""},
        "fp_max": {"valor": 1, "comando": "-", "nota": ""},
        "fp_abiertas": {"valor": [{"id": "FP-1", "creado": "2026-01-01", "dias": 1, "que": "x"}], "comando": "-", "nota": ""},
        "encargos_archivados": {"valor": 1, "comando": "-", "nota": ""},
        "encargos_consumidos": {"valor": 1, "comando": "-", "nota": ""},
        "cola_encargos": {"valor": {"a.md": "LISTO"}, "comando": "-", "nota": ""},
    }


NARRATIVA_ANTES = "**Nota humana previa.** Texto de prosa que NO debe tocarse.\n\n"
NARRATIVA_DESPUES = "\n\n## Sección histórica\nMás prosa humana que tampoco debe tocarse.\n"


def _escribe_fixture(dirpath, cuerpo_bloque="<!-- placeholder -->"):
    ruta = os.path.join(dirpath, "TABLERO-FIXTURE.md")
    contenido = (
        NARRATIVA_ANTES
        + TP.MARCA_INICIO + "\n" + cuerpo_bloque + "\n" + TP.MARCA_FIN
        + NARRATIVA_DESPUES
    )
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


def prueba_idempotencia_y_preservacion():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = _escribe_fixture(d)
        antes = open(ruta, encoding="utf-8").read()

        rc1 = TP._actualiza_tablero(ruta, I)
        afirma(rc1 == 0, f"primera pasada debió retornar 0, retornó {rc1}")
        despues1 = open(ruta, encoding="utf-8").read()

        afirma(despues1.startswith(NARRATIVA_ANTES), "el texto antes del BEGIN debe preservarse byte a byte")
        afirma(despues1.endswith(NARRATIVA_DESPUES), "el texto después del END debe preservarse byte a byte")
        afirma(TP.MARCA_INICIO in despues1 and TP.MARCA_FIN in despues1, "los marcadores deben seguir presentes")
        afirma("abc1234" in despues1, "el bloque nuevo debe contener el SHA derivado")
        afirma(despues1 != antes, "la primera pasada debe cambiar el contenido (placeholder -> bloque real)")

        rc2 = TP._actualiza_tablero(ruta, I)
        afirma(rc2 == 0, f"segunda pasada debió retornar 0, retornó {rc2}")
        despues2 = open(ruta, encoding="utf-8").read()
        afirma(despues2 == despues1, "segunda pasada sobre el mismo dict de indicadores debe ser un no-op (idempotencia)")


def prueba_ancla_invalida_sin_marcadores():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "TABLERO-SIN-MARCAS.md")
        contenido = "Solo prosa, sin marcadores.\n"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        rc = TP._actualiza_tablero(ruta, I)
        afirma(rc != 0, "0 marcadores debe abortar con código != 0")
        despues = open(ruta, encoding="utf-8").read()
        afirma(despues == contenido, "0 marcadores no debe escribir nada")


def prueba_ancla_invalida_doble_begin():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "TABLERO-DOBLE.md")
        contenido = (
            NARRATIVA_ANTES
            + TP.MARCA_INICIO + "\nbloque 1\n" + TP.MARCA_FIN
            + "\n" + TP.MARCA_INICIO + "\nbloque 2\n" + TP.MARCA_FIN
            + NARRATIVA_DESPUES
        )
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        rc = TP._actualiza_tablero(ruta, I)
        afirma(rc != 0, "2+ BEGIN debe abortar con código != 0")
        despues = open(ruta, encoding="utf-8").read()
        afirma(despues == contenido, "2+ BEGIN no debe escribir nada")


def prueba_ancla_invalida_end_antes_de_begin():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "TABLERO-INVERTIDO.md")
        contenido = TP.MARCA_FIN + "\n" + TP.MARCA_INICIO + "\n"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        rc = TP._actualiza_tablero(ruta, I)
        afirma(rc != 0, "END antes de BEGIN debe abortar con código != 0")
        despues = open(ruta, encoding="utf-8").read()
        afirma(despues == contenido, "END antes de BEGIN no debe escribir nada")


def prueba_estado_cola_lee_cabecera_no_substring():
    """NC-0252: `_estado_cola` debe leer `ESTADO:` real, no colarse por un
    substring que la BITACORA solo *menciona* (p.ej. "seguía LISTO-CAJA con
    el PR ya fusionado" dentro de un renglón `ESTADO: CONSUMIDO`)."""
    afirma(TP._estado_cola("ESTADO: CONSUMIDO — PR #602. Sincronizado: "
                            "seguía LISTO-CAJA con el PR ya fusionado.\n") == "CONSUMIDO",
           "ESTADO: CONSUMIDO no debe leerse LISTO por mencionar LISTO-CAJA en la glosa")
    afirma(TP._estado_cola("ESTADO: CONSUMIDO — PR #600. Sincronizado: "
                            "seguía GATEADO con el PR ya fusionado.\n") == "CONSUMIDO",
           "ESTADO: CONSUMIDO no debe leerse GATED por mencionar GATEADO en la glosa")
    afirma(TP._estado_cola("ESTADO: LISTO-NUBE\n") == "LISTO", "LISTO-<ENTORNO> -> LISTO")
    afirma(TP._estado_cola("ESTADO: GATEADO\nCOMPUERTA: X\n") == "GATED", "GATEADO -> GATED")
    afirma(TP._estado_cola("ESTADO: EN-CURSO\n") == "GATED", "EN-CURSO no es ni CONSUMIDO ni LISTO")
    afirma(TP._estado_cola("ESTADO: PARO-REPORTADO\n") == "GATED", "PARO-REPORTADO -> GATED")
    # formato viejo, sin cabecera ESTADO: -- cae al heurístico por substring.
    afirma(TP._estado_cola("texto libre\n## CONSUMIDO · PR #1\n") == "CONSUMIDO",
           "sin cabecera ESTADO:, el heurístico viejo sigue vigente")
    afirma(TP._estado_cola("texto libre, LISTO-NUBE mencionado\n") == "LISTO",
           "sin cabecera ESTADO:, el heurístico viejo sigue vigente (LISTO-)")
    afirma(TP._estado_cola("texto libre sin marcas\n") == "GATED",
           "sin cabecera ESTADO: ni substrings conocidos -> GATED")


def prueba_estado_cola_contra_arbol_real():
    """Cruza `_estado_cola` contra la cabecera `ESTADO:` real de
    `forense/encargos/cola/` -- el desfase que NC-0252 midió (GEN2-E1/E2/E4
    con `ESTADO: CONSUMIDO` reportados LISTO/GATED) no puede volver a pasar
    silencioso."""
    base = os.path.join(ROOT, "forense", "encargos", "cola")
    if not os.path.isdir(base):
        return
    revisados = 0
    for dirpath, _, nombres in os.walk(base):
        for nombre in nombres:
            if not nombre.endswith(".md"):
                continue
            ruta = os.path.join(dirpath, nombre)
            texto = TP.leer(ruta)
            m = TP._ESTADO_CABECERA.search(texto)
            if not m:
                continue
            revisados += 1
            estado = m.group(1).rstrip(".,;:")
            calculado = TP._estado_cola(texto)
            if estado.startswith("CONSUMIDO"):
                afirma(calculado == "CONSUMIDO", f"{ruta}: ESTADO: {estado} debe leerse CONSUMIDO, leyó {calculado}")
            elif estado.startswith("LISTO"):
                afirma(calculado == "LISTO", f"{ruta}: ESTADO: {estado} debe leerse LISTO, leyó {calculado}")
    afirma(revisados > 0, "debe haber al menos un archivo con cabecera ESTADO: en forense/encargos/cola/")


def prueba_render_incluye_marcador_corridas_nc():
    """P1/P2/P5 (ACTO GEN2-TABLERO-SENAL-1): las líneas nuevas y el censo de
    NC por razón deben aparecer en el bloque renderizado, y el rótulo del
    Corredor debe llevar la corrección de P2. `ramas_remotas_detalle` dejó
    de rendirse aquí (P4, ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1: `git
    ls-remote`/`git fetch` en vivo hacían el bloque no determinista entre
    dos derivaciones sobre el mismo HEAD) -- sigue disponible en `--json`."""
    I = _indicadores_fixture()
    I["marcador_segmento"] = {"valor": {
        "total_filas": 3, "por_estado": {"IDENTICO": 2, "SOLO-PISO": 1},
        "emitida_sin_evaluar": "1 / 3", "cobertura_de_piso": "2 / 3",
        "valor_anadido_sobre_evaluadas": "0 / 1", "veto_pisos_activo": True,
    }, "comando": "-", "nota": ""}
    I["corridas_pendientes_de_contar"] = {"valor": {
        "selladas_total": 5, "por_cuenta_gen2": {"SI": 3, "PENDIENTE-DE-MESA": 2},
        "pendientes_de_mesa": [{"corrida_id": "CORR-X", "resultado_replay": "REPRODUCE"}],
    }, "comando": "-", "nota": ""}
    I["nc_por_razon"] = {"valor": {"abiertas": 4, "por_token": {"PARO-PREMISA": 1}, "prosa": 3}, "comando": "-", "nota": ""}
    I["instrucciones_vigentes"] = {"valor": "v2.14", "comando": "-", "nota": ""}
    bloque = TP.render_bloque_vivo(I)
    afirma("Marcador por segmento" in bloque, "debe traer la línea Marcador por segmento (P1)")
    afirma("2 / 3" in bloque, "debe mostrar cada número con su denominador (P1)")
    afirma("Corridas selladas que no cuentan todavía" in bloque, "debe traer la línea de corridas pendientes de contar (P1)")
    afirma("CORR-X" in bloque, "debe listar la corrida PENDIENTE-DE-MESA (P1)")
    afirma("Ramas presentes en origin" not in bloque,
           "ramas_remotas_detalle ya no se rinde en el bloque committeado (P4, no determinista)")
    afirma("Corredor LEGACY (eje x = ∅, GO-MARCADOR)" in bloque, "el rótulo Corredor debe llevar la corrección de P2")
    afirma("NC abiertas por razón" in bloque, "debe traer el censo de NC por razón (P5)")
    afirma("instrucciones vigentes `v2.14`" in bloque, "instrucciones_vigentes debe aparecer en el bloque vivo (P2)")


def prueba_render_cola_solo_estados_no_consumido():
    """P3: la cola de encargos del bloque renderizado lista solo estados
    != CONSUMIDO, y da el conteo aparte de los consumidos."""
    I = _indicadores_fixture()
    I["cola_encargos"] = {"valor": {"a.md": "CONSUMIDO", "b.md": "CONSUMIDO", "c.md": "GATED"}, "comando": "-", "nota": ""}
    bloque = TP.render_bloque_vivo(I)
    afirma("`c.md`: GATED" in bloque, "un estado != CONSUMIDO debe listarse")
    afirma("`a.md`: CONSUMIDO" not in bloque, "un estado CONSUMIDO no debe listarse por nombre")
    afirma("consumidos `2`" in bloque, "debe dar el conteo de consumidos")


def prueba_nc_por_razon_prefijo_exacto():
    """P5: el parser censa por PREFIJO EXACTO del token de A.14, no por
    corte de espacio/dos puntos (el defecto real que motivó la pieza)."""
    tok = next((t.rstrip(":") for t in TP._NC_TOKENS_A14 if "DIFERIDO-A:E7".startswith(t)), None)
    afirma(tok == "DIFERIDO-A", "DIFERIDO-A:E7 debe clasificar como token DIFERIDO-A")
    tok2 = next((t.rstrip(":") for t in TP._NC_TOKENS_A14 if "una nota en prosa sin token".startswith(t)), None)
    afirma(tok2 is None, "prosa sin token al inicio no debe clasificar en ningún token")


def prueba_celdas_d_adoptadas_activas_sintetica():
    """P5 (GEN2-TUBERIA-EFICIENCIA-1, trámite #981): una celda-D sintética
    con `champion_actual` NO vacío cuenta en `adoptados_activos`; una con
    `champion_actual: NINGUNO` o sin ese campo, no. Corre sobre un directorio
    temporal -- nunca toca `data/curacion-registro/celdas-d/` real (D-14/PARO d)."""
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "SIN.adoptar.yaml"), "w", encoding="utf-8") as fh:
            fh.write("celda_d:\n  id: SIN.adoptar\n  champion_actual: NINGUNO\n")
        with open(os.path.join(tmp, "ADOPTADA.sintetica.yaml"), "w", encoding="utf-8") as fh:
            fh.write("celda_d:\n  id: ADOPTADA.sintetica\n  champion_actual: C2\n")
        with open(os.path.join(tmp, "SIN.campo.yaml"), "w", encoding="utf-8") as fh:
            fh.write("celda_d:\n  id: SIN.campo\n")
        r = TP._celdas_d_adoptadas_activas(directorio=tmp)
    afirma(r["total_adoptadas_activas"] == 1,
           f"una sola celda-D sintética adoptada debe contar (obtuve {r['total_adoptadas_activas']})")
    afirma(r["detalle"][0]["celda_d"] == "ADOPTADA.sintetica",
           "el detalle debe citar la celda-D adoptada por id")
    afirma(set(r["celdas_d_sin_adoptar"]) == {"SIN.adoptar", "SIN.campo"},
           "NINGUNO y campo ausente deben quedar fuera del conteo, no silenciados")


def prueba_celdas_d_adoptadas_activas_universo_real():
    """Contra el árbol real: el universo examinado son los YAML que existen
    hoy en data/curacion-registro/celdas-d/, ni más ni menos (A.13)."""
    import glob as _glob
    n_real = len(_glob.glob(os.path.join(TP.RAIZ, "data", "curacion-registro", "celdas-d", "*.yaml")))
    r = TP._celdas_d_adoptadas_activas()
    afirma(f"{n_real} archivos" in r["universo_examinado"],
           f"universo_examinado debe declarar los {n_real} archivos reales examinados")
    afirma(any(d["celda_d"] == "GOB.gobierno_digital.encig2025.edad_x_escolaridad"
               for d in r["detalle"]),
           "la celda-D del piloto 3 (champion_actual: C2, firma F3) debe contar como adoptada activa")


def prueba_compara_head_origin_main():
    """P2 (ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1): puro, sin tocar git real --
    coincide, discrepa, y `origin/main` sin resolver es NO-RESUELTO, nunca
    una coincidencia por default (A.13)."""
    ok, motivo = TP._compara_head_origin_main("abc123", "abc123")
    afirma(ok and motivo == "", "HEAD == origin/main debe pasar sin motivo")
    ok, motivo = TP._compara_head_origin_main("abc123", "def456")
    afirma(not ok and "abc123" in motivo and "def456" in motivo,
           "HEAD != origin/main debe fallar citando los dos SHA")
    ok, motivo = TP._compara_head_origin_main("abc123", "")
    afirma(not ok and "no resoluble" in motivo,
           "origin/main vacío (ref no resuelto) debe fallar como NO-RESUELTO, no como coincidencia")


def prueba_render_rotula_no_es_origin_main():
    """P2: el rótulo NO-ES-ORIGIN-MAIN solo aparece cuando se pide
    explícitamente -- nunca por defecto, para no falsear un bloque normal."""
    I = _indicadores_fixture()
    normal = TP.render_bloque_vivo(I)
    afirma("NO-ES-ORIGIN-MAIN" not in normal, "un bloque normal no debe llevar el rótulo")
    fuera_de_main = TP.render_bloque_vivo(I, no_es_origin_main=True)
    afirma("NO-ES-ORIGIN-MAIN" in fuera_de_main, "--permitir-rama debe rotular el bloque")


def prueba_render_determinista():
    """ADENDA-1 P4: dos renders sobre los mismos indicadores = mismo bloque
    byte a byte (un derivado no determinista abre PR [deriva] infinitos)."""
    I = _indicadores_fixture()
    afirma(TP.render_bloque_vivo(I) == TP.render_bloque_vivo(I),
           "render_bloque_vivo debe ser determinista sobre el mismo árbol")


def prueba_sucios_ajenos():
    """ADENDA-1 P2: el árbol sucio niega, salvo los derivados que el canal
    mismo escribe antes del tablero (en CI ya están modificados)."""
    afirma(TP._sucios_ajenos("") == [], "árbol limpio no tiene sucios")
    afirma(TP._sucios_ajenos(" M data/corrida0/usos.tsv\nM  docs/tablero.md") == [],
           "los derivados del canal no cuentan como suciedad")
    afirma(TP._sucios_ajenos(" M data/corrida0/usos.tsv\n M tools/x.py") == ["tools/x.py"],
           "un archivo ajeno sí ensucia el árbol")


def prueba_gen2_rotula_en_arbol():
    """ADENDA-1 P5: la línea GEN2 dice que sus valores son EN ÁRBOL y qué vistas difieren de HEAD."""
    I = _indicadores_fixture()
    afirma("EN ÁRBOL" in TP.render_bloque_vivo(I), "la línea GEN2 rotula los valores en árbol")


# P4 (ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1): NO hay aquí una prueba que
# llame dos veces a `derivar_indicadores()` real. Se probó así durante el
# desarrollo de este acto -- medido: 123.1s UNA sola llamada -- y encontró
# el defecto real que motivó el fix de `prueba_render_rotula_no_es_origin_main`
# / la línea "Ramas presentes en origin" (ver la nota de cierre y el ADR
# para la evidencia cruda). Pero `tools/ci_guardias.py --censo` clasifica
# por EJECUCIÓN con un timeout de 40s (`ejecuta()`, default); dos pasadas
# reales (>240s) habrían marcado el ARCHIVO ENTERO `FALLA-DE-VERDAD
# (TIMEOUT>40s)` en el próximo censo, sacando las otras 13 pruebas de este
# archivo de `--ejecuta-huerfanos` en silencio -- el costo de la prueba le
# habría costado la cobertura a todas las demás. La guarda barata que
# queda en la suite (arriba: el rótulo NO-ES-ORIGIN-MAIN nunca por
# defecto, y abajo: "Ramas presentes en origin" ausente del bloque
# committeado) cubre la clase de defecto -- una fuente de dato que no es
# función del árbol filtrándose al bloque -- sin pagar el costo de la
# derivación completa en cada corrida de CI.


def main():
    prueba_idempotencia_y_preservacion()
    prueba_ancla_invalida_sin_marcadores()
    prueba_ancla_invalida_doble_begin()
    prueba_ancla_invalida_end_antes_de_begin()
    prueba_estado_cola_lee_cabecera_no_substring()
    prueba_estado_cola_contra_arbol_real()
    prueba_render_incluye_marcador_corridas_nc()
    prueba_render_cola_solo_estados_no_consumido()
    prueba_nc_por_razon_prefijo_exacto()
    prueba_celdas_d_adoptadas_activas_sintetica()
    prueba_celdas_d_adoptadas_activas_universo_real()
    prueba_compara_head_origin_main()
    prueba_render_rotula_no_es_origin_main()
    prueba_render_determinista()
    prueba_sucios_ajenos()
    prueba_gen2_rotula_en_arbol()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_tablero_programa.py: 16 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
