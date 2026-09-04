# MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1 — spec Lote 1 (COMMIT-1)

Encargo: `forense/encargos/2026-09-03-MAESTRA38-A1-SONDA-Y-DESCARGA-UNIVERSO-1.md`
(SHA de redacción `2e79d153`). Lote 1 de 3 (D-11): ENADIS · ENCO · ENCRIGE ·
MOTRAL — las cuatro INEGI, agrupadas por el encargo como de mayor rendimiento
esperado (portal público, sin cuenta).

Este documento se escribe **antes de abrir ningún FD ni microdato** de las
cuatro. Lo que sigue sale de (a) identidad pública del instrumento (nombre
oficial, tema, universo — confirmado por búsqueda web de su portal, no de su
contenido interno) y (b) los documentos YA existentes de este repo que
listan qué reglas/necesidades siguen sin instrumento — no de abrir el FD de
ninguna de las cuatro candidatas.

## Corrección a la premisa A.8 del encargo (declarada aquí, no en el encargo)

El encargo afirma "Ninguna fue abierta byte a byte: SIN-FETCH hasta este
acto" para las 12. Verificado contra el árbol (`data/manifiesto.yaml`,
1233 entradas): **falso para Pew** (candidata del Lote 3, no de éste) — hay
dos entradas ya en el manifiesto (`pew_gas2025_social_trust_topline` /
`_shortread`, FP-29) de la misma casa (Pew Research, Global Attitudes
Survey 2025), aunque no bajo el rótulo exacto "Pew Global Attitudes México"
y como *topline* agregado, no microdato. Se declara ahora porque A.6 se
verifica contra el árbol, no se hereda; se resuelve en el Lote 3, no aquí.
Las cuatro candidatas de este Lote 1 (ENADIS, ENCO, ENCRIGE, MOTRAL) **sí**
están en `NO-ENCONTRADO` limpio, verificado por frontera de palabra sobre
manifiesto (0/1233) y cola (0/112) — sin corrección que hacer para éstas.

## Identidad pública de las cuatro (portal, no contenido)

| candidata | nombre oficial | operador | universo/unidad | portal declarado |
|---|---|---|---|---|
| ENADIS | Encuesta Nacional sobre Discriminación | INEGI + CONAPRED + CNDH | personas 12+, hogares | inegi.org.mx/programas/enadis/2022/ (ed. 2022; también 2017) |
| ENCO | Encuesta Nacional sobre Confianza del Consumidor | INEGI + Banxico | hogares urbanos, mensual | inegi.org.mx/programas/enco/ |
| ENCRIGE | Encuesta Nacional de Calidad Regulatoria e Impacto Gubernamental en Empresas | INEGI | unidades económicas (empresas) | inegi.org.mx/programas/encrige/2020/ (ed. 2020; también 2016) |
| MOTRAL | Módulo de Trayectorias Laborales | INEGI + CONSAR | personas 18-54 con experiencia laboral, submuestra ENOE | inegi.org.mx/contenidos/programas/motral/2012/ (ed. 2012 y 2015) |

Fuente de la identificación: búsqueda web contra dominios `inegi.org.mx`
(sitios oficiales del programa), 3/sep/2026 — no contra ningún archivo de
este repo, que no las traía (MOTRAL no aparecía en ningún archivo del árbol
antes de este documento, ni siquiera como mención).

## La pregunta de cada una — qué regla/necesidad la pide, con la cita

**MOTRAL → N35 (`trabajo.prestaciones.formalidad_pesa_mas_que_salario`,
`data/curacion-registro/necesidad-objeto-modelo.tsv:40`).** Es la más fuerte
de las cuatro: MOTRAL mide formalidad (afiliación IMSS/ISSSTE) e ingreso a
lo largo de una trayectoria laboral — exactamente el par que N35 necesita.
**Pero hay una advertencia que se congela aquí, no después de ver el FD**:
`forense/notas/2026-09-03-mapeo-ola6-N5.md` (hoy mismo, sondeo dirigido
sobre el corpus ya indexado) midió que esta regla es **`EXISTE-NO-SATISFACE`**,
no `NO-ENCONTRADO`: el disparador (prestaciones/formalidad) YA está medido
en ENIGH/ENOE — lo que falta es el **desenlace**, una preferencia comparada
explícita ("pesan más que el salario"), y ese documento concluye que
adquirir más payloads del mismo tipo estructural (encuestas INEGI de
estructura y conducta) **no destraba** ese tipo de hueco, que es de
instrumento, no de dato. MOTRAL es, por diseño, exactamente ese tipo de
encuesta (estructura: trayectoria formal/informal). El criterio de abajo
refleja esto sin forzar el resultado.

**ENCRIGE → `tramite.evasion.norma_inutil_sancion_improbable`**
(NO-ENCONTRADO confirmado en `forense/notas/2026-09-01-MAESTRA33-E18-P2-mapeo-tabla.md:22`,
una de las 9 reglas activas NO-ENCONTRADO que el encargo cita). Es la
candidata más limpia de las cuatro: ENCRIGE es, por diseño, la encuesta
INEGI de percepción empresarial sobre trámites — carga regulatoria, utilidad
percibida de los requisitos, y prevalencia/probabilidad de sanción por
incumplimiento. También puede reforzar (no resolver por sí sola, es
`EXISTE-NO-SATISFACE` ya con ENCUCI2020) `tramite.mordida.discrecional` /
`tramite.mordida.con_registro` con un ítem a nivel empresa — se declara como
hallazgo secundario si aparece, no se persigue.

**ENADIS → N15 (`G6.deferencia`)**, exploratorio y declarado **débil desde
antes de este acto**: `forense/REVERIFICACION-DEMANDA-vs-UNIVERSO-2026-08-07-v1_0.md`
(7/ago/2026, §3) ya listaba "deferencia (15) | ENADIS (actitudes) — débil"
un mes antes de este encargo. ENADIS mide discriminación **recibida**
(estar del lado receptor); `deferencia` en el modelo es sobre trato
diferencial **dado** hacia status/autoridad — son conceptos adyacentes, no
el mismo. Se sondea porque es pública y de alto rendimiento esperado
(Lote 1), no porque el ajuste conceptual esté confirmado.

**ENCO → exploratorio, sin cita previa de regla ni necesidad en el repo.**
Hipótesis propia (no heredada): el componente de "intención de compra de
bienes duraderos" de ENCO podría tocar `dinero.consumo.estatus_mediado_por_credito`
(`EXISTE-NO-SATISFACE`, `forense/notas/2026-09-01-MAESTRA33-E18-P2-mapeo-tabla.md:27`
— "falta el cruce con crédito"), **si** el cuestionario pregunta explícitamente
si la compra sería a crédito. Es la candidata más débil de las cuatro; se
sondea porque es INEGI, mensual, de alto rendimiento esperado, no por
convicción de que cierre una regla.

## Qué cuenta como "trae lo que se pide" — congelado antes de abrir el FD

- **MOTRAL / N35**: `EXISTE-SATISFACE` sólo si el cuestionario trae un ítem
  de **preferencia declarada o trade-off** entre salario y prestaciones/
  seguridad social (p. ej. "¿aceptaría un empleo con menor salario si tiene
  prestaciones/seguridad social?" o un ranking de atributos del empleo).
  Si sólo trae afiliación IMSS/ISSSTE + monto de ingreso/prestaciones (lo
  que ya existe en ENOE/ENIGH), el veredicto es `EXISTE-NO-SATISFACE` — se
  registra igual como relación `CANDIDATA` en las tres tablas (N35 pasa de
  0 relaciones a 1), pero no se declara satisfecha. No se amplía este
  criterio después de leer el cuestionario para que calce.
- **ENCRIGE / tramite.evasion...**: `EXISTE-SATISFACE` si trae (a) un ítem
  sobre percepción de utilidad/necesidad de un trámite/regulación específica
  Y (b) un ítem sobre percepción de probabilidad de sanción/verificación por
  incumplimiento — ambos en la misma unidad de análisis (empresa). Si trae
  sólo uno de los dos, `EXISTE-NO-SATISFACE`.
- **ENADIS / N15**: `EXISTE-SATISFACE` sólo si trae un ítem de **trato
  diferencial dado** hacia figuras de autoridad/status (obedecer, no
  contradecir, iniciativa suprimida) — no basta con discriminación recibida
  ni con actitudes generales de tolerancia. Umbral alto a propósito, dado el
  "débil" ya declarado antes de este acto.
- **ENCO / dinero.consumo...**: `EXISTE-SATISFACE` sólo si el módulo de
  bienes duraderos especifica la modalidad de pago (crédito vs. contado) o
  trae desagregación por marca/tipo de bien de estatus. Si es sólo el índice
  agregado de "momento oportuno para comprar", `NO-ENCONTRADO` para esta
  regla (el instrumento no la toca en absoluto, no es un hueco parcial).

## Frase de sello

El veredicto A.4 que produzca la lectura del FD/cuestionario real de cada
una de las cuatro, contra el criterio congelado arriba, es el que se
reporta en COMMIT-2 — no se amplía ni se estrecha el criterio después de
abrir el FD para que el veredicto salga distinto al que el criterio, leído
en frío, habría dado.
