# ENCARGO · ACTO GEN2-TUBERIA-RES-LLAVE-1 · EL NÚMERO `RES` SE CONGELA COMO ALIAS ESTABLE DE LA LLAVE LÓGICA · `CORR` DEJA DE SER CITABLE · LA VISTA DE RELEVO CASA POR LLAVE

**CABECERA** · redactado contra `a61dd000` (re-deriva al abrir; si `main` se movió **no es PARO**: refresca, fusiona hacia la rama, re-deriva y reporta) · **ENTORNO: NUBE — Claude en la nube**, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, **con credenciales de Git y publicación de PR**; cero microdato, `data/raw` no hace falta · una sola sesión, rama propia (D-17) · **MODO: ABIERTO** (D-18) · **MODELO SUGERIDO: Opus** (se puede subir, nunca bajar) · **COMPUERTA: ninguna** — no abre dato, no congela spec, no adopta, no borra (D-20) · **CONTADOR: `cuenta_gen2 = NO`; y `dependencias_numericas_legacy_activas` NO SE MUEVE** (criterio 3) · vehículo: `/acto`.

**EL PR NO SE FUSIONA EN ESTE ACTO.** Se publica y queda **propuesto; mesa central fusiona.** Por la firma D-r4, el diff **no pasa por revisión de dirección**: «hecho» son los cinco criterios por comando de §2.

**ANEXO OBLIGATORIO, con sha256:** `DISENO-RES-CORR-llave-logica-v1_1.md` · `a7b5e3adc6c789b8067fa3a97ff6b50dc4307454ac1453d91f3ea2b670aa0f06`. **Mesa lo adjunta al lanzar.** El ejecutor verifica el hash antes de leerlo; si falta o discrepa, **PARA con cero commits** (A.3). Es el diseño completo con sus mediciones; este encargo dice qué entregar, el anexo dice por qué.

**IDS.** `ADR` numérico (máximo en `main`: `ADR-578`; deriva al cierre). `NC`/`FP` con **raíz de acto** —`SUCESOR-1` ya está en `main` (#939)—: `NC-<AAMMDD>-GEN2-TUBERIA-RES-LLAVE-1-<4 hex del 0-bis>-<NN>`.

**Ramas vivas:** re-deriva y declara el conteo al abrir (A.13). Si corren a la vez `SIDECAR-CUERPO-1` o `PREFLIGHT-CI-1`, comparten `verify.yml`, `hallazgos.md` y `no-corrido.tsv`: concurrencia normal. **No necesita ventana**: no migra ningún id existente.

---

## 1 · FIRMA DE MESA, verbatim (21/sep/2026)

> «RES se congela como alias estable de la llave lógica; asignar número es un paso explícito y ningún comando de lectura escribe el registro. CORR deja de ser citable. Se declara el espacio cortes-C1. Un alias hereda número solo si quien es dueño del consumidor certifica que es el mismo slot; el par ENCUCI queda certificado por tramite.yaml:77,86. Un solo acto de TUBERÍA toca las tres herramientas; "hecho" son los criterios por comando, no una revisión.»

Y las decisiones que la acompañan: **D-r1** A · **D-r2** A · **D-r3** sí, con el nombre `cortes-C1::<corte>` · **D-r4** A, sin revisión del diff.

**Esta firma no está todavía en el repo.** Las firmas dadas en chat no se propagan solas: **este acto la asienta** (P0).

## 2 · OBJETIVO Y CRITERIOS DE «HECHO» — verbatim de la firma D-r4

Todos verificables **por comando sobre el commit final, con `main` fusionado**:

1. la numeración de hoy se preserva 210/210;
2. la vista re-derivada difiere sólo en las 6 filas CIV y en la de `NC-0213`;
3. `status` y el contador quedan idénticos;
4. el test de oro pasa sin tocar el registro;
5. las guardas G1 a G5 y la de biyección están en CI.

Más lo de siempre: `python3 tests/check.py --baseline --parallel` en **LÍNEA BASE VERDE**, PR publicado y propuesto, `## CONSUMIDO` con el PR real.

**La nota de cierre trae, por criterio, el comando y su salida cruda.** Un criterio sin comando a la vista no cuenta como cumplido.

## 3 · LO QUE TUBERÍA SABE — cada línea con su rótulo (detalle en el anexo)

- `EJECUTADO` · **La llave lógica ya existe y no se rediseña.** `tools/pines_mesa.py::llave_logica` —«ÚNICO sitio donde vive la traducción»— con su tabla `_ESPACIOS`. Traduce 204 de los 210 consumidores de hoy, sin colisiones, y es inyectiva en las 12 versiones históricas de `demanda-resultados.tsv`. Los 6 sin espacio son `milpa/src/celdas.py:CORTES_C1:<corte>`. El archivo `pines-de-mesa.tsv` ya cita por esa llave: **cero migración**.
- `LEÍDO` · **El número es posicional:** `tools/corrida0.py:705-707` (`RES-{i:04d}` por posición) y `:855` (`CORR-{i:04d}` por orden de grupo). `cmd_demanda` llama `_asigna_ids` tres veces; el comentario de `GEN2-T9` ya expresa la intención de no renumerar, pero una entrada nueva en la primera familia recorre todas las de abajo (`NC-0343`).
- `EJECUTADO` · **Deriva histórica:** 135 de 208 llaves han tenido más de un número; 82 de 86 números `CORR` han nombrado más de un instrumento.
- `EJECUTADO` · **Citas selladas mal resueltas hoy**, resolviendo cada una contra la demanda del momento en que se escribió: de 110 citas `RES` en 35 specs, **10**; de 50 citas `CORR` en 31 specs, **7**. Las 10 `RES`: 6 derivas posicionales (los `CALC-R-CIV-*`) y 4 claves cambiadas en su sitio en `6134100f`.
- `EJECUTADO` · **Las 4 claves cambiadas, con sus líneas:** ENCUCI (`RES-0005`, `RES-0006`) cambió de estimando —0.125822 → 0.126006, de «tasa base» a «unión condicional a contacto»—; ENIF (`RES-0059`, `RES-0060`) cambió sólo de etiqueta —valor y clase idénticos—. **Las cuatro las declara el consumidor como alias:** `milpa/tramite.yaml:77,86` (ENCUCI, certificado por la firma) y `:1518,1519` (ENIF, con el comentario *«etiqueta corregida por NC-0127 sin cambiar cálculo ni adopción»*). **Por la regla firmada, el alias declarado por el dueño del consumidor es su certificación: las cuatro heredan número.** El criterio 2 sólo es alcanzable así.
- `EJECUTADO` · **La vista hoy:** en 6 filas propone el CALC equivocado como candidato (los CIV); en las 4 de claves cambiadas marca `YA-ADOPTADO` (3) y `VETADO-POR-DECISION` (1) porque el número posicional acertó por accidente.
- `EJECUTADO` · **`NC-0213` es deriva:** cuando se escribió `CALC-ENVIPE-0001`, `CORR-0009` era ENVIPE 2025 y contenía `RES-0027`/`RES-0028`. El autor citó bien.
- `LEÍDO` · **El contador no depende de candidatos:** `tools/corrida0.py:4575` cuenta usos cuyo consumidor lee GEN1 (`generacion_leida`). Arreglar la identidad es neutral por construcción — el criterio 3 lo verifica.
- `LEÍDO` · **El test de oro** (`tests/test_corrida0_oro.py`) corre `demanda` y restaura los TSV que toca, sin `git checkout`. Si `demanda` escribiera el registro, cada corrida en una rama sucia quemaría números.
- `LEÍDO` · `milpa/src/emisor.py:129,141,1003` ya lee `aliases:` del consumidor. `tools/corrida0.py` no lo lee hoy. Sólo `milpa/tramite.yaml` usa el campo.
- `EJECUTADO` · **Prototipo del registro** contra los 210 slots reales: numeración preservada 210/210; un slot insertado al principio de `tramite` → 0 números existentes cambian, el nuevo recibe `RES-0211`. **El prototipo del anexo §4 tiene dos defectos que mesa señaló** —asigna dentro de `demanda` y deja vivos nombre viejo y nuevo—: no se copia, se corrige.
- `EJECUTADO` · **149 números `RES`/`CORR` literales** en 11 archivos de `tools/` y `tests/`. Con el congelamiento siguen siendo válidos: **no se tocan**.

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO (A.8)

- La llave lógica y su espacio de pines: **EXISTE-SATISFACE** para su canal (`pines_mesa.py`, `pines-de-mesa.tsv`); este acto la **extiende**, no la rehace.
- Registro persistente de números: **NO-ENCONTRADO** (`data/corrida0/`, `tools/`, sin archivo ni función que guarde `llave → RES`).
- Resolución de citas selladas a su momento: **NO-ENCONTRADO**.
- Guardas de biyección o de citas nuevas a `RES`: **NO-ENCONTRADO** en `tests/` ni en `verify.yml`.
- `NC-0213` ABIERTA, reasignada a TUBERÍA (firma B5 del 21/sep). `NC-0343` ABIERTA. `NC-0393` y `NC-0426` **no son de este acto** (§10).

## 5 · PIEZAS — resultado esperado, no receta

**P0 · 0-bis (A.3), anexo y firma.** Este encargo verbatim a `forense/encargos/`, y el anexo verbatim a su lado, verificado por sha256. Chequeo de duplicado **por contenido** (¿alguna rama viva archiva ya este encargo?), con el conteo de ramas examinadas. **Asienta la firma del §1 verbatim** donde la casa asienta las firmas dadas, marcada FIRMADA con este acto (A.12).

**P1 · El espacio `cortes-C1`.** Una línea en `tools/pines_mesa.py::_ESPACIOS`: `milpa/src/celdas.py` → `cortes-C1`, de modo que `CORTES_C1:formalidad` sea `cortes-C1::formalidad` —sin repetir el nombre de la tabla dentro de la llave si el ejecutor lo ve redundante, y declarándolo—. `tests/test_pines_mesa.py` debe cubrir de ida y vuelta **los 210** consumidores. **Declarar el espacio no vuelve pineable nada por sí solo**: un pin sigue exigiendo firma de mesa y las guardas de 4.1.

**P2 · El registro y la asignación explícita.** `data/corrida0/registro-res.tsv`, persistente: por fila, la llave, el número y su estado (vigente o retirado), con la fecha y el commit en que nació. **Contenido inicial = la numeración de hoy, 210/210.**
- **Asignar** es un subcomando explícito con `--escribe`, al estilo de `registro --escribe`. Es el único código que escribe el registro.
- **Leer** es todo lo demás: `demanda`, `status`, el CI, el test de oro. `_asigna_ids` sólo lee; **un slot sin número hace fallar la lectura en voz alta, con el nombre del slot y el comando que lo numera.**
- **Alias:** se leen del campo `aliases:` del consumidor. Un nombre nuevo hereda el número del viejo **sólo** si el consumidor lo declara como alias; si no, el viejo se retira y el nuevo recibe número propio. **No se crea un archivo de alias aparte** (D-15): nace el día que un consumidor sellado lo necesite.
- Un número retirado **no se reusa nunca**.

**P3 · La llave, visible.** Columna `llave_logica` en `data/corrida0/demanda-resultados.tsv`, para que quien lea la vista vea la identidad y no sólo el alias.

**P4 · Las citas selladas, resueltas a su momento.** `data/corrida0/pines-sellados-resueltos.tsv`: una fila por cita `RES` o `CORR` en la spec de un CALC sellado → la llave (o, para `CORR`, las llaves de los slots que el grupo tenía **en ese momento**), resuelta contra la demanda del commit que fijó la spec por última vez. Se construye **una vez, con historia completa, en este acto**. Esperado, re-derívalo: ~160 filas, de las que 17 difieren de lo que el número nombra hoy. **Y el resolvedor queda expuesto como comando** —«qué nombraba `RES-X` (o `CORR-X`) en tal fecha»—, porque es la misma función que construye la tabla.

**P5 · La vista casa por llave.** `tools/relevo_usos.py`: los canales `C1-MAPA`, `C1-SINGULAR`, `C2-RESULTADO` y `C3-CORRIDA` dejan de casar por el token de la spec: cita sellada → tabla de P4 → llave; cita nueva → llave, o `RES` → registro → llave. **`CORR` deja de ser citable**: `C3` acredita cobertura sobre los slots que el grupo tenía cuando se escribió la cita, y un slot que entró después ya no recibe crédito.

**P6 · Las guardas, en CI, cada una probada por mutación.**

| Guarda | Falla cuando |
|---|---|
| **G1** registro inmutable | un par llave→número de la base cambia en el PR |
| **G2** sin reúso | un número retirado se reasigna |
| **G3** citas nuevas | una spec añadida o tocada cita un `RES` que no existe en el registro de la base, o cita `CORR` |
| **G4** sin citas colgantes | una llave citada por `pines-de-mesa.tsv` o por la tabla de P4 no existe vigente ni se resuelve por un alias declarado |
| **G5** tabla completa | una cita `RES`/`CORR` en una spec sellada no tiene fila en la tabla de P4 |
| **G6** biyección | una llave vigente con dos números, un número con dos llaves, o una llave vigente que es a la vez alias de otra |

**G1 y G3 necesitan la ref base**: corren en un job con su propio clonado que la traiga, sin hacer `fetch` dentro del clon de la suite (D-23). G2, G4, G5 y G6 no necesitan historia.

**P7 · Los criterios del §2, verificados.** Antes de tocar nada, guarda la vista y la salida de `status` de `main`. Al final, con `main` fusionado: numeración 210/210 (1) · `diff` de la vista vieja contra la re-derivada, listado fila por fila (2) · `diff` de `status` (3) · el test de oro contra el árbol final, verificando que el registro no cambió de bytes (4) · las seis guardas en `verify.yml` (5).

**P8 · Hallazgos y semillas** en `forense/hallazgos.md`:
1. `NC-0213` se cierra como **deriva, no error de autor**, con la resolución de P4 como evidencia; su fila en `no-corrido.tsv` pasa a CERRADA citando este PR.
2. `NC-0343`: su causa estructural queda cerrada; las 37 filas dejan de poder desincronizarse porque el número ya no depende del orden.
3. **Semilla PARA-v2.16:** *un slot nuevo se cita por su llave —en la spec, en la nota y en el ADR— hasta que su número entra a `main`, porque si otro PR fusiona antes su número provisional cambia.*
4. La auditoría honesta: **este acto no quita la ceguera de los 37 slots** que la vista no ve —son CALC que no escriben pin; eso es trabajo de pines de mesa— **ni mueve el contador**. Arregla lo mal atribuido e impide que la deriva siga.

**P9 · Cierre.** Cascada de `/acto`, `## NO-CORRIDO / RESERVAS` al **final** del encargo («Ninguno.» es obligatorio), `## CONSUMIDO` con el PR real. La nota de cierre lleva basename distinto del encargo (`T02`) y los rótulos nuevos se registran con prefijo de espacio (`T25`).

## 6 · LATITUD

El cómo es tuyo: el nombre del subcomando de asignación, el formato exacto de los dos archivos nuevos, dónde vive el resolvedor, cómo se cablean las guardas. Un obstáculo reversible y barato se resuelve y se declara (D-19). Si `main` se mueve, fusiona hacia la rama y re-deriva; si entran slots nuevos a la demanda mientras corres, se numeran con el paso explícito y se declaran.

`NC-0213` toca una cita (`CORR-0009` en `CALC-ENVIPE-0001`) que cubre dos slots, `RES-0027` y `RES-0028`: si la vista cambia en las filas de esos dos slots por esa causa, es el caso de `NC-0213` del criterio 2, y la nota lo lista fila por fila.

## 7 · PAROS — lista cerrada

Anexo ausente o con hash distinto · entorno sin credenciales de publicación · otra rama viva ya archiva este encargo · editar una spec sellada · que **la vista re-derivada cambie en alguna fila fuera de las 6 CIV y las de `NC-0213`** — es la red de seguridad de las adopciones: se reporta la lista de filas y no se sigue · que **`dependencias_numericas_legacy_activas` o cualquier cifra de `status` cambie** · que un comando de lectura escriba el registro · objetivo inalcanzable. **Fuera de esta lista no se para**: se resuelve, o se pregunta a mesa con opciones y recomendación y se sigue con lo demás.

## 8 · PERÍMETRO

Escribes en: `tools/corrida0.py` · `tools/pines_mesa.py` · `tools/relevo_usos.py` · el resolvedor, si va aparte · `data/corrida0/registro-res.tsv` y `data/corrida0/pines-sellados-resueltos.tsv` (nuevos) · los derivados que el propio `corrida0` re-escribe (`demanda-*.tsv`, `relevo-usos-v1_0.tsv`) · `tests/test_pines_mesa.py` y los tests de las guardas · `.github/workflows/verify.yml` (**sólo** pasos o jobs nuevos) · `forense/encargos/` (este encargo y su anexo) · `forense/notas/` · `forense/hallazgos.md` · `forense/no-corrido.tsv` · donde la casa asienta la firma (P0) · y la cascada de gobernanza que `cierre_acto.py --aplica` reconcilia. Más el perímetro de cierre permanente (D-21). **Si te encuentras escribiendo fuera de esta lista, PARA.**

**No tocas:** `milpa/` (se lee, incluido `tramite.yaml`) · ninguna spec ni resultado de CALC · `data/corrida0/pines-de-mesa.tsv` (cero migración) · los 149 literales `RES`/`CORR` del código · `.claude/commands/acto.md` · las menciones de `RES` en `decisiones.tsv`, firmas y `NC` (son prosa; con el congelamiento dejan de envejecer).

## 9 · LO QUE NO HACE · SUCESORES

No escribe pines · no adopta nada · no quita la ceguera de los 37 slots · no mueve el contador · no renumera ningún id existente · no crea archivo de alias aparte · no toca la numeración de `ADR` (careo propio, firma 1) · no fusiona su propio PR.

Sucesores, en el orden de mesa: (4) un archivo por entrada; (5) taxonomía de PR y regla de enrutamiento.

## 10 · NO ES DE ESTE ACTO

`NC-0393` —el reconocedor `RE_ENLACE` no acepta «candidato para»— es un defecto de vocabulario adyacente, no de identidad. `NC-0426` —el quinto canal por `parametros.id_celda`— quedó sustituido en la práctica por los pines de mesa. Ninguno se toca; si el trabajo de P5 los hace triviales, se anota en hallazgos, no se arregla.

## 11 · FALSADOR (§9)

Si en tres meses ninguna de las seis guardas ha fallado una sola vez, se anota y se revisa si valían el aparato. Si aparece un consumidor que renombra una clave **sin** declarar el alias y G4 no lo atrapa, la guarda está mal escrita.
