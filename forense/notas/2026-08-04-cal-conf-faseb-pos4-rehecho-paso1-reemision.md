# CAL-CONF Fase B — posición 4 rehecha, paso 1 (reemisión): localizar el reactivo real de `exposicion_violencia`

*4 de agosto de 2026.*

**Resultado de este acto, dicho antes que nada: BLOQUEADO por alcanzabilidad
de red — la misma clase de bloqueo que `PR #61`, no resuelto por la
reemisión.** La reemisión (§3-bis del encargo) afirma que este acto "va
ahora a Ubuntu, donde los PDF están en disco: §1-bis no aplica, no hay
sonda que correr". **Esa premisa no se sostiene en este entorno,
verificado antes de obedecerla** (§1 del encargo lo exige): este acto
corre en un entorno de nube (`cloud_default`), sin `data/raw/` poblado y
con el mismo bloqueo de política de red que documentó `PR #61`. No se
enumeran candidatos de `TPer_Vic1` — el paso previo obligatorio, leer
`fd_envipe2025.pdf`, no se pudo ejecutar.

---

## 0 · Verificación de procedencia y de premisas antes de obedecer

Tipo (1), verificado contra `main` en `0b61c52` (`git fetch origin main`,
ya al día).

- `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md` §0.2 y §4.0 —
  leídos completos (heredado de la verificación de `PR #57`/`PR #61`,
  re-confirmado contra este checkout). Confirman por qué
  `BP1_20`/`BP1_23`/`BP1_28` no sirven: viven en `TMod_Vic` (subpoblación
  de víctimas, `RESUL_H='A'` al 100% de 40 280 filas), no en `TPer_Vic1`
  (población elegida completa, 91 182 filas) — la exposición vive un paso
  antes, en `P(víctima | x)`.
- `forense/hitoE-campana-medicion-v2_0.md` §15 (líneas 1203-1268) — leído
  completo. Fila 4 de `§14.3`: **PENDIENTE DE VERIFICACIÓN**, reactivo
  anterior retirado, contador sin cambio de destino (7/14 en la tabla
  original; **8/14** es la cifra vigente hoy en `canon/modelo-decision-v4_0.md:277,621`
  tras las posiciones 5-6 medidas tres actos después — verificado, no de
  memoria).
- `canon/modelo-decision-v4_0.md:374` (**no `:372`** — desfase de 2 líneas
  frente a la cita del encargo, documentado en vez de citado de memoria,
  mismo principio que aplicó `PR #61`): fila `G4`, *"Exposición a
  violencia + impunidad → Conducta defensiva, retracción del espacio
  público"*, **SIN FALSAR**. Contenido exacto, solo la línea corrió.
- `milpa/procedencia.yaml:441` — **sigue sin sostenerse en esa línea**,
  igual que encontró `PR #61`: la línea 441 vigente es la nota de
  `tramite.gobierno_digital.coercitivo`. La escala 0.35–0.70 de
  `exposicion_violencia` vive en **`milpa/procedencia.yaml:498`**
  (`riesgos_cruzados`), sin cambio de línea frente a lo que ya documentó
  `PR #61` — el desfase no se corrigió porque no era el objeto de ningún
  acto entre medias.
- Payloads `envipe2025_fd_pdf` (`data/manifiesto.yaml:1750-1762`) y
  `cuest_principal_envipe2025.pdf` (`:1763-1775`) — confirmados
  registrados, con `url_origen` verificable. **Ninguno de los dos está en
  disco en este entorno**: `data/raw/` no existe (`ls data/raw` → "No such
  file or directory"; el propio `.gitignore` lo declara ignorado, y no hay
  clon previo de otra sesión en este worktree).

### 0.1 · Las dos actualizaciones que pide §3-bis, verificadas

1. **Clase sellada `ADR-52 A`, verificada contra `canon/gobernanza-v1_15.md:527`.**
   `exposicion_violencia` está en **"sin reactivo verificado — búsqueda
   abierta"**, con condición de caducidad de tres actos nombrados. El
   texto exacto del ADR nombra **dos actos ya en curso**: *"posición 4
   rehecha sobre `TPer_Vic1`, barrido de alcanzabilidad ENDIREH/ENSU"* —
   es decir, **este mismo encargo** (el intento anterior, `PR #61`, y esta
   reemisión son la misma posición, no dos actos distintos) ya es uno de
   los dos que el ADR cuenta como en curso. Este acto, al volver
   bloqueado otra vez, **no agrega un acto nuevo a la cuenta** — sigue
   siendo el mismo acto "en curso" que el ADR ya nombró, todavía sin
   cerrar. La lectura literal del encargo (*"este acto cuenta como uno de
   esos tres si vuelve sin reactivo"*) presupone que "volver sin
   reactivo" significa *buscar contra el instrumento y no encontrar un
   candidato que sirva* — no *no poder abrir el instrumento*. Este acto no
   hizo lo primero: no llegó a abrir el descriptor. Declarado así, sin
   decidir por cuenta propia si un bloqueo de red cuenta como "vuelve sin
   reactivo" para la caducidad — es lectura de ADR, no ejecución de ADR,
   y queda para la mesa si hace falta precisarlo.
2. **Acto paralelo de ENDIREH, verificado — no es este acto y ya produjo
   resultado, no duplicado.** `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md`
   §2 y su tabla de cierre (línea con `| 1 | ENDIREH 2021 | **RESPONDE**
   ... | \`exposicion_violencia\`, candidata \`familismo_apoyo\`/\`familismo_obligacion\`
   — **parcial declarado, universo mujeres 15+** |`) confirma que esa
   sesión sí corrió en un entorno donde INEGI **RESPONDE** (se declara
   `Sesión Sonnet, Ubuntu`, línea 3 de esa nota — entorno real, no de
   nombre) y ya señaló un candidato **parcial** (universo mujeres 15+) sin
   adjudicarlo. Por la propia regla del encargo (§3-bis): *"si las dos
   vuelven con reactivo, la de universo completo manda y la otra queda
   como parcial"* — hoy solo ENDIREH tiene avance, y queda como parcial
   hasta que ENVIPE (universo completo) se resuelva o se cierre.

### 0.2 · La sonda de alcanzabilidad, corrida pese a que la reemisión dice que no aplica

**Se corre igual, porque la premisa de §3-bis no se sostuvo en §0.** Mismo
comando exacto que exige el encargo, no `curl -I`:

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000
```

Verificado con `-v` para no confundir un `000` de fallo de DNS/TLS con un
bloqueo de política — mismo patrón que documentó `PR #61`, reproducido
aquí de cero, no copiado de esa nota:

```
* CONNECT tunnel: HTTP/1.1 negotiated
* Establish HTTP proxy tunnel to www.inegi.org.mx:443
> CONNECT www.inegi.org.mx:443 HTTP/1.1
< HTTP/1.1 403 Forbidden
* CONNECT tunnel failed, response 403
```

Confirmado contra `$HTTPS_PROXY/__agentproxy/status` → `recentRelayFailures`:
`{"kind": "connect_rejected", "detail": "gateway answered 403 to CONNECT
(policy denial or upstream failure)", "host": "www.inegi.org.mx:443"}`.

**Diagnóstico del entorno, verificado (no supuesto por el rótulo del
encargo):**

```
$ cat /etc/os-release | head -1
PRETTY_NAME="Ubuntu 24.04.4 LTS"
$ echo $CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE
cloud_default
$ ls data/raw
ls: cannot access 'data/raw': No such file or directory
```

El sistema operativo se llama "Ubuntu" (24.04 LTS) pero eso **no** es lo
que el vocabulario del encargo distingue en §1-bis/§3-bis — `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md`
(§0.1.2 arriba) ya estableció que la sesión que sí obtuvo `RESPONDE`
declaraba explícitamente un entorno distinto (`Sesión Sonnet, Ubuntu`,
worktree, sin la variable `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`
que sí tiene este). Este acto corre en el mismo tipo de sandbox de nube
que bloqueó `PR #61` — con la misma firma exacta de bloqueo (`403` al
`CONNECT`, `policy denial`) — no en el entorno que la reemisión asumía.

**NO ALCANZABLE DESDE ESTE ENTORNO.** No es `RESPONDE PERO SIN EL
RECURSO` (eso exigiría que el `CONNECT` se completara y el 403/404 viniera
de `inegi.org.mx` mismo) ni `RESPONDE`. Por política del entorno, no por
falla transitoria: no se reintenta en bucle.

**Este acto para aquí, siguiendo la instrucción literal de §1-bis del
encargo original ("si no, repórtalo con esas palabras y para"), aplicada
pese a que §3-bis decía que no haría falta.** No hay descarga ciega
posible sin alcanzabilidad (ADR-46(2) exige que el sitio responda). No se
abre microdato (tampoco disponible: mismo `.gitignore`, mismo `data/raw/`
ausente). No se enumeran candidatos de `TPer_Vic1` por parecido de nombre
ni de memoria.

## 1 · El criterio, escrito antes de intentar abrir nada (§2.1 del encargo)

**Constructo buscado:** proporción de personas que estuvieron expuestas a
violencia/victimización en el periodo, condicionada a atributos.

Distinción declarada por adelantado, igual que exigió el encargo original:
**haber sido víctima (exposición directa)** no es lo mismo que **percibir
el entorno como inseguro** (más cercano a lo que `G4` *produce* que a lo
que *consume* como antecedente). Cualquier candidato de percepción que se
proponga en el paso 2 tendrá que declarar explícitamente por qué no es el
desenlace de `G4` disfrazado de su causa. Esta frase queda congelada para
la sesión que sí pueda abrir `fd_envipe2025.pdf`.

## 2 · Qué NO se hizo, declarado explícito

- No se abrió microdato (no disponible en este entorno).
- No se abrió `fd_envipe2025.pdf` ni `cuest_principal_envipe2025.pdf`
  (bloqueados por red — §0.2).
- No se propuso clase nueva ni se cerró la fila 4 de `hitoE` — sigue
  **PENDIENTE DE VERIFICACIÓN**, `§14.3`/`§15` sin tocar.
- No se tocó `data/manifiesto.yaml`, `canon/`, ni `milpa/`.
- No se decidió si este bloqueo cuenta como "vuelve sin reactivo" para la
  caducidad de `ADR-52 A` — señalado en §0.1, no adjudicado (sería acto de
  mesa, fuera de perímetro).
- No se recuperó el descriptor por otra vía (motor de búsqueda, caché,
  otro host) — el mecanismo que autoriza el encargo (`curl` directo,
  descarga ciega por manifiesto) está bloqueado por política del entorno,
  no por ausencia del recurso en origen (`forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md`
  ya demostró que el recurso responde desde otro tipo de entorno).

## 3 · Declaración de contaminación (ADR-46(4), conservador)

**Este acto no leyó ningún instrumento de ENVIPE** (ni FD, ni cuestionario,
ni microdato) — solo notas forenses ya escritas por sesiones anteriores
(tipo (1)) y el propio repositorio de canon/milpa/gobernanza. Por lo
tanto, **este acto no queda inhabilitado para pre-registrar contra
ENVIPE**: la regla general se declara igual — *"leer el instrumento de
ENVIPE te inhabilita para pre-registrar contra ENVIPE"* — y no aplica aquí
porque el instrumento no se leyó, no porque la regla se relaje.

## 4 · El contador y la fila 4 — sin cambio

**Condicionales medidas sobre atributos: sigue en 8 de 14.** Este acto no
midió nada. La fila 4 de `hitoE §14.3`/`§15` sigue **PENDIENTE DE
VERIFICACIÓN**, sin fuente/variable. La clase `ADR-52 A` de `exposicion_violencia`
("sin reactivo verificado — búsqueda abierta") tampoco se mueve: sigue
abierta, con el mismo acto "posición 4 rehecha" que ya contaba, todavía
sin cerrar.

**Qué le falta a la próxima sesión para completar el paso 1:** el mismo
paso 2 de este mismo encargo, ejecutado en un entorno donde
`https://www.inegi.org.mx/` responda de verdad (verificado con la misma
sonda antes de asumirlo por el nombre del entorno) — enumerar las columnas
de `TPer_Vic1` contra el criterio de §1 usando `fd_envipe2025.pdf` /
`cuest_principal_envipe2025.pdf`, ya registrados con hash en
`data/manifiesto.yaml`. Alternativa declarada, no ejecutada aquí: si la
sesión de ENDIREH (§0.1.2) completa su candidato parcial antes de que
ENVIPE se resuelva, ese candidato de universo mujeres 15+ queda como la
única fuente con avance para `exposicion_violencia`, sujeta a que ENVIPE
(universo completo) la desplace si aparece.

---

## 5 · Límite de lectura declarado

Esta sesión leyó completos: `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md`
(§0.2, §4.0-§4.2), `forense/notas/2026-08-04-cal-conf-faseb-pos4-rehecho-paso1.md`
(nota de `PR #61`, completa — para no repetir su verificación de cero),
`forense/hitoE-campana-medicion-v2_0.md` §15 (y §14.3 para la fila citada),
`canon/modelo-decision-v4_0.md:270-280,374,619-627` (contador vigente y
fila `G4`), `canon/gobernanza-v1_15.md:525-535` (`ADR-52`, completo),
`milpa/procedencia.yaml:435-445,470-500` (línea citada por el encargo y la
escala real de `exposicion_violencia`), `data/manifiesto.yaml` (entradas
`envipe2025_fd_pdf`, `cuest_principal_envipe2025.pdf`, sin editar),
`forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md` (completa —
confirma el candidato parcial de ENDIREH y el entorno donde INEGI sí
responde). No se abrió microdato. No se leyó FD ni cuestionario
(bloqueados por red, §0.2). Se corrió `python3 tests/check.py --baseline`
— 19 FAIL · 84 WARN, línea base VERDE, sin cambio atribuible a este acto
(nota de solo lectura, sin tocar corpus/canon/milpa). No se tocó
`data/manifiesto.yaml` ni `canon/` ni `milpa/`.
