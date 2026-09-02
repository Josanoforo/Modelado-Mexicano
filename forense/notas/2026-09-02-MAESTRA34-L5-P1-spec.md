# ACTO MAESTRA34-L5 · P1 · `tramite.gobierno_digital.util_sin_coercion` — SPEC CONGELADA

**COMMIT-1 de la pieza P1.** Este archivo se escribe **antes de calcular ningún
desenlace**. Lo único que se ha tocado de ENCIG 2025 hasta aquí son la estructura
de la base de datos, la lista de columnas y los **denominadores por `N_TRA`**
(P0 · censo, `forense/notas/2026-09-02-MAESTRA34-L5-P0-censo.md`): en ningún
momento se ha cruzado `N_TRA` ni ningún filtro contra `P7_3`, que es la variable
de desenlace de esta pieza.

**Prior que se pone a prueba** (`milpa/tramite.yaml:177-201`, clase ASIGNADO, tier
MEDIA-FUERTE, **probabilidades explícitamente NO CALIBRADAS** según su propia
`nota_calibracion`): `adopta p=0.71` / `rechaza_servicio p=0.29`, bajo
`contexto_producto: {coercitivo: false, riesgo_fiscal_percibido: false}`.

---

## §1 · Spec

### 1.1 Payload y tabla

| campo | valor |
|---|---|
| payload | `data/raw/encig25_base_datos_csv.zip` · id de manifiesto `encig25_base_datos_csv` (`data/manifiesto.yaml:4214`) |
| tabla | `encig2025_04_sec_7.csv` (sección VII · Calidad de trámites y servicios públicos) |
| unidad de análisis | **TRÁMITE**, no persona |
| lector | `leer_csv_cr` de `tools/calibracion_mordida_encig_serie.py` (tolerante al CR suelto y embebido de INEGI), `encoding='utf-8'` — verificado en P0 que esta tabla decodifica en UTF-8 sin reemplazos |

### 1.2 Deduplicación

`sec_7` trae filas repetidas: 124 314 filas contra 113 717 `ID_TRA` únicos.
`MAESTRA34-L1` ya verificó que los 10 597 excedentes son **duplicados exactos**
en `P7_3`/`FAC_TRA`/`EST_DIS`/`UPM_DIS` (`forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`,
fila `TRA-M-13`). **Se deduplica por `ID_TRA` conservando la primera aparición**, y
la corrida **re-verifica por su cuenta** que dentro de cada `ID_TRA` repetido los
valores de `N_TRA`, `P7_3`, `FAC_TRA`, `EST_DIS` y `UPM_DIS` son idénticos. Si no
lo fueran, la pieza **PARA** y lo reporta en vez de elegir una fila.

### 1.3 Universo — el juicio declarado del acto

ENCIG 2025 **no** pregunta si el canal digital estaba disponible ni si su uso era
obligatorio (P0 · §2: cero ítems en 483 columnas de 2025 y ~100 000 de cinco
olas). La situación `le_ofrecen_servicio_gobierno_digital` y los disparadores
`coercitivo: false` / `riesgo_fiscal_percibido: false` **no los dicta el dato**:
los fija este acto restringiendo el universo a tipos de trámite (`N_TRA`) que
cumplen los tres criterios siguientes, declarados aquí y no derivados de mirar el
desenlace:

1. **Disponibilidad nacional del canal digital** — el canal existe para todo
   informante del país, no depende del municipio o del estado en que viva.
2. **Uso opcional** — existe canal presencial legalmente equivalente, así que
   elegir el digital es una conducta y no una imposición.
3. **Sin riesgo fiscal percibido** — el trámite no es ante autoridad fiscal ni
   obliga a declarar ingresos o patrimonio.

**Universo principal: `N_TRA == '01'`** — «el pago ordinario del servicio de luz».
Es el único tipo del catálogo que cumple los tres sin ambigüedad: la Comisión
Federal de Electricidad opera portal y aplicación de cobertura nacional (1), el
mismo recibo se paga en ventanilla, banco o tienda (2), y no interviene autoridad
fiscal alguna (3). Denominador contado en P0: **n = 20 392 filas** antes de
deduplicar.

**Exclusiones y su razón** (se declaran para que el juicio sea auditable, no para
justificarlo después): `02` agua y `03` predial son municipales y su canal digital
varía por municipio — falla (1), y `03` además es un impuesto — falla (3); `04`
tenencia y `05` trámites vehiculares son estatales y varias de sus piezas exigen
presencia física — falla (1) y (2); `06` trámites fiscales ante el SAT falla (2) y
(3) y es justamente el caso que P2 no pudo medir; `07`/`08` atención médica
confunden el trámite con acudir al hospital, de modo que el canal presencial queda
impuesto por el propio trámite — falla (2); `17` pasaporte exige comparecencia —
falla (2); el resto son locales o de ventanilla.

**Sensibilidad pre-declarada A — universo ampliado: `N_TRA ∈ {'01','10'}`.**
Añade «trámites en el registro civil (actas de nacimiento, defunción, matrimonio,
divorcio)», donde el acta de nacimiento sí tiene expedición digital nacional pero
las otras tres no la tienen de manera uniforme: cumple (1) solo parcialmente. Se
reporta como sensibilidad, **nunca** como resultado principal.

### 1.4 Dicotomización de la conducta

`P7_3` — «¿A qué tipo de lugar acudió o a qué medio recurrió para realizar el
trámite o pago?»

| valor de `P7_3` | etiqueta INEGI | asignación |
|---|---|---|
| `4` | Internet (página web, aplicaciones de celular, tablet) | **`adopta` = 1** |
| `5` | Cajero automático o kiosco inteligente | **`adopta` = 1** |
| `1` | Instalaciones de gobierno (oficinas, tesorería, hospital) | `adopta` = 0 |
| `2` | Banco, supermercado, tiendas o farmacias | `adopta` = 0 |
| `6` | Módulos, clínicas u oficinas temporales o móviles | `adopta` = 0 |
| `3` | Líneas de atención telefónica | **fuera del universo** |
| `7` | No se ha podido concluir el trámite o pago | **fuera del universo** |
| `8` | Otro | **fuera del universo** |
| `9` | No sabe / no responde | **fuera del universo** |
| blanco | — | **fuera del universo** |

`3` sale porque una línea telefónica es un canal remoto **atendido por una
persona**: ni servicio digital de autoservicio ni ventanilla presencial. Se
prefiere excluirlo a forzar una categoría binaria sobre un canal mixto — el mismo
criterio que `MAESTRA34-L1` aplicó a `2` y `6` en su propia pieza. `7` sale porque
es fracaso del trámite, no elección de canal.

**Divergencia explícita frente a `MAESTRA34-L1`, declarada aquí y no descubierta
después.** `TRA-M-13` clasificó `P7_3 ∈ {3,4,5}` como «digital/registrado» porque
su constructo era el **registro** — una llamada telefónica deja rastro. El
constructo de esta pieza es **adopción de un servicio digital de gobierno**
(utilidad ⇒ adopción, mecanismo del §3.3 del modelo, validado contra SPEI/CoDi),
y una llamada atendida por una persona no es un servicio digital. Misma fuente,
misma variable, distinto constructo, distinta partición: se declara para que nadie
lea las dos cifras como si midieran lo mismo.

**Sensibilidad pre-declarada B — `3` dentro del denominador como NO adopción**
(`adopta = 0`), por si mesa prefiere leer el teléfono como canal no digital en
lugar de excluirlo.

### 1.5 Ponderador, diseño e intervalo

| campo | valor |
|---|---|
| ponderador | **`FAC_TRA`** — factor de expansión de **trámite**, que es la unidad de análisis. No `FAC_P18`, que expande personas |
| estrato | `EST_DIS` |
| UPM | `UPM_DIS` |
| estimador | proporción ponderada `p̂ = Σ(w·d) / Σw` |
| IC95 | **bootstrap conglomerado estratificado**, `n_boot = 10 000`, `seed = 42`, remuestreando UPM dentro de estrato — función `wprop_ic_conglomerado` de `tools/calibracion_mordida_encig_serie.py`, importada, **no reescrita** |
| escala | proporción en [0, 1] |

### 1.6 Estimando

**p̂ = proporción, ponderada por trámite, de trámites del universo realizados por
canal digital de autoservicio.** Es la contraparte empírica de `adopta` bajo
`coercitivo: false, riesgo_fiscal_percibido: false`, con la salvedad de que la
condición no la declara el informante sino la construcción del universo (§1.3).

### 1.7 Lo que este resultado NO es, dicho antes de tener el número

- **No** es «la tasa de adopción de gobierno digital en México»: es la de un tipo
  de trámite elegido por cumplir tres criterios declarados.
- **No** se compara contra P2, porque P2 quedó en EXISTE-NO-SATISFACE (P0 · §3).
  La comparación de SIGNO y razón que el encargo pedía **no se hace**.
- **No** se compara contra el `0.91` de la regla coercitiva: son escalas distintas
  sin enlace, y el encargo lo prohíbe expresamente.
- El prior `0.71` que se contrasta es, según su propia `nota_calibracion` en
  `milpa/tramite.yaml`, una probabilidad **no calibrada** cuyo corpus «da la
  dirección, no la magnitud». Una diferencia de magnitud contra él es información
  sobre la magnitud que nunca se afirmó, y así se reportará.

---

## §2 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

Si el procedimiento resulta equivocado, se escribe un tercer commit que lo diga;
no se corrige hacia atrás ni se reescribe esta spec.
