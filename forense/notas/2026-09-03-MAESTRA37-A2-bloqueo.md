# ACTO MAESTRA37-A2 · REVISA-COLA-A-DETALLE — bloqueo de COMPUERTA

3/sep/2026, entorno NUBE con red (cloud_default).

## Verificación de la COMPUERTA

El encargo `forense/encargos/2026-09-03-MAESTRA37-A2-REVISA-COLA-A-DETALLE.md`
exige como COMPUERTA: «PR de N8 fusionado (mismo archivo de cola; N8
reclasifica estados, éste añade informe por fila)».

Búsqueda hecha antes de tocar el SPEC:

```
git log --all --oneline --grep='N8' -i
git log --all --oneline --grep='MAESTRA37-N8'
ls forense/encargos | grep -i N8
ls forense/encargos/cola | grep -i N8
git log --all --oneline -- 'forense/encargos/*N8*'
```

Resultado: existen `MAESTRA34-N8-FECHAS-SON-LIMITES` (2/sep, fusionado en
`28a13ee`/PR sin relación con la cola) y `MAESTRA35-N8-SELLA-L7` (fusionado
en `e1afa2a`/PR #492, sobre `milpa/tramite.yaml` y L0, no sobre la cola).
**No existe ningún `MAESTRA37-N8`** — ni encargo redactado, ni PR, ni
commit, ni mención — en ninguna rama del árbol local tras `git fetch
origin main`.

## Veredicto

**COMPUERTA NO SATISFECHA.** No hay evidencia de que un PR de N8 (serie
maestra-37) que reclasifique estados en
`data/curacion-registro/cola-adquisicion-registro.tsv` se haya fusionado.
Por protocolo de `/acto` ante compuerta no satisfecha, este acto **no
ejecuta el SPEC** (no arma el informe por fila, no sondea rutas, no busca
hermanas, no toca la columna `nota` de la cola). Se declara BLOQUEADO y se
deja constancia aquí y en el propio encargo, para que dirección o mesa
decidan: (a) redactar y correr MAESTRA37-N8 primero, o (b) instruir a este
acto a proceder sobre el universo de 29 filas tal cual está hoy,
declarando explícitamente que las reclasificaciones de N8 (5→
NO-ADQUIRIDA-POR-COSTO, 2→PENDIENTE-DE-MESA) no están reflejadas.

Ninguna fila de la cola fue tocada. No se hizo ninguna descarga, sonda de
red, ni cambio a `estado_A4A5`, `data/manifiesto.yaml` ni
`aliases-fuentes.tsv`.

## CONTADOR

Filas con informe: 0 → 0 (bloqueado antes de COMMIT-1). Medición: cero
directo.
