# Retracción: `curaduria-archivos.md:66` declaró aplicado un parche que no lo estaba

**Fecha:** 29 de julio de 2026 (sesión de correcciones)
**No se edita `forense/curaduria-archivos.md`** (append-only). Esto es una nota nueva, no un parche del cuerpo.

---

## Qué dice la fuente

`forense/curaduria-archivos.md:66`, fechado 27/jul/2026, fila de `meta-auditoria-comunicacion.md`:

> *"Parche canónico. ⚠️ **Estatus cambia hoy:** su orden de retirar 'honor' ya se ejecutó en la fuente. Sigue vigente por lo demás."*

## Por qué es falso

`canon/glosario-v5_6.md §14`, punto 2 (verificación fechada 28/jul/2026), es explícito:

> *"Las dos afirmaciones eran falsas: ADR-29 sí está aprobado (gobernanza v1.1), y los dos parches no existían en el report — la decisión se había tomado y registrado, pero la nota nunca bajó al documento. Estado real hoy: Hofstede en consumidor parchado 28/jul; honor en comunicación parchado 28/jul; honor 'híbrido' en foundational resuelto por ADR-31 y parchado 28/jul."*

El retiro de "honor" en `La_arquitectura_invisible_de_la_interacción_social_en_México.md` (el report que `meta-auditoria-comunicacion.md` gobierna) se parchó **el 28/jul**, un día después de que `curaduria-archivos.md:66` declarara "ya se ejecutó". La afirmación del 27/jul no era una corrección tardía de un hecho verdadero — era, en el momento en que se escribió, **falsa**: nadie había corrido el `grep` contra la fuente antes de marcarla ✅.

## Patrón

Es el mismo defecto que el propio glosario documenta cuatro veces en su §14 (Hofstede, honor-comunicación, honor-foundational, marianismo): *"un ADR de retropropagación no se marca aplicado sin `grep` contra el report dueño"*. `curaduria-archivos.md:66` es una quinta instancia del mismo patrón, en un archivo que ninguna de las cuatro correcciones de §14 había señalado.

## Qué NO hace falta corregir aguas abajo

Ningún artefacto canónico vigente (`glosario`, `gobernanza`, `estado`) hereda esta afirmación falsa — todos ya reflejan el estado real (parchado 28/jul), verificado en `glosario §14`. El error queda contenido en `curaduria-archivos.md:66`, un documento fechado y no consultado como fuente de estado vigente. Esta nota existe para que quien lea `curaduria-archivos.md` de punta a punta no se quede con la lectura errónea, ya que nada dentro de `forense/` remitía hacia la corrección real antes de esta nota.

*(Hallazgo original: `censo-integridad-v1_0.md` C3-07.)*
