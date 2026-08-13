**SHA de redacción:** `e993752` (merge #202)
**Entorno asignado:** CAJA con red. NO en nube — mide alcanzabilidad de portales y la nube da 403 `host_not_allowed`. NO en los dos.
**Estado:** CONSUMIDO — `PR #205` (rama `vp/verifica-puertas`, merge `b7aa67c`, ancestro confirmado de `fd788a9`). *Corrección de ACTO E2, 13/ago/2026: este archivo seguía marcado `VIVO` pese a estar fusionado; ver `forense/notas/2026-08-13-e2-cierre.md`.*

---

ENCARGO VERIFICA-PUERTAS · quién puede bajar qué, con vocabulario cerrado
y, al final, la cola completa de lo que queda por correr, por entorno
SHA de redacción: e993752 (merge #202). Entorno: CAJA con red. NO en nube — mide alcanzabilidad de portales y la nube da 403 host_not_allowed. NO en los dos.
Estado: VIVO. Sin gate: no depende de ningún PR abierto.

§0 · Por qué existe — el defecto, medido

El puntero de puertas tiene 114 filas. De ellas, 52 traen sondeo real de portal y 62 declaran universo interno ("buscada en el puntero y en la cola-adquisicion por nombre exacto y por URL") — esas 62 no son un veredicto sobre el mundo, son "no está en nuestras tablas".

Y las 52 no se pueden leer mecánicamente. El campo condicion_acceso es texto libre. Prueba de que falla: una lectura por patrón clasificó como "requiere cuenta" filas cuyo texto dice "libre, descarga directa sin registro ni sesion" — casó la palabra sin leer la negación. Es el mismo defecto de subcadena que este programa ya midió tres veces (SE→"falsador", PI→"estimación propia", INE→"diccionario").

Consecuencia operativa, que es la que duele: no existe hoy ninguna forma derivable de contestar "¿esta fuente la puede bajar el agente, la tengo que bajar yo, o no la puede bajar nadie?". Se ha contestado a mano cada vez, y se ha contestado mal — un agente declaró imposible lo que el usuario bajó después con tres clics, tres veces.

Y se degrada solo: 26 de los 52 sondeos son del 8/ago, hechos antes de que existiera el override de sandbox y antes de que el vocabulario A.4/A.5 estuviera completo. Once filas dicen literalmente "no verificado", "no determinada" o "bloqueado esta sesion" — no son veredicto, son hueco con etiqueta.

§1 · PERÍMETRO

ESCRIBE: data/acceso-puertas-2026-08-13.tsv (nuevo) · forense/notas/2026-08-13-verifica-puertas.md (1) · forense/hallazgos.md (append, merge local siempre) · forense/encargos/2026-08-13-VP-verifica-puertas.md (A.3 — prefijo de acto obligatorio, la nota va sin él; T02 normaliza sin distinguir directorio y ha mordido a cinco actos, ver forense/encargos/convencion.md).

NO ESCRIBE: data/universo-puertas-2026-08-12.tsv (ni una fila — es de otro carril y P·LOTE-2 puede estar añadiéndole) · data/cola-adquisicion-*.tsv · data/manifiesto.yaml · data/curacion-registro/** · canon/** · tools/** · tests/** · data/raw/**.

Este acto NO descarga nada. Sondea y clasifica.

En paralelo: P·LOTE-2 (caja, descargando — añade filas al puntero, por eso este acto no lo toca) y ALIAS-P (repo). Perímetros disjuntos salvo hallazgos.md (merge=union; GitHub no lo honra, merge local, editor web prohibido).

Carga: MEDIA-BAJA. Sondas HTTP, sin descarga de payload. No compite con P·LOTE-2 por memoria, pero sí por red y por override — si P·LOTE-2 sigue vivo, coordina o espera.

§2 · ARRANQUE

1 · REPO. Clon existente. Ruta absoluta · git log -1 --format="%h %s" · git status. No desde el home. Worktree propio. 2 · SHA. Base e993752. Refresca y reporta la diferencia. No es PARO. 3 · data/raw. No aplica — no descarga. Decláralo y salta. 4 · ENTORNO. echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]" → sin variable · curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ → 200. NUNCA curl -I. Si da 403 host_not_allowed: PARA, entorno equivocado. 4-bis · OVERRIDE. Reporta si el override de sandbox está disponible en esta sesión y contra qué dominio lo comprobaste. De ello depende la mitad del universo: SONDA-1 midió que solo inegi.org.mx y banxico.org.mx están en allowlist directo. 5 · ESPEJO. Ninguna cifra del espejo.

PREMISAS (script, crudas):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l          # filas del puntero
awk -F'\t' 'NR>1 && $4 ~ /^http/' data/universo-puertas-2026-08-12.tsv | wc -l   # con URL sondeable
ls data/acceso-puertas-*.tsv 2>/dev/null && echo "YA EXISTE - PARA"
```

Lecturas obligatorias, íntegras — sus barreras ya están pagadas, NO las re-descubras: forense/notas/2026-08-12-acto-sonda1-mapa-barreras.md (§5 por fuente, §6 recetas, §7 PRISMA) · forense/notas/2026-08-12-acto-p-lote1-adquisicion.md (§5.1 Cloudflare de GESIS con 11 intentos, §11 el patrón descargas_mx).

§3 · COMMIT 1 — el vocabulario cerrado, antes de sondear
3.1 · La columna que falta, y es la razón de ser del acto

quien_puede, enum cerrado de cinco valores. Es la respuesta a "¿quién baja esto?" y nada más:

| valor | significa | criterio, verificable |
|---|---|---|
| AGENTE | un agente con curl lo baja hoy | responde 200/206 y el payload se alcanza sin cookie de sesión y sin resolver JavaScript |
| USUARIO_REGISTRO | necesitas cuenta, la cuenta es gratuita | el portal muestra formulario de registro sin pago ni afiliación institucional |
| USUARIO_NAVEGADOR | necesitas un navegador real, no cuenta | reto anti-bot (Cloudflare cf-mitigated: challenge, AWS WAF x-amzn-waf-action: challenge) que se resuelve solo con JS |
| NADIE | ni tú ni el agente, sin cambiar de condición | pago confirmado, o afiliación institucional, o acuerdo de uso restringido |
| NO_PROBADO | nadie ha corrido el mecanismo contra esta puerta | incluye las 62 de universo interno |

Regla que no se puede violar, y es la que el usuario pidió por nombre: el código HTTP crudo se registra siempre y no se interpreta solo. Un 403 puede ser reto anti-bot (→ USUARIO_NAVEGADOR), muro de pago (→ NADIE) o allowlist de la caja (→ no dice nada del portal, es límite del entorno). Un 200 en la portada no significa que el payload baje. Las tres columnas son distintas y no se colapsan: http_sin_override · http_con_override · quien_puede.

3.2 · El universo, declarado y priorizado

Las que tienen URL sondeable, en tres tandas:

Las 13 de tu cola manual hoy — las 5 USUARIO_REGISTRO presuntas + las 8 bloqueadas. De estas, cuatro llevan desde el 8/ago sin reintento: Mejoredu_INEE_Bases_Datos, CIDE_Panel_Mexico_2006, DataCivica_Explorador_Violencia, Tandas_para_el_Bienestar. Van primero: su clasificación vieja es de antes del override.
Las 11 filas que declaran "no verificado" / "no determinada" / "bloqueado esta sesion" — no son veredicto, son hueco.
Las 21 de cubeta D (responden pero no sirven) — solo se re-clasifica quien_puede, NO se re-juzga si sirven. Eso es de otro acto.

Fuera de alcance, declarado: las 62 de universo interno entran al TSV como NO_PROBADO sin sondearse — sondearlas es un lote propio y este acto no lo hace. Ponerlas con su etiqueta correcta ya vale, porque hoy figuran como NO-ENCONTRADO, que se lee como "no existe".

3.3 · Pre-registro de falsación (B-bis)
Si una fila cambia de cubeta, esa es la noticia. Precedente medido: WVS pasó de "NO OBTENIDO POR ESTE AGENTE EN 6 INTENTOS" a EXISTE-SATISFACE cuando el usuario se registró. Cuatro filas del 8/ago nunca se reintentaron con override.
Si nada cambia, el acto igual entrega el artefacto que no existe: una columna derivable que contesta quién baja qué. Ese es el entregable, no el cambio.
Si el override no está disponible en esta sesión: se sondea sin él, se marca http_con_override = NO_DISPONIBLE_EN_ESTA_SESION, y no se clasifica AGENTE a ninguna que no esté en allowlist directo. Declararlo, no adivinarlo.

Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

§4 · COMMIT 2 — el sondeo

data/acceso-puertas-2026-08-13.tsv:

puerta · url · http_sin_override · http_con_override · cabecera_diagnostica ·
quien_puede · receta_manual · fuentes_que_sirve · fecha_sondeo · universo_declarado
cabecera_diagnostica: la cabecera que decidió la clasificación, verbatim — cf-mitigated: challenge, x-amzn-waf-action: challenge, x-deny-reason: host_not_allowed, www-authenticate. Es lo que distingue un 403 de portal de un 403 de caja, y es exactamente lo que se ha confundido antes.
receta_manual: obligatoria para todo USUARIO_*, ejecutable en navegador en menos de un minuto. "La receta no es el consuelo del acto: es su entregable de mayor rendimiento, medido" — el usuario ya bajó a mano, tres veces, lo que un agente declaró imposible.
quien_puede = AGENTE exige haber alcanzado el payload, no la portada. GET -r 0-0 y el tamaño real. SONDA-1 encontró en INEGI un contentUrl señuelo a prueba.pdf (soft-404 de 2,263 bytes fijos). No te creas la portada.

Cierre: conteo por quien_puede (los cinco valores, suman el total) · cuántas filas cambiaron de cubeta y cuáles · y la lista de descarga manual del usuario, ordenada por cuántas necesidades sirve cada fuente — ese listado es el producto que hoy no existe.

Suite: --baseline VERDE contra 948ad70. T03: no cites gitignorados entre backticks.

§5 · NO HACE

No descarga ningún payload. No toca el puntero de puertas ni la cola. No re-juzga si una fuente sirve al modelo (eso es de M-APERTURA/mesa). No sondea las 62 de universo interno — las etiqueta NO_PROBADO y lo dice. No fuerza ninguna fuente al carril del agente si su dominio no alcanza.

LA COLA COMPLETA · qué queda, por entorno (contexto del encargo, no ejecutado por este acto — ver forense/hallazgos.md de este mismo acto para el estado en que se recibió)
