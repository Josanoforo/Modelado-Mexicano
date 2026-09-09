ENTORNO: CAJA

<!--
CORRECCIÓN REGISTRADA, 9/sep/2026, por `ACTO GEN2-SONDA-ADQ-CABLEADO`
(P2/H3, `forense/encargos/2026-09-09-GEN2-SONDA-ADQ-CABLEADO.md`).

Este encargo estaba `LISTO-CAJA` desde el 8/sep y declaraba su entorno solo
en prosa Markdown (`**Entorno asignado:** CAJA/Ubuntu…`). `/despacha` lista
los pendientes de caja con el comando literal
`git show "origin/main:$f" | grep -q '^ENTORNO: CAJA'`
(`.claude/commands/despacha.md`:479), que sobre este archivo devolvía CERO
coincidencias: la compuerta estaba satisfecha y el trabajo estaba listo,
pero el anuncio de «esperando caja» no lo incluía — trabajo preparado que no
llegaba a quien debe ejecutarlo.

Lo ÚNICO que cambia es la cabecera canónica de la primera línea y este
bloque. El texto original de abajo no se edita, no se re-redacta el piloto y
no se crea otro: es el mismo encargo, ahora visible.

Deuda vigente: se reutiliza `NC-0060` (ABIERTA, `forense/no-corrido.tsv:61`,
sucesor `GEN2-SONDA-3-PILOTO-CAJA`) — no se abre una deuda gemela. El número
candidato que menciona el cuerpo histórico del `PR #642` NO es el id vigente
y no se copia como tal.

Este acto NO ejecuta el piloto: es NUBE, y el piloto exige CAJA con corpus y
red real.
-->

# ENCARGO · ACTO GEN2-SONDA-3-PILOTO-CAJA · EJERCITA-SONDA-LATERAL-SOBRE-NEGATIVO-REAL

ESTADO: LISTO-CAJA — compuerta re-derivada por `ACTO GEN2-CIERRES-CON-CITA` (9/sep/2026): `GEN2-SONDA-3 · ESCALAMIENTO-LATERAL` fusionó como `PR #642` (`git log --all --oneline --grep="pull request #642"` → `c5b89a9`); `git cat-file -e origin/main:.claude/commands/sonda.md` existe y `git show origin/main:.claude/commands/sonda.md | grep -c "Segunda pasada crítica"` → `1` (≥1 exigido). Compuerta CUMPLIDA. Entorno asignado es CAJA/Ubuntu (no nube): `/despacha` no lo ejecuta, pero ahora puede nombrarlo como ejecutable para la próxima sesión de caja.
BITACORA:
- 2026-09-09 · LISTO-CAJA · esta línea no existía (fila sin `ESTADO:` reconocible por `/despacha`, solo un `**Estado:** VIVO` de prosa); añadida por `ACTO GEN2-CIERRES-CON-CITA` tras re-derivar la compuerta contra `origin/main` real.

**SHA de redacción:** contra `origin/main` al momento en que se fusione `ACTO GEN2-SONDA-3 · ESCALAMIENTO-LATERAL` — este encargo se redacta antes de conocer ese SHA (el acto que lo escribe deja escrito el mecanismo de derivación, no un SHA que todavía no existe).
**Entorno asignado:** CAJA/Ubuntu con corpus (`data/raw`) montado y red real. Explícitamente NO nube — el piloto ejercita adquisición/verificación de vías laterales, que exige red hacia fuentes externas.
**Estado:** VIVO

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2)

- `.claude/commands/sonda.md` con §5-bis (segunda pasada crítica) y §8
  (advertencias Deep Research) → debe existir tras el merge de
  `GEN2-SONDA-3 · ESCALAMIENTO-LATERAL`.
- `.claude/commands/adquiere.md` con §6-bis (`SONDA-LATERAL-RECOMENDADA`) →
  ídem.
- `data/curacion-registro/cola-adquisicion-registro.tsv` → existe, 138 filas
  a la fecha de redacción de este sucesor.

## COMPUERTA

**GATED a `GEN2-SONDA-3 · ESCALAMIENTO-LATERAL`** — verificar por producto
contra `origin/main` real, antes de cualquier paso sustantivo:
`git cat-file -e origin/main:.claude/commands/sonda.md` y comprobar que el
contenido trae la cadena `5-bis · Segunda pasada crítica` (`git show
origin/main:.claude/commands/sonda.md | grep -c "Segunda pasada crítica"` →
`≥1`). Un `grep --oneline` de mensajes de commit por el rótulo queda como
indicio, no como prueba (mismo criterio que `acto.md §2.2`). Si la compuerta
no se cumple: cero commits, reporta y termina.

## Objetivo

Ejercitar `/sonda` (con su nuevo §5-bis/§8) y `/adquiere` (con su nuevo
§6-bis) sobre un negativo material REAL de la cola vigente — no un ejemplo
fabricado — para que el primer uso del criterio nuevo sea evidencia, no
demostración de escritorio.

## Selección del negativo material — por derivación, no por dedo

Comando sobre la cola vigente (`data/curacion-registro/cola-adquisicion-registro.tsv`),
filtrando `NO-ENCONTRADO` / `OBTENIDO-PARCIAL` con faltante material /
`NO-OBTENIDO-POR-ESTE-AGENTE`, **excluyendo explícitamente** cualquier fila
cuya `fuente_canonica`/`nota` mencione `RUPC` (ya usado como demostración en
`SONDA-CAJA-1`/`#635` — no se re-descarga por segunda vez sólo para volver a
demostrar el mecanismo):

```
python3 - <<'PYEOF'
import csv
with open('data/curacion-registro/cola-adquisicion-registro.tsv') as f:
    r = csv.DictReader(f, delimiter='\t')
    for row in r:
        st = row['estado_A4A5']
        if 'RUPC' in st or 'RUPC' in row.get('nota', '') or 'RUPC' in row['fuente_canonica']:
            continue
        if st.startswith('NO-ENCONTRADO') or st.startswith('OBTENIDO-PARCIAL') or st.startswith('NO-OBTENIDO-POR-ESTE-AGENTE'):
            print(st, '|', row['fila_origen'] or row['fuente_canonica'], '|', row['fuente_canonica'])
PYEOF
```

A la fecha de redacción de este sucesor, ese comando produce (entre otras)
candidatas como `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` (`NO-ENCONTRADO`),
`DD_COMPRANET_DICCIONARIOS_DE_DATOS` (`NO-OBTENIDO-POR-ESTE-AGENTE(4
rutas)`), `ENAFIN` y `ENSAFI_TANDAS_PARTICIPACION_R8_2_N29`
(`OBTENIDO-PARCIAL`) — el piloto vuelve a correr el comando al arrancar
(la cola pudo moverse) y selecciona de la salida real de ESE momento, no de
esta lista congelada.

**Cruce contra consumidores vigentes**, antes de elegir cuál fila trabajar:
`grep` de la `fuente_canonica`/`fila_origen` candidata contra
`data/curacion-registro/relaciones.tsv` y contra
`data/curacion-registro/necesidad-objeto-modelo.tsv` — prioriza la candidata
con consumidor real (una necesidad/objeto del modelo que la cita), sobre una
sin consumidor conocido. Si ninguna de las filtradas tiene consumidor
vigente, decláralo y elige por prioridad de cola (`prioridad`, ascendente).

## Presupuesto explícito

Máximo **90 minutos** de sondeo activo (`/sonda`, modo `LATERAL` — la ruta
principal ya falló) sobre UNA sola fila elegida por el mecanismo de arriba,
más el tiempo de `/adquiere` si `/sonda` entrega una candidata con handoff.
Si el presupuesto se agota sin resolver: se declara el límite (no se
presenta el universo como agotado) y se cierra con negativo mejor acotado.

## Finales válidos — uno de tres, nunca una adquisición fabricada

1. **Dato recuperado** — `/adquiere` corrió sobre la candidata que `/sonda`
   entregó y la fila pasa a `OBTENIDO`/`OBTENIDO-PARCIAL` con completitud
   declarada (§6-bis).
2. **Ruta verificada** — `/sonda` localizó una vía legítima pero no se
   pudo/no dio tiempo completar la descarga en este piloto: handoff a
   `/adquiere` queda registrado en la nota de la fila, `PENDIENTE`/`SIN-FETCH`
   con receta ≤1 minuto si aplica.
3. **Negativo mejor acotado** — `/sonda §5` corrió completo (segunda pasada
   crítica de `§5-bis` incluida) y el negativo declara universo adicional
   agotado, con frontera explícita de lo que NO se examinó.

No se fabrica una adquisición para cumplir un final: si la fila elegida no
rinde ninguno de los tres dentro del presupuesto, se cierra en (3) con lo que
el presupuesto alcanzó.

## Perímetro

La fila elegida en `data/curacion-registro/cola-adquisicion-registro.tsv` +
`data/cola-adquisicion-v1_0.tsv` (regenerada, nunca a mano) + `data/manifiesto.yaml`
si hay `OBTENIDO` + nota de cierre del piloto + cascada estándar. Prohibido:
tocar otras filas de la cola, adoptar ningún resultado en `milpa/**`, abrir
una segunda cola.
