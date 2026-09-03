# P0 · CENSO A.4 · ACTO MAESTRA35-L7 · REGLAS-ACTIVOS-L2

Contra `forense/encargos/2026-09-02-MAESTRA35-L7-REGLAS-ACTIVOS-L2.md`, SHA de
redacción `19770f2`. Base real de este acto: `6c20141` (dos merges por delante
de la redacción — `PR #481` `MAESTRA35-A1` y `PR #482` `MAESTRA35-L5` espejo,
ninguno toca los cuatro ids de esta pieza). Un commit, antes de medir;
denominadores censados sin cruzar contra el desenlace, por regla, con el texto
de la regla verbatim del modelo.

## 0 · Verificación de premisas del encargo, contra el árbol

**A.8(2) reverificado** (no heredado del encargo): `grep -c "id:
civico.denuncia.sin_seguro\|id: familia.union\|id: familia.cuidado\|id:
dinero.ahorro.volatilidad" milpa/tramite.yaml` → `0`; mismo grep sobre
`milpa/tramite-ola5-propuesta-v0.yaml` → `0`. Se sostiene.

**Lo que el encargo NO trae y sí está en el árbol — hallazgo de este censo,
no del encargo.** Tres de las cuatro reglas ya tienen historia en el aparato
de Hito D (`forense/hitoD-preregistro-v2_0.md`, perímetro de 27), que el A.8
del encargo no cruzó (verificó existencia de reactivo/estructura, no el
registro de veredictos archivados). Ninguna de las tres historias **bloquea**
esta pieza — el aparato de Hito D (falsadores A-E, un solo falsador
pre-registrado por regla) y el B-bis/A-bis de este lote (tasas base + ejes,
"asociaciones dentro de una corrida") son pistas distintas y declaradas como
tales en el propio encargo — pero **omitir la cita sería declarar menos de lo
que el árbol sabe** ([[feedback_declare_more_not_less]]), así que se declara
aquí, por regla:

- **R7.2** (pieza a): `D` archivado, `hitoD-R7_2-veredicto-v1_0.md` (4/ago/2026)
  + re-triage `hitoD-R7_2-bbis-triage-v1_0.md` (18/ago, fila `T-2`, confirma
  `D` SOSTENIDO) + `hitoD-R7_2-revision-v1_0.md` (misma fecha, documenta una
  lectura alternativa fila-A no adjudicada). El propio veredicto **ya midió**
  la celda que esta pieza pide (§1 abajo), dos veces, de forma independiente.
- **R1.1** (pieza d): `D` archivado, `hitoD-R1_1-veredicto-v1_0.md`
  (28/jul/2026), **escopado exclusivamente al dominio agrícola** (Fondos de
  Aseguramiento / Seguro Agrícola Catastrófico, productores de temporal). Cita
  textual: *"R1.1 no gana ni pierde información en este dominio. Sale igual
  que entró."* No dice nada de población urbana/nacional — no bloquea la tasa
  base de esta pieza (§4 abajo).
- **R5.2** (pieza c): `A` PROPUESTO, no archivado (`forense/notas/
  2026-08-04-y5-veredicto-r5-2.md` + `...y1-operacionalizacion-r5-2-enut.md`),
  vía ENUT 2024, diseño de **contraste por ocupación** (reducción% de horas de
  cuidado, ocupada-formal-TC vs. no-ocupada, con control de "varón
  disponible"): 23.98%, IC95%=[14.39%,33.57%]. Mide algo distinto de lo que
  pide esta pieza (§3 abajo: reparto de la carga total del hogar, no contraste
  por ocupación) — reusa la MISMA definición de `horas_cuidado`, declarado.
- **R5.3** (pieza b): sin ficha, sin veredicto. Confirmado:
  `find forense -iname "*R5_3*"` → vacío; `grep -rl "R5\.3" forense/notas/` →
  vacío. Territorio abierto, como el encargo supone.

**Ninguna de las tres citas cambia el veredicto A.4 de su pieza** — se
declaran para que quien audite este acto no las redescubra, y para que el
`P1` de cada pieza sepa contra qué está construyendo cuando reutiliza (o
deliberadamente no reutiliza) una definición ya usada.

---

## 1 · Pieza (a) — R7.2 · `civico.denuncia.sin_seguro` / `civico.denuncia.con_seguro`

> **Regla (verbatim, `canon/modelo-decision-v4_0.md:499`, ficha
> `hitoD-preregistro-v2_0.md:179`):** *"SI el delito no tiene cobertura de
> seguro y el agresor es identificable ENTONCES no denuncia — PORQUE miedo +
> inutilidad percibida (denunciar rinde 0.8%); SI es robo de vehículo
> asegurado ENTONCES sí denuncia"* — `[FUERTE]`.

**¿Hay ítem de tenencia de seguro para el delito (robo de vehículo /
vivienda)?** Verificado contra el diccionario de datos de `TMod_Vic`
(`diccionario_de_datos_tmod_vic_envipe2025.csv`, columna `NEMONICO`), filtrando
por `seguro|asegura` en `NOMBRE_CAMPO`: **una sola coincidencia en las 187
filas del diccionario** — `BP2_1` ("Vehículo robado asegurado", `{1,2,9,b}`).
**Vehículo: sí. Vivienda: no** — cero variables de seguro para `BPCOD=04`
(robo casa habitación) ni para ninguna otra de las 15 clases. Verificado por
descriptor, no por nombre corto.

**Denuncia** — `BP1_20` ("Denuncia ante el MP o Fiscalía Estatal"), universo
completo (40 280/40 280, sin blancos), catálogo `{1 Sí, 2 No}`. **Razón**
(pedida por el encargo) — `BP1_23` ("Razón principal de la no denuncia")
también existe, catálogo de 10 códigos, `n=36 040` (universo de quien no
denunció), no se usa en el desenlace de esta pieza (fuera de lo que R7.2
predice: la regla predice SI denuncia, no por qué no).

**Denominador por tipo de delito** (`BPCOD`, 15 clases, `TMod_Vic`, 40 280
filas): `BP2_1` observable **solo** en `BPCOD=01` (robo total de vehículo) —
`1 028` de `40 280` filas (2.6%), verificado empíricamente (`Counter` de
`BP2_1` no-blanco por `BPCOD` da `{'01': 1028, resto: 0}`, reproducido en
`tools/medidor_denuncia_seguro_envipe25.py`). Las 14 clases restantes no son
"no aplica por no respuesta": el instrumento nunca formula la pregunta fuera
de la Sección II del cuestionario (ruteo confirmado en
`hitoD-R7_2-veredicto-v1_0.md §2.2`).

**Lo que ya existe — declarado aquí, no re-derivado por sorpresa en P1.** La
celda que esta pieza necesita (denuncia × cobertura, dentro de `BPCOD=01`) ya
fue medida **dos veces**, de forma independiente (4/ago/2026, la segunda sin
heredar los números de la primera): asegurado 79.1% [74.9,83.3] n=402; no
asegurado 67.2% [63.7,70.7] n=614; brecha 11.9pp IC95%(brecha)=[6.4,17.4]pp
(`hitoD-R7_2-revision-v1_0.md §2.4`). **Reverificado una TERCERA vez, hoy,
desde el CSV crudo** (`tools/medidor_denuncia_seguro_envipe25.py`): reproduce
79.1%/67.2%/11.9pp exacto. **Pendiente de mesa, sin resolver, ajeno a Hito
D**: si esto cierra el `ASIGNADO [0.78, 0.22]` de `civico.denuncia.con_seguro`
(`milpa/procedencia.yaml:806-809`, reverificado hoy — sigue `ASIGNADO`, sin
tocar) — 79.1% queda a 1.1pp de 0.78. Esta pieza no lo adjudica (fuera de
perímetro Hito D **y** fuera de perímetro de este acto, que no toca
`procedencia.yaml`); lo que **sí** aporta, y que Hito D explícitamente declinó
(`hitoD-R7_2-revision-v1_0.md §4`: *"No se toca `milpa/procedencia.yaml`"*),
es aterrizar el número como entrada `PENDIENTE-DE-MESA` en
`milpa/tramite-ola5-propuesta-v0.yaml`, vía el apparatus formal de ejes
(CORROBORADA/NO-DISCRIMINA/CONTRARIA) que ninguno de los dos documentos de
Hito D usaba.

**Guardia de degeneración:** `BP2_1` dentro de `BPCOD=01` no tiene blancos
(`{'2':614,'1':402,'9':12}` exacto, 1028=1028); código `9` se excluye de la
tasa, no se colapsa. No degenerada.

**Veredicto A.4: EXISTE-SATISFACE.** El ítem existe (vehículo, no vivienda —
el encargo preguntaba por ambos y la respuesta real es asimétrica), el
denominador por delito está censado, la celda no es degenerada.

---

## 2 · Pieza (b) — R5.3 · `familia.union.baja_garantia_institucional`

> **Regla (verbatim, `canon/modelo-decision-v4_0.md:537`):** *"SI hay baja
> garantía institucional del matrimonio ENTONCES la unión libre es opción
> racional (no 'unión fallida') — PORQUE evita costos ante baja garantía"* —
> `[MEDIA]`.

Sin ficha Hito D (§0). El disparador "baja garantía institucional" no está
medido en ningún instrumento del corpus — se declara, no se busca; se mide la
tasa base de unión libre con ejes, en DOS instrumentos, no promediados (son
preguntas distintas):

**D1 · EDER 2017** (`eder_2017_eder2017_bases_csv`, tabla `historiavida.csv`,
panel retrospectivo persona-año, 886 976 filas / 23 831 personas). Variable
`edo_civil1` ("Estado civil primera unión", FD `eder2017_fd.pdf`, catálogo de
27 códigos verificado línea por línea contra el PDF, no por nombre corto).
Derivación: primer código no-cero por persona, en orden de `anio_retro`.
`LIBRE = {1,12,13,14,17,18,126}` (inicio de unión libre, y las transiciones
"posterior a Inicio de Unión libre" — código que confirma que la unión SÍ
empezó como libre aunque la fila de inicio exacta esté censurada por el
borde del panel); `DIRECTO = {2,3,4,26,27,28,46,47,48}` (matrimonio civil/
religioso/ambos, inicio o transición). **Verificado: 0 personas tienen como
primer-no-cero un código de disolución pura** (`{6,7,8,60,70,80}`, divorcio/
separación/viudez) — sin censura izquierda que corrija esa clase. Código `37`
(n=2) queda sin clasificar, declarado.

```
personas con primer estado civil no-cero: 18 689 de 23 831 (78.4%)
  unión_libre        9 044  (48.4%)
  matrimonio_directo  9 643  (51.6%)
  sin clasificar (37)    2
```

Diseño y ponderador, join sin huérfanos: `factor_per` (`antecedentes.csv`,
23 831 filas = personas únicas) → 0 huérfanos de 18 689; `est_dis`/`upm`/
`tam_loc` (`vivienda.csv`, a nivel `folioviv`) → 0 huérfanos. Ejes candidatos,
los tres con dato real: cohorte de nacimiento (`anio_nac`, 4 tramos),
escolaridad (`nivel_inst` de `persona.csv`, join 100% exacto, catálogo `00-12`
+ 4 693 blancos declarados — no universales, `NIV` no siempre capturado),
ámbito (`tam_loc`, 4 categorías `{1..4}`, sin inventar corte).

**D2 · ENADID 2023** (`enadid2023_base_datos_csv`, tabla `TSDEM.csv`, 359 018
personas todas edades). `sit_conyugal` (nombre que cita el encargo) **no
existe literalmente** — verificado contra el header (96 columnas): 0
coincidencias. La variable real es `p3_27_ag` ("Situación conyugal
agrupada", FD `fd_enadid23.xlsx` hoja TSDEM): `{1 Soltera(o), 2 Casada(o), 3
En unión libre, 4 Separada/divorciada/viuda}`. Universo 15+: 277 003, sin
blancos: `{1:80 382, 2:100 218, 3:52 732, 4:43 736}` (reverificado hoy desde
el CSV crudo, no heredado). **Elegida como desenlace: condicional a estar
actualmente casada(o) O en unión libre** (código 2 o 3) — la regla compara
las DOS formas institucionales alternativas, no la población general (que
incluye a quien nunca formó pareja); universo condicional = 152 950. La
prevalencia SIN condicionar (34.65% [nota: esto es ya el condicionado — ver
cifra bruta abajo]) se reporta también como cifra de contexto:
**prevalencia bruta sobre 15+ completo = 19.02%** (`w·(p3_27_ag=='3')`,
`fac_viv`). Diseño: `est_dis`/`upm_dis`/`fac_viv`, sin blancos en los 277 003.
Eje: tramos de edad (`tramos_edad`, proxy imperfecto de cohorte — ENADID no
trae año de nacimiento en `TSDEM`, declarado, no corregido).

**Guardia de degeneración:** ninguna de las dos celdas base (EDER: libre/
directo; ENADID: casada/libre) tiene `n` cercano a 0 o al universo completo.
No degenerada en ninguno de los dos instrumentos.

**Veredicto A.4: EXISTE-SATISFACE**, en los dos instrumentos, con
operacionalizaciones distintas y complementarias (retrospectiva de primera
unión vs. prevalencia actual condicional).

---

## 3 · Pieza (c) — R5.2 · `familia.cuidado.recae_mujeres_40mas`

> **Regla (verbatim, `canon/modelo-decision-v4_0.md:536`):** *"SI se trata de
> cuidado (mayores, niños, enfermos) ENTONCES recae sobre mujeres 40+ (hijas/
> nueras) — PORQUE estructura + guion marianista, no 'cultura del cuidado'"*
> — `[FUERTE]`.

`A` propuesto (§0), no archivado, sobre un desenlace de CONTRASTE (reducción%
por ocupación). Esta pieza mide REPARTO: proporción del total de horas de
cuidado del hogar que aportan mujeres 40+.

**ENUT 2019 investigado y NO elegido.** No tiene tabla `tvar_crea` (variables
ya agregadas): las 5 tablas son `THOGAR/TMODULO/TSDEM/TVIVIENDA`. El módulo de
cuidado vive en `TMODULO.csv`, preguntas `6.11` (especiales, 11 sub-ítems) a
`6.15` (60+, 4 sub-ítems), cada sub-ítem con 4 columnas de tiempo (horas/min
× entre-semana/fin-de-semana) — ~40 columnas crudas sin agregar, verificado
contra `enut2019_fd.xlsx` hoja `TModulo` (1 344 filas, filtrado por
`NOMBRE_CAMPO` conteniendo "cuidad"). Reconstruir la bucketización
"CON_CP"/"SIN_CP" (cuidado pasivo/vigilancia, que en 2024 SÍ está pre-validada
por el precedente Y1) desde cero, sin precedente en este repo para 2019, es
exactamente la clase de riesgo definicional que
[[feedback_spec_congelada_puede_salir_degenerada]] documentó — no se intenta
bajo el presupuesto de este acto.

**ENUT 2024 — elegida.** `tvar_crea.csv` (74 053 personas, 29 181 hogares),
variables ya agregadas y validadas por el precedente Y1 (4/ago/2026):
`horas_cuidado = CUID_ESP_INT_HOG_CON_CP + CUID_INT_0A5_CON_CP +
CUID_INT_6A14_CON_CP + CUID_INT_60MAS_CON_CP` — **reusada tal cual, no
redefinida**. Las cuatro columnas, verificadas: 0 nulos, numéricas, rango
`[0, ~280]` horas/semana (valores >168h posibles porque "cuidado pasivo"
puede solaparse con otras actividades declaradas — característica conocida
del instrumento, no defecto de este acto).

**Llave de hogar y diseño, verificados por join:** `LLAVEHOG` (29 181
hogares), `EST_DIS`/`UPM_DIS` **constantes dentro de hogar** (verificado:
`groupby(LLAVEHOG)[...].nunique()==1` para las dos, en el 100% de los
hogares). `FAC_PER` **NO** es constante dentro de hogar (verificado, es
ponderador de persona) — para el estimador de razón a nivel hogar se usa
`FAC_HOG` (`tsdem.csv`, 29 181 hogares únicos, constante dentro de hogar
verificado), traído por join sin huérfanos.

**Censo descriptivo, sin ponderar y sin cruzar contra el desenlace formal aún
(solo para ver que no degenera):**

```
hogares totales: 29 181
hogares con alguna hora de cuidado registrada (total_hogar>0): 17 394 (59.6%)
hogares sin ninguna mujer 40+ (aportan 0 al numerador, no se excluyen): 11 557
share poblacional de mujeres 40+ (12+, ponderado): 26.57%
```

**Guardia de degeneración:** ni el numerador ni el denominador del estimador
de razón son idénticamente cero o constante; 59.6% de hogares con carga>0 es
un universo sano, no un borde.

**Ejes candidatos declarados** (el encargo no pide ejes adicionales para
esta pieza más allá de la proporción y "por sexo × edad"): sexo × 5 tramos de
edad (12-17/18-29/30-39/40-59/60+) para el desenlace descriptivo de horas
promedio — **no** es proporción de un binario, es media ponderada
(`wprop_ic_conglomerado` acepta `d` continuo sin modificación, verificado).

**Veredicto A.4: EXISTE-SATISFACE.** ENUT 2024, `tvar_crea.csv`, sin
degeneración, con las dos piezas del encargo cubiertas (horas por sexo×edad;
proporción del total del hogar).

---

## 4 · Pieza (d) — R1.1 · `dinero.ahorro.volatilidad_horizonte_corto`

> **Regla (verbatim, `canon/modelo-decision-v4_0.md:499`):** *"SI el ingreso
> es volátil/informal (`segsoc`=2 ∨ sin `contrato`/`pres_*`) ENTONCES horizonte
> corto, ahorro informal (tanda, 'guardado en casa'), foco en emergencia —
> PORQUE G3 (volatilidad) + escasez"* — `[FUERTE]`. 🚫 Dominio agrícola
> inejecutable (`hitoD-R1.1`, §0) — no aplica aquí (población nacional/urbana
> vía ENIF).

**`P4_10`** — `enif_2024_bd_csv.zip`, tabla `TMODULO.csv` (misma tabla que
`P3_13`/`P5_1_*`/`P5_6_*`, ya usada por `tools/medidor_ahorro_enif24.py`). FD
(`enif_2024_fd.xlsx`, hoja `TMODULO`, fila 290): pregunta 4.10, *"Si usted
dejará de recibir ingresos, ¿por cuánto tiempo podría cubrir sus gastos con
sus ahorros?"* — catálogo verificado contra el microdato, universo completo
**sin gate** (13 502/13 502, cero blancos):

```
1  Menos de una semana / No tiene ahorros     4 275
2  Al menos una semana, menos de un mes       2 443
3  Al menos un mes, menos de tres meses       3 405
4  Al menos tres meses, menos de seis meses   1 328
5  Seis meses o más                           1 479
8  No responde                                   74
9  No sabe                                      498
```

⚠️ **Nota de medición, declarada antes de dicotomizar:** el código `1` funde
"menos de una semana" con "no tiene ahorros" — no son lo mismo, pero el
instrumento no los separa. Para el mecanismo que la regla predice (horizonte
corto **y** ahorro informal como conductas emparejadas) la fusión no es un
defecto: quien no tiene ahorros tiene, por definición, horizonte cero.

**Universo de `P3_13`** (seguridad social, ya usado por `MAESTRA35-L1`):
válidos `1-7` = 9 312 de 13 502 = **68.9676%** — reverificado desde el CSV
crudo, coincide con la cifra que `L1` ya declaró. El resto es blanco
estructural (`NaN`, no código "no aplica"), consistente con que la sección 3
solo se pregunta a quien trabaja.

**Intersección triple** (ahorro-elegible ∧ `P3_13` válido ∧ `P4_10` válido):
**n = 9 031** de 13 502 (66.9%). Cross-tabs preliminares (`P4_10` × seg.
social) sin ninguna celda cercana a 0: la más chica tiene `n≈483`.

**Ahorro informal exclusivo** — reutiliza, sin redefinir,
`ahorra_solo_informal` de `tools/medidor_ahorro_enif24.py::desenlaces()`
(`P5_1_1..6` informal `&` `~P5_6_1..9` formal).

**Guardia de degeneración:** `P4_10` sin gate, seis códigos sustantivos +
2 de no-respuesta, ninguna celda cercana a 0 o al universo completo. No
degenerada.

**Veredicto A.4: EXISTE-SATISFACE.** Desenlace primario "horizonte corto"
(`P4_10='1'`, lectura literal, sensibilidad declarada `P4_10∈{1,2}`) cruzado
por seguridad social (`P3_13`, 2 celdas, universo restringido 68.97% ya
declarado A-bis 4 por `L1`), y como segundo desenlace del mismo cruce,
`ahorra_solo_informal` reutilizada de `L1` — el compuesto SI-ENTONCES de la
regla predice ambos.

---

## 5 · Veredictos A.4 — resumen

| Pieza | Regla | Fuente | Veredicto A.4 |
|---|---|---|---|
| (a) | `civico.denuncia.sin_seguro`/`con_seguro` (R7.2) | ENVIPE 2025, `TMod_Vic` | **EXISTE-SATISFACE** |
| (b) | `familia.union.baja_garantia_institucional` (R5.3) | EDER 2017 + ENADID 2023 | **EXISTE-SATISFACE** |
| (c) | `familia.cuidado.recae_mujeres_40mas` (R5.2) | ENUT 2024, `tvar_crea.csv` | **EXISTE-SATISFACE** |
| (d) | `dinero.ahorro.volatilidad_horizonte_corto` (R1.1) | ENIF 2024, `TMODULO.csv` | **EXISTE-SATISFACE** |

Las cuatro piezas EXISTE-SATISFACE. El lote continúa completo a `COMMIT-1`
(spec congelada).
