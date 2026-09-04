# Encargo `PACK-UBUNTU-2`

**SHA de redacción:** `dfdf4fd` (`origin/main`, merge de `PR #352`) — declarado por dirección. Al arrancar, `origin/main` ya era `151cf04`: main había avanzado **5 commits** (`ACTO CONGELA-SORTEA` `PR #353` y `ACTO ESCALAS-P2` `PR #354`, los dos actos que el propio encargo declaraba «en vuelo»). El encargo previó el caso —*"si main avanzó: refresca, re-deriva, reporta — no es PARO"*— y así se hizo: el acto corrió sobre `151cf04`.
**Entorno asignado:** **UBUNTU**. Explícitamente **NO** la nube: este pack abre microdato y la nube no tiene los bytes. Firma de entorno de tres partes verificada al arrancar (§ARRANQUE).
**Estado:** **CONSUMIDO** por `ACTO PACK-UBUNTU-2`, 25/ago/2026 — los dos abridores corridos, `ADR-181` y `ADR-182` sellados, ningún veredicto archivado y el contador de Hito D sin mover, como el propio encargo manda. Nota de cierre: `forense/notas/2026-08-25-pack-ubuntu-2-cierre.md`.

## Bloque VERIFICACIÓN DE EXISTENCIA (Parte 2 de A.8)

- **`forense/hitoD-preregistro-v2_0.md`** — EXISTE. Las dos fichas están donde el encargo dice: `R1.4` en `:59` y `R8.3` en `:236`, verificado por `awk` sobre número de línea. Ambas leídas íntegras antes de congelar (`:59-67` y `:236-246`).
- **`data/manifiesto.yaml`** — EXISTE, 792 entradas. Las cifras del encargo se verificaron y **cuadran**: WVS **11** entradas, GESIS/ISSP **16**, ambas con raíz `descargas_mx` y `url_origen` poblado. ENNViH aporta **29** entradas (el encargo no daba cifra). Los 17 payloads usados verificaron **COINCIDE** por `tests/manifiesto.py --verifica --id`, una invocación por id.
- **`data/diseno-muestral.yaml`** — EXISTE; su entrada de ENNViH es la que gobierna el régimen de varianza del acto 2.
- **Ningún abridor previo** — CONFIRMADO: ni `R8.3` ni `R1.4` aparecen en el bloque `## Registro de veredictos archivados`, que trae **19 líneas / 18 fichas distintas** (`R4.3` ocupa dos líneas, mitad A y mitad B). Los «9 restantes» del encargo cuadran contra las 27 del perímetro.
- **Este pack nunca lanzado** — CONFIRMADO: 0 coincidencias en `forense/encargos/` (169 entradas) antes de este archivo.
- **Compuertas** — `conf.06` **CERRADO** (`ADR-64`); `R1.3` **archivado** (5/ago, desenlace `E`); `FP-118` **`ABIERTA`** (contra lo que el encargo suponía posible; ver `ADR-182`).

---

## Texto del encargo, verbatim

PACK UBUNTU-2 — los dos abridores de Hito D con dato ya en corpus: R8.3 (WVS/ISSP) y R1.4 (ENNViH) · re-redactado desde el canon

⚠️ Anti-duplicación: re-redacción canónica de los entregables no archivados de la conversación anterior (PACK-UBUNTU2-R83-R14, A.3). Si conservas el original, lanza UN SOLO juego. SHA de redacción: dfdf4fd+ (si main avanzó: refresca, re-deriva, reporta — no es PARO). Redactado por: dirección, 25/ago/2026. ENTORNO: UBUNTU — este pack SÍ abre microdato; la NUBE no tiene los bytes. NO lanzar en NUBE; no lanzar dos veces. FIRMA: ninguna nueva — los abridores PROPONEN veredicto y no lo archivan («C3 intacta», en palabras del transfer): el contador de Hito D no se toca en este pack; archivarlo será acto posterior con firma/ADR de mesa.

Reglas comunes

Firma de entorno de TRES partes (A.2): CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado sin_variable · sonda curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ (NUNCA curl -I) · ls data/raw/ 2>/dev/null | head -1 → el corpus DEBE estar montado; si no lo está, PARO: la asignación de entorno falló (precedente medido 5/ago). Verificación de payloads una invocación por --id (A.1), tres respuestas sin colapsar (AUSENTE / raíz-no-configurada / hash-discordante). Tuberías con iconv; negativos con conteo de archivos (A.13). Suite --baseline antes/después; 🚫 jamás --freeze. Renumera quien fusiona segundo. Regla de estimación de la casa, obligatoria en ambos actos: DOS COMMITS — el primero congela la especificación (variables, universo, ponderadores, ejes, dicotomizaciones) ANTES de abrir ningún dato y cierra con «el primer resultado que produzca este procedimiento es el que se reporta»; el segundo trae resultados y no edita el primero; si la spec estaba mal, un tercer commit lo dice — nunca se corrige hacia atrás. A-bis completo aplica: un β̂ marginal es asociación, no coeficiente identificado (regla 1); condicionar no lo vuelve correcto (regla 2); toda cantidad con su escala declarada y sin comparar entre escalas (regla 3); estimando de subpoblación no se compara contra poblacional (regla 4); punto que cumple umbral con IC que no lo despeja NO adjudica — se propone con la reserva escrita.

════════ ARRANQUE ════════ 1 · REPO: clon existente; ruta · git log -1 · git status. 2 · SHA: compara con el declarado; reporta. 3 · data/raw: aquí SÍ es sustantiva — se crea/enlaza al CORPUS COMPARTIDO; reporta cuál. ⚠️ Si este pack registrara algo nuevo (no debería): verifica al cerrar que quedó en el corpus compartido (defecto PR #77). 4 · ENTORNO: las TRES partes de arriba, valores crudos. 5 · ESPEJO: cero cifras del espejo. ══════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (25/ago, contra dfdf4fd) ═══ Estructura. Gobernantes: forense/hitoD-preregistro-v2_0.md (fichas R1.4 en :59 «Movilidad bloqueada → consumo compensatorio [FUERTE como correlación]» y R8.3 en :236 «Puente personal → confía en el desconocido [FUERTE]») · data/manifiesto.yaml (payloads) · data/diseno-muestral.yaml · tablero/gobernanza/estado. Este pack escribe: fichas B-bis/notas de propuesta en forense/ · gobernanza · estado · tablero (solo si alguna fila ya existente recibe ejecutada_en) · notas -cierre · pack archivado. NO escribe: el Registro de veredictos archivados del preregistro, README.md, modelo-decision (eso es del acto que archive), milpa/ valores. Contenido (crudo). Dato en corpus, del manifiesto: WVS 11 entradas y GESIS/ISSP 16 entradas registradas desde el 12/ago (raíz descargas_mx, url_origen poblado — cifra citada de instrucciones-proyecto-v2_11.md, A.8, que la derivó del manifiesto) y ENNViH con payloads ennvih* (p.ej. ennvih1_2002_hogar_dta, ehh02dta_all.zip) más la licencia de dominio público declarada en el propio manifiesto. Ningún abridor previo: los veredictos de R8.3/R1.4 no existen en el Registro (por eso son "9 restantes"). Este pack: 0 de 167 en forense/encargos/ — nunca lanzado. F0 re-corre todo; si un abridor ya corrió → salta y declara (A.8). Cobertura. Gobernantes ≤25/ago; trabajo posterior — sin brecha. ═════════════════════════════════════════════

PERÍMETRO Y CONCURRENCIA

Lista cerrada: forense/ (ficha-abridor + nota por acto) · gobernanza · estado · tablero (solo ejecutada_en de filas existentes si aplica) · /home de trabajo y data/raw en LECTURA. "Si escribes fuera de esta lista, PARA." Concurrencia: NUBE-2, CONGELA-SORTEA y ESCALAS-P2 pueden estar en vuelo — colisión solo en gobernanza/estado/tablero (renumeración normal). Dependencia declarada con NUBE-2 acto 1: si FP-118 aún está ABIERTA cuando corra el ACTO 2 de este pack, R1.4 solo puede producir estimación puntual ponderada (la fila lo permite verbatim); con la firma de FP-118 propagada, puede además reportar EE bajo supuesto MAS con la subestimación escrita. El ejecutor verifica el estado de FP-118 en F0 del ACTO 2 y elige la rama en consecuencia — las dos están pre-autorizadas aquí.

ACTO 1 · Abridor de R8.3 — puente personal → confianza en el desconocido, sobre WVS/ISSP

F0: lee ÍNTEGRA la ficha R8.3 del preregistro (:236) — su cláusula, tier, y lo que su escala de falsación exige (B-bis: declara qué significa que el falsador NO refute, y la precedencia entre filas, ANTES de correr). Resuelve los payloads por manifiesto (grep -n "wvs\|issp" + verificación A.1 por --id). COMMIT 1 (spec congelada): instrumento(s) y ola(s) elegidos con razón escrita · variable de "puente personal" y de "confianza en el desconocido" con su pregunta verbatim y escala declarada · universo México · ponderador · ejes de estratificación disponibles · dicotomizaciones · qué patrón CONFIRMA / ACOTA / ROMPE la regla, por adelantado. COMMIT 2 (resultados): estimaciones con escala y universo declarados; marginal rotulado ASOCIACIÓN; estratificado reportado sin promoverlo a "el verdadero" (A-bis 2); PROPUESTA de veredicto en la ficha-abridor (forense/hitoD-R8_3-abridor-v1_0.md) — el Registro del preregistro NO se toca.

ACTO 2 · Abridor de R1.4 — movilidad bloqueada → consumo compensatorio, sobre ENNViH

Misma estructura exacta que el ACTO 1, sobre el panel ENNViH (olas en corpus; etiquetas/labels de variables leídas del propio microdato — cita libro/columna). La ficha dice [FUERTE como correlación]: el abridor propone en ese registro — correlación con diseño intra-hogar/olas si el panel lo permite, jamás promovida a causal sin identificación (A-bis 1/2). Varianza: rama según FP-118 (ver dependencia arriba), con la reserva MAS escrita si aplica. PROPUESTA de veredicto en forense/hitoD-R1_4-abridor-v1_0.md; Registro intacto.

Cierre del pack

ADR por acto (qué se propuso, con qué spec congelada, qué NO se archivó y por qué — el contador espera firma de mesa); estado (línea de Hito D: "2 propuestas de abridor en mesa, contador sin mover"); notas -cierre; pack archivado CONSUMIDO; suite VERDE con tail pegado. CONTADOR: cero, declarado — y es correcto que sea cero: este pack fabrica las dos propuestas que la siguiente firma de mesa convierte en Hito D 19→21 (o 20→21 si R10.1 ya archivó).

Lo que este pack NO hace

No archiva veredictos ni mueve Hito D. No toca CAL-G3, el duelo, el sorteo, el pool de 253, tools/ ni milpa/. No descarga nada nuevo. No adjudica causalidad. No colapsa "no pude abrir el payload" con "el dato no está" (A.1/v2.2: tres hallazgos distintos, tres palabras distintas).

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-25-PACK-UBUNTU-2-abridores.md" canon/gobernanza-v1_15.md` → 2: citado bajo ADR-181, ADR-182 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
