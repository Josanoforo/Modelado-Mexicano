#!/usr/bin/env python3
"""ADR-220 (`ACTO MAESTRA32-E1 · SELLA-ENLACE`): `B` usa `valor_ejecutable`
de `coeficientes_generador_sellados` para los pares uni-valor con
override; sigue el fallback de `asignados_coeficiente.detalle` para los
pares sin medición y para los 2 multi-ítem -- que no traen
`valor_ejecutable` y por tanto NO se consumen aquí (`M-AGREGA=(a)`).
Universo re-derivado 30/ago/2026 (`ACTO MAESTRA32-E9 · PROPAGA-2`,
`ADR-225`, firma b1/F5): 3 -> 4 pares uni-valor con override
(`G3.horizonte_temporal` nuevo, enlace lineal de dirección), 10 -> 9
pares en fallback puro; los 2 multi-ítem sin cambio.

Construye `Procedencia` a mano (`yaml.safe_load` directo), no vía
`P.cargar()`: el árbol de hoy trae una entrada preexistente y ajena a este
acto (`EVIDENCIA_EXPERIMENTAL_TERCEROS`, `ADR-204`) cuyo `clase:` no casa
con ningún prefijo de `clases.py` y hace que `cargar()` completo lance
`ClaseDesconocida` antes de llegar a la sección nueva -- defecto
preexistente (verificado también en `test_motor_procedencia.py`/
`test_motor_matriz.py`/`test_motor_clases.py`, los tres ya fallan igual en
`HEAD`, antes de este acto), fuera del perímetro de `ACTO MAESTRA32-E1`
(`clases.py` no está en su lista de archivos -- ver el comentario junto a
`BLOQUES_CON_CLASE_IMPLICITA` en `procedencia.py` y la nota de cierre de
este acto). `cargar_B` en sí nunca llama a `cargar()` -- solo lee
`procedencia.crudo` -- así que probarlo así ejercita el código real, no un
doble.
"""
import os

import yaml

from _motor_arnes import Arnes, cierto, igual  # noqa: E402

from milpa.src import matriz as M  # noqa: E402
from milpa.src import procedencia as P  # noqa: E402

RUTA_PROCEDENCIA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "milpa", "procedencia.yaml",
)


def _cargar_crudo():
    with open(RUTA_PROCEDENCIA, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main():
    a = Arnes("T-MATRIZ-SELLADOS")
    crudo = _cargar_crudo()
    proc = P.Procedencia(crudo=crudo)
    B = M.cargar_B(proc)

    sellados = crudo["coeficientes_generador_sellados"]
    con_ejecutable = [e for e in sellados if "valor_ejecutable" in e]
    sin_ejecutable = [e for e in sellados if "valor_ejecutable" not in e]

    asignados_detalle = crudo["asignados_coeficiente"]["detalle"]
    asignado_de = {}
    for fila in asignados_detalle:
        gen = fila["gen"]
        for nombre, valor in fila["coefs"].items():
            asignado_de[(gen, nombre)] = valor

    def test_universo_cuatro_mas_dos():
        # Blindaje del universo antes de probar nada más: si M-AGREGA
        # cambiara algún día, esto debe fallar aquí primero, no en un sitio
        # silencioso más abajo. Re-derivado 30/ago/2026 (ACTO MAESTRA32-E9 ·
        # PROPAGA-2, ADR-225): 3 -> 4 con la entrada nueva G3.horizonte_temporal.
        igual(len(con_ejecutable), 4, "pares uni-valor con valor_ejecutable:")
        igual(len(sin_ejecutable), 2, "pares multi-ítem sellados sin agregar:")

    def test_quince_celdas_sin_cambio_de_conteo():
        # El override cambia VALORES, nunca el número de celdas.
        igual(B.no_cero, 15, "celdas no-cero de B tras el override:")

    def test_override_para_los_cuatro_uni_valor():
        for entrada in con_ejecutable:
            gen, coef = entrada["gen"], entrada["coef"]
            celda = B.celdas[(gen, coef)]
            cierto(isinstance(celda, M.Coeficiente),
                   f"{gen}.{coef}: no cargó como Coeficiente")
            igual(celda.valor, float(entrada["valor_ejecutable"]),
                  f"{gen}.{coef}: B no usa el valor_ejecutable sellado")
            # Y el override es REAL -- distinto del ASIGNADO de siempre. Si
            # algún día coincidieran, este test dejaría de poder distinguir
            # override de fallback y debe fallar aquí, no dar falso verde.
            asignado = asignado_de[(gen, coef)]
            cierto(celda.valor != float(asignado),
                   f"{gen}.{coef}: valor_ejecutable ({celda.valor}) coincide "
                   f"con el ASIGNADO ({asignado}) -- el test no distingue "
                   f"override de fallback en este par")

    def test_fallback_intacto_para_los_nueve_sin_medicion():
        # Re-derivado 30/ago/2026 (ACTO MAESTRA32-E9 · PROPAGA-2, ADR-225):
        # 10 -> 9, G3.horizonte_temporal sale del fallback y entra al override.
        pares_sellados = {(e["gen"], e["coef"]) for e in sellados}
        pares_diez = [par for par in asignado_de if par not in pares_sellados]
        igual(len(pares_diez), 9, "pares ASIGNADO sin entrada sellada:")
        for gen, nombre in pares_diez:
            valor_asignado = asignado_de[(gen, nombre)]
            celda = B.celdas[(gen, nombre)]
            if isinstance(valor_asignado, (int, float)):
                cierto(isinstance(celda, M.Coeficiente),
                       f"{gen}.{nombre}: cambió de tipo respecto al fallback")
                igual(celda.valor, float(valor_asignado),
                      f"{gen}.{nombre}: fallback alterado")
            else:
                cierto(isinstance(celda, M.CoeficienteSinMagnitud),
                       f"{gen}.{nombre}: SIN MAGNITUD dejó de cargar como tal")
                igual(celda.literal, str(valor_asignado),
                      f"{gen}.{nombre}: literal SIN MAGNITUD alterado")

    def test_multi_item_no_se_consume():
        for entrada in sin_ejecutable:
            gen, coef = entrada["gen"], entrada["coef"]
            igual(entrada.get("rotulo"), "SELLADO-ESCALA·SIN-AGREGACION",
                  f"{gen}.{coef}: rótulo inesperado")
            # La celda de B para este par sigue siendo el ASIGNADO de
            # siempre -- el par multi-ítem no produjo override.
            celda = B.celdas[(gen, coef)]
            asignado = asignado_de[(gen, coef)]
            igual(celda.valor, float(asignado),
                  f"{gen}.{coef}: par multi-ítem SÍ se consumió en B")

    def test_no_rompe_conteos_globales_de_b():
        # Que exista la sección nueva no debe alterar puntuales/sin_magnitud/
        # generadores -- mismo blindaje que test_motor_matriz.py.
        igual(len(B.puntuales) + len(B.sin_magnitud), 15, "suma tras override:")
        igual(len(B.generadores), 6, "generadores tras override:")

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
