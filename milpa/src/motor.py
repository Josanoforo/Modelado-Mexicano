"""La rebanada mínima del motor de matriz — punto de entrada del paquete.

NOTA DE FORMA, deliberada: `milpa/src/` es un PAQUETE DE ESPACIO DE NOMBRES —
no lleva `__init__.py`. La razón es del repo, no de estilo: `T02` normaliza
nombres sin distinguir directorio, y un `milpa/src/__init__.py` colisiona por
construcción con `tools/curador_registro/__init__.py`, que ya existe. Se
verificó corriendo la suite con y sin el archivo. Los imports funcionan igual
(`from milpa.src import motor`).

La rebanada mínima: `m = Σ_x π(x)·h_r(B·θ(x), C(x))`, hasta donde E0 llega.

QUÉ HACE ESTA REBANADA, dicho sin adorno: carga `milpa/procedencia.yaml`
validando clases, construye `B` con su celda sin magnitud declarada, carga el
catálogo de momentos sellado, y evalúa las TRES CELDAS-SEMILLA de
`data/curacion-registro/celdas-d/` contra los momentos `AJUSTE` — produciendo
para cada una un VEREDICTO DE ESTADO, no un número.

QUÉ NO HACE, y por qué eso no es un defecto: no calibra, no estima, no produce
ninguna cifra nueva. La ley de mesa vigente lo prohíbe en E0 y toda calibración
E1+ espera el cierre de BARRIDO-2. Una rebanada que devolviera números aquí
estaría violando el encargo, no superándolo.

LA TERCERA CELDA-SEMILLA está `PENDIENTE` y sin coeficiente de generador que le
corresponda. Corre igual, CON SU ESTADO DECLARADO, y produce un veredicto de
estado. No se la "completa" para que corra.
"""

import os
from dataclasses import dataclass, field

import yaml

from . import matriz as _matriz
from . import momentos as _momentos
from . import procedencia as _procedencia
from .clases import SinMagnitud

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR_CELDAS_D = os.path.join(RAIZ, "data", "curacion-registro", "celdas-d")

#: Vocabulario A.4 — el veredicto de computabilidad se registra AQUÍ (C2), no
#: como condición de pertenencia en el catálogo (C1). Fix M10 de RONDA-M.
VEREDICTOS = (
    "EXISTE-SATISFACE",
    "EXISTE-NO-SATISFACE",
    "NO-ENCONTRADO",
    "EXISTE-NO-VERIFICADO",
)


@dataclass
class Resultado:
    celda_id: str
    tipo_adjudicacion: str
    estado_operativo: str
    veredicto: str
    razon: str
    momentos_ajuste_considerados: int
    momentos_holdout_intocados: int
    generadores_en_B: tuple = ()
    semilla: int = 0
    notas: list = field(default_factory=list)

    def como_dict(self):
        return {
            "celda_id": self.celda_id,
            "tipo_adjudicacion": self.tipo_adjudicacion,
            "estado_operativo": self.estado_operativo,
            "veredicto": self.veredicto,
            "razon": self.razon,
            "momentos_ajuste_considerados": self.momentos_ajuste_considerados,
            "momentos_holdout_intocados": self.momentos_holdout_intocados,
            "generadores_en_B": list(self.generadores_en_B),
            "semilla": self.semilla,
            "notas": list(self.notas),
        }


def celdas_semilla(directorio=None):
    """Las celdas-D del disco. Son las que hay; no se enumeran de memoria."""
    directorio = directorio or DIR_CELDAS_D
    nombres = sorted(
        n for n in os.listdir(directorio) if n.endswith((".yaml", ".yml"))
    )
    salida = []
    for n in nombres:
        with open(os.path.join(directorio, n), encoding="utf-8") as fh:
            salida.append((n, yaml.safe_load(fh)["celda_d"]))
    return salida


def evaluar(celda_d, catalogo, matriz_B, *, semilla=0):
    """Un veredicto de estado por celda-semilla. Nunca un número nuevo."""
    ajuste = _momentos.momentos_ajuste(catalogo)
    holdout = _momentos.momentos_holdout(catalogo)
    notas = []

    estado = str(celda_d.get("estado_operativo", "SIN-ESTADO"))
    tipo = str(celda_d.get("tipo_adjudicacion", "SIN-TIPO"))
    cid = str(celda_d.get("id", "SIN-ID"))

    if estado != "LISTO":
        veredicto = "EXISTE-NO-SATISFACE"
        razon = (
            f"`estado_operativo` = {estado}: la celda existe y está registrada, "
            f"pero no satisface la condición de corrida. Se declara; no se "
            f"completa para que corra."
        )
    else:
        # El estimando de la celda se busca en `B` por clave compuesta.
        sin_magnitud = [
            c for c in matriz_B.sin_magnitud
            if c.nombre in cid
        ]
        if sin_magnitud:
            veredicto = "EXISTE-NO-SATISFACE"
            c = sin_magnitud[0]
            razon = (
                f"`{c.generador} × {c.nombre}` es SIN MAGNITUD: "
                f"{c.literal}. El check obligatorio de ADR-30 persiste "
                f"inejecutable bajo la matriz (defecto M1 de RONDA-M)."
            )
        else:
            veredicto = "EXISTE-NO-VERIFICADO"
            razon = (
                "el contrato de clases se respeta y `B` carga completa, pero "
                "E0 no computa el momento: `universo_candidatos` está POR "
                "DECLARAR y la calibración es E1+, que espera el cierre de "
                "BARRIDO-2."
            )

    # El muro, ejercido de verdad, no declarado: se toca cada HOLDOUT por el
    # único camino permitido (metadatos) y se comprueba que el prohibido lanza.
    intocados = 0
    for m in holdout:
        try:
            _momentos.valor_de(m)
        except _momentos.HoldoutTocado:
            intocados += 1
        else:  # pragma: no cover — si esto ocurre, el muro no existe
            raise AssertionError(
                f"`{m.id_momento}` devolvió valor siendo HOLDOUT: el muro de "
                f"pre-registro no está puesto."
            )
    if intocados != len(holdout):  # pragma: no cover
        raise AssertionError("no todos los HOLDOUT quedaron intocados")

    notas.append(f"momentos HOLDOUT reproducidos: 0 de {len(holdout)}")

    return Resultado(
        celda_id=cid,
        tipo_adjudicacion=tipo,
        estado_operativo=estado,
        veredicto=veredicto,
        razon=razon,
        momentos_ajuste_considerados=len(ajuste),
        momentos_holdout_intocados=intocados,
        generadores_en_B=matriz_B.generadores,
        semilla=semilla,
        notas=notas,
    )


def correr(*, semilla=0, ruta_procedencia=None, ruta_catalogo=None,
           dir_celdas=None):
    """La rebanada completa, de punta a punta. Determinista por construcción."""
    proc = _procedencia.cargar(ruta_procedencia)
    B = _matriz.cargar_B(proc)
    cat = _momentos.cargar_catalogo(ruta_catalogo)
    resultados = [
        evaluar(celda_d, cat, B, semilla=semilla)
        for _, celda_d in celdas_semilla(dir_celdas)
    ]
    return {
        "version_motor": "0.1.0",
        "semilla": semilla,
        "contador_condicionales_medidas": proc.contador_condicionales_medidas(),
        "celdas_no_cero_en_B": B.no_cero,
        "coeficientes_puntuales": len(B.puntuales),
        "coeficientes_sin_magnitud": len(B.sin_magnitud),
        "momentos_total": len(cat),
        "momentos_ajuste": len(_momentos.momentos_ajuste(cat)),
        "momentos_holdout": len(_momentos.momentos_holdout(cat)),
        "holdout_reproducidos": 0,
        "resultados": [r.como_dict() for r in resultados],
    }


__all__ = ["Resultado", "celdas_semilla", "evaluar", "correr", "SinMagnitud",
           "VEREDICTOS"]
