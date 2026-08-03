# CAL-CONF Fase B — posición 4 rehecha, paso 1: localizar el reactivo real de `exposicion_violencia`

*4 de agosto de 2026.*

**Resultado de este acto, dicho antes que nada: BLOQUEADO por alcanzabilidad de
red, no por el corpus.** Este acto no produce tabla de candidatos ni rama de
conclusión (§2.4 del encargo) porque el paso previo obligatorio —leer el
descriptor de `TPer_Vic1`— no se pudo ejecutar en este entorno. Se reporta el
bloqueo con el vocabulario exigido y se para, tal como pide el encargo §1-bis.

---

## 0 · Verificación de procedencia antes de obedecer

Tipo (1), verificado contra `main` en `6a09a37` (`git fetch origin`, ya al
día — no hizo falta `pull`) antes de escribir esta nota:

- `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md` §0.2 y §4.0 —
  leídos completos. Confirman, con cita literal del propio FD, por qué
  `BP1_20`/`BP1_23`/`BP1_28` no sirven: viven en `TMod_Vic` (subpoblación de
  víctimas, 40 280 filas, `RESUL_H='A'` al 100%), no en `TPer_Vic1`
  (población elegida completa, 91 182 filas) — la exposición vive un paso
  antes, en `P(víctima | x)`, que `TMod_Vic` no puede poblar porque su
  denominador ya excluyó a quien no fue víctima.
- `forense/hitoE-campana-medicion-v2_0.md` §15 (líneas 1203-1268) — leído
  completo. Confirma la fila 4 de `§14.3`: **PENDIENTE DE VERIFICACIÓN**,
  reactivo anterior retirado, contador sin cambio de destino (7/14), ninguna
  fuente/variable lo sustituye todavía.
- `canon/modelo-decision-v4_0.md:372` — verificado, cita exacta: fila `G4`
  de la tabla de generadores/cláusulas falsables, *"Exposición a violencia +
  impunidad → Conducta defensiva, retracción del espacio público"*, **SIN
  FALSAR**.
- `milpa/procedencia.yaml:441` — **la cita del encargo no se sostiene en
  esa línea.** La línea 441 de `milpa/procedencia.yaml` en `6a09a37` es la
  nota de `tramite.gobierno_digital.coercitivo` ("Es la regla del gate de
  Fase 1..."), no la escala 0.35-0.70 de `exposicion_violencia`. Esa escala
  sí existe, verificada, pero en **`milpa/procedencia.yaml:498`**
  (`riesgos_cruzados` → `"exposicion_violencia base en los 6 perfiles (0.35
  a 0.70)"`, `refutacion_en_riesgo: ref.B.05.violencia_no_es_cultura`). Se
  documenta el desfase de línea (probable corrimiento por ediciones
  posteriores del archivo) en vez de citar de memoria — mismo principio que
  §0.1 de la nota de `PR #57` aplicó a la cola de `hitoE`.
- Payloads registrados en `data/manifiesto.yaml`: `envipe2025_fd_pdf`
  (línea 1750, `fd_envipe2025.pdf`) y `cuest_principal_envipe2025.pdf`
  (línea 1764) — confirmados en el manifiesto. **Ninguno de los dos está en
  disco en este entorno** (`data/raw/` vacío, en `.gitignore`; `find /
  -iname "*envipe2025*"` sin resultados fuera de `.git`).

## 1 · El criterio, escrito antes de abrir nada (§2.1 del encargo)

**Constructo buscado:** proporción de personas que estuvieron expuestas a
violencia/victimización en el periodo, condicionada a atributos.

Esta frase es la que se usará para juzgar cada candidato en `TPer_Vic1`
cuando el paso 2 pueda ejecutarse. Distinción declarada por adelantado, tal
como pide el encargo §2.3: **haber sido víctima (exposición directa)** no es
lo mismo que **percibir el entorno como inseguro** (que es más cercano a lo
que `G4` *produce* —retracción del espacio público, conducta defensiva—
que a lo que `G4` *consume* como antecedente). Un candidato de percepción
que se proponga en el paso 2 tendrá que declarar explícitamente por qué no
es el desenlace de `G4` disfrazado de su causa.

## 2 · Por qué no se enumeran candidatos — sonda de alcanzabilidad, §1-bis

Este entorno es nube (sin `data/raw/`, sin clon de los PDF). Antes de
cualquier otra cosa, sonda de alcanzabilidad — exactamente el comando que
pide el encargo, no `curl -I`:

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000   (exit 56 — "failure receiving network data")
```

Verificado con `-v` para no confundir un `000` de fallo de DNS/TLS con un
bloqueo de política: el `CONNECT` hacia `www.inegi.org.mx:443` sí llegó al
proxy del entorno (`127.0.0.1:46471`) y el **proxy respondió `403 Forbidden`
al `CONNECT` mismo**, antes de que la petición HTTP saliera hacia INEGI.
Confirmado además contra `$HTTPS_PROXY/__agentproxy/status`, que registra el
mismo evento en `recentRelayFailures`:

```
{"kind": "connect_rejected", "detail": "gateway answered 403 to CONNECT
(policy denial or upstream failure)", "host": "www.inegi.org.mx:443"}
```

**NO ALCANZABLE DESDE ESTE ENTORNO.** No es un `RESPONDE PERO SIN EL
RECURSO` (eso sería un 404/403 de `inegi.org.mx` mismo, después de que el
`CONNECT` se completara) ni un `RESPONDE` — el gateway del entorno corta la
conexión antes de que salga cualquier petición HTTP. Por política del
entorno (`recentRelayFailures` lo etiqueta `policy denial`), no por falla
transitoria: no se reintenta en bucle.

**Por lo tanto, y siguiendo la instrucción literal del encargo §1-bis ("Si
no, repórtalo con esas palabras y para"): este acto para aquí.** No hay
descarga ciega posible sin alcanzabilidad — el ADR-46(2) autoriza bajar por
URL conocida del manifiesto cuando el sitio responde; aquí no responde. No
se abre microdato (tampoco estaría disponible: mismo `.gitignore`). No se
enumeran candidatos de `TPer_Vic1` por parecido de nombre ni de memoria —
sería exactamente el error que esta misma posición 4 ya cometió una vez
(`PR #57` §4.0: un rótulo de P2 sin verificar contra el cuestionario bajó
intacto hasta la cola y costó un PR entero corregirlo). Sin el FD/cuestionario
abierto en este acto, no hay base verificada para declarar SIRVE/NO
SIRVE/AMBIGUO sobre ningún código de columna — hacerlo sin el descriptor
sería repetir el patrón de "reportado, no verificado" que `§15` de `hitoE`
ya identificó como el origen del defecto.

## 3 · Qué NO se hizo, declarado explícito

- No se abrió microdato (tampoco estaba disponible en este entorno).
- No se propuso clase nueva ni se cerró la fila 4 de `hitoE` — sigue
  **PENDIENTE DE VERIFICACIÓN**, sin tocar `§14.3` ni `§15`.
- No se tocó `data/manifiesto.yaml`.
- No se editó `forense/hallazgos.md` más allá de una línea de append (abajo),
  sincronizado con `main` antes de este PR.
- No se recuperó el descriptor por otra vía (motor de búsqueda, caché, otro
  host) — el encargo especifica el mecanismo (`curl` directo contra
  `inegi.org.mx`, descarga ciega por manifiesto) y ese mecanismo está
  bloqueado por política del entorno, no por ausencia del recurso en
  origen.

## 4 · Declaración de contaminación (ADR-46(4), conservador)

**Este acto no leyó ningún instrumento de ENVIPE** (ni FD, ni cuestionario,
ni microdato) — solo notas forenses ya escritas por sesiones anteriores
(tipo (1), citadas en §0) y el propio repositorio de canon/milpa. Por lo
tanto, **este acto no queda inhabilitado para pre-registrar contra ENVIPE**:
la regla general se declara igual — *"leer el instrumento de ENVIPE te
inhabilita para pre-registrar contra ENVIPE"*— y no aplica aquí porque el
instrumento no se leyó, no porque la regla se relaje.

## 5 · El contador y la fila 4 — sin cambio

**Condicionales medidas sobre atributos: sigue en 8 de 14** (sin cambio —
este acto no midió nada; ni falla C1 el reactivo anterior otra vez ni
localiza uno nuevo). La fila 4 de `hitoE §14.3`/`§15` sigue
**PENDIENTE DE VERIFICACIÓN**, sin fuente/variable — este acto no la
resuelve ni la cierra, exactamente lo que pedía el encargo si el paso 1 no
se puede completar: nombra el bloqueo, no fabrica un resultado.

**Qué le falta a la próxima sesión para completar el paso 1:** el mismo
paso 2 de este mismo encargo, ejecutado en un entorno donde
`https://www.inegi.org.mx/` sea alcanzable (Ubuntu con `data/raw/`
poblado, o una nube sin este bloqueo de política) — enumerar las columnas
de `TPer_Vic1` contra el criterio de §1 usando `fd_envipe2025.pdf` /
`cuest_principal_envipe2025.pdf`, ya registrados y con hash en
`data/manifiesto.yaml`, sin necesidad de volver a bajarlos si ya están en
disco de esa sesión.

---

## 6 · Límite de lectura declarado

Esta sesión leyó completos: `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md`
(§0.2, §4.0-§4.2, §5-6), `forense/hitoE-campana-medicion-v2_0.md` §15 (y
§14.3 para la fila citada), `canon/modelo-decision-v4_0.md:360-380` (tabla
de generadores), `milpa/procedencia.yaml:418-450` y `:490-505`
(coeficientes de `G4` y `riesgos_cruzados`), `data/manifiesto.yaml`
(entradas `envipe2025_fd_pdf`, `cuest_principal_envipe2025.pdf`, sin
editar), `forense/notas/2026-07-31-inventario-segmentacion.md` (búsqueda de
candidatos ya documentados de percepción/victimización — sin hallazgo de
columna verificada más allá de lo ya citado), `data/inventarios/inventario_fuentes_seguridad_justicia_mexico.md`
(nivel de encuesta, no de columna). No se abrió microdato. No se leyó FD ni
cuestionario (bloqueados por red, §2). Se corrió `python3 tests/check.py`
— 19 FAIL · 84 WARN, igual a `tests/baseline.json` (`19 FAIL`), sin cambio
atribuible a este acto (nota de solo lectura, sin tocar corpus/canon/milpa).
No se tocó `data/manifiesto.yaml` ni `canon/` ni `milpa/`.
