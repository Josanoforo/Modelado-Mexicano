"""El cargador: `milpa/procedencia.yaml` → objetos, con validación de clase.

El insumo 3 del encargo de MOTOR-3/E0 se vuelve CINCO REGLAS EJECUTABLES, cada
una con su test en `tests/test_motor_clases.py`:

  MEDIDO·NACIONAL jamás se segmenta   → `SegmentacionProhibida`
  MEDIDO·PARCIAL(x) sólo sobre sus x  → `EjeNoDeclarado`
  ASIGNADO con su banda declarada     → HOY NO EJECUTABLE: punto con
                                        `banda=None` + deuda. NUNCA fabrica
                                        un intervalo.
  GATE·ID excluye                     → `GateDetiene`
  PENDIENTE no entra                  → se carga y se registra; excluida de
                                        todo consumo del motor

Violación de clase = bug de contrato, y el test lo atrapa.
"""

import os
from dataclasses import dataclass, field

import yaml

from .clases import (
    Clase,
    EjeNoDeclarado,
    GateDetiene,
    SegmentacionProhibida,
    clasificar,
    ejes_declarados,
)

#: Raíz del repo, derivada del propio archivo: los tests corren desde
#: `tests/` y el motor desde la raíz; una ruta relativa rompería en uno de
#: los dos y el fallo aparecería como "archivo no existe", que es
#: exactamente el diagnóstico equivocado.
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA_POR_DEFECTO = os.path.join(RAIZ, "milpa", "procedencia.yaml")

#: SEGUNDO HALLAZGO DE FORMA, declarado en vez de parcheado: dos de las clases
#: NO aparecen nunca como valor de un campo `clase:`. `ASIGNADO` es la clase
#: del BLOQUE entero (`asignados_probabilidad`, `asignados_coeficiente`) y
#: vive en el nombre del bloque y en sus comentarios, no en los datos. Un
#: cargador que sólo buscara `clase:` reportaría cero entradas `ASIGNADO` en un
#: archivo cuyo diagnóstico dice, textualmente, que los 15 coeficientes son
#: todos `ASIGNADO`.
#:
#: La correspondencia se declara AQUÍ, explícita y auditable, en vez de
#: inferirse del nombre del bloque en tiempo de ejecución: inferirla haría que
#: un bloque nuevo entrara al motor sin que nadie lo decidiera.
BLOQUES_CON_CLASE_IMPLICITA = {
    "asignados_probabilidad": Clase.ASIGNADO,
    "asignados_coeficiente": Clase.ASIGNADO,
}


@dataclass(frozen=True)
class Entrada:
    """Una entrada con `clase:` de `milpa/procedencia.yaml`.

    `crudo` conserva el valor literal ÍNTEGRO de `clase:` — con sus ejes entre
    paréntesis y su párrafo, si lo trae. Se conserva porque es lo que se pierde
    al normalizar, y es exactamente donde vive la información.
    """

    llave: str
    clase: Clase
    crudo: str
    ejes: tuple = ()
    banda: object = None            # hoy SIEMPRE None para ASIGNADO
    deuda: str = None
    ruta_yaml: tuple = ()           # camino de llaves hasta la entrada


@dataclass
class Procedencia:
    entradas: list = field(default_factory=list)
    crudo: dict = field(default_factory=dict)
    texto: str = ""

    def por_clase(self, clase):
        return [e for e in self.entradas if e.clase is clase]

    def consumibles(self):
        """Lo que el motor puede consumir.

        `PENDIENTE` no entra (regla 5) y `GATE·ID` tampoco: el gate detiene.
        Las dos se cargaron y están registradas en `entradas` — excluirlas del
        consumo no es lo mismo que no haberlas leído.
        """
        return [
            e
            for e in self.entradas
            if e.clase not in (Clase.PENDIENTE, Clase.GATE_ID)
        ]

    def contador_condicionales_medidas(self):
        """`condicionales medidas sobre atributos: N de 15`.

        SE REPLICA LA FÓRMULA OFICIAL, NO SE RE-INVENTA: `tests/check.py`
        (T19b/T19c) deriva el numerador contando sobre TEXTO CRUDO
        `clase: "MEDIDO·PARCIAL` + `clase: "MEDIDO·NACIONAL`, no sobre YAML
        parseado. Cualquier otra fórmula produciría una cifra que compite con
        canon — que es justo lo que E0 tiene prohibido.
        """
        return (
            self.texto.count('clase: "MEDIDO·PARCIAL')
            + self.texto.count('clase: "MEDIDO·NACIONAL')
        )


def _clase_implicita(camino):
    """Devuelve la clase del bloque que contiene a `camino`, si está declarada."""
    for c in camino:
        if isinstance(c, str) and c in BLOQUES_CON_CLASE_IMPLICITA:
            return BLOQUES_CON_CLASE_IMPLICITA[c]
    return None


def _recorrer(nodo, camino, salida):
    if isinstance(nodo, dict):
        implicita = _clase_implicita(camino)
        if implicita is not None and ("regla" in nodo or "gen" in nodo):
            llave = nodo.get("regla") or nodo.get("gen")
            salida.append(
                Entrada(
                    llave=str(llave),
                    clase=implicita,
                    crudo=f"{implicita.value} (clase del bloque "
                          f"`{camino[0]}`, no campo `clase:`)",
                    ejes=(),
                    banda=None,      # §4.1: la banda NO existe en el archivo
                    deuda="dispersion_no_declarada",
                    ruta_yaml=tuple(str(c) for c in camino),
                )
            )
        if "clase" in nodo and isinstance(nodo["clase"], str):
            crudo = nodo["clase"]
            clase, _ = clasificar(crudo)
            llave = camino[-1] if camino else "?"
            deuda = None
            if clase is Clase.ASIGNADO:
                # §4.1 del plan: no hay campo de banda ni de IC en las
                # entradas ASIGNADO. El propio archivo lo declara como deuda
                # (`deuda_dispersion`). No se fabrica un intervalo.
                deuda = "dispersion_no_declarada"
            salida.append(
                Entrada(
                    llave=str(llave),
                    clase=clase,
                    crudo=crudo,
                    ejes=ejes_declarados(crudo),
                    banda=None,
                    deuda=deuda,
                    ruta_yaml=tuple(str(c) for c in camino),
                )
            )
        for k, v in nodo.items():
            _recorrer(v, camino + [k], salida)
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            _recorrer(v, camino + [i], salida)


def cargar(ruta=None):
    """Carga y valida. Falla si alguna `clase:` no resuelve por prefijo."""
    ruta = ruta or RUTA_POR_DEFECTO
    with open(ruta, encoding="utf-8") as fh:
        texto = fh.read()
    crudo = yaml.safe_load(texto)
    entradas = []
    _recorrer(crudo, [], entradas)
    return Procedencia(entradas=entradas, crudo=crudo, texto=texto)


def segmentar(entrada, eje):
    """Valida que `entrada` pueda segmentarse por `eje`. No calcula nada.

    Es una compuerta de contrato, y por eso vive aquí y no en el llamador:
    dejarla al llamador es exactamente cómo un contrato se incumple en
    silencio.
    """
    if entrada.clase is Clase.MEDIDO_NACIONAL:
        raise SegmentacionProhibida(
            f"`{entrada.llave}` es MEDIDO·NACIONAL (x = ∅): admitirla a esta "
            f"clase NO abre su condicional por eje. La medición condicionada "
            f"se corre aparte (puerta D3-B)."
        )
    if entrada.clase is Clase.GATE_ID:
        raise GateDetiene(
            f"`{entrada.llave}` es GATE·ID: el gate detiene, no estima."
        )
    if entrada.clase is Clase.MEDIDO_PARCIAL and eje not in entrada.ejes:
        raise EjeNoDeclarado(
            f"`{entrada.llave}` declara los ejes {entrada.ejes}; `{eje}` no "
            f"está entre ellos."
        )
    return True


def como_estimando(entrada):
    """Devuelve la entrada si puede usarse como estimando. Si no, para.

    `GATE·ID` no es un estimando pobre: no es un estimando. El gate detiene el
    acto ANTES de cruzar exposición contra desenlace.
    """
    if entrada.clase is Clase.GATE_ID:
        raise GateDetiene(
            f"`{entrada.llave}`: compuerta de identificación inalcanzable por "
            f"construcción. El gate detiene, no estima."
        )
    if entrada.clase is Clase.PENDIENTE:
        raise ValueError(
            f"`{entrada.llave}` es PENDIENTE: se registra, no entra al motor."
        )
    return entrada
