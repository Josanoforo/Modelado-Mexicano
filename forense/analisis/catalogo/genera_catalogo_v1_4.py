#!/usr/bin/env python3
"""Catálogo del mexicano v1.4 (ACTO GEN2-CIERRE-Y-PRODUCTO-3; sucesor del generador v1.3 de
GEN2-CIERRE-SEMANAL-2, que queda intacto — E.1).

Añade a v1.3 (secciones S9–S12 y el rótulo del lote 3): los CALC sellados del 27–28/sep
que el registro derivado del commit ve SELLADA con cuenta_gen2=SI (constancia:
v1_4/registro-semana-v1_4.tsv) — pisos de confianza ENCIG 2023 (PISOS-Y-ADENDAS-1),
pisos de dominio PDR1 (PISOS-DOMINIOS-Y-REGLAS-1) y contrastes de momento CALC-ALT-*
(CALC-ALTERNOS-LOTE-1, con `holdout_gastado` en la fila) — con estado de adopción
PROPUESTO POR INSTRUMENTO en v1_4/bloque-adopcion-cifras-v1_4.tsv. La adopción es el
merge de mesa del PR que trae este bloque (E.2): `firma_fp = MERGE-DE-MESA:GEN2-CIERRE-Y-PRODUCTO-3`.
Rótulo del lote 3 de validación ciega (dictamen-lote3-v1_1.tsv) en `validacion_ciega_lote3`;
las 15 ENVIPE 2024 retiradas por fb50-02 (R21) pasan a SUSPENDIDA-POR-FIRMA con sucesor.

Texto heredado de v1.3:

Añade a v1.2: los pisos de FIRMAS-20 A1–A6 (ENSU, COLA-LOTE-1, COLA-COMPLETA-1; el
VETO de Intercensal 2015 va a excluidos y a data/corrida0/decisiones.tsv) y el
rótulo de la validación ciega del lote 1 (beee-02: columna `validacion_ciega`;
las 7 PROPONER-SUSPENDER pasan a estado SUSPENDIDA-POR-FIRMA con `sucesor`, sin
borrarse ni tocar el sello).

Deriva, sin teclear una sola cifra, las tablas del catálogo v1.4:

  canon/catalogo-del-mexicano-v1_4.tsv            estimadores (P1)
  forense/analisis/catalogo/v1_4/calcs-v1_4.tsv         CALC citados, con sus hashes
  forense/analisis/catalogo/v1_4/pendientes-de-firma-v1_4.tsv
  forense/analisis/catalogo/v1_4/excluidos-v1_4.tsv     fuera por regla, con nota
  forense/analisis/catalogo/v1_4/cobertura-31-v1_4.tsv  cobertura por report (P3)
  forense/analisis/catalogo/v1_4/conteos-v1_4.json      toda cifra de la portada

y renderiza la portada canon/catalogo-del-mexicano-v1_4.md desde
forense/analisis/catalogo/v1_4/plantilla-v1_4.md ({{c:clave}} -> conteos.json;
{{r:RESULT-ID}} -> valor sellado del RESULT).

Entra un estimador SOLO si (a) su RESULT vive en un CALC con sello válido,
(b) una firma de mesa lo adopta y se cita por id (FP-… FIRMADA en
forense/firmas-pendientes.tsv, u objeto de data/corrida0/decisiones.tsv), y
(c) su piso no es HEREDADO-DE-LEGACY (censo de ENCIG-PISOS-GEN2-1).

Uso:  python3 forense/analisis/catalogo/genera_catalogo_v1_4.py [--sin-registro]
      --sin-registro reutiliza v1_4/adoptados-activos-v1_4.tsv en vez de derivar
      los adoptados activos de la vista en memoria de corrida0 (~2 min).
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import pathlib
import re
import sys
from collections import Counter

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
CORRIDA = ROOT / "data/corrida0"
DIR = ROOT / "forense/analisis/catalogo/v1_4"
TSV = ROOT / "canon/catalogo-del-mexicano-v1_4.tsv"
MD = ROOT / "canon/catalogo-del-mexicano-v1_4.md"
csv.field_size_limit(sys.maxsize)
sys.path.insert(0, str(ROOT / "forense/analisis/catalogo"))
sys.path.insert(0, str(ROOT / "tools"))
from genera_catalogo import INSTRUMENT_FALLBACK, related, verified  # noqa: E402

FIELDS = [
    "llave", "dominio", "instrumento", "ola", "conducta", "eje", "segmento",
    "unidad", "punto", "ic95_inf", "ic95_sup", "naturaleza_ic", "temporalidad",
    "origen_piso", "estado_adopcion", "alcance", "firma_fp", "result_id",
    "celda", "calc", "oferta_exclusion", "reserva", "validacion_ciega", "sucesor",
    "validacion_ciega_lote3", "holdout_gastado",
]

# ── asignación de dominio (PROPUESTO-POR-EJECUTOR; los ids son los del mapa
# U0, canon/mapa-dominios-v1_0.tsv columna `dominio`). Por prefijo de regla
# consumidora; por CALC para los pisos por instrumento.
DOMINIO_POR_REGLA = {
    "dinero": "DINERO", "DIN": "DINERO",
    "tramite": "CONFIANZA", "TRA": "CONFIANZA",
    "civico": "POLITICA", "CIV": "POLITICA",
    "familia": "FAMILIA_CUIDADOS", "FAM": "FAMILIA_CUIDADOS",
    "salud": "SALUD",
}
DOMINIO_POR_CALC = [
    ("CALC-ENOE-", "TRABAJO"),
    ("CALC-ENDIREH-", "GENERO"),
    ("CALC-ENDUTIH-", "TECNOLOGIA"),
    ("CALC-MOCIBA-", "TECNOLOGIA"),
    ("CALC-ENIGH20", "FAMILIA_CUIDADOS"),
]

# ── pisos por instrumento adoptados por Firma T (FIRMAS-15 §1 T + ADENDA-1).
ASTRA = {
    "FP-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01": ["CALC-ENOE-PISOS-0003"],
    "FP-260923-ASTRA5-U2-ENDIREH-6a2c-01": [
        "CALC-ENDIREH-PISOS-2021-AYUDA-0001",
        "CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001",
        "CALC-ENDIREH-PISOS-2021-DECISIONES-0001",
        "CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001",
        "CALC-ENDIREH-PISOS-2021-ESCOLAR-0001",
        "CALC-ENDIREH-PISOS-2021-FAMILIAR-0001",
        "CALC-ENDIREH-PISOS-2021-LABORAL-0001",
        "CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001",
        "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0004",
        "CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-BC-0001",
    ],
    "FP-260923-ASTRA5-U2-ENDIREH-6a2c-02": [
        "CALC-ENDIREH-PISOS-2016-DISCRIMINACION-0001",
        "CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002",
        "CALC-ENDIREH-PISOS-2016-RESTANTES-0001",
    ],
    "FP-260923-ASTRA5-U2-ENDIREH-6a2c-03": ["CALC-ENDIREH-PISOS-2011-MODULOS-0001"],
    "FP-260923-ASTRA5-U2-ENDIREH-6a2c-04": ["CALC-ENDIREH-PISOS-2006-MODULOS-0002"],
    "FP-260923-ASTRA5-U4-TECNOLOGIA-1f30-01": [
        f"CALC-ENDUTIH-PISOS-{a}-0001" for a in (2023, 2024, 2025)
    ] + [f"CALC-ENDUTIH-EMPLEO-15MAS-{a}-0001" for a in (2023, 2024, 2025)],
    "FP-260923-ASTRA5-U4-TECNOLOGIA-1f30-02": [
        f"CALC-MOCIBA-PISOS-{a}-0001" for a in (2015, 2016, 2017)
    ],
}
# Firma M (GEN2-ADOPCION-BLOQUE-Y-PINES-1): bloque ENIGH con replay IDENTICO;
# se cita por su fila de decisiones.tsv (objeto = CALC).
ENIGH_MEDIDAS = (
    "PREVALENCIA", "REMESAS-MEDIA", "REMESAS-MEDIANA",
    "PARTICIPACION-MEDIA-HOGAR", "PARTICIPACION-AGREGADA", "PARTICIPACION-GE50",
)
# Adopción de marginales (piso t−1) por instrumento.
MARG_ENIF = "FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01"
MARG_ENVIPE = "decisiones.tsv:adopcion:piso-t1-marginales-por-instrumento"
CENSO = ROOT / "forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv"
RAMA_PISOS2 = "acto/gen2-pisos-gen2-2"
FIRMAS16 = (
    "FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01",
    "FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-02",
    "FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-03",
    "FP-260924-GEN2-CLASE-AMAI-1-e773-01",
)
FIRMAS16_PISOS = (
    ("FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01", "CALC-ENSANUT-PISOS-SALUD-0001", "SALUD", "ENSANUT",
     "ADOPTADO-CON-RESERVA-DE-ANCHO"),
    ("FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-02", "CALC-ENCODAT-PISOS-SUSTANCIAS-0001", "SALUD", "ENCODAT",
     "ADOPTADO-CON-RESERVA-DE-ANCHO"),
    ("FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-03", "CALC-ENBIARE-PISOS-BIENESTAR-0001", "SALUD_MENTAL",
     "ENBIARE", "ADOPTADO"),
)
FP_NSE = "FP-260924-GEN2-CLASE-AMAI-1-e773-01"
# Letra de la firma: ENIGH 2022 y ENIF 2024; ENDUTIH 2023 como aproximación rotulada.
NSE_ADMITIDO = {("ENIGH", "2022"): "regla AMAI reproducida", ("ENIF", "2024"): "aproximación conforme",
                ("ENDUTIH", "2023"): "APROXIMACIÓN ROTULADA"}
NSE_DOMINIO = {"ENIGH": "FAMILIA_CUIDADOS", "ENIF": "DINERO", "ENDUTIH": "TECNOLOGIA"}

# ── FIRMAS-19 (J1–J10): pisos por instrumento. (fp, calc, dominio, instrumento, estado, reserva)
_F19 = "FP-260925-GEN2-"
FIRMAS19_PISOS = (
    (_F19 + "CONSUMO-Y-GASTO-PISOS-1-2d37-01", "CALC-ENIGH-CONSUMO-PISOS-0002", "CONSUMO", "ENIGH",
     "ADOPTADO-CON-RESERVA-DE-ANCHO", "J1: 2020 (pandemia) infla tau2; canal y fiado sin columna de oferta (NO-CONSTRUIBLE); unidad HOGAR"),
    (_F19 + "CONSUMO-Y-GASTO-PISOS-1-2d37-02", "CALC-ENGASTO-CONSUMO-PISOS-0001", "CONSUMO", "ENGASTO",
     "ADOPTADO-CON-RESERVA-DE-ANCHO", "J2: describe 2012; una ola; sin extrapolación a olas posteriores; unidad HOGAR"),
    (_F19 + "CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-01", "CALC-WVS-PISOS-2018-0001", "CONFIANZA", "WVS",
     "ADOPTADO-CON-RESERVA-DE-ANCHO", "J4: sin estrato público"),
    (_F19 + "CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-02", "CALC-LATINOBAROMETRO-PISOS-2023-0001", "CONFIANZA",
     "LATINOBAROMETRO", "ADOPTADO-CON-RESERVA-DE-ANCHO", "J5: sin estrato ni UPM; 2024 sigue RESERVADA"),
    (_F19 + "CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-03", "CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001", "RELIGIOSIDAD",
     "PEW", "ADOPTADO-CON-RESERVA-DE-ANCHO", "J6: diseño parcial por ola"),
    (_F19 + "CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-04", "CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001", "CAPITAL_SOCIAL",
     "LAPOP", "ADOPTADO-CON-RESERVA-DE-ANCHO", "J7: SIN SERIE hasta dictamen de equivalencia; cada ola se lee sola"),
    (_F19 + "FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-01", "CALC-ENADID-FAMILIA-HOGARES-0001", "FAMILIA_CUIDADOS",
     "ENADID", "ADOPTADO", "J8: tres olas, diseño completo"),
    (_F19 + "FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-02", "CALC-ENASIC-CUIDADOS-VEJEZ-0001", "FAMILIA_CUIDADOS",
     "ENASIC", "ADOPTADO-CON-RESERVA-DE-ANCHO", "J9: una ola; cuidador principal con n pequeña; sin tamaño de localidad"),
    (_F19 + "FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-03", "CALC-PEW-MIGRACION-MEX-0001", "MIGRACION",
     "PEW", "ADOPTADO-CON-RESERVA-DE-ANCHO", "J10: 2013 y 2023 sin PSU; disposiciones, no flujos; clase de evidencia según la FP"),
)
FP_AFE1 = "FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01"
AFE1_CALCS = ("CALC-ENIF-0001", "CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001",
              "CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001", "CALC-R-DIN-M-01-v4")
# Actos fusionados durante el corte cuya FP de adopción se lista si sigue ABIERTA (encargo §2).
FP_ADOPCION_EN_CURSO: tuple = ()  # v1.2 listaba ENSU aquí; en v1.4 ENSU entra por FIRMAS-20 A1
FP_J3 = _F19 + "CONSUMO-Y-GASTO-PISOS-1-2d37-03"

# ── FIRMAS-20 (A1–A6, 26/sep): pisos por instrumento con llave RESULT-<pref><conducta>-<ola>-<eje>-<seg>-P.
# (fp, calc, prefijo RESULT, dominio del mapa, instrumento, estado, unidad, reserva). Dominio: PROPUESTO-POR-EJECUTOR.
_A1 = "FP-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-01"
_A6 = "FP-260926-GEN2-COLA-COMPLETA-1-0d4a-01"
_L1 = "FP-260926-GEN2-COLA-LOTE-1-3a49-0"
_RES = "ADOPTADO-CON-RESERVA-DE-ANCHO"
FIRMAS20_PISOS = (
    (_A1, "CALC-ENSU-PISOS-0001", "RESULT-ENSU-PISOS-", "VIOLENCIA", "ENSU", _RES, "proporcion (persona 18+ urbana)",
     "A1: C09–C12 con «No aplica» en el denominador, no comparables con comunicados"),
    (_A1, "CALC-ENSU-SERIE-0001", "RESULT-ENSU-SERIE-", "VIOLENCIA", "ENSU", _RES, "proporcion (persona 18+ urbana)",
     "A1: serie trimestral; 2017T1 sin sexo/edad; C09–C12 no comparables con comunicados"),
    (_L1 + "1", "CALC-CCPV-FAM-PISOS-0001", "RESULT-CCPV-FAM-PISOS-", "FAMILIA_CUIDADOS", "CCPV", _RES,
     "proporcion (hogar; PER60-VIVE-SOLO: persona 60+)", "A2: descripción de 2010, sin extrapolar a 2020"),
    (_L1 + "2", "CALC-EMAT-PAREJA-PISOS-0001", "RESULT-EMAT-PAREJA-PISOS-", "PAREJA", "EMAT", _RES,
     "proporcion (matrimonio o contrayente registrado)",
     "A3: matrimonio civil inscrito por año de registro (unión libre fuera); sin tasas"),
    (_L1 + "3", "CALC-EDR-SUICIDIO-PISOS-0001", "RESULT-EDR-SUICIDIO-PISOS-", "SALUD_MENTAL", "EDR", _RES,
     "proporcion (defuncion registrada)",
     "A4: composición de defunciones registradas, nunca tasa por habitante; ola = año de registro; unidad DEFUNCIÓN"),
    (_L1 + "4", "CALC-ENPECYT-CONOC-PISOS-0001", "RESULT-ENPECYT-CONOC-PISOS-", "CONOCIMIENTO", "ENPECYT", _RES,
     "proporcion (persona 18+ urbana de 100 000+)", "A5: universo urbano; cambio de reactivo 2015 absorbido por tau2"),
    (_A6, "CALC-ENDISEG-PISOS-2021-0001", "RESULT-ENDISEG-PISOS-2021-", "GENERO", "ENDISEG", "ADOPTADO",
     "proporcion (persona)", "A6: una ola"),
    (_A6, "CALC-MMSI-PISOS-2016-0001", "RESULT-MMSI-PISOS-2016-", "MOVILIDAD", "MMSI", "ADOPTADO",
     "proporcion (persona)", "A6: una ola"),
    (_A6, "CALC-ENASEM-ESCOLARIDAD-2021-0001", "RESULT-ENASEM-ESCOLARIDAD-2021-", "MOVILIDAD", "ENASEM", "ADOPTADO",
     "proporcion (persona 50+)", "A6: una ola"),
    (_A6, "CALC-ENVIPE-PERCEPCION-2024-0001", "RESULT-ENVIPE-PERCEPCION-2024-", "VIOLENCIA", "ENVIPE", "ADOPTADO",
     "proporcion (persona 18+)", "A6: una ola; unidad persona, no delito"),
    (_A6, "CALC-ENOE-PARTICIPACION-2024T4-0001", "RESULT-ENOE-PARTICIPACION-2024T4-", "TRABAJO", "ENOE", "ADOPTADO",
     "proporcion (persona)", "A6: un trimestre"),
    (_A6, "CALC-LATINOBAROMETRO-COLA-2023-0001", "RESULT-LATINOBAROMETRO-COLA-2023-", "POLITICA", "LATINOBAROMETRO", _RES,
     "proporcion (persona 18+)", "A6: complemento de 2023; sin estrato ni UPM"),
    (_A6, "CALC-PEW-RELIGION-2024-0001", "RESULT-PEW-RELIGION-2024-", "RELIGIOSIDAD", "PEW", _RES,
     "proporcion (persona 18+)", "A6: una ola"),
    (_A6, "CALC-ENADID-COLA-2018-0001", "RESULT-ENADID-COLA-2018-", "FAMILIA_CUIDADOS", "ENADID", _RES,
     "proporcion (hogar o mujer, según conducta)", "A6: una ola"),
)
# A6: VETO de Intercensal 2015 (payload solo Estado de México). Fila en decisiones.tsv por RESULT.
FIRMAS20_VETADOS = ((_A6, "CALC-EIC-HOGARES-2015-0001"),)
RX_A20 = re.compile(r"(?P<c>.+?)-(?P<o>(?:19|20)\d\d(?:T[1-4])?)-(?P<r>.+)-P$")
EJES_A20 = ("EDAD-JEFE", "ESCOLARIDAD-JEFE", "SEXO-JEFE", "CLASE-SUBJETIVA")
# beee-02 (27/sep): rótulo de la validación ciega del lote 1, por llave de la tabla del recibo.
FP_BEEE02 = "FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02"
RECIBO = ROOT / "forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/2026-09-27-gen2-recibo-astra6-1--tabla-result-estado-efecto.tsv"
# CALC sucesor de las suspendidas, nombrado por llave (D-24): no existe ni se abre aquí.
SUCESOR_SUSPENDIDAS = ("CALC sucesor por llave: <CALC-ENDIREH-PISOS-2011-MODULOS-sucesor> (caja; spec nueva con el "
                       "denominador de la spec humana; instituciones de ayuda 2011 y celda de publicabilidad)")
ROTULO_ACOTAR = {"cifra": "ACOTADA:DELTA-PUNTO-EN-VALIDACION-CIEGA", "alcance": "ACOTADA:PUBLICABILIDAD-FRAGIL-AL-RNG"}
# Ejes de varios tokens en las llaves RESULT (el resto: primer token).
EJES_COMPUESTOS = ("EDAD-JEFE", "ESCOLARIDAD-JEFE", "SEXO-JEFE", "CONDICION-PAREJA", "CLASE-SUBJETIVA",
                   "INGRESO-SUBJETIVO", "TAMANO-HOGAR")
RELIG_RE = re.compile(r"RELIG|DIOS|IGLESIA|SERVICIO|REZA|ORA-")
PREFIJO_RESULT = {
    "CALC-ENIGH-CONSUMO-PISOS-0002": "RESULT-ENIGH-CONSUMO-PISOS-",
    "CALC-ENGASTO-CONSUMO-PISOS-0001": "RESULT-ENGASTO-CONSUMO-PISOS-",
    "CALC-WVS-PISOS-2018-0001": "RESULT-WVS-PISOS-2018-",
    "CALC-LATINOBAROMETRO-PISOS-2023-0001": "RESULT-LATINOBAROMETRO-PISOS-2023-",
    "CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001": "RESULT-PEW-PISOS-",
    "CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001": "RESULT-LAPOP-PISOS-CS-",
    "CALC-ENADID-FAMILIA-HOGARES-0001": "RESULT-ENADID-FAMILIA-HOGARES-",
    "CALC-ENASIC-CUIDADOS-VEJEZ-0001": "RESULT-ENASIC-CUIDADOS-VEJEZ-",
    "CALC-PEW-MIGRACION-MEX-0001": "RESULT-PEW-MIGRACION-MEX-",
}
FP_RE = re.compile(r"FP-(?:\d{6}-[A-Z0-9-]+-[0-9a-f]{4}-\d{2}|\d+)")


def lee(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(newline="") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def escribe(path: pathlib.Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as s:
        w = csv.DictWriter(s, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def num(x) -> str:
    return "" if x is None else repr(float(x)) if isinstance(x, (int, float)) else str(x)


def tabla(data: dict, key: str) -> list[dict]:
    v = data[key]
    v = json.loads(v) if isinstance(v, str) else v
    return v["celdas"] if isinstance(v, dict) else v


def firmas() -> dict[str, str]:
    return {r["id"]: r["estado"] for r in lee(ROOT / "forense/firmas-pendientes.tsv")}


def decisiones() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in lee(CORRIDA / "decisiones.tsv"):
        out.setdefault(r["objeto"], r)
    return out


class Calcs:
    """Cache de CALC verificados (sello.sha256 → sello.json → resultados.json)."""

    def __init__(self) -> None:
        self.c: dict[str, tuple[dict, str, str, dict]] = {}

    def __call__(self, calc: str) -> tuple[dict, str, str, dict]:
        if calc not in self.c:
            data, rh, sh = verified(calc)
            spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
            self.c[calc] = data, rh, sh, spec
        return self.c[calc]


def adoptados_activos(sin_registro: bool) -> list[dict[str, str]]:
    """Los adoptados activos de `corrida0 status` (misma definición, misma vista)."""
    path = DIR / "adoptados-activos-v1_4.tsv"
    fields = ["result_id", "calc", "consumidor", "regla", "tipo_uso", "pin_de_mesa",
              "origen_numerico"]
    if sin_registro and path.exists():
        return lee(path)
    import corrida0 as c0  # noqa: PLC0415
    v = c0._filas_registro(verifica=False)
    escribe(REGISTRO_SEMANA, ["spec_id", "estado", "cuenta_gen2", "n_resultados", "resultado_replay"],
            sorted(({k: str(f.get(k, "")) for k in ("spec_id", "estado", "cuenta_gen2", "n_resultados", "resultado_replay")}
                    for f in v["corridas"] if f["spec_id"] in {x[0] for x in SEMANA} | {x[0] for x in SEMANA_FUERA}),
                   key=lambda f: f["spec_id"]))
    sell = {f["resultado_id"]: f for f in v["resultados"]
            if f["origen"] == "OFERTA" and f["cuenta_gen2"] == "SI"
            and str(f["estado"]).startswith(("SELLADA", "SUPERADO"))}
    rows, vistos = [], set()
    for u in v["usos"]:
        rid = u["corrida0_resultado_id"]
        if (u["activo"] != "SI" or u["generacion_leida"] != "GEN2"
                or not str(u["aptitud_uso"]).startswith("APTA-") or rid not in sell):
            continue
        clave = (rid, u["consumidor"])
        if clave in vistos:
            continue
        vistos.add(clave)
        rows.append({"result_id": rid, "calc": sell[rid]["spec_id"],
                     "consumidor": u["consumidor"], "regla": u["reglas_impacto"],
                     "tipo_uso": u["tipo_uso"], "pin_de_mesa": u["pin_de_mesa"] or "",
                     "origen_numerico": u["origen_numerico"]})
    rows.sort(key=lambda r: (r["result_id"], r["consumidor"]))
    escribe(path, fields, rows)
    return rows


def firma_de(calc: str, pin: str, dec: dict, fps: dict) -> str:
    """FP firmada citada por id; si no hay, el objeto de decisiones.tsv."""
    for texto in (pin, dec.get(calc, {}).get("fuente", ""), dec.get(calc, {}).get("decision", "")):
        for fp in FP_RE.findall(texto or ""):
            if str(fps.get(fp, "")).startswith("FIRMADA"):
                return fp
    if calc in dec and dec[calc]["decision"].startswith("cuenta_gen2=SI"):
        return f"decisiones.tsv:{calc}"
    # FIRMAS-18 (afe1-01, opción a): los adoptados por etiqueta sin FP citable entran citando la firma.
    if calc in AFE1_CALCS and str(fps.get(FP_AFE1, "")).startswith("FIRMADA"):
        return FP_AFE1
    # Firma de mesa verbatim en un encargo archivado (A.12), citada por el pin.
    m = re.search(r"(forense/encargos/\S+\.md)\b.*?\((firma [^)]+)\)", pin or "")
    if m and (ROOT / m.group(1)).exists():
        return f"{m.group(1)}#{m.group(2)}"
    return ""


def instrumento_de(calc: str, spec: dict, rid: str) -> str:
    texto = str(spec.get("universo", "")) + " " + str(spec.get("estimando", ""))
    m = re.findall(r"\b(ENIF|ENCIG|ENVIPE|ENCUCI|ENIGH|ENFIH|ENUT|ENSANUT|EDER|ENNViH-1|LAPOP)\s*(20\d{2})",
                   texto, re.IGNORECASE)
    if calc.startswith("CALC-ENCUCI-"):
        return "ENCUCI 2020"
    if calc == "CALC-B-0001":
        return "ENIGH 2022"
    if m:
        return f"{m[0][0].upper()} {m[0][1]}"
    return INSTRUMENT_FALLBACK.get(calc, "INSTRUMENTO-NO-IDENTIFICADO")


def main() -> None:
    sin_registro = "--sin-registro" in sys.argv
    fps, dec, get = firmas(), decisiones(), Calcs()
    censo = {r["resultado_puntual"]: r for r in lee(CENSO)}
    legacy = {k for k, r in censo.items() if r["clase_censo"] == "HEREDADO-DE-LEGACY"}
    marcador = lee(CORRIDA / "marcador-segmento.tsv")
    prosp = {m["resultado_id"]: m["prospectividad"] for m in marcador if m["resultado_id"]}
    rows: dict[str, dict] = {}
    excl: list[dict] = []
    pend: list[dict] = []

    def fuera(llave, calc, causa, nota, firma=""):
        excl.append({"llave": llave, "calc": calc, "causa": causa, "firma": firma, "nota": nota})

    # ── S1 · adoptados activos (parámetros de reglas y celdas-D del marcador)
    for a in adoptados_activos(sin_registro):
        rid, calc = a["result_id"], a["calc"]
        if rid in legacy:
            fuera(rid, calc, "PISO-HEREDADO-DE-LEGACY",
                  f"re-medido por GEN2-PISOS-GEN2-2 (PR #1123: pisos y sucesores -0002 sellados, sin adopción firmada; censo {CENSO.name})")
            continue
        data, _rh, _sh, spec = get(calc)
        firma = firma_de(calc, a["pin_de_mesa"], dec, fps)
        if not firma:
            pend.append({"id": "SIN-FP-CITABLE", "objeto": rid, "calc": calc,
                         "estado_fp": "NO-ENCONTRADA",
                         "nota": "uso activo sin FP firmada ni decisión cuenta_gen2 por CALC"})
            continue
        if rid in rows:
            # Un momento (M04, M08) no trae prefijo de regla: el dominio sale de otro consumidor.
            pref2 = re.split(r"[.\-]", a["regla"])[0] if a["regla"] else ""
            if rows[rid]["dominio"] == "SIN-DOMINIO" and pref2 in DOMINIO_POR_REGLA:
                rows[rid]["dominio"], rows[rid]["segmento"] = DOMINIO_POR_REGLA[pref2], a["regla"]
            continue
        lo, hi = related(data, rid, "INF"), related(data, rid, "SUP")
        regla = a["regla"]
        pref = re.split(r"[.\-]", regla)[0] if regla else ""
        inst = instrumento_de(calc, spec, rid)
        ola = (re.search(r"(20\d{2}|19\d{2})", inst) or [""])[0] if inst else ""
        dom = DOMINIO_POR_REGLA.get(pref, "SIN-DOMINIO")
        t = prosp.get(rid, "")
        rows[rid] = {
            "llave": rid, "dominio": dom, "instrumento": inst.split(" ")[0], "ola": ola,
            "conducta": ":".join(a["consumidor"].split(":")[-2:]) if a["consumidor"].split(":")[-1] in ("M", "R", "L") else a["consumidor"].split(":")[-1], "eje": "regla",
            "segmento": regla or "VER-ESTIMANDO",
            "unidad": str(spec.get("unidad", "VER-SPEC"))[:120],
            "punto": num(data[rid]),
            "ic95_inf": num(data[lo]) if lo else "", "ic95_sup": num(data[hi]) if hi else "",
            "naturaleza_ic": "IC95-DE-SPEC-SIN-CALIBRACION" if lo else "SIN-IC-IDENTIFICADO",
            "temporalidad": "PROSPECTIVA" if t == "PROSPECTIVA" else "RETROSPECTIVA",
            "origen_piso": "NUEVO" if a["origen_numerico"] == "NUEVO" else a["origen_numerico"],
            "estado_adopcion": "ADOPTADO", "alcance": "PARAMETRO-DE-REGLA",
            "firma_fp": firma, "result_id": rid, "celda": "", "calc": calc,
            "oferta_exclusion": "", "reserva": a["tipo_uso"],
        }

    # ── S2 · marginales: piso t−1 adoptado (ENVIPE 2025) y con reserva de ancho (ENIF 2024)
    for m in marcador:
        if m["tipo"] != "MARGINAL" or m["estado"] != "EVALUADA" or not m["resultado_id"]:
            continue
        inst = m["instrumento"]
        piso_calc = m["piso_fuente"].split("/")[0]
        piso_rid = m["resultado_id"]
        if inst.startswith("ENIF 2024"):
            cel = re.sub(r"^RESULT-PISOS-ENIF2021-(V2|FORMALIDAD)-", "", piso_rid).removesuffix("-P")
            calc = "CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001"
            data = get(calc)[0]
            rid = f"RESULT-ENIFPIC-{cel}-PISO-P"
            lo, hi = f"RESULT-ENIFPIC-{cel}-IC-CALIBRADO-INF", f"RESULT-ENIFPIC-{cel}-IC-CALIBRADO-SUP"
            for k in (rid, lo, hi):
                if k not in data:
                    raise ValueError(f"marginal ENIF sin RESULT: {k}")
            firma, estado, ola, instr = MARG_ENIF, "ADOPTADO-CON-RESERVA-DE-ANCHO", "2024", "ENIF"
            nat = "IC-CALIBRADO-PERSISTENCIA (conservador: un solo choque 2018→2021)"
        elif inst.startswith("ENVIPE 2025"):
            calc, rid = piso_calc, piso_rid
            data = get(calc)[0]
            if rid not in data:
                raise ValueError(f"marginal ENVIPE sin RESULT: {rid}")
            lo, hi = related(data, rid, "INF"), related(data, rid, "SUP")
            firma, estado, ola, instr = MARG_ENVIPE, "ADOPTADO", "2025", "ENVIPE"
            nat = "IC95-MUESTRAL-DE-LA-OLA-T-1" if lo else "SIN-IC-IDENTIFICADO"
        else:
            fuera(m["resultado_id"], piso_calc, "MARGINAL-NO-ADOPTADA",
                  f"{inst.split(' · ')[0]}: sin adopción en nivel (veto o diferida)")
            continue
        rows[rid] = {
            "llave": rid, "dominio": DOMINIO_POR_REGLA.get(m["regla_o_eje_origen"].split(".")[0], "SIN-DOMINIO"),
            "instrumento": instr, "ola": ola, "conducta": m["regla_o_eje_origen"],
            "eje": m["eje_o_par"], "segmento": m["categoria"], "unidad": m["unidad_objetivo"],
            "punto": num(data[rid]), "ic95_inf": num(data[lo]) if lo else "",
            "ic95_sup": num(data[hi]) if hi else "", "naturaleza_ic": nat,
            "temporalidad": "RETROSPECTIVA", "origen_piso": "HEREDADO-DE-GEN2",
            "estado_adopcion": estado, "alcance": "ESTIMADOR-DE-CELDA", "firma_fp": firma,
            "result_id": rid, "celda": m["celda_id"], "calc": calc, "oferta_exclusion": "",
            "reserva": f"piso t−1 = {piso_rid}; ninguna frase lo llama cobertura",
        }

    # ── S3 · pisos por instrumento (Firma T): una fila por celda de la TABLA sellada
    for fp, calcs in ASTRA.items():
        if not str(fps.get(fp, "")).startswith("FIRMADA"):
            pend.append({"id": fp, "objeto": ";".join(calcs), "calc": "", "estado_fp": fps.get(fp, "AUSENTE"),
                         "nota": "Firma T no FIRMADA al abrir el acto"})
            continue
        for calc in calcs:
            data, _rh, _sh, spec = get(calc)
            dom = next(d for p, d in DOMINIO_POR_CALC if calc.startswith(p))
            for key in [k for k in data if k.endswith("-TABLA")]:
                for i, c in enumerate(tabla(data, key)):
                    llave = f"{key}#{i}"
                    if calc.startswith("CALC-ENOE-"):
                        ola, conducta, eje, seg = c["ola"], c["conducta"], c["eje"], c["segmento"]
                        p, lo, hi, est = c["punto"], c["ic95_lo"], c["ic95_hi"], "ESTIMABLE"
                        instr, unidad, res = "ENOE", c["unidad"], f"calidad={c['calidad']}"
                    elif calc.startswith("CALC-ENDIREH-"):
                        ola = re.search(r"-(20\d\d)-", calc).group(1)
                        conducta = c.get("resultado") or calc.split(f"-{ola}-")[1].rsplit("-", 1)[0].lower()
                        eje, seg, est = c["eje"], str(c["categoria"]), c["estado"]
                        p = c.get("p")
                        lo, hi = (c.get("ic95") or [None, None])
                        instr, unidad = "ENDIREH", "proporcion"
                        res = f"ventana={c.get('ventana', '')}"
                    else:
                        ola = re.search(r"-(20\d\d)-", calc).group(1)
                        conducta, seg, est = c["medida"], c["dominio"], c["estado"]
                        eje = seg.split("_", 1)[0]
                        p = c.get("punto")
                        lo, hi = (c.get("ic95") or [None, None])
                        instr, unidad = calc.split("-")[1], "proporcion"
                        res = "sin uso predictivo"
                        if calc.startswith("CALC-ENDUTIH-PISOS-") and conducta == "actividad_empleo":
                            fuera(llave, calc, "EXCLUIDA-POR-FIRMA",
                                  "celda original de empleo; la sustituye CALC-ENDUTIH-EMPLEO-15MAS", fp)
                            continue
                    if est not in ("ESTIMABLE", "PUBLICABLE") or p is None:
                        fuera(llave, calc, f"CELDA-{est}", "sin punto publicable en el CALC", fp)
                        continue
                    rows[llave] = {
                        "llave": llave, "dominio": dom, "instrumento": instr, "ola": str(ola),
                        "conducta": conducta, "eje": eje, "segmento": seg, "unidad": unidad,
                        "punto": num(p), "ic95_inf": num(lo), "ic95_sup": num(hi),
                        "naturaleza_ic": "IC95-DE-DISENO" if lo is not None else "SIN-IC-IDENTIFICADO",
                        "temporalidad": "RETROSPECTIVA", "origen_piso": "NUEVO",
                        "estado_adopcion": "ADOPTADO", "alcance": "DESCRIPTIVO-DE-OLA",
                        "firma_fp": fp, "result_id": key, "celda": str(i), "calc": calc,
                        "oferta_exclusion": "", "reserva": "piso retrospectivo; " + res,
                    }

    # ── S4 · bloque ENIGH (Firma M): descriptores de remesas con punto e IC sellados
    for a in (2016, 2018, 2020):
        calc = f"CALC-ENIGH{a}-INTENSIDAD-REMESAS-0001"
        firma = f"decisiones.tsv:{calc}"
        if calc not in dec:
            raise ValueError(f"Firma M sin fila en decisiones: {calc}")
        data, _rh, _sh, spec = get(calc)
        for med in ENIGH_MEDIDAS:
            rid = f"RESULT-ENIGH{str(a)[-2:]}-REMINT-{med}"
            lo, hi = f"{rid}-IC-LO", f"{rid}-IC-HI"
            has = lo in data and hi in data
            rows[rid] = {
                "llave": rid, "dominio": "FAMILIA_CUIDADOS", "instrumento": "ENIGH",
                "ola": str(a), "conducta": med.lower().replace("-", "_") + "_remesas",
                "eje": "nacional", "segmento": "hogares" if med == "PREVALENCIA" else "hogares receptores",
                "unidad": "pesos" if "REMESAS-" in med else "proporcion",
                "punto": num(data[rid]), "ic95_inf": num(data[lo]) if has else "",
                "ic95_sup": num(data[hi]) if has else "",
                "naturaleza_ic": "IC95-BOOTSTRAP-UPM-EN-ESTRATO" if has else "SIN-IC-IDENTIFICADO",
                "temporalidad": "RETROSPECTIVA", "origen_piso": "NUEVO",
                "estado_adopcion": "ADOPTADO", "alcance": "DESCRIPTIVO-DE-OLA", "firma_fp": firma,
                "result_id": rid, "celda": "", "calc": calc, "oferta_exclusion": "",
                "reserva": "describe hogares e ingreso por remesas; no mide gasto ni efecto causal",
            }
    for a in (2016, 2018, 2020):
        for tipo in ("PERFIL-ESTRUCTURAL", "REMESAS-CONTEXTO"):
            fuera(f"CALC-ENIGH{a}-{tipo}-0001", f"CALC-ENIGH{a}-{tipo}-0001", "ADOPTADO-TABLA-NO-DESAGREGADA",
                  "tabla JSON adoptada por Firma M; su desagregación por celda no entra en v1.4 (NC-260927-GEN2-CIERRE-SEMANAL-2-facd-01, re-diferida por GEN2-CIERRE-Y-PRODUCTO-3)", f"decisiones.tsv:CALC-ENIGH{a}-{tipo}-0001")
    fuera("CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001", "CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001", "EVALUACION-NO-ESTIMADOR",
          "mide error de candidatos (MAE, cobertura), no una conducta", "decisiones.tsv:CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001")

    # ── S5 · pisos de salud y bienestar (FIRMAS-16: FP 6d56-01..03)
    for fp, calc, dom, instr, estado in FIRMAS16_PISOS:
        if not str(fps.get(fp, "")).startswith("FIRMADA"):
            continue
        data = get(calc)[0]
        pref = calc.removeprefix("CALC-").removesuffix("-0001")
        for rid in [k for k in data if k.endswith("-P")]:
            m = re.match(rf"RESULT-{pref}-(.+)-(20\d\d)-([A-Z]+)-(.+)-P$", rid)
            if not m or data[rid] is None:
                continue
            conducta, ola, eje, seg = m.group(1).lower(), m.group(2), m.group(3), m.group(4)
            base = rid.removesuffix("-P")
            cal = f"{base}-ICC-LO" in data and data.get(f"{base}-ICC-LO") is not None
            lo, hi = (f"{base}-ICC-LO", f"{base}-ICC-HI") if cal else (f"{base}-IC-LO", f"{base}-IC-HI")
            has = lo in data and hi in data and data[lo] is not None
            rows[rid] = {
                "llave": rid, "dominio": dom, "instrumento": instr, "ola": ola,
                "conducta": conducta, "eje": eje, "segmento": seg, "unidad": "proporcion",
                "punto": num(data[rid]), "ic95_inf": num(data[lo]) if has else "",
                "ic95_sup": num(data[hi]) if has else "",
                "naturaleza_ic": ("IC-CALIBRADO-PERSISTENCIA" if cal else "IC95-DE-DISENO") if has else "SIN-IC-IDENTIFICADO",
                "temporalidad": "RETROSPECTIVA", "origen_piso": "NUEVO",
                "estado_adopcion": estado, "alcance": "DESCRIPTIVO-DE-OLA", "firma_fp": fp,
                "result_id": rid, "celda": "", "calc": calc, "oferta_exclusion": "",
                "reserva": "piso retrospectivo; sin uso predictivo",
            }

    # ── S6 · eje NSE AMAI (FIRMAS-16: FP e773-01, con reserva de instrumento)
    if str(fps.get(FP_NSE, "")).startswith("FIRMADA"):
        for r in lee(ROOT / "forense/analisis/clase-amai/pisos-nse-v1_0.tsv"):
            clave = (r["instrumento"], r["ola"])
            if clave not in NSE_ADMITIDO:
                fuera(r["result_punto"], r["calc"], "NSE-FUERA-DE-RESERVA-DE-INSTRUMENTO",
                      f"{r['instrumento']} {r['ola']}: fuera por la letra de la firma", FP_NSE)
                continue
            if r["estado"] != "PUBLICABLE":
                fuera(r["result_punto"], r["calc"], f"CELDA-{r['estado']}", "sin punto publicable", FP_NSE)
                continue
            data = get(r["calc"])[0]
            rid = r["result_punto"]
            if rid not in data or float(data[rid]) != float(r["punto"]):
                raise ValueError(f"piso NSE no coincide con su CALC: {rid}")
            base = rid.removesuffix("-P")
            lo = next((k for k in (f"{base}-IC-LO", f"{base}-IC95-INF") if k in data), "")
            hi = next((k for k in (f"{base}-IC-HI", f"{base}-IC95-SUP") if k in data), "")
            rows[rid] = {
                "llave": rid, "dominio": NSE_DOMINIO[r["instrumento"]], "instrumento": r["instrumento"],
                "ola": r["ola"], "conducta": r["conducta"], "eje": "NSE", "segmento": r["grupo_nse"],
                "unidad": r["unidad"], "punto": num(data[rid]),
                "ic95_inf": num(data[lo]) if lo else "", "ic95_sup": num(data[hi]) if hi else "",
                "naturaleza_ic": "IC95-DE-DISENO" if lo else "SIN-IC-IDENTIFICADO",
                "temporalidad": "RETROSPECTIVA", "origen_piso": "NUEVO",
                "estado_adopcion": "ADOPTADO", "alcance": "DESCRIPTIVO-DE-OLA", "firma_fp": FP_NSE,
                "result_id": rid, "celda": "", "calc": r["calc"], "oferta_exclusion": "",
                "reserva": "eje NSE con reserva de instrumento; " + NSE_ADMITIDO[clave],
            }

    # ── S7 · pisos por instrumento de FIRMAS-19 (J1, J2, J4–J10; J3 = veto de filas de -0001)
    j3 = fps.get(FP_J3, "AUSENTE")
    if not j3.startswith("FIRMADA"):
        pend.append({"id": FP_J3, "objeto": "CALC-ENIGH-CONSUMO-PISOS-0001", "calc": "", "estado_fp": j3,
                     "nota": "veto J3 no FIRMADO: J1 no entra"})
    for fp, calc, dom, instr, estado, reserva in FIRMAS19_PISOS:
        est_fp = fps.get(fp, "AUSENTE")
        if not est_fp.startswith("FIRMADA") or (calc == "CALC-ENIGH-CONSUMO-PISOS-0002" and not j3.startswith("FIRMADA")):
            pend.append({"id": fp, "objeto": calc, "calc": calc, "estado_fp": est_fp,
                         "nota": "FIRMAS-19 no FIRMADA al abrir el acto: no entra"})
            continue
        data = get(calc)[0]
        for rid in [k for k in data if k.endswith("-P")]:
            m = re.match(re.escape(PREFIJO_RESULT[calc]) + r"([A-Z0-9-]+?)-((?:19|20)\d\d)-([A-Z0-9-]+)-P$", rid)
            if not m:
                raise ValueError(f"llave RESULT sin forma conducta-ola-eje: {rid}")
            if data[rid] is None:
                fuera(rid, calc, "CELDA-SIN-PUNTO", "punto nulo en el CALC sellado", fp)
                continue
            base = rid.removesuffix("-P")
            conducta, ola, resto = m.group(1), m.group(2), m.group(3)
            eje = next((e for e in EJES_COMPUESTOS if resto.startswith(e + "-")), resto.split("-")[0])
            seg = resto[len(eje) + 1:] or resto
            cal = data.get(f"{base}-ICC-LO") is not None
            lo, hi = (f"{base}-ICC-LO", f"{base}-ICC-HI") if cal else (f"{base}-IC-LO", f"{base}-IC-HI")
            has = data.get(lo) is not None and data.get(hi) is not None
            d = "RELIGIOSIDAD" if dom == "CONFIANZA" and RELIG_RE.search(conducta) else dom
            rows[rid] = {
                "llave": rid, "dominio": d, "instrumento": instr, "ola": ola,
                "conducta": conducta.lower(), "eje": eje, "segmento": seg,
                "unidad": "proporcion (hogar)" if instr in ("ENIGH", "ENGASTO") else "proporcion",
                "punto": num(data[rid]), "ic95_inf": num(data[lo]) if has else "",
                "ic95_sup": num(data[hi]) if has else "",
                "naturaleza_ic": ("IC-CALIBRADO-PERSISTENCIA" if cal else "IC95-DE-DISENO") if has else "SIN-IC-IDENTIFICADO",
                "temporalidad": "RETROSPECTIVA", "origen_piso": "NUEVO",
                "estado_adopcion": estado, "alcance": "DESCRIPTIVO-DE-OLA", "firma_fp": fp,
                "result_id": rid, "celda": "", "calc": calc, "oferta_exclusion": "",
                "reserva": "piso retrospectivo; sin uso predictivo; " + reserva,
            }

    # ── S8 · pisos por instrumento de FIRMAS-20 (A1–A6) y veto de Intercensal 2015
    for fp, calc, pref, dom, instr, estado, unidad, reserva in FIRMAS20_PISOS:
        est_fp = fps.get(fp, "AUSENTE")
        if not est_fp.startswith("FIRMADA"):
            pend.append({"id": fp, "objeto": calc, "calc": calc, "estado_fp": est_fp,
                         "nota": "FIRMAS-20 no FIRMADA al abrir el acto: no entra"})
            continue
        data = get(calc)[0]
        olas = sorted({m.group("o") for k in data if k.endswith("-P") and k.startswith(pref)
                       for m in [RX_A20.match(k[len(pref):])] if m})
        for rid in [k for k in data if k.endswith("-P")]:
            m = RX_A20.match(rid[len(pref):]) if rid.startswith(pref) else None
            if not m:
                raise ValueError(f"llave RESULT sin forma conducta-ola-eje: {rid}")
            if data[rid] is None:
                fuera(rid, calc, "CELDA-SIN-PUNTO", "punto nulo en el CALC sellado", fp)
                continue
            base = rid.removesuffix("-P")
            conducta, ola, resto = m.group("c"), m.group("o"), m.group("r")
            eje = next((e for e in EJES_A20 if resto.startswith(e + "-")), resto.split("-")[0])
            seg = resto[len(eje) + 1:] or resto
            # IC calibrado de persistencia: por celda (…-ICC-*) o sobre la última ola (llave sin ola).
            sin_ola = pref + conducta + "-" + resto
            cands = [(f"{base}-ICC-LO", f"{base}-ICC-HI")]
            if ola == olas[-1]:
                cands.append((f"{sin_ola}-ICC-LO", f"{sin_ola}-ICC-HI"))
            cal = next(((lo, hi) for lo, hi in cands if data.get(lo) is not None and data.get(hi) is not None), None)
            lo, hi = cal or (f"{base}-IC-LO", f"{base}-IC-HI")
            has = data.get(lo) is not None and data.get(hi) is not None
            rows[rid] = {
                "llave": rid, "dominio": dom, "instrumento": instr, "ola": ola,
                "conducta": conducta.lower(), "eje": eje, "segmento": seg, "unidad": unidad,
                "punto": num(data[rid]), "ic95_inf": num(data[lo]) if has else "",
                "ic95_sup": num(data[hi]) if has else "",
                "naturaleza_ic": ("IC-CALIBRADO-PERSISTENCIA" if cal else "IC95-DE-DISENO") if has
                else "SIN-IC-IDENTIFICADO",
                "temporalidad": "RETROSPECTIVA", "origen_piso": "NUEVO",
                "estado_adopcion": estado, "alcance": "DESCRIPTIVO-DE-OLA", "firma_fp": fp,
                "result_id": rid, "celda": "", "calc": calc, "oferta_exclusion": "",
                "reserva": "piso retrospectivo; sin uso predictivo; " + reserva,
            }
    vetos = {r["objeto"] for r in lee(CORRIDA / "decisiones.tsv")
             if r["decision"].startswith("adopcion=VETADA-POR-DECISION")}
    for fp, calc in FIRMAS20_VETADOS:
        data = get(calc)[0]
        for rid in [k for k in data if k.endswith("-P")]:
            if rid not in vetos:
                raise ValueError(f"veto firmado sin fila en decisiones.tsv: {rid}")
            fuera(rid, calc, "VETADO-POR-FIRMA", "Intercensal 2015: payload solo Estado de México (FIRMAS-20 A6)", fp)

    semana(rows, fuera, get)

    for fp, objeto in FP_ADOPCION_EN_CURSO:
        est_fp = fps.get(fp, "AUSENTE")
        if not est_fp.startswith("FIRMADA"):
            pend.append({"id": fp, "objeto": objeto, "calc": "", "estado_fp": est_fp,
                         "nota": "acto fusionado; FP de adopción no FIRMADA al cerrar: no entra (encargo §2)"})

    # ── oferta al lado de cada marginal de mercado (DINERO)
    # Sólo la serie que describe el texto de abajo (DIN-OFERTA-EXCLUSION-ENIF-spec-v1_0): un CALC nuevo con el
    # mismo prefijo no reescribe un catálogo publicado (GEN2-ASTRA6-C2-EJECUCION-1, oferta de cuenta ENIF 2024).
    oferta_olas = sorted(d.name[-9:-5] for d in CORRIDA.glob("CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001")
                         if "DIN-OFERTA-EXCLUSION-ENIF-spec-v1_0.md" in (d / "spec.yaml").read_text())
    for r in rows.values():
        if r["dominio"] == "DINERO":
            r["oferta_exclusion"] = (
                "SIN-MEDIDA-DE-OFERTA-SELLADA-PARA-ESTA-OLA-Y-CONDUCTA: exclusión por oferta sellada "
                f"solo para crédito ENIF {'/'.join(oferta_olas)} (CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001); "
                "oferta de cuenta ENIF 2024 sellada sin adoptar (CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001)")
        else:
            r["oferta_exclusion"] = "NO-APLICA"

    # ── pendientes de firma (FIRMAS-16 u otras FP ABIERTAS al abrir el acto)
    for fp in FIRMAS16:
        estado = fps.get(fp, "AUSENTE")
        if not estado.startswith("FIRMADA"):
            pend.append({"id": fp, "objeto": "pisos/eje del acto emisor", "calc": "",
                         "estado_fp": estado, "nota": "no entra a v1.4 (encargo §2)"})

    # ── beee-02 · rótulo de validación ciega (lote 1) por llave; suspender no es borrar
    for r in rows.values():
        r.setdefault("validacion_ciega", "")
        r.setdefault("sucesor", "")
    est_b = fps.get(FP_BEEE02, "AUSENTE")
    if not est_b.startswith("FIRMADA"):
        pend.append({"id": FP_BEEE02, "objeto": "7 PROPONER-SUSPENDER · 689 ACOTAR", "calc": "",
                     "estado_fp": est_b, "nota": "rótulo de validación ciega no FIRMADO: no se aplica"})
    else:
        for t in lee(RECIBO):
            r = rows.get(t["llave"])
            if r is None:
                raise ValueError(f"llave del recibo ausente del catálogo: {t['llave']}")
            rec = t["recomendacion"]
            if rec == "PROPONER-SUSPENDER":
                r["estado_adopcion"] = "SUSPENDIDA-POR-FIRMA"
                r["validacion_ciega"] = f"SUSPENDIDA:{t['componente']}:{t['estado_recibo']}"
                r["sucesor"] = SUCESOR_SUSPENDIDAS
            elif rec == "ACOTAR":
                r["validacion_ciega"] = ROTULO_ACOTAR[t["efecto"]] + (
                    f" (delta_punto={t['delta_punto']})" if t["delta_punto"] else
                    f" (margen_publicabilidad={t['margen_publicabilidad']}; banda_mc={t['banda_mc']})")
            else:
                r["validacion_ciega"] = rec
            r["reserva"] += f"; validación ciega lote 1: {FP_BEEE02}"

    lote3(rows, fps, pend)

    # ── toda ADOPCION POR INSTRUMENTO FIRMADA debe estar cableada (encargo §1: se deriva del TSV de firmas)
    firmas_en = {r["firma_fp"] for r in rows.values()} | {e["firma"] for e in excl}
    for r in lee(ROOT / "forense/firmas-pendientes.tsv"):
        if (r["qué_se_firma"].startswith("ADOPCION POR INSTRUMENTO") and r["estado"].startswith("FIRMADA")
                and r["id"] not in firmas_en):
            pend.append({"id": r["id"], "objeto": r["gatea"][:80], "calc": "", "estado_fp": r["estado"],
                         "nota": "ADOPCION FIRMADA sin sección en el generador: no entra (se lista)"})

    lista = sorted(rows.values(), key=lambda r: r["llave"])
    for r in lista:
        for k in ("punto", "ic95_inf", "ic95_sup"):
            if r[k] and not re.fullmatch(r"-?[0-9.e+-]+", r[k]):
                raise ValueError(f"valor no numérico: {r['llave']} {k}={r[k]}")
            if r[k] in ("nan", "inf", "-inf"):
                raise ValueError(f"valor no finito: {r['llave']}")
    escribe(TSV, FIELDS, lista)
    calcs = sorted({r["calc"] for r in lista})
    escribe(DIR / "calcs-v1_4.tsv", ["calc", "sha256_resultados", "sha256_sello", "filas"],
            [{"calc": c, "sha256_resultados": get(c)[1], "sha256_sello": get(c)[2],
              "filas": sum(1 for r in lista if r["calc"] == c)} for c in calcs])
    escribe(DIR / "excluidos-v1_4.tsv", ["llave", "calc", "causa", "firma", "nota"], excl)
    escribe(DIR / "pendientes-de-firma-v1_4.tsv", ["id", "objeto", "calc", "estado_fp", "nota"], pend)
    cob = cobertura(lista, get)
    conteos(lista, excl, pend, cob)
    render()
    print(f"estimadores={len(lista)} calcs={len(calcs)} excluidos={len(excl)} pendientes={len(pend)}")


# ── v1.4 · S9–S12: sellado del 27–28/sep, adopción por bloque (merge de mesa, E.2) ──────────────
FIRMA_BLOQUE = "MERGE-DE-MESA:GEN2-CIERRE-Y-PRODUCTO-3"
BLOQUE = DIR / "bloque-adopcion-cifras-v1_4.tsv"
REGISTRO_SEMANA = DIR / "registro-semana-v1_4.tsv"
# (calc, dominio, instrumento, unidad, propuesta, alcance, reserva). Dominio: PROPUESTO-POR-EJECUTOR,
# leído de la nota del acto emisor (PISOS-DOMINIOS-Y-REGLAS-1 §tabla; CALC-ALTERNOS-LOTE-1 etiquetas.dominio).
_P = "PISO-DESCRIPTIVO-DE-OLA"
_M = "CONTRASTE-DE-MOMENTO"
SEMANA = (
    ("CALC-ENCIG2023-CONFIANZA-PISOS-0001", "CONFIANZA", "ENCIG", "proporcion (persona 18+, ciudades de 100 000+)",
     _RES, _P, "PISOS-Y-ADENDAS-1 H4: escala de 4 puntos, no se enlaza con otras escalas; ENCIG 2025 no se abrió"),
    ("CALC-PDR1-ENCUCI2020-0002", "AUTORIDAD", "ENCUCI", "proporcion (persona)", _RES, _P,
     "PDR1: sucede a -0001 (descartado por VALOR-LARGO); una ola"),
    ("CALC-PDR1-ENSU2024-0001", "SANCION_SOCIAL", "ENSU", "proporcion (persona 18+ urbana)", _RES, _P,
     "PDR1: 2024T1; una ola"),
    ("CALC-PDR1-ENUT2024-0001", "TIEMPO", "ENUT", "proporcion (persona)", _RES, _P,
     "PDR1: TIME-002/VEJEZ-009 no reproducen el report; contrastes rural/indígena van a RURAL_INDIGENA"),
    ("CALC-PDR1-ENADID2023-0001", "RURAL_INDIGENA", "ENADID", "diferencia de proporciones (persona)", _RES, _P,
     "PDR1: brecha de TEC-010; 19 % / 24.2 % del report no reproducen"),
    ("CALC-PDR1-ENIGH2022-0001", "CONOCIMIENTO", "ENIGH", "proporcion (hogar)", _RES, _P,
     "PDR1: colegiatura privada por decil; unidad HOGAR"),
    ("CALC-PDR1-ENVIPE2025-0001", "CAPITAL_SOCIAL", "ENVIPE", "proporcion (persona; estrato del área)", _RES, _P,
     "PDR1: RG-b913 solo mitad observable; la mitad «crisis» es NO-CONSTRUIBLE"),
    ("CALC-ALT-M05-LAPOP2019-0001", "POLITICA", "LAPOP", "proporcion (persona)", _RES, _M,
     "ALT: el contraste cubre 0; no hace serie con 2021 (cambio de modo)"),
    ("CALC-ALT-M05-LAPOP2021-0001", "POLITICA", "LAPOP", "proporcion (persona)", _RES, _M,
     "ALT: BAJO−ALTO cubre 0, no corrobora; COMMIT-1-bis por VALOR-LARGO"),
    ("CALC-ALT-M13-CIDECSES2015-0001", "POLITICA", "CIDE-CSES", "proporcion (persona)", _RES, _M,
     "ALT: p17/p18 NO-ESTIMABLE (n=0)"),
    ("CALC-ALT-M19-ENCUCI2020-0001", "CONFIANZA", "ENCUCI", "proporcion (persona)", _RES, _M,
     "ALT: reserva de método común"),
    ("CALC-ALT-M19-WVS2018-REPRO-0001", "CONFIANZA", "WVS", "proporcion (persona)", _RES, _M,
     "ALT: reproduce el abridor GEN1 de RES-0194 (reproducir no es validar)"),
    ("CALC-ALT-M22-ENVIPE2025-0001", "VIOLENCIA", "ENVIPE", "proporcion (delito)", _RES, _M,
     "ALT: unidad DELITO, no persona; no se promedia con cifras de persona"),
    ("CALC-ALT-M23-ENSAFI2023-0001", "DINERO", "ENSAFI", "proporcion (persona)", _RES, _M,
     "ALT: ahorro solo informal por tamaño de localidad"),
    ("CALC-ALT-R03-ENCRIGE2020-0001", "CONFIANZA", "ENCRIGE", "proporcion (empresa)", _RES, _M,
     "ALT: tabulados oficiales, sin IC ni n muestral; unidad EMPRESA"),
    ("CALC-ALT-R03-ENVE2024-0001", "CONFIANZA", "ENVE", "proporcion (unidad económica)", _RES, _M,
     "ALT: tabulados oficiales, sin IC ni n muestral; unidad ECONÓMICA"),
)
# Sellados de la semana que no son estimador de conducta: fuera, rotulados.
SEMANA_FUERA = (
    ("CALC-PISO-PERSISTENCIA-ERROR-0002", "EVALUACION-NO-ESTIMADOR",
     "mide error del piso contra constancia (RETROSPECTIVA-MECÁNICA); FP-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-01 ABIERTA"),
    ("CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001", "MEDIDA-DE-OFERTA-NO-ESTIMADOR",
     "exclusión por oferta de cuenta ENIF 2024 (etiqueta adopta=NO); se cita en `oferta_exclusion` de las filas DINERO"),
)
RURAL_RE = re.compile(r"RURAL|INDIG|-IND-|HABL")
ESTADOS_OK = {"ESTIMADA", "EXTRAIDA", "ESTIMABLE", "PUBLICABLE"}


def _es_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _ic_de(data: dict, k: str):
    """(base, lo, hi) si k es un punto con par de IC hermano; (base, None, None) si es -P sin IC; None si no es punto."""
    for suf, pares in (("-PP", (("-LO", "-HI"),)), ("-P", (("-IC-LO", "-IC-HI"), ("-IC95-INF", "-IC95-SUP"),
                                                         ("-IC95INF", "-IC95SUP"), ("-ICC-LO", "-ICC-HI"))),
                       ("", (("-IC95-INF", "-IC95-SUP"), ("-IC95INF", "-IC95SUP"), ("-IC-LO", "-IC-HI")))):
        if suf and not k.endswith(suf):
            continue
        b = k[: len(k) - len(suf)] if suf else k
        for a, z in pares:
            if _es_num(data.get(b + a)) and _es_num(data.get(b + z)):
                return b, b + a, b + z
        if suf == "-P":
            return b, None, None
    return None


def _ref(data: dict, key: str):
    v = data[key]
    if isinstance(v, str) and v.startswith("REF:"):
        ruta, _, h = v[4:].partition("#sha256:")
        raw = (ROOT / ruta).read_bytes()
        if hashlib.sha256(raw).hexdigest() != h:
            raise ValueError(f"tabla REF con hash discordante: {ruta}")
        return json.loads(raw)
    return json.loads(v) if isinstance(v, str) else v


def _camina(nodo, ruta=()):
    if isinstance(nodo, dict):
        num_ = nodo.get("diferencia") if "diferencia" in nodo else nodo.get("p")
        if ("diferencia" in nodo or "p" in nodo) and not any(isinstance(x, dict) for x in nodo.values()):
            yield ruta, nodo, num_
            return
        for k, v in nodo.items():
            if not str(k).startswith("_"):
                yield from _camina(v, ruta + (str(k),))


def semana(rows: dict, fuera, get) -> None:
    """S9–S12. Solo entra lo que el registro derivado del commit ve SELLADA con cuenta_gen2=SI."""
    reg = {r["spec_id"]: r for r in lee(REGISTRO_SEMANA)}
    bloque = []
    for calc, dom, instr, unidad, prop, alcance, reserva in SEMANA:
        r = reg.get(calc)
        if not r or not r["estado"].startswith("SELLADA") or r["cuenta_gen2"] != "SI":
            fuera(calc, calc, "SELLADA-EN-DISCO-NO-REGISTRADA", "sin fila SELLADA/cuenta_gen2=SI en el registro del commit")
            continue
        data, _rh, _sh, spec = get(calc)
        et = spec.get("etiquetas", {}) or {}
        hold = str(et.get("holdout_gastado", "")) if alcance == _M else ""
        ola = str(et.get("ola", "") or "")
        m = re.search(r"(19|20)\d\d", ola) or re.search(r"(19|20)\d\d", calc)
        ola = m.group(0)
        n = 0
        base = dict(dominio=dom, instrumento=instr, ola=ola, unidad=unidad, temporalidad="RETROSPECTIVA",
                    origen_piso="NUEVO", estado_adopcion=prop, alcance=alcance, firma_fp=FIRMA_BLOQUE,
                    calc=calc, oferta_exclusion="", holdout_gastado=hold,
                    reserva=f"propuesto por instrumento en el bloque v1.4; {reserva}")
        if alcance == _P:
            pref = f"RESULT-{calc.removeprefix('CALC-').rsplit('-', 1)[0].replace('-CONFIANZA-PISOS', '-CONF')}-"
            for k in sorted(data):
                v = data[k]
                if not _es_num(v) or re.search(r"-(N|EE|SE|IC-LO|IC-HI|IC95-INF|IC95-SUP|IC95INF|IC95SUP|LO|HI|ICC-LO|ICC-HI)$", k):
                    continue
                ic = _ic_de(data, k)
                if ic is None:
                    continue
                b, lo, hi = ic
                resto = b.removeprefix(pref)
                partes = resto.split("-")
                d = "RURAL_INDIGENA" if dom == "TIEMPO" and RURAL_RE.search(resto) else dom
                rows[k] = {**base, "llave": k, "dominio": d, "conducta": partes[0].lower(),
                           "eje": partes[1] if len(partes) > 1 else "NACIONAL",
                           "segmento": "-".join(partes[2:]) or partes[-1],
                           "punto": num(v), "ic95_inf": num(data[lo]) if lo else "", "ic95_sup": num(data[hi]) if hi else "",
                           "naturaleza_ic": "IC95-DE-SPEC" if lo else "SIN-IC-IDENTIFICADO", "result_id": k, "celda": ""}
                n += 1
        else:
            for key in [k for k in data if k.endswith("-TABLA")]:
                for ruta, nodo, val in _camina(_ref(data, key)):
                    llave = f"{key}#{'/'.join(ruta)}"
                    est = str(nodo.get("estado", "ESTIMADA"))
                    if est not in ESTADOS_OK or not _es_num(val):
                        fuera(llave, calc, f"CELDA-{est}", "sin punto en la tabla sellada", FIRMA_BLOQUE)
                        continue
                    ic = nodo.get("ic95") or [nodo.get("ic95_lo"), nodo.get("ic95_hi")]
                    lo, hi = (ic + [None, None])[:2] if isinstance(ic, list) else (None, None)
                    rows[llave] = {**base, "llave": llave, "conducta": ruta[0].removeprefix("CONTRASTE:").lower(),
                                   "eje": "CONTRASTE" if "diferencia" in nodo else (ruta[1] if len(ruta) > 2 else "NACIONAL"),
                                   "segmento": "/".join(ruta[1:]) or "NACIONAL", "punto": num(val),
                                   "ic95_inf": num(lo) if _es_num(lo) else "", "ic95_sup": num(hi) if _es_num(hi) else "",
                                   "naturaleza_ic": "IC95-DE-SPEC" if _es_num(lo) else "SIN-IC-IDENTIFICADO",
                                   "result_id": key, "celda": "/".join(ruta)}
                    n += 1
        bloque.append({"calc": calc, "instrumento": instr, "ola": ola, "dominio": dom, "unidad": unidad,
                       "propuesta": "ADOPTAR" if prop == "ADOPTADO" else "CON-RESERVA-DE-ANCHO",
                       "alcance": alcance, "holdout_gastado": hold, "filas": n,
                       "registro": f"{r['estado']} · cuenta_gen2={r['cuenta_gen2']} · replay={r.get('resultado_replay', '')}",
                       "reserva": reserva})
    for calc, causa, nota in SEMANA_FUERA:
        fuera(calc, calc, causa, nota)
        bloque.append({"calc": calc, "instrumento": "", "ola": "", "dominio": "", "unidad": "", "propuesta": "NO-ENTRA",
                       "alcance": causa, "holdout_gastado": "", "filas": 0,
                       "registro": reg.get(calc, {}).get("estado", "AUSENTE"), "reserva": nota})
    escribe(BLOQUE, list(bloque[0].keys()), bloque)


# ── lote 3 de validación ciega (C1-SUCESORES-Y-LOTE-3, dictamen-lote3-v1_1.tsv) ─────────────
LOTE3 = ROOT / "forense/validacion-independiente/catalogo-1-lote3/dictamen-lote3-v1_1.tsv"
R21 = ROOT / "forense/validacion-independiente/catalogo-1-sucesores/r21-envipe-15-llaves.tsv"
FP_FB50 = "FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02"
FP_0C1F = "FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01"


def lote3(rows: dict, fps: dict, pend: list) -> None:
    for r in rows.values():
        r.setdefault("validacion_ciega_lote3", "")
        r.setdefault("holdout_gastado", "")
    for t in lee(LOTE3):
        r = rows.get(t["llave"])
        if r is None:
            raise ValueError(f"llave del lote 3 ausente del catálogo: {t['llave']}")
        punto = t["punto"].split(" ")[0].upper()
        rot = f"LOTE3:{t['dictamen']}:punto={punto}:ic={t['ic'].split(' ')[0].upper() or 'NO-COMPARADO'}"
        if t["dictamen"] == "ACOTAR":
            if "EDAD=98" in t["motivo"] and t["instrumento"] == "ENDIREH":
                est = fps.get(FP_0C1F, "AUSENTE").split(" ")[0]
                rot = f"ACOTADA-PROPUESTA:60+-INCLUYE-EDAD-98 ({FP_0C1F} {est}; merge del bloque)"
            else:
                rot = "ACOTADA:R26A-EXCLUYE-EDAD-98 (cambio de estimando firmado; sucesora --R26A)"
        r["validacion_ciega_lote3"] = rot
    est = fps.get(FP_FB50, "AUSENTE")
    for t in lee(R21):
        r = rows.get(t["llave_historica"])
        if r is None:
            raise ValueError(f"llave R21 ausente del catálogo: {t['llave_historica']}")
        if not est.startswith("FIRMADA"):
            pend.append({"id": FP_FB50, "objeto": t["llave_historica"], "calc": r["calc"], "estado_fp": est,
                         "nota": "R21 no FIRMADA: no se suspende"})
            continue
        r["estado_adopcion"] = "SUSPENDIDA-POR-FIRMA"
        r["validacion_ciega_lote3"] = f"SUSPENDIDA:{t['estado_c1']} ({FP_FB50}; R21)"
        r["sucesor"] = (f"CALC nuevo por llave: <{t['llave_sucesora_propuesta']}> "
                        f"(ola {t['ola_sucesora']}, unidad {t['unidad_sucesora']}); no se abre aquí")


# ── P3 · cobertura por report (los 31 de corpus/reports) ────────────────────
def cobertura(lista: list[dict], get: Calcs) -> list[dict]:
    reportes = sorted(p.name for p in (ROOT / "corpus/reports").glob("*.md"))
    rad = {pathlib.Path(r["ruta"]).name: r["dominio_primario"]
           for r in lee(ROOT / "forense/analisis/dominios/report-a-dominio-v1_0.tsv")}
    mapa = lee(ROOT / "canon/mapa-dominios-v1_1.tsv")
    medidos = Counter(r["dominio"] for r in lista)
    # CALC con cuenta_gen2=SI sellados en disco, por instrumento declarado en su nombre.
    gen2 = []
    for d in sorted(CORRIDA.glob("CALC-*")):
        s = d / "spec.yaml"
        if not (s.exists() and (d / "sello.json").exists()):
            continue
        txt = s.read_text()
        if re.search(r"cuenta_gen2:\s*['\"]?SI\b", txt):
            gen2.append(d.name)
    instr_dom = {
        "ENSANUT": "SALUD", "ENCODAT": "SALUD", "ENBIARE": "SALUD_MENTAL",
        "ENCUP": "POLITICA", "LAPOP": "POLITICA", "INE": "POLITICA", "NSE": "MOVILIDAD",
        "ENUT": "TIEMPO", "ENADID": "MIGRACION", "ENCUCI": "CAPITAL_SOCIAL",
    }
    en_med = Counter()
    for c in gen2:
        for ins, dom in instr_dom.items():
            if re.search(rf"(^|-){ins}(\d|-)", c.removeprefix("CALC-")):
                en_med[dom] += 1
    out = []
    for rep in reportes:
        dom = rad.get(rep, "SIN-MAPEO")
        af = [m for m in mapa if m["dominio"] == dom]
        dic = Counter(m["dictamen"] for m in af)
        if medidos[dom]:
            estado = "MEDIDO"
        elif en_med[dom]:
            estado = "EN-MEDICIÓN"
        elif dic["MEDIBLE-EN-CORPUS"]:
            estado = "MEDIBLE-EN-CORPUS-SIN-CALC"
        elif dic["MEDIBLE-CON-ADQUISICIÓN"]:
            estado = "MEDIBLE-CON-ADQUISICIÓN"
        elif af:
            estado = "NO-MEDIBLE-POR-DISEÑO"
        else:
            estado = "SIN-AFIRMACIONES-EN-MAPA"
        out.append({
            "report": rep, "dominio": dom, "estado": estado,
            "estimadores_v1_4": medidos[dom], "calc_gen2_sin_adoptar": en_med[dom],
            "afirmaciones": len(af), "medible_en_corpus": dic["MEDIBLE-EN-CORPUS"],
            "medible_con_adquisicion": dic["MEDIBLE-CON-ADQUISICIÓN"],
            "no_medible_por_diseno": dic["NO-MEDIBLE-POR-DISEÑO"],
        })
    escribe(DIR / "cobertura-31-v1_4.tsv", list(out[0].keys()), out)
    return out


def conteos(lista, excl, pend, cob) -> None:
    c: dict[str, object] = {}
    c["estimadores"] = len(lista)
    c["calcs"] = len({r["calc"] for r in lista})
    c["reports"] = len(cob)
    c["dominios_mapa"] = len({r["dominio"] for r in cob})
    for k in ("dominio", "instrumento", "estado_adopcion", "alcance", "temporalidad", "origen_piso"):
        for v, n in Counter(r[k] for r in lista).items():
            c[f"{k}:{v}"] = n
    for v, n in Counter(r["estado"] for r in cob).items():
        c[f"cobertura:{v}"] = n
    c["reports_medidos"] = sum(1 for r in cob if r["estado"] == "MEDIDO")
    c["dominios_medidos"] = len({r["dominio"] for r in cob if r["estado"] == "MEDIDO"})
    c["dominios_mapa_con_estimador"] = len({r["dominio"] for r in lista})
    for v, n in Counter(e["causa"] for e in excl).items():
        c[f"excluidos:{v}"] = n
    c["pendientes_de_firma"] = len(pend)
    c["firmas_citadas"] = len({r["firma_fp"] for r in lista})
    c["con_ic"] = sum(1 for r in lista if r["ic95_inf"])
    for v, n in Counter(r["validacion_ciega"].split(":")[0].split(" ")[0] for r in lista if r["validacion_ciega"]).items():
        c[f"vc:{v}"] = n
    c["vc:filas"] = sum(1 for r in lista if r["validacion_ciega"])
    for v, n in Counter(r["validacion_ciega"].split(" ")[0] for r in lista if r["validacion_ciega"].startswith("ACOTADA")).items():
        c[f"vc:{v}"] = n
    c["firmas20:filas"] = sum(1 for r in lista if r["calc"] in {f[1] for f in FIRMAS20_PISOS})
    c["firmas20:calcs"] = len({r["calc"] for r in lista if r["calc"] in {f[1] for f in FIRMAS20_PISOS}})
    # donde-cambio (P4): dictámenes por comando sobre la tabla del acto emisor
    dc = lee(ROOT / "forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv")
    c["dc:series"] = len(dc)
    for v, n in Counter(r["dictamen"] for r in dc).items():
        c[f"dc:{v}"] = n
    for v, n in Counter(r["direccion"] for r in dc if r["dictamen"] == "CAMBIO-SOSTENIDO").items():
        c[f"dc:CAMBIO-SOSTENIDO:{v or 'SIN-DIRECCION'}"] = n
    # clase (P4): pisos NSE del acto emisor, sin adoptar
    nse = lee(ROOT / "forense/analisis/clase-amai/pisos-nse-v1_0.tsv")
    c["nse:celdas"] = len(nse)
    c["celdas_validadas"], c["celdas_validadas_prospectiva"], c["celdas_validadas_retrospectiva"] = \
        _celdas_validadas()
    c["adoptados_activos"] = json.loads((DIR / "status-v1_4.json").read_text())["N_resultados_gen2_adoptados_activos"]
    (DIR / "conteos-v1_4.json").write_text(json.dumps(c, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


def _celdas_validadas() -> tuple[int, int, int]:
    """Definición vigente (`corrida0 status`), leída de su propia salida guardada."""
    p = DIR / "status-v1_4.json"
    if "--sin-registro" not in sys.argv or not p.exists():
        import corrida0 as c0  # noqa: PLC0415
        import contextlib  # noqa: PLC0415
        import io  # noqa: PLC0415
        with contextlib.redirect_stdout(io.StringIO()):
            s = c0.status(imprime=False)
        keep = {k: s[k] for k in ("celdas_validadas", "celdas_validadas_prospectiva",
                                  "celdas_validadas_retrospectiva", "celdas_validadas_definicion_desde", "N_corridas_selladas",
                                  "N_resultados_gen2_adoptados_activos")}
        p.write_text(json.dumps(keep, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    s = json.loads(p.read_text())
    return s["celdas_validadas"], s["celdas_validadas_prospectiva"], s["celdas_validadas_retrospectiva"]


def render() -> None:
    c = json.loads((DIR / "conteos-v1_4.json").read_text())
    tpl = (DIR / "plantilla-v1_4.md").read_text()
    get = Calcs()
    idx = {}
    for r in lee(TSV):
        idx[r["llave"]] = r

    def sub(m: re.Match) -> str:
        kind, key = m.group(1), m.group(2)
        if kind == "c":
            if key not in c:
                return "0" if key.split(":")[0] in ("cobertura", "excluidos", "dc") else _falta(key)
            v = c[key]
            return f"{v:,}".replace(",", " ") if isinstance(v, int) else str(v)
        r = idx.get(key)
        if not r:
            raise ValueError(f"RESULT no en catálogo: {key}")
        p = float(r["punto"])
        txt = f"{p:.3f}"
        if r["ic95_inf"]:
            txt += f" [{float(r['ic95_inf']):.3f}, {float(r['ic95_sup']):.3f}]"
        return txt

    def tab(m: re.Match) -> str:
        return TABLAS[m.group(1)]()

    out = re.sub(r"\{\{t:([a-z-]+)\}\}", tab, tpl)
    out = re.sub(r"\{\{([cr]):([^}]+)\}\}", sub, out)
    MD.write_text(out)


def _tabla_cobertura() -> str:
    rows = lee(DIR / "cobertura-31-v1_4.tsv")
    out = ["| report | dominio (mapa U0) | estado | estimadores v1.4 | CALC GEN2 sin adoptar | afirmaciones (en corpus / con adquisición / no medibles) |",
           "|---|---|---|---:|---:|---|"]
    for r in rows:
        nombre = r["report"].removesuffix(".md").replace("_", " ").strip()[:70]
        out.append(f"| {nombre} | `{r['dominio']}` | **{r['estado']}** | {r['estimadores_v1_4']} | "
                   f"{r['calc_gen2_sin_adoptar']} | {r['afirmaciones']} ({r['medible_en_corpus']} / "
                   f"{r['medible_con_adquisicion']} / {r['no_medible_por_diseno']}) |")
    return "\n".join(out)


def _tabla_dominios() -> str:
    rows = lee(TSV)
    c = Counter((r["dominio"], r["instrumento"]) for r in rows)
    firmas_ = {}
    for r in rows:
        firmas_.setdefault((r["dominio"], r["instrumento"]), set()).add(r["firma_fp"])
    out = ["| dominio | instrumento | estimadores | firmas citadas (ids distintos) |", "|---|---|---:|---:|"]
    for (d, i), n in sorted(c.items()):
        out.append(f"| `{d}` | {i} | {n:,} | {len(firmas_[(d, i)])} |".replace(",", " "))
    return "\n".join(out)


def _tabla_pendientes() -> str:
    rows = lee(DIR / "pendientes-de-firma-v1_4.tsv")
    out = ["| id | objeto | estado de la FP |", "|---|---|---|"]
    for r in rows:
        out.append(f"| `{r['id']}` | `{r['objeto']}` | {r['estado_fp'].split(' ')[0]} |")
    return "\n".join(out)


def _tabla_propuestas() -> str:
    """FP FIRMADA que «EJECUTA: GEN2-CATALOGO-V1-3-1» y no son adopción: propuestas recibidas, no reglas del catálogo."""
    out = ["| id | qué se recibe |", "|---|---|"]
    for r in lee(ROOT / "forense/firmas-pendientes.tsv"):
        if ("GEN2-CATALOGO-V1-3-1" in r["ejecutada_en"] and r["estado"].startswith("FIRMADA")
                and not r["qué_se_firma"].startswith("ADOPCION")):
            out.append(f"| `{r['id']}` | {r['gatea'][:90]} |")
    return "\n".join(out)


def _tabla_validacion() -> str:
    rows = lee(TSV)
    c = Counter((r["validacion_ciega"].split(" ")[0] or "SIN-VALIDACION-CIEGA", r["estado_adopcion"]) for r in rows)
    out = ["| rótulo de validación ciega (lote 1) | estado de adopción | filas |", "|---|---|---:|"]
    for (v, e), n in sorted(c.items()):
        out.append(f"| `{v}` | `{e}` | {n:,} |".replace(",", " "))
    return "\n".join(out)


TABLAS = {"cobertura": _tabla_cobertura, "dominios": _tabla_dominios, "pendientes": _tabla_pendientes,
          "propuestas": _tabla_propuestas, "validacion": _tabla_validacion}


def _falta(key: str) -> str:
    raise ValueError(f"conteo inexistente en conteos.json: {key}")


if __name__ == "__main__":
    main()
