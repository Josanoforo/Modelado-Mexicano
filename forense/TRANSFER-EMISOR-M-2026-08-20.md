# TRANSFER · dirección → SESIÓN EMISOR-M · 20/ago/2026

**Redactado por la maestra Opus contra un clon propio, `origin/main = c6fe985` (PR #302, 20/ago 16:56 −0600). Regla de lectura (v2.1): TODO lo de aquí es procedencia (3) hasta que lo re-derives del clon. Cada cifra trae su comando. Tu primer acto es §6.**

---

## §1 · Quién eres y cómo se trabaja

Eres una sesión de **diseño e implementación**, no de dirección. Tu producto no es un encargo: es **un documento de diseño verificado y, si el diseño cierra, el código**. Trabajas sobre `github.com/Josanoforo/Modelado-Mexicano`, clonas a `/home/claude/repo`, y **todo se deriva por comando** (A.4/A.5: receta probada antes de confiar; `command grep` con conteo de archivos examinados; `iconv -f utf-8 -t utf-8 -c` en salidas, el repo tiene bytes no-UTF8 que revientan pipes).

Reglas del programa que te aplican y no se negocian: ningún negativo sin universo declarado (A.4) · el fallo de un agente es hecho sobre el agente, no sobre el mundo (A.5) · ninguna cifra tecleada de memoria (v2.1) · la premisa del encargo se verifica antes de ejecutarlo, y encontrar que estaba mal fundada **es entregable, no interrupción**.

⚠️ **La advertencia que más te va a servir.** Esta dirección amplificó tres veces esta semana un negativo acotado a un negativo general —derivó un conteo, no leyó los archivos, y concluyó—. Dos de esos tres costaron una sesión completa. **Cuando un grep te devuelva un número, abre los archivos.**

---

## §2 · La tarea y el objetivo

**La tarea.** Diseñar y construir **el emisor del corredor M**: el componente que, dada una pregunta operacionalizada, produce **la respuesta que el modelo de decisión afirma** para esa pregunta, en una forma que el marcador del duelo pueda calificar.

**Por qué existe la tarea.** El programa montó un duelo entre cuatro corredores —`L` (LLM, dos variantes), `M` (el motor), `B` (baseline ingenuo), `E` (ensamble)— y construyó tres de los cuatro. **`M` no tiene forma de contestar.** El pre-registro lo asumió: `forense/prereg-duelo-v2/pipeline-L-adv1-m2.py:33` dice *«M ya vive en el motor de decisión»*. **Esa premisa es falsa y tu primer entregable es confirmarlo o refutarlo con tu propio comando.**

**El objetivo, en una frase.** Que exista un procedimiento reproducible que convierta las reglas del modelo en predicciones calificables, sin inventar números que el modelo no afirma y sin ocultar los que no puede producir.

**Lo que NO es el objetivo.** No es reescribir el modelo. No es calibrar. No es adquirir datos. No es correr el duelo. **Y no es entregar algo a medias que parezca que enlaza** — el programa ya tiene un caso así (la rebanada mínima que se leyó como «el motor») y le costó dos semanas de plan mal dirigido.

---

## §3 · Dependencias verificadas — derivadas en esta sesión, re-derívalas tú

### 3.1 · El modelo de datos del emisor **ya existe**, y para 5 reglas

`milpa/tramite.yaml` (127 líneas) trae reglas en forma ejecutable. Una completa, verbatim:

```yaml
- id: tramite.mordida.discrecional
  situacion: realiza_tramite_gobierno
  si:
    disparadores: {sancion_creible: false, quien_observa: "nadie"}
  entonces:
    - {conducta: paga_mordida,  p: 0.62, clase: ASIGNADO}
    - {conducta: tramite_normal, p: 0.38, clase: ASIGNADO}
  porque: {generador: [G1], mecanismo: "trampa social: cada quien paga porque supone que los demás pagan"}
  tier: FUERTE
  falsable_si: "Si al digitalizar y agregar testigos la mordida no baja, no es trampa social sino otra cosa"
  fuente: ["ENCIG2023", "Rothstein_trampa_social", "report:politica"]
```

**Léelo con cuidado: esa forma ya resuelve la mitad del problema.** Tiene condición (`si.disparadores`), salida con probabilidad (`entonces[].p`), clase de procedencia, tier, fuente, **y `falsable_si` en el vocabulario del programa**. No hay que inventar un esquema: hay que decidir si este se generaliza o se sustituye.

Derivado: **5 reglas** (`grep -c "^  - id:" milpa/tramite.yaml`), **11 probabilidades `clase: ASIGNADO`**.

### 3.2 · Las otras 44 reglas viven en prosa

`canon/modelo-decision-v4_0.md` declara **49 reglas SI-ENTONCES**. Solo 5 tienen forma de máquina. Las 44 restantes son texto.
⚠️ **Y hay un `49` adyacente que puede o no ser el mismo conjunto:** `milpa/refutations.yaml` tiene **49 refutaciones**. **Verifica si son las mismas 49 o dos conjuntos distintos del mismo tamaño** antes de asumir nada. Confundirlos sería el defecto de contabilidad que este programa ya pagó varias veces.

### 3.3 · El modelo afirma **puntos**, casi sin incertidumbre — y ahí está el problema de fondo

Derivado sobre `milpa/procedencia.yaml` (1 132 líneas):

```
clase:          18        n_util:  19
valor:          10        ic95:     2
ee:              0        intervalo: 1
error_estandar:  0
```

**Cero errores estándar.** El modelo dice «0.62», no «0.62 ± algo».

**Y el marcador que mesa adoptó exige distribuciones.** `ADV1-M3` puntúa contra el árbitro **como distribución** (CRPS en continuas, Brier en categóricas) y mide **calibración empírica al 80%** como resultado independiente. Un corredor que solo emite puntos no puede ser calificado por ese diseño — o se le califica como distribución degenerada, y entonces **su calibración es 0% por construcción y toda diferencia es material**, que es exactamente el defecto que `FP-83` registró para los árbitros de censo, ahora del lado del corredor.

**Esta es la pregunta central de tu diseño y está en §4.**

### 3.4 · Lo que existe como código, y lo que no

Derivado sobre los ~120 `.py` del repo (~30 000 líneas): **ningún `.py` menciona `perfil`, `disparador`, `regla`, `SI-ENTONCES` ni `simulad`.** Cero.

- `milpa/src/` — 9 módulos, 1 119 líneas. Su propio encabezado dice: *«la **rebanada mínima**… **no calibra, no estima, no produce ninguna cifra nueva**… produce para cada una un **VEREDICTO DE ESTADO, no un número**»*. Evalúa las 3 celdas-semilla de `data/curacion-registro/celdas-d/` contra los momentos `AJUSTE`.
- `tools/curador_registro/` — ~15 000 líneas de adquisición y curación. **Funciona y no es tu perímetro.**
- `tests/svystat.py` (447 líneas) — estadística de encuesta con diseño complejo. Es del lado del árbitro. **Tampoco es tuyo, pero léelo: es el estándar de calidad de código de esta casa.**

⚠️ **NO construyas desde `milpa/milpa-spec-v0_2.md`.** Lleva desde el 4/ago un banner de incompatibilidad puesto por `ADR-62(a)`: describe una arquitectura *«que `ADR-51` y `ADR-36.b` ya superaron»*. Es el mapa viejo.

### 3.5 · La arquitectura de dos niveles que la spec implementó como uno

`ADR-26`, verbatim: *«Los disparadores de contexto tienen **DOS niveles, no uno**. Siete globales + **42 palancas de dominio**, evaluadas contra `(perfil, params, d_global, d_dominio)`. El modelo siempre tuvo dos niveles; la spec implementó uno, y las palancas quedaron invisibles para el bucle.»*
**Ese ADR describe tu trabajo mejor que cualquier otro documento del repo. Empieza por ahí.**

### 3.6 · El consumidor de tu salida, ya escrito

`forense/prereg-duelo-v2/scoring-adv1-m3.py` (277 líneas) y `pipeline-L-adv1-m2.py` (296 líneas), del 20/ago. **Tu salida tiene que ser consumible por ese scoring sin modificarlo** — o, si hay que modificarlo, eso se declara como hallazgo y va a mesa, no se parchea.
También `corredor-B-tasa-base.py` y `corredor-E-combinacion-LM.py`: **`E` combina `L⊕M`, así que la forma de tu salida determina si `E` es implementable.**

### 3.7 · El marco de 60 preguntas **no tiene ninguna columna que ligue al modelo**

`forense/marco-candidatas-piloto-v1_0.tsv`, 60 filas, 17 columnas: `id · encuesta · ola · universo · variable · estimador · ponderador · escala · grado_dependencia · publicada · cv_arbitro · n_no_ponderado · frase_discriminacion · post_corte_u_ola_retenida · dominio · dificultad · estrato`.

**Todas son del árbitro. Ninguna dice qué afirma el modelo.** Se construyó una lista de preguntas que el *dato* puede contestar sin verificar que el *modelo* pueda. **Hace falta un crosswalk pregunta↔regla, y probablemente es un entregable tuyo.**
⚠️ Y mesa ya firmó que **el marco se amplía a saturación** antes de sortear, así que el crosswalk se diseña para un marco que va a crecer.

### 3.8 · Restricciones que no puedes violar

- **`ADR-68(a)`: congelamiento del motor durante el piloto.** *«El piloto NO edita reglas del motor; lo que quiera editar se anota como candidato de OLA 5.»* **Verifica si construir el emisor cuenta como editar** — si es ambiguo, es fila de mesa, no tu decisión.
- **Seis tests de motor vivos**: `test_motor_holdout.py` («EL MURO», protege el examen a libro cerrado), `test_motor_determinismo.py`, `test_motor_matriz.py`, `test_motor_clases.py`, `test_motor_procedencia.py`, `test_motor_umbrales.py`. **Los seis tienen que seguir pasando sin editarse.** Si uno falla, el diseño está mal, no el test.
- **`python3 tests/check.py --baseline` tiene que cerrar VERDE.** Hoy lo está (21 FAIL · 119 WARN contra la base congelada). **🚫 Prohibido `--freeze`.**
- **Un valor sin `clase` de procedencia no entra.** `procedencia.yaml` manda.

### 3.9 · La prueba de aceptación que ya está escrita, y es de a de veras

**`R3.4` del Hito D.** Su gate son las tres condiciones de `ADR-37`: **(A)** con `coercitivo` y `riesgo_fiscal_percibido` encendidos, la adopción tipo CoDi queda <10% del canal retail-efectivo; **(B)** al apagar `riesgo_fiscal_percibido` con el canal constante, la brecha colapsa ≥70%; **(C)** al apagar el canal de confianza personal con el riesgo encendido, la brecha persiste (reducción <30%). Pasa solo si A ∧ B ∧ C.

Derivado: **`riesgo_fiscal_percibido`, `coercitivo`, `oxxo_vs_codi`, `palanca` y `d_dominio` aparecen en 0 archivos de `milpa/src/`.** Ese interruptor no existe.

**Si tu emisor puede correr A, B y C, funciona.** Y de paso `R3.4` deja de estar bloqueada: `FP-86` la identificó como *«la única cuya desbloqueo no exige adquirir nada»*, y **mueve el contador de `Hito D`, que lleva quince días en 13/27.** Es tu criterio de éxito y tu mejor argumento.

---

## §4 · La pregunta central de diseño — resuélvela antes de escribir código

**¿Qué emite `M` cuando el modelo solo afirma un punto?**

Tres salidas, y ninguna es obviamente correcta:

1. **Punto como distribución degenerada.** Simple, y rompe el marcador: calibración 0% por construcción, toda diferencia material. Es el defecto de `FP-83` trasplantado al corredor.
2. **Incertidumbre derivada de la clase de procedencia.** `ASIGNADO` → banda ancha declarada; `MEDIDO·PARCIAL` → intermedia; `MEDIDO·NACIONAL` → el EE real de su medición. Tiene la virtud de que **la clase ya existe y está poblada** (18 valores clasificados). Tiene el riesgo de que las bandas por clase serían **inventadas**, y el diseño manda «adoptar, no inventar».
3. **`M` emite punto y se declara que no compite en calibración.** Honesto, y pierde uno de los cuatro productos del piloto.

**Ninguna la eliges tú.** Diseñas las tres con su consecuencia medida, y las subes a mesa como opciones sin aplanar. **Y si encuentras una cuarta mejor, esa es exactamente la razón por la que esta sesión existe.**

---

## §5 · Lo que esta sesión NO hace

No corre el duelo. No sortea. No toca el marco de candidatas. No adquiere datos. No edita `tools/curador_registro/`. No resuelve `ADV1-M5` — **su precedencia y su vocabulario los está trabajando dirección en paralelo, y llegarán como insumo.** No decide la pregunta de §4. No baja la línea base de la suite.

---

## §6 · Arranque de tu primera sesión

```bash
git clone https://github.com/Josanoforo/Modelado-Mexicano.git /home/claude/repo && cd /home/claude/repo
git log -1 --format="%h %ci %s"                      # compara contra c6fe985; lo de encima, derívalo
echo "CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=[${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}]"
ls data/raw/ 2>/dev/null | head -1                   # tercera parte de la firma de entorno (A.2)
timeout 900 python3 tests/check.py --baseline | tail -4

# La premisa que tienes que verificar ANTES de nada:
git ls-files "*.py" | xargs command grep -l "disparador\|SI-ENTONCES\|riesgo_fiscal_percibido" | wc -l
sed -n '1,30p' milpa/src/motor.py                    # qué dice de sí misma la rebanada mínima
sed -n '1,26p' milpa/tramite.yaml                    # el esquema que ya existe
command grep -n "ADR-26 " canon/gobernanza-v1_15.md  # los dos niveles de disparadores
```

**Si la primera premisa no se sostiene —si sí hay un emisor y esta dirección lo pasó por alto— PARA y repórtalo.** Sería el cuarto negativo mal ensanchado de la semana y saberlo vale más que el código.

**Entorno:** este trabajo es **NUBE, repo-only**. No abre microdato. Si en algún momento crees que lo necesitas, es señal de que te saliste del perímetro.
**Modelo:** Opus.

---

## §7 · Entregables, en orden

1. **Nota de verificación de premisas** — las de §3, re-derivadas con tus comandos, con lo que confirmes y lo que refutes. *Esto solo ya justifica la sesión.*
2. **Documento de diseño** — el esquema del emisor, la respuesta a §4 con sus tres opciones costeadas, el crosswalk pregunta↔regla, y **qué hacer con las 44 reglas sin forma de máquina** (¿migrar todas? ¿un subconjunto? ¿con qué criterio?).
3. **La prueba de aceptación de `R3.4`** — corriendo, o con el impedimento nombrado.
4. **El código**, si y solo si el diseño cerró y mesa firmó §4.

**Contador que esta sesión puede mover:** `Hito D 13/27 → 14/27` vía `R3.4`, si la aceptación corre. **Es el primer contador de medición que se movería en dieciséis días.**

---

## §8 · Contexto, para que no repitas nuestros errores

El programa lleva una semana de actos impecables con **cero contadores de medición movidos**. No por descuido: dos actos descubrieron que su trabajo estaba mal apuntado y lo dijeron en vez de fingir. **Uno lo apuntó mal esta dirección.**

La causa raíz es la misma tres veces: **alguien derivó una cifra parcial y completó el resto por inferencia.** «Los pobres no pagan» (un documento ya estaba en el árbol) · `LOTE-RETRIAGE` (las cinco fichas ya estaban archivadas) · «falsador no existe en el corpus» (existe en 119 archivos; el ejecutor había dicho «en estos cuatro documentos» y dirección lo ensanchó).

**El duelo entero está construido salvo un corredor, y ese corredor se llama motor.** La maquinaria de adquisición, la de medición, el corredor `L`, el `B`, el `E`, los índices, el manifiesto, el marco: todo eso costó semanas y está hecho. Lo que nunca se construyó es la pieza que traduce 49 reglas en prosa a 49 números calificables.

**Tu trabajo es esa pieza, y el criterio de que quedó bien es que `R3.4` corra.**
