# ENCARGO · ACTO RECENSO-DISEÑO-14 — ejecuta lo que FP-84 selló; cierra FP-95

- **SHA de redacción:** `fb02421` (clon propio de dirección, `origin/main` al redactar). **Base efectiva del acto:** `22d792f` — `main` avanzó 3 commits entre redacción y arranque; se refrescó y re-derivó conforme al propio bloque ARRANQUE punto 2.
- **Entorno asignado:** **UBUNTU** (corpus montado). **NO NUBE.**
- **Estado:** `CONSUMIDO` — ejecutado el 24/ago/2026, `ADR-148`, nota `forense/notas/2026-08-24-recenso-diseno.md`.

---

## Texto completo tal como se lanzó

Redactado por    dirección, 24/ago/2026, contra clon propio origin/main = fb02421
Firma que ejecuta    Ya dada: ADR-135 (mesa, 20/ago) «ordena re-censo acotado a las 14 fuentes que cambiaron de estado»; FP-95 registra que falta ejecutarlo. Este acto no decide nada — ejecuta.
⛔ ORDEN    Lanzar tras fusionar REPARA-PROPAGA-15. Puede correr en paralelo con TRIAGE-UNIVERSO-12 (NUBE) — colisión solo en gobernanza/tablero: renumera quien fusiona segundo.
ENTORNO ASIGNADO    UBUNTU (corpus montado — los descriptores/DDI viven con los payloads). NO NUBE: sin corpus, este acto muere como E-ENCIG/S-IDG3 el 5/ago (A.2).
Modelo    Opus
Reglas fijas    🚫 --freeze · pgrep -af claude · iconv -f utf-8 -t utf-8 -c en TODA tubería (el grep de esta caja tira no-UTF8 en silencio — A.13)
CONTADOR DECLARADO    Ninguno de medición — desbloquea: al cerrar, diseno-muestral.yaml deja de gatear toda estimación con ponderadores (coeficientes, condicionales, celdas del duelo). Declarado a propósito (v2.3).

Encontrar que el terreno no es el que este encargo supone es entregable, no interrupción.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════ 1 · REPO. Clon existente; ruta · git log -1 --format="%h %s" · git status. No arranques desde el home. 2 · SHA. Base con REPARA-PROPAGA-15 fusionado (suite VERDE al abrir). Si main se movió más allá: refresca, re-deriva, reporta. 3 · data/raw. AUSENTE NO ES PARO — enlázala al corpus compartido de la caja (/home/pc0/mm-corpus/raw) o créala. Reporta: existe / la enlacé a <ruta> / la creé. Este acto NO descarga: solo lee descriptores ya adquiridos. 4 · ENTORNO — firma de TRES partes (A.2): CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ (NUNCA curl -I) → reporta el código crudo ls data/raw/ 2>/dev/null | head -1 → el corpus DEBE estar montado; vacío = PARO. ⚠️ [v2.11] Un negativo de un comando que no examinó archivos no es un negativo (A.13): todo veredicto negativo —incluida la sonda— declara cuántos archivos examinó el comando que lo produjo. 5 · ESPEJO. Ninguna cifra del espejo; todo del clon y del corpus, comando a la vista. ════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (24/ago) ═══ 1 · ESTRUCTURA. Gobiernan: data/diseno-muestral.yaml (existe, verificado ls data/) · data/censo-explotacion-2026-08-17.tsv (627 filas, cifra de la propia FP-95) · data/manifiesto.yaml (rutas de payload). Este acto escribe SOLO en el primero; los otros dos se leen. 2 · CONTENIDO. Las filas objetivo: las marcadas PENDIENTE en diseno-muestral.yaml que ya tienen payload material hoy (definición textual de FP-95). Dirección NO derivó la lista de 14 — derívala tú con grep sobre el yaml cruzado contra manifiesto, pega comando y salida, y si no son exactamente 14 repórtalo ANTES de censar (la cifra viene de FP-95/ADR-135; si el universo se movió desde el 20/ago, la lista manda sobre la cifra, con la discrepancia declarada). 3 · COBERTURA RETROACTIVA. diseno-muestral.yaml es anterior a la ola de adquisición de agosto: fuentes adquiridas después pueden no tener fila — si encuentras payload material sin fila, la fila faltante es hallazgo (repórtala, no la inventes fuera del alcance de FP-95). ════════════════════════════════════════════════════════════════════

Método, por fuente (las ~14)
Localiza el descriptor del payload en el corpus (DDI, «descriptor de archivos», documento metodológico, FD) — ruta real bajo data/raw/, no la de memoria.
Extrae con archivo:página/línea del documento fuente: variable de ponderador (nombre exacto, p. ej. FAC_HOG/FACTOR), estrato, UPM/conglomerado, y réplicas/varianza si el diseño las trae (BRR/jackknife) — más el universo del ponderador (hogar/persona/vivienda) cuando el descriptor lo diga.
Escribe la fila en diseno-muestral.yaml con la cita al descriptor. Nada se infiere de encuestas «parecidas»: si el descriptor no trae diseño → EXISTE-NO-SATISFACE con qué falta y dónde buscaste (conteo de archivos, A.13); si el payload no trae descriptor → dilo y propone de dónde bajarlo (receta manual A.5), sin bajarlo aquí.
Verificación cruda mínima por fuente (no estimación): abre el microdato lo justo para confirmar que la variable de ponderador nombrada existe en el archivo y no es toda-vacía (head/lector de columnas). Es confirmación de existencia, no cálculo — ningún número entra al canon.

Cierre: FP-95 → FIRMADA (ejecutada_en hoy, citando ADR-135 como firma de origen) · nota en forense/notas/2026-08-24-recenso-diseno.md con la tabla resumen (fuente · ponderador · estrato · UPM · réplicas · estado A.4) · ADR (candidatea contra el máximo re-derivado; renumera si colisiona) · párrafo a mesa: cuántas de las ~14 quedaron EXISTE-SATISFACE y cuáles siguen cojas, porque la corrida #1 de mañana (CAL-G3 sobre ENNViH) se diseña sobre esta tabla.

PERÍMETRO Y CONCURRENCIA

Archivos: data/diseno-muestral.yaml (solo filas PENDIENTE objetivo) · forense/notas/2026-08-24-recenso-diseno.md (nueva) · forense/firmas-pendientes.tsv (FP-95 + hallazgos A.12) · canon/gobernanza-v1_15.md (ADR) · forense/encargos/2026-08-24-RECENSO-DISENO-14.md (este, CONSUMIDO al cerrar).

Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

Concurrencia: TRIAGE-UNIVERSO-12 corre en NUBE en paralelo (disjunto salvo gobernanza/tablero — renumera quien fusiona segundo). Nadie más toca diseno-muestral.yaml hoy.

---

## Cierre

- **Universo derivado:** 18, no 14. La discrepancia se reportó antes de censar y se resolvió por la regla del propio encargo (la lista manda sobre la cifra). Ver `ADR-148(a)`.
- **Resultado:** 11 `EXISTE-SATISFACE`, 7 `EXISTE-NO-SATISFACE`, 0 `NO-ENCONTRADO`.
- **`FP-95`** → `FIRMADA`. Abiertas `FP-114` a `FP-118`.
- **Perímetro:** respetado. `PARA` en `canon/estado-programa-v1_10.md:27,103` (contador de ADR), fuera de la lista — pendiente de adenda de dirección, ver `ADR-148(f)`.
