# Nota · ACTO GEN2-RECIBO-ASTRA6-1 · recibo post-merge de #1184 (C1 lote 1), #1185 (C1 lote 2, preparación) y #1189 (revisión tanda 2)

Contadores movidos por este trabajo: **cero mediciones, cero adopciones**; `cuenta_gen2` intacto. Asienta `validacion_independiente = NO-PASA` en 6 RESULT (overlay, §6). Todas las cifras de esta nota son **RETROSPECTIVAS** (validación de pisos ya sellados), unidad **mujer** (proporciones ponderadas `FAC_MUJ`/factor 2011), datos primarios mexicanos (a).

Encargo: `forense/encargos/2026-09-26-GEN2-RECIBO-ASTRA6-1.md` (cuerpo `fb439145…`, 0-bis `beeecf2c`). ENTORNO NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus montado=NO, 0 archivos examinados). Base: `origin/main` = `0304bf21` (el encargo declara `57a3f2a4`; main avanzó con #1189, que está en el alcance). Cero microdato: se leyeron paquetes archivados, comparaciones congeladas, constancias de sesión, `spec.yaml`/`resultados.json` sellados y catálogo/piso.

Herramienta (pieza §5): `python3 tools/recibo/comparaciones.py --lote forense/validacion-independiente/catalogo-1-ejecucion-lote1 --salida forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1` → produce, en esta carpeta, `…--tabla-result-estado-efecto.tsv` (3 371 llaves), `…--ceguera.tsv` (9 paquetes) y `…--resumen.json`. Test: `tests/test_recibo_comparaciones.py` (6 pasan). Las reglas de dictamen están declaradas en el docstring de la herramienta (1–7) y no por llave.

## Tabla por lote

| PR | objeto | ¿escribió en sellos / catálogo / `decisiones.tsv`? | recomendación |
|---|---|---|---|
| #1184 (`2af4f29c`) | C1 lote 1: 9 paquetes ENDIREH, 3 371 identidades | NO. `git diff --name-only 2af4f29c^1..2af4f29c`: 148 en `forense/validacion-independiente/catalogo-1-ejecucion-lote1/`, 10 en `tools/validacion/astra6_lote1/`, 5 en `forense/encargos/` | **RECIBIDO-POST-MERGE-CON-NC** |
| #1185 (`57a3f2a4`) | C1 lote 2: 11/59 paquetes preparados (425/32 772 estimadores), cero recálculos | NO. Solo su carpeta, su herramienta y la cascada de gobierno propia (ADR/L0/rótulos/NC/FP/INFRAESTRUCTURA) | **RECIBIDO-POST-MERGE-CON-NC** |
| #1189 (`0304bf21`) | Dictamen documental de tanda 2 | NO. 3 archivos en `forense/analisis/astra6-revision-tanda2/` | **RECIBIDO-POST-MERGE** |

Ningún caso de `PROPONER-REVERTIR`: ninguno de los tres escribió en sellos, catálogo ni `decisiones.tsv`.

## 1 · Ceguera (lote 1) — `CIEGA-POR-SEPARACIÓN` en los 9 paquetes

EJECUTADO por la herramienta (columnas a–e de `…--ceguera.tsv`), por paquete:

- **(a) Paquete antes de la sesión.** Los 9 contenedores `*-entradas.tar.gz` se localizan en `forense/validacion-independiente/catalogo-1/paquetes/` por SHA-256 igual a `sha256_contenedor` de `entregas.json`; entraron al repo en `2b655cfc` (26/sep 19:06 UTC), antes de la primera entrada de sesión (27/sep 00:24 UTC). 9/9.
- **(b) Contenido.** 7 miembros cada uno: `encargo.md, estimandos.tsv, faltantes.json, insumos.json, manifiesto.json, metodo.md, tolerancia.json`; `manifiesto.json` casa con `paquete_sha256` y cada miembro con su hash; `estimandos.tsv` no trae ninguna columna de valor (`punto`, `ic95_*`, `se`, `replicas`…). Insumos = microdato, cuestionarios, FD y diseño muestral por URL/sha. 9/9.
- **(c) Sesión.** Un solo mensaje de usuario (el del launcher); el barrido de los 13–24 comandos por sesión no encuentra acceso a red, `/home`, `/mnt`, `/root`, `resultados.json`, `sello.json` ni comparaciones (las únicas coincidencias de «comparacion» están dentro del texto del propio recibo del validador). 9/9.
- **(d) Orden por historial.** 10 commits de reconstrucción (comunitaria tiene dos) con oid SHA-1 recomputado desde el contenido archivado; fecha de committer anterior a `revelacion_utc` en los 10.
- **(e)** `congelacion_recibida_utc < revelacion_utc` en 9/9.

**Bubblewrap vs. NO-CIEGA.** El launcher efectivo `tools/validacion/astra6_lote1/lanza.sh` (SHA-256 `a766b2b4…` = `launcher_sha256` de los 8 lanzamientos registrados) monta solo `/usr /bin /lib /lib64` de solo lectura, `/entrada`, `/raw`, `/work` y `/config` nuevo, con `--clearenv` y guardia `test ! -e /home && test ! -e /mnt && test ! -e /root`. El perfil `read :root` que llevó a 6 validadores (2011, comunitaria, decisiones, discriminación, familiar, laboral) a autorrotularse `NO-CIEGA` es la raíz **del sandbox**, no del host. Dictamen: la separación está acreditada por evidencia (montajes + guardia + transcript), no por declaración → `CIEGA-POR-SEPARACIÓN`. Se conserva literal el autorrótulo del validador; el rótulo del recibo es otro campo.

**Reservas (no degradan el rótulo, se declaran):** (i) `lanza.sh` no usa `--unshare-net`: la red no está aislada por el sandbox (lo exige la API); la ausencia de acceso a red se acredita por el transcript, no por el sandbox → NC-…-08. (ii) El contenido de `/raw` que materializó el orquestador no se archivó (la sesión archivada excluye salidas) → NO-VERIFICABLE-AQUÍ. (iii) Comunitaria corrió con la versión anterior del launcher (editada durante la ejecución, retorno 2) y su SHA no se registró; es irrelevante para cifras: ese paquete no produjo ninguna.

**Materializador no ciego.** Leyó el snapshot con esperados para verificar integridad **antes** de entregar, fuera del sandbox; el validador no tuvo montaje hacia él. Está separado de la sesión que recalculó → el lote **no** colapsa a NO-CIEGA. El orquestador sí era no ciego cuando hizo el commit de «normalización» de comunitaria (`c0cc754a`, 00:29:56 UTC).

**Normalización.** Única normalización: comunitaria, `FALTANTE_HORIZONTE_EN_LLAVE` → `NO-RECALCULABLE-DESDE-SPEC` en 100/100 filas, commit del orquestador **anterior** a la revelación (00:30:16 UTC), con **0** filas de llave o cifra distintas entre el blob original (`715ee64b`) y el canónico (blobs verificados por SHA-1). Rótulo: `SOLO-ESTADO-PRE-REVELACIÓN` — no invalida ninguna comparación.

Verificador propio de Astra, EJECUTADO sin raw: `python3 tools/validacion/astra6_lote1/verifica_lote.py` → rc 0, `evaluados 3371`, `commit_sin_verificacion_de_objeto: []`.

## 2 · Las 685 (y las 2 569 DISCREPA) — distribución

Tolerancia citada: la de cada `spec.yaml` sellado, `flotante abs=1e-10`, razón «semilla y sumas deterministas»; el comparador usó exactamente esa en los 9 (`sin_estado = 0`). Recomputar `dentro = |Δ| ≤ 1e-10` sobre los 3 × 2 561 campos: **0** desacuerdos con el comparador (cero artefactos del comparador). `comparacion_sha256` de `entregas.json` casa en 9/9.

| componente | n | estado del recibo | efecto | nota |
|---|---:|---|---|---|
| punto e IC | 3 | COINCIDE | ninguno | 2011 |
| solo IC | 1 873 | DISCREPA | incertidumbre | punto COINCIDE a 1e-10; artefacto `TOLERANCIA-DE-REPLAY-SOBRE-IC-ALEATORIO` |
| punto | 685 | DISCREPA | cifra | 683 en 2011, 2 en no-física B/C 2021 |
| publicabilidad | 11 | DISCREPA | alcance | §3 |
| sin cifra | 799 | NO-RECALCULABLE-DESDE-SPEC | ninguno | §4 |

**IC (1 873).** La tolerancia sellada es de *replay* (misma semilla, mismo orden); la spec no fija el orden de consumo del RNG ni el marco de UPM, así que un bootstrap reimplementado no puede caer a 1e-10 por construcción. Tamaño de la diferencia respecto al ancho del IC sellado: ≤1 %: 34 · ≤5 %: 597 · ≤10 %: 808 · ≤25 %: 431 · >25 %: 3. No es evidencia de error ni de equivalencia inferencial: falta la vara (NC-…-06). No se inventa tolerancia.

**Punto (685), por magnitud |Δ|:** ≤0.0001: 419 · ≤0.001: 241 · ≤0.01: 18 · ≤0.05: 1 · >0.05: 6. Es decir, **660 difieren menos de 0.1 pp**; **7 difieren más de 1 pp**.
**Por hipótesis del ejecutor** (de `efectos-discrepancias.tsv`; `comparacion.json` no trae causa y no se archivó contrafactual → causa del recibo `CAUSA-NO-DETERMINABLE`, NC-…-04): ámbitos externos (desconocidos vs. negativos) 535 · pareja reciente 62 · edad 60+ 38 (36 en 2011, 2 en 2021) · permisos (filtro CP4_1) 34 · denuncia externa (columnas 1/5 vs. 1–4) 10 · instituciones (solicitantes vs. afectadas) 6. Ninguna «normalización» del comparador después de ver esperados.

**Las 7 grandes:** las 6 de instituciones 2011 (`RESULT-ENDIREH2011-MOD-TABLA#1656`–`#1661`, Δ −0.09 a −0.33) y `#924` (edad 60+, Δ −0.015). En instituciones la spec sellada dice «a DIF, Instituto de la Mujer, MP… **entre mujeres con al menos un acto**» (`spec.md:7`), mientras el medidor sellado condiciona a solicitantes de ayuda (`discrepancias-2011.md:12`): la cifra publicada (p. ej. 0.370 para `pareja_institucion_01`; el recálculo entre afectadas da 0.044) no mide el estimando que la spec humana describe. Leída como «proporción de afectadas que acudió a DIF», la cifra publicada es 8.3–8.4 veces la del recálculo en las 6 celdas; es la lectura peligrosa que motiva `PROPONER-SUSPENDER`.

## 3 · Las 11 de publicabilidad

Regla de la spec (ambas olas): publicable con n ≥ 100, ≥ 5 UPM, ancho IC ≤ 0.20 **y** CV ≤ 0.30. El validador suprimió; el sello publicó. Margen = distancia relativa del valor sellado al umbral más cercano; banda de ruido Monte Carlo del EE bootstrap con R = 200 réplicas = 2/√(2·199) = 0.100.

| llave | CV sellado | ancho | margen | fila catálogo v1.2 = fila piso v1.1 | recomendación |
|---|---:|---:|---:|---:|---|
| `RESULT-ENDIREH2011-MOD-TABLA#606` | 0.110 | 0.1947 | 0.026 | 3909 | ACOTAR |
| `RESULT-ENDIREH2011-MOD-TABLA#1919` | 0.292 | 0.0120 | 0.027 | 3351 | ACOTAR |
| `RESULT-ENDIREH2011-MOD-TABLA#1993` | 0.297 | 0.0110 | 0.009 | 3377 | ACOTAR |
| `RESULT-ENDIREH2011-MOD-TABLA#2039` | 0.269 | 0.0135 | 0.104 | 3393 | **PROPONER-SUSPENDER** |
| `RESULT-ENDIREH2011-MOD-TABLA#2067` | 0.290 | 0.0258 | 0.033 | 3410 | ACOTAR |
| `RESULT-ENDIREH2011-MOD-TABLA#2082` | 0.293 | 0.0165 | 0.025 | 3415 | ACOTAR |
| `RESULT-ENDIREH2021-DIS-TABLA#220` | 0.296 | 0.0198 | 0.013 | 6780 | ACOTAR |
| `RESULT-ENDIREH2021-DIS-TABLA#221` | 0.298 | 0.0187 | 0.006 | 6781 | ACOTAR |
| `RESULT-ENDIREH2021-DIS-TABLA#228` | 0.292 | 0.0172 | 0.027 | 6786 | ACOTAR |
| `RESULT-ENDIREH2021-DIS-TABLA#296` | 0.291 | 0.0213 | 0.029 | 6829 | ACOTAR |
| `RESULT-ENDIREH2021-DIS-TABLA#315` | 0.292 | 0.0154 | 0.025 | 6845 | ACOTAR |

Valor sellado = `resultados.json` del CALC; filas = número de fila de datos (1 = primera tras la cabecera) en `canon/catalogo-del-mexicano-v1_2.tsv` y `canon/tabla-de-piso-v1_1.tsv` (coinciden en las 11). ACOTAR = rótulo «publicabilidad frágil al RNG» (10); `#2039` queda fuera de la banda por 0.004 y la regla lo manda a PROPONER-SUSPENDER — la diferencia de marco UPM de 2011 (`informe-lote1.md`) es la hipótesis más probable y no se probó. En ningún caso se toca el sello; el sucesor es un CALC nuevo.

## 4 · Las 799 «specs insuficientes» — 767 no lo son

La ventana temporal (vida / desde octubre 2020 / desde inicio de relación) **sí** está en la identidad sellada: campo `ventana` de cada celda de `resultados.json` y `reserva: ventana=…` del catálogo v1.2. La omitió el preparador en `estimandos.tsv` (sin columna `ventana`). Reparto (regla 7 de la herramienta):

| causa | paquete | n | tipo | sucesor |
|---|---|---:|---|---|
| `PAQUETE-SIN-IDENTIDAD-DE-VENTANA` | comunitaria 100 · escolar 96 · laboral 100 · no-física B/C 471 | 767 | defecto de empaquetado, **no D-15** | paquete v2 con columna `ventana`, sesión nueva (NC-…-01) |
| `D15-RECODIFICACION-AUSENTE` | discriminación 23 · no-física B/C 8 | 31 | D-15 genuino: la spec 2021 nombra «ninguna/básica/media superior/superior» sin mapa `NIV`/`GRA` (la de 2011 sí lo trae) | spec sucesora sellada con el mapa (NC-…-02) |
| `D15-IDENTIDAD-CONTRADICTORIA` | ayuda `#115` | 1 | D-15: `metodo.md` dice «desconocía servicios»; FD p. 632 y cuestionario A 14.22 dicen «no sabía que existían leyes» | spec sucesora (NC-…-03) |

Denominador de D-15 real: **32**, no 799. No se corrige ninguna spec aquí.

## 5 · Recomendación a mesa y frase de producto

**RECIBIDO-POST-MERGE-CON-NC** para #1184 y #1185; **RECIBIDO-POST-MERGE** para #1189. Filas del catálogo a tratar por `CATALOGO-V1-3-1` (lista completa por comando: `recomendacion` en `…--tabla-result-estado-efecto.tsv`): **PROPONER-SUSPENDER 7** (6 instituciones 2011 + `#2039`), **ACOTAR 689** (679 puntos con Δ ≤ 5 pp + 10 de publicabilidad), SOSTENER 1 876, SOSTENER-SIN-CORROBORACIÓN 799. FP-…-01 y FP-…-02.

Frase honesta para el informe v1.5 (RETROSPECTIVA; unidad mujer):
«En el primer lote de validación ciega (ENDIREH 2011 y 2021, 9 paquetes, 3 371 identidades), 1 876 de 2 561 cifras recalculadas coinciden en el punto dentro de la tolerancia sellada, pero sus intervalos no son comparables bajo esa tolerancia de replay (solo 3 coinciden en punto e IC); 685 puntos discrepan con efecto en la cifra —660 por menos de 0.1 pp y 7 por más de 1 pp, seis de ellos por un denominador distinto en instituciones de ayuda 2011— y 11 celdas cambian de publicabilidad (alcance); 32 specs no bastan para recalcular y otras 767 identidades no se evaluaron porque el paquete omitió la ventana temporal; ceguera: CIEGA-POR-SEPARACIÓN en los 9 paquetes, con la red no aislada por el sandbox.»

## 6 · Asiento de `validacion_independiente`

Premisa del encargo caída (logística, se replantea y se declara): `forense/replay-evidencia.tsv` no tiene columna `validacion_independiente` (`grep -c` → 0; cabecera de 14 columnas sin ella). El asiento vive en `data/corrida0/validaciones-independientes.tsv` (`tools/corrida0.py:3144`, `_aplica_validaciones_independientes`, llave `(spec_id, resultado_id)`, estados `PASA · NO-PASA · CONCUERDA-NO-APROBADA`, evidencia con SHA-256 verificada en cada registro). Se añaden 6 filas `NO-PASA` — `RESULT-ENDIREH2011-MOD-TABLA`, `-2021-AYU-`, `-DEC-`, `-DIS-`, `-FAM-`, `-NF-BC-TABLA` — con `validacion_ref` = su `*--comparacion.json` y alcance desglosado. `COM`, `ESC` y `LAB` no reciben asiento (quedan `NO-HECHA`): cero cifras recalculadas por defecto de empaquetado; asentar NO-PASA ahí confundiría «no se evaluó» con «no pasó». Ninguno es `PASA`: la compuerta del encargo (tolerancia preexistente citada) no se satisface para el IC. `NO-PASA` no altera origen, rol ni aptitud (docstring del overlay). `python3 tools/corrida0.py registro` en seco con el overlay: ver § cierre.

## 7 · Lotes 2 y tanda 2

**#1185 (preparación).** EJECUTADO: los 11 paquetes `LISTO-PARA-SESION-NUEVA` de `astra6-c1-lote2-entrega-59.tsv` localizados por `sha256_contenedor` en `catalogo-1-preparacion-lote2/entradas/`; manifiesto casa 11/11; `estimandos.tsv` sin columnas de valor 11/11; miembros extra solo cuestionarios/FD/`conductas.md`; suman 425 estimadores. Preguntas 2–4 no aplican (cero comparaciones). Hallazgo A.7: `astra6-c1-lote2-entrega-59.tsv` no casa con su hash en `preparacion/hashes-recibo-lote2.json` (`75b1febc…` vs `3393c425…`); el declarado es el de la misma tabla con fin de línea CRLF — identidad de contenido sostenida, hash crudo discordante (línea en `forense/hallazgos.md`). Advertencia hacia adelante (EJECUTADO): ninguno de los 59 `estimandos.tsv` del lote 2 trae columna `ventana`; de los 11 LISTO, solo `endireh-pisos-2016-pareja-fisica-0002-v2` tiene celdas selladas con dos ventanas (46 `vida` + 46 `desde_octubre_2015`) y pares eje/segmento repetidos (`#1` y `#50` son ambos `edad`): repetirá el defecto de §4 en sus 92 estimadores si se lanza así. Corregible antes de revelación (NC-…-09).
**#1189.** Documental; sus cifras (3+2 569+799 = 3 371; 685/1 873/11) casan con el resumen de #1184. Sin NC.

## Auditoría (módulo v2.16, solo lo que esta nota afirma sobre México)

Cifras escritas a mano: ninguna; todo sale de la herramienta o de `resultados.json`/`spec.md` citados. PROSPECTIVA/RETROSPECTIVA: todo RETROSPECTIVA; ninguna frase mezcla. Unidad: mujer en todas las proporciones; no se promedia con hogar ni trámite. Escala: proporciones [0,1], Δ en la misma escala. Nada de esto afirma rasgos culturales: las discrepancias son de estimando, filtro o empaquetado, no de conducta. Lectura peligrosa: presentar 2 569 DISCREPA como 2 569 cifras erróneas, o 799 como specs rotas (son 32). Las 9 sesiones comparten dos olas: no son 9 pruebas independientes.
