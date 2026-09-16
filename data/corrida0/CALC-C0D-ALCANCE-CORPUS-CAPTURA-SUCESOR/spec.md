# `CALC-C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR` — el metadato de alcance, censado de verdad

> `RESULT-C0D-ALCANCE-CORPUS-CAPTURA` (sellado en `CALC-C0D-MARCADOR`,
> heredado byte-idéntico por `-v2`/`-v3`) **no se toca**. Este CALC es el
> sucesor informativo que `NC-0078` y `NC-0242` pedían: censo mecánico de
> las 648 capturas de `forense/prereg-duelo-v2/corridas-L/`, no una muestra
> de una.

`ACTO GEN2-MANTENIMIENTO-3`, 16/sep/2026, `NC-0078`/`NC-0242`. Entorno
**NUBE**, sin corpus y sin red — las 648 capturas ya viven en el repo.
**CONTADOR: cero.**

## 1 · Por qué existe

`NC-0078` (9/sep/2026) midió que `RESULT-C0D-ALCANCE-CORPUS-CAPTURA` sale
pobre (`fecha_congelacion=sin-params`, `modelo=None`) porque su medidor
muestrea **una** captura, y pidió un acto sucesor que derivara el metadato
sobre las dos familias de esquema (`params` y `modelo_real`). `ACTO
GEN2-MARCADOR-C0-D` (15/sep/2026) hizo esa derivación — pero en prosa,
dentro de su nota de cierre (`forense/notas/2026-09-15-GEN2-MARCADOR-C0-D-
A8-hueco.md` §4), sin emitir el `RESULT` que la incorporara: el propio acto
declaró «no se cierra» y abrió `NC-0242` para eso exactamente. Verificado
hoy (`grep -rn "RESULT-C0D-ALCANCE-CORPUS-CAPTURA" .` antes de escribir esta
spec): seguía sin existir ningún `RESULT` sucesor emitido. Este `CALC` lo
emite.

## 2 · Metodología — re-derivada, no transcrita

Las cifras de §4 de la nota de `GEN2-MARCADOR-C0-D` se re-derivaron de
manera independiente (comando propio contra los 648 archivos, antes de
escribir este medidor) y **coinciden exactamente** con las publicadas por
esa nota. El medidor de este `CALC` es esa misma derivación, mecanizada:

1. **Universo**: los 648 archivos `.json` presentes hoy en
   `forense/prereg-duelo-v2/corridas-L/`.
2. **Subuniverso que el marcador consume**: los que **no** traen la llave
   `estado_captura` — 424 de 648. (Las 224 restantes son, en su totalidad,
   de la familia `ambas`: 352 − 128 = 224.)
3. **Tres familias de esquema**, no dos: sólo `params` (120), sólo
   `modelo_real` (176), ambas (352 sobre las 648; 128 sobre las 424
   consumidas).
4. **Sobre las 424**: `params.modelo_id` — `claude-opus-4-6` en 248
   (58.49 %), ausente en 176 (41.51 %); `params.fecha_congelacion` —
   `2026-08-26` en 120, `2026-09-01` en 128, ausente (familia
   `modelo_real`) en 176; `variante` — `L-solo` en 272, `L+corpus` en 152.
5. **`modelo_real`, sobre las 648**: 528 capturas traen la llave; de ésas,
   **cero** son distintas de `None`.

## 3 · La redacción corregida

`RESULT-C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR` publica, en una sola cadena, lo
que el campo debería decir: **`modelo_real=None en todas (0/528 no nulas) ·
modelo_id declarado en 248/424 (claude-opus-4-6) · ausente en 176/424`** —
en vez de `modelo=None` a secas, que la fila de `NC-0078` temía que una
lectura futura interpretara como «el brazo no declara modelo». La lectura
correcta se parte en dos: por `modelo_real`, en efecto ninguna captura
declara modelo; por `params.modelo_id`, 472 de 648 sí (472 = 248 + las 224
de familia `ambas`/`solo_params` fuera del subuniverso de 424 que también
traen `params`), y todas el mismo modelo.

## 4 · Qué no hace

No re-mide nada del duelo, no toca ningún tier, ninguna banda, ningún `p`
del motor. No re-escribe el `RESULT` sellado de `CALC-C0D-MARCADOR` ni de
sus sucesoras `-v2`/`-v3` (E.3). No decide si el metadato pobre del sellado
debe "mejorarse" — esa decisión, si alguna vez se toma, es de mesa y sobre
el propio sello, no sobre este CALC informativo aparte.

## 5 · Por qué `cuenta_gen2: NO`

Es un censo de metadatos sobre capturas ya existentes, no una medición que
entre a ningún veredicto de regla (T9): no hay `p`, no hay tier, no hay
adopción.
