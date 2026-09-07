# `ACTO MAESTRA38-L16-BIS` · RAMA A `ENNViH` — **PARO**, cero mediciones, cero cambios de datos

**Acto:** `ACTO MAESTRA38-L16-BIS`, 7/sep/2026, entorno **CAJA con corpus** (worktree
`/home/pc0/mm-l16-bis-paro`), sobre `origin/main = e1c3c84`. **Encargo** (archivado por A.3):
`forense/encargos/2026-09-07-MAESTRA38-L16-BIS.md`. **ADR:** `ADR-374`.

El acto **no midió nada**: paró antes de `COMMIT-1` porque el `COMMIT-1` que el encargo dicta cita
una spec que no existe en el árbol. Dirección resolvió el paro el mismo día (§4). Esta nota es el
registro de qué se verificó, con qué comando, y qué queda dictado para el sucesor.

---

## 1 · ARRANQUE (los cinco puntos de `/acto`, D-11)

| punto | valor crudo |
|---|---|
| **0 · GUARD DE RAMA** | `git ls-remote --heads origin \| grep -iE "l16"` → **0 líneas** (exit 1). Ninguna sesión corriendo esto. Rama creada y empujada con el 0-bis en el primer minuto. |
| **1 · REPO** | Clon existente `/home/pc0/Modelado-Mexicano`; worktree nuevo `/home/pc0/mm-l16-bis-paro` desde `origin/main`. `git log -1` → `e1c3c84 Merge pull request #580 …`. `git status` limpio al arrancar. |
| **2 · SHA** | El encargo no declara SHA de redacción. Base real declarada: `origin/main = e1c3c84` (`ADR` máx `373`, `FP` máx `329`, por `python3 tools/cierre_acto.py` Fase A). |
| **3 · `data/raw`** | El worktree nació sin ella (normal, raíz integrada gitignorada). **Enlazada** a `/home/pc0/mm-corpus/raw` y `data/raices.local.yaml` copiada del clon padre **antes** de evaluar nada — corrección de `PR #522`. `ls data/raw/ \| head -1` → `2005trim1_csv.zip`. El corpus **está** montado. |
| **4 · ENTORNO** | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → `sin_variable`. Sonda de red: **no corrida** — este acto no toca red (paró antes de abrir microdato y no descarga nada). Tercera parte (A.2): corpus montado, ver punto 3. |
| **5 · ESPEJO** | Ninguna cifra de esta nota sale del espejo del proyecto: todas salen del worktree de (1), con el comando a la vista. |

## 2 · COMPUERTA — cumplida **por rótulo**, no cumplida **por producto**

El encabezado del encargo declara «tras `LOTE-CRUCE` fusionado y `N18` sellado», y el cuerpo añade
la condición de redacción «se redacta completo cuando `N18` selle (**no antes: la spec fija el
universo**)». Verificado por producto, no por `grep` de asunto (`ADR-277`):

| premisa | comando | resultado |
|---|---|---|
| `ACTO MAESTRA38-LOTE-CRUCE` fusionado | `gh pr view 578 --json state,mergedAt` | **CUMPLE** — `MERGED`, `2026-09-07T02:43:02Z` |
| `ACTO MAESTRA38-N18` sellado | `git show origin/main:forense/encargos/2026-09-07-MAESTRA38-N18-S7-L17-SPEC-V1_1.md` | **CUMPLE** — archivado, con `## CONSUMIDO` |
| «`COMMIT-1` cita `S6` v1.1 y su sha» | `git cat-file -e origin/main:forense/prereg-caja/S6-L16-spec-v1_1.md` | **`fatal: path … does not exist in 'origin/main'`** |

**El rótulo del gate se cumple; el producto que el gate existe para garantizar, no.** `ACTO
MAESTRA38-N18` no selló `S6` v1.1: selló **`S7-L17` v1.1** — su propio cuerpo lo dice verbatim
(*«Escribe `forense/prereg-caja/S7-L17-spec-v1_1.md` + `.sha256`: copia de v1.0 con una corrección
— §2, mapeo del bloque `a0927`…»*), y `git cat-file -e origin/main:forense/prereg-caja/S7-L17-spec-v1_1.md`
sale `0`. De `S6` existe **sólo v1.0** (`forense/prereg-caja/S6-L16-spec-v1_0.md`, `sha256
317e42c3becca6402aa0848f9cd5a4ace2af784ea174024c7dab0687db724b9f`). Ningún acto en vuelo la
produce: `gh pr list --state open` → **0 PRs**; `git ls-remote --heads origin | grep -iE "l16|s6"`
→ **0 ramas**.

Consecuencia, per `/acto` §2.3: **cero commits sustantivos**. No se adelantó ningún paso «por si
acaso» — es exactamente el defecto que `ADR-224`/`ADR-234` existen para dejar de pagar dos veces.

## 3 · Los tres puntos donde el universo pedido choca con la spec congelada

El encargo pide medir con un universo que `prereg-caja-S6-L16` **v1.0** no autoriza. No se ajustó
el texto para que cuadre (`el ejecutor propaga una decisión dictada, no decide`, `ADR-76`/`ADR-79`).

**(1) 2005 no tiene desenlace.** `clave1`/`clave2` («ID CLINICA COMUNITARIO» / «ID PROVEEDOR SALUD
COMUNITARIO») es la única vía a institución de la Rama A — la propia spec ya lo declara en §0.3
(`cen10*` es **sólo geografía**) y en §3 (`NO-CONSTRUIBLE-SIN-DIRECTORIO-EXTERNO` salvo que caja
confirme `clave1`/`clave2`, **solo 2002**). Medido sobre `data/inventario-reactivos-ext-v1_0.tsv`
(**63 350 filas examinadas**, A.13):

```
$ awk -F'\t' '($6=="clave1"||$6=="clave2"){split($1,a,"/"); print a[2]"\t"$6}' \
      data/inventario-reactivos-ext-v1_0.tsv | sort | uniq -c
      8 ehh02dta_all.zip	clave1
      8 ehh02dta_all.zip	clave2
```

**8+8 filas en 2002; cero en 2005 y cero en 2009.** Control positivo, mismo comando, mismas tres
olas: `es09` → 2/2/2 y `cen10d_1` → 1/1/1 — el filtro sí encuentra variables de estas olas cuando
las hay, así que el cero de `clave*` es un cero medido, no un cero de comando mal escrito.
Pedir «2002 y 2005» produce celda de desenlace **sólo en 2002**; 2005 cae en la fila
`NO-ESTIMABLE` que la propia §4 ya tenía pre-registrada.

**(2) «IC por conglomerado» no tiene conglomerado.** La spec §1.3 lo declara y esta nota lo
re-verifica sobre las **16 925 filas** de las tres olas `ehh0[259]dta_all.zip`:

```
# negativo: nombre o etiqueta de unidad primaria / conglomerado
$ awk -F'\t' '$1 ~ /ennvih\/ehh0[259]dta_all.zip/ && (tolower($6) ~ /^(upm|psu|cluster|conglomerado)/ \
      || tolower($7) ~ /unidad primaria|conglomerad|cluster/)' … | wc -l
0
# control positivo, mismo filtro de olas
$ awk -F'\t' '… && tolower($6)=="estrato" {print $1"\t"$5"\t"$6"\t"$7}' …
ennvih/ehh02dta_all.zip	ehh02dta_all/ehh02dta_bc/c_portad.dta	estrato	ESTRATO
ennvih/ehh05dta_all.zip	ehh05dta_bc/c_portad.dta	estrato	ESTRATO
ennvih/ehh09dta_all.zip	ehh09dta_all/ehh09dta_bc/c_portad.dta	estrato	ESTRATO
```

**Cero unidades primarias, tres estratos.** Un IC «por conglomerado» no es construible tal como
está escrito; hay que declarar cuál es el conglomerado (dirección lo dictó en §4(c): el hogar).

**Dato nuevo, no en la spec, para el sucesor:** el diseño real **sí está documentado en el corpus**
— `ennvih1_muestra_diseno` (`ennvih_diseno/ennvih-1_muestra.pdf`, `data/manifiesto.yaml`), cuyo
`usado_para` dice verbatim *«nota metodologica de muestra ENNViH-1: UPM/estrato/USM, esquema
polietapico estratificado por conglomerados»*. Lo que falta no es la documentación del diseño: es
la **columna de UPM en los `.dta`**. La distinción importa para redactar la reserva de varianza sin
afirmar de más.

**(3) El ponderador de 2005 no está en la lista congelada de §6.** `fac_3b_px`/`fac_3b` están
adjudicables **sólo para 2002**: la tabla que los mide, `data/ennvih2002-ponderadores-candidatos-v1_0.tsv`
(`ACTO MAESTRA38-C1`, pieza (h)), es de 2002 y de un solo payload (`ennvih1_2002_ponderador`).
`ennvih2_2005_ponderador_transversal` (`ennvih/ehh05w_all.zip`) **sí está registrado** en
`data/manifiesto.yaml`, pero la lista de §6 de la spec congelada no lo trae — medir 2005 ponderado
exige añadirlo a §6, que es acto de spec, no de caja.

## 4 · Resolución de dirección — verbatim, 7/sep/2026

> **INPUT AL PARO DE MAESTRA38-L16-BIS · OPCIÓN 1 · N19 (S6 v1.1) → L16-BIS-2**
> dirección (Fable) · 7/sep/2026 · contra origin/main = e1c3c84 · decidido en conversación; la firma es el merge
>
> **0 · Decisión**
>
> Opción 1. Un acto de nube (N19) escribe S6-L16-spec-v1_1.md + .sha256; L16-BIS se relanza citándola. Se descartan la 2 (medir con desviaciones declaradas cuando ya se conocen antes de abrir el dato — eso es pre-registrar después de saber) y la 3 (fijar el universo en el encargo y no en la spec deja sin sidecar lo que la regla exige sellado). Cierre del acto que paró: se archiva como ADR de PARO (patrón ADR-358): 0-bis con el encargo, forense/notas/2026-09-07-MAESTRA38-L16-BIS-paro.md con la tabla de premisas y los tres puntos, cero cambios de datos, check.py VERDE, PR. Hallazgo para hallazgos.md, una línea: «dirección encargó L16-BIS citando una spec que N18 no produjo (N18 selló S7 v1.1, no S6 v1.1): compuerta por rótulo cumplida, por producto no».
>
> **1 · Las tres correcciones, dictadas (van verbatim al COMMIT-1 de N19)**
>
> (a) Ponderador. Rama bx (libro proxy, sección ES, p_es.dta): fac_3b_px (ennvih1_2002_ponderador, ehh02w_all/ehh02w_bx.dta). Rama b3b (libro directo, «SERIO»): fac_3b. Llave folio/ls normalizados a entero (C1: sin normalizar, todos los joins dan 0). Razón: la sección ES pertenece al libro 3B y el libro proxy replica 3A/3B/4 con un factor por libro replicado; fac_3a_px/fac_3b_px tienen media ≈ 1 914.8 (adultos) y fac_4_px 808.7 (niños). Verificación previa obligatoria: sobre las filas de p_es.dta con es09 no nulo, n_no_nulo_gt0(fac_3b_px) ≥ n_no_nulo_gt0(fac_3a_px) y ≥ (fac_4_px); si no, PARA — la asignación libro→factor es otra. Las dos ramas se reportan por separado, nunca agrupadas (A-bis 4: bx es la subpoblación respondida por proxy). (b) Universo y olas. El desenlace de R4.4 (institución pública vs privada, clave1/clave2) existe sólo en 2002 (8+8 filas en ehh02dta_all.zip; 0 en 2005 y 2009; control positivo cen10*/es09 en las tres olas). Por tanto: celda de desenlace sólo 2002; 2005 entra únicamente como réplica descriptiva del disparador (es09: prevalencia ponderada con ennvih2_2005_ponderador_transversal, que se añade a §6), sin celda de desenlace y con la fila NO-ESTIMABLE de §4 ya pre-registrada para 2005 — se cita, no se fuerza. 2009 fuera (adjetivo «SERIO» y sin desenlace). ENDIREH 2016 queda como está en v1.0. (c) Varianza. No hay UPM/PSU en ninguna ola (buscado, cero); hay estrato en c_portad.dta. Se declara el diseño real: conglomerado = hogar (folio), estrato = el de c_portad, IC por bootstrap de hogares dentro de estrato. Se escribe en la spec que la unidad primaria real de ENNViH (localidad) no está en los archivos, que el IC por hogar subestima la varianza respecto al diseño verdadero, y que por eso un resultado que apenas excluya 0 se reporta como PROPUESTA con reserva (A-bis, contraparte). Escala declarada: proporciones ponderadas; universo declarado por rama. Fila B-bis: qué significa que no discrimine en 2002 (→ R4.4 queda ACOTADA por su se_mueve_si de SELLO-2 fila 2) y qué significa que discrimine (CORROBORADA en un instrumento, sin réplica: no mueve tier).

**Sucesores declarados, no ejecutados por este acto:** `ACTO MAESTRA38-N19` (nube) escribe
`forense/prereg-caja/S6-L16-spec-v1_1.md` + `.sha256` llevando §4(a)(b)(c) verbatim a su
`COMMIT-1`; después `ACTO MAESTRA38-L16-BIS-2` (caja con corpus) mide la Rama A citando la v1.1 y
su sha. Este acto **no** escribe la v1.1: hacerlo sería que el ejecutor que encontró el hueco
redacte la spec que lo tapa, con el dato ya a la vista.

## 5 · Estado de `R4.4` al cerrar este acto — qué está medido y qué no

`python3 tools/ya_medido.py R4.4` → `MEDIDA-EN: 2026-09-06-MAESTRA38-LOTE-ENSANUT-resultados.md, S6`.
El marcador es correcto **y sólo cubre la Rama B**: `ACTO MAESTRA38-LOTE-ENSANUT` (rótulo
`MAESTRA38-L16`, `canon/registro-rotulos.tsv:189`) midió `ENSANUT2024` y selló `B-bis
NO-DISCRIMINA` (`p(publico|grave)=52.23%`, `IC95[36.82,69.84]`, `n=423`). **La Rama A (`ENNViH`)
sigue sin medir** — es exactamente lo que este acto iba a hacer y no hizo. `salud.atencion.grave`
queda `[MEDIA]` en `canon/modelo-decision-v4_0.md:527`, sin tocar.

## 6 · Perímetro real de este acto

**Toca:** `forense/encargos/2026-09-07-MAESTRA38-L16-BIS.md` (0-bis + `## CONSUMIDO`) · esta nota ·
`canon/gobernanza-v1_15.md` (`ADR-374`) · `canon/estado-programa-v1_12.md` (L0) ·
`canon/registro-rotulos.tsv` (rótulo propio) · `forense/hallazgos.md` (una línea).

**NO toca — verificado:** ningún `.dta`/`.zip` abierto (cero microdato) · `data/**` sin un solo
cambio (`git status` de datos limpio) · `forense/prereg-caja/**` intacto (no escribe la v1.1) ·
`milpa/tramite.yaml` ni `milpa/tramite-ola5-propuesta-v0.yaml` (el encargo pedía «entra a la
propuesta como entrada nueva»: **no ejecutado**, no hay medición que cargar) ·
`canon/modelo-decision-v4_0.md` · `forense/firmas-pendientes.tsv` (no se firma ni se abre ninguna
fila; `FP-328` ya lleva la adjudicación del ponderador como decisión de mesa) · `tests/*.py` ·
`tools/*.py`.

**Medición: cero.** Cero celdas, cero `p`, cero IC, cero veredictos.

## 7 · `tests/check.py --baseline`

**VERDE** — ver la salida citada en `ADR-374`.
