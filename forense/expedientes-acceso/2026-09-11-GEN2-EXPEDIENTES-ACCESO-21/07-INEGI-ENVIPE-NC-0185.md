# Expediente 07 · INEGI / ENVIPE 2013 y 2015 / NC-0185

Estado: **BORRADOR FINAL; LISTO-PARA-TITULAR; NO ENVIADO**. Expediente hermano
abierto por firma de mesa (15/sep/2026) sobre el sucesor declarado en
`NC-0185` (`forense/no-corrido.tsv`), por la vía comprobada del expediente 04
de este mismo paquete. Este acto no presenta nada: no hay solicitud enviada,
acceso concedido ni archivo obtenido.

## Objeto

`ACTO GEN2-VERIFICACION-CAJA-2` acreditó 32/32 identidades DBF residuales de
ENVIPE 2013/2015 contra el descriptor oficial de cada ola y dejó **siete**
como `NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL` — negativo declarado con página, no
ausencia científica (`NC-0100` cerrada con ese saldo; tabla en
`forense/notas/2026-09-14-GEN2-VERIFICACION-CAJA-2-cierre.md`):

| identidad | ola / archivo | qué falta en el descriptor oficial |
|---|---|---|
| `AP5_3_02` | ENVIPE 2015, `TPer_Vic1.dbf` | `fd_envipe2015.pdf` salta de `AP5_6_01` (p. 26) a `AP5_7_2` (p. 27); la sección que documentaría estas cinco variables no existe en el PDF |
| `AP5_4_02` | ENVIPE 2015, `TPer_Vic1.dbf` | idem |
| `AP5_5_02` | ENVIPE 2015, `TPer_Vic1.dbf` | idem |
| `AP5_6_02` | ENVIPE 2015, `TPer_Vic1.dbf` | idem |
| `AP5_7_1` | ENVIPE 2015, `TPer_Vic1.dbf` | idem |
| `EST_SOC` (2013-a) | ENVIPE 2013, `tmod_vic.dbf` | `fd_envipe2013.xlsx` documenta `EST`, no `EST_SOC`; códigos observados en archivo 1–4 |
| `EST_SOC` (2013-b) | ENVIPE 2013, `tper_vic.dbf` | idem, segundo archivo de la misma ola |

Las siete no alimentan ningún `CALC` ni regla del motor y esto no cambia:
sólo se solicita el texto oficial (pregunta y códigos) para acreditar o
descartar cada una con cita, no para incorporarlas a ninguna medición.

## Canal oficial comprobado

- Productor/programa: [ENVIPE](https://www.inegi.org.mx/programas/envipe/) —
  ediciones 2013 y 2015.
- Ruta primaria: [Contacto INEGI](https://www.inegi.org.mx/inegi/contacto.html),
  `Solicitud de información estadística y geográfica` (misma vía que el
  expediente 04 de este paquete).
- Correo de atención publicado en el catálogo de microdatos:
  **`atencion.usuarios@inegi.org.mx`**.
- Asunto: `Consulta técnica ENVIPE 2013/2015: texto oficial de variables ausentes del descriptor de diseño`
- Si INEGI determina que la respuesta requiere el Laboratorio de
  Microdatos/Procesamiento Remoto, seguir la vía que responda; el
  [formato correspondiente](https://www.inegi.org.mx/contenidos/app/microdatos/laboratoriodatos/doc/Solicitud_Uso.pdf)
  es alternativa, no una afiliación o costo que este expediente dé por hecho.

## Texto final para formulario o correo

> Solicito orientación técnica sobre el diccionario de datos oficial de la
> Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública
> (ENVIPE), ediciones 2013 y 2015, para acreditar siete variables presentes en
> los microdatos que no localizamos en el descriptor de diseño publicado.
>
> **ENVIPE 2015, tabla `TPer_Vic1`:** el archivo trae `AP5_3_02`, `AP5_4_02`,
> `AP5_5_02`, `AP5_6_02` y `AP5_7_1`, con códigos coherentes con las preguntas
> vecinas de la sección AP5. En el diccionario de datos oficial (`fd_envipe2015.pdf`)
> la numeración salta de `AP5_6_01` (página 26) a `AP5_7_2` (página 27): la
> sección que documentaría estas cinco variables no aparece entre esas
> páginas ni en ninguna otra del documento que revisamos.
>
> **ENVIPE 2013, tablas `tmod_vic` y `tper_vic`:** ambos archivos traen
> `EST_SOC`, con códigos observados 1 a 4. El diccionario de datos oficial
> (`fd_envipe2013.xlsx`) documenta `EST`, no `EST_SOC`.
>
> Para cada una de las siete variables, agradeceré el texto de la pregunta o
> etiqueta oficial, la lista completa de códigos/categorías y, si aplica, la
> página o sección correcta del diccionario de datos donde debería estar
> documentada (o la fe de erratas correspondiente, si el diccionario público
> tiene una omisión conocida). Si la numeración cambió entre ediciones o
> erratas del diccionario, agradeceré la correspondencia oficial vigente.
>
> Cualquiera de estas respuestas resolvería la consulta, en orden de menor
> riesgo de divulgación:
> 1. la sección faltante del diccionario de datos (o su fe de erratas), con
>    el texto y códigos de las siete variables; o
> 2. una tabla de equivalencias/crosswalk que documente pregunta, etiqueta y
>    códigos de cada variable, aunque no forme parte del PDF/XLSX público; o
> 3. la confirmación explícita de que estas variables no tienen texto
>    documentado por [razón que INEGI especifique], para poder declarar la
>    ausencia con esa cita en vez de con la nuestra.
>
> No se solicita microdato adicional, geografía identificable ni datos
> personales: los archivos correspondientes ya están en nuestro poder por la
> vía pública. La finalidad es investigación no comercial sobre percepción y
> victimización; sólo se publicarían resultados agregados. Ya se revisaron el
> cuestionario, el diccionario de datos y los microdatos públicos de ambas
> ediciones antes de esta consulta.
>
> Atentamente,
> [NOMBRE REAL — completar sólo al presentar]

En el formulario web elegir `Información estadística y geográfica` (o la
opción equivalente vigente), pegar el texto en `Otra información` y conservar
el acuse. No es necesario adjuntar los microdatos públicos. Si el cuadro de
texto limita caracteres, adjuntar una copia privada PDF de este pedido y
escribir en el campo un resumen con el mismo objeto.

## Dato del titular

| dato faltante del titular | por qué se exige | dónde se escribe |
|---|---|---|
| nombre, apellidos y correo reales | campos obligatorios y respuesta | formulario/cuenta remitente |
| institución/escuela/empresa real, si el formulario la exige | campo del canal | campo institucional; escribir sólo la situación verdadera |
| ocupación/cargo real, sólo si la vía elegida lo exige | posible formulario de procesamiento | copia privada, no en Git |
| CV, identificación, filiación y supervisor, sólo si INEGI deriva al laboratorio y aplican | requisitos de esa vía, no del primer contacto | adjuntos privados del trámite posterior |

## Recepción y continuación

Registrar folio, fecha, edición y cuál de las tres opciones respondió INEGI.
Para una sección de diccionario o fe de erratas: verificar que cubre las
siete variables citadas y conservar copia fuera de Git. Para un crosswalk:
verificar que asigna pregunta y códigos a cada una de las siete, sin mezclar
ediciones. Para una confirmación de ausencia: registrar la razón dada.

Si la respuesta identifica el texto oficial de alguna o todas las siete, el
buscador de reactivos sube su veredicto de `PREGUNTA_NO_LOCALIZADA` /
`ETIQUETA_TECNICA_NO_ACREDITADA` a `ACREDITADA` con la cita nueva, por
enmienda fechada sobre `NC-0100`/`NC-0185` (original intacto, no se reescribe
el negativo histórico). Una negativa o falta de respuesta se asienta en
`NC-0185` y cierra la fila con esa decisión — no se convierte en ausencia
científica ni se reintenta por otra vía.
