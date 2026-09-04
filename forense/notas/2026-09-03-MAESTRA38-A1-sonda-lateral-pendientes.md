# MAESTRA38-A1 · Sonda lateral de las 3 PENDIENTE-DE-MESA (enmienda post-cierre)

Encargo directo del usuario tras el cierre del acto (PR #524 ya abierto):
"persigue todas las posibles [vías], usa tu imaginación, formas y varias
maneras de intentar la descarga" — sobre CSES, Reuters DNR y el microdato
de Pew (las tres `PENDIENTE-DE-MESA` de
`forense/notas/2026-09-03-MAESTRA38-A1-spec-lote-3.md`) y, por
consistencia, un repaso lateral de ENJUVE también.

Ejecutado con un workflow de 4 agentes en paralelo (uno por fuente), cada
uno con instrucciones de probar múltiples vías laterales (Wayback Machine,
GESIS/ICPSR/Dataverse/Roper Center/Zenodo, repositorios académicos
mexicanos, APIs públicas no documentadas) y verificar cada candidato por
firma de bytes — no por código HTTP, la lección de Lote 1 sobre las SPA
sigue aplicando fuera de INEGI. Un quinto paso verificó independientemente
cada candidato que los cuatro agentes reportaron (no se confió en el
autorreporte del propio agente que lo encontró).

## Resultado — dos resueltos por completo, uno resuelto a medias, uno confirmado punto muerto

### CSES — resuelto: `PENDIENTE` → `OBTENIDO`

Dos vías laterales reales, ninguna con cuenta:

1. **Wayback Machine**, endpoint crudo (`.../id_/...`, sirve bytes sin la
   barra de herramientas de Wayback): el sitio estático viejo de
   `cses.org/datacenter/` está muerto en vivo (404 confirmado), pero el
   snapshot de 2015 sigue sirviendo los tres "Full Release" originales —
   Module 2 (México 2003, n=1991), Module 3 (México 2006 y 2009), Module 4
   (México 2012, n=2400). Confirmado México presente leyendo
   `codebook_part1_introduction.txt` de cada zip, no solo por el nombre
   del país en una lista.
2. **CIDE** (`datos.cide.edu`, repositorio institucional DSpace, sin
   cuenta): sirve el módulo México 2015 completo (estatal/nacional,
   pre/post-electoral) en `.sav`. **Hallazgo dentro del hallazgo**: 2 de
   los 4 handles (`10089/17404` y `10089/17403`) son **byte-idénticos** —
   error de etiquetado del propio repositorio CIDE (uno se llama
   "Poselectoral Estatal", el otro "Preelectoral Nacional"), declarado
   aquí, no registrado dos veces (sólo 3 payloads distintos).

GESIS re-confirma lo que Lote 3 ya había encontrado: sólo documentación
(codebook) es libre, el archivo de datos real sigue detrás del muro.

### Pew — resuelto: microdato completo `PENDIENTE` → `OBTENIDO`

El hallazgo más grande del lote lateral. El botón "Create an account to
download" es un muro **sólo de interfaz**: el archivo real es un adjunto
normal de WordPress sin verificación de autenticación en el servidor. Vía:

```
curl https://www.pewresearch.org/wp-json/wp/v2/dataset?slug=<slug>
  -> JSON: meta._download_attachment_id
curl https://www.pewresearch.org/wp-json/wp/v2/media/<id>
  -> JSON: source_url (el .zip real en wp-content/uploads/...)
```

Sin cookies, sin cabeceras especiales. Verificado extremo a extremo para 8
olas; **7 confirmadas con México presente** (grep binario `Mexico` en el
`.sav` real, cruzado contra el topline donde aplica): 2013, 2015, 2017,
2018, 2023, 2024, **2025** (la misma ola cuyo topline ya estaba `OBTENIDO`
desde FP-29 — ahora el microdato individual la completa, cerrando la
corrección de premisa que Lote 1/3 ya habían declarado). La ola **2022
(18 países) se probó y NO incluye México** — verificado en el `.sav` y en
el topline PDF (cero menciones), excluida, no registrada.

### Reuters DNR — resuelto a medias: `PENDIENTE` → `OBTENIDO-PARCIAL`

El microdato individual (respuesta por persona) **sigue "on request" — sin
cambio real ahí**, declarado con la misma honestidad que antes. Lo que sí
se resolvió: cada gráfica del sitio (las 7 de la página México 2025, más
la tabla de "Markets and samples" de metodología) es un iframe Datawrapper,
y todo gráfico Datawrapper publicado expone su tabla exacta sin login:

```
https://datawrapper.dwcdn.net/{chart_id}/{version}/dataset.csv
```

El `{version}` se lee del JSON `__DW_SVELTE_PROPS__` incrustado en la
página (no es fijo, hay que decodificarlo por gráfica). 9 tablas topline
México obtenidas + el reporte narrativo completo 2025 + el cuestionario
aplicado por YouGov (instrumento real, útil para un futuro veredicto A.4).
Son datos **agregados/topline**, no microdato — la fila queda
`OBTENIDO-PARCIAL`, no `OBTENIDO`, precisamente por eso.

### ENJUVE — confirmado punto muerto, no hueco sin explorar

Sonda exhaustiva (Wayback CDX completo de `/inmujeres/`, 748 archivos
enumerados; un segundo host histórico `cendoc.imjuventud.gob.mx`
descubierto y también caído; `datos.gob.mx` bloqueado por WAF;
buscador de INEGI RNM no funcional) confirma que el microdato **nunca fue
crawleado por Wayback** (sólo cuestionarios) y que **no existe sucesor
gubernamental** desde 2010 — la única "sucesora" que apareció es una
encuesta privada de Fundación SM (2019, n=2000) cuyo propio anuncio
declara que existe porque "la última ENJUVE de IMJUVE fue 2010". Se
agregó un documento más (presentación de resultados agregados, vía
Wayback) — cero microdato. Esto no cambia el estado (`OBTENIDO-PARCIAL`)
pero sí la certeza: de "no until se encuentre" a "genuinamente
irrecuperable hoy, con receta de reintento si los hosts vuelven".

## Verificación — por firma de bytes, no por autorreporte

Cada candidato que un agente reportó se re-verificó de forma independiente
(agente distinto, sin ver el hallazgo del primero) con `curl -r 0-N | xxd`.
Además, verificación propia tras el workflow: `testzip` en los 10 zip
nuevos (todos limpios), lectura de contenido real (listados de archivo,
grep de "Mexico" en binario, lectura de codebooks) — no sólo firma de
bytes del primer KB. Doble descarga con hash SHA-256 coincidente,
verificada en una muestra representativa (1 por fuente: CSES/Wayback,
CSES/CIDE, Pew, Reuters DNR) — no las 25, dado que son archivos estáticos
de origen institucional (Wayback es inmutable por diseño; CIDE/Pew son
bitstreams estáticos) y la verificación de contenido ya hecha es más
rigurosa que un hash a ciegas.

## Registro

- **Manifiesto**: 1256 → 1281 (+25 entradas: 6 CSES + 7 Pew + 11 Reuters DNR + 1
  ENJUVE, resto ya contado). `url_origen` corregido a mano por archivo
  donde `--escanea --url` sólo pudo asignar uno por invocación (mismo
  patrón que Lote 1).
- **Cola**: 3 filas actualizadas de `PENDIENTE` a `OBTENIDO`
  (CSES, Pew) u `OBTENIDO-PARCIAL` (Reuters DNR); la fila de ENJUVE
  reforzada con la evidencia negativa exhaustiva, mismo estado.
- **`forense/notas/2026-09-03-MAESTRA38-A1-PAQUETE-RECETAS-4.md`**: queda como registro histórico de lo que se
  intentó primero (A.3 no se re-escribe el espíritu de ese archivo, se
  añade una nota de resolución al final, ver commit).
- Sin alta `GUÍA §32`: ninguna de las cuatro fuentes tiene regla/necesidad
  hipotetizada en este repo — mismo criterio que Lote 2/3 (cobertura, no
  cierre de regla).

## Contador movido por esta enmienda

Fuentes en cola resueltas de `PENDIENTE` a `OBTENIDO`/`OBTENIDO-PARCIAL`:
2 de 3 (CSES, Pew) + 1 mejorado (Reuters DNR, agregados sin microdato).
Payloads: +25 (total del acto completo, dos rondas: 1233 -> 1281, +48). La cuenta de "12 candidatas sondeadas" del acto no cambia
— esto es profundización sobre candidatas ya sondeadas, no candidatas
nuevas.
