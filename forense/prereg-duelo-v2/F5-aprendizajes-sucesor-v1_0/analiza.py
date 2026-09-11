#!/usr/bin/env python3
"""Descompone F5 completa sin modificar ni recalcular salidas selladas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "forense/prereg-duelo-v2"
OUT = Path(__file__).resolve().parent
RESULTADO = BASE / "F5-completa-resultado-v1_0.json"
EXTRACCION = BASE / "F5-completa-extraccion-v1_0.tsv"
L_SPEC = BASE / "L-spec-v1_4.json"
SNAPSHOT = BASE / "snapshot-M-triada-v1_0.json"
MANIFIESTO = BASE / "paquete-corpus-F5-v2_0/manifiesto-F5-v2_0.json"
SELLADO = ROOT / "data/corrida0/CALC-TRIADA-0002/resultados.json"

BRAZOS = ("L_SOLO", "L_CORPUS", "M")
COLORES = {"L_SOLO": "#4c78a8", "L_CORPUS": "#f58518", "M": "#54a24b"}


def cargar_json(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8"))


def escribir_tsv(ruta: Path, filas: list[dict], campos: list[str]) -> None:
    with ruta.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def familia(celda: str) -> str:
    if celda.startswith("CIV-"):
        return "CIV-ENVIPE"
    if celda == "DIN-M-01":
        return "DIN-ENNViH"
    if celda == "FAM-M-01":
        return "FAM-ENIF-APOYO"
    if celda in {"FAM-M-05", "FAM-M-06", "FAM-M-07"}:
        return "FAM-ENIGH-REMESAS"
    if celda == "TRA-M-02":
        return "TRA-ENCUCI"
    return "TRA-ENCIG"


def cuantil_lineal(valores: list[float], q: float) -> float | None:
    if not valores:
        return None
    xs = sorted(valores)
    pos = (len(xs) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - pos) + xs[hi] * (pos - lo)


def fmt(x: float | None, n: int = 6) -> str:
    return "" if x is None else f"{x:.{n}f}"


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def figura_svg(filas: list[dict], ruta: Path) -> None:
    filas = [f for f in filas if f["en_u3"] == "SI"]
    ancho, alto = 980, 90 + 31 * len(filas)
    x0, plot_w = 145, 760
    maximo = max(float(f[f"contrib_mae_{b.lower()}_pp"]) for f in filas for b in BRAZOS)
    escala = plot_w / maximo
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:system-ui,sans-serif;fill:#222}.t{font-size:16px;font-weight:600}.l{font-size:11px}.a{font-size:10px;fill:#555}</style>',
        '<text x="20" y="25" class="t">Contribución de cada celda al MAE de U3 (pp)</text>',
    ]
    for i, brazo in enumerate(BRAZOS):
        x = 430 + i * 130
        partes += [f'<rect x="{x}" y="42" width="13" height="9" fill="{COLORES[brazo]}"/>',
                   f'<text x="{x + 18}" y="51" class="a">{brazo}</text>']
    for i, fila in enumerate(filas):
        y = 70 + i * 31
        partes.append(f'<text x="20" y="{y + 15}" class="l">{fila["id_celda"]}</text>')
        for j, brazo in enumerate(BRAZOS):
            valor = float(fila[f"contrib_mae_{brazo.lower()}_pp"])
            yy = y + j * 7
            partes.append(f'<rect x="{x0}" y="{yy}" width="{valor * escala:.2f}" height="5" rx="1" fill="{COLORES[brazo]}"/>')
            if valor >= 0.08:
                partes.append(f'<text x="{x0 + valor * escala + 4:.2f}" y="{yy + 5}" class="a">{valor:.3f}</text>')
    partes.append('</svg>')
    ruta.write_text("\n".join(partes) + "\n", encoding="utf-8")


def main() -> None:
    resultado = cargar_json(RESULTADO)
    sellado = cargar_json(SELLADO)["resultados"]
    spec = {x["id"]: x for x in cargar_json(L_SPEC)["celdas"]}
    snapshot = {x["id_celda"]: x for x in cargar_json(SNAPSHOT)["celdas"]}
    manifiesto = cargar_json(MANIFIESTO)["celdas"]
    u3 = set(resultado["u3_ids"])
    n_u3 = len(u3)

    capturas: dict[tuple[str, str], list[dict]] = defaultdict(list)
    with EXTRACCION.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f, delimiter="\t"):
            capturas[(fila["id_celda"], fila["variante"])].append(fila)

    filas = []
    for celda, datos in resultado["celdas"].items():
        r_meta = cargar_json(BASE / "corridas-R" / f"{celda}.json")
        puntos = {
            "L_SOLO": datos["brazos"]["L_SOLO"]["punto_mediana"],
            "L_CORPUS": datos["brazos"]["L_CORPUS"]["punto_mediana"],
            "M": datos["M"],
        }
        fila = {
            "id_celda": celda,
            "familia_mecanismo": familia(celda),
            "encuesta": spec[celda]["encuesta"],
            "ola_R": spec[celda]["ola"],
            "en_u3": "SI" if celda in u3 else "NO",
            "R_pct": fmt(datos["R"] * 100),
            "R_EE_pp": fmt(r_meta.get("EE_R", 0) * 100),
        }
        for brazo, variante in (("L_SOLO", "L-solo"), ("L_CORPUS", "L+corpus")):
            resumen = datos["brazos"][brazo]
            validos = [float(x["valor"]) * 100 for x in capturas[(celda, variante)] if x["estado"] == "VALIDA"]
            fila.update({
                f"{brazo.lower()}_mediana_pct": fmt(None if puntos[brazo] is None else puntos[brazo] * 100),
                f"{brazo.lower()}_validas": resumen["validas"],
                f"{brazo.lower()}_abstenciones": resumen["abstenciones"],
                f"{brazo.lower()}_iqr_pp": fmt(None if not validos else cuantil_lineal(validos, .75) - cuantil_lineal(validos, .25)),
            })
        fila["m_pct"] = fmt(datos["M"] * 100)
        for brazo in BRAZOS:
            punto = puntos[brazo]
            error = None if punto is None else abs(punto - datos["R"]) * 100
            contrib = error / n_u3 if error is not None and celda in u3 else None
            fila[f"error_abs_{brazo.lower()}_pp"] = fmt(error)
            fila[f"contrib_mae_{brazo.lower()}_pp"] = fmt(contrib)
        filas.append(fila)

    # Una columna siempre poblada al final evita tabs terminales en filas con
    # punto ausente, sin representar los faltantes como cero.
    campos = [c for c in filas[0] if c != "en_u3"] + ["en_u3"]
    escribir_tsv(OUT / "celdas.tsv", filas, campos)

    familias = []
    for nombre in sorted({f["familia_mecanismo"] for f in filas}):
        grupo = [f for f in filas if f["familia_mecanismo"] == nombre]
        gu3 = [f for f in grupo if f["en_u3"] == "SI"]
        fila = {"familia_mecanismo": nombre, "n_celdas": len(grupo), "n_u3": len(gu3)}
        for brazo in BRAZOS:
            fila[f"contrib_mae_{brazo.lower()}_pp"] = fmt(sum(float(f[f"contrib_mae_{brazo.lower()}_pp"]) for f in gu3))
        familias.append(fila)
    escribir_tsv(OUT / "familias.tsv", familias, list(familias[0]))

    abstenciones = []
    for celda in ("DIN-M-01", "TRA-M-07"):
        paquete = manifiesto[celda]
        patrones = sorted((BASE / "corridas-L-completa-v1_0").glob(f"L-{celda}-M__L+corpus__*.json"))
        assert len(patrones) == 8
        for ruta in patrones:
            captura = cargar_json(ruta)
            texto = captura["texto_crudo"]
            assert texto.rstrip().endswith("ABSTENCION")
            abstenciones.append({
                "id_celda": celda,
                "replica": captura["replica"],
                "sha256_paquete_captura": captura["sha256_paquete"],
                "sha256_contenido_manifiesto": paquete["sha256_contenido_entregado"],
                "evidencia_directa_evento": paquete["evidencia_directa_evento"],
                "clasificacion": "FALTA-DOCUMENTO-ESPECIFICO-Y-EVIDENCIA-CUANTITATIVA",
                "definicion_en_prompt": "PRESENTE",
                "decision_del_brazo": "ABSTENCION-VALIDA-ANTE-CONTEXTO-NO-PERTINENTE",
                "justificacion": " ".join(texto.splitlines()[:-1]).strip(),
            })
    escribir_tsv(OUT / "abstenciones.tsv", abstenciones, list(abstenciones[0]))

    traza = [
        {"celdas": "CIV-M-01/02/04/10/12/13", "regla_M": "civico.denuncia.miedo_desconfianza", "fuente_ola_M": "ENVIPE 2025", "poblacion_evento_transformacion_M": "persona 18+ víctima; algún delito no denunciado en U1 con BP1_23∈{01,02,06,08}; tasa ponderada FAC_ELE, colapso a persona", "contraste_R": "ENVIPE 2012/13/15/21/23/24; unidad delito; BP1_23∈{01,02,06} sobre razones válidas que incluyen 08/09 en el cero", "diagnostico": "NO-ALINEADO: unidad, recorte, códigos y ola; #689 explicitó el contrato, no volvió comparables los estimandos"},
        {"celdas": "DIN-M-01", "regla_M": "dinero.ahorro.tiene_ahorros", "fuente_ola_M": "ENNViH ola 2, 2005-06", "poblacion_evento_transformacion_M": "panel retenido con pr02/cr27 válidos en olas 2-3; cr27 Sí; tasa ponderada fac_3b", "contraste_R": "ENNViH ola 1, 2002; libro 3B sección CR; cr27 Sí entre respuestas válidas", "diagnostico": "TRANSFERENCIA temporal/poblacional; fuera de U3 por abstención L_CORPUS"},
        {"celdas": "FAM-M-01", "regla_M": "familia.apoyo.recibe_dinero_familiares", "fuente_ola_M": "ENIF 2024", "poblacion_evento_transformacion_M": "FILTRO_S9_1=2 y EDAD_V<71; P9_9_4=Sí; tasa ponderada FAC_PER", "contraste_R": "ENIF 2018; personas seleccionadas de tmodulo2 sección 9.9 con p9_9_4 válido", "diagnostico": "MISMO ítem general, pero transferencia de ola y elegibilidad no armonizada; medir/registrar serie comparable"},
        {"celdas": "FAM-M-05/06/07", "regla_M": "familia.seguro.volatilidad_ausencia_estado", "fuente_ola_M": "ENIGH 2022", "poblacion_evento_transformacion_M": "hogares completos; remesas>0; tasa ponderada factor", "contraste_R": "ENIGH 2016/18/20 con el mismo evento y universo", "diagnostico": "ALINEADO salvo ola: repetición legítima del punto vigente; serie_olas ya contiene los puntos históricos y aporta poco error"},
        {"celdas": "TRA-M-02", "regla_M": "tramite.mordida.discrecional", "fuente_ola_M": "ENCIG 2025", "poblacion_evento_transformacion_M": "personas 18+ con P8_3_1 válido; solicitud directa; tasa FAC_P18", "contraste_R": "ENCUCI 2020; personas 15+ con contacto; unión AP5_17 solicitud ∪ AP5_18 entrega", "diagnostico": "USO NO ALINEADO del snapshot; #689 ya implementó transición ENCUCI unión=0.126006 y dominio correcto"},
        {"celdas": "TRA-M-03/07", "regla_M": "tramite.mordida.discrecional", "fuente_ola_M": "ENCIG 2025", "poblacion_evento_transformacion_M": "personas 18+; P8_3_1=Sí; tasa FAC_P18", "contraste_R": "ENCIG 2013 P8_3 y 2021 P8_3_1, respuesta válida", "diagnostico": "ALINEADO por evento general, no por ola; serie_olas vigente permite selección temporal"},
    ]
    escribir_tsv(OUT / "traza-motor.tsv", traza, list(traza[0]))

    # Reanálisis exploratorio sobre el panel conocido: no es nueva medición.
    # Sustituye sólo usos ya disponibles y alineados en el contrato vivo.
    usos_actuales = {
        "FAM-M-05": 0.047459,
        "FAM-M-06": 0.047285,
        "FAM-M-07": 0.043775,
        "TRA-M-02": 0.126006,
        "TRA-M-03": 0.044538,
    }
    mae_sens = statistics.mean(abs(usos_actuales.get(c, resultado["celdas"][c]["M"]) - resultado["celdas"][c]["R"]) for c in resultado["u3_ids"]) * 100

    reconciliacion = {}
    for brazo in BRAZOS:
        calculado = statistics.mean(
            abs(
                (resultado["celdas"][c]["M"] if brazo == "M" else resultado["celdas"][c]["brazos"][brazo]["punto_mediana"])
                - resultado["celdas"][c]["R"]
            )
            for c in resultado["u3_ids"]
        ) * 100
        esperado = resultado["mae_pp"][brazo]
        assert abs(calculado - esperado) < 1e-12
        reconciliacion[brazo] = {"mae_pp_resultado": esperado, "mae_pp_recalculado": calculado, "delta_pp": calculado - esperado}
    assert sellado["RESULT-F5C-U3-N"] == n_u3
    assert sellado["RESULT-F5C-VEREDICTO-GLOBAL"] == resultado["veredicto_global"]
    salida = {
        "acto": "GEN2-F5-APRENDIZAJES-Y-SUCESOR",
        "tipo": "DIAGNOSTICO-EXPLORATORIO-SOBRE-PANEL-CONOCIDO",
        "insumos_sha256": {p.relative_to(ROOT).as_posix(): sha256(p) for p in (RESULTADO, EXTRACCION, L_SPEC, SNAPSHOT, MANIFIESTO, SELLADO)},
        "u3_ids": resultado["u3_ids"],
        "reconciliacion": reconciliacion,
        "sensibilidad_no_confirmatoria": {
            "descripcion": "selección por ola en series ENIGH/ENCIG alineadas y unión ENCUCI ya corregida por #689; conserva las demás celdas del snapshot",
            "mae_M_original_pp": resultado["mae_pp"]["M"],
            "mae_M_reanalisis_pp": mae_sens,
            "reduccion_pp": resultado["mae_pp"]["M"] - mae_sens,
            "advertencia": "usa el panel R ya conocido y no prueba mejora fuera de muestra",
        },
        "controles": {"filas_celdas": len(filas), "filas_abstenciones": len(abstenciones), "veredicto_preservado": resultado["veredicto_global"]},
    }
    (OUT / "F5-aprendizajes-sucesor-resultados-v1_0.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    figura_svg(filas, OUT / "figura-contribucion-mae.svg")
    print(f"OK: {len(filas)} celdas; U3={n_u3}; 16 abstenciones; MAE reconciliados")


if __name__ == "__main__":
    main()
