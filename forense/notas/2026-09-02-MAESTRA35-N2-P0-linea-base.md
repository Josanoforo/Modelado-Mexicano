# P0 · línea base ANTES de tocar F-DD — ACTO MAESTRA35-N2

Comando corrido, emisor SIN editar (`tools/emite_m.py` intacto, commit
`1c53bd9`):

```
python3 forense/notas/2026-09-02-MAESTRA35-N2-p0-script.py
```

Script: `forense/notas/2026-09-02-MAESTRA35-N2-p0-script.py` (temporal, vive
en `forense/notas/`, mencionado aquí — no ensucia `tools/`). Re-deriva las 13
celdas del sorteado v1_2 con M (`CIV-M-01/02/04/10/12/13`, `FAM-M-01/05/06/07`,
`TRA-M-02/03/07`, usando el nombre real de archivo comiteado, con o sin sufijo
`__v1_2`) vía `emite_celda(..., marco_nombre="marco-M-sorteado-v1_2.tsv")`
leyendo la fila por `id` de `marco-M-sorteado-v1_2.tsv`, más corre
`regresion()` (`M-TRA-M-01/02`) tal cual el módulo la define hoy.

## Salida cruda (resumen; ver `/tmp/p0-out.txt` de esta sesión para el
detalle campo por campo, reproducible con el comando de arriba)

Las 13 celdas y las 2 de `regresion()` (15 comparaciones en total) divergen
del comiteado **solo** en tres campos, nunca en un valor sustantivo:

1. `cita_p` y `cita_ola_calibracion` — el NÚMERO DE LÍNEA citado de
   `milpa/tramite.yaml` cambió (p.ej. CIV-M-01: `tramite.yaml:202` →
   `tramite.yaml:315`; TRA-M-01/02: `tramite.yaml:45` → `tramite.yaml:50`).
   El TEXTO citado (conducta, `p`, `clase`) es idéntico byte a byte; solo el
   prefijo `milpa/tramite.yaml:<N> --` corrió porque `tramite.yaml` creció
   entre la emisión original (MAESTRA33-E6, 1/sep) y hoy — inserciones de
   MAESTRA34-N9/MAESTRA35-N1 (enmienda `enif2024`, sellado de FASE1, etc.)
   desplazaron todo lo que vive debajo. **Hallazgo de MAESTRA35-N1** (el
   propio encargo lo anticipa: "el motor cambió tres reglas después de esa
   prueba"), no se corrige aquí.
2. `archivos_abiertos` — para las celdas cuyo M comiteado NO trae sufijo
   `__v1_2` (`CIV-M-01`, `CIV-M-12`, `CIV-M-13`, `FAM-M-01`, `TRA-M-02`,
   `TRA-M-03`, `TRA-M-07`), el archivo original cita
   `marco-M-sorteado-v1_1.tsv` porque así se emitieron (ACTO MAESTRA33-E6,
   antes de que existiera v1_2); esta corrida de P0 pasa
   `marco_nombre="marco-M-sorteado-v1_2.tsv"` por instrucción explícita del
   encargo, así que la entrada de `archivos_abiertos` que nombra el TSV
   difiere por diseño de la metodología de P0, no por un cambio del emisor.
   Mecánico, no sustantivo.
3. `TRA-M-02`: el JSON comiteado trae una clave extra
   `aviso_F_DD_abierto_por_FP_200b` que el esquema actual del emisor ya no
   produce — esquema previo, declarado, no se toca.

Ningún campo sustantivo (`p`, `valor_punto`, `clase`, `grado_DD`,
`razon_grado_DD`, `encuesta`, `ola`, `ola_calibracion`, `conducta`,
`variable`, `ponderador`, `estado_M`, `invocacion_emisor`, `determinismo`,
`ciego_a_R`, `id_celda`, `regla`) diverge en ninguna de las 15 comparaciones.

`fuente` y `correcciones_aplicadas_por_referencia` divergen como se espera
(campos exentos: cita el acto que corre / prosa a mano).

`regresion()` tal como el módulo la define hoy (que exige match byte a byte
en `cita_p`, sin exentarlo) devuelve `False` para ambas celdas
(`TRA-M-01`, `TRA-M-02`) — **por el mismo motivo (1)**: el corrimiento de
línea en `cita_p`, no por ningún cambio de lógica o de valor. Es decir: la
propia `regresion()` del módulo, HOY, sin tocar nada, ya falla por este
efecto colateral de MAESTRA35-N1 sobre `milpa/tramite.yaml`. Se reporta como
hallazgo, no se corrige (el emisor no se edita para "ajustar" citas; fuera
de perímetro de este acto arreglar `regresion()`).

## Veredicto por celda

| celda | archivo comiteado | veredicto |
|---|---|---|
| CIV-M-01 | M-CIV-M-01.json | diverge en campo no-exento (cita_p/cita_ola_calibracion línea, archivos_abiertos por diseño P0) — sin drift sustantivo |
| CIV-M-02 | M-CIV-M-02__v1_2.json | ídem (solo cita_p/cita_ola_calibracion línea) |
| CIV-M-04 | M-CIV-M-04__v1_2.json | ídem |
| CIV-M-10 | M-CIV-M-10__v1_2.json | ídem |
| CIV-M-12 | M-CIV-M-12.json | ídem (+ archivos_abiertos por diseño P0) |
| CIV-M-13 | M-CIV-M-13.json | ídem |
| FAM-M-01 | M-FAM-M-01.json | ídem (+ archivos_abiertos por diseño P0) |
| FAM-M-05 | M-FAM-M-05__v1_2.json | ídem (solo cita línea) |
| FAM-M-06 | M-FAM-M-06__v1_2.json | ídem |
| FAM-M-07 | M-FAM-M-07__v1_2.json | ídem |
| TRA-M-02 | M-TRA-M-02.json | ídem (+ archivos_abiertos, + clave de esquema previo) |
| TRA-M-03 | M-TRA-M-03.json | ídem (+ archivos_abiertos) |
| TRA-M-07 | M-TRA-M-07.json | ídem (+ archivos_abiertos) |
| TRA-M-01 (regresion()) | M-TRA-M-01.json | ídem (solo cita_p línea) |
| TRA-M-02 (regresion()) | M-TRA-M-02.json | ídem (+ clave de esquema previo) |

## Resumen

**Sin drift sustantivo.** Las 15 comparaciones (13 celdas + 2 de
`regresion()`) coinciden en TODOS los campos de valor sustantivo. La única
divergencia real y medida es el corrimiento del número de línea citado en
`cita_p`/`cita_ola_calibracion`, causado por ediciones de
`milpa/tramite.yaml` posteriores a la emisión original (MAESTRA34-N9,
MAESTRA35-N1) — hallazgo de esas fases, no de F-DD, no se corrige aquí. Se
anota en `forense/hallazgos.md` en la cascada de cierre.

Como este corrimiento de línea afecta a las 15 comparaciones por igual (no
selectivamente), y no involucra la gramática de F-DD que P1 va a tocar, la
metodología de P1 (ver `2026-09-02-MAESTRA35-N2-P1-regresion.md`) compara el
emisor NUEVO contra el emisor VIEJO (esta misma corrida P0) campo por campo
— la comparación que sí aísla si F-DD v1.1 introdujo algún cambio nuevo — y
declara por separado que ambas corridas (vieja y nueva) comparten la misma
divergencia de línea contra el comiteado, sin agravarla.

Script temporal usado: `forense/notas/2026-09-02-MAESTRA35-N2-p0-script.py`
(no se borra: queda como evidencia reproducible, mencionado en el perímetro
del encargo bajo `forense/notas/`).
