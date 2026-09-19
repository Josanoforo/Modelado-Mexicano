# GEN2-FAM-UNION-ESTIMANDO-1 · cierre

Encargo archivado verbatim (A.3) en
`forense/encargos/2026-09-19-GEN2-FAM-UNION-ESTIMANDO-1.md`.
Base: `origin/main = 8e455bd6a387`, el SHA que el encargo declara — sin
deriva, re-verificado con `git rev-list --count HEAD..origin/main = 0`.
Entorno NUBE (`cloud_default`), `data/raw` ausente, `corpus montado=NO`
(`archivos_examinados=0`), `numpy`/`pandas`/`scipy`/`pyreadstat` AUSENTES.
**Cero microdato abierto · cero medición · cero red · ningún `spec.yaml`
sellado tocado (E.3).**

## Compuerta (cumplida, por PRODUCTO)

`COMPUERTA: CALC-ENADID-0001 (#869) y CALC-EDER-0003 en main`.
Verificado por el producto, no por `grep` de asunto (`ADR-277`):

```
$ git ls-tree -r --name-only origin/main | grep -E "ENADID-0001|EDER-0003"
data/corrida0/CALC-EDER-0003/{ejecucion,resultados,sello}.json + medidor.py + spec.{md,yaml} + sello.sha256
data/corrida0/CALC-ENADID-0001/{ejecucion,resultados,sello}.json + medidor.py + spec.{md,yaml} + sello.sha256
```

A.8 sobre la regla (`ADR-340`, exigido por `T-YAMEDIDO`):

```
$ python3 tools/ya_medido.py familia.union.libre
  milpa/tramite.yaml:1031  situacion=primera_union tier=FUERTE
      veredicto=CORROBORADA p=0.190500  [CORROBORADA]      (antes)
  milpa/tramite.yaml:1031  situacion=primera_union tier=FUERTE
      veredicto=CORROBORADA p=0.480971  [TASA-EJECUTADA]   (después)
```

## P1 · Los dos estimandos, por texto de pregunta (A.15)

Los tres hechos del encargo se leyeron contra el árbol y **ninguno se
contradice**: no hay PARO. Una precisión menor y una confirmación:

* El encargo cita `milpa/tramite.yaml:1034-1037`; las dos conductas estaban
  en `1035-1036` dentro de la entrada que abre en `1031`. Es la misma
  entrada y las mismas dos cifras.
* El encargo dice `CALC-EDER-0003` con `cuenta_gen2 = SI`. Su `spec.yaml`
  congelado dice `PENDIENTE-DE-MESA`; el registro vigente dice `SI`
  (`data/corrida0/corridas.tsv:114`, por `data/corrida0/decisiones.tsv:75`,
  firma de mesa del 15/sep/2026). **El encargo tiene razón**: la firma
  posterior sucedió a la etiqueta congelada, que no se reescribe (E.3).

| | **EDER 2017** — el que la regla CARGA | **ENADID 2023** — el descriptivo aparte |
|---|---|---|
| reactivo | `edo_civil1` en `historiavida.csv`; etiqueta verbatim del FD `eder2017_fd.pdf`: «**Estado civil primera unión**», catálogo de 27 códigos verificado línea por línea contra el PDF por `ACTO MAESTRA35-L7` | `P3_27` en `TSDEM`; el cuestionario de hogar lo rotula «**SITUACIÓN CONYUGAL**» y pregunta «**¿Actualmente (NOMBRE)…** vive con su pareja en unión libre? / está separada(o) de una unión libre? / está separada(o) de un matrimonio? / está divorciada(o)? / esta viuda(o)? / está casada(o)? / está soltera(o)?». (`P3_27_AG` está documentada aparte como **agrupación** y no gobierna la operación.) |
| **evento** | **TIPO DE LA PRIMERA UNIÓN** — cómo se ENTRÓ a la primera unión, retrospectivo | **ESTADO EN QUE SE ESTÁ HOY** — situación conyugal al momento de la entrevista |
| unidad | persona (EDER declara persona de 20 a 54 años del hogar, FD §1.1.2) | persona residente, una fila por `LLAVE_PER` en `TSDEM` |
| **universo** | personas **alguna vez unidas**: primer `edo_civil1` no-cero por orden de `anio_retro`, con `factor_per` > 0 | personas de **15+** con edad conocida y `P3_27 ∈ {1..7}` (el reactivo se aplica desde los 12 años cumplidos) |
| **denominador** | **n = 18 689** de 23 831 personas (`RESULT-EDER-UNION-A-N-U`) | **n = 276 849** (bruto) · **n = 152 834** (condicional a unión actual, `P3_27 ∈ {1,6}`) |
| periodo | historia retrospectiva de vida; **una sola ola** (2017) | corte transversal 2023 |
| ponderador | `factor_per` (`antecedentes.csv`) | `FAC_VIV` (TSDEM no trae `FAC_PER`) |
| punto | `P-LIBRE = 0.480971` · `P-DIRECTO = 0.518946` | unión libre bruta `0.190541` · actualmente casada bruta `0.359446` · unión libre entre unión actual `0.346446` |

**Por qué no se restan ni se promedian:** proporciones sobre universos
distintos (alguna vez unidos vs. población 15+), sobre eventos distintos
(entrada a la unión vs. estado actual) y sobre periodos distintos. El
propio sello lo dice: `RESULT-EDER-UNION-A-DELTA-VS-GEN1 =
NO-APLICA-ESTIMANDO-DISTINTO`, **declarado y no calculado**.

**Y por qué 0.8095 no era matrimonio:** es `1 − 0.190541`. La distribución
nacional 15+ de `CALC-ENADID-0001` la desarma: unión libre 19.05% ·
separada de unión libre 4.15% · separada de matrimonio 2.92% · divorciada
2.19% · viuda 6.16% · **casada 35.94%** · soltera 29.58%. El complemento
llamado `matrimonio_directo` cargaba, dentro de sí, a 29.58 puntos de
solteras.

## P2 · La regla (`milpa/tramite.yaml`, entrada `familia.union.libre`)

Una sola entrada editada. Nada más de `milpa/` se tocó.

| campo | antes | después |
|---|---|---|
| `union_libre` `p` | 0.190500 | **0.480971** (`RESULT-EDER-UNION-A-P-LIBRE`, GEN2) |
| `matrimonio_directo` `p` | 0.809500 | **0.518946** (`RESULT-EDER-UNION-A-P-DIRECTO`, GEN2) |
| `clase` (ambas) | «prevalencia bruta ponderada 15+, tasa base; ENADID 2023, p3_27_ag» | «proporción ponderada del TIPO DE PRIMERA UNIÓN; EDER 2017, `historiavida.csv/edo_civil1`…; universo: personas alguna vez unidas, n = 18 689; ponderador `factor_per`» |
| `ic95` | `NO-APLICA` | **[0.469175, 0.492482]** (IC de diseño de `union_libre`) |
| `n` | 152950 (el n de ENADID) | **18689** |
| `ponderador` | «factor_per (EDER) / peso ENADID» | `factor_per` solo |
| `situacion` | `primera_union` | `primera_union` (**no cambia**: ahora el nombre y la cifra coinciden) |

Notas de ejecución:

* **La partición no cierra en 1 y eso es correcto**: `0.480971 + 0.518946 =
  0.999917`. El código `37` (n = 2) queda sin clasificar y contado
  (`RESULT-EDER-UNION-A-N-SIN-CLASIFICAR`); la corrida declara
  `SUMA-PARTICION = SI` con ese residuo. No se re-escala.
* `matrimonio_directo` **conserva su nombre** y ahora es el nombre correcto:
  bajo EDER, `DIRECTO = {2,3,4,26,27,28,46,47,48}` es matrimonio
  civil/religioso/ambos como primera unión, **contado sobre su propio
  numerador, nunca como `1 − p`**. El slot `RES-0044` no se renombra.
* **Gradiente por cohorte:** el bloque legacy `eje_cohorte_eder2017` se
  **conserva** (encargo P2). Al lado se declara
  `eje_cohorte_eder2017_gen2_sellado`, con `RESULT-EDER-UNION-B-COHORTE-P-LIBRE`
  por id: puntos iguales en 3 de 4 celdas al 6º decimal (1981-1990 difiere
  en −1.58e-04, y su n en +2), IC de diseño ligeramente distintos. No se
  sustituye ninguno: se ponen los dos a la vista.
* `eje_edad_enadid2023` se **conserva** y se **re-rotula**
  (`estimando: situacion_conyugal_actual_condicional_a_union`): no es un eje
  del estimando que la regla carga.
* **Bloque descriptivo aparte**, `descriptivo_situacion_conyugal_actual_enadid2023`,
  con nombre propio por firma de mesa: `union_libre_actual` (0.190541,
  `RESULT-ENADID-UA-G-P-BRUTA`), `actualmente_casada` (0.359446),
  `union_libre_entre_union_actual` (0.346446,
  `RESULT-ENADID-UA-G-P-CONDICIONAL`) y
  `actualmente_casada_entre_union_actual` (0.653554,
  `RESULT-ENADID-UA-G-P-CASADA-CONDICIONAL`). **No es una conducta, no entra
  a `entonces`, no carga ninguna `p` del motor.**
  `actualmente_casada` es el único punto sin `RESULT` escalar propio: sale de
  la fila `distribucion_actual_15_mas,casada,15_mas` de
  `forense/analisis/enadid-union-actual-cli-1/resultados.csv`, **cuyo sha256
  `4c2abc76…1efc2` está sellado** en `RESULT-ENADID-UA-G-TABLA-SHA256`
  (recomputado en esta sesión: coincide). Nada sin `RESULT` entró a la regla.

### A.17 · La decisión previa, localizada y citada (no heredada)

La spec congelada de `CALC-EDER-0003` (`spec.yaml`, `reglas_bajo_prueba`)
dice: «NINGUNA cambia de cifra por esta corrida. `familia.union.libre`
(R5.3) conserva su p, su veredicto CORROBORADA y su segmentacion por
cohorte sellada.» **Quién lo decidió:**

* **`ADR-510`** — `ACTO GEN2-SPECS-DEMANDA-1 · SEIS SPECS CONGELADAS EN
  NUBE…`, 15/sep/2026 (`canon/gobernanza-v1_15.md:624`). Su firma
  autorizaba **CONGELAR, no contar** ni adoptar; por eso la spec se escribió
  declarando que no movía ninguna cifra.
* **`NC-0254`** — abierta por `ACTO GEN2-PINS-REPRODUCE-1`
  (`forense/no-corrido.tsv:249`), razón `DECISION-DE-MESA-PENDIENTE`:
  «`milpa/tramite.yaml` ya cita EDER2017 como eje de CORROBORACION … y no
  como reemplazo del p primario». Cerrada en `PR #872` con sucesor
  «corrida ENADID 2023».

**Esta firma la sucede, no la ignora.** La reserva era correcta mientras
faltara la re-medición de la fuente GEN1: sin ella no se podía saber si
0.1905/0.8095 eran un error de cálculo o un error de nombre.
`CALC-ENADID-0001` (`PR #869`, `REPRODUCE/IDENTICO`) contestó — reprodujo
0.1905406 sobre la misma fuente — y dejó el diagnóstico en pie: no hay error
de cálculo, hay un nombre sobre otra cantidad. El sucesor que `NC-0254`
declaró («corrida ENADID 2023») existe; lo que faltaba era el relevo, y es
lo que este acto hace bajo la firma del 19/sep/2026.

### Tier · re-evaluado por separado, declarado en la entrada, a mesa como FP-387

El esquema admite **un escalar** en `tier` (`milpa/src/emisor.py:154`,
`r.get("tier", "")`), así que el tier partido se declara en el campo
`tier_partido` de la propia entrada (precedente: `reserva_tier` de
`dinero.digital.adopcion`, `milpa/tramite.yaml:290`, firma D2) y va a mesa
como **`FP-387`**:

* **cifra → FUERTE.** Medida y sellada bajo GEN2, `cuenta_gen2=SI`, IC de
  diseño, partición que cierra, gradiente por cohorte con IC por celda. Dos
  olas de fuente distinta describen el campo y no se promedian.
* **mecanismo → HIPÓTESIS.** El `porque` afirma que la baja garantía
  institucional del matrimonio hace de la unión libre una opción racional.
  `baja_garantia_institucional` está marcado `NO-MEDIDO` en la propia
  entrada: **ningún instrumento del corpus mide garantía institucional
  percibida**. Lo medido es la tasa base del desenlace y su gradiente, no la
  condicional al disparador — y un gradiente por cohorte es compatible con
  varios mecanismos (costo de formalización, secularización, composición).
* **escalar publicado → FUERTE**, el de la cifra, porque es lo que el motor
  consume. Mientras mesa no resuelva `FP-387`, quien use `tier` como
  respaldo del MECANISMO lo está sobreleyendo, y la entrada lo dice.

## P3 · Relevo (por comando, con `status` antes/después)

```
$ python3 tools/relevo_usos.py            # ANTES        DESPUÉS
  LISTADO-PARA-MESA                            9      →      7
  YA-ADOPTADO                                 22      →     24
  control_c0[COINCIDE]                        15      →     15
  control_c0[DISCREPA]                         0      →      0
  control_c0[NO-DERIVABLE-DESDE-LA-SPEC]       7      →      9
  slots                                      208             208

$ python3 tools/corrida0.py status        # ANTES        DESPUÉS
  dependencias_numericas_legacy_activas      184      →    182
  N_resultados_gen2_adoptados_activos         36      →     38
  diferencias_materiales                       0      →      0
  (el resto, sin cambio: corridas 85/83, resultados 208/5012/208, …)
```

`RES-0043` y `RES-0044` pasan de `LEGACY-GEN1 · LISTADO-PARA-MESA` a
`GEN2 · YA-ADOPTADO`, con `RESULT-EDER-UNION-A-P-LIBRE` y
`RESULT-EDER-UNION-A-P-DIRECTO` por canal **`C0-CONSUMIDOR`** (el propio
`milpa/` declara `corrida0_resultado_id` + `corrida0_generacion: GEN2`).
**No hubo renombre de conducta**, así que la pieza P3 no PARA: el comando
cubre el caso.

`control_c0` pasa a `NO-DERIVABLE-DESDE-LA-SPEC` en esas dos filas: es
lectura correcta y esperada — la `spec.yaml` sellada de `CALC-EDER-0003`
declara explícitamente que **no** fija qué RESULT releva qué slot
(«Este acto NO escribe cita en `milpa/` y NO sustituye la celda ENADID»).
El pin lo pone el consumidor por firma de mesa, no la spec. No es
`DISCREPA`, que sigue en 0.

### Hallazgo colateral, reproducido en árbol limpio: `NC-0343`

`tools/relevo_usos.py --escribe` reescribe, además de esas dos filas,
**37 filas cuyo `RES-####` estaba desincronizado** de la autoridad
(`data/corrida0/demanda-resultados.tsv`) desde antes de este acto:

```
discrepancias del relevo COMMITEADO vs demanda-resultados.tsv: 37
discrepancias del relevo REGENERADO vs demanda-resultados.tsv:  0
```

Reproducido con `git stash` (árbol limpio, **sin** la edición de este acto):
la regeneración produce las mismas 37 correcciones. **No es efecto de este
acto**; el derivado estaba viejo. Se commitea la salida completa del escritor
canónico porque el archivo es `# DERIVADO — NO EDITAR` y editarlo a mano para
ocultar la corrección sería el defecto peor. Queda `NC-0343` para que mesa
sepa que el derivado llevaba 37 filas corridas y por qué nadie lo vio.

## P4 · El test (`tests/test_union_estimando.py`, nuevo)

Falla si una conducta `matrimonio_directo` declara una `clase` que cite
`p3_27`/`p3_27_ag` o «situación conyugal» (con y sin acento), en `entonces`
o en `transiciones`. **El defecto ocurrido; ninguno más.**

Control negativo y positivo, corridos:

```
$ git stash -- milpa/tramite.yaml && python3 tests/test_union_estimando.py
FAIL test_matrimonio_directo_no_cita_situacion_conyugal_actual
  familia.union.libre · entonces · clase=MEDIDO·p(prevalencia bruta
  ponderada 15+, tasa base; ENADID 2023, p3_27_ag)
exit=1
$ git stash pop && python3 tests/test_union_estimando.py
OK   test_el_detector_reconoce_el_defecto_historico
OK   test_matrimonio_directo_no_cita_situacion_conyugal_actual
# conductas `matrimonio_directo` examinadas: 1
```

A.13: el test aserta primero que **examinó al menos una** conducta
`matrimonio_directo`; un verde sobre cero conductas no es un verde.

## Sucesor · barrido de una pasada

¿Qué otras conductas de `tramite.yaml` son «complemento aritmético con
nombre sustantivo»? Barrido sobre las reglas con exactamente dos conductas
con `p` que suman 1.0:

| archivo:línea | regla | conductas | ¿defecto del mismo tipo? |
|---|---|---|---|
| `milpa/tramite.yaml:245` | `tramite.gobierno_digital.coercitivo` | `rechaza_servicio` 0.91 / `adopta` 0.09 | **CANDIDATA**. `p` `ASIGNADO`, no medido; ya trae `reserva_tier` y `campo_administrativo` (firma D2, `FP-273`): «credencial acumulada != uso vigente; cota superior del stock, no adopcion medida». El nombre `adopta` sobre una cota superior es el mismo patrón. |
| `milpa/tramite.yaml:627` | `civico.denuncia.miedo_desconfianza` | `denuncia_con_miedo_o_desconfianza` 0.294313 / `denuncia_por_otra_razon` 0.705687 | **DECLARADA, no oculta**: la segunda trae `complemento_de`. `ADR-509` ya propuso el nombre descriptivo `denuncia_sin_miedo_ni_desconfianza` para no colisionar con el código literal «09 Otra». Revisar el nombre, no la cifra. |
| `milpa/tramite.yaml:1292` | `dinero.ahorro.horizonte_corto` | `horizonte_corto` / `horizonte_no_corto` | no — el complemento se llama `_no_`. |
| `milpa/tramite.yaml:1344` | `dinero.ahorro.horizonte_no_corto_con_seguridad_social` | idem | no. |
| `milpa/tramite.yaml:1570` | `salud.vacunacion.disponible_ensanut2024` | `razon_no_vacunacion_logistica` / `..._no_logistica` | no. |
| `milpa/tramite.yaml:1601` | `dinero.ahorro.horizonte_no_trabajadores` | idem | no. |

**No se tocó ninguna** (el encargo lo prohíbe): se listan. De aquí sale, si
hay demanda, el siguiente acto.

## Módulo de auditoría (afirma sobre México: completo)

* **¿Estructura confundida con cultura?** La entrada dice, en
  `enmienda_estimando_2026_09_19.lectura_peligrosa_declarada`, que «48% entra
  por unión libre» no es juicio sobre estabilidad familiar, ni «preferencia
  cultural», ni «unión fallida». El gradiente por cohorte va de **30.5% en
  ≤1970 a 77.3% en 1991+**: leer el punto nacional sin el gradiente es leer
  mal. Y el mecanismo del `porque` («opción racional ante baja garantía
  institucional») **es hipótesis, no hallazgo** — está en `tier_partido` y en
  `FP-387`.
* **¿Sobregeneralización?** EDER 2017 cubre **personas alguna vez unidas**: no
  habla de quienes nunca se unieron ni de uniones posteriores a la primera.
  Escrito en el `universo` de la regla. **Ninguna de las dos fuentes segmenta
  aquí por condición indígena**, donde la unión consuetudinaria es otro orden
  institucional: **fuera por diseño, y se dice** — también en el `universo`.
* **Clase de evidencia:** (a) en ambas fuentes — microdato de encuesta
  probabilística nacional con diseño acreditado, re-medido y sellado bajo
  GEN2 con replay independiente.
* **Escalas:** proporción sobre universos distintos (alguna vez unidos
  n=18 689 vs. población 15+ n=276 849). **Por eso no se restan ni se
  promedian**, y por eso los dos bloques viven separados en la entrada.
* **Falsabilidad:** en `falsable_si`, partida. CIFRA: una EDER posterior que
  mueva `P-LIBRE` fuera de [0.469175, 0.492482] o que rompa el gradiente por
  cohorte fuera de los IC por celda. MECANISMO: un instrumento que mida
  garantía institucional percibida y NO correlacione.
* **Peligroso leído simplista:** declarado en la propia entrada, no sólo aquí.

## Lo que este acto NO hizo

No midió · no re-ejecutó ENADID ni EDER · no abrió microdato · no tocó
ningún `CALC` ni ningún `spec.yaml`/`sello` (E.3) · no tocó
`tramite-ola5-propuesta-v0.yaml`, el marcador, `tools/corrida0.py` ni
ninguna otra regla · no tocó `milpa/procedencia.yaml` (la entrada no lo
exigió) · no fusionó ningún PR · **`cuenta_gen2` NO-APLICA**: este acto no
sella corrida.
