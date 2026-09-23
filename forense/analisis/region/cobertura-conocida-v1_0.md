# Cobertura conocida de conductas U5 · RETROSPECTIVA

Esta lista coteja conductas expresas de `milpa/tramite.yaml` y la matriz de consumo de U1 (`origin/codex/astra4-catalogo-1`, commit de entrega `3d8e82fb`) con el canon regional. **Es un mínimo conocido, no un denominador exhaustivo del catálogo adoptado/adoptable.** U1 sigue en rama separada; no se infiere cierre de universo por la ausencia de una fila aquí.

El [snapshot de alcance U1](alcance-u1-v1_0.tsv) se deriva por `python3 tools/astra/region/alcance_u1.py` del commit fijado: identifica 37 identidades activas/adoptables de ENVIPE, ENCIG y ENIF, con RESULT consumidor y estado regional. Algunas son códigos de celda/interacción y requieren desdoblar el estimando antes de contar una expectativa geográfica; por eso **37 no es el denominador de cobertura de conductas**. El piso ENIF `informal_cualquiera` 18+ del portafolio ya cubre el consumidor general; la serie histórica 18–70 permanece diferenciada.

| Instrumento | Conducta / consumidor | Dominio R1 esperado | Estado U5 | Motivo de no medición cuando aplica |
|---|---|---|---|---|
| ENVIPE | `evade_norma_envipe2025` | 32 entidades de residencia | Medida, 2023–25 | — |
| ENVIPE | `cumple_norma_envipe2025` | 32 entidades | Medida, 2023–25 | Complemento determinista con RESULT sellado propio; mismo denominador. |
| ENVIPE | `denuncia_con_miedo_o_desconfianza`, `denuncia_por_otra_razon` | 32 entidades | Pendiente | Reactivos, códigos y universos separados por fijar. |
| ENVIPE | `civico.denuncia.con_seguro_ejes_envipe2025` | 32 entidades | Pendiente | Dominio de robo total de vehículo pequeño; R2 podría suprimir muchas celdas. |
| ENCIG | `canal_digital_luz` | 32 entidades, marco urbano 100 mil+ | Medida, 2017–23 | — |
| ENCIG | `paga_mordida_encig2025`, variante primaria | 32 entidades, marco urbano 100 mil+ | Pendiente | Serie 2011–25 y codificación de solicitud/pago requieren spec propia. |
| ENCIG | `adopta_encig2025_luz` | 32 entidades, marco urbano 100 mil+ | Pendiente | No equivale al canal digital medido. |
| ENCIG | variantes presencial/digital de mordida | 32 entidades, marco urbano 100 mil+ | Pendiente | Consumidor y reserva de semántica/deduplicación deben respetarse; no se sustituyen con canal. |
| ENIF | `tiene_ahorros_enif2024` | seis regiones oficiales | Medida, 2024, 18+ | — |
| ENIF | `no_tiene_ahorros_enif2024` | seis regiones oficiales | Medida, 2024, 18+ | RESULT propio del portafolio. |
| ENIF | `informal_cualquiera` | seis regiones oficiales | Medida, 2024, 18+; serie 2018/21/24, 18–70 | Dominios separados en el canon. |
| ENIF | `ahorra_solo_informal`, `ahorra_solo_formal`, `ahorra_ambas_vias`, `formal_cualquiera`, `no_ahorra` | seis regiones oficiales | Medidas, 2024, 18+ | RESULT por conducta/región. |
| ENIF | `horizonte_corto`, `horizonte_no_corto` | seis regiones oficiales | Pendiente | Identidad del estimando y batería pendiente. |
| ENIF | `desconfianza_o_mal_servicio_como_razon_principal_*` | seis regiones oficiales | Pendiente | Subgrupos de conocimiento de protección; R2 material. |

La fracción **medida dentro de cada serie corrida** se deriva del canon: todas las filas esperadas de sus tres pisos iniciales, ocho olas históricas, bloque de portafolio y complemento ENVIPE están presentes, incluidas las que R2 pudiera suprimir. Esta fracción no es cobertura del catálogo general. En el lote actual, `python3 tools/astra/region/publica.py` declara 386 filas y estados; los denominadores de conductas pendientes no se convierten en ceros. El complemento ENVIPE no añade un evento independiente al mapa de estabilidad: su comparación dentro/fuera del IC se invierte algebraicamente y da la misma categoría.

El efecto urbano documentado es un **límite del universo ENCIG**: sus resultados no incluyen localidades rurales ni ciudades menores del marco. ENIF tiene regiones de diseño sin entidad. ENVIPE usa residencia, no lugar de ocurrencia. Estas exclusiones no miden por sí solas sesgo de selección ni permiten atribuir una cifra a población indígena o clase popular. El mapa temporal tampoco convierte la diferencia entre dos olas en cambio sostenido.
