#!/usr/bin/env python3
"""Pruebas dirigidas del cableado necesidad -> residual -> selector -> cierre."""
from __future__ import annotations

import datetime
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import adq_doctor as doctor  # noqa: E402
import adq_residual as residual  # noqa: E402


CAMPOS = [
    "fila_origen", "fuente_canonica", "fuente_canonica_normalizada",
    "discordancia_alias", "estado_A4A5", "prioridad", "url_conocida",
    "ids_manifiesto", "origen", "nota",
]


def _fila(**cambios):
    base = {c: "" for c in CAMPOS}
    base.update({"fila_origen": "legacy:1", "fuente_canonica": "PADRE",
                 "fuente_canonica_normalizada": "PADRE",
                 "estado_A4A5": "OBTENIDO", "nota": "historia padre"})
    base.update(cambios)
    return base


def test_residual_con_acceso_no_rebaja_padre_y_aparece_en_cierre():
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td)
        registro = raiz / "registro.tsv"
        vista = raiz / "vista.tsv"
        registro.write_text("\t".join(CAMPOS) + "\n" +
                            "\t".join(_fila()[c] for c in CAMPOS) + "\n",
                            encoding="utf-8")
        nueva = residual.construye_fila(
            objeto_id="PADRE_MICRODATO", padre="PADRE", consumidor="N1",
            objeto="microdato exacto", cobertura="documentación obtenida",
            residual="filas de datos", via="formulario institucional",
            autoridad="D1; identidad humana requerida",
            siguiente_accion="titular presenta y aporta acuse",
            estado="SOLICITUD-PREPARADA", prioridad="1", origen="NC-1")
        residual.upsert_residual(nueva, registro=registro, vista=vista)
        filas = doctor.lee_cola_dicts(registro)
        assert len(filas) == 2
        assert filas[0]["estado_A4A5"] == "OBTENIDO"
        seleccion = doctor.selecciona_filas(
            [(f["fuente_canonica"], f["estado_A4A5"], f["prioridad"], f["nota"])
             for f in filas], corte=datetime.date(2026, 9, 11))
        cierre = doctor.resumen_necesidades(filas, seleccion)
        assert seleccion["elegidos"] == []
        assert cierre["pendientes_acceso"]["ids"] == ["PADRE_MICRODATO"]
        assert cierre["cubiertas"]["cantidad"] == 0
        assert "PADRE_MICRODATO" in vista.read_text(encoding="utf-8")


def test_pendiente_exige_autorizacion_del_objeto_y_llega_al_selector():
    argumentos = dict(
        objeto_id="OBJETO_PUBLICO", padre="PADRE", consumidor="N2",
        objeto="CSV exacto", cobertura="ninguna", residual="CSV",
        via="URL pública", siguiente_accion="descargar y verificar",
        estado="PENDIENTE", prioridad="0", origen="SONDA", url="https://example.test/a.csv")
    try:
        residual.construye_fila(autoridad="AUTORIZADA:mesa/2026-09-11/OTRO", **argumentos)
    except ValueError:
        pass
    else:
        raise AssertionError("una autorización de otro objeto no debe habilitar el residual")
    fila = residual.construye_fila(
        autoridad="AUTORIZADA:mesa/2026-09-11/OBJETO_PUBLICO", **argumentos)
    seleccion = doctor.selecciona_filas(
        [(fila["fuente_canonica"], fila["estado_A4A5"], fila["prioridad"], fila["nota"])],
        corte=datetime.date(2026, 9, 11))
    assert [x["id"] for x in seleccion["elegidos"]] == ["OBJETO_PUBLICO"]


def test_no_accesible_nombrada_no_salta_barrera():
    seleccion = doctor.selecciona_filas(
        [("CERRADO", "NO-ACCESIBLE", "1", "requiere cuenta")],
        corte=datetime.date(2026, 9, 11), nombradas=["CERRADO"])
    assert seleccion["elegidos"] == []
    assert "nombrarla no supera" in seleccion["excluidos"][0]["razon"]


if __name__ == "__main__":
    test_residual_con_acceso_no_rebaja_padre_y_aparece_en_cierre()
    test_pendiente_exige_autorizacion_del_objeto_y_llega_al_selector()
    test_no_accesible_nombrada_no_salta_barrera()
    print("OK -- test_adq_residuales.py: 3 casos, 0 fallos")
