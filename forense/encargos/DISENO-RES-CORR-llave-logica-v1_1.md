# DISEÑO · RES/CORR CON LLAVE LÓGICA · v1.1 — TUBERÍA → mesa · 21/sep/2026

**v1.1 sustituye a v1.0** e incorpora las correcciones y firmas de mesa del 21/sep (§7). Cambios de fondo: los cuatro «renombres» no eran renombres puros; el alias se lee del consumidor, no de un archivo aparte; `demanda` no escribe el registro; se añade la guarda de biyección; G1 y G3 necesitan la ref base.

**Qué es.** El diseño del paso (3) del orden de mesa: que el id de un slot de demanda sea estable desde que nace, y que ninguna cita sellada vuelva a apuntar en silencio a otro slot. **No es encargo**: es el anexo del encargo `GEN2-TUBERIA-RES-LLAVE-1`. Las recomendaciones de §5 son **de TUBERÍA**; dirección no las había dado.

**Medido contra:** `main` `a61dd000`, clon propio. Todo `EJECUTADO` salvo rótulo distinto. Nada se escribió en el repo.

---

## 0 · Lo que ya existe, y que este diseño NO rediseña

`EJECUTADO`, A.8 por objeto. **La llave lógica ya vive en la casa.** `tools/pines_mesa.py` (ACTO `GEN2-RELEVO-TANDA-3`, 21/sep) define `llave_logica(consumidor)`, declarada «ÚNICO sitio donde vive la traducción consumidor → llave», sin ruta, sin versión y sin `RES-####`, con una tabla cerrada de espacios (`_ESPACIOS`: `marco-M`, `tramite`, `procedencia`, `catalogo-momentos`, `celda-D`, `marcador`). La usa `data/corrida0/pines-de-mesa.tsv` (27 filas firmadas, llave `marco-M::CIV-M-01::R`) y la importan `corrida0.py` y `relevo_usos.py`.

Y el encargo de aquel acto dejó escrito para TUBERÍA: *«el canal usa llave lógica; si su diseño de `RES`/`CORR` fija otra forma, una migración del archivo de pines, no un rediseño»*. **Este diseño adopta esa forma tal cual.** Cero migración del archivo de pines.

Medida sobre los datos reales: la llave de la casa traduce **204 de 210** consumidores, sin una sola colisión, y es inyectiva en **las 12 versiones** históricas de `demanda-resultados.tsv`. Los 6 que no traduce son `milpa/src/celdas.py:CORTES_C1:*`, que no tiene espacio declarado (D-r3).

**Lo que falta**, y es el objeto de este diseño: la llave está sólo en el canal de pines de mesa. El número `RES-####` sigue siendo la identidad en todo lo demás —la vista de relevo, las specs selladas, el código—, y sigue siendo posicional.

## 1 · Lo medido

### 1.1 · El número se mueve, y se sabía

`LEÍDO` · `tools/corrida0.py:705-707`: `fila["resultado_id"] = f"RES-{i:04d}"`, por posición. `:855`: `CORR-{i:04d}`, por orden de grupo. `cmd_demanda` llama a `_asigna_ids` tres veces, y el comentario de `GEN2-T9` dice la intención: *«se AÑADE al final a propósito: así ningún `RES-` ya emitido cambia de id»*. Pero añadir al final sólo protege a las familias nuevas: una entrada nueva en `tramite.yaml`, que es la primera familia, recorre todas las de abajo. Así nació `NC-0343` (37 filas corridas en uno).

`EJECUTADO` · en la historia completa de los dos archivos:

| | Cuántos | Sobre |
|---|---|---|
| Llaves lógicas que han tenido **más de un número** `RES` | **135** | 208 |
| Números `CORR` que han nombrado **más de un instrumento** | **82** | 86 |

### 1.2 · Las citas selladas que ya apuntan a otra cosa

`EJECUTADO` · cada cita resuelta contra el archivo de demanda **del momento en que se escribió la spec**, y comparada con lo que ese número nombra hoy:

| | Specs | Citas | Hoy nombran otro slot |
|---|---|---|---|
| `RES-####` en specs de CALC | 35 | 110 | **10** |
| `CORR-####` en specs de CALC | 31 | 50 | **7** |

Las 10 de `RES` son de **dos clases que no se colapsan**:

- **6 derivas posicionales** — los seis `CALC-R-CIV-*`: la identidad escrita **sigue existiendo** hoy con otro número (`RES-0093` → hoy `RES-0095`, etc.; corrimiento +2 uniforme). Coincide 6 de 6 con lo que el informe de `RELEVO-RECONCILIA-1` identificó por otra vía (`parametros.id_celda`).
- **4 claves cambiadas en el consumidor** — `CALC-ENCUCI-0001` (`RES-0005`, `RES-0006`) y `CALC-ENIF-0001` (`RES-0059`, `RES-0060`): la clave escrita **ya no existe**; cambió **en su sitio, con el mismo número**, todas en un solo commit (`6134100f`, 10/sep). **No son renombres puros por igual** (corrección de mesa, verificada): en **ENCUCI** cambió el estimando —`RES-0005` pasó de 0.125822 a 0.126006, y de «tasa base ponderada» a «unión ponderada, condicional a contacto y respuesta válida»—; en **ENIF** sólo cambió la etiqueta —valor (0.06078; 0.054767) y clase **idénticos** antes y después—. En los cuatro el consumidor declara el alias: `milpa/tramite.yaml:77,86` (ENCUCI) y `:1518,1519` (ENIF, con el comentario *«etiqueta corregida por NC-0127 sin cambiar cálculo ni adopción»*). Aquí el número posicional acertó **por accidente**.

Las 7 de `CORR` son los seis CIV más `CALC-ENVIPE-0001`.

### 1.3 · Lo que la vista muestra hoy por culpa de eso

`EJECUTADO` · `data/corrida0/relevo-usos-v1_0.tsv`: en **6 filas** la vista propone como candidato **el CALC equivocado** — p. ej. `CALC-R-CIV-M-02` como candidato de `CIV-M-01:L:L+corpus`, y `CALC-R-CIV-M-01` como candidato de un coeficiente de `procedencia` sobre gobierno digital. Su veredicto es `SIN-CANDIDATO`, así que no hay adopción equivocada; hay una atribución equivocada a la vista de quien la lea.

Y en las 4 filas renombradas la vista marca `YA-ADOPTADO` (tres) y `VETADO-POR-DECISION` (una) **gracias** a que el número acertó por accidente. **Esto es un riesgo del propio diseño** (§3.2).

### 1.4 · `NC-0213` era deriva, no error de autor

`NC-0213` (ABIERTA, reasignada a TUBERÍA por la firma B5 del 21/sep) dice que `CALC-ENVIPE-0001` cita `CORR-0009` cuando la corrida correcta es `CORR-0007`. `EJECUTADO`: **cuando la spec se escribió, `CORR-0009` era ENVIPE 2025 y contenía `RES-0027`/`RES-0028`.** El autor citó bien; la demanda se re-derivó después. Se cierra con la resolución al momento de escritura, sin tocar la spec sellada.

### 1.5 · El código también fija números

`EJECUTADO` · censo en `tools/`, `tests/` y `.claude/`: **149 números `RES`/`CORR` literales en 11 archivos** — `tests/test_corrida0.py` (84), `tools/rutas_sin_candidato.py` (24), `tools/relevo_candidatos_delta.py` (14), y ocho más. Hoy son correctos porque los tests pasan; la próxima re-derivación de la demanda los re-apunta en silencio.

### 1.6 · El contador no se mueve con esto

`LEÍDO` · `tools/corrida0.py:4575`: `dependencias_numericas_legacy_activas` cuenta usos cuyo consumidor **lee** GEN1 (`generacion_leida`), no candidatos de la vista. **Arreglar la identidad es neutral para el contador por construcción.** Los 37 slots ciegos del informe de `RELEVO-RECONCILIA-1` son sobre todo `CALC-SIN-PIN` (64 slots de 11 CALC que no escriben ningún pin): **eso no lo arregla la identidad**, lo arreglan los pines de mesa, que ya existen y son decisiones de contenido.

## 2 · La propuesta

### 2.1 · El número `RES` se congela como alias estable

`data/corrida0/registro-res.tsv`, persistente y sólo-añadir: `llave_logica → RES-####`.

- **Contenido inicial = la numeración de hoy.** Ningún número actual cambia; los 149 literales del código y toda cita escrita desde hoy siguen valiendo.
- **Un slot nuevo** toma el siguiente número libre. **Un número retirado no se reusa nunca**: el registro guarda también los números retirados.
- **Asignar es un paso explícito** (al estilo de `registro --escribe`). **Ningún comando de lectura escribe el registro** —ni `demanda`, ni `status`, ni el CI, ni `tests/test_corrida0_oro.py`, que corre `demanda` y promete restaurar lo que toca—. Un slot sin número hace **fallar la lectura en voz alta**; nunca recibe número en silencio. Así una corrida en una rama sucia no quema números.
- `_asigna_ids` deja de numerar por posición y lee el registro (diff en §4).

`EJECUTADO`, prototipo contra los 210 slots reales: numeración de hoy preservada **210/210**; un slot insertado al principio de `tramite` → **0** números existentes cambian y el nuevo recibe `RES-0211` (con el esquema actual cambiarían todos); un renombre con alias declarado conserva su número, sin alias recibe uno nuevo y el viejo queda retirado.

### 2.2 · El alias se lee del consumidor, y hereda número sólo si su dueño lo certifica

El dato ya vive en la casa: `milpa/tramite.yaml` lleva `aliases:` y `milpa/src/emisor.py` ya lo lee. Un archivo aparte duplicaría el dato (D-15). Por eso: **el alias se lee del campo `aliases:` del consumidor**; un archivo propio de alias sólo nace el día que un consumidor que **no** puede llevar el campo —uno sellado— lo necesite, y no antes (§1: no se instrumenta lo que no ha ocurrido). **Heredar el número es una decisión de contenido**: sólo ocurre si quien es dueño del consumidor certifica que es el mismo slot, y la declaración `aliases:` en el propio consumidor es esa certificación (firma de mesa, §7). Sin certificación, el nombre viejo se **retira** y el nuevo recibe número propio. Los cuatro de `6134100f` están declarados en el consumidor.

### 2.3 · Las citas selladas se resuelven al momento en que se escribieron

`data/corrida0/pines-sellados-resueltos.tsv`, **una fila por cita** `RES`/`CORR` en una spec sellada: `(CALC, token) → llave(s) lógica(s)`, resuelta contra la demanda del commit que fijó la spec. Se calcula **una vez**, con historia completa, en el acto; y como las specs selladas no cambian, la tabla no crece salvo por specs selladas antes del congelamiento. Hoy serían **160 filas** (110 + 50), de las que 17 difieren de lo que el número dice hoy.

### 2.4 · `CORR` deja de ser citable

No tiene llave natural: su única identidad inyectiva es el conjunto de llaves de sus slots, y eso cambia en cuanto un slot entra al grupo. Y el único canal que la usa (`C3-CORRIDA`) **sólo acredita cobertura**. Así que: `CORR-####` queda como etiqueta derivada, de lectura; **las specs nuevas citan slots por llave, nunca `CORR`**; las 50 citas viejas se resuelven a las llaves de sus slots por la tabla de §2.3.

### 2.5 · La vista casa por llave

`tools/relevo_usos.py`: los canales `C1-MAPA`, `C1-SINGULAR`, `C2-RESULTADO` y `C3-CORRIDA` dejan de casar por el token `RES-####` de la spec y casan por **llave**: cita sellada → tabla de §2.3 → llave; cita nueva → llave directa, o `RES` → registro → llave.

### 2.6 · Guardas — cada una con el defecto que ya ocurrió

| Guarda | Qué falla | Defecto que atrapa |
|---|---|---|
| **G1** registro inmutable | un par llave→número de `main` que cambia en el PR | la deriva de §1.1 (135 de 208) |
| **G2** sin reúso | un número retirado reasignado | un pin viejo que re-apunta a un slot nuevo |
| **G3** citas nuevas | una spec añadida o tocada que cita un `RES` inexistente en el registro de la base, o que cita `CORR` | las 17 citas de §1.2 |
| **G4** sin citas colgantes | una llave citada por pines de mesa, por la tabla de §2.3 o por un alias, que ya no existe en la demanda ni está declarada retirada o renombrada | los 4 renombres de §1.2 |
| **G5** tabla completa | una cita `RES`/`CORR` en una spec sellada sin fila en la tabla de §2.3 | una spec sellada que la vista no sabe leer |

| **G6** biyección | una llave vigente con dos números, un número con dos llaves, o una llave vigente que figura a la vez como alias de otra | el registro del diff v1.0, donde el nombre viejo y el nuevo quedaban vivos apuntando al mismo número |

**Historia y base.** G2, G4, G5 y G6 no necesitan historia de git. **G1 y G3 sí necesitan la ref base**, porque comparan contra el registro de `main`: en CI corren en un job con su propio clonado que traiga la base, sin mutar el clon de la suite (D-23). La historia completa se usa una sola vez, en el acto, para construir la tabla de §2.3.

**Un slot nuevo se cita por llave hasta que su número entra a `main`** —también en la nota y en el ADR del PR que lo crea—, porque si otro PR fusiona antes, su número provisional cambia al re-numerar.

**Concurrencia del registro.** Dos PR que añaden slots a la vez chocan en el registro. Se resuelve re-derivando tras fusionar `main`: el segundo recibe el siguiente número. Es seguro **porque G3 impide que nada cite un número que aún no existe en `main`**.

## 3 · Riesgos

### 3.1 · El diseño no quita ceguera

Los 37 slots que la vista no ve son casi todos CALC que no escriben pin. El diseño impide que el problema **crezca** y arregla lo que está **mal atribuido**; lo que está **sin atribuir** sigue siendo trabajo de pines de mesa. Leer «se arregló la identidad» como «se arregló el contador» sería el error.

### 3.2 · Sin los alias, el diseño rompe tres adopciones

Si la vista pasa a casar por llave resuelta al momento de escritura **sin** leer los 4 alias del consumidor, las filas `RES-0005`, `RES-0059` y `RES-0060` (hoy `YA-ADOPTADO`) y `RES-0006` (hoy `VETADO-POR-DECISION`) **pierden su enlace**: la llave que escribió su spec ya no existe. **La lectura de alias va en el mismo acto que el cambio de la vista, o el acto no se lanza.** Criterio de hecho: la vista re-derivada después del cambio difiere de la de antes **sólo** en las 6 filas CIV mal atribuidas y en la de `NC-0213`, y el contador queda igual.

### 3.3 · La tabla de §2.3 depende de un momento

Se resuelve contra el commit que fijó la spec por última vez. Para specs selladas es lo mismo que el commit de sello. Para specs no selladas no aplica: G3 las obliga a citar por llave o por número existente cuando alguien las toque.

## 4 · El cambio en `tools/corrida0.py` — referencia, no receta

*Firma D-r4: el acto no pasa por revisión de dirección; «hecho» son los criterios por comando. El prototipo de abajo es el de v1.0 y **tiene dos defectos que mesa señaló**: asigna número dentro de `demanda` (debe ser un paso explícito aparte) y deja vivos el nombre viejo y el nuevo (viola la biyección). Se conserva como referencia del mecanismo.*

Hoy:

```python
def _asigna_ids(filas: list[dict]) -> None:
    for i, fila in enumerate(filas, start=1):
        fila["resultado_id"] = f"RES-{i:04d}"
```

Propuesto (prototipo probado, §2.1):

```python
def _asigna_ids(filas: list[dict]) -> None:
    """RES deja de ser posicional: se lee del registro persistente
    llave_logica -> RES (data/corrida0/registro-res.tsv). Un slot nuevo toma el
    siguiente numero libre; un renombre declarado hereda el suyo; un numero
    retirado no se reusa. Llamar varias veces en la misma corrida es estable."""
    registro, alias = _registro_res()           # carga una vez y cachea en el proceso
    heredado = {nuevo: viejo for viejo, nuevo in alias.items()}
    usados = {int(v[4:]) for v in registro.values()}
    for fila in filas:
        k = pines_mesa.llave_logica(fila["consumidor"])
        if k not in registro and heredado.get(k) in registro:
            registro[k] = registro[heredado[k]]
        if k not in registro:
            n = max(usados, default=0) + 1
            usados.add(n)
            registro[k] = f"RES-{n:04d}"
        fila["resultado_id"] = registro[k]
```

Corregido en v1.1: `_asigna_ids` **sólo lee**; si falta un número, falla con el nombre del slot. Asignar vive en un subcomando explícito con `--escribe`. Los alias vienen del campo `aliases:` del consumidor. Y una columna `llave_logica` en `demanda-resultados.tsv` para que quien lea la vista vea la identidad y no sólo el alias. **`CORR` no cambia de numeración**: queda como etiqueta derivada, y lo que deja de hacerse es citarlo. En total, del orden de 40 líneas en `corrida0.py`.

## 5 · Decisiones para mesa

**D-r1 · ¿Congelar `RES` como alias estable, o migrar todo a llave y dejar `RES` posicional?**
Opción A: congelar (§2.1). Opción B: migrar las 110 citas de specs —imposible en las selladas—, los 149 literales del código y la vista a llave, y dejar el número moviéndose.
*Recomendación de TUBERÍA:* **A**. Mismo resultado de identidad, sin tocar código que hoy funciona, y con un id corto y dictable que ya no miente. (v1.0 citaba aquí una «firma del 20/sep»: era una valoración de mesa en chat, no una firma, y no está en el repo. Queda sustituida por la firma de §7.)

**D-r2 · ¿`CORR` deja de ser citable?**
Opción A: sí, etiqueta derivada de lectura; las citas viejas se resuelven por la tabla. Opción B: darle registro propio como a `RES`.
*Recomendación de TUBERÍA:* **A**. 82 de 86 ya derivaron, no hay llave natural que congelar, y el único canal que lo usa sólo acredita cobertura.

**D-r3 · ¿Se declara el espacio `celdas` para `milpa/src/celdas.py`?**
Los 6 consumidores `CORTES_C1:*` no tienen llave. `pines_mesa.py` dice que un espacio nuevo *«se declara ahí, no se infiere»*, porque declararlo los vuelve pineables.
*Recomendación de TUBERÍA:* **sí**, `celdas::CORTES_C1::<corte>`. Sin llave no pueden entrar al registro, y quedarían como los únicos seis slots con número posicional.

**D-r4 · ¿Quién toca qué?**
El diseño toca tres herramientas: `tools/corrida0.py` (tuya: el diff de §4), `tools/pines_mesa.py` (una línea en `_ESPACIOS`, si D-r3) y `tools/relevo_usos.py` (los cuatro canales). Opción A: un solo acto de TUBERÍA con autorización explícita sobre las tres, y el diff de `corrida0.py` revisado por dirección antes de congelarlo. Opción B: dirección aplica el diff de `corrida0.py` en su propio acto y TUBERÍA hace el resto después.
*Recomendación de TUBERÍA:* **A**. El registro, los alias, la vista y las guardas sólo tienen sentido juntos —§3.2 lo mide—; partirlos deja una ventana en la que la vista casa por llave sin alias, o el registro existe sin que nadie lo lea.

## 6 · Lo que cierra y lo que no

**Cierra:** la deriva futura de `RES` (135 de 208 llaves la sufrieron) · las 17 citas selladas mal resueltas · las 6 filas mal atribuidas de la vista · `NC-0213` (deriva, no error de autor) · `NC-0343` en su causa estructural · el riesgo de los 149 literales del código.

**No cierra:** los 37 slots ciegos por `CALC-SIN-PIN` (pines de mesa) · `NC-0393` (el vocabulario de `RE_ENLACE`, que no reconoce «candidato para»; es adyacente pero es otro defecto) · la renumeración de `ADR` (su careo propio) · ninguna adopción · el contador, que no se mueve.

## 7 · Firmas de mesa (21/sep/2026) y decisiones resueltas

**D-r1:** opción A. **D-r2:** opción A — *«Resolver cada cita vieja a los slots que tenía el grupo en ese momento es incluso mejor que lo actual, porque un slot que entró después ya no recibe crédito.»* **D-r3:** sí, con el nombre **`cortes-C1::<corte>`**, para no confundirlo con `celda-D::`. *«Declarar el espacio no obliga a nada: un pin sigue exigiendo tu firma y las guardas de 4.1.»* **D-r4:** opción A, **sin revisión del diff**; «hecho» son estos criterios, verificables por comando sobre el commit final con `main` fusionado:

1. la numeración de hoy se preserva 210/210;
2. la vista re-derivada difiere sólo en las 6 filas CIV y en la de `NC-0213`;
3. `status` y el contador quedan idénticos;
4. el test de oro pasa sin tocar el registro;
5. las guardas G1 a G5 y la de biyección están en CI.

**Texto de firma, verbatim:**

> «RES se congela como alias estable de la llave lógica; asignar número es un paso explícito y ningún comando de lectura escribe el registro. CORR deja de ser citable. Se declara el espacio cortes-C1. Un alias hereda número solo si quien es dueño del consumidor certifica que es el mismo slot; el par ENCUCI queda certificado por tramite.yaml:77,86. Un solo acto de TUBERÍA toca las tres herramientas; "hecho" son los criterios por comando, no una revisión.»

**El par ENIF, con las líneas que mesa pidió** (`6134100f`, `data/corrida0/demanda-resultados.tsv`): `RES-0059` `desconfianza_como_razon_principal_conoce_proteccion_enif2024` → `desconfianza_o_mal_servicio_como_razon_principal_conoce_proteccion_enif2024`, valor 0.06078 → 0.06078, clase idéntica; `RES-0060` idem, 0.054767 → 0.054767. Es un cambio de etiqueta puro, y el consumidor declara el alias en `milpa/tramite.yaml:1518,1519`. **Por la regla firmada —el alias declarado por el consumidor es la certificación de su dueño— queda certificado por esas dos líneas**, igual que ENCUCI por `:77,86`. Además, el criterio 2 sólo es alcanzable si lo está: sin él, `RES-0059` y `RES-0060` perderían su enlace en la vista.

**Fuera, y está bien así** (mesa): las menciones de `RES` en `decisiones.tsv` (38), en firmas (23) y en `NC` (164) son prosa para humanos; con el congelamiento dejan de envejecer. El resolvedor «qué nombraba `RES-X` en tal fecha» **sale gratis** —es la misma función que construye la tabla de §2.3—, así que se expone como comando.
