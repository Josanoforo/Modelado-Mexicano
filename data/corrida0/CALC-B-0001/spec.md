# `CALC-B-0001` — ENSAYO de la línea base temporal `B` sobre remesas ENIGH 2016→2022

Cara **local** de la spec sellada `forense/prereg-caja/B-REMESAS-spec-v1_0.md`
(`prereg-caja-B-REMESAS`, sha256 `2376c21a0668a5f57db8cbddcd8cc59dd468dc7e10838f66da3b8156fb93c7ba`).
Lo que este archivo dice, lo dice la spec sellada primero; si alguna vez discrepan,
manda la sellada. Congelado en el `COMMIT-1` de `ACTO GEN2-C0-B`, antes de abrir
microdato.

## 1 · Qué mide

Proporción ponderada de hogares con `concentradohogar.remesas > 0`, por ola de
ENIGH Nueva Serie, en **2016, 2018, 2020 y 2022** — una ola a la vez, jamás
agrupadas ni promediadas. Ponderador `factor`. Universo: el completo de
`concentradohogar` (`folioviv` + `foliohog`), sin filtro adicional.

Sobre esa serie corre el selector `tools/baseline_temporal.py` (sha
`886f2da43724f26ead82736eb48cdbba4b4145b51cdedf2b38f2fd1701871d92`, `PR #620`),
**sin modificarlo**, para tres objetivos (2018, 2020, 2022) y **dos brazos** que
difieren únicamente en el metadato `disponible_desde` que se le entrega:

- `OPERATIVO` — `disponible_desde` = el campo `Modified` de los metadatos de la
  versión que el corpus tiene de esa ola (2016: `2021-11-29` · 2018: `2021-11-29`
  · 2020: `2021-07-28` · 2022: `2023-07-26`).
- `PERSISTENCIA` — `disponible_desde` = `periodo_fin` de la ola (el valor más
  temprano que el selector admite): el contrafáctico «si cada ola hubiera estado
  disponible el día que cerró su levantamiento».

`fecha_corte(objetivo) = <objetivo − 1>-12-31`. Períodos = año calendario de la
ola (§2.2 y §0.3 de la sellada: el campo `Temporal` del payload de 2022 declara
**2021** y es un defecto sistemático de INEGI; se sella verbatim y no se usa).

## 2 · Qué NO mueve

Ninguna regla. `R5.1` / `familia.seguro.volatilidad_ausencia_estado` conserva su
`p`, su `ic95`, su `tier` y su `serie_olas`. Ninguna cifra de este CALC entra a un
veredicto (`T9`, citada verbatim en la sellada). `etiquetas.cuenta_gen2` queda en
`PENDIENTE-DE-MESA`.

## 3 · Guardias que PARAN (no supuestos heredados)

- `N-NULOS-REMESAS > 0` en una ola → esa ola sale `NO-ESTIMABLE-NULOS-INESPERADOS`.
  La dicotomización pre-registrada tiene dos ramas y sólo dos; la rama NA no se
  fabrica sobre la marcha. (`milpa/tramite.yaml` afirma cero nulos en las seis
  olas: aquí se vuelve a medir, no se hereda.)
- `N-SIN-DISENO > 0` entre las filas válidas → IC en `null` y
  `NO-ESTIMABLE-DISENO-INCOMPLETO`.
- Más de un CSV de datos bajo `<directorio>/conjunto_de_datos/` → la corrida PARA:
  elegir cuál sería elegir el dato.

## 4 · IC95

Bootstrap de UPM con reemplazo dentro de cada `est_dis`, conservando el número de
UPM por estrato; percentiles 2.5/97.5; 2 000 réplicas; semilla `20260908`, RNG
`numpy.PCG64`. Ranura **no** pre-registrada por nadie para esta serie: la elige el
ejecutor, se declara y se eleva a mesa (§3 de la sellada). No se espera coincidencia
dígito a dígito con los IC de la corrida GEN1, que usó otra implementación.

## 5 · Lectura pre-declarada

`B` predice bien un objetivo si su predicción cae **dentro del IC95 de la
proporción observada de esa ola** — umbral que esta corrida mide, no que esta
sesión elige. Agregado por brazo: `PISO-ALTO` / `PISO-BAJO` / `MIXTO` /
`SIN-PREDICCIONES` (§5.2 de la sellada). Todo objetivo con
`|MARGEN-AL-BORDE| < 1e-4` se reporta como `ROZA-EL-BORDE` y **no** se cuenta como
decisión limpia.

## 6 · Adopción (P3), pre-declarada en TRES ramas

`RESULT-B-ENIGH-2022-P` mide la cantidad que
`milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas`
materializa hoy con `p: 0.045694`. La cita sólo se escribe si puede escribirse **sin
crear un `FAIL` nuevo**: `T35 (c)` compara el valor materializado contra el RESULT con
la **tolerancia de replay** de este CALC, y el motor materializa con seis decimales.
Sobre `Δ = RESULT-B-ENIGH-2022-P − 0.045694`:

- `ADOPTABLE` — `|Δ| <= tolerancia.abs`: se escribe la cita, **sin tocar `p`**; la sella
  el merge de mesa (el PR ES la firma).
- `NO-ADOPTABLE-POR-GRANO` — `tolerancia.abs < |Δ| < 1e-6`: reproduce al grano de
  `milpa/` pero no al de `verify`. **La cita no se escribe** y el hecho es el hallazgo.
- `NO-ADOPTABLE-POR-DISCREPANCIA` — `|Δ| >= 1e-6`: la re-medición GEN2 no reproduce la
  cifra GEN1 del mismo payload. La cita no se escribe y **eso** es el hallazgo.

No se afloja `tolerancia.abs`, no se redondea ningún RESULT, no se reescribe el `p` del
motor y no se firma `data/corrida0/decisiones.tsv` para que la adopción pase.

## 7 · Contaminación declarada (ADR-46)

Al congelar esta spec, la sesión ya había leído `milpa/tramite.yaml:850-856` —
la serie GEN1 observada de las seis olas, con sus IC. El ensayo **no es ciego** y
§0.2/§5.3 de la sellada dicen exactamente qué se deriva de eso y qué sigue siendo
desconocido.
