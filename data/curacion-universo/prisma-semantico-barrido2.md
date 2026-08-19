# PRISMA semántico BARRIDO-2

Fecha: 2026-08-18. Acto: `ACTO B2-SEMANTICO` (C4/C5/C6). Red material: deshabilitada.

Toda cifra declara denominador y comando (§23). Ninguna está tecleada: todas se
derivan de los productos versionados de este acto.

| Métrica | Cifra | Denominador | Comando de derivación |
|---|---:|---|---|
| objetos_revisados | 23 | objetos lógicos distintos elegidos por curaduría | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| tareas_semanticas | 37 | elecciones de curador verificadas por hash | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| propuestas | 37 | tareas con veredicto supervisado | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| accion_ALTA | 0 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| accion_CAMBIO | 23 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| accion_SIN_CAMBIO | 0 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| accion_TERMINAL | 14 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| EXISTE-SATISFACE | 7 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| EXISTE-NO-SATISFACE | 16 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| negativos | 14 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| SIN-DEMANDA-CONFIRMADO | 0 | propuestas — este acto no emite ninguno; exige E2 + revisión N1-N33 + supervisor | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| dependencia_fp24_SI | 0 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| FP24_integrables_ordinariamente | 37 | propuestas — decidibles por evidencia fuente/objeto-específica | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| validadas | 37 | propuestas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| integradas | 37 | decisiones de integración | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| rechazadas_fail_closed | 0 | decisiones de integración | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| conflictos_materiales | 0 | decisiones de integración | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| no_determinadas | 0 | decisiones de integración | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| filas_de_cableado | 37 | una por propuesta proyectada | `python3 data/curacion-universo/prisma-semantico-derivar.py` |

## PRISMA de M-APERTURA absorbido (§18, §23)

Las esperadas son las filas de `data/lista-apertura-enlace2-2026-08-14.tsv` con
`destino=APERTURA-PENDIENTE`. Las de `destino=PROPUESTA-A-COLA` llevan
denominador propio y **no** se cuentan entre ellas: no tienen payload en el
ledger, de modo que no hay material que absorber.

| Métrica | Cifra | Denominador | Comando de derivación |
|---|---:|---|---|
| esperadas | 17 | filas de lista-apertura con destino=APERTURA-PENDIENTE | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| denominador_propio_sin_payload | 2 | filas con destino=PROPUESTA-A-COLA — no pertenecen a las 17 | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| observadas_E2 | 17 | de las esperadas, con material E2 elegido y verificado | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| con_capa3_EXISTE_antes_del_acto | 7 | de las esperadas — el resto tenía capa2/capa3 NO_REFERENCIADO | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| propuestas | 17 | propuestas emitidas sobre las esperadas | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| capa4_corregida | 17 | de las esperadas, ya fuera de INDEXADO-NO-DESCARGADO | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| excepciones | 0 | de las esperadas — ninguna quedó sin material accesible | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
| pendientes | 0 | de las esperadas, sin propuesta | `python3 data/curacion-universo/prisma-semantico-derivar.py` |
