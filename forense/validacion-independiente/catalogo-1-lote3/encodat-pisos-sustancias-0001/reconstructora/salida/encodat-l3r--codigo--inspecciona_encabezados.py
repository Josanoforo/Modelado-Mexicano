"""Lee solo metadatos de encabezado (lista de variables, tipos, formatos) de los .dta.

No lee filas. Uso: python3 salida/codigo/inspecciona_encabezados.py (desde el directorio de trabajo).
"""
import pandas as pd

IND = "paquete/datos/ENCODAT_2016_2017_Individual.dta"
HOG = "paquete/datos/ENCODAT_2016_2017_Hogar.dta"
INTERES = ['id_pers', 'id_hogar', 'ds2', 'ds3', 'ds9', 'ponde_ss', 'al1', 'al4', 'al9', 'al11',
           'tb02', 'tb05', 'tb50', 'di1a', 'di1i', 'dm1a', 'dm1d', 'tp1', 'est_var', 'code_upm', 'estrato']


def encabezado(ruta):
    with pd.read_stata(ruta, iterator=True) as r:
        r._ensure_open()  # abre y lee solo el encabezado
        vl = list(r._varlist)
        info = {v: (t, f, l) for v, t, f, l in zip(vl, r._typlist, r._fmtlist, r._lbllist)}
        return vl, info, r._nobs


for nombre, ruta in (("INDIVIDUAL", IND), ("HOGAR", HOG)):
    vl, info, nobs = encabezado(ruta)
    print(nombre, "nvars", len(vl), "nobs", nobs)
    for v in INTERES:
        if v in info:
            print("  ", v, info[v])
    print("  vars tipo id/folio/upm/estrato:",
          [v for v in vl if any(s in v.lower() for s in ("id", "fol", "upm", "estr", "est_"))])
