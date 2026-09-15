# CORR-0001 · corrección de premisa, no sonda (P4)

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, NUBE.

### Por qué esta pieza no es una `/sonda`

El lanzamiento de este acto lista `CORR-0001 (ENCIG 2023 sin payload)` entre
los objetos de `P4` a sondear. Verificado contra `data/corrida0/mapa-demanda-19-corr-v1_0.tsv`
(escrito por `ACTO GEN2-SPECS-DEMANDA-1`, mismo día) y contra `NC-0197`
(`forense/no-corrido.tsv`): la premisa **"sin payload" es falsa desde el
29/jul/2026**. `/sonda` existe para buscar una fuente que no se sabe si
existe (`A.4`/`A.5`, universo examinado, candidatas). Aquí no hay nada que
buscar — el objeto ya está localizado, con `sha256` verificado:

```
$ grep "^CORR-0001" data/corrida0/mapa-demanda-19-corr-v1_0.tsv
CORR-0001  ENCIG2023  4  BLOQUEADA  DECISION-DE-MESA  NINGUNO  0/4  MESA · decision D1 armada
  El payload NO falta: encig23_base_datos_csv (sha af733d86..., 38309647
  bytes, 29/jul/2026) mas cuatro gemelos (RData/DBF/DTA/SAV, 5/ago/2026)
  estan en el manifiesto. ...
```

Correr `/sonda` sobre un objeto ya `EXISTE-SATISFACE` (por identidad de
payload) sería exactamente el defecto que `A.8` existe para prevenir:
volver a pagar por un hallazgo que ya está escrito, con cita. Se declara la
corrección en su lugar.

### El bloqueo real es `D1`, una decisión de mesa, no una fuente

`CORR-0001` (4 `RESULT`) queda `BLOQUEADA · DECISION-DE-MESA`: la pregunta
es **qué hacer** con los cuatro `RESULT` `ASIGNADOS` (0.62/0.38, 0.88/0.12)
de dos reglas cuyas celdas `ENCIG2025` ya están `MEDIDAS` (`CORR-0002`) —
retirar / medir `ENCIG2023` / conservar como prior (`D1`, armada por
`ACTO GEN2-SPECS-DEMANDA-1 §3`, sin firmar). Ninguna búsqueda de este acto
cambia eso: **es la misma decisión `D2`** (precedencia del MEDIDO sobre el
ASIGNADO) a escala de una sola regla, ya diagnosticada.

### Qué SÍ hace esta pieza

Nada más que esta declaración — no escribe spec, no corre sonda, no toca
`milpa/`. Es la corrección de premisa que `A.8` exige antes de gastar
trabajo en un objeto que no lo necesita.

### Cierre

Ninguna `NC` nueva: `NC-0197` ya cubre `D1` como `DECISION-DE-MESA-PENDIENTE`.
Este documento sólo asienta por qué `P4` de este acto no produjo una sonda
sobre `CORR-0001`.
