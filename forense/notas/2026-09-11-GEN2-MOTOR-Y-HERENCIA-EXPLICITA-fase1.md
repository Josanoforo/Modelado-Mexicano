# GEN2-MOTOR-Y-HERENCIA-EXPLICITA · mapa de Fase 1

Fecha real: 11 de septiembre de 2026. Base inicial inspeccionada:
`origin/main=c23dce15a917bb6fb0a4e44dabf3767e03c9ded8`. Revalidación:
`origin/main=e7a471bf1499a096abbe58dc298f02243e885135` (#708). La primera parte
de este artefacto conserva la captura anterior a la compuerta de 17; la
sección «Resolución ejecutable» documenta su integración y sustituye los
estados provisionales.

## Reproducción y perímetro ejecutable

```bash
python3 tools/corrida0.py demanda
python3 tools/corrida0.py registro
python3 tools/corrida0.py status --json
awk -F '\t' 'NR>2 && $4=="SI" {n[$6]++} END {for (k in n) print k, n[k]}' \
  data/corrida0/usos.tsv
```

La re-derivación dio 207 usos activos: 16 leídos como `GEN2` y 191 como
`LEGACY-GEN1`. `registro` informó que las vistas propuestas de corridas,
resultados y usos no difieren de las publicadas (152, 3505 y 207 filas,
respectivamente). Estos números son salida del recorrido actual, no constantes
de prueba.

El recorrido numérico efectivo del duelo es
`tools/emite_m.py:emite_celda` → `milpa/src/emisor.py:emitir_binaria` → `p`
o complemento de `milpa/tramite.yaml`. `milpa/src/motor.py` es otro objeto:
la rebanada matricial de E0 que produce veredictos de estado y no una
probabilidad del duelo. Tratar ambos como un único “motor” ocultaría qué
ejecutable materializa cada cifra.

## Captura previa: los 16 usos rotulados GEN2, sin promover su linaje

`origen numérico` queda deliberadamente `INDETERMINADO-HASTA-17`: el registro
actual comprueba que existe el RESULT y que su corrida es GEN2, pero no separa
origen nuevo/heredado/mixto ni aptitud para el uso. Una firma de contador o la
igualdad a seis decimales no resuelve ese eje.

| consumidor | parámetro/regla | origen numérico | fuente y RESULT | unidad / evento / universo / ola | uso permitido hoy | condición de activación | estado |
|---|---|---|---|---|---|---|---|
| `tramite.mordida.discrecional:paga_mordida_encig2025` | `RES-0003`, p | INDETERMINADO-HASTA-17 | `CALC-ENCIG-0001`; `RESULT-ENCIG-MOR-A-P-SOL1` | persona 18+ urbana; solicitud directa P8_3_1; ENCIG 2025 | baseline histórico/mixto; no emisión Gen2 explícita aún | P8_3_1 válido | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `tramite.mordida.discrecional:solicitud_o_entrega_mordida_encuci2020` | `RES-0005`, p de unión | INDETERMINADO-HASTA-17 | `CALC-ENCUCI-0001`; `RESULT-ENCUCI-A-P-CUALQUIERA` | persona 15+ con contacto; AP5_17=1 o AP5_18=1; ENCUCI 2020 | baseline; la transición separada sigue disponible | `contacto_funcionario_ultimos_12_meses=true`, respuesta válida | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `tramite.mordida.con_registro:paga_mordida_encig2025_presencial_r2` | `RES-0013`, proxy condicional | INDETERMINADO-HASTA-17 | `CALC-ENCIG-0001`; `RESULT-ENCIG-MOR-B-P-PRE-SD` | fila de tabla unida; P8_4 observado y canal presencial; ENCIG 2025 | consulta descriptiva, escenario o baseline; no probabilidad empírica por evento | `p8_4_observado=true`, `canal_p7_3=presencial` | RESULT sellado, rol proxy; petición de probabilidad por evento da NO_COVERAGE; aptitud pendiente |
| `tramite.mordida.con_registro:paga_mordida_encig2025_digital_r2` | `RES-0015`, proxy condicional | INDETERMINADO-HASTA-17 | `CALC-ENCIG-0001`; `RESULT-ENCIG-MOR-B-P-DIG-SD` | fila de tabla unida; P8_4 observado y canal digital/registrado; ENCIG 2025 | consulta descriptiva, escenario o baseline; no probabilidad empírica por evento | `p8_4_observado=true`, `canal_p7_3=digital_registrado` | RESULT sellado, rol proxy; petición de probabilidad por evento da NO_COVERAGE; aptitud pendiente |
| `tramite.gobierno_digital.util_sin_coercion:adopta_encig2025_luz` | `RES-0021`, p | INDETERMINADO-HASTA-17 | `CALC-ENCIG-0001`; `RESULT-ENCIG-MOR-C-P-ADOPTA` | trámite de pago de luz N_TRA=01; canal P7_3∈{4,5}; ENCIG 2025 | baseline; no extrapolar a otros trámites | contexto propio de la regla y N_TRA=01 en el estimando | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `civico.denuncia.miedo_desconfianza:denuncia_con_miedo_o_desconfianza` | `RES-0027`, p C2/U4 | INDETERMINADO-HASTA-17 | `CALC-ENVIPE-0001`; `RESULT-ENVIPE-DEN-P-C2-U4` | persona 18+ víctima; algún delito personal no denunciado, BP1_23∈{01..08}; colapso a persona; ENVIPE 2025, referencia 2024 | baseline; no comparar como si fuera la unidad delito de F5 | `victima_18_mas=true`, `delito_no_denunciado=true`, `bp1_23_en_01_08=true` | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `familia.seguro.volatilidad_ausencia_estado:recibe_remesas` | `RES-0035`, p | INDETERMINADO-HASTA-17 | `CALC-B-0001`; `RESULT-B-ENIGH-2022-P` | hogar; remesas>0; ENIGH 2022 | calibración puntual 2022; transferencia sólo por serie y corte | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `dinero.ahorro.horizonte_corto:horizonte_corto` | `RES-0046`, p | INDETERMINADO-HASTA-17 | `CALC-ENIF-0001`; `RESULT-ENIF-AHO-A-P-CORTO-SIN-P` | persona que trabaja sin seguridad social; P4_10∈{1,2}; ENIF 2024 | baseline dentro de población declarada | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `dinero.ahorro.horizonte_no_corto_con_seguridad_social:horizonte_corto` | `RES-0048`, p | INDETERMINADO-HASTA-17 | `CALC-ENIF-0001`; `RESULT-ENIF-AHO-A-P-CORTO-CON-P` | persona que trabaja con seguridad social; P4_10∈{1,2}; ENIF 2024 | baseline dentro de población declarada | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `dinero.ahorro.via_informal:formal_cualquiera` | `RES-0057`, p | INDETERMINADO-HASTA-17 | `CALC-ENIF-0001`; `RESULT-ENIF-AHO-B-P-FORMAL-P` | persona 18+; cualquier ahorro formal; ENIF 2024 | descriptivo; comparte denominador con informal, no complemento | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `dinero.ahorro.via_informal:informal_cualquiera` | `RES-0058`, p | INDETERMINADO-HASTA-17 | `CALC-ENIF-0001`; `RESULT-ENIF-AHO-B-P-INFORMAL-P` | persona 18+; cualquier ahorro informal; ENIF 2024 | descriptivo; coexiste con formal, no forzar suma uno | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `dinero.ahorro.seguro_deposito_enif2024:desconfianza_o_mal_servicio_..._conoce_...` | `RES-0059`, p condicional | INDETERMINADO-HASTA-17 | `CALC-ENIF-0001`; `RESULT-ENIF-AHO-C-P-DESCONFIA-CONOCE-P` | persona sin cuenta que conoce protección IPAB; P5_20=03 “desconfianza o mal servicio”; ENIF 2024 | sólo categoría conjunta observada | `sin_cuenta=true`, `conoce_proteccion_ipab=true` | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `dinero.ahorro.seguro_deposito_enif2024:desconfianza_o_mal_servicio_..._no_conoce_...` | `RES-0060`, p condicional | INDETERMINADO-HASTA-17 | `CALC-ENIF-0001`; `RESULT-ENIF-AHO-C-P-DESCONFIA-NOCONOCE-P` | persona sin cuenta que no conoce protección IPAB; P5_20=03; ENIF 2024 | sólo categoría conjunta observada | `sin_cuenta=true`, `conoce_proteccion_ipab=false` | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `civico.protesta.agravio_urbano_encuci2020:protesta_alguna_vez_urbano_...` | `RES-0061`, p condicional | INDETERMINADO-HASTA-17 | `CALC-ENCUCI-0001`; `RESULT-ENCUCI-B-P-URB-AGR` | persona 15+ urbana {U,C} con agravio; protesta alguna vez; ENCUCI 2020 | descriptivo con reserva de agrupación urbana | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `civico.protesta.agravio_urbano_encuci2020:protesta_alguna_vez_rural_...` | `RES-0062`, p condicional | INDETERMINADO-HASTA-17 | `CALC-ENCUCI-0001`; `RESULT-ENCUCI-B-P-RUR-AGR` | persona 15+ rural {R} con agravio; protesta alguna vez; ENCUCI 2020 | descriptivo con reserva de agrupación | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |
| `dinero.ahorro.horizonte_no_trabajadores:horizonte_corto` | `RES-0065`, p | INDETERMINADO-HASTA-17 | `CALC-ENIF-0002`; `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` | persona que no trabaja; P4_10∈{1,2}; ENIF 2024 | baseline dentro de población declarada | contexto propio de la regla | RESULT sellado, etiqueta GEN2; aptitud pendiente |

## Los 191 usos legacy, agrupados por causa

No son 191 mediciones faltantes. La unión de `demanda-resultados.tsv` y
`usos.tsv` por `resultado_id` produce cuatro grupos materiales:

| causa compartida | tipos derivados | usos | tratamiento |
|---|---|---:|---|
| Supuestos explícitos sin medición | 17 `conducta_p_asignado`, 8 `coeficiente_asignado`, 13 `asignado_probabilidad` | 38 | conservar como hipótesis/supuesto de baseline; una emisión Gen2 no los llama “medidos” |
| Medición o derivación histórica sin contrato Gen2 por uso | 26 `conducta_p_medido`, 7 complementos, 7 coeficientes ejecutables, 12 condicionales Theta, 22 momentos | 74 | agrupar por medición compartida y comprobar origen/función con el resolver 17 antes de emitir |
| Artefactos del duelo histórico | 14 R, 14 M, 28 L, 14 agregados | 70 | R es árbitro/evaluación; M y L conservan identidad histórica; no son sustitutos automáticos de parámetros operativos |
| Estructura y metadatos del motor matricial | 6 cortes π y 3 celdas D | 9 | no confundir metadato/clasificación con origen numérico |

Por familias del marco del duelo hay 30 usos legacy CIV, 15 TRA, 20 FAM y 5
DIN; los otros 121 pertenecen a parámetros, coeficientes, momentos y piezas
estructurales. Esta agrupación evita crear 191 encargos y conserva la unidad de
deuda que realmente comparte medición o función.

## Transformaciones y selección que sí entran a la salida

- Los complementos activos se derivan como `1-p(padre)` y comparten universo;
  `emitir_binaria` detecta una materialización discordante. No cuentan como
  observación independiente.
- `emitir_binaria_en_contexto` ya exige `dominio_elegible`; el modo histórico
  `emitir_binaria` sigue accesible y no hace esa comprobación.
- ENCUCI separa solicitud, entrega y unión en `emitir_transicion`; no fabrica
  una conjunta multiplicando marginales.
- `tools/emite_m.py:ola_previa_estricta` impide escoger ola futura y marca las
  entradas provenientes de R como `VERIFICACION-NO-PUNTUA`, pero
  `emite_celda` todavía usa la calibración puntual histórica. La selección
  temporal contractual aún no está cableada al recorrido vigente.
- `emite_celda` materializa también clase/tier, cita de p, cita de ola,
  ponderador y grado DD. Por ello un RESULT nuevo no acredita por sí solo toda
  la regla.

## Diagnóstico #698 incorporado sin convertirlo en evaluación

El snapshot histórico repitió ENVIPE 2025 contra seis R con unidad, recorte,
códigos y olas distintos; eso no autoriza ajustar `p`. ENIGH 2016/18/20 sí es
una serie comparable con el punto vigente 2022. TRA-M-02 ya tiene la transición
ENCUCI correcta desde #689. TRA-M-03/07 tienen serie ENCIG, pero falta que un
consumidor temporal seleccione por contrato. FAM-M-01 sigue sin una serie ENIF
armonizada. La sensibilidad publicada (−0.722844 pp en el panel conocido)
permanece descriptiva y no se usa aquí como criterio de selección.

## Adenda: benchmark web de cuatro decisiones

Se revisó
`forense/notas/BENCHMARK-WEB-CUATRO-DECISIONES-GEN2-2026-09-11.md`, cargado
por la sesión concurrente y fusionado en #708. Este acto consumió ese archivo
sin duplicarlo. Sus cuatro recomendaciones siguen siendo propuestas, no
firmas. Se aplicaron sólo los candados técnicos que corresponden al perímetro
de 18:

- r2 de ENCIG conserva sus puntos y la ruta histórica, pero ahora declara
  `rol_uso=proxy_descriptivo`; una petición explícita con
  `uso_solicitado=probabilidad_evento` devuelve `NO_COVERAGE`. Consulta
  descriptiva, escenario y baseline continúan disponibles.
- RES-0028 explicita que una persona con razones 01 y 04 tiene indicador
  padre=1 y complemento=0. “Alguna razón residual” daría 1 y es otro
  estimando; tampoco se confunde con la categoría literal 09.
- DIN y S6 no reciben intervalos oficiales ni promoción nueva. Sus puntos y
  sensibilidades permanecen en los artefactos que ya los rotulan; este acto no
  los incorpora a una salida Gen2 apta.

No se cierran NC-0085 ni NC-0107: el benchmark no firma la adopción del
complemento ni el destino científico de las tasas antiguas. Tampoco se crea
una medición/evento nuevo para r2. El cambio hace visible y ejecutable la
separación de propósito sin alterar ningún valor.

## Resolución ejecutable tras integrar 17

Se integró por objeto `d19c92d` (`[GEN2] separa linaje numerico y aptitud de
adopcion`). El emisor consume `milpa/src/linaje.py`, `usos.tsv` y
`resultados.tsv`; no replica su resolvedor. La re-derivación vigente clasifica
los 16 enlaces directos como `origen_numerico=NUEVO` y
`aptitud_uso=APTA-POR-LINAJE`. Esa aptitud no certifica por sí sola la
compatibilidad semántica del estimando.

`milpa/src/emisor.py:emitir_binaria_contrato` conserva dos identidades:

- `HISTORICO` emite el valor anterior con las dependencias heredadas visibles;
- `GEN2` exige propósito, dominio, consumidor activo, RESULT sellado, origen
  apto e identidad numérica; ante cualquier ausencia devuelve `NO_COVERAGE`;
- `transferencia` recibe la elección de `tools/baseline_temporal.py`, vuelve a
  leer el RESULT y rechaza un valor con rol `ARBITRO`;
- los proxies r2 sólo admiten `DESCRIPTIVO`; una probabilidad por evento falla
  cerrada;
- los complementos usan el RESULT del padre. El complemento ENCUCI ya
  adoptado emite sin sumar una medición; la propuesta ENVIPE devuelve
  `NO_COVERAGE` mientras no exista firma de adopción.

El snapshot nuevo es
`forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_0.json`. Registra hashes
del emisor, contrato de linaje y selector, además de unidad, evento, universo,
ola, activación, uso, RESULT completo y dependencias estructurales por salida.
Sus conteos se derivan en cada ejecución:

| alcance | antes | después en modo GEN2 explícito |
|---|---:|---:|
| registro activo global | 207: 16 directos GEN2, 191 legacy | 16 directos evaluados, 16 `EMITE` |
| emisor `milpa/tramite.yaml` | 66: 16 directos GEN2, 50 legacy | CIV 3, TRA 5, FAM 1, DIN 7 |

La demostración contractual de transferencia ENIGH-NS para objetivo 2022 y
corte `2021-12-31` elige `RESULT-B-ENIGH-2020-P`; queda rotulada
`OPERATIVO-NO-ARBITRO` y `NO-EVALUACION-INDEPENDIENTE`. No usa la ola 2022,
una ola posterior, un estimando parecido ni el valor del árbitro.

## Aceptación de la adenda

| decisión o límite acreditado | RESULT/fuente | consumidor | uso efectivo | prueba | cierre/residual |
|---|---|---|---|---|---|
| S6: IC por localidad no es diseño oficial | `RESULT-S6-*`; #702 y `S6-L16-spec-v1_5.md` | `salud.atencion.grave_ennvih2002` | puntos/asociaciones descriptivas; `IC-SENSIBILIDAD-LOCALIDAD-NO-DISENO-OFICIAL` | `test_s6_traslada_limite_sin_reescribir_veredictos` | Enmienda trasladada; FP-372 y NC-0156 siguen abiertas; R4.4 permanece MEDIA |
| Fintech D10 | `CALC-ENIF-FINTECH-0001--5b92cee28946` | contexto R1.6 en `milpa/procedencia.yaml` | `DESCRIPTIVO-NO-CALIBRA`; 2021/2024 lado a lado, 2018 no estimable | `test_fintech_d10_incorpora_serie_sin_calibrar_r16` | D10 consumida; NC-0122 conserva el límite estructural |
| Identidad ENCIG2023 | payload ya aplicado por #700 | entradas pertinentes de NC-0106 | etiqueta documental | `test_identidad_encig_ya_deriva_del_payload` | Ya corregida; no se repitió ni cambió ola/medición |
| Tandas | #700 | escenario académico | antecedente, no parámetro | pruebas de ausencia/calibración existentes | D18 comercial diferida; no se infiere adopción |
| DIN | `DIN-M-01` y benchmark #708 | consumidores DIN | punto descriptivo; sensibilidades separadas | snapshot explicita uso/linaje | FP-371 sigue sin firma inferencial |
| Complemento ENVIPE | padre `RESULT-ENVIPE-DEN-P-C2-U4` | `denuncia_por_otra_razon` | dependencia a nivel persona, no observación nueva | `test_res0028_persona_con_razones_mixtas_no_es_alguna_otra` y caso 05 GEN2 | `NO_COVERAGE` hasta firma; NC-0085 no cierra |
| Corrupción r2 | `RESULT-ENCIG-MOR-B-P-{PRE,DIG}-SD` | dos salidas r2 | proxy descriptivo dentro del grupo observado | `test_encig_r2_es_proxy_y_no_probabilidad_por_evento` | Probabilidad por evento rechazada; NC-0107 y adopción de tasas antiguas no cierran |

No se firmaron las opciones DIN/S6, la adopción concreta del complemento ni
una nueva regla de corrupción. No se promovió el escenario de tandas. Las
únicas decisiones nuevas del acto son de interfaz y trazabilidad: fallar
cerrado, preservar identidad y exponer herencia.

## Baseline preservado

El baseline de F5 queda intacto:

| artefacto | sha256 |
|---|---|
| `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json` | `b53ac6d51d1b50ce929fdf1b3e14b124c11db39fb216a15d7073a287ed3f065c` |
| `data/corrida0/CALC-TRIADA-0002/resultados.json` | `e2d0adc2a9fb9722d50a9479916129b3524cb87ce9021359ebfe755ec0e9e22a` |
| `forense/prereg-duelo-v2/F5-completa-resultado-v1_0.json` | `e1ec8765f769f76c7f649958f46b72b34fcef786bcc113f5c3cbc997c4ed0079` |

Los diez casos obligatorios viven en
`tests/test_motor_gen2_explicito.py`; sus conteos de cobertura se comparan con
la vista recién derivada, no con el literal 16. El snapshot de TRIADA-0002 y
los resultados F5 no fueron modificados.
