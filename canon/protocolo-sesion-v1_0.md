# Protocolo de sesión · v1.0

### `protocolo` · **v1.0** · 29 de julio de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `protocolo-sesion-v1.0.md` |
> | **NOMBRE ESTABLE** | **`protocolo`** — cítalo así, nunca por nombre de archivo |
> | **VERIFICAS ASÍ** | §1 tiene **dos** comandos · §4 lista cinco prohibiciones · §5 define el esquema de la cola |

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
- La cola abierta (`canon/cola.yaml`), agrupada por clase
- La versión de `instrucciones` vigente y su commit

Eso es la apertura completa. No se pega `estado §4`. No se re-deriva a mano lo que el script deriva. Si el script no existe todavía, escribirlo es el primer pendiente y va antes que cualquier otro trabajo.

**Primera obligación del chat, antes de opinar:** comparar la versión de `instrucciones` que reporta el script contra la que tiene en contexto. Si no coinciden, decirlo y detenerse. El 29/jul el chat operó una jornada entera sin dos reglas por no hacer esta comparación.

---

## 2 · Cierre — obligatorio, no opcional

```
python3 tests/bitacora.py --cierra
```

Anexa a `forense/bitacora.md` un bloque derivado, nunca escrito a mano:

- Fecha, HEAD inicial y final, rama usada
- Commits de la sesión: hash, autor, co-autor, asunto
- Archivos tocados
- ADRs añadidos, versiones subidas
- Delta de suite: FAIL/WARN antes y después
- IDs de cola abiertos y cerrados en la sesión

Lo único que se escribe a mano en ese bloque son dos líneas: **qué se decidió** y **qué quedó bloqueado**. Todo lo demás lo deriva el script o no entra.

**Regla dura:** una sesión que no termina en commit no dejó nada. Si se acaba el tiempo, se comitea lo que haya con el bloque de bitácora. Un hallazgo en una conversación no es un hallazgo del programa.

---

## 3 · El traspaso se parte por procedencia

Dos documentos, no uno. El defecto del TRANSFER-8 —siete premisas falsas— vino de mezclarlos.

**Parte derivada.** La escribe CC, sale de `bitacora.py`. Estado, commits, suites, cola, versiones. Tipo (1). No la toca el chat.

**Parte de dirección.** La escribe el chat. Una página, máximo. Prioridades, decisiones de mesa tomadas, qué no se re-litiga, en qué orden. Encabezado obligatorio: tipo (3), se lee como pregunta.

**Prohibición explícita:** el chat no escribe hechos sobre el repo en un traspaso. Ni conteos, ni números de línea, ni nombres de archivo como si los hubiera visto, ni "el estado es X". Si necesita afirmarlo, lo formula como pregunta a verificar. El chat es un generador de sospechas falsables, no una fuente — el 29/jul emitió seis hipótesis sobre el repo y las seis cayeron contra archivo.

---

## 4 · Cinco prohibiciones

1. **No se abre trabajo de evidencia y de instrumento en la misma sesión.** Los hallazgos de instrumento van a la cola, no al turno.

2. **No se congela una línea base en la misma corrida que cambió el medidor.** Primero se ve el efecto sin `--baseline`, luego se decide. (`015af3a` lo hizo y su `head` no identifica el código que produjo sus conteos.)

3. **No se declara una cifra que un test vigila sin derivarla de la salida de ese test.** Y ojo: algunos tests miden antes de emitir su propio veredicto — el número a declarar es el que el test reporta, no el total de la corrida. (T16: escribir el total lo hace fallar para siempre.)

4. **No se edita un pre-registro.** Adenda fechada o veredicto. (El alcance exacto de esta protección es una decisión abierta: ver la cola.)

5. **`accept edits` apagado en toda sesión que escriba al canon.** Anula la confirmación de ediciones pero no la regla `ask` de `git commit`: auto mode puede escribir un artefacto y no poder sellarlo.

---

## 5 · La cola tiene IDs y vive en un archivo

`canon/cola.yaml`. Una entrada por pendiente. El chat puede proponer entradas; solo CC las escribe.

```yaml
- id: I-01                      # I instrumento · C canon · E evidencia · D decisión
  titulo: "T03 no puede marcar una cita ilustrativa"
  clase: instrumento
  abierto: 2026-07-29
  casos: 3                      # cuántas veces se ha manifestado
  bloquea: []                   # IDs que no avanzan sin esto
  evidencia: "forense/bitacora.md#2026-07-29"
  estado: abierto               # abierto · en_curso · cerrado · descartado
```

**Reglas de la cola.** Un pendiente sin ID no existe. Se cierra con referencia al commit que lo cierra. `casos` sube cuando reaparece — un defecto que se manifiesta tres veces tiene prioridad sobre uno que se manifestó una vez, y eso deja de ser impresión y pasa a ser un campo.

---

## 6 · Qué se responde en la apertura y qué no

**Se responde con el script:** en qué estado está el repo, qué hizo la última sesión, qué está abierto, qué versión de las reglas rige.

**No se responde nunca en la apertura:** por qué se decidió algo. Eso vive en `gobernanza` y se consulta cuando se necesita, no se recita al empezar. Recitar el porqué de las decisiones pasadas en cada apertura es la mitad del costo que este protocolo existe para eliminar.
