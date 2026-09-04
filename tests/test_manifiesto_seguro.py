#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_manifiesto_seguro.py -- seguridad de escritura de
data/manifiesto.yaml (tests/manifiesto.py). ACTO MAESTRA38 · TESTS-FRENTE-A-B.

Todo lo que sigue corre sobre fixtures temporales (tempfile), nunca contra
data/manifiesto.yaml real -- no hay ninguna importación ni referencia a la
raíz del repo salvo `import manifiesto` (código, no dato).

Qué defecto real fija cada caso:

  test_registra_no_sobreescribe_id_existente
      Regla explícita de cmd_registra (tests/manifiesto.py:439-443): un id
      que ya existe es ERROR, nunca un edit silencioso. Sin este test, un
      refactor futuro de cmd_registra podría convertir el `sys.exit(1)` en
      un overwrite y nada lo atraparía -- exactamente el tipo de regresión
      silenciosa que I-04 (cifras tecleadas a mano) mide en el otro
      extremo: aquí no es una cifra mala, es una entrada buena que se pierde.

  test_registra_no_duplica_por_sha256
      Dedup por contenido (tests/manifiesto.py:453-462): dos ids distintos
      para el mismo archivo (mismo sha256) es el defecto que el propio
      docstring de tests/manifiesto.py cita como ya ocurrido -- "dejó pasar
      dos entradas para el mismo PDF de ENCIG bajo dos ids, de dos sesiones
      que no se vieron" (30/jul). Este test reproduce esa condición
      (dos --registra sobre el mismo contenido, ids distintos) y exige que
      el segundo falle.

  test_escritura_atomica_no_corrompe_si_falla_validacion
      _escribir_atomico + _validar_manifiesto_completo (tests/manifiesto.py
      :207-360): una entrada que rompe la validación (aquí, `tamano_bytes`
      no entero) nunca debe tocar el archivo en disco -- el temporal se
      valida ANTES de os.replace(). Fija la garantía que el propio
      docstring de _escribir_atomico declara ("cualquier fallo antes de que
      os.replace termine deja `path` intacto") con un caso real, no solo
      con la prosa.

  test_lock_serializa_dos_escritores_concurrentes
      Fija el defecto "dos escritores el 3/sep": dos --registra concurrentes
      (hilos) sobre el MISMO data/manifiesto.yaml, con _con_lock_manifiesto
      como única protección. Sin el lock (flock exclusivo), dos escritores
      que leen-modifican-escriben el mismo archivo pueden pisarse: el
      segundo en escribir sobrescribe el archivo entero con SU copia de
      `entradas` (leída antes de que el primero terminara), perdiendo la
      entrada del primero aunque ambos "tuvieron éxito". Este test corre
      ambos registros de verdad en paralelo (threading, no simulado en
      secuencia) y exige que las DOS entradas sobrevivan.

Corre solo:
    python3 tests/test_manifiesto_seguro.py
"""
import argparse
import contextlib
import io
import os
import sys
import tempfile
import threading

sys.path.insert(0, "tests")
import manifiesto  # noqa: E402


def _preparar_root(tmp):
    root = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(root, "data", "raw"), exist_ok=True)
    return root


def _archivo_dato(raw_dir, nombre, contenido=b"contenido-de-prueba"):
    ruta = os.path.join(raw_dir, nombre)
    with open(ruta, "wb") as f:
        f.write(contenido)
    return ruta


def _args_registra(**overrides):
    valores = dict(
        id=None, archivo=None, usado_para=["prueba"], url_origen="https://example.mx/x",
        descargado_por="test", formato="csv", licencia="publica",
        fecha_descarga=None, nota=None,
    )
    valores.update(overrides)
    return argparse.Namespace(**valores)


def _registra(manifiesto_path, raw_dir, id_, archivo):
    args = _args_registra(id=[id_], archivo=archivo)
    salida = io.StringIO()
    try:
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(salida):
            manifiesto.cmd_registra(args, manifiesto_path, raw_dir)
        return True, salida.getvalue()
    except SystemExit:
        return False, salida.getvalue()


def _registra_sin_capturar(manifiesto_path, raw_dir, id_, archivo):
    """Igual que `_registra`, sin `contextlib.redirect_stdout`: ese context
    manager pisa `sys.stdout` global y no es seguro invocarlo desde dos
    hilos a la vez (el segundo restaura sobre el cambio del primero,
    dejando `sys.stdout` corrupto para el resto del proceso). Usado por
    `test_lock_serializa_dos_escritores_concurrentes`, que corre dos
    `cmd_registra` de verdad en paralelo -- lo que mide es la
    serialización de la ESCRITURA AL ARCHIVO (`_con_lock_manifiesto`), no
    la de la salida a consola, así que dejarla sin capturar (va a stdout
    real, inofensivo) es correcto aquí."""
    args = _args_registra(id=[id_], archivo=archivo)
    try:
        manifiesto.cmd_registra(args, manifiesto_path, raw_dir)
        return True
    except SystemExit:
        return False


def test_registra_no_sobreescribe_id_existente():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        manifiesto_path, raw_dir = manifiesto.rutas(root)
        _archivo_dato(raw_dir, "a.csv", b"AAA")
        _archivo_dato(raw_dir, "b.csv", b"BBB")

        ok1, _ = _registra(manifiesto_path, raw_dir, "id-1", "a.csv")
        assert ok1, "el primer --registra debe tener éxito"

        ok2, salida2 = _registra(manifiesto_path, raw_dir, "id-1", "b.csv")
        assert not ok2, "un id repetido debe fallar, nunca sobreescribir"
        assert "ya existe" in salida2

        _, entradas = manifiesto.leer_manifiesto(manifiesto_path)
        assert len(entradas) == 1
        assert entradas[0]["archivo"] == "a.csv", (
            "la entrada original no debió cambiar")


def test_registra_no_duplica_por_sha256():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        manifiesto_path, raw_dir = manifiesto.rutas(root)
        _archivo_dato(raw_dir, "encig23_original.pdf", b"mismo-contenido-encig")
        _archivo_dato(raw_dir, "encig23_copia.pdf", b"mismo-contenido-encig")

        ok1, _ = _registra(manifiesto_path, raw_dir, "encig23_a", "encig23_original.pdf")
        assert ok1

        ok2, salida2 = _registra(manifiesto_path, raw_dir, "encig23_b", "encig23_copia.pdf")
        assert not ok2, "mismo sha256 bajo id distinto debe fallar"
        assert "ya está registrado" in salida2
        assert "encig23_a" in salida2

        _, entradas = manifiesto.leer_manifiesto(manifiesto_path)
        assert len(entradas) == 1


def test_escritura_atomica_no_corrompe_si_falla_validacion():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        manifiesto_path, raw_dir = manifiesto.rutas(root)
        _archivo_dato(raw_dir, "bueno.csv", b"contenido-bueno")

        ok, _ = _registra(manifiesto_path, raw_dir, "id-bueno", "bueno.csv")
        assert ok
        texto_antes = open(manifiesto_path, encoding="utf-8").read()

        cabecera, entradas = manifiesto.leer_manifiesto(manifiesto_path)
        entradas.append({
            "id": "id-malo",
            "archivo": "bueno.csv",
            "sha256": "0" * 64,
            "tamano_bytes": "no-es-entero",
        })
        try:
            manifiesto.escribir_manifiesto(manifiesto_path, cabecera, entradas)
            raise AssertionError("se esperaba ValueError por tamano_bytes inválido")
        except ValueError as exc:
            assert "tamano_bytes" in str(exc)

        texto_despues = open(manifiesto_path, encoding="utf-8").read()
        assert texto_antes == texto_despues, (
            "una escritura que falla validación no debe tocar el archivo en disco")
        assert not any(
            nombre.startswith(".manifiesto.yaml.")
            for nombre in os.listdir(os.path.dirname(manifiesto_path))
        ), "el temporal debe limpiarse incluso cuando la validación falla"


def test_lock_serializa_dos_escritores_concurrentes():
    with tempfile.TemporaryDirectory() as tmp:
        root = _preparar_root(tmp)
        manifiesto_path, raw_dir = manifiesto.rutas(root)
        _archivo_dato(raw_dir, "uno.csv", b"contenido-uno")
        _archivo_dato(raw_dir, "dos.csv", b"contenido-dos")

        resultados = {}

        def escribe(id_, archivo):
            resultados[id_] = _registra_sin_capturar(manifiesto_path, raw_dir, id_, archivo)

        t1 = threading.Thread(target=escribe, args=("id-uno", "uno.csv"))
        t2 = threading.Thread(target=escribe, args=("id-dos", "dos.csv"))
        t1.start()
        t2.start()
        t1.join(timeout=10)
        t2.join(timeout=10)

        assert resultados["id-uno"], "id-uno debió registrarse con éxito"
        assert resultados["id-dos"], "id-dos debió registrarse con éxito"

        _, entradas = manifiesto.leer_manifiesto(manifiesto_path)
        ids = sorted(e["id"] for e in entradas)
        assert ids == ["id-dos", "id-uno"], (
            f"las dos entradas debieron sobrevivir sin pisarse, quedó: {ids}")


def main():
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"OK   {nombre}")
            except AssertionError as exc:
                fallos += 1
                print(f"FAIL {nombre}: {exc}")
    if fallos:
        print(f"\n{fallos} fallo(s)")
        return 1
    print("\ntodo OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
