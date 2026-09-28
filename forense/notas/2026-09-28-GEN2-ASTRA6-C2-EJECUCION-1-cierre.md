# Nota de cierre · ACTO GEN2-ASTRA6-C2-EJECUCION-1 · 28/sep/2026

**Contadores:** cero cifras para el canon desde las familias 2027 (`celdas_validadas` 219 → 219, `cierre_acto.py` sobre `f73d79e0`). Un CALC GEN2 descriptivo nuevo, `CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001` (RETROSPECTIVA, `adopta: NO`): sellado en disco, no registrado hasta que el canal publique tras el merge (E.7). Su replay está asentado.

## 0 · Arranque

- Caja `/home/pc0/mm-gen2-astra6-c2-ejecucion-1`, rama `acto/gen2-astra6-c2-ejecucion-1` sobre `origin/main` = `16ba3d02`, que es el SHA de redacción, sin commits nuevos.
- 0-bis `e897d3df` con sello de cuerpo `febd6b2d…`. El encargo se copió byte a byte del adjunto (mismo sha256).
- `tools/entorno.py --arranque`: `ENTORNO-DERIVADO = CAJA`, `montado=SI archivos_examinados=515`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`.
- Guard 0.c: sin rama, worktree ni PR previos del rótulo.
- Fusiones de `origin/main` durante el acto: `6b0b6629` y `06099042`, sin conflicto.

## 1 · Compuerta «tercera de caja» y decisiones de mesa (verbatim)

El encargo: «cabe si CORPUS-CACHE-PARQUET-1 ya cerró o si mesa levanta el tope; si no, espera». Estado EJECUTADO a las 10:56:
- PARQUET acababa de hacer su 0-bis (`01aac006`) y no tenía PR;
- C1-LOTE-3 estaba activa;
- PISOS-Y-ADENDAS-1 estaba haciendo polling de su PR.

Respuestas de mesa en esta sesión, copiadas verbatim:
1. A «¿Cómo procedo…?» → **«Dividir: ligero ya»** (P1 y COMMIT-1 ahora; lo pesado espera).
2. A «P2/P3 ya están sellados desde el 26/09. ¿Cómo trato esas piezas?» → **«YA-HECHO: verificar (Recomendado)»**.
3. A «La medida de oferta de E4… ¿Cuándo?» → **«Esta sesión, tras PARQUET»**.
4. A «¿A qué marginal va la medida de exclusión por oferta firmada en E4?» → **«ENIF ahorro (Recomendado)»**.
5. A «¿Corro ya el COMMIT-2 o sigo esperando a que cierre PARQUET?», tras medir que el payload pesa 3,1 MB → **«Correr ya (Recomendado)»**.
6. A «/tmp… está al 100 %…» → **«Solo los deriva»**. Se borraron los siete `/tmp/modelado-deriva-2026-09-26-*`, sin proceso vivo; `/tmp` pasó a 47 %.

Nota sobre (1): la división resultó innecesaria. P3 ya estaba sellada, y la única pieza con dato fue ENIF 2024 (corrida de 24 s, RSS 236 MB). Ninguna sesión pesada corrió en este acto.

## 2 · Premisas del encargo

- [EJECUTADO] expediente v1.0 con 8 filas y los gates declarados: **se sostiene**.
- [SUPUESTO] «las specs existen y sólo falta la forma firmada»: **se sostiene, y va más allá**. También existen las emisiones selladas (COMMIT-2), fechadas el 26/09. Por eso P2 y P3 del encargo, «llevar cada familia a COMMIT-1 y COMMIT-2», **ya estaban hechos**, y lo que bloqueaban B4/E3/E4 era el **COMMIT-3**. Es una premisa caída de logística (el objetivo sigue alcanzable): no se selló nada nuevo, porque habría sido un segundo contendiente sobre las mismas familias (regla 6, PARO c). Decisión de mesa (2).
- E4 «con la medida de oferta al lado»: el texto firmado la pone en la frase de ENVIPE, pero la pieza nace en `1178-ENIF-NC-F` («Cifra de oferta… no obtenidas») y en `interpretacion-y-oferta.md` («junto a cada marginal de ahorro o canal»). Decisión de mesa (4): va a ENIF ahorro.

## 3 · P1 · firmas ejecutadas

Van en `forense/analisis/familias-2027/astra6-enif/enmienda-firmas-c2-v1_0 · astra6-{encig,envipe}/enmienda-firmas-c2-{encig,envipe}-v1_0.md` y `.yaml` (commit `9fa14eea`).

- **ENIF, control del COMMIT-3.** `paquete-control-hashes.json` da 18/18 OK. `verifica_cierre_material.py --verifica --hoja --pruebas` da «23 passed», «INVENTARIO: VERDE; 231 archivos efectivos» y «CONTROL-SUCESOR: VERDE; 18 identidades».
- **ENCIG, identidad.** `evaluar.py` `143cd5b4…`, `cierre.py` `3f1989c2…`, `enmienda-verificacion.json` `22f9857e…` y `.md` `a2134526…` dan OK contra `inventario-portable.json` (corte `1eeb8552`).
- **ENVIPE, unidad de remuestreo.** «Singleton contribuyente» = `singleton_marco`, el estrato con una sola UPM en el marco completo `tper_vic2`. Así lo hace el código congelado (`tools/familias-2027/envipe/medidor.py` l.88–96, l.168–180, l.195–198); `singleton_soporte` (l.149) queda como diagnóstico. En el oro 2025: `singleton_marco=0` en 746 estratos y 13 742 UPM; los singletons de dominio son 83 en U4 y 23 en evasión.
- **FP y NC.** `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06`, `-14` y `-15` pasan a FIRMADA; `firmas-pendientes.tsv` numstat `3 3`. Se cierran `NC-…96f9-01`, `NC-…ad01-01` y `NC-…ad01-03`; numstat `3 3`.

## 4 · Oferta al lado del ahorro · dos commits

- **COMMIT-1 `8c66156c`:**
  - spec humana `astra6-enif/DIN-OFERTA-EXCLUSION-ENIF2024-spec-v1_0.md` (sidecar `3d2d94f0…`), `spec.yaml` y `medidor.py` con guardia;
  - `tests/test_din_oferta_enif2024.py`: 14 passed, 7 ramas terminales por `_valida_outputs` y 5 mutaciones que hacen caer la guardia, con control positivo;
  - `spec-check`: 16 OK · 0 FAIL · 317 718 filas;
  - `preflight`: VERDE.
  - Se congeló antes de leer bytes de casos. La estructura se leyó así: un subagente Sonnet transcribió el cuestionario y el descriptor 2024/2021, y lo verifiqué contra el PDF y el diccionario.
- **COMMIT-2 `f73d79e0`:**
  - `run`: exit 0, 24 s, RSS 236 MB;
  - sello `09e9729c…` COINCIDE;
  - `verify`: REPRODUCE, CONTEXTO=IDENTICO, 57/57;
  - asiento en `forense/replay-evidencia.tsv`, por línea.
- **Primer resultado** (tabla completa en `EXPEDIENTE-v1_1.md` §3):
  - SIN-CUENTA-UB 0.3446 [0.3327, 0.3568];
  - entre no usuarios: OFERTA 0.1037 [0.0917, 0.1162] · PREFERENCIA 0.5374 [0.5171, 0.5570] · OTRO-NS 0.3589 [0.3389, 0.3787];
  - denominadores: n U_B 13 502; no usuarios 4 346.
- **A.8 de reserva, antes de abrir.** La reserva de ola de ENIF 2024 se consumió con el lote de 14 cruces (`FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01`; `FP-…8e53-01`: «la reserva de ENIF 2024 ya no protege esta ola»). `CALC-ENIF-0001` ya había leído `P5_4_*`, `P5_6_*` y `P5_20`. Lo que sigue sin decidir es **el módulo 7 (pagos)**, que no se tocó: HOJA-FIRMAS-21 R06, `NC-260927-GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1-4b11-04`.

## 5 · P2/P3 verificados (YA-HECHO)

- `sello.json`: SELLO_COINCIDE en los cinco `CALC-FAMILIA-2027-*`.
- Pruebas: ENIF 32 passed · ENVIPE 23 · ENCIG 50 · cierre material 23.
- `preflight` BLOQUEADO por `CALC-INMUTABLE-YA-SELLADO` en los cinco, que es lo esperado en un CALC ya sellado. Los dos de ENVIPE tampoco siguen el esquema de `corrida0` (NC `…ba6c-02`, abierta, de otro acto).

## 6 · P4

`familias-2027-estado-v1_1.tsv` (8 filas × 17 columnas, ningún gate vacío), `EXPEDIENTE-v1_1.md` y `hoja-c2-para-mesa-v1_1.md`.

## 7 · Módulo de auditoría v2.16

- ¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA? PROSPECTIVA: las emisiones 2027 del 26/09, que este acto no tocó. RETROSPECTIVA: la oferta 2024. No se mezclan.
- Unidades: persona (oferta, ENIF, ENCIG-MORDIDA, ENVIPE-U4), delito (ENVIPE-EVASIÓN), trámite (ENCIG-PAGO). No se promedian.
- ¿Pobreza confundida con cultura? La partición deja «ingreso insuficiente» (20.8 % de los no usuarios) fuera de PREFERENCIA, justo para no leerlo como gusto. Aun así, «no la necesita» puede ser adaptación racional a ingresos bajos.
- ¿Sesgo de clase? La cohorte sin cuenta es un tercio de los adultos. La cifra nacional no describe a la clase media urbana formal ni al orden indígena-comunal.
- ¿Afirmaciones sobre el corpus escritas a mano? Ninguna: los conteos, sha y estados salen de comandos citados.
