#!/usr/bin/env python3
"""Cifras de los tres pilotos para el informe del programa -- ACTO GEN2-MARCADOR-E-INFORME-1 · P4.

POR QUÉ ESTE TOOL EXISTE. El encargo pide que cada cifra del informe traiga su
comando o su `RESULT` citado. Un informe con 30 cifras tecleadas a mano desde
notas de cierre es exactamente el defecto que §2 nombra («ninguna cifra esperada
se teclea»), y el que v2.1 pone en el módulo de auditoría («¿qué afirmación
sobre el estado del corpus fue escrita a mano y no derivada?»). Aquí hay UN
comando y el informe cita su salida.

QUÉ DERIVA, por piloto y por candidato:
  * n de celdas PUNTUADAS,
  * MAE y error máximo en PUNTOS PORCENTUALES,
  * COBERTURA del IC95 del candidato: en cuántas celdas la R cae DENTRO del
    intervalo del candidato,
  * intervalo binomial de esa cobertura.

LA COBERTURA ES LA DEL CANDIDATO, NO LA DEL ÁRBITRO. El piloto 2 selló un campo
`ARB-DENTRO-IC-R-C2-<celda>` que mide lo contrario: el PUNTO del candidato
dentro del IC de R. Son dos preguntas distintas -- «¿mi intervalo atrapa la
verdad?» vs «¿mi punto cae donde la verdad es plausible?» -- y sólo la primera
es cobertura. Este tool no lee ese campo: recalcula R ∈ [IC_inf, IC_sup] del
candidato desde los RESULT sellados de la corrida de EMISIONES.

INTERVALO BINOMIAL: WILSON (score), z=1.959964, declarado porque importa. No es
Clopper-Pearson: `scipy` no está en este entorno y un exacto mal implementado a
mano sería peor que un Wilson correcto. Wilson es cerrado, no degenera en 0/n ni
en n/n, y con n=8..35 es el que se recomienda. Quien quiera el exacto lo corre
donde haya `scipy`; la diferencia se declara como limitación, no se esconde.

LAS CELDAS DE UNA MISMA OLA NO SON INDEPENDIENTES. El intervalo binomial supone
ensayos independientes y las celdas de un cruce comparten marco muestral,
réplicas de bootstrap y ola. El intervalo que sale de aquí es, por eso, DEMASIADO
ANGOSTO. Se publica con la advertencia pegada, no sin ella.

TODA CIFRA SE VERIFICA CONTRA UN SELLO. El MAE derivado se compara contra el
`RESULT-...-ARB-G-MAE-<candidato>` sellado del propio árbitro (pilotos 1 y 2) o
contra el `margen_material` de la celda-D (piloto 3); la salida trae la columna
`check` con COINCIDE o con la discrepancia. Una receta que no se prueba contra un
caso conocido es una receta sin verificar (§2).

Uso:
    python3 tools/informe_pilotos.py            # tabla legible
    python3 tools/informe_pilotos.py --json     # el mismo contenido en JSON
"""
from __future__ import annotations

import json
import math
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORRIDA0 = os.path.join(RAIZ, "data", "corrida0")
Z95 = 1.959964

# Los tres pilotos, con los nombres REALES de sus RESULT sellados. Las plantillas
# no son una convención elegida aquí: son la forma exacta con la que cada corrida
# nombró sus resultados, y `--json` las imprime para que cualquiera las verifique
# contra el `resultados.json` correspondiente.
PILOTOS = [
    {
        "piloto": 1,
        "celda_d": "DIN.ahorro_solo_informal.enif2024.localidad_x_edad",
        "dominio": "FIN · ENIF 2024",
        "unidad": "persona",
        "escala_emision": "PROPORCION",
        "emisiones": "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001",
        "arbitro": "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001",
        "raiz": "RESULT-DIN-LXE8-",
        "celdas_desde": "ARB-D-C2-",
        # Dos formas vivas: el piso C2 emitió `C2-IC95INF-<celda>` y el piso 2021
        # (C1) emitió por DESENLACE, `C1-D9-IC95INF-<celda>`. D9 es el desenlace
        # de la R contra la que se compara (`ARB-R-D9-P-<celda>`); D7 es la otra
        # definición y NO se usa aquí, porque comparar un IC de D7 contra una R
        # de D9 sería comparar dos universos (§4.4).
        "cand_p": ("{c}-P-{k}", "{c}-D9-P-{k}"),
        "cand_lo": ("{c}-IC95INF-{k}", "{c}-D9-IC95INF-{k}"),
        "cand_hi": ("{c}-IC95SUP-{k}", "{c}-D9-IC95SUP-{k}"),
        "r_p": "ARB-R-D9-P-{k}",
        "err": "ARB-D-{c}-{k}",
        "err_en_pp": False,
        "mae_sellado": "ARB-G-MAE-{c}",
        "mae_sellado_en_pp": False,
        "candidatos": ["C1", "C2", "C3"],
    },
    {
        "piloto": 2,
        "celda_d": "TRA.evade_norma.envipe2025.escolaridad_x_dominio",
        "dominio": "TRA · ENVIPE 2025",
        "unidad": "delito",
        "escala_emision": "PROPORCION",
        "emisiones": "CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001",
        "arbitro": "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001",
        "raiz": "RESULT-TRA-SXD12-",
        "celdas_desde": "ARB-D-C2-",
        "cand_p": "{c}-P-{k}",
        "cand_lo": "{c}-IC95INF-{k}",
        "cand_hi": "{c}-IC95SUP-{k}",
        "r_p": "ARB-R-P-{k}",
        "err": "ARB-D-{c}-{k}",
        "err_en_pp": True,
        "mae_sellado": "ARB-G-MAE-{c}",
        "mae_sellado_en_pp": True,
        "candidatos": ["C1", "C2", "C6", "C7"],
    },
    {
        "piloto": 3,
        "celda_d": "GOB.gobierno_digital.encig2025.edad_x_escolaridad",
        "dominio": "TRA · ENCIG 2025",
        "unidad": "trámite",
        "escala_emision": "PROPORCION",
        "emisiones": "CALC-GOB-DIGITAL-EXE-EMISIONES-0002",
        "arbitro": "CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001",
        "raiz": "RESULT-GOB-EXE15-ADJ-2025-",
        # La corrida de EMISIONES nombra sin el `ADJ-`: los puntos e IC de cada
        # candidato viven bajo `RESULT-GOB-EXE15-2025-<celda>-<cand>-P-IC-LO`.
        "raiz_emisiones": "RESULT-GOB-EXE15-2025-",
        "celdas_desde": "-C2-D-PP",
        "cand_p": "{k}-{c}-P",
        "cand_lo": "{k}-{c}-P-IC-LO",
        "cand_hi": "{k}-{c}-P-IC-HI",
        "r_p": "{k}-R-P",
        "err": "{k}-{c}-D-PP",
        "err_en_pp": True,
        "soporte": "{k}-SOPORTE",
        # La adjudicación selló el MAE de las dos referencias (`C1A-MAE-PP`,
        # `C1B-MAE-PP`) pero no el del piso ni el de los retadores; el del piso
        # se checa contra el `margen_material` de la celda-D y los dos
        # retadores se quedan SIN-SELLO, declarado en la salida.
        "mae_sellado": "{c}-MAE-PP",
        "mae_sellado_en_pp": True,
        "mae_check_celda_d": "C2",
        # `S-LAMBDA-VS-C2` / `S-MEDIO-VS-C2` por celda: VENCE / INDECIDIBLE /
        # PIERDE. La regla de ¾ del criterio de adjudicación se lee de aquí.
        "duelo": "{k}-{c}-VS-C2",
        # ΔMAE del retador contra el piso, con su IC95 bootstrap, SELLADO por la
        # propia adjudicación. No se recalcula aquí: se lee y se cita.
        "delta_mae": "{c}-DELTA-MAE-PP",
        "delta_mae_lo": "{c}-DELTA-MAE-IC-LO",
        "delta_mae_hi": "{c}-DELTA-MAE-IC-HI",
        "candidatos": ["C1A", "C1B", "C2", "S-MEDIO", "S-LAMBDA"],
    },
]


def _res(calc_id):
    p = os.path.join(CORRIDA0, calc_id, "resultados.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as fh:
        return json.load(fh).get("resultados", {})


def wilson(exitos: int, n: int, z: float = Z95) -> tuple[float, float]:
    """IC de Wilson para una proporción binomial. Cerrado, sin dependencias."""
    if n == 0:
        return (0.0, 1.0)
    p = exitos / n
    d = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / d
    semi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centro - semi), min(1.0, centro + semi))


def celdas_de(spec, res_arb) -> list[str]:
    """Los ids de celda, leídos de los RESULT de error del piso C2."""
    pat = spec["celdas_desde"]
    raiz = spec["raiz"]
    if pat.startswith("-"):      # sufijo (piloto 3)
        return sorted(k[len(raiz):-len(pat)] for k in res_arb
                      if k.startswith(raiz) and k.endswith(pat))
    return sorted(k[len(raiz) + len(pat):] for k in res_arb
                  if k.startswith(raiz + pat))


def deriva_piloto(spec) -> dict:
    raiz = spec["raiz"]
    res_e, res_a = _res(spec["emisiones"]), _res(spec["arbitro"])
    if not res_a:
        return {"piloto": spec["piloto"], "error": f"AUSENTE: {spec['arbitro']}"}
    juntos = dict(res_e)
    juntos.update(res_a)

    raiz_e = spec.get("raiz_emisiones", raiz)

    def _busca(plantilla, prefijos, **kw):
        """Primera plantilla que resuelve, probada bajo cada raíz declarada.

        Devolver la PRIMERA que existe no es preferir una: son nombres de la
        misma cantidad en corridas distintas, y la lista de arriba declara cuál
        es cuál y por qué. Si ninguna resuelve, devuelve None y la celda entra
        como `celdas_sin_ic` -- nunca se rellena con otra cosa.
        """
        if plantilla is None:
            return None
        for p in ((plantilla,) if isinstance(plantilla, str) else plantilla):
            for pre in prefijos:
                v = juntos.get(pre + p.format(**kw))
                if v is not None:
                    return v
        return None

    def g(plantilla, **kw):
        """Cantidad del ÁRBITRO (R, error, soporte, MAE sellado)."""
        return _busca(plantilla, (raiz,), **kw)

    def ge(plantilla, **kw):
        """Cantidad del CANDIDATO (punto e IC), que vive en EMISIONES."""
        return _busca(plantilla, (raiz_e, raiz), **kw)

    celdas = celdas_de(spec, res_a)
    if "soporte" in spec:
        celdas = [k for k in celdas
                  if (g(spec["soporte"], k=k) or "PUNTUADA") == "PUNTUADA"]

    margen = None
    if spec.get("mae_check_celda_d"):
        try:
            import yaml
            p = os.path.join(RAIZ, "data", "curacion-registro", "celdas-d",
                             spec["celda_d"] + ".yaml")
            with open(p, encoding="utf-8") as fh:
                margen = ((yaml.safe_load(fh) or {}).get("celda_d")
                          or {}).get("margen_material")
        except Exception:  # pragma: no cover -- sin yaml no hay check, se declara
            margen = None

    filas = []
    for c in spec["candidatos"]:
        err, cubiertas, sin_ic, n_err = [], 0, 0, 0
        for k in celdas:
            e = g(spec["err"], c=c, k=k)
            if isinstance(e, (int, float)):
                err.append(e if spec["err_en_pp"] else e * 100.0)
                n_err += 1
            lo, hi, r = (ge(spec["cand_lo"], c=c, k=k),
                         ge(spec["cand_hi"], c=c, k=k),
                         g(spec["r_p"], c=c, k=k))
            if all(isinstance(x, (int, float)) for x in (lo, hi, r)):
                cubiertas += 1 if lo <= r <= hi else 0
            else:
                sin_ic += 1
        n_cob = len(celdas) - sin_ic
        lo_w, hi_w = wilson(cubiertas, n_cob)
        mae = round(sum(err) / len(err), 3) if err else None

        # ── el check: la cifra derivada contra la sellada ─────────────────
        sellado = g(spec["mae_sellado"], c=c) if spec.get("mae_sellado") else None
        if isinstance(sellado, (int, float)):
            sellado_pp = sellado if spec.get("mae_sellado_en_pp") else sellado * 100.0
            check = ("COINCIDE" if mae is not None
                     and abs(mae - sellado_pp) <= 5e-3
                     else f"DISCREPA: derivado={mae} sellado_pp={sellado_pp}")
            ref = raiz + spec["mae_sellado"].format(c=c)
        elif margen is not None and c == spec.get("mae_check_celda_d"):
            check = ("COINCIDE" if mae is not None and abs(mae - margen) <= 5e-3
                     else f"DISCREPA: derivado={mae} margen_material={margen}")
            ref = f"celda-D {spec['celda_d']}:margen_material"
        else:
            check = "SIN-SELLO-CONTRA-EL-CUAL-CHECAR"
            ref = ""

        duelo = {}
        if spec.get("duelo"):
            for k in celdas:
                v = g(spec["duelo"], c=c, k=k)
                if isinstance(v, str):
                    duelo[v] = duelo.get(v, 0) + 1

        dmae = g(spec.get("delta_mae"), c=c) if spec.get("delta_mae") else None
        dlo = g(spec.get("delta_mae_lo"), c=c) if spec.get("delta_mae_lo") else None
        dhi = g(spec.get("delta_mae_hi"), c=c) if spec.get("delta_mae_hi") else None

        filas.append({
            "candidato": c,
            "duelo_vs_piso_C2": duelo or "NO-SELLADO-POR-CELDA",
            "delta_MAE_vs_piso_pp": (
                {"punto": round(dmae, 3),
                 "ic95": [round(dlo, 3), round(dhi, 3)]
                 if isinstance(dlo, (int, float)) and isinstance(dhi, (int, float))
                 else "SIN-IC-SELLADO",
                 "sello": raiz + spec["delta_mae"].format(c=c)}
                if isinstance(dmae, (int, float)) else "NO-SELLADO"),
            "n_celdas_con_error": n_err,
            "MAE_pp": mae,
            "error_max_pp": round(max(err), 3) if err else None,
            "cobertura_ic95_candidato": (
                f"{cubiertas}/{n_cob}" if n_cob else "SIN-IC-EN-NINGUNA-CELDA"),
            "cobertura_prop": round(cubiertas / n_cob, 3) if n_cob else None,
            "cobertura_ic_binomial_wilson95": (
                [round(lo_w, 3), round(hi_w, 3)] if n_cob else None),
            "celdas_sin_ic": sin_ic,
            "check_contra_sello": check,
            "sello_de_referencia": ref,
        })

    return {
        "piloto": spec["piloto"],
        "celda_d": spec["celda_d"],
        "dominio": spec["dominio"],
        "unidad": spec["unidad"],
        "n_celdas_puntuadas": len(celdas),
        "emisiones": spec["emisiones"],
        "arbitro": spec["arbitro"],
        "por_candidato": filas,
    }


def juntos_los_tres(pilotos) -> dict:
    """Cobertura del PISO C2 sumando los tres pilotos.

    Se suma la COBERTURA (un conteo de celdas) y NO los errores: el MAE del
    piloto 1 está en unidad persona, el del 2 en unidad delito y el del 3 en
    unidad trámite, y §4.4 prohíbe promediarlos. Un conteo de «cuántas veces el
    intervalo atrapó a la verdad» sí es la misma pregunta en los tres.
    """
    ex = n = 0
    detalle = []
    for p in pilotos:
        f = next((x for x in p.get("por_candidato", []) if x["candidato"] == "C2"), None)
        if not f or "/" not in str(f["cobertura_ic95_candidato"]):
            continue
        a, b = f["cobertura_ic95_candidato"].split("/")
        ex += int(a)
        n += int(b)
        detalle.append(f"piloto {p['piloto']}: {a}/{b}")
    lo, hi = wilson(ex, n)
    return {
        "candidato": "C2 (el piso, el único presente en los tres)",
        "cobertura": f"{ex}/{n}" if n else "SIN-DATO",
        "cobertura_prop": round(ex / n, 3) if n else None,
        "ic_binomial_wilson95": [round(lo, 3), round(hi, 3)] if n else None,
        "detalle": detalle,
        "advertencia": ("las celdas de una misma ola comparten marco muestral y "
                        "réplicas de bootstrap: NO son ensayos independientes y "
                        "este intervalo es demasiado angosto"),
        "no_se_promedian": ("los MAE de los tres pilotos NO se promedian: unidad "
                            "persona, unidad delito y unidad trámite son escalas "
                            "distintas (§4.3/§4.4)"),
    }


def main() -> int:
    pilotos = [deriva_piloto(s) for s in PILOTOS]
    salida = {
        "pilotos": pilotos,
        "piso_C2_los_tres_juntos": juntos_los_tres(pilotos),
        "metodo_ic_binomial": f"Wilson (score), z={Z95}; scipy ausente en este entorno",
        "comando": "python3 tools/informe_pilotos.py --json",
    }
    if "--json" in sys.argv:
        print(json.dumps(salida, ensure_ascii=False, indent=1))
        return 0
    for p in pilotos:
        if "error" in p:
            print(f"PILOTO {p['piloto']}: {p['error']}")
            continue
        print(f"\n== PILOTO {p['piloto']} · {p['celda_d']}")
        print(f"   {p['dominio']} · unidad {p['unidad']} · "
              f"{p['n_celdas_puntuadas']} celdas puntuadas")
        print(f"   {'candidato':<10} {'MAE pp':>8} {'max pp':>8} "
              f"{'cobertura':>10} {'IC binomial 95%':>20}  check")
        for f in p["por_candidato"]:
            ic = f["cobertura_ic_binomial_wilson95"]
            print(f"   {f['candidato']:<10} {str(f['MAE_pp']):>8} "
                  f"{str(f['error_max_pp']):>8} "
                  f"{str(f['cobertura_ic95_candidato']):>10} "
                  f"{str(ic):>20}  {f['check_contra_sello']}")
    j = salida["piso_C2_los_tres_juntos"]
    print(f"\n== PISO C2, LOS TRES JUNTOS: cobertura {j['cobertura']} "
          f"IC {j['ic_binomial_wilson95']}  ({'; '.join(j['detalle'])})")
    print(f"   {j['advertencia']}")
    print(f"   {j['no_se_promedian']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
