# Revisión del programa — perfiles como descriptores, población por síntesis

**31/jul/2026 · propuesta para mesa, sin sellar. No es canon.**
Derivado de `main` en `5f59902` + el veredicto de INV-SEG parte 3 (`forense/notas/
2026-07-31-identificabilidad-perfiles.md`) + benchmark de práctica estándar
(LCA, poblaciones sintéticas/IPF, criterios de segmentación). Lo que es lectura
mía va marcado.

---

## 0 · El diagnóstico en una línea

Los seis perfiles fallan el criterio eliminatorio número uno de cualquier
segmentación (identificabilidad), por un mecanismo con nombre en la literatura
(forced choice de segmentación a priori), y la práctica estándar de ABM no
asigna agentes a tipos: **genera poblaciones con vectores de atributos que
reproducen marginales observadas** (IPF/síntesis, estándar desde Beckman 1996).
El modelo no está roto — está resuelto al revés.

---

## 1 · SE MANTIENE — y es la mayoría del programa

**Los generadores G1–G6.** Derivado de `modelo §2.2` en esta sesión: los seis
condicionan sobre **parámetros** (`confianza_institucional`, `radio_confianza`,
`sens_estatus`, `horizonte_temporal`, `familismo_*`, `exposicion_violencia`,
`deferencia`) — ninguno sobre número de perfil. **La maquinaria causal del
modelo es agnóstica a la partición.** Esto es lo que hace viable todo lo demás.

**Las 49 reglas del motor.** Solo 10 citan perfil, y lo hacen sobre `{1,4}` y
`{2,3}` — que son formalidad con otro nombre. Reescribirlas para condicionar
sobre el atributo directamente no cambia una sola predicción.

**El corpus entero.** 31 reports + 5 forenses + índice. La evidencia sobre
México no depende de cómo se particione la población simulada. Los patrones
que los perfiles resumían (horizonte corto bajo volatilidad, familismo como
seguro, deferencia instrumental) viven en los reports y en los generadores,
no en la tabla de §1.1.

**La reformulación identificación→ajuste.** Se **refuerza**: IPF + ajuste por
momentos es exactamente la ruta 3 de la metodología, y es como se calibran los
ABM en la práctica. ADR-50 acertó en el método; falló en la unidad sobre la
que se aplica.

**Toda la infraestructura.** Manifiesto (172/172), raíz externa, ids estables,
cobertura-motor, suite, índice de corpus, modelo de contaminación ADR-46,
firewall Fase A/B. Nada de esto se toca.

**El inventario de INV-SEG partes 1–2.** No solo sobrevive: **cambia de
función y sube de valor.** La tabla eje × fuente × variable es exactamente el
insumo que IPF necesita — marginales y semilla. Se construyó para responder
una pregunta y responde mejor la siguiente.

---

## 2 · CAMBIA — la revisión mayor, y es una sola

**§1.1 deja de ser una tabla de 6 filas con valores puntuales.**

- **Antes:** 6 perfiles × 15 parámetros = 90 celdas `ASIGNADO`, cada agente
  pertenece a un perfil, forced choice.
- **Después:** los agentes se generan por **síntesis de población** — semilla
  de microdato (candidata natural: ENIGH, la fuente con más ejes en el mismo
  registro) reponderada contra marginales de las demás fuentes. Cada agente
  lleva un **vector de atributos observables** (formalidad, edad, localidad,
  ingreso, acceso digital, migración) y los parámetros del modelo se expresan
  como **distribuciones condicionales sobre atributos**, no como constantes
  por perfil.
- **Los seis perfiles pasan de BASES a DESCRIPTORES** (la distinción estándar
  de Wedel & Kamakura): dejan de asignar agentes y pasan a describir regiones
  del espacio de atributos. "Popular informal" sigue existiendo como forma de
  hablar de los agentes informales de ingreso bajo — deja de existir como
  casilla que un agente ocupa en exclusiva.

*Lectura mía:* esto no es una concesión — es lo que `procedencia.yaml` ya
pedía cuando se advertía a sí mismo que valores puntuales por perfil producen
"seis clases de mexicano, la forma estadística del esencialismo que este
corpus combate". La literatura llegó a la misma conclusión por la vía técnica.

**Consecuencias directas del cambio:**

- Los **90 `params_base`** se redefinen: ya no son 90 celdas sino condicionales
  por atributo. El denominador de los 144 cambia — cuánto, lo decide el diseño
  nuevo de §1.1, no se sabe hoy.
- **CAL-CONF Fase B** deja de ser "poblar 36 celdas" y pasa a ser "medir
  confianza por institución condicionada a atributos observables" — que es
  **más fácil**: los cruces confianza × formalidad × edad existen en el
  microdato sin reconstruir ningún perfil.
- **ADR-50 §(1)** sobrevive en método y cambia en unidad: la exención de los
  90 ("se miden de transversal") vuelve a ser verdadera, porque medir
  condicionales sobre atributos observables sí es posible en transversal — lo
  imposible era medir por perfil.

---

## 3 · SE AJUSTA — barato, sin decisión nueva

- **Las 10 reglas con número de perfil** → citan el atributo (formalidad) que
  ya codifican. Cero cambio predictivo, un commit.
- **Perfiles 5 y 6** → atributos transversales (edad × digital; migración).
  El solapamiento que hacía fallar a la celda C desaparece porque ya no hay
  partición que violar.
- **Perfil 3 (trayectoria)** → deja de ser celda. Si se conserva, es una
  **transición** — y eso conecta con el pseudo-panel de cohortes, la única
  ruta que observa trayectorias. Deja de ser "el activo grande sin tocar" y
  pasa a ser la vía específica para lo que el perfil 3 quería capturar.
- **D-12** probablemente se disuelve: "operacionalización única por
  constructo" era una pregunta sobre celdas; sobre condicionales, cada
  componente del vector de confianza se mide donde su instrumento vive.
  (Verificar antes de cerrarla — no la cierra este documento.)
- **La cascada de ADR-50** (refutations.yaml:65, estado §L4) se ejecuta junto
  con esta revisión, en un solo acto, como estaba esperando.

---

## 4 · SE PIERDE — dicho sin suavizar

- **Los 90 valores puntuales de §1.1.** Eran `ASIGNADO` — juicio informado,
  cero medidos. Lo que valía de ellos (los patrones relativos: el perfil 2
  con horizonte más corto que el 1) se conserva como hipótesis sobre las
  condicionales, ahora falsables.
- **La cola alta sigue sin observarse.** IPF no inventa datos: si las
  encuestas de hogar no capturan a la élite A/B, la población sintética
  tampoco. Esto se declara como límite permanente del dato público mexicano,
  no se resuelve.
- **La comparabilidad con todo lo escrito en términos de perfiles.** hitoD
  (12 menciones), fichas, notas históricas — son append-only y quedan como
  historia. Toda referencia futura necesita la traducción perfil→región de
  atributos.

---

## 5 · QUEDA POR PROBAR — en orden, cada prueba con lo que decide

**P1 · ¿ENIGH sirve como semilla?** IPF necesita un microdato con la
**conjunta** de atributos en el mismo registro. INV-SEG tabla A da ENIGH en
régimen laxo cubriendo los 6 ejes. Falta verificar que todos viven en el
mismo registro/persona (no repartidos entre módulos sin llave). *Fase A-style,
solo descriptores, media sesión. Si falla: ENOE como semilla alternativa
(A B D en estricto).* **Decide: la viabilidad de la síntesis.**

**P2 · ¿Los momentos por atributo identifican los 29 libres?** Rehacer la
aritmética de INV-SEG parte 3 sobre celdas de atributos en vez de 4 celdas de
perfil. *Lectura mía, a confirmar:* debería mejorar mucho — las marginales
observables (formalidad × edad × localidad × ingreso) generan más celdas con
soporte real que las 4 uniones forzadas. Pero dos hallazgos del veredicto
**no** se arreglan con esto y hay que re-verificarlos: (a) G3/G5 justo
identificados con cero grados de libertad — infalsables; (b) el check ADR-30
de familismo sin contraste que separe apoyo de obligación. Si sobreviven al
reencuadre, son problemas del modelo, no de la segmentación.
**Decide: si ADR-50 se corrige o se reescribe.**

**P3 · LCA como prueba falsable de la segmentación del corpus.** La prueba
más valiosa del paquete: correr análisis de clases latentes sobre microdato
(Fase B, con pre-registro limpio) y ver **qué estructura emerge** — sin
imponerla. Si emergen ~2 clases separadas por formalidad, el corpus
sobre-segmentó y lo sabremos con dato. Si emergen más, los ejes que las
separan son la segmentación que los datos sí sostienen. Es la primera vez
que la segmentación del proyecto sería **falsable en vez de asumida** — y el
pre-registro debe escribirlo una sesión limpia (nube), porque INV-SEG
contaminó a las de Ubuntu contra las ocho fuentes.
**Decide: cuántas clases de mexicano sostiene el dato.**

**P4 · El check de ADR-28.b, ahora medible.** Dispersión de confianza entre
instituciones, condicionada a atributos. Los reactivos existen (CAL-CONF Fase
A los citó variable por variable). Sigue pre-registrado por ADR-49 D3 como lo
que revisita la pendiente común de G1a. **Decide: si G1a se desdobla.**

---

## 6 · Las decisiones de mesa que esto implica

1. **Sellar el reencuadre** (perfiles→descriptores, población por síntesis,
   parámetros como condicionales). Es LA revisión mayor de canon — un ADR
   grande o una v4 del modelo. No se toma hoy: se toma con P1 y P2 corridas,
   que son baratas y la vuelven decisión informada en vez de apuesta.
2. **El orden de las pruebas**: P1 y P2 primero (repo + descriptores, sin
   microdato), P3 y P4 después (Fase B, exigen pre-registro limpio).
3. **Qué pasa con `4 de 144`** mientras el denominador está en revisión: se
   congela como cifra histórica o se retira del titular. No debe seguir
   moviéndose mientras su definición cambia.

---

## 7 · Módulo de auditoría

**Contadores movidos por este artefacto: cero.** Es una revisión de plan.

**1–6.** No aplican — no afirma nada sobre México.

**7 · ¿Qué conclusión sería peligrosa simplificada?** *"La literatura dice que
los perfiles estaban mal."* No: dice que los perfiles como **bases de
asignación exclusiva** no pasan el criterio de identificabilidad con estos
datos. Como descriptores de heterogeneidad siguen siendo el resumen del
corpus. Y la síntesis IPF hereda sus propios supuestos (la conjunta de la
semilla se preserva al reponderar) — no es magia, es un supuesto distinto y
declarable.

**8 · ¿Qué afirmación sobre el estado del corpus no fue derivada?** Derivadas
en esta sesión: que G1–G6 condicionan sobre parámetros (grep de §2.2), el
conteo de menciones de perfil por artefacto, que 10 reglas citan perfil sobre
{1,4}/{2,3}. **No derivadas:** que ENIGH tenga la conjunta en el mismo
registro (P1 existe para eso); que los momentos por atributo superen 29 (P2);
la magnitud del cambio al denominador de los 144 (depende del diseño nuevo).
