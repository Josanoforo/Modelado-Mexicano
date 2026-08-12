#!/usr/bin/env python3
"""ACTO J -- test de cobertura por entidad para el cruce folioviv+foliohog
entre {poblacion,ingresos} y {concentradohogar,hogares} de ENIGH.

Por que hace falta (forense/notas/2026-08-12-j-alcance-folioviv.md S1.3).
`validar_contra_publicado()` (en `r5_1_pension_bienestar.py`) solo suma
columnas propias de `concentradohogar` contra una cifra publicada por INEGI
-- nunca abre `poblacion`/`ingresos`, nunca ejercita el cruce por
`folioviv`, y por construccion no puede ver una fila que ese cruce pierde
en silencio. Este archivo si las abre y compara, hogar por hogar y entidad
por entidad, contra una verdad de referencia calculada de forma
independiente -- con `folioviv.str.zfill(ancho_nativo)`, el mismo mecanismo
que e4c commit 3 declaro y verifico contra el valor real de
`concentradohogar` (heredado aqui, generalizado de un `zfill(10)` fijo a un
ancho derivado por ola porque 2012 resulto ser `C(6)`, no una version
truncada de `C(10)` -- ver
`forense/notas/2026-08-11-e4c-r5-1-d2-commit3-ajuste-preejecucion.md` y
`forense/notas/2026-08-12-j-alcance-folioviv.md` S2.2).

Dos asserts se colapsaron en uno, mas fuerte: la S1.3 original preveia (a)
frenar si el arreglo pierde cobertura que antes tenia, y (b) frenar si el
codigo SIN arreglar muestra >5pp de asimetria entre entidades. Un solo
`assert n_perdidos_total == 0` implica ambas -- cero perdidas por ola
implica asimetria cero para esa ola, y es mas facil de verificar que una
comparacion cruzada entre dos corridas del mismo proceso. La asimetria se
sigue calculando e imprimiendo (diagnostico), ya no se usa como umbral.

Ejercita las funciones REALES de produccion (`r5_1_pension_bienestar.
procesar_ola`, `p3_lca_data.cargar_universo`) -- no reimplementa el join
bajo prueba, lo audita desde afuera con una segunda lectura independiente
de los mismos CSV.

Corre sola, mismo patron que `tests/test_svystat.py` (no depende de
`check.py`, no esta wireada a CI en este acto -- fuera de su perimetro):

    python3 tests/test_join_folioviv.py

Requiere `data/raw/` montado (corpus real). Si no lo esta, cada test que
abre ola se SALTA con aviso explicito impreso -- nunca un PASS silencioso.
"""
import csv
import io
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r5_1_pension_bienestar as R5  # noqa: E402
import p3_lca_data as P3  # noqa: E402

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def _corpus_disponible():
    return RAW.exists() and any(RAW.glob("enigh*_nc_csv.zip"))


def _reader(z, path):
    with z.open(path) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace")
        yield from csv.DictReader(text)


# ---------------------------------------------------------------------------
# R5.1 -- cobertura del cruce ingresos -> hogares (via concentradohogar)
# ---------------------------------------------------------------------------

def _ancho_nativo_concentradohogar(year):
    """El ancho REAL de folioviv en concentradohogar de esta ola -- NO se
    asume 10. Medido en esta sesion (S0/S2 de la nota): concentradohogar es
    SIEMPRE uniforme dentro de una ola (2012: 6 caracteres, 9,002/9,002;
    2014/2016/2018/2020/2022: 10, uniforme en cada una) pero el ancho NATIVO
    cambia entre 2012 (6) y el resto (10) -- 2012 es un esquema mas angosto,
    autoconsistente, no una version truncada de 10. zfill(10) a ciegas
    ROMPERIA el cruce de 2012 (ya funciona a 6 caracteres tal cual viene).
    Se deriva el ancho de la primera fila y se confirma uniforme en todas."""
    cfg = R5.WAVES[year]
    z = zipfile.ZipFile(RAW / cfg["zip_name"])
    anchos = set()
    for row in _reader(z, cfg["ch"]):
        anchos.add(len(row["folioviv"].strip()))
    assert len(anchos) == 1, (
        f"concentradohogar {year} NO es uniforme en longitud de folioviv ({anchos}) -- "
        f"la premisa de tabla testigo confiable no se sostiene, hay que parar y mirar a mano."
    )
    return anchos.pop()


def _verdad_pension(year, ancho):
    """Verdad de referencia, independiente de procesar_ola(): por hogar
    (folioviv normalizado al ANCHO NATIVO de concentradohogar de esta ola +
    foliohog), si `ingresos` trae alguna fila con clave de pension e
    ing_tri>0. Ninguna otra logica de procesar_ola() se repite aqui."""
    cfg = R5.WAVES[year]
    z = zipfile.ZipFile(RAW / cfg["zip_name"])
    claves_pension = cfg["pension_claves"]
    tiene_pension = set()
    for row in _reader(z, cfg["ing"]):
        if row["clave"] not in claves_pension:
            continue
        try:
            ing_tri = float(row["ing_tri"])
        except ValueError:
            ing_tri = 0.0
        if ing_tri <= 0:
            continue
        fv = row["folioviv"].strip().zfill(ancho)
        tiene_pension.add((fv, row["foliohog"]))
    return tiene_pension


def _cobertura_r5(year):
    """Llama procesar_ola() REAL (produccion, sin tocar) y la compara contra
    _verdad_pension(). hogares queda siempre indexado por el folioviv de
    `concentradohogar`, uniforme dentro de cada ola (ver
    _ancho_nativo_concentradohogar) -- agrupar por entidad = fv[:2] es
    seguro sin normalizar de nuevo SALVO en 2012 (ancho 6: fv[:2] sigue
    siendo la entidad, el formato corto tambien la trae al frente, mismo
    orden que ubica_geo)."""
    ancho = _ancho_nativo_concentradohogar(year)
    hogares = R5.procesar_ola(year)
    verdad = _verdad_pension(year, ancho)

    por_entidad = defaultdict(lambda: [0, 0])  # entidad -> [n_hogares, n_perdidos]
    perdidos = []
    for (fv, foliohog), hh in hogares.items():
        assert len(fv) == ancho, (
            f"folioviv de concentradohogar con longitud inesperada: {fv!r} ({year}, esperado {ancho})"
        )
        ent = fv[:2]
        por_entidad[ent][0] += 1
        if (fv, foliohog) in verdad and not hh["beneficiario"]:
            por_entidad[ent][1] += 1
            perdidos.append((fv, foliohog))
    return ancho, por_entidad, perdidos


def test_r5_cobertura_por_entidad_todas_las_olas():
    if not _corpus_disponible():
        print("SALTADO -- data/raw/ no montado, no se puede ejercitar el join real (r5_1).")
        return None
    print("TEST R5.1 -- cobertura del cruce ingresos->hogares (deteccion de `beneficiario`), por entidad, seis olas:")
    resumen = {}
    fallas = []
    for year in sorted(R5.WAVES):
        ancho, por_entidad, perdidos = _cobertura_r5(year)
        tasas = {ent: (n_perd / n_tot if n_tot else 0.0) for ent, (n_tot, n_perd) in por_entidad.items()}
        asimetria = (max(tasas.values()) - min(tasas.values())) if tasas else 0.0
        entidades_afectadas = sorted(ent for ent, t in tasas.items() if t > 0)
        n_perdidos_total = sum(n for _, n in por_entidad.values())
        n_hogares_total = sum(t for t, _ in por_entidad.values())
        resumen[year] = {
            "ancho_nativo_concentradohogar": ancho,
            "n_hogares_total": n_hogares_total,
            "n_perdidos_total": n_perdidos_total,
            "asimetria_pp": asimetria * 100,
            "entidades_afectadas": entidades_afectadas,
        }
        print(f"  {year} (ancho nativo={ancho}): hogares={n_hogares_total} "
              f"beneficiarios_perdidos_en_silencio={n_perdidos_total} "
              f"asimetria_max_min={asimetria*100:.2f}pp entidades_afectadas={entidades_afectadas}")
        if n_perdidos_total:
            fallas.append((year, n_perdidos_total, entidades_afectadas))

    if fallas:
        detalle = "; ".join(f"{y}: {n} hogares en entidades {ents}" for y, n, ents in fallas)
        raise AssertionError(
            f"procesar_ola() pierde hogares beneficiarios en silencio (join folioviv roto sin zfill): {detalle}"
        )
    print("  OK -- cero hogares beneficiarios perdidos en silencio, en las seis olas.")
    return resumen


# ---------------------------------------------------------------------------
# P3-LCA -- cobertura del cruce poblacion -> concentradohogar/hogares (2022)
# ---------------------------------------------------------------------------

def test_p3_cobertura_por_entidad_2022():
    if not _corpus_disponible():
        print("SALTADO -- data/raw/ no montado, no se puede ejercitar el join real (p3_lca).")
        return None
    print("TEST P3-LCA -- cobertura del cruce poblacion->concentradohogar/hogares, por entidad, 2022"
          " (unica ola que este script procesa):")
    universo, meta = P3.cargar_universo()

    n_sin_conc = meta["n_sin_match_concentradohogar"]
    n_sin_hog = meta["n_sin_match_hogares"]
    print(f"  n_poblacion_total={meta['n_poblacion_total']} n_18_mas={meta['n_18_mas']} "
          f"sin_match_concentradohogar={n_sin_conc} sin_match_hogares={n_sin_hog}")

    if n_sin_conc or n_sin_hog:
        # Desglose por entidad SOLO si hay algo que desglosar -- 2022 esta
        # confirmada limpia por e4c commit 3 (poblacion.factor ==
        # concentradohogar.factor exacto en 29,974/29,974), asi que esta
        # rama no deberia ejecutarse; si se ejecuta, es la senal de que algo
        # cambio y hay que pararse a mirarlo, no forzar el desglose fino.
        por_entidad = defaultdict(int)
        zpath = Path(P3.RAW) / P3.ENIGH_ZIP
        z = zipfile.ZipFile(zpath)
        conc_keys = set()
        for row in _reader(z, f"{P3.TABLAS['concentradohogar']}/conjunto_de_datos/{P3.TABLAS['concentradohogar']}.csv"):
            conc_keys.add((row["folioviv"], row["foliohog"]))
        for row in _reader(z, f"{P3.TABLAS['poblacion']}/conjunto_de_datos/{P3.TABLAS['poblacion']}.csv"):
            if (row["folioviv"], row["foliohog"]) not in conc_keys:
                por_entidad[row["entidad"].strip()] += 1
        raise AssertionError(
            f"construir_universo() pierde personas en silencio (sin_match_concentradohogar={n_sin_conc}, "
            f"sin_match_hogares={n_sin_hog}); por entidad (concentradohogar): {dict(por_entidad)}"
        )
    print("  OK -- cero personas sin hogar en concentradohogar/hogares, ENIGH 2022.")
    return meta


if __name__ == "__main__":
    resultados = {}
    fallo = False
    for nombre, fn in [
        ("r5_1_cobertura", test_r5_cobertura_por_entidad_todas_las_olas),
        ("p3_lca_cobertura", test_p3_cobertura_por_entidad_2022),
    ]:
        print()
        try:
            resultados[nombre] = fn()
        except AssertionError as e:
            fallo = True
            print(f"  FALLA -- {e}")
    print()
    if fallo:
        print("test_join_folioviv.py: AL MENOS UN TEST FALLÓ (ver arriba).")
        sys.exit(1)
    print("test_join_folioviv.py: todos los tests pasaron.")
    sys.exit(0)
