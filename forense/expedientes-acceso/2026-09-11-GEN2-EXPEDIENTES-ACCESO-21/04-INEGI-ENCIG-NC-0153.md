# Expediente 04 · INEGI / ENCIG / NC-0153

Estado: **BORRADOR FINAL; LISTO-PARA-TITULAR; NO ENVIADO**. No se repitió la
búsqueda pública agotada en #695 y la fila conserva `OBTENIDO-PARCIAL`, no
`PENDIENTE`.

## Canal oficial comprobado

- Productor/programa: [ENCIG 2025](https://www.inegi.org.mx/programas/encig/2025/).
- Ruta primaria: [Contacto INEGI](https://www.inegi.org.mx/inegi/contacto.html),
  `Solicitud de información estadística y geográfica`.
- Correo de atención publicado en el catálogo de microdatos:
  **`atencion.usuarios@inegi.org.mx`**.
- Asunto: `Consulta técnica ENCIG 2025: enlace de corrupción 8.5 con tipo y canal de trámite`
- Si INEGI determina que se requiere procesamiento especial o acceso
  confidencial, seguir la vía que responda. El [formato de Laboratorio de
  Microdatos/Procesamiento Remoto](https://www.inegi.org.mx/contenidos/app/microdatos/laboratoriodatos/doc/Solicitud_Uso.pdf)
  es alternativa, no una afiliación o costo que este expediente dé por hecho.

## Texto final para formulario o correo

> Solicito orientación técnica o una salida oficial de la Encuesta Nacional de
> Calidad e Impacto Gubernamental (ENCIG) 2025 para estimar, con
> representatividad nacional de su población objetivo, la tasa de solicitudes o
> insinuaciones de pago informal por **evento/tipo de trámite y canal de
> realización**, incluyendo los eventos elegibles sin corrupción en el
> denominador.  
>  
> En los materiales públicos revisados, los reactivos de la sección 8.3
> identifican experiencias, 8.4 caracteriza tipo y 8.5 registra conteos de actos
> de corrupción. En los archivos, `P7_3` describe canal por combinación de
> `ID_TRA` y `NT_TIPO`, mientras la información de corrupción disponible a nivel
> `ID_TRA` no permite una asignación unívoca cuando una misma persona/trámite
> tiene más de un `NT_TIPO` o canal. Si la numeración o nombres cambiaron en la
> versión definitiva, agradeceré la correspondencia oficial correcta.  
>  
> Cualquiera de estas tres respuestas resolvería la consulta, en orden de menor
> riesgo de divulgación:  
> 1. la llave/crosswalk y documentación que asigna cada conteo de 8.5 al
>    `NT_TIPO/P7_3` correspondiente;  
> 2. un archivo anonimizado a nivel evento que contenga identificador no
>    personal de caso/evento, tipo de trámite, canal, solicitud/insinuación o
>    conteo, **ceros/negativos**, periodo de referencia, factor de expansión,
>    estrato, conglomerado/UPM anonimizado y reglas de universo/exclusión; o  
> 3. un tabulado/procesamiento oficial con numerador, denominador, tasa, error
>    estándar o IC95 y `n` no ponderado para cada evento × canal, además del
>    total nacional, aplicando el diseño oficial.  
>  
> El denominador requerido son todos los eventos/contactos elegibles del mismo
> universo y periodo, no sólo personas que reportaron corrupción ni sólo
> eventos con `P8_4` observado. La población objetivo que se conservará es la de
> ENCIG 2025: personas de 18 años o más en viviendas particulares de ciudades
> de 100 mil habitantes o más. Se solicita la documentación de cualquier
> exclusión y el uso correcto de ponderación, estratos y conglomerados.  
>  
> La finalidad es investigación no comercial sobre la relación entre modalidad
> de atención y experiencia de solicitud de pago informal. Sólo se publicarían
> resultados agregados; no se solicita geografía identificable ni datos
> personales. Ya se revisaron cuestionario, documentación y microdatos públicos;
> fuentes locales parciales no sustituyen la estimación nacional descrita.  
>  
> Atentamente,  
> [NOMBRE REAL — completar sólo al presentar]

En el formulario web elegir `Información estadística y geográfica` (o la opción
equivalente vigente), pegar el texto en `Otra información` y conservar el acuse.
No es necesario adjuntar los microdatos públicos. Si el cuadro de texto limita
caracteres, adjuntar una copia privada PDF de este pedido y escribir en el campo
un resumen con el mismo objeto.

## Dato del titular

| dato faltante del titular | por qué se exige | dónde se escribe |
|---|---|---|
| nombre, apellidos y correo reales | campos obligatorios y respuesta | formulario/cuenta remitente |
| institución/escuela/empresa real, si el formulario la exige | campo del canal | campo institucional; escribir sólo la situación verdadera |
| ocupación/cargo real, sólo si la vía elegida lo exige | posible formulario de procesamiento | copia privada, no en Git |
| CV, identificación, filiación y supervisor, sólo si INEGI deriva al laboratorio y aplican | requisitos de esa vía, no del primer contacto | adjuntos privados del trámite posterior |

## Recepción y continuación

Registrar folio, fecha, edición y cuál de las opciones 1–3 respondió INEGI. Para
un archivo: conservarlo fuera de Git, calcular SHA-256/tamaño/dimensiones y
verificar presencia de negativos, unidad evento, llave unívoca y diseño. Para un
tabulado: verificar numerador+denominador, universo nacional, ponderación y
incertidumbre. Una respuesta estatal o de microempresas sigue siendo parcial.

Si la respuesta identifica el objeto, el sucesor congela primero unidad,
denominador, canal, evento y diseño, y sólo entonces calcula la tasa. Una
negativa se asienta en NC-0153 y evita repetir la solicitud; no se convierte en
ausencia mundial del dato.
