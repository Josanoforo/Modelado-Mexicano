"""tests/test_corpus_loader.py -- caché Parquet y cargador (ACTO GEN2-CORPUS-CACHE-PARQUET-1).

Defecto que atrapa: una caché que no reproduce el original -- filas o
columnas perdidas, un valor cambiado al tipar, un Parquet reemplazado sin
constancia -- le da a un medidor nuevo otro dato del que el CSV le daría, sin
error. Casos:

1. Sintético (corre donde haya pyarrow): zip con `conjunto_de_datos/` +
   `diccionario_de_datos/`, y un DBF. Tipos declarados (N entero, N con
   soporte 'NA' -> texto, C con ceros a la izquierda -> texto intacto),
   verificación IGUAL, `cargar()` con proyección, Parquet adulterado ->
   ValueError, y una mutación del conteo de referencia -> DISCORDANTE.
2. Real (CAJA, corpus y caché presentes): dos payloads CSV pequeños de la
   caché; filas y columnas del Parquet contra `pandas.read_csv(dtype=str)` del
   miembro original, un lector independiente del conversor.
"""
import importlib.util
import io
import os
import struct
import sys
import zipfile
from pathlib import Path

import pytest

pa = pytest.importorskip("pyarrow")
pytest.importorskip("pyarrow.parquet")
pytest.importorskip("zipfile_deflate64")

RAIZ = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("corpus_loader", RAIZ / "tools" / "corpus_loader.py")
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

DOS_PEQUENOS = ["enasem2021_bd_csv_zip", "enut2019_bd_csv"]


def _dbf(campos, filas):
    """DBF III mínimo: campos = [(nombre, tipo, ancho, dec)], filas = listas de str."""
    rsize = 1 + sum(c[2] for c in campos)
    hsize = 32 + 32 * len(campos) + 1
    out = io.BytesIO()
    out.write(struct.pack("<BBBBIHH20x", 3, 126, 9, 28, len(filas), hsize, rsize))
    for n, t, w, d in campos:
        out.write(struct.pack("<11sc4xBB14x", n.encode("latin-1"), t.encode(), w, d))
    out.write(b"\x0d")
    for f in filas:
        out.write(b" ")
        for (n, t, w, d), v in zip(campos, f):
            v = v.encode("latin-1")
            out.write(v.rjust(w) if t in "NF" else v.ljust(w))
    out.write(b"\x1a")
    return out.getvalue()


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    monkeypatch.setenv("MM_CACHE_RAIZ", str(tmp_path / "cache"))
    monkeypatch.setenv("MM_CACHE_REGISTRO", str(tmp_path / "reg"))
    csv = ("FOLIO,EDAD,P1,ENT,PESO\r\n"
           "0001,34,1,01,1.5\r\n"
           "0002,,NA,09,2.25\r\n"
           "0003,71,2,32,\r\n")
    dic = ('"NOMBRE_CAMPO","NEMONICO","TIPO","LONGITUD"\r'
           '"Folio","FOLIO","Alfanumérico",4\r'
           '"Edad","EDAD","Numérico",2\r'
           '"Pregunta 1","P1","Numérico",1\r'
           '"Entidad","ENT","Carácter",2\r'
           '"Peso","PESO","Numérico",6\r')
    zp = tmp_path / "sint.zip"
    with zipfile.ZipFile(zp, "w") as z:
        z.writestr("cd_x/conjunto_de_datos/cd_x.csv", csv.encode("latin-1"))
        z.writestr("cd_x/diccionario_de_datos/diccionario_de_datos_x.csv", dic.encode("latin-1"))
        z.writestr("cd_x/catalogos/ENT.csv", b"ENT,NOM\r\n01,Ags\r\n")
    with zipfile.ZipFile(tmp_path / "sint_dbf.zip", "w") as z:
        z.writestr("tabla.dbf", _dbf([("ID", "C", 4, 0), ("N", "N", 3, 0), ("W", "N", 6, 2)],
                                     [["a1", "5", "1.25"], ["a2", "", "0.50"], ["a3", "12", "3.00"]]))
    return tmp_path, zp


def _convierte(zp, miembro, fmt):
    destino = L.raiz_cache() / "sint" / f"{L.tabla_de(miembro)}.parquet"
    cons, verif = L._convierte_texto_tabular("sint", zp, miembro, "0" * 64, destino, fmt)
    return cons, verif, destino


def test_miembros_y_diccionario(entorno):
    _, zp = entorno
    ms = [m for m, _ in L.miembros_tabulares(zp)]
    assert ms == ["cd_x/conjunto_de_datos/cd_x.csv"]  # ni diccionario ni catálogo son tabla
    assert [m for m, _ in L.miembros_tabulares(zp.parent / "sint_dbf.zip")] == ["tabla.dbf"]
    d = L.diccionario_csv(zp, ms[0])
    assert d == {"FOLIO": "C", "EDAD": "N", "P1": "N", "ENT": "C", "PESO": "N"}


def test_csv_tipos_declarados_y_verificacion(entorno):
    import pyarrow.parquet as pq
    _, zp = entorno
    cons, verif, destino = _convierte(zp, "cd_x/conjunto_de_datos/cd_x.csv", "csv")
    assert verif["veredicto"] == "IGUAL" and cons is not None
    assert verif["sha256_origen_1"] == verif["sha256_origen_2"]
    t = pq.read_table(destino)
    tipos = {f.name: str(f.type) for f in t.schema}
    assert tipos == {"FOLIO": "string", "EDAD": "int64", "P1": "string", "ENT": "string", "PESO": "double"}
    assert t.column("FOLIO").to_pylist() == ["0001", "0002", "0003"]      # ceros intactos
    assert t.column("EDAD").to_pylist() == [34, None, 71]                 # '' -> nulo
    assert t.column("P1").to_pylist() == ["1", "NA", "2"]                 # soporte no numérico -> texto
    assert verif["cols_texto_soporte_no_numerico"] == 1
    assert cons["sha256_parquet"] == L.sha256_archivo(destino)


def test_dbf_descriptor(entorno):
    import pyarrow.parquet as pq
    _, zp = entorno
    cons, verif, destino = _convierte(zp.parent / "sint_dbf.zip", "tabla.dbf", "dbf")
    assert verif["veredicto"] == "IGUAL"
    t = pq.read_table(destino)
    assert t.column("ID").to_pylist() == ["a1", "a2", "a3"]
    assert t.column("N").to_pylist() == [5, None, 12]
    assert t.column("W").to_pylist() == [1.25, 0.5, 3.0]


def test_cargar_proyeccion_y_sello(entorno):
    _, zp = entorno
    miembro = "cd_x/conjunto_de_datos/cd_x.csv"
    cons, _, destino = _convierte(zp, miembro, "csv")
    L._anexa_tsv(L._constancias(), L.COLS_CONSTANCIA, cons)
    df = L.cargar("sint", "cd_x", ["FOLIO", "EDAD"])
    assert list(df.columns) == ["FOLIO", "EDAD"] and len(df) == 3
    assert df.attrs["fuente"].startswith("PARQUET:sint/cd_x.parquet:")
    assert str(df["EDAD"].dtype) == "Int64"
    with open(destino, "ab") as f:  # adulterar: ya no casa con la constancia
        f.write(b"x")
    with pytest.raises(ValueError, match="CACHE-DISCORDANTE"):
        L.cargar("sint", "cd_x", ["FOLIO"])


def test_mutacion_verificacion_detecta(entorno, monkeypatch):
    """Si el Parquet no reprodujera una columna, la constancia no se escribe."""
    _, zp = entorno
    real = L.huellas_parquet

    def huellas_mutadas(ruta):
        f, cols, h = real(ruta)
        h["ENT"] = h["ENT"][:-1] + ("0" if h["ENT"][-1] != "0" else "1")
        return f, cols, h

    monkeypatch.setattr(L, "huellas_parquet", huellas_mutadas)
    cons, verif, destino = _convierte(zp, "cd_x/conjunto_de_datos/cd_x.csv", "csv")
    assert cons is None and verif["veredicto"] == "DISCORDANTE" and not destino.exists()


def test_reservada_se_niega():
    assert L.motivo_reserva("envipe2026_csv", {}) .startswith("m: ENVIPE 2026")
    assert L.motivo_reserva("x", {"estado_reserva": "RESERVADA-NO-ABIERTA-NO-INDEXAR-L"}).startswith("manifiesto")
    assert L.motivo_reserva("encig23_base_datos_csv", {}) == ""


def _real_disponible(pid):
    if os.environ.get("MM_CACHE_RAIZ") or not (RAIZ / "data" / "raw").exists():
        return False
    return any(r["id"] == pid for r in L._lee_tsv(L._constancias()))


@pytest.mark.parametrize("pid", DOS_PEQUENOS)
def test_real_parquet_vs_csv(pid):
    """Filas y columnas de cada Parquet del payload contra pandas.read_csv del original."""
    if not _real_disponible(pid):
        pytest.skip("corpus o caché ausentes (NECESITA-CORPUS): corre en CAJA")
    import pandas as pd
    import pyarrow.parquet as pq
    filas = [r for r in L._lee_tsv(L._constancias()) if r["id"] == pid]
    assert filas
    ruta = L.ruta_payload(pid)
    for r in filas:
        p = L.ruta_parquet(pid, L.tabla_de(r["miembro"]))
        assert L.sha256_archivo(p) == r["sha256_parquet"]
        meta = pq.ParquetFile(p).metadata
        enc = pq.ParquetFile(p).schema_arrow.metadata[b"mm.encoding"].decode()
        _, delim, _ = L._cabecera_csv(ruta, r["miembro"], "latin1" if enc == "latin1" else None)
        f, cierra = L._abre_miembro(ruta, r["miembro"])
        try:
            df = pd.read_csv(f, dtype=str, keep_default_na=False, na_filter=False, sep=delim,
                             encoding="utf-8-sig" if enc == "utf8" else "latin-1")
        finally:
            f.close()
            for c in cierra:
                c.close()
        assert (meta.num_rows, meta.num_columns) == (len(df), df.shape[1]) == (int(r["filas"]), int(r["columnas"]))
        assert pq.ParquetFile(p).schema_arrow.names == [c.strip() for c in df.columns]


def test_tabla_unica_por_carpeta():
    """edr2015_2019: cinco carpetas por año con el mismo CAPGPO.dbf se pisaban
    cuando la tabla era sólo el tallo (lo atrapó `corpus_loader.py verifica`)."""
    ms = [f"defunciones_base_datos_{a}/CAPGPO.dbf" for a in range(2015, 2020)]
    assert len({L.tabla_de(m) for m in ms}) == 5
    assert L.tabla_de("cd_x/conjunto_de_datos/cd_x.csv") == "cd_x"
    assert L.tabla_de("e.zip!sub/T.dbf") == "e__sub__T"
