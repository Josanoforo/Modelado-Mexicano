#!/usr/bin/env python3
"""ACTO GEN2-C1-SUCESORES-Y-LOTE-3 · P2 · tablas de R21, R24, R25 y R28.

Solo lee listas de identidades, rótulos de estado y columnas documentales. No abre
microdato ni valores de resultados (`punto`, `ic95_*` no se leen).

  R21 · r21-envipe-15-llaves.tsv     quince llaves ENVIPE de fb50-02 → PROPONER-SUSPENDER
  R24 · r24-transporte-ventana-767.tsv   ventana literal (columna `reserva`) del catálogo v1.2
  R25 · r25-cobertura-beee02.tsv     685 decisiones de 39de-01 contra la tabla de beee-02
  R28 · r28-130-no-ciegas.tsv        130 COINCIDE no ciegas del lote 2 (ENBIARE 126, ENCIG 4)

Uso: p2_tablas.py <dir-salida>
"""
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[3]
VI = R / "forense/validacion-independiente"
OUT = Path(sys.argv[1])


def lee(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def escribe(nombre, cols, filas):
    for f in filas:
        for c in cols:
            if "\t" in str(f[c]) or "\n" in str(f[c]):
                raise SystemExit(f"PARO · separador dentro de {nombre}:{c}")
    texto = "\t".join(cols) + "\n" + "".join("\t".join(str(f[c]) for c in cols) + "\n" for f in filas)
    (OUT / nombre).write_text(texto, encoding="utf-8")
    print(f"{nombre}: {len(filas)} filas · sha256 {hashlib.sha256(texto.encode()).hexdigest()}")


# R21 ---------------------------------------------------------------------------
src21 = VI / "catalogo-1-impedimentos-lote2/p2/impedimentos-lote2-p2-envipe15-retiro-sucesor.tsv"
cons21 = VI / "catalogo-1-impedimentos-lote2/p2/impedimentos-lote2-p2-envipe15-consumidores.tsv"
f21 = lee(src21)
n_cons = Counter(r["result_id"] for r in lee(cons21))
if len(f21) != 15 or len({r["llave_historica"] for r in f21}) != 15:
    raise SystemExit("PARO · R21: la fuente no tiene 15 llaves distintas")
escribe("r21-envipe-15-llaves.tsv",
        ["llave_historica", "estado_c1", "propuesta_catalogo", "llave_sucesora_propuesta",
         "ola_sucesora", "unidad_sucesora", "consumidores_por_identidad", "fuente_sha256"],
        [{"llave_historica": r["llave_historica"],
          "estado_c1": "RETIRADA-DEL-UNIVERSO-C1 (fb50-02, R21)",
          "propuesta_catalogo": "PROPONER-SUSPENDER · sucesor por CALC nuevo · CIERRE-SEMANAL-3",
          "llave_sucesora_propuesta": r["llave_sucesora_propuesta"],
          "ola_sucesora": r["ola_sucesora"], "unidad_sucesora": r["unidad_sucesora"],
          "consumidores_por_identidad": n_cons.get(r["llave_historica"], 0),
          "fuente_sha256": sha(src21)} for r in f21])

# R24 ---------------------------------------------------------------------------
src24 = VI / "catalogo-1-incertidumbre-spec/p3/identidades-799.tsv"
cat = R / "canon/catalogo-del-mexicano-v1_2.tsv"
ids = [r for r in lee(src24) if r["clase_sucesor"] == "RESTAURACION-DE-TRANSPORTE-DOCUMENTADA"]
with open(cat, encoding="utf-8", newline="") as fh:
    reserva = {r["llave"]: r["reserva"] for r in csv.DictReader(fh, delimiter="\t")}
filas24 = []
for r in ids:
    if r["llave"] not in reserva:
        raise SystemExit(f"PARO · R24: {r['llave']} no está en el catálogo v1.2")
    lit = reserva[r["llave"]]
    if not lit.endswith("ventana=" + r["ventana_demostrada"]):
        raise SystemExit(f"PARO · R24: {r['llave']}: `reserva` no termina en la ventana demostrada")
    filas24.append({"llave": r["llave"], "paquete": r.get("paquete", ""),
                    "ventana_literal_catalogo_v1_2": lit,
                    "metodo": "SIN-CAMBIO", "estado_historico": "SIN-CAMBIO (DISCREPA/NO-RECALCULABLE histórico intacto)",
                    "catalogo_sha256": sha(cat), "fuente_sha256": sha(src24)})
if len(filas24) != 767:
    raise SystemExit(f"PARO · R24: {len(filas24)} identidades, no 767")
escribe("r24-transporte-ventana-767.tsv",
        ["llave", "paquete", "ventana_literal_catalogo_v1_2", "metodo", "estado_historico",
         "catalogo_sha256", "fuente_sha256"], filas24)

# R25 ---------------------------------------------------------------------------
src25 = VI / "catalogo-1-adjudicacion-puntos/decisiones-por-objeto.tsv"
b02 = R / "forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/2026-09-27-gen2-recibo-astra6-1--tabla-result-estado-efecto.tsv"
trato = {r["llave"]: r["recomendacion"] for r in lee(b02)}
filas25 = []
for r in lee(src25):
    k = r["identidad_original"]
    cub = trato.get(k, "")
    filas25.append({"identidad_original": k, "decision_recomendada": r["decision_recomendada"],
                    "motivo": r["motivo"], "trato_beee02": cub or "NO-CUBIERTA",
                    "retiro_temporal_R25": "NO-APLICA (cubierta por beee-02)" if cub else "APLICA",
                    "fuente_sha256": sha(src25), "beee02_sha256": sha(b02)})
print("R25 · decisiones", dict(Counter(f["decision_recomendada"] for f in filas25)),
      "· trato beee-02", dict(Counter(f["trato_beee02"] for f in filas25)))
escribe("r25-cobertura-beee02.tsv",
        ["identidad_original", "decision_recomendada", "motivo", "trato_beee02",
         "retiro_temporal_R25", "fuente_sha256", "beee02_sha256"], filas25)

# R28 ---------------------------------------------------------------------------
src28 = VI / "catalogo-1-ejecucion-lote2/lote2-tabla-estimadores.tsv"
led = R / "data/corrida0/validaciones-independientes.tsv"
asiento = {(r["spec_id"], r["resultado_id"]): r["validacion_independiente"] for r in lee(led)}
filas28 = []
for r in lee(src28):
    if r["instrumento"] in ("ENBIARE", "ENCIG") and r["estado_punto"] == "COINCIDE":
        filas28.append({"llave": r["llave"], "calc": r["calc"], "instrumento": r["instrumento"],
                        "estado_lote2": "CONCUERDA-NO-APROBADA", "rotulo": "NO-CIEGA-PENDIENTE",
                        "asiento_vigente": asiento.get((r["calc"], r["llave"]), "SIN-ASIENTO"),
                        "recomparacion": ("LOTE-3 paquete enbiare-pisos-bienestar-0001"
                                          if r["instrumento"] == "ENBIARE" else
                                          "SIN-PAQUETE-EN-LOTE-3 (ENCIG sin acceso C1 firmado)"),
                        "fuente_sha256": sha(src28)})
c28 = Counter(f["instrumento"] for f in filas28)
if dict(c28) != {"ENBIARE": 126, "ENCIG": 4}:
    raise SystemExit(f"PARO · R28: {dict(c28)} ≠ ENBIARE 126 · ENCIG 4")
print("R28 · asiento vigente", dict(Counter((f["instrumento"], f["asiento_vigente"]) for f in filas28)))
escribe("r28-130-no-ciegas.tsv",
        ["llave", "calc", "instrumento", "estado_lote2", "rotulo", "asiento_vigente",
         "recomparacion", "fuente_sha256"], filas28)
