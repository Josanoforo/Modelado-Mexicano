"""Fidelidad del emisor (EMISOR-M-1): las tres fuentes-máquina se consumen
sin distorsión. Cada aserción cita su fuente; ninguna cifra esperada se
teclea de memoria sin ancla — las constantes de abajo vienen del propio
árbol (tramite.yaml header v0.3.0: "Las 10 probabilidades... (5 reglas × 2)";
modelo:8 VERIFICAS ASÍ: "§7 trae el Registro congelado de IDs (tabla de 49
filas)") y el test es el comando que las re-deriva."""
from pathlib import Path

import pytest

from milpa.src import emisor

RAIZ = Path(__file__).resolve().parents[1]


def test_tramite_cinco_reglas_diez_probabilidades():
    reglas = emisor.cargar_reglas()
    assert len(reglas) == 5, "tramite.yaml declara 5 reglas (header v0.2.0/v0.3.0)"
    ps = [s.p for r in reglas for s in r.entonces if s.p is not None]
    assert len(ps) == 10, "header v0.3.0: 'Las 10 probabilidades de este archivo (5 reglas × 2)'"
    assert all(s.clase == "ASIGNADO" for r in reglas for s in r.entonces), \
        "v0.3.0: TODO p gana clase ASIGNADO"


def test_dos_niveles_presentes_en_la_pareja_del_gate():
    """El esquema ya separa niveles (verificación de sesión, 20/ago):
    disparadores = globales; contexto_* = palancas (ADR-26)."""
    reglas = {r.id: r for r in emisor.cargar_reglas()}
    coer = reglas["tramite.gobierno_digital.coercitivo"]
    assert dict(coer.disparadores) == {"cobertura_formal": False}
    assert dict(coer.palancas) == {"coercitivo": True, "riesgo_fiscal_percibido": True}
    assert coer.palancas_origen == ("contexto_producto",)
    espejo = reglas["tramite.gobierno_digital.util_sin_coercion"]
    assert dict(espejo.palancas) == {"coercitivo": False, "riesgo_fiscal_percibido": False}, \
        "la regla espejo (anti-NO_COVERAGE del gate) debe estar restituida"


def test_registro_7_49_ids_unicos_incluye_r34():
    filas = emisor.parsear_registro_7()
    assert len(filas) == 49, f"modelo:8 declara tabla de 49 filas; el parser vio {len(filas)}"
    assert "R3.4" in filas
    assert "MEDIA-FUERTE" in filas["R3.4"].tier
    assert "el gate" in filas["R3.4"].enunciado


def test_registro_7_filas_verbatim_en_el_archivo():
    """El parser copia, no transcribe: cada fila cruda existe byte a byte en
    el canon. Si esto falla, el parser está inventando — el defecto Hito 2."""
    texto = emisor.RUTA_MODELO.read_text(encoding="utf-8")
    filas = emisor.parsear_registro_7()
    for f in filas.values():
        assert f.cruda in texto, f"fila de {f.id} no existe verbatim en modelo"


def test_evaluar_es_determinista():
    reglas = emisor.cargar_reglas()
    a = emisor.evaluar(reglas, emisor.SIT_GOB, {"cobertura_formal": False}, emisor.CTX_A)
    b = emisor.evaluar(reglas, emisor.SIT_GOB, {"cobertura_formal": False}, emisor.CTX_A)
    assert a == b
    assert a.estado == "EMITE"
    assert a.p_de("adopta") == pytest.approx(0.09)


def test_no_coverage_es_salida_explicita_no_silencio():
    """Combo TF de palancas: ninguna regla lo cubre — el bucle lo DICE con el
    contexto a la vista (gobernanza:275: un gate no puede pasar por pérdida
    de cobertura sin que nadie lo vea)."""
    reglas = emisor.cargar_reglas()
    r = emisor.evaluar(reglas, emisor.SIT_GOB, {},
                       {"coercitivo": True, "riesgo_fiscal_percibido": False})
    assert r.estado == "NO_COVERAGE"
    assert "coercitivo" in r.detalle and "riesgo_fiscal_percibido" in r.detalle
    with pytest.raises(LookupError):
        r.p_de("adopta")


def test_apagar_generador_es_puro_y_conserva_sin_magnitud():
    detalle = [
        {"gen": "G1", "coefs": {"confianza_institucional": -0.60, "radio_confianza": -0.35}},
        {"gen": "G5", "coefs": {"familismo_apoyo": 0.50,
                                "familismo_obligacion": "signo negativo o no monotónico — SIN MAGNITUD"}},
    ]
    copia = [dict(d, coefs=dict(d["coefs"])) for d in detalle]
    apagado = emisor.apagar_generador(detalle, "G1")
    assert detalle == copia, "la función no debe mutar su entrada"
    g1 = next(c for c in apagado if c["gen"] == "G1")
    assert g1["coefs"] == {"confianza_institucional": 0.0, "radio_confianza": 0.0}
    g5 = next(c for c in apagado if c["gen"] == "G5")
    assert g5["coefs"]["familismo_obligacion"].startswith("signo negativo"), \
        "SIN MAGNITUD se conserva: cero también es una magnitud, y no la tiene"


def test_emision_binaria_forma_prediccion_corredor():
    """Campos núcleo idénticos a PrediccionCorredor (corredor-E): E solo exige
    valor_punto; la clase viaja como confianza cualitativa (IPCC), el intervalo
    queda None sin EE real (Q1-bis)."""
    reglas = {r.id: r for r in emisor.cargar_reglas()}
    p = emisor.emitir_binaria(reglas["tramite.gobierno_digital.util_sin_coercion"], "adopta")
    assert (p.tipo_escala, p.valor_punto, p.clase) == ("binaria", 0.71, "ASIGNADO")
    assert p.intervalo_lo is None and p.intervalo_hi is None
    assert p.confianza_declarada is None, "la clase NO se convierte a número (doctrina IPCC)"


def test_estampa_de_base_empirica_en_el_gate():
    """Advertencia de mesa (20/ago/2026): un cálculo correcto sobre insumos
    sin base medida no debe poder confundirse con uno medido. El gate deriva
    la clase de procedencia de cada probabilidad que consumió y la estampa en
    el resultado: hoy, 2 de 2 ASIGNADO y base medida 0 de 2. El día que un
    coeficiente del par gradúe a MEDIDO, este test truena y obliga a leer la
    estampa nueva — es la parte que se actualiza sola."""
    g = emisor.gate_r3_4()
    assert dict(g.insumos_clase) == {"ASIGNADO": 2}
    assert "base medida: 0 de 2" in g.estampa
    assert "estructurales" in g.estampa, \
        "la estampa debe decir que B y C son propiedades del par asignado, no hallazgos"
