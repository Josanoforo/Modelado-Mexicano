# Tarea D · Los cuatro D de PR #92, releídos contra el catálogo extendido

**Disciplina obligatoria, respetada en todo este documento:** este acto **no revierte ningún
veredicto**. El registro de `## Registro de veredictos archivados` de `hitoD-preregistro-v2_0.md`
es append-only y no se toca. Lo que sigue es evidencia para que mesa decida — se escribe
literalmente "la razón se sostiene" o "la razón no se sostiene", y nada más, por cada D.

## R4.1 → `D` — razón declarada (Nota 23, `hitoD-preregistro-v2_0.md:966`)

> "Ninguna fuente del catálogo construye la comparación antes/después que el Umbral exige
> (ENSANUT y ENIGH son ambas corte transversal, sin panel de acceso a salud anclado a un evento
> fechado)."

**Contraste contra el catálogo extendido:**

- **¿ESTAD ("ENSATD")?** No cambia la razón. ESTAD es transversal por establecimiento
  (`data/inventarios/inventario_fuentes_clase-fuente-mexico.md` #12), sin panel ni evento
  fechado propio — aporta un proxy de trato más fuerte para el confusor de la ficha, pero no
  construye el antes/después que la condición principal exige.
- **¿SINERHIAS?** Reporta capacidad instalada por unidad médica de forma semestral/anual desde
  hace años (`inventario_fuentes_clase-fuente-mexico.md` #2) — **en principio** podría fechar
  cuándo una unidad amplió consultorios o abrió, lo que serviría como "evento de mejora de acceso
  documentado". **No verificado en este acto** si sus series históricas por CLUES son
  públicamente descargables con la granularidad temporal necesaria (solo se confirmó la
  existencia del subsistema y su periodicidad, no el acceso a series retrospectivas por unidad).
  Queda como pista para un acto posterior, no como candidata resuelta.
- **¿La transición Seguro Popular→INSABI→IMSS-Bienestar como choque documentado?** Es un
  candidato genuino que la declaración original no consideró, y el precedente ya existe en este
  mismo corpus: `R5.1` (Nota 16) usó **corte transversal repetido** de ENIGH, no panel, para
  medir antes/después del choque de 2019 — el mismo tipo de diseño que R4.1 podría aplicar con
  las olas de ENSANUT (2018 vs. 2020-2024 Continua, que flanquean el arranque de INSABI en
  enero de 2020). **Reserva importante, no ignorada:** el Umbral de R4.1 habla de una mejora
  *local* de acceso (distancia y tiempo de espera a una clínica específica), y la transición
  INSABI/IMSS-Bienestar es un cambio *institucional* nacional de derechohabiencia, no
  necesariamente un cambio medible de distancia/tiempo de espera por localidad — no es el mismo
  tipo de evento que el Umbral describe literalmente.

**Veredicto de esta relectura:** **la razón se sostiene para la lectura literal del Umbral**
(panel o evento local fechado de apertura de clínica, con las tres fuentes del catálogo
extendido revisadas — ninguna lo construye). **La razón no se sostiene sin reserva** frente a una
lectura ecológica alternativa (corte transversal repetido de ENSANUT antes/después de
INSABI/IMSS-Bienestar), que la declaración original no consideró y que el precedente de R5.1
demuestra que es un diseño admisible para este corpus — sin que eso signifique que sea el diseño
que el Umbral de R4.1 pide literalmente. **No se adjudica aquí cuál lectura prevalece** — mismo
tratamiento que Notas 11-13 dieron a la ambigüedad de R7.2.

## R9.1 → `D` — razón declarada (Nota 23)

> "Sin variable de distancia en km (solo tiempo de traslado) y con exclusión estructural, por
> diseño del cuestionario de Utilizadores, de quien no consultó a nadie."

**Dos condiciones, verificadas por separado:**

1. **Distancia en km.** CLUES es una georreferenciación de establecimientos que el catálogo v1.0
   no tenía — **la razón declarada no consideró esta clase porque no existía en el catálogo al
   momento de escribirse.** Pero CLUES por sí sola no resuelve la condición: **no se confirmaron
   coordenadas GPS nativas** en el catálogo oficial (solo domicilio/localidad/municipio), y **no
   se verificó que ENSANUT libere la clave CLUES del establecimiento consultado en su microdato
   público** — sin esa llave, no hay forma de calcular una distancia persona-establecimiento real
   con las dos fuentes tal como están hoy. **La razón se sostiene con la evidencia verificada en
   este acto**, pero con una reserva declarada: si un acto futuro confirma (a) coordenadas
   geocodificadas de CLUES y (b) la llave CLUES en el microdato de ENSANUT, la razón dejaría de
   sostenerse. Ninguna de las dos piezas se verificó aquí — no se promueve sin abrir el
   instrumento.
2. **Población que no consulta a nadie.** Es un hueco de diseño de cuestionario (el Cuestionario
   de Utilizadores excluye por construcción a quien no buscó atención), no de clase de fuente
   faltante. Ninguna de las 6 clases nuevas aporta un instrumento que mida esta subpoblación con
   la variable de acceso objetivo que el Umbral pide. **La razón se sostiene sin reserva.**

**Veredicto de esta relectura:** **la razón se sostiene**, con una reserva explícita y acotada
sobre la condición de distancia (arriba) que un acto posterior podría cerrar si verifica
geocodificación y llave de enlace — ninguna de las dos está confirmada hoy.

## R4.3 mitad A → `D` — razón declarada (Nota 24)

> "...la única variable de adherencia en el catálogo entero (`A0313`, ENSANUT) es por
> entrevista, no por surtimiento."

**Contraste:** el barrido de la clase Registro administrativo (CLUES, SINERHIAS, SAEH, SINAVE)
no encontró ningún registro de dispensación/surtimiento de medicamento a nivel de paciente
individual — no existe en México, hasta donde este acto pudo verificar, un registro público de
receta electrónica o surtimiento farmacéutico enlazable a persona. **La condición que dispara el
`D` sigue siendo cierta**, verificada de nuevo contra el catálogo extendido, no solo contra el
original.

**Veredicto de esta relectura:** **la razón se sostiene.** Éste es el caso que el encargo mismo
advierte tratar distinto: el `D` salió de una fila que la propia ficha pre-declaró ("D si solo
hay adherencia auto-reportada") — es el pre-registro funcionando, no un error de búsqueda, y la
búsqueda de este acto no encontró nada que cambie esa condición.

## R4.3 mitad B → `D` — razón declarada (Nota 24)

> "...no existe variable de cuidadora en absoluto (más allá del proxy de corresidencia)."

**Contraste:** ninguna de las 18 fuentes nuevas del inventario de clase trae variable de
"cuidadora" o "persona a cargo del cuidado" de un adulto con padecimiento crónico — ni en
registro administrativo, ni en padrón, ni en las encuestas institucionales revisadas (ESTAD,
ENCAL). **La condición sigue siendo cierta.**

**Veredicto de esta relectura:** **la razón se sostiene**, mismo motivo que la mitad A — pre-
registro funcionando.

## R9.2 → `D` — razón declarada (Nota 25)

> "El Umbral exige cobertura baja Y abasto/campaña verificados por tercero; la segunda condición
> no tiene ninguna fuente en el catálogo completo — la única disponible (DGIS) es el propio
> prestador, excluida por la ficha misma."

**Contraste — el hallazgo más consecuente de este acto.** **Cero Desabasto**
(`inventario_fuentes_clase-fuente-mexico.md` #6) es exactamente el tipo de instrumento que la
declaración original buscaba y no encontró — **porque el catálogo v1.0 no tenía la clase
"transparencia/sociedad civil" en absoluto**, no porque se haya buscado y no exista. Verificado
en este acto: es independiente del prestador por diseño (recolecta reportes directos de
pacientes/personal, no del gobierno), y su cobertura declarada incluye explícitamente
**medicamentos, insumos, vacunas y anticonceptivos** — vacunas están dentro de su alcance.

**Lo que NO se verificó, y por qué esto no se adjudica como resuelto:**
- **Granularidad ambigua** — no se confirmó si Cero Desabasto reporta a nivel de entidad, unidad
  médica, o solo nacional agregado. Sin esa granularidad, no se puede evaluar si enlaza con la
  cobertura de vacunación de ENSANUT (que si es individual/hogar, necesitaría al menos
  granularidad de entidad×año de Cero Desabasto para un enlace ecológico).
- **"Alcance de campaña" específicamente, no solo "abasto".** El Umbral de R9.2 pide dos cosas:
  disponibilidad Y alcance de campaña. Cero Desabasto documenta reportes de desabasto (ausencia
  de producto) — no se confirmó que también documente fechas/cobertura geográfica de campañas de
  vacunación como evento programático, que es una pieza distinta de "hay o no hay medicamento".

**Veredicto de esta relectura:** **la razón declarada, tal como está escrita ("ninguna fuente en
el catálogo completo... la única disponible es el propio prestador"), NO se sostiene sin
reserva.** Existe al menos una fuente independiente del prestador (Cero Desabasto) que el
catálogo v1.0 no tenía clase para catalogar, y que cubre explícitamente vacunas dentro de su
alcance de desabasto. **La razón sí se sostiene, en cambio, para la pieza específica de "alcance
de campaña verificado por tercero"** — esa pieza no se confirmó que Cero Desabasto (ni ninguna
otra fuente de las 6 clases) la construya con la evidencia verificada en este acto. La condición
completa del Umbral (disponibilidad Y alcance, ambas por tercero) sigue sin cerrar limpio, pero
por un motivo distinto al que la nota original declaró.

---

## Lo que este documento no hace

No revierte `R4.1 → D`, `R9.1 → D`, `R4.3 → D` (ambas mitades), ni `R9.2 → D` — las cinco líneas
archivadas siguen exactamente como están en `## Registro de veredictos archivados` de
`hitoD-preregistro-v2_0.md`. No propone una fila nueva de veredicto. Lo que aporta es evidencia
verificada de que **una de las cinco razones (R9.2) fue producto del punto ciego del catálogo, no
solo de la ausencia real del fenómeno en México** — que es exactamente la distinción que el
módulo de auditoría de este encargo (§8) pide separar: qué es propiedad del mundo y qué es
propiedad de la búsqueda.
