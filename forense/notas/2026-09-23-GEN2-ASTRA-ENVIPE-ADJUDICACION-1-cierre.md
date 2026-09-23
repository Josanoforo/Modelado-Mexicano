# GEN2-ASTRA-ENVIPE-ADJUDICACION-1 · cierre de sesión · 23/sep/2026

**Veredicto: PARO-ENTORNO, no adaptación.** El objetivo del encargo pide
heredar **verbatim, sin cambio** el procedimiento del piloto 4
(`TRA-evade-norma-cruces-encogida-spec-v1_0.md`) para adjudicar C-ASTRA
contra el piso C2: "mismo ΔMAE, mismas réplicas de R del árbitro, mismo
umbral primario" (§3 del encargo). Ese procedimiento propaga la
incertidumbre de ΔMAE con **réplicas bootstrap de R sobre el microdato
ENVIPE 2025** (`tools/celda_d/marginales_reproduccion.py::replicas_compartidas`,
usado por `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001/adjudicacion.py`
líneas 217–247): por cada celda puntuada se generan réplicas de `R` a
partir de `ola25 = mr.carga_ola(envipe2025_csv, ...)`, y `ΔMAE` se calcula
réplica a réplica.

Este acto corre en **NUBE**, con la instrucción explícita del propio
encargo: *"cero microdato"* (cabecera ENTORNO) y PARO (a) *"abrir
microdato de ENVIPE 2025/2026 (este acto no tiene código autorizado)"*.
Verificado que el CALC sellado del árbitro **no** guarda las réplicas
bootstrap crudas — solo resultados escalares:

```
$ python3 -c "
import json
d=json.load(open('data/corrida0/CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001/resultados.json'))
res = d.get('resultados', d)
if isinstance(res, list):
    res = {x['id']: x['valor'] for x in res}
listy = {k:v for k,v in res.items() if isinstance(v, list)}
print('entradas tipo lista:', len(listy))
print('total entradas:', len(res))
"
entradas tipo lista: 0
total entradas: 685
```

Las 685 entradas selladas son todas escalares (puntos, IC de la proporción
por celda, MAE agregado, ΔMAE por candidato ya cerrado — C1/C2/C7/C-ENCOGIDA
únicamente). Ningún RESULT contiene el arreglo de réplicas por celda que el
medidor heredado necesita para calcular el IC de ΔMAE de un candidato
**nuevo** (C-ASTRA), porque C-ASTRA no era uno de los cuatro candidatos
originales del piloto 4 — el procedimiento sellado no anticipó una quinta
comparación, y su IC de ΔMAE está calculado y sellado solo para C7 y
C-ENCOGIDA contra C1/C2.

**Conclusión de la verificación:** reproducir el mismo procedimiento
(RÍGIDO desde COMMIT-1, D-18: "el código congelado no corre es PARO — no
se parcha") para C-ASTRA exige volver a abrir `envipe2025_csv` y volver a
correr `replicas_compartidas` — exactamente el PARO (a) de este mismo
encargo. No hay forma de cumplir a la vez "hereda el procedimiento por
sha, sin parámetro nuevo" y "cero microdato en NUBE": las dos instrucciones
de la cabecera se contradicen entre sí para este caso concreto (los
otros cuatro candidatos ya tenían su IC sellado antes de este acto; C-ASTRA
no).

## Premisas verificadas antes de declarar el PARO (§3 del encargo, con comando)

- `[EJECUTADO]` Compuerta cumplida: `#1031` (`ec0a8c7`) y el piloto 4
  (`#1036`, merge `73b7f11`) están los dos en `origin/main`
  (`git merge-base --is-ancestor <sha> origin/main` → sí, los dos).
- `[EJECUTADO]` Los cuatro `CALC-ASTRA-ENVIPE-*-0001` existen y sus
  `ejecucion.json` declaran `input_ids: [envipe2023_csv, envipe2024_csv,
  MARGINALES-PUBLICOS]` — **ningún id de 2025**, coincide con la premisa.
- `[EJECUTADO]` Orden de sellos verificado por búsqueda de contenido:
  `git log -p -S<sha256 de sello.json de la ARBITRO-CRUCES>` sobre la
  rama de Astra (`ec0a8c7^2`, PR #1031) → **0** apariciones. Astra nunca
  vio el sello de R antes de su propia emisión.
- `[LEÍDO]` Empate de celdas por texto: **ya documentado por la propia
  rama de Astra**, commit `159dc87` "Document pilot 4 cell compatibility
  and predictive interval limits" — `forense/analisis/astra-envipe/admisibilidad.tsv`
  (39 filas: header + 38 celdas), columna `compatibilidad_documental =
  COMPATIBLE-POR-SPEC` para las que se pudo verificar, columna
  `estado_admision = PENDIENTE-DE-CAJA` (el propio equipo de Astra ya
  sabía que la adjudicación final requería abrir R en un entorno con
  microdato). Esta pieza **sí está resuelta** y sirve al sucesor sin
  volver a derivarla.
- `[SUPUESTO]` Los cuatro cruces no fueron derivados por otro acto:
  `git grep -l 'CALC-ASTRA-ENVIPE' origin/main -- forense/notas` no
  arroja ningún acto de adjudicación previo (solo el recibo
  `GEN2-RECIBO-ASTRA-1`, que **no** adjudica: solo determina admisibilidad
  al piloto 4, `NO-ENTRA` por ventana de tiempo).

## Por qué esto no se resuelve "ajustando el procedimiento"

instrucciones-proyecto-v2_16.md §2/§6: una premisa falsa que toca **qué se
mide** (aquí: el método de propagación de incertidumbre, parte del
`estimando`/procedimiento congelado) para y se reporta; no se adapta para
que cuadre. Sustituir el bootstrap de réplicas por otro método (p. ej. una
IC basada solo en la proporción por celda, sin correlación entre celdas)
sería cambiar el procedimiento heredado — expresamente PARO (d) de este
mismo encargo ("cambiar el procedimiento heredado (umbral, réplicas,
agregador)"), y el propio §6 LATITUD dice "NO DECIDES: nada del
procedimiento heredado".

## Lo que sí queda de valor para el sucesor

- Los cuatro `CALC-ASTRA-ENVIPE-*` están sellados, con `REPRODUCE`/`IDENTICO`
  ya verificado en su propio PR (#1031).
- `admisibilidad.tsv` ya trae, por celda, las claves exactas de eje y el
  hash de `resultados.json` de cada CALC — el trabajo de empate celda-a-celda
  (§4 LATITUD, primera pregunta) está hecho y no hay que rehacerlo.
- El punto exacto donde el procedimiento necesita CAJA está acotado: **solo**
  la propagación de incertidumbre de ΔMAE (réplicas de R). El punto de
  ΔMAE en sí (diferencia de MAE puntual, sin IC) sí es derivable en NUBE
  desde los RESULT sellados — pero el encargo pide la comparación primaria
  **con IC**, no solo el punto, así que no se emite un veredicto parcial sin
  autorización de mesa.

## Suite

`python3 tests/check.py --rapido` → ver comando y salida en el commit de
cascada de este mismo PR.
