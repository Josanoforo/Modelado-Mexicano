# `ACTO MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA` — P0 · censo A.4 de los `.xls` del SAT

3/sep/2026 · entorno UBUNTU, worktree `/home/pc0/mm-maestra36-l13`, base
`origin/main = ea45e01` (SHA de redacción del encargo, EXACTO — `main` no se movió).
Comando: `python3 tools/medidor_l13_sat_efirma.py --censo`.

**Esta pieza no calcula ninguna tasa.** Abre las hojas para leer estructura
(encabezados, periodos, unidades) y decide, por objeto, si hay numerador y
denominador que compartan periodo y universo. La cifra `p` es de `P1`, y su
spec y su falsador se congelan en el mismo `COMMIT-1` que archiva esta nota.

## A.2 — tercera parte, la que describe el dato

```
$ ls "$(python3 -c 'import yaml;print(yaml.safe_load(open("data/raices.local.yaml"))["descargas_mx"])')/Descargas Manuales" | grep -c '\.xls$'
11
```

La dirección esperaba `≥ 9`. **11** — se cumple. De esos 11, **6** son los ids
del SAT que el encargo nombra; los otros 5 (`DataDetails.xls`,
`DecAnuaTipCon (1).xls` —duplicado de descarga—, `FORMATO_9_Impuesto.xls`,
`NumPagTipCon.xls`, `NumPagosMedRec.xls`) quedan fuera del perímetro de este acto.

## Identidad de los payloads

Los 6 se verifican por `sha256` contra `data/manifiesto.yaml`, no por nombre de
archivo. **6/6 COINCIDE.**

| id | archivo | `sha256` (16) | hoja |
|---|---|---|---|
| `firelenumcontri` | `Descargas Manuales/FirEleNumcontri.xls` | `dce5a06c278cf8f5…` | `'79'` 280×5 |
| `firelenumcert` | `…/FirEleNumcert.xls` | `e813b6c12d613a33…` | `'80'` 280×5 |
| `portipocontribuyente` | `…/PorTipoContribuyente.xls` | `d14769a74c4adef6…` | `'5'` 208×9 |
| `porentfed` | `…/PorEntFed.xls` | `51f79b5a2d9191b9…` | `'1'` 207×36 |
| `decanuatipcon` | `…/DecAnuaTipCon.xls` | (censo) | 209×5 |
| `ingresostributarios` | `…/IngresosTributarios.xls` | (censo) | 213×23 |

## Censo por objeto (A.4)

### 1 · `firelenumcontri` — **EXISTE-SATISFACE (como cota superior)** · numerador

- **Qué mide.** `[4,3]`: «Contribuyentes que han obtenido el certificado de
  e.firma **(se considera el primer certificado emitido)**», desglosado en
  `Personas Físicas` / `Personas Morales`.
- **Unidad.** Contribuyentes (personas), **flujo mensual de altas primeras**.
- **Periodo.** `2004-01` → `2026-07` (`* Cifras preliminares`, `Fuente: SAT.`).
- **Por qué sirve.** La cláusula «primer certificado» es lo que hace legítima la
  **suma acumulada**: no hay doble conteo por renovación, así que el acumulado es
  el número de contribuyentes *distintos* que alguna vez obtuvieron e.firma.
- **Qué le falta, y se declara.** No es «e.firma **vigente**»: el certificado
  caduca (4 años) y el acumulado no da de baja a quien salió del padrón. Por eso
  el acumulado es **cota superior** del stock vigente — y, en consecuencia, toda
  `p` que produzca `P1` es una cota superior de la adopción vigente.

### 2 · `firelenumcert` — **EXISTE-NO-SATISFACE** · control, no numerador

- `[4,3]`: «Certificados **emitidos**», misma rejilla mensual `2004-01`→`2026-07`.
- Cuenta **certificados**, no personas: incluye renovaciones, así que un mismo
  contribuyente entra varias veces. **Qué le falta:** unicidad de la unidad.
  Sirve como control de consistencia (`certificados ≥ contribuyentes`), nunca
  como numerador de una proporción de personas.

### 3 · `portipocontribuyente` — **EXISTE-SATISFACE** · denominador

- `[3,1]`: «Número de contribuyentes **activos**». Columnas: `Personas Físicas`,
  `Grandes Contribuyentes (PF)`, `Asalariados (PF)`, `Personas Morales`,
  `Grandes Contribuyentes (PM)`, `Total`.
- **Unidad.** Contribuyentes en el padrón activo, **stock mensual**.
- **Periodo.** `2010-01` → `2026-07`.
- **Por qué sirve, y qué le falta.** No trae una columna de «obligados a
  e.firma» — el encargo lo anticipa. Pero **sí aísla `Asalariados (PF)`**, que es
  precisamente el grupo que en general no está obligado. Eso permite las dos
  cotas del denominador que `P1` exige, sin suponer nada: `Total` (amplio) y
  `Total − Asalariados (PF)` (obligado aproximado). Nota de la propia hoja: desde
  `2021-01` los Grandes Contribuyentes incluyen Hidrocarburos.

### 4 · `porentfed` — **EXISTE-NO-SATISFACE** para este par

- Mismo universo («contribuyentes activos») pero desglosado por las 32 entidades,
  `2010-01`→`2026-07`. **Qué le falta:** no distingue tipo de contribuyente, así
  que no permite construir el universo obligado. Queda como control del
  denominador (su total debe coincidir con el de `portipocontribuyente`) y como
  insumo de un acto sucesor que quiera variación subnacional.

### 5 · `decanuatipcon` — **EXISTE-NO-SATISFACE**

- «Número de declaraciones anuales», PF/PM, flujo mensual `2010-01`→`2026-07`.
  **Qué le falta:** cuenta **declaraciones**, no contribuyentes (la propia hoja
  avisa que incluye complementarias y regularizaciones de ejercicios anteriores),
  y no dice nada de e.firma ni de padrón.

### 6 · `ingresostributarios` — **NO SATISFACE** (fuera de escala)

- «Ingresos por impuesto (Millones de pesos)», 21 impuestos, `2010-01`→`2026-07`.
  Es dinero, no personas: no puede ser numerador ni denominador de una tasa de
  adopción.

## Veredicto de pieza

**Hay par.** `firelenumcontri` (numerador, `2004-01`→`2026-07`) y
`portipocontribuyente` (denominador, `2010-01`→`2026-07`) comparten unidad
(contribuyentes), fuente (SAT) y rejilla (mensual, año×mes); su periodo común
cubre `2010`→`2025` en años completos, muy por encima de los **≥ 3** que el
encargo exige para la serie. **`P1` procede — no hay PARO.**

## Exposición declarada (honestidad del ciego)

El censo imprimió las primeras y últimas filas crudas de cada hoja para leer
periodo y unidad: vi magnitudes sueltas (altas mensuales de `2026-07`, padrón
total de `2026-07`), **no** el acumulado del numerador ni ningún cociente. El
falsador de `P1`, además, no lo elige el ejecutor: viene **congelado por la
dirección en el encargo** (`SHA ea45e01`), archivado por `A.3` en
`ea3bf92` — antes de que este acto abriera un solo `.xls`.
