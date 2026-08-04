# CAL-CONF Fase B — posición 4, ENDIREH paso 1: ¿trae reactivo de `exposicion_violencia`?

*4 de agosto de 2026.*

**Resultado de este acto, dicho antes que nada: SÍ TRAE — candidatos SIRVEN
contra la frase-criterio, con universo parcial declarado y una brecha C2
señalada para paso 2.** Este acto no mide nada y no mueve el contador (sigue
en **8/14**); desbloquea el paso 2. Es uno de los actos nombrados de la
condición de caducidad de ADR-52 A — no el que la cierra, porque sí produjo
candidatos.

---

## 0 · Verificación de procedencia antes de obedecer

Tipo (1). Verificado contra `origin/main` en `0b61c52` (`git fetch origin`,
worktree nuevo `sesion/cal-conf-faseb-pos4-endireh-descriptor`) antes de
escribir esta nota:

- `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md` §2 —
  leída completa. Las dos URLs citadas por el encargo se verificaron de
  nuevo esta sesión, independientemente (§1 abajo): coinciden byte a byte
  con lo que esa nota reportó. La nota declara, sin resolver, si
  `datosabiertos/conjunto_de_datos_endireh_2021_csv.zip` (74 222 707 B) y
  `microdatos/bd_endireh_2021_csv.zip` (78 902 567 B) son el mismo
  conjunto con empaquetado distinto o productos distintos — **se resuelve
  aquí, por el propio API, no se adivina**: la respuesta JSON de
  `archivoscompaginacion` (tipodocto=0, §3 abajo) marca cada archivo con
  un sufijo `CON_ESTANDAR`/`SIN_ESTANDAR` en el campo `formato` —
  `datosabiertos/conjunto_de_datos_endireh_2021` es el único
  `CON_ESTANDAR` (un solo `.csv`, 70.8 MB declarados); `microdatos/bd_endireh_2021`
  es `SIN_ESTANDAR` en sus 5 formatos (`csv`/`dbf`/`dta`/`RData`/`sav`,
  75.2 MB el csv). Es el mismo levantamiento (ENDIREH 2021) publicado bajo
  dos estándares de INEGI distintos —"datos abiertos" (formato normalizado
  único) vs. "microdatos" (formatos de software estadístico)—, no dos
  productos de contenido distinto; la diferencia de tamaño es consistente
  con que cada estándar serializa catálogos/columnas de forma distinta (no
  verificado campo por campo — el FD describe una sola base, no distingue
  entre los dos productos de descarga).
- `forense/hitoE-campana-medicion-v2_0.md` §14.3 (fila 4) y §15 — leídas
  completas. Confirman: reactivo anterior (`BP1_20`/`BP1_23`/`BP1_28` de
  ENVIPE) **retirado** por `PR #57`; fila 4 **PENDIENTE DE VERIFICACIÓN**;
  contador en 7/14 en ese momento del archivo, hoy **8/14** tras las
  posiciones 5-6 (`radio_confianza`, `familismo_apoyo`).
- `canon/modelo-decision-v4_0.md:275-278` — leído. Confirma ADR-52 A: la
  clase "sin reactivo verificado — búsqueda abierta" para
  `exposicion_violencia`, con **dos actos de búsqueda ya en curso**
  nombrados ahí mismo: *"posición 4 rehecha sobre `TPer_Vic1`"* (`PR #61`,
  volvió **NO ALCANZABLE**, no examinó nada) y *"barrido de alcanzabilidad
  ENDIREH/ENSU"* (`PR #65`, confirmó alcanzabilidad, no leyó contenido).
  Este acto es el que **sí abre el descriptor** — ninguno de los dos
  anteriores lo hizo.
- `canon/modelo-decision-v4_0.md:372` — verificado. `G4`: *"Exposición a
  violencia + impunidad → Conducta defensiva, retracción del espacio
  público"*, **SIN FALSAR**.
- `forense/notas/2026-08-01-p2-momentos-atributos.md` §2.b-§2.d — leídas
  completas. Criterio C1-C4 de identificación de `β_gk`; fila `G4
  exposicion_violencia` (antigua, ya retirada); las tres reglas que `G4`
  enruta: `civico.protesta.agravio_urbano`, `civico.autodefensa.agravio_rural`
  (`modelo:490-491`), `comunicacion.inseguridad.ver_oir_callar`
  (`modelo:517`) — `grep -n "PORQUE G4" canon/modelo-decision-v4_0.md`.
- `forense/notas/2026-07-31-inventario-segmentacion.md` (Tabla B) —
  `grep -in "endireh"` da **cero resultados**. ENDIREH no es una de las 8
  fuentes de Tabla B. Esto importa para el chequeo C3/C2 (§4).
- `data/manifiesto.yaml` — sin entrada previa de ENDIREH antes de esta
  sesión (confirmado por `grep -i endireh` antes de tocar el archivo).

## 1 · Sesión-tipo: Ubuntu, red a INEGI verificada

```
$ curl -s -o /dev/null -w "http_code=%{http_code}\n" --max-time 15 \
    https://www.inegi.org.mx/programas/endireh/2021/
http_code=200
```

Alcanzable. A diferencia de `PR #61` (bloqueado por política de proxy en
sandbox de nube), este entorno tiene `inegi.org.mx` en su lista de hosts
permitidos.

## 2 · El criterio, escrito antes de abrir nada (§2.1 del encargo)

**Frase-criterio:** *proporción de personas expuestas a violencia o
victimización —sufrida, no solo percibida ni la conducta posterior a ella
(denuncia, búsqueda de ayuda, silencio)— en un periodo de referencia
declarado (a lo largo de la vida vs. últimos 12 meses, distinguidos como
parámetros distintos, no variantes del mismo), condicionada al vector de
atributos observables de `canon` §1.1.A.*

Tres distinciones obligatorias, declaradas antes de mirar el descriptor
(§0 del encargo):

1. **Prevalencia de violencia sufrida** (por ámbito: pareja, familiar,
   comunitario, laboral, escolar; por periodo: vida vs. 12 meses) → es la
   exposición. **SIRVE si aparece.**
2. **Percepción de inseguridad del entorno** → otro constructo — más
   cercano a lo que `G4` *produce* (retracción del espacio público) que a
   lo que *consume* como antecedente. **NO SIRVE si aparece.**
3. **Actitudes o normas sobre la violencia** (p. ej. si se justifica la
   violencia, roles de género) → ni exposición ni desenlace. **NO SIRVE
   si aparece.**

## 3 · Localización del descriptor — no el microdato

Mecanismo documentado (no adivinado), mismo que usó el barrido de
alcanzabilidad y las sesiones de posición 5-6/8:

1. `curl` de `https://www.inegi.org.mx/programas/endireh/2021/` → shell
   real (no soft-404), `idm='3117'` → `idBiinegi=3117`.
2. `curl` de `.../data/pestana/pestanadata.js` → confirma 5 pestañas:
   Documentación, Tabulados (`tipoinformacion=5`), **Microdatos**
   (`tipoinformacion=4`), Datos abiertos (`tipoinformacion=12`),
   Herramientas. El FD vive clasificado bajo `tipoInformacion=Microdatos`
   en el API (no es el microdato en sí — es su descriptor).
3. `GET` a `archivoscompaginacion` con `idBiinegi=3117&tipodocto=0` (todos
   los tipos, no solo `tipodocto=4` que usó el barrido para forzar el
   microdato) → **42 archivos**: 1 Microdatos-base, 1 Datos abiertos, 38
   Tabulados, y **`Descriptor de archivos (FD)` →
   `/programas/endireh/2021/doc/endireh2021_fd` (pdf)** — exactamente el
   patrón `/doc/` que el encargo cita como ya probado para otras fuentes.
   (También aparece `endireh2021_calc_r.pdf`, "Cálculo de los principales
   indicadores... con R" — no descargado, no hacía falta para este acto.)
4. Verificado antes de bajar, `-r 0-0` (no `HEAD`):

   ```
   $ curl -s -o /dev/null -D - -r 0-0 --max-time 20 \
       https://www.inegi.org.mx/contenidos/programas/endireh/2021/doc/endireh2021_fd.pdf
   HTTP/1.1 206 Partial Content
   Content-Type: application/pdf
   Content-Range: bytes 0-0/10369637
   ```

5. Descargado a `data/raw/endireh2021/endireh2021_fd.pdf` (10 369 637
   bytes — coincide exacto con `Content-Range`). Registrado con
   `tests/manifiesto.py --registra` (sha256/tamaño derivados del archivo,
   no tecleados) como `endireh2021_fd_pdf`; **verificado**
   (`--verifica --id endireh2021_fd_pdf` → COINCIDE). **No se abrió
   ningún microdato** — ni el de `datosabiertos/` ni el de `microdatos/`.

**Qué es el FD.** "ENDIREH 2021. Estructura de la base de datos" (730
pp.): §1-2 describen las 28 tablas (una de vivienda, `TSDem`, 20 de
sección temática, `TB_VD` de variables derivadas); §3 ("Estructura del
archivo de explotación") lista, tabla por tabla, cada variable con su
pregunta/descripción literal y catálogo de valores — es un descriptor de
contenido, no solo de esquema técnico. No es el cuestionario en PDF
independiente (ese vive en la pestaña "Documentación", componente
`ldocumentos-inegi`, que no expone una API JSON legible por `curl` con el
mecanismo de esta sesión — se intentaron dos rutas plausibles del mismo
patrón y ambas dieron soft-404 o vacío; no se adivinó un tercer nombre).
El FD basta para el criterio: trae la pregunta/descripción literal de cada
campo, que es lo que §2.1 exige juzgar.

## 4 · Candidatos, por descriptor literal

**Universo del instrumento (todas las tablas):** *"la encuesta está
diseñada para recoger información de la población femenina de 15 años y
más, independientemente de su situación conyugal"* (FD §1.2.2, verbatim).
**Mujeres 15+.** Confirma lo que `hitoE §14.3` ya anotaba (cita del
encargo) y lo que el barrido de alcanzabilidad declaró sin verificar
(§2 de esa nota) — **aquí sí se verificó, contra el descriptor.** Cualquier
candidato de abajo es **parcial declarado, nunca reactivo poblacional.**

La tabla `TB_VD` ("Tabla de variables derivadas", FD p.2: *"Contiene
información sobre la condición de violencia total, por ámbito y por tipo
de violencia a lo largo de la vida y en los últimos 12 meses"*) trae 42
variables; las de exposición, con su descripción literal exacta del FD
(§3, pp.727-729) y catálogo `1=Con incidencia de violencia / 2=Sin
incidencia / 9=No especificado`, salvo donde se anota:

| Código | Descriptor literal (FD) | Universo efectivo | Periodo | Veredicto |
|---|---|---|---|---|
| `VTOT_A` | "Condición de violencia total a lo largo de la vida" | mujeres 15+ (todas las situaciones conyugales A1/A2/B1/B2/C1/C2) | vida | **SIRVE** — agregado, cualquier tipo/ámbito |
| `VTOT_12M` | "Condición de violencia total en los últimos 12 meses" | ídem | 12 meses | **SIRVE** |
| `VPSI_A` / `VPSI_12M` | "Condición de violencia psicológica" (vida / 12m) | ídem | vida / 12m | **SIRVE** — por tipo |
| `VFIS_A` / `VFIS_12M` | "Condición de violencia física" (vida / 12m) | ídem | vida / 12m | **SIRVE** — por tipo |
| `VECO_A` / `VECO_12M` | "Condición de violencia económica, patrimonial o discriminación" (vida / 12m) | ídem | vida / 12m | **SIRVE** — por tipo |
| `VSEX_A` / `VSEX_12M` | "Condición de violencia sexual" (vida / 12m) | ídem | vida / 12m | **SIRVE** — por tipo |
| `VESC_A` / `VESC_12M` | "Condición de violencia total en el ámbito escolar" (vida / 12m) | mujeres 15+ que **son o han sido estudiantes** (`POB_E_A`/`POB_E_12M`; catálogo trae `blanco` para quien no aplica) | vida / 12m | **SIRVE** — por ámbito, universo más angosto que "mujeres 15+" |
| `VLAB_A` / `VLAB_12M` | "Condición de violencia total en el ámbito laboral" (vida / 12m) | mujeres 15+ que **realizan o han realizado actividad remunerada** (`POB_L_A`/`POB_L_12M`; `blanco` si no aplica) | vida / 12m | **SIRVE** — por ámbito, universo condicionado |
| `VCOM_A` / `VCOM_12M` | "Condición de violencia total en el ámbito comunitario" (vida / 12m) | mujeres 15+, sin condicionante adicional (sin categoría `blanco`) | vida / 12m | **SIRVE** — por ámbito |
| `VFAM` | "Condición de violencia total en el ámbito familiar **en los últimos 12 meses**" | mujeres 15+ | **12 meses únicamente** — el FD no trae una `VFAM_A` de "a lo largo de la vida"; asimetría real del instrumento, no omisión de esta lectura (`grep -n "VFAM" ` da un solo resultado) | **SIRVE**, con hueco declarado: no hay versión "vida" de este ámbito en `TB_VD` |
| `VPAR_A` / `VPAR_12M` | "Condición de violencia total en el ámbito de pareja a lo largo de su relación actual o última" (vida / 12m) | mujeres 15+ **con pareja o expareja actual/última** — catálogo trae `blanco`; columna "Situación Conyugal" lista **solo C1** (soltera con pareja/exnovio), **excluye C2** (soltera que nunca tuvo pareja) | vida / 12m | **SIRVE** — universo más angosto todavía: excluye explícitamente a quien nunca tuvo pareja |

Fuera de `TB_VD`, dos hallazgos que resuelven las distinciones 2 y 3 del
§2:

- **Distinción 2 (percepción de inseguridad del entorno): buscada y NO
  ENCONTRADA.** `grep -in "percepci\|insegur"` sobre el texto completo del
  FD da un solo resultado, y es de la sección VI (roles de género, ver
  abajo) — no de inseguridad. ENDIREH, a diferencia de ENVIPE/ENSU, no
  trae un ítem de percepción de inseguridad del entorno. Examinado, no
  hallado — no es candidato ni con veredicto NO SIRVE, porque no existe.
- **Distinción 3 (actitudes/normas): encontrada, NO SIRVE.**
  `TB_SEC_VI` — descrita en el FD p.2 como *"percepción de las mujeres de
  15 años y más respecto a los roles socialmente asignados a hombres y
  mujeres"*. Ítems `P6_2_1`-`P6_2_4`: *"¿Está usted de acuerdo en que..."*
  (p.ej. *"las mujeres que se visten con escotes... provocan..."* —
  wording exacto del FD, ítem `P6_2_3`). Es actitud/norma sobre roles de
  género y justificación de conducta, no exposición ni desenlace de `G4`.
  **NO SIRVE**, declarado por descriptor, no por familiaridad con el
  instrumento.

**Lo que el FD no permite verificar en este acto:** la metodología de
construcción de `VTOT_A`/`V*_A` (qué ítems de las secciones VII-XIV se
agregan para producir cada bandera) no está en este documento — el FD es
estructural (variable × descripción × catálogo), no metodológico. El
juicio SIRVE/NO SIRVE de arriba se apoya en la **descripción literal de
la variable derivada misma** ("condición de violencia... a lo largo de la
vida/12 meses", catálogo con-incidencia/sin-incidencia), que es
categóricamente distinta del patrón que hizo fallar a `BP1_20` de ENVIPE
(*"¿Acudió a denunciar el delito?"*, conducta posterior). Ninguna de las
11 variables de `TB_VD` de arriba tiene wording de denuncia, búsqueda de
ayuda o actitud — todas preguntan por la ocurrencia. Confirmar la cadena
de ítems exacta que arma cada bandera es trabajo del paso 2 (o de quien
lea las secciones VII-XIV completas), no de este acto.

## 5 · Chequeo C3 (obligatorio antes de declarar que sirve)

`grep -in "endireh"` sobre `forense/notas/2026-07-31-inventario-segmentacion.md`
(Tabla B, la tabla parámetro × fuente que P2 §2.d cita) da **cero
resultados**. ENDIREH no es una de las 8 fuentes de Tabla B — ninguna de
las variables candidatas (`VTOT_A`, `VPSI_A`, ..., `VPAR_12M`) puede
aparecer del lado del desenlace de ninguna regla de Tabla B, porque Tabla
B no conoce ENDIREH. **C3 pasa — no hay circularidad posible.**

**Lo que esto NO resuelve, declarado sin que el encargo lo pidiera
explícitamente (ADR-46(4), conservador — más exploración, no menos).**
El criterio completo de identificación de `β_gk` (P2 §2.b) exige además
**C2**: que la *misma fuente* observe un desenlace de una regla enrutada
por `G4` — `civico.protesta.agravio_urbano`, `civico.autodefensa.agravio_rural`,
`comunicacion.inseguridad.ver_oir_callar` (`grep -n "PORQUE G4"
canon/modelo-decision-v4_0.md`). Ninguna de las 20 secciones de ENDIREH
listadas en el FD (§2, pp.1-3) se describe como protesta, autodefensa o
"ver-oír-callar" — son violencia, roles, ingresos, decisiones, recursos
sociales, división del trabajo, discapacidad. **No se leyeron las
secciones completas para descartar C2 con certeza** (el FD describe cada
tabla en una frase; una lectura ítem por ítem de las 20 secciones está
fuera del perímetro de este acto). Si C2 falla, `exposicion_violencia`
podría medirse (θ_k(x) vía ENDIREH) sin que eso identifique `β_G4` — el
mismo patrón que "compra la condicional, no el coeficiente" que este
encargo cita para `familismo_apoyo`/`radio_confianza`. **Declarado como
pregunta abierta para paso 2 o para quien intente identificar el
coeficiente, no como bloqueo de este acto** — el encargo pide juzgar el
reactivo de la condicional, no identificar el coeficiente.

## 6 · Ejes disponibles (canon §1.1.A), declarados sin fabricar ninguno

Evaluados contra `TB_VD` (la tabla donde viven los candidatos) y lo unible
por la llave primaria compartida `UPM+VIV_SEL+HOGAR+N_REN` (FD §1.2.4):

| Eje (canon §1.1.A) | ¿En `TB_VD` directamente? | ¿Unible desde otra tabla ENDIREH? |
|---|---|---|
| 1. Formalidad laboral (`segsoc`) | No | **No equivalente confirmado.** `TSDem` trae estatus de actividad la semana pasada (trabajó sí/no, tipo: patrón/cuenta propia/sin pago) pero ningún campo de derechohabiencia/seguridad social — las menciones de IMSS/ISSSTE en el FD son sobre a qué institución acudió la mujer tras un incidente (`P7_15_6` y análogas), no un campo demográfico. No se fabrica la equivalencia. |
| 2. Edad | No | **Sí** — `EDAD` en `TSDem`, misma llave. |
| 3. Urbanización | **Sí, directo** | `DOMINIO` (Urbano/Complemento Urbano/Rural) está en `TB_VD` mismo — 3 categorías, más grueso que las 4 de `tam_loc` de ENIGH, mismo eje. |
| 4. Ingreso | No | **Parcial, no verificado a fondo.** `TB_SEC_IV` trae montos de ingreso monetario de la mujer (y de su pareja) — de la mujer, no un agregado de hogar como `ing_cor`/`est_socio` de ENIGH. No se abrió esa sección a detalle en este acto. |
| 5. Acceso digital | No | **Sí, mismo tipo de dato que ENIGH.** `P1_4_5` (tenencia de teléfono celular) y `P1_4_9` (servicio de internet) viven en la tabla de vivienda (`TVIV`, no `TB_VD`) — tenencia binaria de hogar, unible por `UPM+VIV_SEL` (un nivel más agregado que persona, misma restricción de nivel-hogar que ya documenta `canon` §1.1.A para ENIGH). |
| 6. Condición migratoria | No | **No equivalente confirmado.** Lo único hallado (`P12_2`/`P12_3`, sección XII "familia de origen") pregunta dónde vivió la mujer **cuando era niña** — no residencia actual ni residencia hace 5 años, que es lo que mide `residencia` de ENIGH. No se fabrica la equivalencia. |

**Tres de seis ejes disponibles con confianza** (edad, urbanización,
acceso digital — este último a nivel hogar, con la misma restricción que
ya aplica a ENIGH). **Uno parcial sin verificar a fondo** (ingreso, a
nivel persona no hogar). **Dos sin equivalente confirmado** (formalidad
laboral, migración) — no se leyeron a fondo las secciones donde
podrían vivir variantes más cercanas; declarado como límite de este acto,
no como ausencia categórica del instrumento.

## 7 · Rama de conclusión

**Hay reactivo que sirve.** Once variables candidatas en `TB_VD`
(`VTOT_A`/`VTOT_12M` como agregado; `VPSI`/`VFIS`/`VECO`/`VSEX` × vida/12m
por tipo; `VESC`/`VLAB`/`VCOM`/`VFAM`/`VPAR` × vida/12m por ámbito, con
universos progresivamente más angostos). Ninguna mide conducta posterior
(denuncia, búsqueda de ayuda) ni percepción ni actitud — las tres
distinciones del §2 se resolvieron por descriptor literal, no por
familiaridad con el instrumento.

**Código, universo, periodo y ejes, listos para paso 2 — declarados, no
adjudicados a una sola variable.** Paso 2 (o mesa) decide entre el
agregado (`VTOT_A`/`VTOT_12M`, que replica la generalidad de la cláusula
de `G4` en `canon` §2.1 — "exposición a violencia" sin calificar ámbito)
y el desglose por ámbito/tipo (que permitiría, eventualmente, desdoblar
`exposicion_violencia` como ya hace `confianza_institucional`) — decisión
de diseño, no de esta acta.

**Marca de parcialidad, como propiedad del resultado, no como advertencia
genérica:** cualquier medición que use estos candidatos describe **solo a
mujeres de 15 años y más** (`VESC`/`VLAB`/`VPAR` además condicionan a
subpoblaciones más angostas todavía — estudiantes, trabajadoras, con
pareja). No hay forma de que este instrumento hable de hombres ni de
mujeres menores de 15. Cualquier `θ_k(x)` construida desde ENDIREH hereda
esta restricción de universo y debe declararla junto con el número, no
junto a un aparte.

**No se declara SIRVE/NO SIRVE definitivo sobre C2** (§5) — es la única
pieza que este acto deja abierta explícitamente, por elección de
perímetro, no por hallazgo negativo.

## 8 · Declaración de contaminación (ADR-46(4), conservador)

**Este acto SÍ leyó el instrumento de ENDIREH** — el FD completo
(estructura, 28 tablas, descripciones de sección) y, a nivel de ítem, las
descripciones literales de `TB_VD` (42 variables) y de `TB_SEC_VI`
(`P6_2_1`-`P6_2_4`). **Esta sesión y esta máquina, mientras retengan este
contexto, quedan inhabilitadas para pre-registrar contra ENDIREH**
(ADR-46, unidad = sesión). No se abrió microdato — la inhabilitación es
sobre estructura de contenido, no sobre haber visto filas de datos; se
declara igual, conservador, sin distinguir grados dentro de "estructura".

## 9 · Qué NO se hizo

- No se abrió ningún microdato (`datosabiertos/` ni `microdatos/`) — solo
  el FD.
- No se leyeron las 20 secciones temáticas completas — solo sus
  descripciones de tabla (FD §2) y, a nivel de ítem, `TB_VD` completa y
  `TB_SEC_VI` parcial (los 4 ítems citados en §4).
- No se resolvió C2 (§5) — declarado abierto, no fabricado.
- No se tocó `canon/` ni `milpa/`.
- No se adjudicó una sola variable como "el" reactivo de posición 4 —
  eso es juicio de paso 2 o de mesa, once candidatas quedan declaradas.
- No se movió el contador ni se editó `hitoE §14.3`/`§15` — la fila 4
  sigue **PENDIENTE DE VERIFICACIÓN** hasta que paso 2 mida.

## 10 · Límite de lectura declarado

Leído completo: `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md`
§0-§2; `forense/hitoE-campana-medicion-v2_0.md` §14.3 (fila 4), §15;
`canon/modelo-decision-v4_0.md:260-280` (paso 5, ADR-52 A), `:360-400`
(tabla de generadores/coeficientes, ejes `PORQUE G4`), `:100-180`
(§1.1.A, vector de atributos); `forense/notas/2026-08-01-p2-momentos-atributos.md`
§2.b-§2.d; `forense/notas/2026-07-31-inventario-segmentacion.md` (grep
dirigido, no lectura completa — 41 grupos-regla, se buscó "endireh" y las
tres reglas de `G4`); `data/manifiesto.yaml` (grep dirigido antes de
registrar). Descargado y leído completo (`pdftotext -layout`, 51 795
líneas): `data/raw/endireh2021/endireh2021_fd.pdf` — estructura (§1-2)
completa, §3 leída dirigida (grep por `TB_VD`, `TB_SEC_VI` P6_2, búsqueda
de los seis ejes) — **no leída línea por línea completa** (730 páginas;
las 18 secciones no citadas en este acto no se inspeccionaron ítem por
ítem). No se abrió microdato. `python3 tests/check.py` — 19 FAIL · 84
WARN, igual a `tests/baseline.json`, sin cambio atribuible a este acto.
