# MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1 — spec Lote 2 (COMMIT-1)

Lote 2 de 3: CONEVAL · ENJUVE · ENVE · ENH. Igual disciplina que Lote 1
(`spec-lote-1.md`): identidad pública antes de abrir contenido, criterio
de "trae lo que se pide" congelado antes del FD. Verificado en A.8 del
encargo: las cuatro NO-ENCONTRADO en manifiesto (1233) y cola (112 antes
de Lote 1) por frontera de palabra — sin corrección que hacer (a diferencia
de Pew en Lote 3).

## Identidad pública

| candidata | nombre oficial | operador | nota |
|---|---|---|---|
| CONEVAL | Medición multidimensional de la pobreza, indicadores municipales | CONEVAL (no INEGI) | CONEVAL no levanta encuesta propia — procesa ENIGH/MCS-ENIGH (ya en corpus). Su producto propio y descargable es el INDICADOR derivado (pobreza/carencias por municipio, 2010-2020), en coneval.org.mx y espejado en datos.gob.mx |
| ENJUVE | Encuesta Nacional de Juventud | IMJUVE (no INEGI) | **Advertencia de premisa, verificada por búsqueda pública, no por el corpus**: ediciones 2000/2005/2010 únicamente — sin edición desde hace ~16 años a la fecha de este acto. La sonda de este lote declara esto en A.6, no lo descubre después |
| ENVE | Encuesta Nacional de Victimización de Empresas | INEGI | ed. 2022, 2024 — victimización de empresas (robo, extorsión, corrupción) |
| ENH | Encuesta Nacional de los Hogares | INEGI | ed. 2016, 2017 — demografía de hogar, salud/bienestar, TIC; propósito general |

## La pregunta de cada una

**ENVE → refuerza `tramite.mordida.discrecional`/`tramite.mordida.con_registro`
(ya `EXISTE-NO-SATISFACE` con ENCUCI2020) y potencialmente N18 (junto con
ENCRIGE, Lote 1) — hipótesis propia, sin cita previa en el repo.** ENVE mide
victimización de empresas por corrupción/extorsión de funcionarios, a nivel
empresa — mismo universo que ENCRIGE, ángulo distinto (delito vs. carga
regulatoria).

**CONEVAL, ENJUVE, ENH → exploratorias, sin cita previa de regla ni
necesidad en el repo.** Se sondean porque el encargo pide cobertura del
universo público completo (§0 "sondear... lo que sea público"), no porque
haya una hipótesis de cierre. Si el sondeo revela un ítem que ata a una
regla NO-ENCONTRADO/E18/Ola6 no anticipada aquí, se declara al leer el FD
(A.4), no se fuerza de antemano.

## Qué cuenta como "trae lo que se pide"

- **ENVE**: `EXISTE-SATISFACE` (para el refuerzo de `tramite.mordida.*`) si
  trae un ítem de corrupción/mordida en trámites **a nivel empresa**,
  comparable en granularidad al de ENCUCI2020 a nivel persona. Si sólo mide
  delito convencional (robo, extorsión criminal sin funcionario público),
  `NO-ENCONTRADO` para este refuerzo — la victimización por delito común no
  es mordida en trámite.
- **CONEVAL**: no hay regla que cerrar; el criterio es de **cobertura**, no
  de satisfacción — se descarga si el archivo es público y es un indicador
  real (no un mapa/infografía), se registra como fuente de inventario.
- **ENJUVE**: igual — cobertura, no cierre de regla. Además: si la sonda
  confirma que no hay edición posterior a 2010, la pieza se registra como
  `OBTENIDO` (edición histórica) con la antigüedad declarada explícitamente
  en `usado_para`, no oculta.
- **ENH**: igual — cobertura.

## Frase de sello

El veredicto A.4 (para ENVE) o el simple hecho de "descargado/registrado"
(para CONEVAL/ENJUVE/ENH, sin regla que cerrar) que produzca la lectura
real del FD/portal es el que se reporta en COMMIT-2 — no se busca una
regla a la fuerza para justificar la descarga de las tres exploratorias.
