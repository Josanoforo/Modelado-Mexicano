# Cierre · GEN2-RELEVO-REMESAS-F3-1

Rama `acto/gen2-relevo-remesas-f3-1`; PR `#835` contra `main`.

## Producto

`tools/relevo_usos.py` aplica F-3 exclusivamente a `RES-0035` y al consumidor
firmado. La compuerta exige pareja CALC/RESULT/veredicto exacta, las dos
corridas selladas exactas, sello físico y vista en `COINCIDE`, recibos de
ejecución correspondientes, cronología acreditable y coincidencia al grano
vigente del consumidor. Si falla una condición del caso, conserva
`CONFLICTO-ENTRE-VEREDICTOS` y escribe `F-3-NO-APLICA:<causa>`.

La vista `data/corrida0/relevo-usos-v1_0.tsv` fue regenerada únicamente con:

```text
python3 tools/relevo_usos.py --escribe
```

El productor anterior y el modificado se compararon sobre los mismos insumos:
sólo cambió `RES-0035`, en `veredicto_sellado` y
`veredicto_sellado_ref`. La tabla completa está en
`forense/analisis/relevo-remesas-f3-1/relevo-remesas-f3-1-antes-despues.md`.

## Verificación ejecutada

- `python3 tests/test_relevo_remesas_f3.py`: 6/6 casos.
- `python3 tests/test_relevo_candidatos_delta.py`: 6/6 casos.
- `python3 -m py_compile tools/relevo_usos.py tests/test_relevo_remesas_f3.py`.
- `corrida0._verifica_sello(...)`: `COINCIDE` para ambos CALC.
- Comparación estructurada de las 207 filas entre productor anterior y nuevo:
  única fila distinta, `RES-0035`.
- SHA-256 de specs, resultados y recibos de ambos CALC sin cambio; la prueba
  focal también fija los hashes de las specs y resultados sellados.

No se ejecutaron medidores históricos, `corrida0 registro --escribe`, cron,
`/tramite`, `/despacha` ni `/deriva`; no se abrió microdato ni reserva.

## Estado y reservas

- **PREPARADO:** encargo archivado con procedencia y SHA del original.
- **EJECUTADO:** selector, prueba focal, comparación y vista canónica listos.
- **SELLADO:** se consumen dos corridas previamente selladas; este acto no
  crea ni reescribe un sello.
- **INTEGRADO:** pendiente de fusión por Jonás.
- **ADOPTADO:** `RESULT-B-ENIGH-2022-P` ya era la cita adoptada; este acto no
  adopta una cifra ni cambia el consumidor.

**CIERRE COMPARTIDO DIFERIDO:** queda para el trámite serial propagar el cierre
administrativo de NC-0216. F-2/NC-0217, NC-0244 y cualquier decisión sobre
`RES-0047/0049` permanecen fuera de alcance.

El producto deja más cerca una decisión mejor: la vista ya expresa la decisión
firmada en vez de presentar una indecisión inexistente.
