# `ACTO MAESTRA36-L14 · COERCITIVO-TRES-UNIVERSOS` — P1 · razones y P2 · tabla para mesa (COMMIT-2)

3/sep/2026 · UBUNTU · `/home/pc0/mm-l14-coercitivo` · base `18fd2bd`.
Comando: `python3 tools/medidor_l14_coercitivo_universos.py --mide --json data/l14-coercitivo-universos-v1_0.json`.

> **«El primer resultado que produzca este procedimiento es el que se reporta.»**
> Lo es. Los tres denominadores, el filtro, el estimador de varianza, la
> corrección de la premisa del numerador y la lista de incompatibilidades con su
> signo quedaron congelados en `COMMIT-1` (`da68109`), antes de correr `--mide`.
> Esta nota no edita `COMMIT-1`.

**Este acto no adjudica.** No evalúa ningún tramo del falsador `B-bis`, no emite
veredicto y no sella. Entrega la tabla; la elección de lectura es de mesa.

---

## P2 · Tabla para mesa — una página

Numerador **único** para las cinco filas: `N = 32 331 680` contribuyentes con
primer certificado de e.firma acumulados `2004-01 → 2025-12` (`firelenumcontri`,
L13/`ADR-312`, re-citado, no recalculado). **`N` es cota superior del stock
vigente**, luego **toda `p` de esta tabla es una cota superior**.

| | denominador | `D` | `IC95` de `D` | **`p`** | `IC95` de `p` | qué incluye | qué excluye | qué confunde |
|---|---|---|---|---|---|---|---|---|
| **A** · poblacional | ENOE, ocupados totales (`clase2==1`, 15+) | **59 785 854** | [59 205 562, 60 366 146] | **0.5408** | [0.5356, 0.5461] | a todo el que trabaja, formal o informal, asalariado o no | a los no ocupados con e.firma (desocupados, PNEA, jubilados, arrendadores) y a las personas morales del numerador | mezcla obligados y no obligados: 55.0 % de los ocupados son informales |
| **B** · padrón amplio *(L13, re-citada)* | SAT, padrón activo `Total` | **87 773 627** | sin `IC` (censo) | **0.3684** | sin `IC` (censo) | a todo el que tiene RFC activo, incluidos 52 673 672 asalariados PF | a quien trabaja sin RFC — el grueso de la informalidad | inflado por los asalariados, que en general **no** están obligados a e.firma |
| **C** · padrón obligado *(L13, re-citada)* | SAT, `Total − Asalariados PF` | **35 099 955** | sin `IC` (censo) | **0.9211** | sin `IC` (censo) | PF con actividad empresarial/profesional + PM + grandes contribuyentes | a los asalariados PF y a todo el que no está en el padrón | numerador acumulado desde 2004 contra padrón de 2025: la cota más floja de las tres |
| *puente* **A′** | ENOE, ocupados **formales** (`emp_ppal==2`) | **26 901 029** | [26 538 706, 27 263 352] | **1.2019** | [1.1859, 1.2183] | al ocupado cuyo empleo principal es formal | a los 32 884 825 informales | **`p > 1`**: el numerador no cabe en este denominador |
| *puente* **A″** | ENOE, formales **no asalariados** (`pos_ocu ∈ {2,3}`) | **3 434 364** | [3 347 667, 3 521 061] | **9.4142** | [9.1824, 9.6580] | empleadores (1 831 506) y cuenta propia formales (1 602 858) | subordinados y remunerados (23 466 665), sin pago, no especificado | **`p ≈ 9.4`**: la aproximación ENOE del «obligado» es dos órdenes demasiado estrecha |

`IC95` por diseño, estimador de conglomerado último con estrato `est_d_tri` y
UPM `upm`; `CV` de `0.5 %` en (A) y `1.3 %` en (A″). El `IC` de `p` se obtiene
invirtiendo el del denominador: el límite inferior de `p` usa el superior de `D`.

> ### Pregunta a mesa
>
> **¿A quién describe `coercitivo`: A, B o C?**
>
> Sin recomendación de dirección. La letra que mesa elija fija la `p` que el
> sucesor `N13 · SELLA-COERCITIVO` sellaría; este acto no la propone.

---

## Lo que los dos puentes miden, que no es un error de cuenta

`A′ = 1.20` y `A″ = 9.41` **no son razones fallidas: son la medición del
desacople**. Una proporción mayor que `1` con numerador y denominador correctos
prueba, por sí sola, que **los universos no son el mismo** — no que la adopción
sea del 120 %. Concretamente:

- Hay **más contribuyentes que alguna vez sacaron e.firma (32.3 M) que ocupados
  con empleo formal (26.9 M)**. Basta eso para descartar la lectura «e.firma ≈
  formalidad laboral».
- La aproximación ENOE del obligado (`A″`, 3.4 M) es **diez veces más chica** que
  la aproximación SAT del obligado (`C`, 35.1 M). Las dos pretenden nombrar al
  mismo conjunto y difieren en un orden de magnitud: **la definición de
  «obligado» es la variable, no una constante que se pueda dar por sabida**. Esto
  es exactamente lo que mesa detectó cuando negó el sello de L13 sobre el padrón.

El puente que el encargo pedía —`A′` como paso entre A y B— **no puentea**: A
(`0.54`) y B (`0.37`) están a menos de un factor 1.5, y A′ los sobrepasa a los
dos cruzando el `1`. Se reporta así, y no se elige un denominador intermedio
distinto para que el puente «funcione»: eso sería escoger la cifra.

## Incompatibilidades de universo, cada una con su signo

Sobre `p_A`. Congeladas en `COMMIT-1`, no derivadas del resultado.

| incompatibilidad | signo | cota |
|---|---|---|
| **Personas morales en el numerador.** `N` cuenta PF **y** PM; el denominador ENOE cuenta personas ocupadas. Cada PM con e.firma suma arriba y no puede sumar abajo. | **+** infla `p_A` | acotable con `PorTipoContribuyente` (~7 % del padrón son PM); **no se resta aquí** porque L13 no separó `N` por tipo de persona |
| **Acumulado ≠ stock vigente.** `N` acumula desde `2004-01` y no da de baja al que caducó o salió del padrón; el denominador es un stock trimestral. | **+** infla `p_A` | no acotada por este acto; es la cota superior que L13 ya declaró |
| **Menores de 15 fuera del denominador.** La ENOE 15ymas no los observa; un menor con e.firma vía representante suma arriba y no abajo. | **+**, magnitud despreciable | — |
| **No ocupados con e.firma.** Desocupados, PNEA, jubilados y arrendadores pueden tenerla y están fuera de **los cuatro** denominadores ENOE (todos exigen `clase2==1`). | **+** infla las cuatro `p` de ENOE | el denominador crecería si se abriera a toda la población de 15 y más; **esa quinta lectura no se mide**: el encargo pide tres |
| **Residentes en el extranjero.** Están en el padrón del SAT y no en el marco muestral de la ENOE (viviendas en territorio nacional). | **+** infla `p_A` | — |
| **Informalidad laboral ≠ ausencia de registro fiscal.** El ocupado informal puede tener RFC y e.firma. | rompe la equivalencia «formal = obligado» | por eso (c) es **aproximación** y no medida; es la razón de que `A″` reviente |
| **Unidad de observación.** El SAT cuenta **contribuyentes**; la ENOE cuenta **personas** por su ocupación **principal** (`emp_ppal` es de la primera actividad). | ambiguo | afecta el reparto entre (b) y (c), no el total (a) |

Todas las acotables apuntan en el **mismo sentido**: `p_A = 0.5408` es cota
superior por partida doble —por el numerador acumulado y por las PM—, y ninguna
incompatibilidad identificada empuja en dirección contraria.

## Contra el `0.09` asignado: sólo orden de magnitud

La escala declarada (A-bis 3) autoriza **una sola** comparación, y es la que se
hace: `p_A = 0.54` está **un orden de magnitud por encima** del `0.09` de
`adopta`, y la lectura poblacional —la que mesa pidió— **no rescata** la regla:
es la más alta de las tres, no la más baja. Ni A ni B ni C caen cerca de `0.09`.
**No se dice «difiere en Z %»** y **no se emite fila de veredicto**.

## Controles de consistencia

- **Partición.** `ocupados − informales − formales = 0` exacto: las 190 187 filas
  del filtro tienen `emp_ppal ∈ {1,2}`, sin residuo. Guardia de `COMMIT-1`, pasa.
- **Discriminación.** `formales_no_asalariados (3 434 364) < formales
  (26 901 029)`: el filtro `pos_ocu` discrimina. Guardia de `COMMIT-1`, pasa.
- **Externo, de pertenencia y no de reproducción.** La tasa de informalidad que
  cae del filtro, `32 884 825 / 59 785 854 = 55.00 %`, y el nivel de ocupación,
  `59.8` millones, son del orden de lo que INEGI publica para 2025. Es un control
  de **orden de magnitud**: este acto **no** reproduce la cifra publicada de
  INEGI ni lo intenta, porque la TIL1 publicada no usa exactamente este filtro.
- **Estratos con una sola UPM.** 11 en (A), 13 en informales, 15 en formales, 104
  en (A″). Aportan `0` a la varianza y **están contados en el JSON**: no se
  colapsan en silencio, y en (A″) son suficientes para que su `IC` se lea como
  ligeramente optimista.

## Contador

**`S1` sigue en `1`**, declarado. Este acto **no** produce la `p` de
`tramite.gobierno_digital.coercitivo`: produce **tres candidatas** y la pregunta
de cuál es. Lo que se mueve es **«lecturas de universo medidas para coercitivo:
2 → 3»**. **Cargas al motor: 0.**

## Lo que esta pieza no hace

No sella. No adjudica ni evalúa tramo. No propone letra. No toca
`milpa/tramite.yaml` ni `milpa/procedencia.yaml`: el prior `0.91`/`0.09`
`ASIGNADO` y el tier `MEDIA-FUERTE` quedan intactos. No amplía
`sin_dato_universo_examinado`. No descarga nada: el payload ENOE ya estaba en el
corpus (`data/manifiesto.yaml`, id `enoe_2025_4t_csv`), verificado por `sha256`.
No mide `2026-1T` — la elección de trimestre fue previa y por razón (`P0`).
