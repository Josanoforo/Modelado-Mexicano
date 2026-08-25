# Elección ciega pre-registrada — Paso 2 de `FP-149` (`ADR-173`, opción d)

**Encargo:** `forense/encargos/2026-08-25-ESCALAS-P2.md` (archivado al cierre de este acto). **Entorno:** NUBE, sesión fresca — sin lectura de `forense/registro-llaves-identificacion-v1_0.md`, ningún archivo `CAL-G3`, la sección de llaves de `canon/estado-programa-v1_10.md`, ni el término del β medido. **Firma:** ninguna nueva — ejecuta el verbatim ya sellado en `ADR-173`/`FP-149`: *"(2) elección ciega pre-registrada solo para el residuo subdeterminado, con higiene de contexto tipo R10.1"*.

**Insumo de partida:** el extracto por comando de `forense/notas/2026-08-25-escalas-p1.md` §3 (comando: `awk '/^## 3 ·/{flag=1} /^## 4 ·/{flag=0} flag' forense/notas/2026-08-25-escalas-p1.md`), que deja la partición de las 15 `SUBDETERMINADA` en: **7 con un extremo (θ) ya en mano** — `G1.confianza_institucional`, `G1.radio_confianza`, `G3.familismo_apoyo`, `G4.exposicion_violencia`, `G4.confianza_institucional`, `G5.familismo_apoyo`, `G5.radio_confianza` — y **8 sin ningún extremo declarado** — `G2.sens_estatus`, `G2.aversion_riesgo`, `G3.horizonte_temporal`, `G3.aversion_riesgo`, `G4.horizonte_temporal`, `G4.sens_estatus`, `G5.familismo_obligacion`, `G6.deferencia`.

## 1 · Qué se fija en cada clase

- **(a) Las 7 con θ en mano:** se fija SOLO el extremo del generador (la escala/forma de su salida). El extremo θ ya está resuelto por medición pre-existente (Paso 1/`ADR-174`) y no se toca aquí.
- **(a) Las 8 sin ningún extremo:** se necesitan AMBOS extremos — el de θ y el del generador. Si el procedimiento de la sección 2 no puede fijar los dos con las fuentes admitidas, la fila queda `SUBDETERMINADA-PERSISTENTE` (sección 3).

## 2 · Criterios admisibles, en el orden en que se aplican

Para cada extremo por resolver, en este orden, el primero que produzca una respuesta cierra la fila (regla de la casa: el primer resultado que produce el procedimiento es el que se reporta, sin comparar contra otras corridas posibles):

1. **Unidad natural de la θ en su fuente pre-medición.** Si la θ tiene una fuente pre-medición declarada (`milpa/procedencia.yaml`, secciones `condicionales_escalares*`/`condicionales_confianza_institucional`), su unidad ya está fijada ahí (proporción ponderada, dicotomizada, IC95% por diseño complejo) — se cita esa unidad, no se re-deriva.
2. **Naturaleza declarada de la salida del generador** (`canon/modelo-decision-v4_0.md` §2, cláusula falsable). Si la cláusula falsable de un generador declara explícitamente una escala o unidad numérica para su salida, se usa esa.
3. **Convenciones ya selladas del modelo** — proporciones en `[0,1]`, diferencias en puntos porcentuales, índices ya declarados en otra parte del canon. Se aplica solo cuando (1) y (2) no producen nada, y solo si la convención tiene un ancla concreta y ya existente en el documento (no una convención inventada para esta ocasión).

**Criterio prohibido — declarado, no aplicado en ningún paso:** elegir una forma "porque ajusta/reconcilia con algo medido". Ninguna fuente post-24/ago/2026 ni ningún β de `CAL-G3` entra en esta sección ni en la siguiente. Si en algún punto de la ejecución esta sesión se sorprende razonando hacia un dato medido, para y lo declara — esa sesión queda quemada para este acto.

## 3 · Qué cuenta como `SUBDETERMINADA-PERSISTENTE`

Una fila queda `SUBDETERMINADA-PERSISTENTE` cuando, agotados los tres criterios de la sección 2 para el/los extremo(s) que le faltan, ninguno produce una unidad o escala concreta — es decir, cuando ni la θ tiene fuente pre-medición propia, ni la cláusula falsable del generador declara una escala numérica, ni existe ya en el canon una convención sellada con ancla propia aplicable a esa variable específica. **Persistente no es "no se buscó" — es "se buscó con los tres criterios y ninguno ancla".** No se inventa una escala por default para cerrar el hueco: la ausencia de base dimensional se declara como resultado, no como falla del procedimiento.

**Cierre de la regla:** el primer resultado que produzca este procedimiento, aplicado en el orden de la sección 2 a cada una de las 15 filas, es el que se reporta en `forense/escalas-eleccion-ciega-v1_0.md` §2 (commit 2) y se propaga a `milpa/procedencia.yaml`. No hay una segunda pasada que reconsidere una elección ya hecha.
