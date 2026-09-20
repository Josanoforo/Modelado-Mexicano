# `ACTO GEN2-CELDA-D-PILOTO-3-EJECUCION` · S2 y S1 cerradas por texto; COMMIT-2 PARA: la guardia S2 dispara y, detrás de ella, el código congelado no tiene cuerpo de medición

**20/sep/2026 · CAJA (`ENTORNO-DERIVADO = CAJA`, corpus montado, `archivos_examinados = 419`) · Opus 5 · rama `acto/gen2-celda-d-piloto-3-ejecucion` · base `8b7b0562` = `origin/main` al abrir (`git rev-list --count HEAD..origin/main` → `0`).**

Encargo archivado (A.3): `forense/encargos/2026-09-20-GEN2-CELDA-D-PILOTO-3-EJECUCION.md`.

**COMPUERTA (A.1, tres estados, por producto):** `git cat-file -e origin/main:<ruta>` → `OK` para `data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0001/spec.yaml`, `…/medidor.py`, `forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_0.md` y su sidecar (`…-spec-v1_0.sha256`; el encargo lo nombra `.md.sha256`, la convención de la carpeta es sin `.md`). `sha256sum -c` → `OK`, `20c358b6…`. COMMIT-1 = `352c7aed` (`#903`).

**F3:** esta sesión no leyó los diseños A y B ni el careo (`ADR-533`); abrió sólo lo que el encargo nombra: la spec congelada, el medidor congelado, la nota P0 de `#903` (para saber qué dejó abierto) y los seis PDF de ENCIG.

**Lo que este acto NO hizo (E.6):** no editó spec, medidor, λ, lista PUNTUADA, umbrales, B-bis; no abrió `encig25_base_datos_csv.zip`; no agrupó nada de 2025 por dos variables; no parchó el código congelado.

---

## 1 · S2 · Qué significan `97`, `98` y `99`, por ola — texto literal del descriptor

Fuente: `Estructura de la base de datos`, tabla `RESIDENTES`, variable `EDAD` (pregunta 2.5 «¿Cuántos años cumplidos tiene (NOMBRE)?»). Hash de cada PDF verificado contra `data/manifiesto.yaml` (prefijo de sha256 en la tabla).

| código | ENCIG 2021 (`encig21_estructura_base_datos.pdf`, `365c031b…`) | ENCIG 2023 (`encig23_estructura_base_datos.pdf`, `eb89820c…`) | ENCIG 2025 (`encig25_estructura_base_datos.pdf`, `09e1b19b…`) |
|---|---|---|---|
| `00` | «Menor de un año» | «Menor de un año» | «Menor de un año» |
| `01…96` | «Años cumplidos» | «Años cumplidos» | «Años cumplidos» |
| **`97`** | **«97 o más años»** | **«97 años o más»** | **«97 años o más»** |
| `98` | «Edad no especificada en personas de 18 años o más» | «Edad no especificada en personas de 18 años y más» | «Edad no especificada en personas de 18 años y más» |
| `99` | «Edad no especificada en personas menores de 18 años» | «Edad no especificada en personas de 17 años o menos» | «Edad no especificada en personas de 17 años o menos» |

**Veredicto S2 por texto: `97` ES edad real censurada en las tres olas.** `98` y `99` son no-respuesta. La condición S2 de la spec (`spec.yaml: condicion_suspensiva_2`; `_guardia_suspensiva()`) dispara con `edad_real_censurada = True` en `2021`, `2023` y `2025`.

### 1.1 · Conteo por código, sobre el universo del cruce (2021 y 2023; 2025 NO se abre)

El encargo pide el conteo «si el FD lo permite sin abrir respuestas de 2025». El FD no trae conteos; los payloads de 2021 y 2023 están dentro del perímetro y ya fueron abiertos por los CALC sellados. Universo reproducido con el cargador del script sellado (`tools/encig_cruces_historicos.py::_member_csv`, join `sec_7 ↔ residentes` por `ID_PER`, `N_TRA == 01`, `P7_3 ∈ {1,2,4,5,6}`):

| ola | n universo | residuo F1-bis (97/98/99) | masa `FAC_TRA` | `EDAD=97` | `EDAD=98` | `EDAD=99` | residentes 97+ en el archivo completo |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2021 | 21 152 | **104** | 672 707.0 | **0** | 104 | 0 | 37 |
| 2023 | 20 934 | **107** | 571 754.0 | **0** | 107 | 0 | 21 |
| 2025 | — no abierto — | — | — | — | — | — | — |

Los 104 / 107 de la nota P0 se reproducen exactos. **El residuo es 100 % código `98` (edad no especificada, ≥18): cero trámites con `EDAD = 97` en las dos olas históricas**, aunque el archivo de residentes sí trae personas de 97+ (37 y 21) — ninguna resultó informante elegido con pago de luz. Por texto la regla excluye edad real censurada; por dato, en 2021 y 2023, no excluyó a ningún adulto mayor real. Para 2025 no se sabe y no se mira aquí. Reportado a mesa como `FP-399` (abajo). La rejilla del árbitro (`60-96`) no se toca.

---

## 2 · S1 · `NC-0355` — ¿`P7_3` es el mismo instrumento en 2021, 2023 y 2025?

Fuentes: cuestionario general (`encig21_cuestionario.pdf` `9ee82981…`, `encig23_cuestionario.pdf` `65000ad3…`, `encig25_cuestionario.pdf` `807196d6…`, sección VII) y descriptor (tabla `SEC_7`). Transcripción `pdftotext -raw`/`-layout`; los puntos guía se omiten.

| aspecto | ENCIG 2021 | ENCIG 2023 | ENCIG 2025 |
|---|---|---|---|
| **C5 (entrada a la sección)** | «Ahora le preguntaré por el último (TRÁMITE O PAGO) que usted realizó durante 2021.» | «…durante 2023.» | «…durante 2025.» |
| **Redacción 7.3** | «¿A qué tipo de lugar acudió o a qué medio recurrió para realizar el trámite o pago?» | idéntica | idéntica |
| **Opciones y códigos** | 1 Instalaciones de gobierno (oficinas, tesorería, hospital, etc.) · 2 Banco, supermercado, tiendas o farmacias · 3 Líneas de atención telefónica · 4 Internet (página web, aplicaciones de celular, tablet, etc.) · 5 Cajero automático o kiosco inteligente · 6 Módulos, clínicas u oficinas temporales o móviles · 7 No se ha podido concluir el trámite o pago · 8 Otros (ESPECIFIQUE) · 9 No sabe / no responde · FD: `b` blanco | idénticos; «etc.» → «etcétera» | idénticos; «etc.» → «etcétera» |
| **Instrucción de captura** | «REGISTRA UN SOLO CÓDIGO» | «REGISTRA UN SOLO CÓDIGO» | «REGISTRE UN SOLO CÓDIGO» (voz tú → usted) |
| **Filtro `N_TRA` (universo)** | FD `SEC_7`: `N_TRA` Numérico, `01` = «pago ordinario del servicio de luz»; llave primaria `ENT, UPM, V_SEL, R_ELE, N_TRA` | `01` = «pago ordinario del servicio de luz»; llave `CVE_ENT, UPM, V_SEL, R_ELE, N_TRA` | `01` = «pago ordinario del servicio de luz»; llave `CVE_ENT, UPM, V_SEL, R_ELE, N_TRA` |
| **Flujo que lleva a 7.3** | 6.1 «Durante este año (2021), es decir, de enero a la fecha, ¿usted ha realizado…» → catálogo `01`–`22` → 6.2 cuántas veces → 6.3a «usted mismo?» → «CUANDO EN TODAS LAS OPCIONES DE 6.3a SE REGISTRE “00” PASA A LA SECCIÓN VIII. PARA LOS TRÁMITES Y PAGOS DEL 1 AL 7 INDAGA SOBRE EL ÚLTIMO TRÁMITE REALIZADO POR TIPO» → sección VII: «REGISTRA EL ÚLTIMO TRÁMITE POR TIPO PARA LOS CÓDIGOS DEL 1 AL 7 REPORTADO EN 6.3a» → 7.1, 7.2, **7.3** → salto «PARA TRÁMITE 20, PASA A PREGUNTA 7.7»; 7.4/7.5 «NO APLICAR … SI EN 7.3 LOS CÓDIGOS DE RESPUESTA SON 4, 5 Ó 9» | idéntico (6.3a «usted mismo(a)?») | idéntico en estructura, voz usted («INDAGUE», «REGISTRE», «PASE»); el salto dice «PARA TRÁMITE **21**, PASE A PREGUNTA 7.7» porque el ítem policías se renumeró 20→21 |
| **Catálogo de trámites (6.1)** | `01` «el pago ordinario del servicio de luz?» · `02` agua potable · `03` predial · `04` tenencia · `05` trámites vehiculares · `06` fiscales · `07` cita médica programada · `08` urgencia · … · `20` contacto con policías · `21` abrir empresa · `22` otros — **22 códigos** | **22 códigos**, `01`–`22` con la misma numeración (`07`/`08` añaden «IMSS-Bienestar»; `17` añade «o Fiscalía Estatal») | **23 códigos**: se inserta **`15` «trámites para ser o permanecer como beneficiario(a) de programas [sociales]»** y `15`–`22` de 2023 pasan a `16`–`23`. **`01`–`14` no se mueven.** `06` reordena la frase («trámites fiscales ante el SAT o la Secretaría de Hacienda, tales como…») sin cambiar contenido |

**Veredicto `NC-0355`: `CAMBIO-MENOR`.**

- **Qué cambió:** (i) el catálogo de 2025 inserta un código nuevo (`15`, programas sociales) y desplaza `15`–`22` → `16`–`23`; (ii) la voz de las instrucciones al entrevistador pasa de tú a usted; (iii) «etc.» → «etcétera» y «satisfecho» → «satisfecho(a)» en otras secciones; (iv) `07`/`08`/`17` en 2023+ nombran IMSS-Bienestar / Fiscalía Estatal.
- **Por qué no afecta `{4,5}` sobre `{1,2,4,5,6}`:** el estimando vive en `N_TRA == 01`, cuyo texto («pago ordinario del servicio de luz») y código son idénticos en las tres olas; el desplazamiento del catálogo empieza en `15`; la redacción de 7.3, sus nueve opciones y sus códigos `1`–`9` son idénticos palabra por palabra salvo la abreviatura; el flujo (6.1 → 6.3a → último trámite por tipo para `1`–`7` → 7.3, un solo código) es el mismo y el único salto interno (policías → 7.7) no toca `01`. No hay opción nueva, fusionada ni partida en 7.3; no hay cambio de modo de captura declarado en el cuestionario.
- **No cierra con `MISMO-INSTRUMENTO`** porque el catálogo sí cambió y el veredicto debe decirlo; **no cierra con `CAMBIO-DE-INSTRUMENTO`** porque nada de lo que cambió entra en el estimando.

`NC-0355` pasa a `CERRADA` con este veredicto. `CALC-PISO-PERSISTENCIA-ERROR-0001` **no** se re-rotula (sólo lo mandaba el veredicto de cambio de instrumento). El `+11 pp` de ENCIG sigue sin atribución hasta que el piloto corra: el instrumento es comparable, pero eso no lo convierte en conducta por sí solo.

---

## 3 · COMMIT-2 · PARO — salida cruda del código congelado, sin parche

Con S1 y S2 leídas, se invocó `medir()` de `data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0001/medidor.py` tal cual, con el contrato leído:

```
== intento 1: contrato leído (S1=CAMBIO-MENOR, S2 censura=True en 3 olas)
ParoDeGuardia -> S2: en ['2021', '2023', '2025'] al menos uno de 97/98/99 es EDAD REAL
CENSURADA, así que F1-bis está sacando población del universo. Se REPORTA A MESA ANTES
DE EMITIR. La rejilla sellada del árbitro (60-96) no se toca aquí.
== intento 2 (diagnóstico): mismo contrato con censura=False
NotImplementedError -> COMMIT-2: el cuerpo de medición se completa en la sesión de caja
que abra el microdato, con el contrato de arriba congelado. F3: no la de este acto.
== funciones definidas: ParoDeGuardia, _banda_edad, _expit, _guardia_suspensiva, _logit,
_marginales, _prepara, c2_replica, clasifica_soporte, medir, retadores
== 'bootstrap(' / 'json' / 'ID_PER' / 'adjudica' / '__main__' en el fuente: []
tests/test_piloto3_guardias.py: 24 passed
```

**Dos paros, en cascada, y ninguno se resuelve aquí:**

1. **La guardia S2 es un PARO mecánico, no una nota.** El encargo dice «eso no detiene el piloto … pero se reporta a mesa antes de emitir»; el código congelado dice lo mismo con otra consecuencia: `raise ParoDeGuardia`. Con `97` = edad real censurada por texto en las tres olas, el módulo rehúsa medir hasta que mesa firme. Desactivar la guardia o pasarle `False` sabiendo que es `True` sería parchar (E.6).
2. **Detrás de la guardia no hay medición.** `medir()` es `raise NotImplementedError`. El módulo congelado trae el contrato (universo, desenlace, rejilla, λ, C2 por réplica, retadores, clasificación de soporte) pero **no** trae: carga del payload, join por `ID_PER` (el `_prepara()` que existe une `sec_7` ↔ `residentes` por índice de fila, `left_index/right_index` — un join sin llave entre trámites y personas, distinto del `merge(on="ID_PER", validate="m:1")` del script sellado `tools/encig_cruces_historicos.py:141`), bootstrap por UPM dentro de estrato, IC por celda, `ejecucion.json`/`resultados.json`, derivación de `R(a,b)`, adjudicación, ΔMAE ni B-bis. No hay «modo de emisión» que ejecutar «tal cual». La nota P0 de `#903` declaró «código congelado, `medidor_ejecutado_al_congelar: NO`» y «el COMMIT-2 corre sin ella»; no declaró que el cuerpo estuviera vacío.

**Consecuencia (E.6, verbatim del encargo):** «Si el código congelado no corre, no se parcha: PARO, y el sucesor es un COMMIT-1 v1.1 de otra sesión.» COMMIT-2 y COMMIT-3 no corren. Cero corridas selladas, cero `resultados.json`, cero microdato de 2025 abierto. La spec v1.0 **no** se retira (eso sólo lo manda `CAMBIO-DE-INSTRUMENTO`); queda congelada e inejecutable hasta el v1.1.

### 3.1 · Lo que el COMMIT-1 v1.1 tiene que traer (para la sesión que lo congele; ésta no lo escribe)

- Cuerpo de `medir()` completo: carga de `encig2025_04_sec_7.csv` + `encig2025_02_residentes_sec_2.csv` desde `encig25_base_datos_csv`, join por `ID_PER` `m:1` (no por índice), bootstrap UPM-dentro-de-estrato con réplicas compartidas, C2/C1a/C1b/S½/Sλ con IC por celda, soporte por marginales, `ejecucion.json`/`resultados.json`/sello, modo R + adjudicación + ΔMAE + B-bis para el COMMIT-3.
- Semántica de S2 decidida por mesa **antes** de congelar: o la guardia S2 se queda como PARO (y entonces se necesita firma para `97` = censurada real, con el dato de §1.1: cero trámites afectados en 2021/2023), o se reescribe como advertencia registrada que no detiene — pero eso lo decide mesa (`FP-399`), no el ejecutor.
- El contrato de unidad de la celda-D (`FP-393`) sigue abierto; el v1.1 no lo destraba.

---

## 4 · Registro, marcador, contadores

- **Celda-D `GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml`:** no se registra. No hay veredicto que registrar (sin COMMIT-3) y el contrato de unidad (`FP-393`, `NC-0367`) sigue sin firma. Celdas-D siguen en **5**.
- **Marcador:** `CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::edadxescolaridad` sigue `RESERVADA` / `RESERVADA-SIN-R`; no se re-deriva porque nada lo mueve. El par **no** queda consumido.
- **Contadores:** `N_corridas_selladas` +0; `cuenta_gen2` NO-APLICA; `adoptados_activos` sin cambio. `NC-0355` → `CERRADA` (`CAMBIO-MENOR`). Nuevas: `NC-0404`–`NC-0407`, `FP-399`, `FP-400`.

## 5 · Auditoría (afirma sobre México — aplica completo)

Nada de lo que este acto produjo es una cifra sobre conducta. Lo único que afirma es sobre el **instrumento**: la pregunta 7.3 y el universo «pago de luz» de ENCIG son comparables entre 2021, 2023 y 2025 por texto. Eso habilita medir; no dice qué se va a encontrar. El `+11 pp` de ENCIG sigue sin poder citarse como cambio en México: con instrumento comparable, todavía puede ser cambio de canal (más CFE en app, más bancos con pago en línea) y no actitud hacia el Estado. `edad × escolaridad` en gobierno digital es brecha de acceso, conectividad y alfabetización digital por cohorte antes que disposición; el universo excluye a quien no hizo trámites —más rural, más informal— y, por S2, formalmente también a quien tiene 97 o más años, aunque en 2021 y 2023 esa exclusión no alcanzó a nadie. Cuando el piloto corra: si nadie vence con IC ancho, el veredicto honesto es falsador débil, no tercera corroboración.
