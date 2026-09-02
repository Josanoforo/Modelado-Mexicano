# ACTO MAESTRA35-L1 · RESULTADOS por pieza

Este documento crece un bloque por commit de resultados. **No edita** la spec
congelada (`forense/notas/2026-09-02-MAESTRA35-L1-spec.md`, `e2dbd82`) ni el
censo (`…-P0-censo.md`, `0763c07`). Una sola corrida por celda, sin reintentos.

---

# `P1` · `tramite.mordida.con_registro` recorrida sin deduplicar

**Script:** `tools/recorre_mordida_con_registro_encig25.py` · **spec:** §2 ·
**firma:** mesa 2/sep/2026, `d1` = `FP-238`.
**Payload:** `encig25_base_datos_csv`,
sha256 `47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12`.

## §1 · Salida cruda de la única corrida

```
sec_7    : 124,314 filas · ID_TRA distintos 113,717 · (ID_TRA,NT_TIPO) grupos 124,314
sec_8    : 1,083,672 filas · ID_TRA llave unica (guardia 1 OK)
universo : P8_4 in {0,1} = 21,139 filas de sec_8; al grano de EVENTO -> 24,974 en 21,139 ID_TRA
           una deduplicacion por ID_TRA descartaria 3,835 eventos: no se deduplica.

MAPEO principal (MAESTRA34-L1: digital {3,4,5})
  DIGITAL/REGISTRADO · P7_3 in ['3', '4', '5']
    p̂ = 0.029868   IC95 = [0.021133, 0.040452]
    n = 7,219 EVENTOS de tramite (en 6,384 ID_TRA) · con mordida = 242
    estratos = 362 · UPM = 2,518 · poblacion expandida = 29,467,394
  PRESENCIAL · P7_3 in ['1']
    p̂ = 0.141041   IC95 = [0.116817, 0.169579]
    n = 11,167 EVENTOS de tramite (en 9,992 ID_TRA) · con mordida = 1,496
    estratos = 381 · UPM = 2,996 · poblacion expandida = 34,171,657
    RAZON presencial/digital = 4.7222x  (signo: presencial MAYOR)
    IC95 se traslapan: False

MAPEO sensibilidad A (MAESTRA34-L5: digital {4,5}, 3 fuera)
  DIGITAL/REGISTRADO · P7_3 in ['4', '5']
    p̂ = 0.025078   IC95 = [0.015990, 0.036467]
    n = 5,251 EVENTOS de tramite (en 5,040 ID_TRA) · con mordida = 158
    estratos = 357 · UPM = 2,308 · poblacion expandida = 25,821,039
  PRESENCIAL · P7_3 in ['1']
    p̂ = 0.141041   IC95 = [0.116817, 0.169579]
    n = 11,167 EVENTOS de tramite (en 9,992 ID_TRA) · con mordida = 1,496
    estratos = 381 · UPM = 2,996 · poblacion expandida = 34,171,657
    RAZON presencial/digital = 5.6241x  (signo: presencial MAYOR)
    IC95 se traslapan: False
```

## §2 · Antes y después, en la misma escala

| conducta cargada en `milpa/tramite.yaml` | sellada (1/sep) | recorrida (2/sep) | Δ | Δ relativo |
|---|---|---|---|---|
| `paga_mordida_encig2025_digital` | 0.027358 (n 6 337) | **0.029868** (n 7 219) | +0.002510 | +9.2 % |
| `paga_mordida_encig2025_presencial` | 0.116000 (n 9 937) | **0.141041** (n 11 167) | +0.025041 | +21.6 % |
| razón presencial/digital | 4.2401× | **4.7222×** | +0.4821 | +11.4 % |

Las `n` suben porque la deduplicación borraba eventos: 6 337 → 7 219 en el
canal digital y 9 937 → 11 167 en el presencial.

## §3 · Los dos veredictos — y el hueco de la spec

**Canal digital: `CORRECCIÓN SIN CAMBIO MATERIAL`.** La regla congelada en la
spec §2.1, escrita antes de ver el número, decía: si el IC95 nuevo del canal
digital contiene `0.027358`, se reporta así. **Lo contiene**:
`0.027358 ∈ [0.021133, 0.040452]`.

**Canal presencial: `VENCIDA EN ALCANCE — re-sello de mesa`, y se reclama
`FP-241`.** Aquí hay que decir dos cosas y no una:

1. **La spec congelada solo regló el canal digital.** Es un hueco de la spec,
   no un resultado: el `CONTADOR` del propio encargo pone los **dos** canales
   en alcance («cifra sellada corregida +1 (`con_registro`, **dos canales**)»),
   y `milpa/tramite.yaml:139-142` carga las cuatro conductas con `tier: FUERTE`.
   La spec no se edita (COMMIT-1 es intocable); el hueco se dice aquí.
2. **Aplicada al presencial la misma prueba, falla — por poco.**
   `0.116000 ∉ [0.116817, 0.169579]`: queda fuera **por 0.000817** del límite
   inferior. El criterio de pertenencia falla estrechamente; **el movimiento del
   punto no es estrecho**: +0.025041, +21.6 % relativo. Mesa tiene los dos
   números para decidir si el re-sello vale el trámite.

**Contra-hipótesis declarada: NO se cumple, y el hallazgo se refuerza.**
La spec decía que si la razón presencial/digital caía **por debajo de 2×** con
la llave correcta, el hallazgo de `MAESTRA34-L1` («el registro rompe la trampa
social») quedaba **ACOTADO**. Sube de 4.2401× a **4.7222×** (5.6241× en la
sensibilidad A), con IC95 sin traslape en los dos mapeos. **El hallazgo no
queda acotado: queda más grande.**

## §4 · Por qué el número se movió hacia arriba en los dos canales

No es ruido de remuestreo: el universo cambió. Los 3 835 eventos que la
deduplicación borraba no eran una muestra aleatoria del resto — eran **eventos
repetidos del mismo trámite por la misma persona**, y quien repite un trámite
tiene más ocasiones de encontrarse la mordida. Al devolverlos al universo, la
tasa por evento sube en los dos canales. Que suba **más** en el presencial
(+21.6 % vs +9.2 %) es consistente con el mismo mecanismo, pero **no** se
declara aquí como hallazgo: esta pieza recorre, no identifica. Es asociación
dentro de una corrida (A-bis 1), no un efecto (A-bis 2).

## §5 · Lo que este resultado escribió

- **Enmienda in situ** bajo `tramite.mordida.con_registro_encig2025` en
  `milpa/tramite-ola5-propuesta-v0.yaml`, clave `enmienda_maestra35_l1`.
  Verificado: **0 líneas del cuerpo viejo eliminadas o modificadas** (A.10
  corolario 1); el YAML parsea.
- **Filas nuevas** `TRA-M-13b` y `TRA-M-14b` en
  `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`, con
  `estado: SUSTITUYE-A TRA-M-13` / `SUSTITUYE-A TRA-M-14`. Verificado:
  **0 filas existentes editadas**; 37 filas, todas con 12 campos.
- **`milpa/tramite.yaml` NO se tocó.** El sello es de mesa, en RH.

---

# `P2` · `dinero.ahorro.via_informal` por ejes, ENIF 2024

**Script:** `tools/medidor_ahorro_enif24.py --ejes` · **spec:** §3.
**Payload:** `enif_2024_bd_csv`, sha256 `00e4b0b4…7684f039`, `TMODULO.csv`,
13 502 personas elegidas 18+, `FAC_PER`/`EST_DIS`/`UPM_DIS`.

**Diff sobre el medidor de `MAESTRA34-L5`:** aditivo. Se añadieron un `import`,
las definiciones de eje, `desenlaces()`, `_celda_cuenta()` y `main_ejes()`, y se
sustituyó la única línea `main()` del bloque `__main__` por una rama
`if "--ejes" in sys.argv`. **Control positivo:** corrido sin `--ejes`, el
medidor reproduce `MAESTRA34-L5` al último dígito — unión 0.642080, solo
formal 0.284927, solo informal 0.561920.

## §1 · Globales

| desenlace | p̂ | IC95 | n | numerador |
|---|---|---|---|---|
| `ahorra_solo_informal` (**principal**) | **0.357152** | [0.344596, 0.369687] | 13 502 | 4 621 |
| `informal_cualquiera` (secundario) | 0.561920 | [0.549922, 0.573502] | 13 502 | 7 590 |

El secundario coincide exacto con la sensibilidad B de `L5`: es la misma
cantidad, y sirve de control de que el universo no cambió.

## §2 · Veredicto por eje

| eje | cobertura | principal | secundario |
|---|---|---|---|
| `sexo` | 100.00 % | DISCRIMINA | NO-DISCRIMINA |
| `edad` | 99.89 % | DISCRIMINA | DISCRIMINA |
| `escolaridad` | 99.96 % | **CONTRARIA** (no monótono) | **CONTRARIA** |
| `localidad` | 100.00 % | **CORROBORADA** | NO-DISCRIMINA |
| `formalidad` | **68.97 %** ⚠ | **CORROBORADA** | **CONTRARIA** |
| `cuenta_formal` | 100.00 % | DISCRIMINA (tope) | **CONTRARIA** |

⚠ `formalidad` corre bajo **universo restringido (A-bis 4)** y no reconcilia
contra el marginal poblacional.

## §3 · El caso para el que se escribió la regla de precedencia

`escolaridad` contra el principal:

| celda | p̂ | IC95 | n |
|---|---|---|---|
| hasta primaria | 0.351594 | [0.328573, 0.374051] | 3 249 |
| secundaria | **0.415635** | [0.394176, 0.436785] | 3 635 |
| media superior | 0.389338 | [0.363063, 0.415331] | 3 408 |
| superior | 0.260438 | [0.240043, 0.280613] | 3 205 |

Las **celdas extremas van en el signo esperado** (0.3516 > 0.2604) y sin
traslape: leídas solas, `CORROBORADA`. Pero el par
`hasta primaria → secundaria` va limpio **en contra** (0.3516 → 0.4156, IC95 sin
traslape), y otro par consecutivo limpio va a favor: el eje es **NO MONÓTONO** y
la precedencia congelada en la spec §1.1 (`CONTRARIA` manda sobre
`CORROBORADA`) da **CONTRARIA**. Es exactamente el caso para el que esa regla
existe, y aparece en el primer lote que la usa.

**Operacionalización que este commit añade y la spec no fijó:** «tramos
distintos» se recorre como **pares consecutivos** en el orden declarado del eje.
La spec fijó la regla, no cómo se recorre el orden; se dice aquí en vez de
editarla.

## §4 · El hallazgo grande: el ahorro informal es complemento, no sustituto

Contra el desenlace **secundario** — el que **sí** es falsable, porque
`informal_cualquiera` no está anidado en la tenencia de cuenta — el mecanismo
`G3`/`informal_sin_puente` **se cae entero**:

| eje | celda baja | celda alta | veredicto |
|---|---|---|---|
| `cuenta_formal` | sin cuenta **0.493506** | con cuenta **0.597889** | CONTRARIA |
| `formalidad` | sin seg. social 0.604060 | con seg. social **0.644733** | CONTRARIA |
| `escolaridad` | hasta primaria 0.414094 | superior **0.640107** | CONTRARIA |

Quien tiene cuenta ahorra informalmente **más**, no menos. Quien tiene seguridad
social por su trabajo, **más**. El ahorro informal **sube** con la escolaridad.
La lectura que estos números soportan es que el ahorro informal en México **no
es un sustituto de la exclusión financiera sino un complemento del ahorro
formal**; y que lo que el desenlace exclusivo capta no es «ahorrar
informalmente» sino **la ausencia de la pata formal**, que el cuestionario gatea
por tenencia de cuenta — el anidamiento que el censo `P0` encontró.

Esto es **asociación dentro de una corrida** (A-bis 1), no efecto (A-bis 2).

## §5 · Los dos ejes que sí corroboran

Contra el principal, con IC95 sin traslape y en el signo pre-registrado:

| eje | celda esperada alta | celda esperada baja |
|---|---|---|
| `localidad` | menor de 15 000 **0.409255** [0.387307, 0.429960] | 15 000 y más 0.329868 [0.315113, 0.344834] |
| `formalidad` | sin seg. social **0.413689** [0.394927, 0.432857] | con seg. social 0.309328 [0.288930, 0.329834] |

---

# `P3` · `tramite.gobierno_digital.util_sin_coercion` por ejes, ENCIG 2025

**Script:** `tools/medidor_gobierno_digital_encig25.py --ejes` · **spec:** §4.
Diff aditivo idéntico en forma al de `P2` (una sola línea sustituida: la llamada
a `main()`); la **dicotomización no se tocó**. **Control positivo:** sin
`--ejes` reproduce `L5`, principal 0.673393.

**Universo:** `N_TRA=='01'`, `P7_3 ∈ {1,2,4,5,6}`, **n = 20 203 trámites**.
**Unidad = TRÁMITE**, se declara en cada celda: quien pagó doce veces contribuye
doce veces. **Llave:** `ID_TRA → ID_PER → residentes_sec_2`, **0 huérfanos**.
**GLOBAL:** p̂ = 0.673393, IC95 [0.663165, 0.683910], adoptan 13 905.

| eje | cobertura | celdas (p̂) | veredicto |
|---|---|---|---|
| `sexo` | 100.00 % | H 0.681276 · M 0.665192 | NO-DISCRIMINA |
| `edad` | 99.43 % | 0.751812 · 0.774735 · 0.669153 · **0.475822** | **CORROBORADA** |
| `escolaridad` | 100.00 % | 0.391961 · 0.564634 · 0.678563 · **0.812944** | **CORROBORADA** |

`escolaridad` es **el gradiente más limpio del lote**: monótono creciente en los
cuatro tramos, con los IC95 de todos los pares consecutivos sin traslape
(0.3920 → 0.5646 → 0.6786 → 0.8129).

`edad` va en el signo esperado entre extremos (0.7518 en 18-29 vs 0.4758 en 60+,
sin traslape). No es monótona en el primer par — 30-44 mide 0.7747, más alto que
18-29 — pero ese par **traslapa** ([0.727749, 0.775779] vs [0.759377, 0.789671]),
así que no es un par limpio en contra y no dispara la precedencia.

**Ejes ausentes, declarados y no sustituidos:** tamaño de localidad (el universo
de ENCIG son ciudades de 100 mil habitantes y más, FD pág. 1) y formalidad
laboral (el FD no trae ítem de prestaciones ni de seguridad social).

---

# `P4` · `tramite.evasion_norma` por ejes, ENVIPE 2025

**Script:** `tools/medidor_evasion_norma_envipe25.py --ejes` · **spec:** §5.
Diff aditivo idéntico en forma; el estimando **no se tocó** (la conjunta, unidad
delito, `FAC_DEL`). **Control positivo:** sin `--ejes` reproduce `L5`,
principal 0.562774.

**Universo:** `BP1_20 ∈ {1,2}`, **n = 40 280 delitos**. **Unidad = DELITO.**
**Llave:** `ID_PER` (`tmod_vic` → `tsdem`), **0 huérfanos**.
**GLOBAL:** p̂ = 0.562774, IC95 [0.551982, 0.573448], numerador 21 761.

| eje | cobertura | celdas (p̂) | veredicto |
|---|---|---|---|
| `sexo` | 100.00 % | H **0.597383** · M 0.530654 | DISCRIMINA |
| `edad` | 99.77 % | 0.520035 · 0.580792 · 0.601214 · 0.566020 | DISCRIMINA |
| `escolaridad_proxy` | 99.75 % | 0.493221 · 0.567369 · 0.543368 · 0.590093 | DISCRIMINA |
| `dominio_urbano_rural` | 100.00 % | R 0.403310 · C 0.522090 · U **0.592703** | DISCRIMINA |

**Los cuatro DISCRIMINAN y ninguno podía corroborar: así se pre-registró, por la
fuente y no por el resultado.**

**El gradiente de dominio apunta al revés de la corazonada del encargo.** La
evasión de norma es **más alta en lo urbano** (0.5927) que en lo rural (0.4033),
con complemento urbano en medio (0.5221) y los tres IC95 sin traslape — mientras
que el encargo esperaba «localidad menor de 15 000 **más alta** (sanción menos
creíble)». **Esto NO se reporta como `CONTRARIA`**: el eje medido **no es** el
corte de 15 000, ENVIPE no publica umbral, y `R` ↔ «menor de 15 000» no está
verificado en ninguna fuente del payload. Si mesa acepta leer `R` como localidad
pequeña, el signo esperado del encargo quedaría **invertido** — y esa lectura es
de mesa, no del ejecutor.

`escolaridad_proxy` discrimina **sin patrón monótono** (0.4932 / 0.5674 / 0.5434
/ 0.5901), que es consistente con que subsistencia y cinismo empujen en sentidos
opuestos — justo la razón por la que la regla no predice signo ahí.

---

# Cierre del lote

**Cuatro piezas, cuatro midieron. Ninguna PARÓ.** 55 celdas con IC nuevas en las
tres entradas por ejes, más los tres estimandos de `P1`.

Las tres entradas de `P2`/`P3`/`P4` y la enmienda de `P1` se emitieron **desde
los propios resultados**, no a mano: `tools/emite_propuesta_ejes_maestra35_l1.py`
importa los tres `main_ejes()` y serializa lo que devuelven. **Control de
transcripción:** los 55 valores `p:` del YAML son un subconjunto exacto de los
59 `p̂` impresos por las tres corridas — los 4 que sobran son los `GLOBAL`, que
por diseño no llevan celda. Cero deriva.
