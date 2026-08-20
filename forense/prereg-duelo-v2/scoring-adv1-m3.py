#!/usr/bin/env python3
"""
`ADV1-M3` (+ `M3-bis`) · scoring propio con el árbitro incierto adentro.

ACTO: DUELO-PREREG-V2 (nube, Opus). Escrito 20/ago/2026. Gate: T-SELLO + ACT-PIL-2 fusionados.

*** ESTE SCRIPT NO SE EJECUTA EN ESTE ACTO. *** Pre-registro ejecutable de la
función de scoring -- se congela ANTES de que exista una sola celda de R,
para que nadie pueda ajustar la regla de puntuación después de ver el dato.

Fuente normativa, verbatim (CAREO-ADV-DUELO-diseno-v2-2026-08-19.md §B, M3):

    "M3 · Scoring propio con el árbitro incierto adentro. Por celda:
    skill = 1 - error/error(B); CRPS/interval-score en continuas, Brier en
    categóricas, evaluado contra R como distribución (Normal(R̂, EE) o su
    IC), nunca contra el punto. INDECIDIBLE si ambos caen dentro del IC de
    R o si |d_L-d_M| < 0.5*EE(R). Calibración (cobertura empírica de
    intervalos al 80%) reportada como resultado independiente. M3-bis,
    secundario: donde R es microdato, distancia de forma (KS/Wasserstein),
    razón de varianzas como alarma de aplanamiento, y >=1 corte por
    subgrupo mexicano por celda."

Nota de precedencia (ver `forense/prereg-duelo-v2/mesa-pendientes.md` §2):
este script calcula las cinco condiciones de `ADV1-M5` de forma
independiente y NO las compone en una etiqueta única por celda -- la
composición/precedencia entre casillas queda pendiente de mesa.
"""
from __future__ import annotations

import dataclasses
import math
from typing import Literal


# --------------------------------------------------------------------------
# 1 · R como distribución -- NUNCA como punto (M3, textual: "nunca contra
#     el punto"). R̂ es el estimador puntual del árbitro, EE su error
#     estándar; se modela como Normal(R̂, EE) salvo que la celda traiga un
#     IC empírico propio (microdato), en cuyo caso se usa ese IC.
# --------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ArbitroR:
    """La distribución del árbitro para una celda. NUNCA se colapsa a un
    solo número al puntuar -- eso es exactamente el defecto que M3
    corrige (CAREO §A: "Scoring impropio · árbitro sin incertidumbre ·
    sin calibración", 5/5 corridas adversariales)."""

    r_hat: float
    ee: float  # error estándar REAL del árbitro para esta celda (nunca de diseño)
    ic_lo_80: float | None = None  # IC empírico al 80% si viene de microdato
    ic_hi_80: float | None = None

    def ic_80(self) -> tuple[float, float]:
        if self.ic_lo_80 is not None and self.ic_hi_80 is not None:
            return (self.ic_lo_80, self.ic_hi_80)
        # Normal(r_hat, ee), z_0.90 ~= 1.2816 para IC central al 80%
        z = 1.2815515655446004
        return (self.r_hat - z * self.ee, self.r_hat + z * self.ee)

    def dentro_del_ic(self, valor: float, nivel_z: float = 1.2815515655446004) -> bool:
        lo, hi = self.ic_80() if nivel_z == 1.2815515655446004 else (
            self.r_hat - nivel_z * self.ee, self.r_hat + nivel_z * self.ee
        )
        return lo <= valor <= hi


# --------------------------------------------------------------------------
# 2 · skill = 1 - error/error(B) -- relativo al baseline, nunca absoluto.
# --------------------------------------------------------------------------


def skill(error_corredor: float, error_baseline: float) -> float | None:
    """skill = 1 - error/error(B). Si error(B) == 0, skill es indefinido
    (no se sustituye por 0 ni por infinito -- se reporta None y se declara)."""
    if error_baseline == 0:
        return None
    return 1.0 - (error_corredor / error_baseline)


# --------------------------------------------------------------------------
# 3 · CRPS / interval-score (continuas) y Brier (categóricas), evaluados
#     contra R como distribución.
# --------------------------------------------------------------------------


def interval_score(lo: float, hi: float, valor_real: float, alpha: float = 0.20) -> float:
    """Interval score (Gneiting & Raftery 2007) para un intervalo de
    predicción [lo, hi] al nivel (1-alpha). Penaliza ancho y cobertura a
    la vez -- sustituto cerrado del CRPS cuando el corredor solo emite un
    intervalo, no una distribución completa."""
    ancho = hi - lo
    penal_lo = (2.0 / alpha) * max(0.0, lo - valor_real)
    penal_hi = (2.0 / alpha) * max(0.0, valor_real - hi)
    return ancho + penal_lo + penal_hi


def crps_normal_aprox(pred_media: float, pred_sd: float, valor_real: float) -> float:
    """CRPS de una predicción Normal(pred_media, pred_sd) contra un valor
    real puntual -- fórmula cerrada estándar. Usado cuando el corredor
    emite punto+intervalo que se puede leer como Normal; si el corredor
    solo emite un punto sin incertidumbre, usar interval_score con un
    intervalo degenerado o declarar NO EVALUABLE (no se le inventa SD)."""
    if pred_sd <= 0:
        raise ValueError("CRPS cerrado exige SD > 0 -- un punto sin incertidumbre no es evaluable así; usar interval_score o declarar NO EVALUABLE.")
    z = (valor_real - pred_media) / pred_sd
    # Aproximación de la fórmula cerrada del CRPS normal (Gneiting & Raftery 2007, eq. 21)
    phi = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)  # densidad normal estándar
    Phi = 0.5 * (1 + math.erf(z / math.sqrt(2)))            # cdf normal estándar
    return pred_sd * (z * (2 * Phi - 1) + 2 * phi - 1 / math.sqrt(math.pi))


def brier_score(prob_predicha: float, ocurrio: bool) -> float:
    """Brier score estándar para categóricas/binarias: (p - o)^2, o en {0,1}."""
    o = 1.0 if ocurrio else 0.0
    return (prob_predicha - o) ** 2


# --------------------------------------------------------------------------
# 4 · INDECIDIBLE -- las dos condiciones exactas del texto, ninguna
#     aplanada ni sustituida por una sola.
# --------------------------------------------------------------------------


def es_indecidible(
    valor_L: float, valor_M: float, arbitro: ArbitroR,
) -> tuple[bool, dict]:
    """INDECIDIBLE si (condición 1) AMBOS caen dentro del IC de R, O
    (condición 2) |d_L - d_M| < 0.5*EE(R). Las dos condiciones se
    verifican por separado y se reportan por separado -- una celda puede
    cumplir una, la otra, ambas, o ninguna; el resultado NUNCA se colapsa
    a un solo booleano sin dejar rastro de cuál condición disparó."""
    lo, hi = arbitro.ic_80()
    cond1_ambos_en_ic = (lo <= valor_L <= hi) and (lo <= valor_M <= hi)

    d_L = abs(valor_L - arbitro.r_hat)
    d_M = abs(valor_M - arbitro.r_hat)
    cond2_diferencia_menor_medio_ee = abs(d_L - d_M) < 0.5 * arbitro.ee

    return (cond1_ambos_en_ic or cond2_diferencia_menor_medio_ee), {
        "condicion_1_ambos_en_ic_R": cond1_ambos_en_ic,
        "condicion_2_diferencia_bajo_0.5EE": cond2_diferencia_menor_medio_ee,
        "d_L": d_L, "d_M": d_M, "ic_80_R": (lo, hi),
    }


# --------------------------------------------------------------------------
# 5 · Calibración al 80% -- resultado INDEPENDIENTE, no un ingrediente del
#     skill. Se reporta por corredor, agregado sobre todas las celdas
#     puntuadas del piloto.
# --------------------------------------------------------------------------


@dataclasses.dataclass
class RegistroCalibracion:
    corredor: Literal["L", "M", "B", "E"]
    id_celda: str
    valor_real: float
    intervalo_lo: float
    intervalo_hi: float

    def cubierto(self) -> bool:
        return self.intervalo_lo <= self.valor_real <= self.intervalo_hi


def calibracion_80(registros: list[RegistroCalibracion]) -> dict:
    """Cobertura empírica de intervalos al 80% -- si el corredor está bien
    calibrado, ~80% de las celdas deberían tener el valor real dentro de
    su intervalo declarado. Se reporta la cifra cruda, sin blanquear
    sub- o sobre-cobertura."""
    if not registros:
        return {"n": 0, "cobertura_empirica": None}
    cubiertos = sum(1 for r in registros if r.cubierto())
    return {
        "n": len(registros),
        "cubiertos": cubiertos,
        "cobertura_empirica": cubiertos / len(registros),
        "objetivo": 0.80,
        "desviacion_del_objetivo": (cubiertos / len(registros)) - 0.80,
    }


# --------------------------------------------------------------------------
# 6 · M3-bis, secundario y distribucional -- solo donde R es microdato.
#     Distancia de forma (KS/Wasserstein), razón de varianzas, >=1 corte
#     por subgrupo mexicano por celda.
# --------------------------------------------------------------------------


def distancia_ks(muestra_a: list[float], muestra_b: list[float]) -> float:
    """Estadístico de Kolmogorov-Smirnov (distancia máxima entre CDFs
    empíricas) -- implementación directa O(n log n), sin dependencias
    externas (scipy no se asume disponible)."""
    a = sorted(muestra_a)
    b = sorted(muestra_b)
    todos = sorted(set(a) | set(b))
    max_dif = 0.0
    for x in todos:
        cdf_a = sum(1 for v in a if v <= x) / len(a) if a else 0.0
        cdf_b = sum(1 for v in b if v <= x) / len(b) if b else 0.0
        max_dif = max(max_dif, abs(cdf_a - cdf_b))
    return max_dif


def distancia_wasserstein_1d(muestra_a: list[float], muestra_b: list[float]) -> float:
    """Distancia de Wasserstein-1 en una dimensión = integral de |CDF_a -
    CDF_b|, calculable exactamente ordenando ambas muestras (caso 1D,
    sin necesidad de programación lineal)."""
    a = sorted(muestra_a)
    b = sorted(muestra_b)
    if len(a) != len(b):
        # interpolación simple a un grid común de percentiles
        n = max(len(a), len(b))
        a = [a[min(len(a) - 1, int(i * len(a) / n))] for i in range(n)]
        b = [b[min(len(b) - 1, int(i * len(b) / n))] for i in range(n)]
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def razon_varianzas(muestra_corredor: list[float], muestra_R: list[float]) -> float | None:
    """Alarma de aplanamiento (Bisbee et al.): razón var(corredor)/var(R).
    Muy por debajo de 1 == el corredor sub-representa la varianza real
    (aplana la heterogeneidad); no se interpreta como "mejor" solo por
    tener menor varianza."""
    if len(muestra_R) < 2:
        return None
    var_r = _varianza_muestral(muestra_R)
    if var_r == 0:
        return None
    var_c = _varianza_muestral(muestra_corredor) if len(muestra_corredor) >= 2 else 0.0
    return var_c / var_r


def _varianza_muestral(valores: list[float]) -> float:
    n = len(valores)
    if n < 2:
        return 0.0
    media = sum(valores) / n
    return sum((v - media) ** 2 for v in valores) / (n - 1)


@dataclasses.dataclass
class CorteSubgrupo:
    """>=1 corte por subgrupo mexicano por celda -- M3-bis lo exige cuando
    R es microdato. El subgrupo lo declara la spec de la celda (M1: cuota
    de condicionales/subgrupo), no se inventa aquí."""

    nombre_subgrupo: str  # p.ej. "sexo", "entidad_federativa", "grado_escolar"
    ks: float
    wasserstein: float
    razon_varianzas: float | None


# --------------------------------------------------------------------------
# 7 · Ensamblado de un resultado por celda -- las cinco piezas de M3/M3-bis
#     juntas, sin componerlas en un veredicto único (eso es ADV1-M5 y su
#     precedencia, pendiente de mesa).
# --------------------------------------------------------------------------


@dataclasses.dataclass
class ResultadoCelda:
    id_celda: str
    skill_L: float | None
    skill_M: float | None
    indecidible: bool
    detalle_indecidible: dict
    m3_bis: list[CorteSubgrupo] = dataclasses.field(default_factory=list)


if __name__ == "__main__":
    raise SystemExit(
        "scoring-adv1-m3.py es pre-registro ejecutable de la función de "
        "puntuación, no un script para correr aquí. Se ejecuta solo "
        "después de que R exista, y solo con los hashes de L/M/B/E ya "
        "comprometidos (pipeline-L-adv1-m2.py, commit_hash_registry)."
    )
