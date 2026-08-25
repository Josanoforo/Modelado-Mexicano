# `ACTO INDICE-NO-INEGI` — nota de cierre

**Fecha:** 25/ago/2026 · **Entorno:** UBUNTU · **SHA de arranque:** `f1ed541` (tip de `ACTO GEMELAS-20`) ·
**Fila ejecutada:** `FP-146` (`L10`-`a`).

**ARRANQUE (A.2, tres partes).** `sin_variable` · sonda INEGI **200** · `ls data/raw/ | head -1` →
`2005trim1_csv.zip`, **321** entradas.

---

## 1 · El filtro (i), completo: **0 filas sin evaluar**

`FP-93`/`BIBLIOTECARIO-56` dejó **8** filas en `PENDIENTE-FUERA-DE-INDICE` porque sus publicadores no son INEGI y
los dos índices del diseño de dos pasos son 100 % INEGI. Este acto construye el **paso 1 con los índices de sus
propios publicadores** y corre el **paso 2 idéntico** al de `FP-93`. Resultado: **5 SI · 3 NO · 0 pendientes**.

## 2 · Paso 1 — universo declarado por índice

| publicador | host | ruta | entradas |
|---|---|---|---|
| **Banxico** (ECF) | `www.banxico.org.mx` | `/publicaciones-y-prensa/encuesta-de-competencias-financieras-de-la-poblaci/` | **10** (5 años × texto completo + presentación ejecutiva), **545 páginas** |
| **CNBV** | `portafolioinfo.cnbv.gob.mx` | `/` · `/PUBLICACIONES/` · `/PUBLICACIONES/Cartera/` | **297 + 48 + 48** enlaces |
| **BMV** | `www.bmv.com.mx` | `/es/emisoras/informacion-de-emisoras` | **187** enlaces (137 774 B) |
| **HR Ratings** | `www.hrratings.com` | `/` + `/analysis/` | **131** enlaces (79 049 B) |

El índice de Banxico se enumeró **entrada por entrada** desde `competencias-financieras-en.html`, extrayendo los
10 `GUID` y descargando los 10 PDF; el mapeo `GUID → año` se derivó abriendo cada uno, no del orden de la página.

**Control de que el aserto de `FP-134` era cierto — y no dado por bueno.** La ECF **no** está en INEGI:
`/programas/encf/2018`, `/2021` y `/2024` devuelven los tres **el mismo cuerpo de 13 370 B**, título
*«Página no encontrada»*, **byte a byte idéntico** (`md5 30cc2fe6b2d14cab5f95a4071b70d050`) al que devuelve un
programa **inventado**. Control positivo: `/programas/enif/2021/` devuelve **3 348 B** distintos. El `200` de
INEGI es un soft-404, y aquí se prueba por comparación, no por confianza.

**Nota de acceso — un obstáculo nuevo, diagnosticado y resuelto sin bajar la guardia.** `www.cnbv.gob.mx`
**no sirve su certificado intermedio** (`GlobalSign RSA OV SSL CA 2018`): toda petición muere con
`Verify return code: 21 (unable to verify the first certificate)`, **reproducido también fuera del sandbox** —
es un defecto del servidor, no un bloqueo de red ni un WAF. Se resolvió **anexando el intermedio público**, que
encadena a `GlobalSign Root CA - R3` del bundle del sistema: verificación **completa**, sin `--insecure`.

## 3 · Paso 2 — doble extractor, cita por celda

| id | ola | reactivo | veredicto | dónde |
|---|---|---|---|---|
| **DIN-07** | 2019 | `SF2` presupuesto | **SI** | Informe *2019 y 2020*, bloque `Resultados 2019`, anexo **AMAI**, pág. impresa 50 — columna **NSE D y E = 52.8 %** |
| **DIN-08** | 2019 | `SF7` puntualidad de pago | **SI** | mismo informe, anexo **edad del jefe del hogar**, pág. impresa 55 — **De 18 a 25 años**, renglón *Servicios crediticios*: 33.4 / 2.6 / 1.8 / 0.6 / 2.1 (+ 59.5 sin servicio) |
| **DIN-09** | 2021 | `SF5` pagos de servicios básicos | **SI** | Informe *2021*, **Gráfica 2**, pág. impresa 9, serie `Encuesta 2021`: 48.1 / 24.2 / 8.1 / 13.1 / 6.1 |
| **DIN-10** | 2021 | `SF13` deudas del hogar | **SI** | Informe *2021*, bloque `Resultados 2021`, anexo **género del jefe del hogar**, pág. física 115 — **Jefa mujer**: 40.4 / 12.9 / 6.1 / 40 |
| **DIN-12** | 2021 | `SF10e` pidieron prestado | **SI** | mismo anexo — **Jefe hombre = 32.4** (y el reparto completo de `SF10`, que la fila daba por no publicado) |
| **DOC-03** | jun 2025 | razón de dos IMOR | **NO** | CNBV: `IMOR`=0 · `ajustado`=0 · `Azteca`=0 · `razón`=0 sobre los 3 índices; control positivo `cartera`=41/9/3 |
| **DOC-05** | 4T2025 | castigos / cartera | **NO** | BMV: `GENTERA`=0 · `castigos`=0 (control `emisora`=46) · CNBV: `Gentera`=0, `Compartamos`=0 |
| **DOC-06** | 4T2026 | IMOR ajustado Findep | **NO** | HR + BMV + CNBV: `FINDEP`/`Independencia`=0, con controles positivos |

**Los tres `NO` no son fallos de búsqueda.** `DOC-03` pide una **razón** entre el IMOR ajustado de una institución
y el de un producto agregado: un regulador publica los dos componentes por separado, **nunca su cociente** — la
propia fila lo dice («compass-4 yuxtapone 10.7 y 13.7 **sin dividirlos**»). `DOC-05` pide una **fracción** que la
fila misma declara que «hay que componerla de dos cifras publicadas». `DOC-06` tiene árbitro **estrictamente
futuro**: la ola es `4T2026` y hoy es 25/ago/2026 — ninguna búsqueda podía devolver otra cosa. Los tres son el
`NO` por **aserto estructural** que `BIBLIOTECARIO-56` mandó no tocar, ahora **corroborado por búsqueda**.

## 4 · Fila `A.12`: **no se abre**

El encargo la condiciona a que alguna resulte inevaluable **con razón nueva**. Ninguna lo es: las cinco `DIN` se
evaluaron, y las tres `DOC` salen `NO` por razones que **ya están escritas en sus propias filas**. La razón nueva
que sí apareció —el certificado intermedio ausente de CNBV— **no dejó nada inevaluable**, porque se resolvió.

---

## 5 · Cuadro de la cuota, re-derivado — alimenta directo al sorteo-v2

```
CUADRO DE LA CUOTA (i) de ADV1-M1 -- re-derivado del marco tras este acto
  filas del marco ........ 60
  publicada = SI ......... 33
  publicada = NO ......... 27
  PENDIENTE .............. 0

  SI sobre 60 ............ 33/60 = 55.0 %   (tope 20 % = 12 filas; exceso +21)
  SI sobre el marcador 50  33/50 = 66.0 %   (tope 20 % = 10 filas; exceso +23)

  antes de este acto: SI=28 (46.7 % / 56.0 %) con 8 sin evaluar
  movimiento del acto: +5 SI, +3 NO, PENDIENTE 8 -> 0
```

**Lectura.** El cierre del filtro (i) **no salva la cuota: la agrava**. La cuota (i) de `ADV1-M1` fija un tope de
**20 %** de candidatas publicadas; el marco pasa de **28/60 (46.7 %)** con 8 sin evaluar a **33/60 (55.0 %)** con
**cero** sin evaluar. Contra el marcador de 50, de **56.0 %** a **66.0 %**. El exceso es de **+21** filas sobre 60
y **+23** sobre 50. Lo que este acto entrega al sorteo-v2 no es margen: es la cifra **completa y firme**, que era
justamente lo que faltaba para poder rediseñar el sorteo (`FP-145`) sabiendo contra qué.

---

## 6 · Defecto de una fila del marco, reportado y NO corregido aquí

`DIN-09` declara en su `frase_discriminacion` que es «**misma pregunta que DIN-08 en la ola 2021, con mnemónico
distinto (SF5 en vez de SF7)**», y que por eso sirve de sonda de perturbación barata. **Es falso.** El manual de
la base 2021 trae los tres reactivos por separado y con el texto verbatim:

- `SF5` — renta, agua, luz, teléfono fijo, internet fijo o celular
- `SF6` — televisión por cable, plataformas tipo Netflix, colegiaturas
- `SF7` — **créditos hipotecarios y tarjetas de crédito** ← idéntico al `SF7` de 2019

**El mnemónico no cambió.** `DIN-09` mide un reactivo **distinto** del de `DIN-08`, así que la sonda no compara lo
que dice comparar: dos cifras distintas no probarían que el corredor modela, y dos iguales no probarían que
recita. **No se corrige aquí**: el perímetro de este acto es **sólo la columna `publicada` de esas 8 filas**.
Queda escrito en la propia celda, en esta nota y en el ADR, para que lo tome un acto con perímetro sobre
`frase_discriminacion`.

## 7 · Reservas de universo, declaradas y no calladas

Las cinco `DIN` salen `SI` con una reserva común que **no** cambia el veredicto de «publicada» pero sí importa
para quien use la cifra: los cortes publicados por Banxico son por **nivel socioeconómico, edad o sexo *del jefe
del hogar***, mientras las filas describen su universo como «personas … que administran o aportan dinero al
hogar». El propio informe define al informante como la persona más involucrada en administrar los recursos del
hogar, y sus anexos la rotulan «jefe/jefa de familia» — son la misma persona por diseño de la encuesta, pero el
rótulo **no es el mismo** y se declara en vez de equipararse en silencio. Reserva adicional, tampoco declarada por
las filas: el módulo se levanta **sólo en localidades de 50 mil habitantes y más**.

## 8 · Discrepancia entre extractores, declarada

`pdftotext -layout` **no capturó** la cabecera `Resultados 2021` del Informe 2021 (está sangrada); `pypdf` sí, en
la pág. 95. La ola del anexo de `DIN-10`/`DIN-12` quedó fijada por **concordancia de los dos extractores sobre las
cifras** (`SF2` = 71.2 / 65.4 en los dos) y por la posición de página, no por la cabecera de uno solo. Es
exactamente para lo que sirve el doble extractor.

## 9 · Lo que este acto NO hace

- **No toca ninguna columna del marco salvo `publicada`** en esas 8 filas — ni `frase_discriminacion`, ni
  `cv_arbitro`, ni `n_no_ponderado`, pese a que el §6 documenta un defecto en la primera.
- **No abre fila `A.12`**: ninguna resultó inevaluable con razón nueva (§4).
- **No rediseña el sorteo** (`FP-145`), que es acto propio; sólo le entrega el cuadro firme.
- **No adquiere**: los 10 PDF de Banxico se abrieron desde el scratchpad, **no** se registraron en el manifiesto
  ni se copiaron al corpus — este acto no es de adquisición y el manifiesto no está en su perímetro.
- **No toca `forense/hallazgos.md`**: no está en el perímetro.
