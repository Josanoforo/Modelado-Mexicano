# MAESTRA38-CRON-3 · especificación de la huella (congelada) y desviaciones declaradas

## Ajuste de base (verificado contra el árbol, no supuesto)

El encargo asumía #558 sin fusionar (a corregir con un PR que lo sustituyera) y
#556/#557 pendientes de fusión previa (D-a). Contra el árbol real al arrancar:

- Dirección fusionó **#558 por error** antes de lanzar este acto («me equivoqué
  y merge 558, entonces toma ese PR de base para tu trabajo» — mensaje directo
  de dirección, 6/sep/2026). Este acto toma `main` (con #558 ya dentro) como
  base y corrige sus tres defectos **directamente sobre main**, en vez de abrir
  un PR que lo sustituya — no aplica la instrucción "#558 se cierra con la nota
  «superado por CRON-3»" porque #558 ya no es una rama viva que cerrar.
- #556 y #557 se fusionaron igual (D-a sigue firmada). #557 traía un conflicto
  real contra `forense/tablero/TABLERO-PROGRAMA-v1_1.md` (ambos PRs — #557 y el
  ya fusionado #558 — añadían una entrada al mismo bloque final del archivo).
  Resuelto conservando **ambas** entradas, en orden cronológico de creación
  (#557 21:21 antes de #558 21:44), sin tocar el marcador de merge huérfano
  preexistente que #557 ya había declarado como hallazgo fuera de perímetro
  (línea 976, bloque `MAESTRA38-L2-LISTA`, anterior a este acto).
  Verificación de integridad tras el merge:
  `python3 -c "...Counter(ADR)..."` → 352 entradas, máximo 352, sin duplicados,
  sin huecos.

## Desviación declarada en P1(b): qué PARO se fuerza

`PARO-RAIZ` (paso 2.5 de `tools/adquiere_cron.sh`, `descargas_mx` sin
resolver) **no detiene el script** — el propio comentario del código dice "el
resto del cron sigue", y en efecto continúa al paso 2.6, a la sonda de red y a
`claude -p`. Forzarlo renombrando `data/raices.local.yaml` (el ejemplo del
encargo) no produce `invocado=no`: produce, si todo lo demás está sano,
`invocado=si`. Verificado contra el script real antes de tocarlo, no supuesto.

Este acto usa en su lugar `data/raw` para P1(b): ese sí es un `exit 1` real
(paso 2, "corpus no montado"), anterior a `claude -p`, motivo `PARO-CORPUS`. Es
una desviación del **ejemplo** del encargo ("por ejemplo... renombrado"), no de
su intención (forzar un PARO real y verificar que la huella lo registra y lo
commitea con `invocado=no`, `commits_nuevos=0`).

## Especificación de la huella `[ADQ]` (COMMIT-1, congelada antes de tocar el script)

Línea única por corrida, escrita **al final** (tras `claude -p` o tras
cualquier `PARO`/`exit 1`), commiteada en la rama `censo/<fecha>` con su propio
commit `[ADQ] <fecha>`:

```
[ADQ] <fecha> <HH:MM>: invocado=<si|no> motivo=<-|PARO-RAIZ|PARO-RED|PARO-PROMPT|PARO-CORPUS> exit=<código|-> duracion=<s> commits_nuevos=<k> ramas_nuevas=<j> archivos_modificados=<m>
```

- `commits_nuevos` = `git rev-list --count <HEAD_ANTES>..<HEAD_DESPUES>` en el clon.
- `ramas_nuevas` = diferencia de `git ls-remote --heads origin | wc -l` antes/después.
- `archivos_modificados` = `git status --short | wc -l` tras la corrida.
- Si `invocado=no`, los tres últimos son `0` medidos (no supuestos).

`[ADQ-PDN]` (días 1-3): el re-escaneo se añade al censo y se commitea en la
misma rama con `[ADQ-PDN] <fecha>`; fuera de ventana escribe (y commitea) una
línea `[ADQ-PDN] <fecha>: fuera de ventana`.

Sello: «el primer resultado que produzca este procedimiento es el que se
reporta» — este documento no anticipa el resultado de P1, sólo el formato.
