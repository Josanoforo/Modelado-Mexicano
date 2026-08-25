#!/usr/bin/env python3
"""Scoring pareado y composición agregada de ``ADV1-M3``/``ADV1-M5 v2``.

Este módulo construye la maquinaria; no contiene ni puntúa celdas reales. La
entrada JSON tiene dos claves: ``configuracion`` y ``celdas``. La configuración
declara los cuatro corredores separados (L-solo, L+corpus, M y E), todas las
comparaciones L↔M, el scope adjudicante y los parámetros del bootstrap. Cada
celda declara ``id_celda``, ``estado`` y ``mediciones``; cada medición puede ser
un ``skill`` ya calculado o ``error`` junto con ``error_baseline`` en la celda.
Las mediciones forman una matriz celda × corredor. Cada marginal y cada
comparación materializa su propio universo estricto; no existe una intersección
global que exija L-solo, L+corpus, M y E simultáneamente.

Para efectos de adjudicación, PASO 1/PASO 2 operan sobre el scope adjudicante
predeclarado {L seleccionado, M}. L no seleccionado y E permanecen visibles
como resultados auxiliares. La selección del scope no tiene default ni puede
depender de resultados.

La salida JSON conserva la estructura completa. La salida TSV es una
representación determinista de sus hojas con columnas ``ruta`` y ``valor``.
Ambas se serializan en UTF-8 sin BOM, LF, orden estable y sin timestamps. Uso::

    python3 scoring-adv1-m3.py entrada.json --json salida.json --tsv salida.tsv

Las opciones de parámetros en CLI son aserciones, no overrides: si contradicen
la configuración, la ejecución falla cerrada. ``replicas`` usa el default
técnico visible ``10000`` cuando la clave se omite; seed, nivel_ic, delta y la
comparación principal nunca tienen default.
"""
from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import io
import json
import math
import random
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


REPLICAS_DEFAULT = 10_000
ESTADOS_INCLUIBLES = frozenset({"EVALUABLE", "INDECIDIBLE"})
CODIGO_SCOPE_AUSENTE = "SCOPE_ADJUDICANTE_NO_PREDECLARADO"
CODIGO_POSICION_NO_DEFINIDA = "POSICION_NO_DEFINIDA_POR_SPEC"
RESERVA_SCOPE = (
    "Para efectos de adjudicación, PASO 1/PASO 2 operan sobre el scope "
    "adjudicante predeclarado {L seleccionado, M}. L no seleccionado y E "
    "permanecen visibles como resultados auxiliares. La selección del scope "
    "no tiene default ni puede depender de resultados."
)


class ErrorScoring(ValueError):
    """Fallo técnico cerrado; ``codigo`` no es un veredicto del duelo."""

    def __init__(self, codigo: str, mensaje: str):
        super().__init__(f"{codigo}: {mensaje}")
        self.codigo = codigo
        self.mensaje = mensaje


@dataclasses.dataclass(frozen=True)
class CorredorActivo:
    id: str
    familia: str
    variante: str


@dataclasses.dataclass(frozen=True)
class ComparacionLM:
    id: str
    l_id: str
    m_id: str


@dataclasses.dataclass(frozen=True)
class Configuracion:
    corredores_activos: tuple[CorredorActivo, ...]
    comparaciones_l_m: tuple[ComparacionLM, ...]
    comparacion_principal_id: str
    e_id: str
    delta: float
    nivel_ic: float
    seed: int
    replicas: int = REPLICAS_DEFAULT

    @property
    def por_id(self) -> dict[str, CorredorActivo]:
        return {corredor.id: corredor for corredor in self.corredores_activos}

    @property
    def comparaciones_por_id(self) -> dict[str, ComparacionLM]:
        return {comparacion.id: comparacion for comparacion in self.comparaciones_l_m}

    @property
    def comparacion_principal(self) -> ComparacionLM:
        return self.comparaciones_por_id[self.comparacion_principal_id]

    @property
    def l_id_adjudicado(self) -> str:
        return self.comparacion_principal.l_id

    @property
    def m_id_adjudicado(self) -> str:
        return self.comparacion_principal.m_id

    @property
    def l_ids_no_seleccionados(self) -> tuple[str, ...]:
        return tuple(
            corredor.id
            for corredor in self.corredores_activos
            if corredor.familia == "L" and corredor.id != self.l_id_adjudicado
        )

    def normalizada(self) -> dict[str, Any]:
        return {
            "comparacion_principal_id": self.comparacion_principal_id,
            "comparaciones_l_m": [dataclasses.asdict(valor) for valor in self.comparaciones_l_m],
            "corredores_activos": [dataclasses.asdict(valor) for valor in self.corredores_activos],
            "delta": self.delta,
            "e_id": self.e_id,
            "nivel_ic": self.nivel_ic,
            "replicas": self.replicas,
            "seed": self.seed,
        }

    @property
    def hash_configuracion(self) -> str:
        canonico = json.dumps(
            self.normalizada(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(canonico).hexdigest()


@dataclasses.dataclass(frozen=True)
class CeldaMedida:
    """Fila validada de la matriz celda × corredor, sin intersección global."""

    id_celda: str
    estado: str
    skills: dict[str, float]
    cobertura_r: dict[str, bool | None]


@dataclasses.dataclass(frozen=True)
class MatrizMediciones:
    celdas: tuple[CeldaMedida, ...]


@dataclasses.dataclass(frozen=True)
class CeldaPareada:
    """Celda incluida en un scope explícito, solo con sus corredores extremos."""

    id_celda: str
    estado: str
    skills: dict[str, float]
    cobertura_r: dict[str, bool | None]


@dataclasses.dataclass(frozen=True)
class ConjuntoPareado:
    """Universo estricto de un único scope; nunca exige los cuatro corredores."""

    scope_id: str
    corredor_ids: tuple[str, ...]
    incluidas: tuple[CeldaPareada, ...]
    excluidas: tuple[dict[str, Any], ...]


def _es_numero(valor: Any) -> bool:
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _numero_finito(valor: Any, nombre: str) -> float:
    if not _es_numero(valor) or not math.isfinite(float(valor)):
        raise ErrorScoring("CONFIGURACION_INVALIDA", f"{nombre} debe ser un número finito")
    return float(valor)


def _texto_no_vacio(valor: Any, nombre: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ErrorScoring("CONFIGURACION_INVALIDA", f"{nombre} debe ser texto no vacío")
    return valor.strip()


def _lista_de_mapeos(valor: Any, nombre: str) -> list[Mapping[str, Any]]:
    if not isinstance(valor, list) or not all(isinstance(item, Mapping) for item in valor):
        raise ErrorScoring("CONFIGURACION_INVALIDA", f"{nombre} debe ser una lista de objetos")
    return valor


def validar_configuracion(datos: Mapping[str, Any]) -> Configuracion:
    """Valida todo el scope antes de que se consulte una sola medición.

    La función no recibe celdas por diseño. Así, ni disponibilidad, cobertura,
    puntos, intervalos ni orden de entrada pueden participar en la selección.
    """
    if not isinstance(datos, Mapping):
        raise ErrorScoring("CONFIGURACION_INVALIDA", "la configuración debe ser un objeto")
    principal_crudo = datos.get("comparacion_principal_id")
    if not isinstance(principal_crudo, str) or not principal_crudo.strip():
        raise ErrorScoring(
            CODIGO_SCOPE_AUSENTE,
            "comparacion_principal_id es obligatoria y no tiene default",
        )

    corredores_crudos = _lista_de_mapeos(datos.get("corredores_activos"), "corredores_activos")
    corredores: list[CorredorActivo] = []
    for posicion, crudo in enumerate(corredores_crudos):
        corredores.append(
            CorredorActivo(
                id=_texto_no_vacio(crudo.get("id"), f"corredores_activos[{posicion}].id"),
                familia=_texto_no_vacio(
                    crudo.get("familia"), f"corredores_activos[{posicion}].familia"
                ).upper(),
                variante=_texto_no_vacio(
                    crudo.get("variante"), f"corredores_activos[{posicion}].variante"
                ).lower(),
            )
        )
    ids = [corredor.id for corredor in corredores]
    if len(ids) != len(set(ids)):
        raise ErrorScoring("CONFIGURACION_INVALIDA", "hay IDs de corredor duplicados")
    if any(corredor.familia not in {"L", "M", "E"} for corredor in corredores):
        raise ErrorScoring("CONFIGURACION_INVALIDA", "familia de corredor fuera de L/M/E")

    roles_requeridos = {
        ("L", "solo"): 1,
        ("L", "corpus"): 1,
        ("M", "principal"): 1,
        ("E", "combinacion"): 1,
    }
    for rol, cantidad in roles_requeridos.items():
        encontrados = sum(
            1 for corredor in corredores if (corredor.familia, corredor.variante) == rol
        )
        if encontrados != cantidad:
            raise ErrorScoring(
                "CONFIGURACION_INVALIDA",
                f"se requiere exactamente {cantidad} corredor {rol[0]}/{rol[1]}; hay {encontrados}",
            )
    if len(corredores) != 4:
        raise ErrorScoring(
            "CONFIGURACION_INVALIDA",
            "este contrato requiere exactamente L-solo, L+corpus, M y E activos",
        )
    corredores.sort(key=lambda corredor: corredor.id)
    por_id = {corredor.id: corredor for corredor in corredores}

    comparaciones_crudas = _lista_de_mapeos(
        datos.get("comparaciones_l_m"), "comparaciones_l_m"
    )
    comparaciones: list[ComparacionLM] = []
    for posicion, crudo in enumerate(comparaciones_crudas):
        comparacion = ComparacionLM(
            id=_texto_no_vacio(crudo.get("id"), f"comparaciones_l_m[{posicion}].id"),
            l_id=_texto_no_vacio(crudo.get("l_id"), f"comparaciones_l_m[{posicion}].l_id"),
            m_id=_texto_no_vacio(crudo.get("m_id"), f"comparaciones_l_m[{posicion}].m_id"),
        )
        if comparacion.l_id not in por_id or por_id[comparacion.l_id].familia != "L":
            raise ErrorScoring(
                "CONFIGURACION_INVALIDA", f"{comparacion.id}.l_id no identifica una familia L activa"
            )
        if comparacion.m_id not in por_id or por_id[comparacion.m_id].familia != "M":
            raise ErrorScoring(
                "CONFIGURACION_INVALIDA", f"{comparacion.id}.m_id no identifica una familia M activa"
            )
        comparaciones.append(comparacion)
    comparacion_ids = [comparacion.id for comparacion in comparaciones]
    pares = [(comparacion.l_id, comparacion.m_id) for comparacion in comparaciones]
    if len(comparacion_ids) != len(set(comparacion_ids)) or len(pares) != len(set(pares)):
        raise ErrorScoring("CONFIGURACION_INVALIDA", "hay comparaciones L↔M duplicadas")
    pares_requeridos = {
        (l.id, m.id)
        for l in corredores
        for m in corredores
        if l.familia == "L" and m.familia == "M"
    }
    if set(pares) != pares_requeridos:
        raise ErrorScoring(
            "CONFIGURACION_INVALIDA", "comparaciones_l_m debe declarar todos los pares L↔M activos"
        )
    comparaciones.sort(key=lambda comparacion: comparacion.id)

    principal_id = _texto_no_vacio(
        principal_crudo, "comparacion_principal_id"
    )
    if principal_id not in {comparacion.id for comparacion in comparaciones}:
        raise ErrorScoring(
            "CONFIGURACION_INVALIDA", "comparacion_principal_id no identifica una comparación L↔M"
        )
    e_id = _texto_no_vacio(datos.get("e_id"), "e_id")
    if e_id not in por_id or por_id[e_id].familia != "E":
        raise ErrorScoring("CONFIGURACION_INVALIDA", "e_id no identifica una familia E activa")

    if "delta" not in datos or "nivel_ic" not in datos or "seed" not in datos:
        faltantes = [clave for clave in ("delta", "nivel_ic", "seed") if clave not in datos]
        raise ErrorScoring(
            "CONFIGURACION_INVALIDA", "faltan parámetros obligatorios: " + ", ".join(faltantes)
        )
    delta = _numero_finito(datos["delta"], "delta")
    nivel_ic = _numero_finito(datos["nivel_ic"], "nivel_ic")
    if delta < 0:
        raise ErrorScoring("CONFIGURACION_INVALIDA", "delta debe ser mayor o igual a cero")
    if not 0 < nivel_ic < 1:
        raise ErrorScoring("CONFIGURACION_INVALIDA", "nivel_ic debe estar entre 0 y 1")
    seed = datos["seed"]
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ErrorScoring("CONFIGURACION_INVALIDA", "seed debe ser entero y es obligatorio")
    replicas = datos.get("replicas", REPLICAS_DEFAULT)
    if not isinstance(replicas, int) or isinstance(replicas, bool) or replicas <= 0:
        raise ErrorScoring("CONFIGURACION_INVALIDA", "replicas debe ser entero positivo")

    return Configuracion(
        corredores_activos=tuple(corredores),
        comparaciones_l_m=tuple(comparaciones),
        comparacion_principal_id=principal_id,
        e_id=e_id,
        delta=delta,
        nivel_ic=nivel_ic,
        seed=seed,
        replicas=replicas,
    )


# ---------------------------------------------------------------------------
# Primitivas M3 preservadas
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ArbitroR:
    """Distribución del árbitro de una celda; nunca se colapsa al punto."""

    r_hat: float
    ee: float
    ic_lo_80: float | None = None
    ic_hi_80: float | None = None

    def ic_80(self) -> tuple[float, float]:
        if self.ic_lo_80 is not None and self.ic_hi_80 is not None:
            return self.ic_lo_80, self.ic_hi_80
        z = 1.2815515655446004
        return self.r_hat - z * self.ee, self.r_hat + z * self.ee

    def dentro_del_ic(self, valor: float, nivel_z: float = 1.2815515655446004) -> bool:
        lo, hi = self.ic_80() if nivel_z == 1.2815515655446004 else (
            self.r_hat - nivel_z * self.ee,
            self.r_hat + nivel_z * self.ee,
        )
        return lo <= valor <= hi


def skill(error_corredor: float, error_baseline: float) -> float | None:
    """Calcula ``1 - error_corredor/error_baseline`` sin inventar el caso B=0."""
    if error_baseline == 0:
        return None
    return 1.0 - (error_corredor / error_baseline)


def interval_score(lo: float, hi: float, valor_real: float, alpha: float = 0.20) -> float:
    ancho = hi - lo
    penal_lo = (2.0 / alpha) * max(0.0, lo - valor_real)
    penal_hi = (2.0 / alpha) * max(0.0, valor_real - hi)
    return ancho + penal_lo + penal_hi


def crps_normal_aprox(pred_media: float, pred_sd: float, valor_real: float) -> float:
    if pred_sd <= 0:
        raise ValueError("CRPS cerrado exige SD > 0")
    z = (valor_real - pred_media) / pred_sd
    phi = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    phi_acumulada = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    return pred_sd * (
        z * (2 * phi_acumulada - 1) + 2 * phi - 1 / math.sqrt(math.pi)
    )


def brier_score(prob_predicha: float, ocurrio: bool) -> float:
    observado = 1.0 if ocurrio else 0.0
    return (prob_predicha - observado) ** 2


def es_indecidible(
    valor_L: float, valor_M: float, arbitro: ArbitroR
) -> tuple[bool, dict[str, Any]]:
    lo, hi = arbitro.ic_80()
    condicion_1 = lo <= valor_L <= hi and lo <= valor_M <= hi
    d_l = abs(valor_L - arbitro.r_hat)
    d_m = abs(valor_M - arbitro.r_hat)
    condicion_2 = abs(d_l - d_m) < 0.5 * arbitro.ee
    return condicion_1 or condicion_2, {
        "condicion_1_ambos_en_ic_R": condicion_1,
        "condicion_2_diferencia_bajo_0.5EE": condicion_2,
        "d_L": d_l,
        "d_M": d_m,
        "ic_80_R": (lo, hi),
    }


@dataclasses.dataclass
class RegistroCalibracion:
    corredor: str
    id_celda: str
    valor_real: float
    intervalo_lo: float
    intervalo_hi: float

    def cubierto(self) -> bool:
        return self.intervalo_lo <= self.valor_real <= self.intervalo_hi


def calibracion_80(registros: list[RegistroCalibracion]) -> dict[str, Any]:
    if not registros:
        return {"n": 0, "cubiertos": 0, "cobertura_empirica": None, "objetivo": 0.80}
    cubiertos = sum(registro.cubierto() for registro in registros)
    cobertura = cubiertos / len(registros)
    return {
        "n": len(registros),
        "cubiertos": cubiertos,
        "cobertura_empirica": cobertura,
        "objetivo": 0.80,
        "desviacion_del_objetivo": cobertura - 0.80,
    }


def distancia_ks(muestra_a: list[float], muestra_b: list[float]) -> float:
    a, b = sorted(muestra_a), sorted(muestra_b)
    todos = sorted(set(a) | set(b))
    max_dif = 0.0
    for valor in todos:
        cdf_a = sum(elemento <= valor for elemento in a) / len(a) if a else 0.0
        cdf_b = sum(elemento <= valor for elemento in b) / len(b) if b else 0.0
        max_dif = max(max_dif, abs(cdf_a - cdf_b))
    return max_dif


def distancia_wasserstein_1d(muestra_a: list[float], muestra_b: list[float]) -> float:
    a, b = sorted(muestra_a), sorted(muestra_b)
    if not a or not b:
        raise ValueError("Wasserstein requiere dos muestras no vacías")
    if len(a) != len(b):
        cantidad = max(len(a), len(b))
        a = [a[min(len(a) - 1, int(i * len(a) / cantidad))] for i in range(cantidad)]
        b = [b[min(len(b) - 1, int(i * len(b) / cantidad))] for i in range(cantidad)]
    return math.fsum(abs(x - y) for x, y in zip(a, b)) / len(a)


def _varianza_muestral(valores: list[float]) -> float:
    if len(valores) < 2:
        return 0.0
    media = math.fsum(valores) / len(valores)
    return math.fsum((valor - media) ** 2 for valor in valores) / (len(valores) - 1)


def razon_varianzas(muestra_corredor: list[float], muestra_R: list[float]) -> float | None:
    if len(muestra_R) < 2:
        return None
    var_r = _varianza_muestral(muestra_R)
    if var_r == 0:
        return None
    var_corredor = _varianza_muestral(muestra_corredor)
    return var_corredor / var_r


@dataclasses.dataclass
class CorteSubgrupo:
    nombre_subgrupo: str
    ks: float
    wasserstein: float
    razon_varianzas: float | None


@dataclasses.dataclass
class ResultadoCelda:
    """Compatibilidad M3: estado por celda, distinto del veredicto agregado."""

    id_celda: str
    skill_L: float | None
    skill_M: float | None
    indecidible: bool
    detalle_indecidible: dict[str, Any]
    m3_bis: list[CorteSubgrupo] = dataclasses.field(default_factory=list)


# ---------------------------------------------------------------------------
# Celda -> matriz de mediciones -> universos marginales y pareados por scope
# ---------------------------------------------------------------------------


def _skill_de_medicion(medicion: Any, celda: Mapping[str, Any]) -> float | None:
    if _es_numero(medicion):
        valor = float(medicion)
        return valor if math.isfinite(valor) else None
    if not isinstance(medicion, Mapping):
        return None
    if _es_numero(medicion.get("skill")):
        valor = float(medicion["skill"])
        return valor if math.isfinite(valor) else None
    if _es_numero(medicion.get("error")):
        error_b = medicion.get("error_baseline", celda.get("error_baseline"))
        if _es_numero(error_b) and math.isfinite(float(error_b)):
            valor = skill(float(medicion["error"]), float(error_b))
            return valor if valor is not None and math.isfinite(valor) else None
    return None


def _cobertura_de_medicion(
    corredor_id: str, medicion: Any, celda: Mapping[str, Any]
) -> bool | None:
    coberturas = celda.get("cobertura_r")
    if isinstance(coberturas, Mapping) and isinstance(coberturas.get(corredor_id), bool):
        return coberturas[corredor_id]
    if not isinstance(medicion, Mapping):
        return None
    for clave in ("cubierto_r", "cobertura_r"):
        if isinstance(medicion.get(clave), bool):
            return medicion[clave]
    intervalo = medicion.get("intervalo_80")
    valor_real = celda.get("valor_real", celda.get("r_hat"))
    if (
        isinstance(intervalo, Sequence)
        and not isinstance(intervalo, (str, bytes))
        and len(intervalo) == 2
        and _es_numero(intervalo[0])
        and _es_numero(intervalo[1])
        and _es_numero(valor_real)
    ):
        return float(intervalo[0]) <= float(valor_real) <= float(intervalo[1])
    return None


def construir_matriz_mediciones(
    celdas: Any, configuracion: Configuracion
) -> MatrizMediciones:
    """Valida cada medición por separado, sin crear una intersección global.

    ``INDECIDIBLE`` permanece como estado visible y no vota. Una medición
    ausente solo queda ausente para su corredor; los universos se materializan
    después, scope por scope.
    """
    if not isinstance(celdas, list) or not all(isinstance(celda, Mapping) for celda in celdas):
        raise ErrorScoring("MEDICIONES_INVALIDAS", "celdas debe ser una lista de objetos")
    ids_crudos = [celda.get("id_celda") for celda in celdas]
    if any(not isinstance(id_celda, str) or not id_celda.strip() for id_celda in ids_crudos):
        raise ErrorScoring("MEDICIONES_INVALIDAS", "cada celda requiere id_celda no vacío")
    ids = [str(id_celda).strip() for id_celda in ids_crudos]
    if len(ids) != len(set(ids)):
        raise ErrorScoring("MEDICIONES_INVALIDAS", "hay id_celda duplicados")

    filas: list[CeldaMedida] = []
    ordenadas = sorted(zip(ids, celdas), key=lambda par: par[0])
    for id_celda, celda in ordenadas:
        estado = str(celda.get("estado", "EVALUABLE")).strip().upper()
        mediciones = celda.get("mediciones", celda.get("corredores"))
        mediciones = mediciones if isinstance(mediciones, Mapping) else {}
        skills: dict[str, float] = {}
        cobertura: dict[str, bool | None] = {}
        for corredor in configuracion.corredores_activos:
            medicion = mediciones.get(corredor.id)
            valor = _skill_de_medicion(medicion, celda)
            if valor is not None:
                skills[corredor.id] = valor
            cobertura[corredor.id] = _cobertura_de_medicion(corredor.id, medicion, celda)
        filas.append(
            CeldaMedida(
                id_celda=id_celda,
                estado=estado,
                skills=skills,
                cobertura_r=cobertura,
            )
        )
    return MatrizMediciones(tuple(filas))


def _construir_universo(
    matriz: MatrizMediciones,
    corredor_ids: tuple[str, ...],
    scope_id: str,
) -> ConjuntoPareado:
    incluidas: list[CeldaPareada] = []
    excluidas: list[dict[str, Any]] = []
    for celda in matriz.celdas:
        motivos: list[str] = []
        if celda.estado not in ESTADOS_INCLUIBLES:
            motivos.append(f"ESTADO_NO_EVALUABLE:{celda.estado or 'VACIO'}")
        for corredor_id in corredor_ids:
            if corredor_id not in celda.skills:
                motivos.append(f"MEDICION_AUSENTE_O_NO_EVALUABLE:{corredor_id}")
        if motivos:
            excluidas.append(
                {
                    "estado": celda.estado,
                    "id_celda": celda.id_celda,
                    "motivos": sorted(set(motivos)),
                }
            )
            continue
        incluidas.append(
            CeldaPareada(
                id_celda=celda.id_celda,
                estado=celda.estado,
                skills={corredor_id: celda.skills[corredor_id] for corredor_id in corredor_ids},
                cobertura_r={
                    corredor_id: celda.cobertura_r[corredor_id]
                    for corredor_id in corredor_ids
                },
            )
        )
    return ConjuntoPareado(scope_id, corredor_ids, tuple(incluidas), tuple(excluidas))


def construir_universo_marginal(
    matriz: MatrizMediciones, corredor_id: str
) -> ConjuntoPareado:
    return _construir_universo(matriz, (corredor_id,), f"MARGINAL:{corredor_id}")


def construir_universo_pareado(
    matriz: MatrizMediciones, a_id: str, b_id: str, comparacion_id: str
) -> ConjuntoPareado:
    return _construir_universo(
        matriz, (a_id, b_id), f"COMPARACION:{comparacion_id}"
    )


def construir_conjunto_pareado(
    celdas: Any, configuracion: Configuracion
) -> ConjuntoPareado:
    """Compatibilidad: devuelve solo el universo de la comparación principal."""
    matriz = construir_matriz_mediciones(celdas, configuracion)
    principal = configuracion.comparacion_principal
    return construir_universo_pareado(
        matriz, principal.l_id, principal.m_id, principal.id
    )


# ---------------------------------------------------------------------------
# Bootstrap pareado -> intervalos agregados
# ---------------------------------------------------------------------------


def generar_indices_bootstrap(n_celdas: int, replicas: int, seed: int) -> tuple[tuple[int, ...], ...]:
    """Genera una secuencia local compartida dentro de un scope explícito."""
    if n_celdas <= 0:
        raise ValueError("n_celdas debe ser positivo")
    rng = random.Random(seed)
    return tuple(
        tuple(rng.randrange(n_celdas) for _ in range(n_celdas)) for _ in range(replicas)
    )


def _media(valores: Sequence[float]) -> float:
    return math.fsum(valores) / len(valores)


def _cuantil_7(ordenados: Sequence[float], probabilidad: float) -> float:
    if len(ordenados) == 1:
        return float(ordenados[0])
    posicion = (len(ordenados) - 1) * probabilidad
    inferior = math.floor(posicion)
    superior = math.ceil(posicion)
    if inferior == superior:
        return float(ordenados[inferior])
    peso = posicion - inferior
    return float(ordenados[inferior] * (1 - peso) + ordenados[superior] * peso)


def _resumen_bootstrap(punto: float, replicas: Sequence[float], nivel_ic: float, n: int) -> dict[str, Any]:
    ordenadas = sorted(replicas)
    cola = (1.0 - nivel_ic) / 2.0
    return {
        "ic_hi": _cuantil_7(ordenadas, 1.0 - cola),
        "ic_lo": _cuantil_7(ordenadas, cola),
        "n_celdas": n,
        "punto": punto,
    }


def derivar_seed_scope(seed: int, scope_id: str) -> int:
    """Deriva una semilla estable con SHA-256; nunca usa ``hash()`` de Python."""
    carga = json.dumps([seed, scope_id], ensure_ascii=False, separators=(",", ":"))
    return int.from_bytes(hashlib.sha256(carga.encode("utf-8")).digest()[:16], "big")


def _descripcion_universo(conjunto: ConjuntoPareado) -> dict[str, Any]:
    return {
        "corredor_ids": list(conjunto.corredor_ids),
        "excluidas": list(conjunto.excluidas),
        "ids_incluidos": [celda.id_celda for celda in conjunto.incluidas],
        "incluidas": [
            {
                "estado": celda.estado,
                "id_celda": celda.id_celda,
                "skills": dict(sorted(celda.skills.items())),
            }
            for celda in conjunto.incluidas
        ],
        "n_excluidas": len(conjunto.excluidas),
        "n_incluidas": len(conjunto.incluidas),
        "scope_id": conjunto.scope_id,
    }


def _bootstrap_metadata(
    conjunto: ConjuntoPareado,
    configuracion: Configuracion,
    indices: Sequence[Sequence[int]],
) -> dict[str, Any]:
    hash_indices = hashlib.sha256()
    for replica in indices:
        hash_indices.update((",".join(map(str, replica)) + "\n").encode("ascii"))
    return {
        "indices_compartidos": True,
        "metodo_ic": "percentil_central_tipo_7",
        "nivel_ic": configuracion.nivel_ic,
        "replicas": configuracion.replicas,
        "scope_id": conjunto.scope_id,
        "seed_base": configuracion.seed,
        "seed_scope": derivar_seed_scope(configuracion.seed, conjunto.scope_id),
        "sha256_indices": hash_indices.hexdigest(),
    }


def _resumen_vacio() -> dict[str, Any]:
    return {"ic_hi": None, "ic_lo": None, "n_celdas": 0, "punto": None}


def bootstrap_marginal(
    conjunto: ConjuntoPareado, configuracion: Configuracion
) -> dict[str, Any]:
    if len(conjunto.corredor_ids) != 1:
        raise ValueError("bootstrap_marginal requiere un único corredor")
    corredor_id = conjunto.corredor_ids[0]
    n = len(conjunto.incluidas)
    if n == 0:
        resumen = _resumen_vacio()
        resumen.update(
            {
                "bootstrap": _bootstrap_metadata(conjunto, configuracion, ()),
                "corredor_id": corredor_id,
                "ids_incluidos": [],
                "universo": _descripcion_universo(conjunto),
            }
        )
        return resumen
    seed_scope = derivar_seed_scope(configuracion.seed, conjunto.scope_id)
    indices = generar_indices_bootstrap(n, configuracion.replicas, seed_scope)
    valores = tuple(celda.skills[corredor_id] for celda in conjunto.incluidas)
    replicas = [
        math.fsum(valores[indice] for indice in replica) / n for replica in indices
    ]
    resumen = _resumen_bootstrap(_media(valores), replicas, configuracion.nivel_ic, n)
    resumen.update(
        {
            "bootstrap": _bootstrap_metadata(conjunto, configuracion, indices),
            "corredor_id": corredor_id,
            "ids_incluidos": [celda.id_celda for celda in conjunto.incluidas],
            "universo": _descripcion_universo(conjunto),
        }
    )
    return resumen


def _definiciones_comparaciones(configuracion: Configuracion) -> tuple[dict[str, str], ...]:
    definiciones = [
        {"a_id": comparacion.l_id, "b_id": comparacion.m_id, "id": comparacion.id, "tipo": "L_M"}
        for comparacion in configuracion.comparaciones_l_m
    ]
    for corredor in configuracion.corredores_activos:
        if corredor.id != configuracion.e_id:
            definiciones.append(
                {
                    "a_id": configuracion.e_id,
                    "b_id": corredor.id,
                    "id": f"{configuracion.e_id}_vs_{corredor.id}",
                    "tipo": "E_AUXILIAR",
                }
            )
    ids = [definicion["id"] for definicion in definiciones]
    if len(ids) != len(set(ids)):
        raise ErrorScoring("CONFIGURACION_INVALIDA", "colisión entre IDs de comparaciones agregadas")
    return tuple(sorted(definiciones, key=lambda definicion: definicion["id"]))


def bootstrap_pareado(
    conjunto: ConjuntoPareado, configuracion: Configuracion
) -> dict[str, Any]:
    """Bootstrap estricto de dos extremos y su diferencia sobre el mismo scope."""
    if len(conjunto.corredor_ids) != 2:
        raise ValueError("bootstrap_pareado requiere exactamente dos corredores")
    n = len(conjunto.incluidas)
    a_id, b_id = conjunto.corredor_ids
    universo = _descripcion_universo(conjunto)
    if n == 0:
        vacio = _resumen_vacio()
        return {
            "a": dict(vacio),
            "a_id": a_id,
            "b": dict(vacio),
            "b_id": b_id,
            "bootstrap": _bootstrap_metadata(conjunto, configuracion, ()),
            "diferencia": dict(vacio),
            "ids_incluidos": [],
            "ic_hi": None,
            "ic_lo": None,
            "n_celdas": 0,
            "punto": None,
            "universo": universo,
        }
    seed_scope = derivar_seed_scope(configuracion.seed, conjunto.scope_id)
    indices = generar_indices_bootstrap(n, configuracion.replicas, seed_scope)
    valores_a = tuple(celda.skills[a_id] for celda in conjunto.incluidas)
    valores_b = tuple(celda.skills[b_id] for celda in conjunto.incluidas)
    replicas_a: list[float] = []
    replicas_b: list[float] = []
    for replica in indices:
        replicas_a.append(math.fsum(valores_a[indice] for indice in replica) / n)
        replicas_b.append(math.fsum(valores_b[indice] for indice in replica) / n)
    agregado_a = _resumen_bootstrap(
        _media(valores_a), replicas_a, configuracion.nivel_ic, n
    )
    agregado_b = _resumen_bootstrap(
        _media(valores_b), replicas_b, configuracion.nivel_ic, n
    )
    replicas_diferencia = [a - b for a, b in zip(replicas_a, replicas_b)]
    diferencia = _resumen_bootstrap(
        agregado_a["punto"] - agregado_b["punto"],
        replicas_diferencia,
        configuracion.nivel_ic,
        n,
    )
    return {
        "a": agregado_a,
        "a_id": a_id,
        "b": agregado_b,
        "b_id": b_id,
        "bootstrap": _bootstrap_metadata(conjunto, configuracion, indices),
        "diferencia": diferencia,
        "ids_incluidos": [celda.id_celda for celda in conjunto.incluidas],
        "ic_hi": diferencia["ic_hi"],
        "ic_lo": diferencia["ic_lo"],
        "n_celdas": n,
        "punto": diferencia["punto"],
        "universo": universo,
    }


def _comparaciones_agregadas(
    matriz: MatrizMediciones, configuracion: Configuracion
) -> dict[str, dict[str, Any]]:
    resultados: dict[str, dict[str, Any]] = {}
    for definicion in _definiciones_comparaciones(configuracion):
        conjunto = construir_universo_pareado(
            matriz, definicion["a_id"], definicion["b_id"], definicion["id"]
        )
        resultado = bootstrap_pareado(conjunto, configuracion)
        resultado.update(definicion)
        resultados[definicion["id"]] = resultado
    return resultados


# ---------------------------------------------------------------------------
# Scope adjudicante predeclarado -> secuencia §4 -> veredicto
# ---------------------------------------------------------------------------


def adjudicar_secuencia(
    configuracion: Configuracion,
    paquete_principal: Mapping[str, Any],
) -> dict[str, Any]:
    """Adjudica solo el paquete pareado completo de la comparación principal.

    Deliberadamente no lee la clave ``punto`` de ningún agregado.
    """
    principal = configuracion.comparacion_principal
    if (
        paquete_principal.get("a_id") != principal.l_id
        or paquete_principal.get("b_id") != principal.m_id
    ):
        raise ErrorScoring(
            "SCOPE_PRINCIPAL_INVALIDO",
            "el paquete principal no coincide con la comparación predeclarada",
        )
    l_agregado = paquete_principal["a"]
    m_agregado = paquete_principal["b"]
    l_supera_cero = float(l_agregado["ic_lo"]) > 0
    m_supera_cero = float(m_agregado["ic_lo"]) > 0
    paso_1 = {
        "continua": l_supera_cero or m_supera_cero,
        "l_id": principal.l_id,
        "l_supera_cero": l_supera_cero,
        "m_id": principal.m_id,
        "m_supera_cero": m_supera_cero,
        "n_celdas": paquete_principal["n_celdas"],
        "regla": "supera cero solo si ic_lo > 0",
    }
    if not paso_1["continua"]:
        return {
            "detenida_despues_de": "PASO_1",
            "estado_adjudicacion": "VEREDICTO",
            "fallo_cerrado": None,
            "paso_1": paso_1,
            "paso_2": None,
            "veredicto": {
                "codigo": "NINGUNO_SUPERA_B",
                "ganador_id": None,
                "ganador_semantico": None,
            },
        }

    diferencia = paquete_principal["diferencia"]
    lo, hi = float(diferencia["ic_lo"]), float(diferencia["ic_hi"])
    delta = configuracion.delta
    paso_2 = {
        "comparacion_id": principal.id,
        "delta": delta,
        "ic_hi": hi,
        "ic_lo": lo,
    }
    if lo >= -delta and hi <= delta:
        codigo, ganador_semantico, ganador_id = "EQUIVALENTES", None, None
    elif lo > delta:
        codigo, ganador_semantico, ganador_id = "GANA_L", "L", principal.l_id
    elif hi < -delta:
        codigo, ganador_semantico, ganador_id = "GANA_M", "M", principal.m_id
    elif lo <= 0 <= hi:
        codigo, ganador_semantico, ganador_id = "INDETERMINADO", None, None
    else:
        return {
            "detenida_despues_de": "PASO_2",
            "estado_adjudicacion": "FALLO_CERRADO",
            "fallo_cerrado": {
                "codigo": CODIGO_POSICION_NO_DEFINIDA,
                "ic_hi": hi,
                "ic_lo": lo,
                "mensaje": "posición de IC no cubierta por §4; no se crea un veredicto",
            },
            "paso_1": paso_1,
            "paso_2": paso_2,
            "veredicto": None,
        }
    return {
        "detenida_despues_de": "PASO_2",
        "estado_adjudicacion": "VEREDICTO",
        "fallo_cerrado": None,
        "paso_1": paso_1,
        "paso_2": paso_2,
        "veredicto": {
            "codigo": codigo,
            "ganador_id": ganador_id,
            "ganador_semantico": ganador_semantico,
        },
    }


def calcular_paso_0(matriz: MatrizMediciones, configuracion: Configuracion) -> dict[str, Any]:
    """Cobertura marginal contra R por corredor; nunca entra al adjudicador."""
    cobertura: dict[str, dict[str, Any]] = {}
    for corredor in configuracion.corredores_activos:
        conjunto = construir_universo_marginal(matriz, corredor.id)
        disponibles = [
            celda.cobertura_r[corredor.id]
            for celda in conjunto.incluidas
            if celda.cobertura_r[corredor.id] is not None
        ]
        cubiertas = sum(valor is True for valor in disponibles)
        cobertura[corredor.id] = {
            "cobertura_empirica": cubiertas / len(disponibles) if disponibles else None,
            "cubiertas": cubiertas,
            "ids_incluidos": [celda.id_celda for celda in conjunto.incluidas],
            "n_con_cobertura": len(disponibles),
            "n_celdas_puntuadas": len(conjunto.incluidas),
        }
    return {
        "calibracion_contra_r": cobertura,
        "gating": False,
        "nota": "PASO 0 siempre se calcula y nunca altera el veredicto",
    }


def _extraer_configuracion(documento: Mapping[str, Any]) -> Mapping[str, Any]:
    configuracion = documento.get("configuracion", documento)
    if not isinstance(configuracion, Mapping):
        raise ErrorScoring("CONFIGURACION_INVALIDA", "configuracion debe ser un objeto")
    return configuracion


def ejecutar_scoring(documento: Mapping[str, Any]) -> dict[str, Any]:
    """Ejecuta el contrato completo, validando el scope antes de tocar celdas."""
    if not isinstance(documento, Mapping):
        raise ErrorScoring("ENTRADA_INVALIDA", "la entrada debe ser un objeto JSON")
    configuracion = validar_configuracion(_extraer_configuracion(documento))
    # Solo después de validar el scope se consulta la colección de mediciones.
    matriz = construir_matriz_mediciones(documento.get("celdas"), configuracion)
    marginales = {
        corredor.id: bootstrap_marginal(
            construir_universo_marginal(matriz, corredor.id), configuracion
        )
        for corredor in configuracion.corredores_activos
    }
    comparaciones = _comparaciones_agregadas(matriz, configuracion)
    paquete_principal = comparaciones[configuracion.comparacion_principal_id]
    if paquete_principal["n_celdas"] == 0:
        raise ErrorScoring(
            "SIN_CELDAS_PAREADAS",
            "ninguna celda contiene L seleccionada y M evaluables",
        )
    paso_0 = calcular_paso_0(matriz, configuracion)
    secuencia = adjudicar_secuencia(configuracion, paquete_principal)
    agregados = {
        "bootstrap": {
            "estrategia_seed": "SHA-256(seed, scope_id)",
            "indices_compartidos_dentro_de_comparacion": True,
            "replicas": configuracion.replicas,
            "seed_base": configuracion.seed,
        },
        "comparaciones": comparaciones,
        "corredores": marginales,
    }
    l_no_seleccionadas = list(configuracion.l_ids_no_seleccionados)
    comparaciones_auxiliares = {
        comparacion_id: valor
        for comparacion_id, valor in comparaciones.items()
        if comparacion_id != configuracion.comparacion_principal_id
    }
    universo_principal = paquete_principal["universo"]
    scope_principal = {
        "bootstrap": paquete_principal["bootstrap"],
        "comparacion_principal_id": configuracion.comparacion_principal_id,
        "diferencia": paquete_principal["diferencia"],
        "l": paquete_principal["a"],
        "l_id": configuracion.l_id_adjudicado,
        "m": paquete_principal["b"],
        "m_id": configuracion.m_id_adjudicado,
        "reserva_normativa": RESERVA_SCOPE,
        "secuencia": secuencia,
        "universo": universo_principal,
    }
    return {
        "agregados": agregados,
        "celdas": universo_principal,
        "comparacion_principal_id": configuracion.comparacion_principal_id,
        "configuracion": configuracion.normalizada(),
        "delta": configuracion.delta,
        "hash_configuracion": configuracion.hash_configuracion,
        "l_id_adjudicado": configuracion.l_id_adjudicado,
        "l_ids_no_seleccionados": l_no_seleccionadas,
        "nivel_ic": configuracion.nivel_ic,
        "paso_0": paso_0,
        "replicas": configuracion.replicas,
        "resultados_auxiliares": {
            "comparaciones": comparaciones_auxiliares,
            "e": {
                "agregado": marginales[configuracion.e_id],
                "id": configuracion.e_id,
            },
            "l_no_seleccionadas": [
                {"agregado": marginales[l_id], "id": l_id}
                for l_id in l_no_seleccionadas
            ],
        },
        "scope_adjudicante": {
            "comparacion_principal_id": configuracion.comparacion_principal_id,
            "l_id": configuracion.l_id_adjudicado,
            "m_id": configuracion.m_id_adjudicado,
            "regla": (
                "scope predeclarado; sin default; selección independiente de resultados"
            ),
            "reserva_normativa": RESERVA_SCOPE,
        },
        "scope_principal": scope_principal,
        "seed": configuracion.seed,
        "secuencia": secuencia,
        "universos": {
            "comparaciones": {
                comparacion_id: valor["universo"]
                for comparacion_id, valor in comparaciones.items()
            },
            "marginales": {
                corredor_id: valor["universo"]
                for corredor_id, valor in marginales.items()
            },
        },
    }


# ---------------------------------------------------------------------------
# Serialización y CLI deterministas
# ---------------------------------------------------------------------------


def serializar_json(resultado: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def _hojas(valor: Any, ruta: str = "$") -> list[tuple[str, Any]]:
    if isinstance(valor, Mapping):
        if not valor:
            return [(ruta, {})]
        filas: list[tuple[str, Any]] = []
        for clave in sorted(valor):
            filas.extend(_hojas(valor[clave], f"{ruta}.{clave}"))
        return filas
    if isinstance(valor, list):
        if not valor:
            return [(ruta, [])]
        filas = []
        for indice, elemento in enumerate(valor):
            filas.extend(_hojas(elemento, f"{ruta}[{indice}]"))
        return filas
    return [(ruta, valor)]


def serializar_tsv(resultado: Mapping[str, Any]) -> bytes:
    salida = io.StringIO(newline="")
    escritor = csv.writer(salida, delimiter="\t", lineterminator="\n")
    escritor.writerow(("ruta", "valor"))
    for ruta, valor in _hojas(resultado):
        escritor.writerow(
            (ruta, json.dumps(valor, ensure_ascii=False, sort_keys=True, allow_nan=False))
        )
    return salida.getvalue().encode("utf-8")


def escribir_salida(ruta: str | Path, contenido: bytes) -> None:
    Path(ruta).write_bytes(contenido)


def validar_aserciones_cli(configuracion: Configuracion, argumentos: argparse.Namespace) -> None:
    esperados = {
        "comparacion_principal_id": argumentos.comparacion_principal_id,
        "delta": argumentos.delta,
        "nivel_ic": argumentos.nivel_ic,
        "replicas": argumentos.replicas,
        "seed": argumentos.seed,
    }
    for clave, valor_cli in esperados.items():
        if valor_cli is not None and getattr(configuracion, clave) != valor_cli:
            raise ErrorScoring(
                "CONFIGURACION_CLI_CONTRADICTORIA",
                f"--{clave.replace('_', '-')}={valor_cli!r} contradice la configuración",
            )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="JSON de configuración y celdas, o - para stdin")
    parser.add_argument("--json", dest="salida_json", help="ruta de salida JSON")
    parser.add_argument("--tsv", dest="salida_tsv", help="ruta de salida TSV")
    parser.add_argument("--comparacion-principal-id")
    parser.add_argument("--delta", type=float)
    parser.add_argument("--nivel-ic", type=float)
    parser.add_argument("--replicas", type=int)
    parser.add_argument("--seed", type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    argumentos = _parser().parse_args(argv)
    try:
        texto = sys.stdin.read() if argumentos.entrada == "-" else Path(argumentos.entrada).read_text(
            encoding="utf-8"
        )
        documento = json.loads(texto)
        # Repite solo la validación de configuración para comprobar aserciones CLI;
        # sigue ocurriendo antes de evaluar mediciones.
        configuracion = validar_configuracion(_extraer_configuracion(documento))
        validar_aserciones_cli(configuracion, argumentos)
        resultado = ejecutar_scoring(documento)
        json_bytes = serializar_json(resultado)
        if argumentos.salida_json:
            escribir_salida(argumentos.salida_json, json_bytes)
        if argumentos.salida_tsv:
            escribir_salida(argumentos.salida_tsv, serializar_tsv(resultado))
        if not argumentos.salida_json and not argumentos.salida_tsv:
            sys.stdout.buffer.write(json_bytes)
        return 0
    except (ErrorScoring, json.JSONDecodeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
