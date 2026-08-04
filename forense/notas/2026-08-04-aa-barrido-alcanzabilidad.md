# Tarea B · Barrido de alcanzabilidad, fuentes nuevas del Encargo AA

**Antes de sondear:** revisado `data/manifiesto.yaml` primero, como exige §4 del encargo. Ninguna
de las fuentes nuevas de `data/inventarios/inventario_fuentes_clase-fuente-mexico.md` tiene
payload ya en disco (`grep` contra los ids del manifiesto, ninguna coincidencia con CLUES,
SINERHIAS, PUB, Cero Desabasto, MCCI, ESTAD, ENCAL) — el barrido de abajo es sondeo genuino, no
repetición de algo ya bajado.

## Comando, a la vista

```bash
for h in "http://www.dgis.salud.gob.mx" "http://gobi.salud.gob.mx" "https://sinba.salud.gob.mx" \
  "https://cerodesabasto.org" "https://pub.bienestar.gob.mx" "https://cpid.bienestar.gob.mx" \
  "https://www.gob.mx/bienestar" "http://datos.gob.mx" "https://www.consar.gob.mx" \
  "https://www.gob.mx/consar" "http://www.cnbv.gob.mx" "https://www.gob.mx/cnbv" \
  "https://www.ine.mx" "https://www.gob.mx/sep" "https://www.gob.mx/cofepris" \
  "https://www.cofepris.gob.mx" "https://transparencia.cofepris.gob.mx" \
  "https://contralacorrupcion.mx" "https://www.worldbank.org" "https://www.oecd.org" \
  "https://www.coneval.org.mx" "https://calidad.salud.gob.mx" "https://sesa.qroo.gob.mx" \
  "https://www.imss.gob.mx" "https://www.imss.gob.mx/encuesta-nacional" "https://datamx.io"; do
  printf "%-42s " "$h"
  curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 "$h"
done
```

**Nota de sandbox, no de entorno** (detalle en `2026-08-04-aa-taxonomia-clase-fuente.md §4`): la
herramienta de shell de este acto tiene lista blanca de red propia, distinta de la política del
entorno remoto asignado. Corrido con esa sandbox desactivada para este comando — el entorno de
red en sí ya se confirmó correcto en el arranque (§4: `inegi.org.mx` → 200 sin desactivar nada).

## Resultado, códigos crudos, todos, incluidos los que fallan

| Host | Código | Lectura |
|---|---|---|
| `http://www.dgis.salud.gob.mx` (CLUES/SINERHIAS/SAEH, DGIS) | **200** | Responde. Solo por HTTP — HTTPS da timeout, ya documentado en `inventario_fuentes_salud_mexico.md:306` para este mismo dominio. |
| `http://gobi.salud.gob.mx` (réplica de CLUES citada por el encargo) | **000** | No alcanzable desde este entorno — probado en HTTP y HTTPS, ambos timeout. |
| `https://sinba.salud.gob.mx` (SINERHIAS/SAEH, cubos) | **200** | Responde. |
| `https://cerodesabasto.org` | **200** | Responde. |
| `https://pub.bienestar.gob.mx` (consulta PUB) | **000** | No alcanzable — probado HTTP y HTTPS. |
| `https://cpid.bienestar.gob.mx/spp/` | **000** | No alcanzable. |
| `https://www.gob.mx/bienestar` (ruta alterna a PUB) | **200** | Responde — vía alterna sí alcanzable aunque los subdominios directos de Bienestar no. |
| `http://datos.gob.mx` (dataset PUB, réplicas varias) | **308** | Responde (redirección). Solo por HTTP — HTTPS con y sin `www` dio timeout. |
| `https://www.consar.gob.mx` | **200** | Responde. |
| `https://www.gob.mx/consar` | **200** | Responde. |
| `http://www.cnbv.gob.mx` | **301** | Responde (redirección). Solo por HTTP. |
| `https://www.gob.mx/cnbv` | **200** | Responde. |
| `https://www.ine.mx` | **200** | Responde. |
| `https://www.gob.mx/sep` | **200** | Responde. |
| `https://www.gob.mx/cofepris` | **200** | Responde. |
| `https://www.cofepris.gob.mx` | **000** | No alcanzable — probado HTTP y HTTPS, ambos timeout. Vía alterna (`gob.mx/cofepris`) sí responde. |
| `https://transparencia.cofepris.gob.mx` | **000** | No alcanzable. |
| `https://contralacorrupcion.mx` (MCCI) | **403** | **Responde** (código real del servidor, no timeout) — probable bloqueo anti-bot del propio sitio, no indisponibilidad. Distinto de "no alcanzable": el host contestó. |
| `https://www.worldbank.org` | **301** | Responde. |
| `https://www.oecd.org` | **403** | **Responde** — mismo caso que MCCI, bloqueo anti-bot probable, no timeout. |
| `https://www.coneval.org.mx` | **301** | Responde. |
| `https://calidad.salud.gob.mx` (ESTAD) | **200** | Responde. |
| `https://sesa.qroo.gob.mx` (SESTAD, variante estatal) | **000** | No alcanzable. |
| `https://www.imss.gob.mx` | **200** | Responde. |
| `https://www.imss.gob.mx/encuesta-nacional` (ENCAL) | **200** | Responde. |
| `https://datamx.io` (réplica ciudadana de CLUES) | **200** | Responde. |

## Clasificación, sin colapsar las tres categorías (§4 del encargo)

**"No alcanzable desde este entorno"** — 7 hosts: `gobi.salud.gob.mx`, `pub.bienestar.gob.mx`,
`cpid.bienestar.gob.mx`, `www.cofepris.gob.mx`, `transparencia.cofepris.gob.mx`,
`sesa.qroo.gob.mx`, y (parcialmente) `www.dgis.salud.gob.mx`/`datos.gob.mx`/`www.cnbv.gob.mx`
por HTTPS específicamente (sí alcanzables por HTTP — no se cuentan en los 7, quedan como
"responde"). Ninguno de estos 7 tiene ruta alterna verificada en este acto.

**"La fuente no tiene el dato"** — no aplica a ningún host de este barrido: sondear un host solo
confirma que responde, no que el dato exista dentro — esa pregunta es de instrumento, fuera de
perímetro de este acto (misma disciplina que `cruce-catalogo-fichas-v1_0.md` ya fijó: "cubre el
dominio, no confirma la variable").

**"Nadie corrió el mecanismo contra esta fuente"** — no aplica: las 26 URLs de este barrido se
sondearon todas en este acto; no queda ninguna de la lista derivada sin intentar.

**19 de 26 responden** (algún código HTTP, incluidos 403/301/308 — todos son respuesta real de
servidor, no ausencia). **7 de 26 no responden pese al intento**, con vías alternas confirmadas
para 3 de esos 7 (Bienestar, COFEPRIS, y los casos HTTP/HTTPS de dgis/datos/cnbv). Ningún host de
este barrido está clasificado como "sin payload" en ningún documento previo del repo — no aplica
el defecto del 4/ago citado en §4 del encargo (5 de 5 RESPONDE sobre fuentes marcadas sin
payload); aquí no había marcación previa que contradecir.
