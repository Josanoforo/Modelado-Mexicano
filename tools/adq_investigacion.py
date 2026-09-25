#!/usr/bin/env python3
"""Proyecta demanda científica activa y selecciona investigación recurrente."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import tempfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "data" / "adq-investigacion.yaml"
DIMENSIONES_PRESUPUESTO = ("necesidades", "objetos", "segundos_ejecutor")


def _fecha(valor: object) -> dt.date | None:
    if valor in (None, ""):
        return None
    if isinstance(valor, dt.date):
        return valor
    return dt.date.fromisoformat(str(valor))


def _revision_por_evento(valor: object) -> bool:
    """Distingue una espera humana explícita de una fecha ISO."""
    return isinstance(valor, str) and valor.strip().upper().startswith("EVENTO:")


def _ahora() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _json_atomico(path: Path, dato: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporal = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dato, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporal, path)
    except BaseException:
        try:
            os.unlink(temporal)
        except FileNotFoundError:
            pass
        raise


def cargar_config(path: Path = CONFIG) -> dict:
    dato = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(dato, dict) or dato.get("version") != "GEN2-ADQ-INVESTIGACION-V1":
        raise ValueError("configuración de investigación ausente o versión inválida")
    for grupo in dato.get("conciliacion_elementos", []):
        if not grupo.get("elementos"):
            raise ValueError("grupo de conciliación sin elementos exactos")
        for oferta in grupo.get("ofertas", []):
            requeridos = (
                "oferta_id", "fuente", "ola", "estimando", "unidad",
                "poblacion", "transformacion", "proposito", "compatibilidad",
                "evidencia",
            )
            if any(not oferta.get(k) for k in requeridos):
                raise ValueError(
                    f"oferta {oferta.get('oferta_id', '<sin-id>')} sin "
                    "compatibilidad documental completa")
    return dato


def _demandas_independientes(cfg: dict) -> dict[str, dict]:
    """Demandas científicas cuyo ciclo de vida no depende de una NC.

    Una NC conserva el historial de un acto.  Una pregunta todavía requerida
    por un consumidor puede sobrevivir a ese cierre sin reabrir la NC.  La
    configuración es la ampliación mínima del registro operativo existente;
    no crea una segunda tabla de autoridad.
    """
    demandas: dict[str, dict] = {}
    for item in cfg.get("demandas_instrumento", []):
        ident = str(item.get("id") or "")
        if not ident or ident in demandas:
            raise ValueError(f"demanda de instrumento sin identidad única: {ident!r}")
        if item.get("vigente", True):
            demandas[ident] = dict(item)
    return demandas


def _base_demanda_independiente(item: dict) -> dict:
    return {
        "id": item["id"],
        "acto": "DEMANDA-INDEPENDIENTE",
        "pieza": item.get("consumidor", ""),
        "que_no_se_corrio": item.get("pregunta") or item.get("brecha", ""),
        "razon": item.get("investigacion_previa", ""),
        "impacto": item.get("brecha", ""),
        "sucesor": item.get("siguiente_accion", ""),
        "estado": "VIGENTE",
        "origen_demanda": "CONSUMIDOR_Y_USO",
    }


def fuentes_demanda_vigente(cfg: dict, raiz: Path = RAIZ) -> dict[str, dict]:
    """Une NC abiertas y demandas independientes, sin equiparar sus estados."""
    fuentes = {
        ident: {**base, "origen_demanda": "NC_ABIERTA"}
        for ident, base in necesidades_canonicas(cfg, raiz).items()
        if base.get("estado") == "ABIERTA"
    }
    for ident, item in _demandas_independientes(cfg).items():
        if ident in fuentes:
            raise ValueError(f"identidad repetida entre NC y demanda: {ident}")
        fuentes[ident] = _base_demanda_independiente(item)
    return fuentes


def necesidades_canonicas(cfg: dict, raiz: Path = RAIZ) -> dict[str, dict]:
    ruta = raiz / cfg["fuente_necesidades"]
    with ruta.open(encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f, delimiter="\t")}


def _tsv(path: Path) -> list[dict[str, str]]:
    """Lee vistas TSV que pueden comenzar con comentarios de derivación."""
    texto = "".join(
        linea for linea in path.read_text(encoding="utf-8").splitlines(True)
        if linea.strip() and not linea.startswith("#"))
    return list(csv.DictReader(io.StringIO(texto), delimiter="\t")) if texto else []


def _texto_nc(base: dict) -> str:
    return " ".join(str(base.get(k) or "") for k in (
        "que_no_se_corrio", "razon", "impacto", "sucesor"))


def _naturaleza_nc(base: dict) -> str:
    """Separa ciencia, acceso y operación sin inventar campos científicos."""
    ident = str(base.get("id") or "")
    acceso = {
        "NC-0056", "NC-0061", "NC-0090", "NC-0151", "NC-0153", "NC-0156",
        "NC-0159",
    }
    operativas = {
        "NC-0007", "NC-0012", "NC-0033", "NC-0038", "NC-0039", "NC-0050",
        "NC-0054", "NC-0055", "NC-0058", "NC-0100", "NC-0106", "NC-0120",
        "NC-0130", "NC-0136", "NC-0165",
    }
    if ident in acceso:
        return "OPERATIVA_ACCESO_HUMANO"
    if ident in operativas:
        return "OPERATIVA_TECNICA_O_DOCUMENTAL"
    return "CIENTIFICA_O_DE_ADOPCION"


def _etapa_faltante(base: dict) -> str:
    texto = _texto_nc(base).lower()
    pregunta = str(base.get("que_no_se_corrio") or "").lower()
    sucesor = str(base.get("sucesor") or "").lower()
    accion = f"{pregunta} {sucesor}"
    if re.search(r"presentar|enviar|credencial|login|compra|convenio|contacto|folio", accion):
        return "ACCESO_O_DESCARGA"
    if re.search(r"llenar texto_reactivo|indexar|codebook|diccionario|mapear|join|limpiar", accion):
        return "PREPARACION"
    if re.search(r"buscar|localizar|fuente|microdato|instrumento|reactivo|variable|dato", accion):
        return "FUENTE_O_VARIABLE"
    if re.search(r"prepar|spec", accion):
        return "PREPARACION"
    if re.search(r"calcul|medir|estimar|re-correr|ejecutar", accion):
        return "CALCULO"
    if re.search(r"valid|verific|replay|varianza|diseño", accion):
        return "VALIDACION"
    if re.search(r"adopt|cita corrida0|parametr", accion):
        return "ADOPCION"
    if "decision" in texto or "mesa decide" in texto or "elegir" in texto:
        return "DECISION_CIENTIFICA"
    return "DECISION_O_IMPLEMENTACION"


def _responsable(base: dict, etapa: str) -> str:
    texto = _texto_nc(base).lower()
    sucesor = str(base.get("sucesor") or "").strip()
    if etapa == "ACCESO_O_DESCARGA" or "titular" in texto:
        return "titular-acceso-y-receptor-tecnico"
    if etapa == "DECISION_CIENTIFICA" or "decision-de-mesa" in texto:
        return "mesa"
    if etapa == "FUENTE_O_VARIABLE":
        return "servicio-gen2-38"
    if sucesor and not sucesor.lower().startswith(("sin-asignar", "n/a", "ninguno")):
        return sucesor.split(";", 1)[0]
    return "direccion-programa"


def _siguiente_accion(base: dict, etapa: str, responsable: str) -> str:
    sucesor = str(base.get("sucesor") or "").strip()
    if sucesor and not sucesor.lower().startswith("sin-asignar"):
        return sucesor
    pregunta = str(base.get("que_no_se_corrio") or "brecha vigente").strip()
    if etapa == "FUENTE_O_VARIABLE":
        return f"{responsable}: investigar la brecha explícita: {pregunta}"
    if etapa == "DECISION_CIENTIFICA":
        return f"mesa: resolver con opciones explícitas la brecha: {pregunta}"
    return f"{responsable}: asignar y ejecutar el sucesor de: {pregunta}"


def _ruteo_automatico(base: dict, etapa: str) -> tuple[str, str]:
    """Enruta sólo búsquedas explícitas; nunca revive diferidos por heurística."""
    texto = _texto_nc(base).lower()
    bloqueos = (
        "diferido", "sustituido", "descartado", "fuera-de-perimetro",
        "decisión-de-mesa", "decision-de-mesa", "paro-premisa",
        "requiere-identidad", "vía-comercial-diferida", "via-comercial-diferida",
        "paro-entorno", "gen2-f5",
    )
    if any(x in texto for x in bloqueos):
        return "ESPERA_O_DELEGADA", "precedencia explícita impide reactivación automática"
    if etapa == "FUENTE_O_VARIABLE" and re.search(
            r"buscar|localizar|obtener|adquirir|fuente|microdato|instrumento|reactivo",
            texto):
        return "LISTA_SONDA", "brecha de datos explícita sin compuerta posterior"
    return "NO_SONDA", f"etapa vigente {etapa}; no corresponde investigación externa"


def _evidencia_nueva_aplicable(estado: dict, item: dict) -> bool:
    """Acepta sólo la señal estructurada de la versión vigente, nunca prosa suelta."""
    nueva = estado.get("evidencia_nueva_identificada")
    return bool(isinstance(nueva, dict) and all((
        nueva.get("identificada") is True,
        nueva.get("necesidad_id") == item.get("id"),
        nueva.get("version_pregunta") == item.get("version_pregunta"),
        isinstance(nueva.get("evidencias"), list),
        nueva.get("evidencias"),
    )))


def _ruteo_efectivo(item: dict, estado: dict, corte: dt.date, *,
                    cambio_material: bool = False) -> tuple[str, str]:
    """Reanuda espera por fecha/evidencia; conserva barreras humanas."""
    ruteo = item.get("estado_ruteo") or "NO_SONDA"
    if ruteo in {"ESPERA_ACCESO_HUMANO", "BARRERA_HUMANA"}:
        return ruteo, str(item.get("motivo_ruteo") or "barrera humana vigente")
    if cambio_material:
        return "LISTA_SONDA", "reanudada por cambio material de consumidor/uso/contrato"
    if ruteo != "ESPERA_NUEVA_PISTA":
        return ruteo, str(item.get("motivo_ruteo") or "ruteo estructurado vigente")
    if _evidencia_nueva_aplicable(estado, item):
        return "LISTA_SONDA", "reanudada por evidencia nueva estructurada y aplicable"
    revision = estado.get("proxima_revision") or item.get("proxima_revision")
    if _revision_por_evento(revision):
        return ruteo, f"espera nueva pista; revisión condicionada a {revision}"
    proxima = _fecha(revision)
    if proxima and corte >= proxima:
        return "LISTA_SONDA", f"reanudada al vencer revisión {proxima}"
    return ruteo, (f"espera nueva pista; revisión {proxima}" if proxima else
                    "espera nueva pista sin fecha vencida")


def _contrato_derivado(base: dict) -> dict:
    etapa = _etapa_faltante(base)
    responsable = _responsable(base, etapa)
    ruteo, motivo = _ruteo_automatico(base, etapa)
    naturaleza = _naturaleza_nc(base)
    aplica_ciencia = naturaleza == "CIENTIFICA_O_DE_ADOPCION"
    if not aplica_ciencia and ruteo == "LISTA_SONDA":
        ruteo = "NO_SONDA"
        motivo = f"{naturaleza}; no es una búsqueda científica pública"
    identidad = "\t".join(str(base.get(k) or "") for k in (
        "id", "que_no_se_corrio", "impacto", "sucesor", "estado"))
    return {
        "id": base["id"],
        "version_pregunta": "AUTO-NC-v1-" + hashlib.sha256(
            identidad.encode("utf-8")).hexdigest()[:12],
        "consumidor": "/".join(filter(None, (base.get("acto"), base.get("pieza")))),
        "uso": "INVESTIGACION-DE-BRECHA; uso científico por decidir",
        "prioridad_consumidor": 60,
        "bloqueo_material": 1,
        "asignacion": responsable,
        "modos": ["CONSTRUCTO", "HERMANAS", "LATERAL"],
        "poblacion": "NO_ESPECIFICADA_EN_NC; verificar antes de evaluar suficiencia",
        "unidad": "NO_ESPECIFICADA_EN_NC; verificar antes de calcular",
        "periodo": "EL_DECLARADO_POR_LA_NC; no inferir vigencia",
        "variables": base.get("que_no_se_corrio") or "brecha explícita de la NC",
        "evidencia_disponible": base.get("impacto") or "sin evidencia resumida",
        "brecha": base.get("que_no_se_corrio") or "brecha vigente",
        "investigacion_previa": base.get("razon") or "no asentada",
        "frontera_previa": base.get("impacto") or "no asentada",
        "siguiente_accion": _siguiente_accion(base, etapa, responsable),
        "etapa_faltante": etapa,
        "responsable": responsable,
        "estado_ruteo": ruteo,
        "motivo_ruteo": motivo,
        "naturaleza_necesidad": naturaleza,
        "contrato_operativo": (
            "DESCRIPCION_MINIMA_DERIVADA" if aplica_ciencia else
            "OPERATIVO_DERIVADO_SIN_CAMPOS_CIENTIFICOS_FICTICIOS"),
        "contrato_cientifico_completo": False,
        "aplica_contrato_cientifico": aplica_ciencia,
        "opciones_decision": ([
            "MANTENER_ESTADO_VIGENTE",
            "APROBAR_SIGUIENTE_ACCION_DESCRITA",
            "DESCARTAR_O_DIFERIR_CON_CAUSA",
        ] if etapa == "DECISION_CIENTIFICA" else []),
    }


def _contrato_cientifico_explicito_completo(item: dict) -> bool:
    """No confunde placeholders ni prosa genérica con un contrato científico."""
    requeridos = (
        "version_pregunta", "consumidor", "uso", "poblacion", "unidad",
        "periodo", "variables", "evidencia_disponible", "brecha",
        "investigacion_previa", "frontera_previa", "siguiente_accion",
    )
    prohibidos = ("NO_ESPECIFIC", "EL_DECLARADO_POR", "brecha vigente",
                  "sin evidencia resumida", "no asentada")
    return bool(
        item.get("modos") and
        all(isinstance(item.get(k), str) and item[k].strip() for k in requeridos) and
        not any(str(item[k]).startswith(prohibidos) for k in requeridos)
    )


def contratos_vigentes(cfg: dict, raiz: Path = RAIZ) -> dict[str, dict]:
    fuentes = fuentes_demanda_vigente(cfg, raiz)
    independientes = _demandas_independientes(cfg)
    explicitos = {x["id"]: x for x in cfg.get("necesidades", [])}
    explicitos.update(independientes)
    sucesoras = {
        anterior: item["id"]
        for item in cfg.get("necesidades", [])
        for anterior in item.get("sucede_necesidades", [])
    }
    contratos: dict[str, dict] = {}
    for ident, base in fuentes.items():
        if ident in explicitos:
            item = dict(explicitos[ident])
            item.setdefault("etapa_faltante", _etapa_faltante(base))
            item.setdefault("responsable", item.get("asignacion") or _responsable(
                base, item["etapa_faltante"]))
            item.setdefault("estado_ruteo", "LISTA_SONDA" if item.get("lista") else
                            "NO_SONDA")
            item.setdefault("motivo_ruteo", "contrato explícito vigente")
            item.setdefault("aplica_contrato_cientifico", True)
            item.setdefault("naturaleza_necesidad", (
                "CIENTIFICA_O_DE_ADOPCION" if item["aplica_contrato_cientifico"]
                else "OPERATIVA_TECNICA_O_DOCUMENTAL"))
            completo = (
                item.get("aplica_contrato_cientifico") is True and
                item.get("contrato_cientifico_completo", True) is not False and
                _contrato_cientifico_explicito_completo(item))
            item["contrato_cientifico_completo"] = completo
            item.setdefault(
                "contrato_operativo",
                "COMPLETO_CIENTIFICO_EXPLICITO" if completo else
                "EXPLICITO_INCOMPLETO")
            item.setdefault("opciones_decision", [])
        else:
            item = _contrato_derivado(base)
        if ident in sucesoras:
            item["estado_ruteo"] = "ABSORBIDA_POR_SUCESORA_VIGENTE"
            item["motivo_ruteo"] = (
                f"la investigación continúa bajo {sucesoras[ident]}; no duplicar")
            item["responsable"] = sucesoras[ident]
            item["siguiente_accion"] = (
                f"seguir el estado y la siguiente acción de {sucesoras[ident]}")
        item["origen_demanda"] = base.get("origen_demanda", "NC_ABIERTA")
        item.setdefault("antecedentes_nc", [])
        contratos[ident] = item
    return contratos


def _lee_json(path: Path) -> dict:
    try:
        dato = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return dato if isinstance(dato, dict) else {}


def _reserva_activa(path: Path, ahora: dt.datetime) -> dict | None:
    dato = _lee_json(path)
    try:
        vence = dt.datetime.fromisoformat(dato["vence"])
    except (KeyError, TypeError, ValueError):
        return None
    return dato if vence > ahora else None


def selecciona(cfg: dict, corte: dt.date, maximo: int = 3,
               nombradas: set[str] | None = None, raiz: Path = RAIZ,
               ahora: dt.datetime | None = None,
               cambios_materiales: set[str] | None = None) -> dict:
    nombradas = nombradas or set()
    cambios_materiales = cambios_materiales or set()
    ahora = ahora or _ahora()
    fuentes = fuentes_demanda_vigente(cfg, raiz)
    estado_dir = raiz / cfg["estado_dir"]
    reserva_dir = raiz / cfg["reservas_runtime_dir"]
    configuradas = {n["id"] for n in cfg.get("necesidades", [])}
    abiertas = {i for i, r in necesidades_canonicas(cfg, raiz).items()
               if r.get("estado") == "ABIERTA"}
    contratos = contratos_vigentes(cfg, raiz)
    excluidos: list[dict] = []
    candidatas: list[tuple[tuple, dict]] = []

    for item in contratos.values():
        ident = item["id"]
        base = fuentes.get(ident)
        if base is None:
            excluidos.append({"id": ident, "razon": "no existe en la fuente canónica"})
            continue
        if base.get("estado") not in {"ABIERTA", "VIGENTE"}:
            excluidos.append({"id": ident, "razon": f"estado canónico {base.get('estado')}"})
            continue
        estado = _lee_json(estado_dir / f"{ident}.json")
        if estado.get("version_pregunta") not in (None, item["version_pregunta"]):
            estado = {}  # pregunta nueva: no hereda agotamiento de la versión anterior
        ruteo, motivo_ruteo = _ruteo_efectivo(
            item, estado, corte, cambio_material=ident in cambios_materiales)
        barrera_humana = ruteo in {"ESPERA_ACCESO_HUMANO", "BARRERA_HUMANA"}
        if ruteo != "LISTA_SONDA" and (barrera_humana or ident not in nombradas):
            excluidos.append({
                "id": ident,
                "razon": (
                    f"ruteo={ruteo}: {motivo_ruteo}; "
                    f"responsable={item.get('responsable')}; "
                    f"siguiente={item.get('siguiente_accion')}")})
            continue
        reserva_cfg = _fecha(item.get("reserva_hasta"))
        if (item.get("asignacion") not in (None, "", "servicio-gen2-38")
                and reserva_cfg and corte <= reserva_cfg):
            excluidos.append({"id": ident, "razon":
                              f"asignada a {item['asignacion']} hasta {reserva_cfg}"})
            continue
        reserva = _reserva_activa(reserva_dir / f"{ident}.json", ahora)
        if reserva:
            excluidos.append({"id": ident, "razon":
                              f"reserva runtime de {reserva.get('owner')} hasta {reserva.get('vence')}"})
            continue
        revision = estado.get("proxima_revision") or item.get("proxima_revision")
        espera_evento = _revision_por_evento(revision)
        if (espera_evento and ident not in cambios_materiales and
                not _evidencia_nueva_aplicable(estado, item)):
            excluidos.append({
                "id": ident,
                "razon": f"revisión condicionada a {revision}",
            })
            continue
        # EVENTO es una condición, no una fecha. Si una señal estructurada la
        # reactiva, debe avanzar sin caer después en el parser ISO.
        proxima = None if espera_evento else _fecha(revision)
        if (proxima and corte < proxima and ident not in nombradas and
                ident not in cambios_materiales and
                not _evidencia_nueva_aplicable(estado, item)):
            excluidos.append({"id": ident, "razon": f"revisión no vence hasta {proxima}"})
            continue
        elegido = dict(item)
        elegido["estado_ruteo_declarado"] = item.get("estado_ruteo")
        elegido["estado_ruteo"] = ruteo
        elegido["motivo_ruteo"] = motivo_ruteo
        elegido["pregunta"] = base.get("que_no_se_corrio", "")
        elegido["impacto_canonico"] = base.get("impacto", "")
        elegido["estado_previo"] = estado
        ultima = _fecha(estado.get("ultima_exploracion"))
        clave = (int(item["prioridad_consumidor"]), -int(item["bloqueo_material"]),
                 ultima.toordinal() if ultima else 0, ident)
        candidatas.append((clave, elegido))

    elegidos = [x for _clave, x in sorted(candidatas, key=lambda x: x[0])[:maximo]]
    por_tope = [x for _clave, x in sorted(candidatas, key=lambda x: x[0])[maximo:]]
    excluidos.extend({"id": x["id"], "razon": f"lista, fuera del tope maximo={maximo}"}
                     for x in por_tope)
    return {
        "version": cfg["version"], "corte": corte.isoformat(), "maximo": maximo,
        "demanda_activa_total": len(abiertas), "demanda_configurada": len(configuradas),
        "demandas_independientes_vigentes": len(_demandas_independientes(cfg)),
        "demanda_vigente_total": len(fuentes),
        "demanda_con_contrato_operativo": len(contratos),
        "elegidos": elegidos, "excluidos": excluidos,
    }


def _naturaleza_elemento(tipo: str) -> str:
    if tipo.startswith("celda_"):
        return "EVALUACION_O_DIAGNOSTICO"
    if tipo.startswith("coeficiente"):
        return "COEFICIENTE_DEL_MOTOR"
    if tipo == "momento":
        return "MOMENTO_O_TRANSFORMACION"
    if tipo == "corte_pi":
        return "CORTE_ESTRUCTURAL"
    return "PROBABILIDAD_O_CONDUCTA"


def _proposito_elemento(tipo: str) -> str:
    if tipo == "celda_R":
        return "ARBITRO_EMPIRICO_DE_EVALUACION; NO_PARAMETRO_M"
    if tipo in {"celda_L", "celda_M", "celda_AGREGADO", "celda_D"}:
        return "EVALUACION_DEL_MODELO; NO_ADOPCION_AUTOMATICA"
    if tipo.startswith("coeficiente"):
        return "PARAMETRIZACION_DEL_MOTOR"
    if tipo == "momento":
        return "CALIBRACION_O_HOLDOUT_SEGUN_CATALOGO"
    if tipo == "corte_pi":
        return "DECISION_ESTRUCTURAL_DEL_MODELO"
    return "USO_DIRECTO_POR_CONSUMIDOR_DECLARADO"


def _indice_conciliacion(cfg: dict) -> dict[str, dict]:
    indice: dict[str, dict] = {}
    for grupo in cfg.get("conciliacion_elementos", []):
        for ident in grupo["elementos"]:
            if ident in indice:
                raise ValueError(f"elemento repetido en conciliación: {ident}")
            indice[ident] = grupo
    return indice


def _oferta_resultado(fila: dict, proposito: str, evidencia: str) -> dict:
    return {
        "oferta_id": fila["resultado_id"],
        "resultado_id": fila["resultado_id"],
        "corrida_id": fila.get("corrida_id"),
        "spec_id": fila.get("spec_id"),
        "valor": fila.get("valor"),
        "fuente": fila.get("fuente_replay") or evidencia,
        "ola": "SEGUN_SPEC_SELLADA",
        "estimando": fila.get("unidad"),
        "unidad": fila.get("unidad"),
        "poblacion": "SEGUN_SPEC_SELLADA_Y_CODIFICACION_CONGELADA",
        "transformacion": "NINGUNA; valor leído del RESULT exacto",
        "proposito": proposito,
        "compatibilidad": "EXACTA_POR_REGLA_TIPO_Y_ARTEFACTO; NO_POR_SUBCADENA_RES",
        "evidencia": evidencia,
        "estado": fila.get("estado"),
        "validacion_independiente": fila.get("validacion_independiente"),
    }


def _oferta_evaluacion(uso: dict, resultados: dict[str, dict], cfg: dict) -> dict | None:
    tipo = uso.get("tipo_uso") or ""
    regla = uso.get("reglas_impacto") or ""
    consumidor = uso.get("consumidor") or ""
    rid = None
    if tipo == "celda_R":
        rid = f"RESULT-R-{regla}-PUNTO"
    elif tipo == "celda_M":
        rid = f"RESULT-M-{regla}-P"
    elif tipo == "celda_L":
        sufijo = "L-CORPUS" if consumidor.endswith("L:L+corpus") else "L-SOLO"
        rid = f"RESULT-TRIADA-{regla.replace('-', '_')}-{sufijo}"
    elif tipo == "celda_AGREGADO":
        rid = f"RESULT-TRIADA-{regla.replace('-', '_')}-EN-U3"
    if not rid or rid not in resultados:
        return None
    evidencia = (cfg.get("fuente_codificacion_r") if tipo == "celda_R" else
                 cfg.get("fuente_universo_triada")) or cfg["fuente_resultados"]
    oferta = _oferta_resultado(
        resultados[rid], _proposito_elemento(tipo), evidencia)
    oferta["autoridad"] = (
        "FP-370_FIRMADA_EJECUTADA" if tipo == "celda_R" else
        "SPEC_Y_CORRIDA_DE_EVALUACION_SELLADAS")
    return oferta


def _campos_receta_faltantes(anterior: dict) -> list[str]:
    mapa = {
        "payload_ids": "payload_ids_legacy", "sha256": "sha256_legacy",
        "script": "script_legacy", "spec": "spec_legacy",
        "spec_sha": "spec_sha_legacy",
    }
    return [nombre for nombre, campo in mapa.items()
            if str(anterior.get(campo) or "").startswith("NO-DECLARADO")]


def proyecta_elementos(cfg: dict, contratos: dict[str, dict],
                       raiz: Path = RAIZ) -> list[dict]:
    """Concilia el alcance por identidad y propósito, nunca por parecido textual."""
    usos = _tsv(raiz / cfg["fuente_usos"])
    # `tolerancia`/`funciones_dependencia`/`fuente_replay` salieron de
    # resultados.tsv en COMMIT-A (ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2):
    # el join las reconstruye desde corridas.tsv por corrida_id. Ruta de
    # corridas.tsv: mismo directorio que fuente_resultados. `sys.path` se
    # ajusta aqui (no `from tools.vista import`) porque este archivo se
    # invoca como script suelto (`python3 tools/adq_investigacion.py`),
    # sin la raiz del repo en el path -- un `from tools.X import` revienta
    # con `ModuleNotFoundError` fuera de un checkout con RAIZ en sys.path.
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    from vista import join_resultado, corridas_por_id
    ruta_resultados = raiz / cfg["fuente_resultados"]
    _corridas = corridas_por_id(ruta_resultados.parent / "corridas.tsv")
    # `linajes={}`: desde VISTA-NORMALIZADA-4 `camino_linaje` ya no viaja
    # en resultados.tsv y el join lo derivaria importando corrida0 (todo el
    # arbol milpa/CALC). Esta proyeccion no lo consume -- el linaje que
    # publica sale de `usos.tsv` -- asi que no se paga ni se exige.
    resultados = {x["resultado_id"]: join_resultado(x, _corridas, linajes={})
                  for x in _tsv(ruta_resultados)}
    demanda = {x["resultado_id"]: x for x in _tsv(
        raiz / cfg["fuente_demanda_resultados"])}
    decisiones = _tsv(raiz / cfg["fuente_decisiones"])
    mapa_modelo = _tsv(raiz / cfg["fuente_necesidad_modelo"])
    utilidad = _tsv(raiz / cfg["fuente_utilidad_modelo"])
    n_por_objeto: dict[str, list[dict]] = {}
    for fila in mapa_modelo:
        n_por_objeto.setdefault(fila["objeto_modelo_origen"], []).append(fila)
    utilidad_por_n: dict[str, list[dict]] = {}
    for fila in utilidad:
        utilidad_por_n.setdefault(fila["necesidad_id"], []).append(fila)

    conciliacion = _indice_conciliacion(cfg)

    elementos = []
    for uso in usos:
        if uso.get("activo") != "SI":
            continue
        resultado_id = uso.get("corrida0_resultado_id") or ""
        resultado = resultados.get(resultado_id, {})
        regla = uso.get("reglas_impacto") or ""
        consumidor = uso["consumidor"]
        # La proyección no interpreta suficiencia por segunda vez.  Consulta
        # exactamente la misma guardia usada por consulta_gen2 y después sólo
        # refleja su decisión para esta identidad RESULT+uso.
        try:
            from tools import adq_suficiencia
        except ImportError:
            import adq_suficiencia
        guardia = adq_suficiencia.proyecta_consumidor(
            consumidor, cfg, raiz,
            resultado_id=resultado_id or None,
            uso_solicitado=uso.get("uso_solicitado") or None)
        usos_alcance_menor = []
        # Los vínculos de uso pueden sobrevivir al cierre histórico de una NC
        # (p. ej. NC-0126); se leen del registro configurado completo, no sólo
        # de la selección de investigación vigente.
        for contrato in cfg.get("necesidades", []):
            for vinculo_menor in contrato.get("vinculos_alcance_menor", []):
                if not all((
                    vinculo_menor.get("consumidor") == consumidor,
                    vinculo_menor.get("resultado_bloqueado_id") == resultado_id,
                )):
                    continue
                uso_menor = vinculo_menor.get("uso_menor")
                guardia_menor = adq_suficiencia.proyecta_consumidor(
                    consumidor, cfg, raiz,
                    resultado_id=resultado_id or None,
                    uso_solicitado=uso_menor)
                usos_alcance_menor.append({
                    "uso": uso_menor,
                    "categoria": vinculo_menor.get("categoria"),
                    "evento": vinculo_menor.get("evento"),
                    "transformacion": vinculo_menor.get("transformacion"),
                    "limites": vinculo_menor.get("limites"),
                    "disponible_hoy": bool(
                        guardia_menor and guardia_menor[
                            "accion_consumidor"] ==
                        "SOLO_EMITIR_ALCANCE_MENOR_ROTULADO"),
                    "guardia": ({
                        "necesidad_id": guardia_menor["necesidad_id"],
                        "estado_efectivo": guardia_menor["estado_efectivo"],
                        "accion_consumidor": guardia_menor[
                            "accion_consumidor"],
                        "motivo": guardia_menor["motivo_bloqueo"],
                    } if guardia_menor else None),
                })
        grupo = conciliacion.get(uso["resultado_id"], {})
        # La conciliación conserva referencias históricas aunque una NC cierre.
        # Sólo los contratos todavía vigentes entran a faltantes y ruteo.
        necesidades = [
            ident for ident in grupo.get("necesidades_nc", [])
            if ident in contratos
        ]
        for ident, contrato in contratos.items():
            por_consumidor = consumidor in contrato.get("consumidores_consulta", [])
            por_regla = regla in contrato.get("reglas_motor", [])
            if por_consumidor or por_regla:
                if ident not in necesidades:
                    necesidades.append(ident)
        adoptada = uso.get("corrida0_generacion") == "GEN2" and bool(resultado_id)
        bloqueada = adoptada and any(
            any(v.get("consumidor") == consumidor
                for v in contratos[n].get("vinculos_consulta", []))
            for n in necesidades)
        anterior = demanda.get(uso["resultado_id"], {})
        ofertas = [dict(x) for x in grupo.get("ofertas", [])]
        oferta_eval = _oferta_evaluacion(uso, resultados, cfg)
        if oferta_eval:
            ofertas.append(oferta_eval)
        for oferta in ofertas:
            rid = oferta.get("resultado_id")
            if rid and rid in resultados:
                fila = resultados[rid]
                oferta.setdefault("valor", fila.get("valor"))
                oferta.setdefault("corrida_id", fila.get("corrida_id"))
                oferta.setdefault("spec_id", fila.get("spec_id"))
                oferta.setdefault("estado", fila.get("estado"))
                oferta.setdefault("validacion_independiente",
                                  fila.get("validacion_independiente"))
        faltantes: list[str] = []
        if grupo:
            faltantes.extend(grupo.get("faltantes", []))
        elif oferta_eval:
            faltantes = []
        elif adoptada:
            if not resultado or resultado.get("estado") != "SELLADA":
                faltantes.append("CALCULO")
            elif resultado.get("validacion_independiente") != "PASA":
                faltantes.append("VALIDACION")
        else:
            veredictos = " ".join(str(x.get("valor") or "") for x in ofertas)
            if "ADOPTABLE" in veredictos and "NO-ADOPTABLE" not in veredictos:
                faltantes.append("ADOPCION")
            elif ofertas:
                faltantes.append("DECISION_CIENTIFICA")
            elif anterior.get("receta_legacy") == "SIN-RECETA":
                faltantes.append("DECISION_CIENTIFICA")
            else:
                faltantes.append("PREPARACION")
        for ident in necesidades:
            etapa = contratos[ident].get("etapa_faltante")
            if not grupo and etapa and etapa not in faltantes:
                faltantes.append(etapa)
        modelo = n_por_objeto.get(regla, [])
        necesidades_modelo = sorted({x["necesidad_id"] for x in modelo})
        utilidad_modelo = [
            {
                "relacion_id": x["relacion_id"],
                "necesidad_id": x["necesidad_id"],
                "estado_productivo": x["estado_productivo"],
                "uso_actual": x["uso_actual"],
                "siguiente_accion": x["siguiente_accion"],
                "evidencia_ref": x["evidencia_ref"],
            }
            for n in necesidades_modelo for x in utilidad_por_n.get(n, [])
        ]
        decisiones_resultado = [
            {"objeto": x["objeto"], "decision": x["decision"],
             "fuente": x["fuente"], "fecha": x["fecha"]}
            for x in decisiones if x.get("objeto") in {
                resultado.get("spec_id"), consumidor, regla,
                uso["resultado_id"], anterior.get("corrida_natural"),
                *(x.get("spec_id") for x in ofertas),
                *(x.get("resultado_id") for x in ofertas),
                *(grupo.get("autoridades", [])),
            }]
        evidencias = sorted(set(filter(None, (
            f"{cfg['fuente_usos']}#{uso['resultado_id']}",
            f"{cfg['fuente_resultados']}#{resultado_id}" if resultado_id else None,
            *[f"{cfg['fuente_resultados']}#{x.get('resultado_id')}"
              for x in ofertas if x.get("resultado_id")],
            *[x.get("evidencia") for x in ofertas],
            resultado.get("validacion_ref"), uso.get("fuente_replay"),
            *[x.get("fuentes_verificacion") for x in modelo],
            *[f"{cfg['fuente_necesidades']}#{n}" for n in necesidades],
            *[x["fuente"] for x in decisiones_resultado],
        ))))
        if guardia and guardia["accion_consumidor"] == "NO_EMITIR_RESULTADO_SOLICITADO":
            situacion = "PENDIENTE_DATOS_O_DECISION_DE_USO"
        elif grupo.get("situacion"):
            situacion = grupo["situacion"]
        elif oferta_eval:
            situacion = "EVALUACION_GEN2_DISPONIBLE"
        elif bloqueada:
            situacion = "PENDIENTE_DATOS_O_DECISION_DE_USO"
        elif not adoptada:
            situacion = f"PENDIENTE_{faltantes[0]}"
        elif resultado.get("estado") == "SELLADA" and resultado.get(
                "validacion_independiente") == "PASA" and not necesidades:
            situacion = "CUBIERTA"
        elif faltantes:
            situacion = f"PENDIENTE_{faltantes[0]}"
        else:
            situacion = "CUBIERTA"
        siguientes = list(grupo.get("siguiente_accion", []))
        siguientes.extend(contratos[n]["siguiente_accion"] for n in necesidades
                           if n in contratos)
        if not siguientes:
            if adoptada and faltantes == ["VALIDACION"]:
                siguientes = ["ejecutor-validacion: validar el RESULT sellado antes de ampliar su uso"]
            elif oferta_eval:
                siguientes = ["consumir como evaluación bajo su spec; no trasladar R a M ni adoptar automáticamente"]
            elif not adoptada:
                campos = _campos_receta_faltantes(anterior)
                detalle = ", ".join(campos) if campos else "definición, método y uso"
                siguientes = [
                    f"motor-gen2: completar {detalle} para "
                    f"{anterior.get('corrida_natural') or uso['resultado_id']} "
                    f"({uso['resultado_id']}, {uso.get('tipo_uso')}, {consumidor}); "
                    "no reutilizar el valor GEN1"]
            else:
                siguientes = ["mantener adopción; reabrir sólo por evidencia o decisión nueva aplicable"]
        elementos.append({
            "elemento_id": uso["resultado_id"],
            "consumidor": consumidor,
            "regla": regla,
            "naturaleza": _naturaleza_elemento(uso.get("tipo_uso") or ""),
            "proposito": _proposito_elemento(uso.get("tipo_uso") or ""),
            "uso_vigente": uso.get("uso_solicitado"),
            "contrato_id": (grupo.get("contrato_id") or resultado.get("spec_id") or
                            anterior.get("corrida_natural") or uso["resultado_id"]),
            "identidad_contrato": {
                "elemento_id": uso["resultado_id"],
                "tipo": uso.get("tipo_uso"),
                "consumidor": consumidor,
                "regla": regla,
            },
            "resultado_id": resultado_id,
            "resultado_estado": resultado.get("estado") or "SIN_RESULTADO_ADOPTADO",
            "validacion_independiente": resultado.get("validacion_independiente") or
            "NO_HECHA",
            "adopcion": ("ADOPTADO_EN_CONSUMIDOR_VIGENTE" if adoptada else
                         "NO_ADOPTADO; GEN1_ES_SOLO_ANTECEDENTE"),
            "antecedente_gen1": {
                "valor": anterior.get("valor_legacy") or "NO_DECLARADO",
                "estado": anterior.get("estado") or "NO_DECLARADO",
                "vigencia": anterior.get("vigencia") or "NO_DECLARADA",
            },
            "situacion": situacion,
            "faltantes": faltantes,
            "primer_faltante": faltantes[0] if faltantes else None,
            "campos_contrato_faltantes": _campos_receta_faltantes(anterior),
            "uso_disponible_hoy": (
                guardia["accion_consumidor"] != "NO_EMITIR_RESULTADO_SOLICITADO"
                if guardia else bool(grupo.get(
                    "uso_disponible_hoy", oferta_eval is not None or
                    situacion == "CUBIERTA"))),
            "guardia_uso": ({
                "necesidad_id": guardia["necesidad_id"],
                "estado_efectivo": guardia["estado_efectivo"],
                "accion_consumidor": guardia["accion_consumidor"],
                "motivo": guardia["motivo_bloqueo"],
            } if guardia else None),
            "usos_alcance_menor": usos_alcance_menor,
            "medicion_disponible_hoy": bool(
                grupo.get("medicion_disponible_hoy", adoptada and
                          not (uso.get("tipo_uso") or "").startswith("celda_"))),
            "incertidumbre_pendiente": (
                grupo.get("incertidumbre_pendiente") or
                ("FP-371 sigue abierta sólo para EE/IC con diseño aproximado; "
                 "el punto descriptivo de R está disponible"
                 if uso.get("tipo_uso") == "celda_R" and regla == "DIN-M-01"
                 else None)),
            "ejecutor_siguiente": grupo.get("ejecutor") or (
                "SONDA" if faltantes and faltantes[0] in {"FUENTE_O_VARIABLE", "ACCESO_O_DESCARGA"}
                else "MESA" if faltantes and faltantes[0] == "DECISION_CIENTIFICA"
                else "MOTOR_GEN2"),
            "necesidades_nc_abiertas": necesidades,
            "necesidades_utilidad_modelo": necesidades_modelo,
            "cruce_utilidad_modelo": (
                "RELACIONES_EXACTAS_POR_OBJETO_MODELO" if necesidades_modelo else
                "SIN_RELACION_EXACTA_POR_REGLA; no equivale a ausencia de datos"),
            "utilidad_modelo": utilidad_modelo,
            "decisiones_posteriores": decisiones_resultado,
            "ofertas_conciliadas": ofertas,
            "ofertas_no_adoptadas": [x.get("resultado_id") or x["oferta_id"]
                                      for x in ofertas],
            "advertencias": (["R_ES_ARBITRO_DE_EVALUACION; NO_ES_PARAMETRO_M"]
                              if uso.get("tipo_uso") == "celda_R" else []),
            "dependencias": {
                "resultado": resultado.get("depende_de") or None,
                "funciones": resultado.get("funciones_dependencia") or None,
                "camino_linaje": uso.get("camino_linaje") or None,
            },
            "evidencias": evidencias,
            "siguiente_accion": siguientes,
        })
    return elementos


def proyecta_demanda(cfg: dict, corte: dt.date, raiz: Path = RAIZ) -> dict:
    """Vista total: ninguna NC ni adopción GEN2 desaparece fuera del selector."""
    canonicas = necesidades_canonicas(cfg, raiz)
    fuentes = fuentes_demanda_vigente(cfg, raiz)
    contratos = contratos_vigentes(cfg, raiz)
    filas = []
    for ident, contrato in sorted(contratos.items()):
        base = fuentes[ident]
        estado = _lee_json(raiz / cfg["estado_dir"] / f"{ident}.json")
        if estado.get("version_pregunta") != contrato["version_pregunta"]:
            estado = {}
        filas.append({
            "id": ident,
            "version_pregunta": contrato["version_pregunta"],
            "pregunta": base.get("que_no_se_corrio", ""),
            "consumidor": contrato["consumidor"],
            "uso": contrato["uso"],
            "poblacion": contrato["poblacion"],
            "unidad": contrato["unidad"],
            "periodo": contrato["periodo"],
            "variables": contrato["variables"],
            "evidencia_disponible": contrato["evidencia_disponible"],
            "brecha": contrato["brecha"],
            "investigacion_previa": contrato["investigacion_previa"],
            "frontera": estado.get("frontera_no_examinada") or
            contrato["frontera_previa"],
            "cursor_continuacion": estado.get("cursor_continuacion"),
            "prioridad": contrato["prioridad_consumidor"],
            "etapa_faltante": contrato["etapa_faltante"],
            "responsable": contrato["responsable"],
            "siguiente_accion": contrato["siguiente_accion"],
            "estado_ruteo": contrato["estado_ruteo"],
            "motivo_ruteo": contrato["motivo_ruteo"],
            "condicion_reapertura": contrato.get("condicion_reapertura"),
            "opciones_decision": contrato["opciones_decision"],
            "suficiencia": estado.get("suficiencia") or
            contrato.get("suficiencia_actual"),
            "contrato_operativo": contrato["contrato_operativo"],
            "contrato_cientifico_completo": contrato[
                "contrato_cientifico_completo"],
            "aplica_contrato_cientifico": contrato[
                "aplica_contrato_cientifico"],
            "naturaleza_necesidad": contrato["naturaleza_necesidad"],
            "origen_demanda": contrato["origen_demanda"],
            "antecedentes_nc": contrato.get("antecedentes_nc", []),
            "evidencias": ([f"{cfg['fuente_necesidades']}#{ident}"]
                           if contrato["origen_demanda"] == "NC_ABIERTA" else
                           list(contrato.get("evidencias_guardia", []))),
        })
    elementos = proyecta_elementos(cfg, contratos, raiz)
    seleccion_siguiente = selecciona(cfg, corte, maximo=3, raiz=raiz)
    fuente = raiz / cfg["fuente_necesidades"]
    rutas_fuente = [cfg[k] for k in (
        "fuente_necesidades", "fuente_usos", "fuente_resultados",
        "fuente_demanda_resultados", "fuente_decisiones",
        "fuente_necesidad_modelo", "fuente_utilidad_modelo",
        "fuente_codificacion_r", "fuente_universo_triada")]
    fuentes_sha = {
        ruta: hashlib.sha256((raiz / ruta).read_bytes()).hexdigest()
        for ruta in rutas_fuente
    }
    fuentes_sha[str(CONFIG.relative_to(RAIZ))] = hashlib.sha256(
        (raiz / CONFIG.relative_to(RAIZ)).read_bytes()).hexdigest()
    canon_fuentes = "".join(
        f"{ruta}\t{sha}\n" for ruta, sha in sorted(fuentes_sha.items()))
    return {
        "generado": True, "version": cfg["version"], "corte": corte.isoformat(),
        "fuente": cfg["fuente_necesidades"],
        "sha256_fuente": hashlib.sha256(fuente.read_bytes()).hexdigest(),
        "fuentes_sha256": fuentes_sha,
        "sha256_insumos_demanda": hashlib.sha256(
            canon_fuentes.encode("utf-8")).hexdigest(),
        "advertencia_suficiencia": (
            "cero tareas elegibles sólo describe el selector; nunca acredita "
            "suficiencia general ni cierra necesidades"),
        "total_activas": len(filas),
        "total_nc_abiertas": sum(
            x.get("estado") == "ABIERTA" for x in canonicas.values()),
        "total_demandas_independientes": len(_demandas_independientes(cfg)),
        "contrato_cientifico_completo": sum(
            x["contrato_cientifico_completo"] for x in filas),
        "descripcion_minima_derivada": sum(
            x["contrato_operativo"] == "DESCRIPCION_MINIMA_DERIVADA" for x in filas),
        "contrato_operativo_explicito_no_cientifico": sum(
            x["contrato_operativo"] == "COMPLETO_OPERATIVO_NO_CIENTIFICO"
            for x in filas),
        "contrato_operativo_no_cientifico": sum(
            not x["aplica_contrato_cientifico"] for x in filas),
        "contrato_cientifico_incompleto": sum(
            x["aplica_contrato_cientifico"] and
            not x["contrato_cientifico_completo"] for x in filas),
        # Alias conservados para consumidores del JSON v1; ya no equiparan una
        # descripción genérica con completitud científica.
        "contrato_completo": sum(
            x["contrato_cientifico_completo"] for x in filas),
        "contrato_minimo_derivado": sum(
            x["contrato_operativo"] == "DESCRIPCION_MINIMA_DERIVADA" for x in filas),
        "contrato_incompleto": sum(
            x["aplica_contrato_cientifico"] and
            not x["contrato_cientifico_completo"] for x in filas),
        "elementos_gen2_vigentes_total": len(elementos),
        "elementos_con_brecha_abierta": sum(
            bool(x["necesidades_nc_abiertas"]) for x in elementos),
        "elementos_con_alcance_menor_disponible": sum(
            any(u["disponible_hoy"] for u in x["usos_alcance_menor"])
            for x in elementos),
        "situaciones_elementos": {
            estado: sum(x["situacion"] == estado for x in elementos)
            for estado in sorted({x["situacion"] for x in elementos})
        },
        "seleccion_siguiente": seleccion_siguiente,
        "elementos_gen2": elementos,
        "necesidades": filas,
    }


def cambio_pertinente_proyeccion(antes: dict, despues: dict) -> bool:
    """True si `despues` difiere de `antes` en algo más que `corte`.

    `corte` avanza cada día aunque nada del registro haya cambiado; un
    consumidor mecánico (el cron) que republicara por eso solo generaría
    commits/PR sin contenido nuevo (ENCARGO GEN2-DEMANDA-VIGENTE-ANTES-
    DESPACHO, 15/sep/2026: "evitar commits/PR repetidos solo por una marca
    de tiempo"). Cualquier otra diferencia -- NC abierta/cerrada, cambio de
    ruteo, selección siguiente -- sí es pertinente, incluida una que sólo
    exista porque `corte` avanzó (p. ej. una revisión que vence hoy).
    """
    a = dict(antes)
    a.pop("corte", None)
    b = dict(despues)
    b.pop("corte", None)
    return a != b


def reserva_seleccion(seleccion: dict, owner: str, cfg: dict,
                      raiz: Path = RAIZ, ahora: dt.datetime | None = None) -> list[str]:
    ahora = ahora or _ahora()
    vence = ahora + dt.timedelta(minutes=int(cfg.get("reserva_minutos", 75)))
    directorio = raiz / cfg["reservas_runtime_dir"]
    directorio.mkdir(parents=True, exist_ok=True)
    creadas: list[str] = []
    try:
        for item in seleccion.get("elegidos", []):
            path = directorio / f"{item['id']}.json"
            existente = _reserva_activa(path, ahora)
            if existente and existente.get("owner") != owner:
                raise RuntimeError(f"{item['id']} ya reservado por {existente.get('owner')}")
            _json_atomico(path, {"necesidad_id": item["id"], "owner": owner,
                                "inicio": ahora.isoformat(), "vence": vence.isoformat()})
            creadas.append(item["id"])
    except BaseException:
        libera(owner, cfg, raiz)
        raise
    return creadas


def libera(owner: str, cfg: dict, raiz: Path = RAIZ) -> list[str]:
    directorio = raiz / cfg["reservas_runtime_dir"]
    borradas: list[str] = []
    if not directorio.exists():
        return borradas
    for path in directorio.glob("*.json"):
        if _lee_json(path).get("owner") == owner:
            path.unlink(missing_ok=True)
            borradas.append(path.stem)
    return borradas


def actualiza_desde_resultados(path: Path, cfg: dict, raiz: Path = RAIZ) -> list[str]:
    dato = json.loads(path.read_text(encoding="utf-8"))
    validas = contratos_vigentes(cfg, raiz)
    escritas: list[str] = []
    estado_dir = raiz / cfg["estado_dir"]
    for r in dato.get("investigaciones", []):
        ident = r["necesidad_id"]
        if ident not in validas or r["version_pregunta"] != validas[ident]["version_pregunta"]:
            raise ValueError(f"resultado de investigación no corresponde al contrato vigente: {ident}")
        anterior = _lee_json(estado_dir / f"{ident}.json")
        hubo_avance = bool(r.get("candidatas"))
        ciclos_sin_avance = (0 if hubo_avance else
                             int(anterior.get("ciclos_sin_avance", 0)) + 1)
        corte = _fecha(dato.get("seleccion_investigacion", {}).get("corte"))
        proxima_revision = r["proxima_revision"]
        continuacion = r.get("estado") == "continua"
        if continuacion and corte:
            # Una frontera concreta se retoma en el ciclo siguiente, no se
            # manda a una pausa general de treinta días.
            proxima_revision = (corte + dt.timedelta(days=1)).isoformat()
        estado = {
            "necesidad_id": ident, "version_pregunta": r["version_pregunta"],
            "ultima_exploracion": dato.get("seleccion_investigacion", {}).get("corte"),
            "estado": r["estado"], "proxima_revision": proxima_revision,
            "cursor_continuacion": r["cursor_continuacion"],
            "frontera_no_examinada": r["frontera_no_examinada"],
            "evidencias": r["evidencias"], "suficiencia": r["suficiencia"],
            "continuacion_pendiente": continuacion,
            "ciclos_sin_avance": ciclos_sin_avance,
            "alternativa_requerida": (
                ciclos_sin_avance >= 2 and not hubo_avance),
            "alternativas": validas[ident].get("opciones_decision", [])
            if ciclos_sin_avance >= 2 and not hubo_avance else [],
        }
        # Una reprogramación de mesa es historia de la misma pregunta, no una
        # versión nueva ni una reapertura de su NC antecedente. El escritor de
        # resultados conserva esa historia cuando avanza el cursor.
        if anterior.get("reprogramaciones"):
            estado["reprogramaciones"] = anterior["reprogramaciones"]
        _json_atomico(estado_dir / f"{ident}.json", estado)
        escritas.append(ident)
    return escritas


def _ruta_presupuesto(cfg: dict, fecha: dt.date, raiz: Path) -> Path:
    directorio = cfg.get("presupuesto_runtime_dir", "forense/adq-log/estado")
    return raiz / directorio / f"presupuesto-{fecha.isoformat()}.json"


def _cantidades(dato: dict | None) -> dict[str, int]:
    dato = dato or {}
    return {k: max(0, int(dato.get(k, 0))) for k in DIMENSIONES_PRESUPUESTO}


def _reserva_normalizada(reserva: dict) -> dict:
    """Lee tanto el ledger v2 como la reserva plana publicada por #777."""
    salida = dict(reserva)
    reservada = _cantidades(reserva.get("reservada") or reserva)
    salida["reservada"] = reservada
    salida["estado"] = reserva.get("estado") or "activa"
    salida["consumido"] = _cantidades(reserva.get("consumido"))
    salida["devuelto"] = _cantidades(reserva.get("devuelto"))
    salida["checkpoints"] = list(reserva.get("checkpoints") or [])
    # Campos planos: compatibilidad para lectores y recibos ya desplegados.
    salida.update(reservada)
    return salida


def _componentes_presupuesto(cfg: dict, fecha: dt.date,
                             raiz: Path) -> tuple[Path, dict, dict, list[dict]]:
    limites = cfg.get("presupuesto_diario", {})
    defaults = {"necesidades": 3, "objetos": 5, "segundos_ejecutor": 3900}
    techo = {k: int(limites.get(k, defaults[k]))
             for k in DIMENSIONES_PRESUPUESTO}
    path = _ruta_presupuesto(cfg, fecha, raiz)
    dato = _lee_json(path)
    if dato.get("fecha") != fecha.isoformat():
        return path, techo, _cantidades({}), []
    reservas = [_reserva_normalizada(r) for r in dato.get("reservas", [])]
    activas = [r for r in reservas if r["estado"] in {
        "activa", "recuperacion_pendiente"}]
    if "consumido" in dato:
        consumido = _cantidades(dato["consumido"])
    else:
        # Migración sin reset: en v1 `usado` mezclaba consumo y reservas. Lo
        # que no está explicado por una reserva sigue siendo consumo firme.
        usado_legacy = _cantidades(dato.get("usado"))
        reservado = {k: sum(r["reservada"][k] for r in activas)
                     for k in DIMENSIONES_PRESUPUESTO}
        consumido = {k: max(0, usado_legacy[k] - reservado[k])
                     for k in DIMENSIONES_PRESUPUESTO}
    return path, techo, consumido, reservas


def _guarda_presupuesto(path: Path, fecha: dt.date, techo: dict,
                        consumido: dict, reservas: list[dict]) -> None:
    activas = [r for r in reservas if r["estado"] in {
        "activa", "recuperacion_pendiente"}]
    reservado_activo = {k: sum(r["reservada"][k] for r in activas)
                        for k in DIMENSIONES_PRESUPUESTO}
    usado = {k: consumido[k] + reservado_activo[k]
             for k in DIMENSIONES_PRESUPUESTO}
    _json_atomico(path, {
        "version": "GEN2-ADQ-PRESUPUESTO-V2",
        "fecha": fecha.isoformat(), "techo": techo,
        "consumido": consumido, "reservado_activo": reservado_activo,
        "usado": usado, "reservas": reservas,
    })


def _token_proceso(pid: int) -> str | None:
    try:
        texto = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
        # starttime es el campo 22; después del último ')' quedan campos 3+.
        return texto.rsplit(")", 1)[1].split()[19]
    except (FileNotFoundError, PermissionError, IndexError, ValueError):
        return None


def _proceso_reserva_vivo(reserva: dict) -> bool:
    try:
        pid = int(reserva["pid"])
    except (KeyError, TypeError, ValueError):
        return False
    esperado = reserva.get("proceso_inicio")
    actual = _token_proceso(pid)
    return bool(actual and esperado and actual == esperado)


def presupuesto_diario(cfg: dict, fecha: dt.date, raiz: Path = RAIZ) -> dict:
    path, techo, consumido, reservas = _componentes_presupuesto(cfg, fecha, raiz)
    activas = [r for r in reservas if r["estado"] in {
        "activa", "recuperacion_pendiente"}]
    reservado_activo = {k: sum(r["reservada"][k] for r in activas)
                        for k in DIMENSIONES_PRESUPUESTO}
    usado = {k: consumido[k] + reservado_activo[k]
             for k in DIMENSIONES_PRESUPUESTO}
    return {
        "fecha": fecha.isoformat(), "ruta": str(path), "techo": techo,
        "consumido": consumido, "reservado_activo": reservado_activo,
        "usado": usado,
        "disponible": {k: max(0, techo[k] - usado[k]) for k in techo},
        "reservas": reservas,
        "recuperacion_pendiente": [r["run_id"] for r in activas
                                    if r["estado"] == "recuperacion_pendiente"],
    }


def reserva_presupuesto(cfg: dict, fecha: dt.date, run_id: str, necesidades: int,
                        objetos: int, segundos: int, raiz: Path = RAIZ,
                        ahora: dt.datetime | None = None,
                        pid: int | None = None) -> dict:
    actual = presupuesto_diario(cfg, fecha, raiz)
    pedido = {"necesidades": necesidades, "objetos": objetos,
              "segundos_ejecutor": segundos}
    if any(r.get("run_id") == run_id for r in actual["reservas"]):
        return actual
    excede = [k for k, n in pedido.items() if n > actual["disponible"][k]]
    if excede:
        raise RuntimeError("presupuesto diario insuficiente: " + ", ".join(excede))
    ahora = ahora or _ahora()
    pid = pid or os.getpid()
    reserva = {
        "run_id": run_id, "estado": "activa",
        "registrada": ahora.isoformat(), "fecha_imputacion": fecha.isoformat(),
        "pid": pid, "proceso_inicio": _token_proceso(pid),
        "reservada": pedido, "consumido": _cantidades({}),
        "devuelto": _cantidades({}), "checkpoints": [], **pedido,
    }
    _guarda_presupuesto(Path(actual["ruta"]), fecha, actual["techo"],
                        actual["consumido"], [*actual["reservas"], reserva])
    return presupuesto_diario(cfg, fecha, raiz)


def checkpoint_presupuesto(cfg: dict, fecha: dt.date, run_id: str,
                           tipo: str, clave: str, raiz: Path = RAIZ,
                           ahora: dt.datetime | None = None) -> dict:
    """Checkpoint idempotente antes de iniciar una investigación/objeto."""
    if tipo not in {"necesidades", "objetos", "ejecutor"}:
        raise ValueError(f"tipo de checkpoint inválido: {tipo}")
    path, techo, consumido, reservas = _componentes_presupuesto(cfg, fecha, raiz)
    indice = next((i for i, r in enumerate(reservas)
                   if r.get("run_id") == run_id), None)
    if indice is None or reservas[indice]["estado"] != "activa":
        raise RuntimeError(f"reserva activa no encontrada: {run_id}")
    reserva = reservas[indice]
    identidad = f"{tipo}:{clave}"
    if not any(c.get("id") == identidad for c in reserva["checkpoints"]):
        if tipo in {"necesidades", "objetos"}:
            actuales = sum(c.get("tipo") == tipo for c in reserva["checkpoints"])
            if actuales >= reserva["reservada"][tipo]:
                raise RuntimeError(f"checkpoint excede reserva de {tipo}")
        ahora = ahora or _ahora()
        reserva["checkpoints"].append({
            "id": identidad, "tipo": tipo, "clave": clave,
            "registrado": ahora.isoformat(),
        })
        if tipo == "ejecutor":
            reserva["ejecutor_iniciado"] = ahora.isoformat()
        reservas[indice] = reserva
        _guarda_presupuesto(path, fecha, techo, consumido, reservas)
    return presupuesto_diario(cfg, fecha, raiz)


def liquida_presupuesto(cfg: dict, fecha: dt.date, run_id: str,
                        necesidades: int, objetos: int, segundos: int,
                        raiz: Path = RAIZ, ahora: dt.datetime | None = None,
                        asegurar_investigacion_iniciada: bool = False,
                        evidencia: str = "cierre-wrapper") -> dict:
    """Consolida trabajo real y devuelve una sola vez la reserva restante."""
    path, techo, consumido_total, reservas = _componentes_presupuesto(
        cfg, fecha, raiz)
    indice = next((i for i, r in enumerate(reservas)
                   if r.get("run_id") == run_id), None)
    if indice is None:
        raise RuntimeError(f"reserva no encontrada: {run_id}")
    reserva = reservas[indice]
    if reserva["estado"] == "liquidada":
        return presupuesto_diario(cfg, fecha, raiz)
    checkpoints = reserva.get("checkpoints", [])
    acreditado = {
        "necesidades": max(necesidades, sum(
            c.get("tipo") == "necesidades" for c in checkpoints)),
        "objetos": max(objetos, sum(
            c.get("tipo") == "objetos" for c in checkpoints)),
        "segundos_ejecutor": segundos,
    }
    if (asegurar_investigacion_iniciada and reserva.get("ejecutor_iniciado")
            and reserva["reservada"]["necesidades"] > 0
            and acreditado["necesidades"] == 0):
        # Una salida incompleta del LLM no vuelve cero un trabajo que el
        # wrapper sí acredita que arrancó. Sólo se imputa la primera unidad.
        acreditado["necesidades"] = 1
    acreditado = {k: min(max(0, int(acreditado[k])), reserva["reservada"][k])
                  for k in DIMENSIONES_PRESUPUESTO}
    devuelto = {k: reserva["reservada"][k] - acreditado[k]
                for k in DIMENSIONES_PRESUPUESTO}
    ahora = ahora or _ahora()
    reserva.update({
        "estado": "liquidada", "consumido": acreditado,
        "devuelto": devuelto, "liquidada": ahora.isoformat(),
        "evidencia_liquidacion": evidencia,
    })
    reservas[indice] = reserva
    consumido_total = {k: consumido_total[k] + acreditado[k]
                       for k in DIMENSIONES_PRESUPUESTO}
    _guarda_presupuesto(path, fecha, techo, consumido_total, reservas)
    return presupuesto_diario(cfg, fecha, raiz)


def recupera_reservas_huerfanas(cfg: dict, fecha: dt.date, run_id_actual: str,
                                lock_exclusivo: bool,
                                raiz: Path = RAIZ) -> dict:
    """Libera sólo reservas sin trabajo; deja incertidumbre material visible."""
    path, techo, consumido, reservas = _componentes_presupuesto(cfg, fecha, raiz)
    cambiadas = False
    ahora = _ahora()
    for reserva in reservas:
        if reserva["estado"] not in {"activa", "recuperacion_pendiente"}:
            continue
        if reserva.get("run_id") == run_id_actual or _proceso_reserva_vivo(reserva):
            continue
        checkpoints = reserva.get("checkpoints", [])
        inicio_ejecutor = reserva.get("ejecutor_iniciado") or any(
            c.get("tipo") == "ejecutor" for c in checkpoints)
        evidencia_proceso = bool(reserva.get("pid") and reserva.get("proceso_inicio"))
        if not lock_exclusivo or inicio_ejecutor or not evidencia_proceso:
            reserva["estado"] = "recuperacion_pendiente"
            reserva["motivo_recuperacion"] = (
                "falta evidencia suficiente para devolver: proceso no acreditado "
                "vivo y ejecutor iniciado o identidad de proceso ausente; liquidar "
                "con logs/eventos")
            cambiadas = True
            continue
        acreditado = {
            "necesidades": sum(c.get("tipo") == "necesidades" for c in checkpoints),
            "objetos": sum(c.get("tipo") == "objetos" for c in checkpoints),
            "segundos_ejecutor": 0,
        }
        acreditado = {k: min(acreditado[k], reserva["reservada"][k])
                      for k in DIMENSIONES_PRESUPUESTO}
        devuelto = {k: reserva["reservada"][k] - acreditado[k]
                    for k in DIMENSIONES_PRESUPUESTO}
        reserva.update({
            "estado": "liquidada", "consumido": acreditado,
            "devuelto": devuelto, "liquidada": ahora.isoformat(),
            "evidencia_liquidacion": "recuperación: lock exclusivo; proceso no vivo; ejecutor no inició",
        })
        consumido = {k: consumido[k] + acreditado[k]
                     for k in DIMENSIONES_PRESUPUESTO}
        cambiadas = True
    if cambiadas:
        _guarda_presupuesto(path, fecha, techo, consumido, reservas)
    return presupuesto_diario(cfg, fecha, raiz)


def _huella_material(cfg: dict, raiz: Path = RAIZ) -> str:
    rutas = [Path(cfg[k]) for k in (
        "fuente_necesidades", "fuente_usos", "fuente_resultados",
        "fuente_demanda_resultados", "fuente_decisiones",
        "fuente_necesidad_modelo", "fuente_utilidad_modelo",
    )]
    canon = ("config\t" + hashlib.sha256(json.dumps(
        cfg, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")).hexdigest() + "\n" + "".join(
        f"{ruta}\t{hashlib.sha256((raiz / ruta).read_bytes()).hexdigest()}\n"
        for ruta in sorted(rutas, key=str)))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _huellas_contratos(cfg: dict, raiz: Path = RAIZ) -> dict[str, str]:
    usos = _tsv(raiz / cfg["fuente_usos"])
    contratos = contratos_vigentes(cfg, raiz)
    elementos = proyecta_elementos(cfg, contratos, raiz)
    salida = {}
    for ident, contrato in contratos.items():
        consumidores = {contrato.get("consumidor"),
                        *contrato.get("consumidores_consulta", [])}
        reglas = set(contrato.get("reglas_motor", []))
        usos_afectados = [x for x in usos if (
            x.get("consumidor") in consumidores or
            x.get("reglas_impacto") in reglas)]
        elementos_afectados = [{
            "elemento_id": x.get("elemento_id"),
            "consumidor": x.get("consumidor"),
            "uso_vigente": x.get("uso_vigente"),
            "situacion": x.get("situacion"),
            "uso_disponible_hoy": x.get("uso_disponible_hoy"),
            "guardia_uso": x.get("guardia_uso"),
        } for x in elementos if (
            ident in x.get("necesidades_nc_abiertas", []) or
            x.get("consumidor") in consumidores or
            x.get("regla") in reglas)]
        material = {
            "contrato": {k: v for k, v in contrato.items()
                         if k not in {"motivo_ruteo"}},
            "usos": usos_afectados,
            "elementos": elementos_afectados,
        }
        canon = json.dumps(material, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"))
        salida[ident] = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    return salida


def _excluye_atendidas_runtime(investigacion: dict, previo: dict,
                               corte: dt.date, cambiadas: set[str]) -> dict:
    # El hijo publica el estado científico en una rama que mesa todavía no
    # fusionó y el launcher restaura después el SHA desplegado. El checkpoint
    # runtime evita volver a cobrar/repetir esa misma versión durante la
    # espera; una revisión vencida o un cambio material la habilitan otra vez.
    atendidas = previo.get("investigaciones_atendidas", {})
    elegibles_investigacion = []
    for item in investigacion["elegidos"]:
        ident = item["id"]
        marca = atendidas.get(ident, {})
        revision = marca.get("proxima_revision")
        espera_evento = _revision_por_evento(revision)
        proxima = None if espera_evento else _fecha(revision)
        misma_version = marca.get("version_pregunta") == item.get("version_pregunta")
        atendida_hoy = marca.get("fecha_imputacion") == corte.isoformat()
        if (misma_version and ident not in cambiadas and
                (espera_evento or (proxima and corte < proxima) or
                 (not proxima and atendida_hoy))):
            investigacion["excluidos"].append({
                "id": ident,
                "razon": (f"atendida por {marca.get('run_id')} para esta versión; "
                          f"próxima revisión {marca.get('proxima_revision') or 'después del día'}"),
            })
        else:
            elegibles_investigacion.append(item)
    investigacion["elegidos"] = elegibles_investigacion
    return investigacion


def comprueba_despacho(cfg: dict, corte: dt.date, raiz: Path = RAIZ,
                       ahora: dt.datetime | None = None) -> dict:
    """Chequeo determinista para el único scheduler; nunca invoca un LLM."""
    ahora = ahora or _ahora()
    presupuesto = presupuesto_diario(cfg, corte, raiz)
    try:
        from tools import adq_doctor
    except ImportError:
        import adq_doctor
    filas = _tsv(raiz / "data/curacion-registro/cola-adquisicion-registro.tsv")
    selector = adq_doctor.selecciona_filas(
        [(f.get("fuente_canonica", ""), f.get("estado_A4A5", ""),
          f.get("prioridad", ""), f.get("nota", "")) for f in filas],
        corte=corte, maximo=5)
    ruta_estado = raiz / cfg.get(
        "comprobacion_runtime", "forense/adq-log/estado/comprobacion.json")
    previo = _lee_json(ruta_estado)
    huella = _huella_material(cfg, raiz)
    huellas_contratos = _huellas_contratos(cfg, raiz)
    anteriores = previo.get("huellas_contratos", {})
    cambiadas = ({ident for ident, valor in huellas_contratos.items()
                  if ident in anteriores and anteriores[ident] != valor}
                 if anteriores else set())
    investigacion = _excluye_atendidas_runtime(selecciona(
        cfg, corte, 3, raiz=raiz, ahora=ahora,
        cambios_materiales=cambiadas), previo, corte, cambiadas)
    hora_diaria = (yaml.safe_load((raiz / "data/adq-config.yaml").read_text(
        encoding="utf-8")) or {}).get("calendario", {}).get("hora", "07:30")
    hora, minuto = map(int, hora_diaria.split(":"))
    from zoneinfo import ZoneInfo
    zona = (yaml.safe_load((raiz / "data/adq-config.yaml").read_text(
        encoding="utf-8")) or {}).get("calendario", {}).get(
            "zona_iana", "America/Mexico_City")
    ahora_local = ahora.astimezone(ZoneInfo(zona))
    ciclo_diario_pendiente = (
        previo.get("ultima_corrida") != corte.isoformat() and
        (ahora_local.hour, ahora_local.minute) >= (hora, minuto))
    trabajo = bool(selector["elegidos"] or investigacion["elegidos"])
    trabajo_con_cupo = bool(
        (selector["elegidos"] and presupuesto["disponible"]["objetos"] > 0) or
        (investigacion["elegidos"] and
         presupuesto["disponible"]["necesidades"] > 0))
    presupuesto_agotado = presupuesto["disponible"]["segundos_ejecutor"] <= 0
    despachar = not presupuesto_agotado and (trabajo_con_cupo or ciclo_diario_pendiente)
    razones = []
    if selector["elegidos"]:
        razones.append("adquisicion_atendible")
    if investigacion["elegidos"]:
        razones.append("investigacion_atendible")
    if ciclo_diario_pendiente:
        razones.append("ciclo_diario_pendiente_o_recuperacion")
    if previo.get("huella_material") not in (None, huella):
        razones.append("insumos_materiales_cambiaron")
    if presupuesto["recuperacion_pendiente"]:
        razones.append("reserva_pendiente_recuperacion")
    if not trabajo:
        razones.append("sin_trabajo_elegible")
    if presupuesto_agotado or (trabajo and not trabajo_con_cupo):
        razones.append("presupuesto_diario_agotado")
    if trabajo and not trabajo_con_cupo and not presupuesto_agotado:
        razones.append("dimensiones_requeridas_sin_cupo")
    estado_despacho = (
        "DESPACHAR" if despachar else
        "RESERVA_PENDIENTE_RECUPERACION" if presupuesto["recuperacion_pendiente"] else
        "PRESUPUESTO_REALMENTE_AGOTADO" if presupuesto_agotado else
        "DIMENSION_REQUERIDA_AGOTADA" if trabajo and not trabajo_con_cupo else
        "SIN_TRABAJO_ELEGIBLE")
    doc = {
        **previo, "ultima_comprobacion": ahora.isoformat(),
        "fecha_corte": corte.isoformat(), "huella_material": huella,
        "huellas_contratos": huellas_contratos,
        "identidades_afectadas": sorted(cambiadas),
        "cambio_material": previo.get("huella_material") not in (None, huella),
        "despachar": despachar, "estado_despacho": estado_despacho,
        "razones": razones,
        "elegibles": {"objetos": [x["id"] for x in selector["elegidos"]],
                       "necesidades": [x["id"] for x in investigacion["elegidos"]]},
        "presupuesto": presupuesto,
    }
    _json_atomico(ruta_estado, doc)
    return doc


def registra_ciclo(cfg: dict, fecha: dt.date, run_id: str,
                   raiz: Path = RAIZ,
                   resultado: Path | None = None) -> dict:
    path = raiz / cfg.get(
        "comprobacion_runtime", "forense/adq-log/estado/comprobacion.json")
    doc = _lee_json(path)
    marcas = dict(doc.get("investigaciones_atendidas", {}))
    if resultado and resultado.is_file():
        dato = _lee_json(resultado)
        for item in dato.get("investigaciones", []):
            ident = item.get("necesidad_id")
            version = item.get("version_pregunta")
            if ident and version:
                marcas[ident] = {
                    "version_pregunta": version,
                    "fecha_imputacion": fecha.isoformat(),
                    "run_id": run_id,
                    "estado": item.get("estado"),
                    "proxima_revision": item.get("proxima_revision"),
                    "registrada": _ahora().isoformat(),
                }
    doc.update({"ultima_corrida": fecha.isoformat(),
                "ultimo_run_id": run_id, "registrada": _ahora().isoformat(),
                "investigaciones_atendidas": marcas,
                # La comprobación previa no conoce todavía la reserva del hijo.
                # Persistir una foto nueva evita anunciar cupo ya consumido.
                "presupuesto": presupuesto_diario(cfg, fecha, raiz)})
    _json_atomico(path, doc)
    return doc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=CONFIG)
    ap.add_argument("--selecciona", action="store_true")
    ap.add_argument("--maximo", type=int, default=3)
    ap.add_argument("--nombrada", action="append", default=[])
    ap.add_argument("--corte")
    ap.add_argument("--reserva-seleccion", type=Path)
    ap.add_argument("--owner")
    ap.add_argument("--libera")
    ap.add_argument("--actualiza-desde-resultados", type=Path)
    ap.add_argument("--escribe-proyeccion", type=Path)
    ap.add_argument("--compara-proyeccion", type=Path, nargs=2,
                     metavar=("ANTES", "DESPUES"))
    ap.add_argument("--presupuesto", action="store_true")
    ap.add_argument("--reserva-presupuesto", action="store_true")
    ap.add_argument("--checkpoint-presupuesto", action="store_true")
    ap.add_argument("--liquida-presupuesto", action="store_true")
    ap.add_argument("--recupera-presupuesto", action="store_true")
    ap.add_argument("--necesidades", type=int, default=0)
    ap.add_argument("--objetos", type=int, default=0)
    ap.add_argument("--segundos", type=int, default=0)
    ap.add_argument("--pid", type=int)
    ap.add_argument("--tipo-checkpoint", choices=("necesidades", "objetos", "ejecutor"))
    ap.add_argument("--checkpoint-id")
    ap.add_argument("--asegura-investigacion-iniciada", action="store_true")
    ap.add_argument("--evidencia-liquidacion", default="cierre-wrapper")
    ap.add_argument("--lock-exclusivo", action="store_true")
    ap.add_argument("--comprueba-despacho", action="store_true")
    ap.add_argument("--registra-ciclo", action="store_true")
    ap.add_argument("--resultado-ciclo", type=Path)
    args = ap.parse_args(argv)
    cfg = cargar_config(args.config)
    corte = _fecha(args.corte) or dt.date.today()
    if args.presupuesto:
        print(json.dumps(presupuesto_diario(cfg, corte), ensure_ascii=False, indent=2))
        return 0
    if args.reserva_presupuesto:
        if not args.owner:
            ap.error("--reserva-presupuesto exige --owner")
        print(json.dumps(reserva_presupuesto(
            cfg, corte, args.owner, args.necesidades, args.objetos,
            args.segundos, pid=args.pid), ensure_ascii=False, indent=2))
        return 0
    if args.checkpoint_presupuesto:
        if not args.owner or not args.tipo_checkpoint or not args.checkpoint_id:
            ap.error("--checkpoint-presupuesto exige --owner, --tipo-checkpoint y --checkpoint-id")
        print(json.dumps(checkpoint_presupuesto(
            cfg, corte, args.owner, args.tipo_checkpoint, args.checkpoint_id),
            ensure_ascii=False, indent=2))
        return 0
    if args.liquida_presupuesto:
        if not args.owner:
            ap.error("--liquida-presupuesto exige --owner")
        print(json.dumps(liquida_presupuesto(
            cfg, corte, args.owner, args.necesidades, args.objetos,
            args.segundos,
            asegurar_investigacion_iniciada=args.asegura_investigacion_iniciada,
            evidencia=args.evidencia_liquidacion), ensure_ascii=False, indent=2))
        return 0
    if args.recupera_presupuesto:
        if not args.owner:
            ap.error("--recupera-presupuesto exige --owner")
        print(json.dumps(recupera_reservas_huerfanas(
            cfg, corte, args.owner, args.lock_exclusivo),
            ensure_ascii=False, indent=2))
        return 0
    if args.comprueba_despacho:
        dato = comprueba_despacho(cfg, corte)
        print(json.dumps(dato, ensure_ascii=False, indent=2))
        return 0 if dato["despachar"] else 10
    if args.registra_ciclo:
        if not args.owner:
            ap.error("--registra-ciclo exige --owner")
        print(json.dumps(registra_ciclo(
            cfg, corte, args.owner, resultado=args.resultado_ciclo),
            ensure_ascii=False))
        return 0
    if args.selecciona:
        print(json.dumps(selecciona(cfg, corte, args.maximo, set(args.nombrada)),
                         ensure_ascii=False, indent=2))
        return 0
    if args.reserva_seleccion:
        if not args.owner:
            ap.error("--reserva-seleccion exige --owner")
        dato = json.loads(args.reserva_seleccion.read_text(encoding="utf-8"))
        print(json.dumps({"reservadas": reserva_seleccion(dato, args.owner, cfg)},
                         ensure_ascii=False))
        return 0
    if args.libera:
        print(json.dumps({"liberadas": libera(args.libera, cfg)}, ensure_ascii=False))
        return 0
    if args.actualiza_desde_resultados:
        print(json.dumps({"actualizadas": actualiza_desde_resultados(
            args.actualiza_desde_resultados, cfg)}, ensure_ascii=False))
        return 0
    if args.compara_proyeccion:
        ruta_antes, ruta_despues = args.compara_proyeccion
        try:
            antes = json.loads(ruta_antes.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            antes = {}
        despues = json.loads(ruta_despues.read_text(encoding="utf-8"))
        print("si" if cambio_pertinente_proyeccion(antes, despues) else "no")
        return 0
    if args.escribe_proyeccion:
        dato = proyecta_demanda(cfg, corte)
        _json_atomico(args.escribe_proyeccion, dato)
        print(json.dumps({"ruta": str(args.escribe_proyeccion),
                          "total_activas": dato["total_activas"],
                          "contrato_completo": dato["contrato_completo"],
                          "contrato_minimo_derivado": dato[
                              "contrato_minimo_derivado"],
                          "contrato_incompleto": dato["contrato_incompleto"],
                          "elementos_gen2_vigentes_total": dato[
                              "elementos_gen2_vigentes_total"]},
                         ensure_ascii=False))
        return 0
    ap.error("elige --selecciona, --reserva-seleccion, --libera, "
             "--actualiza-desde-resultados o --escribe-proyeccion")


if __name__ == "__main__":
    raise SystemExit(main())
