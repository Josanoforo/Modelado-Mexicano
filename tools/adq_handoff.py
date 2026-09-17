#!/usr/bin/env python3
"""Handoff redundante y métricas mecánicas del cierre ADQ."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

import adq_doctor

RAIZ = Path(__file__).resolve().parent.parent


def _escribe_json_atomico(ruta: Path, dato: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fd, temporal = tempfile.mkstemp(
        dir=ruta.parent, prefix=f".{ruta.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dato, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporal, ruta)
    except BaseException:
        try:
            os.unlink(temporal)
        except FileNotFoundError:
            pass
        raise


def _lee_json(ruta: Path) -> object:
    with ruta.open(encoding="utf-8") as f:
        return json.load(f)


def _canonico(dato: dict) -> str:
    return json.dumps(
        dato, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def evalua_candidato(nombre: str, ruta: Path, seleccion: dict,
                     seleccion_investigacion: dict, *, raiz: Path = RAIZ,
                     comprobar_remoto: bool = True) -> dict:
    """Parsea, normaliza y valida un candidato con el validador productivo."""
    base = {"origen": nombre, "archivo": ruta.name, "presente": ruta.is_file(),
            "valido": False, "errores": []}
    if not ruta.is_file():
        base["errores"] = ["candidato ausente"]
        return base
    try:
        dato = _lee_json(ruta)
    except (OSError, json.JSONDecodeError) as e:
        base["errores"] = [f"JSON ilegible: {type(e).__name__}: {e}"]
        return base
    if not isinstance(dato, dict):
        base["errores"] = ["el candidato no es un objeto JSON"]
        return base
    try:
        normalizado = adq_doctor.normaliza_selecciones_resultado(
            dato, seleccion, seleccion_investigacion)
        validacion = adq_doctor.valida_resultado_adquisicion(
            normalizado, seleccion, seleccion_investigacion,
            comprobar_remoto=comprobar_remoto, raiz=raiz)
    except Exception as e:
        base["errores"] = [f"normalización/validación falló: {type(e).__name__}: {e}"]
        return base
    base.update({
        "valido": bool(validacion["valido"]),
        "errores": list(validacion["errores"]),
        "validacion": validacion,
        "normalizado": normalizado,
        "canonico": _canonico(normalizado),
    })
    return base


def selecciona_resultado(candidatos: list[tuple[str, Path]], seleccion: dict,
                         seleccion_investigacion: dict, *, raiz: Path = RAIZ,
                         comprobar_remoto: bool = True) -> tuple[dict, dict | None]:
    """Elige el único resultado válido o falla ante ausencia/conflicto."""
    evaluados = [evalua_candidato(
        nombre, ruta, seleccion, seleccion_investigacion, raiz=raiz,
        comprobar_remoto=comprobar_remoto) for nombre, ruta in candidatos]
    validos = [x for x in evaluados if x["valido"]]
    aceptado = None
    if not validos:
        origen, causa, codigo = "ninguno", "sin_candidato_valido", 65
    elif len(validos) == 1:
        aceptado = validos[0]["normalizado"]
        origen = validos[0]["origen"]
        causa = f"{origen}_unico_valido"
        codigo = 0
    elif len({x["canonico"] for x in validos}) == 1:
        # Orden de candidatos = precedencia declarada por el wrapper. No hay
        # doble conteo: se materializa una sola copia canónica.
        aceptado = validos[0]["normalizado"]
        origen = validos[0]["origen"]
        causa = "candidatos_validos_iguales"
        codigo = 0
    else:
        origen, causa, codigo = "conflicto", "candidatos_validos_divergentes", 67
    informe = {
        "valido": codigo == 0,
        "resultado_origen": origen,
        "causa": causa,
        "codigo": codigo,
        "candidatos": [{k: v for k, v in x.items()
                         if k not in {"normalizado", "canonico"}}
                        for x in evaluados],
    }
    if codigo == 0:
        elegido = next(x for x in validos if x["origen"] == origen)
        informe["validacion_aceptada"] = elegido["validacion"]
    return informe, aceptado


def captura_estado_antes(seleccion_investigacion: dict,
                         raiz: Path = RAIZ) -> dict:
    """Fotografía pre-hijo de las dimensiones que pueden acreditar avance."""
    estados = {}
    directorio = raiz / "data" / "curacion-registro" / "investigacion-estado"
    for elegido in seleccion_investigacion.get("elegidos", []):
        ident = elegido["id"]
        ruta = directorio / f"{ident}.json"
        try:
            dato = _lee_json(ruta)
        except (OSError, json.JSONDecodeError):
            dato = {}
        estados[ident] = {
            "version_pregunta": dato.get("version_pregunta"),
            "evidencias": list(dato.get("evidencias") or []),
            "suficiencia": dict(dato.get("suficiencia") or {}),
        }
    return {"seleccionadas": [x["id"] for x in
                               seleccion_investigacion.get("elegidos", [])],
            "estados": estados}


_ORDEN_DIMENSION = {
    "NO_ACREDITADA": 0, "PARCIAL": 1, "ACREDITADA": 2,
}
_ORDEN_USO = {
    "INCOMPATIBLE": 0, "APTA_ALCANCE_MENOR": 1,
    "APTA_USO_DECLARADO": 2,
}
_ORDEN_PREGUNTA = {"ABIERTA": 0, "CUBIERTA": 1}


def _mejora(valor_antes: object, valor_despues: object, orden: dict) -> bool:
    return (valor_antes in orden and valor_despues in orden and
            orden[valor_despues] > orden[valor_antes])


def metricas_resultado(resultado: dict, estado_antes: dict,
                       raiz: Path = RAIZ) -> dict:
    """Distingue evidencia, brecha y bytes sin confiar en prosa libre."""
    evidencia_nueva, reduccion, sin_avance = [], [], []
    previos = estado_antes.get("estados", {})
    for item in resultado.get("investigaciones", []):
        ident = item["necesidad_id"]
        previo = previos.get(ident, {})
        evidencias_previas = set(previo.get("evidencias") or [])
        rutas_nuevas = []
        for referencia in item.get("evidencias", []):
            real, permitido = adq_doctor._ruta_evidencia_local(
                referencia, os.path.realpath(raiz))
            if (referencia not in evidencias_previas and permitido and
                    os.path.exists(real)):
                rutas_nuevas.append(referencia)
        candidata_nueva = any(
            c.get("nuevo_respecto_corpus") is True
            for c in item.get("candidatas", []))
        tiene_evidencia = bool(rutas_nuevas or candidata_nueva)
        if tiene_evidencia:
            evidencia_nueva.append(ident)

        antes = previo.get("suficiencia") or {}
        despues = item.get("suficiencia") or {}
        dimensiones = (
            "identidad", "conceptual", "poblacional",
            "seleccion_no_respuesta", "unidad", "temporalidad", "diseno",
            "identificacion",
        )
        mejora = any(_mejora(antes.get(k), despues.get(k), _ORDEN_DIMENSION)
                     for k in dimensiones)
        mejora = mejora or _mejora(
            antes.get("uso_habilitado"), despues.get("uso_habilitado"),
            _ORDEN_USO)
        mejora = mejora or _mejora(
            antes.get("pregunta_original"), despues.get("pregunta_original"),
            _ORDEN_PREGUNTA)
        if mejora:
            reduccion.append(ident)
        if not tiene_evidencia and not mejora:
            sin_avance.append(ident)

    objetos = resultado.get("resultados_por_objeto", [])
    intentados = len({x["objeto_id"] for x in objetos})
    adquiridos = sum(x.get("desenlace") == "adquirido" for x in objetos)
    archivos = set()
    for item in objetos:
        if item.get("desenlace") != "adquirido":
            continue
        for declarado in item.get("archivos", []):
            ruta = Path(declarado) if os.path.isabs(declarado) else raiz / declarado
            if ruta.is_file():
                archivos.add(os.path.realpath(ruta))
    bytes_nuevos = sum(os.path.getsize(p) for p in archivos)
    if adquiridos:
        salud = "AVANCE_ADQUISICION"
    elif reduccion:
        salud = "REDUCCION_BRECHA"
    elif evidencia_nueva:
        salud = "EVIDENCIA_NUEVA_SIN_REDUCCION"
    elif resultado.get("investigaciones"):
        salud = "EJECUCION_SIN_EVIDENCIA_NUEVA"
    else:
        salud = "SIN_TRABAJO_ATENDIBLE"
    return {
        "investigaciones_validadas": len(resultado.get("investigaciones", [])),
        "investigaciones_evidencia_nueva": len(evidencia_nueva),
        "investigaciones_reduccion_brecha": len(reduccion),
        "investigaciones_sin_avance": len(sin_avance),
        "ids_evidencia_nueva": evidencia_nueva,
        "ids_reduccion_brecha": reduccion,
        "ids_sin_avance": sin_avance,
        "objetos_intentados": intentados,
        "objetos_adquiridos": adquiridos,
        "bytes_nuevos": bytes_nuevos,
        "salud_trabajo": salud,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--selecciona-resultado", action="store_true")
    grupo.add_argument("--captura-antes", action="store_true")
    grupo.add_argument("--metricas", action="store_true")
    ap.add_argument("--last-message", type=Path)
    ap.add_argument("--handoff", type=Path)
    ap.add_argument("--seleccion-archivo", type=Path)
    ap.add_argument("--seleccion-investigacion-archivo", type=Path, required=True)
    ap.add_argument("--resultado", type=Path)
    ap.add_argument("--estado-antes", type=Path)
    ap.add_argument("--resultado-aceptado", type=Path)
    ap.add_argument("--informe", type=Path)
    ap.add_argument("--salida", type=Path)
    ap.add_argument("--raiz", type=Path, default=RAIZ)
    ap.add_argument("--sin-remoto", action="store_true")
    a = ap.parse_args()
    raiz = a.raiz.resolve()
    seleccion_inv = _lee_json(a.seleccion_investigacion_archivo)
    if a.captura_antes:
        if not a.salida:
            ap.error("--captura-antes exige --salida")
        _escribe_json_atomico(a.salida, captura_estado_antes(seleccion_inv, raiz))
        return 0
    if a.metricas:
        if not a.resultado or not a.estado_antes or not a.salida:
            ap.error("--metricas exige --resultado, --estado-antes y --salida")
        dato = metricas_resultado(
            _lee_json(a.resultado), _lee_json(a.estado_antes), raiz)
        _escribe_json_atomico(a.salida, dato)
        return 0
    if not all((a.last_message, a.handoff, a.seleccion_archivo,
                a.resultado_aceptado, a.informe)):
        ap.error("--selecciona-resultado exige ambos candidatos, selecciones y salidas")
    informe, aceptado = selecciona_resultado(
        [("last-message", a.last_message), ("handoff", a.handoff)],
        _lee_json(a.seleccion_archivo), seleccion_inv, raiz=raiz,
        comprobar_remoto=not a.sin_remoto)
    if aceptado is not None:
        _escribe_json_atomico(a.resultado_aceptado, aceptado)
    _escribe_json_atomico(a.informe, informe)
    return int(informe["codigo"])


if __name__ == "__main__":
    raise SystemExit(main())
