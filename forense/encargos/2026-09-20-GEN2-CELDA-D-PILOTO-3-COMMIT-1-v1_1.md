# ENCARGO · ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1

**Archivado verbatim por 0-bis A.3 el 20/sep/2026.** Texto recibido de dirección (input a la sesión del `ACTO GEN2-CELDA-D-PILOTO-3-EJECUCION`, PR #924), sin editar. Base del acto: HEAD de PR #924 (`25fe4dd0` = `origin/main` `98c00806` + los cuatro commits de #924), porque las filas `FP-399`/`FP-400` y `NC-0407`..`NC-0410` que este acto firma y enmienda solo existen ahí; #924 estaba OPEN al abrir (el merge es de mesa). Rama apilada: `acto/gen2-celda-d-piloto-3-commit-1-v1_1`.

---

INPUT DE DIRECCIÓN · 20/sep/2026 · a la sesión del ACTO GEN2-CELDA-D-PILOTO-3-EJECUCION (CAJA)
El lanzamiento de mesa con este texto es el sello de las dos firmas de abajo.
PR #924 se fusiona como está (PARO bien cerrado). Lo que sigue es un ACTO NUEVO, en rama nueva,
en esta misma sesión: GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1.

0. Tu PARO fue correcto en sus dos mitades. El encargo de dirección decía «código ya
   congelado» sin haber abierto `medidor.py`: son 191 líneas cuyo `medir()` lanza
   NotImplementedError. Dirección verificó que el directorio existía, no que midiera.
   Y tus dos observaciones finales entran tal cual a este acto (puntos 3 y 5).

FIRMAS DE MESA
> FP-399 · S2: "El código 97 es edad real censurada y se reconoce como tal. En 2021 y 2023 el
> residuo de F1-bis es 100 % código 98 (no especificada): la regla no está sacando población
> real y se mantiene. Para 2025, el COMMIT-2 cuenta los trámites con código 97 con una sola
> variable de agrupación y lo reporta. Siguen fuera del universo del cruce para conservar la
> comparabilidad con la rejilla sellada del árbitro (60–96). Si superan el 1 % de los
> trámites de la banda 60+, el veredicto lleva la marca RESERVA-S2; no detiene el piloto."
> FP-400 · quién congela: "El COMMIT-1 v1.1 lo congela esta sesión, en caja. Hereda VERBATIM
> de la spec v1.0: estimando, rejilla, las 15 PUNTUADA y la FUERA-DE-SOPORTE ex ante,
> candidatos y fórmulas, λ = 0.8937949410086089, soporte, adjudicación, lectura secundaria y
> B-bis. Cambian solo tres cosas: el cuerpo de medición, la semántica de la guardia S2 (según
> FP-399) y la cláusula de validación del punto 3. Los COMMIT-2 y 3 los ejecuta OTRA sesión
> (F3). Nadie ha visto ENCIG 2025: revisar el COMMIT-1 es legítimo (E.6)."

1. PRIMERA LÍNEA DE LA SPEC v1.1, obligatoria — dirección lo leyó en
   `tools/medidor_gobierno_digital_encig25.py:12,38`: el universo `N_TRA=='01'` es **PAGO
   ORDINARIO DEL SERVICIO DE LUZ**. El estimando es "proporción de pagos de luz hechos por
   canal digital ({4,5}) entre los de canal válido", por edad × escolaridad. No es "gobierno
   digital" en general ni "confianza en el Estado". Confírmalo por texto del cuestionario
   (qué trámite es el 01 en 2021, 2023 y 2025 — ya leíste el catálogo para S1) y escríbelo
   así. El nombre de la regla no se cambia aquí; el rótulo del estimando sí se precisa.

2. CUERPO DE MEDICIÓN. Carga de payloads por id de manifiesto; unión trámites↔personas
   **por llave (`ID_PER` o la que el FD declare), nunca por índice de fila**; marginales por
   una sola variable; bootstrap de diseño con réplicas y semilla leídas del precedente y
   citadas; C2, C1a, C1b, S½, Sλ réplica por réplica; en archivo o función SEPARADA, la
   derivación de R(a,b) y la adjudicación, que se niega a correr si no existe el sello de
   emisiones. La ola es PARÁMETRO del medidor, no constante.

3. VALIDACIÓN DE «CONGELADO» — tu propuesta, endurecida. Un COMMIT-1 no está congelado si su
   punto de entrada nunca corrió. Dos pruebas, las dos obligatorias:
   a) sintética: `medir()` de punta a punta sobre un fixture chico; produce las cinco
      emisiones por celda con IC, y la adjudicación corre sobre un R sintético;
   b) **de oro, sobre ENCIG 2023** (ola anterior, NO reservada): el mismo código, con
      ola=2023, debe reproducir los `p(a,b)`, `n` y δ ya sellados en
      `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`, a tolerancia de redondeo, sobre el universo
      de F1-bis. Si no reproduce, el cuerpo está mal: se corrige ANTES de congelar. Esto
      prueba el join, el universo y los ponderadores sin tocar 2025.
   El resultado de (b) NO es una medición nueva: es control; no se sella como CALC.

4. GUARDIA DE RESERVA. Durante todo este acto, ENCIG 2025 no se abre: ni respuestas, ni
   conteos. Test que falla si el COMMIT-1 deja en el árbol cualquier salida derivada de
   `encig25*`. La guardia S2 del código pasa de paro mecánico a: exige que FP-399 figure
   FIRMADA en `firmas-pendientes.tsv`, y cuenta el código 97 en el COMMIT-2.

5. HALLAZGOS, dos líneas `PARA-v2.15`: (i) "«congelado» exige que el punto de entrada haya
   corrido al menos sobre datos sintéticos; un medidor cuyas pruebas solo ejercitan guardias
   y constantes no es un COMMIT-1" (tuya); (ii) "cuando un encargo y una spec congelada
   discrepan sobre si algo detiene, manda la spec — es el pre-registro — y la discrepancia
   se resuelve por firma antes de ejecutar, no durante".

6. CIERRE. Spec v1.1 + sidecar; la v1.0 queda SUPERADA-SIN-CORRER (n_res = 0), no se borra.
   El CALC-id: `CALC-GOB-DIGITAL-EXE-EMISIONES-0001` no se ejecutó nunca; si la casa permite
   suceder una spec no corrida con el mismo id, úsalo y dilo; si no, `-0002` — verifica el
   id libre en toda rama viva antes. NC-0407..0410: enmienda fechada con este sucesor.
   FP-399 y FP-400 → FIRMADA. Registra la celda-D en estado SPEC-CONGELADA.

7. LO QUE NO HACES: no ejecutas COMMIT-2 ni 3; no abres 2025; no cambias un umbral, un
   candidato, ni λ; no renombras la regla del motor; no tocas el CALC de persistencia.

---

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «Los COMMIT-2 y 3 los ejecuta OTRA sesión (F3)» — COMMIT-2 emisiones sobre 2025 | DIFERIDO-A:sesión de CAJA distinta (F3) | `N_corridas_selladas` +0; el par sigue `RESERVADA`; `NC-0407` | `corrida0 run CALC-GOB-DIGITAL-EXE-EMISIONES-0002`, vista y replay en el mismo acto |
| COMMIT-3 R y adjudicación; llenar la celda-D; re-derivar marcador | DIFERIDO-A:sesión que ejecute COMMIT-3 tras COMMIT-2 empujado | `NC-0408`, `NC-0409`, `NC-0410` | `corrida0 run CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` |
| «Registra la celda-D en estado SPEC-CONGELADA» con unidad TRÁMITE | DECISIÓN-DE-MESA-PENDIENTE | Registrada con `unidad_objetivo: persona` (precedente `TRA.evade_norma`; enum no admite evento); `FP-393` sigue ABIERTA | `FP-393` |
| Lectura de `n(a,b)` 2025 en COMMIT-2 (v1.0 §4 «sólo se puede verificar en el COMMIT-2») | SUSTITUIDO-POR:lectura en COMMIT-3 (E.6, una variable en emisiones) | Regla de soporte intacta; el COMMIT-2 emite `SOPORTE-HISTORICO`; absorbe: clasificación definitiva en `adjudicacion.py`; huérfano: nada | spec v1.1 §4; si mesa quiere el conteo en COMMIT-2, una línea + firma |
| `tests/test_piloto3_v11.py` en CI | NO-VERIFICABLE-AQUÍ | CI no tiene numpy/pandas/pytest (FP-398 de mesa): la fila del censo lo declara `NECESITA-DEPENDENCIA(pytest)` y el job `guardias` lo salta en voz alta; corre en CAJA (7/7) | `FP-398` |
| IC de C1a | NO-VERIFICABLE-AQUÍ | Las réplicas de 2023 no se sellaron; C1a se emite como punto con `IC-CAUSA = SIN-REPLICAS-SELLADAS-2023`; C1a es referencia, no piso | SIN-ASIGNAR (re-bootstrap de 2023 sería un CALC nuevo) |

## CONSUMIDO

Ejecutado por `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1`, **PR #926** (apilado sobre PR #924), 20/sep/2026 (CAJA, Opus 5). Congela spec v1.1 + `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` + `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`, validados por prueba sintética y oro sobre 2023 (7/7); `FP-399`/`FP-400` FIRMADAS; celda-D SPEC-CONGELADA; `ADR-568`. No ejecuta COMMIT-2 ni 3; ENCIG 2025 no abierta. Nota: `forense/notas/nota-2026-09-20-gen2-celda-d-piloto-3-commit-1-v1_1.md`.
