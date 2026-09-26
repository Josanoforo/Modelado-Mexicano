#!/usr/bin/env python3
"""Dictamen afirmación → serie administrativa para las 30 afirmaciones de la
cola v1.1 DINERO/CNBV (21) y DINERO/BANXICO (9).

ACTO GEN2-DINERO-SERIES-CNBV-BANXICO-1. El juicio (serie, dictamen, veredicto)
vive en DICTAMEN; los VALORES se leen de los resultados.json sellados, nunca
se teclean. Los ids se re-derivan de la cola y el script falla si difieren.

Vocabulario de dictamen: RESULT (al menos un RESULT sellado lo contesta) ·
NO-CONSTRUIBLE (la fuente no publica esto como serie; se dice qué se buscó) ·
NO-ACCESIBLE (la serie existe en un portal que esta sesión no alcanzó; NC a
caja). Veredicto (spec DINERO-SERIES-IMOR v1.0 §5): CONFIRMA · MATIZA · ROMPE
· NO-CONTESTA · — (sin RESULT).

    python3 tools/dominios/dinero-series/dictamina.py             # escribe
    python3 tools/dominios/dinero-series/dictamina.py --verifica  # byte a byte
"""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COLA = ROOT / "forense/analisis/dominios/cola-medicion-v1_0.tsv"
OUT = ROOT / "forense/analisis/dinero-series/afirmacion-serie-v1_0.tsv"
CALCS = ["CALC-BANXICO-SERIES-IMOR-0001", "CALC-CNBV-SERIES-IMOR-R16-0001"]

BX = ("Banxico · IMOR de consumo por producto, banca comercial (Informe Trimestral ene-mar 2026)",
      "gen2_banxico_imor_consumo_producto_mensual_2026t1_html", "mensual",
      "https://www.banxico.org.mx/TablasWeb/informes-trimestrales/enero-marzo-2026/B133C3DC-462F-40C1-B2BA-04086A1CFAB1.html",
      "2026-09-11")
R16 = ("CNBV · Portafolio de Información 040-1A-R16, IMOR por tipo de cartera, Total Banca Múltiple",
       "gen2_cnbv_040_1a_r16_imor_tipo_cartera", "foto 2021-12",
       "https://portafolioinfdoctos.cnbv.gob.mx/Documentacion/minfo/XLS/40/040_1a_R16.xls", "2026-09-11")
R16_INST = ("CNBV · 040-1A-R16 por institución (IMOR/IMORA por tipo de cartera)", "040-1A-R16 por institución",
            "mensual", "https://portafolioinfo.cnbv.gob.mx/", "")
SOFIPO = ("CNBV · Boletín estadístico del sector de ahorro y crédito popular (SOFIPO), por entidad",
          "boletín EACP/SOFIPO", "trimestral", "https://portafolioinfo.cnbv.gob.mx/", "")
BDIF = ("CNBV · Base de Datos de Inclusión Financiera (corresponsales, sucursales, puntos de acceso)",
        "BDIF", "trimestral", "https://www.cnbv.gob.mx/Inclusión/", "")
RIB_TDC = ("Banxico · Indicadores Básicos de Tarjetas de Crédito (RIB)", "RIB tarjetas", "semestral",
           "https://www.banxico.org.mx/", "")
RIB_PER = ("Banxico · Indicadores Básicos de Créditos Personales y de Nómina (RIB)", "RIB personales/microcrédito",
           "anual", "https://www.banxico.org.mx/", "")
SIE_FIN = ("Banxico SIE · financiamiento al sector privado / cartera de consumo", "SIE CF297 (manifiesto: "
           "banxico_sie_cf297_financiamiento_sector_privado)", "mensual", "https://www.banxico.org.mx/SieInternet/", "")
NADA = ("—", "—", "—", "—", "")

U_SALDO = "porcentaje de saldo de cartera (SERIE-ADMINISTRATIVA; no persona)"
DENEGADO = ("host denegado por la política de red de esta sesión (proxy 403: www.banxico.org.mx, "
            "portafolioinfo.cnbv.gob.mx, www.cnbv.gob.mx, www.gob.mx, web.archive.org)")

# id: (dictamen, fuente, result_ids, veredicto, razón)
DICTAMEN = {
    "ASTRA5-U0-APUEST-008": ("RESULT", BX, ["BANXICO-SERIES-CON-2024-12"], "MATIZA",
        "el comparador de sistema (IMOR consumo banca comercial dic-2024) está debajo de 6.52%, así que el orden "
        "«por encima del promedio» se sostiene del lado del sistema; la cifra de BanCoppel (R16 por institución) es "
        "NO-ACCESIBLE aquí y además 6.52% puede no ser IMOR de consumo"),
    "ASTRA5-U0-APUEST-018": ("NO-ACCESIBLE", BDIF, [], "—",
        f"número de corresponsales 2019 y participación de OXXO: serie BDIF de CNBV; {DENEGADO}. «50% con cuenta / "
        "33% con tarjeta» de OXXO Pay es dicho de empresa, NO-CONSTRUIBLE como serie (el piso de persona es ENIF)"),
    "ASTRA5-U0-CRFAC-003": ("NO-ACCESIBLE", R16_INST, ["BANXICO-SERIES-CON-2025-09"], "NO-CONTESTA",
        f"la afirmación es IMORA (con castigos); las dos constancias publican solo IMOR, que en sep-2025 da el RESULT "
        f"citado, otro concepto. IMORA consumo: boletín de banca múltiple CNBV; {DENEGADO}"),
    "ASTRA5-U0-CRPOP-001": ("RESULT", BX, ["BANXICO-SERIES-CON-2024-12"], "MATIZA",
        "con el IMOR de consumo del sistema dic-2024 como denominador, el ~5% de Azteca que cita la propia "
        "afirmación queda por debajo del «2-4 veces»; la cifra por institución es NO-ACCESIBLE aquí"),
    "ASTRA5-U0-CRPOP-002": ("RESULT", R16,
        ["CNBV-SERIES-PER-2021-12", "CNBV-SERIES-TDC-2021-12", "CNBV-SERIES-ABCD-2021-12", "CNBV-SERIES-BM-2021-12",
         "BANXICO-SERIES-PER-2026-03", "BANXICO-SERIES-TDC-2026-03", "BANXICO-SERIES-ABCD-2026-03"], "MATIZA",
        "dentro de la banca, personales > tarjeta > ABCD en las dos series; pero «adquisición de bienes muebles» "
        "bancaria supera a personales en R16 2021-12, y el crédito de tienda con cobranza domiciliaria no está en "
        "ninguna serie bancaria: el techo por producto se sostiene para personales y no para «bien durable»"),
    "ASTRA5-U0-CRPOP-005": ("NO-ACCESIBLE", SOFIPO, [], "—",
        f"IMOR/IMORA de Nu México SOFIPO ago-2023: boletín SOFIPO por entidad; {DENEGADO}. Impago de "
        "Klarna/Aplazo: dicho de empresa, NO-CONSTRUIBLE como serie"),
    "ASTRA5-U0-CRPOP-006": ("RESULT", BX, ["BANXICO-SERIES-PER-2024-02"], "MATIZA",
        "el IMOR de créditos personales de banca comercial feb-2024 queda muy lejos de ~10.8%: la cifra no es IMOR "
        "de personales de ese universo; solo sería compatible con IMORA u otro universo, no verificable aquí"),
    "ASTRA5-U0-CRPOP-007": ("RESULT", BX, ["BANXICO-SERIES-NOM-2024-03", "BANXICO-SERIES-TDC-2024-03"], "MATIZA",
        "solo el comparador de sistema mar-2024 (nómina y tarjeta); las cifras de BanCoppel (R16 por institución) "
        "son NO-ACCESIBLE aquí; si fueran IMOR, serían varias veces las del sistema"),
    "ASTRA5-U0-CRPOP-012": ("RESULT", BX, ["BANXICO-SERIES-CON-2024-12"], "CONFIRMA",
        "la parte de sistema (IMOR consumo 3.1% dic-2024) cae dentro de 0.5 pp del RESULT; las cifras de Azteca "
        "(IMOR 3.8/5.2, IMORA ~10.7, cobertura 313%) son R16 por institución, NO-ACCESIBLE aquí"),
    "ASTRA5-U0-CRPOP-017": ("NO-ACCESIBLE", R16_INST, [], "—",
        f"IMOR/IMORA por institución 3T24 y serie 2021-2024: R16 por institución; {DENEGADO}. El ICV de PCR Verum "
        "es calificadora, no serie pública"),
    "ASTRA5-U0-CRPOP-018": ("RESULT", BX, ["BANXICO-SERIES-NOM-2024-03", "BANXICO-SERIES-TDC-2024-03"], "MATIZA",
        "igual que CRPOP-007: solo el comparador de sistema mar-2024; la cifra de la institución y el ROA quedan "
        "NO-ACCESIBLE aquí"),
    "ASTRA5-U0-CRPOP-029": ("NO-CONSTRUIBLE", NADA, [], "—",
        "IMOR/IMORA/ROE de una SOFOM ENR y su línea de fondeo: la CNBV no publica serie prudencial de ENR (buscado: "
        "boletín estadístico de SOFOM ENR en el manifiesto y en las dos constancias); la fuente son reportes de "
        "calificadora y emisora"),
    "ASTRA5-U0-CRPOP-031": ("NO-ACCESIBLE", SOFIPO, [], "—",
        f"IMOR sector SOFIPO jun-2025 e indicadores de CAME: boletín SOFIPO; {DENEGADO}. NICAP e intervención: "
        "comunicados, no serie"),
    "ASTRA5-U0-CRPOP-036": ("NO-ACCESIBLE", R16_INST, [], "—",
        f"«IMOR de consumo del sector popular» abr-2021 no es agregado publicado; se construiría agregando R16 por "
        f"institución con una lista de bancos populares a declarar; {DENEGADO}"),
    "ASTRA5-U0-CRPOP-040": ("NO-CONSTRUIBLE", NADA, [], "—",
        "umbrales normativos de alerta (partes relacionadas, interés capitalizado) y un dato de emisora quebrada: "
        "no es afirmación sobre una serie; buscado: R16 y boletines en las dos constancias"),
    "ASTRA5-U0-CRPOP-044": ("RESULT", BX, ["BANXICO-SERIES-CON-2024-12", "BANXICO-SERIES-CON-2026-03"], "CONFIRMA",
        "la parte de sistema («IMOR de consumo del sistema ~3%») se sostiene en dic-2024 y mar-2026; la de bancos "
        "populares (5-8% / 10-16% ajustado) es R16 por institución, NO-ACCESIBLE aquí"),
    "ASTRA5-U0-CRPOP-049": ("NO-ACCESIBLE", R16_INST, [], "—",
        f"IMOR etapa 3 de Compartamos: R16 por institución; {DENEGADO}. Castigos trimestrales: reporte BMV de la "
        "emisora, no serie CNBV"),
    "ASTRA5-U0-CRPOP-055": ("RESULT", BX, ["BANXICO-SERIES-CON-2023-12"], "CONFIRMA",
        "IMOR de consumo dic-2023 (3.4%) cae dentro de 0.5 pp del RESULT; los IMOR ajustados (consumo 10.5%, "
        "tarjeta 13.7% jun-2025) y la banca total (2.1/4.1) no están en las constancias: NO-ACCESIBLE aquí"),
    "ASTRA5-U0-CRPOP-057": ("NO-ACCESIBLE", R16_INST, [], "—",
        f"la regla IMORA > 2.5×IMOR se evalúa por institución con R16 (bancos) y boletín SOFIPO (CAME); {DENEGADO}"),
    "ASTRA5-U0-CRPOP-060": ("NO-ACCESIBLE", SOFIPO, [], "—",
        f"castigos y cartera vencida ajustada de CAME y comparación con Azteca/BanCoppel/Findep: boletín SOFIPO y "
        f"R16 por institución; {DENEGADO}"),
    "ASTRA5-U0-CLASE-042": ("NO-ACCESIBLE", SOFIPO, [], "—",
        f"morosidad de SOFIPO 2025 (9.91%): boletín SOFIPO; {DENEGADO}. La alerta del REF es texto, no serie"),
    "ASTRA5-U0-CRFAC-004": ("NO-ACCESIBLE", SIE_FIN, [], "—",
        f"crecimiento real de la cartera de consumo: SIE (el payload CF297 está en el manifiesto pero no en este "
        f"clon; se trae desde caja); {DENEGADO}"),
    "ASTRA5-U0-CRFAC-007": ("RESULT", BX,
        ["BANXICO-SERIES-CON-YOY-2026-03-PP", "BANXICO-SERIES-TDC-YOY-2026-03-PP", "BANXICO-SERIES-ABCD-YOY-2026-03-PP",
         "BANXICO-SERIES-NOM-YOY-2026-03-PP", "BANXICO-SERIES-PER-YOY-2026-03-PP"], "MATIZA",
        "RETROSPECTIVO-NO-PREREGISTRADO (no estaba en spec §5): el patrón «morosidad sube en todos los segmentos "
        "salvo nómina» se ve en el cambio interanual a mar-2026 (nómina es el único negativo); la cita del REF es "
        "de dic-2025 y el crecimiento de saldos no está en esta serie"),
    "ASTRA5-U0-CRFAC-011": ("NO-ACCESIBLE", RIB_TDC, [], "—",
        f"CAT promedio de tarjetas clásicas 2024: RIB de tarjetas de Banxico; {DENEGADO}. Fichas CONDUSEF y "
        "«44% totaleros»: otra fuente (CONDUSEF / encuesta), fuera de este acto"),
    "ASTRA5-U0-CRFAC-013": ("NO-ACCESIBLE", SIE_FIN, [], "—",
        f"financiamiento a hogares como % del PIB: SIE financiamiento + PIB; {DENEGADO}"),
    "ASTRA5-U0-CRFAC-020": ("NO-CONSTRUIBLE", NADA, [], "—",
        "morosidad de SOFOM ENR y OIFNB «en niveles históricamente altos»: dicho del REF, que la construye con "
        "información de burós; no hay serie pública por sector (buscado: boletines CNBV y SIE en el manifiesto)"),
    "ASTRA5-U0-CRPOP-050": ("NO-ACCESIBLE", RIB_PER, [], "—",
        f"pérdida esperada y CAT por institución: RIB de créditos personales de Banxico; {DENEGADO}"),
    "ASTRA5-U0-TRUST-018": ("NO-CONSTRUIBLE", NADA, [], "—",
        "«82% de las transacciones en efectivo»: sin fuente identificada; no es serie administrativa de pagos "
        "(las series SPEI/CoDi del manifiesto miden montos y operaciones electrónicas, no la proporción en "
        "efectivo); el piso de persona sería ENIF, fuera de este acto"),
    "ASTRA5-U0-VIOL-041": ("NO-CONSTRUIBLE", NADA, [], "—",
        "estudio econométrico de Banxico (homicidios → IED estatal): estimación de investigación, no serie; título "
        "no identificado por el report"),
    "ASTRA5-U0-CONS-021": ("NO-ACCESIBLE", RIB_TDC, [], "—",
        f"participación de MSI en saldos de tarjeta: RIB de tarjetas de Banxico; {DENEGADO}"),
}

COLS = ["id_afirmacion", "programa_cola", "dictamen", "serie", "id_serie_tabla", "periodicidad", "unidad",
        "url", "fecha_descarga_constancia", "result_ids", "valores", "veredicto", "evaluacion", "razon"]


def cola_ids() -> dict:
    lineas = [l for l in COLA.read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    out = {}
    for r in csv.DictReader(lineas, delimiter="\t"):
        if r["dominio"] == "DINERO" and r["programa"] in ("CNBV", "BANXICO"):
            for i in r["ids"].split(";"):
                out[i] = r["programa"]
    return out


def valores() -> dict:
    v = {}
    for c in CALCS:
        v.update(json.loads((ROOT / "data/corrida0" / c / "resultados.json").read_text())["resultados"])
    return v


def main(verifica: bool) -> int:
    ids, val = cola_ids(), valores()
    if set(ids) != set(DICTAMEN):
        print("ERROR ids cola≠dictamen:", sorted(set(ids) ^ set(DICTAMEN)))
        return 2
    filas = []
    for i, prog in ids.items():
        dic, f, rids, ver, razon = DICTAMEN[i]
        rids = ["RESULT-" + r for r in rids]
        filas.append({"id_afirmacion": i, "programa_cola": prog, "dictamen": dic, "serie": f[0],
                      "id_serie_tabla": f[1], "periodicidad": f[2],
                      "unidad": U_SALDO if rids else ("—" if f is NADA else "serie administrativa (ver fuente)"),
                      "url": f[3], "fecha_descarga_constancia": f[4] if rids else "",
                      "result_ids": ";".join(rids), "valores": ";".join(f"{r}={val[r]}" for r in rids),
                      "veredicto": ver, "evaluacion": "RETROSPECTIVA" if rids else "—", "razon": razon})
    buf = io.StringIO()
    buf.write("# GENERADO por tools/dominios/dinero-series/dictamina.py — no editar\n")
    w = csv.DictWriter(buf, COLS, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(filas)
    txt = buf.getvalue()
    if verifica:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == txt
        print(("COINCIDE " if ok else "DIFIERE  ") + str(OUT.relative_to(ROOT)))
        return 0 if ok else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(txt, encoding="utf-8")
    from collections import Counter
    print("afirmaciones:", len(filas), "· dictamen:", dict(Counter(f["dictamen"] for f in filas)),
          "· veredicto:", dict(Counter(f["veredicto"] for f in filas)), "· sin dictamen:",
          sum(1 for f in filas if not f["dictamen"]))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifica" in sys.argv))
