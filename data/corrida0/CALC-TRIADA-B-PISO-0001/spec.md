# CALC-TRIADA-B-PISO-0001 · la tabla común de la tríada con `B` de piso

**Acto:** `GEN2-F5-CIERRE-Y-PANEL-1`, 15/sep/2026. **Generación:** GEN2.
**Cuenta GEN2:** `SI`, por firma de contador con objeto embebida en el
lanzamiento y escrita en `data/corrida0/decisiones.tsv`. La firma es lo que
resuelve el contador: la regla `E.1` marca esta corrida `envuelto_legacy = SI`
**por cadena** (consume `RESULT` de `CALC-B-MARCO-MAE-0001` y de
`CALC-TRIADA-0002`, que leen `corridas-R/`), y sin firma el registro la
resolvería `NO`. Se declara así, antes de correr, para que nadie lea el
contador como derivado por la máquina. **Contar no adopta nada.**

## Objeto

Congelar la **tabla común** de los cuatro corredores sobre el único universo
donde los cuatro tienen punto: `U_COMUN = U3 ∩ {celdas con B bajo PERSISTENCIA}`.
Es una **corrida de registro**. `D-2` de la firma de mesa del 15/sep/2026 la
autoriza como comparación **descriptiva**: sin pareadas nuevas, sin IC nuevos,
sin adjudicación. El veredicto vigente de la tríada, `SIN-GANADOR-UNICO`, se
cita desde `CALC-TRIADA-0002` y **no se toca**.

## Método — el acto deriva, no hereda

El medidor no cita ningún `MAE` de la tríada: los **recalcula** desde
`celdas.tsv` del sucesor, celda por celda. Por eso corre primero el
**control de derivación**, que es la razón de ser de este CALC: recalcula
sobre `U3` los tres `MAE` que `CALC-TRIADA-0002` selló y los enfrenta a los
sellados, en tres ramas pre-declaradas —`REPRODUCE-EXACTO` (|Δ| ≤ 1e-9),
`REPRODUCE-AL-CENTESIMO` (|Δ| < 0.005, umbral **estricto**) y
`NO-REPRODUCE`—. **Si una sola rama sale `NO-REPRODUCE`, la tabla común no se
emite** y el veredicto es `NO-DERIVA-CONTROL-FALLA`: una derivación que no
reproduce su origen no es una derivación. `U_COMUN` vacío tampoco emite tabla
(`NO-EMITE-UCOMUN-VACIO`); un `MAE` de cero celdas no es un `MAE`.

`B` entra sólo por el brazo `PERSISTENCIA`, leyendo
`RESULT-BM-MAE-<celda>-PERSISTENCIA-ERR-PP` del asiento sellado, en valor
absoluto. `MAE_pp` es media simple de `|err_pp|` en orden fijo de `id`, y se
reporta **siempre con su `n` y su lista de celdas** (A-bis.4). Nada se imputa:
una celda sin punto en cualquiera de los cuatro corredores queda fuera, con
razón nominal (`FUERA-DE-U3`, `SIN-B-PERSISTENCIA`, `FUERA-DE-U3-Y-SIN-B`).

La ordenación por `MAE` se emite rotulada `ORDEN-DESCRIPTIVA` y el veredicto
es `NO-ADJUDICA-POR-DISENO`. Ordenar cuatro medias sobre nueve celdas sin IC
no corona a nadie, y esta spec lo dice antes de ver el orden.

## Insumos y límite de identidad

`spec.yaml` fija por `sha256` los cuatro insumos: `celdas.tsv` del sucesor,
los `resultados.json` sellados de `CALC-B-MARCO-MAE-0001` y `CALC-TRIADA-0002`,
y `marco-M-sorteado-v1_3.tsv` como guardia de identidad (las 14 filas de
`celdas.tsv` son exactamente las 14 del marco, o el medidor levanta).

No abre microdato, no llama a modelos, no lee `corridas-R/M/L` directamente,
no modifica capturas históricas, no re-corre ningún brazo y no habilita `F6`
ni adopción al motor.

## Salidas

Se declaran antes de ejecutar: guardia de identidad; `U3` re-derivado con su
lista; el control de derivación por corredor (derivado, sellado, Δ y rama) y
su veredicto; cobertura de `B` con su lista; `U_COMUN` con su lista; por celda
del marco, pertenencia, razón de exclusión y `|err_pp|` de los cuatro
corredores; los cuatro `MAE` sobre `U_COMUN`; la ordenación descriptiva; el
conteo de celdas donde `B` yerra menos que `M`; el veredicto; el veredicto
vigente de la tríada citado intacto; y los cuatro contadores de lo que este
acto **no** hizo (pareadas, IC, adopciones, llamadas a modelo = 0).

Los textos comparan exacto y los flotantes con tolerancia absoluta 1e-9.
