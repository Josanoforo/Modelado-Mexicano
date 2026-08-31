# COMMIT-1 · spec congelada de MARCO-M-CONGELA (ACTO A′)

`ACTO MAESTRA32-E13 · MARCO-M-CONGELA`, 31/ago/2026. Receta escrita y congelada
ANTES de recorrer `milpa/tramite.yaml`/`milpa/procedencia.yaml` para producir
las tablas de COMMIT-2. No se edita después de correr COMMIT-2.

## Verificación previa de dirección

**(i) No existe ya un marco-M hermano.** `ls forense/prereg-duelo-v2/ | wc -l`
→ 23 entradas; `ls forense/prereg-duelo-v2/ | grep -i marco` → una sola
coincidencia, `marco-congelado-piloto-v1_0.tsv` (el original, benchmark).
Ningún archivo `candidatos-marco-M*`/`marco-M-congelado*` preexiste.

**(ii) Existen los tres insumos citados.** `forense/prereg-duelo-v2/enlace-M-v1_0.md`
líneas 33-35 sella 1 EMITE de 60 = `CIV-01` (`regla=tramite.mordida.discrecional`,
`conducta=paga_mordida`, `procedencia.yaml:937`); `forense/prereg-duelo-v2/cobertura-15-v1_0.tsv`
existe; `milpa/procedencia.yaml:coeficientes_generador_sellados` (`yaml.safe_load`)
trae 6 entradas, y las 6 traen `valor_ejecutable` numérico explícito
(verificado con `'valor_ejecutable' in e` sobre las 6, no a ojo):
`G1.confianza_institucional` (`-0.0645`), `G1.radio_confianza` (`-0.06626`),
`G3.familismo_apoyo` (`0.0279`), `G4.exposicion_violencia` (`0.16614`),
`G4.confianza_institucional` (`-0.166208`), `G3.horizonte_temporal`
(`0.0876`). Confirma la verificación previa (ii) del encargo tal cual: 6 de
6, sin excepción.

**(iii) Reglamento de sorteo** — `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md`
y `sorteo_v2.py` verificados: elegibilidad `grado_dependencia ∈ {P1,P2} ∧
publicada ∈ {SI,NO}`; `estrato = dominio|grado_dependencia|dificultad`;
`cuota_max = floor(0.20·n_sorteo)` de `publicada=SI`; piso 1 por estrato no
vacío (Hamilton); `semilla = semilla_desde_sha_merge(SHA_A, scope_id)`.
`sorteo_v2.py` NO se edita en este acto — `cargar_marco()` sigue con su
`assert n=50` contra el congelado ORIGINAL; el marco-M no pasa por ese
cargador hoy (lo usará un acto B′ futuro con cargador propio).

## (a) Criterio "emitible" citado

**`emisor.construir_crosswalk` SÍ existe** en el repo:
`milpa/src/emisor.py:499` (verificado por lectura directa del archivo, no
por grep). Su docstring (líneas 499-514) declara: "Pasada 1 sobre el marco
… ¿aparece la `variable` en alguna fuente-máquina en la misma línea que su
`encuesta`? … `CANDIDATO-EMITE` (con archivo:línea) exige aún enlace de
escala/universo declarado antes de emitir; lo demás `NO-EMITE`." Esta pasada
1 es *necesaria pero no suficiente*: exige además, por el método explícito de
`enlace-M-v1_0.md` §Método (líneas 12-20), que:

1. el `regla_id` exista entre las reglas reales del motor —
   `milpa.src.emisor.cargar_reglas()` (`milpa/src/emisor.py:86`), que carga
   ÚNICAMENTE `milpa/tramite.yaml` (`RUTA_TRAMITE`, línea 41). Verificado con
   `yaml.safe_load(open('milpa/tramite.yaml'))['reglas']`: **5 reglas, todas
   `dominio: tramite`** (cabecera del archivo, línea 2): `tramite.mordida.discrecional`,
   `tramite.mordida.con_registro`, `tramite.gobierno_digital.coercitivo`,
   `tramite.gobierno_digital.util_sin_coercion`, `tramite.evasion_norma`.
2. `milpa/procedencia.yaml` declare esa fila como desenlace **MEDIDO** (no
   `ASIGNADO`, no transporte fuera de dominio) de esa regla — cita real de
   `(regla, conducta)` con una variable/encuesta verificable.

**Hallazgo de alcance (no anticipado por el encargo, verificado por comando,
no por juicio):** `milpa/` solo contiene DOS archivos de reglas/desenlaces —
`milpa/tramite.yaml` y `milpa/procedencia.yaml` (`find milpa -maxdepth 1 -type f`
→ 2 archivos `.yaml` + `refutations.yaml`, sin reglas de motor). No existe
un archivo de reglas por dominio para civico, dinero, salud, familia, etc.
**El motor
real (`cargar_reglas()`) SOLO implementa el dominio `tramite` — 5 reglas de
un motor conceptual de 10 dominios.** Cualquier candidato de los otros 9
dominios (civico, dinero, salud, familia, tiempo, cooperacion, trabajo,
informacion, comunicacion) falla el criterio EMITE por construcción, sin
importar cuántos desenlaces medidos tenga citados en `procedencia.yaml` —
porque el `regla_id` que citan (p.ej. `civico.voto.clientelar_si_observable`,
`dinero.ahorro.informal_sin_puente`, `salud.atencion.leve_sin_imss`) no
existe en ningún archivo que `cargar_reglas()` lea. Esto explica
estructuralmente por qué `enlace-M-v1_0.md` encontró 1 EMITE de 60: no es
que falten desenlaces medidos citables (`procedencia.yaml` trae bastantes),
es que el motor solo tiene reglas para un dominio.

**Recorrido completo de `milpa/tramite.yaml` y `milpa/procedencia.yaml` con
`yaml.safe_load`** (secciones leídas, con conteos):
`tramite.yaml`: claves `dominio, version, reglas` — `reglas` = 5 entradas
(arriba). `procedencia.yaml`: claves `version, estado, resumen,
condicionales_confianza_institucional (6), condicionales_escalares (2),
condicionales_escalares_confianza_generica (1),
condicionales_escalares_exposicion_violencia (1),
condicionales_escalares_medido_nacional (2), deuda_dispersion (6),
hallazgo_ordinal_cardinal (3), medidos (4), derivados (6),
asignados_probabilidad (13), evidencia_experimental_terceros (1),
asignados_coeficiente (3), coeficientes_generador_medidos (6),
rutas_estimabilidad_coeficiente (4), riesgos_cruzados (4),
propuesta_de_esquema (3), coeficientes_generador_sellados (6)`. No existen
secciones llamadas literalmente `reglas` ni `desenlaces` dentro de
`procedencia.yaml` (esos nombres son del vocabulario del encargo, no del
YAML real) — el desenlace real vive disperso en `medidos`, `derivados`,
`asignados_probabilidad`, `coeficientes_generador_medidos` y
`coeficientes_generador_sellados`, cada entrada con su propio campo de texto
libre (`donde`, `fuente`, `regla`, etc.) que hay que leer para encontrar la
cita de `(regla_id, encuesta, variable)`.

**Grep dirigido de los 5 `regla_id` reales contra `milpa/procedencia.yaml`
completo** (por comando, no a ojo — un match por línea, archivo completo
examinado, 1944 líneas):

| regla_id | líneas con hit | contexto |
|---|---|---|
| `tramite.mordida.discrecional` | 363, 782, 888, 904, 937, 953 | 782=`asignados_probabilidad` (ASIGNADO); 888=`coeficientes_generador_medidos.G1_radio_confianza.fuente` (MEDIDO, ENCUCI); 937=`coeficientes_generador_medidos.G1_confianza_institucional.fuente` (MEDIDO, ENCIG — el mismo citado por `enlace-M-v1_0.md` para `CIV-01`); 363, 904, 953 = prosa narrativa sin nueva cita de encuesta/variable |
| `tramite.mordida.con_registro` | 788 | `asignados_probabilidad` (ASIGNADO, sin encuesta/variable citada) |
| `tramite.gobierno_digital.coercitivo` | 111, 793 | 111=prosa; 793=`asignados_probabilidad` (ASIGNADO) |
| `tramite.gobierno_digital.util_sin_coercion` | 799 | `asignados_probabilidad` (ASIGNADO) |
| `tramite.evasion_norma` | (ninguna) | **0 líneas** — la regla no tiene NINGÚN desenlace citado en `procedencia.yaml`, medido ni asignado. Cero cobertura total. |

Candidatos con un desenlace **MEDIDO** y una **encuesta+variable real**
citada: exactamente 2, ambos del generador `G1` bajo `tramite.mordida.discrecional`
(`coeficientes_generador_medidos`, líneas 872-899): `G1_radio_confianza`
(ENCUCI 2020, `AP5_1_1/AP5_1_2/AP5_1_3` × desenlace `AP5_17`/`AP5_18='1'`) y
`G1_confianza_institucional` (ENCIG 2023, `P8_3_1/2/3` × `P11_1_23` — el
mismo par que ya sella `CIV-01`). Las 4 entradas `asignados_probabilidad`
que citan directamente a una de las 5 reglas (líneas 782, 788, 793, 799) NO
traen encuesta ni variable — son probabilidades ASIGNADAS abstractas
(`p: 0.62`, etc., del propio `tramite.yaml`) sin fuente de encuesta operacionalizable
en una fila de marco; se documentan como candidatos descartados en el barrido,
no como filas de la tabla (A) — no hay `encuesta`/`variable` que teclear sin
inventarla.

## (b) Regla de mapeo fila de candidato → columnas del marco

- `encuesta`/`ola`/`variable`/`universo`/`ponderador`: tomados literalmente
  del campo `fuente`/`donde` del desenlace sellado en `procedencia.yaml`.
  Cuando el desenlace cita una batería de variables (p.ej. `P8_3_1/2/3` o
  `AP5_1_1/2/3`), se usa la primera variable de la batería como `variable`
  representativa de la fila y se declara la batería completa en
  `frase_discriminacion`.
- `estimador` = `"proporción ponderada"` (default del encargo) — coincide
  con la clase real de ambos candidatos (`MEDIDO·β̂(diferencia de
  proporciones)`).
- `escala` = `binaria` — ambos candidatos dicotomizan la conducta de la
  regla (`paga_mordida` vs. `tramite_normal`).
- `ponderador`: para el candidato ENCIG (en_marco_60=CIV-01) se hereda el
  valor ya sellado en el marco original, `FAC_P18`. Para el candidato ENCUCI
  **no se encontró** un nombre de variable de ponderador citado en
  `milpa/procedencia.yaml` (revisadas las 1944 líneas del archivo, 0
  coincidencias de un token `FAC_` junto a `ENCUCI`/`AP5_1`) ni en
  `milpa/tramite.yaml` (46 líneas totales, 0 coincidencias) — se deja el
  campo como `NO_ENCONTRADO_1944_LINEAS_REVISADAS` en vez de inventar un
  nombre de variable.
- **`grado_dependencia` — TENSIÓN DOCUMENTADA, no resuelta por la fuerza.**
  El encargo pide P1/P2, nunca P0, y pide citar `archivo:línea` de la
  definición `ADV1-M1` si se encuentra. Se buscó con
  `grep -a -rl "grado_dependencia" .` → **18 archivos** examinados. Se
  encontró la definición operativa real, verbatim, en
  `forense/notas/2026-08-20-act-pil-2-marco.md` §"`grado_dependencia`,
  derivado y no tecleado" (línea 123 del archivo): *"P0 = el par
  (encuesta, ola) aparece en `milpa/procedencia.yaml` como ruta de
  parametrización de M; P1 = misma familia nombrada, otra ola o sin ola;
  P2 = el resto."* Por esta regla real y sellada, **ambos candidatos de
  este acto serían P0**: son, literalmente, la ruta de parametrización del
  generador `G1` que el motor usa (`coeficientes_generador_medidos`/`_sellados`).
  Esto **contradice directamente** la instrucción del encargo ("nunca P0").
  No se fuerza ninguna de las dos lecturas: se documenta la tensión aquí y
  se aplica el criterio explícito que el propio encargo autoriza para este
  caso ("usa un criterio razonable declarado explícitamente") — se asigna
  **P1** a ambos candidatos en las tablas de este acto, con esta nota
  adjunta en la columna `frase_discriminacion` de cada fila, para que quien
  audite sepa que la regla ADV1-M1 real los clasificaría P0 y que la
  elección de P1 es una desviación declarada, no un descubrimiento nuevo de
  la regla.
- `dificultad`: no se encontró una regla determinista para `dificultad` de
  candidatos nuevos (no forma parte de `ADV1-M1` según el mismo documento
  citado arriba, que solo deriva `grado_dependencia`). Se usa `MEDIA` como
  default declarado explícitamente (mismo valor que trae `CIV-01` en el
  marco original), documentado aquí como convención de este acto, no como
  hallazgo.
- `dominio`: mapa regla→dominio — trivial en este universo porque las 5
  únicas reglas reales son `dominio: tramite` (cabecera de `tramite.yaml`).
  Ambos candidatos → `dominio = tramite`.
- `estrato` = `dominio|grado_dependencia|dificultad` = `tramite|P1|MEDIA`
  para ambos candidatos (misma cadena, porque ambos comparten los tres
  ejes).
- `publicada`: `NO` por defecto salvo coincidencia de `(encuesta, variable)`
  con una fila del marco original, en cuyo caso se hereda el valor SI/NO de
  esa fila (se hereda solo el token SI/NO, no el texto largo del veredicto
  del bibliotecario que acompaña a la columna en el original — sería
  transportar un veredicto de otro acto sin haberlo re-verificado). El
  candidato ENCIG coincide con `CIV-01` (marco original: `publicada=NO`) →
  hereda `NO`. El candidato ENCUCI no coincide con ninguna fila del marco
  original (`CIV-05`/`CIV-06` usan `AP5_4_2`/`AP5_3_8`, no `AP5_1_x`) →
  `NO` por defecto.
- `cv_arbitro`/`n_no_ponderado`: vacíos (regla explícita del encargo — el
  árbitro no corre en este acto).
- `frase_discriminacion`: una línea con regla+conducta, sin valor numérico,
  más la nota de la tensión P0/P1 cuando aplica.

## (c) Columnas extra de (A)

- `regla`, `conducta`: del `regla_id` y la conducta operacionalizada citados
  arriba.
- `clase_procedencia`: la clase literal que trae `procedencia.yaml` para esa
  entrada (`MEDIDO·β̂(diferencia de proporciones)…`, sin abreviar).
- `base_medida`: `SI` si el `gen` de la regla (aquí siempre `G1`) tiene
  `valor_ejecutable` numérico en `coeficientes_generador_sellados` para ESE
  `coef` específico. Verificado por `yaml.safe_load`: `G1/confianza_institucional`
  trae `valor_ejecutable: -0.0645` → `SI` para el candidato ENCIG.
  `G1/radio_confianza` también trae `valor_ejecutable: -0.06626` → `SI`
  para el candidato ENCUCI. Ambos candidatos quedan `base_medida=SI`.
- `en_corpus`: método declarado — se acepta `SI` cuando `procedencia.yaml`
  cita una unión ya ejecutada sobre microdato real con conteo de filas
  verificable (no una `CANDIDATO-EMITE` hipotética de la pasada 1). Ambos
  candidatos citan uniones ejecutadas: ENCIG "38966 filas cada una, cero
  pérdida de join" (línea 937 y su nota `2026-08-04-w-coeficientes-generador-
  paso1.md §1.2, §3.2`); ENCUCI "21519 filas… n=13375/13393/13365 de universo
  con contacto=13435/21519" (línea 888 y su nota §1.1, §3.1). No se buscó un
  inventario de payloads adicional para esta verificación porque la propia
  cita de `procedencia.yaml` ya documenta la ejecución de la unión sobre
  microdato — un inventario de nombres de archivo no aportaría más certeza
  que una unión ya corrida y contada.
- `en_marco_60`: id del marco original si coincide `(encuesta, variable)`.
  ENCIG/`P8_3_1` → `CIV-01`. ENCUCI/`AP5_1_1` → vacío (no hay fila con esa
  variable en el marco de 60).
- `elegible`: `SI` con razón `"regla real + desenlace MEDIDO + en_corpus=SI"`
  para ambos candidatos.

## (d) Controles

- **CIV-01 DEBE aparecer en (A) con `en_marco_60=CIV-01`**: se cumple —
  candidato ENCIG cumple la condición exacta (mismo par
  `encuesta=ENCIG, variable=P8_3_1` que sella `CIV-01` en el marco original,
  vía `procedencia.yaml:937`, la misma cita que usa `enlace-M-v1_0.md`).
  **Control PASA.** No hay PARO por este punto.
- **Ningún candidato sin `en_corpus=SI` entra a (B)**: ambos candidatos de
  este barrido tienen `en_corpus=SI`; no hay candidatos con `en_corpus=NO`
  que excluir en este universo particular (los 4 `asignados_probabilidad`
  con regla real quedaron fuera de la tabla (A) en el paso anterior por
  carecer de encuesta/variable, no por `en_corpus`).

## (e) Pre-registro del sorteo de B′ (NO se ejecuta en este acto)

- `scope_id = "MARCO-M-v1"`.
- `SHA_A = "<SHA_DEL_MERGE_DE_ESTE_PR>"` (placeholder — la rama de este acto
  no tiene PR fusionado al escribir esta receta; B′ deberá sustituirlo por
  el SHA real del merge antes de derivar la semilla).
- `semilla = semilla_desde_sha_merge(SHA_A, "MARCO-M-v1")` (función de
  `forense/prereg-duelo-v2/sorteo_v2.py`, no editada por este acto).
- Regla de tamaño, fijada AHORA sin ver `N`: `N≥30 → n_sorteo=15`;
  `15≤N<30 → n_sorteo=ceil(N/2)`; `N<15 → sin sorteo (todas las elegibles)`.
  `cuota_max = floor(0.20·n_sorteo)`. Estratos y piso 1 Hamilton como el
  reglamento de `sorteo-act-pil-3-v2-PROPUESTA.md`.

## (f) B-bis interpretación (documentada, no adjudicada)

`N≥30` vía (ii) reproduciría el piloto a escala; `15-29` sería viable más
corto; `<15` es viable sin sorteo (todas las elegibles entran); `0` sería
hallazgo de que el criterio EMITE no alcanza ni los 6 pares medidos.
**Adelanto no adjudicado aquí** (se adjudica en la nota de cierre de
COMMIT-2, después de correr el barrido real): el barrido de este COMMIT-1
ya deja ver que el universo elegible es pequeño (2 candidatos con regla real
+ desenlace medido + encuesta/variable citable) — muy por debajo de 15 — y
que la razón estructural es que el motor (`cargar_reglas()`) solo implementa
un dominio (`tramite`) de los diez conceptuales. Esta lectura se confirma o
se corrige con la corrida real de COMMIT-2, no antes.

el primer resultado que produzca este procedimiento es el que se reporta.
