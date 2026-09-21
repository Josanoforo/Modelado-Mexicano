#!/usr/bin/env python3
"""ACTO GEN2-RELEVO-RECONCILIA-1 · P1 + P2.

Reconcilia los 173 slots `LEGACY-GEN1` de `data/corrida0/relevo-usos-v1_0.tsv`
contra la oferta GEN2 sellada **por identidad de slot**, nunca por su numero
`RES-####`.

Por que no por `RES`
====================
Los cuatro canales de descubrimiento de `tools/relevo_usos.py` (C1-MAPA,
C1-SINGULAR, C2-RESULTADO, C0-CONSUMIDOR) estan TODOS tecleados sobre el
token literal `RES-####` escrito en la spec del CALC. Y el `RES-####` es
POSICIONAL: su autoridad, `data/corrida0/demanda-resultados.tsv`, se deriva
por orden, asi que insertar un slot recorre a todos los de abajo (NC-0343:
37 filas corridas en uno al entrar el slot DIN). Una spec sellada NO se
puede editar (E.3), asi que su pin queda congelado apuntando a un numero
que ya es de otro slot. Resultado: el CALC esta sellado, el trabajo esta
hecho, y la vista no lo ve.

Este modulo NO MIDE, NO ADOPTA, NO ESCRIBE en `milpa/`, no toca ningun CALC
ni `prereg-duelo-v2/`, y no cambia ningun contador. Solo lee y deriva.

Identidad, por clase de consumidor
==================================
  marco del duelo (70 slots) · `marco-M-sorteado-v1_3.tsv:<id_celda>:<rol>`
      La identidad es la pareja (id_celda, rol), y esta escrita DENTRO de la
      oferta, no en su nombre:
        rol R        -> `parametros.id_celda` de los CALC-R sellados
                        (y `RESULT-TRIADA-<celda>-R` como segunda lectura).
        rol M        -> `RESULT-TRIADA-<celda>-M`
        rol L:L-solo -> `RESULT-TRIADA-<celda>-L-SOLO`
        rol L:L+corpus -> `RESULT-TRIADA-<celda>-L-CORPUS`
        rol AGREGADO -> se busca un RESULT de TRIADA con el agregado por
                        celda; si no existe, el slot queda SIN-REHACER.
      El id de celda viaja con GUION en el marco (`CIV-M-01`) y con GUION
      BAJO en los RESULT de TRIADA (`CIV_M_01`). Se normaliza; no se
      adivina nada mas.

  milpa/ y celdas-d (103 slots) · `<archivo>:<clave>[:<campo>]`
      La identidad es la CLAVE DEL CONSUMIDOR (p. ej.
      `tramite.mordida.discrecional`). Se busca esa clave, literal, en el
      texto de la spec de cada CALC sellado. Un acierto acredita que un CALC
      GEN2 sellado habla de ESE consumidor, y se reporta con el fragmento
      que lo acredita; no acredita por si solo que releve el slot — eso lo
      dice el casamiento de estimando, que es humano.

Vocabulario de salida (A.4)
===========================
  YA-REHECHO-EN-GEN2      hay valor GEN2 sellado para la identidad, y el
                          delta contra el legacy esta dentro de tolerancia.
  REHECHO-CON-DIFERENCIA  hay valor GEN2 sellado y el delta NO lo esta.
  SIN-REHACER             NO-ENCONTRADO en la oferta sellada, con el
                          universo examinado declarado (A.13).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tools"))
import corrida0  # noqa: E402

C0 = RAIZ / "data" / "corrida0"
SALIDA = Path(__file__).resolve().parent

# Tolerancia de delta. Declarada aqui, no tecleada desde un resultado:
# 1e-9 absoluto para "identico bit a bit salvo ruido de serializacion".
# Por encima de eso el slot es REHECHO-CON-DIFERENCIA y la diferencia se
# explica a mano. No se afloja para que algo case.
TOL_ABS = 1e-9


def _tsv(p: Path) -> list[dict]:
    lineas = [l for l in p.read_text(encoding="utf-8").splitlines(True)
              if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------- oferta
def indice_oferta() -> dict:
    """Todos los CALC del arbol, con su estado derivado por el comando de
    la casa (`corrida0.estado_calc`) — nunca por lectura de un campo."""
    calcs = {}
    for d in sorted(C0.iterdir()):
        if not d.is_dir() or not (d / "spec.yaml").exists():
            continue
        est = corrida0.estado_calc(d.name)
        try:
            spec = yaml.safe_load((d / "spec.yaml").read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            spec = {}
        res = {}
        rr = d / "resultados.json"
        if rr.exists():
            res = json.loads(rr.read_text(encoding="utf-8")).get("resultados", {})
        calcs[d.name] = {
            "estado": est.get("estado"),
            "spec": spec,
            "texto_spec": (d / "spec.yaml").read_text(encoding="utf-8"),
            "resultados": res,
            "cuenta_gen2": str((spec.get("etiquetas") or {}).get("cuenta_gen2", "")),
            "pins_res": sorted(set(re.findall(r"RES-\d{4}",
                                              (d / "spec.yaml").read_text(encoding="utf-8")))),
        }
    return calcs


def sellados(calcs: dict) -> dict:
    return {k: v for k, v in calcs.items() if v["estado"] == "SELLADA"}


# ----------------------------------------------------------- marco M
RE_MARCO = re.compile(r"marco-M-sorteado-v1_3\.tsv:([A-Z]+-M-\d\d):(.+)$")


def casa_marco(slot: dict, ofer: dict) -> dict | None:
    m = RE_MARCO.search(slot["consumidor"])
    if not m:
        return None
    celda, rol = m.group(1), m.group(2)
    celda_u = celda.replace("-", "_")

    if rol == "R":
        # por `parametros.id_celda`, no por el nombre del CALC
        cands = [(cid, c) for cid, c in ofer.items()
                 if (c["spec"].get("parametros") or {}).get("id_celda") == celda
                 and str((c["spec"].get("etiquetas") or {}).get("tipo", "")).startswith("ARBITRO-R")]
        if not cands:
            return {"como": "id_celda", "calc": None}
        cid, c = sorted(cands)[-1]           # ultima version sellada
        rid = f"RESULT-R-{celda}-PUNTO"
        return {"como": "parametros.id_celda", "calc": cid, "result": rid,
                "valor": c["resultados"].get(rid), "pins_res": c["pins_res"],
                "clase_relevo": "RE-MEDIDO-EN-GEN2"}

    suf = {"M": "M", "L:L-solo": "L-SOLO", "L:L+corpus": "L-CORPUS",
           "AGREGADO": None}.get(rol)
    tri = ofer.get("CALC-TRIADA-0001")
    if tri is None:
        return {"como": "TRIADA", "calc": None}
    if suf is None:
        # AGREGADO: se busca, no se supone. Cualquier RESULT de TRIADA de
        # esta celda que NO sea R / M / L / control.
        agr = [k for k in tri["resultados"]
               if k.startswith(f"RESULT-TRIADA-{celda_u}-")
               and k.split("-")[-1] in ("AGREGADO", "Z", "ZSCORES")]
        if not agr:
            return {"como": "TRIADA", "calc": "CALC-TRIADA-0001", "result": None,
                    "valor": None, "pins_res": tri["pins_res"],
                    "nota": "NO-ENCONTRADO: CALC-TRIADA-0001 no emite agregado por celda"}
        k = agr[0]
        return {"como": "TRIADA", "calc": "CALC-TRIADA-0001", "result": k,
                "valor": tri["resultados"][k], "pins_res": tri["pins_res"]}
    rid = f"RESULT-TRIADA-{celda_u}-{suf}"
    presente = rid in tri["resultados"]
    # La spec de TRIADA declara, RESULT por RESULT, de donde sale cada punto:
    #   -R       "citado de data/corrida0/CALC-R-<celda>/resultados.json"  -> re-medido
    #   -M       "punto del snapshot sellado"                              -> ingerido
    #   -L-*     "mediana de replicas EXTRAIBLE"                           -> re-derivado
    # No se colapsan (§2, tres hallazgos distintos).
    clase = {"M": "INGERIDO-CON-CADENA-NO-RE-MEDIDO",
             "L-SOLO": "RE-DERIVADO-EN-GEN2",
             "L-CORPUS": "RE-DERIVADO-EN-GEN2"}[suf]
    val = tri["resultados"].get(rid)
    nota = ""
    if not presente:
        nota = ("NO-ENCONTRADO: CALC-TRIADA-0001 no emite este RESULT "
                f"({rid}) — el mecanismo no cubre esta identidad")
    elif val is None:
        nota = ("CORRIDO-SIN-PUNTO: el RESULT existe y vale null — el "
                "mecanismo SI corrio contra esta celda y no produjo punto. "
                + str(tri["resultados"].get(f"RESULT-TRIADA-{celda_u}-NOTA-DE-CORTE", "")))
    return {"como": "TRIADA·id_celda", "calc": "CALC-TRIADA-0001", "result": rid,
            "valor": val, "pins_res": tri["pins_res"],
            "clase_relevo": clase if val is not None else "NO-APLICA",
            "nota": nota}


# ------------------------------------------------------- milpa / celdas-d
def clave_consumidor(cons: str) -> str:
    partes = cons.split(":")
    return partes[1] if len(partes) > 1 else ""


def casa_consumidor(slot: dict, ofer: dict) -> dict:
    """Busca la CLAVE del consumidor, literal, en el texto de cada spec
    sellada. Es identidad de consumidor, no numero de RES."""
    clave = clave_consumidor(slot["consumidor"])
    if not clave or len(clave) < 4:
        return {"como": "clave-consumidor", "calc": None,
                "nota": "clave de consumidor vacia o demasiado corta para buscar"}
    hits = sorted(cid for cid, c in ofer.items() if clave in c["texto_spec"])
    if not hits:
        return {"como": "clave-consumidor", "calc": None}
    return {"como": "clave-consumidor", "calc": ";".join(hits), "result": None,
            "valor": None,
            "pins_res": sorted({p for h in hits for p in ofer[h]["pins_res"]})}


# -------------------------------------------------------------- P2 causa
def causa_ceguera(slot: dict, casado: dict, ofer: dict) -> str:
    """Por que la vista no enlaza este slot, dado que la oferta existe.

    Las categorias no se colapsan. En particular, un slot que la vista
    declara NO-ADOPTABLE por un VEREDICTO SELLADO no es ceguera: la vista
    lo ve, lo lee y lo obedece. Contarlo como ceguera inflaria el hallazgo.
    """
    if str(slot.get("veredicto", "")).startswith("NO-ADOPTABLE-POR-VEREDICTO-SELLADO"):
        return "NO-ES-CEGUERA-VEREDICTO-SELLADO-OBEDECIDO"
    if not casado or not casado.get("calc"):
        return "SIN-OFERTA-QUE-VER"
    if casado.get("como") == "clave-consumidor":
        # El casamiento fue por clave de consumidor, no por identidad de
        # celda: varios CALC pueden aparecer y el pin de uno de ellos no
        # dice nada sobre este slot. No se evalua.
        return "CANDIDATO-POR-CLAVE-PIN-NO-EVALUADO"
    calc = casado["calc"].split(";")[0]
    pins = ofer[calc]["pins_res"]
    rid = slot["resultado_id"]
    if not pins:
        return "CALC-SIN-PIN"
    if rid in pins:
        return "PIN-CORRECTO-CEGUERA-DE-OTRA-CAUSA"
    return f"PIN-A-RES-AJENO:{','.join(pins)}"


def main() -> int:
    relevo = _tsv(C0 / "relevo-usos-v1_0.tsv")
    demanda = {r["resultado_id"]: r for r in _tsv(C0 / "demanda-resultados.tsv")}
    corridas = {r["corrida_id"]: r for r in _tsv(C0 / "demanda-corridas.tsv")}
    legacy = [r for r in relevo if r["generacion_hoy"] == "LEGACY-GEN1"]

    calcs = indice_oferta()
    ofer = sellados(calcs)
    # Un candidato exige, ademas de SELLADA, cuenta_gen2 = SI (misma regla
    # que relevo_usos.py; no se afloja aqui).
    ofer = {k: v for k, v in ofer.items() if v["cuenta_gen2"] == "SI"}

    filas = []
    for s in legacy:
        casado = casa_marco(s, ofer)
        clase = "marco-del-duelo"
        if casado is None:
            casado = casa_consumidor(s, ofer)
            cons = s["consumidor"]
            clase = ("motor" if cons.startswith("milpa/tramite.yaml")
                     or cons.startswith("milpa/src/") else
                     "procedencia" if cons.startswith("milpa/procedencia.yaml") else
                     "catalogo-de-momentos" if "catalogo-momentos" in cons else
                     "celdas-D")
        valor_gen2 = casado.get("valor")
        valor_leg = _num(s["valor_legacy"])
        v2 = _num(valor_gen2)
        delta = (v2 - valor_leg) if (v2 is not None and valor_leg is not None) else None

        nota_c = casado.get("nota", "")
        if v2 is None and nota_c.startswith("CORRIDO-SIN-PUNTO"):
            estado = "SIN-REHACER"          # mecanismo corrido, sin punto
        elif v2 is None and nota_c.startswith("NO-ENCONTRADO"):
            estado = "SIN-REHACER"          # mecanismo no cubre la identidad
        elif v2 is None and casado.get("calc"):
            # Hay oferta GEN2 sellada que nombra esta identidad, pero este
            # acto NO extrajo de ella un valor comparable: casar el estimando
            # es trabajo de texto en cinco dimensiones, no de script, y
            # A-bis.3/4 prohiben aparear cifras sin enlace declarado.
            estado = "CANDIDATO-POR-IDENTIDAD-SIN-CASAR"
        elif v2 is None:
            estado = "SIN-REHACER"
        elif delta is not None and abs(delta) <= TOL_ABS:
            estado = "YA-REHECHO-EN-GEN2"
        else:
            estado = "REHECHO-CON-DIFERENCIA"

        corr = corridas.get(s["corrida_natural"], {})
        filas.append({
            "resultado_id": s["resultado_id"],
            "consumidor": s["consumidor"],
            "clase_consumidor": clase,
            "tipo_uso": s["tipo_uso"],
            "estado_reconciliacion": estado,
            "clase_de_relevo": casado.get("clase_relevo", "NO-APLICA"),
            "como_se_caso": casado.get("como", ""),
            "calc_gen2": casado.get("calc") or "",
            "result_gen2": casado.get("result") or "",
            "valor_gen2": "" if valor_gen2 is None else repr(valor_gen2),
            "valor_legacy": s["valor_legacy"],
            "delta_gen2_menos_legacy": "" if delta is None else repr(delta),
            "veredicto_vista_hoy": s["veredicto"],
            "razon_vista_hoy": s["razon"][:120],
            "causa_ceguera": causa_ceguera(s, casado, ofer),
            "pins_res_en_spec": ",".join(casado.get("pins_res", []) or []),
            "corrida_natural": s["corrida_natural"],
            "receta_demanda": (corr.get("receta") or "SIN-RECETA")[:160],
            "entorno_demanda": corr.get("entorno_requerido", ""),
            "nota": casado.get("nota", ""),
        })

    cols = list(filas[0].keys())
    out = SALIDA / "reconcilia-173-v1_0.tsv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# DERIVADO por forense/analisis/relevo-reconcilia-1/"
                 "reconcilia_relevo.py — NO EDITAR\n")
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(filas)

    import collections
    print(f"CALC en el arbol: {len(calcs)}  ·  SELLADA+cuenta_gen2=SI: {len(ofer)}")
    print(f"slots LEGACY-GEN1 examinados: {len(filas)}  (A.13)")
    print("\nestado_reconciliacion:")
    for k, v in collections.Counter(f["estado_reconciliacion"] for f in filas).most_common():
        print(f"  {v:4d}  {k}")
    print("\npor clase de consumidor (P4):")
    tab = collections.Counter((f["clase_consumidor"], f["estado_reconciliacion"]) for f in filas)
    for cl in sorted({f["clase_consumidor"] for f in filas}):
        tot = sum(v for (c, _), v in tab.items() if c == cl)
        ya = tab.get((cl, "YA-REHECHO-EN-GEN2"), 0)
        dif = tab.get((cl, "REHECHO-CON-DIFERENCIA"), 0)
        can = tab.get((cl, "CANDIDATO-POR-IDENTIDAD-SIN-CASAR"), 0)
        sin = tab.get((cl, "SIN-REHACER"), 0)
        print(f"  {cl:22s} total={tot:3d}  YA-REHECHO={ya:3d}  CON-DIFERENCIA={dif:3d}"
              f"  CANDIDATO-SIN-CASAR={can:3d}  SIN-REHACER={sin:3d}")
    print("\nclase de relevo (no se colapsan):")
    for k, v in collections.Counter(f["clase_de_relevo"] for f in filas).most_common():
        print(f"  {v:4d}  {k}")
    print("\ncausa de ceguera (P2):")
    for k, v in collections.Counter(f["causa_ceguera"].split(":")[0] for f in filas).most_common():
        print(f"  {v:4d}  {k}")
    print(f"\nescrito: {out.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
