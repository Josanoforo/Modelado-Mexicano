# Cobertura conocida de conductas U5 · RETROSPECTIVA

Esta lista coteja conductas expresas de `milpa/tramite.yaml` y la matriz de consumo de U1 (`origin/codex/astra4-catalogo-1`, commit de entrega `3d8e82fb`) con el canon regional. **Es un mínimo conocido, no un denominador exhaustivo del catálogo adoptado/adoptable.** U1 sigue en rama separada; no se infiere cierre de universo por la ausencia de una fila aquí.

El [snapshot de alcance U1](alcance-u1-v1_0.tsv) se deriva por `python3 tools/astra/region/alcance_u1.py` del commit fijado: identifica 37 identidades activas/adoptables de ENVIPE, ENCIG y ENIF, con RESULT consumidor y estado regional. Algunas son códigos de celda/interacción y requieren desdoblar el estimando antes de contar una expectativa geográfica; por eso **37 no es el denominador de cobertura de conductas**. El piso ENIF `informal_cualquiera` 18+ del portafolio ya cubre el consumidor general; la serie histórica 18–70 permanece diferenciada.

| Instrumento | Conducta / consumidor | Dominio R1 esperado | Estado U5 | Motivo de no medición cuando aplica |
|---|---|---|---|---|
| ENVIPE | `evade_norma_envipe2025` | 32 entidades de residencia | Medida, 2023–25 | — |
| ENVIPE | `cumple_norma_envipe2025` | 32 entidades | Medida, 2023–25 | Complemento determinista con RESULT sellado propio; mismo denominador. |
| ENVIPE | `denuncia_con_miedo_o_desconfianza`, `denuncia_por_otra_razon` | 32 entidades | Pendiente | Reactivos, códigos y universos separados por fijar. |
| ENVIPE | `civico.denuncia.con_seguro_ejes_envipe2025` | 32 entidades | Pendiente | Dominio de robo total de vehículo pequeño; R2 podría suprimir muchas celdas. |
| ENCIG | canal digital de luz / `adopta_encig2025_luz` | 32 entidades, marco urbano 100 mil+ | Medida, 2017–25 | Misma codificación y denominador documentados; nombre consumidor 2025 distinto. |
| ENCIG | `paga_mordida_encig2025`, variante primaria | 32 entidades, marco urbano 100 mil+ | Medida, 2025 | Primer inciso de **solicitud**, no pago; serie completa 2011–25 pendiente. |
| ENCIG | variantes presencial/digital `_r2` de mordida | 32 entidades, marco urbano 100 mil+ | Medidas, 2025 | Unidad registro sin deduplicar; R2 suprime celdas pequeñas. |
| ENIF | `tiene_ahorros_enif2024` | seis regiones oficiales | Medida, 2024, 18+ | — |
| ENIF | `no_tiene_ahorros_enif2024` | seis regiones oficiales | Medida, 2024, 18+ | RESULT propio del portafolio. |
| ENIF | `informal_cualquiera` | seis regiones oficiales | Medida, 2024, 18+; serie 2018/21/24, 18–70 | Dominios separados en el canon. |
| ENIF | `ahorra_solo_informal`, `ahorra_solo_formal`, `ahorra_ambas_vias`, `formal_cualquiera`, `no_ahorra` | seis regiones oficiales | Medidas, 2024, 18+ | RESULT por conducta/región. |
| ENIF | `horizonte_corto`, `horizonte_no_corto` por seguridad social | seis regiones oficiales | Medidas, 2024 | Cuatro tasas condicionales con denominadores separados; 24/24 publicables. No se crea tasa general mezclando los dominios. |
| ENIF | `desconfianza_o_mal_servicio_como_razon_principal_*` | seis regiones oficiales | Medidas con supresión R2, 2024 | Conoce protección: 0/6 publicables; no conoce: 5/6. Las siete filas restantes conservan n y cifra nula. |

La fracción **medida dentro de cada serie corrida** se deriva del canon: todas las filas esperadas de sus pisos, olas históricas y bloques de consumidores/derivación están presentes, incluidas las que R2 suprime. Esta fracción no es cobertura del catálogo general. En el lote actual, `python3 tools/astra/region/publica.py` declara 620 filas: 550 de diseño o derivación y 70 de IC predictivo; 593 PUBLICABLE y 27 SUPRIMIDA-N. Los denominadores de conductas pendientes no se convierten en ceros. El complemento ENVIPE no añade un evento independiente al mapa de estabilidad: su comparación dentro/fuera del IC se invierte algebraicamente y da la misma categoría.

El efecto urbano documentado es un **límite del universo ENCIG**: sus resultados no incluyen localidades rurales ni ciudades menores del marco. ENIF tiene regiones de diseño sin entidad. ENVIPE usa residencia, no lugar de ocurrencia. Estas exclusiones no miden por sí solas sesgo de selección ni permiten atribuir una cifra a población indígena o clase popular. El mapa temporal tampoco convierte la diferencia entre dos olas en cambio sostenido.
