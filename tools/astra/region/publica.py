"""Deriva el eje regional de CALC sellados; ninguna cifra se teclea."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
CALCS = {
    "ENVIPE": ("2024", "evade_norma_envipe2025", "ENTIDAD", "delito",
               "delitos con BP1_20 válido", "CALC-REGION-ENVIPE-2024-0001"),
    "ENCIG": ("2023", "canal_digital_luz", "ENTIDAD", "trámite",
              "trámites ordinarios de luz con canal válido; marco urbano 100 mil+",
              "CALC-REGION-ENCIG-2023-0001"),
    "ENIF": ("2024", "tiene_ahorros_enif2024", "REGION", "persona",
             "personas elegidas 18+ con batería de ahorro válida",
             "CALC-REGION-ENIF-2024-0001"),
}
HISTORIA = {
    "ENVIPE": ([2023, 2025], "evade_norma_envipe2025", "ENTIDAD", "delito",
               "delitos con BP1_20 válido"),
    "ENCIG": ([2017, 2019, 2021], "canal_digital_luz", "ENTIDAD", "trámite",
              "trámites ordinarios de luz con canal válido; marco urbano 100 mil+"),
    "ENIF": ([2018, 2021, 2024], "informal_cualquiera_18a70", "REGION", "persona",
             "personas elegidas 18–70 con batería P5_1 válida"),
}
CAMPOS = ("instrumento", "conducta", "nivel_geografico", "geografia_codigo",
          "ola", "naturaleza_estimacion", "punto", "ic95_inf", "ic95_sup",
          "unidad", "escala", "universo", "n", "n_efectivo_kish", "calidad",
          "generacion", "temporalidad", "estado_publicacion", "result_punto",
          "result_inf", "result_sup", "calc", "sha256_resultados", "sha256_sello")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def genera():
    filas = []
    fuentes = [(instrumento, ola, conducta, nivel, unidad, universo, calc, False)
               for instrumento, (ola, conducta, nivel, unidad, universo, calc) in CALCS.items()]
    for instrumento, (olas, conducta, nivel, unidad, universo) in HISTORIA.items():
        for ola in olas:
            fuentes.append((instrumento, str(ola), conducta, nivel, unidad, universo,
                            f"CALC-REGION-HIST-{instrumento}-{ola}-0001", True))
    for instrumento, ola, conducta, nivel, unidad, universo, calc, historico in fuentes:
        carpeta = ROOT / "data/corrida0" / calc
        resultados_path = carpeta / "resultados.json"
        datos = json.loads(resultados_path.read_text(encoding="utf-8"))["resultados"]
        pref = f"RESULT-REGION-{'HIST-' if historico else ''}{instrumento}-{ola}"
        bruto = json.loads(datos[pref + "-JSON"])
        for fila in bruto["filas"]:
            base = pref + "-" + fila["geografia"]
            ids = [base + suf for suf in ("-P", "-IC-LO", "-IC-HI")]
            punto, lo, hi = (datos[i] for i in ids)
            if fila["estado"] == "PUBLICABLE" and not (0 <= lo <= punto <= hi <= 1):
                raise ValueError(f"IC o punto incoherente: {base}")
            if fila["estado"] != "PUBLICABLE" and any(v is not None for v in (punto, lo, hi)):
                raise ValueError(f"fila suprimida con cifra: {base}")
            filas.append(dict(zip(CAMPOS, (
                instrumento, conducta, nivel, fila["geografia"], ola, "IC-DE-DISEÑO",
                punto, lo, hi, unidad, "proporción [0,1]", universo,
                datos[base + "-N"], datos[base + "-N-EFECTIVO-KISH"],
                "n≥200 y varianza bootstrap estimable" if fila["estado"] == "PUBLICABLE" else fila["estado"],
                "GEN2", "RETROSPECTIVA", fila["estado"], *ids, calc,
                sha(resultados_path), sha(carpeta / "sello.json"),
            ))))
    calc = "CALC-REGION-ENIF-PORTAFOLIO-2024-0001"
    carpeta = ROOT / "data/corrida0" / calc
    resultados_path = carpeta / "resultados.json"
    datos = json.loads(resultados_path.read_text(encoding="utf-8"))["resultados"]
    from tools.astra.region.enif_portafolio import CONDUCTAS
    for conducta in CONDUCTAS:
        pref = f"RESULT-REGION-ENIF-PORT-2024-{conducta}"
        bruto = json.loads(datos[pref + "-JSON"])
        for fila in bruto["filas"]:
            base = pref + "-" + fila["geografia"]
            ids = [base + suf for suf in ("-P", "-IC-LO", "-IC-HI")]
            punto, lo, hi = (datos[i] for i in ids)
            if fila["estado"] == "PUBLICABLE" and not (0 <= lo <= punto <= hi <= 1):
                raise ValueError(f"IC o punto incoherente: {base}")
            if fila["estado"] != "PUBLICABLE" and any(v is not None for v in (punto, lo, hi)):
                raise ValueError(f"fila suprimida con cifra: {base}")
            filas.append(dict(zip(CAMPOS, (
                "ENIF", conducta, "REGION", fila["geografia"], "2024", "IC-DE-DISEÑO",
                punto, lo, hi, "persona", "proporción [0,1]",
                "personas elegidas 18+ con batería de ahorro válida",
                datos[base + "-N"], datos[base + "-N-EFECTIVO-KISH"],
                "n≥200 y varianza bootstrap estimable" if fila["estado"] == "PUBLICABLE" else fila["estado"],
                "GEN2", "RETROSPECTIVA", fila["estado"], *ids, calc,
                sha(resultados_path), sha(carpeta / "sello.json"),
            ))))
    calc = "CALC-REGION-ENVIPE-COMPLEMENTO-0001"
    carpeta = ROOT / "data/corrida0" / calc
    resultados_path = carpeta / "resultados.json"
    datos = json.loads(resultados_path.read_text(encoding="utf-8"))["resultados"]
    for ola in (2023, 2024, 2025):
        pref = f"RESULT-REGION-ENVIPE-CUMPLE-{ola}"
        bruto = json.loads(datos[pref + "-JSON"])
        for fila in bruto["filas"]:
            base = pref + "-" + fila["geografia"]
            ids = [base + suf for suf in ("-P", "-IC-LO", "-IC-HI")]
            punto, lo, hi = (datos[i] for i in ids)
            if fila["estado"] == "PUBLICABLE" and not (0 <= lo <= punto <= hi <= 1):
                raise ValueError(f"IC o punto incoherente: {base}")
            if fila["estado"] != "PUBLICABLE" and any(v is not None for v in (punto, lo, hi)):
                raise ValueError(f"fila suprimida con cifra: {base}")
            filas.append(dict(zip(CAMPOS, (
                "ENVIPE", "cumple_norma_envipe2025", "ENTIDAD", fila["geografia"],
                str(ola), "IC-DE-DISEÑO-DERIVADO", punto, lo, hi, "delito",
                "proporción [0,1]", "delitos con BP1_20 válido; complemento de evasión",
                datos[base + "-N"], datos[base + "-N-EFECTIVO-KISH"],
                "R2 heredada del piso sellado" if fila["estado"] == "PUBLICABLE" else fila["estado"],
                "GEN2", "RETROSPECTIVA", fila["estado"], *ids, calc,
                sha(resultados_path), sha(carpeta / "sello.json"),
            ))))
    calc = "CALC-REGION-ENCIG-CONSUMIDORES-2025-0001"
    carpeta = ROOT / "data/corrida0" / calc
    resultados_path = carpeta / "resultados.json"
    datos = json.loads(resultados_path.read_text(encoding="utf-8"))["resultados"]
    from tools.astra.region.encig2025_consumidores import CONDUCTAS as ENCIG25_CONDUCTAS
    for conducta in ENCIG25_CONDUCTAS:
        pref = f"RESULT-REGION-ENCIG-2025-{conducta}"
        bruto = json.loads(datos[pref + "-JSON"])
        unidad = bruto["unidad"]
        for fila in bruto["filas"]:
            base = pref + "-" + fila["geografia"]
            ids = [base + suf for suf in ("-P", "-IC-LO", "-IC-HI")]
            punto, lo, hi = (datos[i] for i in ids)
            if fila["estado"] == "PUBLICABLE" and not (0 <= lo <= punto <= hi <= 1):
                raise ValueError(f"IC o punto incoherente: {base}")
            if fila["estado"] != "PUBLICABLE" and any(v is not None for v in (punto, lo, hi)):
                raise ValueError(f"fila suprimida con cifra: {base}")
            filas.append(dict(zip(CAMPOS, (
                "ENCIG", conducta, "ENTIDAD", fila["geografia"], "2025", "IC-DE-DISEÑO",
                punto, lo, hi, unidad, "proporción [0,1]",
                "población urbana 100 mil+; códigos y denominador en spec de consumidor",
                datos[base + "-N"], datos[base + "-N-EFECTIVO-KISH"],
                "n≥200 y varianza bootstrap estimable" if fila["estado"] == "PUBLICABLE" else fila["estado"],
                "GEN2", "RETROSPECTIVA", fila["estado"], *ids, calc,
                sha(resultados_path), sha(carpeta / "sello.json"),
            ))))
    calc_pred = "CALC-REGION-IC-PREDICTIVO-0001"
    pred_path = ROOT / "data/corrida0" / calc_pred / "resultados.json"
    pred = json.loads(pred_path.read_text(encoding="utf-8"))["resultados"]
    pisos = {("ENVIPE", "2024"): "evade_norma_envipe2025",
             ("ENCIG", "2023"): "canal_digital_luz",
             ("ENIF", "2021"): "informal_cualquiera_18a70"}
    originales = {(f["instrumento"], f["ola"], f["conducta"], f["geografia_codigo"]): f
                  for f in filas if f["naturaleza_estimacion"] == "IC-DE-DISEÑO"}
    for inst, year in (("ENVIPE", "2024"), ("ENCIG", "2023"), ("ENIF", "2021")):
        payload = json.loads(pred[f"RESULT-REGION-ICP-{inst}-JSON"])
        for row in payload["filas"]:
            original = originales[(inst, year, pisos[(inst, year)], row["geografia"])]
            base = f"RESULT-REGION-ICP-{inst}-{row['geografia']}"
            loid, hiid = base + "-IC-LO", base + "-IC-HI"
            clone = dict(original)
            clone.update(naturaleza_estimacion="IC-PREDICTIVO-CALIBRADO",
                         ic95_inf=pred[loid], ic95_sup=pred[hiid],
                         calidad="intervalo predictivo retrospectivo; ajuste anterior a evaluación",
                         result_inf=loid, result_sup=hiid,
                         calc=original["calc"] + ";" + calc_pred,
                         sha256_resultados=original["sha256_resultados"] + ";" + sha(pred_path),
                         sha256_sello=original["sha256_sello"] + ";" +
                         sha(ROOT / "data/corrida0" / calc_pred / "sello.json"))
            if clone["estado_publicacion"] != "PUBLICABLE" or pred[loid] is None or pred[hiid] is None:
                raise ValueError(f"piso predictivo inválido: {base}")
            filas.append(clone)
    destino = ROOT / "canon/eje-regional-v1_0.tsv"
    with destino.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(filas)
    c = Counter(f["estado_publicacion"] for f in filas)
    resumen = "\n".join(f"- {k}: {v}" for k, v in sorted(c.items()))
    (ROOT / "canon/eje-regional-v1_0.md").write_text(
        "# Eje regional v1.0 · avance medido\n\n"
        "**ARCHIVO**: `canon/eje-regional-v1_0.md`  \n"
        "**NOMBRE ESTABLE**: eje regional v1.0  \n"
        "**ESTADO**: propuesta; adopta NO; RETROSPECTIVA.\n\n"
        "Fuente única de cifras: `python3 tools/astra/region/publica.py`, que lee quince CALC sellados. "
        "La tabla TSV conserva las filas suprimidas. Esta entrega aún no cubre todas las conductas "
        "adoptadas/adoptables ni todas las olas del mandato U5; por tanto, no acredita cierre integral.\n\n"
        "## Decisiones de geografía y publicación\n\n"
        "R1: entidades solo donde el diseño y el estimando lo admiten; ENIF 2024 usa sus seis regiones "
        "oficiales. R2: punto e IC solo con n≥200, varianza estimable y cualquier requisito oficial "
        "más estricto. ENVIPE y ENCIG son entidades de residencia, no ubicación del delito o trámite.\n\n"
        f"## Filas medidas ({len(filas)})\n\n" + resumen + "\n\n"
        "Las filas tienen nivel geográfico explícito y un RESULT por punto y límite. Los IC de "
        "diseño y predictivos calibrados ocupan filas distintas; estos últimos citan dos CALC. Todas las cifras son "
        "RETROSPECTIVA. La repetición conjunta de réplicas por ola se conserva dentro del RESULT "
        "`-JSON` de cada CALC sin identificadores ni pesos individuales.\n\n"
        "## Auditoría de rigor extremo\n\n"
        "El estado de residencia no equivale a una ciudad ni al lugar del evento. ENCIG cubre "
        "un marco urbano y ENIF solo seis regiones: no permiten inferir todos los habitantes "
        "de cada estado. Los niveles reflejan también oferta, recursos e instituciones; no prueban "
        "preferencias culturales. No hay medida de clase o pertenencia indígena en estas filas. "
        "Una variación regional requeriría una comparación histórica con unidades, geografía e IC "
        "comparables; esta tabla no promete detectar cambios futuros.\n\n"
        "La [cobertura conocida](../forense/analisis/region/cobertura-conocida-v1_0.md) "
        "explicita conductas aún pendientes. El [mapa descriptivo](../forense/analisis/region/mapa-estabilidad-v1_0.md) "
        "y la [hoja de mesa](../forense/analisis/region/HOJA-EJE-REGIONAL-para-mesa.md) "
        "mantienen esas reservas; adopta: NO.\n",
        encoding="utf-8")
    print(len(filas), dict(c))


if __name__ == "__main__":
    genera()
