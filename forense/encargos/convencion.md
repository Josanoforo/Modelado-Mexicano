Convención de `forense/encargos/`

Por qué existe. Un encargo que solo existe en la salida de una conversación es invisible para el programa. Medido el 5/ago/2026 (ENCARGO P2, mesa #20): de una batería de seis encargos rescatados ese día, cinco ya se habían ejecutado por otras vías sin que nadie lo supiera, y el sexto había muerto una vez. La regla que atrapa esa clase de defecto la fija `instrucciones-proyecto-v2_5.md` Bloque D-bis, A.3: todo encargo que se lance se commitea aquí antes o junto con su lanzamiento.

Qué va aquí. El texto completo del encargo tal como se lanzó — no un resumen, no un enlace a una conversación. Si el encargo cita un archivo del repo, ese archivo ya existe en el commit que lo acompaña (un encargo que cita un archivo inexistente está mal escrito — ocurrió tres veces, `instrucciones-proyecto-v2_5.md` A.3). Si el encargo necesita un texto que vive fuera del repo, ese texto va pegado inline dentro del propio encargo, o el encargo no se lanza.

Cabecera obligatoria de cada encargo archivado aquí:

- **SHA de redacción** — el commit de `origin/main` (o de la rama base) contra el que el encargo se escribió, para que quien lo audite después sepa qué terreno asumía.
- **Entorno asignado** — a cuál va (nube / Ubuntu) y, si aplica, el que NO — mismo criterio que Bloque D de `instrucciones-proyecto`.
- **Estado** — `VIVO` o `CONSUMIDO` (ver abajo).

Nombre de archivo. El archivo de encargo lleva el código del acto como prefijo tras la fecha (AAAA-MM-DD-<CÓDIGO>-<tema>.md); su nota no. T02 normaliza sin distinguir directorio, así que un encargo y una nota con el mismo tema y sin prefijo colisionan por construcción — ha ocurrido en cinco actos.

Ciclo de vida. Un encargo nace `VIVO`. Cuando el acto que lo ejecuta cierra, se marca `CONSUMIDO`, con el PR que lo ejecutó. Un encargo consumido **no se borra**: es el registro de qué se pidió exactamente, y es lo que permite auditar después si el ejecutor hizo lo que se le dijo — borrar un encargo consumido destruiría esa auditoría tan bien como nunca haberlo escrito.

Este acto (ENCARGO P2) establece la convención y el sitio. **No** puebla el directorio con encargos concretos — eso depende de textos que hoy viven fuera del repo (en conversaciones), y mesa los añade después, uno por uno, con su cabecera completa.
