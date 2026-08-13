# ENCARGO ACTO SONDA-1 — el mapa de barreras que le falta a la firma del Lote 2

- **SHA de redacción**: `b17a6f6` (verificado en ARRANQUE de este acto: `origin/main` estaba exactamente en `b17a6f6` al abrir el worktree — sin deriva que re-derivar).
- **Entorno asignado**: caja Ubuntu, worktree propio. Prohibido nube (medido: 403 host_not_allowed) y prohibido lanzarlo en los dos entornos a la vez.
- **Estado**: `VIVO`.

Archivado per convención de este directorio (`forense/encargos/convencion.md`), como primer commit de este acto, antes de ejecutar el resto del bloque de ARRANQUE — Regla A.3 (`instrucciones-proyecto-v2_5.md`, Bloque D-bis).

---

## Texto completo del encargo, tal como se recibió

════════════════════════════════════════════════════════════════════════
§3 · ENCARGO ACTO SONDA-1 — el mapa de barreras que le falta a la firma del Lote 2

Por qué existe, medido y no supuesto. Revisé las 62 filas gap_mapeo_map_b del puntero de puertas. Su campo universo_declarado dice, las 62, verbatim:

"buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)"

El universo de búsqueda fueron las dos tablas internas del propio programa. Ningún portal. A.4 se cumple —el universo está declarado, y honestamente— pero NO-ENCONTRADO aquí significa "no tiene fila en nuestro puntero", no "no hay puerta". 43 de las 44 fuentes pendientes nunca han sido sondeadas contra un portal.

Es la tercera variante de v2.4, literal: no es que el entorno no llegue, ni que el recurso no exista — es que nadie corrió el mecanismo de resolución contra ellas.

Y por eso la firma propuesta del Lote 2 en el PLAN v1 (GDELT·11 · ENCOAP·17 · WB_ENTERPRISE·9) está mal ordenada: elige tres fuentes sobre las que nadie sabe nada, se salta palancas 12 y 16 que también tienen URL, y gasta la caja —el recurso escaso— en tres sondas. Un acto de sondeo puro sobre las 15 cuesta lo mismo que bajar una fuente y devuelve el mapa completo de barreras, que es justo lo que le falta a la firma para no ser una apuesta.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status. ⚠️ No arranques desde el home.

2 · SHA. Este encargo se redactó contra b17a6f6. Si main se movió: NO es PARO — refresca, re-deriva el §1 de premisas, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Este acto no descarga nada, así que ni se crea ni se enlaza — dilo y sigue.

4 · ENTORNO. echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]" → esperado: sin variable · curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ → esperado 200. Reporta los dos valores crudos. NUNCA curl -I. Si la sonda da 403 host_not_allowed, estás en el entorno equivocado: PARA — este acto es inútil sin red a dominios de datos.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

ENTORNO ASIGNADO: caja Ubuntu, worktree propio. NO lo lances en la nube. (La nube no alcanza dominios de datos — medido: 403 host_not_allowed.) Y no lo lances en los dos.

PERÍMETRO Y CONCURRENCIA. Este acto toca: data/universo-puertas-2026-08-12.tsv (SOLO filas nuevas, jamás editar filas ajenas) · forense/notas/ (1 nota) · forense/encargos/ (A.3) · forense/hallazgos.md (union, merge local siempre). Corre en paralelo: el acto de nube de ENLACE-1 (perímetro disjunto: él toca relaciones.tsv, este no) y U3 si mesa lo lanza (mismo puntero — cada quien añade filas). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

PREMISAS (script — repórtalas crudas, no las interpretes):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
ls data/cola-adquisicion-*.tsv | sort | tail -1              # la cola vigente
awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l   # filas del puntero, valor crudo
awk -F'\t' 'NR>1 && $2=="gap_mapeo_map_b"' data/universo-puertas-2026-08-12.tsv | wc -l  # las filas de universo interno
```

Y la premisa que sí puede PARAR el acto: lee íntegra forense/notas/2026-08-12-acto-p-lote1-adquisicion.md. Sus §5.1-§5.5 ya mapearon las barreras de GESIS, WVS, Banco Mundial, GPS y CSES. No re-descubras Cloudflare. Si una fuente de tu lote está ahí con barrera ya documentada, cita la nota y no la vuelvas a sondear.

Commit 1 — el lote de sondeo, congelado antes de tocar red

Las 15 fuentes. Derivadas en sesión así (corre el filtro, no copies mi lista — si difiere, reporta la diferencia y usa la tuya): de las 54 de la cola, las que tienen url_conocida con http, menos las ya cerradas EXISTE-SATISFACE contra portal (ISSP·1, CSES·7), menos las dos que el usuario está resolviendo por su carril (EARLY_CHILDHOOD·4, GPS·6), menos las dos NEGATIVA selladas cuya reapertura es de mesa (BRASDEFER·2, MOBILE_TUTORS·5 — plan-descargas-completo §8), menos la ya sondeada contra portal y cerrada NO-ACCESIBLE (MEXICO_PANEL_STUDY·18, ICPSR exige afiliación).

Lo que queda, por palanca, para congelar verbatim en este commit:

pal    fuente    nec    FIN    URL de la cola
9    WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023    3    NO    https://microdata.worldbank.org/catalog/6453
11    GDELT    2    SI    https://www.gdeltproject.org/data.html
12    INTERACTING_AS_EQUALS_..._IN_MEXICO    2    SI    https://www.nature.com/articles/s41562-024-02043-y
14    MASS_MOBILIZATION_PROTEST_DATA    2    SI    https://massmobilization.github.io/
16    UCDP    2    SI    https://ucdp.uu.se/downloads/
17    ENCOAP    2    NO    https://www.inegi.org.mx/programas/encoap/2023/default.html
23    LARGE_SCALE_FINANCIAL_EDUCATION_..._2011_2    1    SI    https://microdata.worldbank.org/catalog/2049
25    MICROCREDIT_IMPACTS_RANDOMIZED_..._EXP    1    SI    https://www.openicpsr.org/openicpsr/project/116334/version/V1/view
28    CNGMD    1    NO    https://www.inegi.org.mx/rnm/index.php/catalog/977
30    DOES_CORRUPTION_INFORMATION_...    1    NO    https://www.povertyactionlab.org/evaluation/information-dissemination-campaign-and-voters-behavior-2009-municipal-elections-mexico
31    ELECTORAL_PRECINCT_LEVEL_DATABASE_...    1    NO    https://www.nature.com/articles/s41597-025-04999-0
33    ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION    1    NO    https://www.banxico.org.mx/publicaciones-y-prensa/encuesta-de-competencias-financieras-de-la-poblaci/microdatos/competencias-financieras-mi.html
35    IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM    1    NO    https://microdata.worldbank.org/catalog/1039/study-description
36    OECD    1    NO    https://www.oecd.org/en/data/datasets/oecd-trust-survey-data.html
38    PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND    1    NO    https://cenfri.org/research-paper/price-and-information-type-in-life-microinsurance-demand-experimental-evidence-from-mexico/

El criterio de clase A.4, por fuente, escrito ANTES de sondear. Este acto no descarga, así que su vocabulario es más estrecho que el de P·Lote-k y hay que decirlo:

EXISTE-SATISFACE — la puerta responde, y la portada declara microdato de México accesible con registro gratuito o menos. (No afirma que el payload se bajó: eso es de P·Lote-k.)
EXISTE-NO-SATISFACE — responde, y falta algo específico: no hay México, no hay microdato, la cobertura temporal no sirve. Se dice qué falta.
NO-ACCESIBLE — pago, afiliación institucional o licencia restringida. Registro gratuito o aceptar términos de uso NO cuenta aquí.
NO OBTENIDO POR ESTE AGENTE EN N INTENTOS — la sonda falló. No es NO-ENCONTRADO. Van los N intentos con salida cruda + receta manual ejecutable en navegador en <1 min (A.5).
NO-ENCONTRADO — solo si la puerta responde y el recurso no está ahí, con los términos y el universo en la misma línea.

Prohibido concluir cualquier cosa de un portal desde conocimiento de entrenamiento. El corte es anterior a hoy. Si no se sondeó en esta sesión, no se sabe.

Cierra el commit con: "el primer resultado que produzca este procedimiento es el que se reporta."

Commit 2 — la ejecución

Por fuente, en este orden: sonda con curl (no curl -I) → si falla, repite con cabeceras de navegador real y declara si el 403 cambia (fue lo que distinguió "caja" de "portal" en ISSP) → apertura byte a byte de la portada de lo que responda → clasificación A.4 en la misma línea que su universo + mecanismo + fecha → una fila nueva en universo-puertas-2026-08-12.tsv.

Regla que este acto no puede violar (A.6): una candidata localizada por buscador y no abierta byte a byte se registra SIN-FETCH, jamás se promueve. El barrido de las 17 condiciones reportó WebFetch 403 en el 100% de los intentos contra dominio de control neutral — si tu WebFetch está en ese estado, dilo y usa curl.

Contra-regla, escrita antes de ver el dato (B-bis): este acto puede terminar sin una sola puerta nueva utilizable, y eso sería un resultado, no un fracaso. Si las 15 vuelven NO OBTENIDO POR ESTE AGENTE, el entregable son 15 recetas manuales — y el carril usuario+descargas_mx ya cerró tres veces lo que el agente declaró imposible. La receta no es el consuelo del acto: es su entregable de mayor rendimiento, medido.

Cierre: PRISMA de 7 cifras (intentadas / respondieron / con-México-declarado / con-microdato-declarado / no-accesibles / no-obtenidas / con-receta-manual) + la propuesta de firma del Lote 2 ordenada por lo que el sondeo encontró, no por palanca a ciegas.

Contador que este acto mueve: filas del puntero de puertas con clasificación A.4 derivada de un portal, no de una tabla interna — hoy son 12 de 75 en el crosswalk. Y este acto NO mueve capa2. No lo prometas y no lo intentes.
════════════════════════════════════════════════════════════════════════
