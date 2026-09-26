"""Contrato futuro y dictamen puro, sin I/O de reservas.

El ingreso de tablas exige adaptador de cableado auditado y autorización de ola
en COMMIT-3. Aquí se ejecuta la regla congelada con tablas ya autorizadas.
"""
import numpy as np

from medidor import FAMILIAS, activacion, dictamen, medir


def evaluar(tablas, contrato, emisiones, metadatos):
    if not activacion(metadatos):
        return {'estado': 'NO-COMPARABLE', 'apertura_autorizada': False}
    if set(emisiones) != set(FAMILIAS) or any(
            e['R_futura'] is not None or e['retadores'] for e in emisiones.values()):
        raise ValueError('emisiones base inválidas')
    diag, reps = medir(tablas, contrato)
    resultados, diferencias = {}, {}
    for name in FAMILIAS:
        p0 = emisiones[name]['p0']
        d = reps[name] - p0
        valid = d[np.isfinite(d)]
        diferencias[name] = d
        info = diag['familias'][name]
        ic = np.quantile(valid, [.025, .975]) if len(valid) else [np.nan, np.nan]
        error = info['punto'] - p0 if info['punto'] is not None else None
        resultados[name] = {
            'p0': p0, 'R': info['punto'], 'error_con_signo': error,
            'error_absoluto': abs(error) if error is not None else None,
            'ic95_d': ic.tolist() if np.isfinite(ic).all() else None,
            'fraccion_replicas_en_banda': float(np.mean(np.abs(valid) <= .02)) if len(valid) else None,
            'dictamen': dictamen(*ic, estimable=info['estimable']),
            'soporte': info, 'alcance': 'compatibilidad local; no causalidad ni calibración general',
            'delta_mae': 'NO-APLICABLE', 'B_bis': 'NO-APLICABLE',
        }
    return {'resultados': resultados, 'R_k': reps, 'd_k': diferencias,
            'diagnostico': diag, 'aperturas': 1}
