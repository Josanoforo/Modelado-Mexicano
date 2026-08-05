# ENCARGO E-ENVIPE: tanda doble G4 sobre ENVIPE 2025 — paso 1, especificación congelada

## 0 · Verificación de entorno (protocolo §0, ARRANQUE)

Clon existente en `/home/pc0/Modelado-Mexicano` (no home). El clon base
estaba parado en `sesion/cal-conf-faseb-pos4-envipe-paso1` (no `main` —
verificado, no supuesto). Este acto trabaja en worktree propio,
`/home/pc0/mm-encargo-e-envipe-g4`, rama `sesion/encargo-e-envipe-g4`,
creada desde `origin/main`.

**SHA.** El encargo se redactó contra `origin/main = 2bc613b`. `git fetch
origin` mostró `origin/main` movido a `bd2c975` (6 commits: `ed2d668`,
`0abcdb0`, `6dbcc27`, `062f700`, `ff10d04`, `bd2c975`). Re-derivado antes de
editar, como exige el protocolo:

- `milpa/procedencia.yaml` cambió (`git diff --stat 2bc613b..origin/main`:
  4 inserciones/4 eliminaciones) — pero el diff está confinado a
  `:662-685` (bloque `G1·radio_confianza`, corrección de recuento por
  `ADR-61`: 28/12 → 33/9). `limite_c2` sigue exactamente en la línea `396`
  citada por el encargo (`git show origin/main:milpa/procedencia.yaml |
  grep -n limite_c2:` → `396:`), sin desplazamiento — el edit está 266
  líneas después, no reordena nada antes.
- `forense/censo-estimabilidad-coeficientes-v1_0.md` **no cambió** en el
  rango — filas 8-9 citadas por el encargo son las mismas que a
  `2bc613b`.
- `ADR-61(d)` declara el censo `E-CE` "vencido por segunda vez" — pero por
  instrumentos añadidos **después** de la foto del censo (`ENASEM` en
  `65302f7`, `ENFIH`/`ENSAFI`/ocho más en `PR #109`/`dff4877`), todos
  posteriores a `0db6d1d`. `envipe2025_csv` está en el manifiesto desde
  `ce3c284` (commit muy anterior, previo incluso a la foto `8cdabcb` del
  censo) — la clasificación RUTA-C de las filas 8-9 no está afectada por
  el vencimiento declarado en `ADR-61(d)`. Verificado, no supuesto.
- **Actos vivos.** `gh pr list --state open`: una sola PR abierta (`#114`,
  `sesion/hitoD-r1-3-canal-confianza`). `gh pr diff 114 --name-only`: solo
  toca `forense/hallazgos.md`, `forense/hitoD-R1_3-*`,
  `forense/hitoD-preregistro-v2_0.md` — ninguna de `milpa/procedencia.yaml`
  ni de ENVIPE. Coincide con lo que el encargo afirma de TANDA-4
  (ENIF/ENDUTIH, no procedencia), verificado independientemente vía PR, no
  solo citado. Rama `origin/sesion/r1-3-spec-huerfana` presente: residuo
  huérfano ya preservado por convención (push directo a rama descriptiva,
  sin PR) — no es acto vivo, no requiere acción de este encargo.

**data/raw.** Symlink creado en este worktree (`data/raw ->
/home/pc0/mm-corpus/raw`, mismo patrón que el resto de worktrees).
`python3 tests/manifiesto.py --verifica --id envipe2025_csv` (un solo id,
por el defecto documentado 4/ago): **COINCIDE** — sha256 y tamaño
(17 600 019 bytes) verificados contra `data/manifiesto.yaml:309`.

**Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `` (sin variable,
valor crudo). Sonda `curl -s -o /dev/null -w "%{http_code}" --max-time 10
https://www.inegi.org.mx/` = `200` (valor crudo). Coincide con Ubuntu con
datos, NO nube.

**Espejo.** Nada leído del espejo — todo vía `git show
origin/main:<ruta>` o lectura directa del clon/worktree, comandos citados
arriba.

**Remoto.** `git remote -v` → `https://github.com/Josanoforo/
Modelado-Mexicano.git` (fetch y push). Coincide.

## 1 · MESA-E1, verbatim

> (i) `BP1_23` se habilita como desenlace de estas dos estimaciones
> únicamente, con universo declarado "entre disparadores de `AP7_3`" y
> disciplina A-bis 4 completa. NO operacionaliza `ver_oir_callar`
> globalmente; `limite_c2` NO se toca. Se registra verbatim en la spec
> como decisión MESA-E1 (patrón MESA-M4/MESA-R12, sin ADR salvo que mesa
> lo pida).

Marcada `(i)` en la cabecera del encargo ("corrible al pegar MESA-E1 =
(i)"). Este acto corre bajo esa marca. `limite_c2`
(`procedencia.yaml:396-413`) no se edita — verificado que ninguna de las
dos entradas nuevas de este acto lo toca (perímetro exacto, abajo).

## 2 · PASO 0 — verificación estructural contra el FD (sin abrir microdato)

Extraído con `pdftotext -layout` (mismo método que `PR #57`/`PR #74`/
`2026-08-04-envipe-tper-vic2-tmod-vic-paso1.md`, líneas idénticas —
7207/`fd.txt`, 987/`cuest_principal.txt`, 597/`cuest_modulo.txt` —
confirma reproducibilidad de las citas previas antes de confiar en
ellas):

**(1) `BP1_23` es reactivo distinto de ambas θ.** `BP1_23` vive en
`Tabla TMod_Vic` (`fd.txt:4417-7207`, Instrumento B). θ de fila 8
(`AP7_3_10`-`_14`) vive en `Tabla TPer_Vic2`, Sección VII
(`fd.txt:2885-4416`). θ de fila 9 (`AP5_4_01/02/03/05/06/07/11`) vive en
`Tabla TPer_Vic1` (`fd.txt:858-2884`). Tres tablas distintas, con llave
de identificación compartida (`ID_PER`, `UPM+VIV_SEL+HOGAR+R_SEL`) pero
sin superposición de contenido — confirmado por localización directa en
`fd.txt`, no por cita de tercero.

**(2) Estructura exacta del filtro de `BP1_23`.** Cuestionario impreso
(`cuest_principal.txt:942`): pregunta **7.3** = binario `AP7_3_XX`
("¿usted sufrió... del grupo B?"), catálogo `05`-`15` (`cuest_
principal.txt:933-973`, confirmado contra `BPCOD` del FD,
`fd.txt:4460-4540`: `05` robo en calle … `15` otros delitos — **mapeo
1:1 entre `BPCOD` 05-15 y `AP7_3_05`-`AP7_3_15`**, verificado código por
código). Instrucción de instrumento (`cuest_principal.txt:973`): *"SI HAY
REGISTRO DE ALGÚN DELITO EN LAS PREGUNTAS 6.6 o 7.4, APLIQUE EL MÓDULO
SOBRE VICTIMIZACIÓN (INSTRUMENTO B)"* — "7.4" es la pregunta de
frecuencia inmediatamente adyacente a 7.3 en el layout (`cuest_
principal.txt:942`, misma línea de la tabla impresa), con valor no-blanco
si y solo si `AP7_3_XX`=1 (FD: "01-99 / blanco si `AP7_3_XX`≠1") — el
disparador operativo es `AP7_3_XX`=1, confirmado por dos vías
independientes (wording del instrumento + estructura de blancos del FD).
Dentro de `TMod_Vic` (`cuest_modulo.txt:252-276`): `BP1_20` ("¿Acudió...a
denunciar?") 1=Sí→PASE A 1.24 / 2=No→continúa; nota impresa inmediata
*"SI EL CÓDIGO DEL DELITO ES DEL 05 AL 15, PASE A LA PREGUNTA 1.23"* —
para todo delito personal (05-15, el catálogo completo de Sección VII,
**no** solo el núcleo de violencia 10-14), `BP1_20`=2 pasa directo a
`BP1_23`. **Disparador exacto: `AP7_3_XX`=1 para XX ∈ {05,...,15} (once
ítems, todo el catálogo personal — patrimonial y de violencia) Y
`BP1_20`=2 (No denunció) para ese delito.** Códigos válidos de `BP1_23`:
`01` miedo al agresor, `02` miedo a extorsión, `03` delito de poca
importancia, `04` pérdida de tiempo, `05` trámites largos, `06`
desconfianza en la autoridad, `07` no tenía pruebas, `08` actitud hostil
de la autoridad, `09` otra, `99` NS/NR, `b` blanco (no aplica). No
incluye `AP6_6` (Sección VI, hogar) en el disparador de este acto —
exclusión declarada: mezclaría el informante-hogar que la propia nota de
`exposicion_violencia` (`procedencia.yaml:381-387`) ya identificó como
contaminante (`RESUL_H`), y el encargo cita literalmente `AP7_3_XX`, no
`AP6_6`.

**(3) Ponderador/UPM/estrato y join.** `TPer_Vic1`/`TPer_Vic2` (mismo
diseño): peso `FAC_ELE` (no `FAC_ELE_AM`, subconjunto urbano), estrato de
varianza `EST_DIS` (001-607), UPM `UPM_DIS` — confirmado en `TPer_Vic1`
(`fd.txt:1972-2022`) y ya validado para `TPer_Vic2` por
`procedencia.yaml:344-350`. `ESTRATO` (1-4, área, no ingreso) es variable
distinta de `EST_DIS` (diseño/varianza) — confirmado, no confundido.
`TMod_Vic` trae su propia copia de `EST_DIS`/`UPM_DIS` (`fd.txt`, bloque
identificación) pero **no** trae `FAC_ELE` — el peso se importa por join.
**Join:** las tres tablas comparten `ID_PER` (alfanumérico,
`0100001.01.01.01` = `UPM.VIV_SEL.HOGAR.R_SEL`, confirmado presente en
`TPer_Vic1` `fd.txt:873`, y en `TMod_Vic` `fd.txt:4438`) — **fila 9 exige
join `ID_PER` entre `TPer_Vic1` (θ) y `TMod_Vic` (desenlace)**, tal como
el propio censo lo declara (`censo-estimabilidad-coeficientes-v1_0.md`,
fila 9: *"unión vía `ID_PER` entre `TPer_Vic1` y `TPer_Vic2`"* — leído
aquí como el mismo campo `ID_PER`, presente también en `TMod_Vic`, sin
necesidad de un salto intermedio por `TPer_Vic2` dado que `TMod_Vic` ya
lo trae nativo). Fila 8 no requiere join externo para el desenlace (θ y
universo comparten instrumento con `TMod_Vic` vía el mismo `ID_PER`,
todo dentro de la familia ENVIPE 2025).

**(4) ¿Contradice el FD al censo?** No. Las filas 8-9 del censo
(`censo-estimabilidad-coeficientes-v1_0.md:72-73`) describen exactamente
lo verificado arriba: RUTA-C, misma limitación estructural, mismo
`BP1_23`, join `ID_PER` para la fila 9. `limite_c2`
(`procedencia.yaml:396-413`) coincide palabra por palabra con la
estructura re-derivada aquí de forma independiente. `hitoE §15`
(`forense/hitoE-campana-medicion-v2_0.md:1203-1257`) confirma que
`BP1_20`/`BP1_23`/`BP1_28` fueron retirados **solo** como reactivo de
`exposicion_violencia` misma (`PR #57`) — `BP1_23` sigue vivo, sin
retirar, como candidato Parcial de `comunicacion.inseguridad.
ver_oir_callar` (`P2:264`). Sin contradicción — no hay PARO.

## 3 · Perímetro, confirmado antes de escribir la spec

`milpa/procedencia.yaml`: únicamente dos entradas nuevas en
`coeficientes_generador_medidos` (`G4_exposicion_violencia`,
`G4_confianza_institucional_justicia`). No se toca `limite_c2`,
`rutas_estimabilidad_coeficiente`, `asignados_coeficiente.detalle`,
entradas `W` existentes, ni `eje_policial`. `forense/notas/` (esta nota +
resultados) y `forense/hallazgos.md` (append). No `canon/`, no el censo,
no `hitoD-preregistro`.

## 4 · Desenlace `BP1_23`, codificación exacta (para estas dos
estimaciones únicamente — no operacionaliza `ver_oir_callar` globalmente)

Unidad nativa de `BP1_23`: **fila de `TMod_Vic`** (delito, llave `UPM+
VIV_SEL+HOGAR+R_SEL+BPCOD+ND_TIPO`), no persona — una persona con más de
un delito personal no denunciado puede tener más de una fila. θ (ambas
filas) es un atributo de **persona**. Para no mezclar niveles de
análisis, el desenlace se colapsa a persona por regla declarada, con
precedencia fija (no ajustada post-hoc):

1. Restringir a filas de `TMod_Vic` con `BPCOD` ∈ {05,...,15} y `BP1_23`
   no blanco (evidencia directa de haber llegado a la pregunta — chequeo
   de robustez en Commit 2: debe coincidir con `BP1_20`=2 en esas mismas
   filas; si no coincide, se reporta la discrepancia, no se oculta).
2. Por persona (`ID_PER`): si **alguna** fila califica con `BP1_23` ∈
   {`01`,`02`,`06`,`08`} (miedo al agresor, miedo a extorsión,
   desconfianza en la autoridad, actitud hostil de la autoridad) →
   desenlace = **1** ("razón de miedo/desconfianza").
3. Si ninguna fila calificó en el paso 2 pero **alguna** fila tiene
   `BP1_23` ∈ {`03`,`04`,`05`,`07`} (poca importancia, pérdida de tiempo,
   trámites, falta de pruebas) → desenlace = **0** ("razón práctica").
4. Si las únicas filas disponibles son `BP1_23` ∈ {`09` otra, `99`
   NS/NR} → persona **excluida** del desenlace binario; se cuenta y
   reporta aparte (n de "otra/NS-NR"), no se fuerza a 0 ni a 1.

**Razón de la dicotomización:** `01`/`02`/`06`/`08` son las cuatro
razones cuyo contenido es miedo o desconfianza hacia el agresor o la
autoridad — el contenido más cercano a "callar por miedo" que el
catálogo permite sin inventar categorías. `03`/`04`/`05`/`07` son
razones prácticas/logísticas (costo-beneficio percibido, no miedo). Es
una elección de este acto, declarada, no un rótulo canónico de
`ver_oir_callar` — otra sesión que sí adjudique esa variable puede elegir
distinto sin que esto la ate.

## 5 · Universo (A-bis 4), explícito, igual para ambas filas

**"Personas de 18+ del universo ENVIPE 2025 que dispararon `AP7_3_XX`=1
para algún XX ∈ {05,...,15} (catálogo completo de delito personal,
Sección VII) y con `BP1_20`=2 (no denunció) para ese delito."**
Operacionalizado como: personas con ≥1 fila en `TMod_Vic` con `BPCOD` ∈
{05,...,15} y `BP1_23` no blanco (ver §4.1). Todo lo que se estima y
reporta en Commit 2 vive dentro de este universo, incluido el marginal de
reconciliación (proporción de desenlace=1 sin condicionar por θ, dentro
del mismo universo). **Prohibido comparar cualquier cifra de este acto
contra el marginal de la población general de ENVIPE (91 182 filas)** —
el universo está seleccionado por construcción (ya víctima, ya no
denunciante), y esa selección es precisamente el mecanismo bajo estudio.

## 6 · θ y su solapamiento con el disparador

**Fila 8 (`exposicion_violencia`).** θ =
binario "sufrió al menos uno de los cinco del núcleo (`AP7_3_10`-`_14`)
durante 2024" (definición ya `MEDIDO`, `procedencia.yaml:344-345`, sin
redefinir). El núcleo (10-14) es **subconjunto** del disparador (05-15,
incluye además 05,06,07,08,09,15 — patrimonial/fraude/extorsión/otros).
El universo de este acto **no** se restringe a θ=1 — incluye tanto
personas con θ=1 (expuestas al núcleo violento y no denunciantes) como
personas con θ=0 pero disparador=1 (víctimas de delito patrimonial/
fraude puro, sin ítem núcleo, no denunciantes). Esto es deliberado: si el
universo colapsara a θ=1 no habría variación en θ para estimar una
diferencia de proporciones. **Tratamiento declarado:** θ se usa como el
predictor binario primario (θ=1 vs θ=0 dentro del universo de
disparadores), igual que cualquier otra fila. Como vista **secundaria,
descriptiva, no ajustada** (patrón `disciplina X §5` — tasa de desenlace
por nivel, lectura no paramétrica): se reporta también la proporción de
desenlace=1 por número de ítems núcleo disparados (0 a 5) dentro del
universo, sin ajustar, sin modelo. **Qué NO se afirma:** que θ "cause" el
desenlace; que el posible gradiente por número de ítems sea lineal o
monótono; que el universo (ya seleccionado por ser víctima no
denunciante) permita generalizar a la población de expuestos en general.
Techo: asociación condicional, nunca intervención (A-bis 2).

**Fila 9 (`confianza_institucional_justicia`).** θ = 7 ítems
`AP5_4_01/02/03/05/06/07/11` (Tránsito, Preventiva, Estatal, Ministerial/
Judicial, MP y Fiscalías Estatales, FGR, Jueces — ya `MEDIDO·PARCIAL
(edad,dominio)` por institución, `procedencia.yaml:191-201`), cada uno
dicotomizado **por ítem, universo propio**: `{1,2}` (mucha/algo de
confianza) = "confía" vs `{3,4}` (algo/mucha desconfianza) = "no
confía"; excluidos del binario `9` (NS/NR) y blanco (no identifica la
institución — no-aplicabilidad estructural ya documentada,
`procedencia.yaml:188-190`). θ es de contenido **independiente** del
disparador (confianza institucional general, no correlacionada por
diseño del instrumento con haber sido víctima) — pero condicionar el
universo a "víctima, no denunciante" introduce un riesgo de selección
nombrado por A-bis 2: quien no denuncia por desconfianza institucional
puede estar sobrerrepresentado en este universo por razones que
correlacionan con el propio θ — riesgo de **colisionador** (el universo
mismo pudo ser afectado por una causa común de θ y del desenlace).
**Lectura permitida: asociación condicional en el universo seleccionado
— techo del censo. Ninguna lectura causal, ninguna lectura de
intervención, ninguna extrapolación a la población general de ENVIPE.**
Vista secundaria no ajustada (mismo patrón que fila 8): proporción de
desenlace=1 por cada uno de los 4 niveles de confianza, sin colapsar,
por institución.

## 7 · Ejes de condicionamiento, uno a la vez (patrón Encargo X)

**Fila 8** (1 ítem θ × 4 ejes, cada uno por separado, sin cruces
conjuntos): edad (18-29 · 30-44 · 45-59 · 60+, 4 celdas) · dominio (U ·
C · R, 3 celdas) · formalidad (jornalero · empleado/obrero · cuenta
propia · patrón · sin pago — vía join a `TSDem`/`AP3_8`+`AP3_10`, mismas
5 categorías que `procedencia.yaml:337-340`, no redefinidas, 5 celdas) ·
`ESTRATO` de área (1·2·3·4, marginal, no ingreso individual, 4 celdas).
16 celdas por eje, 1 ítem = 16 celdas totales. Justificación: mismos
cuatro ejes que la propia medición de θ ya usó para `exposicion_
violencia` — reutilizar, no reinventar categorías.

**Fila 9** (7 ítems θ × 2 ejes, cada uno por separado): edad (4 celdas)
· dominio (3 celdas) — mismas categorías que fila 8. 7 celdas por eje
(4+3=7) × 7 ítems = 49 celdas totales. Justificación: dos ejes
declarados por el encargo; formalidad/ESTRATO no se corren para esta
fila porque el encargo no los declara para fila 9 — universo ya
pequeño (intersección disparador × identifica-institución) y correr ejes
no declarados invitaría a fragmentar celdas por debajo del soporte sin
justificación previa.

**Soporte mínimo:** 30 casos ponderados-crudos por celda (mismo umbral
usado en `procedencia.yaml:201`, "ninguna celda cae bajo el mínimo de
soporte"). Celdas por debajo de 30 se reportan como **SIN SOPORTE**, con
su n exacto — no se ocultan, no se computan como si tuvieran varianza
confiable.

## 8 · Enlace y forma (fila G4), declarado aquí

Por defecto: **no paramétrica por nivel** — la vista secundaria de §6
(tasa de desenlace por nivel de θ, sin colapsar) es la única lectura de
forma que este acto produce, leída sin ajustar (mismo criterio que
`disciplina X §5`: "tasa por nivel... no monótona... sin escalón
visible" fue una lectura directa de la curva, no un modelo ajustado). No
se ajusta ninguna curva paramétrica, no se estima ningún parámetro de
forma. Si esa lectura muestra escalón o monotonicidad clara, se declara
como observación, no como parámetro identificado.

## 9 · Escala local

Diferencia de proporciones del desenlace (θ=1 menos θ=0, o "confía" menos
"no confía"), condicional por eje, universo restringido a disparadores de
`AP7_3` — **no** la escala del índice del generador `G4`. Ningún ADR de
D-ABC ha sellado una función de enlace a la fecha de este commit
(verificado: `grep -rn "D-ABC" canon/` sin resultados de sellado) — la
clase de las dos entradas nuevas queda **`MEDIDO·β̂(dif. proporciones),
condicional(ejes), universo=disparadores AP7_3, no denunciantes`**, con
el hook de conversión declarado (si un ADR de D-ABC sella antes de
Commit 2, la fórmula de conversión entraría a la vista en ese commit; no
selló, así que no aplica).

## 10 · Regla de discordancia entre ejes

Plantilla: misma estructura que `G1_radio_confianza`
(`procedencia.yaml`, clave `eje_condicionante` bajo
`coeficientes_generador_medidos`) — reporte de cuántas celdas del total
invierten signo respecto al marginal de reconciliación (§5), y cuántas
son distinguibles de cero al 95%. **Cifra de referencia citada
correctamente:** `ADR-61(c)` (`gobernanza-v1_15.md:721-723`, ya sellado a
la fecha de este commit) corrigió el recuento original de `Encargo X` de
28/39·12 a **33 de 39 positivas, 9 de 39 significativas** — esta nota
cita 33/9, no 28/12, por instrucción explícita del encargo y porque
`M-3`/`ADR-61` ya cerraron esa corrección antes de que este acto
arrancara.

## 11 · Declaración de contaminación (ADR-46), a la fecha de este commit

Esta sesión abrió: `fd_envipe2025.pdf`, `cuest_principal_envipe2025.pdf`,
`cuest_modulo_envipe2025.pdf` completos vía `pdftotext -layout`
(estructura — secciones, catálogos, wording, códigos, reglas de pase).
**No** se abrió `envipe2025_csv.zip` (ni estructura de índice ni
contenido) — el hash se verificó por `tests/manifiesto.py` (que no abre
el zip, solo compara sha256). Esta sesión, mientras retenga este
contexto, queda **inhabilitada para pre-registrar contra ENVIPE**
(unidad = sesión, ADR-46) desde este punto en adelante. No inhabilita a
otras sesiones ni a otras máquinas.

## 12 · Qué NO hace este commit

- No abre `envipe2025_csv.zip`.
- No calcula ningún β̂, ningún n_util real, ninguna proporción.
- No toca `milpa/procedencia.yaml` (las dos entradas nuevas se escriben
  en Commit 2, con `universo:` explícito como campo, según lo aquí
  congelado).
- No opera `limite_c2` ni `comunicacion.inseguridad.ver_oir_callar` como
  variable global.
- No adjudica nada de `civico.denuncia.con_seguro` (candidato distinto de
  `BP1_20`/`BP1_28`, fuera de perímetro).
- No fusiona ningún PR.

**El primer resultado que produzca este procedimiento es el que se
reporta.**
