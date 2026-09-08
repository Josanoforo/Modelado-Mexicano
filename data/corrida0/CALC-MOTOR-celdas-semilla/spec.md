# `CALC-MOTOR-celdas-semilla` — el motor matricial, corrido con cadena

`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, 8/sep/2026, P3(e).
Entorno **NUBE**, sin corpus y sin red. **CONTADOR: cero.**

## 1 · Qué pregunta responde

No una pregunta sobre México. Una sobre el aparato: **¿la ruta matricial
sellada por `ADR-91` también nace con cadena?** Es decir, ¿se puede correr
`milpa/src/motor.py` bajo `corrida0 preflight → run → verify`, con inputs
declarados y con sello, igual que cualquier otro `CALC`?

`ADR-91` (17/ago/2026, `PR #246`), firma de mesa verbatim:
*«M1 cómputo matricial como definición del ejecutable»*, adoptado **antes**
del gate de Fase 1. `D11` de `ACTO GEN2-E3-1` (`ADR-396`, 8/sep/2026)
declaró ese mismo ejecutable «scaffold histórico». Las dos cosas no pueden
ser verdad a la vez; `ACTO GEN2-T9` revoca `D11` y esta corrida es la
demostración material de la revocación.

## 2 · Por qué `cuenta_gen2: NO`

Firma de mesa D-1, 8/sep/2026: *«decisión 1 no cuentan como Gen2, no
cometamos un error sobre los 600 PR's que ya cagamos»*. La regla que
`ACTO GEN2-T9` escribe con nombre (E.1): **ningún `CALC` cuyo input resuelva
a `milpa/tramite.yaml`, `milpa/procedencia.yaml` o `corridas-R/M/L` cuenta
como GEN2, por completa que sea su cadena.** Esta corrida declara
`milpa/procedencia.yaml` entre sus inputs — el motor lo consume — y por eso
cae bajo la regla mecánicamente, sin necesidad de que nadie se acuerde.
Que la envoltura sea impecable no cambia la procedencia del número.

## 3 · Qué corre, y qué no

Se ejerce lo que el árbol permite ejercer. Lo que no, se declara con su
razón medida — no se rellena, no se salta, no se convierte en `NO-APLICA`:

| pieza | estado | cómo se comprueba |
|---|---|---|
| `momentos.cargar_catalogo()` | **corre** | 22 momentos, 8 `AJUSTE` / 14 `HOLDOUT` |
| el muro `AJUSTE`/`HOLDOUT` | **se ejerce** | se toca cada `HOLDOUT` por el único camino permitido y se comprueba que `valor_de` LANZA; 14 de 14 intocados |
| `motor.celdas_semilla()` | **corre** | las tres celdas-D del disco, por `listdir`, no de memoria |
| `celdas.CORTES_C1` | **corre** | 4 ejes sellados bajo M2, 2 `PENDIENTE` (`FP-53`) |
| `procedencia.cargar()` → `matriz.cargar_B()` → `motor.evaluar()` | **NO-EJECUTABLE** | `ClaseDesconocida`; ver §4 |

## 4 · El hallazgo: el ejecutable sellado no arranca hoy

`procedencia.cargar()` LANZA `ClaseDesconocida` sobre
`milpa/procedencia.yaml`. Dos valores de `clase:` que `milpa/src/clases.py`
no conoce por prefijo:

  · `REFUTADO-POR-COTA` — `asignados_probabilidad[10]`, escrita por
    `ACTO MAESTRA37-N8` (D2-g, firmas de mesa 3/sep/2026);
  · `EVIDENCIA_EXPERIMENTAL_TERCEROS` — el bloque homónimo, sellado por
    `ADR-204` y ya declarado como defecto preexistente en el comentario de
    `milpa/src/procedencia.py` (`ACTO MAESTRA32-E1`, 28/ago/2026).

Sin `Procedencia` no hay `B`; sin `B` no hay `g(x) = B·θ(x)` ni
`motor.evaluar()`. **El ejecutable que `ADR-91` selló como definición del
ejecutable no arranca**, y nadie lo había notado porque nada lo corría —
que es, exactamente, la consecuencia de haberlo declarado «scaffold».

Esta spec **no lo repara**: `milpa/src/**` está fuera del perímetro de
`ACTO GEN2-T9` (*«el motor se corre, no se edita»*). Lo mide, lo declara y
lo deja asentado en `forense/no-corrido.tsv` y en
`forense/firmas-pendientes.tsv` con sucesor nombrado.

## 5 · Determinismo

No hay estocasticidad: `seed.aplica: false`. Todas las lecturas son de
archivos versionados del repo, con SHA declarado. Dos corridas sobre el
mismo árbol producen los mismos bytes, y `verify` debe dar
`REPRODUCE` / `IDENTICO`.

## 6 · A.13 — cuántos archivos examinó el negativo

`RESULT-MOTOR-ARCHIVOS-EXAMINADOS` lleva la cuenta de los archivos que el
medidor abrió para producir su veredicto. Un negativo producido por un
comando que no examinó archivos no es un negativo.
