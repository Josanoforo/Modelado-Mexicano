#!/usr/bin/env python3
"""tests/idg3_corrida.py -- ENCARGO CORRIDA-IDG3: ejecucion de ficha-id-g3-v1_0.md.

Construye la muestra analitica desde microdato real (ENNViH/MxFLS olas 2-3)
y recalcula la compuerta ID-X (ficha Paso 2(8)) con los n reales, ANTES de
cruzar el desenlace contra la exposicion -- Encargo CORRIDA-IDG3 §4.

Lee con pandas (pd.read_stata, convert_categoricals=False), directamente
desde los .zip de data/raw/ennvih/ (sin extraer a disco). Reusa
tests/idx_g3.py sin modificarlo (se_log_rr, Z, IC_SUP_ID_C) para que el
recalculo use exactamente la misma formula que el precalculo sellado.

Restriccion de lectura (ficha Paso 10): solo TB (Libro IIIA), AH seccion
ii_ah (Libro II), roster Libro C, ponderadores longitudinales. No abre
CRH, SE ni CR en ningun punto.

Cada pieza de la construccion (jefatura, ronda de origen del pid_link,
codigos TB33, conteos ah03h) se valido contra documentacion publicada
(codebook/guia de usuario) o una cifra ya archivada en la ficha con
archivo:linea -- ver forense/notas/2026-08-05-corrida-idg3.md para la
transcripcion completa de esas verificaciones.

Requiere pandas (no es dependencia estandar del repo -- ver
forense/notas/2026-08-05-corrida-idg3.md §2 sobre por que este acto la
necesito y como se resolvio su ausencia).
"""
import math
import sys
import os
import zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idx_g3 import se_log_rr, IC_SUP_ID_C, Z  # noqa: E402 -- reuso, no modifico

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'raw', 'ennvih')


def leer(zip_name, member):
    with zipfile.ZipFile(os.path.join(RAIZ, zip_name)) as z:
        with z.open(member) as f:
            return pd.read_stata(f, convert_categoricals=False)


def cascada(msg, n):
    print(f"  {n:>7,}  {msg}")


def clasifica_tb33(df):
    """FORMAL_CONTRATO = tb33p_a | tb33p_b ; INFORMAL = tb33p_c (ficha Paso 2(3)).
    notna(), no ==1: cada tb33p_X marca con SU PROPIO codigo de Stata
    (a->1, b->2, c->3, d->4...), no con un indicador 0/1 uniforme -- un
    ==1 parejo sobre todas produciria falsos ceros silenciosos."""
    a = df['tb33p_a'].notna()
    b = df['tb33p_b'].notna()
    c = df['tb33p_c'].notna()
    out = pd.Series('sin_abc', index=df.index)
    out[(a | b) & ~c] = 'FORMAL_CONTRATO'
    out[c & ~(a | b)] = 'INFORMAL'
    out[(a | b) & c] = 'ambiguo_a_y_c'
    return out


def recalcula_gate(n_util, si_w2, si_w3, etiqueta):
    techo = si_w2 + si_w3
    N = 2 * n_util
    p = techo / N
    se = se_log_rr(p, techo)
    ic = math.exp(Z * se)
    cruza = ic < IC_SUP_ID_C
    print(f"\n  GATE ID-X recalculado ({etiqueta}):")
    print(f"    n_util={n_util}  Si_w2={si_w2}  Si_w3={si_w3}  techo={techo}  N={N}")
    print(f"    p={p:.4%}  se={se:.4f}  IC95%sup={ic:.3f}  umbral={IC_SUP_ID_C}")
    print(f"    {'ALCANZA (<1.25)' if cruza else 'NO ALCANZA (>=1.25)'}  margen={IC_SUP_ID_C - ic:+.3f}")
    return ic, cruza


def main():
    print("=" * 78)
    print("CORRIDA-IDG3 -- cascada de construccion, ambas especificaciones")
    print("=" * 78)

    w2_ls = leer('ehh05dta_all.zip', 'ehh05dta_bc/c_ls.dta')
    w3_ls = leer('ehh09dta_all.zip', 'ehh09dta_all/ehh09dta_bc/c_ls.dta')

    jefes_w2 = w2_ls[w2_ls['ls05_1'] == 1].copy()
    jefes_w3 = w3_ls[w3_ls['ls05_1'] == 1].copy()
    cascada("jefes ola 2 (ls05_1==1)", len(jefes_w2))
    cascada("jefes ola 3 (ls05_1==1)", len(jefes_w3))

    jefes_w2['pid_link'] = jefes_w2['pid_link'].astype(str).str.strip()
    jefes_w3['pid_link'] = jefes_w3['pid_link'].astype(str).str.strip()
    jefes_w3['ronda_origen'] = jefes_w3['pid_link'].str[6]
    jefes_w3['pid_link_stripped'] = jefes_w3['pid_link'].str[:6] + jefes_w3['pid_link'].str[8:]

    n_ronda_c = int((jefes_w3['ronda_origen'] == 'C').sum())
    jefes_w3e = jefes_w3[jefes_w3['ronda_origen'] != 'C'].drop_duplicates(subset='pid_link_stripped')
    jefes_w2 = jefes_w2.drop_duplicates(subset='pid_link')
    cascada(f"  ola3 tras excluir ronda C (pid_link[6]=='C', no enlazables, n={n_ronda_c})", len(jefes_w3e))

    pl_w2 = set(jefes_w2.loc[jefes_w2['pid_link'] != '', 'pid_link'])
    pl_w3 = set(jefes_w3e.loc[jefes_w3e['pid_link_stripped'] != '', 'pid_link_stripped'])
    enlazados = pl_w2 & pl_w3
    cascada("jefes enlazados en AMBAS olas (pid_link)", len(enlazados))

    j2 = jefes_w2.set_index('pid_link')
    j3 = jefes_w3e.set_index('pid_link_stripped')
    base = pd.DataFrame({'pid_link': sorted(enlazados)})
    base['folio_w2'] = base['pid_link'].map(j2['folio']).astype(str).str.strip()
    base['folio_w3'] = base['pid_link'].map(j3['folio']).astype(str).str.strip()

    w2_tb = leer('ehh05dta_all.zip', 'ehh05dta_b3a/iiia_tb.dta')
    w3_tb = leer('ehh09dta_all.zip', 'ehh09dta_all/ehh09dta_b3a/iiia_tb.dta')
    w2_tb['pid_link'] = w2_tb['pid_link'].astype(str).str.strip()
    w3_tb['pid_link'] = w3_tb['pid_link'].astype(str).str.strip()
    w2_tb['folio'] = w2_tb['folio'].astype(str).str.strip()
    w3_tb['folio'] = w3_tb['folio'].astype(str).str.strip()
    w3_tb['pid_link_stripped'] = w3_tb['pid_link'].str[:6] + w3_tb['pid_link'].str[8:]
    w2_tb['exp'] = clasifica_tb33(w2_tb)
    w3_tb['exp'] = clasifica_tb33(w3_tb)

    n_amb_w2 = int((w2_tb['exp'] == 'ambiguo_a_y_c').sum())
    n_amb_w3 = int((w3_tb['exp'] == 'ambiguo_a_y_c').sum())
    print(f"  (nota: {n_amb_w2} casos ambiguos [a Y c marcados] ola2, {n_amb_w3} ola3 -- excluidos de ambas especificaciones)")

    w2_ah = leer('ehh05dta_all.zip', 'ehh05dta_b2/ii_ah.dta')
    w3_ah = leer('ehh09dta_all.zip', 'ehh09dta_all/ehh09dta_b2/ii_ah.dta')
    w2_ah['folio'] = w2_ah['folio'].astype(str).str.strip()
    w3_ah['folio'] = w3_ah['folio'].astype(str).str.strip()
    ah_w2 = w2_ah.drop_duplicates(subset='folio').set_index('folio')['ah03h']
    ah_w3 = w3_ah.drop_duplicates(subset='folio').set_index('folio')['ah03h']

    resultados = {}
    for etiqueta, jefe_only in (('PRIMARIA (jefe)', True), ('SENSIBILIDAD (algun miembro del hogar)', False)):
        m = base.copy()
        if jefe_only:
            exp_w2_idx = w2_tb.set_index('pid_link')['exp']
            exp_w3_idx = w3_tb.set_index('pid_link_stripped')['exp']
            m['exp_w2'] = m['pid_link'].map(exp_w2_idx).fillna('sin_abc')
            m['exp_w3'] = m['pid_link'].map(exp_w3_idx).fillna('sin_abc')
        else:
            def hogar_exp(df):
                g = df.groupby('folio')['exp']
                formal = g.apply(lambda s: (s == 'FORMAL_CONTRATO').any())
                informal = g.apply(lambda s: (s == 'INFORMAL').any())
                out = pd.Series('sin_abc', index=formal.index)
                out[informal & ~formal] = 'INFORMAL'
                out[formal] = 'FORMAL_CONTRATO'
                return out
            hexp_w2 = hogar_exp(w2_tb)
            hexp_w3 = hogar_exp(w3_tb)
            m['exp_w2'] = m['folio_w2'].map(hexp_w2).fillna('sin_abc')
            m['exp_w3'] = m['folio_w3'].map(hexp_w3).fillna('sin_abc')

        valid_exp = m['exp_w2'].isin(['FORMAL_CONTRATO', 'INFORMAL']) & m['exp_w3'].isin(['FORMAL_CONTRATO', 'INFORMAL'])
        print(f"\n--- {etiqueta} ---")
        cascada("con TB33 determinado (a/b/c) en AMBAS olas", int(valid_exp.sum()))
        m = m[valid_exp].copy()

        m['ah_w2'] = m['folio_w2'].map(ah_w2)
        m['ah_w3'] = m['folio_w3'].map(ah_w3)
        valid_ah = m['ah_w2'].notna() & m['ah_w3'].notna()
        n_util = int(valid_ah.sum())
        cascada("con ah03h no faltante en AMBAS olas -- MUESTRA ANALITICA FINAL", n_util)
        m = m[valid_ah].copy()

        si_w2 = int((m['ah_w2'] == 1).sum())
        si_w3 = int((m['ah_w3'] == 1).sum())
        print(f"    ah03h Si: ola2={si_w2}/{n_util} · ola3={si_w3}/{n_util}")
        print("    transicion de exposicion (estructura, no cruzada aun con desenlace):")
        print(pd.crosstab(m['exp_w2'], m['exp_w3']).to_string().replace('\n', '\n    '))

        ic, cruza = recalcula_gate(n_util, si_w2, si_w3, etiqueta)
        resultados[etiqueta] = (n_util, ic, cruza)

    print()
    print("=" * 78)
    print("VEREDICTO")
    print("=" * 78)
    n_primaria, ic_primaria, cruza_primaria = resultados['PRIMARIA (jefe)']
    if not cruza_primaria:
        print(f"La especificacion PRIMARIA no alcanza el gate (IC95%sup={ic_primaria:.3f} >= 1.25).")
        print("Fila = ID-X. No se calcula RR -- correr la relacion exposicion-desenlace")
        print("sobre un gate que no alcanza produciria un veredicto que no significa lo")
        print("que aparenta (mismo defecto D-09 que ADR-47 cerro para CAL-G3).")
        print("Reportado, no forzado -- Encargo CORRIDA-IDG3 §4.")
    else:
        print(f"La especificacion PRIMARIA SI alcanza el gate (IC95%sup={ic_primaria:.3f} < 1.25).")
        print("Procederia el calculo de RR (fuera del alcance de este chequeo).")


if __name__ == '__main__':
    main()
