"""Regresión del defecto de subcadena en `construir_crosswalk` (FP-166,
DERIVACION-M-v1_0.md): el emparejamiento antiguo decidía con `var in l`,
sin comparar la columna `encuesta` ni exigir token exacto de la variable,
y producía tres falsos positivos citados verbatim en el hallazgo del acto
E7 (DIN-03/ENIF/P7_1, DIN-11/ENIF/P5_3, TIC-06/ENTI/P2). Este test fija
esos tres como negativos y un caso real (CIV-01/ENCIG/P8_3_1,
procedencia.yaml:937) como positivo de control."""
from milpa.src.emisor import _tiene_token, _token_encuesta, construir_crosswalk, RUTA_PROCEDENCIA


def test_token_encuesta_toma_el_acronimo():
    assert _token_encuesta("ENCIG 2023") == "ENCIG"
    assert _token_encuesta("ENAFIN (Encuesta Nacional de Financiamiento de las Empresas)") == "ENAFIN"


def test_tiene_token_exige_frontera_no_subcadena():
    assert _tiene_token("hit único de mnemónico es AP7_1 de ENCUCI", "P7_1") is False
    assert _tiene_token("P7_12_7 (tabla TPER_ELE)", "P7_1") is False
    assert _tiene_token("AP5_3_XX (:231)", "P5_3") is False
    assert _tiene_token("sería circular (P2 §2.d).", "ENTI") is False
    assert _tiene_token("ENCIG 2023, ... P8_3_1/2/3", "P8_3_1") is True
    assert _tiene_token("ENCIG 2023, ... P8_3_1/2/3", "ENCIG") is True


def test_falsos_positivos_de_subcadena_quedan_no_emite():
    """Reproduce el emparejamiento fila por fila para los tres casos de
    DERIVACION-M-v1_0.md sin pasar por el CSV del marco: cada hit citado
    en el hallazgo debe fallar la coincidencia de encuesta o de token."""
    lineas = RUTA_PROCEDENCIA.read_text(encoding="utf-8").splitlines()
    casos_falso_positivo = [
        ("ENIF", "P7_1"),
        ("ENIF", "P5_3"),
        ("ENTI", "P2"),
    ]
    for encuesta, var in casos_falso_positivo:
        enc = _token_encuesta(encuesta)
        hits = [l for l in lineas if _tiene_token(l, var) and _tiene_token(l, enc)]
        assert hits == [], f"{encuesta}/{var} no debe emparejar tras la corrección"


def test_caso_positivo_de_control_sigue_emitiendo(tmp_path):
    salida = tmp_path / "crosswalk.tsv"
    n = construir_crosswalk(salida)
    assert n == 60
    filas = salida.read_text(encoding="utf-8").splitlines()
    civ01 = next(f for f in filas if f.startswith("CIV-01\t"))
    assert "CANDIDATO-EMITE" in civ01
    assert "procedencia.yaml:937" in civ01
