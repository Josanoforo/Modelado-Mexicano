# ENCARGO · ACTO GEN2-EMISOR-ESTADO-1 · ¿DÓNDE EL EMISOR ES EL ÁRBITRO? — CENSO POR CELDA, Y LA ESCALA QUE FALTA EN 15 SALIDAS

CABECERA · redactado contra `0189562` (merge de #827); re-deriva al abrir · ENTORNO: NUBE — cero microdato; lee `milpa/tramite.yaml` y `milpa/tramite-ola5-propuesta-v0.yaml` · COMPUERTA: ninguna · MODELO SUGERIDO: Opus (P1 es lectura con juicio; P2 puede bajar a Sonnet si se lanza suelta) · FP/ADR/NC: deriva al cierre, no heredes (máximos hoy: FP-378, NC-0282, ADR-533) · vehículo: `/acto` · lote de dos piezas afines (D-11): las dos viven en `tramite.yaml`.

FIRMA DE MESA, verbatim (cerrada en conversación de dirección el 16/sep/2026; su archivo aquí la sella):

"Se autoriza (1) el censo, entrada por entrada y celda por celda, de qué valores del emisor (`milpa/tramite.yaml`) son copia del árbitro (`milpa/tramite-ola5-propuesta-v0.yaml`), con el veredicto por celda IDÉNTICO / MISMO-INSTRUMENTO-OTRA-OLA / INDEPENDIENTE, y una propuesta de marcador que compare M contra R solo donde no son el mismo número; y (2) declarar la `escala` en las 15 salidas `conducta_p_medido` que hoy la tienen `NO-DECLARADO-EN-EL-REGISTRO`, sin cambiar ningún valor de `p`."

## VERIFICACIÓN DE EXISTENCIA (A.8, dirección, contra `0189562`)

* (1) Estructura: `milpa/tramite.yaml` (emisor; GEN1, valores no se reescriben — E.1 — pero sus campos de metadato sí se completan), `milpa/tramite-ola5-propuesta-v0.yaml` (árbitro sellado), `data/corrida0/demanda-resultados.tsv` (derivado: `escala_legacy` sale de `salida.escala`, `tools/corrida0.py:307`; `NO_DECLARADO` cuando el campo falta), Dominio 8 (notas), tablero. Cubren.
* (2) Contenido: `grep -c "copiada verbatim" milpa/tramite.yaml` → 12 (líneas 114, 133, 207, 221, 422, 441, 519, … — el acto deriva la lista completa); NC-0275 los registra como 5 de 7 entradas `_ejes_` — el censo dice cuántas son en total y cuáles celdas. `grep -c "^ *escala:" milpa/tramite.yaml` → 3 (p. ej. `:284` `"proporcion administrativa agregada, censo, sin IC, COTA-SUPERIOR"`): el campo existe y es texto libre. Las 15 filas sin escala, derivadas del TSV: `RES-0003 0004 0005 0009 0011 0013 0015 0021 0022 0025 0026 0057 0058 0061 0062`. Un marcador que compare M contra R donde son idénticos: NO-ENCONTRADO (`forense/notas/2026-09-15-GEN2-MARCADOR-C0-D-A8-hueco.md` no lo contempla; F5 usó `IN-F5C-SNAPSHOT-M`). Ninguna nota censa la identidad: NO-ENCONTRADA (patrón `IDENTICO|copiada verbatim` sobre `forense/notas/`, reporta el conteo).
* (3) Cobertura retroactiva: NC-0275/0276 nacieron el 16/sep con el careo; el TSV derivado nace con cada `demanda`; nada anterior está oculto.

## PIEZAS

**P1 · Censo de identidad emisor ↔ árbitro (sucesor de NC-0275).** Tabla `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv` con una fila por celda del emisor que tenga contraparte en el árbitro (nacional y por eje): `regla · salida · celda · p_emisor · p_arbitro · instrumento_ola_emisor · instrumento_ola_arbitro · origen_linea (tramite.yaml:N) · veredicto`. Veredicto: `IDENTICO` (mismo número, misma ola, mismo instrumento — comparar es medir identidad) / `MISMO-INSTRUMENTO-OTRA-OLA` (M viene de una ola anterior: comparable como persistencia, y se dice) / `INDEPENDIENTE` (otra fuente: comparable de verdad) / `SIN-CONTRAPARTE`. Conteo por veredicto y por entrada `_ejes_`. Luego, en prosa, la propuesta de marcador: (a) las celdas `IDENTICO` salen de la comparación M-vs-R y se rotulan "emisor = árbitro"; (b) donde el emisor tenga ola anterior, M-vs-R se lee como persistencia (y se dice que es el mismo piso b de la tríada); (c) lo que queda como comparación legítima, contado. Ninguna cifra nueva: todo son números ya sellados leídos de los dos YAML. La propuesta no se implementa: va a mesa como decisión de diseño del marcador (fila FP). NC-0275 recibe el sucesor = esa FP; no se cierra aquí.

**P2 · Escala declarada en 15 salidas (sucesor de NC-0276).** Para cada una de las 15 `RES-*`: localizar la salida en `tramite.yaml`, leer su `origen`/`fuente` y escribir `escala:` con la fórmula de la casa — `"proporcion ponderada [0,1], <instrumento> <ola>, <unidad>"` — solo si `p ∈ [0,1]` y el origen citado es una proporción; si el origen es un índice, una razón o un agregado sin IC, se escribe la escala que sea y se dice; si no se puede determinar desde el origen citado, se deja `NO-DECLARADO` con la razón en una línea (no se adivina — A.15). Prohibido cambiar `p`, `tier`, `situacion` o cualquier campo que una receta de contador lea (A.16). Cierre: `python3 tools/corrida0.py demanda` re-derivado; `escala_legacy` en el TSV pasa de 15 a N `NO-DECLARADO` (reporta N y los que quedaron, con razón). NC-0276 → CERRADA si N = 0; si N > 0, sigue ABIERTA con las que faltan nombradas.

## PERÍMETRO Y CONCURRENCIA

`milpa/tramite.yaml` (solo campos `escala:` nuevos en las 15 salidas — ningún otro byte) · `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv` (nuevo) · nota de cierre en `forense/notas/` · `data/corrida0/demanda-resultados.tsv` (derivado, por comando) · tablero al cierre (`no-corrido.tsv`, `firmas-pendientes.tsv`, `hallazgos.md`) + cascada. No toca `tramite-ola5-propuesta-v0.yaml` (solo lectura), `milpa/src/`, el marcador, specs ni resultados. En paralelo: GEN2-CELDA-D-PILOTO-1 (caja: `prereg-caja/`, `CALC-DIN-*`, `corridas-L/`, catálogo, celda-D; lee `tramite.yaml:1306` sin editarlo) y GEN2-TRAMITE-4 (nube: `decisiones.tsv`, `gobernanza`, crosswalk, registro de corridas Codex) — sin archivo común salvo el tablero al cierre; quien fusione después renumera. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

## CONTADOR

Cero mediciones, dicho sin disfraz. Mueve `escala_legacy` NO-DECLARADO 15 → N (reportado) y produce la primera tabla de identidad emisor↔árbitro. LO QUE NO HACE: no cambia ningún `p` · no rediseña ni corre el marcador · no cierra NC-0275 (deja la FP de diseño abierta para mesa) · no toca el piloto ni el crosswalk. SUCESOR: el rediseño del marcador por segmento (dirección, con la FP de P1 firmada) · `GEN2-CORTE-EDAD-1` (después de TRAMITE-4). CIERRE: cascada + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P1 · «la propuesta no se implementa: va a mesa como decisión de diseño del marcador (fila FP)» | `DECISIÓN-DE-MESA-PENDIENTE` — así lo manda el encargo. La propuesta está redactada en prosa con sus tres reglas (a)/(b)/(c) y contada; no se tocó el marcador. | El rediseño del marcador por segmento no avanza hasta la firma. Ningún contador de medición se mueve. | `FP-380` (`forense/firmas-pendientes.tsv`, abierta hoy) |
| P1 · cierre de NC-0275 | `DECISIÓN-DE-MESA-PENDIENTE` — el encargo lo prohíbe explícitamente («no se cierra aquí»). La fila recibe sucesor y sigue `ABIERTA`. | NC-0275 sigue contando como deuda abierta del tablero. | `FP-380`, que es lo que la cerrará cuando mesa la firme |
| P2 · escala en 11 de las 15 salidas (`RES-0003`, `0004`, `0005`, `0009`, `0011`, `0013`, `0015`, `0021`, `0022`, `0025`, `0026`) | `FUERA-DE-PERÍMETRO` — no por falta de información: la escala de las 11 **sí** se determina desde su `origen` citado. `tools/corrida0.py:282` lee `escala` al nivel de la REGLA y la línea 307 la estampa en todas sus conductas; esas 11 viven en cuatro reglas de escala mixta, así que ninguna cadena única es verdadera para todas. Declararla a nivel de conducta no serviría (el derivador no la leería) y arreglar el lector es tocar `tools/corrida0.py`, que el perímetro excluye. | `escala_legacy` `NO-DECLARADO` en `conducta_p_medido` baja a **11**, no a 0; `NC-0276` sigue `ABIERTA`. | `NC-0283` (lectura de `escala` por conducta), abierta hoy |
| P1 · reparación de las once citas `origen:` desfasadas del emisor al árbitro | `FUERA-DE-PERÍMETRO` — el perímetro limita `milpa/tramite.yaml` a «solo campos `escala:` nuevos en las 15 salidas — ningún otro byte». Corregirlas sería reescribir once campos más. | Cualquier lectura futura que siga una de esas citas al pie de la letra leerá la entrada equivocada del árbitro. No mueve ningún `p`. | `NC-0284`, abierta hoy |
| Contraparte de `familia.cuidado.recae_mujeres_40mas / segmentacion_ejes_enut2024` | Resuelta, con reserva de método declarada: no hay cita ni prefijo común, y se emparejó por **alias declarado** contra `familia.cuidado.reparto_mujeres40_ejes_enut2024`. La evidencia es que sus 10 celdas etiquetadas coinciden en el valor exacto, 10 de 10 — no es inferencia, es medición. Queda como alias único y explícito, no como regla general. | Si mesa lo rechaza, esas 10 celdas vuelven a `SIN-CONTRAPARTE` y el censo pasa de 89 a 79 `IDENTICO`. El sentido del hallazgo no cambia. | `FP-380` (mesa lo ve al firmar el censo) |
| Desfase preexistente del derivado `data/corrida0/demanda-*.tsv` respecto de su fuente en `main` | `FUERA-DE-PERÍMETRO` en cuanto a causa — lo introdujo el merge de #834 (una celda-D nueva corre la numeración `RES-*` desde `RES-0174` y `CORR-*` desde `CORR-0080`), no este acto. Entra en este commit porque el comando re-deriva el archivo entero. | Los 15 ids que este acto toca (`RES-0003`…`RES-0062`) están por debajo del corte y no se renumeran. Quien lea `RES-0174`+ contra un commit anterior verá otro id. | `SIN-ASIGNAR` — se resuelve solo en cuanto cualquier acto vuelva a correr `demanda`, como hizo éste |

### A.8 · `ya_medido` de la única regla que este acto cita por `id` fuera del censo

La cita de `familia.cuidado.recae_mujeres_40mas` en la tabla de arriba es del
alias de contraparte, no una clasificación ni un pre-registro: este acto no
clasifica, no pre-registra, no carga y no sella ninguna regla del motor. Aun
así, `ADR-340` pide la salida del comando cuando un encargo archivado cita un
`id`, y aquí está — `python3 tools/ya_medido.py familia.cuidado.recae_mujeres_40mas`:

```
=== ya_medido: familia.cuidado.recae_mujeres_40mas ===
  resuelto por canon: familia.cuidado.recae_mujeres_40mas -> R5.2 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
-- milpa/tramite.yaml --
  milpa/tramite.yaml:1065  situacion=hogar_con_carga_de_cuidado tier=FUERTE veredicto=DISCRIMINA p=0.221500  [TASA-EJECUTADA]
-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)
-- data/corrida0 (RESULT + ejecución + sello) --
  data/corrida0/CALC-ENUT-0001/resultados.json:16  resultado_id=RESULT-ENUT-A-R ejecutado=SI sello=VALIDO  [TASA-EJECUTADA]
MEDIDA-EN: CALC-ENUT-0001, tramite.yaml
```

Lectura, y vale la pena decirla porque toca el censo: la regla está **MEDIDA**
y su `p` nacional (`0.221500`) es una **tasa ejecutada y sellada**
(`CALC-ENUT-0001`, `RESULT-ENUT-A-R`), mientras el árbitro «sin apariciones»
para este `id` es justamente por qué su contraparte tuvo que resolverse por
alias declarado y no por cita. Lo que el censo compara de esta regla son las
**10 celdas de su `segmentacion_ejes_enut2024`**, no ese nacional — y las 10
son `IDENTICO`.
