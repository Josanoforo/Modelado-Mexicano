# ACTO MAESTRA34-N1 · SELLA-REGLAS-ACTIVOS-2 — cierre

1/sep/2026, redactado por dirección (Fable); ejecutado 2/sep/2026, NUBE `cloud_default`, skill `/acto` (`ADR-237`).

## Compuerta

`COMPUERTA: PR de EJECUCIÓN #447 (ACTO MAESTRA33-E18-P3 · REGLAS-ACTIVOS-L1) fusionado en origin/main con entradas MEDIDO·p que lo citen en milpa/tramite-ola5-propuesta-v0.yaml Y este encargo archivado por PR [COLA] fusionado por mesa.`

Verificado mecánicamente al arrancar (main se había movido de `8598a72` a `92fd3f7` desde la redacción — refrescado con `git fetch origin main`, sin diferencia de perímetro):

- `git log --oneline origin/main | grep -c "#447"` → `2`.
- `git merge-base --is-ancestor 8598a72 origin/main` → sí, ancestro.
- `grep -n "recibe_remesas\|tiene_afore" milpa/tramite-ola5-propuesta-v0.yaml` → ambas con `clase: "MEDIDO·p(tasa base ponderada)"`.
- El encargo ya vivía archivado en `forense/encargos/2026-09-01-MAESTRA34-N1-SELLA-REGLAS-ACTIVOS-2.md` (PR `[COLA]`, `bb54f99`) — segunda condición cumplida por existencia del archivo.

Ambas condiciones cumplidas: el acto arranca.

## P1 — carga al motor

Dos reglas cargadas VERBATIM a `milpa/tramite.yaml` (10 reglas del motor, antes 8), campo por campo, sin reinterpretar: `familia.seguro.volatilidad_ausencia_estado` (p=0.045694, IC95 [0.043754, 0.047711], n=90 102, ENIGH 2022 + serie de 6 olas) y `dinero.planeacion.formal_estable` (p=0.538502, IC95 [0.526700, 0.550616], n=17 765, ENFIH 2019). `hallazgo` NO se copió: el bloque CARGA del encargo no lo lista entre los campos a copiar (precedente: los tres primeros `MEDIDO` de OLA-5 FASE 1 tampoco lo traen). `tier` propagado a `FUERTE` por lectura de dirección de D1-a (el motor no tiene el token "FUERTE-MEDIDO"; §3.1/§3.5 del modelo ya declaran FUERTE para R1.2/R5.1). Entradas de `milpa/tramite-ola5-propuesta-v0.yaml` marcadas SELLADA con cabecera citando D1-a, sin borrarse ni editarse el cuerpo.

Ninguna regla devuelta.

## P2 — tablero

- `FP-224`: recibo de `PR #447` (S2 había corrido P1 sin insumo; ese insumo es exactamente lo que este acto consume).
- `FP-222` enmendada: `vence` adelantado de 2026-09-30 a 2026-09-08 con la cláusula verbatim de D5-b en la fila ("si ya dio frutos se mantiene").
- `FP-225`: fila abierta para `MARCO-M-v1_2`, `vence: 2026-09-05`, gatea al merge de este acto.
- `FP-226`: fila abierta para `ACTO MAESTRA34-E1 · REVISION-FALSADORES` (dirección, propuesta 8/sep) — no existía.

## P3 — nota

Cargado: las dos reglas de arriba, tier FUERTE, clase MEDIDO·p. Devuelto: ninguna. `MAESTRA34-L1` (caja, en paralelo, perímetros disjuntos) trae la sustitución de mordida — mordida NO se toca en esta pieza — para un sello posterior `MAESTRA34-N1-bis`, mismo formato.

CONTADOR: reglas del motor 8 → 10, declarado.

No mide; no edita valores medidos; no toca el marco ni corridas; no abre Ola 6.
