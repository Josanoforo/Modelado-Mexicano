# ACTO COEF-UNIVERSO — los 15 coeficientes contra el universo conocido completo

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-19-coef-universo-cierre.md` |
> | **QUÉ ES** | Nota de cierre del ACTO COEF-UNIVERSO. Ejecuta el encargo archivado en `forense/encargos/2026-08-19-COEF-UNIVERSO-quince-coeficientes.md`. |
> | **VERIFICAS ASÍ** | Cada cifra de esta nota trae el comando que la produce, corrido contra el clon `/home/pc0/mm-coef-universo` en la base declarada en §0. Ninguna cifra viene del espejo del proyecto. |
> | **ENTORNO** | UBUNTU, caja con corpus. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin variable; INEGI responde `200`; `data/raw` enlazada al corpus compartido. |

---

## 0 · ARRANQUE — las cinco líneas

| # | | valor crudo |
|---|---|---|
| 1 · REPO | clon existente | `/home/pc0/Modelado-Mexicano` (main). Worktree nuevo de este acto: `/home/pc0/mm-coef-universo`, rama `coef-universo`. No se clonó nada nuevo. `git log -1` → `35c9c9f Merge pull request #278 from Josanoforo/limpia-caja`; `git status` limpio (0 líneas). |
| 2 · SHA | base real ≠ declarada | Declarada `e6864ed` (#267). Real **`35c9c9f`**. Main se movió cinco merges entre redacción y ejecución: #274, #275, #276, #277 (ADQ-15, cerrado), #278 (LIMPIA-CAJA). No es PARO por instrucción del propio encargo; el perímetro se re-derivó contra `35c9c9f`. |
| 3 · data/raw | **la enlacé** | No existía en el worktree nuevo. `ln -s /home/pc0/mm-corpus/raw data/raw`. Corpus montado: 284 entradas en raíz. |
| 4 · ENTORNO | tres partes (A.2) | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = **sin variable** · `curl -s -o /dev/null -w "%{http_code}" https://www.inegi.org.mx/` → **200** · `ls data/raw/ \| head -1` → **`20260813130000.export.CSV.zip`**. |
| 5 · ESPEJO | acatado | Toda cifra sale del clon de (1), con comando a la vista. |

**Nota de terreno.** `git worktree add` emitió dos veces `could not write config file .git/config: Device or resource busy` — contención conocida de esta caja. El worktree quedó correcto; se verificó por `git worktree list` y `git rev-parse`, no por el texto del comando.

**Segunda deriva de main, a mitad de acto.** Mientras este acto corría, `origin/main` avanzó otros cinco PR — #279 (`FP57-DECLARA`), #280 (`FUSION-PUERTAS`), #281 (`CORTE-EDAD-CONVENCION`), #282 (`FP10-PRECEDENCIA`), #283 (`REFUTACIONES-SIN-OBJETO`) — hasta `20c7dee`. Se fusionó **local**, main hacia la rama, nunca por el botón de GitHub (`forense/hallazgos.md` lleva `merge=union`, que el lado servidor no honra). El merge fue limpio. Efecto sobre la numeración, que es la razón por la que el encargo manda derivarla dos veces: **el máximo de ADR pasó de 113 a 117** y **el máximo de firma pendiente pasó de `FP-60` a `FP-61`** entre el arranque y el cierre de este acto — y `#281` ya había tenido que renumerar su propio `ADR-115` a `ADR-116` por la misma colisión. Todas las cifras de esta nota se re-derivaron contra el árbol fusionado y se sostienen sin cambio.

**Línea base al arrancar:** `python3 tests/check.py --baseline` → `21 FAIL · 118 WARN`, **LÍNEA BASE: VERDE** (1 entrada de la línea base ya no aparece: mejora, no baja la cifra congelada sin `--freeze`, que este acto tiene prohibido).

---

## 1 · PASO 0 — `data/INFRAESTRUCTURA-v1_0.md`: no dispara PARO, y el motivo importa

El encargo instruye parar si el índice no cubre **demanda / cableado / coeficientes**. La búsqueda literal de esas tres palabras da:

```
$ grep -c "cablead"     data/INFRAESTRUCTURA-v1_0.md   → 6
$ grep -c "coeficiente" data/INFRAESTRUCTURA-v1_0.md   → 1   (y es de celda-D, no de generador)
$ grep -c "demanda"     data/INFRAESTRUCTURA-v1_0.md   → 0
```

Con esa lectura correspondía PARAR. **No se para, y no por indulgencia: la vía existe bajo otro nombre.**

**`demanda` es el nombre histórico; `necesidad` es el nombre vigente del mismo concepto.** El linaje está documentado en el repo, no inferido: `forense/rescate/curador-untracked-20260807/multi1-staging/integrado/registro-demanda-universo-curado.tsv` es el prototipo, y `forense/notas/2026-08-18-rescate-curador-cierre.md` lo dice verbatim — *"Confirma linaje real: el prototipo `Demanda-Universo` de `curador` evolucionó hacia el esquema que hoy vive trackeado en `main`"*, es decir `data/curacion-registro/relaciones.tsv`, cuyas columnas `capa1..capa4`/`clasificacion_relacion`/`reason_code` son casi idénticas.

Traducido el vocabulario, el índice **sí cubre las tres**: `cableado` en el Dominio 4-bis (fila propia, escritor, contrato de 26 columnas, juez T23); `demanda`/`necesidad` en el Dominio 4 vía `data/curacion-registro/necesidad-objeto-modelo.tsv`; `coeficientes` en esa misma tabla, cuyas filas `N1`–`N15` **son** los 15 coeficientes de generador.

**Dos huecos reales del índice, que se reportan sin parar el acto:**

1. **No hay regla de escritura para dar de alta demanda nueva.** La sección `## Si tu encargo hace X, escribe en Y` tiene once filas; ninguna dice *"voy a registrar una necesidad/demanda nueva"*. Y el propio índice clasifica `necesidad-objeto-modelo.tsv` como `SIN VÍA` de escritura por script, a mano, precedente único `59d6c40`.
2. **El índice no menciona `milpa/` ni una vez** (`grep -ci "milpa" data/INFRAESTRUCTURA-v1_0.md` → `0`). El dominio donde viven los 15 coeficientes —`milpa/procedencia.yaml`, editada a mano en 27 commits, con test dedicado `tests/test_motor_procedencia.py`— queda fuera de la jurisdicción del único índice de infraestructura del programa.

**Defecto adicional del índice, encontrado al derivarlo.** El índice afirma que `necesidad-objeto-modelo.tsv` la lee *"solo `test_barrido_completo.py`"* y que tiene *"0 lectores fuera del test"*. Es falso: tiene **cinco** lectores, dos de ellos de producción — `tools/censo_estimabilidad.py` y `tools/curador_registro/tareas_barrido2.py` —, más `integrate_barrido2.py`, que la recibe por el flag **obligatorio** `--mapping` de la rama `--barrido2` del CLI real.

---

## 2 · FUNCIÓN A — los 15 coeficientes, y la ruta que el encargo citó está equivocada

El encargo manda derivar la lista de `milpa/procedencia.yaml:829` (`coeficientes_generador_medidos:`, slots `G*`). **Esa clave existe y no contiene los 15: contiene 6.**

```
$ python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); print(len(d['coeficientes_generador_medidos']))"
6
```

Las 6 son entradas de auditoría de medición (5 con un β̂ marginal, 1 con un gate de identificación fallido), no el censo de coeficientes. **El roster de los 15 vive en otra clave: `asignados_coeficiente.detalle`, `milpa/procedencia.yaml:787-806`**, con su espejo de rutas en `rutas_estimabilidad_coeficiente.detalle`, `milpa/procedencia.yaml:1053-1078`. Las tres listas cuadran en 15; la que el encargo señaló, no.

Lista canónica, cruzando `data/curacion-registro/necesidad-objeto-modelo.tsv` (filas `N1`–`N15`), `asignados_coeficiente.detalle` (valor) y `forense/censo-estimabilidad-coeficientes-v1_2.md` §1 (ruta vigente, sellada por `ADR-89`):

| # | necesidad | Gen.coeficiente | valor ASIGNADO | ruta v1.2 |
|---|---|---|---|---|
| 1 | `N1` | `G1.confianza_institucional` | −0.60 | RUTA-A |
| 2 | `N2` | `G1.radio_confianza` | −0.35 | RUTA-A |
| 3 | `N3` | `G2.sens_estatus` | 0.55 | SIN-RUTA |
| 4 | `N4` | `G2.aversion_riesgo` | 0.20 | SIN-RUTA |
| 5 | `N5` | `G3.horizonte_temporal` | −0.60 | RUTA-I |
| 6 | `N6` | `G3.aversion_riesgo` | 0.40 | SIN-RUTA |
| 7 | `N7` | `G3.familismo_apoyo` | 0.20 | RUTA-A |
| 8 | `N8` | `G4.exposicion_violencia` | 0.70 | RUTA-C |
| 9 | `N9` | `G4.confianza_institucional[justicia]` | −0.40 | RUTA-C |
| 10 | `N10` | `G4.horizonte_temporal` | −0.20 | SIN-RUTA |
| 11 | `N11` | `G4.sens_estatus` | −0.15 | SIN-RUTA |
| 12 | `N12` | `G5.familismo_apoyo` | 0.50 | RUTA-C |
| 13 | `N13` | `G5.familismo_obligacion` | *sin magnitud* (ADR-30) | RUTA-C |
| 14 | `N14` | `G5.radio_confianza` | 0.15 | RUTA-C |
| 15 | `N15` | `G6.deferencia` | 0.45 | SIN-RUTA |

**Dos divergencias declaradas, no resueltas por este acto.** (a) `canon/modelo-decision-v4_0.md` §2.2 usa **siete** ids de slot (`G1a`, `G1b`, `G2`…`G6`) contra los seis de `procedencia.yaml`; los dos coeficientes de `G1` cuelgan íntegros de `G1a`, y `G1b` aporta cero (está contradicho por el Hito C). Los valores y nombres coinciden uno a uno en las dos fuentes. (b) `canon/modelo-decision-v4_0.md` afirma *"Los quince coeficientes son `ASIGNADO`. Ninguno es medido"* y no menciona el Encargo W ni `β̂` en ningún punto, mientras `procedencia.yaml` trae literalmente `clase: "MEDIDO·β̂..."` en cinco entradas. La reconciliación ya existe en el repo (`ADR-57(a)` rotula esos β̂ como asociaciones, no coeficientes, por eso el `0 de 15` no se mueve) — pero **`README.md` cita "tres asociaciones marginales" cuando hoy son cinco**: cifra vencida desde el 4/ago, cuando el Encargo E añadió dos entradas.

---

## 3 · FUNCIÓN B — la llave (ii): dónde está, y por qué no tiene renglón

`canon/gobernanza-v1_15.md` (ADR-57(c)) define las tres clases de llave de identificación, verbatim: *"(i) panel con el desenlace en el instrumento (mismos sujetos entre olas); (ii) experimento natural con grupo de comparación sobre encuestas repetidas; (iii) diseño experimental de terceros (evaluaciones aleatorizadas publicadas, clase Progresa/Oportunidades)"*.

**El contador `1 de 2`** vive en `canon/estado-programa-v1_10.md` y se deriva de `forense/registro-llaves-identificacion-v1_0.md` §3, que tiene exactamente dos filas:

| llave_id | diseño | clase declarada | estado |
|---|---|---|---|
| `CAL-G3` | panel ENNViH/MxFLS, tres olas | **llave (i)**, literal | `SELLADA_NO_EJERCIDA` |
| `R5.1-D2` | diferencias-en-diferencias por grupo de elegibilidad (ENIGH 2018→2022) | **ninguna** | `EJERCIDA_INDECISA` |

**Tres derivaciones, ninguna de ellas obtenible con los términos que dirección buscó:**

1. **La única llave que cuenta como ejercida nunca fue adjudicada contra la taxonomía.** El `1` del contador es `R5.1-D2`. Su diseño —DiD por regla de elegibilidad sobre transversales repetidas— encaja en la definición de la clase (ii), pero **nadie ha escrito nunca "R5.1-D2 ejerce la llave (ii)"**, ni en el registro, ni en su pre-registro, ni en ningún ADR.
2. **La llave (ii) tiene candidato nombrado en canon y cero renglón operativo.** `ADR-57(c)` dice de ENOE, verbatim: *"permanece elegible únicamente como portador de desenlaces laborales para experimentos naturales (p. ej. salario mínimo de franja fronteriza)"*. ENOE no es ninguna de las dos filas del registro de llaves, no aparece en el censo de estimabilidad, y no tiene fila en ninguna tabla del programa.
3. **El diagnóstico ya estaba escrito y sin remediar.** `forense/RONDA-M-motor-matriz-veredicto-opus-2026-08-13-v1_0.md`, hallazgos M2 y M11, dice verbatim: *"la llave omitida es la de clase (ii)"*, y muestra que el libro de demanda de tres clases **no puede representarla por construcción**. La remediación sigue sin escribirse: `propuesta-motor-matriz-v0_1.md` sigue en v0_1 y `milpa/catalogo-momentos-v0_1.tsv` tiene cero filas de datos.

**Corrección a una premisa del encargo.** El encargo dice *"NO reabre ID-X/ENNViH: ADR-107 cerró esa ruta"*, en un contexto que sugiere que eso afecta a la llave (ii). No es así: **ADR-107 cierra una aplicación fallida de la llave (i)** —`G3·horizonte_temporal` sobre el panel ENNViH/MxFLS olas 2-3, compuerta inalcanzable con n reales (`IC95%sup` 1.483 primaria y 1.372 sensibilidad, contra un umbral `<1.25`)— y su propia cláusula de reversión dice que *"la ficha sigue siendo el diseño correcto para la llave (i), el panel es lo que no alcanza"*. ADR-107 no menciona ENOE, ni "experimento natural", ni la clase (ii) en ningún punto de su texto. La instrucción de no reabrir ENNViH se acata; la inferencia de que eso cierra la (ii) no se sostiene.

**T24**, el vigía citado por el encargo (`tests/check.py`, introducido por PR #269), cruza el conteo estructurado del registro de llaves contra su cita en prosa en `canon/estado-programa-v1_10.md`. Tiene seis puntos de disparo y **ninguna ruta de WARN**: solo llama `fail()`, de modo que estructuralmente solo puede salir `[FAIL]` o `[ ok ]`. Consecuencia operativa para cualquier acto futuro: **añadir una fila al registro de llaves sin actualizar la cita de `estado-programa` rompe la suite**, y viceversa.

---

## 4 · FUNCIÓN D — el cableado no admite altas, y ése es el entregable

El encargo instruye cablear demanda *"conforme al esquema del cableado"* y añade: *"Si el esquema no admite altas nuevas, ese hueco es entregable — repórtalo, no inventes vía."* **No las admite.**

`tools/curador_registro/build_cableado.py` toma cuatro insumos obligatorios (`--proposals`, `--tasks`, `--decisions`, `--reports`) y **nunca lee el cableado existente**. Su `write_tsv()` construye el archivo entero desde cero y hace `path.write_text(...)`: sobreescritura total, sin modo `append`, sin merge. Su propio docstring lo declara: *"El cableado es una PROYECCIÓN de decisiones y conocimiento, no una credencial de escritura: nada de lo que se escribe aquí puede mutar el registro."*

Y **T23 lo cierra por join**, no por formato. Tres de sus diecinueve condiciones bastan para que una fila escrita a mano falle:

- **condición 14** — una fila `INTEGRADA` exige una decisión verificable en `decisiones-integracion-barrido2.tsv` para ese `propuesta_id`, con el mismo `estado_integracion`;
- **condición 15** — el `propuesta_id` exige fila real en `propuestas-barrido2.tsv`, y esa propuesta exige join a una `tarea_id` real;
- **condición 16** — un `payload_id` que no esté en el conjunto conocido se reporta literalmente como *"inventado"*.

La única vía legítima de alta es correr el pipeline completo: `tareas_barrido2 → propuestas → integrate --barrido2 → build_cableado`, que exige elecciones de curador **y** veredictos de supervisor — dos papeles que un mismo acto no puede desempeñar. **Este acto no inventa vía. La demanda derivada aquí se entrega en `data/coef-universo-v1_0.tsv`, que es tabla nueva autorizada por el perímetro, y queda sin cablear por diseño del registro, no por omisión del ejecutor.**

**Defecto encontrado al abrir el cableado para consumirlo (Función E).** En las 37 filas, `reactivo_id` es **idéntico** a `objeto_logico_id`, y ninguno de los 37 nombra una variable:

```
$ awk -F'\t' 'NR>1{if($8==$6) i++; else d++} END{print i+0, d+0}' data/cableado-universo-v1_0.tsv
37 0
$ awk -F'\t' 'NR>1 && $8 !~ /^OBJ-B2-/' data/cableado-universo-v1_0.tsv   # vacío
```

El `texto_reactivo_recortado` no es texto de reactivo: es un descriptor de material (`COLUMNA` ×13, `[REDACTADO-PRIVACIDAD]` ×6, `VARIABLE-DICCIONARIO-XLSX` ×4, `SECCION-TEXTO` ×4, `VARIABLE-SAV` ×3, `SECCION-PDF` ×3, `FORMATO-NO-SOPORTADO` ×2, `REACTIVO-PDF` ×1, `ELEMENTO-XML` ×1). **El cableado no llega a nivel de variable pese a que su columna se llama `reactivo_id`.** Consecuencia directa sobre la Función E: las 7 `EXISTE-SATISFACE` no se pueden "abrir y medir" tal como el encargo supone, porque no traen una variable que medir — traen un objeto con N objetos dentro. Para medir hay que bajar a la variable, que es trabajo aparte.

---

## 5 · `SIN-DEMANDA` no significa "sin explotar" — lo que ya estaba sellado y lo que añade este acto

La firma de mesa que abre este encargo dice: *"No puedo creer que de toda la data en el universo conocido [...] no haya nada para poder mover indicadores."* La cifra que sostiene esa lectura es **538 SIN-DEMANDA de 627 (85.8%)**, y reproduce exacta:

```
$ awk -F'\t' 'NR>1{t++; if($8=="SIN-DEMANDA") s++} END{printf "%d/%d = %.1f%%\n", s,t,100*s/t}' data/censo-explotacion-2026-08-17.tsv
538/627 = 85.8%
```

**Lo primero que hay que decir es que la corrección de esa lectura ya estaba sellada, y no es de este acto.** `ADR-83` (14/ago/2026, ACTO S4-AMANUENSE-MESA) cerró la Entrada 6 de `forense/registro-recalculo-v1_0.md` midiendo que **22 de los 538 payloads `SIN-DEMANDA` sí tienen consumo trazable** (2 `CONSUMIDO-POR-PRODUCCIÓN` por hash, 20 `CONSUMIDO-POR-CORRIDA` por ruta citada en once scripts de `tests/`), y selló una **regla anti-poda vinculante**: ningún acto puede podar un payload `SIN-DEMANDA` sin comprobar antes su columna `consumo_detectado`. Cita de origen, verbatim: *"`SIN-DEMANDA` se lee como 'nadie necesita esto'; para los payloads que alimentaron veredictos sellados significa 'la tabla no sabe que la estimación lo usó'."* Este acto **no reclama ese hallazgo**.

### 5.1 · La salvaguarda que ADR-83 selló está redactada en el censo vigente

`ADR-83` §(b) nombra `data/censo-explotacion-2026-08-13.tsv`. El censo **vigente** es el del 17/ago — es el que dirección usó para derivar las cifras de este mismo encargo. En él, la columna que la regla manda comprobar no dice nada:

```
$ awk -F'\t' 'NR>1{c[$10]++} END{for(k in c) print c[k], k}' data/censo-explotacion-2026-08-17.tsv
550 [REDACTADO-PRIVACIDAD]
 77 NO-DETERMINADO-W0

$ awk -F'\t' 'NR>1{c[$10]++} END{for(k in c) print c[k], k}' data/censo-explotacion-2026-08-13.tsv
528 SIN-CONSUMO-DETECTADO
 20 CONSUMIDO-POR-CORRIDA
  2 CONSUMIDO-POR-PRODUCCIÓN
```

**Quien aplique la regla anti-poda contra el censo vigente no puede cumplirla**: las 550 filas heredadas traen el centinela de redacción y las 77 nuevas traen `NO-DETERMINADO-W0`. El censo del 13/ago conserva los valores reales, pero no es el vigente.

**El censo del 17/ago nació así.** Sus cuatro commits (`62e67ed`, `ec5a787`, `4abfccd`, `ffc05de`) traen ya `550 [REDACTADO-PRIVACIDAD]` desde el primero. **La causa queda `NO-DETERMINADO` y este acto no la adivina**: el escritor `tools/curador_registro/write_barrido2_w0.py` fusiona `{**_predecessor_defaults(...), **previous, ...}`, de modo que un valor real en el predecesor habría sobrevivido — la redacción entró aguas arriba de ese merge, y determinar dónde exige abrir el pipeline de W0, que está fuera del perímetro de este acto. Se reporta el hecho, no la causa. **Ninguno de los tres valores reales (`SIN-CONSUMO-DETECTADO`, `CONSUMIDO-POR-CORRIDA`, `CONSUMIDO-POR-PRODUCCIÓN`) contiene dato personal**, lo que hace que la redacción sea, al menos, desproporcionada respecto de lo que protege.

### 5.2 · Lo que este acto sí añade: dos criterios nuevos, y su unión con el de ADR-83

**Criterio A — `usado_para` cita una nota forense concreta.** Falsable: la ruta existe o no existe.

```
44 payloads SIN-DEMANDA cuyo usado_para cita una ruta forense/notas/*.md
18 notas distintas citadas — las 18 existen en el repo (18/18)
```

| nota citada | payloads |
|---|---|
| `2026-08-05-m3-lote-b3-diez-reactivos.md` | 13 |
| `2026-08-03-cbis-deferencia-externas.md` | 9 |
| `2026-08-04-enut-paso1-familismo-obligacion.md` | 6 |
| `2026-08-05-m2-incognitas.md` | 5 |
| `2026-08-03-descarga-masiva-xml-mecanismo.md` | 4 |
| `2026-08-04-barrido-alcanzabilidad-27fuentes.md` | 3 |
| `2026-07-31-cola-descarga-rederivada.md` · `2026-08-04-enasem-paso1-descriptor.md` | 2 c/u |
| las otras diez notas | 1 c/u |

**Criterio B — pertenecer a uno de los cinco instrumentos que produjeron los β̂ del programa.** Las seis entradas de `coeficientes_generador_medidos` salen íntegramente de ENCUCI 2020, ENCIG 2023, ENIF 2024, ENVIPE 2025 y ENNViH/MxFLS. En el censo vigente esos cinco instrumentos suman **164 payloads, y los 164 están `SIN-DEMANDA`** — ni uno solo en otro estado:

```
$ awk -F'\t' 'NR>1 && $1 ~ /^(encig|enif|encuci|envipe|ennvih)/ {c[$8]++} END{for(k in c) print c[k], k}' \
    data/censo-explotacion-2026-08-17.tsv
164 SIN-DEMANDA
```

El `usado_para` de `ennvih2_2005_hogar_cb` dice literalmente *"CAL-G3 — estimación propia de la elasticidad formalidad→composición del ahorro del hogar en el panel ENNViH/MxFLS"* — la única llave (i) del programa, adjudicada por `ADR-107` el 19/ago — y aun así lee `SIN-DEMANDA`.

**Los tres criterios son en gran medida independientes**, lo que importa porque significa que ninguno agota el problema:

| | payloads | traslape con ADR-83 |
|---|---|---|
| ADR-83 · consumo trazable (censo 13/ago) | 22 | — |
| A · `usado_para` cita nota forense | 44 | 4 |
| B · los cinco instrumentos de los β̂ | 164 | 14 |
| **unión de los tres, sobre los 538 SIN-DEMANDA** | **212** | |

**212 de 538 es el 39.4%.** Es decir: de la cifra que la mesa leyó como "no hay nada", casi dos quintas partes tienen contacto previo documentado por al menos uno de tres criterios independientes y verificables.

### 5.3 · Conclusión de §5 — la clasificación del hueco son dos variantes, no una

El encargo clasifica el hueco como la tercera variante de v2.4, *"nadie corrió el mecanismo contra estas fuentes"*. La derivación no lo sostiene como clasificación única. Son dos, y hay que contarlas por separado:

- **"se corrió el mecanismo y nunca se registró"** — ≥212 payloads (39.4% de los SIN-DEMANDA), por tres criterios. `SIN-DEMANDA` es una etiqueta de **cobertura de cableado**, no de explotación.
- **"nadie corrió el mecanismo contra estas fuentes"** — el resto, ≤326 payloads (60.6%). Ahí sí aplica la variante que el encargo asumió, y ahí es donde la Función C tiene que buscar.

**Este acto no corrige el censo** — está fuera de perímetro y su escritor es `write_barrido2_w0.py`. Propone que la cifra se cite siempre con su denominador real: *"85.8% de los payloads no tiene una necesidad que lo cite en el registro de barrido2"*, nunca *"85.8% sin explotar"*.

---
## 6 · Defectos encontrados al derivar — ninguno se arregla aquí, todos están fuera de perímetro

Este acto no toca `canon/modelo-decision-v4_0.md` (prohibido explícitamente por el encargo), ni `README.md`, ni `data/INFRAESTRUCTURA-v1_0.md`, ni el censo. Los cuatro defectos siguientes se reportan con su comando y quedan para el acto que tenga perímetro.

### 6.1 · `canon/modelo-decision-v4_0.md` se contradice consigo mismo sobre el proxy de `norma_de_género`

En el árbol vigente conviven dos afirmaciones incompatibles sobre la misma θ:

- La fila **H-11** de la tabla de hipótesis declara *"**PROXY CON SUPUESTO DECLARADO** — ENUT 6.11/6.11a, carga de cuidado a nivel persona (ADR-51 (c), M2)"*.
- La fila **MEDIDO·NACIONAL** de la tabla de clases dice, del mismo generador, *"**cita corregida 13/ago/2026 por `ACTO PROC-11`**: decía «ENUT 6.11/6.11a, M2», obsoleta desde que ADR-67(b) fijó `P7_12_7` como la θ real de este generador el 10/ago; **ENUT queda como capa conductual, no como θ**"*.

La corrección se aplicó en un sitio y no en el otro. **Consecuencia medida en este mismo acto:** la cita viva de H-11 fue lo que llevó a este ejecutor a tratar ENUT como el proxy vigente y a lanzar un barrido sobre sus 16 payloads antes de encontrar que el programa ya lo había resuelto. Un lector que entre por H-11 repite el rodeo.

Corrobora la corrección, de forma independiente, `forense/notas/2026-08-04-enut-paso1-familismo-obligacion.md` (4/ago), que ya había derivado el argumento sustantivo contra microdato real: las series `P6_11_01`–`P6_11_14` preguntan **conducta observada** (*"¿usted le(s) dio de comer o ayudó a hacerlo?"*, catálogo `1` Sí / `2` No), mientras el glosario define `familismo_obligacion` como **creencia internalizada** de deber sacrificarse por la familia (escalas Zeiders/Fuligni/Calzada, actitudinales); la Sección VI completa de ENUT (`6.1`–`6.23`) es tiempo dedicado a actividades, sin un solo ítem de actitud. Añade además dos límites de universo que ningún resumen posterior conserva: la batería está condicionada por `FILTRO_S6_11` a **8 943 de 74 053** informantes (12.08%), y la disponibilidad conjunta que H-11 exige (obligación ∧ formalidad ∧ ingreso, misma persona) cae a **3 496 (39.1%)** porque los proxies de empleo exigen haber trabajado la semana de referencia — lo que excluye estructuralmente a las cuidadoras sin empleo remunerado, justo la población donde la hipótesis importaría más.

### 6.2 · `README.md` cita «tres asociaciones marginales» y hay cinco

```
$ python3 -c "print(open('milpa/procedencia.yaml',encoding='utf-8').read().count('clase: \"MEDIDO·β̂'))"
5
```

`README.md` dice, en la línea del contador de coeficientes: *"tres asociaciones marginales (β̂) existen para tres de los quince"*. Son cinco desde el 4/ago/2026, cuando el Encargo E añadió las dos entradas de ENVIPE (`G4.exposicion_violencia` y `G4.confianza_institucional[justicia]`). **El «0 de 15» de esa misma línea es correcto** —`ADR-57(a)` rotula esos β̂ como asociaciones, no coeficientes—; lo vencido es el «tres». El contador vecino, *"Condicionales medidas 12 de 15"*, sí está al día: se deriva por la fórmula de T19b y da 10 `MEDIDO·PARCIAL` + 2 `MEDIDO·NACIONAL` = 12, verificado en este acto.

### 6.3 · `data/INFRAESTRUCTURA-v1_0.md` subdeclara lectores y cuenta mal las celdas-D

- **Lectores.** El índice afirma que `necesidad-objeto-modelo.tsv` la lee *"solo `test_barrido_completo.py`"*, con *"0 lectores fuera del test"*. Tiene **cinco**, dos de producción: `tools/censo_estimabilidad.py` (el derivador del censo de coeficientes) y `tools/curador_registro/tareas_barrido2.py`; más `integrate_barrido2.py`, que la recibe por el flag **obligatorio** `--mapping` de la rama `--barrido2` del CLI real; más dos tests de `tools/curador_registro/tests/`. Importa porque el índice se usa para decidir si tocar una tabla es seguro: «nadie la lee» y «la lee el derivador de los 15 coeficientes» llevan a decisiones opuestas.
- **Celdas-D.** El índice dice *"hoy **2 archivos**"* y los nombra. Hay **tres**: falta `G5.obligacion_medida.conducta.yaml`, escrita el 13/ago por `ACTO PROC-11` — el mismo día en que el índice se construyó.

```
$ ls data/curacion-registro/celdas-d/ | wc -l
3
```

### 6.4 · El cableado nombra `reactivo_id` a algo que no es un reactivo

Ya derivado en §4 y se repite aquí porque es el defecto con más consecuencia operativa: en las 37 filas, `reactivo_id` es idéntico a `objeto_logico_id`, ninguno nombra una variable, y `texto_reactivo_recortado` guarda un descriptor de material (`COLUMNA`, `VARIABLE-SAV`, `SECCION-PDF`, `[REDACTADO-PRIVACIDAD]`…), no texto de pregunta. Quien lea el cableado creyendo que `EXISTE-SATISFACE` significa «esta variable mide este coeficiente» concluye de más: significa «este objeto material satisface, al grado de un resumen neutral compacto». La distancia entre las dos lecturas es exactamente el trabajo que falta.

---
