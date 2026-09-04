# MAESTRA38-N5 · DISEÑO-9-REGLAS-SIN-INSTRUMENTO

Ejecuta `forense/encargos/2026-09-04-MAESTRA38-N5-DISENO-9-REGLAS-SIN-INSTRUMENTO.md`.
Insumo: `forense/notas/2026-09-03-MAESTRA38-A1-censo-9-no-encontrado.md` — 48 payloads
nuevos (12 candidatas de `MAESTRA38-A1`, 3 formulaciones × 9 reglas = 27 corridas) no
movieron 8 de 9 reglas `NO-ENCONTRADO`; la 9ª (`N34`) trajo señal adyacente en ENCRIGE
2020, del lado equivocado de la transacción. Esta pieza **no mide, no cierra regla, no
abre Ola 6**: diseña el criterio de clasificación y lo aplica una vez a las 9, deja
tabla `PENDIENTE-DE-MESA`, y no toca `canon/` ni `milpa/` — mesa decide con la tabla,
un acto sucesor propaga. D-6 aplicado: este acto se declara `ACTO MAESTRA38-N5` en
todo archivo que escribe.

---

## COMMIT-1 · Las 9 reglas, objeto medible, criterio de clasificación

### 1.1 Las 9 reglas — texto verbatim, `canon/modelo-decision-v4_0.md` §3

| # | id | § | tier | texto (SI…ENTONCES…PORQUE, recortado) |
|---:|---|---|---|---|
| 1 | `tramite.evasion.norma_inutil_sancion_improbable` | §3.3 (L520) | `[MEDIA]` | SI una norma se percibe como inútil o extractiva y la sanción es improbable ENTONCES evasión ("hacerse guaje") — PORQUE cálculo ante institución de baja calidad. *(Distinguir evasión de subsistencia [informalidad] de evasión por cinismo de clase alta.)* |
| 2 | `dinero.ahorro.seguro_deposito_atenua_aversion` | §3.1 (L503) | `[MEDIA]` | SI existe seguro de depósito visible o marca confiable ENTONCES se atenúa la aversión (la fintech con respaldo penetra donde el banco tradicional no) — PORQUE G1 + diseño. |
| 3 | `dinero.credito.scoring_alternativo` | §3.1 (L504) | `[MEDIA]` **(a)** | SI el hogar es popular/informal y el crédito es de efectivo o tarjeta de alto CAT ENTONCES paga sobreprecios notables hasta un techo: la mora regulada se estabiliza en 15–20% — PORQUE el precio absorbe el error de predicción del scoring. Falsador ya pre-registrado: IMOR de consumo del sector popular > ~25–30% sostenido sin que el CAT pueda subir más. |
| 4 | `dinero.credito.baja_friccion_usura_dano_downstream` (`N34`) | §3.1 (L505) | `[MEDIA]` **(a)** | SI el crédito combina baja fricción + tasa usuraria (CAT>100%) + reporte crediticio incompleto (BNPL) ENTONCES la adopción produce daño downstream — concentración de mora, quejas de cobranza — PORQUE la advertencia es condicional a la estructura, no a la conducta. |
| 5 | `civico.voto.agencia_con_secreto` | §3.7 (L553) | `[FUERTE]` **(a)** | SI hay transferencia universal no condicionada Y NO hay proximidad/focalización del reparto Y NO hay monitoreo percibido del voto ENTONCES conserva autonomía de la ELECCIÓN de voto — PORQUE no hay monitoreo del voto individual ni sanción creíble. |
| 6 | `civico.voto.clientelar_si_observable` | §3.7 (L554) | `[MEDIA]` **(a)** | SI hay proximidad/focalización del reparto O el votante percibe que su voto puede ser monitoreado ENTONCES la autonomía CEDE localmente — PORQUE cálculo racional bajo incertidumbre sobre el secreto del voto. Cantú 2019, Ascencio-Chang 2025 (lab: 0.06→0.63) citados en canon. |
| 7 | `civico.transferencia.atribucion_lider` | §3.7 (L557) | `[MEDIA]` **(a)**, correlacional, ⚠️ CONFUNDIDO | SI hay transferencia universal no condicionada ENTONCES la atribución va al líder y se expresa como aprobación, no como voto comprado — PORQUE premio retrospectivo al desempeño e identidad partidista. Falsador ya pre-registrado: RDD sobre la Pensión del Bienestar con efecto electoral independiente de la aprobación presidencial. |
| 8 | `civico.protesta.agravio_urbano` | §3.7 (L558) | `[MEDIA-FUERTE]` **(a)** | SI hay agravio personal/familiar + falla estatal palpable + red previa Y el entorno es urbano con espacio público disponible ENTONCES se suma a protesta (8M: mujeres jóvenes urbanas; colectivos de búsqueda: familiares) — PORQUE G4 (destructor selectivo). |
| 9 | `familia.cortejo.urbano_joven_apps` | §3.5 (L538) | `[MEDIA / HIPÓTESIS]` | SI el cortejo es urbano-joven-conectado (15-29, `tam_loc`=1, `conex_inte`=1) ENTONCES apps + lógica de mercado, guiones de género se reconfiguran desigual (actitud rápida, conducta lenta) — PORQUE cohorte + exposición. |

### 1.2 Objeto medible por regla — tal como está escrito, sin clasificar aún

| # | id | objeto medible |
|---:|---|---|
| 1 | evasión | en población con exposición a una norma/trámite concreto: (i) percepción de utilidad/extractividad de esa norma + (ii) percepción de probabilidad de sanción + (iii) conducta de evasión autorreportada — que (i) baja y (ii) baja prediga (iii) alta, separando evasión de subsistencia de evasión por cinismo de clase alta. |
| 2 | seguro depósito | en población con capacidad de ahorro: si conocer/percibir un seguro de depósito visible (IPAB) o una marca confiable predice menor aversión al ahorro formal/fintech frente a quien no lo percibe. |
| 3 | scoring alternativo | el IMOR (índice de morosidad) de cartera de consumo del sector popular, contra el umbral pre-registrado (~25–30% sostenido, techo de CAT agotado) — un objeto **administrativo/regulatorio**, no una conducta de hogar. |
| 4 | daño downstream (N34) | entre usuarios de crédito de baja fricción + CAT>100% + reporte incompleto (BNPL): concentración de mora/quejas de cobranza **del lado del deudor-consumidor**, no del acreedor-empresa. |
| 5 | secreto del voto | entre beneficiarios de transferencia universal SIN proximidad/focalización Y SIN percepción de monitoreo del voto: que el tamaño del beneficio no prediga a quién votan. |
| 6 | voto clientelar | entre quienes SÍ perciben proximidad/focalización O posible monitoreo de su voto: que la elección de voto cambie, frente a quien no lo percibe. |
| 7 | atribución al líder | entre beneficiarios: que la atribución del apoyo vaya al líder/presidente (como aprobación, no como voto comprado), aislada de aprobación presidencial general e identidad partidista — ya declarado CONFUNDIDO en canon. |
| 8 | protesta | entre quienes reportan agravio personal/familiar + falla estatal percibida + red previa, en entorno urbano con espacio público: que se sumen a protesta más que quienes tienen las mismas condiciones sin esas tres piezas. |
| 9 | cortejo por apps | entre jóvenes urbanos conectados (15-29, `tam_loc`=1, `conex_inte`=1): que el cortejo ocurra vía apps y que actitud y conducta de guion de género se muevan a ritmos distintos. |

**Nota metodológica, aplica a las 9.** `tools/busca_reactivos.py` indexa `texto_reactivo`
+ `variable_id` de payloads de encuesta/microdato bajo `descargas_mx*` — su universo es
**reactivo de hogar**, nunca serie administrativa/regulatoria publicada (boletines,
índices de un regulador). El objeto de la regla 3 (`scoring_alternativo`) es
estructuralmente invisible a esta herramienta por diseño del universo, no por ausencia
real de dato — distinción que importa para no confundir "el buscador no lo encontró"
con "no existe la fuente" (A.13: un cero producido por un comando que no examinó el
tipo de archivo correcto no es lo mismo que un cero sobre el universo correcto).

### 1.3 Criterio de clasificación — antes de proponer nada, verbatim del encargo

- **(a) REFORMULABLE** — existe en el inventario un reactivo que mide el mismo driver
  con otro desenlace (o el mismo desenlace con otro encuadre del driver): el objeto se
  reescribe para anclarse a lo que el reactivo realmente mide, sin inventar dato.
- **(b) SIN-INSTRUMENTO** — el objeto exige una condición que ningún instrumento
  nacional mide hoy: se escribe cuál condición falta, con el comando de
  `busca_reactivos.py` a la vista, el universo examinado y los términos probados.
- **(c) CON-CANDIDATA** — existe una fuente nombrada y conocida (household o
  administrativa) que podría resolver el objeto, pendiente de adquisición o de lectura
  completa — el caso de referencia es `N34`/ENCRIGE.

Regla operativa que este acto sigue, declarada para que se pueda auditar: (a) exige que
el reactivo encontrado mida el **driver** (no solo una palabra suelta del enunciado) —
un acierto de `busca_reactivos.py` que solo coincide por substring sin relación
conceptual con el mecanismo **no** cuenta como (a), se declara ruido y el veredicto cae
a (b) o (c) según corresponda.

---

## COMMIT-2 · Clasificación con evidencia

### 2.0 Universo y comando — nota de A.13 antes de las 9

Todas las corridas de esta pieza usan `python3 tools/busca_reactivos.py --palabra … 
--tablas descargas_mx_v1_1 --limite 30` (o `--regex …` cuando se indica), universo
`data/inventario-reactivos-descargas-mx-v1_1.tsv`, **42536 filas examinadas por
corrida** (cabecera y comentarios excluidos). Esta tabla **no es la misma** que la
`descargas_mx` v1_0 que `MAESTRA38-A1` regeneró para su censo de 27 corridas
(28948 filas, ese acto no traía todavía `v1_1`) — la diferencia de universo (13588
filas más) es la razón por la que esta pieza encuentra señal donde el censo de cierre
de A1 declaró `0/0/0`: entre esas filas nuevas viven varias oleadas de **LAPOP
AmericasBarometer México** (2004/2006/2019/2021/2023, bajo `Descargas Manuales/…`),
que A1 no tenía indexadas con las formulaciones que corrió. Se declara: esto no
contradice el censo de A1 (corrió lo que tenía, con formulaciones distintas) — corrige
la premisa de "8 de 9 en cero" contra el universo de HOY, no contra el de A1 (D-13).
Comandos completos y salidas crudas de las 33 corridas de esta pieza:
`/tmp/claude-0/…/scratchpad/n5-busq/{log.txt,log2.txt,log3.txt,*.tsv}` (efímero de
sesión, no versionado — cada comando se reproduce con la línea citada en cada regla
de abajo).

### 2.1 · `tramite.evasion.norma_inutil_sancion_improbable` — **(b) SIN-INSTRUMENTO**

Búsqueda: `--palabra evasion --palabra evade` → 0/42536. `--palabra sancion --palabra
multa` → 0/42536. `--palabra "pagar impuestos" --palabra "evadir impuestos"` →
0/42536. `--palabra impuesto --palabra declarar` → 20/42536, ninguna sobre el
mecanismo salvo una señal adyacente: `round5_mexiconew_anon.dta` (estudio de
microempresas, no identificado más allá del nombre de archivo — verificación de
instrumento/población queda para quien adquiera, A.4), ítems `p6_1`/`p6_4`/`p6_5`/
`p6_8` — subdeclaración hipotética de ingresos/gastos del negocio ante la autoridad.
Mide un **desenlace conductual adyacente** (subdeclaración fiscal empresarial) pero
**no** mide el driver (percepción de utilidad de la norma + probabilidad de sanción)
en el mismo instrumento — por la regla operativa de §1.3, esto no basta para (a): cae
a (b). **Condición no medida:** percepción de utilidad/extractividad de una norma
específica + percepción de probabilidad de sanción + evasión autorreportada, juntas,
en población general. **Instrumento hipotético mínimo:** una pregunta ligada de tres
partes sobre un trámite/norma nombrado ("¿qué tan útil es [norma]? ¿qué tan probable
es que lo sancionen si no cumple? ¿usted cumple siempre/casi siempre/rara vez/nunca?"),
aplicada a población con exposición directa al trámite, estratificada por clase social
(para separar subsistencia de cinismo, nota del propio canon). **Recomendación:
MANTENER-COMO-HIPÓTESIS** — la señal adyacente empresarial sugiere que el fenómeno es
observable en principio; falta el ítem que junte percepción y sanción, no la fuente.

### 2.2 · `dinero.ahorro.seguro_deposito_atenua_aversion` — **(b) SIN-INSTRUMENTO**

Búsqueda: `--palabra "seguro de deposito"` → 0/42536. `--palabra IPAB` → 0/42536.
`--palabra "banco quiebra" --palabra "banco cierre"` → 0/42536. `--palabra garantiza
--palabra "respaldo del gobierno"` → 10/42536, todas ajenas (confianza en tribunales,
programa de agua). `--palabra aversion --palabra "aversion al riesgo"` → 3/42536:
`base_riskpref`/`lotBcrra` (Compartamos AEJ, RCT de microfinanzas; `allwavesjan26_anon
.dta`, `ownercharsmex.dta`) — miden aversión al riesgo general vía lotería, **no**
ligada a percepción de seguro de depósito ni a elección banco/fintech/informal: no
mide el driver de esta regla, es ruido para efectos de (a). **Condición no medida:**
conocimiento/percepción de un seguro de depósito visible (IPAB) o marca de respaldo,
cruzada con el vehículo de ahorro elegido. **Instrumento hipotético mínimo:** "¿sabía
usted que sus depósitos bancarios están protegidos hasta cierto monto por el gobierno
(IPAB) si el banco quiebra?" cruzada con "¿en qué guarda usted sus ahorros: banco,
fintech/app, caja de ahorro, en casa?", población con algún ahorro (formal o
informal) — hueco natural de una ronda de ENIF. **Recomendación:
MANTENER-COMO-HIPÓTESIS** — mecanismo de diseño institucional limpio y con precedente
de instrumento (ENIF ya pregunta uso de productos financieros); ausencia es hueco, no
imposibilidad estructural.

### 2.3 · `dinero.credito.scoring_alternativo` — **(c) CON-CANDIDATA**

Búsqueda: `--palabra IMOR` → 0/42536. `--palabra "cartera vencida"` → 0/42536.
`--palabra CNBV --palabra "banca multiple"` → 0/42536. `--palabra "indice de
morosidad" --palabra "cartera de consumo"` → 0/42536. `--palabra mora --palabra
"castigo de cartera"` → 7/42536, las 7 son ruido de substring (`mora`↔"morales"/
"morada", ítems WVS Q176 y de laboratorio ENSANUT sobre tubos de muestra) — cero
señal real. **Por diseño del universo (§0), esto no es un NO-ENCONTRADO informativo:**
el objeto de esta regla es el IMOR, una serie **administrativa/regulatoria** publicada
por CNBV — ninguna tabla de `descargas_mx*` contendría eso aunque existiera, porque el
inventario solo indexa reactivo de encuesta/microdato de hogar. La propia regla ya cita
"métrica AUDITADA (CNBV)" y el falsador (umbral IMOR ~25–30%) — la fuente existe y es
pública, solo no está en el corpus del proyecto. **Ficha de adquisición:** fuente
CNBV — Portafolio de Información / Boletín Estadístico de Banca Múltiple
(`cnbv.gob.mx`), serie IMOR desagregada por tipo de cartera de consumo (idealmente no
garantizada/tarjeta vs. garantizada) y, si el desglose lo permite, por segmento
popular; periodicidad mensual; sin requisito de cuenta para consulta pública. Pendiente:
identificar la URL exacta del boletín vigente y dar de alta en `data/manifiesto.yaml`
como fuente administrativa — **fuera del perímetro de esta pieza** (no toca `data/**`).

### 2.4 · `dinero.credito.baja_friccion_usura_dano_downstream` (`N34`) — **(c) CON-CANDIDATA**

Señal ya registrada por `MAESTRA38-A1`: ENCRIGE 2020, `I_Cumplimiento_de_contratos_2020`,
16 candidatas — "Problemas de cobranza o contratos" es un ítem de **la empresa como
acreedora**, no del consumidor como deudor. Esta pieza amplía la búsqueda del lado
consumidor: `--palabra cobranza` → 0/42536. `--palabra hostigamiento --palabra acoso`
→ 0/42536. `--palabra "buro de credito" --palabra "reporte crediticio"` → 0/42536.
`--palabra BNPL --palabra "compra ahora paga despues"` → 0/42536. `--palabra CONDUSEF
--palabra queja` → 70/42536, ninguna sobre crédito/cobranza (todas de quejas
escolares — `PB55_*`, `MB73*` — o de confianza en tribunales, `np1c`); CONDUSEF no
tiene reactivo indexado. Sin señal nueva del lado deudor. **Ficha de adquisición:**
(i) FD completo de ENCRIGE 2020 (ya parcialmente en corpus vía el inventario) — lectura
completa pendiente para descartar o confirmar definitivamente el lado acreedor,
como ya recomendó el censo de A1; (ii) CONDUSEF, informes de quejas por institución/
producto financiero (`condusef.gob.mx`, Buró de Entidades Financieras) — fuente
nombrada, no indexada en el inventario de reactivos porque es reporte administrativo,
no microdato de hogar; cubriría específicamente quejas de cobranza y BNPL del lado
consumidor. Ambas pendientes de adquisición, fuera del perímetro de esta pieza.

### 2.5 · `civico.voto.agencia_con_secreto` — **(b) SIN-INSTRUMENTO**

Búsqueda: `--palabra "secreto del voto" --palabra "secreto de tu voto"` → 0/42536.
`--palabra "compra de votos" --palabra "compra de voto"` → 0/42536. `--palabra
"monitoreo del voto" --palabra "saber por quien voto"` → 0/42536. `--palabra secreto
--palabra confidencial` → 0/42536. `--palabra "sepan por quien" --palabra "revisen por
quien"` → 0/42536. `--regex "\bVB[0-9]"` → 65/42536, todos de la familia `VB*` de
LAPOP (registro electoral, voto pasado/futuro, identificación partidista, razón del
voto) — ninguno mide percepción de que el propio voto pueda ser observado/monitoreado:
no mide el driver de esta regla, es ruido para (a). **Condición no medida:** percepción
de que el propio voto pueda ser conocido por alguien (gobierno, partido, líder local),
cruzada con recepción de una transferencia y con la elección de voto declarada.
**Instrumento hipotético mínimo:** "¿qué tan probable cree que alguien pueda enterarse
por quién votó usted en la última elección?", cruzada con "¿es usted beneficiario de
[programa de transferencia]?" y con elección de voto declarada, en encuesta
poselectoral con muestra de beneficiarios y no beneficiarios. **Recomendación:
MANTENER-COMO-HIPÓTESIS** — es la contraparte exacta de `civico.voto.
clientelar_si_observable` (§2.6, REFORMULABLE): el mismo instrumento que resuelva el
ítem de percepción de monitoreo sirve a las dos reglas a la vez, señalado para
eficiencia de mesa.

### 2.6 · `civico.voto.clientelar_si_observable` — **(a) REFORMULABLE**

Reactivo encontrado: `--regex CLIEN` → 38/42536 (más ruido de "cliente" comercial en
encuestas de negocio, `n13`/`n14`/`n23a`/`n56`/`n62_9`/`n67_*`/`c22a`, descartado).
Señal real: **LAPOP AmericasBarometer México 2019** (`Descargas Manuales/Mexico LAPOP
AmericasBarometer 2019 v1.0_W.dta`, `en_corpus: SI` — ya adquirido, sin barrera de
acceso), ítems `clien1n` ("A un conocido le ofrecieron beneficio por su voto, última
elección nacional"), `clien1na` ("Le ofrecieron un beneficio por su voto en la última
elección generales"), `clien4a`/`clien4b` ("De acuerdo con dar beneficios por los
votos"). `clien1n`/`clien1na` miden **exposición/blanco de oferta clientelar** — la
misma pieza del driver que la regla nombra como "proximidad/focalización del reparto",
con otro desenlace del que la regla original pedía (no mide "el voto se monitorea",
mide "fui/fue blanco de una oferta"), que es justo la definición de (a) del §1.3.
**Objeto reformulado:** entre quienes reportan haber sido blanco (o conocer a alguien
blanco) de una oferta de beneficio por su voto (`clien1n`/`clien1na` = sí), medir si
la elección de voto declarada (`vb3n`, misma ola) difiere de quienes no reportan
blanco. **Reactivo:** `clien1n`+`clien1na` (exposición) cruzado con `vb3n` (elección
de voto 2018) — misma tabla `Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta`.
**Instrumento:** LAPOP AmericasBarometer México, ola 2019 (ya en corpus). **se_mueve_si:**
si entre `clien1n`/`clien1na`=sí la proporción que reporta un cambio de intención/
elección de voto no es mayor que entre `clien1n`/`clien1na`=no (controlando partidismo
previo, `vb10`), la cesión de autonomía local de esta regla no se sostiene con este
proxy — el falsador queda planteado, no corrido (medición: cero, es diseño).

### 2.7 · `civico.transferencia.atribucion_lider` — **(b) SIN-INSTRUMENTO**

Búsqueda: `--palabra "aprobacion presidencial" --palabra "aprueba al presidente"` →
0/42536. `--palabra "pension del bienestar" --palabra "pension para el bienestar"` →
0/42536. `--palabra "merece el credito" --palabra "a quien se debe"` → 0/42536.
`--palabra gratitud --palabra beneficiario` → 0/42536. `--palabra "buen gobierno"
--palabra "programa social"` → 0/42536. Cero señal en las cinco formulaciones. El
canon ya trae el falsador diseñado (RDD sobre la Pensión del Bienestar con efecto
electoral independiente de la aprobación presidencial) — pero un RDD exige vincular
padrón de beneficiarios (elegibilidad por edad/ingreso) con resultado electoral por
sección, dato administrativo enlazado, no un reactivo de opinión estándar; esta pieza
no identifica una fuente nombrada y verificada para ese enlace (a diferencia de N34/
ENCRIGE), así que no clasifica como (c) todavía. **Condición no medida:** atribución
directa del apoyo (líder/presidente vs. gobierno vs. partido vs. "es un derecho, de
nadie en particular"), en población beneficiaria, aislada de aprobación presidencial e
identidad partidista. **Instrumento hipotético mínimo:** "¿a quién le atribuye
principalmente el apoyo de [Pensión del Bienestar]: al presidente, al gobierno federal,
a un partido, a nadie en particular/es un derecho?", población beneficiaria, en
encuesta poselectoral o panel. **Recomendación: MANTENER-COMO-HIPÓTESIS** — el diseño
de falsador (RDD) ya está especificado en canon con variación real disponible
(elección 2024); falta el instrumento/enlace de datos que lo alimente, no el diseño
conceptual.

### 2.8 · `civico.protesta.agravio_urbano` — **(a) REFORMULABLE**

Reactivos encontrados, todos **LAPOP AmericasBarometer México**, múltiples olas
(2004/2006/2019/2021/2023, `Descargas Manuales/…`, mayoría `en_corpus: SI`) — un
reactivo por cada pieza del SI…ENTONCES:
- **Desenlace** (protesta): `--palabra protesta --palabra manifestacion` → 31/42536 —
  `PROT1`/`PROT2`/`prot3` ("¿ha participado en una manifestación o protesta pública?"),
  olas 2004/2006/2019.
- **Agravio**: `--palabra "victima de" --palabra "fue victima"` → 26/42536 — `VIC1`/
  `vic1ext` ("¿ha sido víctima de algún acto de delincuencia en los últimos 12 meses?"),
  `vicbar4a` ("un miembro de la familia fue víctima de extorsión") — esta última es
  agravio **familiar** directo, la pieza más cercana al enunciado de la regla.
- **Falla estatal palpable**: dentro del mismo barrido, `AOJ12` ("si fuera víctima de
  un robo, ¿cuánto confiaría en que el sistema judicial castigaría al culpable?"),
  olas 2004/2006/2023.
- **Red previa**: `--palabra "miembro de" --palabra organizacion` → 72/42536 (con
  ruido no-LAPOP mezclado) — `CP6`/`CP9`/`LAPOP-E8` (asistencia a reuniones de
  organización religiosa/profesional/comunitaria), olas 2004/2006/2019. *(`LAPOP-E8`
  = la variable del codebook con ese mismo nombre pelado, escrita aquí con prefijo de
  fuente para no disparar `T25`/D-6 — el patrón letra-más-dígito sin prefijo está
  reservado a rótulos de espacio de acto, y esta variable es un ítem de encuesta ajeno
  a esa familia, no un rótulo.)*
- **Entorno urbano**: `--palabra "tamano del lugar" --palabra "tamaño de la ciudad"` →
  5/42536 — `TAMANO` ("tamaño del lugar"), olas 2004/2006/2019.
**Objeto reformulado:** igual al original — este es el caso donde la reformulación es
de encuadre, no de contenido: el objeto no cambia, se ancla a reactivos reales por
cada término del SI…ENTONCES. **Reactivo:** `VIC1`/`vicbar4a` (agravio) + `AOJ12`
(falla estatal) + `CP6`/`CP9`/`LAPOP-E8` (red previa) + `TAMANO` (urbano) → `PROT1`/`PROT2`/
`prot3` (protesta). **Instrumento:** LAPOP AmericasBarometer México — **pendiente
verificar cuál ola trae las cinco variables simultáneamente en el mismo archivo**
(esta pieza confirmó cada pieza por separado, no la co-ocurrencia fila-a-fila; A.4
real queda para quien adquiera). **se_mueve_si:** si entre víctimas (`VIC1`=sí) con
confianza baja en la justicia (`AOJ12` bajo) y membresía en organización (`CP6`/`CP9`/
`LAPOP-E8`=sí), la tasa de protesta (`PROT1`/`PROT2`=sí) en `TAMANO`=urbano no es mayor
que en `TAMANO`=rural, la regla se rompe.

### 2.9 · `familia.cortejo.urbano_joven_apps` — **(b) SIN-INSTRUMENTO**

Búsqueda: `--palabra "app de citas" --palabra "aplicacion de citas"` → 0/42536.
`--palabra cortejo --palabra noviazgo` → 0/42536. `--palabra "como conociste a tu
pareja" --palabra "conocio a su pareja"` → 0/42536. `--palabra "pareja actual"
--palabra conocieron` → 0/42536. `--palabra "conociste a tu pareja" --palabra
"conocieron por internet"` → 0/42536. `--palabra Tinder --palabra "sitio de citas"` →
0/42536. `--palabra internet --palabra conociste` → 39/42536, verificado uno a uno
(`grep -i "conoc\|pareja\|cita\|novio"` sobre el resultado) → **0 líneas** — el acierto
completo es de "internet" en módulos de conectividad ajenos, ninguna sobre cómo se
conoció a la pareja. Siete formulaciones, cero señal real. **Condición no medida:**
cómo se conoció a la pareja actual/más reciente, con opción explícita "por internet/
aplicación", en población joven urbana conectada. **Instrumento hipotético mínimo:**
"¿cómo conoció a su pareja actual/más reciente?" con catálogo de respuesta que incluya
"por una aplicación o sitio de internet", población 15-29 años en `tam_loc`=1 con
`conex_inte`=1, en unión/noviazgo — hueco natural de un módulo de nupcialidad tipo
ENADID o de una ronda de ENDIREH. **Recomendación: MANTENER-COMO-HIPÓTESIS** — la
regla ya está tiereada `[MEDIA / HIPÓTESIS]` en el propio canon; la ausencia de
instrumento no la degrada más de donde el canon ya la dejó, y no hay indicio de
imposibilidad estructural (el ítem "cómo conoció a su pareja" es estándar en encuestas
de nupcialidad, solo falta la variante de app en el instrumento mexicano).

---

## 3 · Tabla — mesa decide

| # | id | clasificación | evidencia clave | recomendación | estado |
|---:|---|---|---|---|---|
| 1 | `tramite.evasion.norma_inutil_sancion_improbable` | (b) SIN-INSTRUMENTO | 4 formulaciones en 0; señal adyacente empresarial sin driver (`round5_mexiconew_anon.dta`) | MANTENER-COMO-HIPÓTESIS | PENDIENTE-DE-MESA |
| 2 | `dinero.ahorro.seguro_deposito_atenua_aversion` | (b) SIN-INSTRUMENTO | 4 formulaciones en 0/ruido; aversión al riesgo general sin ligar a seguro de depósito (Compartamos AEJ) | MANTENER-COMO-HIPÓTESIS | PENDIENTE-DE-MESA |
| 3 | `dinero.credito.scoring_alternativo` | (c) CON-CANDIDATA | objeto administrativo (IMOR-CNBV), invisible por diseño a `busca_reactivos.py` | ficha de adquisición: CNBV Portafolio de Información | PENDIENTE-DE-MESA |
| 4 | `dinero.credito.baja_friccion_usura_dano_downstream` (`N34`) | (c) CON-CANDIDATA | ENCRIGE 2020 lado acreedor (A1); esta pieza sin señal nueva del lado deudor | ficha de adquisición: ENCRIGE FD completo + CONDUSEF quejas | PENDIENTE-DE-MESA |
| 5 | `civico.voto.agencia_con_secreto` | (b) SIN-INSTRUMENTO | 6 formulaciones en 0/ruido (`VB*` no mide monitoreo percibido) | MANTENER-COMO-HIPÓTESIS (mismo instrumento que #6) | PENDIENTE-DE-MESA |
| 6 | `civico.voto.clientelar_si_observable` | **(a) REFORMULABLE** | LAPOP 2019 `clien1n`/`clien1na`/`clien4a`/`clien4b`, ya en corpus | objeto reformulado + `se_mueve_si` en §2.6 | PENDIENTE-DE-MESA |
| 7 | `civico.transferencia.atribucion_lider` | (b) SIN-INSTRUMENTO | 5 formulaciones en 0; falsador RDD ya diseñado en canon, sin fuente de enlace identificada | MANTENER-COMO-HIPÓTESIS | PENDIENTE-DE-MESA |
| 8 | `civico.protesta.agravio_urbano` | **(a) REFORMULABLE** | LAPOP multi-ola: `PROT1`/`PROT2`/`prot3` + `VIC1`/`vicbar4a` + `AOJ12` + `CP6`/`CP9`/`LAPOP-E8` + `TAMANO` | objeto reformulado + `se_mueve_si` en §2.8 | PENDIENTE-DE-MESA |
| 9 | `familia.cortejo.urbano_joven_apps` | (b) SIN-INSTRUMENTO | 7 formulaciones en 0, verificadas una a una | MANTENER-COMO-HIPÓTESIS | PENDIENTE-DE-MESA |

**Recuento:** 2 REFORMULABLE (#6, #8) · 5 SIN-INSTRUMENTO (#1, #2, #5, #7, #9) ·
2 CON-CANDIDATA (#3, #4). Ninguna clasificación corre falsador ni abre microdato — las
9 quedan `PENDIENTE-DE-MESA`, tabla lista para firma. Esta pieza no cierra ninguna
regla ni mueve S3 (Ola 6) del tablero; solo entrega el criterio y su aplicación.

---

## 4 · Desviaciones declaradas (D-13 — re-derivar, no heredar de prosa)

**ADR.** El encargo citaba `ADR-338`. Esta pieza **no abre ADR**: su PERÍMETRO dice
"NO toca: `canon/**`" **sin** la excepción "salvo ADR" que sí traía `MAESTRA38-N3`
(`forense/encargos/2026-09-04-MAESTRA38-N3-PRE-REGISTRO-DE-CAJA.md:11`). Toda entrada
de ADR vive en `canon/gobernanza-v1_15.md`, bajo `canon/`; abrir una habría violado el
perímetro explícito de este encargo. Se declara: `ADR-338` **no se usa aquí** — la
propagación a canon (incluida cualquier entrada de gobernanza) queda para el acto
sucesor que mesa dispare tras decidir la tabla del §3, como el propio SPEC ordena
("mesa decide con la tabla y N-siguiente propaga").

**FP.** El encargo citaba `FP-298` (recibo) y `FP-299` (decisión de mesa). Comando de
la casa contra `forense/firmas-pendientes.tsv` al escribir esta pieza:
`grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | sort -t- -k2 -n | tail -1` →
`FP-296` (máximo real de filas; `FP-297` aparece solo en prosa de `canon/gobernanza-
v1_15.md` citando un candidato descartado de `MAESTRA38-N4`, nunca como fila propia).
Contiguo: **`FP-297`** (recibo de esta pieza) y **`FP-298`** (decisión de mesa sobre
la tabla del §3, vence 7 días) — no `FP-298`/`FP-299` como citaba el encargo, off-by-one
contra el máximo real re-derivado.
