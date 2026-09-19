# Cierre · ACTO GEN2-RECIBO-CODEX-3

Fecha: 19/sep/2026. Entorno: Codex CLI documental, sin abrir microdatos y sin mediciones nuevas. Base al abrir: `843a5f977e024ef5d74863e95856c763bee9e58d`. Compuerta inicial satisfecha por productos: instrucciones v2.14, PR #865 y PR #867 estaban en `main`; PR #866 también estaba fusionado (`782293a33f3849aa2e9400259e62f1702ccd6cf1`).

## Alcance y procedencia

Los adjuntos disponibles se archivaron byte a byte en `forense/encargos/insumos-gen2-recibo-codex-3-2026-09-19/`, con `MANIFIESTO-RECIBO3-SHA256.txt`; tres insumos idénticos ya archivados se citan por su ruta canónica y no se duplican. El original quedó incorporado en `main` mediante #872 como `forense/encargos/2026-09-19-GEN2-RECIBO-CODEX-3.md`; sus seis semillas `PARA-v2.15` se conservan allí.

## Decisiones y cierres aplicados

| Objeto | Resultado |
|---|---|
| D1 / marcador | Dueño operativo `GEN2-MARCADOR-REDISENO-1` (Claude); el sucesor Codex anterior queda cancelado/sustituido sólo para trabajo futuro. |
| D2 / pisos #866 | Veto acotado a los cuatro `CALC` originales. No alcanza a sucesores ni a los 20 C2; medir no adopta. |
| D3 / ENCIG original | `FP-387` ABIERTA. La relación técnica de sucesión no decide `cuenta_gen2`, `SUPERADO` ni clasificación. |
| Piloto 1 y 2 | FP-379, su enmienda D9 y FP-385 representadas por objeto en `decisiones.tsv`; registrar firma no prueba consumo. |
| NC-0274, NC-0328, NC-0227, NC-0255, NC-0256 | CERRADAS por las decisiones citadas de TRÁMITE-5. |
| NC-0237 | Sigue ABIERTA; diferida a F6. |
| NC-0254 | CERRADA; `RES-0043/0044` siguen `SIN-CANDIDATO` con sucesor ENADID 2023. |
| NC-0024, NC-0076, NC-0239, NC-0300 | Siguen ABIERTAS; sucesor vigente Claude. PR #868 no es cierre. |
| NC-0305 | CERRADA por producto real de #865: contrato v0.6, vocabulario y pruebas; no por etiqueta. |
| DEM-AHORRO / #855 | `NC-0335` ABIERTA; el handoff no decide su disposición. |

`tools/relevo_usos.py` consume las dos decisiones exactas de ENADID y genera `relevo-usos-v1_0.tsv` con columna `sucesor`; 13 pruebas dirigidas de relevo pasan. Foto del 19/sep: 208 slots, 156 `SIN-CANDIDATO`, 12 `CANDIDATO-GEN2`, 7 `LISTADO-PARA-MESA`, 22 `YA-ADOPTADO`, 8 no adoptables, 2 conflictos y 1 veto.

## Recibos de automatización

| PR | Merge | Producto recibido | Medición atribuida aquí |
|---|---|---|---|
| #851 | `fe3a745929c65db103a4ff872009fbaac33c81ea` | snapshot derivado del universo del 17/sep y actualización del tablero | 0 |
| #852 | `80efb751efe2872712f9c6bfb456948731f88fed` | proyección de demanda activa y censo raíz | 0 |
| #853 | `e46e7e44db55a73ea87a6e74362b9f186fe9f9f7` | estados de investigación ADQ y nota de corrida | 0 |
| #855 | `89610c54429cca3e0f181902f23400ea878aee79` | handoff de resultado/salud, prueba y cableado de automatización | 0; deja `NC-0335` |
| #866 | `782293a33f3849aa2e9400259e62f1702ccd6cf1` | verificador aislado, escritor acotado, 41 asientos de replay y cuatro pisos originales | 0 en este acto |

## Replay y pisos

La fuente integrada contiene además el asiento `REPRODUCE/IDENTICO` de `CALC-ENADID-0001` fusionado por #869. #871 restableció el acceso de ENCRIGE y ENSANUT y publicó tres asientos de pisos sucesores. La proyección ordinaria de 215 corridas arroja cero transiciones y `_para_si_pisa_replay(..., set())` pasa; por eso `NC-0315` queda demostrada con el guardia real. Un `verify` que imprime y no asienta sigue siendo media verificación.

Los cuatro pisos originales de #866 quedan preservados, vetados y `SUPERADO→`. #871 publicó tres sucesores distintos: ENVIPE `0002`, ENCIG `0002` y ENIF `0003`, todos `REPRODUCE/IDENTICO`, con 53/57 identidades construidas y cuatro ENIF dictaminadas `NO-CONSTRUIBLE`. Corrige persistencia/código real, cardinalidad, universos ENCIG, `BP1_20`, semántica documental de `P5_6` y salida numérica por celda. Los sucesores no heredan el veto ni quedan adoptados; su contador sigue `PENDIENTE-DE-MESA`.

## Corrección del estado e infraestructura

Se reconstruyó §13 de `estado-programa-v1_14.md` desde respaldo comprobable, preservando §0–§12 y L0. Distingue sellos físicos, filas publicadas, clasificación GEN2 y consumo; corrige 97 frente al falso denominador 117; separa decisión, representación y uso activo; no convierte las incompatibilidades de escala en una nueva decisión. `INFRAESTRUCTURA-v1_0.md` registra celdas-D, la capa de identificación, catálogo/replay y la forma vigente del relevo. La huella histórica de rutina queda enmendada para que FAIL adjudique y WARN sea estado, conforme a ADR-539.

## NO-CORRIDO / RESERVAS

- El original y las seis semillas `PARA-v2.15` quedaron preservados por #872; este delta no construye guardias nuevos.
- `FP-387` requiere decisión de mesa sobre el ENCIG original y el contador.
- `NC-0237`, `NC-0024`, `NC-0076`, `NC-0239`, `NC-0300` y `NC-0335` permanecen abiertas por sus objetos propios.
- `NC-0313` permanece abierta: el replay global DIN conserva `NO-REPRODUCE`; 220 resultados sustantivos, incluidos puntos/IC C2, reproducen, pero el snapshot de orden no.
- `NC-0285` permanece abierta sólo por el encargo #831 fuera del directorio canónico; `NC-0335` permanece abierta por la disposición de DEM-AHORRO. Las demás piezas de replay/pisos aquí recibidas cierran individualmente por producto.
- PR #868, SHA `9e9e89225f0d986cf51b955940ebee7526809f1b`, sigue siendo propuesta abierta con check fallido; no se incorporó ninguna de sus vistas ni código.

## CONSUMIDO

Se consume por el PR de este acto, después de revisión humana; este archivo no autoriza su propio merge.
