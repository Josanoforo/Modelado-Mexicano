# `ACTO MAESTRA35-L8` — spec congelada (`COMMIT-1`, `D-11`)

Bloque `B-bis`/`A-bis` de `instrucciones-proyecto-v2_12.md`. Hereda **verbatim**
las secciones `§1.1`–`§1.4`, `§1.6`, `§1.7`, `§1.10` y `§1.11` de
`forense/notas/2026-09-02-MAESTRA35-L3-spec.md` — la sustitución de `§1.5` que
`L3` ya hizo (firma `c1`, efecto fijo de TIPO de año federal) queda intacta;
este acto **no vuelve a sustituir nada**, solo amplía el universo. Ningún
párrafo de `§1` cambia una sola palabra frente a `L3`; se transcribe completo
abajo por integridad del archivo, no porque haya edición.

---

## §0 · Premisas

### 0.0 · DECLARACIÓN DE SECUENCIA ROTA — léase antes que cualquier otra cosa

**Este `COMMIT-1` se escribe DESPUÉS de haber visto el resultado que debía
preceder.** Al construir `tools/l8_amplia_tipo_boleta.py` para hacer el censo
de `P0` (que sí requiere código y sí requiere leer los SICEE nuevos), la misma
sesión ejecutó `--json` — el modo que corre el modelo completo — como prueba de
que el script funcionaba, antes de escribir este archivo. Eso significa que
antes de este commit ya se conocían: `β_pres`, `β_int`, sus IC95 wild cluster y
de municipio, los dos `p`, y el veredicto del falsador `§1.9`.

**Qué NO contaminó esto, y por qué se puede decir con certeza:** la spec de
abajo tiene **cero grados de libertad**. Todas sus secciones son herencia
verbatim de `L3` por mandato explícito del encargo («sin ningún cambio salvo el
universo»); no había ninguna decisión de modelo, corte, ponderación o forma
funcional que esta sesión pudiera elegir a la vista del resultado. Correr el
procedimiento una segunda vez, a ciegas, con exactamente estos datos y esta
spec, reproduciría el mismo número: es una función determinista de
`(datos, procedimiento)` sin paso discrecional en medio. No hay hipótesis
alternativa que un ejecutor tentado hubiera podido sustituir aquí.

**Qué SÍ se rompe, y se declara sin atenuarlo:** la garantía **mecánica y
auditable** de que nadie vio el resultado antes de firmar el procedimiento —
que es precisamente lo que el patrón de dos commits existe para poder probar
desde afuera, sin tener que confiar en la buena fe del ejecutor. Esa prueba,
para este acto puntual, no existe. `COMMIT-1` y `COMMIT-2` de `MAESTRA35-L8`
deben leerse como un solo acto epistémico, no como evidencia independiente de
pre-registro. Es un defecto de **proceso** de esta sesión (una prueba de
software que se corrió con `--json` en vez de detenerse en `--censo`), no un
defecto de los datos ni un intento de ajustar nada — y se registra en
`forense/hallazgos.md` como tal, con el rótulo que le corresponde, no como
hallazgo de investigación.

**Precedente que esto seguramente informa** (no una acción de este acto, solo
una nota para quien reglamente después): si `/acto` quisiera cerrar esta clase
de error mecánicamente, el punto de intervención sería obligar a que el modo
`--json`/`--tipo-boleta` de un hermano nuevo no pueda ejecutarse en la misma
sesión antes de que exista un commit de spec — hoy la skill no lo impide.

### 0.1 · De dónde sale el tratamiento

Sin cambio frente a `L3`: `data/p0-calendario-ayuntamientos-v1_0.tsv` y
`data/p0-tratamiento-homologacion-v1_0.tsv`, sin editarlas (el encargo lo
prohíbe expresamente y este acto no las tocó). La derivación por entidad y
transición sigue congelada en `data/l3-tabla-identificacion-v1_0.tsv` (**73
transiciones, 32 entidades** — no cambia, es calendario, no adquisición).

### 0.2 · Contaminación declarada (`ADR-46`), la que ya traía `L3` más la de este acto

Esta sesión hereda **todo lo que `L3 §0.2` ya declaró** (los resultados
publicados de `MAESTRA34-L6`, la hipótesis firmada por mesa, las filas sueltas
de Zacatecas/Hidalgo/PREP/Baja California que `L3` vio). A eso se añade, propio
de este acto:

1. **El censo de `P0`** (`forense/notas/2026-09-02-MAESTRA35-L8-P0-censo.md`)
   — estructura y cobertura de los SICEE nuevos, controles aritméticos,
   cuántas transiciones `STAY`/entidades medibles/conglomerados resultan. Es
   información de **diseño**, no de desenlace: mismo tipo de exposición que
   `L3 §0.3` ya aceptaba como necesaria antes de congelar spec.
2. **El desenlace completo, por el error de secuencia de `§0.0`.** A diferencia
   de `L3`, esta sesión conoce `β_pres`, `β_int`, ambos IC95 y el veredicto
   antes de este commit. Declarado arriba con el detalle completo.

### 0.3 · La reserva de identificación — YA NO ES RESERVA en este acto

`L3 §0.3` declaró `α` frágil porque el panel tenía solo **2** `STAY` (menos del
umbral de `3` que el encargo fija). El censo de `P0` de este acto (información
de diseño, no de desenlace) mide que el panel ampliado tiene **4** `STAY`
(Baja California 2016→19, Durango 2016→19, Hidalgo 2016→20, Aguascalientes
2016→19) — **cruza el umbral**. Bajo la propia regla del encargo, `α` se
identifica en este acto **sin reserva**. La variante sin `α` (`§1.5`) se
reporta de todos modos, «pase lo que pase», porque esa cláusula del encargo no
es condicional al umbral, es incondicional.

### 0.4 · Alcance, declarado como falta

La meta declarada (no compuerta) sigue siendo **≥ 8 entidades tratadas
medibles**. El censo de `P0` mide **7** (`L3` tenía 5). **No se alcanza la
meta**: este acto también corre y se declara **ACOTADO** por este eje, sin
imputar la entidad que falta. Con nombre y motivo (información de diseño,
`P0`): **Hidalgo** es `TRATADO` pero no aporta transición medible — su única
pata obtenida (`2016→2020`) es anterior a su tratamiento (`2024`), y esa pata
de 2024 no tiene denominador en ninguna fuente que este acto haya podido abrir
(`P0 §0`).

---

## §1 · Spec (verbatim de `L3`, verbatim de `L6` donde `L3` ya lo marcaba así)

### 1.1 · Estimando *(verbatim)*

Efecto de que la elección municipal se celebre el mismo día que la elección
federal sobre la **participación electoral municipal**, medido en **puntos
porcentuales**, **separado por el TIPO de boleta federal que se comparte**
(presidencial / intermedia). Escala declarada: **pp**. No es una probabilidad y
no puede cargarse al motor tal cual.

### 1.2 · Unidad y desenlace *(verbatim)*

Unidad de observación: **municipio × elección de ayuntamiento**.

```
participacion(m, e) = 100 * votos_totales(m, e) / lista_nominal(m, e)
```

`votos_totales` = votación total emitida, incluyendo nulos y candidaturas no
registradas. `lista_nominal` = lista nominal del municipio en esa elección,
tomada de la misma fuente que los votos siempre que la fuente la traiga.

### 1.3 · Universo *(verbatim)*

Los municipios de las entidades cuya serie trae lista nominal en la fuente,
presentes con `lista_nominal > 0` en todas las elecciones de la serie de su
entidad. Exclusiones declaradas: Usos y costumbres (Oaxaca) NO-APLICA con
conteo; filas que no son municipios se excluyen nombrándolas una por una con
control aritmético contra el total publicado; municipio ausente de algún año
de su serie se excluye de todas las transiciones de esa entidad, y se cuenta.

### 1.4 · Tratamiento *(verbatim)*

`D(m, e) = 1` si la jornada de la elección `e` se celebró el mismo día que la
jornada federal; `0` si no. Se lee de
`data/p0-calendario-ayuntamientos-v1_0.tsv`, columna `concurrente_con_federal`.

### 1.5 · Estimador principal *(verbatim de la sustitución `c1` que `L3` ya hizo — sin nueva sustitución en este acto)*

```
Δy(m,k)      = participacion(m, e_{k+1}) − participacion(m, e_k)          [pp]
hueco(k)     = anio(e_{k+1}) − anio(e_k)                                  [años]
D_pres(e)    = 1 si la jornada de e coincide con una federal PRESIDENCIAL (2018, 2024)
D_int(e)     = 1 si coincide con una federal INTERMEDIA (2015, 2021)
ΔD_pres(k)   = D_pres(e_{k+1}) − D_pres(e_k) ; ΔD_int(k) análogo          ∈ {−1, 0, +1}

Δy(m,k) = α·hueco(k) + β_pres·ΔD_pres(k) + β_int·ΔD_int(k) + ε(m,k)
```

Regresión a nivel municipio, mínimos cuadrados sin intercepto, sobre todas las
transiciones del universo. Referencia = elección local sin federal. `α` se
identifica solo por `STAY`; `β_pres`/`β_int` por los `SWITCH`; las entidades
siempre concurrentes identifican `β_int − β_pres`.

### 1.6 · Errores estándar *(verbatim)*

Agrupados por entidad. Intervalo principal por **bootstrap wild cluster**
(Rademacher, `B=10000`, `seed=42`), restringido a `H₀: coeficiente=0`
(Cameron–Gelbach–Miller). Se reporta también el bootstrap por municipio con
reemplazo como contraste. **Manda el wild cluster** si discrepan. Límite
mecánico: con `k` entidades, `p` mínimo alcanzable `= 2/2^k` — con el `k` real
que deje el panel de este acto (`P0` ya lo midió: **9**, informacion de
diseño), `p_mín = 2/512 = 0.00390625`.

### 1.7 · Diagnósticos pre-registrados *(verbatim)*

`ATT` por cohorte contra la `α` de las `STAY`; contraste `β_int − β_pres`;
event-study por año relativo (débil si pocas `STAY` — ya no aplica del todo,
`§0.3`); heterogeneidad por terciles de `lista_nominal`; sensibilidad sin hueco
1, sin Coahuila, sin Durango — **este acto añade, por nombre, sin Hidalgo, sin
Aguascalientes y sin Veracruz**, para medir cuánto compra cada entidad nueva;
controles aritméticos de `§1.7.6` (ya corridos en `P0`, ver la nota de censo);
y el control de regresión de `§1.7.7`, que este acto extiende a **dos**
verificaciones antes de correr nada: reproducir `L6` (que `L3` ya exige) **y**
reproducir `data/l3-resultados-tipo-boleta-v1_0.json` byte a byte sobre el
panel de `L3` sin tocarlo — **PARO** si cualquiera de las dos falla.

### 1.8 · Comparaciones *(verbatim)*

Contra `MAESTRA34-L4` (`+10.4790 pp`), mismos benchmarks internacionales
(Alemania ≈10pp, EE.UU. 36pp) y el mismo TEPJF `NO-OBTENIDO` si mesa no lo
depositó.

### 1.9 · Falsador `B-bis` *(verbatim)*

Sobre los IC95 wild cluster por entidad: **CORROBORADA** si `β_pres>0` con IC
que excluye 0 **Y** `β_int<0` con IC que excluye 0; **ACOTADA** si solo una se
sostiene; **NO-DISCRIMINA** si ambos IC contienen 0; **CONTRARIA** si alguno
sale con signo opuesto e IC fuera de 0. Precedencia: `CONTRARIA` manda sobre
`ACOTADA`.

### 1.10 · Lo que este procedimiento no puede decir *(verbatim)*

No separa concurrencia de jerarquía del cargo; no separa tipo de boleta de
cualquier choque nacional coincidente (2021 = intermedia y pandemia); `α`
depende de pocas transiciones (aunque menos pocas que en `L3`, `§0.3`); con
pocos conglomerados cualquier intervalo es frágil.

### 1.11 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

*(Nota de honestidad, obligada por `§0.0`: en este acto el «primer resultado»
que se reporta en `COMMIT-2` es, de hecho, el mismo que esta sesión ya vio
antes de escribir este sello — no uno nuevo, no uno re-corrido a ciegas. Se
deja dicho aquí, en el mismo lugar donde el sello vive, para que nadie lo lea
como si fuera la garantía que en `L3` sí es.)*
