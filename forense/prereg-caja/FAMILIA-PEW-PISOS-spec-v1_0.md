# Pisos por segmento Pew Global Attitudes, México 2013–2023 (intención migratoria, lazos y remesas) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1`, 25/sep/2026, CAJA,
rama `acto/gen2-familia-cuidados-y-migracion-pisos-1`, 0-bis `2a0ebb63`. CALC:
`CALC-PEW-MIGRACION-MEX-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de
registro de Pew (sólo `metadataonly`). **El primer resultado que produzca este procedimiento
es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Pew GAS en el manifiesto por id: `pew_gas_spring{2013,2015,2017,2018,2023,2024,2025}`
  (más dos piezas documentales 2025). Los ZIP viven en `descargas_mx`, fuera del sandbox:
  copiados al espejo durable `mm-corpus/descargas_mx_espejo/UNIVERSO-2026-09/PEW/`, sha256
  idéntico al manifiesto en los siete (A.13: 7 archivos).
- **E.6:** Spring 2025 es la ola más reciente → RESERVADA; no es input; el medidor PARA si
  llega. 2024 no trae ninguna pregunta de la lista (metadatos recorridos) → no es input.
- **Evidencia (a).** Firma §3 v2.16 (encargo §2): Pew se etiqueta (b) cuando encuesta a
  mexicanos en EE. UU. GAS entrevista residentes de México en México (filtro por país) → (a).
  Los reportes de Pew sobre mexicanos en EE. UU. (p. ej. `MIGR-042`) son otro producto y no
  entran aquí.
- No hay CALC previo de Pew (`ls data/corrida0 | grep -ci pew` = 0 al COMMIT-1).

## 1 · Unidad, universo, diseño

Persona adulta entrevistada en México; edad 18–97 (98/99 fuera). Peso `weight`
(`WEIGHT` 2013/2015). PSU/estrato de México donde existen (2015 `PSU`/`STRATUM_MEX`; 2017,
2018 `PSU_MEX`/`STRATUM_MEX`): bootstrap de PSU dentro de estrato. 2013 y 2023 no publican
PSU: bootstrap de entrevistas (un estrato, cada entrevista su UPM) — el IC no incorpora
efecto de diseño y es más estrecho de lo real (declarado).

## 2 · Conductas (por texto)

Lista cerrada §2 (Pew): 6 proporciones, cada una sólo en las olas donde se hizo la misma
pregunta. `IRIA-SIN-AUTORIZACION-…` sólo entre quienes respondieron 1 a «iría a vivir a
EE. UU.» en la misma ola.

## 3 · Ejes (uno a la vez)

SEXO (1/2) · EDAD 18–29/30–44/45–59/60+.

## 4 · Estimación

Razón ponderada con bootstrap (`PCG64(20260925)`, 2 000 réplicas, percentiles 2.5/97.5,
contrato conservador), receta común y lectores por sha256. IC calibrado de persistencia por
conducta sobre sus olas (≥ 3), piso = última ola con la pregunta; con 2 olas
(`BUENO-PARA-MEXICO-…`) → sin IC calibrado.

## 5 · Controles, secuencia

Sintético en `tests/test_familia_pisos_gen2.py` (SAV fabricados, con filas de otro país que
el filtro debe excluir). Ninguna ejecución diagnóstica.

## 6 · Auditoría (afirma sobre México)

**Contadores:** cuenta (`cuenta_gen2: SI`, `adopta: NO`). **Intención ≠ conducta:** «iría si
tuviera los medios» es disposición declarada, no migración; no se compara con flujos (EMIF,
ENADID) sin enlace. **Estructura ≠ cultura:** la intención de emigrar sigue a ingreso,
violencia y redes; recibir remesas es exposición a una red, no «cultura migrante». **Muestra
Pew:** cara a cara, n ≈ 1 000 por ola; con sobre-cobertura urbana posible — rural no se puede
segmentar aquí (sin variable armonizada). **Una pregunta, varios años:** los cambios entre
olas pueden reflejar coyuntura política bilateral (2017: primer año de Trump). **Cifra a
mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
