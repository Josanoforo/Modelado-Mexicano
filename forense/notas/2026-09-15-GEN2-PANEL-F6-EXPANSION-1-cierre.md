# ACTO GEN2-PANEL-F6-EXPANSION-1 · EL ALIMENTADOR DE F6 — LA LISTA CRECE A 27 Y LAS EJECUTABLES SIGUEN SIENDO DOS

**15/sep/2026 · entorno NUBE · Opus · cero llamadas a modelo · cero microdato abierto · cero adopciones · cero escrituras en la cola de adquisición.**
Sucesor de `ACTO GEN2-F5-CIERRE-Y-PANEL-1` (`PR #791`), cuyo `P2` entregó `F5-panel-candidatos-v1_1.tsv` con 13 filas y 2 retenidas realistas.

## 0 · Qué se pidió y qué salió

| | pedido | salió |
|---|---|---|
| **Sonda CONSTRUCTO/HERMANAS** sobre instrumentos sin exposición al desarrollo, en los cuatro dominios de `M` | ampliar el panel hasta **≥6 familias retenidas ejecutables con reserva** | **HECHO, Y SIGUE SIN ALCANZAR.** La lista nominal pasa de 13 a **27 filas** y de 7 a **10 retenidas**; las **ejecutables con reserva siguen siendo 2**, y otras 2 cuelgan de una sola firma |
| **El paso barato que vuelve firme a MOCIBA** (leer los `FD` 2021/2023 y fijar la batería de denuncia) | una familia congelable | **NO EJECUTABLE EN NUBE**, declarado con A.4, no supuesto: `data/raw` no montada y `inegi.org.mx` responde `000` / `CONNECT 403` por política del proxy. **En su lugar se dio el mismo paso barato donde sí se podía**, y salió: `R09 · ISSP` quedó con reactivo, universo, ponderador y dominios fijados **sin abrir payload y sin red** |
| **Enterprise Survey** | dejarla como pregunta a mesa, sin resolverla | **NO RESUELTA**, y ahora **vale por dos**: `R08 · ENCRIGE`, la hermana nacional de `ENCIG`, depende de la misma firma |
| **Tabla de «qué falta conseguir»** al servicio de adquisición, sin escribir en su cola | una tabla por familia | **HECHA**: `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv`, 9 filas. `data/cola-adquisicion-v1_0.tsv` y `data/curacion-registro/` **sin tocar** |
| **Parada** | 6+12, o universo agotado declarado con A.4 | **Para por la segunda**: el universo de instrumentos no expuestos se agotó en los cuatro dominios. §4 |

**El titular:** la lista se duplicó y el diagnóstico no cambió — y eso es el hallazgo, no el fracaso. Ahora se puede decir **con nombre y cita por instrumento** que el cuello de botella de `F6` no es la búsqueda: es que **cada familia limpia muere por una de tres causas repetidas** —una sola ola levantada, unidad que no es persona, o un documento que la nube no puede abrir— y las tres tienen remedio conocido y barato.

---

## 1 · La corrección que este acto le hace a su antecesor

`v1_1` declaró para `R01 · MOCIBA`: *«`CALC`/marco/`corridas-R`/`prereg-caja` 0»*. **Es incorrecta.** El marco congelado piloto trae **dos celdas MOCIBA**:

```
marco-congelado-piloto-v1_0.tsv
  TIC-10  MOCIBA 2023  P4_01  FACTOR  ... prueba del bibliotecario FP-93 ... abriendo mociba2023_tabulados.xlsx
  TIC-11  MOCIBA 2024  P3     FACTOR  ... abriendo mociba2024_tabulados.xlsx (61 cuadros)
```

y `crosswalk-pregunta-regla-v1_1.tsv` las cita con veredicto `NO-EMITE`. Hay además una **contaminación `ADR-46` de estructura declarada el 4/ago/2026** sobre el `FD` 2024 (`forense/hallazgos.md:120`: *«esta sesión no queda "limpia sin matiz" para pre-registrar contra ENDUTIH/MOCIBA/ENASEM»*).

**Consecuencia operativa, no retórica:** el par que `v1_1` proponía —2021 y **2023**— usaba una ola que ya es celda de otro marco. `v1_2` mueve el par a **2021 y 2022** y deja 2019/2020/2025 de reserva. `v1_1` **no se reescribe** (una sucesora no reescribe a su antecesora); la corrección vive en `v1_2` y aquí.

---

## 2 · Las cuatro familias nuevas que sí son algo

### 2.1 · `R09 · ISSP` (FAM) — la que se pudo volver firme sin payload y sin red

El encargo pedía un paso barato de lectura documental. En la nube **no** se puede leer el `FD` de MOCIBA; sí se puede leer el **inventario canónico**, y ahí estaba:

```
data/inventario-reactivos-descargas-mx-v1_2.tsv   (ZA6980_v2-0-0.dta, 357 variables CON etiqueta)
  v26       Q8a Whom or where to ask for help: borrow large sum of money?
  WEIGHT    Weighting factor
  c_alphan  Country/ Sample Prefix ISO 3166 Code
  SEX · URBRURAL · AGE · CASEID · MX_INC · MX_REG · MX_RELIG …
```

Con eso quedan fijados **reactivo** (`v26`), **universo** (Mexico por `c_alphan`, `N = 1002` verificado el 31/ago/2026 en `data/cola-adquisicion-v1_0.tsv`), **ponderador** (`WEIGHT`) y **dominios** de las dos celdas (`SEX`, precedente literal de `TIC-10`/`TIC-11`, que declaran su universo *«por sexo»*). Falta **una sola cosa**: las categorías de respuesta de `v26` — etiquetas de **valor**, que el inventario no guarda —, y el `PDF` que las trae (`ZA6980_q_mx.pdf`) **ya está adquirido**. `NC-0231`.

La transferencia es de **constructo**: `familia.apoyo.recibe_dinero_familiares` está calibrada en `ENIF 2024` sobre recepción **efectiva** de dinero de familiares; `v26` pregunta a **quién acudiría** para pedir prestada una suma grande. No es la misma cantidad y no se disfraza de serlo: es exactamente el tipo de transferencia que el panel busca.
Reserva: `ZA5900` (ISSP 2012 Family, México) intacta, y dentro de la propia ola 2017 las otras nueve situaciones de apoyo (`v21`–`v25`, `v27`–`v30`) sin tocar.

### 2.2 · `R08 · ENCRIGE` (TRA) — la hermana nacional de ENCIG

`ENCRIGE` es a las unidades económicas lo que `ENCIG` a las personas: mismo INEGI, mismo concepto de trámite. **Limpia en las cuatro superficies** (`grep -ril -F encrige`: 0 en `milpa/`, 0 en el corpus de `L`, 0 en `traza-motor.tsv`, 0 en `data/corrida0` + `prereg-caja` + `corridas-*`, 0 en marcos y crosswalk). Los tabulados 2020 ya adquiridos traen los cuadros que la regla necesita (*«Trámites, pagos o actos de autoridad»*, *«Percepción sobre la frecuencia de actos de corrupción»*, *«Causas del desinterés: es necesario dar sobornos»*), y el precedente `EMP-01…EMP-04` del marco piloto ya construye celdas como razones por dominio sobre tabulados.

**Y por eso mismo no cuenta todavía:** su unidad es el establecimiento — la **misma** pregunta que `R02 · WBES`. El encargo ordena dejarla planteada y no resolverla, y no se resolvió. Lo que `v1_2` añade es que **la firma ahora vale por dos familias**, y que la versión nacional es más barata que la del Banco Mundial. `NC-0233`.

### 2.3 · `R10 · ENCO` (DIN) — la única puerta que le queda al dominio vacío

El dominio `DIN` perdió a `Global Findex` por exposición (el corpus de `L` lo cita **con cifra**) y a la `ENCF` de Banxico/CNBV porque ya es universo de evaluación (cinco celdas `DIN-07…DIN-12` del marco piloto y `payload_id` en `corridas-R/DIN-07.json`). Queda `ENCO`: mensual desde 2001 —reserva prácticamente infinita—, con `FACTOR` en el archivo y **limpia en las cuatro superficies**. El único hit fue la frase *«confianza del consumidor»* en prosa sobre marcas, adjudicado a mano como **falso positivo**.
Falta lo barato primero: leer el cuestionario ya adquirido y ver si alguno de los 15 ítems pregunta por **posibilidad de ahorrar**. Sólo si eso devuelve `EXISTE-SATISFACE` se pide adquisición. `NC-0232`.

### 2.4 · `R11 · ENPOL` (TRA) — limpia en desarrollo, comprometida en el marco

Cero huella en `milpa/`, corpus y `traza-motor`. Pero la única ola adquirida (2021) **ya es la celda `CIV-12`** del marco piloto, con variable `P3_21_1` fijada y prueba del bibliotecario corrida, y `ENPOL` sólo tiene dos olas en el mundo. Con `ENPOL 2016` adquirida pasa a dos olas, **una sola libre**: sigue sin reserva. Se declara así, sin estirarla.

---

## 3 · Las que cayeron, con cita

| familia | causa | cita |
|---|---|---|
| **ENSU** | expuesta en desarrollo | `milpa/procedencia.yaml`, `milpa/src/salida.py`, `milpa-whitepaper`, `milpa-spec`, `milpa-plan` + **4** documentos del corpus de `L` (`grep -rlw ENSU`) |
| **ENCOAP 2023** | expuesta **por la cifra** | `corpus/reports/El_Mexicano_y_el_Tiempo…md:137` — *«la ENCOAP 2023 de INEGI (urbana) reporta que 56.5%…»* |
| **Global Findex** | expuesta por cifra y por lista de fuentes | `Behavioral_Finance_Mexicano…md` (2) y `Non-Family_Social_Capital…md` (1) |
| **ENCF (Banxico/CNBV)** | ya evaluada | `marco-congelado-piloto` `DIN-07/08/09/10/12` · `corridas-R/DIN-07.json` `payload_id=banxico_…_2019` |
| **ENTI 2022 · CPV ampliado 2020** | ya evaluadas | `TIC-05/06`, `EMP-05/06` del marco piloto · `corridas-R/TIC-06.json` |
| **UNAM-IIJ** (*Los mexicanos vistos por sí mismos*, *Cultura Constitucional 3ª*) | ya evaluadas | `prereg-caja/S14-R7-4-spec-v1_0.md` (batería `P55_1_1…P55_7_3`) y `S16-R9-3-spec-v1_0.md` (miembro `.sav` con `sha256` y barrido de ponderador) |
| **ECOPRED 2014 · ELCOS 2012** | limpias, **una sola ola** | manifiesto: 1 ola cada una; no hay segunda que comprar |
| **ENH 2017** | limpia, **sin reactivo** (A.15) | sobre las **181** filas de `ENH` en `inventario-reactivos-descargas-mx-v1_2.tsv`, el patrón `remes|ahorr|transf|apoyo|ingres|dinero|beca|jubil` devuelve 4 nombres y los cuatro son becas o jardinero → `EXISTE-NO-SATISFACE` |
| **GPS · CNBV-BDIF · OMCA · JPAL · Votar entre Balas · Interacting as Equals · IIEG · ENCEVI** | **limpias y aun así no elegibles** | ninguna de las cinco reglas de `M` emite sobre preferencias, eventos, agregados administrativos o experimentos con brazo asignado |

**Un defecto de método, corregido dentro del acto.** La primera pasada usó los tokens `ensu20`/`ensu_` para `ENSU` y la dio por **limpia**. La palabra completa (`grep -rlw ENSU`) la encuentra en `milpa/` y en cuatro documentos del corpus. Es el gemelo del defecto que `v1_1` documentó al revés (`\bENGASTO\b` perdía `engasto2012`): **una sola forma de buscar no basta en ninguna de las dos direcciones**, y por eso cada coincidencia de este acto se adjudicó a mano.

---

## 4 · A.4 — la parada, con el universo declarado

**Clasificación: `NO-ENCONTRADO`** para *«una sexta familia retenida ejecutable con reserva en los cuatro dominios de `M`»*, con este universo:

- **Qué se examinó.** `data/manifiesto.yaml` (**1 610** entradas, agrupadas en **250** raíces de instrumento); `data/cola-adquisicion-v1_0.tsv` (**153** filas, **~150** fuentes canónicas con estado); los tres inventarios de reactivos vigentes (`-v1_2`, `-descargas-mx-v1_2`, `-ext-v1_0`); `forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv` (60 celdas), `marco-M-sorteado-v1_3.tsv` (14), `crosswalk-pregunta-regla-v1_1.tsv` y `enlace-M-v1_0.md`; `forense/prereg-caja/**`; `data/corrida0/**`; `milpa/**`; los **37** documentos del corpus de `L`; `traza-motor.tsv` (5 reglas, 4 dominios).
- **Con qué mecanismo.** `grep -ril -F <token>` y `grep -rlw` por instrumento sobre cuatro superficies (desarrollo · evaluación · marcos · crosswalk), **58 tokens** en tres barridos, con **adjudicación a mano de cada coincidencia** — la subcadena produce falsos positivos (`ensu` dentro de `censual`, `enco` dentro de `encontrado`) y la frontera de palabra produce falsos negativos (`engasto2012`).
- **En qué fecha.** 15/sep/2026, contra `origin/main = 0cdbd72`.
- **Qué NO se examinó, dicho sin disfraz.** Ningún payload: `data/raw` no está montada (`tools/entorno.py` → `corpus=NO(examinados=0)`), así que **ninguna** afirmación de este acto sobre contenido de microdato existe; todas son sobre manifiesto, inventario y documentación versionada. Y no se buscó fuera del repo: un instrumento que nadie haya registrado nunca queda fuera de este universo por construcción, y eso es una **cota del censo, no del mundo**.

**Conclusión del A.4:** dentro de ese universo, las familias limpias en las tres superficies de desarrollo están **enumeradas y agotadas**; ninguna de las no enumeradas sobrevive a los tres filtros (dos olas libres · unidad persona · regla de `M` que emita a ciegas). La lista nominal de **6+12** que `FP-374` exigía **no existe hoy**, por segunda vez y ahora con el doble de nombres.

**Y una premisa que cambió mientras el acto corría, declarada y no escondida.** Al integrar `origin/main` para cerrar (`PR #794`) entró la **Hoja de firmas 2**: `FP-374` ya **no está ABIERTA** — quedó `FIRMADA-CON-ALCANCE-ACOTADO` por `F-16` (15/sep/2026), que autoriza *«con 7 retenidas, factibilidad acotada AHORA (piloto de 6, producto = tabla `d_f` por familia con IC, parada = primer resultado que decida H0), en vez de seguir adquiriendo»*. Este acto **no la toca y no la re-propaga** (`forense/firmas-pendientes.tsv` sin tocar; la firma sobre `R02`/`R08` viaja en el acto de caja que sigue). Pero su producto es **insumo directo** de esa firma y le corrige dos cosas, que es justo para lo que servía: las retenidas son **10**, no 7 — y **sólo 2 son ejecutables con reserva**, ninguna congelable desde la nube. Un piloto de 6 sobre este panel tendría hoy **2 familias con material y reactivo**, dos colgadas de la firma de unidad y el resto sin segunda ola.

---

## 5 · Lo que este acto NO hizo

No lanzó llamadas · no abrió microdato ni ningún payload · no escribió en `data/cola-adquisicion-v1_0.tsv` ni en `data/curacion-registro/` · no reescribió `F5-panel-candidatos-v1_1.tsv` · no resolvió la pregunta de unidad (`R02`/`R08`) · no congeló ninguna spec · no tocó `marco-congelado-piloto-v1_0.tsv` ni ninguna celda · no tocó `FP-374` ni propagó ninguna firma · no abrió `F6` · y **no estiró la lista para llegar a seis** — por segunda vez, con el doble de nombres y la misma respuesta.

## 6 · Perímetro

Escritos: `forense/prereg-duelo-v2/F5-panel-candidatos-v1_2.tsv` (27 filas × 17 columnas, sucesor de `v1_1`), `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv` (9 filas, entrega a adquisición **fuera** de su cola), cinco filas `NC-0230…NC-0234` en `forense/no-corrido.tsv`, el encargo archivado (0-bis A.3), esta nota y la cascada administrativa de costumbre.

---

## 7 · La entrega a adquisición, hecha por la fuente y no por su cola

El encargo pide entregar la tabla *«sin escribir en su cola»*. Se cumplió en los dos sentidos:

1. **La tabla** vive en `forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv`, fuera del perímetro del servicio.
2. **El ruteo** se hace donde el propio servicio lo lee: `forense/no-corrido.tsv`. Verificado, no supuesto — importando `tools/adq_investigacion.py` y llamando sus funciones sobre las cinco filas reales:

```
NC-0230  FUENTE_O_VARIABLE        LISTA_SONDA        servicio-gen2-38
NC-0231  PREPARACION              NO_SONDA           CAJA/Ubuntu con la raiz montada
NC-0232  DECISION_O_IMPLEMENTACION NO_SONDA          CAJA/Ubuntu
NC-0233  DECISION_CIENTIFICA      ESPERA_O_DELEGADA  mesa
NC-0234  DECISION_O_IMPLEMENTACION ESPERA_O_DELEGADA FP-374 + NC-0230/0231/0232
```

Las tres clases caen donde deben: lo que es adquisición va al servicio, lo que es lectura de un documento ya adquirido va a CAJA, y la firma va a mesa.

**La proyección derivada (`data/adq-demanda-activa-v1_0.json`) NO se regeneró.** Se probó: el generador corre sin error (el `KeyError` de `NC-0220` ya está arreglado en `main`), pero su salida difiere de la versión en el árbol en **403 inserciones y 238 borrados**, y el grueso no es de este acto — es deriva acumulada de otros actos entre la última regeneración y hoy (cambios de `adopcion`, `contrato_id`, `camino_linaje` de objetos ajenos). Regenerarla desde aquí atribuiría a este acto el trabajo de otros; se revirtió y la fuente queda diciendo lo que debe decir, que es de donde la proyección lo tomará sola.

---

## 8 · Cascada de renumeración (renumera quien fusiona segundo)

La fila de este acto se renumeró **dos veces**, y las dos por la misma razón de siempre: otro acto fusionó antes.

| sync | quién llegó primero | qué tomó | lo mío pasa a |
|---|---|---|---|
| 1º (`ce79136`) | `GEN2-ARCHIVO-LECTURA-F5-1` (`PR #794`) | `NC-0225` | `NC-0225…0229` → **`NC-0226…0230`**; `ADR-517` seguía libre (máximo real 516) |
| 2º (`3880cf4`) | `GEN2-MANTENIMIENTO-Y-ARCHIVO-2` (`PR #795`) | **`ADR-517`** y `NC-0226…0229` | `ADR-517` → **`ADR-518`** y `NC-0226…0230` → **`NC-0230…0234`** |

En los dos casos el lado de `main` queda **intacto** y se mueve el mío. Los cuatro conflictos del segundo sync (`no-corrido.tsv`, `registro-rotulos.tsv`, `gobernanza-v1_15.md`, `estado-programa-v1_13.md`) se resolvieron igual: se toma el archivo de `main` **entero** y se le añade encima sólo la pieza propia, ya renumerada — cero filas y cero entradas ajenas alteradas.

El primer sync trajo además la **Hoja de firmas 2** (§4, el cambio de premisa de `FP-374`); el segundo trajo `GEN2-VALIDACION-INDEPENDIENTE-2` (`PR #799`) y `GEN2-MANTENIMIENTO-Y-ARCHIVO-2`, ninguno de los cuales toca el panel, el marco piloto ni las superficies de la auditoría de exposición: **ninguna cifra ni clasificación de este acto cambia por los dos merges**, sólo sus identificadores.
