#!/usr/bin/env python3
"""ACTO GEN2-C1-SUCESORES-Y-LOTE-3 · P1 · prepara los cuatro paquetes residuales para
la reconstructora (opción A, R32), sin abrir ningún valor sellado.

Por paquete:
  <REC>/<paq>/paquete/   contenedor residuales-documentales-v2 extraído + CONTRATO-v3.md
                         + FIRMAS-Y-ACCESO.md + datos/ (miembros autorizados del ZIP,
                         extraídos byte a byte, sin parsear)
  <REC>/<paq>/salida/    vacío
  <repo>/…/catalogo-1-lote3/<paq>/entrada/{allowlist.json, allowlist.canon.sha256,
                         identidad.json, tolerancia-v2.json, prompt.md}

Uso: prepara_residuales.py <REC>   (p. ej. /home/pc0/c1-sucesores-rec)
"""
import hashlib
import json
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[3]
AQUI = Path(__file__).resolve().parent
CONT = R / "forense/validacion-independiente/catalogo-1-entradas-residuales-lote2/p4"
CONTRATO = R / "forense/validacion-independiente/catalogo-1-ejecutor-v3/CONTRATO-v3.md"
CONTRATO_SHA = "821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb"
REC = Path(sys.argv[1])
IDS = "las columnas identificadoras de vínculo que existan y el FD documente como llave"

PAQ = {
    "enbiare-pisos-bienestar-0001": {
        "zip": "data/raw/enbiare2021/enbiare_2021_base_de_datos_csv.zip",
        "zip_sha": "afe9013a4cc26538dfe81da686f0d09e756a7d0e2fc407cd22f596fd53c0f354",
        "miembros": {"TENBIARE.csv": "TENBIARE.csv", "TSDEM.csv": "TSDEM.csv"},
        "campos": {
            "TENBIARE.csv": ["FOLIO", "VIV_SEL", "HOGAR", "N_REN", "TLOC", "FAC_ELE", "EST_DIS",
                             "UPM_DIS", "PA1", "PA5"] + [f"PD2_{i}" for i in range(1, 8)]
                            + ["PD3_1", "PD3_2", "PB1_01", "PB1_02", "PB1_04", "PB1_11",
                               "PB2_1", "PB2_2", "PG6", "PG7"],
            "TSDEM.csv": ["FOLIO", "VIV_SEL", "HOGAR", "N_REN", "SEXO", "EDAD", "NIVEL"]},
        "specs": "`enbiare-metodo-base.md`, `spec-conductas-base.md`, `enbiare-ventanas-restauradas.md` y `enbiare-edades-propuesta.md`",
    },
    "encodat-pisos-sustancias-0001": {
        "zip": None,
        "zips": {
            "ENCODAT_2016_2017_Individual.dta": (
                "data/raw/ENCODAT/2016-2017/Bases de datos de ENCODAT 2016 2017/02-Cuestionario individual/ENCODAT_2016_2017_Individual.stata.stata.zip",
                "bb0c7d999e45bebcffb3a26da00bd2d5caa2d982de7d9e330211c11960153346"),
            "ENCODAT_2016_2017_Hogar.dta": (
                "data/raw/ENCODAT/2016-2017/Bases de datos de ENCODAT 2016 2017/01-Cuestionario de Hogar/01-Información sobre el hogar/ENCODAT_2016_2017_Hogar.stata.stata.zip",
                "716f58f817f3203ec2cba8d265d8812d3015bb9ffdb56a39ff50bd3ce1d0d781")},
        "campos": {
            "ENCODAT_2016_2017_Individual.dta": ["id_pers", "id_hogar", "ds2", "ds3", "ds9", "ponde_ss",
                                                 "al1", "al4", "al9", "al11", "tb02", "tb05", "tb50"]
                + [f"di1{c}" for c in "abcdefghi"] + [f"dm1{c}" for c in "abcd"] + ["tp1"],
            "ENCODAT_2016_2017_Hogar.dta": ["id_hogar", "est_var", "code_upm", "estrato"]},
        "specs": "`spec-base-metodo.md` y `spec-base-conductas.md`",
    },
    "encuci-0001": {
        "zip": "data/raw/BD_ENCUCI2020_dbf.zip",
        "zip_sha": "0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283",
        "miembros": {"ENCUCI_2020_SEC_4_5.dbf": "ENCUCI_2020_SEC_4_5.dbf",
                     "ENCUCI_2020_SEC_6_7_8.dbf": "ENCUCI_2020_SEC_6_7_8.dbf"},
        "campos": {
            "ENCUCI_2020_SEC_4_5.dbf": ["ID_PER", "AP4_3_2", "FAC_SEL", "EST_DIS", "UPM_DIS", "DOMINIO"],
            "ENCUCI_2020_SEC_6_7_8.dbf": ["ID_PER", "AP7_3_5", "FAC_SEL", "EST_DIS", "UPM_DIS", "DOMINIO"]},
        "specs": "`encuci-rural-restaurado.md`",
    },
    "enigh-0001": {
        "zip": "data/raw/enigh2022_nc_csv.zip",
        "zip_sha": "3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06",
        "miembros": {
            "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2022_ns.csv": "concentradohogar_enigh2022_ns.csv",
            "conjunto_de_datos_concentradohogar_enigh2022_ns/diccionario_de_datos/diccionario_datos_concentradohogar_enigh2022_ns.csv": "diccionario_datos_concentradohogar_enigh2022_ns.csv"},
        "campos": {"concentradohogar_enigh2022_ns.csv": ["folioviv", "foliohog", "factor", "remesas", "est_dis", "upm"]},
        "specs": "`enigh-complemento-restaurado.md`",
    },
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def extrae(zip_path, zip_sha, miembro, destino):
    zp = R / zip_path
    if sha(zp) != zip_sha:
        raise SystemExit(f"PARO · sha del ZIP discorda: {zip_path}")
    with zipfile.ZipFile(zp) as z, z.open(miembro) as src, open(destino, "wb") as dst:
        shutil.copyfileobj(src, dst)


def prompt(paq, cfg, ident, n):
    campos = "\n".join(f"- `datos/{m}`: {', '.join(f'`{c}`' for c in cs)}, y {IDS}."
                       for m, cs in cfg["campos"].items())
    return f"""Eres una sesión de reconstrucción independiente. No tienes historial ni memoria, y no debes buscarlos. Tu único insumo es el directorio `./paquete/`, de solo lectura. Escribes únicamente en `./salida/`.

## Objetivo

Recalcula el punto y el IC95 de cada una de las {n} llaves de `paquete/esquema-identidades.tsv`, implementando tú mismo el método de los documentos humanos del paquete, en Python 3 (numpy, pandas; `pyreadstat` o `dbfread` si los tienes). No existe código previo que puedas consultar, y no debes buscarlo.

- Punto: {cfg['specs']}.
- IC: `residuales-p3-contrato-ic.md` y `residuales-p3-modulos-ic.md`.
- Formato de salida: `CONTRATO-v3.md` (`version` = 3). `esquema-salida-v2.md` describe la versión 2 del mismo documento; donde difieran, rige `CONTRATO-v3.md`.
- `FIRMAS-Y-ACCESO.md` registra qué documentos del paquete firmó mesa, con su sha256 y el alcance de cada firma. Los documentos firmados son contrato vigente aunque su encabezado diga «PROPUESTO»; aplícalos dentro del alcance registrado.

## Límites de acceso (autorización delimitada)

Del microdato puedes leer la fila de encabezados (o la lista de variables) completa, y de las filas solo estas columnas; en pandas usa `usecols` / `columns`:
{campos}

Si el método exige una columna que no está en esta lista, no la leas: marca las llaves afectadas con `BLOQUEADO-POR-ACCESO` y escribe el `motivo`. No imprimas filas de microdato; conteos y agregados sí. No uses la red ni leas nada fuera de `./paquete/`.

## Qué entregar en `./salida/`

1. `salida/resultado.json`: exactamente el documento de `CONTRATO-v3.md`; `version` = 3; `identidad` = `{json.dumps(ident, ensure_ascii=False)}`; una fila por llave, con `llave` y `unidad` literales del esquema. Con estimación: `estado: "RECONSTRUIDO"`, `punto` y `estado_ic` explícito (`CALCULADO` con `ic95_inf`/`ic95_sup`, o `NO-IDENTIFICADA` con `motivo_ic`). Sin estimación: el estado del contrato que corresponda, con `motivo`. Números como strings `repr(float(x))`, sin redondear. No suprimas celdas por publicabilidad.
2. `salida/diagnosticos-ic-v1.tsv`: las columnas que fija `residuales-p3-contrato-ic.md`, una fila por llave.
3. `salida/diagnostico.json`: por llave, n válido, exclusiones por causa (no ponderadas y ponderadas) y publicabilidad según el contrato; y las decisiones de implementación que tomaste donde la spec admitía más de una lectura, cada una con la frase que la motiva.
4. `salida/codigo/`: todo tu código; `python3 salida/codigo/reconstruye.py`, desde el directorio de trabajo, regenera los archivos 1–3 desde `paquete/`.
5. `salida/entorno.txt`: versiones de python, numpy, pandas y de cualquier lector usado, y `uname -a`.
6. `salida/archivos-leidos.txt`: cada ruta que abriste, una por línea.
7. `salida/insuficiencias.md`: lo que la spec humana no alcanzó a fijar, por llave o grupo; «Ninguna.» si nada.

## Reglas

- Si falta método, acceso o un dato, informa el faltante sin adivinar (`NO-RECALCULABLE-DESDE-SPEC` con `motivo`).
- El primer resultado completo que produzca tu código es el que se entrega. No tienes valores esperados y no debes buscarlos.
- Al terminar, escribe el sha256 de cada archivo de `salida/` en `salida/SELLO.txt` y no modifiques nada después.
- La última línea de tu respuesta final es `RECONSTRUCCION-TERMINADA sha256(resultado.json)=<hex>`.
"""


for paq, cfg in PAQ.items():
    tar = CONT / f"{paq}-residuales-documentales-v2.tar.gz"
    ident = {"paquete": paq, "version_entrada": "residuales-documentales-v2", "sha256_entrada": sha(tar)}
    base = REC / paq
    if base.exists():
        raise SystemExit(f"PARO · ya existe {base}: no se sobrescribe")
    pk = base / "paquete"
    (pk / "datos").mkdir(parents=True)
    (base / "salida").mkdir()
    with tarfile.open(tar) as t:
        t.extractall(pk, filter="data")
    shutil.copyfile(CONTRATO, pk / "CONTRATO-v3.md")
    if sha(pk / "CONTRATO-v3.md") != CONTRATO_SHA:
        raise SystemExit("PARO · sha de CONTRATO-v3.md")
    ent = AQUI / paq / "entrada"
    shutil.copyfile(ent / "FIRMAS-Y-ACCESO.md", pk / "FIRMAS-Y-ACCESO.md")
    if cfg.get("zips"):
        for dst, (zp, zs) in cfg["zips"].items():
            with zipfile.ZipFile(R / zp) as z:
                (m,) = [i.filename for i in z.infolist() if i.filename.endswith(".dta")]
            extrae(zp, zs, m, pk / "datos" / dst)
        fuente = {k: {"zip": v[0], "zip_sha256": v[1]} for k, v in cfg["zips"].items()}
    else:
        for m, dst in cfg["miembros"].items():
            extrae(cfg["zip"], cfg["zip_sha"], m, pk / "datos" / dst)
        fuente = {"zip": cfg["zip"], "zip_sha256": cfg["zip_sha"], "miembros": cfg["miembros"]}
    n = sum(1 for _ in open(pk / "esquema-identidades.tsv", encoding="utf-8")) - 1
    files = sorted(p for p in pk.rglob("*") if p.is_file())
    allow = {"paquete": paq, "identidad": ident, "fuente_datos": fuente,
             "campos_autorizados": cfg["campos"],
             "herramientas": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"],
             "autorizacion": ["FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01",
                              "FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02",
                              "FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-03",
                              "FP-260927-GEN2-ASTRA6-C1-ENTRADAS-LOTE2-RESIDUALES-1-1653-01",
                              "acceso C1 firmado por mesa 28/sep (ver FIRMAS-Y-ACCESO.md)"],
             "input_files": [{"path": str(p.relative_to(base)), "sha256": sha(p)} for p in files]}
    canon = json.dumps(allow, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    (ent / "allowlist.json").write_text(json.dumps(allow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ent / "allowlist.canon.sha256").write_text(hashlib.sha256(canon.encode()).hexdigest() + "\n")
    (ent / "identidad.json").write_text(json.dumps(ident, ensure_ascii=False, sort_keys=True) + "\n")
    (ent / "tolerancia-v2.json").write_text('{"abs": "1e-10", "rel": "0"}\n')
    pr = prompt(paq, cfg, ident, n)
    (ent / "prompt.md").write_text(pr, encoding="utf-8")
    (REC / f"{paq}.prompt").write_text(pr, encoding="utf-8")
    for p in pk.rglob("*"):
        p.chmod(0o555 if p.is_dir() else 0o444)
    pk.chmod(0o555)
    print(paq, n, "llaves ·", len(files), "archivos · entrada", ident["sha256_entrada"][:12])
