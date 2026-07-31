# Sonda de alcanzabilidad: descarga dirigida ENOE/ENIF/ENVIPE/ENCIG (E-G)

**Fecha:** 31 de julio de 2026 (sondeado 30-31/jul, sesión Ubuntu local — única vertiente con salida a dominios de datos mexicanos)

---

## 0. Vocabulario, sin colapsar (v2.2, corolarios 1 y 2)

- **RESPONDE** — el host contesta desde este entorno.
- **NO ALCANZABLE DESDE ESTE ENTORNO** — política de egreso, pasarela, DNS. No se observó ningún caso de este tipo esta sesión.
- **RESPONDE PERO SIN EL RECURSO** — el host contesta y la ruta específica no tiene el dato.

"No pude alcanzar la fuente" y "la fuente no tiene el dato" son hallazgos distintos. Ninguno de los dos es "no alcanzable".

---

## 1. Host `www.inegi.org.mx`: RESPONDE

Confirmado contra: `/` (raíz del portal), `/programas/enoe/15ymas/` (página de programa, SPA), los paths estáticos `/contenidos/programas/{prog}/{año}/datosabiertos/` y `/contenidos/programas/{prog}/{año}/doc/`, y el catálogo de microdatos `/rnm/index.php/catalog/`.

Ningún caso de **NO ALCANZABLE DESDE ESTE ENTORNO** contra este host esta sesión: no hubo 403 de política de egreso, ni 000 de CONNECT rechazado, ni verify error de cadena TLS del servidor. `curl -k` no se usó ni fue necesario.

Fuera de alcance esta sesión (no tocado, no reportado con estado): `datos.gob.mx`. El encargo cita como precedente que ese host tiene la cadena TLS rota del lado del servidor, pero no era uno de los objetivos asignados (Parte 2: ENOE, ENIF, ENVIPE, ENCIG, todos en inegi.org.mx) y no se sondeó.

---

## 2. Hallazgo central: inegi.org.mx sirve un "soft-404" con HTTP 200

Cualquier ruta inexistente bajo `/datosabiertos/` o `/doc/` devuelve **HTTP 200** con:

```
Content-Type: text/html
Content-Length: 2263
Last-Modified: Fri, 07 Dec 2018 22:52:56 GMT
```

Es una página de error estática fija en todo el sitio ("Esta liga ya no existe, lamentamos el inconveniente" / "Página no encontrada"). El código HTTP por sí solo **no distingue** RESPONDE de RESPONDE-PERO-SIN-RECURSO en este host — hay que leer `Content-Type`/`Content-Length`/`Last-Modified`, no solo el status.

Ejemplo RESPONDE (recurso real): `conjunto_de_datos_enoe_2020_1t_csv.zip` → `Content-Type: application/x-zip-compressed`, `Content-Length: 43904494`, `Last-Modified: Mar 2024`.

Ejemplo RESPONDE PERO SIN EL RECURSO: el ZIP inventado de ENOE 2026 Q4 (trimestre que no debería existir aún, y no existe) devuelve la firma de soft-404 de arriba. Mismo resultado en las ~30 variantes de nombre de archivo probadas para descriptores de ENIF/ENVIPE/ENCIG-2019/ENOE (§5).

---

## 3. El JSON-LD de las páginas de programa no es fuente confiable de URLs

Cada página `/programas/{prog}/{año}/` trae un `<script type="application/ld+json">` con un campo `"distribution"` que declara **un solo** `contentUrl` de muestra — no la cobertura completa — y a veces ni siquiera es real: el de ENVIPE 2024 apunta a `.../app/administracion/sasi/prueba.pdf`, un placeholder de plantilla que al pedirse da la firma de soft-404 de §2. Sirve solo como pista del patrón de nombre, nunca como fuente de verdad sobre qué existe.

---

## 4. El catálogo de microdatos (`/rnm/index.php/catalog/`) SÍ es navegable por curl

A diferencia de `/programas/`, que es una SPA, el catálogo (`inegi.org.mx/rnm/index.php/catalog/`) responde con HTML real y enlaces directos (`/catalog/{id}/download/{n}`, `/catalog/{id}/data-dictionary`). Se localizó ahí la entrada 1121 para "ENOE", pero corresponde a un producto **distinto**: tablas de indicadores mensuales/trimestrales, no microdatos. Su "Diccionario de Datos" (descarga 35003, "Diccionario de datos de las tablas de indicadores") describe esas tablas de indicadores, no la estructura de los CSV de microdatos bajados esta sesión — no sirve como descriptor de lo bajado. El endpoint `/catalog/1121/technicaldocuments` de esa misma entrada devolvió **HTTP 500**.

---

## 5. Tabla de objetivos sondeados

| Host / patrón de ruta | Estado | Mecanismo |
|---|---|---|
| `www.inegi.org.mx` (raíz) | RESPONDE | HTTP 200, portal real |
| `.../enoe/15ymas/datosabiertos/{2019Q1..2020Q1}` | RESPONDE | naming `enoe`, edición clásica pre-pandemia |
| `.../enoe/15ymas/datosabiertos/2020Q2` | RESPONDE PERO SIN EL RECURSO | hueco real de la fuente — campo suspendido por contingencia sanitaria (abril 2020), no un error de sondeo |
| `.../enoe/15ymas/datosabiertos/{2020Q3..2022Q4}` | RESPONDE | naming `enoen`, ENOE Nueva Edición |
| `.../enoe/15ymas/datosabiertos/{2023Q1..2026Q1}` | RESPONDE | naming revierte a `enoe`, pero metodológicamente sigue siendo ENOEN — ruptura de **nombre**, no de dato |
| `.../enoe/15ymas/datosabiertos/2026Q2` en adelante | RESPONDE PERO SIN EL RECURSO | aún no publicado, consistente con rezago editorial real |
| `.../programas/encig/{2015,2017,2021}/doc/encigYY_estructura_base_datos.pdf` | RESPONDE | descriptor real, patrón de nombre encontrado por script |
| `.../programas/encig/2019/doc/...` (9 variantes probadas) | RESPONDE PERO SIN EL RECURSO | no implica que el documento no exista — solo que el nombre de archivo no se pudo adivinar por script |
| `.../programas/{enif,envipe}/.../doc/...` (~20 variantes probadas) | RESPONDE PERO SIN EL RECURSO | mismo matiz que arriba |
| `.../programas/{enoe,enif,envipe,encig}/{año}/` (páginas de programa) | RESPONDE, pero SPA | el HTML crudo es un shell de ~5-6 KB con componentes custom (`<menu-gen>`, `<pestanas-gen>`, etc.), sin ningún `href` real; el contenido de las pestañas "Microdatos"/"Documentación" se renderiza client-side. **No es** "no alcanzable" ni "sin recurso" — es una tercera cosa: el recurso existe pero solo lo expone un navegador real, no un cliente headless |

---

## 6. Pendiente de navegador

Lista exacta de lo que un headless no puede completar, y por qué (mismo mecanismo en todos: SPA no expone el enlace a curl — ya documentado en este repo para ENCUCI/ENUT, ver id `hitoD_fase1_ediciones_requieren_navegador` en `data/manifiesto.yaml`):

- **Descriptor de ENOE**, ambas ediciones (clásica y Nueva Edición).
- **Descriptores de ENIF**: 2018, 2021, 2024.
- **Descriptores de ENVIPE**: 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 (ocho ediciones).
- **Descriptor de ENCIG 2019** (2015, 2017 y 2021 sí se localizaron por script — ver §5).

Esta es la lista que el autor tiene que bajar a mano desde la pestaña Microdatos/Documentación de cada portal.

---

## 7. Contaminación de esta sesión (ADR-46)

Esta sesión leyó y tocó `inegi.org.mx`: páginas de programa (incluido su JSON-LD embebido), el catálogo de microdatos, y el host estático de `datosabiertos`/`doc`. Por diseño (ADR-46: la unidad de contaminación es la sesión, no la máquina), **queda contaminada para pre-registrar contra cualquiera de estas fuentes**. El pre-registro correspondiente lo hace otra sesión, no esta.
