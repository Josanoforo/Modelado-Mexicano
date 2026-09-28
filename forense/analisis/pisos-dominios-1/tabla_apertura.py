"""P1 de ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · tabla de apertura, derivada.

Universo (encargo §1 P1), sin teclear:
  · dominios sin estimador = dominios de canon/mapa-dominios-v1_1.tsv menos los que
    cuenta `cifra_v1_5.py mapa11_dominios_medidos` (intersección con el catálogo v1.3);
    por cada uno, sus afirmaciones con dictamen MEDIBLE-EN-CORPUS.
  · reglas = filas SIN-CIFRA-GEN2 de canon/reglas-contrastadas-v1_0.tsv cuya columna
    `instrumento_sugerido` no es vacía, «NO-APLICA*» ni «ninguno*», y cuyo dominio no es
    GENETICA (firewall §3).
Reserva por id: tools/corpus_loader.motivo_reserva (manifiesto + reservas firmadas).

La columna `pieza` y `decision` son la asignación del ejecutor (latitud §6 del encargo),
declarada aquí antes de todo COMMIT-1. Uso: python3 tabla_apertura.py [--escribe]
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import corpus_loader  # noqa: E402

OUT = Path(__file__).with_name("tabla-apertura-v1_0.tsv")


def lee(p):
    with open(ROOT / p, newline="", encoding="utf-8") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


# Asignación por afirmación/regla -> (pieza, payload_id, decision). Pieza = instrumento×ola.
AFIRMACIONES = {
    "ASTRA5-U0-AUTOR-001": ("P-ENCUCI2020", "encuci2020_bd_dbf", "MEDIR"),
    "ASTRA5-U0-AUTOR-002": ("P-ENCUCI2020", "encuci2020_bd_dbf", "MEDIR"),
    "ASTRA5-U0-AUTOR-003": ("P-ENCUCI2020", "encuci2020_bd_dbf", "MEDIR"),
    "ASTRA5-U0-AUTOR-010": ("P-ENCUCI2020", "encuci2020_bd_dbf", "MEDIR"),
    "ASTRA5-U0-AUTOR-030": ("P-ENCUCI2020", "encuci2020_bd_dbf", "MEDIR"),
    "ASTRA5-U0-AUTOR-031": ("P-ENCUCI2020", "encuci2020_bd_dbf", "MEDIR"),
    "ASTRA5-U0-AUTOR-004": ("—", "", "DIFERIDO: WVS ola 7 sin payload de microdato identificado por id en el manifiesto; PISOS-DOMINIOS-Y-REGLAS-2"),
    "ASTRA5-U0-AUTOR-021": ("P-CPV2020-ITER", "cpv2020_iter_nal_csv", "MEDIR"),
    "ASTRA5-U0-AUTOR-026": ("P-LATINOBAROMETRO", "latinobarometro2023_bd_stata_zip", "MEDIR"),
    "ASTRA5-U0-HUM-006": ("P-LATINOBAROMETRO", "latinobarometro2024_bd_stata", "MEDIR"),
    "ASTRA5-U0-TIME-001": ("—", "enif2024_csv", "DIFERIDO-A apertura: ENIF 2024 reservada por id (R06); pisos ENIF sellados se citan (E.5)"),
    "ASTRA5-U0-TIME-002": ("P-ENUT2024", "enut2024_bd_csv", "MEDIR"),
    "ASTRA5-U0-TIME-020": ("P-ENUT2024", "enut2024_bd_csv", "MEDIR (citar CALC-ENUT2024-* sellados donde coincida, E.5)"),
    "ASTRA5-U0-VEJEZ-009": ("P-ENUT2024", "enut2024_bd_csv", "MEDIR"),
    "ASTRA5-U0-VEJEZ-032": ("P-ENUT2024", "enut2024_bd_csv", "MEDIR (parte a); parte b CONAPO: NO-CONSTRUIBLE aquí"),
    "ASTRA5-U0-RURAL-002": ("P-ENUT2024", "enut2024_bd_csv", "MEDIR (ENUT 2024; ENUT 2019 como ola previa por eje)"),
    "ASTRA5-U0-RURAL-026": ("P-CPV2020-ITER", "cpv2020_iter_nal_csv", "MEDIR"),
    "ASTRA5-U0-RURAL-027": ("P-CPV2020-ITER", "cpv2020_iter_nal_csv", "MEDIR"),
    "ASTRA5-U0-FAM-037": ("P-CPV2020-ITER", "cpv2020_iter_nal_csv", "MEDIR (parte indígena Oaxaca); pobreza CONEVAL: NO-CONSTRUIBLE aquí"),
    "ASTRA5-U0-RURAL-041": ("—", "enasem2024_bd_csv_zip", "DIFERIDO: PISOS-DOMINIOS-Y-REGLAS-2 (tope de sesión CACHE-PARQUET-1)"),
    "ASTRA5-U0-SALMEN-032": ("—", "", "DIFERIDO: PISOS-DOMINIOS-Y-REGLAS-2 (tope de sesión)"),
    "ASTRA5-U0-TEC-010": ("P-ENADID2023", "enadid2023_base_datos_csv", "MEDIR"),
    "ASTRA5-U0-TIME-027": ("P-CPV2020-ITER", "cpv2020_iter_nal_csv", "MEDIR"),
    "ASTRA5-U0-JUV-001": ("P-EDER2025", "eder2025_bd_csv_zip", "MEDIR"),
    "ASTRA5-U0-JUV-002": ("P-EDER2025", "eder2025_bd_csv_zip", "MEDIR"),
    "ASTRA5-U0-TRAB-022": ("—", "", "DIFERIDO: ENOE NO-LANZAR-TODAVÍA (MEMORIA-OPERATIVA §1)"),
    "ASTRA5-U0-SANC-007": ("P-ENSU2024", "ensu2024_bd_csv_zip", "MEDIR"),
    "ASTRA5-U0-SANC-008": ("—", "", "NO-CONSTRUIBLE aquí: ENVE 2024 sólo como DDI en el manifiesto (enve2024_rnm1058_ddi), sin microdato"),
    "ASTRA5-U0-DUEL-001": ("—", "", "NO-CONSTRUIBLE como piso: acto documental ONU (CED/C/MEX/A.34/D/1), sin cuestionario"),
    "ASTRA5-U0-DUEL-002": ("—", "", "NO-CONSTRUIBLE como piso: acto documental ONU"),
    "ASTRA5-U0-DUEL-003": ("—", "", "NO-CONSTRUIBLE como piso: acto documental ONU"),
}

# Reglas: sólo las que predicen conducta observable con reactivo en el corpus entran a pieza.
# El resto (prescriptivas/metodológicas, ya NO-CONSTRUIBLE por REGLAS-Y-RESULT-1 por texto)
# se listan con decision = SIGUE-SIN-CIFRA y la razón de la v1.0, no re-dictaminadas.
REGLAS = {
    "RG-67c84a2224": ("P-ENCUCI2020", "encuci2020_bd_dbf", "CONTRASTAR (derecho × autonomía de voto; E.5: citar CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001)"),
    "RG-3920de961d": ("P-ENUT2024", "enut2024_bd_csv", "CONTRASTAR (trabajo comunitario gratuito rural/indígena vs urbano; unidad persona)"),
    "RG-b91375cbd5": ("P-ENVIPE2025", "envipe2025_csv", "CONTRASTAR (organización con vecinos por inseguridad × estrato socioeconómico)"),
    "RG-cc1c9ab8f1": ("P-ENIGH2022", "enigh2022_nc_csv", "CONTRASTAR (gasto en colegiaturas privadas por decil; motivo no observable → sólo conducta)"),
    "RG-7c6dd83a03": ("P-INE", "", "CONTRASTAR (participación presidencial 2018/2024; unidad lista nominal)"),
    "RG-b723d6e18b": ("P-INE", "", "CONTRASTAR (abstención elección judicial 2025; unidad lista nominal)"),
    "RG-34a21bc6a2": ("—", "enif2024_csv", "INCOMPARABLE: ENIF no registra tipo de organizador de la tanda (enlace que falta: reactivo de organizador conocido/desconocido)"),
    "RG-145b91d071": ("—", "", "INCOMPARABLE: unidad comunidad; enlace que falta: registro de autodefensas por municipio"),
}


def main(escribe: bool) -> int:
    mapa = lee("canon/mapa-dominios-v1_1.tsv")
    cat = {r["dominio"] for r in lee("canon/catalogo-del-mexicano-v1_3.tsv")}
    doms = {r["dominio"] for r in mapa}
    faltan = sorted(doms - cat)
    man = corpus_loader.manifiesto()
    filas = []
    for r in mapa:
        if r["dominio"] not in faltan or r["dictamen"] != "MEDIBLE-EN-CORPUS":
            continue
        pieza, pid, dec = AFIRMACIONES.get(r["id_afirmacion"], ("—", "", "SIN-ASIGNAR"))
        filas.append({
            "dominio": r["dominio"], "clase": "afirmacion", "id": r["id_afirmacion"],
            "instrumento_ola": r["instrumento_ola"][:120], "payload_id": pid,
            "reactivo": (r["pregunta_textual_codigo_respuestas"] or r["texto_pregunta_v1_1"])[:200],
            "unidad": r["conducta_unidad_universo"][:120],
            "reserva": (corpus_loader.motivo_reserva(pid, man.get(pid)) or "LIBRE") if pid else "NO-APLICA",
            "pieza": pieza, "decision": dec})
    reglas = lee("canon/reglas-contrastadas-v1_0.tsv")
    for r in reglas:
        ins = r["instrumento_sugerido"].strip()
        if r["dictamen"] != "SIN-CIFRA-GEN2" or not ins or ins.startswith("NO-APLICA") \
                or re.match(r"ningun", ins, re.I) or r["dominio_catalogo"] == "GENETICA":
            continue
        pieza, pid, dec = REGLAS.get(r["regla_id"], (
            "—", "", "SIGUE-SIN-CIFRA: " + r["detalle_dictamen"].split("·")[0].strip()[:160]))
        filas.append({
            "dominio": r["dominio_catalogo"], "clase": "regla", "id": r["regla_id"],
            "instrumento_ola": ins[:120], "payload_id": pid,
            "reactivo": (r["segmento_si"] + " → " + r["conducta_entonces"])[:200],
            "unidad": r["unidad"] or "—",
            "reserva": (corpus_loader.motivo_reserva(pid, man.get(pid)) or "LIBRE") if pid else "NO-APLICA",
            "pieza": pieza, "decision": dec})
    sin = [f["id"] for f in filas if f["decision"] == "SIN-ASIGNAR"]
    c = Counter((f["clase"], f["pieza"] != "—") for f in filas)
    print(f"dominios_sin_estimador={len(faltan)} {faltan}")
    print(f"afirmaciones={sum(v for (k, _), v in c.items() if k == 'afirmacion')} "
          f"en_pieza={c[('afirmacion', True)]} · reglas_candidatas={sum(v for (k, _), v in c.items() if k == 'regla')} "
          f"en_pieza={c[('regla', True)]} · sin_asignar={len(sin)} {sin}")
    print("piezas:", dict(Counter(f["pieza"] for f in filas if f["pieza"] != "—")))
    if escribe:
        with open(OUT, "w", newline="", encoding="utf-8") as s:
            w = csv.DictWriter(s, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(filas)
        print("escrito", OUT.relative_to(ROOT))
    return 1 if sin else 0


if __name__ == "__main__":
    sys.exit(main("--escribe" in sys.argv))
