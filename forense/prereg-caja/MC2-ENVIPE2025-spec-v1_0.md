# MC2 · ENVIPE 2025 (+ ENVIPE 2024) · cifra negra, extorsión telefónica, preocupaciones y espacios inseguros · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENVIPE 2025, entorno CAJA, rama
`acto/gen2-medicion-carriles-2--envipe2025`. CALC: `data/corrida0/CALC-MC2-ENVIPE2025-0001`
(medidor `medidor.py`; prueba sintética `tests/test_mc2_envipe2025.py`). Encargo:
`forense/encargos/2026-09-28-GEN2-MEDICION-CARRILES-2.md`. Todo es **RETROSPECTIVA**. No adopta.

## 0 · Premisas, reserva y lectura previa

- `[EJECUTADO]` Payloads (manifiesto): `envipe2025_csv` (miembros
  `conjunto_de_datos_tmod_vic_envipe2025.csv` y `conjunto_de_datos_tper_vic1_envipe2025.csv`) y
  `envipe2024_csv` (`conjunto_de_datos_tper_vic1_envipe2024.csv`); el preflight compara sha256.
- `[EJECUTADO]` Reserva E.6: ENVIPE 2026 es la ola RESERVADA (memoria operativa §1) y no es input.
  ENVIPE 2025 está **abierta** (memoria operativa §1: «ENCIG 2025 y ENVIPE 2025: abiertas»; CALC
  sellados `CALC-PDR1-ENVIPE2025-0001`, `CALC-ALT-M22-ENVIPE2025-0001`,
  `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001`). ENVIPE 2024 es ola vista
  (`CALC-ENVIPE-PERCEPCION-2024-0001`, `CALC-PISOS-ENVIPE2024-EJES-0001/-0002`).
  `corpus_loader.motivo_reserva` → vacío para ambos ids.
- Lectura de estructura antes del COMMIT-1 (permitida, declarada): FD `fd_envipe2025.pdf` y
  `fd_envipe2024.pdf` (texto por `pdftotext`; secciones 4 y módulo de victimización: BPCOD,
  BP1_5A, BP1_20–BP1_25, BP5_1, FAC_DEL, AP4_2, AP4_3, AP4_4, AP4_10), la **cabecera** de los tres
  miembros, el índice de tablas del zip y el lector del medidor sellado `CALC-PDR1-ENVIPE2025-0001`
  (fin de línea `\r` solo). Ningún registro leído, contado ni tabulado. De
  `CALC-ENVIPE-PERCEPCION-2024-0001` se leyeron **sólo los ids** de sus RESULT, no sus valores.
- E.5 (lo sellado se cita): `CALC-ENVIPE-PERCEPCION-2024-0001` ya trae para 2024 ESTADO-INSEGURO
  (AP4_3_3; nacional y por entidad, incl. `ENTIDAD-25` Sinaloa), INSEGURO-CAMINAR-DE-NOCHE y
  DEJO-PERMITIR-MENORES-SALIR-SOLOS; `CALC-PDR1-ENVIPE2025-0001` trae AP4_11_06 (acciones conjuntas
  con vecinos). Ningún CALC sellado mide BP1_24 (carpeta), la cifra negra como tal, BP1_5A_2 entre
  extorsiones, AP4_2 (preocupaciones), AP4_4 por espacio, AP4_10_01 ni AP4_3_3 de 2025 para
  Sinaloa. Aquí `EDO-INSEGURO-2024-*` se recalcula sólo como insumo de la diferencia 2025−2024; su
  punto debe coincidir con el sellado y se reporta como control.

## 1 · Variables por texto (A.15)

**Delitos (ENVIPE 2025, módulo de victimización; unidad delito ocurrido en 2024, ponderador
`FAC_DEL` «Ponderador que se utiliza para estimar resultados de los delitos registrados en el
Módulo de delitos»):**
- `BPCOD` código de delito («CÓDIGOS PARA DELITOS»): 09 = «Amenazas, presiones o engaños para
  exigirle dinero o bienes; o para que hiciera algo o dejara de hacerlo (extorsión)».
- `BP1_20` «1.20 ¿Acudió ante el Ministerio Público o Fiscalía Estatal a denunciar el delito?» 1/2;
  `BP1_21` «1.21 ¿Algún(a) otro(a) integrante de este hogar acudió a denunciar el delito…?» 1/2/9.
  **DENUNCIA** = BP1_20 = 1 o BP1_21 = 1; denominador = BP1_20 ∈ {1,2} (otro: fuera, contado).
- `BP1_24` «1.24 ¿El Ministerio Público o Fiscalía Estatal abrió una carpeta de investigación?» 1 Sí
  2 No 9 No sabe. **CIFRA-NEGRA** = 1 − [DENUNCIA y BP1_24 = 1] (delitos no denunciados, o
  denunciados sin carpeta o con «no sabe»: definición de cifra negra de ENVIPE). Se reporta también
  CARPETA-DADA-DENUNCIA.
- `BP1_5A_2` «1.5a ¿El (DELITO) se realizó por medio de… llamada telefónica?» 1 Sí / 0 No se
  declaró. **EXT-TELEFONICA** = BP1_5A_2 = 1 entre delitos con BPCOD = 09.
- Segmentos: sexo de la víctima (`SEXO`), `DOMINIO` U/C/R.

**Personas 18+ (TPer_Vic1, ponderador `FAC_ELE`):**
- `AP4_3_3` «4.3 En términos de delincuencia, considera que vivir en (ESTADO) es… 1 seguro 2
  inseguro 9 NS». **EDO-INSEGURO** = 2 entre {1,2}. 2024 y 2025; Sinaloa = `CVE_ENT` 25.
- (2024) `AP4_2_01..13` «4.2 De los temas que le voy a mostrar, ¿cuáles son los tres que le
  preocupan más?» (01 Pobreza … 05 Inseguridad, 04 Aumento de precios, 07 Escasez de agua …);
  PREOC-k = ítem = 1; denominador = quien no marcó `AP4_2_99` (no sabe).
- (2024) `AP4_4_xx` «4.4 En términos de delincuencia, dígame si se siente seguro(a) o inseguro(a)
  en…» calle (_03), banco (_07), cajero automático (_08), transporte público (_09), carretera (_11):
  INSEGURO = 2 entre {1,2} (3 No aplica y 9 fuera).
- (2024) `AP4_10_01` «4.10 Durante 2023, por temor a ser víctima de algún delito…, ¿dejó de… salir
  de noche?» 1 Sí 2 No (3 No aplica, 9 fuera).
- Segmentos: sexo, edad (18-29, 30-44, 45-59, 60+), `DOMINIO`.

## 2 · Universo, unidad, ponderador, diseño, IC, agregador

- Unidades: **delito** (módulo de victimización 2025) y **persona 18+** (2024, 2025); nunca se
  mezclan.
- Diseño: estrato `EST_DIS`, UPM `UPM_DIS` (texto opaco); en el marco de personas los estratos se
  prefijan con la ola, así que 2024 y 2025 se remuestrean por separado y una diferencia entre olas
  sale de réplicas independientes.
- Agregador (E.1): razón ponderada Σw·y/Σw por celda; diferencias en la misma réplica.
- IC95: bootstrap de UPM con reemplazo dentro de estrato, **2 000 réplicas**, `PCG64(42)`, bloques
  de 50; percentiles 2.5/97.5. Celda vacía → null.

## 3 · Pre-registro de falsación B-bis (fijado antes del dato)

Regla de nivel (la misma de las hijas ENIF/ENSANUT): `c` ∈ IC95 → CONFIRMA; |punto − c| ≤ 0.10 →
MATIZA; si no, ROMPE. Afirmación de otra ola que la medida: **tope MATIZA**. Componente no
medido: se nombra y el dictamen se rotula `PARCIAL`.

| afirmación | estimando que manda y regla |
|---|---|
| VIOL-007 | DEL-CIFRA-NEGRA-NAC vs 0.932 y DEL-DENUNCIA-NAC vs 0.096 (nivel); «0.8 % con resolución positiva» no se mide: `PARCIAL` |
| TRUST-026 | «superior al 93 %»: CONFIRMA si DEL-CIFRA-NEGRA-NAC IC95-INF > 0.93; ROMPE si punto ≤ 0.90; MATIZA en otro caso. Sólo la ola 2025 se mide: `PARCIAL` |
| CAPSOC-017 | (ENVIPE 2023) DEL-CIFRA-NEGRA-NAC vs 0.924 y DEL-DENUNCIA-NAC vs 0.109 (nivel; tope MATIZA) |
| VIOL-020 | DEL-EXT-TELEFONICA-NAC vs 0.85 (nivel); «5.7 millones de extorsiones» es un total, no se mide: `PARCIAL` |
| CAPSOC-018 | PREOC-INSEGURIDAD-2024-NAC vs 0.607, PREOC-AGUA vs 0.368, PREOC-PRECIOS vs 0.344 (nivel); ROMPE si PREOC-INSEGURIDAD no es la mayor de las once |
| VIOL-033 | INSEGURO-CAJERO 0.723, -TRANSPORTE 0.635, -CALLE 0.610, -CARRETERA 0.604, -BANCO 0.602 (2024-NAC, nivel); ROMPE si CAJERO no es el mayor de los cinco |
| VIOL-032 | «61.4 % dejó de permitir que menores salgan solos» → cita E.5 `RESULT-ENVIPE-PERCEPCION-2024-DEJO-PERMITIR-MENORES-SALIR-SOLOS-2024-TOTAL-TODOS` vs 0.614; «45.9 % dejó de salir de noche» → DEJO-SALIR-NOCHE-2024-NAC vs 0.459 (nivel; el peor) |
| VIOL-043 | EDO-INSEGURO-2024-SINALOA vs 0.549 y EDO-INSEGURO-2025-SINALOA vs 0.805 (nivel); ROMPE si EDO-INSEGURO-SINALOA-DIF-2025-2024 punto ≤ 0. «Tras la ruptura del Cártel de Sinaloa» (causa) no se contrasta |
| TIME-038 | regla SI-ENTONCES (alta percepción de inseguridad → evita salir de noche): no se dictamina aquí; los pisos por segmento de DEJO-SALIR-NOCHE y EDO-INSEGURO quedan como insumo; el mecanismo («cálculo racional») no es observable. **NO-CONSTRUIBLE** como veredicto en esta pieza |
| POL-009 | «1.07 % del PIB; 269.6 mil millones; 6 226 pesos por persona afectada»: el costo total de INEGI suma pérdidas, gasto preventivo y salud y divide por un PIB externo al corpus: **NO-CONSTRUIBLE** por texto |
| CAPSOC-016 | cita E.5 de `CALC-PDR1-ENVIPE2025-0001` (AP4_11_06); no se re-mide ni se dictamina aquí |

Fuera de esta pieza: VIOL-035 y VIOL-038 (ENSU por ciudad, 2025T3; «mismo hueco ENSU» del mapa):
pendientes de adquisición/tabla de apertura.

## 4 · Módulo de auditoría v2.16

- Unidad: delito (cifra negra, extorsión) o persona 18+ (percepción); nunca hogar.
- RETROSPECTIVA; nada es predicción.
- Segmentación: sexo, edad, dominio; Sinaloa contra nacional; México no es bloque.
- ¿Incentivo o psicología? No denunciar se lee primero como costo/expectativa frente a la
  institución (el motivo BP1_23 existe y no se interpreta aquí), no como rasgo cultural.
- Firewall genético: ninguna variable de ascendencia.

El primer resultado que produzca este procedimiento es el que se reporta.
