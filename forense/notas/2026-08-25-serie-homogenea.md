# `ACTO SERIE-HOMOGENEA-CODI` — nota de cierre

**Fecha:** 25/ago/2026 · **Entorno:** UBUNTU · **SHA de arranque:** `7f26983` (tip de `ACTO PURGA-EJECUTA`, que a
su vez fusiona `origin/main` `14a7b42`) · **Fila ejecutada:** `FP-142` · **Fila actualizada:** `FP-104`.

**ARRANQUE (A.2, tres partes).** `sin_variable`: entorno sin variable de clave de proveedor. Sonda de red:
`curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → **200**. Corpus:
`ls data/raw/ | head -1` → `2005trim1_csv.zip`, **321** entradas — montado, no hay PARO.

---

## 1 · Qué pedía la fila y qué se encontró

`FP-142` (firmada por mesa el 25/ago, `L3`/`FP-129` opción `b`) pide **localizar en los Informes Banxico ya
adquiridos** una serie que reporte **el mismo constructo, en la misma unidad, para los dos servicios**, para sacar
la condición A de `R3.4` del cruce `cuentas` (CoDi) × `personas físicas` (SPEI) que `A-bis` regla 3 prohíbe.

**Veredicto: `EXISTE-SATISFACE`.** La serie existe, está en el corpus desde el 6/ago, y es
**número de operaciones**.

### 1.1 · La premisa del encargo no reproduce, en dos puntos

| lo que dice el encargo | lo medido | efecto |
|---|---|---|
| lo que falta es «**cuentas SPEI** o **personas CoDi**» | las dos son `NO-ENCONTRADO`; existe una tercera unidad que el encargo no enumera, `operaciones ↔ operaciones` | la enumeración **se queda corta**, no es falsa: `FP-142` no fija cuál unidad |
| «**22 payloads**» de `EXPLORA-2` | **20** en el directorio y **20** en `data/manifiesto.yaml` | el «22» era el `22/22 COINCIDE+ÍNTEGRO` de las cinco olas de **ENIF**, otra cosa |

---

## 2 · Universo del barrido (A.4) y prueba de que los comandos corrieron (A.13)

Seis Informes Anuales IdMF (2019-2024), **547 páginas**, volcados con **doble extractor** —
`pdftotext -layout` y `pypdf` 6.16.1— a **12** archivos de texto paginado. Los cuatro candidatos de constructo y
sus veredictos están en la enmienda `§10.2` de la ficha; aquí van los negativos con su control positivo, corridos
con `command grep` porque el `grep` de esta caja envuelve `ugrep -I` y descarta no-UTF8 en silencio:

- **personas del lado CoDi** → **5** líneas en 12 archivos, **las 5 prosa**, ninguna serie. Control positivo
  (`personas` a secas, mismos 12 archivos): 7 · 22 · 19 · 34 · 43 · 53 líneas.
- **cuentas del lado SPEI** → **13** líneas, **las 13 prosa**. Control positivo (`cuenta`): 38 · 72 · 57 · 53 ·
  45 · 37 líneas.
- **`CF884` (operaciones CoDi) no es alternativa**: **4** fechas distintas en todo el HTML (25-27/jul/2026 y
  30/sep/2019). Confirma la limitación 2 del §7 de la ficha por medición propia.

**Un negativo que resultó ser un defecto de mi detector y NO se declaró como ausencia.** El primer barrido reportó
«Cuadro A 1 ausente» en los informes 2019/2020/2021. Falso: la tabla está ahí (p51, p110, p91). Lo que no está es
la **fila `Total`** — `command grep` de filas que empiezan por `Total` en esas tres páginas devuelve **0**, y el
mismo comando sobre 2022/2023/2024 devuelve **4** por página (control positivo). El `Total` de operaciones de SPEI
**nace en la edición 2022**. El detector se corrigió antes de escribir nada; queda registrado porque un cero de un
comando roto no es un `NO-ENCONTRADO`, que es justo lo que A.13 existe para impedir.

---

## 3 · La serie, y el control que la valida

El **Informe Anual IdMF 2023** trae los dos lados con el **rótulo literal idéntico**, en el mismo apéndice:
Cuadro A 1 (SPEI, p. física 67 / impresa 57) y Cuadro A 8 (CoDi, p. física 72 / impresa 62), los dos
**«Número de operaciones (millones)»**. No hay ni prefijo que convertir.

**Control de reconciliación entre ediciones.** SPEI 2021/2022/2023 sale **idéntico** en las tres ediciones que lo
publican; CoDi reconcilia entre la edición en millones y la de 2024 en miles hasta el redondeo
(`2.453`↔`2 453.4` · `3.008`↔`3 008.0` · `4.017`↔`4 016.7`). Y los **dos extractores coinciden cifra por cifra** en
las seis series localizadas.

---

## 4 · La corrida, íntegra

```
==============================================================================
PASO 1 · localizacion, universo 6 informes, doble extractor
==============================================================================
informe 2019 ·  60 pags · SPEI«SPEI» pdftotext=[51] pypdf=[51] · CoDi pdftotext=[] pypdf=[]
informe 2020 · 119 pags · SPEI«SPEI» pdftotext=[110] pypdf=[110] · CoDi pdftotext=[] pypdf=[]
informe 2021 · 100 pags · SPEI«SPEI» pdftotext=[91] pypdf=[91] · CoDi pdftotext=[] pypdf=[]
informe 2022 ·  79 pags · SPEI«SPEI» pdftotext=[65] pypdf=[65] · CoDi pdftotext=[69] pypdf=[69]
informe 2023 ·  80 pags · SPEI«SPEI» pdftotext=[67] pypdf=[67] · CoDi pdftotext=[72] pypdf=[72]
informe 2024 ·  96 pags · SPEI«SPEI» pdftotext=[83] pypdf=[83] · CoDi pdftotext=[86] pypdf=[86]

==============================================================================
PASO 2 · extraccion de la serie homogenea «numero de operaciones»
==============================================================================
SPEI · informe 2019 p51 · tabla presente pero fila Total/cabecera no parseable (fila=no/no, cabecera=si) — NO se declara ausencia
CoDi · informe 2019 · titulo NO presente en ninguno de los dos extractores
SPEI · informe 2020 p110 · tabla presente pero fila Total/cabecera no parseable (fila=no/no, cabecera=si) — NO se declara ausencia
CoDi · informe 2020 · titulo NO presente en ninguno de los dos extractores
SPEI · informe 2021 p91 · tabla presente pero fila Total/cabecera no parseable (fila=no/no, cabecera=si) — NO se declara ausencia
CoDi · informe 2021 · titulo NO presente en ninguno de los dos extractores
SPEI · informe 2022 p65 · extractores COINCIDEN · 10 anios / 10 cifras
CoDi · informe 2022 p69 · extractores COINCIDEN · unidad=millones · anios cabecera=['2020', '2021', '2022'] · cifras=15
SPEI · informe 2023 p67 · extractores COINCIDEN · 10 anios / 10 cifras
CoDi · informe 2023 p72 · extractores COINCIDEN · unidad=millones · anios cabecera=['2020', '2021', '2022', '2023'] · cifras=16
SPEI · informe 2024 p83 · extractores COINCIDEN · 10 anios / 10 cifras
CoDi · informe 2024 p86 · extractores COINCIDEN · unidad=miles · anios cabecera=['2021', '2022', '2023', '2024'] · cifras=16

==============================================================================
PASO 3 · serie reconciliada (millones de operaciones) y razon CoDi/SPEI
==============================================================================
anio     CoDi (mill op)   SPEI (mill op)   razon CoDi/SPEI  vs umbral A<10%
2020             1.0120           1226.1          0.08254%     A SATISFECHA
2021             2.4534           1991.7          0.12318%     A SATISFECHA  ⚠ ediciones discrepan
       CoDi por edicion: {'codi_2022': 2.453, 'codi_2023': 2.453, 'codi_2024': 2.4534000000000002} · SPEI por edicion: {'spei_2022': 1991.7, 'spei_2023': 1991.7, 'spei_2024': 1991.7}
2022             3.0080           2787.0          0.10793%     A SATISFECHA
2023             4.0170           3823.0          0.10507%     A SATISFECHA  ⚠ ediciones discrepan
       CoDi por edicion: {'codi_2023': 4.017, 'codi_2024': 4.0167} · SPEI por edicion: {'spei_2023': 3823.0, 'spei_2024': 3823.0}
2024             4.1642           5336.6          0.07803%     A SATISFECHA

Umbral: A < 10 % (ADR-37, ASIGNADO no medido, emisor.py UMBRAL_A_RAZON = 0.10).

==============================================================================
PASO 4 · reserva 1 de §10.6 — contencion: el Cuadro A 1 INCLUYE las
          transferencias de CoDi (nota 1/). Razon parte/todo vs. razon excluyente.
==============================================================================
anio      razon cruda   razon CoDi/(SPEI-CoDi)   delta (pp)  cambia de lado?
2020         0.08254%                 0.08261%     0.000068               no
2021         0.12318%                 0.12333%     0.000152               no
2022         0.10793%                 0.10805%     0.000117               no
2023         0.10507%                 0.10519%     0.000111               no
2024         0.07803%                 0.07809%     0.000061               no

==============================================================================
PASO 5 · segundo constructo homogeneo (monto, pesos constantes) — robustez
==============================================================================
anio         CoDi         SPEI        razon   fuente
2022       2.5600     184504.0     0.00139%   Inf.2022 p65/55 (SPEI) y p69/59 (CoDi)
2023       3.9900     197629.0     0.00202%   Inf.2023 p67/57 (SPEI) y p72/62 (CoDi)
2024       4.5037     218925.0     0.00206%   Inf.2024 p83/73 (SPEI) y p86/76 (CoDi)

==============================================================================
VEREDICTO PROPUESTO — condicion A re-especificada de R3.4
==============================================================================
Escala del §5 leida con la clausula sustituida del §10.7 (razon computada sobre
unidad homogenea, sin enlace):  fila A1 en los CINCO anios de la serie y en los
TRES del constructo de monto.  A SATISFECHA — propuesta, no sellada.
La reserva de contencion no cambia el lado del umbral en ningun anio.
Sin intervalo de confianza: por A-bis contraparte, no adjudica solo; adjudica mesa.
```

---

## 5 · Hallazgo sustantivo que la ficha no tenía — **CoDi está DENTRO de SPEI**

La nota `1/` del Cuadro A 1 dice, verbatim: *«En usuarios finales se incluye las operaciones tercero a tercero,
**las transferencias de CoDi** y la nómina de Banco de México…»*. Los dos extractores la devuelven igual.

Consecuencia: la razón `CoDi / SPEI` es **parte sobre todo**, no tratado contra comparador. La ficha nunca pudo
verlo porque su par cruzaba `cuentas` contra `personas físicas` — dos universos que no se contienen. Al pasar a
`operaciones`, la contención sale a la luz.

**Medido, no argumentado:** la variante excluyente `CoDi / (SPEI − CoDi)` mueve la razón entre **0.00006** y
**0.00015 puntos porcentuales**, y **no cambia de lado del umbral en ninguno de los cinco años**. La reserva es
real y queda escrita; el veredicto no depende de ella.

Esto **no** se registró en `forense/hallazgos.md`: ese archivo **no está en el perímetro** de este acto. Queda en
esta nota y en el ADR, y se nombra aquí para que quien abra el perímetro adecuado lo suba.

---

## 6 · Veredicto propuesto y qué NO hace este acto

**Condición A re-especificada de `R3.4`: fila `A1` — A satisfecha. PROPUESTA, no sellada.** La razón
`CoDi / SPEI` en operaciones va de **0.078 %** a **0.123 %** según el año, dos órdenes de magnitud por debajo del
umbral `A < 10 %`; el constructo de robustez (monto) da **0.0014 %-0.0021 %**. Cinco años de cinco, más tres de
tres.

Lo que **no** hace este acto, declarado:

- **No sella.** Sin intervalo de confianza, la contraparte de `A-bis` obliga a subirlo como propuesta.
- **No cierra `R3.4`.** El gate de `ADR-37` exige **A y B y C**; B y C siguen sin base medida (estampa del emisor,
  0 de 2, ambos `ASIGNADO`). `R3.4` sigue **sin veredicto** y el contador del Hito D **no se mueve**: sigue en
  **13 de 27**{cita-historica}, y el «19 de 27» que el encargo nombra es lo que este acto **arma**, no lo que
  entrega.
  *(Enmienda in situ, 25/ago/2026, `ACTO SELLA-G`.)* El contador vigente cuando este acto se fusionó era **18 de
  27**{cita-historica} (`canon/estado-programa-v1_10.md:279`, `ACTO ADQ-CORRE-R74R75`, 24/ago/2026) — **13**
  era ya la cifra histórica que este archivo cita, no el contador en vivo del árbol. Este acto **no mueve** el
  contador: se limita a dejar escrito, con fecha, cuál era el número real al momento de fusionar, para que nadie
  lea «13 de 27» de este archivo como si fuera la cifra de hoy.
- **No retira el confusor de antigüedad** (§2 de la ficha): quince años de mercado separan a los dos lados y
  ninguna lectura atribuye la brecha entera a `utilidad_marginal_sobre_sustituto`.
- **No adopta** las dos lecturas viejas —**0.35 %**{cita-historica} y **12.7 %**{cita-historica}—, ni como
  confirmación ni como contraste.
- **No toca** `milpa/` ni el preregistro, como el encargo ordena.
- **No adquiere** nada: los 20 payloads ya estaban en el corpus desde el 6/ago.

## 7 · Fila `A3`, y la sustitución que hay que firmar

`A3` («par bien formado, enlace de escala sin firmar») **deja de aplicar**: bajo la opción `b` de `L3` no hay
enlace que firmar, porque mesa retiró esa vía entera. Pero `A1`/`A2` están redactadas *«con enlace firmado»*, así
que su condición literal tampoco encaja. La enmienda `§10.7` propone sustituirla por *«razón computada sobre
unidad homogénea, sin enlace»*. **Esa sustitución es lo que falta firmar.** Si mesa la rechaza, el par vuelve a
`A3` y `FP-104` sigue abierta exactamente donde estaba.

## 8 · Dos commits, en el orden que el encargo exige

1. `a23fda6` — **enmienda-spec**, congelada antes de correr: constructo, unidad, ancla, ventana y las cinco
   reservas. La cláusula de cierre del §8 («el primer resultado que produzca este procedimiento es el que se
   reporta») se aplica a la re-corrida, y el §10 declara por adelantado su propio límite honesto: el barrido que
   localiza la serie ve las magnitudes porque viven en la misma celda que el rótulo, así que lo congelado es el
   **procedimiento**, no la ignorancia del número.
2. este commit — **la corrida** y el veredicto propuesto. Primer resultado, reportado.
