# ASTRA4-U2 · lote ENCIG 2023, correspondencias y consumo

23/sep/2026. Propietario: `codex/astra4-relevo-1`. Lote de cuatro filas `RES-0001/0002/0007/0008`, misma ola e instrumento. Ningún pin firmado ni cambio en `milpa/` por este lote.

## Cadena ejecutada

COMMIT-1 `3461e8f6`: `CALC-RELEVO-ENCIG23-P83-0001` (spec humana, YAML, medidor) congelado antes de abrir la tabla persona. Preflight VERDE. Primer intento: `RUN: FALLO`, **sin cifra ni sello**, porque el comparador del miembro ZIP redujo el nombre a minúsculas y dejó la constante con `A` mayúscula. El fallo no se convierte en resultado favorable ni se borra.

COMMIT-1 sucesor `66cfff97`: `CALC-RELEVO-ENCIG23-P83-0001-v1_1` cambia solo ese comparador; el estimando y todo lo demás permanecen. Preflight VERDE. COMMIT-2: `run` selló la primera medida de esa sucesora; `verify` dio `CONTEXTO=IDENTICO · RESULTADO=REPRODUCE` para 19/19 RESULT, con tres inputs `COINCIDE`. Sello SHA-256 de `sello.json`: `dfb78694a883ee1f8610f4a01383341ac829b89bb0112a674ac50434efc3c5ce`. Replay asentado en `forense/replay-evidencia.tsv`. `cuenta_gen2=PENDIENTE-DE-MESA`, `adopta=NO`; el cálculo está sellado en disco, no se finge publicación en una vista global.

Primario **SOLANY** (algún inciso 8.3 Sí, persona y `FAC_P18`): `RESULT-RELEVO-ENCIG23-P83-P-SOLANY=0.10300147936160087`, n válido 38 829 de 38 966 personas; masa 5 383 732/52 268 492. Secundario inciso directo **SOL1**: `RESULT-RELEVO-ENCIG23-P83-P-SOL1=0.07286276215258057`, n válido 38 838, masa 3 809 585/52 284 389. Se contaron los códigos 9 y se excluyeron conforme a spec; n de diseño incompleto 0. No hay IC de esta primera medida. Frente al prior asignado `0.62`, la diferencia aritmética de SOLANY es `−0.5169985206383991` puntos de proporción, **sin equivalencia de estimando**.

## Dictamen de correspondencia por fila

| Fila | Prior vigente | Oferta medida / fuente | Identidad y decisión |
|---|---:|---|---|
| `RES-0001` `paga_mordida` | ASIGNADO 0.62 | SOLANY 0.10300147936160087 y SOL1 0.07286276215258057, `CALC-RELEVO-ENCIG23-P83-0001-v1_1` | `NO-EQUIVALENTE-PAGO`: 8.3 pregunta intento, solicitud e insinuación a **persona**; no pago efectuado. No pin ni sustitución. |
| `RES-0002` `tramite_normal` | ASIGNADO 0.38 | complemento SOLANY 0.8969985206383991, mismo CALC y denominador | `NO-EQUIVALENTE-PAGO`: ausencia de solicitud observada no identifica «trámite normal» ni pago ausente. No pin. |
| `RES-0007` `tramite_normal` | ASIGNADO 0.88 | `CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001` da q 0.7955693863799501, **solo eventos con P8_4 observado** (23 100/123 186 eventos); `CALC-ENCIG2023-FLUJO-0001` declara `RESULT-ENCIG23-FLUJO-CORRESPONDENCIA-RES-0007=NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR` | `P8_4` marca circunstancias anteriores por tipo; 81.2% de filas evento carecen de desenlace observado y hay tipos con eventos repetidos. No es probabilidad de pago/normalidad del evento general. No pin. |
| `RES-0008` `paga_mordida` | ASIGNADO 0.12 | mismo agregado: p 0.2044306136200499; `CALC-ENCIG2023-FLUJO-0001` declara `RESULT-ENCIG23-FLUJO-CORRESPONDENCIA-RES-0008=NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR` | Circunstancia de solicitud/intento no equivale a pago. `P8_6` sería otra pregunta y requeriría otro estimando, universo y spec; no se infiere aquí. No pin. |

Los dos CALC anteriores permanecen sellados, con `sello.sha256` presentes. La correspondencia deja de estar pendiente como búsqueda de un RESULT exacto entre esos candidatos: **ninguno** satisface el consumidor de pago. Si mesa quiere cambiar la semántica del consumidor, precisa decisión de producto y un acto nuevo; este lote no la firma. Los cuatro priors siguen como consumo efectivo `LEGACY-GEN1`, aunque la evidencia GEN2 lateral ya exista.

## Filas históricas

`dictamen-historicas.tsv` individualiza las 83 filas que el inventario preliminar había agrupado bajo esa etiqueta. Las 43 del marco-M congelado reciben propuesta `HISTORICO-SIN-RELEVO`, sujeta a firma de mesa y sin tocar el marco. Las 40 de `milpa/procedencia.yaml` **no se declaran históricas por defecto**: `milpa/src/procedencia.py` carga el archivo y `consumibles()` puede entregar sus valores al motor; cada una queda con la prueba por llave y CALC o decisión específica pendientes. El censo distingue así historia sellada de procedencia potencialmente ejecutable.

**Contador y lectura.** Esta medida nueva no reduce por sí misma las 146 lecturas legacy activas rederivadas al arranque de U2. El escritor autorizado de RES-0028 está en la PR separada #1080; un pin de mesa puede reducir trazabilidad sin que cambie un consumidor. Aquí no se alteró ninguno.

El baseline inicial señaló T22 por el anexo `TRANSFER-ASTRA-2026-09-23.md`, archivado verbatim: su mención de una reserva y una adjudicación de cuatro emisiones ENVIPE remite a `FP-260923-GEN2-TRAMITE-FIRMAS-11-05da-01`; no abre una ranura U2. Se añadió la ruta del anexo a `dónde` de esa fila existente, sin alterar su firma ni decisión. `check.py --rapido` posterior: T22 sin FAIL, 0 FAIL total. El anexo original permanece intacto.

## NO-CORRIDO / RESERVAS

No se midió pago consumado de `P8_6`, no se estimó IC, no se autorizó `cuenta_gen2=SI`, no se firmó adopción, no se tocó `milpa/`, celdas-D ni motor.py. Quedan otros lotes de U2. El primer intento fallido de nombre de miembro está documentado arriba.
