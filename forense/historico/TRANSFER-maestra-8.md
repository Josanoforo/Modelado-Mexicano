> ⚠️ **DOCUMENTO MUERTO — el estado vive en `estado`.** Movido a `forense/historico/` el 29/jul/2026 (sesión de correcciones); declara estado que ya no es cierto y contiene, en su lista de "seis cifras que cayeron el mismo día", la refutación infundada del caso "pelón" citada como ejemplo de método — ver la retractación en `forense/notas/2026-07-29-b-correccion-perimetro.md §9`. No se edita más abajo de esta línea.

Retomo el programa "Psicología del Mexicano Contemporáneo". Cierre de la
sesión del 29 de julio de 2026. Léela sin dar nada por sabido de sesiones
anteriores — es autocontenida.

═══ HEAD ACTUAL ═══
`8254fde` en `main`. Verificado con `git log --oneline -1` justo antes de
escribir esto.

Commits de hoy, en orden:
  09bfb05  Corrige byte UTF-8 truncado en CONTRIBUTING.md (bloqueaba T03)
  9301e59  Nota forense: auditoría de perímetro T07-T10 y verificación T09/T10
  a79227e  Nota forense: verificación del perímetro y cobertura del pre-registro
  7d6535e  estado v1.8: corrige "cubre las 27" y registra la auditoría de perímetro
  8254fde  Añade TRANSFER-maestra-7.md (documento de traspaso, estaba fuera del repo)

⚠️ Ninguno de los cinco sale firmado en GitHub (Unverified). No es del
trabajo: la clave de firma SSH de este entorno está configurada pero vacía
(0 bytes). Ya afectaba a `9301e59`, que no es de esta sesión.

═══ ESTADO DE LA SUITE ═══
`python3 tests/check.py` corrido sobre `8254fde`: **18 FAIL · 109 WARN.**

⚠️ **No son 107.** La cifra de 107 (reproducida hoy en Windows 11/Python 3.14
contra la corrida original en Linux, desglose por test idéntico) es la del
árbol **antes** de commitear `TRANSFER-maestra-7.md`. Ese archivo introduce
2 WARN propios de T03 (cita `-v3.2.md` y `-v3_2.md`, que no existen como
nombres de archivo — el mismo defecto que el propio documento describe como
"falso positivo declarado" en su línea 49). Verificar con
`python3 tests/check.py` antes de citar cualquiera de las dos cifras: ambas
son reales, corresponden a árboles distintos.

Los 18 FAIL no cambiaron en toda la sesión — nada de lo escrito hoy tocó
`corpus/`, `canon/modelo`, `glosario` ni `integrador`, que es de donde salen.

═══ QUÉ SE CERRÓ HOY ═══

1. **Auditoría de perímetro de T07–T10** (`9301e59`, de una sesión anterior
   el mismo día). Documenta que T07–T10 solo cubren `corpus/reports/*.md` —
   no `canon/`, `corpus/forense/`, `forense/` ni `milpa/` — y que ampliar T10
   sobre el motor encuentra 4 defectos de medida propios de T10 más 1 defecto
   real: `integrador:174` presenta a Arciniega/Castillo/Wheeler como
   "Evidencia a favor" con tier `Sólido` sin marca de procedencia, mientras
   el caveat de diáspora vive en `integrador:175`, la sección opuesta. El
   tier se asigna sin la marca; la marca llega como límite.

2. **Verificación de la hipótesis de perímetro 20/27** (`a79227e`). El
   encargo de hoy planteaba que "el motor usa 7 etiquetas de tier donde el
   canónico define 4, y el perímetro fuerte es 20 o 27 según dónde caiga la
   raya". Se verificó con la salida real de T12 (`tests/check.py`, no
   `grep` sobre el archivo entero): el motor tiene 49 reglas —
   `20 [FUERTE] · 19 [MEDIA] · 5 [MEDIA-FUERTE] · 2 [HIPÓTESIS] ·
   1 [FUERTE como correlación] · 1 [FUERTE / MEDIA] · 1 [MEDIA / HIPÓTESIS]`
   — y el perímetro es exactamente **27** (20+5+1+1), sin ambigüedad, contra
   `gobernanza-v1_8.md:266` (ADR-37). **La ambigüedad se retira: nunca existió
   en el motor real.** Sí sigue abierto que ningún test vigila el vocabulario
   de tier *dentro* del motor — T07 solo audita `corpus/reports/`.

3. **Hallazgo nuevo, no buscado: el pre-registro del Hito D cubre 24 de 27,
   no 27 de 27.** Verificado al confirmar la membresía del perímetro:
   `hitoD-preregistro-v2_0.md` tiene 24 encabezados `## R`
   (18 `[FUERTE]` + 4 `[MEDIA-FUERTE]` + las 2 compuestas), no 27 como
   afirman tres artefactos distintos (`hitoD-preregistro:8`,
   `hitoD-preregistro:13` y `estado` en su v1.7, §7). **Faltan exactamente
   las 3 reglas de perímetro de `modelo §3.3`** (autoridad, trámite y
   relación con el Estado): las dos `[FUERTE]` de trámite/mordida y la
   `[MEDIA-FUERTE]` de gobierno digital coercitivo. `R3.4` —la regla del
   gate de Fase 1, que ADR-37 declaró desbloqueada el 28/jul— se nombra en
   el cuerpo del pre-registro pero **no tiene ficha propia**. Detalle
   completo con las tres reglas citadas textualmente en
   `forense/notas/2026-07-29-b-correccion-perimetro.md §4`.

4. **`estado` sube a v1.8** (`7d6535e`). Corrige en §7 la afirmación
   "cubre las 27" a "cubre 24 de 27"; cierra en §4·S2 una deuda documental
   que llevaba abierta desde antes de ADR-37 ("¿20 o 26?", citando ahora
   `gobernanza:266`); añade el hueco del pre-registro, el vocabulario de
   tier del motor y la disyuntiva T10-vs-integrador, todas como deuda
   abierta, sin resolverlas.

5. **`TRANSFER-maestra-7.md` entra al repo** (`8254fde`), tal cual, sin
   editar — es el documento de traspaso con el que se retomó el programa
   tras migrar de Claude project al repo. Estaba fuera del árbol. Llega
   desactualizado en los dos puntos que este documento ya corrigió (decía
   110 WARN, daba el pre-registro por completo); se anota en el mensaje del
   commit, no se edita el archivo.

**No se tocó** el motor (`modelo`), el `glosario` ni el `integrador`: sus
defectos quedan documentados, corregirlos es decisión abierta. `corpus/` y
`forense/` (el directorio existente) se respetaron append-only.

═══ QUÉ QUEDÓ ABIERTO ═══

**A) El hueco del pre-registro (24/27).** No se propuso cómo llenarlo —eso
es decisión aparte, deliberadamente no tomada hoy. `§3.3` completo sin
falsador, incluida la regla de la que depende el gate de Fase 1. Registrado
en `estado §4·S2` y en `forense/notas/2026-07-29-b-correccion-perimetro.md`,
sección 4.

**B) Dos decisiones de la suite, ninguna tomada:**
- **T07** no vigila el vocabulario de tier *dentro* del motor, solo en
  `corpus/reports/`. Las 3 etiquetas compuestas del motor
  (`[FUERTE como correlación]`, `[FUERTE / MEDIA]`, `[MEDIA / HIPÓTESIS]`)
  no tienen registro de si son extensión sancionada del vocabulario de 4 o
  deriva sin documentar.
- **T10** busca literalmente `(b)` o "diáspora"; el integrador marca
  procedencia con convenciones locales (`[Fuerte, con caveat US]`,
  `Caveat US:`, `muestras US-hispanas`) que no calzan con ese patrón. Sin
  decidir si se amplía el patrón de T10 o si el integrador adopta el
  marcador formal de `modelo §0.1`.

**C) El modo línea base del CI — sin verificar si existe, y todo indica que
no.** `.github/workflows/verify.yml` corre `python3 tests/check.py` sin
`--strict`; `main()` devuelve `1` si `len(FAILS) > 0` (línea 344 de
`tests/check.py`). Con 18 FAIL constantes, **el check de GitHub Actions
sale en rojo en cada push a `main` y en cada PR, sin distinguir un FAIL ya
conocido de una regresión nueva.** No hay bandera, archivo de excepciones
ni comparación contra una corrida anterior — se buscó con
`grep -rn "baseline" .github/ tests/` y no aparece nada. Esto no se
verificó a fondo (no se revisó si algún otro workflow o script externo al
repo implementa algo así); se deja marcado como pendiente de decidir, no
como hallazgo cerrado.

═══ REGLAS QUE NO SE NEGOCIAN ═══
Citadas textualmente de `estado-programa-v1_8.md §5` (sin cambios respecto
a v1.7 — esta sesión no tocó esa sección):

- Los tiers se LEEN del glosario y de los mapas de evidencia. No se
  reconstruyen. Si un tier no está a la vista, ir a buscarlo antes de
  afirmarlo.
- Las reglas se CITAN TEXTUALMENTE de `modelo §3.B`, con tier, dominio y
  perfiles. Sin cita, es propuesta nueva y su veredicto no cuenta como
  validación.
- Marcar procedencia: (a) dato EN México · (b) muestra de diáspora ·
  (c) marco importado. La marca VIAJA hasta la ficha.
- Segmentar siempre. Una afirmación sobre "el mexicano" es señal de alarma.
- Hallar que la psicología NO importó es un resultado VÁLIDO.
- Descartar con rigor es entregable. Archivar los descartes (ADR-29.b).
- Consolidar PRIMERO, borrar DESPUÉS.
- Todo principio nuevo nace con su artefacto de salida (ADR-32). Si no
  falta visiblemente cuando no se cumple, no obliga a nada.
- Español.

A estas, `TRANSFER-maestra-7.md` añade dos que no estaban en `estado §5` y
siguen vigentes:
- corpus/ y forense/ son APPEND-ONLY. Se corrigen con nota fechada, NUNCA
  en silencio.
- Los tests documentan defectos de la evidencia; se corrigen con nota
  fechada en la fuente, no editando el dato para que el test calle.

═══ MÉTODO: SEIS CIFRAS CAYERON HOY AL PEDIRLES CITA ═══
Registrado completo en `forense/notas/2026-07-29-b-correccion-perimetro.md
§8`. Ninguna cayó por análisis ni relectura general — las seis cayeron al
exigir cita textual y número de línea:

  1. WARN de T03: se citaba 44, la corrida real da 41 (antes de
     `TRANSFER-maestra-7.md`; con él, 43).
  2. Estimación de disparos T09/T10: se citaba 22 y 46; enumerados uno por
     uno dieron 26 y 111.
  3. Perímetro fuerte del motor: se citaba "20 o 27, ambiguo"; es 27, sin
     ambigüedad, leyendo la salida de T12 en vez de `grep` sobre el archivo
     entero.
  4. Atribución de esa ambigüedad a la nota `9301e59`: la nota nunca la
     afirmó — venía del encargo de la sesión, no del registro.
  5. Cita a `curaduria-archivos.md:23` ("convirtió un [MEDIO] en un Fuerte
     pelón"): esa frase no aparece en ese archivo ni en ningún otro del
     repo.
  6. Cobertura del pre-registro: se citaba 27 de 27; contando los
     encabezados `## R` son 24.

**Ninguna la habría atrapado la suite.** Los 13 tests corren igual con las
seis circulando: comparan conteos entre canónicos, pero ninguno compara una
cifra declarada contra el artefacto que la respalda. La pregunta que las
atrapó a las seis fue siempre la misma: *¿de qué línea de qué archivo sale
este número?*

**La regla detrás del método: nada entra al canon desde una conversación sin
acceso al repo.** Las seis de arriba son un caso particular de algo más
amplio — hoy cayeron, además, por la misma causa:

  - `TRANSFER-maestra-7.md` decía "18 FAIL · 110 WARN". Se escribió en una
    conversación sin acceso al repo para correr `tests/check.py`; la cifra
    era la mejor disponible en ese momento, no una lectura.
  - Mi propio supuesto de que la nota `9301e59` afirmaba la ambigüedad
    20/27: lo di por bueno de una paráfrasis hasta que grepeé el archivo.
  - **Reportado por el usuario, no verificado por mí contra su origen**
    (no tengo acceso a esa conversación): una lista de "5 decisiones que
    requieren firma" que venía de otro chat, cuya decisión 1 ya estaba
    cerrada en `gobernanza-v1_8.md:266` desde el 28/jul. Lo que sí verifiqué
    de forma independiente es que `gobernanza:266` existe, está fechado
    28/jul, y registra el perímetro del Hito D como decisión cerrada —
    consistente con la afirmación del usuario, aunque no pude cotejar la
    lista de origen misma.

**Lo que sale de un chat es hipótesis hasta verificarse contra archivo, con
línea y cita.** Una conversación no tiene forma de correr `tests/check.py`,
ni de `grep`-ear un archivo, ni de saber si algo que "parece pendiente" ya
se cerró la sesión anterior. El repo es la única fuente que puede
confirmarlo o refutarlo — por eso todo lo de esta sesión que entró al canon
se cita con hash de commit y número de línea, y todo lo que no se pudo
cotejar así queda marcado como no verificado, no como hecho.

═══ LO PRIMERO PARA LA PRÓXIMA SESIÓN ═══
Confirma `git log --oneline -1` y corre `python3 tests/check.py` ANTES de
proponer trabajo — la cifra de WARN cambia según si `TRANSFER-maestra-7.md`
ya está en el árbol que estés leyendo. No asumas 107 ni 109 sin correrlo.

⚠️ Si algo en este documento no trae número de línea o hash de commit junto
a la cifra, es porque no se verificó al escribirlo — trátalo como no
confirmado, no como falso.
