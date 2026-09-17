# GEN2 · Derivado U4 para RES-0028

Fecha: 16 de septiembre de 2026. Acto:
`GEN2-ENVIPE-RES0028-DERIVADO-U4-1`. Base efectiva `origin/main`:
`4fff914f286021574ac0897273ee0e6971b38f04`, que ya contiene el diagnóstico
fusionado del PR #829 (`d8ffe71`, cabeza revisada `15d6683f`). No se abrió
microdato ni se ejecutó un CALC padre.

## Producto

Se creó y selló el CALC independiente
`CALC-ENVIPE-RES0028-U4-DERIVADO-0001`. Su único objeto sustantivo es
transformar el punto y el IC publicados por `CALC-ENVIPE-0001`; no agrega
información muestral independiente.

Correspondencia propuesta, todavía no adoptada:

`RES-0028 → CALC-ENVIPE-RES0028-U4-DERIVADO-0001::RESULT-ENVIPE-RES0028-Q-C2-U4`

| cantidad | valor | unidad y denominador |
|---|---:|---|
| `p(C2,U4)` padre | `0.29431298745731216` | persona; `n=13023`, masa `FAC_ELE=14982594` |
| `q=1-p(C2,U4)` | `0.7056870125426878` | la misma persona U4 y el mismo denominador |
| `IC95(q)` | `[0.6942008049952509, 0.7169802491746927]` | transformación `[1-IC_hi(p), 1-IC_lo(p)]` |
| `p+q` | `1.0` | control de partición sobre el mismo denominador |

El método heredado es `IC-CON-ESTRATOS-DE-UPM-UNICA`: bootstrap de UPM dentro
de estrato, con 83 estratos de una sola UPM en el padre. Por ello el intervalo
conserva la limitación declarada por el padre y se lee como límite inferior de
la anchura verdadera, no como IC exacto.

## Qué significa q

El padre agrega a persona con `d_persona=max(d_delito)` sobre sus delitos
elegibles de U1. En consecuencia, `q=1` sólo cuando **ningún** delito elegible
de la persona tiene `BP1_23` en C2=`{01,02,06,08}`. Si una persona tiene un
delito C2 y otro en `{03,04,05,07}`, vale `p=1, q=0`; no pertenece a dos ramas.

Así definido, q no es automáticamente confianza, tasa por delito, probabilidad
de denunciar, categoría literal `09 Otra`, ni probabilidad de presentar al
menos una razón residual. `09`, `99` y blanco siguen fuera del recorte U1 que
hereda U4.

## Separación de candidatos y compatibilidad

| oferta | referencia | unidad | evento | valor | veredicto frente a RES-0028 |
|---|---|---|---|---:|---|
| candidato antiguo de PR #829 | `CALC-ENVIPE-0001::RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U1` | delito U1 | delito cuya razón está en `{03,04,05,07}` | `0.7327566125957219` | `INCOMPATIBILIDAD`: no se calcula delta contra legacy persona U4 |
| derivado nuevo | `CALC-ENVIPE-RES0028-U4-DERIVADO-0001::RESULT-ENVIPE-RES0028-Q-C2-U4` | persona U4 | ningún delito elegible de la persona está en C2 | `0.7056870125426878` | `COINCIDE-AL-GRANO-U4`; candidato compatible |

La incompatibilidad histórica de PR #829 queda intacta. La nota histórica
`2026-09-15-GEN2-E11-RES0028-PARTICION-cierre.md` parte correctamente de U4 y
describe el evento de persona, pero propone el nombre
`RESULT-ENVIPE-DEN-Q-C2-U1-RESIDUAL`: ese sufijo U1 contradice la unidad del
padre y no se reutiliza aquí.

La rama viva del consumidor dice “ningún delito elegible de la persona
pertenece al grupo padre”, usa `q=1-p(C2,U4)` y materializa `0.705687`. Escala,
codificación, población, unidad, evento y transformación sí coinciden con el
nuevo resultado. Por eso aplica el delta canónico, en dirección candidato
menos legacy:

`0.7056870125426878 - 0.705687 = +1.25426878e-08`.

Su magnitud es menor que `1e-6`, de modo que la representación coincide al
grano de seis decimales. Esto autoriza proponer el relevo, no adoptarlo.

## Cadena y pruebas

La spec se comprometió en `cfbc2ae` antes del primer uso real del medidor. El
ajuste de precisión decimal quedó comprometido en `65d0408`, y esa es la
revisión que registra `ejecucion.json` como código ejecutado.

Comandos efectivos:

```text
python3 tests/test_envipe_res0028_u4_derivado.py
# 5 casos, 5 ok: complemento/suma uno, inversión del IC, límites inválidos,
# padre no estimable, unidad/U1 erróneos, claves reales e inmutabilidad del padre

python3 tools/corrida0.py preflight CALC-ENVIPE-RES0028-U4-DERIVADO-0001
# VERDE; spec NO-EN-MAIN declarada como primera corrida

python3 tools/corrida0.py run CALC-ENVIPE-RES0028-U4-DERIVADO-0001
# EJECUTADO, exit_code=0, SELLADO

python3 tools/corrida0.py verify CALC-ENVIPE-RES0028-U4-DERIVADO-0001
# REPRODUCE; CONTEXTO=IDENTICO, RESULTADO=REPRODUCE
```

Los hashes de `spec.yaml`, `resultados.json`, `sello.json` y `sello.sha256`
del padre antes y después fueron, respectivamente, `06fcd2a…`, `225bbaa1…`,
`18310f8a…` y `d14825ca…`: sus bytes no cambiaron.

## Decisión y propagación diferida

Pendiente de mesa: adoptar o rechazar la correspondencia propuesta. Este acto
no editó `milpa/tramite.yaml`, snapshots del emisor, `usos.tsv`,
`resultados.tsv`, decisiones, firmas, no-corrido, gobernanza, manifiesto,
tableros ni contadores; `cuenta_gen2` queda `PENDIENTE-DE-MESA` y no se declara
una medición independiente.

Después de CAREO/TRÁMITE-4, si mesa adopta, la integración serial debe:

1. registrar la correspondencia `RES-0028 → CALC::RESULT` anterior;
2. sustituir sólo la oferta candidata U1 por la U4 en una nueva revisión del
   contrato de relevo, conservando el diagnóstico histórico de PR #829;
3. volver a ejecutar el delta canónico y tramitar la decisión de adopción;
4. propagar los registros compartidos y el contador que la mesa determine.
