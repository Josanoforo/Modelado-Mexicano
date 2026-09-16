# ACTO GEN2-ADOPCION-VENTANILLA-3

**SHA de redacción de este archivo (0-bis):** `2f5cffe` (`origin/main`,
post-PR #768/#769). Redactado pre-escrito, **gateado** — no se lanza al
redactar, se re-deriva y se lanza cuando la compuerta cierre.

**Entorno asignado:** NUBE, Opus. **NO** se lanza en CAJA. `python3
tools/entorno.py` al arranque, re-derivar contra el commit real de apertura
(no confiar en el de esta redacción).

**COMPUERTA:**
1. Los tres minis fusionados en `origin/main` — **CUMPLIDO**:
   `GEN2-LOTE-MEDICION-PENDIENTE-1` (PR #766),
   `GEN2-SANEA-REGISTRO-Y-RESCATE` (PR #767), `GEN2-F5-DOCUMENTAL-RUN-2`
   (PR #764).
2. **`FP-375` con `estado: FIRMADA`** en `forense/firmas-pendientes.tsv` —
   **CUMPLIDO 15/sep/2026** (`firmada_en`/`ejecutada_en` = 2026-09-15).
   Mesa, 15/sep/2026 · OBJETO: `cuenta_gen2 = SI` para las cuatro corridas
   selladas por el lote; no adopta al motor. Escrita en
   `data/corrida0/decisiones.tsv`, registro re-derivado
   (`N_corridas_selladas` 63→67, `N_resultados_gen2_sellados` 2882→3142).
   Detalle: `forense/notas/2026-09-14-GEN2-LOTE-MEDICION-PENDIENTE-1-cierre.md`
   §5, actualización 15/sep.

**Ambas condiciones cumplidas — compuerta cerrada.** Re-deriva de todos
modos contra el commit real de apertura antes de correr `/acto` (no
confíes en este SHA de redacción); relee `firmas-pendientes.tsv` para
confirmar que nadie revirtió la firma entre esta actualización y la
apertura.

**Estado:** LISTO — compuerta cerrada, listo para lanzar con `/acto`.

---

## ENCARGO, VERBATIM (A.3)

ENCARGO · ACTO GEN2-ADOPCION-VENTANILLA-3 · UNA PASADA INTEGRAL EN VEZ DE
GOTEO — las cuatro corridas del lote que `FP-375` firmó entran a censo y
adopción, los tres `DECISIÓN-DE-MESA` que `COLA-5` dejó propuestos (residuo
vivo, verificado) se re-presentan sin re-trabajarlos, y los 471 `RESULT` de
`CALC-B-MARCO-*` (`NC-0187`) se censan por-consumidor — no para adoptarlos
(la veda de `prereg-caja-B-MARCO` §«QUÉ NO ES» / `T9` sigue intacta), sino
para dejar la decisión B-al-motor-vs-B-al-duelo contada y servida a la
lectura de mesa.

CABECERA · NUBE, Opus · NO se lanza en CAJA · COMPUERTA: merge de los tres
minis (cumplido) + `FP-375` firmada (pendiente al redactar) · re-deriva al
abrir contra el commit real, no contra este SHA de redacción · candidatos:
deriva al cierre, no heredes de `VENTANILLA-2`.

FIRMA DE MESA que autoriza el alcance integral (retry engordado, no el
micro): correr una sola pasada de adopción sobre las cuatro corridas del
lote + el residuo de `COLA-5` + el censo B-MARCO, en vez de trocearlo en
actos sucesivos — la regla de la casa vigente (adopción por lote es firma
de mesa POR MERGE; lo que exija decisión distinta se PROPONE sin ejecutar)
se hereda sin reabrir.

VERIFICACIÓN DE EXISTENCIA (A.8, a re-hacer al abrir, contra el clon real —
lo de abajo es el estado visto el 15/sep, no sustituye la relectura): (1)
`FP-375` — firma de contador para `CALC-EDER-0002`, `CALC-ENVIPE-U4-2012`,
`CALC-ENVIPE-U4-2012-v1_1`, `CALC-ENIF-0003` (`ACTO
GEN2-LOTE-MEDICION-PENDIENTE-1`, 14/sep); mientras `ABIERTA` las cuatro
nacen `cuenta_gen2 = PENDIENTE-DE-MESA` y no cuentan en
`N_corridas_selladas` / `N_resultados_gen2_sellados`. Al abrir este acto,
releer `data/corrida0/decisiones.tsv` para confirmar que la firma sí quedó
escrita (SI a las cuatro, SI a algunas, o NO) — el censo de P1 lee esa fila,
no la supone. (2) Residuo `COLA-5`: `RESULT-CTX-2019-P-ALTO`,
`RESULT-CTX-2021-P-ALTO`, `RESULT-CTX-2023-P-ALTO` quedaron
`DECISIÓN-DE-MESA` propuestos y sin ejecutar (`NC-0183`, sobre cita
`corrida0_*` de `RESULT-EDER-A-P` y la consecuencia literal de
`se_mueve_si`); verifica que `NC-0183` sigue `ABIERTA` y que nadie los
resolvió entre el 14/sep y la apertura — si mesa ya firmó, este acto los
re-presenta con esa cita, no re-abre el debate. (3) `NC-0187` / B-MARCO:
471 `RESULT` (`CALC-B-MARCO-ENVIPE-0001` n=226, `CALC-B-MARCO-ENCIG-0001`
n=45, `CALC-B-MARCO-ENIGH-0001` n=45, `CALC-B-MARCO-MAE-0001` n=155), cero
citas en `milpa/*.yaml` ni `usos.tsv` al 15/sep. La veda de adopción viene
de `forense/prereg-caja/B-MARCO-spec-v1_0.md` §«QUÉ NO ES» (`T9`),
congelada antes de abrir microdato — este acto no la reabre ni la fuerza:
solo cuenta consumo posible por-serie contra la demanda actual y sirve la
tabla. `RESULT-B-ENIGH-2022-P` de `CALC-B-0001` (que sí está adoptado, como
tasa medida ENIGH 2022 para `recibe_remesas`) sigue siendo el precedente
que **no se generaliza** — no se toca ni se recuenta aquí.

PIEZAS: P1 · CENSO INTEGRAL, LEÍDO. Deriva del registro, tres bloques
separados sin mezclarlos: (a) las 4 corridas del lote — id · spec ·
`cuenta_gen2` tras `FP-375` · consumidor si aplica; (b) los 3
`DECISIÓN-DE-MESA` de `COLA-5` — estado de `NC-0183` al abrir, re-presentado
con su cita, no re-trabajado; (c) los 471 de B-MARCO por serie (n por
`CALC-B-MARCO-*`), censo de consumo actual (`milpa/*.yaml`, `usos.tsv`) —
tabla cruda pegada, sin decisión de adopción todavía. P2 · ADOPCIÓN O
DECLARACIÓN, patrón de la casa, aplicado SOLO a (a) y (b) — exactamente una
salida por elemento: ADOPTA (cita re-apuntada o nueva, valor intacto, sonda
de consumo pegada) · NO-ADOPTABLE-POR-DECISIÓN (decisión citada) ·
DECISIÓN-DE-MESA (propuesto con la pregunta exacta, sin ejecutar).
Contadores antes/después, crudos (E.4). P3 · B-MARCO, SERVIDO NO DECIDIDO.
Para cada una de las 4 series: consumidor actual (si lo hay) · consumidor
plausible bajo la veda vigente (motor vs. duelo) · lo que cambiaría si mesa
levantara `T9` para esa serie en particular. Cero adopciones aquí — el
producto es la tabla que deja la decisión B-al-motor-vs-B-al-duelo contada,
no tomada. P4 · CIERRE, contadores de `status` antes/después, y explícito:
qué de este acto quedó `DECISIÓN-DE-MESA` (para que la siguiente ventanilla
no lo re-trabaje) vs. qué quedó `SERVIDO` (para que mesa decida con la
tabla de P3 en mano, no a ciegas).

PERÍMETRO Y CONCURRENCIA. Toca: `milpa/*.yaml` (citas) ·
`data/corrida0/decisiones.tsv` si el vehículo lo exige + TSV re-derivados ·
`forense/notas/` · `forense/no-corrido.tsv` · `forense/firmas-pendientes.tsv`
(cerrar `FP-375` con `ejecutada_en` si este acto es quien la consume) ·
0-bis · cascada. NO toca `data/corrida0/*/spec.yaml` de B-MARCO (censo, no
adopción) ni reabre `prereg-caja-B-MARCO`. «Si te encuentras escribiendo
fuera de esta lista, PARA.»

CONTADOR: mueve `N_corridas_selladas` / `N_resultados_gen2_sellados` (+4
corridas si `FP-375` firmó SI a las cuatro) y los de adopción sobre (a)/(b);
NO mueve nada sobre B-MARCO (censo puro). LO QUE NO HACE: no adopta B-MARCO
ni reabre `T9` · no re-mide · no repite lo que `COLA-5`/`VENTANILLA-2` ya
dejaron propuesto o cerrado · no censa si `FP-375` sigue `ABIERTA` al abrir
(vuelve a comprobar la compuerta, no confía en este encargo). SUCESORES:
mesa decide sobre P2 y sobre la tabla de P3. CIERRE · Cascada + ##
NO-CORRIDO / RESERVAS + ## CONSUMIDO con el PR.

---

## NO-CORRIDO / RESERVAS

*(a llenar al cierre del acto — este encargo se redacta gateado, sin correr)*

## CONSUMIDO

*(pendiente — no lanzar hasta que `FP-375` quede `FIRMADA` en
`forense/firmas-pendientes.tsv`)*
