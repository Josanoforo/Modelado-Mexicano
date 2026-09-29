#!/usr/bin/env python3
"""construye_dictamen_pendientes_4.py -- ACTO GEN2-PENDIENTES-4: convierte el estado final de cada
NC (arma_dictamen_pendientes_4.estado_final) en `dictamen-pendientes-4.tsv`, que aplica
`aplica_dictamen_pendientes_4.py` sobre el libro. No escribe el libro.

Entradas: el directorio de evidencia con los `*.research.json` / `*.verif-*.json` y un
`grupos-pendientes-4.json` con las decisiones de agrupación del ejecutor (supervisor):
  {"encargos":   {"<ROTULO>": ["NC-…", …]},            # ABSORBER -> DIRECCION-ENCARGO (<ROTULO>)
   "decisiones": {"D1": ["NC-…", …]},                  # HOJA-DECISION -> MESA-DECISION (<hoja>#D1)
   "recetas":    {"NC-…": "2026-10-05"},               # HOJA-RECETA -> MESA-ACCION (<fecha>); por defecto FECHA_ACCION
   "manual":     {"NC-…": {"accion": "DUENO|CERRAR|NADA", "nuevo_sucesor": "…", "cerrado_por": "…", "porque": "…"}}}
`manual` gana sobre todo lo demás (para los casos que el supervisor decide fila por fila).

Guardas (fallan en voz alta):
  * ninguna NC ABIERTA queda sin acción (salvo MANTENER-DUENO con dueño ya válido);
  * un CERRAR-DUPLICADA no puede apuntar a una NC que este acto también cierra como duplicada
    (doble cierre: la deuda desaparecería de las dos filas);
  * `cerrado_por` sin paréntesis anidados (los lectores de dictamen cortan en el primer «)»).

    python3 construye_dictamen_pendientes_4.py <dir-res> <grupos.json> <salida.tsv>
"""
import csv
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arma_dictamen_pendientes_4 as AD  # noqa: E402

ACTO = "GEN2-PENDIENTES-4"
HOJA_DECISIONES = "forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md"
FECHA_ACCION = "2026-10-05"
CANAL = "CANAL (derivados/auto-*)"
TIPO = {"CERRAR-PRODUCTO": "producto", "CERRAR-DISENO": "diseño", "CERRAR-FIRMA": "firma",
        "CERRAR-DUPLICADA": "duplicada"}
RE_NC = re.compile(r"NC-(?:\d{4}|\d{6}-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9a-f]{4}-\d{2})")


def detalle_limpio(txt, tipo):
    t = (txt or "").strip()
    t = re.sub(rf"^(?:por )?{tipo}\s*:\s*", "", t, flags=re.I)
    t = t.replace("(", "[").replace(")", "]").replace("\t", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", t)[:460].strip()


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    res, grupos_p, salida = sys.argv[1:4]
    grupos = json.load(open(grupos_p, encoding="utf-8")) if os.path.exists(grupos_p) else {}
    a_enc = {i: r for r, ids in grupos.get("encargos", {}).items() for i in ids}
    a_dec = {i: d for d, ids in grupos.get("decisiones", {}).items() for i in ids}
    fechas = grupos.get("recetas", {})
    manual = grupos.get("manual", {})
    fin = AD.estado_final(AD.carga(res))
    libro = {r["id"]: r for r in csv.DictReader(open(os.path.join(RAIZ, "forense", "no-corrido.tsv"),
                                                       newline="", encoding="utf-8"), delimiter="\t")}
    filas, sin_accion, errores = [], [], []
    cierra_dup = {}
    for i, f in sorted(fin.items()):
        if libro.get(i, {}).get("estado") != "ABIERTA":
            continue
        r, est = f["fila"], f["estado"]
        origen = f"{f['key']}:{r['verdict']}"
        if i in manual:
            m = manual[i]
            filas.append([i, origen + "+MANUAL", m["accion"], m.get("cerrado_por", ""), m.get("nuevo_sucesor", ""),
                          m.get("porque", "")])
            continue
        if est == "CERRAR":
            tipo = TIPO[r["verdict"]]
            det = detalle_limpio(r.get("cerrado_por_detalle"), tipo)
            if "(" in det or ")" in det or not det:
                errores.append(f"{i}: detalle de cierre vacío o con paréntesis")
            if tipo == "duplicada":
                cierra_dup[i] = set(RE_NC.findall(det)) - {i}
            filas.append([i, origen, "CERRAR", f"{ACTO} · CERRADA ({tipo}: {det})", "", r.get("rationale", "")[:200]])
        elif est == "ABSORBER":
            if i in a_enc:
                filas.append([i, origen, "DUENO", "", f"DIRECCION-ENCARGO ({a_enc[i]})", r.get("que_falta", r.get("rationale", ""))[:200]])
            else:
                sin_accion.append((i, "ABSORBER sin encargo asignado"))
        elif est == "HOJA-RECETA":
            filas.append([i, origen, "DUENO", "", f"MESA-ACCION ({fechas.get(i, FECHA_ACCION)})", r.get("rationale", "")[:200]])
        elif est == "HOJA-DECISION":
            if i in a_dec:
                filas.append([i, origen, "DUENO", "", f"MESA-DECISION ({HOJA_DECISIONES}#{a_dec[i]})", r.get("rationale", "")[:200]])
            else:
                sin_accion.append((i, "HOJA-DECISION sin renglón asignado"))
        elif est == "CANAL":
            filas.append([i, origen, "DUENO", "", CANAL, r.get("rationale", "")[:200]])
        elif est == "MANTENER-DUENO":
            filas.append([i, origen, "NADA", "", "", r.get("rationale", "")[:200]])
        else:
            sin_accion.append((i, f"estado {est} sin acción (segunda pasada o verificación pendiente)"))
    # ninguna NC ABIERTA sin fila ni motivo
    ya = {f[0] for f in filas} | {i for i, _ in sin_accion}
    for i, r in libro.items():
        if r["estado"] == "ABIERTA" and i not in ya:
            sin_accion.append((i, "sin estado de investigación"))
    # doble cierre entre duplicadas
    for i, objetivos in cierra_dup.items():
        for x in objetivos:
            if x in cierra_dup and i in cierra_dup[x]:
                errores.append(f"doble cierre: {i} y {x} se cierran como duplicadas una de la otra")
            elif x in cierra_dup:
                errores.append(f"cadena de duplicadas: {i} -> {x} (que también se cierra como duplicada): revisar")
    with open(salida, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["id", "propuesta_evidencia", "accion", "cerrado_por", "nuevo_sucesor", "porque"])
        for f in filas:
            w.writerow([c.replace("\t", " ").replace("\n", " ") for c in f])
    print(f"dictamen: {len(filas)} filas → {salida}")
    from collections import Counter
    print("acciones:", dict(Counter(f[2] for f in filas)))
    print(f"SIN ACCIÓN: {len(sin_accion)}")
    for i, m in sin_accion[:60]:
        print(f"  {i}: {m}")
    for e in errores:
        print("ERROR:", e)
    return 1 if (errores or sin_accion) else 0


if __name__ == "__main__":
    sys.exit(main())
