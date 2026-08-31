# MAESTRA32-E8 · MEDICION-COMPUESTA — cierre (COMMIT-2)

## §0 · Input de dirección que levanta la compuerta (verbatim, 30/ago/2026)

> INPUT DE DIRECCIÓN — maestra-32, 30/ago/2026 — levanta la compuerta de MAESTRA32-E8 y reordena el carril CAJA.
>
> 1. La compuerta "GATED a que MAESTRA32-E3 fusione" era de SECUENCIA de carril, no de DATOS: E8 no consume ningún producto de E3 (E8 abre ENCUCI 2020 SEC_4_5 y ENVIPE 2025 TPer_Vic1+BP1_23, ya medidas el 4/ago; E3 inventaría .dta/.sav/.rdata/.dbf de otros payloads). Se levanta. Tu PARO fue correcto y queda registrado como el entregable de arranque.
>
> 2. Orden nuevo del carril CAJA: E8 (este acto, ahora) → E3 (solo cuando el merge de E8 esté visible en main). La serie estricta dentro del carril se mantiene. E11 · COBERTURA-15 corre en NUBE en paralelo; compartidos, solo la cascada; renumera quien fusiona segundo.
>
> 3. Al archivar el encargo (paso 0-bis) añade en la CABECERA, sin tocar el cuerpo: "Enmienda in situ 30/ago/2026 (dirección): compuerta 'E3 fusionado' LEVANTADA — era de secuencia, no de datos; carril CAJA reordenado E8 → E3; input verbatim en la nota de cierre §0." Pega este input completo como §0 de forense/notas/2026-08-30-compuesta-cierre.md y cítalo en el ADR.
>
> 4. Completa el ARRANQUE antes de nada más: faltan el punto 3 (data/raw: existe / enlazada a <ruta>), el punto 4 con los dos valores crudos (CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE y la sonda curl, con A.13) y el punto 5. A.2 tercera parte es PARO-relevante aquí: `ls data/raw/ 2>/dev/null | head -1` debe mostrar el corpus compartido; si no, PARA y repórtalo.
>
> 5. Todo lo demás del encargo rige sin cambio: 0-bis → COMMIT-1 (spec congelada, frase de sello) → COMMIT-2. Ignora cualquier mención a pyreadstat: es de E3, no de E8. A.1 para los dos payloads: una invocación por --id. PR desde esta rama; ADR y FP re-derivados al escribir.

## Resumen de resultados

Corrida única de `tools/medicion_compuesta.py`, contra árbol `2799132` + esta rama. Ambos pares pasan la regla α (§d de la spec): **α ≥ 0.50 en los dos** ⇒ ambos se escriben al ejecutable. Ambos IC95 excluyen 0 ⇒ ningún sufijo `·NO-DISTINGUIBLE-DE-CERO`.

### G1.radio_confianza (ENCUCI 2020 SEC_4_5)

- n universo re-derivado: **13,348** (4/ago: 13,435 — diff **0.648%**, dentro del umbral del falsador, no dispara).
- α de Cronbach (AP5_1_1/2/3, escala 0-10): **0.7441**.
- β̂ primaria (media/10, y=`tramite.mordida.discrecional`): **−0.06626** IC95[−0.116675, −0.015844] — negativo, significativo.
- β̂ secundaria (proporción de ítems ≥6): −0.02749 IC95[−0.053363, −0.001611] — negativo, significativo, mismo signo que la primaria.
- Condicionamiento: eje `formalidad(POS)` — 6 celdas n≥30, 3 negativas significativas, 2 no distinguibles de cero, **1 invierte a positivo y significativo** (`POS=4`, n=198, β=+0.4419 IC95[0.0446,0.8392]) — coherente con la inversión ya documentada por `Encargo X`/ADR-61 en los ítems individuales. Eje `edad_grupo` — 4 celdas, 1 negativa significativa (18-29), 3 no distinguibles de cero, sin inversión de signo. Eje `ingreso`: **NO LOCALIZABLE** — ningún campo de ingreso monetario en `ENCUCI_2020_SD.dbf` ni `ENCUCI_2020_VIV.dbf` (los dos únicos candidatos revisados). Limitación declarada explícitamente; el condicionamiento es diagnóstico, no gatea la escritura (spec §e).
- Veredictos B-bis: IC no incluye 0 → sin sufijo. Signo consistente entre compuesto y β̂ por ítem (los tres ítems del 4/ago eran negativos). Inversión bajo condicionamiento **sí ocurrió** (celda `POS=4`) → va a `reserva:` verbatim, como anticipaba (f) y como hizo ACTO E1.

### G4.confianza_institucional[justicia] (ENVIPE 2025, TPer_Vic1 + TPer_Vic2 + TMod_Vic, join ID_PER)

- n universo re-derivado (disparador AP7_3_05-15 + desenlace BP1_23 resuelto): **13,399** (4/ago: 13,023 — diff **2.887%**). **FALSADOR DISPARADO** (>2%): se reporta la diferencia y se sigue con el universo re-derivado, sin ajustar hacia el número del 4/ago (A-bis 4). La diferencia es consistente en dirección con una re-derivación honesta: la nota del 4/ago no especificó si excluía duplicados de `ID_PER` entre disparador y módulo con la misma regla exacta que este script; no se investigó más a fondo porque el falsador del encargo exige reportar, no ajustar.
- n primaria (≥4/7 instituciones identificadas): 6,469. n secundaria (7/7, caso completo): 1,240.
- KR-20 (7 ítems dicotómicos, caso completo): **0.8085**.
- β̂ primaria (proporción de confianza entre instituciones identificadas): **−0.166208** IC95[−0.212384, −0.120031] — negativo, significativo.
- β̂ secundaria (caso completo 7/7): −0.324219 IC95[−0.430198, −0.218239] — negativo, significativo, mismo signo, magnitud mayor (consistente con selección: quienes identifican las 7 instituciones son un subgrupo más informado/politizado). Calculado con el mismo método analítico linealizado (n=1,240 ≥30, conglomerado-último aplicable sin necesidad del bootstrap de respaldo declarado en la spec).
- Condicionamiento: eje `edad_grupo` — 4 celdas, 2 negativas significativas (18-29, 30-44), 2 no distinguibles de cero, sin inversión. Eje `dominio` — 3 celdas (U, C, R), 2 negativas significativas, 1 (R) no distinguible de cero, sin inversión de signo.
- Veredictos B-bis: IC no incluye 0 → sin sufijo. Signo consistente con los 7 β̂ por ítem del 4/ago (todos negativos). Sin inversión bajo condicionamiento en este par (a diferencia de G1).

## Escritura al ejecutable

Por script (`tools/medicion_compuesta.py --escribe`), `yaml.safe_load` de entrada y de verificación de salida (precedente ADR-220). Diff real:

```diff
   clase: MEDIDO·β̂(diferencia de proporciones), por ítem, marginal (sin condicionar sobre atributos)
   valor_origen: 'AP5_1_1: -0.0102 [IC95% -0.0292,0.0089] · AP5_1_2: -0.0113 [IC95% -0.0341,0.0114] · AP5_1_3: -0.0269 [IC95% -0.0465,-0.0072]'
   unidad_origen: proporción (diferencia de proporciones, sin sufijo pp, por ítem)
-  rotulo: SELLADO-ESCALA·SIN-AGREGACION
-  reserva: 'ADR-57 (a): la concordancia de signo entre este β̂ marginal y el ASIGNADO (G1 -0.35) NO corrobora el asignado -- condicionar (Encargo X, ver eje_condicionante arriba) mostró que el marginal no es estable (33 de 39 celdas invierten el signo, recontado por ADR-61 -- ver eje_condicionante). Asociar ≠ identificar.'
+  rotulo: ASOCIACION-MEDIDA·COMPUESTO·MARGINAL
+  reserva: 'ADR-57 (a): la concordancia de signo entre este β̂ marginal y el ASIGNADO (G1 -0.35) NO corrobora el asignado -- condicionar (Encargo X, ver eje_condicionante arriba) mostró que el marginal por ítem no es estable (33 de 39 celdas invierten el signo, recontado por ADR-61). El compuesto de este acto (β̂=-0.066260) hereda la misma reserva: asociar ≠ identificar. Rótulo previo (histórico): SELLADO-ESCALA·SIN-AGREGACION.'
+  valor_ejecutable: -0.06626
+  ic: IC95% -0.116675,-0.015844
+  escala: proporción ponderada [0,1], enlace identidad (ADR-220)
+  definicion_compuesto: 'media de AP5_1_1/2/3 en 0-10, /10 -> [0,1]'
+  alpha: 0.7441
   fuente: coeficientes_generador_medidos.G1_radio_confianza, 4/ago/2026
```
```diff
   clase: MEDIDO·β̂(diferencia de proporciones), condicional(ejes), universo=disparadores AP7_3 no denunciantes, por institución
   valor_origen: 'Marginal por ítem (confía − no_confía): AP5_4_01 -6.421pp[-9.096,-3.746] · AP5_4_02 -5.226pp[-8.317,-2.134] · AP5_4_03 -7.919pp[-10.588,-5.251] · AP5_4_05 -9.706pp[-13.286,-6.126] · AP5_4_06 -4.683pp[-8.139,-1.228] · AP5_4_07 -6.658pp[-10.863,-2.452] · AP5_4_11 -11.269pp[-15.729,-6.809]. Los siete significativos al 95% y de signo consistente (negativo).'
   unidad_origen: pp (por ítem, ver valor_origen)
-  rotulo: SELLADO-ESCALA·SIN-AGREGACION
-  reserva: ''
+  rotulo: ASOCIACION-MEDIDA·COMPUESTO·MARGINAL
+  reserva: 'ADR-57 (a): los 7 β̂ por ítem son todos negativos y significativos (6 de 49 celdas condicionadas invierten). El compuesto de este acto (β̂=-0.166208) hereda la misma reserva de asociación marginal: asociar ≠ identificar. marca_c2 (histórica): comparte desenlace y universo con G4.exposicion_violencia -- no se combinan entre entradas. Rótulo previo (histórico): SELLADO-ESCALA·SIN-AGREGACION.'
+  valor_ejecutable: -0.166208
+  ic: IC95% -0.212384,-0.120031
+  escala: proporción ponderada [0,1], enlace identidad (ADR-220)
+  definicion_compuesto: 'proporción de instituciones (de las 7) en que confía, entre quienes identifican >=4 de 7'
+  alpha: 0.8085
   fuente: coeficientes_generador_medidos.G4_confianza_institucional_justicia, 4/ago/2026
```

`valor_origen`/`unidad_origen`/`fuente` NO se tocan (quedan como historia, A.10); `rotulo` se transiciona (campo único, no historia paralela) y el rótulo anterior queda citado en `reserva:` para trazabilidad.

## Recifrado L0

Coeficientes ejecutables con base medida en `coeficientes_generador_sellados`: **4 → 6** (α ≥ 0.50 en ambos pares, sin excepciones que redujeran a 5 o 4). `tests/test_matriz_sellados.py` re-derivado: 4 override · 2 sin-agregación · 9 fallback → **6 override · 0 sin-agregación · 9 fallback**.

## PR

Pendiente: este PR aún no existe en el momento de escribir esta nota; se añade `## CONSUMIDO` con el número de PR en `forense/encargos/2026-08-30-MAESTRA32-E8-MEDICION-COMPUESTA.md` una vez abierto.

## Salida cruda del script, sin editar

```
==============================================================================
MAESTRA32-E8 · MEDICION-COMPUESTA -- corrida única, salida cruda
==============================================================================

--- G1.radio_confianza (ENCUCI 2020 SEC_4_5) ---
n universo re-derivado: 13348 (4/ago: 13435, diff 0.648%)
alpha de Cronbach (AP5_1_1/2/3, 0-10): 0.744099641283322
beta primaria (media/10, y=tramite.mordida.discrecional): -0.066260 IC95[-0.116675,-0.015844] n=13348 -> negativo, significativo
beta secundaria (prop items>=6): -0.027487 IC95[-0.053363,-0.001611] n=13348 -> negativo, significativo
Condicionamiento (n>=30 por celda):
  eje=formalidad(POS)
    (vacio): n=5223 beta=-0.062277 IC95[-0.113138,-0.011416] -> negativo, significativo
    1: n=526 beta=-0.070754 IC95[-0.237777,0.096269] -> no distinguible de cero
    2: n=4800 beta=-0.071672 IC95[-0.183085,0.039741] -> no distinguible de cero
    3: n=2369 beta=-0.128171 IC95[-0.244877,-0.011465] -> negativo, significativo
    4: n=198 beta=0.441899 IC95[0.044612,0.839185] -> positivo, significativo
    5: n=232 beta=-0.147589 IC95[-0.253451,-0.041726] -> negativo, significativo
  eje=edad_grupo
    18-29: n=4212 beta=-0.158035 IC95[-0.236914,-0.079156] -> negativo, significativo
    30-44: n=4106 beta=-0.041792 IC95[-0.132037,0.048454] -> no distinguible de cero
    45-59: n=2757 beta=-0.027560 IC95[-0.120400,0.065281] -> no distinguible de cero
    60+: n=2273 beta=0.023463 IC95[-0.152888,0.199814] -> no distinguible de cero
  ingreso: NO LOCALIZABLE: ningún campo de ingreso en ENCUCI_2020_SD.dbf/VIV.dbf (campos revisados: ambas tablas no traen variable de ingreso monetario; limitación declarada, no bloquea el commit -- condicionamiento es diagnóstico).

--- G4.confianza_institucional[justicia] (ENVIPE 2025 TPer_Vic1+TPer_Vic2+TMod_Vic) ---
n universo re-derivado (disparador+desenlace): 13399 (4/ago: 13023, diff 2.887%)
FALSADOR DISPARADO (>2%): se reporta la diferencia, se sigue con el universo re-derivado (A-bis 4).
n primaria (>=4/7 identificadas): 6469  n secundaria (7/7 caso completo): 1240
KR-20 (7 items dicotómicos, caso completo): 0.8084954093325069
beta primaria (prop confianza entre identificadas): -0.166208 IC95[-0.212384,-0.120031] n=6469 -> negativo, significativo
beta secundaria (caso completo 7/7) [prop_ultimate_cluster-linealizado]: -0.324219 IC95[-0.430198,-0.218239] n=1240 -> negativo, significativo
Condicionamiento (n>=30 por celda):
  eje=edad_grupo
    18-29: n=2050 beta=-0.227823 IC95[-0.307294,-0.148353] -> negativo, significativo
    30-44: n=2626 beta=-0.158242 IC95[-0.235281,-0.081203] -> negativo, significativo
    45-59: n=1299 beta=-0.078363 IC95[-0.167221,0.010496] -> no distinguible de cero
    60+: n=494 beta=-0.038721 IC95[-0.156368,0.078925] -> no distinguible de cero
  eje=dominio
    C: n=1249 beta=-0.187406 IC95[-0.296610,-0.078201] -> negativo, significativo
    R: n=625 beta=-0.082422 IC95[-0.211081,0.046237] -> no distinguible de cero
    U: n=4595 beta=-0.171621 IC95[-0.226132,-0.117110] -> negativo, significativo

--- Veredictos B-bis (pre-registrados, spec §f) ---
G1: IC incluye 0 -> no
G4: IC incluye 0 -> no
==============================================================================

--- Escritura al ejecutable ---
G1.radio_confianza: alpha=0.744099641283322 -> ESCRITO
G4.confianza_institucional: alpha=0.8084954093325069 -> ESCRITO
```
