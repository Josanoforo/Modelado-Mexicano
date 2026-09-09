# `CALC-C0D-MARCADOR-v3` — el marcador GEN2 con el mapa de adjudicación corregido

**Sucede a `CALC-C0D-MARCADOR-v2`**, cuyas cifras son correctas y cuyos bytes quedan
**INTACTOS**. `repite_de: CALC-C0D-MARCADOR-v2` es el campo que el código lee para
derivar `SUPERADO→` en `registro()` y lo único que autoriza repetir sus ids.

Cara **local** de la spec sellada `forense/prereg-caja/C0D-MARCADOR-spec-v1_2.md`
(`prereg-caja-C0D-MARCADOR`, sha256 `03772efb319c2bd4acac2d5408e7388e8d960b2ce6b246a0628503125462aaae`).
Lo que este archivo dice, lo dice la sellada primero; si alguna vez discrepan, manda
la sellada. Congelado en el `COMMIT-1` de `ACTO GEN2-C0-D-CORRECTIVO`, antes de correr.

---

## Qué cambia, y qué NO

**UNA clase de diferencia: a dónde va el veredicto, no cuál es.**

`CALC-C0D-MARCADOR-v3` consume los **260 insumos de `v2`, byte-idénticos** —mismos
`id`, mismas rutas, mismos `sha256`—, más **un solo input de control**
(`IN-V2-RESULTADOS`) que ninguna medición lee y que existe para el control
§5-quater. **Ningún estimador, ningún parámetro de bootstrap, ningún `scope_id` y
ninguna rama de §4 se tocan.** Las cifras de `v2` deben permanecer idénticas, y hay
un control que PARA la corrida si alguna se mueve.

### Los tres defectos que corrige (`v1.2` §0.5, `v2/medidor.py:373-385`)

| # | defecto en `v2` | corrección en `v3` |
|---|---|---|
| **(a)** | **Veto de universo.** `elif (not identicos) and (rank_marginal != rank_comun): adj = "EXPLICADO-POR-UNIVERSO"` se evaluaba **antes** que la pareada. El ranking de `M` vetaba una comparación `L↔L` en la que `M` no participa. | El efecto de universo baja a **diagnóstico** (`RESULT-C0D-DIAGNOSTICO-UNIVERSO`, §5-bis) y **no entra a la adjudicación**. La función `_adjudica` no recibe siquiera el ranking. |
| **(b)** | **`NO-DISCRIMINA → EXPLICADO-POR-METRICA`.** Un IC95 que cruza cero se rotulaba como una explicación. | **`NO-DISCRIMINA → INCONCLUSO`.** Se afirma que no se puede decidir, no que quede explicado. |
| **(c)** | **El `else` mudo.** `CORPUS-AYUDA` (`ic_hi < 0`), la refutación inequívoca, caía en el resto y salía como `EXPLICADO-POR-METRICA`. | **`CORPUS-AYUDA → REFUTADO-CON-ALCANCE`**, rama propia. El mapa es un **diccionario** y una clave ausente **levanta excepción**. |

### Y tres piezas más

- **§3.5 reforzada.** La guardia de correspondencia contrasta `id_celda`, `variante`
  e `indice` **leídos del contenido de la captura**. `v2` tomaba `id_celda` e
  `indice` del nombre del archivo y sólo contrastaba `variante`.
- **§5.4 — el sucesor de alcance se separa del signo.** Se nombra `NC-0077` siempre
  que `RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES > 0`, cualquiera que sea el
  veredicto. `v2` lo ataba a `CONFIRMADO-CON-ALCANCE`. **`NC-0077` se reutiliza; no
  se abre deuda nueva.**
- **§5-ter — falsadores ejecutados.** Siete casos sintéticos, con su valor esperado
  congelado en `parametros.falsadores_pre_declarados`. `A` y `B` son los dos
  contraejemplos de la revisión adversarial. Uno solo en rojo **para la corrida**.

## Verificas así

```
python3 tools/corrida0.py preflight CALC-C0D-MARCADOR-v3
python3 tools/corrida0.py run       CALC-C0D-MARCADOR-v3
python3 tools/corrida0.py verify    CALC-C0D-MARCADOR-v3
```

## Lo que NO hace

No mide ninguna regla y ninguna cifra suya entra a un veredicto de regla (`T9`). No
toca capturas, ni motor, ni `CALC` previos, ni sus sellos, ni la banda `z` primaria
del duelo, ni `agregado_v1_*.py`. No re-captura nada. No introduce prueba de
equivalencia ni umbral post-hoc: `INCONCLUSO` es la ausencia de una conclusión.
