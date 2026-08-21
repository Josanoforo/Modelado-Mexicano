"""Aceptación de `R3.4` — el gate de Fase 1 (ADR-37 / milpa-spec §10.1).

Tres condiciones, verbatim de gobernanza:267+ — "(A) Reproducción... la
adopción tipo CoDi queda <10% de la del canal retail-efectivo. (B) Prueba de
mecanismo — al apagar riesgo_fiscal_percibido con el canal constante, la
brecha debe colapsar ≥70%. (C) Anti-confusión — al apagar el canal de
confianza personal con riesgo_fiscal_percibido encendido, la brecha debe
PERSISTIR (se reduce <30%). El gate pasa solo si A y B y C." Umbrales
ASIGNADOS, no medidos (spec §10.1: "no salen de ningún dato").

Límite pre-registrado que la ficha de R3.4 heredará (hitoD Nota 3, verbatim):
el gate no separa coerción de fricción; `riesgo_fiscal_percibido` captura
solo el primer componente. Se declara, no se resuelve aquí.

Diseño de este harness (diseño v1.0 §5, firmado): PRIMERO el assert
anti-NO_COVERAGE — "un gate que no distingue cuál de dos mecanismos lo hizo
pasar no es un gate: es un espejo", y uno que pasa por hueco de cobertura es
peor. La condición A queda en xfail ESTRICTO nombrando los dos huecos que
suben a mesa (H1: el comparador retail-efectivo es NO-EMITE en la capa
máquina; H2: spec dice OXXO, el Registro §7 enuncia SPEI) — el día que mesa
firme el comparador y exista en máquina, este xfail truena en XPASS y obliga
a quitarle la marca: el estado del gate nunca queda en silencio.
"""
import pytest

from milpa.src import emisor


@pytest.fixture(scope="module")
def gate() -> emisor.GateR34:
    return emisor.gate_r3_4()


def test_0_sin_no_coverage_en_las_corridas_del_gate(gate):
    """Anti-NO_COVERAGE primero: si esto falla, el impedimento queda nombrado
    con la regla ausente — y nada de lo que sigue vale."""
    perdidas = [h for h in gate.huecos if h.startswith("NO_COVERAGE") or h.startswith("CONFLICTO")]
    assert not perdidas, f"el gate no puede correr por pérdida de cobertura: {perdidas}"
    assert gate.adopcion_codi_A == pytest.approx(0.09)
    assert gate.adopcion_pareja_util == pytest.approx(0.71)


def test_B_mecanismo_colapso_de_brecha(gate):
    """B: apagar `riesgo_fiscal_percibido` (canal constante) → colapso ≥70%
    (umbral ASIGNADO). En la capa máquina la brecha ES el mecanismo §3.3, así
    que colapsa completa — 100% ≥ 70%."""
    assert gate.colapso_B is not None
    assert gate.colapso_B >= emisor.UMBRAL_B_COLAPSO
    assert gate.pasa_B is True


def test_C_anticonfusion_brecha_persiste(gate):
    """C: apagar el canal de confianza personal (switch de generador G1a,
    delta v1.1 firmado) con riesgo encendido → reducción <30% (umbral
    ASIGNADO). PASA — y el harness DECLARA la trivialidad en vez de
    esconderla: las p del dominio §3.3 no cargan G1a, así que la reducción es
    0% por construcción; un C no-trivial exige el enlace índice→adopción
    (h_r), que es OLA futura y está nombrado en gate.notas."""
    assert gate.reduccion_C is not None
    assert gate.reduccion_C < emisor.UMBRAL_C_REDUCCION
    assert gate.pasa_C is True
    assert any("trivial" in n for n in gate.notas)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "A no adjudicable hoy — dos huecos a mesa, nombrados por el emisor: "
        "H1 · el comparador de A ('adopción por canal retail-efectivo tipo "
        "OXXO Pay', spec §10.1) es NO-EMITE en la capa máquina (universo: "
        "tramite.yaml + procedencia.yaml, 20/ago/2026) — candidata a UN acto "
        "de promoción prosa→máquina. H2 · discrepancia de comparador: spec "
        "§10.1 dice OXXO (retail), Registro §7 enuncia 'CoDi vs. útil (SPEI)' "
        "— cuál rige es firma de mesa. Diagnóstico bajo lectura pareja-SPEI "
        "(no adjudica): 0.09/0.71 = 12.7% ≥ 10% — tampoco pasaría. Cuando el "
        "comparador exista y esté firmado, este xfail ESTRICTO truena en "
        "XPASS y obliga a retirar la marca."),
)
def test_A_reproduccion_contra_comparador_firmado(gate):
    assert gate.adopcion_retail is not None, "; ".join(gate.huecos)
    assert gate.adopcion_codi_A < emisor.UMBRAL_A_RAZON * gate.adopcion_retail


def test_los_huecos_estan_nombrados_no_callados(gate):
    """El veredicto de hoy es NO-ADJUDICADO con huecos a la vista — nunca un
    verde que esconda el estado real del gate."""
    assert any(h.startswith("H1") for h in gate.huecos)
    assert any(h.startswith("H2") for h in gate.huecos)
    assert "NO-ADJUDICADO" in gate.veredicto
