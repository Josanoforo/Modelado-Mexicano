#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_verifica_sidecars.py -- el sello de cuerpo (D-a1/D-a2/D-a5)
y el verificador de sidecars de `forense/encargos/` y `forense/notas/`
(D-a4). ACTO GEN2-TUBERIA-SIDECAR-CUERPO-1, 21/sep/2026.

DEFECTO REAL QUE ATRAPA, ya ocurrido y medido (§3 del encargo):
  * `#932` -- el sello del 0-bis dejó de casar en cuanto el propio acto
    añadió `## NO-CORRIDO`, se re-selló sobre el texto final, y una
    renumeración posterior rompió ese re-sello. El sidecar vigente
    declaraba `b07f8ba3…` y fallaba. Con la regla firmada, el sello
    original `8a847600…` pasa.
  * `sha256sum -c` ingenuo sobre los 261 sidecars del árbol: 21
    negativos, 17 de ellos falsas alarmas de FORMATO. Un verificador que
    grita en falso no lo lee nadie.

Pruebas por MUTACIÓN sobre fixtures en temporal, más dos lecturas del
repo real. Stdlib puro: sin red, sin corpus, sin escribir producción.

Corre solo:
    python3 tests/test_verifica_sidecars.py
"""
import hashlib
import os
import shutil
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

import sella_sha256  # noqa: E402
import verifica_sidecars as vs  # noqa: E402

CUERPO = """ENCARGO · ACTO DE PRUEBA
CABECERA · redactado contra `deadbeef`.

1 · OBJETIVO
Que el cuerpo del encargo quede sellado y el cierre no lo toque.
"""


def _hash_texto(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def _monta(tmp, nombre, contenido):
    """Escribe `forense/encargos/<nombre>` bajo una raíz temporal."""
    destino = os.path.join(tmp, "forense", "encargos")
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


def _fila(tmp, sidecar_rel):
    for f in vs.recorre(tmp):
        if f["sidecar"] == sidecar_rel:
            return f
    raise AssertionError(f"el verificador no vio {sidecar_rel}")


# --------------------------------------------------------------------
# N(texto) -- D-a1
# --------------------------------------------------------------------

def test_normalizacion_es_idempotente_y_pela_guiones():
    base = "cuerpo\n"
    variantes = [
        "cuerpo",
        "cuerpo\n",
        "cuerpo\n\n\n",
        "cuerpo\n---\n",
        "cuerpo\n\n---\n\n",
        "cuerpo\n---\n\n---\n   \n",
    ]
    for v in variantes:
        n = sella_sha256.normaliza_cuerpo(v)
        assert n == base, f"N({v!r}) = {n!r}, se esperaba {base!r}"
        assert sella_sha256.normaliza_cuerpo(n) == n, "N no es idempotente"


# --------------------------------------------------------------------
# El sello de cuerpo -- P-c, mutaciones mínimas exigidas
# --------------------------------------------------------------------

def test_sello_de_cuerpo_que_pasa():
    with tempfile.TemporaryDirectory() as tmp:
        ruta = _monta(tmp, "encargo.md", CUERPO)
        assert sella_sha256.sella_cuerpo(ruta)[0] == 0
        codigo, mensaje = sella_sha256.verifica_cuerpo(ruta)
        assert codigo == 0, mensaje
        assert "candidato=archivo-entero" in mensaje, mensaje
        assert "WARN_" not in mensaje, mensaje


def test_cuerpo_editado_falla():
    with tempfile.TemporaryDirectory() as tmp:
        ruta = _monta(tmp, "encargo.md", CUERPO)
        sella_sha256.sella_cuerpo(ruta)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(CUERPO.replace("deadbeef", "cafe1234"))
        codigo, mensaje = sella_sha256.verifica_cuerpo(ruta)
        assert codigo == 3, mensaje
        assert "SELLO_NO_COINCIDE" in mensaje
        # el sidecar sigue en disco: verificar NUNCA escribe
        assert os.path.exists(sella_sha256.ruta_sidecar_cuerpo(ruta))


def test_cierre_al_final_bajo_no_corrido_pasa_limpio():
    with tempfile.TemporaryDirectory() as tmp:
        ruta = _monta(tmp, "encargo.md", CUERPO)
        sella_sha256.sella_cuerpo(ruta)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\n## NO-CORRIDO / RESERVAS\n\nNinguno.\n\n## CONSUMIDO\n\nPR #999.\n")
        codigo, mensaje = sella_sha256.verifica_cuerpo(ruta)
        assert codigo == 0, mensaje
        assert "## NO-CORRIDO / RESERVAS" in mensaje, mensaje
        assert "WARN_" not in mensaje, mensaje


def test_cierre_bajo_otro_encabezado_pasa_con_warn_y_nombra_el_candidato():
    with tempfile.TemporaryDirectory() as tmp:
        ruta = _monta(tmp, "encargo.md", CUERPO)
        sella_sha256.sella_cuerpo(ruta)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\n## ADENDA DE MESA\n\nTexto pegado al final.\n")
        codigo, mensaje = sella_sha256.verifica_cuerpo(ruta)
        assert codigo == 0, mensaje            # WARN no adjudica (D-16)
        assert "WARN_ENCABEZADO_AJENO" in mensaje, mensaje
        assert "## ADENDA DE MESA" in mensaje, mensaje
        assert "candidato=prefijo-antes-de-linea-" in mensaje, mensaje


def test_doble_no_corrido_pasa_sin_elegir_delimitador():
    """Cuatro encargos reales tienen más de una línea `## NO-CORRIDO`
    (`PRE-E5`, `BANXICO-PRODUCTO-ATRASO-Y-COSTO`, `CHECADOR-2`, `E3-1-1`).
    El hash desambigua: cualquiera de las dos particiones verifica, sin
    que el verificador tenga que escoger delimitador."""
    real = os.path.join(
        REPO_ROOT, "forense", "encargos",
        "2026-09-08-GEN2-E3-1-1-CABLEADO-FINAL-RUNNER.md")
    texto = open(real, encoding="utf-8").read()
    ocurrencias = [c for c in sella_sha256.candidatos_cuerpo(texto)
                   if c[2] and c[2].startswith("## NO-CORRIDO")]
    assert len(ocurrencias) >= 2, "la premisa del doble `## NO-CORRIDO` ya no se sostiene"

    with tempfile.TemporaryDirectory() as tmp:
        for etiqueta, candidato, _enc in ocurrencias:
            ruta = _monta(tmp, "doble.md", texto)
            sidecar = sella_sha256.ruta_sidecar_cuerpo(ruta)
            esperado = _hash_texto(sella_sha256.normaliza_cuerpo(candidato))
            with open(sidecar, "w", encoding="utf-8") as f:
                f.write(f"{esperado}  doble.md\n")
            codigo, mensaje = sella_sha256.verifica_cuerpo(ruta)
            assert codigo == 0, f"{etiqueta}: {mensaje}"
            assert "WARN_" not in mensaje, mensaje


# --------------------------------------------------------------------
# El verificador -- D-a4
# --------------------------------------------------------------------

def test_los_tres_formatos_viejos_se_leen_sin_falsa_alarma():
    """(1) basename relativo al sidecar · (2) ruta relativa a la raíz ·
    (3) hash pelado contra el archivo hermano. Ninguno es FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        contenido = b"payload historico\n"
        h = hashlib.sha256(contenido).hexdigest()
        destino = os.path.join(tmp, "forense", "notas")
        os.makedirs(destino)
        casos = {
            "f1.md": f"{h}  f1.md\n",
            "f2.md": f"{h}  forense/notas/f2.md\n",
            "f3.md": f"{h}\n",
        }
        for nombre, linea in casos.items():
            with open(os.path.join(destino, nombre), "wb") as f:
                f.write(contenido)
            # `X.md.sha256` para los dos primeros, `X.sha256` para el tercero:
            # las dos convenciones de nombre que conviven en el árbol.
            sidecar = nombre + ".sha256" if nombre != "f3.md" else "f3.sha256"
            with open(os.path.join(destino, sidecar), "w", encoding="utf-8") as f:
                f.write(linea)

        filas = vs.recorre(tmp)
        assert len(filas) == 3, filas
        for fila in filas:
            assert fila["estado"] == vs.CASA, fila
        assert vs.adjudica(filas) == []


def test_sidecar_de_cuerpo_roto_es_fail_y_uno_viejo_roto_declarado_no_adjudica():
    with tempfile.TemporaryDirectory() as tmp:
        ruta = _monta(tmp, "encargo.md", CUERPO)
        sella_sha256.sella_cuerpo(ruta)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\nlínea metida DENTRO del cuerpo\n")
        fila = _fila(tmp, "forense/encargos/encargo.md.cuerpo.sha256")
        assert fila["estado"] == vs.NO_CASA, fila
        assert len(vs.adjudica(vs.recorre(tmp))) == 1


def test_huerfano_es_fail_salvo_declarado():
    with tempfile.TemporaryDirectory() as tmp:
        destino = os.path.join(tmp, "forense", "notas")
        os.makedirs(destino)
        with open(os.path.join(destino, "h.md.sha256"), "w", encoding="utf-8") as f:
            f.write(f"{'0' * 64}  no-esta-aqui.json\n")
        fila = _fila(tmp, "forense/notas/h.md.sha256")
        assert fila["estado"] == vs.HUERFANO, fila
        assert len(vs.adjudica(vs.recorre(tmp))) == 1


def test_el_verificador_nunca_escribe():
    """D-a4: NO reescribe ni normaliza ningún sidecar. Se mide por
    huella (mtime + bytes) de todo el árbol temporal."""
    with tempfile.TemporaryDirectory() as tmp:
        ruta = _monta(tmp, "encargo.md", CUERPO)
        sella_sha256.sella_cuerpo(ruta)
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\n## ADENDA\n\nalgo\n")

        def huella():
            h = {}
            for actual, _d, archivos in os.walk(tmp):
                for n in archivos:
                    p = os.path.join(actual, n)
                    st = os.stat(p)
                    h[os.path.relpath(p, tmp)] = (st.st_size, st.st_mtime_ns,
                                                  hashlib.sha256(open(p, "rb").read()).hexdigest())
            return h

        antes = huella()
        vs.recorre(tmp)
        vs.main(["--raiz", tmp])
        assert huella() == antes, "el verificador tocó el árbol"


def test_repo_real_en_verde():
    """El universo firmado, tal como está hoy en este clon. Si esto
    falla, hay un sidecar real roto y el acto lo debe declarar."""
    filas = vs.recorre(REPO_ROOT)
    assert filas, "el verificador no encontró ningún sidecar en el repo"
    fallos = vs.adjudica(filas)
    assert not fallos, "sidecars en FAIL: " + ", ".join(
        f"{f['estado']} {f['sidecar']}" for f in fallos)
    # Y el sello restaurado de #932 casa con el prefijo del 0-bis.
    fila = next(f for f in filas if f["sidecar"].endswith(
        "2026-09-20-GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1.md.cuerpo.sha256"))
    assert fila["estado"] == vs.CASA, fila
    assert "## NO-CORRIDO" in fila["detalle"], fila


def main():
    casos = [
        test_normalizacion_es_idempotente_y_pela_guiones,
        test_sello_de_cuerpo_que_pasa,
        test_cuerpo_editado_falla,
        test_cierre_al_final_bajo_no_corrido_pasa_limpio,
        test_cierre_bajo_otro_encabezado_pasa_con_warn_y_nombra_el_candidato,
        test_doble_no_corrido_pasa_sin_elegir_delimitador,
        test_los_tres_formatos_viejos_se_leen_sin_falsa_alarma,
        test_sidecar_de_cuerpo_roto_es_fail_y_uno_viejo_roto_declarado_no_adjudica,
        test_huerfano_es_fail_salvo_declarado,
        test_el_verificador_nunca_escribe,
        test_repo_real_en_verde,
    ]
    fallos = 0
    for caso in casos:
        try:
            caso()
            print("OK   {}".format(caso.__name__))
        except AssertionError as e:
            fallos += 1
            print("FAIL {}: {}".format(caso.__name__, e))
    print("---")
    if fallos:
        print("{} de {} casos FALLARON".format(fallos, len(casos)))
        return 1
    print("{} casos OK".format(len(casos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
