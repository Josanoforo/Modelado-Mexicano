> **CLASE.** Propuesta sin sello. NO es canon. No rige hasta que exista ADR.
>
> **ORIGEN.** Conversación de chat, 31/jul/2026. El argumento es tipo (3).
>
> **QUÉ DE ESTO YA ES CANON.** Nada de este documento está sellado. Su
> único punto de contacto con el canon es indirecto: el "candidato vivo"
> que propone (§ El candidato vivo) son las 39 probabilidades de regla, y
> la clase `AJUSTADO` que las tocaría si se aplicara el método sí está
> sellada por ADR-49 (D2) — ver `milpa/procedencia.yaml`. El diseño del
> método en sí (tres brazos, condiciones de uso) no ha sido sellado por
> ningún ADR.
>
> **CIFRAS SUPERADAS POR TRABAJO POSTERIOR — deriva, no copies de aquí.**
> - § El candidato vivo: *"Las 39 probabilidades de regla. Nadie las ha
>   mirado nunca"*. Superado en el mismo sentido que en
>   `forense/metodologia-identificacion-vs-ajuste-v0_1.md`:
>   `forense/cobertura-motor.md` (31/jul/2026, ya en el repo desde antes de
>   esta sesión) ya examinó las 49 reglas del motor una por una. Vigente:
>   15 de 49 reglas tienen algún valor (4 MEDIDO + 1 DERIVADO + 13 entradas
>   ASIGNADO repartidas sobre 10 reglas propias); 34 no tienen ninguno. Lo
>   que el "candidato vivo" pregunta —si esas 39 son estado disfrazado de
>   ritmo— sigue sin decidirse; lo que cambia es que ya no es cierto que
>   "nadie las ha mirado" sin más. Vigente: `forense/cobertura-motor.md`,
>   `milpa/procedencia.yaml` (`estado:`).
> - Nada más en este documento depende de una cifra del corpus que haya
>   cambiado: describe el diseño de un método (tres brazos, condiciones de
>   uso), no un conteo.

---

# Método de tres brazos — tesis, antítesis, síntesis

**Propuesta del autor, 31/jul/2026. Sin sellar. No es canon.**
Se guarda porque el diseño vale y su momento de uso todavía no llega.

---

## El defecto que ataca, y ya ocurrió tres veces

La jornada del 30-31/jul produjo tres errores de la misma familia. Ninguno fue por descuido ni por falta de rigor; los tres pasaron **una sola pasada** de clasificación o lectura, y ninguno se atrapó por añadir más verificación.

| Qué pasó | Cómo se atrapó |
|---|---|
| El cruce de Hito E emitió `SIN CANDIDATA` para `horizonte_temporal` teniendo el instrumento nombrado en el mismo archivo (`unico_calibrable_hoy`) | Una revisión independiente leyó el archivo |
| La revisión (Claude en chat) heredó `unico_calibrable_hoy` tres veces como si fuera terreno, sin verificarlo | El autor lo cuestionó |
| La premisa del cuenta propia entró como instrucción obligatoria al canon sin verificarse contra el codebook | La sesión ejecutora verificó antes de obedecer |

**Lo que los atrapó no fue rigor añadido. Fue que algo independiente miró lo mismo.** Ese es el argumento entero del método.

**Precedente propio de que funciona:** los 10 inventarios ciegos del 30/jul encontraron 119 fuentes distintas cuando el pre-registro conocía 11. Misma apuesta, resultado medido.

---

## El diseño

**Tres brazos, tres corridas cada uno, nueve salidas.**

- **Tesis** y **antítesis** reciben posiciones opuestas y con dientes, no "clasifica" y "busca fallas". Un brazo que solo revisa al otro es una auditoría con otro nombre y converge por cortesía.
- **Los brazos van ciegos entre sí.** Si el segundo lee la salida del primero, ancla, y el desacuerdo que quede es ruido, no señal.
- **La síntesis no promedia.** Entrega tres listas: acuerdo, contestado, y —lo más valioso— **qué evidencia decidiría cada contestado**.
- **El sintetizador nunca fue brazo.** Si clasificó, tiene una posición que defender.

---

## Las cuatro condiciones sin las cuales es teatro

**1 · Ciego no es sin sustrato.** Una conversación sin contexto del proyecto no sabe qué es `familismo_obligacion` ni que el Bloque A prohíbe confundir estructura con cultura. Sin Bloque A es probable que devuelva clasificaciones culturalistas — justo lo que el corpus existe para no hacer. *Ciego* = no ve la salida de los otros brazos ni la hipótesis de quien redactó. No = ignora el dominio.

**2 · Un solo paquete, derivado, commiteado, con hash.** El mismo para los tres brazos. Si quien redacta escribe tres prompts distintos, nadie puede comparar qué recibió cada brazo. El paquete lleva las definiciones derivadas del repo (no parafraseadas), lo que el modelo hace con cada elemento, las clases definidas en abstracto sin ejemplos que insinúen la respuesta, el Bloque A completo, y los riesgos declarados del propio archivo. Queda **fuera** todo lo que sospecha quien redacta. Así su sesgo no desaparece: queda inspeccionable antes de mandarlo y comparable contra lo que vuelva.

**3 · El criterio de desacuerdo va pre-registrado.** Antes de correr nada y por escrito: qué cuenta como discrepancia, con cuánta un elemento queda *contestado*, y qué se hace con los contestados. Sin esto, con nueve salidas encima de la mesa la síntesis puede justificar cualquier conclusión — post-hoc, que el Bloque C prohíbe.

**4 · Modelos distintos confunden, y se declara.** Si tres modelos discrepan, no se sabe si el objeto es indeterminado o si un modelo clasifica distinto. Tres corridas del **mismo** modelo por brazo aíslan la indeterminación del objeto; la variación **entre** modelos es otra pregunta, se reporta aparte y no se suma. Es el `CONFUNDIDO` del Bloque C aplicado al propio instrumento.

---

## Cuándo usarlo, y cuándo no

El método cuesta nueve corridas y un paquete pre-registrado. Bajo la regla de señal de v2.3, eso se paga en sesiones que no midieron. Se usa cuando **las tres** se cumplen:

- El juicio es **genuinamente contestado** — no derivable de un archivo que ya existe.
- Es **consecuente** — se propaga a muchos números o decisiones aguas abajo.
- Una sola pasada **ya falló** en algo de esta familia.

**No se usa** cuando la respuesta se deriva leyendo el repo. Ejemplo real y por eso está aquí: se propuso aplicarlo a clasificar los ~24 constructos en estado / ritmo / compuesto. Esa clasificación **ya estaba hecha por construcción del modelo** — los 90 `params_base` son niveles, los 15 coeficientes son elasticidades por definición (`procedencia.yaml`: *"un coeficiente es una ELASTICIDAD"*). Nueve corridas habrían producido, caro, lo que dan dos archivos.

---

## El candidato vivo

**Las 39 probabilidades de regla.** Nadie las ha mirado nunca: el cruce de Hito E las excluyó explícitamente por "unidad distinta". Una probabilidad de conducta dado un contexto puede ser un estado disfrazado de ritmo, y **no hay nada en el archivo que lo decida**. Cumple las tres condiciones si la derivación previa confirma que están abiertas.

Segundo candidato, más adelante: **si alguno de los 90 niveles es en realidad dinámico.** Esa pregunta toca el riesgo que `procedencia.yaml` se marca a sí mismo — con valores puntuales el modelo produce *seis clases de mexicano, la forma estadística del esencialismo que este corpus combate*.

---

## Antes de usarlo, derivar

El paso que precede a cualquier corrida: **mapear los 144 números a las tres clases desde la estructura del modelo**, y reportar cuántos pasan de *sin ruta* a *medible con dato en disco*. Es derivable, barato, no contamina, y mueve un contador.

Si el resultado deja un conjunto contestado, ahí entra el método. Si no lo deja, el método esperó y no costó nada — que es exactamente el punto.
