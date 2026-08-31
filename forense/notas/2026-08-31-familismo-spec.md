# ACTO MAESTRA32-E16 · MEDIDOR-FAMILISMO-APOYO — COMMIT-1: especificación congelada

Escrita ANTES de abrir un solo archivo de datos de `data/raw/`.

## (a) Ajuste de constructo

**Definición canónica.** `canon/glosario-v5_6.md:119`, entrada `familismo_apoyo`:
"red disponible, corresidencia, pooling de ingreso y cuidado" — tier
**Fuerte**, opera en G3 (pooling ante volatilidad) y en G5 ("seguro ante
Estado ausente"). `canon/modelo-decision-v4_0.md:439`: G5 · "Familia como
seguro ante Estado ausente" — genera "Pooling, corresidencia, carga de
cuidado". `:459`: `familismo_apoyo 0.50` (signo ASIGNADO, positivo).

**texto_reactivo, extraído de las fichas reales del payload (no tecleado
de memoria):**

- `eder2017` `financia_8` — extraído de `eder2017_fd.pdf` (entrada #91,
  Apartado D, pregunta 33): *"¿Para pagar o empezar a construir esta
  vivienda, el dueño tuvo préstamo de un familiar, amigo o
  prestamista?"* Etiqueta: "Tuvo préstamo de un familiar, amigo o
  prestamista". Tipo C(1), presencia/ausencia del código `8` dentro de la
  batería `financia_1`..`financia_8` (multi-respuesta sobre cómo se pagó
  o construyó la vivienda).
- `endireh2016` `p4_8_2`/`p4_8_3` — extraído de `fd_endireh2016_dbf.pdf`
  (dentro del zip, sección 4.8) y confirmado contra
  `data/emparejamiento-motor-v1_2.tsv` líneas 15-16: *"4.8.2. Actualmente,
  ¿usted recibe dinero de familiares o conocidos que viven en Estados
  Unidos de América...? (No incluya a su esposo o pareja)"* / *"4.8.3.
  Actualmente, ¿usted recibe dinero de familiares o conocidos dentro del
  país...?"*

**Regla pre-registrada, aplicada:** ambos reactivos nombran "familiar"
como fuente explícita y en primer lugar de dinero/préstamo recibido —
cumplen la regla ("mide apoyo económico familiar recibido u obtenido:
préstamo/dinero de familiares"). **Veredicto: VÁLIDA en los dos
instrumentos, sin rótulo `·PROXY-DE-THETA`.**

**Reserva declarada, no oculta:** los dos reactivos son *compuestos* —
`financia_8` funde "familiar" con "amigo" y "prestamista" (fuente
comercial) en un solo código; `p4_8_2`/`p4_8_3` funden "familiares" con
"conocidos" (red social más amplia que la familia). Ninguno aísla
"familia" de "no familia". Esta contaminación de constructo es una
reserva que viaja con el β̂ (ver COMMIT-2 sección A), no dispara PROXY
bajo la letra de la regla pre-registrada, pero limita la lectura del
resultado como "familismo" puro.

**Circularidad (precedente ENIF `p9_9_4`):** el desenlace de G5 en este
acto es corresidencia con familiar adulto (EDER) y carga de cuidado de
nietos/sobrinos (ENDIREH) — **ninguno de los dos es una transformación
del mismo reactivo que la θ.** `financia_8` mide financiamiento de
vivienda; el desenlace de corresidencia (`padre_cor`, `madre_cor`, etc.)
mide con quién vivió la persona, columna y batería distintas, en tablas
distintas (`vivienda.csv` vs. `historiavida.csv`). `p4_8_2`/`p4_8_3`
miden dinero recibido; `p18_4` mide cuidado de nietos/sobrinos, batería
distinta (Sección IV vs. Sección XVIII). **Corresidencia y cuidado de
nietos son constructos distintos de "recibir dinero" — declarado
explícitamente, sin circularidad.**

## (b) Fuentes, universos, ponderadores

**EDER 2017** — `data/raw/eder2017/eder2017_bases_csv.zip` (payload
citado en `data/inventario-fd-ext-v1_0.tsv`, ficha `eder2017_fd.pdf`,
sha256 `dd4d93114a38e80192bbc29a4a4ab7fba6e4bce0067ecfcdbb4540ada5890541`
— coincide con el hash ya registrado en el inventario, `dd4d93114a38`
truncado). El zip trae 5 tablas: `persona.csv`, `vivienda.csv`,
`antecedentes.csv`, `historiavida.csv`, `hogar.csv`.

- **Ponderador:** `vivienda.factor`, columna final de `vivienda.csv`
  (citado: `eder2017_fd.pdf`, sección de `vivienda`; la columna existe en
  el CSV, verificado por lectura directa del header). Diseño:
  `vivienda.est_dis` (estrato), `vivienda.upm` (UPM) — ambos presentes en
  el mismo CSV.
- **Universo de EDER (cuestionario retrospectivo):** `historiavida.csv`
  es un panel persona-año retrospectivo — 886,976 filas, 23,831 personas
  únicas (`folioviv`+`foliohog`+`id_pobla`), ~37 filas/persona en
  promedio (una fila por año de vida reconstruido). θ (`financia_8`) es
  una variable de **hogar** (`vivienda.csv`, 23,548 filas) que aplica
  solo a hogares donde el dueño pagó o construyó la vivienda —
  `tipo_adqui` no en blanco (`tenencia` ∈ {3="la están pagando",
  4="propia, ya pagada"} principalmente; `tenencia` ∈ {1="rentada",
  2="prestada"} deja `tipo_adqui` en blanco porque la pregunta de
  financiamiento no aplica). Universo final = personas del panel
  retrospectivo cuyo `folioviv` cae en un hogar con `tipo_adqui` no
  blanco.
- **Ponderador NO localizado a nivel persona** en `historiavida.csv` ni
  `persona.csv` (ninguna de las dos trae `factor`/`fac_*`); el peso
  usado es el de **hogar** (`vivienda.factor`), heredado a la persona del
  panel vía `folioviv` — declarado, no inventado: el respondiente
  retrospectivo es (con rarísima excepción) uno por vivienda, y no hay
  peso de persona distinto en el payload.

**ENDIREH 2016** —
`data/raw/endireh2016/bd_mujeres_endireh2016_sitioinegi_csv.zip` (sha256
a reportar en COMMIT-2, `tools/medicion_familismo.py` lo calcula por
código). Tablas relevantes: `TB_SEC_IV.csv` (P4.8, dinero recibido),
`TB_SEC_XVIII.csv` (P18.4, cuidado de nietos/sobrinos), `TSDem.csv`
(demográficos, dominio urbano/rural). Las tres traen 111,256 filas —
universo completo de `bd_mujeres` (mujer elegida por vivienda).

- **Ponderador:** `FAC_MUJ`, presente en `TSDem.csv` y en las secciones
  temáticas (`TB_SEC_IV.csv`, `TB_SEC_XVIII.csv`) — citado directamente
  del header del CSV. Diseño: `EST_DIS` (estrato), `UPM_DIS` (UPM),
  también presentes en las mismas tablas.
- **Universo de ENDIREH:** `bd_mujeres` — mujeres 15+ (el propio nombre
  del payload y la ficha lo declaran; sin excepciones adicionales en este
  acto).

**Ningún ponderador quedó sin localizar — no aplica el PARO de (b).**

## (c) Operacionalizaciones (cerradas)

**θ binaria:**
- EDER: `vivienda.financia_8` == 1 (código `'8'` marcado en la batería
  multi-respuesta; blanco = no marcado = 0), dentro del universo
  `tipo_adqui` no blanco.
- ENDIREH: `p4_8_2` == 1 ∨ `p4_8_3` == 1 (códigos 1=Sí/2=No, sin códigos
  de no respuesta observados en el corpus — batería limpia).

**Desenlace binario de G5:**
- EDER: corresidencia con familiar adulto = 1 si alguno de {`padre_cor`,
  `madre_cor`, `hnos_cor`, `suegro_cor`, `suegra_cor`} == `'1'` ("Inicio
  corresidencia", código de evento del panel persona-año) en **cualquier
  fila** del historial de esa persona en `historiavida.csv`; 0 si
  ninguna lo es. `hij_cor_1..15` **excluidos** — corresidir con hijos
  menores no es "pooling" bajo la lectura del encargo, declarado
  explícitamente y no usado. **Decisión de agregación declarada, no
  prevista literalmente por el encargo:** `historiavida.csv` es un panel
  persona-año (no una fila por persona); el desenlace se colapsa a nivel
  persona tomando "alguna vez marcó inicio de corresidencia con ese tipo
  de familiar en su historia de vida reconstruida" — es la única forma
  de aplicar "= 1" literalmente (código `'1'` = "Inicio corresidencia")
  sobre una tabla longitudinal.
- ENDIREH: carga de cuidado = `p18_4` ∈ {1,2,3} ("cuida todos los días" /
  "algún día de la semana" / "de vez en cuando") = 1; `p18_4` == 4 ("No
  los cuida") = 0.

**Códigos de no respuesta excluidos, por variable:**
- `p18_4` (ENDIREH): excluidos código `5` ("No tiene" nietos/sobrinos —
  no aplica, no es "no respuesta" en sentido estricto pero tampoco mide
  carga de cuidado; universo distinto de quien sí tiene y elige nivel de
  cuidado), código `9` ("No especificado"), blanco (patrón de salto —
  no se le formuló la pregunta). Conteo exacto por código: ver
  `forense/notas/2026-08-31-familismo-cierre.md` §1 (producido por
  `tools/medicion_familismo.py`, no tecleado).
- `financia_8`/`p4_8_2`/`p4_8_3`: sin código de no respuesta observado en
  el corpus (baterías binarias limpias, blanco=no marcado en `financia_8`
  es una respuesta sustantiva —"no tuvo ese tipo de financiamiento"—, no
  una no-respuesta).
- Corresidencia (`padre_cor` etc.): sin exclusión de no-respuesta — el
  código `'1'` es un evento puntual dentro de un catálogo de estados de
  transición (`{1,2,3,7,60,70,73,90,91,92,93}`, ver `eder2017_fd.pdf`
  #30); no hay código 9/99/blanco reservado a no-respuesta en esta
  variable.

## (d) Estimador

Diferencia de proporciones ponderada del desenlace entre θ=1 y θ=0
(misma escala que ADR-220 — proporción [0,1], enlace identidad). Ambas
bases traen estrato (`est_dis`/`EST_DIS`) y UPM (`upm`/`UPM_DIS`) — el
IC95 se calcula **por diseño**, aproximado mediante bootstrap de
conglomerados (remuestreo de UPMs dentro de cada estrato, con
reemplazo), B=10,000, seed=42 — declarado como aproximación al IC por
diseño porque la caja no trae una librería de encuestas complejas con
linealización de Taylor; el remuestreo por UPM es la aproximación
estándar más cercana disponible con las herramientas del entorno.
Condicionamiento diagnóstico, un eje a la vez, celdas n≥30: sexo (solo
EDER — ENDIREH es universo de mujeres, sexo no varía), edad (ambas,
cuartiles 15-29/30-44/45-59/60+), urbano/rural (ambas: EDER
`tam_loc` 1-2=urbano/3-4=rural; ENDIREH `DOMINIO` U/C=urbano, R=rural).

## (e) B-bis

Signo ASIGNADO de G5.familismo_apoyo, `canon/modelo-decision-v4_0.md:459`:
**`familismo_apoyo 0.50`, positivo.** Concordancia o discordancia entre
el β̂ medido y este signo son ambas informativas, ninguna corrobora ni
refuta (ADR-57(a)) — mismo tratamiento que ADR-220/ADR-226 dieron a los
otros pares RUTA-A. IC que incluye 0 ⇒ sufijo `·NO-DISTINGUIBLE-DE-CERO`.
Signos discordantes entre EDER y ENDIREH ⇒ la primaria lleva sufijo
`·DISCORDANTE-ENTRE-INSTRUMENTOS` y ambas van en reserva. Regla de
escritura: solo la primaria (EDER) lleva `valor_ejecutable`; ENDIREH
queda en `reserva` como robustez — el resultado exacto (β̂, IC, n) de
ambos instrumentos se reporta en COMMIT-2, sin conocerlo aún al congelar
esta especificación.

---

**FALSADOR pre-registrado del acto:** si (a) marca PROXY en AMBOS
instrumentos, no se escribe `valor_ejecutable` ni entrada en
`coeficientes_generador_sellados` — solo la entrada de sección A con
rótulo PROXY.

el primer resultado que produzca este procedimiento es el que se reporta.
