#!/usr/bin/env python3
"""FP-29 -- las tres series externas del residual de `conf.06`.

Mide el reactivo de confianza generalizada en los instrumentos NO-ENCUCI
que `ADR-64(a)` dejo abiertos (12% WVS / 22% procedencia inestable /
18% Pew). NO recalcula ENCUCI: esa mitad esta sellada por `ADR-64` sobre
la corrida `C-06b` y aqui solo se cita.

Especificacion congelada ANTES de correr esto:
`forense/notas/2026-08-18-fp29-reconcilia.md` §2 (commit d264ae9).

Estimador: `tests/svystat.py::prop_ultimate_cluster` -- el mismo
conglomerado ultimo que produjo la matriz de C-06b. No se reimplementa.

Diseno declarado por instrumento (§2.5 de la nota). Ninguno de los dos
instrumentos externos publica identificadores formales de estrato/UPM
como los publica INEGI; se declara el proxy usado y se dice que la
varianza es aproximada -- no se finge un diseno que el productor no
documenta.

Rutas: se resuelven por `tests/manifiesto.py` (raiz declarada en la
entrada del manifiesto), nunca literales -- misma regla que el resto del
programa.
"""
import io
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M          # noqa: E402
from svystat import prop_ultimate_cluster  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ruta_de(id_entrada):
    """Ruta real del payload de una entrada del manifiesto, por su id.

    DEFECTO PREEXISTENTE QUE ESTA FUNCION RODEA, declarado y no silenciado:
    49 entradas de `descargas_mx` guardan en `archivo` el BASENAME y no la
    ruta relativa a la raiz -- los archivos viven bajo la subcarpeta
    `Descargas Manuales/`. `tests/corpus.py` las reporta a la vez como C3
    ("no resuelve") y como C1 ("huerfano"): son los mismos 49 archivos
    contados dos veces, el lote de REG-LOTE3 (PR #225). Aqui se resuelve
    con un descenso recursivo por basename, SOLO cuando el join plano
    falla, y se devuelve la bandera `rodeo` para que la corrida lo diga en
    su salida. Arreglar el manifiesto es acto sucesor, fuera de perimetro.
    """
    manifiesto_path, raw_dir = M.rutas(ROOT)
    _, entradas = M.leer_manifiesto(manifiesto_path)
    for e in entradas:
        if e.get("id") != id_entrada:
            continue
        raiz = e.get("raiz", M.RAIZ_INTEGRADA)
        base = M.resolver_raiz(raiz, ROOT, raw_dir)
        if not base:
            raise SystemExit(f"raiz '{raiz}' no configurada en esta maquina")
        plano = os.path.join(base, e["archivo"])
        if os.path.exists(plano):
            return plano, e.get("sha256"), False
        objetivo = os.path.basename(e["archivo"])
        for dirpath, _d, fns in os.walk(base):
            if objetivo in fns:
                return os.path.join(dirpath, objetivo), e.get("sha256"), True
        raise SystemExit(f"payload de '{id_entrada}' no encontrado bajo {raiz}")
    raise SystemExit(f"id '{id_entrada}' ausente del manifiesto")


def _verifica_hash(ruta, esperado):
    """A.7: la identidad de un artefacto es su contenido. Se comprueba
    antes de medir sobre el -- un payload que no coincide no se mide."""
    import hashlib
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    real = h.hexdigest()
    return real, (esperado is None or real == esperado)


# ---------------------------------------------------------------- WVS W7
def wvs_wave7_mexico():
    """WVS Wave 7 Mexico 2018. Q57 binario; Q58-Q63 bateria 4 puntos.

    Peso    W_WEIGHT   (ponderador dentro de pais que publica WVS)
    UPM     I_PSU      (unidad primaria declarada en el propio microdato)
    Estrato N_REGION_WVS (region; WVS no publica estrato de diseno)
    """
    import csv
    ruta, sha, rodeo = _ruta_de("f00013146_wvs_wave_7_mexico_csv_v5_1")
    real, ok = _verifica_hash(ruta, sha)
    with zipfile.ZipFile(ruta) as z:
        nombre = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        crudo = z.read(nombre).decode("utf-8-sig", errors="replace")
    filas = list(csv.DictReader(io.StringIO(crudo), delimiter=";"))

    meta = {
        "n_filas": len(filas),
        "anio": sorted({f["A_YEAR"] for f in filas}),
        "pais": sorted({f["B_COUNTRY_ALPHA"] for f in filas}),
        "campo_trabajo": (sorted({f["FW_START"] for f in filas}),
                          sorted({f["FW_END"] for f in filas})),
        "version_archivo": sorted({f["version"] for f in filas}),
        "sha256_verificado": real, "sha256_coincide": ok, "rodeo_de_ruta": rodeo,
    }

    def celda(var, positivos, etiqueta):
        rows, n_util, n_missing = [], 0, 0
        for f in filas:
            try:
                v = float(f[var])
            except (TypeError, ValueError):
                n_missing += 1
                continue
            if v < 0:                      # -1 DK, -2 NA, -4/-5 no preguntado
                n_missing += 1
                continue
            y = 1 if int(v) in positivos else 0
            rows.append((f["N_REGION_WVS"], f["I_PSU"],
                         float(f["W_WEIGHT"]), y))
            n_util += 1
        r = prop_ultimate_cluster(rows)
        r.update({"var": var, "etiqueta": etiqueta, "n_util": n_util,
                  "n_missing": n_missing, "positivos": sorted(positivos)})
        return r

    return meta, [
        celda("Q57", {1}, "Q57 -- se puede confiar en la mayoria de la gente (binario)"),
        celda("Q59", {1, 2}, "Q59 -- sus vecinos: confia completamente+algo (4 puntos)"),
        celda("Q60", {1, 2}, "Q60 -- sus conocidos: confia completamente+algo (4 puntos)"),
        celda("Q58", {1, 2}, "Q58 -- su familia: confia completamente+algo (4 puntos)"),
        celda("Q61", {1, 2}, "Q61 -- gente que conoce por primera vez: compl.+algo (4 puntos)"),
    ]


# ------------------------------------------------------ Latinobarometro
def latinobarometro_2024_mexico():
    """Latinobarometro 2024, Mexico (IDENPA=484). P10STGBS binario.

    Peso    WT       (ponderacion que publica Latinobarometro)
    UPM     CIUDAD   (ciudad; no publica UPM formal)
    Estrato TAMCIUD  (tamano de habitat; no publica estrato formal)
    """
    import pandas as pd
    ruta, sha, rodeo = _ruta_de("latinobarometro2024_bd_stata")
    real, ok = _verifica_hash(ruta, sha)
    with zipfile.ZipFile(ruta) as z:
        nombre = [n for n in z.namelist()
                  if n.endswith(".dta") and "_esp_" in n][0]
        crudo = z.read(nombre)
    d = pd.read_stata(io.BytesIO(crudo), convert_categoricals=False)
    mx = d[d["IDENPA"] == 484]

    meta = {
        "n_filas_total": int(len(d)),
        "n_filas_mexico": int(len(mx)),
        "anio_estudio": sorted({int(x) for x in mx["NUMINVES"].unique()}),
        "paises_en_archivo": int(d["IDENPA"].nunique()),
        "archivo_interno": nombre,
        "sha256_verificado": real, "sha256_coincide": ok, "rodeo_de_ruta": rodeo,
    }

    rows, n_util, n_missing = [], 0, 0
    for _, f in mx.iterrows():
        v = f["P10STGBS"]
        if pd.isna(v) or float(v) not in (1.0, 2.0):
            n_missing += 1
            continue
        y = 1 if int(v) == 1 else 0
        rows.append((int(f["TAMCIUD"]), int(f["CIUDAD"]), float(f["WT"]), y))
        n_util += 1
    r = prop_ultimate_cluster(rows)
    r.update({"var": "P10STGBS", "n_util": n_util, "n_missing": n_missing,
              "etiqueta": "P10STGBS -- se puede confiar en la mayoria de las personas (binario)"})
    return meta, [r]


# ------------------------------------------------------------- LAPOP
_LAPOP_OLAS = [
    ("mexico_lapop_americasbarometer_2019_v1_0_w", 2019),
    ("mex_2021_lapop_americasbarometer_v1_2_w", 2021),
    ("mex_2023_lapop_americasbarometer_v1_0_w", 2023),
]


def lapop_mexico():
    """LAPOP/AmericasBarometer Mexico -- `it1`, "Confianza en la comunidad".

    OJO, y es el punto sustantivo: `it1` NO es el reactivo de confianza
    GENERALIZADA. Pregunta por "la gente de su comunidad" en escala de 4
    puntos (muy/algo/poco/nada confiable). El cuestionario ABMex2023
    (`lapop_abmex2023_cuestionario.pdf`) no trae ningun reactivo de "la
    mayoria de las personas" -- verificado por grep sobre su texto, cero
    coincidencias. Se mide aqui para poder decir QUE dice LAPOP, no para
    compararlo en magnitud contra los binarios (Bloque A-bis regla 3).

    Peso    wt          UPM  upm          Estrato  estratopri
    """
    import pandas as pd
    salida = []
    for id_entrada, anio in _LAPOP_OLAS:
        ruta, sha, rodeo = _ruta_de(id_entrada)
        real, ok = _verifica_hash(ruta, sha)
        d = pd.read_stata(ruta, convert_categoricals=False)
        rows, n_util, n_missing, n_sin_diseno = [], 0, 0, 0
        for _, f in d.iterrows():
            v = f["it1"]
            if pd.isna(v) or float(v) not in (1.0, 2.0, 3.0, 4.0):
                n_missing += 1
                continue
            if pd.isna(f["estratopri"]) or pd.isna(f["upm"]) or pd.isna(f["wt"]):
                n_sin_diseno += 1      # sin variables de diseno: se excluye,
                continue               # no se imputa ni se fuerza a un estrato
            y = 1 if int(v) in (1, 2) else 0      # muy + algo confiable
            rows.append((int(f["estratopri"]), int(f["upm"]),
                         float(f["wt"]), y))
            n_util += 1
        r = prop_ultimate_cluster(rows)
        r.update({"var": "it1", "anio": anio, "n_util": n_util,
                  "n_missing": n_missing, "n_sin_diseno": n_sin_diseno,
                  "n_filas": int(len(d)),
                  "sha256_verificado": real, "sha256_coincide": ok,
                  "rodeo_de_ruta": rodeo,
                  "etiqueta": f"it1 {anio} -- la gente de su comunidad: "
                              f"muy+algo confiable (4 puntos)"})
        salida.append(r)
    return salida


def _fmt(r):
    lo, hi = r["ic95"]
    return (f'  {r["etiqueta"]}\n'
            f'    p̂ = {r["p_hat"]*100:.2f}%   SE = {r["se"]*100:.2f}pp   '
            f'IC95% = [{lo*100:.2f}%, {hi*100:.2f}%]\n'
            f'    n util = {r["n_util"]}   no-respuesta excluida = {r["n_missing"]}   '
            f'UPM = {r["n_upm_total"]}   estratos singleton = {r["n_estratos_singleton"]}')


def main():
    salida = {}
    print("=" * 72)
    print("FP-29 · SERIES EXTERNAS — reactivo de confianza generalizada")
    print("=" * 72)

    meta, celdas = wvs_wave7_mexico()
    print("\n### WVS Wave 7 · Mexico")
    print(f"  meta: {meta}")
    for r in celdas:
        print(_fmt(r))
    salida["wvs_w7_mexico"] = {"meta": meta, "celdas": celdas}

    meta, celdas = latinobarometro_2024_mexico()
    print("\n### Latinobarometro 2024 · Mexico")
    print(f"  meta: {meta}")
    for r in celdas:
        print(_fmt(r))
    salida["latinobarometro_2024_mexico"] = {"meta": meta, "celdas": celdas}

    celdas = lapop_mexico()
    print("\n### LAPOP/AmericasBarometer · Mexico — it1 (NO es el reactivo generalizado)")
    for r in celdas:
        print(_fmt(r))
    salida["lapop_mexico"] = {"celdas": celdas}

    destino = os.path.join(ROOT, "data", "fp29-series-externas-2026-08-18.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nEscrito: {os.path.relpath(destino, ROOT)}")


if __name__ == "__main__":
    main()
