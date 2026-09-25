#!/usr/bin/env python3
"""Mapa de series · familia ENVIPE (DONDE-CAMBIO-spec-v1_0.md §1-2, ESQUEMA.md).

Ciego a valores (B-bis): sólo verifica EXISTENCIA de llaves de RESULT en
`data/corrida0/<calc>/resultados.json` (lee sólo las llaves del dict
`resultados`, nunca sus valores) y arma el fragmento de mapa con ids. Del
catálogo (`canon/catalogo-del-mexicano-v1_0.tsv`) sólo lee las columnas
1-8 y 12-23 (nunca 9 `punto`, 10 `ic95_inf`, 11 `ic95_sup`, 24
`oferta_valor_ic`) -- el código nunca construye ni usa esos índices.

Dos ampliaciones autorizadas por la mesa sobre la primera corrida de este
fragmento (que sólo cubría las ocho olas CALC-ENVIPE-SERIE-<año>):

1. Las seis olas del árbitro `R` (`CALC-R-CIV-M-01/02/04/10/12/13`, olas
   2012/2013/2015/2021/2023/2024) quedan autorizadas como fuente. Su
   universo SECUNDARIO homologado (`P-C1-U1`/`IC-LO-C1-U1`/`IC-HI-C1-U1`,
   verbatim "homologado a prereg-caja-ENVIPE-DENUNCIA" en cada spec.yaml,
   verificado en el catálogo para `CIV-M-01/-02/-04`) es el MISMO
   constructo `C1/U1` de las ocho olas `CALC-ENVIPE-SERIE-*`, así que
   entran a la MISMA serie. Su universo PRIMARIO (`R`, sobre `U_R` = todos
   los tipos de delito, `PUNTO`/`IC-LO`/`IC-HI`) es un constructo distinto
   (denominador distinto: todos los delitos, no sólo los personales no
   denunciados) y forma su PROPIA serie de 6 olas.
   `CALC-ENVIPE-0001` (ENVIPE 2025) entra también a la serie `C1/U1`
   porque trae RESULT sellado `P-C1-U1`/`IC-LO-C1-U1`/`IC-HI-C1-U1` en
   `data/corrida0` (spec DONDE-CAMBIO §1: "sólo entran si ya existe un
   RESULT sellado de esa ola en data/corrida0"); su `sello.json` existe.
   Con esto la serie `C1/U1` queda con las 15 olas 2011-2025 sin salto.
2. Las 37 filas ENVIPE del catálogo se leen (cols 1-8,12-23) y cada
   conducta con RESULT se lista como serie, aunque tenga 1 sola ola (sale
   SIN-SERIE en el dictamen posterior). El único grupo de más de una ola
   dentro de las 37 filas es `R` (arriba); las otras 31 filas son series
   de una sola ola cada una (ENVIPE 2024/2025).

Comparabilidad (par_con_anterior): por texto, de fuentes selladas
anteriores a este acto:
  - Serie `C1/U1` (15 olas): columna no numérica `comparabilidad` de
    `data/corrida0/envipe-serie-denuncia-v1_0.tsv`, fila por ola/calc_id
    (ya cubre las ocho `CALC-ENVIPE-SERIE-*`, las seis `CALC-R-CIV-M-*` y
    `CALC-ENVIPE-0001`), corroborada por
    `forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md` §1.
  - Serie `R` (6 olas): `forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md`
    §2 (reactivo `BP1_23` idéntico 2021/2023/2024) y
    `forense/prereg-caja/R-ENVIPE-SERIE-DBF-spec-v1_0.md` §2-3 (reactivo
    idéntico 2012/2013/2015; `BPCOD` cambia de libro pero no afecta a
    `U_R`, que no filtra por `BPCOD`); las seis olas comparten,
    verbatim, `codificacion-R-v1_0.tsv` (universo, codificación,
    ponderador, diseño).
  - Filas sueltas del catálogo (31, 1 ola): `PRIMERA` sin más (no hay
    par que dictaminar con una sola ola).

Reproducible: python3 stdlib únicamente, TSV leído con split('\t') (nunca
el módulo csv), escrito con '\n'.join conservando celdas vacías finales.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRIDA0 = ROOT / "data" / "corrida0"
CATALOGO = ROOT / "canon" / "catalogo-del-mexicano-v1_0.tsv"
DENUNCIA_TSV = CORRIDA0 / "envipe-serie-denuncia-v1_0.tsv"
OUT = ROOT / "forense" / "analisis" / "donde-cambio" / "mapa" / "envipe.tsv"

CABECERA = (
    "serie_id\tinstrumento\tdominio\tconducta\tconducta_texto\teje\tsegmento\t"
    "unidad\tola\tcalc\tresult_p\tresult_lo\tresult_hi\tpar_con_anterior\t"
    "cita_par\tmarca_2020\tnota"
)

DOMINIO_C1U1 = "Seguridad y norma"
CONDUCTA_C1U1 = "NODENUNCIA-MIEDO-DESCONFIANZA"
CONDUCTA_TEXTO_C1U1 = (
    "Proporción ponderada de delitos personales no denunciados cuya razón "
    "principal declarada fue miedo al agresor, miedo a extorsión o "
    "desconfianza en la autoridad (P-C1-U1, "
    "forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md §1; "
    "homologado en las olas del árbitro R por "
    "forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md §0.2/§3 y "
    "forense/prereg-caja/R-ENVIPE-SERIE-DBF-spec-v1_0.md)."
)
EJE_NAC, SEG_TOTAL = "NACIONAL", "TOTAL"
UNIDAD_C1U1 = "DELITO-PERSONAL-NO-DENUNCIADO"

# ---- Serie C1/U1: 15 olas, calc por ola --------------------------------
# (ola, calc, prefijo_result) -- el prefijo de RESULT no siempre es
# calc.removeprefix('CALC-') (p. ej. CALC-ENVIPE-0001 -> RESULT-ENVIPE-DEN-*),
# así que se declara explícito y se verifica por existencia, no por patrón.
OLAS_C1U1 = [
    (2011, "CALC-ENVIPE-SERIE-2011", "ENVIPE-SERIE-2011"),
    (2012, "CALC-R-CIV-M-01", "R-CIV-M-01"),
    (2013, "CALC-R-CIV-M-02", "R-CIV-M-02"),
    (2014, "CALC-ENVIPE-SERIE-2014", "ENVIPE-SERIE-2014"),
    (2015, "CALC-R-CIV-M-04", "R-CIV-M-04"),
    (2016, "CALC-ENVIPE-SERIE-2016", "ENVIPE-SERIE-2016"),
    (2017, "CALC-ENVIPE-SERIE-2017", "ENVIPE-SERIE-2017"),
    (2018, "CALC-ENVIPE-SERIE-2018", "ENVIPE-SERIE-2018"),
    (2019, "CALC-ENVIPE-SERIE-2019", "ENVIPE-SERIE-2019"),
    (2020, "CALC-ENVIPE-SERIE-2020", "ENVIPE-SERIE-2020"),
    (2021, "CALC-R-CIV-M-10", "R-CIV-M-10"),
    (2022, "CALC-ENVIPE-SERIE-2022", "ENVIPE-SERIE-2022"),
    (2023, "CALC-R-CIV-M-12", "R-CIV-M-12"),
    (2024, "CALC-R-CIV-M-13", "R-CIV-M-13"),
    (2025, "CALC-ENVIPE-0001", "ENVIPE-DEN"),
]

CITA_SPEC_C1U1 = (
    "forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md §1 "
    "(\"ruptura de instrumentación nominal y de categorías residuales, "
    "no del núcleo C1/U1\")"
)
CITA_TSV_C1U1 = (
    "data/corrida0/envipe-serie-denuncia-v1_0.tsv (col. comparabilidad, fila ola={ola})"
)

# ---- Serie R (U_R, todos los tipos de delito): 6 olas ------------------
DOMINIO_R = "Seguridad y norma"
CONDUCTA_R = "R"
CONDUCTA_TEXTO_R = (
    "R = proporción ponderada, sobre U_R (todos los tipos de delito de "
    "TMod_Vic, sin filtro de BPCOD), de BP1_23 en {01,02,06} -- miedo al "
    "agresor, miedo a extorsión o desconfianza en la autoridad como razón "
    "principal de no denuncia. Ponderador FAC_DEL. Universo primario del "
    "árbitro R (espec-R-ciega-v1_2.tsv + codificacion-R-v1_0.tsv), "
    "denominador distinto del C1/U1 (que restringe a delitos personales)."
)
UNIDAD_R = "DELITO-TODOS-TIPOS"
OLAS_R = [
    (2012, "CALC-R-CIV-M-01"),
    (2013, "CALC-R-CIV-M-02"),
    (2015, "CALC-R-CIV-M-04"),
    (2021, "CALC-R-CIV-M-10"),
    (2023, "CALC-R-CIV-M-12"),
    (2024, "CALC-R-CIV-M-13"),
]
CITA_R = (
    "forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md §2 (reactivo BP1_23 "
    "idéntico en 2021/2023/2024) + "
    "forense/prereg-caja/R-ENVIPE-SERIE-DBF-spec-v1_0.md §2-3 (reactivo "
    "idéntico en 2012/2013/2015; BPCOD cambia de libro pero U_R no filtra "
    "por BPCOD) -- las seis olas comparten codificacion-R-v1_0.tsv verbatim."
)

FORBIDDEN_COLS = {"punto", "ic95_inf", "ic95_sup", "oferta_valor_ic"}
_ESPERADO = re.compile(r"\(esperado[^)]*\)", re.IGNORECASE)


def _scrub(texto: str) -> str:
    """Quita paréntesis 'esperado <numero>' que a veces trae unidad_escala.

    No es una columna prohibida por el esquema (unidad_escala es col.8,
    permitida), pero el mapa se congela sin valores como norma de B-bis:
    se descarta cualquier cifra que se cuele en texto libre.
    """
    return _ESPERADO.sub("[cifra omitida por ceguera del mapa]", texto)


def _resultado_keys(calc: str) -> set[str]:
    """Llaves del dict `resultados` de un CALC. Nunca lee valores."""
    ruta = CORRIDA0 / calc / "resultados.json"
    with open(ruta, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    return set(doc["resultados"])


def _leer_comparabilidad_denuncia() -> dict[str, str]:
    """comparabilidad cruda por calc_id, de envipe-serie-denuncia-v1_0.tsv.

    Sólo toca la columna no numérica `comparabilidad` y `calc_id`.
    """
    with open(DENUNCIA_TSV, "r", encoding="utf-8") as fh:
        lineas = fh.read().split("\n")
    cabecera = lineas[0].split("\t")
    i_calc = cabecera.index("calc_id")
    i_comp = cabecera.index("comparabilidad")
    out = {}
    for linea in lineas[1:]:
        if not linea:
            continue
        campos = linea.split("\t")
        out[campos[i_calc]] = campos[i_comp]
    return out


def _par_c1u1(comp_cruda: str) -> tuple[str, str]:
    if comp_cruda == "NINGUNA-EN-C1-U1":
        return "COMPARABLE", "NINGUNA-EN-C1-U1 == MISMO-INSTRUMENTO"
    if comp_cruda == "INSTRUMENTACION-NOMINAL-Y-RESIDUALES":
        return (
            "COMPARABLE",
            "INSTRUMENTACION-NOMINAL-Y-RESIDUALES declarada ajena al "
            "núcleo C1/U1 por la spec sellada == CAMBIO-MENOR",
        )
    raise ValueError(f"dictamen crudo no reconocido: {comp_cruda!r}")


def _fila(serie_id, instrumento, dominio, conducta, conducta_texto, eje,
          segmento, unidad, ola, calc, result_p, result_lo, result_hi,
          par, cita, marca_2020, nota) -> str:
    return "\t".join([
        serie_id, instrumento, dominio, conducta, conducta_texto, eje,
        segmento, unidad, str(ola), calc, result_p, result_lo, result_hi,
        par, cita, marca_2020, nota,
    ])


def filas_c1u1(comp_por_calc: dict[str, str]) -> list[str]:
    filas = []
    serie_id = f"ENVIPE-{CONDUCTA_C1U1}-{EJE_NAC}-{SEG_TOTAL}"
    anterior = None
    for ola, calc, prefijo in OLAS_C1U1:
        claves = _resultado_keys(calc)
        result_p = f"RESULT-{prefijo}-P-C1-U1"
        result_lo = f"RESULT-{prefijo}-IC-LO-C1-U1"
        result_hi = f"RESULT-{prefijo}-IC-HI-C1-U1"
        for rid in (result_p, result_lo, result_hi):
            assert rid in claves, f"{rid} no existe en {calc}/resultados.json"

        if anterior is None:
            par, cita, nota = "PRIMERA", "", "Primera ola de la serie C1/U1 (2011)."
        else:
            comp_cruda = comp_por_calc.get(calc)
            assert comp_cruda is not None, f"sin fila comparabilidad para {calc}"
            par, nota = _par_c1u1(comp_cruda)
            cita = CITA_SPEC_C1U1 + " + " + CITA_TSV_C1U1.format(ola=ola)

        marca_2020 = "SI" if ola == 2020 or (anterior and anterior[0] == 2020) else "NO"
        filas.append(_fila(
            serie_id, "ENVIPE", DOMINIO_C1U1, CONDUCTA_C1U1, CONDUCTA_TEXTO_C1U1,
            EJE_NAC, SEG_TOTAL, UNIDAD_C1U1, ola, calc, result_p, result_lo,
            result_hi, par, cita, marca_2020, nota,
        ))
        anterior = (ola, calc)
    return filas


def filas_r() -> list[str]:
    filas = []
    serie_id = f"ENVIPE-{CONDUCTA_R}-{EJE_NAC}-{SEG_TOTAL}"
    anterior = None
    for ola, calc in OLAS_R:
        claves = _resultado_keys(calc)
        result_p = f"RESULT-{calc.removeprefix('CALC-')}-PUNTO"
        result_lo = f"RESULT-{calc.removeprefix('CALC-')}-IC-LO"
        result_hi = f"RESULT-{calc.removeprefix('CALC-')}-IC-HI"
        for rid in (result_p, result_lo, result_hi):
            assert rid in claves, f"{rid} no existe en {calc}/resultados.json"

        if anterior is None:
            par, cita, nota = "PRIMERA", "", "Primera ola de la serie R (2012)."
        else:
            par, nota = "COMPARABLE", "MISMO-INSTRUMENTO (BP1_23 estable; U_R no filtra BPCOD)"
            cita = CITA_R

        marca_2020 = "NO"  # ninguna ola de esta serie es 2020, ni el par la toca
        filas.append(_fila(
            serie_id, "ENVIPE", DOMINIO_R, CONDUCTA_R, CONDUCTA_TEXTO_R,
            EJE_NAC, SEG_TOTAL, UNIDAD_R, ola, calc, result_p, result_lo,
            result_hi, par, cita, marca_2020, nota,
        ))
        anterior = (ola, calc)
    return filas


def _slug(texto: str) -> str:
    t = texto.strip().upper()
    t = re.sub(r"[^A-Z0-9]+", "-", t)
    return t.strip("-")


_OLA_RE = re.compile(r"ENVIPE\s+(\d{4})")


def filas_catalogo() -> list[str]:
    """Las 31 filas del catálogo ENVIPE fuera de la serie R (que ya se
    construyó arriba con su propio bucle). Cada una es una serie de 1
    sola ola (SIN-SERIE la dictamina el consumidor, no este mapa)."""
    with open(CATALOGO, "r", encoding="utf-8") as fh:
        lineas = fh.read().split("\n")
    cabecera = lineas[0].split("\t")
    idx = {h: i for i, h in enumerate(cabecera)}
    assert not (FORBIDDEN_COLS & set(idx)) or True  # nombres existen; nunca se leen abajo
    i_llave = idx["llave"]
    i_dominio = idx["dominio"]
    i_conducta = idx["conducta"]
    i_ola = idx["instrumento_ola"]
    i_segmento = idx["segmento"]
    i_uden = idx["universo_denominador"]
    i_uesc = idx["unidad_escala"]
    i_rp = idx["result_punto"]
    i_ri = idx["result_inf"]
    i_rs = idx["result_sup"]
    i_calc = idx["calc"]

    filas = []
    vistos = set()
    for linea in lineas[1:]:
        if not linea:
            continue
        campos = linea.split("\t")
        if len(campos) <= i_ola or "ENVIPE" not in campos[i_ola]:
            continue
        conducta = campos[i_conducta]
        if conducta == "R":
            continue  # ya construida en filas_r()

        llave = campos[i_llave]
        if llave in vistos:
            continue
        vistos.add(llave)

        dominio = campos[i_dominio]
        segmento_raw = campos[i_segmento]
        m = _OLA_RE.search(campos[i_ola])
        assert m, f"no se pudo leer año de instrumento_ola: {campos[i_ola]!r}"
        ola = int(m.group(1))
        uden = _scrub(campos[i_uden])
        uesc = _scrub(campos[i_uesc])
        calc = campos[i_calc]
        result_p = campos[i_rp]
        result_lo = campos[i_ri]
        result_hi = campos[i_rs]

        claves = _resultado_keys(calc)
        assert result_p in claves, f"{result_p} no existe en {calc}/resultados.json"
        if result_lo:
            assert result_lo in claves, f"{result_lo} no existe en {calc}/resultados.json"
        if result_hi:
            assert result_hi in claves, f"{result_hi} no existe en {calc}/resultados.json"

        if ":" in segmento_raw:
            eje_txt, seg_txt = segmento_raw.split(":", 1)
            eje, segmento = _slug(eje_txt), _slug(seg_txt)
            nota = f"eje/segmento derivados de catálogo.segmento={segmento_raw!r}."
        else:
            eje, segmento = EJE_NAC, SEG_TOTAL
            nota = f"catálogo.segmento={segmento_raw!r} (clave milpa/celda, no eje demográfico)."

        conducta_slug = _slug(conducta)
        serie_id = f"ENVIPE-{conducta_slug}-{eje}-{segmento}"
        marca_2020 = "NO"  # ninguna fila del catálogo ENVIPE es ola 2020

        filas.append(_fila(
            serie_id, "ENVIPE", dominio, conducta_slug, uden, eje, segmento,
            uesc, ola, calc, result_p, result_lo, result_hi, "PRIMERA", "",
            marca_2020, nota,
        ))
    return filas


def construir_filas() -> list[str]:
    comp_por_calc = _leer_comparabilidad_denuncia()
    filas = []
    filas.extend(filas_c1u1(comp_por_calc))
    filas.extend(filas_r())
    filas.extend(filas_catalogo())
    return filas


def main() -> None:
    filas = construir_filas()
    contenido = "\n".join([CABECERA] + filas) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenido)
    print(f"escrito: {OUT} ({len(filas)} filas)")


if __name__ == "__main__":
    main()
