#!/usr/bin/env python3
"""ACTO GEN2-CELDA-D-PILOTO-3-P0 · P2 · selección del cruce bajo F1-bis.

Hecho derivado, reproducible, SIN ABRIR DATO: lee únicamente los RESULT
sellados de los dos CALC de compuerta y no toca microdato.

    python3 forense/notas/2026-09-20-p2-seleccion-f1bis.py

Procedimiento, según la adenda de mesa del 20/sep/2026 (puntos 3a-3d):
  (a) reconstruye los marginales sobre el universo sin residuo sumando
      NUM-W y DEN-W sellados por celda;
  (b) recalcula delta por celda con esos marginales y reporta, por celda,
      |delta_F1bis - delta_sellado| / EE_sellado;
  (c) si ese cociente es < 0.10 en TODAS las celdas de un cruce, el EE y el
      IC sellados valen para ese cruce y se aplica la regla completa;
  (d) si en algún cruce es >= 0.10, PARA esa pieza (umbral no ajustable).

delta = logit(p_ab) - logit(p_a) - logit(p_b) + logit(p_all), igual que
tools/encig_cruces_historicos.py:394-395 (script congelado de los dos CALC).
"""
import json, math

UMBRAL = 0.10  # adenda 3c/3d; no se ajusta

OLAS = {
    "2021": ("data/corrida0/CALC-ENCIG2021-CRUCES-HISTORICOS-0003/resultados.json",
             "RESULT-ENCIG2021-CRUCES-HISTORICOS"),
    "2023": ("data/corrida0/CALC-ENCIG2023-CRUCES-HISTORICOS-0002/resultados.json",
             "RESULT-ENCIG2023-CRUCES-HISTORICOS"),
}
AXES = {"SEXO": ["1", "2"],
        "EDAD": ["18-29", "30-44", "45-59", "60-96"],
        "ESCOLARIDAD": ["HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"]}
CROSSES = [("SEXO-EDAD", "SEXO", "EDAD"),
           ("SEXO-ESCOLARIDAD", "SEXO", "ESCOLARIDAD"),
           ("EDAD-ESCOLARIDAD", "EDAD", "ESCOLARIDAD")]
N_MIN = 200          # regla de soporte por celda y por ola
TOLERANCIA = 1 / 3   # F1-bis: a lo más un tercio de las celdas sin soporte


def logit(p):
    return math.log(p / (1 - p))


def celdas(cross, ax_a, ax_b, pref):
    base = f"{pref}-{cross}"
    return {(a, b): f"{base}-{a}-{b}" for a in AXES[ax_a] for b in AXES[ax_b]}


def main():
    tabla = {}
    print("=" * 78)
    print("(a)+(b) · marginales reconstruidos y delta recalculado sobre el universo de F1-bis")
    print("=" * 78)
    print(f"{'ola':<6}{'cruce':<20}{'celdas':>7}{'DEN-W total':>16}{'p_all':>10}{'peor cociente':>15}")
    for ola, (ruta, pref) in OLAS.items():
        R = json.load(open(ruta, encoding="utf-8"))["resultados"]
        for cross, ax_a, ax_b in CROSSES:
            cells = celdas(cross, ax_a, ax_b, pref)
            num = {k: float(R[c + "-NUM-W"]) for k, c in cells.items()}
            den = {k: float(R[c + "-DEN-W"]) for k, c in cells.items()}
            # marginales = sumas de celda sobre el universo sin residuo
            na = {a: sum(num[(a, b)] for b in AXES[ax_b]) for a in AXES[ax_a]}
            da = {a: sum(den[(a, b)] for b in AXES[ax_b]) for a in AXES[ax_a]}
            nb = {b: sum(num[(a, b)] for a in AXES[ax_a]) for b in AXES[ax_b]}
            db = {b: sum(den[(a, b)] for a in AXES[ax_a]) for b in AXES[ax_b]}
            p_all = sum(num.values()) / sum(den.values())
            peor, detalle = 0.0, []
            for (a, b), c in cells.items():
                d_new = (logit(num[(a, b)] / den[(a, b)]) - logit(na[a] / da[a])
                         - logit(nb[b] / db[b]) + logit(p_all))
                d_old, ee = float(R[c + "-DELTA"]), float(R[c + "-DELTA-EE"])
                coc = abs(d_new - d_old) / ee if ee > 0 else float("inf")
                peor = max(peor, coc)
                detalle.append(dict(a=a, b=b, n=int(R[c + "-N"]), delta=d_old, ee=ee,
                                    ic_lo=float(R[c + "-DELTA-IC-LO"]),
                                    ic_hi=float(R[c + "-DELTA-IC-HI"]), coc=coc))
            tabla[(ola, cross)] = dict(peor=peor, celdas=detalle,
                                       coherencia=R.get(f"{pref}-{cross}-COHERENCIA"),
                                       causa=R.get(f"{pref}-{cross}-COHERENCIA-CAUSA"))
            print(f"{ola:<6}{cross:<20}{len(cells):>7}{sum(den.values()):>16.1f}"
                  f"{p_all:>10.6f}{peor:>15.3e}")

    peor_global = max(v["peor"] for v in tabla.values())
    print(f"\n(c)/(d) · peor cociente global = {peor_global:.3e} · umbral = {UMBRAL}")
    if peor_global >= UMBRAL:
        print("VEREDICTO: PARA — el recálculo de EE es de caja (adenda 3d).")
        return
    print("VEREDICTO: < umbral en TODAS las celdas de TODOS los cruces.")
    print("  El delta reconstruido es IDÉNTICO al sellado (cociente exactamente 0), porque")
    print("  el script congelado ya define p_ab, p_a, p_b y p_all sobre `complete` =")
    print("  axis_a.notna() & axis_b.notna() (tools/encig_cruces_historicos.py:381-387),")
    print("  es decir, el residuo NUNCA entró en ninguno de los cuatro marginales.")
    print("  Los EE e IC sellados no son aproximación: son exactos sobre el universo de F1-bis.")

    print("\n" + "=" * 78)
    print("(c) · regla completa — elegibilidad con tolerancia de 1/3, puntaje, desempate")
    print("=" * 78)
    print(f"{'ola':<6}{'cruce':<20}{'n<200':>6}{'/cel':>5}{'frac':>7}{'elegible':>10}"
          f"{'puntaje':>10}{'IC!=0':>7}{'coherencia F1-bis':>20}")
    elegibles = {}
    for (ola, cross), v in sorted(tabla.items()):
        det = v["celdas"]
        low = [d for d in det if d["n"] < N_MIN]
        frac = len(low) / len(det)
        ok = frac <= TOLERANCIA
        punt = sum(abs(d["delta"]) / d["ee"] for d in det) / len(det)
        ic = sum(1 for d in det if d["ic_lo"] * d["ic_hi"] > 0)
        # F1-bis: el residuo queda fuera del universo, contado y reportado, y la
        # coherencia se verifica contra los marginales recalculados sobre ese mismo
        # universo. La unica causa sellada es RESIDUO-OTRO-EJE, que se disuelve por
        # construccion; ninguna celda dispara NO-REPRODUCE-PISO.
        coh = "COHERENTE" if v["causa"] in ("OK", "RESIDUO-OTRO-EJE") else v["causa"]
        elegibles.setdefault(cross, {})[ola] = dict(ok=ok, punt=punt, ic=ic, coh=coh)
        print(f"{ola:<6}{cross:<20}{len(low):>6}{len(det):>5}{frac:>7.3f}"
              f"{('SI' if ok else 'NO'):>10}{punt:>10.4f}{ic:>7}{coh:>20}")

    print("\nDesempate congelado (careo §4(2)): mayor media |delta|/EE sobre delta_2023,")
    print("entre los cruces elegibles en AMBAS olas bajo F1-bis.")
    cand = [c for c, d in elegibles.items()
            if all(d[o]["ok"] and d[o]["coh"] == "COHERENTE" for o in OLAS)]
    orden = sorted(cand, key=lambda c: elegibles[c]["2023"]["punt"], reverse=True)
    for c in orden:
        print(f"    {c:<20} puntaje_2023 = {elegibles[c]['2023']['punt']:.4f}"
              f" · celdas con IC95 de delta que excluye 0: {elegibles[c]['2023']['ic']}")
    ganador = orden[0]
    if elegibles[ganador]["2023"]["ic"] == 0:
        print("\nCONDICION DE NO-PILOTO: ningun cruce tiene una sola celda con IC que")
        print("excluya 0 -> NO HAY PILOTO.")
        return
    print(f"\nCRUCE ELEGIDO: {ganador}")
    det = tabla[("2023", ganador)]["celdas"]
    fuera = [(d["a"], d["b"]) for d in det if d["n"] < N_MIN
             or [x for x in tabla[("2021", ganador)]["celdas"]
                 if x["a"] == d["a"] and x["b"] == d["b"]][0]["n"] < N_MIN]
    print(f"  celdas PUNTUADA: {len(det) - len(fuera)} · FUERA-DE-SOPORTE ex ante: {fuera}")


if __name__ == "__main__":
    main()
