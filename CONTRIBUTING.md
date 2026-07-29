# Protocolo de cambio

Este repo no es un almacén de documentos: es el aparato de falsación de un
modelo de decisión. Las reglas de abajo salen de defectos reales, cada una
con su ADR.

## 1 · Antes de tocar nada

```bash
python3 tests/check.py          # ¿de qué estado partes?
```

Si algo ya falla, **decláralo en el PR**. Un cambio que "arregla" un test
sin haberlo visto fallar antes no está verificado.

## 2 · Nomenclatura  *(ADR-36)*

`<nombre-estable>-v<MAYOR>.<MENOR>.md` — MAYOR cambia con estructura o
alcance; MENOR con contenido.

**Las referencias internas citan el NOMBRE ESTABLE, nunca el nombre de
archivo.** `ver modelo §3.B`, no `ver modelo-decision-v3.2.md`. Así las
versiones suben sin dejar referencias colgando.

Cada archivo canónico abre con:

> **ARCHIVO** · **REEMPLAZA A** (borrar) · **VERIFICAS ASÍ** · **NOMBRE ESTABLE**

## 3 · Append-only: lo que NUNCA se reescribe

`corpus/reports/` · `corpus/forense/` · `forense/`

Son evidencia fechada. Reescribir un artefacto forense para que cuadre con
el estado posterior **es la racionalización post-hoc que el Bloque C
prohíbe**. Se corrigen con nota fechada, nunca en silencio.

## 4 · Retropropagación  *(ADR-29.a · ADR-32.a)*

Un caso **no se marca aplicado sin `grep` verificado contra el report dueño**.
El artefacto que debe existir es la **nota de corrección fechada en la fuente**.

⚠️ **Cinco de cinco afirmaciones de estado comprobadas resultaron falsas.**
Ninguna se da por buena sin verificar.

**Prohibido el cuantificador absoluto** en una afirmación de estado —
*"las únicas"*, *"todas"*, *"exhaustivo"*. `T11` lo rechaza. Nació de un
parche que declaraba tres ediciones "las únicas" y dejaba diez sin marcar.

## 5 · Tiers  *(ADR-02)*

Los tiers **se LEEN** del glosario y de los mapas de evidencia. **No se
reconstruyen.** Si un tier no está a la vista, ve a buscarlo antes de
afirmarlo.

Toda regla del motor cuyo `PORQUE` nombre un constructo debe tener ese
constructo **en el glosario**. `T05` lo rechaza.

## 6 · Procedencia

**(a)** dato EN México · **(b)** muestra de diáspora — *no es evidencia sobre
M�xico* · **(c)** marco importado.

**La marca VIAJA** con el constructo a cualquier dominio. Un marco **(c)**
no puede usarse como **causa**: `T09` lo rechaza.

## 7 · Búsqueda  *(ADR-38)*

Las consultas **se pre-registran** con el falsador. Toda corrida incluye al
menos una consulta **ADVERSARIA**, redactada para encontrar el caso que
tumbaría el veredicto — **se evalúa por su sintaxis, no por la declaración
de intención de quien la escribió**.

**Log de búsqueda obligatorio** o el veredicto no se archiva.

## 8 · Todo principio nuevo nace con su test  *(ADR-32)*

> Si escribes un principio y no le das un artefacto que **falte visiblemente**
> cuando no se cumple, no obliga a nada.

Es el patrón que explica casi todos los fallos del programa. Un ADR sin test
en `tests/check.py` es un ADR decorativo.
