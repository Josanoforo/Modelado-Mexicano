#!/usr/bin/env python3
"""Prepara y decide los CANDIDATO-GEN2 vigentes sin adoptar consumidores.

El envoltorio reutiliza ``relevo_usos.deriva`` y ``relevo_usos.contrato``.
Solo sustituye la familia genérica ``F-CANDIDATO-SIN-VEREDICTO`` por las
correspondencias explícitas de este acto, acreditadas contra las specs y los
consumidores publicados. ``corrida0 delta`` sigue siendo el único comparador.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

import relevo_usos  # noqa: E402


VEREDICTO = "CANDIDATO-GEN2"
DIMENSIONES = relevo_usos.DIMENSIONES
RE_SLOT = re.compile(r"RELEVO-(RES-\d{4})-VS-")
SLOTS_VIAS = {"RES-0053", "RES-0054", "RES-0055", "RES-0056"}


def _sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as fh:
        for bloque in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def _evidencia(rel: str, cita: str) -> dict:
    ruta = RAIZ / rel
    return {"fuente": rel, "sha256": _sha256(ruta), "cita": cita}


def seleccion_actual() -> tuple[list[dict], list[dict], dict]:
    """Selecciona por veredicto; el tamaño nunca forma parte del criterio."""
    filas, contadores = relevo_usos.deriva()
    seleccion = [f for f in filas if f.get("veredicto") == VEREDICTO]
    ids = [f["resultado_id"] for f in seleccion]
    if len(ids) != len(set(ids)):
        raise RuntimeError(f"slots candidatos duplicados: {ids}")
    return filas, seleccion, contadores


def _familia(slot: str) -> tuple[str, str, dict[str, str], list[dict]]:
    consumidor = "milpa/tramite.yaml"
    if slot in {"RES-0025", "RES-0026"}:
        spec = "data/corrida0/CALC-EVASION-NORMA-0001-v1_1/spec.md"
        razones = {
            "unidad": "DELITO en ambos lados; la spec excluye expresamente la unidad persona.",
            "escala": "Proporción ponderada en [0,1] en ambos lados.",
            "direccion": "El RESULT conserva la conducta exacta evade/cumple; más alto significa más peso de esa conducta.",
            "poblacion": "Los mismos 40 280 delitos con BP1_20 en {1,2}, sin pérdida, ponderados por FAC_DEL.",
            "evento": "La pareja enlaza la conducta legacy exacta con el RESULT que la spec declara que releva al slot.",
            "codigos": "Evade usa BP1_20=2 y BP1_23 en {04,05,06,08}; cumple es el complemento binario contado directamente.",
            "periodo": "ENVIPE 2025, con delitos del periodo de referencia 2024 en ambos lados.",
            "transformacion": "Misma proporción FAC_DEL; el complemento se cuenta directamente y agota la partición de dos celdas.",
        }
        cita = "§1: unidad DELITO, universo BP1_20∈{1,2}, FAC_DEL, desenlace y complemento contado directamente para RES-0025/0026."
        estimando = "p ponderada por delito de evade/cumple norma; ENVIPE 2025, n=40 280"
        return "EVASION-NORMA-DIRECTA", estimando, razones, [
            _evidencia(spec, cita),
            _evidencia(consumidor, "regla tramite.evasion_norma, enmienda_envipe2025 y conductas materializadas."),
        ]

    if slot == "RES-0028":
        spec = "data/corrida0/CALC-ENVIPE-0001/spec.md"
        ficha = "forense/notas/2026-09-15-GEN2-E11-RES0028-PARTICION-cierre.md"
        razones = {
            "unidad": "RUPTURA: legacy U4 usa PERSONA; el candidato usa DELITO U1.",
            "escala": "Ambos son proporciones en [0,1].",
            "direccion": "Ambos crecen hacia el bloque residual, aunque no representan el mismo evento agregado.",
            "poblacion": "RUPTURA: legacy es persona con al menos un delito U1 y colapso máximo; candidato es el conjunto de delitos U1.",
            "evento": "RUPTURA: legacy es ninguna razón padre en la persona; candidato es un delito cuya razón principal cae en {03,04,05,07}.",
            "codigos": "DERIVA-DOCUMENTADA: comparten la partición C2 {01,02,06,08}/{03,04,05,07}, pero la agregación cambia el evento.",
            "periodo": "ENVIPE 2025, delitos de referencia 2024 en ambos lados.",
            "transformacion": "RUPTURA: 1-p(C2,U4) tras colapso a persona no equivale a contar el complemento C2 sobre delitos U1.",
        }
        return "ENVIPE-U4-VS-U1-NO-COMPARABLE", "legacy q=1-p(C2,U4) persona vs candidato p(C2 complementario,U1) delito", razones, [
            _evidencia(spec, "Unidad de observación y codificación: U1=delito, U4=persona con colapso máximo; C2 explícita."),
            _evidencia(ficha, "§1-2: partición/universo de RES-0028 y prohibición de rebautizar el residual como categoría 09 Otra."),
            _evidencia(consumidor, "regla civico.denuncia.miedo_desconfianza: complemento dependiente legacy sobre U1/U4."),
        ]

    if slot in {"RES-0031", "RES-0032"}:
        spec = "data/corrida0/CALC-TIENE-AHORROS-0001-v1_1/spec.md"
        razones = {
            "unidad": "PERSONA elegida de 18 años y más en ambos lados.",
            "escala": "Proporción ponderada en [0,1] en ambos lados.",
            "direccion": "La pareja conserva tiene/no tiene ahorros sin invertir la polaridad.",
            "poblacion": "Las mismas 13 502 personas elegidas, EDAD_V 18-98, sin pérdida, FAC_PER.",
            "evento": "Alguna vía informal o formal de ahorro frente a su complemento, exactamente como en la enmienda legacy.",
            "codigos": "Alguna P5_1_1..P5_1_6 o P5_6_1..P5_6_9 vale 1; el blanco de secuencia formal cuenta como no ahorro por esa vía.",
            "periodo": "ENIF 2024 y su periodo de referencia de ahorro en ambos lados.",
            "transformacion": "Misma proporción FAC_PER; no_tiene_ahorros es el complemento contado directamente.",
        }
        estimando = "p ponderada de persona 18+ con/sin ahorro; ENIF 2024, n=13 502"
        return "TIENE-AHORROS-DIRECTA", estimando, razones, [
            _evidencia(spec, "§1: unidad, universo, desenlace, códigos, FAC_PER y complemento para RES-0031/0032."),
            _evidencia(consumidor, "regla dinero.ahorro.tiene_ahorros y enmienda_enif2024 materializada."),
        ]

    if slot in {"RES-0033", "RES-0034"}:
        spec = "data/corrida0/CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1/spec.md"
        fuente = "forense/notas/2026-08-31-reglas-fase1-spec.md"
        razones = {
            "unidad": "PERSONA en ambos lados.",
            "escala": "Proporción ponderada en [0,1] en ambos lados.",
            "direccion": "La pareja conserva recibe/no recibe dinero familiar para la vejez.",
            "poblacion": "Mismo filtro FILTRO_S9_1=2 y EDAD_V<71, 11 895 personas con respuesta válida y FAC_PER.",
            "evento": "P9_9_4=1 (dinero de familiares para cubrir la vejez) frente a su complemento.",
            "codigos": "P9_9_4 en {1,2}; 1 es el evento y 2 su complemento.",
            "periodo": "ENIF 2024 en ambos lados.",
            "transformacion": "Misma proporción FAC_PER; el no-recibe se cuenta directamente como complemento.",
        }
        estimando = "p ponderada de persona que recibe/no recibe dinero familiar para vejez; ENIF 2024, n=11 895"
        return "APOYO-FAMILIAR-DIRECTA", estimando, razones, [
            _evidencia(spec, "§1-2: unidad, universo, punto y complemento de RES-0033/0034."),
            _evidencia(fuente, "§3: P9_9_4, filtro, códigos, ponderador y estimador de la medición legacy."),
            _evidencia(consumidor, "regla familia.apoyo.recibe_dinero_familiares materializada."),
        ]

    if slot in SLOTS_VIAS:
        spec = "data/corrida0/CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1/spec.md"
        razones = {
            "unidad": "PERSONA elegida de 18 años y más en las cuatro celdas.",
            "escala": "Proporción en [0,1] en legacy y RESULT.",
            "direccion": "Cada RESULT conserva la celda exacta: solo informal, ambas, solo formal o no ahorra.",
            "poblacion": "Mismas 13 502 personas de ENIF 2024; las cuatro celdas forman una partición completa.",
            "evento": "La celda legacy y el RESULT usan la misma combinación de pertenencia a ahorro formal F e informal I.",
            "codigos": "F e I vienen de los mismos bloques P5_6_* y P5_1_*; no se supone independencia.",
            "periodo": "ENIF 2024 y el mismo periodo de referencia de ahorro.",
            "transformacion": "Misma inclusión-exclusión: ambas=F+I-(F∪I), exclusivas por resta y no_ahorra=1-(F∪I).",
        }
        estimando = "partición F/I de ahorro (solo informal, ambas, solo formal, ninguno); ENIF 2024, n=13 502"
        return "VIAS-AHORRO-PARTICION", estimando, razones, [
            _evidencia(spec, "§2: fórmulas de inclusión-exclusión, dependencia de insumos sellados y suma exacta de las cuatro celdas."),
            _evidencia(consumidor, "regla dinero.ahorro.via_informal, nota_l1 y cuatro conductas derivadas sin IC propio."),
        ]

    if slot == "RES-0066":
        spec = "data/corrida0/CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1/spec.md"
        razones = {
            "unidad": "PERSONA no trabajadora elegida de 18 años y más en ambos lados.",
            "escala": "Proporción en [0,1] en ambos lados.",
            "direccion": "Más alto significa mayor proporción con horizonte no corto en el mismo dominio.",
            "poblacion": "Mismas 3 462 personas que no trabajaron el mes anterior y tienen P4_10 válido.",
            "evento": "El evento exacto es el complemento de horizonte_corto dentro del dominio no trabajador.",
            "codigos": "Actividad por P3_8/P3_9 y horizonte corto por P4_10∈{1,2}; el RESULT conserva esos códigos por dependencia explícita.",
            "periodo": "ENIF 2024 en ambos lados.",
            "transformacion": "Mismo 1 - RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P; no se trata como medición independiente.",
        }
        estimando = "1-p(horizonte corto) entre no trabajadores; ENIF 2024, n=3 462"
        return "HORIZONTE-DERIVADO-DEPENDIENTE", estimando, razones, [
            _evidencia(spec, "§2: RES-0066=1-RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P y dependencia explícita."),
            _evidencia(consumidor, "regla dinero.ahorro.horizonte_no_trabajadores, IC95 propio del complemento y derivado_de."),
        ]

    raise RuntimeError(f"slot candidato sin correspondencia propia: {slot}")


def construye_contrato(seleccion: list[dict]) -> tuple[dict, dict[str, str]]:
    doc, saltados = relevo_usos.contrato(seleccion)
    if saltados:
        raise RuntimeError("pares omitidos por generador base: " + " | ".join(saltados))
    por_slot = {f["resultado_id"]: f for f in seleccion}
    familias = {}
    vistos = set()
    for par in doc["pares"]:
        marca = RE_SLOT.search(par["id"])
        if not marca:
            raise RuntimeError(f"id de par no identifica slot: {par['id']}")
        slot = marca.group(1)
        fila = por_slot[slot]
        nombre, estimando, razones, evidencias = _familia(slot)
        familias[slot] = nombre
        vistos.add(slot)
        estados = {}
        for dimension in DIMENSIONES:
            estado = "COINCIDE"
            if slot == "RES-0028":
                if dimension in {"unidad", "poblacion", "evento", "transformacion"}:
                    estado = "RUPTURA"
                elif dimension == "codigos":
                    estado = "DERIVA-DOCUMENTADA"
            estados[dimension] = {
                "estado": estado,
                "razon": f"{nombre} · {razones[dimension]}",
            }
        par["comparabilidad"] = {"dimensiones": estados, "evidencias": evidencias}
        par["uso"] = {
            "descripcion": (
                f"{slot}: {estimando}. Consumidor {fila['consumidor']}; "
                f"legacy en el archivo del consumidor frente a "
                f"{fila['calc_candidato']}::{fila['result_gen2_candidato']}. "
                "Esta comparación no adopta ni edita el consumidor."
            ),
            "evidencias": evidencias,
        }
    faltan = set(por_slot) - vistos
    extras = vistos - set(por_slot)
    if faltan or extras:
        raise RuntimeError(f"cobertura del contrato: faltan={sorted(faltan)} extras={sorted(extras)}")
    doc["descripcion"] = (
        "GEN2-RELEVO-CANDIDATOS-DELTA-1. Contrato filtrado por veredicto "
        "CANDIDATO-GEN2 vigente. Las correspondencias propias completan las "
        "familias que el generador compartido deja prudentemente indeterminadas; "
        "RES-0028 conserva la ruptura U4-persona/U1-delito. Cero adopciones."
    )
    return doc, familias


def _escribe_tsv(ruta: Path, filas: list[dict], columnas: list[str], comentarios=()) -> None:
    buf = io.StringIO()
    for comentario in comentarios:
        buf.write(f"# {comentario}\n")
    w = csv.DictWriter(buf, fieldnames=columnas, delimiter="\t", lineterminator="\n",
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(filas)
    ruta.write_text(buf.getvalue(), encoding="utf-8")


def _head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=RAIZ, text=True).strip()


def _ic_res_0066() -> tuple[float, float]:
    crudo = relevo_usos.corrida0._yaml_safe_load(
        (RAIZ / "milpa/tramite.yaml").read_text(encoding="utf-8"))
    reglas = [r for r in crudo.get("reglas", [])
              if r.get("id") == "dinero.ahorro.horizonte_no_trabajadores"]
    if len(reglas) != 1:
        raise RuntimeError("no se resolvió una regla única para RES-0066")
    ic = reglas[0].get("ic95_horizonte_no_corto")
    if not isinstance(ic, list) or len(ic) != 2:
        raise RuntimeError("RES-0066 no declara IC95 propio del complemento")
    return float(ic[0]), float(ic[1])


def _dependencias_marcador(slot: str) -> list[str]:
    ruta = RAIZ / "data/corrida0/demanda-resultados.tsv"
    with ruta.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(
            (linea for linea in fh if not linea.startswith("#")),
            delimiter="\t"))
    tipos = {"celda_M", "celda_R", "celda_L", "celda_AGREGADO"}
    return [
        f"{f['resultado_id']}:{f['tipo']}"
        for f in filas
        if f.get("tipo") in tipos
        and slot in (f.get("depende_de") or "").split(";")
    ]


def genera(destino: Path) -> tuple[list[dict], dict[str, str]]:
    destino = destino.resolve()
    destino.relative_to(RAIZ.resolve())
    destino.mkdir(parents=True, exist_ok=True)
    universo, seleccion, contadores = seleccion_actual()
    contrato, familias = construye_contrato(seleccion)

    (destino / "relevo-usos-lectura.json").write_text(
        json.dumps(universo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (destino / "seleccion-candidatos.json").write_text(
        json.dumps(seleccion, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _escribe_tsv(
        destino / "seleccion-candidatos.tsv", seleccion,
        relevo_usos.COLUMNAS[:relevo_usos.COLUMNAS.index("razon") + 1],
        ("DERIVADO POR LECTURA; NO ES REGISTRO CANÓNICO; NO ADOPTA.",
         f"criterio: veredicto={VEREDICTO}; HEAD={_head()}"),
    )
    (destino / "contrato-gen2-delta-1.yaml").write_text(
        yaml.safe_dump(contrato, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=100), encoding="utf-8")
    meta = {
        "head": _head(),
        "criterio_seleccion": f"veredicto == {VEREDICTO}",
        "slots_total": len(universo),
        "contadores": contadores,
        "seleccion_ids": [f["resultado_id"] for f in seleccion],
        "familias": familias,
        "sha256_relevo_usos_lectura": _sha256(destino / "relevo-usos-lectura.json"),
        "comando_derivacion": "python3 tools/relevo_usos.py --json (misma función deriva(), sin --escribe)",
        "cero_adopciones": True,
    }
    (destino / "seleccion-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return seleccion, familias


def clasifica(fila: dict, par: dict) -> tuple[str, str, str]:
    """Aplica el bin firmado; no reutiliza la materialidad numérica del CLI."""
    comp = par.get("comparabilidad") or {}
    delta = (par.get("diferencia") or {}).get("delta")
    deps_marcador = _dependencias_marcador(fila["resultado_id"])
    if comp.get("estado") != "DEMOSTRADA" or delta is None:
        reserva = (f" Aunque alimenta {', '.join(deps_marcador)}, sin delta "
                   "comparable no puede pasar a bin 2."
                   if deps_marcador else "")
        return (
            "3",
            "NO-COMPARABLE; no hay delta sustantivo autorizable." + reserva,
            "Resolver la ruptura de estimando/universo y emitir un RESULT sucesor compatible antes de volver a comparar.",
        )
    if fila.get("tipo_uso") == "conducta_p_medido":
        sufijo = (f" Además alimenta {', '.join(deps_marcador)}."
                  if deps_marcador else "")
        return (
            "2",
            "Regla con p medida: firma individual obligatoria aunque el delta sea cero o redondee al mismo punto."
            + sufijo,
            "Mesa decide individualmente si cambia la autoridad numérica del consumidor al RESULT GEN2.",
        )
    slot = fila["resultado_id"]
    if deps_marcador:
        return (
            "2",
            "Insumo directo del marcador/agregado "
            f"({', '.join(deps_marcador)}): firma individual obligatoria aunque el delta sea cero.",
            "Mesa decide individualmente el cambio de autoridad y preserva la dependencia explícita del agregado.",
        )
    if slot in SLOTS_VIAS:
        return (
            "3",
            "Sin se_mueve_si ni IC legacy propio; la cercanía numérica no crea criterio.",
            "Mesa decide este renglón dentro del bloque bin 3 y conserva la identidad de la partición completa.",
        )
    if slot == "RES-0066":
        b = (par.get("referencias") or {}).get("b", {}).get("valor")
        a = (par.get("referencias") or {}).get("a", {}).get("valor")
        mismo_signo = a is not None and b is not None and (a > 0) == (b > 0)
        ic_lo, ic_hi = _ic_res_0066()
        dentro_ic = b is not None and ic_lo <= b <= ic_hi
        if mismo_signo and dentro_ic:
            return (
                "1",
                "Mismo signo; punto GEN2 dentro del IC95 legacy del complemento; no es p medida, coeficiente ni marcador.",
                "Puede incluirse en un merge posterior de adopción en bloque, con cita y registro canónico.",
            )
        return (
            "2",
            "El punto no satisface signo/IC legacy y requiere decisión individual.",
            "Mesa decide individualmente.",
        )
    return (
        "3",
        "No se localizó criterio de autorización acreditado.",
        "Mesa define se_mueve_si o un criterio legacy antes de adoptar.",
    )


def _slot_del_par(par: dict) -> str:
    marca = RE_SLOT.search(par.get("id", ""))
    if not marca:
        raise RuntimeError(f"par sin slot: {par.get('id')}")
    return marca.group(1)


def _delta_texto(par: dict) -> str:
    delta = (par.get("diferencia") or {}).get("delta")
    if delta is None:
        dims = (par.get("comparabilidad") or {}).get("dimensiones") or {}
        malas = [d for d, v in dims.items() if v.get("estado") in {"RUPTURA", "INCOMPATIBLE"}]
        return "NO-COMPARABLE:" + ",".join(malas)
    return repr(delta)


def escribe_decisiones(destino: Path, seleccion: list[dict], familias: dict[str, str],
                       delta_json: Path) -> list[dict]:
    informe = json.loads(delta_json.read_text(encoding="utf-8"))
    pares = {_slot_del_par(p): p for p in informe.get("pares") or []}
    filas_sel = {f["resultado_id"]: f for f in seleccion}
    if set(pares) != set(filas_sel):
        raise RuntimeError(
            f"delta no cubre selección: faltan={sorted(set(filas_sel)-set(pares))} "
            f"extras={sorted(set(pares)-set(filas_sel))}")

    tabla = []
    for slot in filas_sel:
        fila, par = filas_sel[slot], pares[slot]
        bin_, decision, siguiente = clasifica(fila, par)
        _nombre, estimando, _razones, _evidencias = _familia(slot)
        tabla.append({
            "slot": slot,
            "consumidor": fila["consumidor"],
            "estimando_universo": estimando,
            "referencia_legacy": (
                f"milpa/tramite.yaml::{fila['valor_legacy']} "
                f"({fila['tipo_uso']}; {fila['generacion_hoy']})"),
            "calc_result": f"{fila['calc_candidato']}::{fila['result_gen2_candidato']}",
            "sello_generacion": f"{fila['sello_calc']}; cuenta_gen2=SI; familia={familias[slot]}",
            "delta_admisible": _delta_texto(par),
            "bin": bin_,
            "decision": decision,
            "siguiente_accion": siguiente,
        })

    columnas = list(tabla[0]) if tabla else []
    _escribe_tsv(
        destino / "tabla-decision.tsv", tabla, columnas,
        ("PROPUESTA; NO FIRMA, NO ADOPTA, NO EDITA CONSUMIDORES.",
         "bin conforme a la regla firmada; no conforme a tolerancia del comparador."),
    )
    conteos = {b: sum(1 for f in tabla if f["bin"] == b) for b in ("1", "2", "3")}
    por_bin = {b: [f for f in tabla if f["bin"] == b] for b in ("1", "2", "3")}
    valores_vias_gen2 = [
        pares[s]["referencias"]["b"]["valor"] for s in sorted(SLOTS_VIAS)]
    valores_vias_legacy = [
        pares[s]["referencias"]["a"]["valor"] for s in sorted(SLOTS_VIAS)]
    suma_vias_gen2 = sum(valores_vias_gen2)
    suma_vias_legacy = sum(valores_vias_legacy)
    if abs(suma_vias_gen2 - 1.0) > 1e-12 or abs(suma_vias_legacy - 1.0) > 1e-12:
        raise RuntimeError(
            "la partición de vías no suma 1: "
            f"legacy={suma_vias_legacy!r}, gen2={suma_vias_gen2!r}")

    lineas = [
        "# Decisiones propuestas · GEN2-RELEVO-CANDIDATOS-DELTA-1",
        "",
        "Estado: **PROPUESTA PARA MESA; NO FIRMADA; CERO ADOPCIONES**. Este acto no edita consumidores ni vistas canónicas.",
        "",
        "Regla aplicada: `forense/encargos/2026-09-15-GEN2-RELEVO-USOS-1-ADENDA-REGLA-ADOPCION-EN-BLOQUE.md`, líneas de la pieza firmada 53-65. El estado de materialidad que imprime `corrida0 delta` es descriptivo; no sustituye el bin de autorización.",
        "",
        f"Corte efectivo: `{_head()}` · {len(tabla)} slots seleccionados por `veredicto=CANDIDATO-GEN2` · bin 1={conteos['1']}, bin 2={conteos['2']}, bin 3={conteos['3']}.",
        "",
        "## Tabla completa",
        "",
        "| slot | consumidor | estimando / universo | legacy | CALC / RESULT | sello / generación | delta admisible | bin | decisión | siguiente acción |",
        "|---|---|---|---|---|---|---:|:---:|---|---|",
    ]
    for f in tabla:
        vals = [f["slot"], f["consumidor"], f["estimando_universo"],
                f["referencia_legacy"], f["calc_result"], f["sello_generacion"],
                f["delta_admisible"], f["bin"], f["decision"], f["siguiente_accion"]]
        lineas.append("| " + " | ".join(str(v).replace("|", "\\|") for v in vals) + " |")

    lineas += ["", "## Bin 1 · podría entrar por merge posterior", ""]
    for f in por_bin["1"]:
        lineas.append(f"- `{f['slot']}` — {f['decision']} Delta B−A: `{f['delta_admisible']}`.")
    if not por_bin["1"]:
        lineas.append("Ninguno.")

    lineas += ["", "## Bin 2 · decisión individual", ""]
    for f in por_bin["2"]:
        lineas.append(f"- `{f['slot']}` — delta B−A `{f['delta_admisible']}`. {f['decision']}")
    if not por_bin["2"]:
        lineas.append("Ninguno.")

    lineas += ["", "## Bin 3 · decisión en bloque o estimando sucesor", ""]
    for f in por_bin["3"]:
        lineas.append(f"- `{f['slot']}` — `{f['delta_admisible']}`. {f['decision']} {f['siguiente_accion']}")
    if not por_bin["3"]:
        lineas.append("Ninguno.")

    lineas += [
        "",
        "### Control de partición y dependencias de vías de ahorro",
        "",
        f"Los cuatro RESULT publicados de `RES-0053..0056` conservan la dependencia explícita de `F`, `I` y `F∪I`; suma legacy=`{suma_vias_legacy!r}` y suma GEN2=`{suma_vias_gen2!r}`. No son cuatro mediciones independientes. La regla de autorización separa `RES-0053/0054/0056` a bin 2 porque alimentan agregados y deja `RES-0055` en bin 3 por falta de criterio; ninguna celda se adopta en este acto.",
        "",
        "## Texto de resolución propuesto para mesa — no firmado",
        "",
        "> Se acusa recibo de las doce comparaciones de GEN2-RELEVO-CANDIDATOS-DELTA-1. RES-0025, RES-0026, RES-0031, RES-0032, RES-0033 y RES-0034 quedan para decisión individual de bin 2 porque son reglas con p medida. RES-0053, RES-0054, RES-0056 y RES-0066 también quedan en bin 2 porque alimentan celdas M/AGREGADO: la cercanía decimal y, para RES-0066, el cumplimiento de signo e IC, no sustituyen la firma sobre el cambio de autoridad numérica. RES-0055 queda en bin 3 por carecer de se_mueve_si e IC legacy propio; su decisión debe conservar la identidad de la partición completa de vías de ahorro. RES-0028 se rechaza como pareja de relevo actual por ruptura U4-persona/U1-delito; no se interpreta delta y se exige un RESULT sucesor compatible. Todos los relevos requieren decisión de mesa; esta propuesta no promete reducción del contador y este PR no adopta ninguno.",
        "",
        "La eventual aprobación de ese texto no está contenida en este archivo: requiere acto/merge posterior con la autoridad de mesa y las escrituras canónicas correspondientes.",
        "",
    ]
    (destino / "decisiones-propuestas.md").write_text("\n".join(lineas), encoding="utf-8")
    return tabla


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--destino", required=True, type=Path,
                   help="directorio explícito dentro del repositorio")
    p.add_argument("--delta-json", type=Path,
                   help="delta.json ya producido por `corrida0 delta`")
    args = p.parse_args(argv)
    seleccion, familias = genera(args.destino)
    print(f"seleccion={len(seleccion)}")
    print("ids=" + ",".join(f["resultado_id"] for f in seleccion))
    print(f"contrato={args.destino / 'contrato-gen2-delta-1.yaml'}")
    if args.delta_json:
        tabla = escribe_decisiones(args.destino.resolve(), seleccion, familias,
                                   args.delta_json.resolve())
        print("bins=" + ",".join(
            f"{b}:{sum(1 for f in tabla if f['bin'] == b)}" for b in ("1", "2", "3")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
