# GEN2-RELEVO-CANDIDATOS-DELTA-1 · cierre técnico

Fecha: 16 de septiembre de 2026. Base efectiva:
`9dffd6455c67e2ca99740e79f90be59a13f250e1` (`origin/main`). Worktree:
`/home/pc0/mm-gen2-relevo-candidatos-delta-1`; rama
`acto/gen2-relevo-candidatos-delta-1`; PR `#829`.

**Resultado:** NC-0255 queda resuelta en su alcance técnico: selección viva,
contratos explícitos, comparación canónica y tres listas de decisión para los
slots con `veredicto=CANDIDATO-GEN2`. **Cero adopciones, cero edición de
consumidores, cero cambio del snapshot de M.** La integración serial y toda
cascada compartida permanecen diferidas.

## P1 · selección viva

`tools/relevo_usos.py --json`, sin `--escribe`, devolvió 207 slots:

```
YA-ADOPTADO=22
LISTADO-PARA-MESA=9
CANDIDATO-GEN2=12
NO-ADOPTABLE-POR-VEREDICTO-SELLADO=8
CONFLICTO-ENTRE-CANALES=2
VETADO-POR-DECISION=1
SIN-CANDIDATO=153
```

Se seleccionó por el valor de `veredicto`, no por posición ni por una cifra
fijada: `RES-0025`, `RES-0026`, `RES-0028`, `RES-0031`, `RES-0032`,
`RES-0033`, `RES-0034`, `RES-0053`, `RES-0054`, `RES-0055`, `RES-0056` y
`RES-0066`. Cada uno aparece exactamente una vez en contrato, delta y tabla de
decisión. La lectura completa, su SHA y la selección filtrada están en
`forense/relevo-usos/candidatos-delta-1/` y no son vistas canónicas.

## P2 · comparabilidad y delta

`tools/relevo_candidatos_delta.py` importa `deriva()`/`contrato()` y completa
solo las familias que el generador compartido deja prudentemente como
`INFORMACION-INSUFICIENTE`. No modifica el generador. Las ocho dimensiones se
anclan a specs, consumidores y notas publicadas con hash.

`corrida0 delta` examinó 12 parejas: **11 comparables, 1 incompatible; 11
deltas calculados y 1 delta sustantivo rechazado**. Referencias legacy y GEN2,
CALC/RESULT, hashes de spec/resultados/sello, generación y comparabilidad
quedan en `contrato-gen2-delta-1.yaml` y
`relevo-candidatos-delta-1.{json,tsv,md}`.

La exclusión material es `RES-0028`: el legacy `0.705687` es
`1-p(C2,U4)` tras colapso a **persona**; el candidato automático
`RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U1` cuenta delitos de `U1` cuya razón cae
en `{03,04,05,07}`. Rompen unidad, población, evento y transformación. El CLI
publica `DELTA-SUSTANTIVO-RECHAZADO-INCOMPATIBILIDAD`; no se resta ni se
interpreta `0.7327566125957219 - 0.705687`.

Control de consistencia: los cuatro RESULT de vías de ahorro (`RES-0053..0056`)
conservan su dependencia de `F`, `I` y `F∪I`; tanto los valores legacy como
los GEN2 publicados suman exactamente `1.0` en la lectura float del contrato.
No se tratan como cuatro mediciones independientes.

## P3 · regla firmada, separada de la tolerancia

El comparador rotula los 11 deltas numéricos `NO-MATERIAL` frente al umbral
descriptivo de `1e-6`. Ese rótulo **no gobierna la autorización**. Aplicada la
regla firmada de
`forense/encargos/2026-09-15-GEN2-RELEVO-USOS-1-ADENDA-REGLA-ADOPCION-EN-BLOQUE.md`
(pieza de dirección, líneas 53-65), la salida es:

- **Bin 1: 0.** `RES-0066` satisface signo e IC, pero alimenta
  `RES-0164:celda_AGREGADO`; la categoría obligatoriamente material manda.
- **Bin 2: 10** — `RES-0025`, `RES-0026`, `RES-0031`, `RES-0032`, `RES-0033`
  y `RES-0034` por ser las seis filas `conducta_p_medido`; `RES-0053`,
  `RES-0054`, `RES-0056` y `RES-0066` por alimentar celdas
  `M/AGREGADO`. Requieren firma individual aunque todos los cambios sean
  menores que `5e-7` y reproduzcan la representación publicada.
- **Bin 3: 2** — `RES-0028`, por incompatibilidad material sin delta, y
  `RES-0055`, comparable pero sin `se_mueve_si`, IC legacy propio ni la
  categoría de marcador que obliga a sus otras tres celdas hermanas a bin 2.

Todos requieren decisión de mesa: este producto no promete reducción del
contador. La partición de vías permanece una identidad conjunta aunque la
regla de autorización distribuya tres celdas a bin 2 y una a bin 3.

La tabla completa y el texto de resolución que mesa podría aprobar, sin
firma, están en `decisiones-propuestas.md` y `tabla-decision.tsv`.

## Producto reproducible

Directorio `forense/relevo-usos/candidatos-delta-1/`:

- `relevo-usos-lectura.json`, `seleccion-candidatos.{json,tsv}` y
  `seleccion-meta.json`;
- `contrato-gen2-delta-1.yaml`;
- `relevo-candidatos-delta-1.{json,tsv,md}`, escritos por el CLI canónico en
  un destino temporal e importados byte a byte bajo el rótulo propio;
- `tabla-decision.tsv` y `decisiones-propuestas.md`.

Envoltorio: `tools/relevo_candidatos_delta.py`. Regresión material:
`tests/test_relevo_candidatos_delta.py` protege cobertura exacta, p medida en
bin 2 aun con delta cero, incompatibilidad en bin 3, vías sin criterio en bin
3, dependencias `M/R/L/AGREGADO` en bin 2 y el caso de `RES-0066` que cumple
IC pero sigue siendo bin 2 por alimentar un agregado.

Comandos ejecutados:

```bash
python3 tools/relevo_usos.py --json
python3 tools/relevo_candidatos_delta.py --destino forense/relevo-usos/candidatos-delta-1
python3 tools/corrida0.py delta --entrada forense/relevo-usos/candidatos-delta-1/contrato-gen2-delta-1.yaml --formato humano --salida-dir forense/relevo-usos/candidatos-delta-1/_corrida0_delta
python3 tools/relevo_candidatos_delta.py --destino forense/relevo-usos/candidatos-delta-1 --delta-json forense/relevo-usos/candidatos-delta-1/_corrida0_delta/delta.json
python3 tests/test_relevo_candidatos_delta.py
```

No se abrió microdato, no se reejecutó medidor y no se leyó el cruce ENIF
2024 localidad × edad ni material reservado del piloto/F6.

## NO-CORRIDO / RESERVAS

| qué falta | causa | impacto | siguiente acción exacta |
|---|---|---|---|
| Decisión individual de diez slots | Bin 2 obligatorio por p medida o por dependencia `M/AGREGADO` | Conservan autoridad legacy aunque el delta sea pequeño | Mesa firma o rechaza cada renglón de `RES-0025/0026/0031/0032/0033/0034/0053/0054/0056/0066` |
| Decisión de `RES-0055` | Bin 3: no existe `se_mueve_si` ni IC legacy propio | La partición de vías sigue íntegramente legacy | Mesa acepta o devuelve el renglón dentro del bloque bin 3, conservando la identidad con sus tres celdas hermanas de bin 2 |
| Pareja sucesora de `RES-0028` | Ruptura persona U4 / delito U1; el RESULT propuesto por la ficha sucesora aún no existe sellado | No hay delta admisible ni relevo autorizable | Mesa elige el residual U4 documentado o un estimando U3; acto sucesor emite un RESULT compatible y vuelve a correr `corrida0 delta` |
| Cascada compartida de NC/decisiones/ADR/PARA/canon/contadores | Excepción temporal explícita del encargo | NC-0255 no se edita en esta rama aunque el producto técnico ya existe | Integración serial después de CAREO/TRÁMITE-4, sin reservar números aquí |

## CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4

Propagaciones necesarias al integrar: enlazar este cierre desde NC-0255;
registrar el consumo del encargo; y tramitar, sin adoptar por inferencia, el
los diez renglones bin 2 y el bloque bin 3. Un PR listo no equivale a
integrado, adoptado, validado ni desplegado.
