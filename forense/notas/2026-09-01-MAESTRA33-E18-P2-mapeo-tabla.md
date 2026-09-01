# P2 · MAESTRA33-E18 — /mapea sobre las 23 reglas SIN p medida

Encargo: `forense/encargos/2026-09-01-MAESTRA33-E18-MAPEO-ACTIVOS.md`.
Insumo: `forense/notas/2026-09-01-MAESTRA33-E18-P1-reglas-activos-sin-p.md`
(23 filas). Herramienta: `tools/busca_reactivos.py` sobre
`data/inventario-reactivos-v1_2.tsv` (178 246 filas) +
`data/inventario-reactivos-ext-v1_0.tsv` (63 345 filas) — universo
examinado por corrida: **241 591 filas** (A.13, cifra que el propio
comando declara, no recalculada a mano).

Por cada regla se corrieron ≥3 formulaciones (literal / sinónimo /
regex), declaradas antes de correr, log completo en
`/tmp/.../scratchpad/mapea_log.txt` (no versionado — resumen aquí es la
evidencia archivada). Vocabulario A.4: `EXISTE-SATISFACE`,
`EXISTE-NO-SATISFACE`, `NO-ENCONTRADO`, `NO-ACCESIBLE`.

## Tabla completa (23 reglas)

| id(s) | dominio | candidatas (f1/f2/f3) | encuestas/olas vistas | veredicto A.4 | nota |
|---|---|---|---|---|---|
| `tramite.mordida.con_registro` | trámite | 0/11/13 | encup2012 (percepción general de corrupción) | EXISTE-NO-SATISFACE | los hits son percepción difusa de corrupción ("los ciudadanos permiten que haya corrupción"), no la condición del modelo (digitalización/testigo/registro del funcionario) |
| `tramite.evasion.norma_inutil_sancion_improbable` | trámite | 1/0/24 | mixto, sin cita clara de "norma inútil + sanción improbable" | NO-ENCONTRADO | regex genérico (`evad\|incumpl`) trae ruido de otros dominios (impuestos, salud) sin ítem que porte las dos condiciones juntas |
| `tramite.gobierno_digital.coercitivo`+`util_sin_coercion` | trámite | 0/169/160 | ruido alto (codi/spei/"digital" genérico) | EXISTE-NO-SATISFACE | sin ítem que distinga coerción/riesgo fiscal vs. utilidad sin amenaza — el disparador de la regla no está operacionalizado, solo el sustantivo "digital" |
| `dinero.ahorro.volatilidad_horizonte_corto` | dinero | 181/0/221 | ADQ15-CNBV, ENFIH2019, ENGASTO2012/13, EDER2017, ENCUP2012, ENDIREH2016 | EXISTE-NO-SATISFACE | hay ítems de ahorro/tanda dispersos pero ninguno cruza con la condición `segsoc=2 ∨ sin contrato` en un solo instrumento verificado en este acto — declarar candidata puntual pide leer cada payload, fuera de perímetro de /mapea |
| `dinero.planeacion.formal_estable` | dinero | 92/26/112 | **ENFIH2019** (`C_AFORE`/`V_AFORE`), ENGASTO2012/13 (`sar_afore`, con texto "Prestación SAR o AFORE" en la capa `-ext`) | **EXISTE-SATISFACE** | AFORE es el operacionalizador directo de "planeación larga: afore"; 3 payloads, texto legible en la capa `-ext` |
| `dinero.ahorro.informal_sin_puente`+`con_puente_y_respaldo` | dinero | 25/25/28 | genérico "confianza"/"recomendación", sin anclaje a producto financiero | EXISTE-NO-SATISFACE | ninguna candidata liga el canal de confianza personal a la adopción de un producto financiero específico |
| `dinero.consumo.estatus_mediado_por_credito` | dinero | 22/242/69 | ENGASTO2012 (gasto por marca/consumo, 8 filas), ENIGH 2012-2022 (2 filas c/u aprox.) | EXISTE-NO-SATISFACE | los hits de ENIGH son categorías de gasto por rubro, no marca/logo/mensualidades como marcador de estatus — falta el cruce con crédito |
| `dinero.ahorro.seguro_deposito_atenua_aversion` | dinero | 0/0/26 | ninguna candidata directa (regex trae "depósito" genérico bancario) | NO-ENCONTRADO | sin ítem sobre percepción de garantía de depósito (IPAB) |
| `dinero.credito.scoring_alternativo` | dinero | 283/0/1 | ruido: "mora"/"CAT" aparecen como sustantivos sueltos en muchos payloads no financieros | EXISTE-NO-SATISFACE | universo de 283 es dominado por coincidencias de "mora" fuera de contexto crediticio; no se filtró candidata puntual dentro del perímetro de esta corrida |
| `dinero.credito.baja_friccion_usura_dano_downstream` | dinero | 0/0/0 | — | NO-ENCONTRADO | 0 en las 3 formulaciones — BNPL/cobranza no aparecen en el corpus indexado |
| `civico.participacion.contingente` | cívico | 111/9/264 | **ENCUP2012** (participación electoral) | EXISTE-SATISFACE | ítems de intención/participación electoral en ENCUP2012 — una sola ola en el universo examinado |
| `civico.denuncia.sin_seguro`+`con_seguro` | cívico | 158/0/173 | **ENDIREH2016** (serie P13, "¿presentó una queja o denuncia...?") | EXISTE-NO-SATISFACE | ENDIREH2016 mide denuncia de violencia contra mujeres, no delito patrimonial/vehículo asegurado que la regla nombra; y `texto_reactivo` de ENVIPE (la fuente natural) sale vacío en las dos tablas — método `INSPECT_CSV` no extrae texto de ENVIPE, confirmado con `--encuesta envipe` → 0 candidatas en las 2 formulaciones de texto |
| `civico.voto.agencia_con_secreto` | cívico | 2/0/8 | insuficiente | NO-ENCONTRADO | 2-8 candidatas dispersas, sin ítem sobre secreto del voto ligado a transferencia condicionada |
| `civico.voto.clientelar_si_observable` | cívico | 0/0/0 | — | NO-ENCONTRADO | 0 en las 3 formulaciones |
| `civico.clientelismo.turnout_no_vote_choice` | cívico | 0/26/26 | "acarreo" genérico | EXISTE-NO-SATISFACE | sin ítem que separe asistencia a las urnas de elección de voto |
| `civico.transferencia.entitlement_derecho` | cívico | 20/5/21 | ENASEM2024 (`IMSS_BIENESTAR_24`) | EXISTE-NO-SATISFACE | variable de afiliación al programa, no de percepción "se vive como derecho" |
| `civico.transferencia.atribucion_lider` | cívico | 22/0/21 | aprobación presidencial dispersa, sin instrumento identificado limpio en esta corrida | NO-ENCONTRADO | 21-22 candidatas sin encuesta dominante verificable a esta profundidad |
| `civico.protesta.agravio_urbano` | cívico | 1/2/4 | insuficiente | NO-ENCONTRADO | 1-4 candidatas, ninguna clara |
| `civico.autodefensa.agravio_rural` | cívico | 0/0/31 | **ENDIREH2016** ("Juez de paz o Autoridades tradicionales o comunitarias") | EXISTE-NO-SATISFACE | "comunitario" en el corpus refiere a justicia comunitaria/usos y costumbres, no a grupos de autodefensa armada — falso positivo de vocabulario, declarado |
| `familia.seguro.volatilidad_ausencia_estado` | familia | 63/0/63 | **ENIGH 2012/14/16/18/20/22** (`remesas`, `concentradohogar`) | **EXISTE-SATISFACE** | variable de ingreso por remesas, 6 olas, presente en las 6 ediciones bienales de ENIGH |
| `familia.cuidado.recae_mujeres_40mas` | familia | 143/0/145 | ENGASTO2012 (132 filas) + ENIGH 2012-2022 (`cuidados`, 6 olas) | EXISTE-NO-SATISFACE | `cuidados` en ENIGH es gasto monetario en servicios de cuidado (nivel hogar), no la variable persona-nivel de quién cuida — no operacionaliza "recae sobre mujeres 40+" sin cruzar con el módulo de personas |
| `familia.union.baja_garantia_institucional` | familia | 25/0/22 | **ENDIREH2016** (`sit_conyugal`, "Situación conyugal") | EXISTE-NO-SATISFACE | única ola vista en esta corrida es ENDIREH2016 (mujeres); situación conyugal es variable estándar en más encuestas (ENOE, censo) pero esta corrida no las trajo con los términos probados — declarado, no se amplía la búsqueda fuera de las ≥3 formulaciones ya congeladas |
| `familia.cortejo.urbano_joven_apps` | familia | 0/0/10 | ruido de "app"/variable no relacionada | NO-ENCONTRADO | 10 candidatas del regex son ruido (nombres de archivo/variable con "app" como subcadena) |

## Resumen A.4 / A.13

- **EXISTE-SATISFACE:** 3 (`dinero.planeacion.formal_estable`,
  `civico.participacion.contingente`, `familia.seguro.volatilidad_ausencia_estado`).
- **EXISTE-NO-SATISFACE:** 11.
- **NO-ENCONTRADO:** 9.
- **NO-ACCESIBLE:** 0 (las 3 formulaciones corrieron en todas las 23 reglas).
- Total reglas examinadas: 23 (= las 23 de P1 sin p medida).

## Ruta de las EXISTE-NO-SATISFACE y NO-ENCONTRADO

Por mandato del encargo (P3), estas 20 filas **no** entran a ninguna tabla
nueva de este acto: son necesidades nombradas que van al registro del
curador por la vía de A5 (`decide_acquisition` o vía manual precedentada,
`data/curacion-registro/cruce-oferta-demanda-v0_1.tsv`, Dominio 9 del
índice de infraestructura) — fuera de perímetro escribirlas aquí como acto
propio de curación; se declaran para que el acto sucesor las levante.
