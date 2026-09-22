# GEN2-DIN-CREDITO-PISOS-1870-RUN-1 · cierre

ACTO GEN2-DIN-CREDITO-PISOS-1870-RUN-1 · 22/sep/2026 · CAJA · Opus 5.5 (el encargo sugería Sonnet; D-13 permite subir) · MODO RÍGIDO · raíz `009f` (0-bis `009fb76b`) · base `origin/main` `0232aad7`, redactado sobre `ccd7c0eb` (ancestro).

**CONTADOR:** cero corridas nuevas. Una corrida ya sellada (`CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001`) queda re-verificada en caja. Su asiento E.7 lo trae #1004, no este acto (§4). Su fila en la vista **no** viaja en este PR: sigue «sellada en disco, no registrada» hasta que mesa corra `registro` sobre main (NC -01). No adopta.

## 1 · Premisa que cayó y qué se hizo en su lugar

El encargo pedía `run` de un CALC que decía congelado y no corrido («**0** filas en `corridas.tsv` y `replay-evidencia.tsv`»). Verificado contra `origin/main`:

- El CALC **ya corrió sobre ENIF 2021 real** en `17d27f82` (21/sep 20:31, COMMIT-2 de `GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1`). En main están `resultados.json` (2 941 RESULT), `sello.json` y un `ejecucion.json` con `exit_code 0`, el input `enif2021_csv` `0f314fa3…` y `corrida_id …--f1469f52d4b3`.
- Su fila en la vista la revirtió `344739d1` («CI: revierte derivados protegidos (corridas.tsv/resultados.tsv)», 21/sep 21:25). Por eso `grep -c RECORTE1870 data/corrida0/corridas.tsv` da 0.
- El §1 pedía además un `medidor_ejecutado_al_congelar` distinto de «solo sintético». Ese campo es del COMMIT-1 y describe a propósito la prueba sintética; un run no lo cambia.

Un `-0002` idéntico habría sido un segundo «primer resultado» del mismo procedimiento (PARO b/d). El acto se detuvo con cero commits y lo llevó a mesa. Mesa reescribió el objetivo en `forense/encargos/2026-09-22-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-ADENDA-1.md` (verbatim, sellada al recibirse):

> OBJETIVO reescrito: preflight + verify del -0001 existente (réplica sobre ENIF 2021, dos ejes), asiento en replay-evidencia.tsv con cita a 17d27f82, registro --verifica --escribe --lote del -0001, nota. «Hecho» = verify REPRODUCE · fila en corridas.tsv · asiento con los hashes de identidad. Se retira el criterio sobre medidor_ejecutado_al_congelar: es un campo de COMMIT-1 y describe la prueba sintética a propósito; error de redacción de dirección.

**Segunda premisa que cae, ahora sobre la adenda: «fila en `corridas.tsv`» no se puede cumplir desde un PR.** `.github/workflows/verify.yml:542-546` bloquea todo PR que toque un archivo `# DERIVADO — NO EDITAR` (firma de mesa del 21/sep §2(2), `GEN2-TUBERIA-EFICIENCIA-1`). El job de push a main (`verify.yml:358-391`) sólo re-deriva `marcador_segmento` y `demanda`, y deja `registro` fuera a propósito («exigen `--lote` (juicio sobre qué transición de replay puede cambiar)»). Es logística y el resto del objetivo sigue alcanzable. Hice todo menos commitear los derivados, medí la fila en seco y dejé el paso de escritura a mesa (NC -01).

## 2 · P1 · preflight

`python3 tools/corrida0.py preflight CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001` (exit 1):

- `spec_md_sha256` `[EN-MAIN-COINCIDE]` `5f590237…`; 2 941 ids de resultados `[UNICOS]`; 6 inputs `[UNICOS]`.
- Los 6 inputs salen `[COINCIDE]`: `enif2021_csv` `0f314fa3…` en `data/raw` (caja), `MEDIDOR-EJES-0003` `d069f38b…`, `MEDIDOR-PISOS-ENIF2021-0001` `a8f97e4c…`, `PISOS-REJILLA-METADATOS` `1715da93…`, `PISOS-FORMALIDAD-METADATOS` `8cf59f8b…` y `CREDITO-COMPARABILIDAD-TEXTO` `0245333e…`.
- `script_blob_sha256` `cd07759e651ef1960a1970d361dbf1aca096cfd745e5bd82949a0310128a8fc6`; `spec.yaml` `ed44de94de278df681e9b84678198093297fb44fa056e088ffc0e7f7eef4f094`.
- `[LIMPIO]`, `[SELLO_COINCIDE]`.
- Único bloqueo: `PRE-FLIGHT: BLOQUEADO calc_ya_sellado=CALC-INMUTABLE-YA-SELLADO`. Es la negativa de `run` sobre algo ya sellado (E.3), la que se esperaba.

Ninguna edición a lo congelado.

## 3 · P2 · verify (dos ejes)

`python3 tools/corrida0.py verify CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001` (exit 0, 9 s):

```
[1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
[2/5 SPEC.YAML] IDENTICO
[3/5 INPUT COINCIDE] ×6
[4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO  (FP-358: no gatea)  parametros=IDENTICO  seed=IDENTICO  dependencias=IDENTICO
VERIFY: REPRODUCE   (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)
```

Conteo sobre la salida: 2 941 líneas `[5/5 RESULT REPRODUCE]` de 2 941 RESULT (delta 0.0 en todo número). La réplica en proceso aislado (`python3 tools/verifica_aislada.py <CALC> --salida …`) da lo mismo: `REPRODUCE`/`IDENTICO`.

RESULT, tal como los declara el `spec.yaml` sellado:
- `tipo`: 2 941/2 941 (`proporcion` 1 080 · `entero` 881 · `flotante` 600 · `texto` 380).
- `unidad`: 2 941/2 941.
- La **escala** no es campo por RESULT: la fija el `tipo` (proporción en [0,1], n sin ponderar, denominador ponderado).
- El **universo 18-70** tampoco es campo por RESULT. Se declara a nivel CALC (`universo:` del `spec.yaml`, «Persona elegida 18-70…»), y dos RESULT lo dejan medido: `EDAD-RECORTE-MIN`=18 y `EDAD-RECORTE-MAX`=70.

Lo que P2 pedía «en cada uno» se cumple para tipo y unidad; para escala y universo se cumple a nivel CALC. No edito el spec congelado para cambiarlo.

Tipo del CALC: `PISO-PERSISTENCIA-POR-EJE`. Cifras de cabecera citadas del commit que selló (`17d27f82`) y re-verificadas hoy: 12 406 personas de 18-70 (frente a 13 554 de 18+ en #943) y `K1-NACIONAL-TODOS-P` = 0.3268 (frente a 0.3125).

## 4 · P3 · asiento y registro

- **Asiento E.7: retirado para no tener dos escritores.** Commiteé una fila propia (`c38af42d`). Al fusionar main para cerrar vi que el PR #1004 (`GEN2-PENDIENTES-CAJA-1`, abierto el 22/sep a las 20:16Z, antes de mi push, `MERGEABLE`) ya asienta el mismo `corrida_id` (`…RECORTE1870-0001--f1469f52d4b3`) con el mismo veredicto, `REPRODUCE`/`IDENTICO` (`VERIFY-AISLADO · GEN2-PENDIENTES-CAJA-1`). Retiré la mía: `forense/replay-evidencia.tsv` queda idéntico a `origin/main`, con cero líneas de diff. El asiento vigente es el de #1004. Mi verify de §3 es una corroboración independiente, en otro worktree y otra sesión, y deja en esta nota los hashes de identidad: `spec_yaml_sha256` `ed44de94…`, `script_blob_sha256` `cd07759e…` y `input_sha256_efectivos` = los 6 de §2. Si #1004 no se fusiona, el asiento queda por hacer (NC -03).
- **Registro, en seco:** `python3 tools/corrida0.py registro --verifica --lote CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001`, sin `--escribe` porque la guarda de CI no deja que los derivados viajen. La fila que escribiría es `…RECORTE1870-0001--f1469f52d4b3 · OFERTA · SELLADA · GEN2 · cuenta_gen2=SI · adopta=NO · etiqueta de la spec · NUEVO · COINCIDE · REPRODUCE · IDENTICO · VERIFY-EN-ESTA-SESION`.
- **Estado de la vista, medido en la misma pasada:** el diff que `--escribe` pondría sobre el árbol de main es `corridas.tsv` **+44 / −26**, `resultados.tsv` **+21 951 / −1 502** y `usos.tsv` sin diferencia (231). La vista publicada tiene 285 filas de corrida y la derivación da 303. La vista de main va 18 corridas atrás, no sólo la de este CALC (NC -02).
- **`status` antes = después**: el `status` corre en memoria, así que ya contaba esta corrida; el PR no toca derivados. `# derivado de 303 corridas · 47255 resultados · 231 usos`, `N_corridas_selladas=154`, `N_resultados_gen2_sellados=44177`, `N_resultados_gen2_adoptados_activos=72`. El contador de `status` no miente. Lo que miente es la vista publicada (`corridas.tsv`), que es lo que lee quien no re-deriva.
- **Firma `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01`:** `FIRMADA` en #1001 (`GEN2-TRAMITE-FIRMAS-6`, abierto, `CONFLICTING` al 22/sep 14:0x). Es lectura tipo (3): se cita como #1001 y no se asienta aquí. Así lo dice mesa en la adenda: «No la necesitas para registrar: la firma autorizaba el run, y el run ya ocurrió bajo el contador del acto padre».

## 5 · K2-BANCARIA-HISTORIA

`CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001` está en la misma situación: corrió en `17d27f82`, tiene `resultados.json` y la vista de main lo pone `NO-CORRIDA`. Según la adenda, entra en lote sólo si mesa confirma que la sesión del worktree `~/mm-gen2-din-credito-k2-historia-run-1` está muerta. Evidencia que llevé a mesa (22/sep 14:19):
- worktree creado a las 13:45 sobre `ccd7c0eb`;
- cero commits y árbol limpio;
- ningún archivo modificado después de las 13:46;
- sin rama remota (`git ls-remote origin 'refs/heads/*k2*'` vacío).

Lo que resolvió mesa está en §7.

## 6 · Hallazgos de aparato

Ver NC -02 y la línea de `forense/hallazgos.md`. `344739d1` hizo lo que manda la firma del 21/sep: los derivados no viajan en un PR. Lo que falla es el tramo de después: nadie corre `registro` sobre main, así que toda corrida sellada desde entonces queda fuera de la vista publicada. El caso de este acto es uno de 18.

## 7 · Respuesta de mesa sobre K2

Verbatim: «termina el encargo». Mesa no confirmó que la sesión de K2 esté muerta. Se aplica la rama conservadora de la adenda: K2 no entra en el lote y este acto no lo toca. Además, #1004 ya asienta K2 (`…K2-BANCARIA-HISTORIA-0001--78664b318a0c`, `REPRODUCE`/`IDENTICO`), así que el asiento de K2 tampoco es de este acto. Queda en `## NO-CORRIDO` (NC -04).

## 8 · Firma ff56-01

`FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01` pasó a `FIRMADA` en main al fusionarse #1001 (`31da26e0`, `ADR-260922-GEN2-TRAMITE-FIRMAS-6-7c2c-01`) mientras corría este acto. Ahora es lectura tipo (1). Este acto no la asienta: lo hizo el trámite (A.12).
