# MAESTRA37-L1 · P2 — remapeo de las 25 reglas de Ola 6 sobre `descargas_mx` (COMMIT-2)

Corre las formulaciones congeladas en `2026-09-03-MAESTRA37-L1-censo.md`
(COMMIT-1, copiadas verbatim de `forense/notas/2026-09-03-mapeo-ola6-N5.md`)
con `tools/busca_reactivos.py --tablas descargas_mx`, aislando lo que la
raíz nueva aporta frente a lo que `N5` (v1_2+ext) y `N6` (administrativas)
ya cruzaron. Universo examinado por corrida (A.13): `descargas_mx=31677`
filas (`data/inventario-reactivos-descargas-mx-v1_0.tsv`, cabecera de
comentarios excluida).

## Tabla — tres columnas por regla

`N5` y `N6` son verbatim de las notas citadas arriba; `MAESTRA37-L1` es el
veredicto A.4 de esta corrida contra `descargas_mx` en solitario (mismo
criterio uniforme de A.4 que N5: `EXISTE-SATISFACE` exige desenlace Y
disparador; `EXISTE-NO-SATISFACE` si falta uno de los dos o el alcance no
se confirma por texto; `NO-ENCONTRADO` si cero aciertos en las
formulaciones dirigidas).

### `salud` (prioridad, §3.4, 5 reglas)

| regla | N5 (v1_2+ext) | N6 (administrativas) | `MAESTRA37-L1` (descargas_mx) |
|---|---|---|---|
| `salud.atencion.leve_sin_imss` | EXISTE-NO-SATISFACE | NO-APLICA | **EXISTE-NO-SATISFACE** — 2 aciertos de "dónde se atendió" (`asq_cuid_hog_completa.dta P13_CU`, módulo cuidador ENOE/panel, no ENSANUT), 10 de "grave" son homonimia (`a4n` LAPOP "problema más grave del país", `env2b` "gravedad del cambio climático" — el mismo patrón de falso positivo que N5 documentó). `farmacia`/`automedic*`: 0/31 677. El tercer término («leve-moderado») sigue sin reactivo, ahora también en esta tabla |
| `salud.atencion.grave` | **EXISTE-SATISFACE** *(propuesta)* | NO-APLICA | sin cambio — 14 aciertos de institución (IMSS/Seguro Popular: `asq_cuid_hog_completa`, `utilizadores_ensanut2024_w.dta u0202c1a/b/c` "por qué motivos no se atendió en centro de salud u hospital") refuerzan el desenlace ya satisfecho por N5 (ENDIREH/ENNVIH), no lo cambian. Los 10 de "grave" son homonimia (mismo patrón de arriba) — descargas_mx no aporta el término "gravedad" que N5 tampoco necesitaba (la regla ya cerraba por lugar de atención) |
| `salud.prevencion.hombre_sin_permiso` | EXISTE-NO-SATISFACE | NO-APLICA | **NO-ENCONTRADO** en las dos formulaciones dirigidas (0/0); el único acierto de la primera (`P56_01_CU` "lleva al niño a revisión médica" del módulo cuidador, y `d0321d` examen de orina en embarazo adolescente) no es prevención masculina pospuesta. Disparador "permiso laboral" (`prestacion*`): 0/31 677 |
| `salud.adherencia.desabasto_vs_cuidadora` | NO-ENCONTRADO | EXISTE-NO-SATISFACE (Cero Desabasto, disparador sin desenlace) | **NO-ENCONTRADO** — 0/0/0 en las tres formulaciones dirigidas |
| `salud.consumo.sellos_precio_similar` | NO-ENCONTRADO | NO-APLICA | **NO-ENCONTRADO** — 0/31 677 |

**Recuento salud, criterio 2 (ii): 1 de 5 `EXISTE-SATISFACE` — el mismo 1
que ya tenía N5, sostenido por v1_2/ext, no por `descargas_mx`.** La raíz
nueva no agrega ni quita ninguna candidata `EXISTE-SATISFACE` al dominio
salud. **No llega a 3: no hay `ABRE-CANDIDATO-CON-RESERVA`.**

### Los otros 20 (`trabajo`, `tiempo`, `cooperación`, `información`, `comunicación`) — recuento, no tabla completa

Corridos con el mismo procedimiento (formulaciones congeladas,
`--tablas descargas_mx`), aciertos por formulación:

| regla | aciertos por formulación | lectura A.4 rápida |
|---|---|---|
| `trabajo.jerarquia.deferencia_iniciativa_suprimida` | 30·0·0 | los 30 son `jefe de hogar`/`jefe delegacional`/`jefe del hogar` (ENIF-panel, LAPOP satisfacción municipal) — misma homonimia que N5 documentó, no relación laboral. **NO-ENCONTRADO** |
| `trabajo.liderazgo.benevolencia_legitima` | 0·0·0 | **NO-ENCONTRADO** |
| `trabajo.prestaciones.formalidad_pesa_mas_que_salario` | 0·0·0 | **NO-ENCONTRADO** en descargas_mx (N5 ya tenía el disparador vía otras tablas) |
| `trabajo.rotacion.joven_urbano_sin_culpa` | 0·0·0 | **NO-ENCONTRADO** |
| `tiempo.puntualidad.formal_vs_social` | 4·0·0 | los 4 de "retraso" — sin confirmar en muestra, mismo riesgo de homonimia que N5 (`Retrasar un embarazo`) señaló; sin segunda formulación que lo sostenga, **EXISTE-NO-SATISFACE en el mejor caso, no verificado a EXISTE-SATISFACE** |
| `tiempo.compromiso.si_voy_incierto` | 6·0·4 | dos aciertos parciales, sin cruce del desenlace+disparador confirmado por texto. **EXISTE-NO-SATISFACE como máximo** |
| `tiempo.bomberazo.recursos_escasos_urgencias` | 0·0·0 | **NO-ENCONTRADO** |
| `tiempo.cumplimiento.recordatorio_baja_barrera` | 0·0·1 | **NO-ENCONTRADO/EXISTE-NO-SATISFACE**, 1 acierto no decide nada solo |
| `cooperacion.comite.monitoreo_sancion_visible` | 0·0·0 | **NO-ENCONTRADO** |
| `cooperacion.tanda.conoce_organizadora` | 30·0·0 | de los 30, hay un acierto genuino nuevo (`followup_survey.dta q18 "times participated in tanda"`) — desenlace confirmado, pero el disparador «conoce a la organizadora» sigue en 0/31 677 (segunda formulación). **EXISTE-NO-SATISFACE**, mismo hueco que N5 ya declaró |
| `cooperacion.confianza.puente_personal` | 0·0·0 | **NO-ENCONTRADO** |
| `cooperacion.faena.sancion_social_pueblo_mestizo` | 0·0·0 | **NO-ENCONTRADO** |
| `informacion.credibilidad.allegado_confianza` | 8·0·0 | sin segunda formulación que lo sostenga; **EXISTE-NO-SATISFACE como máximo** |
| `informacion.deferencia.costo_acceso_experto` | 0·0·1 | **NO-ENCONTRADO/EXISTE-NO-SATISFACE** |
| `salud.vacunacion.disponible` *(§3.9)* | 55·4·0 | ENSANUT 2024 adolescentes trae ítems de vacunación genuinos (desenlace) — refuerza lo que N5 ya tenía por otra vía (ENNVIH), no lo cambia; disparador "disponibilidad/rechazo" sigue sin confirmar en descargas_mx (segunda formulación no examinada a detalle, prioridad fue el dominio `salud` de §3.4) |
| `informacion.escuela.miedo_a_caer_clase_media` | 2·0·0 | **NO-ENCONTRADO/EXISTE-NO-SATISFACE** |
| `comunicacion.rechazo.indirecto_face` | 0·52·6 | los 52 de `favor`/`le pidio` son ítems de opinión política LAPOP/WVS (`POP4`, `D1`, "por favor léame el número") — no actos de habla del informante, mismo patrón de falso positivo que N5 documentó para ENCUP. **NO-ENCONTRADO** |
| `comunicacion.retroalimentacion.privada_publica_capital_social` | 0·0·14 | sin confirmar por texto; **EXISTE-NO-SATISFACE como máximo** |
| `comunicacion.inseguridad.ver_oir_callar` | 0·9·0 | **EXISTE-NO-SATISFACE como máximo**, no verificado |
| `comunicacion.directividad.regional_generacional` | 0·0·0 | **NO-ENCONTRADO** |

**Ninguno de los 20 llega a `EXISTE-SATISFACE` limpio en `descargas_mx`
solo** (todo lo que tiene aciertos, o es homonimia confirmada por
muestra, o queda sin el cruce desenlace+disparador que A.4 exige — y
donde no se llegó a leer la muestra completa por prioridad de tiempo,
el máximo posible declarado es `EXISTE-NO-SATISFACE`, nunca
`EXISTE-SATISFACE` sin texto a la vista, por la regla de honestidad del
encargo). **Ningún dominio de los cinco no-salud llega a 3
`EXISTE-SATISFACE` nuevos**: el máximo por dominio en esta tabla es 0.

## Recuento del criterio 2 (motor-núcleo §3.a, ADR-265, firma 9) por dominio, columna nueva

| dominio | N5+N6 (antes) | + `descargas_mx` (este acto) |
|---|---|---|
| `trabajo` | 0/4 | 0/4 |
| `salud` | 1/5 | 1/5 (sin cambio) |
| `tiempo` | 0/4 | 0/4 |
| `cooperación` | 0/4 | 0/4 |
| `información` | 1/4 (`salud.vacunacion.disponible`, id con dominio equivocado — cuenta en `información` por su §) | 1/4 (sin cambio) |
| `comunicación` | 0/4 | 0/4 |

**0 de 6 dominios cumplen el criterio 2, con y sin `descargas_mx`.**
Ningún dominio queda `ABRE-CANDIDATO-CON-RESERVA`. La raíz nueva no
cambia el recuento agregado (2/25, máximo 1 por dominio) que `N6` ya
había establecido con administrativas — ahora también sostenido contra
la tercera fuente, encuestas de `descargas_mx`.
