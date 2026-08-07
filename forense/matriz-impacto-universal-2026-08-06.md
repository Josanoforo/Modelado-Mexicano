# Matriz universal de impacto de evidencia

Fecha de corte: 2026-08-06. Capa de orientación reusable; no modifica sellos,
no adjudica resultados y no sustituye las especificaciones de cada objeto.

## Convención de estados

Estados permitidos: `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO`,
`INDEXADO-NO-DESCARGADO`, `DESCARGADO-NO-ABIERTO`, `ABIERTO-SIN-MAPEO`,
`MAPEADO-NO-SATISFACE`, `NO-ACCESIBLE`, `MECANISMO-NO-EJECUTADO`,
`NO-REPRODUCIBLE-CON-ARTEFACTOS-ACTUALES`, `SATISFACE-UMBRAL`,
`REQUIERE-DECISION-DE-MESA`.

Todo negativo se lee junto con cinco campos: universo, mecanismo, criterios,
fecha y condición faltante. Una celda vacía no significa ausencia.

## Pasada 1 — resultados sellados

| objeto | demanda/evidencia original | evidencia nueva positiva o negativa delimitada | premisa de ausencia | impacto | profunda | estado vigente |
|---|---|---|---|---|---|---|
| R1.1-D | Productor temporal, voluntario, >=3 ciclos, comparado con ahorro formal; revisión documental | Cuatro CSV AGROASEMEX abiertos el 5-ago: ninguno llega a productor por ciclo ni separa voluntario/atado a crédito | Sí, superada como disponibilidad física; no como condición faltante | Corrige fundamento, no demuestra umbral | Sí, cerrada en REVALIDA-1B | `MAPEADO-NO-SATISFACE` |
| R1.2-E | ENIF 2024; uso formal estable 42.98%, IC95% [39.88,46.08], umbral <15% | ABRIR-4 abrió ENSAFI/ENFIH, pero no aporta una medición comparable que pueda acercar el resultado a 15% | No | Ninguno material localizado | No | `MAPEADO-NO-SATISFACE` — no-satisfacción decisiva del falsador según su ficha |
| R1.3-E, piernas 1-2 | ENIF 2024, `P5_4_8`; penetración 3.86%, brecha 2.98pp | Ninguna fuente posterior cambia esos dos estimandos | No | Ninguno | No | `MAPEADO-NO-SATISFACE` — activa la rama E preespecificada |
| R1.3-E, pierna 3 | Canal de alta/referidos por fintech | CNBV/COFECE abiertos el 5-ago: no traen canal de adquisición desagregado | Sí, reexaminada | Mantiene el alcance acotado; no completa el falsador | Sí | `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO` — universo CNBV+COFECE; apertura directa; 5-ago; falta canal por fintech |
| R3.1-B | ENCIG 2023, seis cómputos ALTA/BAJA; mecanismo ejecutado históricamente | No apareció fuente nueva; las notas permiten reconstrucción, pero falta el ejecutable preservado | No | No hay reproducción independiente de un comando conservado | Sí | `NO-REPRODUCIBLE-CON-ARTEFACTOS-ACTUALES` — reconstrucción del pipeline pendiente |
| R3.2-B | ENCIG 2023, seis cómputos presencial/digital; mecanismo ejecutado históricamente | No apareció fuente nueva; las notas permiten reconstrucción, pero falta el ejecutable preservado | No | No hay reproducción independiente de un comando conservado | Sí | `NO-REPRODUCIBLE-CON-ARTEFACTOS-ACTUALES` — reconstrucción del pipeline pendiente |
| R4.1-D | ENSANUT/ENIGH transversales; falta evento local pre/post y trato enlazado | SESTAD abierto: trato agregado; SINERHIAS y choque INSABI son candidatos no adjudicados | Sí | Puede cambiar ruta e interpretación | Sí | `REQUIERE-DECISION-DE-MESA` sobre lectura literal local vs ecológica |
| R4.2-D | ENSANUT: no existe permiso laboral x posposición | Aperturas posteriores no localizaron el cruce exacto | Sí, delimitada al instrumento | Ninguno | Sí, cerrada | `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO` — cuestionarios Hogar+Adultos y catálogos; grep dirigido; 4-ago; falta permiso laboral específico |
| R4.3-A-D | ENSANUT `A0313/A0314`; autorreporte y duración insuficiente | Cero Desabasto aporta desabasto independiente, no adherencia individual por surtimiento | Sí | No completa el falsador | Sí | `MAPEADO-NO-SATISFACE` |
| R4.3-B-D | ENSANUT; sin cuidadora identificada y con corresidencia confundida | ENASIC aporta cuidado/obligación, no cuidadora x adherencia del paciente | Sí | No completa el falsador | Sí | `MAPEADO-NO-SATISFACE` |
| R5.1-A | ENIGH 2012-2022 transversal repetida | ENASEM 2018/2021: variables, llave y reactivos documentalmente mapeados; tratamiento 2018 ambiguo y bloqueo principal. ENASEM 2024: payload y FD descargados/verificados, contenido no abierto | Sí, panel omitido | Puede cambiar magnitud e interpretación causal | Sí | `MECANISMO-NO-EJECUTADO` — nueva especificación/corrida requerida |
| R5.2-A | ENUT 2024; 23.98%, IC95% [14.39,33.57], umbral 20% | No hay regla punto/IC; `run_r5_2.py` no está en el árbol | No | Puede cambiar A por no concluyente | Sí | `REQUIERE-DECISION-DE-MESA` |
| R7.2-D | ENVIPE 2025; cobertura solo en robo de vehículo | Ocho olas comparables y script existente confirman el hueco estructural | No | Refuerza D y el alcance estrecho | Sí, cerrada | `MAPEADO-NO-SATISFACE` |
| R9.1-D | ENSANUT Utilizadores; distancia/consulta | Hogar sí observa no-consulta, corrigiendo “excluida”; sigue sin preferencia conocimiento propio ni enlace CLUES | Sí, parcialmente superada | Exige reespecificar método, no demuestra umbral | Sí | `REQUIERE-DECISION-DE-MESA` sobre nueva ruta Hogar+acceso |
| R9.2-D | ENSANUT+DGIS; falta auditor independiente de campaña | Cero Desabasto es independiente del prestador e incluye reportes de vacunas; solo se abrió el portal y se confirmó la sección de datos abiertos | Sí, superada como clase de fuente | Puede habilitar medición y cambiar letra; faltan formato, granularidad, campaña, periodo y denominador | Sí | `INDEXADO-NO-DESCARGADO` |

## Pasada 1 — reglas fuertes abiertas o todavía no selladas

El universo son las reglas marcadas “Sí” en `canon/modelo-decision-v4_0.md`
que no aparecen en el registro sellado anterior. La pasada fue cruce de
`cruce-catalogo-fichas-v2_0`, ABRIR-4, VERIF-3, EXPLORA-2 y BARRIDO-1 al
6-ago-2026; no se abrió microdato nuevo.

| objetos | demanda resumida | evidencia nueva | impacto | profunda | estado |
|---|---|---|---|---|---|
| R1.4 | Prima de marca D/E vs A/B con compra real | EMOVI declara explícitamente no medir consumo/marca; Kantar/Nielsen continúan restringidos | Bajo salvo acceso comercial | No | `NO-ACCESIBLE` — universo comercial identificado; falta microdato de compra comparable |
| R2.1, R2.2 | Disenso ascendente; liderazgo x desempeño | ECCO abierto y mapeado: percepción agregada, sin frecuencia conductual ni tipología autoritario/benévolo | Confirma que ECCO no satisface | No | `MAPEADO-NO-SATISFACE` |
| R3.4 | CoDi vs SPEI y mecanismo de riesgo fiscal | Banxico abierto: series y cuenta validada primaria; no motivo individual ni separación de fricción | Cambia magnitudes primarias, no identifica mecanismo | Sí | `MAPEADO-NO-SATISFACE` para B/C; A parcialmente construible |
| R7.1 | Participación por peso del acto | INE municipal federal abierto; no comparación local concurrente exacta | Puede construir parte ecológica | No | `MAPEADO-NO-SATISFACE` |
| R7.3 | Transferencia y autonomía electoral | PUB abierto: entidad x trimestre, no nominal | Elimina la ruta nominal | No | `MAPEADO-NO-SATISFACE` |
| R7.4, R7.5 | Protesta/autodefensa georreferenciada y actores | ACLED gratuito abierto: mes x país, no evento/actor/geo | Ruta gratuita no satisface; ACLED detallado requiere registro | No | `NO-ACCESIBLE` para detalle; `MAPEADO-NO-SATISFACE` para payload abierto |
| R8.1 | Contribución con monitoreo/sanción | Contraloría Social abierta: nacional x año, sin comité/sanción | Elimina ruta del CSV agregado | No | `MAPEADO-NO-SATISFACE` |
| R8.2 | Tanda por confianza personal | Candidata MINES resultó sitio de apuestas; ninguna candidata directa abierta | Premisa de candidato superada negativamente | No | `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO` — barrido público+apertura candidata, 5-ago; falta tanda con relación personal y participación |
| R8.3 | Puente personal y confianza generalizada | LAPOP/Latinobarómetro tienen cuestionarios abiertos, pero la batería pertinente no está mapeada a este umbral | Puede aportar reactivo, no desenlace causal | Sí | `ABIERTO-SIN-MAPEO` |
| R10.1 | Rechazo indirecto/face | Sin candidata posterior con conducta observada | Ninguno localizado | No | `MECANISMO-NO-EJECUTADO` — no hay barrido dirigido documentado suficiente |
| R10.2 | Feedback público y capital social | ECCO no trae frecuencia/resultado; puertas empresariales siguen propietarias | No satisface | No | `MAPEADO-NO-SATISFACE` |
| R10.3 | Ver-oír-callar | ENVIPE mapeó desenlaces condicionados; restricciones éticas bloquean rutas de testigos protegidos | Puede sostener asociación, no experimento | Sí | `REQUIERE-DECISION-DE-MESA` sobre uso permitido y estimando |

## Pasada 1 — reglas no incluidas todavía en Hito D

| objetos | demanda/evidencia original | evidencia nueva | impacto | profunda | estado |
|---|---|---|---|---|---|
| R1.5-R1.7 | Seguro de depósito; techo de sobreprecio; daño BNPL | ENFIH/ENSAFI profundizan finanzas, pero ABRIR-4 no encontró actitud de riesgo limpia ni desenlace BNPL | Candidatas parciales, ningún umbral completo | No | `ABIERTO-SIN-MAPEO` |
| R2.3-R2.4 | Prestaciones vs salario; rotación joven | ENOE/ENFIH/ENUT disponibles; no existe especificación congelada de desenlace | Puede habilitar diseño transversal | No | `MECANISMO-NO-EJECUTADO` |
| R3.3 | Norma inútil/sanción improbable | ENCIG disponible; sin mapeo dirigido vigente | Potencial alto para trámite | No | `DESCARGADO-NO-ABIERTO` respecto de esta demanda |
| R4.4-R4.5 | Público ante gravedad; sellos x precio | ENSANUT/ENIGH disponibles; no mapeo conjunto exacto | Potencial medio | No | `DESCARGADO-NO-ABIERTO` respecto de estas demandas |
| R5.3-R5.4 | Unión libre; cortejo/apps | ENADID/ENIGH/ENDUTIH disponibles; ningún desenlace de apps mapeado | Potencial medio | No | `ABIERTO-SIN-MAPEO` a nivel temático |
| R6.1-R6.4 | Formalidad temporal/compromisos | ENOE/ENUT disponibles; sin reactivos de promesa/incumplimiento mapeados | Bajo-medio | No | `MECANISMO-NO-EJECUTADO` |
| R7.6-R7.9 | Monitoreo, broker, entitlement, atribución | PUB agregado no satisface persona; paneles electorales restringidos/no accesibles | Puede alterar reglas cívicas si se obtiene panel | Sí para panel | `NO-ACCESIBLE` o `MAPEADO-NO-SATISFACE` según ruta |
| R8.4 | Sanción social rural/urbana | Contraloría agregada no satisface; usos y costumbres fuera de perímetro | Bajo hasta nueva fuente | No | `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO` — barrido público 5-ago; falta contribución individual y sanción visible |
| R9.3-R9.4 | Credibilidad por allegado; escuela privada anticaída | ENBIARE/ENFIH/ENIGH contienen redes/activos, pero no mapeo conjunto al desenlace | Potencial medio | No | `ABIERTO-SIN-MAPEO` |
| R10.4 | Directividad por región/edad | Encuestas de opinión disponibles; sin reactivo conductual directo | Bajo | No | `MECANISMO-NO-EJECUTADO` |

## Pasada 1 — 15 coeficientes

| coeficiente(s) | evidencia original | evidencia posterior | impacto | profunda | estado |
|---|---|---|---|---|---|
| G1·confianza_institucional, G1·radio_confianza, G3·familismo_apoyo | beta marginal ya corrida | Ninguna llave causal nueva | Mantiene asociación, no identificación | No | `SATISFACE-UMBRAL` solo como asociación rotulada |
| G2/G3·aversion_riesgo | Búsqueda cerrada en ENIF por ADR-52 | ABRIR-4 no encontró candidato nuevo en ENBIARE; ENSAFI `IMPULSIVID` conserva texto no verificable y no satisface | ADR-52 no quedó superado | No | `MAPEADO-NO-SATISFACE` — descarte resuelto para las candidatas de ABRIR-4 |
| G2/G4·sens_estatus | Búsqueda cerrada en cinco instrumentos por ADR-54 | ABRIR-4 no encontró candidato nuevo en ENBIARE; ENSAFI no aporta texto verificable ni satisface | ADR-54 no quedó superado | No | `MAPEADO-NO-SATISFACE` — descarte resuelto para las candidatas de ABRIR-4 |
| G3·horizonte_temporal | ENNViH/MxFLS, llave panel y fase descriptiva | ENSAFI `ORIEN_FUT` sin texto; ENBIARE con futuro documentado | Más candidatos, ninguno sustituye automáticamente el panel | Sí | `MECANISMO-NO-EJECUTADO` — diseño intra-persona pendiente |
| G4·exposicion_violencia, G4·confianza_justicia | ENVIPE, condicionales parciales; `BP1_23` limitado | ENDIREH actual no fue consumida; ninguna llave causal nueva | No cambia hoy | No | `MAPEADO-NO-SATISFACE` para identificación; asociación disponible |
| G4·horizonte_temporal | Reactivo y desenlace viven en instrumentos distintos | ENSAFI/ENBIARE agregan reactivo, no desenlace G4 coobservado | Sigue sin par común | No | `ABIERTO-SIN-MAPEO` |
| G5·familismo_apoyo | Único candidato ENIF circular | ENFIH y ENBIARE aportan apoyo/redes; ENASIC aporta cuidado, sin desenlace G5 adjudicado | Puede abrir par no circular | Sí | `ABIERTO-SIN-MAPEO` |
| G5·familismo_obligacion | ENUT proxy conductual, sin magnitud | ENASIC `P7_12_7` satisface texto de obligación familiar; ENBIARE aporta redes | Supera premisa de solo proxy ENUT; falta desenlace coobservado y forma | Sí | `REQUIERE-DECISION-DE-MESA` |
| G5·radio_confianza | Reactivo ENCUCI y desenlace ENIF separados | ENASIC trae desconfianza en cuidados, dominio estrecho | No crea conjunta válida | No | `MAPEADO-NO-SATISFACE` |
| G6·deferencia | Latinobarómetro `P4NOIJ`, proxy y sin diseño publicado | Ningún candidato posterior directo | Sin cambio | No | `NO-ACCESIBLE` para microdato/diseño; proxy abierto no satisface |

## Pasada 1 — 14 condicionales

| condicionales | evidencia actual | nueva evidencia | impacto | profunda | estado |
|---|---|---|---|---|---|
| confianza institucional: salud, educación, financiera, seguridad-FFAA, justicia-policía, electoral-partidos | Nueve condicionales totales `MEDIDO·PARCIAL(x)` incluyen los seis componentes | Ninguna fuente nueva mejora conjuntamente los seis ejes | Números utilizables con truncamiento declarado | No | `SATISFACE-UMBRAL` solo para la malla parcial publicada |
| radio_confianza | ENCUCI `AP5_1_1/2/3`, `MEDIDO·PARCIAL` | ENASIC aporta desconfianza solo en cuidados | No sustituye constructo general | No | `MAPEADO-NO-SATISFACE` para ENASIC; medición ENCUCI vigente |
| familismo_apoyo | ENIF `P9_9_1..6`, `MEDIDO·PARCIAL` | ENFIH/ENBIARE abren rutas no adjudicadas | Puede mejorar validez externa | Sí | `ABIERTO-SIN-MAPEO` para candidatas; medición original vigente |
| exposicion_violencia | ENVIPE `AP7_3_10..14`, `MEDIDO·PARCIAL` | ENDIREH no consumida por esta medición | Sin impacto probado | No | `SATISFACE-UMBRAL` para malla parcial |
| horizonte_temporal | ENIF `P4_10`, proxy C3 | ENSAFI/ENBIARE aportan orientación futura; solo ENBIARE tiene texto | Puede sustituir proxy si comparte condicionantes adecuados | Sí | `ABIERTO-SIN-MAPEO` |
| familismo_obligacion | ENUT proxy pendiente | ENASIC `P7_12_7` mapea obligación explícita | Puede cambiar forma y procedencia | Sí | `REQUIERE-DECISION-DE-MESA` |
| deferencia | Latinobarómetro proxy | Sin nueva candidata directa | Sin cambio | No | `NO-ACCESIBLE` para microdato completo |
| aversion_riesgo | cierre ADR-52 | ABRIR-4 no encontró candidato nuevo en ENBIARE; ENSAFI `IMPULSIVID` conserva texto no verificable y no satisface | ADR-52 permanece vigente | No | `MAPEADO-NO-SATISFACE` — descarte resuelto |
| sens_estatus | cierre ADR-54 | ABRIR-4 no encontró candidato nuevo en ENBIARE; ENSAFI no aporta texto verificable ni satisface | ADR-54 permanece vigente | No | `MAPEADO-NO-SATISFACE` — descarte resuelto |

## Cola priorizada de revisiones profundas

1. R5.1 / ENASEM: pre-registro longitudinal limpio.
2. R5.2: decisión punto-versus-IC y reconstrucción de `run_r5_2.py`.
3. R9.2 / Cero Desabasto: abrir estructura, granularidad y campaña.
4. R4.1: decisión literal-local versus ecológica; luego SINERHIAS/INSABI.
5. R3.2 y R3.1: reconstrucción reproducible compartida.
6. `familismo_obligacion`: adjudicar ENASIC `P7_12_7` frente al proxy ENUT.
7. `aversion_riesgo`: descarte resuelto; ABRIR-4 no encontró candidato nuevo y ADR-52 permanece vigente.
8. `sens_estatus`: descarte resuelto; ABRIR-4 no encontró candidato nuevo y ADR-54 permanece vigente.
9. R9.1 método: reespecificar Hogar+acceso y verificar llave CLUES.
10. R3.4: separar reproducción transaccional de identificación del mecanismo.

## Cola mínima de descargas/aperturas

| prioridad | objeto | acción mínima | por qué es necesaria | estado previo |
|---|---|---|---|---|
| 1 | R5.1 | Tratar primero ENASEM 2018; abrir microdato solo después de pre-registro limpio | Resolver el tratamiento 2018, bloqueo principal; 2018/2021 ya tienen variables, llave y reactivos documentalmente mapeados | `DESCARGADO-NO-ABIERTO` para la medición; en 2024 solo payload y FD descargados/verificados |
| 2 | R9.2 | Descargar exportación/diccionario de Cero Desabasto ya indexado; no medir | Verificar formato, granularidad, campaña, periodo y denominador | `INDEXADO-NO-DESCARGADO`; solo portal y sección de datos abiertos confirmados |
| 3 | R4.1 | Abrir series históricas SINERHIAS por CLUES si son descargables | Confirmar evento local y periodicidad | `INDEXADO-NO-DESCARGADO` / acceso no verificado |
| 4 | R9.1 | Abrir diccionario de llaves ENSANUT/CLUES, no microdato primero | Saber si el enlace existe | `ABIERTO-SIN-MAPEO` |
| 5 | deferencia | Obtener microdato Latinobarómetro solo con autorización/licencia aplicable | El cuestionario solo no permite condicional | `NO-ACCESIBLE` sin registro/licencia |

No se recomienda descargar para R1.1, R4.3-A/B, R4.2 o R7.2: la condición
faltante no se resuelve acumulando más archivos de las mismas fuentes.

## Paquetes vigentes para próximas mediciones

### P-R5.1-ENASEM

Fuentes: ENASEM 2018/2021, con variables, llave y reactivos documentalmente
mapeados. Reactivos: tratamiento `K79/K82` con reserva 2018; llave
`UNHHIDNP`; corresidencia `TRH2A/TRH2B/TRH5`; ayuda familiar `G17/G18`.
ENASEM 2024 tiene payload y FD descargados/verificados, pero su contenido no
se ha abierto; no se le atribuyen esos reactivos ni llaves hasta verificar su
descriptor. Diseño: panel individual. Ruta descartada: tratar “otra
institución” 2018 como Pensión sin adjudicación. El tratamiento 2018 es el
bloqueo principal. Pendientes: estimando, edad-elegibilidad,
mortalidad/attrition y regla de comparabilidad.

### P-R9.2-CERO-DESABASTO

Fuentes: ENSANUT 2024 + Cero Desabasto, independiente del prestador y con
reportes de vacunas. De Cero Desabasto solo se abrió el portal y se confirmó
la sección de datos abiertos; su estado es `INDEXADO-NO-DESCARGADO`.
Reactivos ENSANUT: cartilla/vacuna `M0503/D0501/A0901`; desenlace de
cobertura. Diseño posible: entidad×periodo ecológico, solo si la fuente
externa ofrece campaña y alcance. Ruta descartada: DGIS como auditor
independiente. Pendientes: formato, granularidad, campaña específica, periodo
y denominador.

### P-R4.1-ACCESO

Fuentes: ENSANUT, SESTAD, SINERHIAS/CLUES. Reactivos: uso de farmacia y
trato; desenlace: cambio de uso. Diseños posibles: evento local o corte
ecológico INSABI. Ruta descartada: SESTAD agregado como sustituto de panel.
Pendiente normativo: qué interpretación del umbral autoriza la mesa.

### P-COND-FAMILISMO-OBLIGACION

Fuentes: ENUT 2019/2024 y ENASIC 2022. Reactivos: ENUT `6.11/6.11a` como
carga conductual, condicionado a `FILTRO_S6_11=1` (aproximadamente 12.08% de
informantes en 2024); ENASIC `P7_12_7` como deber explícito. Desenlace
candidato: cuidado/carga coobservada, aún no adjudicado para coeficiente G5.
Ruta descartada: equiparar corresidencia con obligación. La decisión debe
resolver simultáneamente actitud frente a conducta, población general frente
a población con necesidad de cuidado, y forma, dirección y condicionantes.

### P-REPRO-R3

Fuente: ENCIG 2023 `sec_7/sec_8`. Variables: `P7_3`, `P8_4`, `N_TRA`,
`NT_TIPO`, `FAC_TRA`, `FAC_P18`, llaves personales. Debe preservar dos
lecturas de NA, tres ponderaciones y exclusión documentada de llaves
divergentes. No es nueva medición: es reconstrucción de reproducibilidad de
R3.1/R3.2 antes de cualquier addendum.

## ENDIREH

La colisión de ids permanece separada. Ningún objeto profundizado aquí cita
el id histórico ni `_redescarga` como insumo de medición. No altera la cola.
