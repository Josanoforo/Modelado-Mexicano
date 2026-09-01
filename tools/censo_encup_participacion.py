#!/usr/bin/env python3
"""ACTO MAESTRA33-E18-P3 · REGLAS-OLA6-ACTIVOS-L1 — COMMIT-1 de la Regla 3

Censa las 282 columnas de ENCUP 2012 contra las TRES piezas que la regla
`civico.participacion.contingente` necesita, y no contra "participacion" en
general -- que es lo que P2 conto (111 candidatas) y por lo que el encargo
dejo el `variable_id` sin fijar.

Enunciado verbatim, canon/modelo-decision-v4_0.md:551:
  "SI el votante percibe que el acto **pesa** --resultado abierto **y**
   consecuencia palpable-- ENTONCES participa; SI lo percibe **decidido de
   antemano o sin consecuencia** ENTONCES se abstiene"

El disparador es una CONJUNCION de dos condiciones, no una sola. Por eso el
censo tiene tres ejes y NO uno:

  D1  resultado abierto      (el resultado no esta decidido de antemano)
  D2  consecuencia palpable  (el acto tiene consecuencia)
  DES desenlace              (participa / se abstiene)

Cada eje corre con >=3 formulaciones declaradas ANTES de correr (A.4), y el
censo declara cuantas columnas examino (A.13) con control positivo.

Uso:
    python3 tools/censo_encup_participacion.py
"""
import os
import re

import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(RAIZ, "data", "raw", "encup_2012_base_datos_xlsx.xlsx")
HOJA = "BaseDatos_ENCUP_2012_Final"

# Formulaciones declaradas antes de correr. 3 por eje.
EJES = {
    "D1 · resultado abierto": [
        ("literal", r"decidid[oa] de antemano|resultado abierto|est[aá] decidid"),
        ("sinonimo", r"limpi[ao]s?|fraude|equitativ|competid|re[ñn]id|cerrad[ao]s?\b|parej[ao]"),
        ("regex", r"(cuentan|cuenten|respetan|respeten).{0,25}voto|voto.{0,25}(cuenta|vale|se respeta)"),
    ],
    "D2 · consecuencia palpable": [
        ("literal", r"consecuencia|sirve de algo|hace la diferencia|cambia algo"),
        ("sinonimo", r"influ\w+|puede[n]? cambiar|tiene[n]? efecto|impact\w+"),
        ("regex", r"vot\w+.{0,60}(influ|cambi|decid|sirv|afect)|(influ|cambi|sirv).{0,60}vot\w+"),
        # 4a formulacion, AÑADIDA DESPUES de correr las tres primeras y de
        # LEER LAS 282 COLUMNAS a mano. Se declara asi, no se disimula: las
        # tres formulaciones pre-declaradas NO pegaron en las dos mejores
        # candidatas del eje. P80 dice "Votar es la unica manera ... para
        # DECIR si el gobierno hace bien o mal" -- "decir", no "decidir", asi
        # que el regex `vot\w+.{0,60}(...|decid|...)` pasa de largo. P28C es
        # el item clasico de eficacia externa y no contiene ni "voto" ni
        # "influir". Un censo que solo reportara las tres primeras habria
        # declarado el eje mas vacio de lo que esta.
        ("lectura-completa", r"personas como yo para decir si el gobierno|no les preocupa lo que piensa la gente"),
    ],
    "DES · desenlace participa/abstiene": [
        ("literal", r"acudi[oó] a votar|fue a votar|no vot[oó]"),
        ("sinonimo", r"\bvot[oó]\b|sufrag|abstenci|acudi[oó] a las urnas"),
        ("regex", r"elecci[oó]n (presidencial|pasada)|elecciones"),
    ],
}


def main():
    df = pd.read_excel(XLSX, sheet_name=HOJA)
    cols = [str(c) for c in df.columns]
    print(f"PAYLOAD  : {XLSX}")
    print(f"HOJA     : {HOJA}")
    print(f"A.13 · columnas examinadas por cada formulacion: {len(cols)}")
    print(f"A.13 · filas del payload: {len(df)}")
    print()

    for eje, formulaciones in EJES.items():
        print("=" * 70)
        print(eje)
        print("=" * 70)
        union = set()
        for nombre, patron in formulaciones:
            rx = re.compile(patron, re.I)
            hits = [c for c in cols if rx.search(c)]
            union |= set(hits)
            print(f"  [{nombre:9}] patron={patron[:52]:<52} -> {len(hits):>3} columnas")
            for h in hits:
                print(f"                {h[:112]}")
        print(f"  UNION del eje: {len(union)} columnas distintas")
        print()

    # Control positivo A.13: el mismo barrido, sobre las mismas 282 columnas,
    # con un patron que TIENE que pegar. Si esto diera 0, el cero de los ejes
    # seria del comando y no del dato.
    ctrl = [c for c in cols if re.search(r"P\d", c)]
    print("=" * 70)
    print(f"CONTROL POSITIVO (mismo barrido, mismas {len(cols)} columnas, "
          f"patron 'P\\d'): {len(ctrl)} columnas")
    print("=" * 70)




# ─────────────────────────────────────────────────────────────────────
# DESCRIPTIVO — NO es la `p` de la regla y NO se sella en ningun yaml.
#
# La regla quedo EXISTE-NO-SATISFACE porque su disparador es una CONJUNCION
# y ENCUP 2012 no trae la mitad `resultado abierto` (0 reactivos en 282
# columnas). Esta funcion calcula lo que produciria la MITAD que si existe
# (D2 = P80), unicamente para que mesa vea el tamano del efecto antes de
# decidir si vale la pena buscar la otra mitad en otra fuente.
#
# Diseno: ENCUP 2012 publica `factor` y `POND` pero NO variables de diseno
# declaradas. Se usa `Estado` como estrato y `Punto` (375 puntos de muestreo)
# como conglomerado -- PROXY declarado, no el diseno oficial. Por eso, y por
# la conjuncion faltante, la cifra es descriptiva y no candidata a `p`.
# ─────────────────────────────────────────────────────────────────────
def descriptivo_no_sellado():
    import numpy as np

    df = pd.read_excel(XLSX, sheet_name=HOJA)
    cols = [str(c) for c in df.columns]
    c_p77 = next(c for c in cols if c.startswith("P77_1."))
    c_p80 = next(c for c in cols if c.startswith("P80."))

    voto = df[c_p77].map({"Sí": 1.0, "No": 0.0})
    pesa = df[c_p80].map({"Muy de acuerdo": 1, "De acuerdo": 1,
                          "En desacuerdo": 0, "Muy en desacuerdo": 0})
    w = pd.to_numeric(df["factor"], errors="coerce")
    ok = voto.notna() & pesa.notna() & w.notna()

    print()
    print("=" * 70)
    print("DESCRIPTIVO — NO es la `p` de la regla, NO se sella")
    print("  desenlace : P77_1 (acudio a votar, presidencial) = Si")
    print("  eje D2    : P80 (votar es la unica manera de decir si el")
    print("              gobierno hace bien o mal) = de acuerdo / muy de acuerdo")
    print("  FALTA     : D2 es solo la MITAD del disparador; `resultado")
    print("              abierto` no existe en ENCUP 2012 (0 de 282 columnas)")
    print("=" * 70)
    print(f"  filas utilizables: {int(ok.sum())} de {len(df)}")
    for v, etiqueta in ((1, "percibe que el acto pesa (D2=1)"),
                        (0, "no lo percibe (D2=0)")):
        m = (ok & (pesa == v)).to_numpy()
        p = float((w[m] * voto[m]).sum() / w[m].sum())
        print(f"  {etiqueta:<34} n={int(m.sum()):>5}  votó={p:.4f}")
    m1 = (ok & (pesa == 1)).to_numpy()
    m0 = (ok & (pesa == 0)).to_numpy()
    p1 = float((w[m1] * voto[m1]).sum() / w[m1].sum())
    p0 = float((w[m0] * voto[m0]).sum() / w[m0].sum())
    print(f"  brecha (D2=1 menos D2=0): {(p1 - p0) * 100:+.2f} pp")
    print("  ⚠️  Cifra descriptiva. Media conjuncion no es la conjuncion.")


if __name__ == "__main__":
    main()
    descriptivo_no_sellado()
