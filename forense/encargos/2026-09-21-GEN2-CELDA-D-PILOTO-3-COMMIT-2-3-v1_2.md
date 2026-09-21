# ENCARGO · ACTO `GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2` · se abre ENCIG 2025 por primera vez: emisiones selladas, después sus huellas, después la realidad y el veredicto — con el código que ya está congelado y ni una línea más

> ENTORNO: **CAJA** (máquina local, corpus montado). El hook de arranque imprime `ENTORNO-DERIVADO`; si no dice `CAJA`, PARA en una línea. Un worktree nuevo nace sin `data/raw` ni `data/raices.local.yaml`: se enlazan, no es PARO.

**CABECERA** · SHA de redacción: `origin/main = 73d7c816` + `PR #944` (cabeza `48a4aa54`). **No arranques si `#944` no está en main**: sin él los `spec.yaml` no traen el cableado y `run` devuelve `NO-EJECUTADO` por construcción. Si main se movió por otra cosa, re-deriva; no es PARO · **una sola sesión, rama propia** · **MODELO: Opus** · **MODO: RÍGIDO** — reserva de evaluación y spec congelada: la latitud es sobre logística, nunca sobre el procedimiento · **F3 (`FP-400`, `FP-407 a`): quien congela no ejecuta.** Congelaron `pc0-77` (v1.1, `#926`) y la sesión que paró en `#941` y re-congeló en `#944` (v1.2). **Si eres cualquiera de las dos, o tienes en contexto los diseños A/B o el careo del piloto 3, PARA y dilo** · **CONTADOR:** sella dos corridas; `cuenta_gen2 = SI` para ambas, **ya firmado y ya asentado** en `data/corrida0/decisiones.tsv` por `#944`; no adopta; `adoptados_activos` no debe moverse · **FP/ADR/NC:** deriva al cierre, no heredes.

---

## 1 · OBJETIVO

Ejecutar, tal como está congelado, el tercer piloto pre-registrado del programa: **¿se transporta a 2025 una interacción edad × escolaridad que fue estable en 2021 y 2023, cuando el nivel de la cantidad se movió once puntos?** Es la primera vez que alguien del programa abre ENCIG 2025 por dos variables, y se hace una sola vez.

Tres actos seguidos de este piloto se perdieron por cableado (`#903`, `#924`, `#926`) y un cuarto paró antes de abrir nada (`#941`). **`#944` dejó probado el conducto**: preflight de EMISIONES en `VERDE` en caja con el payload `COINCIDE`, y ADJUDICACION bloqueada sólo por los dos inputs que crea el COMMIT-2. Este acto es el que mide.

**«Hecho» significa:** `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` sellado y en origin; las huellas de sus dos salidas escritas en el `spec.yaml` de ADJUDICACION y en origin; `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` sellado; veredicto y B-bis resueltos con las palabras de la spec; las dos corridas en la vista con su asiento de replay (E.7) y **contando** (`cuenta_gen2 = SI` resuelto por el registro); celda-D llena; marcador re-derivado.

---

## 2 · FIRMAS DE MESA — todas dadas, verbatim; no se pide ninguna

**`FP-389` · F1-bis** (20/sep) — rejilla de edad y coherencia sobre el universo sin residuo; elegibilidad con tolerancia de ⅓; 18–29 × hasta primaria `FUERA-DE-SOPORTE` ex ante.

**`FP-399` · S2** (20/sep) — «El código 97 es edad real censurada y se reconoce como tal. […] Para 2025, el COMMIT-2 cuenta los trámites con código 97 con una sola variable de agrupación y lo reporta. Siguen fuera del universo del cruce […]. Si superan el 1 % de los trámites de la banda 60+, el veredicto lleva la marca RESERVA-S2; no detiene el piloto.»

**`FP-400` · F3** (20/sep) — «El COMMIT-1 v1.1 lo congela esta sesión, en caja. […] Los COMMIT-2 y 3 los ejecuta OTRA sesión.»

**`FP-393` · unidad** (21/sep, cuaderno renglón 4.2) — «unidad evento — a». FIRMADA; el contrato de celda-D admite `evento` (`tests/test_celdas_d.py:79`).

**`FP-407`** (21/sep) — «(a) El COMMIT-1 v1.2 lo congela la sesión que paró en #941 u otra sin contexto de los diseños A/B ni exposición a ENCIG 2025. Quien congela no ejecuta: los COMMIT-2/3 los corre otra sesión, como en FP-400. (b) Cuentan como "hereda verbatim" cuatro llaves de cableado en cada `spec.yaml` […]. Las huellas de esos dos inputs se escriben en un COMMIT-3a, después de sellar las emisiones y antes de derivar R, como en el piloto 1. (c) La firma de contador del piloto se hereda al v1.2 y a sus COMMIT-2/3: los CALC-id no cambian. Este acto la asienta como fila de `decisiones.tsv` para que cuente.»

**Firma de contador** — «Cuentan (cuenta_gen2 = SI) CALC-GOB-DIGITAL-EXE-EMISIONES-0002 y CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001, sea cual sea el veredicto: una prueba pre-registrada que sale "nadie vence" o "falsador débil" cuenta igual que una que sale "vence".»

---

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo

- `[LEÍDO]` Spec v1.1 (`forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md`, sin cambios desde `826bf3a1`): estimando = proporción de pagos ordinarios del servicio de luz (`N_TRA == 01`) por canal digital `{4,5}` entre canal válido, **unidad TRÁMITE**; 16 celdas, 15 `PUNTUADA`; candidatos C2, C1a, C1b, S½, Sλ con λ = 0.8937949410086089; `PCG64(20260919)`, 10 000 réplicas en bloques de 50; unión `sec_7 ← residentes` por `ID_PER`, m:1, validada. Spec :43: el tercer requisito de soporte (n ≥ 200 en 2025) agrupa por dos variables y sólo lo lee el COMMIT-3. Spec :62: la adjudicación se niega si falta el sello de emisiones, si su `sha256` no coincide, o si el C2 recalculado no reproduce el sellado a 1e-9.
- `[LEÍDO]` `data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/spec.yaml`, bloque `secuencia_commits` escrito por `#944`: **`commit_2`** corre y sella EMISIONES, vista y replay, push, `git ls-remote` confirma; **`commit_3a`**, «la misma sesión del COMMIT-2, en commit aparte y ANTES de derivar R: escribe en ESTE spec.yaml la llave sha256 de los inputs emisiones_resultados y emisiones_sello […] y verifica corrida0 preflight […] = VERDE. Ninguna otra línea de este archivo cambia»; **`commit_3`** corre ADJUDICACION. **Esa es la secuencia; este encargo no la repite con otras palabras.**
- `[LEÍDO]` Nota de `#944`, líneas 3 y 62: en caja, preflight de EMISIONES → `VERDE`, payload `encig25_base_datos_csv.zip` **`COINCIDE`** (37 624 925 B); `firmas_pendientes_tsv` `COINCIDE` contra la copia inmutable `fp399-firmada-826bf3a1.tsv`.
- `[LEÍDO]` Nota de `#944`, línea 9: la sesión que congeló el v1.2 es la que paró en `#941`, y se declara fuera de los COMMIT-2/3.
- `[LEÍDO]` `#944` añadió dos filas `cuenta_gen2=SI` en `data/corrida0/decisiones.tsv`, una por CALC. `[SUPUESTO]` que el registro las resuelve a `SI`: **verifícalo antes de correr** con `_cuenta_gen2_resuelto` (`tools/corrida0.py:3702`).
- `[LEÍDO]` Nota del COMMIT-1 v1.1 (`forense/notas/nota-2026-09-20-gen2-celda-d-piloto-3-commit-1-v1_1.md:41`): en caja, `test_b_oro_2023_reproduce_los_sellados` PASSED — 16 n exactos, |Δp| = 0.0, |Δδ| = 1.7e-16, |ΔIC| < 1e-9. `#941` la re-corrió: 7/7. **Tú la corres otra vez antes de abrir 2025.**
- `[LEÍDO]` Nota de `#941`, línea 91: `tools/asienta_replay_aislado.py --help` **escribió una fila ajena** en `forense/replay-evidencia.tsv` —el script no tiene `argparse`—. Para asentar el replay, léelo antes de invocarlo y llámalo con los argumentos que el código espera.
- `[EJECUTADO]` `data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml` existe, re-congelada por `#944` sólo con un comentario de cabecera.
- `[SUPUESTO]` que nadie ha abierto ENCIG 2025 por dos variables desde el 20/sep. Busca en el repo y en tu disco restos que por nombre lo sugieran; si hay alguno, ruta, fecha y tamaño —no lo abras— y **PARA antes del COMMIT-2**.

---

## 4 · YA HECHO / YA DECIDIDO

`#894`/`#903` (P0 en nube, selección del cruce) · `#924` (S1 y S2 por texto; PARO por medidor vacío) · `#926` (COMMIT-1 v1.1 con cuerpo y prueba de oro) · `#941` (PARO por preflight; ENCIG 2025 no abierta) · `#944` (COMMIT-1 v1.2: cableado, secuencia, filas de contador). **Nada de COMMIT-2 ni 3 existe**: los dos directorios CALC traen `spec.yaml`, su código y la copia de `firmas-pendientes`, y ningún `ejecucion.json`, `resultados.json` ni `sello.*`. Verifícalo con `ls` antes de empezar: si ya hay salidas, alguien corrió, y eso es PARO (h).

---

## 5 · PIEZAS — orden estricto; cada una gatea a la siguiente

**P0 · Antes de tocar 2025.**
1. Sidecar de la spec: `cd forense/prereg-caja && sha256sum -c GOB-gobierno-digital-exe15-spec-v1_1.sha256` → OK.
2. `python3 -m pytest tests/test_piloto3_v11.py`: **los 7 deben pasar aquí**, incluida la de oro sobre ENCIG 2023. Si la de oro falla: **PARO (f)**. El código congelado ya no reproduce lo sellado y no se abre la ola.
3. `corrida0 preflight CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → `VERDE` en tu caja. Los avisos que no bloquean, como `spec_md_no_esta_en_origin_main`, se admiten.
4. `cuenta_gen2` resuelto a `SI` para los dos ids.

**P1 · COMMIT-2 · las emisiones.** `python3 tools/corrida0.py run CALC-GOB-DIGITAL-EXE-EMISIONES-0002`, sin argumentos que la spec no declare. Sella. Reporta el conteo de código 97 en 2025 con **una sola** variable de agrupación, y si dispara `RESERVA-S2` (`FP-399`). Registro en la vista y asiento de replay en este mismo paso (E.7). Commit y push. **Confirma con `git ls-remote` que el commit está en origin antes de seguir:** el orden del diff es el sello.

**P2 · COMMIT-3a · las huellas, antes de R.** En commit aparte, escribe en el `spec.yaml` de ADJUDICACION la llave `sha256` de `emisiones_resultados` y `emisiones_sello`, derivadas en la sesión de los archivos recién sellados. **Es la única edición de spec admitida en todo el acto, y son exactamente dos valores.** Antes del commit, `git diff` debe mostrar sólo esas dos líneas. Después, `corrida0 preflight CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` → `VERDE`, con la salida cruda pegada. Commit, push, `git ls-remote`.

**P3 · COMMIT-3 · la realidad y el veredicto.** `python3 tools/corrida0.py run CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`. El código deriva R(a,b), verifica el soporte de 2025, adjudica por celda con las dos condiciones `INDECIDIBLE`, aplica la regla de ¾ y calcula ΔMAE con su IC. Si fallan ≥ 5 de 15 por soporte, el veredicto es `FUERA-DE-SOPORTE` global. Sella, vista, replay.

**P4 · El veredicto, con las palabras de la spec.** B-bis tal como está escrito: corroborada · acotada · falsador débil —que manda si caben ambas lecturas— · un retador vence. Si vence Sλ y no S½, o al revés, el hallazgo es sobre cuánto encoger. **Nada que no esté pre-registrado entra al veredicto.** Lo que te parezca interesante va en una sección rotulada `EXPLORATORIO — NO ADJUDICA`, **después** del veredicto y nunca antes.

**P5 · Registro.** En la celda-D `GOB…`: `veredicto`, `margen_material` y `champion_actual`. El `champion_actual` es el que dé la regla, o `NINGUNO` si nadie vence; en ese caso, por la firma del 17/sep, el piso C2 no vencido es el estimador de la celda. **Dilo; no lo adoptes tú.** `unidad_objetivo: evento` (`FP-393`). Marcador re-derivado por comando: el par edad × escolaridad de ENCIG 2025 deja de estar `RESERVADA`. Reporta `celdas_validadas` antes y después, derivado.

**P6 · Para mesa, al frente de la nota, en lenguaje llano.** Una página: qué se probó, qué salió, con qué certeza y **qué no significa**. En particular, el universo es el pago ordinario de luz (`N_TRA == 01`), no «gobierno digital» ni confianza en el Estado.

---

## 6 · LATITUD — sólo logística

Enlazar `data/raw`; instalar dependencias que `requirements.txt` no traiga (`pytest`, `numpy`, `pandas`); resolver rutas; reintentar un paso que falló por entorno **sin haber producido salida**. **Un paso que produjo salida no se repite**: «el primer resultado que produzca este procedimiento es el que se reporta».

---

## 7 · PAROS — lista cerrada

- **(a)** Editar la spec, su sidecar, `medidor.py`, `adjudicacion.py`, λ, umbrales, la lista `PUNTUADA` o B-bis; o cualquier línea de un `spec.yaml` **fuera de las dos huellas de P2**.
- **(b)** El código congelado no corre → no se parcha. El sucesor es un COMMIT-1 v1.3 de otra sesión.
- **(c)** Agrupar `encig25*` por dos variables fuera de `adjudicacion.py`, o antes de que las emisiones estén selladas **y** sus huellas escritas **y** ambas en origin.
- **(d)** Cualquier salida en scratch.
- **(e)** Repetir una corrida que ya produjo resultado.
- **(f)** La prueba de oro no pasa.
- **(g)** Entorno equivocado, o F3 violada.
- **(h)** Rastro de que 2025 ya se abrió por dos variables, o salidas previas en los directorios CALC.

**No es PARO:** main movido; `cuenta_gen2` rebajada por el registro —se reporta el campo que decide—; un veredicto que no te guste.

---

## 8 · COMPUERTAS

- **«Prueba de oro en verde» protege: abrir dato.**
- **«Emisiones selladas y en origin» protege: abrir dato** (el cruce de 2025).
- **«Huellas de las emisiones escritas en el `spec.yaml` de ADJUDICACION, en origin, y su preflight en `VERDE`» protege: abrir dato.** R no existe antes de esto.

No hay más compuertas.

---

## 9 · PERÍMETRO

**Propio:** los dos directorios CALC, **sólo** `ejecucion.json`, `resultados.json` y `sello.*` · las dos huellas del `spec.yaml` de ADJUDICACION (P2) · la celda-D `GOB…` · filas propias en `corridas.tsv`, `resultados.tsv` y `replay-evidencia.tsv` · derivados y marcador por comando · las NC que nombran a este acto o al COMMIT-2/3 como sucesor (entre ellas `NC-0451` y `NC-0455`; derívalas por objeto al cierre) · nota · el archivo verbatim de este encargo con su `sha256` (0-bis) · la cascada de `/acto`.

**Ajeno:** la spec y su sidecar · todo `.py` de los dos CALC · `fp399-firmada-826bf3a1.tsv` · `decisiones.tsv` —las filas ya están— · `tools/` · `tests/test_piloto3_v11.py` · cualquier payload que no sea ENCIG 2021/2023/2025 · **los otros dos cruces de ENCIG 2025 (sexo × edad, sexo × escolaridad), que siguen `RESERVADA`**.

**Perímetro de cierre, permanente (D-21):** `## NO-CORRIDO / RESERVAS`, con «Ninguno.» obligatorio si no hay, antes de `## CONSUMIDO`. Se añaden **al final** del encargo archivado; el cuerpo no se toca.

**«Si te encuentras escribiendo fuera de esta lista, PARA.»**

---

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE

**No hace:** no adopta ningún estimador · no abre los otros dos cruces de ENCIG 2025 · no reinterpreta el veredicto fuera de B-bis · no escribe la regla de elección del cruce de ningún otro piloto.

**Sucesores:**
1. **Informe v1.2** del programa, con el tercer dominio.
2. **El piloto de ahorro de PRODUCTO-DINERO**, que reutiliza este patrón completo: spec, v1.2 cableada, COMMIT-3a.
3. Si el veredicto abre una pregunta sobre cuánto encoger, un encargo de dirección, **no** una re-corrida.

**Auditoría (§5 de las instrucciones).** Tres líneas obligatorias en la nota. (1) **Universo:** pago ordinario de luz, unidad trámite. No se lee como conducta de personas ni como actitud hacia el Estado. (2) **Qué parece psicológico y es estructura:** el salto de once puntos entre olas es de nivel, con el mismo instrumento (`CAMBIO-MENOR`). Si la interacción se transporta, dice que la forma de la brecha por edad y escolaridad es estable, **no por qué**; acceso, bancarización y cobertura del servicio explican canal antes que preferencia. (3) **Escala:** todo en proporción de trámites, en puntos porcentuales; ΔMAE con su IC. Nada se compara contra el duelo nacional sin enlace.

**Cierre:** cascada de `/acto` · primera línea de la nota: veredicto, universo, unidad, escala y clase de evidencia.

---

**Falsador de este encargo, a tres meses:** si este acto para por una causa de cableado o de secuencia que `#944` o este texto no nombraron, la prueba del congelador todavía no cubre el conducto completo y D-22 tiene que exigir más.

## NO-CORRIDO / RESERVAS

| qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| **P1 · COMMIT-2 · las emisiones.** `python3 tools/corrida0.py run CALC-GOB-DIGITAL-EXE-EMISIONES-0002` … Sella. Reporta el conteo de código 97 en 2025 … Registro en la vista y asiento de replay … Commit y push | `PARO-PREMISA`: el CALC congelado corre pero `corrida0` se niega a sellar — `RUN: FALLO — nada se sella`, 40 RESULT `valor_null_sin_NO-ESTIMABLE_permitido` (32 IC de C1a NO-DERIVABLE sin `permite_no_estimable`; 8 de la banda 60-96 cuyo control el CALC sellado rotula `60`). PARO (b): no se parcha. `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01` | `N_corridas_selladas` +0; conteo 97 sin reportar; ninguna cifra de 2025 vista | COMMIT-1 v1.3 de otra sesión (`FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01`) y su COMMIT-2 |
| **P2 · COMMIT-3a · las huellas, antes de R.** | `DIFERIDO-A:COMMIT-2 del v1.3` — sin sello no hay huellas; `spec.yaml` de ADJUDICACION intacto. `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-02` | preflight de ADJUDICACION sigue BLOQUEADO por `emisiones_*`; R no existe | sesión del COMMIT-2 del v1.3 |
| **P3 · COMMIT-3 · la realidad y el veredicto.** | `DIFERIDO-A:COMMIT-3 del v1.3`; reserva: ADJUDICACION tiene 0 `permite_no_estimable` y emite `None` en el camino FUERA-DE-SOPORTE global. `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-03` | sin R ni veredicto; el par sigue `RESERVADA` | sesión del COMMIT-3 del v1.3 |
| **P4 · El veredicto, con las palabras de la spec.** | `DIFERIDO-A:COMMIT-3 del v1.3`. `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-04` | nada que adjudicar ni explorar | acto del COMMIT-3 v1.3 |
| **P5 · Registro.** celda-D, `champion_actual`, `unidad_objetivo: evento`, marcador re-derivado, `celdas_validadas` antes/después | `DIFERIDO-A:COMMIT-3 del v1.3`. `NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-05` | celda-D intacta (`SPEC-CONGELADA`); marcador no re-derivado | acto del COMMIT-3 v1.3 |
| **P6 · Para mesa, al frente de la nota.** | ejecutada en forma de PARO: §0 de `forense/notas/nota-2026-09-21-gen2-celda-d-piloto-3-commit-2-3-v1_2-paro.md` | — | — |
| Por objeto, las NC de `#941`: `NC-0451`–`NC-0454` siguen ABIERTAS (sucesor re-apuntado al v1.3); `NC-0455` CERRADA por producto (`decisiones.tsv:184-185`, resuelto SI) | — | — | — |

## CONSUMIDO

Ejecutado por `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2`, **PR #951**, 21/sep/2026 (CAJA, Opus 5, MODO RÍGIDO, sesión nueva `c0ab3df1`). **PARO (b) sin parche:** P0 en verde; `corrida0 run CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → `RUN: FALLO — nada se sella` (40 RESULT `null` sin `permite_no_estimable`; control 60-96 con clave `60`). Cero sellos, cero adopciones, ninguna cifra de 2025 vista; árbol de los CALC intacto. `ADR-586`; `FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01` ABIERTA; `NC-260921-…-a6f5-01`–`-05`; `NC-0455` CERRADA por producto. Sucesor: COMMIT-1 v1.3 en otra sesión, y sus COMMIT-2 / 3a / 3. Nota: `forense/notas/nota-2026-09-21-gen2-celda-d-piloto-3-commit-2-3-v1_2-paro.md`.
