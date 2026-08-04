# Barrido de escritorio — siete pendientes adjudicados leyendo el repo

Sesión maestra #17 · 4/ago/2026 · verificado tipo (1) contra `main` en `6a09a37`

**Clase: acto de escritorio.** Ninguno de estos siete requirió red, microdato ni
`data/raw/`. Se resolvieron leyendo. Contadores movidos por este barrido: **cero**.
Su función es liberar decisiones y retirar pendientes falsos, no medir. Tres de
los siete resultaron ya cerrados — es decir, el programa cargaba pendientes que
no existían.

---

## 1 · Cascada de CAL-ENOE sobre `procedencia.yaml` — YA CERRADA. Retirar de la lista.

Lo que se afirmaba: que `procedencia.yaml:282-288` conserva la afirmación que
CAL-ENOE Fase A declaró falsa ("el panel de ENOE permite estimar el cambio de
conducta financiera"), porque esa nota dijo *"`procedencia.yaml` NO se toca en
esta nota: la corrección y su cascada son decisión de mesa"*.

**Verificado contra archivo: falso.** La mesa ya la ejecutó.
`milpa/procedencia.yaml:485-490` trae hoy el bloque de retiro:
*"`unico_calibrable_hoy` SE RETIRA (ADR-49, D1): la premisa de conducta
financiera vía ENOE es falsa a nivel de reactivo… Ningún coeficiente de
generador tiene ruta hoy."* Y `canon/modelo-decision-v4_0.md` §2.2 trae el
párrafo espejo (*"`unico_calibrable_hoy` se retira (ADR-49, D1)"*). No queda
ninguna afirmación falsa viva en canon por esta vía.

**Lección, y es sobre quien la escribió.** Se leyó la nota de CAL-ENOE
(31/jul) y no el archivo que describía. Es la Regla de oro al revés —
reconstruir el estado del repo desde un documento que habla de él, en vez de
mirarlo. **Acción: ninguna.**

---

## 2 · Las dos decisiones que el PR #60 dejó propuestas — VAN A MESA, con recomendación

No se editan `canon/` ni `milpa/` para estas dos: son decisiones de mesa, ya
declaradas como tales en `canon/modelo-decision-v4_0.md:396` (ADR-49 D3, la
homogeneidad de pendientes de G1a) y en la nota que abrió la clase
`exposicion_violencia` (PR #60). Se documenta la recomendación, no se sella.

### 2.a · ¿Dónde cae `exposicion_violencia` en el reparto de las 14?

El PR #60 creó la clase "reactivo declarado retirado, pendiente de localizar"
(n=1) y la marcó propuesta.

**Recomendación: sellarla, con nombre más corto y criterio explícito.** La
razón no es estética. Las otras cuatro clases responden a "¿qué tan lejos
está de medirse?"; ésta responde a "¿qué le pasó a su reactivo?" — mezcla dos
preguntas en una taxonomía. El criterio que sí las separa: la clase la
determina el **estado del reactivo**, no su historia. Con ese criterio
`exposicion_violencia` es *"sin reactivo verificado, búsqueda abierta"*,
distinta de `sens_estatus`/`aversion_riesgo` que son *"sin reactivo, búsqueda
cerrada — límite de régimen"*. Misma pregunta, dos respuestas, y el reparto
sigue cerrando 8+1+3+2.

Lo que hace falsable la distinción: una búsqueda abierta tiene un acto
pendiente que la cierra (el barrido de fuentes, la posición 4 rehecha). Si en
tres actos nadie encuentra reactivo, se reclasifica a límite de régimen. Sin
esa condición, "búsqueda abierta" es un eufemismo permanente.

### 2.b · ¿Se desdobla G1a en seis ASIGNADO nombrados?

**Recomendación: sí, desdoblar.** El pre-registro (ADR-49 D3) decía: si la
dispersión entre componentes es grande, la pendiente común queda implausible.
El `PR #58` estableció que esa dispersión no es medible en este régimen. La
lectura fácil es "sin dato, se queda como está" — es la lectura equivocada,
por una razón que el propio programa ya escribió: G4 usa
`confianza_institucional[justicia]`, componente nombrado, y `modelo:396` dice
que por eso "G4 no comparte este problema". La asimetría no está justificada
por evidencia — está justificada por comodidad de escritura.

Desdoblar no inventa información: convierte un ASIGNADO en seis ASIGNADO,
exactamente como ADR-30 hizo con familismo ("se pasa de un número inventado a
dos"). Lo que gana es falsabilidad: seis números nombrados se pueden refutar
de a uno; uno que se aplica "al componente que el dominio seleccione" no se
puede refutar nunca, porque siempre hay un componente donde encaja. Es el
mismo defecto de infalsabilidad que el Bloque A vigila en la "adaptación
racional".

⚠️ **Coste declarado, no escondido:** seis ASIGNADO empeoran la contabilidad
de `procedencia.yaml` — pasan de 1 a 6 números sin medir. Eso es correcto:
hoy el 1 oculta 6.

---

## 3 · ¿Sigue haciendo falta el Cuestionario Ampliado del CPV? — NO como semilla. Retirar de la ruta crítica.

`forense/notas/2026-07-31-cola-descarga-rederivada.md` §3(a) lo pone como
"candidata obvia para marginales de los 6 ejes de perfil".
`forense/notas/2026-07-31-p1-enigh-semilla.md` (P1) corrió después y su
veredicto es CONJUNTA COMPLETA: los seis ejes llegan a nivel persona en
ENIGH con llave de unión (`folioviv+foliohog+numren`), y la ruta IPF vive.
La semilla existe y no es el CPV.

Lo que el CPV todavía podría aportar, sin inflarlo: P1 declara un caveat de
granularidad — urbanización, ingreso y acceso digital son atributos de hogar
en ENIGH, sin varianza intra-hogar. El CPV Ampliado no arregla eso (también
es de vivienda). Queda como validación externa de marginales, no como
insumo.

**Acción tomada:** adenda en el pie de
`forense/notas/2026-07-31-cola-descarga-rederivada.md` §3(a) (ver ese
archivo) reclasificando de "bloqueo" a "deseable sin para-qué crítico". Un
bloqueo que no bloquea nada consume atención cada vez que alguien lee la
cola.

---

## 4 · ¿Qué es la familia CL del XML? — NO adjudicable de escritorio. Queda con guarda.

99 URLs, sin identificar, mismo patrón de acrónimo de tres letras que ya
produjo el error CAAS/CEU. Su descriptor (`Censo2020_CL_descriptor_bd.xlsx`)
está nombrado en el XML y no se bajó. No hay en el repo ninguna pieza que
permita decidir qué es sin abrir ese descriptor.

**Acción: no adivinar.** Se anota con la guarda explícita —no se asume qué es
un acrónimo del INEGI— y se resuelve cuando alguna sesión con red baje su
descriptor. No se le fabrica urgencia: ninguna posición de la cola lo
necesita.

---

## 5 · Triage de los "RESPONDE PERO SIN EL RECURSO" del 31/jul — dos clases distintas, colapsadas bajo un rótulo

Ver adenda fechada en el pie de
`forense/notas/2026-07-31-perimetro-descarga.md` (§8 de ese archivo). Resumen:
la tabla §5 de esa nota usa el mismo rótulo para "la fuente no lo tiene"
(ENOE 2020Q2, hueco real por contingencia sanitaria; ENOE 2026Q2+, aún no
publicado) y para "no acerté el nombre" (ENCIG 2019 `/doc/`, 9 variantes;
ENIF/ENVIPE `/doc/`, ~20 variantes). Las dos últimas ya están refutadas: el
manifiesto (`data/manifiesto.yaml`, ~l.2533) registra que esos descriptores
sí se consiguieron. Marcadas RESUELTAS en la adenda.

---

## 6 · `sens_estatus` — el veredicto es correcto, pero su fundamento no es el que parece

`forense/notas/2026-08-01-p2-momentos-atributos.md` (P2, :234, :268) lo
declara NO DETERMINABLE porque "el inventario solo trae filas sí/parcial, así
que no se puede distinguir 'no reportado' de 'no existe'".

El veredicto no dice que las fuentes no tengan el reactivo. Dice que el
inventario no permite saberlo. Es una limitación del instrumento de
catalogación, no de la realidad — y P2 es honesto al respecto: escribe "sin
ir a la fuente" y "no se colapsa a negativo".

Consecuencia práctica: `sens_estatus` está en `hitoE §14.4`, la sección de
"límite vigente" junto a `aversion_riesgo`. Pero los dos casos no son
iguales. `aversion_riesgo` tiene un candidato examinado y descartado con
argumento (ENIF `P5_23`/`P5_24` mide conocimiento de IPAB, que es moderador,
no aversión). `sens_estatus` no tiene ningún candidato examinado: nadie ha
ido a la fuente. Su desenlace sí existe (ENIGH `gastotarjetas`) y sus celdas
también.

**Acción tomada:** adenda §17 en `forense/hitoE-campana-medicion-v2_0.md`
reclasificando dentro de §14.4: `aversion_riesgo` = límite verificado.
`sens_estatus` = no examinado, y su examen es barato — lectura de descriptor,
del mismo tipo que la posición 8 paso 1. Podría ser un encargo de escritorio
más, no una medición.

---

## 7 · P2 sin corregir — corregir por adenda, no editar el cuerpo

`forense/notas/2026-08-01-p2-momentos-atributos.md:229` sigue diciendo
"(victimización, denuncia y sus razones)" y `:264` "C1 ENVIPE `BP1_20`
(victimización)". El defecto está registrado en `forense/hallazgos.md`
(04/ago/2026, vía `PR #57`) y la nota seguía sin marca.

**Recomendación aplicada: adenda fechada al pie de P2, no edición de las
filas.** Tres razones: (1) es el mecanismo que ya usaron `hitoE` §15 y §16,
así que no se inventa una vía nueva; (2) las notas forenses fechadas son el
registro de qué se sabía cuándo — editar la fila borra que el error existió;
(3) `P2:229` marca el estado **reportado**, no **verificado**, así que la
fila no mintió: dijo que venía del inventario sin verificar, y quien la usó
ignoró esa marca.

El defecto real no es de P2 — es de quien leyó *reportado* como si dijera
*verificado*. La adenda (ver pie de ese archivo) dice eso, porque es la
lección transferible: la columna de estado de una tabla es parte de la
afirmación, no decoración.

---

## Resumen de acciones

| # | Asunto | Resultado | Quién |
|---|---|---|---|
| 1 | Cascada CAL-ENOE | Ya cerrada por ADR-49 D1. Pendiente falso, retirado | — |
| 2a | Clase de `exposicion_violencia` | Sellar con criterio "estado del reactivo, no su historia" + condición de caducidad | Mesa |
| 2b | Desdoblamiento de G1a | Desdoblar: 1 ASIGNADO infalsable → 6 falsables. Coste declarado | Mesa |
| 3 | CPV Ampliado | Fuera de ruta crítica: P1 dio CONJUNTA COMPLETA con ENIGH | Acto de escritorio (hecho) |
| 4 | Familia CL | No adjudicable sin su descriptor. Sin urgencia | Cola |
| 5 | "RESPONDE PERO SIN EL RECURSO" | Dos clases colapsadas; dos filas ya vencidas | Adenda (hecha) |
| 6 | `sens_estatus` | No es límite verificado: es no examinado. Examen barato, de escritorio | Adenda (hecha) |
| 7 | Rótulo de P2 | Adenda al pie, no edición. La lección es sobre leer *reportado* | Adenda (hecha) |

Tres de siete eran pendientes que ya no existían o que nadie necesitaba (1,
3, 4). Ese es el rendimiento real de un barrido de escritorio: no mueve
contadores, pero deja de gastar sesiones en fantasmas.

## Límite de lectura declarado (ADR-46)

Esta sesión leyó: `milpa/procedencia.yaml:270-490` (por `grep`+contexto);
`canon/modelo-decision-v4_0.md` §2.2, l.396; `canon/gobernanza-v1_15.md`
(ADR-49 por `grep`); `forense/hitoE-campana-medicion-v2_0.md` completo;
`forense/notas/2026-08-01-p2-momentos-atributos.md`; `forense/notas/2026-07-31-perimetro-descarga.md`
completa; `forense/notas/2026-07-31-cola-descarga-rederivada.md` §0-§3, §5;
`forense/hallazgos.md`. Cero red, cero microdato, cero `data/raw/`. No se
tocó ningún contador. No se selló ADR-49 D3 ni la clase de
`exposicion_violencia` — ambas van a mesa (§2).
