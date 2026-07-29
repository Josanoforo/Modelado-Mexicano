> ⚠️ **DOCUMENTO MUERTO — el estado vive en `estado`.** Movido a `forense/historico/` el 29/jul/2026 (sesión de correcciones); declara estado que ya no es cierto y no se edita más abajo de esta línea.

Retomo el programa "Psicología del Mexicano Contemporáneo". Esta conversación
es la Maestra.

═══ CAMBIO DE SUSTRATO — LEE ESTO PRIMERO ═══
El programa MIGRÓ A REPOSITORIO. El proyecto de Claude ya no es la fuente de
verdad: es `Modelado-Mexicano` (privado, GitHub, Josanoforo). Commit inicial
`343d589`, 65 archivos versionados.

Motivo: el ciclo de subir-y-bajar archivos costó, en una sola sesión, dos
parches escritos-entregados-y-perdidos, cuatro desincronizaciones de montaje,
dos archivos distintos declarando la misma versión, y una tarde entera
adjudicando cuál de dos auditorías correctas mentía (ninguna: leían snapshots
distintos del mismo archivo). Ninguno era problema de razonamiento. Los seis
eran control de versiones.

**Deja de usar md5 improvisado para sincronizar: cita COMMIT HASH.**

Estructura del repo:
  corpus/reports/   31 reports temáticos        APPEND-ONLY
  corpus/forense/   5 validaciones forenses     APPEND-ONLY
  canon/            modelo · glosario · gobernanza · estado · integrador
  milpa/            whitepaper · spec · plan + 3 YAML
  forense/          auditorías, barridos, pre-registros   FECHADOS, APPEND-ONLY
  tests/check.py    13 tests · CI en GitHub Actions

═══ ESTADO DEL MODELO ═══
`modelo` v3.2 · **49 reglas · 20 [FUERTE]** · 144 números, 4 medidos ·
15 coeficientes de generador, CERO medidos.
`glosario` v5.6 · `gobernanza` v1.8 (37 ADR) · `estado-programa` v1.7.

Es una síntesis rigurosa de literatura con tiers leídos, NO un artefacto
validado. 1 de 27 reglas del perímetro con falsación corrida.

═══ PRIMERA CORRIDA DE LA SUITE: 18 FAIL · 110 WARN ═══
La mitad de los FAIL son hallazgos NUEVOS. Una auditoría manual de los cuatro
pivotes, hecha el mismo día, los subcontó — porque leyó 4 archivos y la suite
lee 36:

  T06  7 valores de Gini (la auditoría vio 4) · 12 de confianza interpersonal (vio 4)
  T07  7 vocabularios de tier ajenos al Bloque A: SÓLIDO×44 · MEDIO×29 ·
       HIPÓTESIS RAZONABLE×22 · Moderada · MODERADA-FUERTE · Narrativa exagerada
  T08  7 reports SIN mapa de evidencia (el glosario declaraba 5) — todo
       constructo suyo es DERIVADO, no LEÍDO
  T09  8 casos de marco importado (c) usado como CAUSA, en todo el corpus
  T05  5 constructos del motor ausentes del glosario — DOS los introduje yo
  T11  atrapó automáticamente el defecto C-01 (ver abajo)

Falsos positivos declarados, en WARN a propósito: T03 (44, cabeceras citando
`-v3.2.md` cuando la plataforma renombró a `-v3_2.md`) y T10 (65, lista de
palabras de diáspora demasiado laxa). Afinarlos antes de subirlos a FAIL.

═══ TRABAJO PENDIENTE, YA ESPECIFICADO ═══
Todo esto está decidido y escrito. Falta ESCRIBIRLO en el canon. Va en UN PR.

A) CARGA DE TIEMPO — 7 decisiones cerradas (`forense/spec-carga-tiempo-v1_0.md`)
   Ocho reglas del motor invocaban "tiempo" y el modelo NO tenía la variable.
   1. El género entra a la capa de parámetros — CON CUELLO: un modificador
      solo modula un parámetro si existe medición publicada de esa modulación.
   2. ESQUEMA DE CELDA (48: perfil × sexo × etnia × ruralidad), poblado solo
      donde hay medición → resultaron CERO. Los 4 datos de ENUT son
      MARGINALES, no celdas: entran como RESTRICCIONES que toda asignación
      debe reproducir, no como valores.
   3. Celda vacía → INTERVALO acotado por los marginales; NO_COVERAGE de red.
      ⚠️ Esto es la puerta de entrada a ADR-28.d y probablemente decide la
      arquitectura de los 15 parámetros, no solo de éste.
   4. V2 `dispersion_jornada` entra DECLARADA Y VACÍA, ruta a microdatos ENOE.
      PROHIBIDO asignarle valor provisional.
   5. Seis reglas reclasificadas · §3.4 va a B1 (permiso laboral) · §3.6 fuera ·
      recuento completo releyendo las 49 al propagar.
   6. `ref.A.02` REFORMULADA sobre ENUT segmentado y BAJADA de MUY_FUERTE a
      FUERTE. No se retira.
   7. Anti-tautología EN CADA REGLA y EN COMPILACIÓN.

   Dato clave que refutó la intuición: en horas de MERCADO el FORMAL trabaja
   MÁS que el informal (Cuevas/De la Torre/Regla 2016; Oxfam-MCV oct 2024).
   Lo que distingue al informal es la DISPERSIÓN. Lo detectaron las consultas
   ADVERSARIAS del pre-registro.

B) TURNO 1 — auditoría de los 4 pivotes (`auditoria-seis-defectos-cuatro-pivotes`)
   A-01..A-14 · C-01..C-14 · R-01..R-07 · M-01..M-07 · T-01..T-05.
   Los más graves:
   - A-02: el FOUNDATIONAL tiene UNA sola marca de tier en 329 líneas, y la
     metí yo con el parche de ADR-31. Sin mapa de evidencia.
   - C-01: MI PROPIO PARCHE declaró tres ediciones "las ÚNICAS que el report
     requería" y dejó DIEZ líneas de Hofstede sin marcar (c). Quinto caso de
     afirmación de estado falsa. T11 ahora lo atrapa solo.
   - C-06/07/08: IZEA (empresa de marketing de influencers), GWI (panel
     comercial con dato GLOBAL), AMVO (cámara del sector), Statista, prensa —
     todos en tier `Fuerte`. Y §13 del mismo report reconoce el sesgo de
     consultoras y NO lo aplica a su propio mapa.
   - M-01: Hofstede sostiene el tier [SÓLIDO] de Moral Emotions; ADR-06 nunca
     llegó ahí. Hofstede tiene CUATRO estatus distintos en cuatro pivotes.

C) DOS CORRECCIONES DE REPORTS
   - `ref.A.02`: la OCDE declara por escrito que sus datos de horas "son
     inadecuados para comparar el nivel de horas entre países". El 2,207 de
     México ≈ ENOE 42.2 h/sem × 52, SIN los descuentos que sí se aplican a
     otros países. Penn World Table da 1,628 h. Reformular sobre ENUT.
   - `La_familia_mexicana`: el "39.7% de mujeres cuidadoras que desean
     trabajar PERO NO PUEDEN" está mal etiquetado. ENASIC 2022: 39.7% =
     "desearían trabajar por un ingreso". El "no pueden" es 26.5%. Dos
     indicadores fusionados.

═══ TURNOS 2, 3 y 4 — PENDIENTES ═══
Los 27 reports restantes, en tres turnos. Protocolo obligatorio:
  PASO 0: reportar nº de archivos, y por cada report nombre, LÍNEAS y MD5.
  Si algo no coincide, DETENERSE. Sin eso, dos corridas leen snapshots
  distintos y ninguna puede saberlo — pasó, y costó medio día.
  Todo hallazgo con NÚMERO DE LÍNEA Y CITA TEXTUAL. Sin las dos, no se archiva.

═══ LA DECISIÓN DE FONDO QUE SIGUE ABIERTA ═══
¿Los tiers del corpus son leíbles? Si el foundational no tiene sistema de
tiers, 7 reports no tienen mapa de evidencia, y hay 7 vocabularios
incompatibles, entonces "los tiers se LEEN del glosario y de los mapas de
evidencia" —la regla que no se negocia— NO SE HA PODIDO CUMPLIR NUNCA. No por
incumplimiento: porque no había de dónde leer.

═══ REGLAS QUE NO SE NEGOCIAN ═══
- Los tiers se LEEN del glosario y de los mapas de evidencia. No se
  reconstruyen. Si un tier no está a la vista, ve a buscarlo.
- Las reglas se CITAN TEXTUALMENTE de `modelo §3.B`, con tier, dominio y
  perfiles. Sin cita, es propuesta nueva y no cuenta como validación.
- Procedencia: (a) dato EN México · (b) muestra de diáspora — NO es evidencia
  sobre México · (c) marco importado. La marca VIAJA.
- Segmenta siempre. Una afirmación sobre "el mexicano" es señal de alarma.
- Hallar que la psicología NO importó es un resultado VÁLIDO.
- Descartar con rigor es entregable. ARCHIVA los descartes.
- Consolidar PRIMERO, borrar DESPUÉS.
- Todo principio nuevo nace con su artefacto de salida — y ahora con su TEST.
  Un ADR sin test en `tests/check.py` es un ADR decorativo.
- ADR-38: las consultas de búsqueda SE PRE-REGISTRAN. Toda corrida lleva una
  consulta ADVERSARIA, evaluada POR SU SINTAXIS, no por la declaración de
  intención de quien la escribió.
- corpus/ y forense/ son APPEND-ONLY. Se corrigen con nota fechada, NUNCA en
  silencio. Reescribir un forense para que cuadre con el estado posterior es
  la racionalización post-hoc que el Bloque C prohíbe.
- Español.

═══ TRAMPAS ESPECÍFICAS ═══
- CHERRY PICKING VERIFICADO, tres casos (`forense/auditoria-sesgo-busqueda-v1_0.md`):
  (1) una consulta anunciada como "anti-superviviente" llevaba `baja demanda`
      dentro — la sintaxis decía lo contrario de la intención declarada;
  (2) el check de ADR-32.c corrió sobre 16 términos que yo elegí, y los
      constructos que escaparon fueron los que yo mismo había introducido;
  (3) el barrido forense buscó `ROMPE|MATIZA`, patrón mío: 14 líneas de
      veredicto quedaron invisibles. La tasa de fuga del 41% SE RETIRA.
- Lo mecánico y exhaustivo NO se puede cherry-pickear. La búsqueda SÍ.
- `R1.1` está en veredicto B, no D. Yo lo cerré como D sobre búsqueda sesgada.
  Candidato irresuelto con nombre: fondos de aseguramiento del sur e indígenas
  (RedSol-Agrícola, AMUCSS, Oaxaca). Ojo: el "Café de Chiapas" que nombré NO
  es un fondo de aseguramiento, es cooperativa Fairtrade — verifiqué mal.
- `conf.06` RESUELTO: eran TRES REACTIVOS distintos de la misma escala
  (62.1% conocidos · 32.1% vecinos · 21.8% "la mayoría"). Pero T06 encontró
  12 valores de confianza en el corpus completo: el patrón es mucho mayor.
- El modelo NO tiene entidad prestamista (frontera declarada de ADR-35).
- MILPA Fase 1 POSPUESTA por decisión, no por olvido.
- PD-01: 14 descartes irrecuperables. NO RECONSTRUIR.
- Ninguna salida con decimales: 60 de 144 números son ordinales cardinalizados.

═══ LO PRIMERO ═══
Confirma el estado del repo (commit hash y resultado de `tests/check.py`)
ANTES de proponer trabajo. Después, el PR de propagación con A + B + C.

⚠️ Si Claude Code empieza a "arreglar" los reports para que pasen los tests,
está rompiendo la regla que sostiene todo el programa. Los tests documentan
defectos de la evidencia; se corrigen con nota fechada en la fuente, no
editando el dato para que el test calle.
