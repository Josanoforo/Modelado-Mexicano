# Cobertura de celdas regionales medidas · RETROSPECTIVA

Generado por `python3 tools/astra/region/cobertura.py` desde el canon y el snapshot U1 fijado en `3d8e82fb`. La tabla TSV enumera **todas** las geografías esperadas de la última ola medida por conducta; la suma publicable + suprimida + otros = esperadas. No interpreta una supresión como cero.

Identidades U1 dictaminadas: 37. De ellas, 11 tienen piso regional, una identidad de seguro tiene 128/128 celdas medidas pero suprimidas por R2, cuatro reglas de ejes tienen conducta base medida sin extender sus cruces a región, y 21 son celdas de interacción, no conductas adicionales. Las 37 identidades no son 37 conductas independientes.

| Instrumento | Conducta | Última ola | Publicables / esperadas | SUPRIMIDA-N |
|---|---|---:|---:|---:|
| ENCIG | `adopta_encig2025_luz` | 2025 | 32/32 | 0 |
| ENCIG | `canal_digital_luz` | 2023 | 32/32 | 0 |
| ENCIG | `paga_mordida_encig2025` | 2025 | 32/32 | 0 |
| ENCIG | `paga_mordida_encig2025_digital_r2` | 2025 | 15/32 | 17 |
| ENCIG | `paga_mordida_encig2025_presencial_r2` | 2025 | 29/32 | 3 |
| ENIF | `ahorra_ambas_vias` | 2024 | 6/6 | 0 |
| ENIF | `ahorra_solo_formal` | 2024 | 6/6 | 0 |
| ENIF | `ahorra_solo_informal` | 2024 | 6/6 | 0 |
| ENIF | `desconfia_conoce_proteccion` | 2024 | 0/6 | 6 |
| ENIF | `desconfia_no_conoce_proteccion` | 2024 | 5/6 | 1 |
| ENIF | `formal_cualquiera` | 2024 | 6/6 | 0 |
| ENIF | `horizonte_corto_con_ss` | 2024 | 6/6 | 0 |
| ENIF | `horizonte_corto_no_trabaja` | 2024 | 6/6 | 0 |
| ENIF | `horizonte_corto_sin_ss` | 2024 | 6/6 | 0 |
| ENIF | `horizonte_no_corto_con_ss` | 2024 | 6/6 | 0 |
| ENIF | `horizonte_no_corto_sin_ss` | 2024 | 6/6 | 0 |
| ENIF | `informal_cualquiera` | 2024 | 6/6 | 0 |
| ENIF | `informal_cualquiera_18a70` | 2024 | 6/6 | 0 |
| ENIF | `no_ahorra` | 2024 | 6/6 | 0 |
| ENIF | `no_tiene_ahorros_enif2024` | 2024 | 6/6 | 0 |
| ENIF | `tiene_ahorros_enif2024` | 2024 | 6/6 | 0 |
| ENVIPE | `cumple_norma_envipe2025` | 2025 | 32/32 | 0 |
| ENVIPE | `denuncia_con_miedo_o_desconfianza` | 2025 | 31/32 | 1 |
| ENVIPE | `denuncia_con_seguro` | 2025 | 0/32 | 32 |
| ENVIPE | `denuncia_por_otra_razon` | 2025 | 31/32 | 1 |
| ENVIPE | `denuncia_sin_seguro` | 2025 | 0/32 | 32 |
| ENVIPE | `evade_norma_envipe2025` | 2025 | 32/32 | 0 |
| ENVIPE | `no_denuncia_con_seguro` | 2025 | 0/32 | 32 |
| ENVIPE | `no_denuncia_sin_seguro` | 2025 | 0/32 | 32 |

El denominador de esta tabla son **celdas de conductas efectivamente medidas en su última ola**, no todas las posibles interacciones del catálogo. Los cruces U1 edad/sexo/escolaridad o interacción no se transforman en región×eje sin una spec propia. La tabla deja explícito ese límite; no declara cobertura total del catálogo general ni una cifra de sesgo rural, indígena o popular. ENCIG cubre solo su marco urbano; ENIF publica región oficial sin estados; ENVIPE usa residencia, no lugar del delito.
