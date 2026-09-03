#!/usr/bin/env python3
"""ACTO MAESTRA35-L6 · P1 · adopción de trámites de gobierno por internet, ENDUTIH.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA35-L6-spec.md` §1 (COMMIT-1).

QUÉ MIDE, Y QUÉ NO. Mide la proporción ponderada de personas usuarias de
internet que usaron internet para REALIZAR TRÁMITES DEL GOBIERNO (`P7_35_4`),
sobre las tres olas de ENDUTIH del corpus. **No es** la `p` de
`tramite.gobierno_digital.coercitivo` (ADR-287 sigue en pie: la situación
coercitiva no está en el instrumento — ver el censo P0 §3). Es la cifra que la
`estampa A.10` de la regla espejo `tramite.gobierno_digital.util_sin_coercion`
declara expresamente no haber medido: «No es la adopción de gobierno digital en
México» (milpa/tramite.yaml).

Unidad = persona usuaria elegida. Universo = `P7_1 == '1'`. Ponderador
`FAC_PER`, diseño `EST_DIS × UPM_DIS`, bootstrap conglomerado n_boot=10000
seed=42 (mismo estimador que el resto del programa, importado y no
reimplementado).
"""
import hashlib
import json
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calibracion_mordida_encig_serie import wprop_ic_conglomerado  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
sys.path.insert(0, os.path.join(RAIZ, "tests"))
from dbfmini import field_names, read_dbf  # noqa: E402

# El miembro de 2025 NO se llama tic_2025_usuarios.DBF -- verificado, no inferido.
OLAS = [
    ("2025", "endutih2025/endutih2025_bd_dbf.zip", "ti25usu.dbf", "PRINCIPAL"),
    ("2024", "endutih2024/endutih2024_bd_dbf.zip", "tic_2024_usuarios.DBF", "sensibilidad de ola"),
    ("2023", "endutih2023/endutih2023_bd_dbf.zip", "tic_2023_usuarios.DBF", "sensibilidad de ola"),
]

GOB = ["P7_35_1", "P7_35_2", "P7_35_3", "P7_35_4"]
CAMPOS = ["P7_1"] + GOB + ["FAC_PER", "EST_DIS", "UPM_DIS"]

MIN_ESTRATOS = 100
MIN_UPM = 100


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def paro(msg):
    raise SystemExit(f"PARO · {msg}")


def carga(zpath, member):
    """Extrae el DBF a un temporal y devuelve la lista de registros pedidos."""
    with zipfile.ZipFile(zpath) as z:
        nombres = [n.filename for n in z.infolist()]
        if member not in nombres:
            paro(f"{member} no está en {zpath}; miembros = {nombres}")
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as td:
            destino = z.extract(member, td)
            campos = {n for n, _t, _l in field_names(destino)}
            faltan = [c for c in CAMPOS if c not in campos]
            if faltan:  # guardia 1
                paro(f"{member}: faltan columnas {faltan}")
            return list(read_dbf(destino, wanted_fields=CAMPOS))


def celda(filas, universo, desenlace, etiqueta):
    """Devuelve el dict de resultado de una celda, o PARA si el diseño colapsa."""
    d, w, est, upm = [], [], [], []
    for r in filas:
        if not universo(r):
            continue
        y = desenlace(r)
        if y is None:
            continue
        try:
            peso = float(r["FAC_PER"])
        except ValueError:
            paro(f"{etiqueta}: FAC_PER no numérico ({r['FAC_PER']!r})")  # guardia 2
        if peso <= 0:
            paro(f"{etiqueta}: FAC_PER no positivo ({peso})")            # guardia 2
        d.append(y)
        w.append(peso)
        est.append(r["EST_DIS"])
        upm.append(r["UPM_DIS"])
    if not d:
        paro(f"{etiqueta}: universo vacío")
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(d, w, est, upm)
    if n_est < MIN_ESTRATOS or n_cl < MIN_UPM:                            # guardia 4
        paro(f"{etiqueta}: diseño colapsado (estratos={n_est}, UPM={n_cl})")
    return {"etiqueta": etiqueta, "p": p, "ic95": [lo, hi], "n": n,
            "numerador": int(sum(d)), "estratos": n_est, "upm": n_cl,
            "poblacion_expandida": float(sum(w))}


def binaria(var):
    def f(r):
        v = r[var]
        if v == "1":
            return 1.0
        if v == "2":
            return 0.0
        return None
    return f


def union_gob(r):
    vals = [r[c] for c in GOB]
    if any(v == "1" for v in vals):
        return 1.0
    if all(v == "2" for v in vals):
        return 0.0
    return None


def main():
    salida = {"acto": "MAESTRA35-L6", "pieza": "P1",
              "spec": "forense/notas/2026-09-02-MAESTRA35-L6-spec.md §1",
              "estimador": "wprop_ic_conglomerado (n_boot=10000, seed=42)",
              "escala": ("proporcion ponderada de PERSONAS USUARIAS DE INTERNET "
                         "de 6 anios y mas; NO es la p de "
                         "tramite.gobierno_digital.coercitivo ni de "
                         "util_sin_coercion (universo construido distinto)"),
              "olas": []}
    for ola, rel, member, papel in OLAS:
        zpath = os.path.join(RAW, rel)
        filas = carga(zpath, member)

        idx_internet = {i for i, r in enumerate(filas) if r["P7_1"] == "1"}
        idx_p7354 = {i for i, r in enumerate(filas)
                     if r["P7_35_4"] in ("1", "2")}
        # guardia 3 -- la premisa ajena escrita como guardia, no como supuesto
        fuera = idx_p7354 - idx_internet
        sin_dato = idx_internet - idx_p7354
        if fuera or sin_dato:
            paro(f"ola {ola}: el universo de P7_35_4 NO coincide con P7_1=='1' "
                 f"(con dato fuera del universo={len(fuera)}, "
                 f"en universo sin dato={len(sin_dato)}). "
                 f"La spec §1 declara que coinciden; no se promedia sobre un "
                 f"universo que no es el declarado.")
        usa_internet = idx_internet

        principal = celda(filas, lambda r: r["P7_1"] == "1",
                          binaria("P7_35_4"),
                          f"{ola} principal · P7_35_4 | P7_1=1")
        sens_a = celda(filas, lambda r: r["P7_1"] == "1", union_gob,
                       f"{ola} sensibilidad A · union P7_35_1..4 | P7_1=1")

        def desenlace_b(r):
            if r["P7_1"] == "2":
                return 0.0
            return binaria("P7_35_4")(r)
        sens_b = celda(filas, lambda r: r["P7_1"] in ("1", "2"), desenlace_b,
                       f"{ola} sensibilidad B · universo ampliado")

        salida["olas"].append({
            "ola": ola, "papel": papel,
            "payload": os.path.relpath(zpath, RAIZ),
            "miembro": member,
            "sha256_payload": sha256(zpath),
            "n_tabla": len(filas),
            "n_usa_internet": len(usa_internet),
            "principal": principal,
            "sensibilidad_A_interaccion": sens_a,
            "sensibilidad_B_universo_ampliado": sens_b,
        })
        print(f"[{ola}] tabla={len(filas)} usa_internet={len(usa_internet)} "
              f"p={principal['p']:.6f} IC95={principal['ic95'][0]:.6f},"
              f"{principal['ic95'][1]:.6f} n={principal['n']} "
              f"estratos={principal['estratos']} UPM={principal['upm']}",
              flush=True)

    destino = os.path.join(RAIZ, "data", "l6-gobierno-digital-endutih-v1_0.json")
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"\nescrito: {os.path.relpath(destino, RAIZ)}")


if __name__ == "__main__":
    main()
