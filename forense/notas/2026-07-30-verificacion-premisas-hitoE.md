# Verificación de premisas · `hitoE-campana-medicion-v2_0.md`

### 30/jul/2026 · derivada contra `78d5d54` · rama `claude/new-session-gdstpo`

> | | |
> |---|---|
> | **QUÉ ES** | La verificación que `instrucciones` v2.1 exige antes de ejecutar un encargo: comprobar contra archivo las premisas del plan de Hito E |
> | **QUÉ NO ES** | Un veredicto sobre el plan. No dictamina si la campaña es buena idea — dictamina qué afirmaciones suyas se sostienen contra el repo |
> | **PROCEDENCIA** | Tipo (1) en todo: cada línea de abajo se derivó leyendo el repo en esta sesión, con `78d5d54` a la vista. El objeto verificado es tipo (3) |
> | **QUÉ NO SE HIZO** | No se editó el cuerpo del plan. `instrucciones` v2.1 prohíbe ajustar el texto para que cuadre |

**Por qué existe.** `instrucciones` v2.1: *«Quien ejecuta verifica las premisas del encargo antes de ejecutarlo. Si una premisa no se sostiene contra el archivo, se detiene y lo reporta — no la ejecuta, y no ajusta el texto para que cuadre. Encontrar que una instrucción estaba mal fundada es un entregable, no una interrupción.»* El plan de Hito E llegó como adjunto de chat —tipo (3)— y afirma catorce cosas sobre el estado del repo. Se verificaron las catorce.

---

## 1 · Lo que se sostiene — diez de catorce

| # | Afirmación del plan | Verificado contra | Veredicto |
|---|---|---|---|
| 1 | Los 6 generadores tienen **15 coeficientes**, con el desglose G1:2 · G2:2 · G3:3 · G4:4 · G5:3 · G6:1 | `milpa/procedencia.yaml:270-281` | **SE SOSTIENE** — derivado por script, suma 15 |
| 2 | Los valores asignados de la tabla de `§0` (`−0.60`, `−0.35`, `0.55`, `0.20`, `−0.60`, `0.40`, `0.20`, `0.70`, `−0.40`, `−0.20`, `−0.15`, `0.50`, `0.15`, `0.45`) | `milpa/procedencia.yaml:270-281` | **SE SOSTIENE** — coinciden uno a uno |
| 3 | `familismo_obligacion` está **sin magnitud** | `milpa/procedencia.yaml:66,274` | **SE SOSTIENE** — spec literal: *«signo negativo o no monotónico — SIN MAGNITUD»* |
| 4 | `CAL-G3` declaró la **opción (b)**: la ficha **no** calibra el `−0.60` | `forense/hitoD-preregistro-v2_0.md:511` | **SE SOSTIENE** — literal: *«La magnitud `-0.60` NO está en juego: es ASIGNADA, y la opción (b) del punto (2) ya declaró que esta ficha no la calibra»* |
| 5 | `CAL-G3` terminó **sin estimar nada** | `forense/bitacora.md:538` | **SE SOSTIENE** — literal: *«CAL-G3 Fases A y B, sin estimar nada»* |
| 6 | ADR-47 nombra la confusión falsar-regla / calibrar-coeficiente | `canon/gobernanza-v1_15.md:388,466` | **SE SOSTIENE** |
| 7 | ADR-46 fija que la unidad de contaminación es la **sesión** | `canon/gobernanza-v1_15.md:363,467` | **SE SOSTIENE** |
| 8 | `R3.2` dejó las probabilidades del motor **4x-34x** fuera de escala | `forense/hitoD-R3_2-veredicto-v1_0.md:75` · `forense/hitoD-preregistro-v2_0.md:472` | **SE SOSTIENE** — *«entre 4x y 34x por encima de lo medido, según la interpretación»* |
| 9 | El **perímetro de 27** mezcla falsación y calibración, y ADR-47 abrió su reclasificación sin resolverla | `canon/gobernanza-v1_15.md:8` · `canon/cola.yaml` `D-11` | **SE SOSTIENE** — el perímetro sigue en 27; `D-11` está abierta y explícitamente sin resolver |
| 10 | **ENUT** — 5 ediciones catalogadas como *existen y son alcanzables*, sin bajar | `canon/cola.yaml` `D-08` | **SE SOSTIENE** — cinco ediciones (2002/2009/2014/2019/2024), *«existen y son alcanzables, falta bajarlas, no falta localizarlas»*, ninguna descargada |

**Nota sobre el punto 9 del plan (`§1`, `§9`, benchmark).** El plan es correcto al declarar `milpa/procedencia.yaml` intocable y al prohibir la conversión efecto→peso. Esa disciplina es coherente con ADR-47 y con el veredicto de `R3.2`. Nada de lo que sigue la contradice.

---

## 2 · Lo que no se sostiene — cuatro afirmaciones

### 2.1 · Los 15 coeficientes se reducen a **9** constructos, no a 8

**La afirmación.** `§0`: *«Los 15 son 8 constructos latentes reutilizados. […] Operacionalizar los 8 constructos resuelve los 15 coeficientes. Ese es el apalancamiento que hace la campaña viable.»* Y `§10`, punto 8, la declara **derivada**: *«que los 15 se reducen a 8 constructos, por inspección de esa misma estructura»*.

**Lo derivado.** Contando los constructos distintos de `milpa/procedencia.yaml:270-281`:

| # | Constructo | Aparece en |
|---|---|---|
| 1 | `aversion_riesgo` | G2 · G3 |
| 2 | `confianza_institucional` | G1 · G4 |
| 3 | `deferencia` | G6 |
| 4 | `exposicion_violencia` | G4 |
| 5 | `familismo_apoyo` | G3 · G5 |
| 6 | `familismo_obligacion` | G5 |
| 7 | `horizonte_temporal` | G3 · G4 |
| 8 | `radio_confianza` | G1 · G5 |
| 9 | `sens_estatus` | G2 · G4 |

**Son nueve.** El propio plan los nombra todos: los cuatro compartidos que enumera en `§0` (`confianza_institucional`, `horizonte_temporal`, `aversion_riesgo`, `sens_estatus`), más `radio_confianza` —también compartido, G1 y G5, y el plan no lo enumera—, más `familismo_apoyo`, `familismo_obligacion`, `exposicion_violencia` y `deferencia`. El `§8` del plan nombra `radio_confianza` entre los frágiles, así que el constructo no se le escapó: se le escapó del conteo.

**Por qué importa, y no es cosmético.** El 8 propaga a cuatro lugares operativos del plan:

- `§1`, el diagrama de E0: *«8 constructos × 61 fuentes»*
- `§2`, el riesgo declarado: *«algunos de los ocho»*, *«si tres de ocho no se operacionalizan»*
- `§5`, la obligación de honestidad: *«una campaña que mide 5 de 8»*
- `§9`, **la puerta E0 → E1**: *«≥5 de 8 constructos con fuente candidata»*

La puerta es lo grave. Un umbral de 5/8 (62.5%) y uno de 5/9 (55.6%) no son el mismo criterio, y el plan pre-registra el primero para una población que es el segundo. Es la familia exacta de `instrucciones` v2.2 —*«todo umbral se verifica antes de pre-registrarse»*— aplicada a un denominador en vez de a una tasa base.

**Clase de defecto.** Pregunta 8 del módulo de auditoría (v2.1): una afirmación sobre el estado del corpus **declarada derivada** que no lo fue. Es el mismo patrón que `I-16`, y es notable dónde ocurrió: en el módulo de auditoría de un documento cuya tesis central es que la v1.0 heredó un supuesto sin verificarlo.

### 2.2 · `confianza_institucional` no es **un** constructo — es un vector de seis

**La afirmación.** `§2`: la operacionalización *«es única por constructo, no por generador»*, presentada en `§4` como **la mitigación** del riesgo técnico de la campaña: *«`confianza_institucional` se estima en G1 y en G4. Si las dos sesiones lo operacionalizan distinto, el modelo queda con dos valores del mismo constructo.»*

**Lo derivado.** `canon/modelo-decision-v3_4.md:119-130` (ADR-28.b): *«No es un escalar. […] El vector mínimo distingue: seguridad-fuerzas armadas · educación · salud · electoral-partidos · justicia-policía · financiera. G1 opera sobre el componente relevante al dominio, no sobre un promedio.»* Y `§2.2` del mismo archivo (`:184-190`, la tabla de coeficientes) lo indexa explícitamente por generador: **G1a** usa `confianza_institucional[dominio]`, **G4** usa `confianza_institucional[justicia]`.

**Por qué importa.** La mitigación del plan invierte la decisión del modelo. El motor **ya decidió** que G1 y G4 operan sobre componentes distintos del vector, y lo decidió con evidencia: la tabla de `§1.3` mide 89% de confianza en la Marina contra 23.9% en partidos políticos. Fijar «una operacionalización única por constructo» para `confianza_institucional` no resuelve un riesgo — **deroga ADR-28.b sin nombrarlo**, y colapsa a un escalar el vector que ADR-28.b creó precisamente porque el escalar era falso y estaba medido.

El plan tiene la salida correcta ya escrita (*«si dos generadores exigen operacionalizaciones distintas, eso es hallazgo y va a mesa antes de estimar»*), pero la trata como excepción improbable cuando el canon la declara como el caso base para este constructo.

**Consecuencia sobre el apalancamiento.** *«Operacionalizar los N constructos resuelve los 15 coeficientes»* es la premisa que el plan llama *«el apalancamiento que hace la campaña viable»*. Con `confianza_institucional` desdoblado en al menos dos componentes medibles por separado (dominio para G1, justicia para G4), el trabajo de operacionalización no es de 8 unidades ni de 9, sino de **10 o más**. El plan sigue siendo más barato que calibrar 15 coeficientes uno a uno —el apalancamiento existe— pero su tamaño no es el que el documento declara.

**Nota lateral, no imputable al plan.** El plan escribe `G1` porque `milpa/procedencia.yaml:270` escribe `G1`. Pero `milpa/procedencia.yaml:39-42` declara que *«G1 se desdobla en G1a (adopción por canal personal) y G1b (difusión radial). G1b está CONTRADICHO por su propio registro […]: sus coeficientes quedan A REVISIÓN, no asignados»*, y `modelo-decision-v3_4.md:184` rotula esa fila **G1a**. El desacuerdo de rótulo es entre dos artefactos del canon, no un defecto del plan; se registra en `I-19` para que no se descubra sin explicación.

### 2.3 · «61 fuentes» no es derivable de ningún archivo del repo

**La afirmación.** `§1`: *«8 constructos × 61 fuentes»*. `§2`: *«alternativas descartadas con su razón — obligatorio, con 61 fuentes disponibles»*.

**Lo derivado.** No existe la cadena `61` con ese sentido en `data/manifiesto.yaml`, `canon/cola.yaml`, `canon/gobernanza-v1_15.md` ni `milpa/procedencia.yaml`. Los conteos reales que el repo sí sostiene:

| Conteo | Valor derivado | Cómo |
|---|---|---|
| Entradas de `data/manifiesto.yaml` | **56** | `grep -c '^- id:'` — y una de las 56 (`hitoD_fase1_ediciones_requieren_navegador`) es una nota de clasificación, no una fuente: quedan **55** |
| De esas 55, paquetes de ENNViH/MxFLS | **27** | `forense/bitacora.md:538` — *«27 paquetes […] --verifica COINCIDE en las 27»*; son componentes de tres olas de **una** encuesta, no 27 fuentes |
| Programas de encuesta distintos con payload registrado | **6** | ENCIG · ENIF · ENVIPE · ENIGH · ENNViH/MxFLS · ENCUCI |
| Documentos del corpus | **36** | 31 en `corpus/reports/` + 5 en `corpus/forense/` |

Ninguna lectura de «fuente» —entrada de manifiesto, payload, edición, programa de encuesta, documento de corpus— da 61.

**Por qué importa.** El 61 aparece dentro de una **obligación de proceso**: E0 exige *«alternativas descartadas con su razón […] con 61 fuentes disponibles»*. Una obligación de exhaustividad calibrada contra un universo que nadie derivó no se puede cumplir ni auditar, porque no se sabe contra qué se declara la exhaustividad. Es `instrucciones` v2.1 al pie de la letra: *«Ninguna cifra esperada se teclea de memoria […] un criterio de parada con una constante escrita a mano es el defecto que el criterio existe para atrapar.»*

### 2.4 · «ENSANUT — 20 archivos bajados, sin registrar. Desbloquea 4 fichas»

**La afirmación.** `§7`, bajo *«lo que corre en paralelo y no bloquea»*, en indicativo.

**Lo derivado.** Tres archivos la contradicen o no la sostienen:

- `data/manifiesto.yaml` no tiene **ninguna** entrada de ENSANUT. La única mención (`:430`) es de clasificación: *«host real es ensanut.insp.mx (INSP), NO inegi.org.mx»*.
- `data/` contiene **un solo archivo**, `manifiesto.yaml`. No existe `data/raw/`. No hay 20 archivos ni 1 en el árbol.
- `forense/notas/2026-07-30-ensanut2024-salud-post-autodirigido.md` confirma que la clasificación *«requiere navegador»* **era correcta**, inventaria **10 filas** en el componente SALUD (no 20 archivos), y cierra con una prohibición explícita: *«no replicar el POST contra este formulario sin instrucción explícita de una sesión que decida deliberadamente hacer ingeniería del formulario contra el servidor del INSP — es decisión de mesa del autor, no de sesión.»*

Lo más cercano que el repo sostiene es `forense/bitacora.md:508`: *«ENSANUT: otra sesión la está bajando por script, en curso, no se espera aquí»* — una descarga **en curso reportada por terceros**, no 20 archivos bajados. Y el número de fichas: `R4.2` es la única ficha del perímetro que el registro asocia a ENSANUT (`canon/cola.yaml:194,226`; `forense/notas/2026-07-30-ensanut2024-salud-post-autodirigido.md:37`), no cuatro.

**Por qué importa.** Es el corolario 2 de `instrucciones` v2.2 en su forma más directa: *«"no pude alcanzar la fuente" y "la fuente no tiene el dato" son hallazgos distintos […] se reportan con palabras distintas y no se colapsan nunca.»* Aquí se colapsó un tercer estado —*descarga en curso, reportada por otra sesión, sin registrar, con un mecanismo que exige visto bueno de mesa*— en *«bajados, sin registrar»*, que suena a trámite administrativo pendiente. Si alguien planifica E0 con ENSANUT como fuente disponible, planifica contra un hecho que no está en el repo.

**Además, `§7` clasifica esto como «no bloquea».** Bajo ADR-46, una sesión que registre esos 20 archivos queda inhabilitada para pre-registrar contra ENSANUT — y E1 exige que las 15 specs se escriban **antes** de abrir ninguna fuente. La descarga en curso y el pre-registro masivo compiten por la misma sesión limpia. Eso es una dependencia, no un paralelo.

---

## 3 · Afirmación no verificable: `D1`

`§6`: *«Esto tiene el mismo reloj que `D1` y es la razón para no demorarlo.»*

No existe `D1` en el repo. `canon/cola.yaml` tiene `D-01` a `D-11`; ninguna trata del reloj de indexación del repositorio público. El candidato más cercano por contenido es **ADR-44** (`canon/gobernanza-v1_15.md:8`, *«publicación del repositorio, sin registro previo»*). No se resuelve aquí: puede ser un identificador de una conversación que el repo no conoce. Se reporta como referencia colgante, no como error.

---

## 4 · Qué NO dice esta nota

- **No dictamina sobre la campaña.** Si Hito E vale la pena, si el benchmark de tres brazos es el diseño correcto, si `E0 → E4` es la secuencia adecuada: nada de eso se toca aquí. Cuatro premisas falsas no refutan un plan.
- **No corrige el plan.** El cuerpo de `forense/hitoE-campana-medicion-v2_0.md` quedó verbatim, con sus cuatro defectos dentro. Corregirlo es decisión de mesa, y `§2.1` y `§2.2` cambian números que el plan usa como puertas — eso no lo ajusta una sesión de verificación.
- **No verifica lo que el plan no presupone.** El plan declara explícitamente que **no** presupone que existan fuentes para los constructos (`§10`, punto 8) — es lo que E0 debe responder. Correcto, y no se auditó.

---

## 5 · Registro

| Defecto | Entrada de cola | Clase |
|---|---|---|
| 8 vs 9 constructos · «61 fuentes» · «15 fichas huérfanas» · rótulo G1/G1a | `I-19` | instrumento |
| `confianza_institucional` es vector de 6 (ADR-28.b) — rompe el apalancamiento y la mitigación de E2 | `D-12` | decision |
| ENSANUT «20 archivos bajados» no verificable; colisiona con ADR-46 y con E1 | `E-07` | evidencia |

**Nota de renumeración, 30/jul/2026, al fusionar con `origin/main`.** Los IDs de esta tabla se asignaron contra `78d5d54`. El PR #14 entró antes del merge y ya había tomado `I-17` e `I-18` para otros dos defectos, así que **los de esta sesión se renumeraron: `I-17` → `I-19` e `I-18` → `I-20`**; `D-12` y `E-07` no chocaron y se conservan. Se renumeran los propios, nunca los que ya están en `main` — mismo patrón que `E-04` → `E-06` (sesión de ENCUCI). Los commits `ef9ac0c` y `0c64eaa`, sus mensajes y el bloque de bitácora de esa sesión citan los IDs viejos: son historia y no se reescriben.

**Sobre «las 15 fichas huérfanas» (`§7`).** La cadena `huérfana`/`huerfana` no aparece en ningún archivo del repo. No es una afirmación falsa: es vocabulario de chat que el registro no conoce, y por eso no se puede verificar ni ejecutar. Registrado en `I-19` junto a las demás cifras no derivadas.

---

## 6 · Módulo de auditoría

**1-6.** No aplican: esta nota no afirma nada sobre México. Verifica afirmaciones de un documento sobre el estado de un repositorio.

**7 · ¿Qué conclusión sería peligrosa simplificada?** *«El plan de Hito E está mal»*. No es lo que dice esta nota. Diez de catorce premisas se sostienen, incluidas las dos que cargan la tesis del documento —que `CAL-G3` declaró la opción (b), y que no hay mapeo defendible entre efecto medido y peso asignado—. Lo que falla son conteos y un supuesto de unicidad, y dos de los cuatro tienen consecuencia operativa concreta (una puerta de decisión y una mitigación que deroga un ADR). Un plan con premisas corregibles no es un plan refutado.

**8 · ¿Qué afirmación sobre el estado del corpus no fue derivada?** Ninguna, por construcción: los conteos de `§2.3` salen de `grep -c` y `ls` corridos en esta sesión contra `78d5d54`; el de constructos, de un script sobre `milpa/procedencia.yaml:270-281` cuya salida se transcribió sin teclear el número; los veredictos de `§1` citan archivo y línea. La única cifra de esta nota que no se derivó de archivo es «catorce afirmaciones verificadas», que es el conteo de las filas que esta nota misma escribió.

**9 · (v2.2) ¿Qué deuda o restricción hereda esta nota sin verificar?** Una, declarada: acepta como cierto que `78d5d54` es el estado vigente de `origin/main` porque `git` lo reporta, sin verificar que `origin/main` no haya avanzado durante la sesión. Si otra sesión escribió al canon en paralelo, los conteos de `§2.3` pueden haber caducado — el defecto de `E-05` y `I-15`, que el repo ya conoce. Se declara en vez de asumirse.
