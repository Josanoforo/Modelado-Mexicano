# Nota de cierre — GEN2-TRAMITE-FIRMAS-10

ARRANQUE: NUBE (`ENTORNO-DERIVADO = NUBE`, coincide con lo declarado por el encargo). Base al día contra `origin/main` (`523f3c6`, tras fusión de #1033). Árbol limpio. Sin duplicado de rótulo (rama remota, worktree, PR abierto — los tres verificados).

## P1

- `python3 tools/corrida0.py status | grep adoptados_activos` antes: `=72`.
- `python3 tools/marcador_segmento.py --escribe`: escribe `data/corrida0/marcador-segmento.tsv` (229 filas) y `milpa/estimadores-por-segmento.yaml` (36 celdas adoptadas + 190 EMITIDA-SIN-EVALUAR + 57 marginales, 47 adoptadas/10 vetadas-o-diferidas).
- `status` después: `=87`.
- `git checkout -- data/corrida0/marcador-segmento.tsv milpa/estimadores-por-segmento.yaml` — revertido. Motivo: ambos llevan cabecera `# DERIVADO — NO EDITAR`; `tools/derivados_protegidos.py --toca` (guardia de PR, firma `GEN2-TUBERIA-EFICIENCIA-1`, 21/sep) rechaza cualquier PR que los traiga. `GEN2-TRAMITE-FIRMAS-9` (PR #1032) tropezó con la misma guardia y revirtió los mismos dos archivos.
- Conclusión: el diagnóstico de `NC-260922-GEN2-TRAMITE-FIRMAS-7-369b-02` era correcto (el 87 de `5ef1f41`/PR #1002 es alcanzable), pero el mecanismo de publicación es el job de push a `main` (`.github/workflows/verify.yml`, `[deriva]`, cableado desde `#1026`), no un commit manual de este PR.
- NC `NC-260923-GEN2-TRAMITE-FIRMAS-10-6980-01` asienta esto; no cierra `…-369b-02` hasta que `origin/main` muestre 87 por comando.

## P2

Lector de campos crudos (`str.split("\t")`, no `csv.reader`) sobre las 10 filas de §Ñ:

```
329 12 NC-0338
330 12 NC-0339
331 12 NC-0340
483 11 NC-260921-GEN2-L-DESDE-CAPTURAS-1-1d7c-01
484 11 NC-260921-GEN2-L-DESDE-CAPTURAS-1-1d7c-02
485 11 NC-260921-GEN2-L-DESDE-CAPTURAS-1-1d7c-03
527 11 NC-260921-GEN2-V216-d3da-02
590 11 NC-260922-GEN2-ESTADO-V15-1-7e23-02
591 11 NC-260922-GEN2-ESTADO-V15-1-7e23-03
605 11 NC-260922-GEN2-TRAMITE-COLA-VIEJA-1-0eca-02
```

Solo 7 de las 10 tenían de verdad 11 campos (cabecera=12). Patrón idéntico en las 7: el campo `que_no_se_corrio` nunca se escribió; el token de `razon` (A.14, ya válido: `DECISION-DE-MESA-PENDIENTE`, `DIFERIDO-A:...`, `FUERA-DE-PERÍMETRO:...`, `NO-VERIFICABLE-AQUI`) aparecía en la posición 6 en vez de la 7. Se insertó un campo vacío en la posición 6 (`que_no_se_corrio`), sin tocar ningún otro valor. Verificado tras la corrección: las 7 tienen 12 campos.

`NC-0338/9/40` ya tenían 12 campos — el inventario v3 §Ñ las incluyó de más. Su defecto real es distinto: el campo `razon` trae la prosa que debería estar en `impacto`, y todo lo posterior corrió una posición (`impacto`→lo que debería ser `sucesor`, `sucesor`→`ABIERTA` que debería estar en `estado`, dejando `estado` vacío). No hay manera no ambigua de saber si alguna vez hubo un token de `razon` que se perdió, o si nunca se escribió — se dejan como están, por la instrucción explícita de la pieza («si el contenido es ambiguo… se deja como está»).

Verificación de universo completo (A.13, no solo las 10 citadas):

```
filas con menos campos que la cabecera (archivo completo, tras la corrección): 9
NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04
NC-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01
NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-01
NC-260922-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-ef6f-01
NC-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01
NC-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-04
NC-260923-GEN2-RECIBO-ASTRA-1-4e74-01
NC-260923-GEN2-RECIBO-ASTRA-1-4e74-02
NC-260923-GEN2-RECIBO-ASTRA-1-4e74-03
```

Estas 9 no están en el inventario v3 §Ñ y el perímetro de esta pieza (§9 del encargo) restringe la edición a "las 10 filas de §Ñ … solo esas". No se tocan. No se pudo nombrar un acto ajeno dueño concreto de estas filas (abarcan cinco actos distintos del 21 al 23/sep sin herramienta de append común identificada en esta sesión), así que `FUERA-DE-PERÍMETRO:<acto>` no aplica con propiedad (A.14: "si no puedes nombrarlo, no era de otro acto y te toca a ti") — pero editarlas expande el perímetro que el propio encargo cerró a "solo esas". Se declara como bifurcación a mesa: NC `…-6980-02`, `DECISIÓN-DE-MESA-PENDIENTE`.

## Objetivo (§1)

- P1: `status` sigue en 72 en este PR (no >72). La nota explica por comando qué falta (mecanismo = job de push a `main`) y la NC `…-6980-01` nombra el sucesor. Satisface la disyunción del objetivo.
- P2: lector CSV sobre las 10 filas citadas cuenta 0 con menos de 12 (7 corregidas + 3 dejadas por ambigüedad explícita, no por defecto). Sobre el archivo completo cuenta 9, fuera de las 10 citadas, declaradas en NC `…-6980-02`.

## Perímetro

`forense/hallazgos.md`, `forense/no-corrido.tsv` (edición en sitio de 7 filas + 2 filas nuevas), `canon/gobernanza-v1_15.md`, `canon/L0/ADR-260923-GEN2-TRAMITE-FIRMAS-10-6980-01.md`, `canon/registro-rotulos.tsv`, esta nota. No se tocó `milpa/tramite.yaml`, `data/corrida0/marcador-segmento.tsv` ni `milpa/estimadores-por-segmento.yaml` (revertidos tras verificar). No se tocó `GEN2-TRAMITE-FIRMAS-9` ni su PR #1032.

## Suite

`python3 tests/check.py --rapido` → VERDE, 0 FAIL (verificado antes de este commit).
