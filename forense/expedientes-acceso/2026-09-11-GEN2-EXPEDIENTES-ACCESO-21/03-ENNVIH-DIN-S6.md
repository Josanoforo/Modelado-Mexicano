# Expediente 03 · ENNViH-1: una solicitud para DIN-M-01 y S6

Estado: **BORRADOR FINAL; LISTO-PARA-TITULAR; NO ENVIADO**. Canal comprobado el
11 de septiembre de 2026. Preparar o enviar esta solicitud no cierra NC-0156 ni
firma FP-371/FP-372.

## Canal oficial

- Contacto: [MXFLS / ENNViH Contact](https://www.ennvih-mxfls.org/english/contact.html).
- Destinatario primario publicado: **`support@ennvih-mxfls.org`**.
- Asunto: `Consulta de varianza oficial ENNViH-1 (2002): DIN-M-01 y tres contrastes S6`
- Sin adjunto obligatorio. Si el equipo lo pide, remitir una copia privada de
  este texto; no adjuntar microdatos ni geografía.

La FAQ confirma que municipio, localidad y UPM no son públicos por
confidencialidad. La solicitud no pide geolocalización ni una llave que permita
identificarla. `id_loc` (150 localidades) no se presenta como las 180 UPM
oficiales, y `c_portad.estrato` (cuatro tamaños) no se presenta como los tres
estratos socioeconómicos de selección.

## Correo final para copiar

> Estimado equipo de soporte de la ENNViH:  
>  
> Utilizamos la ENNViH-1 (2002) y necesitamos estimar incertidumbre bajo su
> diseño para cuatro estimandos ya definidos: una proporción del Libro 3B
> (DIN-M-01) y tres diferencias de proporciones del mismo libro (S6, C1/C3/C4).
> Entendemos por la documentación y FAQ que la UPM y la geografía identificable
> no son públicas; no las solicitamos.  
>  
> Preferimos una solución que preserve confidencialidad, en este orden:  
> (1) pesos replicados oficiales no geográficos que cubran estos universos,
> junto con método (BRR/jackknife/bootstrap u otro), factor global `scale`,
> factores por réplica `rscales`, convención MSE, grados de libertad, tratamiento
> de UPM únicas y FPC aplicable; o  
> (2) un servicio/tabulado oficial que ejecute las recetas de abajo y devuelva
> estimación, error estándar, IC95, grados de libertad, número de observaciones y
> masa ponderada. Para las diferencias solicitamos también la covarianza entre
> los dos cocientes, o una confirmación de que el EE de la diferencia ya la
> incorpora.  
>  
> **DIN-M-01.** Archivos `iiib_cr.dta` y `ehh02w_b3b.dta`, unión 1:1 por
> `folio+ls`; universo `cr27 in {1,3}`; indicador `I(cr27=1)`; ponderador
> `fac_3b`. Nuestra verificación produce `n=19,739`, masa ponderada
> `68,002,840` y punto `0.15558094338412926`. Pedimos el EE/IC95 de ese punto
> con el diseño oficial. Los códigos 7/8 y faltantes quedan excluidos.  
>  
> **S6, Libro IIIB (`b3b`), ponderador `fac_3b`.** Cada contraste es
> `Delta=P_PUBLICO(T=1)-P_PUBLICO(T=0)`, donde
> `P_PUBLICO=n_ponderado(SOLO-PUBLICO) /
> [n_ponderado(SOLO-PUBLICO)+n_ponderado(SOLO-PRIVADO)]`; `AMBOS` y
> `SOLO-OTRO` se cuentan pero quedan fuera del cociente. Unión persona-persona y
> con pesos por `folio+ls`.  
>  
> - C1, primaria: `T=1` si `es09=1`, `T=0` si `es09=3`; hospitalización
>   `hs01=1` y al menos un episodio `hs08_1a=1` (enfermedad) o `hs08_1e=1`
>   (operación). Público: alguna de `hs02a,b,c,d,g`; privado: alguna de
>   `hs02e,f`. Resultado descriptivo a cotejar: 84.2475% frente a 77.6514%,
>   Delta=-6.5961 puntos porcentuales.
> - C3: `T=1` si alguna de `ec01a`...`ec01g`, `ec01h_1`, `ec01i_1` vale 1;
>   `T=0` si ninguna vale 1, respetando códigos de no respuesta; mismo desenlace
>   de hospitalización y clasificación de C1. Resultado descriptivo: 66.6969%
>   frente a 84.8835%, Delta=+18.1865 pp.
> - C4: mismo `T` crónico de C3; universo de consulta `ce01=1`. Público: alguna
>   de `ce04a,b,c,d,g,i,k`; privado: alguna de `ce04e,f,l`. Resultado
>   descriptivo: 63.8801% frente a 70.5836%, Delta=+6.7035 pp.
>  
> Las baterías son de respuesta múltiple: `SOLO-PUBLICO` exige al menos una
> marca pública y ninguna privada; `SOLO-PRIVADO`, al menos una privada y ninguna
> pública; `AMBOS`, marcas de ambos grupos. Para C1/C3 el motivo vive a nivel
> episodio y la institución a nivel persona: entra la persona con al menos un
> episodio elegible, sin atribuir institución a un episodio particular.  
>  
> Agradeceríamos que indicaran también la cobertura/versión de los pesos de
> réplica o, si ninguna de las dos rutas es posible, que confirmaran esa
> indisponibilidad y señalaran una alternativa oficial. Una respuesta que sólo
> identifique `id_loc` como localidad no se interpretará como acreditación de
> UPM.  
>  
> Atentamente,  
> [NOMBRE REAL — completar sólo al enviar]

## Dato del titular

| dato faltante del titular | por qué se exige | dónde se escribe |
|---|---|---|
| nombre y correo reales | identificación mínima del contacto | remitente y firma del correo |
| afiliación, sólo si es verdadera y se desea declarar | contexto opcional; el canal no la publica como requisito | firma, no inventar |

## Recepción y continuación

Registrar Message-ID/acuse, fecha y alcance de la respuesta. Una respuesta útil
incluye bytes de pesos y contrato completo, o resultados con método, EE/IC,
`df`, `n`, masa, FPC/singletons y tratamiento de covarianza. Guardar cualquier
peso o microdato fuera de Git y registrar hash/versión.

El receptor compara primero los cuatro puntos y universos. Si cubre sólo DIN o
sólo alguna celda S6, lo registra por separado. Si es ejecutable, nace una spec
prospectiva en CAJA antes de un nuevo cálculo. Los puntos vigentes no cambian y
la respuesta no decide por sí misma el uso científico pendiente en FP-371/372.
