# `MARCO-M-v1_2` · P3 — emisión M sobre el sorteado v1.2

`ACTO MAESTRA34-N2 · MARCO-M-v1_2`, 2/sep/2026, NUBE. Skill `/emite-m`
(`tools/emite_m.py`), **no editado**: este acto importa sus funciones selladas
(`emite_celda`, `regresion`, `esquema_de_referencia`) y sólo cambia el
`marco_nombre` y el nombre del archivo de salida — `tools/` está fuera del
perímetro del encargo, y la salida `corridas-M/*__v1_2.json` dentro.

## Regresión P2 — compuerta del emisor

`regresion()` contra `M-TRA-M-01.json`/`M-TRA-M-02.json`: **PASA**. Los únicos
campos que no salen `OK` son los dos que el propio módulo declara exentos desde
su emisión original — `fuente` (cita el acto y la fecha que corren) y
`correcciones_aplicadas_por_referencia` (prosa a mano en el original, mismo
valor). Ningún campo de valor diverge. Sin la regresión en verde no se emite
nada, y no se ajustó el emisor para forzar el match (`--ajustar` no existe a
propósito).

## Regresión byte a byte de los M existentes

El encargo manda no tocar los `M` de v1_1 *"aunque la regla haya cambiado
(registro de lo que M creía entonces)"*. Se cumple por construcción: este acto
escribe **únicamente** nombres `M-<id>__v1_2.json`, y `git status` sobre
`corridas-M/` no reporta un solo archivo modificado — sólo los 6 nuevos.

Además se corrió la prueba que de verdad importa: **re-derivar hoy**, con el
motor ya en 10 reglas, las 7 celdas sorteadas en v1.2 que ya traían `M`
(`CIV-M-01`, `CIV-M-12`, `CIV-M-13`, `FAM-M-01`, `TRA-M-02`, `TRA-M-03`,
`TRA-M-07`) y comparar campo por campo contra el archivo comiteado.

**Resultado: cero drift.** Cargar `familia.seguro.volatilidad_ausencia_estado` y
`dinero.planeacion.formal_estable` (`MAESTRA34-N1`, 8 → 10 reglas) **no movió
ninguna emisión previa** — las reglas nuevas son adiciones, no enmiendas, y
`cargar_reglas()` las expone sin perturbar a las 8 anteriores.

## Emitido: 6 celdas

De las 14 sorteadas, 7 ya traían `M` (arriba) y 7 no. De esas 7 se emitieron 6:

| id | encuesta | ola | regla | `p` de M | `grado_DD` |
|---|---|---|---|---|---|
| `CIV-M-02` | ENVIPE | 2013 | `civico.denuncia.miedo_desconfianza` | `0.294313` | `P1 PUNTUA` |
| `CIV-M-04` | ENVIPE | 2015 | idem | `0.294313` | `P1 PUNTUA` |
| `CIV-M-10` | ENVIPE | 2021 | idem | `0.294313` | `P1 PUNTUA` |
| `FAM-M-05` | ENIGH | 2016 | `familia.seguro.volatilidad_ausencia_estado` | `0.045694` | `P1 PUNTUA` |
| `FAM-M-06` | ENIGH | 2018 | idem | `0.045694` | `P1 PUNTUA` |
| `FAM-M-07` | ENIGH | 2020 | idem | `0.045694` | `P1 PUNTUA` |

Esquema verificado contra `M-TRA-M-01.json` leído en tiempo de ejecución (no de
memoria): ni un campo de más ni de menos en los 6.

**El juicio de marco de P1 queda confirmado por el motor, no por argumento.**
Las tres celdas ENIGH emiten `p = 0.045694` — el p de la ola de calibración
(2022) — para las olas 2016/2018/2020. `emitir_binaria` nunca miró `serie_olas`,
exactamente como P1 predijo al leer `milpa/src/emisor.py:475-481`. Y el emisor
**re-derivó `grado_DD` por su cuenta** (`calcula_grado_DD`, su propia
implementación de F-DD) y llegó al mismo veredicto que el congelado:
`P1 PUNTUA`, *"NO coinciden (transferencia de ola) → validación externa"*. Dos
derivaciones independientes de F-DD, mismo resultado.

## Hallazgo — `DIN-M-01` no se pudo emitir (entregable, no defecto de este acto)

`DIN-M-01` salió sorteada y es `elegible_v1_1=SI`, `P1 PUNTUA`. El emisor **se
negó**:

```
ValueError: ola_calibracion sin forma '<INSTRUMENTO> <ANIO>...':
'ENNViH ola 2 (2005-06) -- ponderador fac_3b vive en esta ola'
```

`calcula_grado_DD` parsea `ola_calibracion` con
`_RE_OLA_CAL = ^([^\s(]+)\s+(\d{4})` — instrumento seguido de año. La regla
`dinero.ahorro.tiene_ahorros` declara `ola_calibracion: "ENNViH ola 2
(2005-06) …"`, cuyo segundo token es `ola`, no un año. El emisor **levanta la
excepción en vez de adivinar**, que es su comportamiento sellado y deseado
(mismo criterio que su `LookupError` para reglas sin `ola_calibracion` propia):
*"no se inventa, extiende la constante con la cita real antes de emitir esta
celda"*.

**Es un defecto latente que este sorteo destapó, no uno que este acto
introdujo.** `DIN-M-01` ya era elegible en `marco-M-congelado-v1_1.tsv`, pero
**no salió sorteada en v1.1** (`marco-M-sorteado-v1_1.tsv` no la contiene), así
que nadie había intentado emitirla nunca. El sorteo de v1.2 la sacó y el
defecto apareció al primer intento.

**No se parchó, y la razón es de perímetro, no de dificultad.** El arreglo
correcto es una entrada en `_OLA_CALIBRACION_FIJA` de `tools/emite_m.py` con su
cita real — exactamente el mecanismo que esa constante existe para dar, y que ya
se usó una vez para `tramite.mordida.discrecional`. Pero `tools/emite_m.py` está
**fuera del perímetro** que el encargo declara, y el encargo es explícito: *"Si
te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal
calculado y saberlo vale más que el atajo."* Se reporta con el parche propuesto
y se deja la decisión a mesa.

Parche propuesto (**no aplicado**), para que un acto sucesor con `tools/` en su
perímetro lo tome tal cual:

```python
_OLA_CALIBRACION_FIJA = {
    ...,
    "dinero.ahorro.tiene_ahorros": (
        "ENNViH 2005",   # ola 2 = 2005-06; el anio de inicio es el que el marco usa
        'milpa/tramite.yaml -- ola_calibracion: "ENNViH ola 2 (2005-06) -- '
        "ponderador fac_3b vive en esta ola\"; el marco congelado ya adjudico "
        "que ola 2 Y ola 3 son P0 (DIN-M-02/DIN-M-03, razon_DD: 'panel retenido'), "
        "asi que una entrada de un solo anio NO reproduce esa clasificacion -- "
        "mesa decide si F-DD necesita soportar rangos de ola antes de emitir "
        "DIN-M-01/02/03.",
    ),
}
```

⚠️ El parche de una línea **no basta y no debe aplicarse a ciegas**: el marco
clasificó `DIN-M-02` **y** `DIN-M-03` como `P0` porque el `universo` de la regla
consumió las dos olas juntas ("panel retenido"), mientras que un
`_OLA_CALIBRACION_FIJA` de un solo año haría que el emisor marcara `ola 3`
(2009-12) como `P1 PUNTUA` — **contradiciendo el congelado**. Es decir: el
hallazgo real no es un regex corto, es que **F-DD no tiene forma de expresar una
calibración sobre un rango de olas**, y `dinero.ahorro.tiene_ahorros` es el
primer caso que la necesita. Eso es decisión de mesa, no de un ejecutor.

Consecuencia para el tablero: de las 14 celdas sorteadas, **13 tienen `M`** y una
(`DIN-M-01`) queda sin `M` hasta que mesa resuelva lo anterior. La celda **no**
se retira del sorteado — retirarla sería reescribir un sorteo ya sellado.

## Contador

`M` nuevos: **6** (`corridas-M/M-<id>__v1_2.json`). `M` de v1_1 tocados: **0**.
Celdas sorteadas con `M`: 13 de 14.

## Lo que P3 no hace

No calcula R, no corre L, no puntúa, no edita `tools/emite_m.py`, no reescribe
ningún `M-<id>.json` de v1_1, no retira ninguna celda del sorteado. `ciego_a_R`:
**SÍ** — no se abrió `corridas-R/` ni ninguna columna de valor de R.
