# Protocolo de sesión · v1.0

### `protocolo` · **v1.0** · 29 de julio de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `protocolo-sesion-v1.0.md` |
> | **NOMBRE ESTABLE** | **`protocolo`** — cítalo así, nunca por nombre de archivo |
> | **VERIFICAS ASÍ** | §1 tiene **un** comando · §2 es la regla de R0, sin comando · §4 lista cinco prohibiciones · §5 declara la cola congelada |
>
> **Modificado el 30/jul/2026 por ADR-48 (R0)** — §2 (cierre) y §5 (cola). El número de versión no sube: esa decisión es de mesa, y R0 corta exactamente la clase de trabajo que la renumeración arrastra (retropropagación de citas). Se lee con ADR-48 al lado.

**Qué gobierna.** Cómo abre y cierra una sesión, y quién puede escribir qué en un traspaso. No gobierna rigor de contenido — eso es `instrucciones`. Existe porque el programa gastaba la primera hora de cada sesión reconstruyendo lo que la anterior ya sabía.

**El defecto que corrige, con caso.** El 29/jul, la segunda mitad de la jornada consumió tres encargos de solo-lectura antes de que algo escribiera al canon. Al cerrar, nueve hallazgos existían únicamente en una conversación de chat. Ninguno era recuperable desde el repo.

---

## 1 · Apertura — un comando, no un ritual

```
python3 tests/bitacora.py --abre
```

Imprime, todo derivado en el momento:

- HEAD, `origin/main`, si divergen, y ramas vivas
- Estado de `check.py --baseline` y de `validador_registro_ids.py`
- El último bloque de bitácora (`forense/bitacora.md`, la entrada más reciente)
- Los hallazgos que quedaron abiertos al congelar (`forense/hallazgos-congelados-2026-07-30.yaml`), agrupados por clase — registro, no cola de trabajo (§5)
- La versión de `instrucciones` vigente y su commit

Eso es la apertura completa. No se pega `estado §4`. No se re-deriva a mano lo que el script deriva. Si el script no existe todavía, escribirlo es el primer pendiente y va antes que cualquier otro trabajo.

**Primera obligación del chat, antes de opinar:** comparar la versión de `instrucciones` que reporta el script contra la que tiene en contexto. Si no coinciden, decirlo y detenerse. El 29/jul el chat operó una jornada entera sin dos reglas por no hacer esta comparación.

---

## 2 · Cierre — la regla de R0

**Cada sesión produce una medición o produce nada.**

- **Defecto que no impide medir:** una línea en `forense/hallazgos.md` y sigue. No abre entrada, no abre ADR, no abre discusión.
- **Defecto que impide medir:** para y reporta. Eso es el reporte entero.

Eso es el cierre completo. No hay auditoría por escrito, no hay módulo de proceso, no hay bloque derivado obligatorio.

**Qué desapareció y por qué.** Hasta el 30/jul/2026 este parágrafo obligaba a `python3 tests/bitacora.py --cierra` y a un bloque derivado de once campos anexado a `forense/bitacora.md`. ADR-48 (R0) lo apaga: el aparato de auditoría consumía el trabajo que decía vigilar, y el propio derivador acumuló tres defectos registrados sin que nadie leyera su salida. El script sigue en el árbol con su marca de apagado; `--cierra` no se invoca desde ningún lado. `forense/bitacora.md` queda como está — append-only, no se reescribe, no se le anexa más.

**Lo que no cambia:** una sesión que no termina en commit no dejó nada. Si se acaba el tiempo, se comitea lo que haya. Un hallazgo en una conversación no es un hallazgo del programa.

---

## 3 · El traspaso se parte por procedencia

Dos documentos, no uno. El defecto del TRANSFER-8 —siete premisas falsas— vino de mezclarlos.

**Parte derivada.** La escribe CC, sale de `bitacora.py`. Estado, commits, suites, cola, versiones. Tipo (1). No la toca el chat.

**Parte de dirección.** La escribe el chat. Una página, máximo. Prioridades, decisiones de mesa tomadas, qué no se re-litiga, en qué orden. Encabezado obligatorio: tipo (3), se lee como pregunta.

**Prohibición explícita:** el chat no escribe hechos sobre el repo en un traspaso. Ni conteos, ni números de línea, ni nombres de archivo como si los hubiera visto, ni "el estado es X". Si necesita afirmarlo, lo formula como pregunta a verificar. El chat es un generador de sospechas falsables, no una fuente — el 29/jul emitió seis hipótesis sobre el repo y las seis cayeron contra archivo.

---

## 4 · Cinco prohibiciones

1. **No se abre trabajo de evidencia y de instrumento en la misma sesión.** Los hallazgos de instrumento van a `forense/hallazgos.md`, una línea, no al turno (§2 · §5).

2. **No se congela una línea base en la misma corrida que cambió el medidor.** Primero se ve el efecto sin `--baseline`, luego se decide. (`015af3a` lo hizo y su `head` no identifica el código que produjo sus conteos.)

3. **No se declara una cifra que un test vigila sin derivarla de la salida de ese test.** Y ojo: algunos tests miden antes de emitir su propio veredicto — el número a declarar es el que el test reporta, no el total de la corrida. (T16: escribir el total lo hace fallar para siempre.)

4. **No se edita un pre-registro.** Adenda fechada o veredicto. (El alcance exacto de esta protección quedó sin decidir: `D-01`, congelada en `forense/hallazgos-congelados-2026-07-30.yaml`.)

5. **`accept edits` apagado en toda sesión que escriba al canon.** Anula la confirmación de ediciones pero no la regla `ask` de `git commit`: auto mode puede escribir un artefacto y no poder sellarlo.

---

## 5 · La cola está congelada

**No hay cola.** `canon/cola.yaml` se congeló el 30/jul/2026 como `forense/hallazgos-congelados-2026-07-30.yaml` (ADR-48, R0). Ese archivo es registro: no rige, no bloquea, no ordena prioridades, **y no se le añaden entradas** — ni una. Tampoco se borra: lo citan por ID commits, cuerpos de PR y bloques de `forense/bitacora.md`.

**Dónde va un defecto nuevo.** A `forense/hallazgos.md`, una línea, bajo la regla de §2. Si impide medir, no va a ningún archivo: se para y se reporta.

**Convención de IDs**, para cuando algo necesite uno (declarada en `gobernanza` junto a ADR-48, cierra I-13): `D-AAAAMMDD-HHMM` con la fecha y hora UTC de apertura, o un hash corto. Nunca un correlativo derivado de contar el archivo — eso es lo que hizo colisionar `E-04` entre dos ramas ciegas entre sí. Los IDs correlativos ya asignados son historia y no se renumeran.

---

## 6 · Qué se responde en la apertura y qué no

**Se responde con el script:** en qué estado está el repo, qué hizo la última sesión, qué está abierto, qué versión de las reglas rige.

**No se responde nunca en la apertura:** por qué se decidió algo. Eso vive en `gobernanza` y se consulta cuando se necesita, no se recita al empezar. Recitar el porqué de las decisiones pasadas en cada apertura es la mitad del costo que este protocolo existe para eliminar.
