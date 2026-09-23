# MISION-ASTRA-4 · PRODUCTO: del aparato al modelo del mexicano que alguien pueda usar
**Dirección (Claude Fable), 23/sep/2026 · main `560c4836` al redactar (re-deriva al abrir) · para Astra (decide el cómo) y Codex (ejecuta hasta cerrar); mesa firma adopciones y publica · sustituye a MISION-ASTRA-1 (cerrada) y suspende MISION-ASTRA-2 · cuatro unidades paralelizables; ninguna mide contra una ola reservada; ninguna construye retadores.**

Lo que el programa tiene y no ha convertido en nada: 179 corridas selladas, 87 estimadores adoptables con IC calibrado en tres instrumentos, nueve celdas-D de crédito, dos de ENCIG 2025, cuatro de ENVIPE 2025, tres mediciones nuevas de ASTRA-3, y un hallazgo sellado seis veces («la persistencia es el mejor predictor»). Lo que el programa arrastra: 146 cifras legacy dentro del motor y sus consumidores, tecleadas antes de GEN2, que hoy contestan las consultas. Esta misión convierte lo primero en producto y saca lo segundo.

Reglas comunes: las seis del transfer (§5) y las de México (§6). Toda cifra en cualquier entregable se cita por `RESULT-*` con su CALC y hash, con unidad, escala y generación; ninguna se teclea. Toda afirmación sobre México lleva su tier (fuerte / media / hipótesis razonable / narrativa popular) y su falsador. Cada unidad cierra con recibo de Codex y entra por recibo de Claude.

---

## U1 · CATÁLOGO DEL MEXICANO: lo adoptado, por dominio, en reglas que un lector aplica

**Objetivo.** Un documento consultable (`canon/catalogo-del-mexicano-v1_0.md` + tabla `canon/catalogo-del-mexicano-v1_0.tsv`) con cada estimador adoptado o adoptable —por dominio (dinero, trámites y Estado, seguridad y norma, tiempo y cuidado, ingreso y gasto), instrumento, ola, segmento— con punto, IC calibrado, unidad, PROSPECTIVA/RETROSPECTIVA, y la columna de exclusión por oferta al lado de cada marginal de mercado. Y, por dominio, las reglas del modelo en el formato de §5 de las instrucciones: **SI [segmento] ENTONCES [conducta] — PORQUE [driver] — [TIER]**, con disparadores de contexto y el falsador de cada regla.

**Antecedentes vigentes.** Adopciones firmadas: ENVIPE (#1002, `decisiones.tsv` `5ef1f41`), ENIF con reserva de ancho (#1009, F2), ENCIG vetada hasta IC calibrado (#1002) → tu `CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001` (#1041) es la pieza que puede levantar el veto: propón la adopción con la misma opción que mesa firmó para ENIF. Crédito 2024: nueve celdas-D (#1058), K1 con reserva. Exclusión por oferta: tus CALC de #1042. Bloque de 10 RESULT pendientes de adopción (`…TRAMITE-FIRMAS-7-369b-01`: Banxico, LAPOP, MOTRAL). Marcador: `data/corrida0/marcador-segmento.tsv` (derivado; se lee, no se edita). Lectura de la serie de crédito 2012–2021 pendiente (`GEN2-DIN-CREDITO-SERIE-LECTURA-1`, en cola: absórbela si sigue sin correr).

**Perímetro.** Propio: `canon/catalogo-del-mexicano-v1_0.{md,tsv}`, `forense/analisis/catalogo/` (tablas intermedias, todas derivadas por comando desde `resultados.json`), tests propios (cada RESULT citado existe y su hash coincide), nota, NC, FP de adopción para lo adoptable no adoptado (una fila por instrumento, con recomendación). Ajeno: `milpa/*.yaml`, marcador, celdas-D, `decisiones.tsv` (las adopciones las firma mesa sobre tu FP).

**Datos autorizados.** Solo RESULT sellados en `data/corrida0/CALC-*/resultados.json` de CALC con `cuenta_gen2: SI`. Ningún microdato. ENCIG 2025 y ENVIPE 2025 ya sin reserva: RETROSPECTIVA. Nada de ENVIPE 2026 más allá de lo que el duelo selló.

**Dependencias.** `GEN2-CONTADORES-CONSUMO-1` (en vuelo) publicará el marcador con 87 adoptados; no lo esperes: lee `decisiones.tsv` + celdas-D + specs, que es la fuente, y declara la diferencia si la hay.

**Criterio de terminado.** Tabla con N filas = número de estimadores adoptados o adoptables (derivado por comando, citado); 0 cifras sin `RESULT-*`; cada dominio con ≥ 5 reglas SI-ENTONCES con tier y falsador; cada marginal de mercado con su fila de oferta al lado o el rótulo de por qué no la tiene; módulo de auditoría de rigor extremo al final del .md; test verde. Frase de portada, en una línea: cuántos estimadores, cuántos dominios, y la tesis (estabilidad, no cambio).

---

## U2 · RELEVO DE LAS 146 CIFRAS LEGACY: que el motor conteste con números sellados

**Objetivo.** Que ninguna consulta del motor devuelva una cifra GEN1. Las 146 lecturas legacy activas (`corrida0.py status`: motor 34 · procedencia 40 · catálogo de momentos 23 · marco del duelo 43 · celdas-D 6) se relevan una por una: cada una por un `RESULT` GEN2 que ya exista (vía ii: pin con replay afirmativo), por un derivado determinista de uno (vía iii), o por un **CALC nuevo que re-mide desde el insumo crudo** (E.1: un GEN1 que agregó de otro modo se re-mide, no se reinterpreta). Orden: motor (34) y celdas-D (6) primero porque son los que contestan al usuario; luego catálogo (23); procedencia (40) y marco del duelo (43) al final o dictaminados HISTÓRICO-SIN-RELEVO si mesa lo firma.

**Antecedentes vigentes.** `data/corrida0/relevo-usos-v1_0.tsv` (inventario de usos), `mapa-demanda-19-corr-v1_0.tsv`, `demanda-corridas.tsv` / `demanda-resultados.tsv` (`corrida0.py demanda`: 87 corridas requeridas). Reglas E.1–E.3 y E.7 (vías de relevo; la vía (i) lee el eje RESULTADO desde D6, 23/sep). Ejemplos ya hechos: `milpa/tramite.yaml:94-96` (ENCUCI 2020 mordida) y `:180-181` (ENCIG 2025 presencial) son `p` tecleados → cada uno necesita su CALC o su pin. Codex ya tiene `BRIEF-CODEX-TANDA-CANDIDATOS-1` (12 slots de `tramite.yaml`): Astra lo absorbe y lo extiende al inventario completo.

**Perímetro.** Propio: `forense/prereg-caja/RELEVO-*` (spec humana por CALC nuevo, con sidecar), `data/corrida0/CALC-RELEVO-*`, pines en el archivo de relevo que E.7 nombra, `replay-evidencia.tsv` (append), `milpa/*.yaml` **solo por el comando de relevo que el repo ya tiene** (nunca editando un `p` a mano; si no existe comando, la pieza lo propone en NC y no edita), tests, nota. Ajeno: motor (`milpa/src/motor.py`, autorizado solo a `GEN2-MOTOR-DEUDA-LOTE-1`), tablero.

**Datos autorizados.** Microdato de olas no reservadas, desde CAJA, por id del manifiesto (ENCUCI 2020, ENCIG ≤ 2025, ENVIPE ≤ 2025, ENIF ≤ 2024, ENIGH ≤ 2024, ENUT, ENBIARE, ENASIC…). Tabulados públicos solo como constancia congelada, nunca como fuente de un `p` de motor.

**Dependencias.** D7 firmada (motor editable solo por el acto de MOTOR). Cada CALC de relevo: dos commits mínimo (spec congelada → resultado). Lotes D-11 de hasta cuatro piezas afines por PR.

**Criterio de terminado.** `python3 tools/corrida0.py status | grep legacy_activas_por_consumidor__motor` → 0 y `__celdas_D` → 0, cada relevo con su asiento; `__catalogo_de_momentos` → 0 o con plan fechado; `__procedencia` y `__marco_del_duelo` con dictamen por fila (RELEVADO / HISTÓRICO-SIN-RELEVO propuesto a mesa / NO-CONSTRUIBLE con texto de pregunta y FD recorrido, A.15). `check.py --baseline` VERDE en cada PR. Un test que falle si `milpa/*.yaml` gana una cifra sin `RESULT-*` citado.

---

## U3 · ANEXO DE EVIDENCIA DEL INFORME v1.3: las seis evaluaciones, una tabla, sin adjetivos

**Objetivo.** El anexo que sostiene la tesis del informe (`canon/informe-programa-v1_3-ANEXO.md`; la tesis la escribe dirección): una tabla por evaluación —instrumento, ola, cruces, celdas puntuadas, contendientes, comparación primaria (ΔMAE con IC), umbral, dictamen B-bis, PROSPECTIVA/RETROSPECTIVA, unidad— derivada de los CALC de adjudicación por comando; una sección de cobertura por instrumento con IC binomial por celda y por conglomerado (v2.16 §4), con el apellido del instrumento; una sección «qué haría falta para vencer al piso» escrita por ti, que has construido retadores: qué tamaño de efecto real habría que detectar, con qué n, y por qué las siete familias no lo alcanzan (escala y unidad declaradas, sin promediar personas con trámites ni delitos).

**Antecedentes vigentes.** `canon/informe-programa-v1_2.md` (estructura y frase 26/35 de cobertura); dictámenes: `forense/notas/*PILOTO-4*cierre*`, `*DUELO-ENCIG2025*`, `*DUELO-ENVIPE2026*`, `*ENIGH-DUELO*`, lote ENIF 2024, piloto 3 (`GOB-DIGITAL-EXE`); `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` (#1009) y tu `…ENCIG-…-0001` (#1041); `VALIDACION-INDEPENDIENTE-PILOTOS-1` (#970, 35/35 COINCIDE).

**Perímetro.** Propio: el anexo, `forense/analisis/informe-v1_3/` (tablas derivadas), test (cada cifra del anexo existe como RESULT), nota. Ajeno: `canon/informe-programa-v1_3.md` (dirección), celdas-D, CALC.

**Datos autorizados.** Solo RESULT sellados y notas de cierre. Ningún microdato.

**Dependencias.** Ninguna en vuelo. Si `GEN2-CONTADORES-CONSUMO-1` cambia `celdas_validadas` antes de que cierres, cítalo por commit.

**Criterio de terminado.** Anexo con seis filas de evaluación (o el número que el árbol tenga, derivado y citado), 0 cifras sin `RESULT-*`, cobertura con IC binomial por instrumento, módulo de auditoría al final, y la sección «qué haría falta» con al menos un cálculo de potencia explícito por dominio (n, efecto mínimo detectable, con la varianza de las réplicas selladas).

---

## U4 · FAMILIAS 2027 CON RESERVA: el frente prospectivo en piloto automático

**Objetivo.** La lista nominal que FP-374 pide desde el 15/sep y nadie escribió (NC-0234: ≥ 6 familias ejecutables con reserva): para cada ola que INEGI publicará en los próximos 18 meses, qué estimandos se sellan antes de que exista, con qué piso, qué umbral, qué vocabulario cerrado, y **un solo retador externo** por familia si lo hay (el tuyo, si crees que tienes uno distinto; si no, ninguno: un piso solo también se evalúa). Entregable: una hoja de firma para mesa + una spec humana por familia en `forense/prereg-caja/FAMILIA-2027-*-spec-v1_0.md` con sidecar, sin `spec.yaml` todavía (eso es COMMIT-1 de cada acto futuro).

**Antecedentes vigentes.** FP-374 (re-sello pendiente, `…958c-02`), NC-0161/0162/0234 (familias reservadas), E.6 (toda ola nueva nace RESERVADA; la levanta solo código congelado o mesa por escrito; una apertura sirve a todos los contendientes sellados antes), calendario INEGI (búscalo y cítalo: ENVIPE 2026 ya está reservada; ENCIG 2027, ENIF 2027, ENIGH 2026, ENCO mensual, ENUT, ENBIARE). Duelos previos como plantilla: `2026-09-21-GEN2-DUELO-ENVIPE2026-CONGELA-1.md` y `-COMMIT-1.md`.

**Perímetro.** Propio: `forense/prereg-caja/FAMILIA-2027-*`, `forense/analisis/familias-2027/` (calendario citado, tabla de estimandos), hoja `HOJA-FAMILIAS-2027-para-mesa.md`, NC, nota. Ajeno: `data/manifiesto.yaml` (las reservas las asienta el acto de adquisición), todo CALC.

**Datos autorizados.** Ninguno nuevo: solo RESULT sellados para elegir estimandos con historia y potencia; calendario y cuestionarios públicos de INEGI desde nube. **Nada de ENVIPE 2026 ni ENCO.**

**Dependencias.** Ninguna. Mesa firma la hoja; cada familia se vuelve acto cuando su ola entre al manifiesto.

**Criterio de terminado.** ≥ 6 familias, cada una con: instrumento y ola con fecha INEGI citada, lista cerrada de estimandos (unidad, escala, universo, con RESULT históricos por id), piso declarado, umbral y regla primaria (diferencia de error medio con IC por réplica), vocabulario B-bis, qué pasa si el falsador no refuta, contendientes (máximo: piso + un externo), y el cálculo de potencia con las réplicas selladas de la última ola. Hoja de firma con una fila por familia y recomendación.

---

## Lo que esta misión NO hace
No construye ni evalúa retadores, pilotos ni duelos (regla 6). No edita `p` a mano en ningún yaml. No toca CI, tablero, derivados, motor. No adopta: propone adopciones en FP. No abre olas reservadas. Si una unidad descubre que su premisa es falsa, decirlo con cita y conteo es el entregable.

## Orden sugerido y paralelismo
U1 y U3 en nube desde hoy (leen solo sellados); U2 en caja con Codex desde hoy, empezando por motor y celdas-D; U4 cuando U1 tenga la lista de estimandos con historia. Un PR por unidad o por lote D-11; recibo de Claude por PR. Reporta avance por contador, no por lista de tareas: `legacy_activas_por_consumidor__*` es el de U2; «N estimadores en catálogo con RESULT» el de U1.
