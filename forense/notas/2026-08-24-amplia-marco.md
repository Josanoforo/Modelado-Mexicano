# ACTO AMPLIA-MARCO-SATURA — nota de cierre (24/ago/2026)

Encargo: `forense/encargos/2026-08-24-AMPLIA-MARCO-SATURA.md`. Firma que ejecuta:
`ADR-135(d)`, verbatim: *"Se amplía a saturación para eso creamos una
infraestructura completa en CODEX, no para desperdiciarla."*

**Resultado: PARO.** El marco NO se amplía en este acto. `FP-82` queda `FIRMADA`
(la orden de mesa sigue vigente), no `EJECUTADA` — el hallazgo de esta nota es
el motivo por el que no se pudo ejecutar hoy, no una decisión de no hacerlo.

## ARRANQUE

1. **Repo.** `/home/user/Modelado-Mexicano`, clon existente, no se arrancó
   desde el home. `git log -1 --format="%h %s"` → `d859133 Merge pull request
   #315 from Josanoforo/claude/universo-recalculo-triage-w93rj3`.
   `git status` → limpio, sin cambios previos.
2. **SHA.** `git fetch origin main` → `origin/main` ya en `d859133`, mismo SHA
   que `HEAD` (esta rama arrancó desde `origin/main` post-merge de
   `TRIAGE-UNIVERSO-12`, `PR #315`). `git merge-base HEAD origin/main` →
   `d859133`. No hubo que refrescar: base correcta, `main` no se movió más
   allá.
3. **data/raw.** No aplica — entorno NUBE, sin corpus montado, verificado por
   la propia asignación del encargo (no se corrió ninguna sonda sobre
   `data/raw`).
4. **Entorno.** `echo $CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → `cloud_default`,
   coincide con lo esperado. Sin red ni microdato: no se corrió sonda de red
   (regla del propio encargo, punto 4 del ARRANQUE). `pgrep -af claude` → un
   solo proceso de sesión (mas el árbol de infraestructura del contenedor),
   sin concurrencia detectada — dueña única.
5. **Espejo.** Ninguna cifra de esta nota viene del espejo; todo se deriva del
   clon, comando a la vista abajo.

## Verificación de existencia

**1 · Estructura.** `forense/marco-candidatas-piloto-v1_0.tsv` existe, `61`
líneas (`60` filas + cabecera, `wc -l`), `17` columnas — coincide con lo que
`ADR-130` declara. Los filtros (i)-(v) de `ADV1-M1` se localizaron en
`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B (bloque `ADV1-M1`), citados
verbatim abajo. El crosswalk pregunta↔regla pasada 1 existe:
`forense/crosswalk-pregunta-regla-v1_0.tsv`, confirmado 60 filas / 10
`CANDIDATO-EMITE` por `awk` sobre la columna `emisibilidad_p1` — coincide con
`gobernanza:2795` (`ADR-138(f)`).

**La infraestructura CODEX que la firma cita — buscada, no encontrada como
herramienta de generación de candidatas.** `grep -rniF codex` sobre `.md`/
`.tsv` del árbol (37 archivos) más `git branch -a` y `git log --all --oneline
| grep -i codex` (0 ramas, 0 commits con "codex" en el asunto en este clon)
devuelven exactamente dos cosas, ninguna es una infraestructura de barrido de
corpus para candidatas nuevas:

- `AGENTS.md:1`/`:13` — "Codex" es el nombre del **rol ejecutor** del contrato
  del proyecto (*"Codex ejecuta técnicamente el encargo autorizado"*), el
  mismo rol que hoy corre esta sesión Claude bajo el mismo contrato — no un
  sistema de software.
- Menciones dispersas a ramas históricas `codex/barrido-2` y
  `codex/curador-baseline-semantico` (`ADR-91`…`ADR-113`, `forense/hallazgos.md`),
  todas ya fusionadas o cerradas, todas de **dominio disjunto**: cobertura
  material del universo de fuentes (`BARRIDO-2`) y rescate de historia git
  (`curador`) — ninguna produce specs de candidatas bajo `ADV1-M1`, ninguna
  vive hoy en una rama activa.

Ninguna búsqueda encontró un pipeline, script, o corpus adicional bajo el
nombre "CODEX" distinto de lo ya incorporado a `main`. Por regla del propio
encargo (§1 de la Verificación de existencia: *"si no la encuentras, ese
hueco es hallazgo y PARO de este acto, no improvisación"*), este es el primer
componente del PARO.

**2 · Contenido.** Re-verificado: el marco ampliado no existe.
`git log --oneline --since=2026-08-20 -- forense/marco-candidatas-piloto-v1_0.tsv`
no devuelve commits posteriores a su creación (`ADR-130`, 20/ago). `find . -iname
"*marco-candidatas*"` solo encuentra `v1_0.tsv` — ningún `v1_1`.
`canon/estado-programa-v1_10.md:99` sigue citando `60 de 60`. Confirmado.

**3 · Cobertura retroactiva.** `data/triaje-hitoD-2026-08-24.tsv` (13 filas,
`TRIAGE-UNIVERSO-12`) inspeccionado íntegro. Es la ficha del **Hito D**
(reglas falsificadoras `R1.4`…`R10.3`), población de conteo distinta y
disjunta de "candidatas del marco del piloto" — el propio contador declarado
de este acto lo prohíbe cruzar (`FP-68`/`ADR-67(c)`). Ninguna de las 13 filas
aporta una fuente con ruta nueva al universo `ADV1-M1` (encuestas
tramite/dinero/civismo/documentación/empleo/TIC del dominio del piloto): las
rutas que sí trae (`ENNViH-MxFLS`, `WVS7`/`ISSP ZA6980`, `Banxico CF881-885`,
`GDELT`/`UCDP`) pertenecen todas al universo de falsadores de Hito D, no al de
preguntas-candidata del duelo L-vs-M. Cero candidatas nuevas de esta vía.

## Criterio de saturación (derivado, no supuesto)

De `ADV1-M1` (`CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B): saturación =
el barrido del universo elegible bajo los filtros **(i)** no-publicada
(prueba del bibliotecario, 15 min) **(ii)** grado de dependencia P0/P1/P2 con
cuota ≥1/3 en P2 **(iii)** árbitro decidible (CV bajo el umbral CAC-007/01/2018
+ piso de `n` no ponderado) **(iv)** frase de discriminación pre-registrada
**(v)** ≥3-5 celdas post-corte deja de producir candidatas nuevas.

## Por qué este acto no puede ejecutar el barrido

Los filtros **(i)** y **(iii)** son, por su propio texto, no ejecutables desde
esta caja:

- **(i)** exige "prueba del bibliotecario" — la mitad web ya está declarada
  `NO EJECUTABLE` desde una caja sin navegador/red por el propio
  `marco-candidatas-piloto-v1_0.tsv` (columna `publicada`, fila `CIV-01`) y por
  `ADR-130`; esta sesión NUBE no tiene red de datos (punto 4 del ARRANQUE), así
  que hereda exactamente la misma limitación para cualquier candidata nueva.
- **(iii)** exige el CV del árbitro (motor `M`) y el piso de `n` no
  ponderado de la celda — ambos solo se calculan corriendo el árbitro sobre
  microdato, prohibido explícitamente en este acto NUBE (ver `ENTORNO
  ASIGNADO` del encargo: *"sin microdato"*).

El crosswalk pregunta↔regla pasada 1, la única fuente "insumo formal de la
saturación" que sí es legible sin red ni microdato, se cruzó fila por fila
contra `v1_0.tsv`:

```
cut -f1 forense/marco-candidatas-piloto-v1_0.tsv | tail -n +2 | sort > v1_0_ids.txt
awk -F'\t' '$col=="CANDIDATO-EMITE"{print $1}' forense/crosswalk-pregunta-regla-v1_0.tsv | sort > crosswalk_ids.txt
comm -13 v1_0_ids.txt crosswalk_ids.txt   # → vacío
```

Las 10 filas `CANDIDATO-EMITE` del crosswalk (`CIV-01`, `CIV-06`, `CIV-07`,
`DIN-01`, `DIN-03`, `DIN-11`, `TIC-05`, `TIC-06`, `TIC-07`, `TIC-11`) son
**subconjunto exacto** de las 60 candidatas ya existentes en `v1_0.tsv` — cero
filas nuevas. El crosswalk contesta "¿el motor M puede emitir para esta
variable ya en el marco?", no "¿qué variable nueva entra al marco" — es un
insumo de emisibilidad, no un generador de candidatas.

## Conclusión

No hay universo elegible barrible desde este acto: la única fuente legible
sin red/microdato (crosswalk) aporta cero candidatas nuevas, y toda vía que sí
podría aportarlas (corpus vía filtros (i)/(iii), o una "infraestructura CODEX"
específica) o exige capacidades que este entorno NUBE no tiene, o no se pudo
localizar en el árbol pese a la búsqueda declarada arriba. `60` sigue siendo
`60` — la saturación declarada por la firma de mesa no se puede medir ni
ejecutar hoy.

**Lo que mesa necesita para desbloquear:**
1. Aclarar a qué se refiere "infraestructura completa en CODEX" — no hay rama,
   script ni corpus adicional bajo ese nombre en el árbol verificado hoy; si
   es un recurso externo (chat/sesión), necesita llegar como adjunto con
   verificación de existencia propia, mismo patrón que `ADR-138(c)`/`ADR-139(a)`.
2. O bien: asignar el acto sucesor a **UBUNTU con corpus montado** — ahí sí
   son ejecutables los filtros (i) (prueba del bibliotecario) y (iii) (correr
   el árbitro sobre microdato para CV/n), y el barrido de saturación puede
   correr de verdad.

`ACT-PIL-3` (sorteo) sigue esperando: el marco no se amplió, la semilla
`867948c` sigue anulada, y no hay SHA de merge nuevo que la sustituya porque
este PR no congela ningún marco nuevo — congela el hallazgo de por qué no se
pudo.

**Perímetro respetado.** Tocados en este acto: esta nota (nueva),
`canon/gobernanza-v1_15.md` (ADR nuevo), `canon/estado-programa-v1_10.md`
(solo la línea de candidatas, sin cambiar la cifra), `forense/firmas-pendientes.tsv`
(fila `FP-82`, columna `ejecutada_en`), `forense/encargos/2026-08-24-AMPLIA-MARCO-SATURA.md`
(archivado verbatim, `CONSUMIDO`). No se tocó `forense/marco-candidatas-piloto-v1_0.tsv`
(nada que congelar), ni ningún archivo de `Hito D`/`data/`.
