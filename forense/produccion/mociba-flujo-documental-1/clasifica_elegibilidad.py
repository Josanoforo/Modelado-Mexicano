#!/usr/bin/env python3
"""Clasificador puro del universo de P12_5 para MOCIBA 2021/2022.

No resuelve rutas, no abre microdatos y no llama servicios. La función
``clasificar_fila`` sólo opera sobre un diccionario ya cargado en memoria.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


P4 = tuple(f"P4_{i:02d}" for i in range(1, 14))
OLAS = {2021, 2022}


def _codigo(valor: Any) -> int | str | None:
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, int):
        return valor
    if isinstance(valor, float) and valor.is_integer():
        return int(valor)
    texto = str(valor).strip().lower()
    if not texto:
        return None
    if texto.isdigit():
        return int(texto)
    return texto


def _salida(
    estado: str,
    razon: str,
    *,
    respuesta_estado: str,
    evento: bool | None = None,
    denominador_valido: bool = False,
) -> dict[str, Any]:
    universo = True if estado == "ELEGIBLE" else False if estado == "NO-ELEGIBLE" else None
    return {
        "estado": estado,
        "razon": razon,
        "universo_elegible": universo,
        "respuesta_estado": respuesta_estado,
        "evento": evento,
        "incluye_denominador_todos_elegibles": universo,
        "incluye_denominador_respuestas_validas": denominador_valido,
    }


def _respuesta_elegible(fila: dict[str, Any], ola: int, razon: str) -> dict[str, Any]:
    desenlace = _codigo(fila.get("P12_5"))
    no_respuesta = _codigo(fila.get("P12_99"))
    if no_respuesta == 1:
        return _salida(
            "ELEGIBLE", f"{razon}; P12_99=1 declara no sabe/no responde",
            respuesta_estado="NO-RESPUESTA-EXPLICITA", evento=None,
        )
    if no_respuesta not in {None, 2, "b"}:
        return _salida(
            "ELEGIBLE", f"{razon}; código inválido en P12_99={no_respuesta!r}",
            respuesta_estado="RESPUESTA-INVALIDA", evento=None,
        )
    if desenlace == 1:
        return _salida(
            "ELEGIBLE", f"{razon}; P12_5=1 es respuesta válida de evento",
            respuesta_estado="VALIDA-EVENTO", evento=True, denominador_valido=True,
        )
    if desenlace == 2:
        return _salida(
            "ELEGIBLE", f"{razon}; P12_5=2 es respuesta válida de no-evento",
            respuesta_estado="VALIDA-NO-EVENTO", evento=False, denominador_valido=True,
        )
    if desenlace in {None, "b"}:
        detalle = "b/blanco documentado" if ola == 2022 else "ausencia sin código de blanco documentado"
        return _salida(
            "ELEGIBLE", f"{razon}; {detalle} dentro del universo no equivale a No",
            respuesta_estado="AUSENTE-DENTRO-UNIVERSO", evento=None,
        )
    return _salida(
        "ELEGIBLE", f"{razon}; código inválido en P12_5={desenlace!r}",
        respuesta_estado="RESPUESTA-INVALIDA", evento=None,
    )


def clasificar_fila(fila: dict[str, Any], ola: int) -> dict[str, Any]:
    """Clasifica una fila sintética según el flujo documental acreditado."""
    if ola not in OLAS:
        raise ValueError(f"ola_no_soportada={ola!r}")
    if not isinstance(fila, dict):
        raise TypeError("fila_debe_ser_diccionario")

    edad = _codigo(fila.get("EDAD"))
    internet = _codigo(fila.get("P7_1"))

    # Un fallo conocido de cualquiera de las dos compuertas basta para excluir.
    if isinstance(edad, int) and edad not in {98, 99} and edad < 12:
        return _salida(
            "NO-ELEGIBLE", "salto previo: EDAD<12",
            respuesta_estado="NO-APLICA-ESTRUCTURAL",
        )
    if internet == 2:
        return _salida(
            "NO-ELEGIBLE", "salto previo: P7_1=2, no usó internet en los últimos tres meses",
            respuesta_estado="NO-APLICA-ESTRUCTURAL",
        )
    if not isinstance(edad, int) or edad in {98, 99} or edad < 0:
        return _salida(
            "INDETERMINADO", f"edad ausente, no especificada o inválida: {edad!r}",
            respuesta_estado="NO-EVALUABLE",
        )
    if internet != 1:
        return _salida(
            "INDETERMINADO", f"P7_1 ausente o inválido: {internet!r}",
            respuesta_estado="NO-EVALUABLE",
        )

    valores = {campo: _codigo(fila.get(campo)) for campo in P4}
    if any(valor == 1 for valor in valores.values()):
        # El sí observado impide la condición de salto aun si otros renglones
        # están ausentes: es exactamente la ruta impresa en el cuestionario.
        return _respuesta_elegible(fila, ola, "al menos un P4_01..P4_13=1 abre P5-P12")

    invalidos = {campo: valor for campo, valor in valores.items()
                 if valor not in {None, 2, 9}}
    if invalidos:
        return _salida(
            "INDETERMINADO", f"código P4 fuera de contrato: {invalidos}",
            respuesta_estado="NO-EVALUABLE",
        )
    if all(valor in {2, 9} for valor in valores.values()):
        return _salida(
            "NO-ELEGIBLE", "todos los P4_01..P4_13 son 2 o 9; salto documentado a P13",
            respuesta_estado="NO-APLICA-ESTRUCTURAL",
        )
    faltantes = [campo for campo, valor in valores.items() if valor is None]
    return _salida(
        "INDETERMINADO",
        f"sin P4=1 y batería incompleta; faltan {','.join(faltantes)}",
        respuesta_estado="NO-EVALUABLE",
    )


def ejecutar_fixtures(ruta: Path) -> dict[str, Any]:
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    if datos.get("naturaleza") != "SINTETICO-NO-MEDICION":
        raise ValueError("fixture_sin_rotulo_SINTETICO-NO-MEDICION")
    resultados = []
    for caso in datos.get("casos", []):
        obtenido = clasificar_fila(caso["fila"], int(caso["ola"]))
        esperado = caso["esperado"]
        ok = all(obtenido.get(k) == v for k, v in esperado.items())
        resultados.append({"id": caso["id"], "ok": ok, "obtenido": obtenido})
    return {
        "naturaleza": "SINTETICO-NO-MEDICION",
        "casos": len(resultados),
        "ok": all(x["ok"] for x in resultados),
        "resultados": resultados,
        "microdatos_abiertos": False,
        "llamadas_realizadas": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True)
    args = parser.parse_args()
    salida = ejecutar_fixtures(args.fixtures)
    print(json.dumps(salida, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if salida["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
