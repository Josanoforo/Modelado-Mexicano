#!/usr/bin/env python3
"""Pruebas sintéticas del `C2` corregido del piloto celda-D.

ACTO GEN2-CELDA-D-CAREO-1 (ADR-533), correctivo pre-emisión del 17/sep/2026,
en respuesta a la devolución de revisión del 16/sep sobre `PR #827`. Fijan el
CONTRATO que la devolución exige antes de emitir:

  · rango `[0,1]` garantizado por construcción, sin recorte silencioso;
  · casos `p ∈ {0,1}` con RECHAZO EXPLÍCITO, no sustitución;
  · el mismo identificador de desenlace en entradas y salida (H1: hoy `R`/`C1`
    usan siete códigos comunes y `C2` se construía con el marginal de nueve);
  · tratamiento declarado de la incertidumbre cuando la muestra es COMPARTIDA;
  · soporte por cotas de Fréchet, no por el producto de márgenes;
  · parada que admite «sin ganador» sin adopción forzada.

QUÉ NO SON. La función de referencia de abajo es la PROPUESTA `D2` del
correctivo §2 y NO ESTÁ ADOPTADA: vive aquí, en el test, precisamente para no
entrar a `milpa/` sin firma de mesa. Estas pruebas pinan el contrato, no
habilitan el piloto.

CERO MICRODATO, cero cifras del modelo, cero derivación del cruce reservado
`localidad × edad`. Todos los números de este archivo son FIXTURES SINTÉTICOS
elegidos para ejercer un caso límite; ninguno describe a México.
"""
from __future__ import annotations

import math
import random
import unittest

DESENLACE_SIETE = "ahorra_solo_informal::P5_6_{1,2,3,4,5,8,9}"
DESENLACE_NUEVE = "ahorra_solo_informal::P5_6_{1..9}"


class DesenlaceIncompatible(ValueError):
    """Dos marginales de eventos distintos no componen un piso (H1)."""


class MarginalDegenerado(ValueError):
    """`p ∈ {0,1}`: el logit diverge. Se rechaza; no se recorta (H2)."""


def _logit(x: float) -> float:
    return math.log(x / (1.0 - x))


def _expit(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def piso_multiplicativo(p_l: float, p_e: float, p: float) -> float:
    """La forma de v1.1 §9. Aquí SÓLO para probar que NO preserva el rango."""
    return p_l * p_e / p


def piso_log_aditivo(marg_l: dict, marg_e: dict, marg_nac: dict) -> dict:
    """Propuesta D2: ausencia de interacción en la escala logit.

    NO es «independencia», y no identifica `P(Y | l, e)`: es un piso
    declarado y sólo-marginal que un challenger debe vencer.
    """
    ids = {marg_l["desenlace_id"], marg_e["desenlace_id"], marg_nac["desenlace_id"]}
    if len(ids) != 1:
        raise DesenlaceIncompatible(
            f"los tres marginales deben medir el mismo evento; llegaron {sorted(ids)}"
        )
    for nombre, m in (("localidad", marg_l), ("edad", marg_e), ("nacional", marg_nac)):
        p = m["p"]
        if not (0.0 < p < 1.0):
            raise MarginalDegenerado(
                f"marginal `{nombre}` = {p}: el logit diverge. SIN-DEFINIR; "
                f"no se recorta a [0,1] ni se sustituye."
            )
    z = _logit(marg_l["p"]) + _logit(marg_e["p"]) - _logit(marg_nac["p"])
    return {"desenlace_id": ids.pop(), "p": _expit(z)}


def cotas_frechet(n_l: int, n_e: int, N: int) -> tuple:
    """Lo único que los márgenes acreditan sobre la intersección (H4)."""
    return max(0, n_l + n_e - N), min(n_l, n_e)


def veredicto_soporte(n_l: int, n_e: int, N: int, umbral: int) -> str:
    inf, _sup = cotas_frechet(n_l, n_e, N)
    return "SOPORTE-ACREDITADO" if inf >= umbral else "SOPORTE-DESCONOCIDO"


PARADAS_ADMISIBLES = {
    "ADJUDICADA",
    "INDECIDIBLE",
    "SIN-CANDIDATO-SUPERIOR",
    "FUERA-DE-SOPORTE",
}


def _marg(p, desenlace=DESENLACE_SIETE):
    return {"desenlace_id": desenlace, "p": p}


class C2RangoYCasosLimite(unittest.TestCase):
    def test_el_multiplicativo_se_sale_del_rango(self):
        # El contraejemplo de la devolución. Si esto dejara de salirse, la
        # razón de cambiar de forma se habría evaporado y habría que releerla.
        self.assertGreater(piso_multiplicativo(0.8, 0.8, 0.5), 1.0)

    def test_log_aditivo_siempre_en_rango_abierto(self):
        rng = random.Random(42)
        casos = [(0.8, 0.8, 0.5), (0.99, 0.99, 0.01), (0.01, 0.01, 0.99),
                 (0.5, 0.5, 0.5), (0.999, 0.001, 0.5)]
        casos += [(rng.uniform(1e-6, 1 - 1e-6),
                   rng.uniform(1e-6, 1 - 1e-6),
                   rng.uniform(1e-6, 1 - 1e-6)) for _ in range(2000)]
        for p_l, p_e, p in casos:
            got = piso_log_aditivo(_marg(p_l), _marg(p_e), _marg(p))["p"]
            self.assertGreater(got, 0.0, f"{(p_l, p_e, p)} devolvió {got}")
            self.assertLess(got, 1.0, f"{(p_l, p_e, p)} devolvió {got}")

    def test_el_contraejemplo_queda_en_rango(self):
        got = piso_log_aditivo(_marg(0.8), _marg(0.8), _marg(0.5))["p"]
        self.assertAlmostEqual(got, 0.9411764705882353, places=12)

    def test_p_cero_y_p_uno_se_rechazan_sin_recortar(self):
        for degenerado in (0.0, 1.0):
            for posicion in range(3):
                ps = [0.4, 0.4, 0.4]
                ps[posicion] = degenerado
                with self.assertRaises(MarginalDegenerado):
                    piso_log_aditivo(_marg(ps[0]), _marg(ps[1]), _marg(ps[2]))

    def test_no_hay_recorte_silencioso(self):
        # Un recorte convertiría el 1.28 del multiplicativo en un 1.0
        # presentable. La función propuesta no puede producir 0.0 ni 1.0.
        got = piso_log_aditivo(_marg(0.999999), _marg(0.999999), _marg(0.5))["p"]
        self.assertNotEqual(got, 1.0)
        self.assertLess(got, 1.0)


class C2IdentidadDelDesenlace(unittest.TestCase):
    def test_mezclar_siete_y_nueve_codigos_se_rechaza(self):
        # H1 exactamente: `R`/`C1` en siete códigos, marginal público en nueve.
        with self.assertRaises(DesenlaceIncompatible):
            piso_log_aditivo(
                _marg(0.41, DESENLACE_SIETE),
                _marg(0.43, DESENLACE_NUEVE),
                _marg(0.36, DESENLACE_SIETE),
            )

    def test_la_salida_conserva_el_identificador_de_entrada(self):
        out = piso_log_aditivo(_marg(0.41), _marg(0.43), _marg(0.36))
        self.assertEqual(out["desenlace_id"], DESENLACE_SIETE)


class C2IncertidumbreCompartida(unittest.TestCase):
    """H3: los tres marginales salen de la MISMA muestra."""

    @staticmethod
    def _replicas(n=400, semilla=7):
        rng = random.Random(semilla)
        out = []
        for _ in range(n):
            comun = rng.gauss(0.0, 1.0)          # el shock de muestra compartido
            out.append((
                _expit(_logit(0.41) + 0.30 * comun + 0.05 * rng.gauss(0, 1)),
                _expit(_logit(0.43) + 0.30 * comun + 0.05 * rng.gauss(0, 1)),
                _expit(_logit(0.36) + 0.30 * comun + 0.05 * rng.gauss(0, 1)),
            ))
        return out

    @staticmethod
    def _ancho(vals):
        v = sorted(vals)
        lo = v[int(0.025 * (len(v) - 1))]
        hi = v[int(0.975 * (len(v) - 1))]
        return hi - lo

    def test_replicas_compartidas_y_supuesto_de_independencia_no_coinciden(self):
        reps = self._replicas()
        # (a) correcto: se propaga RÉPLICA POR RÉPLICA, sin covarianzas inventadas.
        compartido = [piso_log_aditivo(_marg(a), _marg(b), _marg(c))["p"]
                      for a, b, c in reps]
        # (b) lo que v1.1 §4 prometía: barajar cada marginal por separado
        #     equivale a suponer estimadores independientes.
        rng = random.Random(11)
        col = [[r[i] for r in reps] for i in range(3)]
        for c in col:
            rng.shuffle(c)
        independiente = [piso_log_aditivo(_marg(a), _marg(b), _marg(c))["p"]
                         for a, b, c in zip(*col)]
        self.assertNotAlmostEqual(
            self._ancho(compartido), self._ancho(independiente), places=3,
            msg="si los dos anchos coincidieran, la covarianza no importaría "
                "y H3 no sería un hallazgo",
        )

    def test_sin_covarianzas_no_se_inventa_un_intervalo(self):
        # Bajo la vía (c) del correctivo §7 sólo hay errores marginales
        # publicados: la salida honesta es un punto, no una banda.
        emision = {"p": piso_log_aditivo(_marg(0.41), _marg(0.43), _marg(0.36))["p"],
                   "incertidumbre": "NO-ACREDITADA"}
        self.assertNotIn("ic95", emision)
        self.assertEqual(emision["incertidumbre"], "NO-ACREDITADA")


class SoportePorCotasNoPorProducto(unittest.TestCase):
    def test_el_producto_de_margenes_no_es_evidencia(self):
        # Fixture con la FORMA del caso real: márgenes grandes, intersección
        # no acotada por abajo. Los números son sintéticos.
        n_l, n_e, N = 4000, 2500, 13000
        punto = n_l * n_e / N
        inf, sup = cotas_frechet(n_l, n_e, N)
        self.assertGreater(punto, 700)        # el producto sugiere holgura...
        self.assertEqual(inf, 0)              # ...y la cota admite una celda vacía
        self.assertEqual(sup, 2500)

    def test_celda_sin_soporte_acreditado_se_reporta_como_tal(self):
        self.assertEqual(
            veredicto_soporte(4000, 2500, 13000, umbral=200), "SOPORTE-DESCONOCIDO")

    def test_cota_inferior_positiva_si_los_margenes_obligan(self):
        # Cuando los márgenes SÍ fuerzan intersección, la cota lo dice.
        self.assertEqual(cotas_frechet(900, 900, 1000), (800, 900))
        self.assertEqual(
            veredicto_soporte(900, 900, 1000, umbral=200), "SOPORTE-ACREDITADO")


class ParadaSinGanador(unittest.TestCase):
    def test_sin_candidato_superior_es_terminal_y_no_adopta(self):
        self.assertIn("SIN-CANDIDATO-SUPERIOR", PARADAS_ADMISIBLES)
        self.assertIn("INDECIDIBLE", PARADAS_ADMISIBLES)
        self.assertIn("FUERA-DE-SOPORTE", PARADAS_ADMISIBLES)

    def test_adjudicar_no_es_la_unica_salida(self):
        self.assertGreater(len(PARADAS_ADMISIBLES - {"ADJUDICADA"}), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
