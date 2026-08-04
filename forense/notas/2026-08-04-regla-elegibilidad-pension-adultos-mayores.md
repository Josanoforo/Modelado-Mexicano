# Regla de elegibilidad — Programa/Pensión (para el Bienestar de) Adultos Mayores, 2013–2021

**Mueve el contador de auditoría del acto: cero, por diseño (§6 del encargo). Aterriza en el repo un hallazgo que hasta hoy solo vivía en un chat.**

*4 de agosto de 2026. Encargo V, mesa #19. Rama `sesion/regla-elegibilidad-preregistro-r5-1`, worktree `~/mm-regla-elegibilidad-preregistro` (nuevo, creado en este acto sobre `origin/main` en `cb331b6`).*

---

## 0 · Entorno — mide, no hereda, la restricción de red

```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.inegi.org.mx/
200
```

Firma buena confirmada: `sin_variable` + `200`.

**Las tres rutas al texto legal, sondeadas, códigos crudos:**

| Ruta | Código crudo | Nota |
|---|---|---|
| `https://www.dof.gob.mx/` | **000** con verificación TLS estándar (`curl: (60) unable to get local issuer certificate`); **200** con `-k` (verificación TLS omitida) | Cadena de certificado incompleta **del propio sitio** — mismo error con `curl` y con `WebFetch` (que no puede desactivar la verificación). No es bloqueo de red del entorno: es un defecto TLS del servidor de DOF, medible independientemente de la herramienta. |
| `https://sidof.segob.gob.mx/` | **200**, TLS válido, cuerpo real (`Server: Apache`, cookies de sesión CI, HTML de la aplicación SIDOF) | Alcanzable sin rodeo. |
| `https://www.gob.mx/` (PDFs de ROP en gob.mx) | **200**, TLS válido, cuerpo real (portal JSF/PrimeFaces de gob.mx) | Alcanzable sin rodeo. |

**Corrección explícita a una afirmación heredada.** `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md:98` y `:121` afirman *"Este entorno no tiene acceso de red a `dof.gob.mx` ni a `coneval.org.mx` (no están en la lista de hosts permitidos)"*. Medido en este acto: **`dof.gob.mx` sí es alcanzable** (200 con `-k`, contenido real de las Reglas de Operación descargado y citado abajo) — la fricción real no es una lista de hosts, es una cadena TLS rota en el servidor del propio DOF, sorteable con `curl -k`. La ruta de espejo `sidof.segob.gob.mx` no tiene ese problema y no requiere rodeo. **No se verificó `coneval.org.mx`** en este acto — no era una de las tres rutas que el encargo pide sondear (§1); se declara que la frase heredada sobre CONEVAL sigue sin medir, no se extiende la corrección a esa parte.

**Todo el texto citado abajo se descargó con `curl -k` de `dof.gob.mx`** (contenido real de la fuente primaria, verificado por inspección directa del HTML — no reconstruido de memoria, no tomado de un resumen de terceros) y se contrastó por búsqueda dirigida contra las citas correspondientes. Ningún ZIP de microdato se abrió en este acto (§2 del encargo).

---

## 1 · La premisa reportada en el chat — verificada, no copiada

Cita reportada (procedencia tipo (3), Encargo V §1): *"de 2013 a 2018 la población objetivo consideró a personas de 65 años y más con un mínimo de 25 años de residencia y que no recibían una pensión mayor a $1,092 pesos mensuales por concepto de jubilación o pensión de tipo contributivo"; en 2019 se crea la pensión universal no contributiva (indígena 65+, no indígena 68+); en las ROP de dic/2021 ya es 65+ para todas las personas.*

**Veredicto: la cifra ($1,092) y el mecanismo (25 años de residencia, prueba de pensión contributiva, split indígena/no indígena en 2019, unificación a 65+) se confirman verbatim contra la fuente primaria. El rango de años ("2013 a 2018") no se confirma verbatim: el propio texto de 2013 no trae la regla. Ver §2.**

No se copió el texto del chat a ningún archivo del repo: cada renglón de §2–§4 abajo cita documento, fecha y pasaje literal, obtenidos por lectura directa en este acto.

---

## 2 · Régimen 2013–2018 — con la fecha exacta del cambio de texto, no la del nombre del programa

### 2013 — el año de relanzamiento del programa, SIN el umbral de $1,092 ni el requisito de 25 años

**Fuente:** DOF, *ACUERDO por el que se emiten las Reglas de Operación del Programa de Pensión para Adultos Mayores, para el ejercicio fiscal 2013*, 26/feb/2013 (código DOF 5288941). `https://www.dof.gob.mx/nota_detalle.php?codigo=5288941&fecha=26/02/2013`

Cita literal, §3.2 Población Objetivo: *"Personas de 65 años de edad en adelante que no reciban ingresos por concepto de pago de jubilación o pensión de tipo contributivo."*

No hay cifra en pesos (la regla es de exclusión total, no de umbral). No hay requisito de años de residencia — "residencia" aparece solo como uno de los documentos admitidos para *acreditar domicilio*, no como duración mínima.

### 2014 — primer texto con el umbral de $1,092 y los 25 años de residencia

**Fuente:** DOF, *ACUERDO por el que se emiten las Reglas de Operación del Programa de Pensión para Adultos Mayores, para el ejercicio fiscal 2014*, 29/dic/2013 (código DOF 5328387). `https://dof.gob.mx/nota_detalle.php?codigo=5328387&fecha=29/12/2013`

Cita literal, §3.2 Población Objetivo: *"Personas de 65 años de edad en adelante mexicanos por nacimiento o con un mínimo de 25 años de residencia en el país, que no reciban pensión mayor a $1,092 pesos mensuales por concepto de jubilación o pensión de tipo contributivo."*

Esta es la primera aparición verificada del texto que el chat reportó, letra por letra salvo la disyunción que el chat omitió: **"mexicanos por nacimiento O con un mínimo de 25 años de residencia"** — los 25 años son la vía de acceso para quien no nació mexicano, no un requisito universal de residencia para todos los solicitantes. El chat lo parafraseó como si fuera general; el documento lo condiciona.

### 2015 y 2018 — el mismo texto se sostiene sin cambio

**Fuente 2015:** DOF, *ACUERDO ... Programa Pensión para Adultos Mayores, para el ejercicio fiscal 2015*, 27/dic/2014 (código DOF 5377505). Cita literal, §3.2: *"Personas de 65 años de edad en adelante mexicanos por nacimiento o con un mínimo de 25 años de residencia en el país, que no reciban pensión mayor a $1,092 pesos mensuales por c[o]ncepto de jubilación o pensión de tipo contributivo."* — idéntico a 2014.

**Fuente 2018:** DOF, *ACUERDO ... Programa Pensión para Adultos Mayores, para el ejercicio fiscal 2018*, 28/dic/2017 (código DOF 5509626). Cita literal, §3.2: *"Personas de 65 años de edad en adelante, mexicanas o con un mínimo de 25 años de residencia en el país, que no reciban pensión mayor a $1,092 mensuales por concepto de jubilación o pensión de tipo contributivo."* — mismo umbral, siete ejercicios fiscales después.

**Corrección de precisión a la premisa del chat:** *"de 2013 a 2018"* es la forma en que el propio DOF se recita a sí mismo en 2021 (ver nota abajo) — no es exacta contra el texto de 2013. Lo verificado directamente en tres cortes (2014, 2015, 2018) es que el umbral de $1,092 y los 25 años rigieron **de 2014 a 2018**, cinco ejercicios fiscales, no seis. **2013 es el año del programa bajo ese nombre, pero no el año del umbral.** No se buscó el texto de 2016 y 2017: con tres cortes (inicio, medio, fin del rango 2014–2018) idénticos, se declara el patrón sostenido sin necesidad de verificar los dos años restantes uno por uno — si alguno rompiera el patrón sería un hallazgo que este acto no tiene forma de descartar por no haberlos abierto; se deja como hueco menor, no como afirmación.

**Dónde vive el "2013 a 2018" en una fuente primaria real, no solo en el chat:** el acuerdo del 7/jul/2021 (§4 abajo) trae, en sus Considerandos, la frase *"durante el periodo de 2013 a 2018 la población objetivo del programa de la 'Pensión para Adultos Mayores' consideró a las personas adultas de 65 años y más con un mínimo de 25 [años de residencia...]"* — el propio gobierno resume su historia con el rango de calendario que empieza en el año de relanzamiento del programa (2013), no en el año en que ese texto específico entró en vigor (2014). El chat no inventó el rango; lo heredó, sin que quien lo escribió en el chat lo supiera, de una imprecisión que ya existía en una fuente oficial posterior. Se documenta la diferencia porque el encargo pidió cita de documento y fecha para cada renglón, no la cifra que "suena bien".

---

## 3 · Régimen 2019–2021 — universal no contributiva, split indígena/no indígena

**Fuente:** DOF, *ACUERDO por el que se emiten las Reglas de Operación de la Pensión para el Bienestar de las Personas Adultas Mayores, para el ejercicio fiscal 2019*, 28/feb/2019 (código DOF 5551445). `https://dof.gob.mx/nota_detalle.php?codigo=5551445&fecha=28/02/2019`

Cambio de nombre del programa: de *"Pensión para Adultos Mayores"* a *"Pensión para el Bienestar de las Personas Adultas Mayores"*.

Cita literal, §3.2 Población Objetivo: *"Personas indígenas adultas mayores de 65 años o más de edad, mexicanas por nacimiento que residan en la República Mexicana y en los municipios catalogados como indígenas. Personas adultas mayores de 68 años o más de edad, mexicanas que residan en la República Mexicana. Personas adultas mayores de 65 a 67 años de edad, incorporadas en el Padrón Activo de Beneficiarios del Programa Pensión para Adultos Mayores, activos a diciembre del ejercicio fiscal 2018."*

Confirma el split reportado: **65+ para municipios catalogados como indígenas, 68+ para el resto**, más una cláusula de transición (65–67 años ya incorporados al padrón del programa anterior a dic/2018, que conservan el beneficio sin esperar a los 68).

**Eliminación de la prueba de pensión contributiva, confirmada.** El mismo documento describe el programa como *"una pensión no contributiva de tendencia universal"* (Introducción) — ya no hay umbral de $1,092 ni prueba de ingreso por jubilación/pensión: la condición pasa a ser exclusivamente edad + nacionalidad/residencia. No se localizó, en el pasaje leído, una fecha de corte distinta a la de publicación (28/feb/2019) para esta transición — se declara sin hueco.

---

## 4 · Régimen 2021 en adelante — unificación a 65+ para todas las personas

**Fuente:** DOF, *ACUERDO por el que se modifica el diverso por el que se emiten las Reglas de Operación del Programa Pensión para el Bienestar de las Personas Adultas Mayores, para el ejercicio fiscal 2021, publicado el 22 de diciembre de 2020*, 7/jul/2021 (código DOF 5623150). `https://www.dof.gob.mx/nota_detalle.php?codigo=5623150&fecha=07/07/2021`

Cita literal (Considerandos): *"el Acuerdo por el que se emiten las Reglas de Operación del Programa Pensión para el Bienestar de las Personas Adultas Mayores, para el ejercicio fiscal 2021, se modifica para poder beneficiar [a] todas las personas adultas mayores de 65 años de edad o más."*

Cita literal (tabla de apoyos modificada, §3.5): *"Todas las personas adultas mayores de 65 años o más de edad, mexicanas por nacimiento o naturalización, con domicilio actual en la República Mexicana."*

**Fecha del acuerdo que unifica a 65+: 7 de julio de 2021.** Elimina la distinción indígena/no indígena introducida en 2019 — el requisito de edad queda en 65+ para toda persona mexicana con domicilio en el país, sin importar municipio. No se verificó en este acto el acuerdo de diciembre de 2021 (ROP del ejercicio fiscal 2022) que el encargo menciona de pasada — el de julio de 2021 ya contiene la unificación completa y con eso se cierra el renglón que pedía el encargo; se declara que la ROP 2022 no se abrió, por no ser necesaria para responder la pregunta planteada.

---

## 5 · Huecos declarados

- **Textos de 2016 y 2017 no abiertos.** Se infiere continuidad del umbral de $1,092/25 años por los cortes de 2014, 2015 y 2018 (§2), pero no se verificó línea por línea. Si algún ejercicio intermedio modificó el monto, este acto no lo detectaría.
- **`coneval.org.mx`** — mencionado en la nota heredada de R5.1 junto con `dof.gob.mx` como host supuestamente inalcanzable — no se sondeó en este acto. El encargo pidió sondear tres rutas específicas al DOF, no CONEVAL; se declara sin verificar, no se extiende la corrección de §0 a esa fuente.
- **ROP del ejercicio fiscal 2022 (acuerdo de diciembre de 2021)** no se abrió — ver nota al final de §4.

---

*Nota propia (§3.1 del encargo). No enmienda ninguna ficha del pre-registro del Hito D ni el registro append-only de veredictos.*
