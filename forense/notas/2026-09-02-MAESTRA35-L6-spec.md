# `ACTO MAESTRA35-L6 · FUENTE-COERCITIVO-Y-PUENTE` — `COMMIT-1` · spec congelada

**2 de septiembre de 2026.** Este archivo es el **commit 1** del patrón de dos
commits (Bloque B-bis / A-bis, `v2.4`). Se escribe **después** del censo `P0`
(`forense/notas/2026-09-02-MAESTRA35-L6-P0-censo.md`) y **antes** de calcular
ninguna de las dos cantidades de abajo. **No se corrige hacia atrás**: si la
spec resulta equivocada, se escribe un tercer commit que lo diga.

---

## §0 · Premisas, y de dónde sale que estas dos piezas se midan

El censo `P0` cerró con **`0` `EXISTE-SATISFACE` de `7` piezas sobre las `4`
candidatas** del encargo. Ninguna `p` de las dos reglas `ASIGNADO` del encargo
—`tramite.gobierno_digital.coercitivo` y el bullet
`dinero.ahorro.informal_sin_puente` + `con_puente_y_respaldo`— es estimable con
el corpus de hoy, y las razones están escritas y refutadas adversarialmente en
`P0` §3, §4, §5 y §6.

Lo que sí quedó habilitado, y es lo que esta spec congela:

- **`P1` · ENDUTIH.** La **adopción nacional de trámites de gobierno por
  internet** (`P7_35_4`), sobre universo limpio. **No es** la `p` de
  `coercitivo`. Es la cifra que la `estampa A.10` de la regla **espejo**
  `tramite.gobierno_digital.util_sin_coercion` declara expresamente no haber
  medido — verbatim de `milpa/tramite.yaml`: *«No es la adopción de gobierno
  digital en México»*.
- **`P2` · ENIF 2024.** La mitad **`respaldo`** del bullet de puente
  (`P4_9_4`), cruzada contra la tenencia de producto formal. La mitad **canal
  personal** es inobservable fuera del universo de adoptantes (`P0` §6.2) y no
  se mide.

**Declaración de alcance.** `P1` **excede la letra del encargo**, que
condicionaba la medición de `P1` a que la pieza (a) satisficiera, y no
satisfizo. Se ejecuta bajo la instrucción de mesa del 2/sep/2026 («censo y
medición en el mismo acto») y la regla de señal `v2.3`, se marca
`PENDIENTE-DE-MESA` y **la adjudica mesa, no el ejecutor**. `P2` está **dentro**
del encargo: su pieza (d) pedía explícitamente ítems «sobre RESPALDO (¿alguien
responde por mí?)».

## §0.1 · Contaminación declarada (`ADR-46`)

Lo que esta sesión ya vio, antes de congelar, y que por tanto **no** puede
reclamar como pre-registro ciego:

- **`P1` NO ES CIEGO en magnitud.** El censo `P0` contó, para poder declarar
  denominadores, la distribución **cruda y sin ponderar** de `P7_35_4`:
  **2023** `8 062` Sí / `38 569` No sobre `46 631`; **2025** `9 221` / `39 497`
  sobre `48 718`. La sesión conoce, pues, el orden de magnitud (~17-19 %). Lo
  que **no** se ha calculado ni visto es la proporción **ponderada**, su `IC95`,
  ni ninguna de las dos sensibilidades. Se declara porque declararlo cuesta menos
  que descubrirlo después.
- **`P2` SÍ ES CIEGO en la cantidad de interés.** El censo contó las marginales
  por separado —`P4_9_4`: `3 145` Sí / `10 357` No sobre `13 502`— y **nunca las
  cruzó** contra ninguna variable de tenencia. El cruce `P4_9_4 × tenencia`, que
  es la cantidad que el falsador de `§2` juzga, **no existe todavía**.
- Estructura leída (contamina parcialmente y se declara): los `FD` de ENDUTIH
  2023/2024/2025, el cuestionario y el `FD` de ENIF 2024, `data/manifiesto.yaml`,
  `data/diseno-muestral.yaml`, `forense/ficha-r34-condBC-v1_0.md` y
  `tools/medidor_ahorro_enif24.py`.

---

## §1 · `P1` — adopción de trámites de gobierno por internet (ENDUTIH)

**Script**: `tools/medidor_gobierno_digital_endutih.py` (**nuevo**; no se edita
ningún `tools/medidor_*` existente).

| campo | valor congelado |
|---|---|
| **Fuente principal** | ENDUTIH **2025** (ola más reciente) |
| **Sensibilidad de ola** | ENDUTIH **2024** y **2023** |
| **Payload** | `data/raw/endutih2025/endutih2025_bd_dbf.zip::ti25usu.dbf` · 2024: `endutih2024_bd_dbf.zip::tic_2024_usuarios.DBF` · 2023: `endutih2023_bd_dbf.zip::tic_2023_usuarios.DBF` |
| **Lector** | `tests/dbfmini.py::read_dbf` (Python puro, latin-1). Los miembros de 2025 se llaman `ti25*.dbf`, **no** `tic_2025_*.DBF` como en 2023/2024 — verificado, no inferido. |
| **Unidad** | persona usuaria elegida (una por hogar) |
| **Universo** | `P7_1 == '1'` (usó internet en los últimos tres meses). Fuera: `P7_1 == '2'` y blancos. |
| **Desenlace** | `adopta = 1` sse `P7_35_4 == '1'`; `adopta = 0` sse `P7_35_4 == '2'`. Cualquier otro valor (blanco incluido) queda **fuera del denominador**. |
| **Ponderador** | `FAC_PER` (tabla usuarios). **No** `FAC_HOGAR` ni `FAC_HOG` ni `FAC_VIV`: son cuatro pesos distintos y no son intercambiables (`data/diseno-muestral.yaml:592-596`). |
| **Diseño** | estrato `EST_DIS` × UPM `UPM_DIS`. **No** `ESTRATO` (socioeconómico) ni `UPM` (llave). Los tres nombres verificados en la cabecera de los tres `DBF`. |
| **Estimador** | `wprop_ic_conglomerado` de `tools/calibracion_mordida_encig_serie.py:81`, importado, **no reimplementado**. `n_boot = 10000`, `seed = 42`. |
| **Escala** | proporción de **personas usuarias de internet de 6 años y más**, ponderada. **No** es proporción de la población total, **no** es proporción de trámites, y **no** es la `p` de ninguna regla `ASIGNADO`. |

**Sensibilidades pre-declaradas** (congeladas aquí, elegidas antes de ver
cualquier resultado, no después):

- **`A` · desenlace ampliado.** `adopta_A = 1` sse alguno de
  `P7_35_1..P7_35_4 == '1'` (cualquier interacción con gobierno por internet:
  comunicarse, consultar, descargar formatos, tramitar), `0` sse los cuatro
  valen `'2'`. Mide si el resultado depende de haber exigido *trámite* y no
  *interacción*.
- **`B` · universo ampliado.** Todas las filas de la tabla usuarios, contando a
  los no usuarios de internet (`P7_1 == '2'`) como **no adopción**. Mide la
  adopción sobre la población de informantes, no sobre los conectados.

**Guardias que PARAN** (`exit 1`, con el defecto a la vista, en vez de producir
un número silenciosamente):

1. Si falta cualquiera de `P7_1`, `P7_35_1..4`, `FAC_PER`, `EST_DIS`, `UPM_DIS`
   en el `DBF`.
2. Si `FAC_PER` no es numérico positivo en toda fila del universo.
3. Si el universo de `P7_35_4` **no coincide exacto** con `P7_1 == '1'`. *(Esta
   guardia es la premisa ajena escrita como guardia, no como supuesto heredado:
   el censo la midió en 2023 y 2025, pero no en 2024, y si en alguna ola el
   salto es distinto el script lo dice en vez de promediar sobre un universo que
   no es el declarado.)*
4. Si el número de estratos o de UPM colapsa a menos de 100 en cualquier ola.

**Pre-registro `B-bis`: esta pieza NO tiene falsador, y se dice.** No contrasta
ningún prior. El `0.71` `ASIGNADO` de `util_sin_coercion` y su `0.673393`
`MEDIDO` pertenecen a un universo **construido distinto** —trámites `N_TRA=01`
(pago del recibo de luz) de ENCIG 2025, unidad *trámite*, no persona—, y
compararlos con esta cifra sería el error de unidad contra el que
`forense/ficha-r34-condBC-v1_0.md` ya advirtió en otro caso. Es una **tasa base
descriptiva** que llena una reserva declarada del propio motor. **Si mesa quiere
leerla contra el prior, la lectura es de mesa.**

---

## §2 · `P2` — respaldo personal × adopción de producto formal (ENIF 2024)

**Script**: `tools/medidor_puente_enif24.py` (**nuevo**).

| campo | valor congelado |
|---|---|
| **Fuente** | ENIF **2024** |
| **Payload** | `data/raw/enif_2024_bd_csv.zip::TMODULO.csv`, `latin-1` |
| **Unidad** | persona elegida de 18 años y más |
| **Universo** | las `13 502` filas de `TMODULO` (`EDAD_V` 18-98, sin faltantes). **Sin gate**: es la razón por la que esta pieza es medible y `P5_15_2` no. |
| **Eje (situación)** | `respaldo = 1` sse `P4_9_4 == '1'`; `respaldo = 0` sse `P4_9_4 == '2'`. Cualquier otro valor queda fuera. `P4_9_4` = *«4.9 Si el día de hoy se le presentara la oportunidad de comprar una casa, un terreno o abrir un negocio, ¿usted podría aprovecharla… con el préstamo de familiares o amistades?»* |
| **Ponderador** | `FAC_PER` · **Diseño** `EST_DIS` × `UPM_DIS` (nombres verificados en la cabecera real del `CSV`; `data/diseno-muestral.yaml:194-199` los escribe en minúsculas, el microdato los trae en **mayúsculas**) |
| **Estimador** | el mismo `wprop_ic_conglomerado`, `n_boot = 10000`, `seed = 42` |
| **Escala** | proporción de **personas de 18+**, ponderada, dentro de cada celda del eje |

**Desenlaces, los tres congelados aquí, con el principal declarado:**

- **`D1` · PRINCIPAL — ahorro formal.** `1` sse alguno de `P5_6_1..P5_6_9 == '1'`.
  Es el desenlace que el bullet nombra (*«sube la adopción»* de un **producto
  financiero**) y el mismo que `tools/medidor_ahorro_enif24.py` usa para la pata
  formal de `dinero.ahorro.tiene_ahorros`.
- **`D2` · tenencia de cuenta.** `1` sse alguno de `P5_4_1..P5_4_9 == '1'`.
- **`D3` · tenencia de crédito formal.** `1` sse alguno de `P6_2_1..P6_2_9 == '1'`.

**Sensibilidad `C` · control de riqueza declarada, pre-registrada.** Repetir el
contraste de `D1` **dentro de cada estrato** de `P4_9_1` (*«¿podría aprovecharla
con sus ahorros?»*). Existe para atacar la lectura obvia —que el respaldo solo
esté midiendo tener familia con dinero—: si la brecha por `respaldo` sobrevive
en las dos celdas de `P4_9_1`, la lectura de riqueza pura no la explica; si
desaparece, se reporta que desaparece. **No se usa `P4_9_2`** («solicitando un
crédito a un banco»), que está anidado en el desenlace.

**Pre-registro `B-bis` — el falsador, escrito antes de ver el número:**

La regla predice que **con puente y respaldo la adopción es MAYOR** que sin
ellos (`0.52 / 0.33 / 0.15` frente a `0.74 / 0.21 / 0.05`). Contra `D1`:

| veredicto | condición |
|---|---|
| **CORROBORADA** | `p(D1 \| respaldo=1) > p(D1 \| respaldo=0)`, con los dos `IC95` **sin traslape** |
| **CONTRARIA** | el orden se invierte, con los dos `IC95` **sin traslape** |
| **NO-DISCRIMINA** | los dos `IC95` se traslapan |
| **ACOTADA** | el signo se sostiene en `D1` pero se rompe o no discrimina en `D2` y `D3` |

**Precedencia: `CONTRARIA` manda.** Si `D1` sale `CONTRARIA`, ese es el
veredicto del acto aunque `D2` y `D3` salgan en el signo esperado.

**Límite declarado antes de medir, no después.** Esto es **asociación dentro de
una corrida** (A-bis 1/2), no efecto. `P4_9_4` mide **respaldo declarado como
disponible**, no respaldo ejercido ni puente de canal; y el bullet exige
`puente ∧ respaldo`, de los cuales esta pieza mide **uno**. Por eso el veredicto
de `§2`, cualquiera que salga, **no cierra la regla**: la acota. Se registra en
la propuesta como `PENDIENTE-DE-MESA`, sin cargar al motor.

---

## §3 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**
