"""DONDE-CAMBIO P4: el documento y la tabla tienen 0 cifras sin RESULT.

Atrapa la cifra tecleada a mano en `canon/donde-cambio-el-mexicano-v1_0.md`
(v2.16 §2, «ninguna cifra esperada se teclea»): (1) regenera tabla y documento
desde los RESULT sellados de `CALC-*-SERIE-DICTAMEN-0001` y exige igualdad
byte a byte; (2) toda línea del documento con una cifra (detector de
`tools/recibo/cifras_sin_result.py`) cita un `RESULT-`; (3) control positivo:
el detector marca una línea con cifra y sin cita.
"""
from tools.recibo.cifras_sin_result import cifras_en_linea
from tools.series import documento as DOC


import re

# Referencias que no son cifras de dato: spans de código (ids, rutas, hashes),
# versión de instrucciones, sección, número de PR, el intervalo (0,1).
_NO_DATO = re.compile(r"`[^`]*`|v\d+\.\d+|§\d+|#\d+|\(0,1\)")


def _sin_cita(texto):
    return [l for l in texto.splitlines()
            if cifras_en_linea(_NO_DATO.sub("", l)) and "RESULT-" not in l]


def test_regenera_byte_a_byte():
    tabla, doc = DOC.main()
    assert DOC.TABLA.read_text(encoding="utf-8") == tabla
    assert DOC.DOC.read_text(encoding="utf-8") == doc


def test_cero_cifras_sin_result():
    malas = _sin_cita(DOC.DOC.read_text(encoding="utf-8"))
    assert not malas, malas[:3]


def test_control_positivo():
    assert _sin_cita("El 42.5 % de algo cambió.") and _sin_cita("en ciudades de 100 mil")
    assert not _sin_cita("42.5 pp `RESULT-X`") and not _sin_cita("v2.16 §4 #972 (0,1) `9aea5a09`")


def test_una_fila_por_serie_con_dictamen():
    from tools.series.dictamen import VOCAB
    lineas = DOC.TABLA.read_text(encoding="utf-8").splitlines()
    cab = lineas[0].split("\t")
    ids = [l.split("\t")[0] for l in lineas[1:]]
    dic = [l.split("\t")[cab.index("dictamen")] for l in lineas[1:]]
    assert len(ids) == len(set(ids)) and all(d in VOCAB for d in dic)


if __name__ == "__main__":
    test_regenera_byte_a_byte(); test_cero_cifras_sin_result(); test_control_positivo()
    test_una_fila_por_serie_con_dictamen()
    print("OK")
