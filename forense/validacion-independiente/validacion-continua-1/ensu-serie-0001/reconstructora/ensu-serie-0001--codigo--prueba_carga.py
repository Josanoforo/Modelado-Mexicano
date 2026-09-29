"""Prueba de carga (solo conteos de diagnóstico, sin estimaciones) en una ola por era."""
import sys
sys.path.insert(0, "salida/codigo")
import reconstruye as R  # noqa: E402

for ola in ["2013T3", "2016T1", "2017T1", "2017T3", "2020T3", "2021T3"]:
    cb, dg = R.carga(ola)
    _, _, dm = R.replicas(cb)
    dg.update(dm)
    print(ola, dg)
