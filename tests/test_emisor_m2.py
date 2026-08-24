"""Tests del vocabulario EMISOR-M-2 (variables dependientes + disparadores por
componente) — ACTO EMISOR-M-2 · 24/ago/2026.

T3(a) celda sin DV → rechazo. T3(b) celda con DV + disparadores bien
formados → pasa validación de forma, sin adjudicar nada. T3(c) verificado
por separado: los tests existentes del emisor (test_emisor_fidelidad.py,
aceptacion_r3_4.py) siguen corriendo sin tocarse en este acto.
"""
from milpa.src import emisor


def test_celda_tec_sin_dv_se_rechaza():
    celda = {"dominio": "TEC", "estimando": "x"}
    errs = emisor.valida_dv_celda_m2(celda, "celda-sin-dv.yaml")
    assert errs, "una celda TEC sin variable_dependiente debe producir error"
    assert any("EMISOR-M-2" in e for e in errs)


def test_celda_tec_con_dv_invalida_se_rechaza():
    celda = {"dominio": "TEC", "variable_dependiente": "obediencia"}
    errs = emisor.valida_dv_celda_m2(celda, "celda-dv-mala.yaml")
    assert errs
    assert any("variable_dependiente inválida" in e for e in errs)


def test_celda_tec_con_dv_y_disparadores_bien_formados_pasa():
    celda = {
        "dominio": "TEC",
        "variable_dependiente": "adopcion",
        "disparadores_m2": {
            "riesgo_fiscal_percibido": True,
            "friccion_uso": False,
            "lado_obligado": "usuario",
            "sancion": "bloqueo",
            "dato_sensible": "identificador",
        },
    }
    errs = emisor.valida_dv_celda_m2(celda, "celda-bien-formada.yaml")
    assert errs == ()


def test_celda_dominio_no_cubierto_no_exige_dv():
    celda = {"dominio": "FIN", "estimando": "x"}
    errs = emisor.valida_dv_celda_m2(celda, "celda-fin.yaml")
    assert errs == ()


def test_disparador_m2_desconocido_se_rechaza():
    celda = {
        "dominio": "TEC",
        "variable_dependiente": "cumplimiento",
        "disparadores_m2": {"variable_inventada": True},
    }
    errs = emisor.valida_dv_celda_m2(celda, "celda-disparador-malo.yaml")
    assert any("desconocido" in e for e in errs)


def test_disparador_m2_enum_invalido_se_rechaza():
    celda = {
        "dominio": "TEC",
        "variable_dependiente": "cumplimiento",
        "disparadores_m2": {"lado_obligado": "ambos"},
    }
    errs = emisor.valida_dv_celda_m2(celda, "celda-enum-malo.yaml")
    assert any("inválido" in e for e in errs)


def test_estampa_base_extendida_reporta_los_seis_disparadores():
    texto = emisor.estampa_base_extendida_m2()
    for disparador in emisor.DISPARADORES_COMPONENTE_M2:
        assert disparador in texto
    # T2: la respuesta esperable es "casi ninguno" -- no se maquilla.
    assert "casi ninguno" in texto
