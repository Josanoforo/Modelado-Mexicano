# ASTRA5-U0 · MAPA-DOMINIOS · nota de cierre (24/sep/2026)

**Contadores movidos por este acto: ninguno.** El mapa no mide y no toca `celdas_validadas` (219 → 219, Δ0, `tools/cierre_acto.py` sobre `7f9629de`, con `origin/main` fusionado).

- ADR `ADR-260924-ASTRA5-U0-MAPA-DOMINIOS-63db-01` (raíz D-24: `63db` del 0-bis `63dbb17d`).
- Encargo `forense/encargos/2026-09-23-ASTRA5-U0-MAPA-DOMINIOS.md` (sello de cuerpo `372c7af8c7ae47d43c142fbb101c49e684e71547ad60760b1cf81988b43f687c`) y `…-ADENDA-1.md` (asignación final de mesa, sello `e9fbe981e596c64e7aa0cbf8fcf384ac837af3eab73a3a67eef4c82d308b2e96`).
- PR #1079, rama `codex/astra5-mapa-dominios-1`. Ejecutaron Codex (hasta `80e5af58`, 23/sep, corte por `usage_limit_exceeded`) y Claude Opus 5.5 como supervisor de ejecutores Sonnet (24/sep).

## 1 · Qué se entrega

| producto | ruta | cifra (derivada por comando) |
|---|---|---|
| mapa canónico, una fila por afirmación | `canon/mapa-dominios-v1_0.tsv` | 1 396 afirmaciones de los 37 archivos: 208 MEDIBLE-EN-CORPUS · 768 MEDIBLE-CON-ADQUISICIÓN · 420 NO-MEDIBLE-POR-DISEÑO; cero pendientes |
| cobertura del universo | `forense/analisis/dominios/cobertura-unidades-v1_0.tsv` | 1 439 líneas, 1 018 unidades: G 474, P 112, T 111 y todas las fichas de lectura cubiertas por fila, contrato o razón cerrada |
| proyección para ASTRA4-U1 | `proyeccion-cobertura-v1_0.tsv`, `proyeccion-dominios-v1_0.tsv` | medibilidad, autorización de apertura y RESULT en ejes separados; 28 dominios; 10 EN-MEDICIÓN, 1 386 SIN-RESULT, 0 MEDIDO |
| tabla report→dominio (U1 y FRONT) | `report-a-dominio-afirmaciones-v1_0.tsv` | report × dominio de la afirmación, no del report |
| hoja de adquisición derivada | `hoja-adquisicion-derivada-v1_0.tsv` | REUTILIZAR 208 · ADQUIRIR 163 · DOCUMENTACIÓN-SOLAMENTE 605 · DESCARTAR-CON-RAZÓN 420; 130 con existencia `NO-ACCESIBLE-DESDE-SANDBOX` |
| lotes auditados | `forense/analisis/dominios/lotes/` | 37 lotes, 1 304 filas con id + 98 ENLACE a contratos Codex; búsquedas crudas por lote y correcciones del supervisor (`busquedas/*.parches.log`) |
| segunda pasada documental | `lotes/segunda-pasada-v1_0.tsv`, `lotes/segunda/tanda-*.{log,parches.jsonl}` | 482 cambios registrados sobre 328 filas; 249 PENDIENTE cerradas; 22 CON-ADQUISICIÓN pasaron a EN-CORPUS al localizar el reactivo en el corpus |
| fusiones entre archivos | `fusiones-v1_0.tsv` | 10 (misma afirmación y componente en dos reports; la canónica conserva las procedencias) |
| correspondencia afirmación→RESULT | `resultado-por-afirmacion-v1_0.tsv` | 10 EN-MEDICIÓN y 2 con RESULT de otro componente |
| receta de acceso | `receta-acceso-fuentes-2026-09-24.md` | rutas medidas que funcionan y las que no |
| filas no accesibles | `no-accesible-desde-sandbox-v1_0.tsv` | 131 (130 en el mapa; `TIME-033` fusionada en `VIOL-023`) |

`ensambla_mapa.py --verifica` reproduce byte a byte las seis salidas; `tests/test_astra5_dominios.py`: 27 pruebas, 0 fallos.

## 2 · Lectura breve del mapa

- **Qué tan medible es el corpus.** Una de cada siete afirmaciones de los reports se puede medir ya con dato y documento que están en `main` (208 de 1 396); algo más de la mitad requiere adquirir una pieza concreta (768, casi todas documentos: artículos, informes, series administrativas), y casi un tercio no es observable con el diseño de los instrumentos recorridos (420: causalidad sin diseño identificador, mecanismos, recomendaciones, proyecciones y constructos que nadie pregunta).
- **Dónde está el dato.** Dinero (40), política y confianza (20 cada uno), tecnología (17), trabajo y salud (13) concentran lo medible en corpus: ENIF, ENCUCI, ENCIG, ENVIPE, ENDUTIH, ENOE ≤2025, ENSANUT 2024, ENADID 2023, Censo 2020, LAPOP y la serie Banxico de morosidad. Genética, genómica, humor, conocimiento, emociones morales e interacción no tienen ninguna afirmación medible en corpus: su evidencia es documental o extranjera.
- **Lo medido de verdad.** Diez contratos tienen un RESULT GEN2 sellado que mide exactamente su componente (ENOE 2024T3 ×3, ENDUTIH 2024 ×4, ENDIREH 2021 pareja física, LAPOP 2023 b18/b21 y la serie LAPOP b21 2004–2023). Están EN-MEDICIÓN, no MEDIDO, porque ninguno tiene fila en la vista de resultados (E.7): **DIFERIDO-A: GEN2-TUBERIA-VISTA-NORMALIZADA-2** — pasan a MEDIDO solos cuando ese acto destrabe el `[deriva]` del canal de derivados (caído por GH001 desde el 23/sep); ninguna fila del mapa se edita para eso, la proyección lo lee de la vista.
- **Cifras que las fuentes corrigen.** La serie LAPOP b21 sellada rompe el «24% → 9.5%» de confianza en partidos (máximo 14.6%, no existe ola 2010). Banxico muestra el IMOR de tarjetas bajando entre oct-2024 y oct-2025 cuando el forense de crédito fácil narra alza. Randstad México pone el salario por encima del balance vida-trabajo, al revés que el report de trabajo. El 55% de la fuerza laboral menor de 25 años es medible con ENOE pero demográficamente inverosímil. ENADIS 2017 da 16.0%, no «1 de cada 10», de educación superior para tonos de piel oscuros.
- **Firewall genético.** Ninguna fila declara medible una segmentación por ascendencia; la frecuencia alélica por grupo quedó rotulada como genética de poblaciones, y el canal individual ADH1B/CYP2A6 se separó del grupal.

## 3 · Cómo se hizo (EJECUTADO / LEÍDO / REPORTADO)

- `[LEÍDO]` Encargo archivado, protocolo de continuación y estado de Codex (102 contratos, 719 fichas, 474 grupos G).
- `[EJECUTADO]` El scratchpad de la sesión Claude anterior se había borrado con 15 ejecutores a medio lote: el aparato (instrucciones, paquetes, validador, importador, caché de texto de 349 PDF registrados) se reconstruyó re-ejecutando los comandos del transcript, y las búsquedas crudas de los ejecutores interrumpidos se entregaron a sus relevos (`lotes/busquedas/*.log` las citan como «ejecutor previo»).
- `[EJECUTADO]` 37 lotes, uno por archivo del censo, redactados por Sonnet con instrucciones congeladas y auditados por el supervisor: validación mecánica, revisión de toda fila NO-MEDIBLE y EN-CORPUS, correcciones registradas y devoluciones con instrucción. El supervisor encontró y corrigió de forma recurrente: encuestas del corpus dictaminadas como adquisición (ENOE, ENUT, ENIGH, ENVIPE, ENIF, ENDUTIH), EN-CORPUS sin documento `id|sha` o apoyados en la copia R16 de CNBV que sólo expone dic-2021, y NO-MEDIBLE sin búsqueda.
- `[EJECUTADO]` Segunda pasada documental en 17 tandas; las filas que el ejecutor dejó PENDIENTE con existencia no comprobada se cerraron por la regla 4 (MEDIBLE-CON-ADQUISICIÓN con faltante), aplicada y registrada por el supervisor.
- `[EJECUTADO]` Reservas: ninguna cifra ENOE 2026T1 entró a campos nuevos (mérito cubre L22 por ENLACE a ENOE-001; `tiempo-007` salió del mapa); ENVIPE 2026 y ENCO sin consulta (una cifra probablemente ENCO quedó RESERVADA sin verificarse). Se retiró de `CONOC-029` la cita a un informe SHCP sobre trimestres de 2026 (`itindc_202602`) cuya sección laboral puede reproducir la ola ENOE reservada.
- `[REPORTADO]` Discrepancias numéricas que señalaron los ejecutores quedan en `dictamen_razon` o `siguiente_operacion` de su fila; ninguna se corrigió en los reports (fuera de perímetro).

## 4 · NO-CORRIDO / RESERVAS

En el encargo archivado (§ `## NO-CORRIDO / RESERVAS`) y en `forense/no-corrido.tsv` (`NC-260924-ASTRA5-U0-MAPA-DOMINIOS-63db-01..05`): las 131 filas `NO-ACCESIBLE-DESDE-SANDBOX` (DIFERIDO-A `GEN2-ASTRA5-U5-ADQUISICION-1`), los diez EN-MEDICIÓN (DIFERIDO-A `GEN2-TUBERIA-VISTA-NORMALIZADA-2`), la herramienta de acceso no instalada, el registro documental de copias físicas SIN-ID y el alcance de la exposición ENOE 2026T1 (DECISIÓN-DE-MESA-PENDIENTE, `FP-260924-ASTRA5-U0-MAPA-DOMINIOS-63db-01`).

## 5 · Auditoría de rigor extremo

- ¿Pobreza, violencia o informalidad confundidas con cultura? Los mecanismos culturales que los reports derivan de esas estructuras quedaron NO-MEDIBLE con su límite; las cifras estructurales se contratan por separado.
- ¿Sobregeneralización desde clase media urbana? Se marcaron los universos urbanos (ENCIG, ENSU, ENDUTIH por TLOC) y las muestras de diáspora (b); las marcas de consumo y encuestas online quedan como documentos, no como población.
- ¿Marcos importados? Hofstede, GLOBE y la «psicología del mexicano» quedan (c) o ensayo; ningún puntaje país se trata como variable de persona.
- ¿Qué cambia con foco rural/indígena? Rural-indígena y usos y costumbres se dictaminaron por afirmación (IEEPCO, Censo, ENADID, ENSANUT medicina tradicional), no por título.
- ¿Qué parece psicológico y es incentivo racional? Las reglas SI-ENTONCES y los veredictos de los forenses quedaron NO-MEDIBLE cuando atribuyen causa a un caso único o a un par sin contrafactual; sus cifras, en filas propias.
- ¿Evidencia débil con intuición fuerte? 131 documentos no se pudieron confirmar desde el sandbox; ninguno se da por existente ni por inexistente.
- ¿Qué sería peligroso leído simplista? Leer MEDIBLE como «verdadero», o EN-MEDICIÓN como medido: el mapa dice qué se puede contrastar y con qué, no si la afirmación es cierta.
- ¿Afirmaciones sobre el estado del corpus escritas a mano? Ninguna: toda cifra de esta nota sale de `ensambla_mapa.py`, de las tablas derivadas o de `cierre_acto.py`.
- ¿Escala y unidad de cada cantidad? Cada fila declara unidad (persona, hogar, delito, trámite, empresa, documento) y universo; las fusiones sólo unen filas con el mismo componente.
- ¿PROSPECTIVA o RETROSPECTIVA? No aplica: el mapa no emite estimaciones.

## 6 · Recibo para el sucesor

`GEN2-ASTRA5-U5-ADQUISICION-1` (CAJA): parte de `hoja-adquisicion-derivada-v1_0.tsv` (ADQUIRIR 163 y DOCUMENTACIÓN-SOLAMENTE 605, con propietario y prioridad) y de `no-accesible-desde-sandbox-v1_0.tsv` (131), con `receta-acceso-fuentes-2026-09-24.md`. Un intento por ruta; resultado por URL en {EXISTE, NO-ENCONTRADO, NO-ACCESIBLE}; sin cambiar dictámenes (una fila que deba cambiar se propone). Descargar y registrar en `data/manifiesto.yaml` es `/adquiere`.
