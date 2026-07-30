Retomo el programa "Psicología del Mexicano Contemporáneo". Esta conversación
es la Maestra.

═══ AVISO DE DUPLICACIÓN — LEE ESTO PRIMERO ═══
Existe ya `TRANSFER-maestra-8.md` en el repo, commit `eb92d99`, escrito por
Claude Code al cerrar el 29/jul. **No lo he leído**: la app colapsó el bloque
y nunca se mostró completo.

Este documento NO lo sustituye. Es el traspaso del lado del chat: prioridades,
orden de trabajo y asignación de modelo — decisiones que se tomaron en
conversación y que TRANSFER-8 puede no traer.

**Primera tarea de la sesión: leer TRANSFER-8 y decir qué dice este documento
que aquel no, y viceversa.** Si son redundantes, se conserva el del repo y
este se descarta. Dos archivos declarando el mismo estado es exactamente lo
que costó medio día en julio.

Fuente de verdad: `Modelado-Mexicano` (privado, GitHub, Josanoforo).
Cita COMMIT HASH, no md5 improvisado.

═══ ESTADO VERIFICADO EL 29/JUL ═══
HEAD `eb92d99` · rama `main` · 8 commits ese día · ninguno firmado
(clave de firma vacía en el entorno de nube; no es del trabajo).

Suite: **18 FAIL · 111 WARN**.
  - Los 18 FAIL se reprodujeron EXACTOS en Windows/Python 3.14 contra la
    corrida original en contenedor Linux, desglose test por test. Primera
    verificación independiente que tiene el programa.
  - Los WARN se movieron tres veces: 107 → 109 → 111. Las tres subidas son
    T03 disparando sobre las citas `-v3.2.md`/`-v3_2.md` que los propios
    documentos de traspaso contienen al describir ese falso positivo. Si
    esperas 107 y ves 111, es eso.
  - T03 = 45 (era 41 antes de commitear las transferencias).

Motor: 49 reglas · 20 [FUERTE] · 19 [MEDIA] · 5 [MEDIA-FUERTE] ·
2 [HIPÓTESIS] · 3 compuestas. Perímetro del Hito D = **27**, fijado el
28/jul en `gobernanza:266`, confirmado por T12. **No es ambiguo.**

Artefactos: `modelo` v3.2 · `glosario` v5.6 · `gobernanza` v1.8 (37 ADR) ·
`estado-programa` **v1.8** (v1.7 borrado por ADR-36).

═══ LO QUE SE CERRÓ ═══
- Migración real al repo, con CI en GitHub Actions.
- `343d589` confirmado real. La transferencia decía la verdad; la duda que
  se le planteó estaba mal fundada.
- Byte `0xC3` truncado en `CONTRIBUTING.md` pos 2149 — rompía la suite en
  T03 con `UnicodeDecodeError`. Por eso nunca había corrido completa.
- **Perímetro de la suite auditado**: T07, T08, T09 y T10 solo miran
  `corpus/reports/`. El canon, del que se leen los tiers, casi no lo revisa
  nadie. Nota `9301e59`.
- T09 verificado con conteo: los 5 usos causales reales están todos en
  reports. Ampliarlo al canon no gana señal, solo ruido.
- T10 verificado: de 45 disparos nuevos, 39 son contexto de auditoría,
  1 falso positivo, 5 en el integrador. Cuatro son defecto de medida del
  test. **Uno es real: `integrador:174`** — el tier [Sólido] se asigna en
  "Evidencia a favor" sin marca, y el caveat vive en "Evidencia en contra".
  Secciones opuestas. La marca no viaja con el dato.
- `estado` v1.8: §7 afirmaba "Paso 1 COMPLETO, cubre las 27". **Cubre 24.**

═══ PRIORIDADES · EL ORDEN IMPORTA ═══

**P0 — No escribir las 3 fichas faltantes hasta decidir el baseline.**
El pre-registro cubre 24 de 27. Las 3 que faltan son todas de §3.3
(autoridad, trámite, Estado), el dominio donde vive el gate de Fase 1 y el
único sin un solo falsador pre-registrado.

Eso convierte el baseline LLM en urgente por una razón precisa: esas tres
predicciones **todavía no existen**, así que aún pueden generarse fuera de
muestra. Si se escriben las fichas primero, la ventana se cierra para
siempre. Cada ficha resuelta sin baseline es una predicción perdida.

Sub-decisión que hay que tomar explícitamente: **qué modelo genera el
baseline debe declararse y congelarse**, y no debería ser el mismo que
luego resuelve las fichas — o, si lo es, que quede declarado como límite.
Si no, el baseline queda contaminado y no mide nada.

**P1 — Modo línea base del CI.** Verificado: `main()` devuelve 1 con
cualquier FAIL, sin distinguir conocido de nuevo. El CI queda rojo
permanente, y un rojo permanente deja de ser señal: a la tercera semana
nadie lo abre, y aparece la presión de editar reports para callarlo — lo
único prohibido. Congelar 18/111 como estado conocido: verde = no
empeoraste, rojo = introdujiste algo. Bajar la cifra queda como acto
deliberado con rastro en el diff. `tests/` NO es append-only.

**P2 — Las dos decisiones de la suite.**
  a) ¿T07 debe vigilar el vocabulario de tier del motor? Las 3 etiquetas
     compuestas existen, nadie las declaró sancionadas ni deriva, y nada
     impide que aparezcan más sin que se note.
  b) ¿T10 se amplía al canon cambiando el patrón, o el integrador adopta
     la marca `(b)`? El integrador usa al menos tres convenciones propias
     — `[Fuerte, con caveat US]`, `Caveat US:`, `muestras US-hispanas`.
     Cumplen la función localmente pero no viajan, que es para lo que la
     marca existe.

**P3 — Verificar las 5 "decisiones que requieren firma".** Llegaron de otra
conversación sin acceso al repo. La #1 (perímetro 27) ya estaba cerrada en
`gobernanza:266`. Las otras cuatro sin contrastar. Son insumo, no estado.

**P4 — Trabajo de corpus.** Todo DECLARADO en TRANSFER-7, nada verificado
contra el repo: carga de tiempo (7 decisiones cerradas por escribir),
turno 1 (auditoría de los 4 pivotes), 2 correcciones de reports
(`ref.A.02` sobre horas OCDE; el 39.7 %/26.5 % de ENASIC en
`La_familia`), turnos 2-3-4 con los 27 reports restantes.
Verificar antes de ejecutar: TRANSFER-7 ya falló en tres cifras.

═══ DÓNDE VA FABLE ═══
La lección del 29/jul es que el trabajo mecánico nunca falló y el de
juicio falló seis veces. Correr la suite, grepear, git, listar archivos:
exacto siempre, y no se puede cherry-pickear. Clasificar 45 disparos,
decidir si `integrador:174` es defecto de medida o real, auditar un
borrador antes de que entre al canon: ahí cayeron las seis cifras. Cuatro
las atrapó Opus releyendo un borrador hecho con Sonnet.

**Fable — juicio caro y difícil de detectar cuando falla:**
- Diseño del baseline LLM (P0). Es la decisión que determina qué cuenta
  como fuera de muestra, y no se puede rehacer.
- Clasificación con cita: el patrón "muéstrame los N con archivo, línea y
  cita textual, y clasifica cada uno".
- **Auditoría de borradores antes de que entren al canon.** Modo explícito:
  "no lo continúes, audítalo". Ahí es donde el modelo más fuerte se pagó
  solo hoy.
- Las decisiones P2 y las de firma de P3.
- Pre-registro adversario de consultas (ADR-38): evaluar la SINTAXIS de la
  consulta, no la intención declarada de quien la escribió.

**Opus/Sonnet en Claude Code — ejecución:**
Correr la suite, git, barridos mecánicos, redacción de borradores,
operaciones de archivo. Barato, verificable, y el error se ve.

**Fable NO para barridos exhaustivos.** No hay ventaja: lo mecánico ya sale
exacto y el costo no se recupera.

Dos cosas prácticas por confirmar en sesión:
- Si Fable es seleccionable en Claude Code o solo en el chat. No lo sé;
  revisa el selector de modelo. Si solo está en chat, el patrón es:
  CC ejecuta y redacta, se pega el borrador aquí, Fable audita, vuelve a CC.
- Las salvaguardas de Fable enrutan a Opus 5 en menos del 5 % de sesiones.
  Este programa usa vocabulario de "red team", "adversario", "ataque" en
  sentido epistémico. Si una respuesta se siente menos afilada de lo
  esperado, puede ser eso; no es un problema, solo hay que reconocerlo.

═══ REGLAS QUE NO SE NEGOCIAN ═══
- **Nada entra al canon desde una conversación sin repo.** Lo que sale de
  un chat es hipótesis hasta verificarse contra archivo, con línea y cita.
  [REGLA NUEVA del 29/jul: cayeron por esto la transferencia, un supuesto
  sobre un commit, y una lista de decisiones estructurales.]
- Los tiers se LEEN del glosario y de los mapas de evidencia. No se
  reconstruyen. Si un tier no está a la vista, ve a buscarlo.
- Las reglas se CITAN TEXTUALMENTE de `modelo §3.B`, con tier, dominio y
  perfiles. Sin cita, es propuesta nueva.
- Procedencia: (a) dato EN México · (b) muestra de diáspora — NO es
  evidencia sobre México · (c) marco importado. La marca VIAJA.
- Segmenta siempre. Una afirmación sobre "el mexicano" es señal de alarma.
- Hallar que la psicología NO importó es un resultado VÁLIDO.
- Descartar con rigor es entregable. ARCHIVA los descartes.
- Consolidar PRIMERO, borrar DESPUÉS.
- `corpus/` y `forense/` son APPEND-ONLY. Se corrigen con nota fechada,
  NUNCA en silencio.
- Los tests documentan defectos de la EVIDENCIA. Si un test falla, NO se
  edita el report para que calle.
- No escribas la causa de algo declarado irrecuperable. Registrar ≠ explicar.
- Español.
- En Windows: `py`, no `python3`. Y `$env:PYTHONIOENCODING="utf-8"` o la
  consola truena con los caracteres de caja.

═══ TRAMPAS ESPECÍFICAS ═══
- **La estimación no es cifra.** "~22 y ~46 disparos" resultaron 26 y 111.
  Cuando un modelo diga "aproximadamente", pide el conteo.
- **El resultado cómodo se verifica primero.** "La mayoría son falsos
  positivos" justificaba no ampliar el perímetro. Resultó cierto para T09
  y falso para T10.
- **Pedir la cita textual es lo que atrapa.** Las seis cifras cayeron así,
  ninguna por la suite. `curaduria-archivos:23` no dice lo que se le
  atribuía; la frase del "Fuerte pelón" solo existe en la nota que la cita.
- Un hook o una instrucción de entorno puede empujar a commitear sin
  revisión. CC se negó bien el 29/jul. Que se siga negando.
- Trabajar en la nube deja dos copias del repo y puede imponer una rama que
  nadie eligió. Si se usa: push antes de cambiar de puerta, pull al llegar.
- PD-01: 14 descartes irrecuperables. NO RECONSTRUIR.
- El modelo NO tiene entidad prestamista (frontera declarada de ADR-35).
- MILPA Fase 1 POSPUESTA por decisión, no por olvido.
- Ninguna salida con decimales: 60 de 144 números son ordinales
  cardinalizados. 15 coeficientes de generador, CERO medidos.

═══ LO PRIMERO ═══
1. Confirmar HEAD y correr `py tests\check.py`. Si no da 18 FAIL, DETENERSE.
2. Leer `TRANSFER-maestra-8.md` y reconciliarlo con este documento.
3. Recién entonces, P0.
