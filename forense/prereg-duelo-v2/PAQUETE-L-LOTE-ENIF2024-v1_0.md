# Paquete de la corrida `L` — lote de cruces ENIF 2024, `ahorra_solo_informal` · **v1.0 (FINAL)**

**Acto que lo produce:** `ACTO GEN2-DIN-LOTE-ENIF2024-COMMIT-1` · pieza P5 · 21/sep/2026 · CAJA ·
rama `acto/gen2-din-lote-enif2024-commit-1`. **Sucede** a `PAQUETE-L-LOTE-ENIF2024-v0_1.md` (`#967`),
de la que **importa** la plantilla de los prompts (sus bloques de código, verbatim) y hereda sin cambio
§0 (prohibición), §1 (qué se elicita), §4 (k = 8, mediana, modelo fijado al correr), §5 (formato de
captura), §6 (sellado antes del COMMIT-2 mecánico) y §7. **CONTADOR: cero.** Este acto **no corre**
ninguna `L`; mesa la ejecuta por CLI y sin `ANTHROPIC_API_KEY` (FP-228).

## Lo que este v1.0 fija y el v0.1 dejaba pendiente

- **La rejilla, leída del árbitro** vía `data/corrida0/CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/spec.yaml`
  (`parametros.ejes`, orden del árbitro): 44 celdas de los 5 pares primarios.
- **Los prompts por celda, generados** por `tools/lote_enif2024/genera_paquete_l.py`:
  `paquete-l-lote-enif2024-v1_0/prompts.jsonl` — **88 prompts** (44 celdas × 2 variantes),
  sha256 `ad774cece8ddd64baf21ec1a7fdde6b9aa5a4c377c9d143bfc9ca6f6a9fc334d`. Cada línea trae `celda_id`, `variante`, `prompt`, `prompt_sha256` y, en `L2`,
  los ids de RESULT de `CALC-ARBITRO-MARGINALES-ENIF2024-0001` (`#971`) de los marginales citados.
- **`celda_id`** = el mismo rótulo de celda que usan los emisores mecánicos
  (`RESULT-DIN-LOTE24-EM-<celda_id>-…`).
- **Marginales del `CONTEXTO` de `L2`:** los sellados en `#971` (D9, precisión completa), redondeados a
  un decimal de porcentaje en el prompt; el id citado permite reconstruir el número exacto.
- **Agregador:** `tools/agrega_l_v1_0.py` (`#973`, mediana con regla de inválidas fijada antes de
  contar). **`#973` no está en `main` al cerrar este acto**: se cita, no se importa (procedencia tipo 3);
  si no fusiona antes del sello de capturas, mesa decide agregador (spec v1_0 §16, Q3).

## Celdas del paquete (44)

| par | celdas (`celda_id`) |
|---|---|
| `edadxsexo` (8) | `EDADXSEXO-18-29-X-1-HOMBRE` · `EDADXSEXO-18-29-X-2-MUJER` · `EDADXSEXO-30-44-X-1-HOMBRE` · `EDADXSEXO-30-44-X-2-MUJER` · `EDADXSEXO-45-59-X-1-HOMBRE` · `EDADXSEXO-45-59-X-2-MUJER` · `EDADXSEXO-60-X-1-HOMBRE` · `EDADXSEXO-60-X-2-MUJER` |
| `escolaridadxsexo` (8) | `ESCOLARIDADXSEXO-HASTA-PRIMARIA-X-1-HOMBRE` · `ESCOLARIDADXSEXO-HASTA-PRIMARIA-X-2-MUJER` · `ESCOLARIDADXSEXO-SECUNDARIA-X-1-HOMBRE` · `ESCOLARIDADXSEXO-SECUNDARIA-X-2-MUJER` · `ESCOLARIDADXSEXO-MEDIA-SUPERIOR-X-1-HOMBRE` · `ESCOLARIDADXSEXO-MEDIA-SUPERIOR-X-2-MUJER` · `ESCOLARIDADXSEXO-SUPERIOR-X-1-HOMBRE` · `ESCOLARIDADXSEXO-SUPERIOR-X-2-MUJER` |
| `localidadxsexo` (4) | `LOCALIDADXSEXO-MENOR-DE-15-000-X-1-HOMBRE` · `LOCALIDADXSEXO-MENOR-DE-15-000-X-2-MUJER` · `LOCALIDADXSEXO-15-000-Y-MAS-X-1-HOMBRE` · `LOCALIDADXSEXO-15-000-Y-MAS-X-2-MUJER` |
| `edadxescolaridad` (16) | `EDADXESCOLARIDAD-18-29-X-HASTA-PRIMARIA` · `EDADXESCOLARIDAD-18-29-X-SECUNDARIA` · `EDADXESCOLARIDAD-18-29-X-MEDIA-SUPERIOR` · `EDADXESCOLARIDAD-18-29-X-SUPERIOR` · `EDADXESCOLARIDAD-30-44-X-HASTA-PRIMARIA` · `EDADXESCOLARIDAD-30-44-X-SECUNDARIA` · `EDADXESCOLARIDAD-30-44-X-MEDIA-SUPERIOR` · `EDADXESCOLARIDAD-30-44-X-SUPERIOR` · `EDADXESCOLARIDAD-45-59-X-HASTA-PRIMARIA` · `EDADXESCOLARIDAD-45-59-X-SECUNDARIA` · `EDADXESCOLARIDAD-45-59-X-MEDIA-SUPERIOR` · `EDADXESCOLARIDAD-45-59-X-SUPERIOR` · `EDADXESCOLARIDAD-60-X-HASTA-PRIMARIA` · `EDADXESCOLARIDAD-60-X-SECUNDARIA` · `EDADXESCOLARIDAD-60-X-MEDIA-SUPERIOR` · `EDADXESCOLARIDAD-60-X-SUPERIOR` |
| `escolaridadxlocalidad` (8) | `ESCOLARIDADXLOCALIDAD-HASTA-PRIMARIA-X-MENOR-DE-15-000` · `ESCOLARIDADXLOCALIDAD-HASTA-PRIMARIA-X-15-000-Y-MAS` · `ESCOLARIDADXLOCALIDAD-SECUNDARIA-X-MENOR-DE-15-000` · `ESCOLARIDADXLOCALIDAD-SECUNDARIA-X-15-000-Y-MAS` · `ESCOLARIDADXLOCALIDAD-MEDIA-SUPERIOR-X-MENOR-DE-15-000` · `ESCOLARIDADXLOCALIDAD-MEDIA-SUPERIOR-X-15-000-Y-MAS` · `ESCOLARIDADXLOCALIDAD-SUPERIOR-X-MENOR-DE-15-000` · `ESCOLARIDADXLOCALIDAD-SUPERIOR-X-15-000-Y-MAS` |

## Cómo se corre (mesa)

1. Sesión limpia, fuera del proyecto, sin abrir nada de §0 del v0.1. `L1` y `L2` en sesiones distintas.
2. Por cada línea de `prompts.jsonl`, `k = 8` llamadas idénticas; cada captura al formato de §5 del v0.1
   (`celda_id`, `variante`, `rep`, `p`, `estado_captura`, `modelo`, `version`, `temperatura`,
   `corte_entrenamiento`, `prompt_sha256`, `ts_utc`). Respuesta inválida → `RECHAZO`, se conserva, no
   se reintenta; celda con < 5 válidas → `L-INSUFICIENTE`.
3. Se sellan (sha256 + conteo OK/RECHAZO + mediana por celda y variante) **antes** de que exista
   `CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/sello.json`. El orden del diff es el sello.

## Lo que este paquete NO hace

No corre las llamadas · no abre microdato · no toca `corridas-R/` ni `corridas-M/` · no adjudica: `L1` y
`L2` son retadores **secundarios** y se rotulan así.
