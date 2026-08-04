#!/usr/bin/env python3
"""P3 -- LCA de segmentacion sobre ENIGH: construccion del universo analitico.

Especificacion congelada en forense/p3-lca-preregistro-v1_0.md (v1.0,
sellado 3/ago/2026). Este modulo SOLO construye el dataset -- no ajusta
ningun modelo. Lo importan tests/p3_lca_run.py y las corridas de
sensibilidad.

Universo: personas de 18+ anios, ENIGH 2022 nueva serie (enigh2022_nc_csv,
data/raw). Siete indicadores I1-I7 (pre-registro Sec.2.1):
  I1 formalidad laboral      segsoc (poblacion, persona)
  I2 edad en tramos          edad (poblacion, persona) -- corte primario
                              {18-29,30-44,45-59,60+}; corte S2
                              {18-24,25-39,40-59,60+}
  I3 condicion migratoria    residencia recodificada a 3 vs entidad actual
                              (poblacion, persona)
  I4 urbanizacion            tam_loc (concentradohogar, hogar)
  I5 nivel socioeconomico    est_socio (concentradohogar, hogar)
  I6 tenencia celular        celular (hogares, hogar)
  I7 conexion a internet     conex_inte (hogares, hogar)

Auxiliares (no indicadores, Sec.2.4): ing_cor, remesas (concentradohogar).
S3 (Sec.2.4/5.3.a): formalidad via modulo `trabajos` en 3 categorias
  formal / informal ocupado / no ocupado, usando el trabajo principal
  (id_trabajo=1) y pres_8='08' (SAR/AFORE) como marcador de formalidad --
  operacionalizacion declarada aqui, no citada del canon porque el canon
  no fija la regla exacta.

Variables de diseno (Sec.5.1, hueco declarado por el pre-registro,
LOCALIZADO aqui): `factor` (persona, en `poblacion`), `est_dis`, `upm` --
las tres viven DIRECTO en `poblacion`, a nivel persona. No hace falta
trasladar un factor de hogar: el paquete ya trae el factor de persona.

No se abre ENVIPE, ENCUCI ni ENIF. Solo ENIGH.
"""
import csv
import os
import sys
import tempfile
import zipfile

RAW = "data/raw"
ENIGH_ZIP = "enigh2022_nc_csv.zip"

TABLAS = {
    "poblacion": "conjunto_de_datos_poblacion_enigh2022_ns",
    "concentradohogar": "conjunto_de_datos_concentradohogar_enigh2022_ns",
    "hogares": "conjunto_de_datos_hogares_enigh2022_ns",
    "trabajos": "conjunto_de_datos_trabajos_enigh2022_ns",
}


def _miembros_necesarios(namelist):
    prefijos = tuple(f"{carpeta}/" for carpeta in TABLAS.values())
    return [n for n in namelist if n.startswith(prefijos)]


def extraer(tmpdir):
    """Extrae solo las 4 tablas que este protocolo permite tocar (Sec.2.0/2.1)."""
    zpath = os.path.join(RAW, ENIGH_ZIP)
    with zipfile.ZipFile(zpath) as z:
        miembros = _miembros_necesarios(z.namelist())
        z.extractall(path=tmpdir, members=miembros)
    return tmpdir


def _csv_path(tmpdir, tabla):
    carpeta = TABLAS[tabla]
    return os.path.join(tmpdir, carpeta, "conjunto_de_datos", f"{carpeta}.csv")


def _leer(tmpdir, tabla):
    with open(_csv_path(tmpdir, tabla), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def tramo_edad(edad, cortes):
    """cortes: lista de (lo, hi_inclusive_or_None, etiqueta), evaluada en orden."""
    for lo, hi, etiqueta in cortes:
        if edad >= lo and (hi is None or edad <= hi):
            return etiqueta
    return None


CORTE_PRIMARIO = [(18, 29, "18-29"), (30, 44, "30-44"), (45, 59, "45-59"), (60, None, "60+")]
CORTE_S2 = [(18, 24, "18-24"), (25, 39, "25-39"), (40, 59, "40-59"), (60, None, "60+")]


def migracion(residencia, entidad):
    residencia = residencia.strip()
    entidad = entidad.strip()
    if residencia in ("33", "34"):
        return "extranjero"
    if residencia == "":
        return None
    if residencia.lstrip("0") == entidad.lstrip("0"):
        return "misma_entidad"
    return "otra_entidad"


def formalidad_segsoc(v):
    v = v.strip()
    if v == "1":
        return "formal"
    if v == "2":
        return "informal"
    return None


def si_no(v):
    v = v.strip()
    if v == "1":
        return "si"
    if v == "2":
        return "no"
    return None


def construir_universo(tmpdir):
    """Devuelve lista de dicts, uno por persona de 18+, con I1-I7, el corte S2
    de edad, campos auxiliares (ing_cor, remesas), variables de diseno
    (factor, est_dis, upm) y llave de hogar (para S3 y para futuras
    verificaciones)."""
    pob = _leer(tmpdir, "poblacion")
    conc = _leer(tmpdir, "concentradohogar")
    hog = _leer(tmpdir, "hogares")
    trab = _leer(tmpdir, "trabajos")

    conc_por_hogar = {}
    for row in conc:
        key = (row["folioviv"], row["foliohog"])
        conc_por_hogar[key] = row

    hog_por_hogar = {}
    for row in hog:
        key = (row["folioviv"], row["foliohog"])
        hog_por_hogar[key] = row

    # Trabajo principal (id_trabajo=1) por persona -- para S3.
    trab_principal = {}
    tiene_trabajo = set()
    for row in trab:
        key = (row["folioviv"], row["foliohog"], row["numren"])
        tiene_trabajo.add(key)
        if row["id_trabajo"] == "1":
            trab_principal[key] = row

    universo = []
    n_sin_hogar_conc = 0
    n_sin_hogar_hog = 0
    for row in pob:
        edad = int(row["edad"])
        if edad < 18:
            continue
        hkey = (row["folioviv"], row["foliohog"])
        pkey = (row["folioviv"], row["foliohog"], row["numren"])
        crow = conc_por_hogar.get(hkey)
        hrow = hog_por_hogar.get(hkey)
        if crow is None:
            n_sin_hogar_conc += 1
        if hrow is None:
            n_sin_hogar_hog += 1

        i1 = formalidad_segsoc(row["segsoc"])
        i2 = tramo_edad(edad, CORTE_PRIMARIO)
        i2_alt = tramo_edad(edad, CORTE_S2)
        i3 = migracion(row["residencia"], row["entidad"])
        i4 = crow["tam_loc"].strip() if crow else None
        i5 = crow["est_socio"].strip() if crow else None
        i6 = si_no(hrow["celular"]) if hrow else None
        i7 = si_no(hrow["conex_inte"]) if hrow else None

        # S3: formalidad via trabajos, 3 categorias.
        if pkey not in tiene_trabajo:
            formal_trab = "no_ocupado"
        else:
            tp = trab_principal.get(pkey)
            if tp is None:
                # tiene trabajo(s) pero ninguno es el "principal" id_trabajo=1
                # (posible solo secundario reportado sin principal) -- se
                # trata como ocupado, informal por defecto de PRES_8 vacio.
                formal_trab = "informal_ocupado"
            else:
                formal_trab = "formal_ocupado" if tp["pres_8"].strip() == "08" else "informal_ocupado"

        ing_cor = float(crow["ing_cor"]) if crow and crow["ing_cor"].strip() != "" else None
        remesas = float(crow["remesas"]) if crow and crow["remesas"].strip() != "" else None

        universo.append({
            "folioviv": row["folioviv"],
            "foliohog": row["foliohog"],
            "numren": row["numren"],
            "factor": float(row["factor"]),
            "est_dis": row["est_dis"].strip(),
            "upm": row["upm"].strip(),
            "I1_formalidad": i1,
            "I2_edad": i2,
            "I2_edad_S2": i2_alt,
            "I3_migracion": i3,
            "I4_tam_loc": i4,
            "I5_est_socio": i5,
            "I6_celular": i6,
            "I7_conex_inte": i7,
            "S3_formalidad_trabajos": formal_trab,
            "ing_cor_hogar": ing_cor,
            "remesas_hogar": remesas,
            "est_socio_raw": i5,
        })

    meta = {
        "n_poblacion_total": len(pob),
        "n_18_mas": len(universo),
        "n_sin_match_concentradohogar": n_sin_hogar_conc,
        "n_sin_match_hogares": n_sin_hogar_hog,
    }
    return universo, meta


def cargar_universo():
    """Punto de entrada: extrae a tempdir y construye. No deja rastro en el
    arbol git (tempfile.mkdtemp, fuera del repo)."""
    tmpdir = tempfile.mkdtemp(prefix="p3_lca_")
    extraer(tmpdir)
    return construir_universo(tmpdir)


if __name__ == "__main__":
    universo, meta = cargar_universo()
    print("=== Metadatos de construccion ===")
    for k, v in meta.items():
        print(f"  {k}: {v}")
    print()
    print(f"n del universo 18+ (I1_1.b): {len(universo)}")
    print()
    print("Ejemplo de 3 registros:")
    for r in universo[:3]:
        print(" ", r)
    sys.exit(0)
