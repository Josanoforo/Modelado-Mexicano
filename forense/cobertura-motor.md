# Cobertura del motor · R3-B

*Escrito el 31 de julio de 2026, contra `canon/modelo-decision-v3_4.md` §3.B
(commit de esta misma sesión que le asigna id a las 49 reglas) y
`milpa/procedencia.yaml` v0.2.0. Perímetro ADR-46: `canon/`, `milpa/`,
`corpus/indice.yaml`. No se leyó `data/raw/`, `data/manifiesto.yaml`,
`forense/bitacora.md` ni notas de descarga.*

## Cómo se cuenta

Una regla "tiene valor numérico" si su probabilidad/parámetro está escrito
en algún lado del perímetro (hoy solo `milpa/procedencia.yaml`: no existen
`rules/*.yaml` — `canon` mismo lo declara en §6, "pendiente cuando existan
los 10 rules/*.yaml"). Clase:

- **MEDIDO** — transcripción directa de un dato publicado
- **DERIVADO** — aritmética sobre un MEDIDO (típicamente complemento a 1)
- **ASIGNADO** — juicio informado; la fuente sostiene dirección, no magnitud
- **ninguna** — la regla no tiene ningún número en el perímetro

Tres reglas (`dinero.*` R1.3, `tramite.*` R3.4, `civico.*` R7.2) recibieron
**dos ids** en `procedencia.yaml` para dos condicionales del mismo bullet —
se listan con ambos ids y ambas clases; cuentan como **una** regla, no dos,
en el ENTREGABLE de abajo. Detalle de la anomalía en `forense/hallazgos.md`.

## Tabla — una fila por regla (49)

| # | id | dominio (§) | tier | ¿valor? | clase | dónde vive |
|---|---|---|---|---|---|---|
| 1 | `dinero.ahorro.volatilidad_horizonte_corto` | §3.1 | `[FUERTE]` | No | ninguna | — |
| 2 | `dinero.planeacion.formal_estable` | §3.1 | `[FUERTE]` | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 3 | `dinero.ahorro.informal_sin_puente` + `dinero.ahorro.con_puente_y_respaldo` | §3.1 | `[FUERTE]` | Sí | ASIGNADO (2 entradas) | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 4 | `dinero.consumo.estatus_mediado_por_credito` | §3.1 | `[FUERTE como correlación]` | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 5 | `dinero.ahorro.seguro_deposito_atenua_aversion` | §3.1 | `[MEDIA]` | No | ninguna | — |
| 6 | `dinero.credito.scoring_alternativo` | §3.1 | `[MEDIA]` (AUDITADA, CNBV) | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 7 | `dinero.credito.baja_friccion_usura_dano_downstream` | §3.1 | `[MEDIA]` | No | ninguna | — |
| 8 | `trabajo.jerarquia.deferencia_iniciativa_suprimida` | §3.2 | `[FUERTE]` | No | ninguna | — |
| 9 | `trabajo.liderazgo.benevolencia_legitima` | §3.2 | `[MEDIA-FUERTE]` | No | ninguna | — |
| 10 | `trabajo.prestaciones.formalidad_pesa_mas_que_salario` | §3.2 | `[MEDIA]` | No | ninguna | — |
| 11 | `trabajo.rotacion.joven_urbano_sin_culpa` | §3.2 | `[MEDIA]` | No | ninguna | — |
| 12 | `tramite.mordida.discrecional` | §3.3 | `[FUERTE]` | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 13 | `tramite.mordida.con_registro` | §3.3 | `[FUERTE]` | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 14 | `tramite.evasion.norma_inutil_sancion_improbable` | §3.3 | `[MEDIA]` | No | ninguna | — |
| 15 | `tramite.gobierno_digital.coercitivo` + `tramite.gobierno_digital.util_sin_coercion` | §3.3 | `[MEDIA-FUERTE]` | Sí | ASIGNADO (2 entradas) | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 16 | `salud.atencion.leve_sin_imss` | §3.4 | `[FUERTE]` | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 17 | `salud.atencion.grave` | §3.4 | `[MEDIA]` | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 18 | `salud.prevencion.hombre_sin_permiso` | §3.4 | `[FUERTE]` | Sí | ASIGNADO | `milpa/procedencia.yaml` → `asignados_probabilidad` |
| 19 | `salud.adherencia.desabasto_vs_cuidadora` | §3.4 | `[FUERTE / MEDIA]` (compuesta) | No | ninguna | — |
| 20 | `salud.consumo.sellos_precio_similar` | §3.4 | `[MEDIA]` | No | ninguna | — |
| 21 | `familia.seguro.volatilidad_ausencia_estado` | §3.5 | `[FUERTE]` | No | ninguna | — |
| 22 | `familia.cuidado.recae_mujeres_40mas` | §3.5 | `[FUERTE]` | No | ninguna | — |
| 23 | `familia.union.baja_garantia_institucional` | §3.5 | `[MEDIA]` | No | ninguna | — |
| 24 | `familia.cortejo.urbano_joven_apps` | §3.5 | `[MEDIA / HIPÓTESIS]` | No | ninguna | — |
| 25 | `tiempo.puntualidad.formal_vs_social` | §3.6 | `[MEDIA]` | No | ninguna | — |
| 26 | `tiempo.compromiso.si_voy_incierto` | §3.6 | `[HIPÓTESIS]` | No | ninguna | — |
| 27 | `tiempo.bomberazo.recursos_escasos_urgencias` | §3.6 | `[MEDIA]` | No | ninguna | — |
| 28 | `tiempo.cumplimiento.recordatorio_baja_barrera` | §3.6 | `[MEDIA]` | No | ninguna | — |
| 29 | `civico.participacion.contingente` | §3.7 | `[FUERTE]` | Sí | MEDIDO + DERIVADO | `milpa/procedencia.yaml` → `medidos` + `derivados` |
| 30 | `civico.denuncia.sin_seguro` + `civico.denuncia.con_seguro` | §3.7 | `[FUERTE]` | Sí | MEDIDO+DERIVADO (`sin_seguro`) / ASIGNADO (`con_seguro`) | `milpa/procedencia.yaml` → `medidos`+`derivados` y `asignados_probabilidad` |
| 31 | `civico.voto.agencia_con_secreto` | §3.7 | `[FUERTE]` | Sí | MEDIDO + DERIVADO | `milpa/procedencia.yaml` → `medidos` + `derivados` |
| 32 | `civico.protesta.agravio_urbano` | §3.7 | `[MEDIA-FUERTE]` | No | ninguna | — |
| 33 | `civico.autodefensa.agravio_rural` | §3.7 | `[MEDIA-FUERTE]` | No | ninguna | — |
| 34 | `civico.voto.clientelar_si_observable` | §3.7 | `[MEDIA]` | Sí | MEDIDO + DERIVADO | `milpa/procedencia.yaml` → `medidos` + `derivados` |
| 35 | `civico.clientelismo.turnout_no_vote_choice` | §3.7 | `[MEDIA]` | No | ninguna | — |
| 36 | `civico.transferencia.entitlement_derecho` | §3.7 | `[HIPÓTESIS]` | No | ninguna | — |
| 37 | `civico.transferencia.atribucion_lider` | §3.7 | `[MEDIA]` (correlacional, CONFUNDIDO) | No | ninguna | — |
| 38 | `cooperacion.comite.monitoreo_sancion_visible` | §3.8 | `[FUERTE]` | No | ninguna | — |
| 39 | `cooperacion.tanda.conoce_organizadora` | §3.8 | `[FUERTE]` | No | ninguna | — |
| 40 | `cooperacion.confianza.puente_personal` | §3.8 | `[FUERTE]` | No | ninguna | — |
| 41 | `cooperacion.faena.sancion_social_pueblo_mestizo` | §3.8 | `[MEDIA]` | No | ninguna | — |
| 42 | `informacion.credibilidad.allegado_confianza` | §3.9 | `[MEDIA]` | No | ninguna | — |
| 43 | `informacion.deferencia.costo_acceso_experto` | §3.9 | `[FUERTE]` | No | ninguna | — |
| 44 | `salud.vacunacion.disponible` ⚠️ id con dominio equivocado (vive en §3.9, prefijo dice `salud.`) | §3.9 | `[FUERTE]` | Sí | DERIVADO (cuasi-medido) | `milpa/procedencia.yaml` → `derivados` |
| 45 | `informacion.escuela.miedo_a_caer_clase_media` | §3.9 | `[MEDIA]` | No | ninguna | — |
| 46 | `comunicacion.rechazo.indirecto_face` | §3.10 | `[FUERTE]` | No | ninguna | — |
| 47 | `comunicacion.retroalimentacion.privada_publica_capital_social` | §3.10 | `[MEDIA-FUERTE]` | No | ninguna | — |
| 48 | `comunicacion.inseguridad.ver_oir_callar` | §3.10 | `[FUERTE]` | No | ninguna | — |
| 49 | `comunicacion.directividad.regional_generacional` | §3.10 | `[MEDIA]` | No | ninguna | — |

## ENTREGABLE — el número

**15 de las 49 reglas tienen valor numérico en el perímetro; 34 no tienen
ninguno** (ni MEDIDO, ni DERIVADO, ni ASIGNADO — ni en `procedencia.yaml`
ni en `canon`).

Desglose de las 15: 4 MEDIDO (con su complemento DERIVADO) + 1 DERIVADO
cuasi-medido (`salud.vacunacion.disponible`) + 13 entradas ASIGNADO en
`procedencia.yaml` repartidas sobre **10** reglas propias (3 reglas —
R1.3, R3.4, R7.2 en la numeración `RX.Y` de `canon` §7 — reciben 2 entradas
ASIGNADO cada una, para las dos mitades condicionales de un mismo bullet).

**Esto REFUTA el "18/31" que `milpa/procedencia.yaml` `estado:` declara
hoy.** El archivo cuenta **entradas** (4 MEDIDO + 1 DERIVADO + 13 ASIGNADO
= 18) y las trata como si fueran 18 reglas distintas. No lo son: tres pares
de esas entradas apuntan a la **misma** regla —

- `dinero.ahorro.informal_sin_puente` + `dinero.ahorro.con_puente_y_respaldo` → una sola regla (§3.1, canal de confianza personal)
- `tramite.gobierno_digital.coercitivo` + `tramite.gobierno_digital.util_sin_coercion` → una sola regla (§3.3, el gate CoDi/SPEI)
- `civico.denuncia.sin_seguro` + `civico.denuncia.con_seguro` → una sola regla (§3.7, cifra negra / robo asegurado)

Contando reglas (no entradas): **15 reglas con valor, 34 sin valor** —
no 18/31. Ver `forense/hallazgos.md` para el detalle línea por línea.

## Dominios sin ninguna cobertura

Confirmado por conteo directo de esta tabla, consistente con lo que
`procedencia.yaml` `estado:` ya señalaba: **§3.2 (trabajo), §3.5 (familia),
§3.6 (tiempo), §3.8 (cooperación) y §3.10 (comunicación)** — 20 reglas —
no tienen ni una sola regla con valor. §3.9 tiene 1 de 4 (y esa una con el
id de dominio equivocado, ver arriba).
