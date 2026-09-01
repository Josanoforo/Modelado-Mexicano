---
description: Corre tools/emite_m.py -- regresion P2 contra M-TRA-M-01/02 y, si PASA, emite M-<id>.json para toda celda elegible del sorteado vigente con regla cargada y sin json previo. Uso — /emite-m
argument-hint: (sin argumentos)
---

# `/emite-m` — emite, no puntúa

Creada por `ACTO MAESTRA33-E6 · EMISOR-M-1` (1/sep/2026). Ejecuta
`tools/emite_m.py` sobre `forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv`
(columna `elegible_v1_1=='SI'`). Sin argumentos: el tool no acepta ruta de
marco por ahora — es especifico a v1_1, mismo patrón que
`sorteo_marco_m_v1_1.py` fue especifico a v1_1 en vez de generico (ADR-178).
Si algún día hay un `marco-M-sorteado-v1_2.tsv`, esta skill necesita que
alguien primero extienda `tools/emite_m.py` con las constantes de esa
versión — no asume que "caminatas futuras" significa que el tool de hoy ya
las sabe caminar.

## 1 · Arranque mínimo

Si esta invocación corre dentro de un `/acto` que ya hizo su propio
ARRANQUE, no lo repitas. Si corre sola: `ls tools/emite_m.py` — si falta,
PARA. No toca `data/raw`, no toca red: todo lo que lee es texto ya en el
repo (`milpa/tramite.yaml`, los dos `marco-M-sorteado-*.tsv`,
`candidatos-marco-M-v1_1.tsv`, `corridas-M/*.json`).

CIEGO: esta skill jamás abre `forense/prereg-duelo-v2/corridas-R/`. El tool
mismo lo verifica y lista, al final de su salida, cada archivo que sí abrió
— esa lista es la que se copia a la nota de cierre, no se resume a mano.

## 2 · Corre el tool

```
python3 tools/emite_m.py
```

Sale por dos fases, en este orden:

**Fase P2 (regresión).** Re-deriva `M-TRA-M-01.json`/`M-TRA-M-02.json` desde
`marco-M-sorteado-v1_0.tsv` y compara campo por campo contra lo ya
comiteado. Por campo, tres veredictos posibles:

- `OK` — byte a byte igual.
- `exento` — solo el campo `fuente` (cita el acto+fecha que corre; distinto
  por construcción entre la emisión original y cualquier regresión
  posterior).
- `DIVERGE EN REDACCION` — solo `correcciones_aplicadas_por_referencia`
  cuando sí hubo corrección (caso `TRA-M-02`): el *valor* corregido se
  verifica en los campos `variable`/`ponderador` (esos si son `OK` a
  fuerza), la prosa que lo explica es compuesta a mano en el original y no
  se fuerza a coincidir letra por letra (ver docstring de
  `tools/emite_m.py`).
- `FALLA` — cualquier otro desacuerdo. Esto es lo que P2 vino a atrapar.

Si aparece un `FALLA`, el tool termina con código de salida 1 y **no
escribe ningún archivo nuevo** — es el `PARO-reporta, sin ajustar` del
encargo original. No edites `tools/emite_m.py` para forzar el match sin
antes entender POR QUÉ cambió: la regresión existe para que un cambio real
de lógica (no de redacción) se note antes de tocar `corridas-M/`.

**Fase P1/P3 (caminata).** Solo corre si P2 PASA. Por cada fila elegible
del sorteado vigente imprime uno de:

- `EMITIDO` — regla cargada, sin json previo, `M-<id>.json` recién escrito.
- `YA-EXISTIA` — ya había `corridas-M/M-<id>.json`; no se toca (no se
  re-emite, no se compara contra lo existente — eso es tarea de P2, no de
  esta fase).
- `SIN-REGLA` — la celda no tiene `regla` cargada en `milpa/tramite.yaml`
  (o la columna viene vacía). Esto es la fila "sin regla" que el encargo
  pide declarar, no inventar — cópiala tal cual a la nota de cierre.
- `NO-ELEGIBLE-V1_1` — `elegible_v1_1 != 'SI'`; no se toca.

## 3 · Commit

Un commit con `tools/emite_m.py` (si cambió) + los `corridas-M/*.json`
**nuevos** que la corrida haya escrito — nunca archivos `YA-EXISTIA`, esos
no cambiaron. El mensaje de commit cita, para cada `id` `EMITIDO`:
`regla`, `p`/`valor_punto`, `grado_DD`. Si hubo filas `SIN-REGLA`,
decláralas en el mensaje o en la nota de cierre — no se emite un valor por
esa fila bajo ninguna circunstancia.

## 4 · Al cerrar

Copia a la nota de cierre la lista de "archivos abiertos" que el tool
imprime al final (CIEGO a R, A.13: la lista sale del propio comando, no se
reescribe a mano). Si el sorteo vigente trae una fila con `estrato`
`tramite|P1|MEDIA` sin asiento (hallazgo de `FP-213`/`ADR-248`), esa fila
es informativa para la caminata M — no cambia ningún paso de esta skill,
pero la nota de cierre del acto que invoque `/emite-m` la declara si
aplica.

## Lo que esta skill no hace

No carga ni sella reglas nuevas en `milpa/tramite.yaml` — si una celda cae
`SIN-REGLA`, la respuesta es declarar, nunca editar `tramite.yaml` desde
aquí. No abre ni pondera `corridas-R/` — CIEGO, sin excepción. No decide
`grado_DD` por juicio: es la fórmula F-DD (`ADR-237`) aplicada mecánicamente
por `tools/emite_m.py`, nunca a ojo. No sortea celdas nuevas — eso es
`/arbitra`-adyacente pero para R, y para M es el mecanismo de
`sorteo_marco_m_v1_1.py`, fuera de esta skill.
