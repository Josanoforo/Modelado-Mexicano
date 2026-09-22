# ACTO GEN2-DIN-LOTE-C2-RESTRINGIDO-1 · cierre — los cinco pares con `formalidad` del lote ENIF 2024 ya tienen piso, en el universo de quien trabaja

**Contador: +1 corrida sellada GEN2 (`CALC-C2-RESTRINGIDO-IC-ENIF2024-0001`, `cuenta_gen2 = SI`) — «sellada en disco, no registrada» (E.7): el asiento de replay aislado viaja en el PR; la fila de la vista no (los derivados no viajan en los PR, §6). Cero adopciones, `celdas_validadas` no se mueve aquí.**

22/sep/2026 · CAJA (`ENTORNO-DERIVADO = CAJA`, corpus montado, `archivos_examinados=436`, `sin_variable`, red 200) · Opus · MODO RÍGIDO desde COMMIT-1 · rama `acto/gen2-din-lote-c2-restringido-1` · base `ccd7c0eb` · 0-bis `4e123a98` (raíz `4e12`) · encargo `forense/encargos/2026-09-22-GEN2-DIN-LOTE-C2-RESTRINGIDO-1.md` (sello de cuerpo `53cd0775…`). ADR `ADR-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01`.

## 1 · Qué se hizo, en orden de commits

| commit | qué | microdato |
|---|---|---|
| `4e123a98` | 0-bis A.3: encargo verbatim + sello de cuerpo | no |
| `31b5f734` | COMMIT-1: spec humana `forense/prereg-caja/C2-RESTRINGIDO-ENIF2024-spec-v1_0.md` (+ `.sha256`), `spec.yaml` (367 RESULT, generados desde `catalogo_resultados()` del medidor), `medidor.py`, `tests/test_c2_restringido_enif2024_guardia.py` (52/52 OK, sólo datos fabricados). `corrida0 preflight` **VERDE** sobre ese commit (payload `enif_2024_enif_2024_bd_csv` COINCIDE; 8/8 inputs repo COINCIDE). Empujado a `origin` antes de abrir el dato. | no |
| `e510e6a0` | COMMIT-2: primer y único `run` (`CALC-C2-RESTRINGIDO-IC-ENIF2024-0001--31b5f734dd90`, 6 s), sellado al primer intento | **sí, una vez** |
| `f1cbc86a` | E.7: asiento de replay aislado en `forense/replay-evidencia.tsv` (1 fila propia) | no |
| `bc452294` → revertido | filas propias en `corridas.tsv`/`resultados.tsv`: revertido porque los derivados no viajan en los PR (§6) | no |

## 2 · Verificación (salida cruda)

```
$ python3 tools/corrida0.py verify CALC-C2-RESTRINGIDO-IC-ENIF2024-0001
  [5/5 RESULT REPRODUCE] RESULT-C2R-ENIF2024-G-UPM (tipo=entero): sellado=2164 · hoy=2164 · delta=None
  [5/5 RESULT REPRODUCE] RESULT-C2R-ENIF2024-G-UPM-CON-T (tipo=entero): sellado=2138 · hoy=2138 · delta=None
VERIFY: REPRODUCE   (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)

$ python3 tools/verifica_aislada.py CALC-C2-RESTRINGIDO-IC-ENIF2024-0001 --salida …
  resultado_replay=REPRODUCE · contexto_replay=IDENTICO · exit_code=0
```

**Oro (spec §6)** — los dos marginales de `formalidad` re-derivados sobre la ola T contra los R sellados de `CALC-ARBITRO-MARGINALES-ENIF2024-0001`: `G-CONTROL-ARBITRO-VEREDICTO = REPRODUCE`, `|ΔP|max = 0.0`, `|ΔIC|max = 0.0`, `|ΔDEN-W|max = 0.0`, `ΔN = 0`, `ΔB-VALIDAS = 0`, `ΔFILAS = 0` (13 502), `ΔFUERA-T = 0` (4 190). Reproducción exacta, no «a tolerancia»: el plan de réplicas de este medidor es el de `_estimate` del piso que el árbitro GEN2 importó. Guardia AST: `PASA`, 0 violaciones. `G-C2-VECTORIZADO-VS-REFERENCIA-DELTA-MAX = 1.1e-16`. Réplicas sin definir: 0.

## 3 · P3 — qué pares quedan con piso

**Los 5 de 5**, 28 de 28 celdas con punto e IC95 publicados (`IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS-UNIVERSO-T`, 10 000/10 000 réplicas válidas en cada celda). Universo T = 9 312 personas (cobertura 0.689676 de filas, 0.675320 ponderada; 2 138 de 2 164 UPM). Ids: `RESULT-C2R-ENIF2024-AHORRA-SOLO-INFORMAL-<par>-<a>-X-<b>-{P,IC95INF,IC95SUP}`, con el mismo `_slug` y el mismo orden `(a, b)` que el lote.

| par | celdas | IC publicados |
|---|---|---|
| `formalidadxsexo` | 4 | 4 |
| `edadxformalidad` | 8 | 8 |
| `escolaridadxformalidad` | 8 | 8 |
| `formalidadxlocalidad` | 4 | 4 |
| `cuenta_formalxformalidad` | 4 | 4 |

`cuenta_formal × formalidad`: `NO-DEGENERADO` por la regla fijada antes del dato (ningún marginal en {0,1}, ninguna categoría vacía en T). **La pregunta a mesa del encargo (§6) no se dispara**: no hay nada que declarar `NO-CONSTRUIBLE`. Sigue vigente la nota del dictamen: en `sin cuenta`, D9 se reduce a `informal_cualquiera` por construcción del cuestionario.

## 4 · P3 — qué pierde el marcador por segmento si consume estos pisos

Para que el lote lo lea al evaluar (este acto no evalúa ni adopta):

1. **No se promedia con los otros nueve.** El error de C2R contra R vive en T; el de C2 compuesto, en la población 18+. Un ΔMAE, una cobertura o un conteo de celdas que junte los 14 pares mezcla dos universos (A-bis 4). Los 5 pares van en su propia fila/estrato del marcador, con el apellido «universo T», y la frase de producto no los suma a los 44 primarios.
2. **La comparación contra R sí es limpia**: la R de un cruce `formalidad × eje` es por construcción una proporción dentro de T (quien no llega a 3.13 no tiene celda de formalidad). C2R y R comparten universo; lo que C2R pierde frente al C2 poblacional es el nacional: su ancla es `p(D9 │ T) = 0.368586`, no el 0.357153 poblacional, y ninguna de sus celdas es comparable con una celda de C2 compuesto.
3. **Régimen de réplicas.** Este CALC corre en el régimen `ARBITRO-2024` (13 502 filas, marco entero) — el del árbitro cuyo R de formalidad reproduce a 0.0. El lote corre su R y sus réplicas en `PILOTO-1` (13 492). Los IC de aquí son sellados y citables; **las réplicas no están en `resultados.json`**, así que un ΔMAE con IC réplica-a-réplica en el lote exige re-derivar C2R dentro del lote con este mismo procedimiento (o importar este medidor) bajo el régimen que el lote declare, y emitir la diferencia contra los puntos sellados aquí — lo mismo que el lote ya hace con C2 compuesto.
4. **Persistencia (`P2`) y retadores (`R1/R2/R3`)** de esos pares usan 2021 con `P3_10` (1–5 con, 6 sin): otro texto de pregunta y otro T. El piso restringido no arregla esa asimetría; la hereda el lote.
5. **Soporte.** Las celdas más chicas de T son `60+` (n = 1 055 en T) y `hasta primaria` (1 691): el soporte por celda del cruce (umbral 200 del lote) puede caer en algunas `60+ × formalidad`; eso lo mide el lote sobre R, no aquí.

## 5 · Premisas del encargo, verificadas

| premisa | rótulo | verificación | resultado |
|---|---|---|---|
| FP `…8e53-02` opción B | [LEÍDO] | `forense/firmas-pendientes.tsv:442` (ABIERTA, sin respuesta) + texto verbatim en el encargo | Firma viaja en el encargo (A.12, §0 «dirección resuelve; mesa sella»): el lanzamiento sin borrarla es el sello — mismo patrón que `FP-260922-GEN2-FP374-RESELLO-1-dfbe-01`. Se asienta `FIRMADA`/`EJECUTADA` en el tablero. |
| FP `…6c10-02` (Q1) | [LEÍDO] | `firmas-pendientes.tsv:433` | Existe, ABIERTA; sus opciones A/B/C son las mismas que `…8e53-02` resolvió. No se toca (no es de este acto cerrarla); mesa puede cerrarla con este ADR. |
| dictamen `NO-EMITIBLE` «por objeto» | [EXISTE] | `data/corrida0/c2-compuesto-dictamen-v1_0.tsv`, columna `veredicto`, filas `ENIF 2024` | 10 filas NO-EMITIBLE (5 pares × 2 desenlaces); las 5 de D9 son las que este acto sirve. Vive en el dictamen TSV y en `parametros.pares.<par>.c2` del contrato del lote, no en `resultados.json` (por eso el `grep -c` de dirección daba 0). |
| crosswalk `formalidad` = P3_13, cobertura 0.689676 | [LEÍDO] | FD 2024 `TMODULO` filas 138–146; contrato del lote `ejes.formalidad.cobertura_arbitro`; árbitro GEN2 `G-FORMALIDAD-BLANCO` 4 134 + `G-FORMALIDAD-NO-SABE` 56 | Se sostiene: 9 312 / 13 502 = 0.6896756. |
| marginales restringidos no sellados | [SUPUESTO] | 7 `resultados.json` de `CALC-*ENIF2024*`/`CALC-DIN-LOTE-*` por id | Se sostiene: sólo `formalidad` existía en T (citado, y es el oro). |
| ningún otro acto de caja en vuelo | compuerta «borrar» | `gh pr list --state open` al arrancar: #998, #999 (NUBE, sin microdato), ambos fusionados durante el acto; `git worktree list` sin el rótulo | Cumplida. |

## 6 · Decisiones tomadas por latitud (declaradas)

- **Plan de réplicas del árbitro GEN2**, no el `replicas_compartidas` que usó el C2-IC: es el que selló los R contra los que el lote puntúa y el que permite reproducir el R de formalidad a 0.0. Probado idéntico a `_estimate` del piso en sintético (test) y en el dato (oro).
- **Marginal de formalidad citado del CALC GEN2 sellado** (`#971`, precisión completa), no del yaml GEN1 de 6 decimales.
- **Un solo desenlace (D9)**: el primario y único del lote. `informal_cualquiera` no se deriva (NC).
- **Vista: no registrada en este PR.** `registro --verifica --escribe --lote CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` se corrió (15 s) y, sobre `origin/main`, reescribía ~45 corridas y ~22 000 resultados de otros actos cuyos CALC están sellados pero no figuran en la vista (p. ej. los tres `CALC-ARBITRO-MARGINALES-2-*`; los CALC del lote aún como `SPEC-FIJADA`). Se publicaron primero sólo las filas propias (1 corrida + 367 resultados, 0 líneas ajenas) en `bc452294`, y se **revirtió**: por firma de mesa del 21/sep §2(2) (`GEN2-TUBERIA-EFICIENCIA-1`) ningún PR toca un archivo `# DERIVADO — NO EDITAR` (`tools/derivados_protegidos.py --toca`, bloqueante en CI), y el job de `main` no corre `registro` (exige `--lote`, juicio de mesa). Queda «sellada en disco, no registrada»; NC y hallazgo de una línea: la vista de `main` no tiene quien la registre.
- **`spec_md`** apunta a la spec humana en `forense/prereg-caja/` (precedente: árbitro GEN2), sin copia en el CALC.

## 7 · Lo que queda para mesa

`FP-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01` — cómo consume el lote estos pisos (opciones y recomendación en la fila). No gatea nada de este acto.
