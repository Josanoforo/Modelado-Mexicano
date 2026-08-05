# ENCARGO M-4: adjudica ADR-63 con la fila `E` de `R1.3` (MESA-M4)

Mesa #20 + consultoría, 5/ago/2026 (TZ America/Mexico_City, verificado con
`TZ=America/Mexico_City date` → `2026-08-05 00:25 CST`). Ejecutor: sesión
Claude Code, entorno de nube (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`).
Acto de escritorio: no abre microdato. Contador: Hito D 12→13.

## 0 · ARRANQUE

Clon existente en `/home/user/Modelado-Mexicano` (no home), rama
`claude/encargo-m4-r1-3-adjudicacion-czqze3`. `git fetch origin` movió `main`
de `bd2c975` (base declarada del encargo) a `3f73c29` (fusión de PR #114,
`sesion/hitoD-r1-3-canal-confianza`) — prereq 1 cumplido: `Nota 29` presente en
`hitoD-preregistro-v2_0.md:1026`, `hitoD-R1_3-veredicto-v1_0.md` existe en
`main`. Obsolescencia (2-bis): último ADR = **ADR-61** en ese momento, ninguno
adjudicaba `R1.3`, y el bloque "Registro de veredictos archivados" no traía
línea `R1.3` — la adjudicación no existía. Entorno: `cloud_default`, firma
correcta de nube (ADR-59(b)); sonda saltada. `data/raw`: no aplica.

**Hallazgo bloqueante en ACTOS VIVOS, detectado por esta sesión (no declarado
de antemano por mesa).** `git branch -r` expuso `origin/claude/encargo-mt-mantenimiento-37tsdp`,
sin PR abierto (`list_pull_requests` state=open → vacío), un commit por
delante de `origin/main`, mensaje `"...(ADR-62)"`, tocando
`canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md` y
`forense/hallazgos.md` — exactamente el perímetro de este encargo, y
reclamando el mismo número de ADR (62) que le habría correspondido a este
acto. Reportado a mesa antes de tocar ningún archivo (regla del encargo: "si
alguno toca gobernanza/estado: no lances o secuencia"). Mesa confirmó por
verificación directa contra el árbol: `origin/main` avanzó a `1c8d14a` — PR
#115 (MT, que se llevó ADR-62), #116 (E-ENVIPE) y #117 (E-MXFLS) ya fusionados,
cero ramas remotas sin fusionar. El hallazgo quedó resuelto por secuencia, no
por decisión de este acto.

## 1 · Refresco y ADR máximo — derivado, no copiado

```
$ git fetch origin && git merge --ff-only origin/main
Updating 3f73c29..1c8d14a  (fast-forward, cero commits propios en la rama)
$ grep -noE "ADR-[0-9]+" canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -5
ADR-58
ADR-59
ADR-60
ADR-61
ADR-62
```

Máximo = **62**, único, sin huecos. Este acto sella **ADR-63** (máximo + 1,
derivado contra el árbol real en el momento de editar, no copiado de ningún
mensaje previo).

Re-verificado tras el refresco: `Nota 29` sigue presente, el bloque de
veredictos archivados sigue sin línea `R1.3` — la adjudicación seguía sin
existir. PREREQ 1 y 2-bis se sostienen.

## 2 · Verificación de la redacción MESA-M4 contra el veredicto (§5-§7)

Redacción de mesa, pre-declarada en `hitoD-R1_3-especificacion-v1_0.md §2`
Rama 1: *"el falsador corrió limpio en penetración y brecha rural-urbana, y no
se satisfizo — la regla sobrevive esta prueba, acotada porque la condición 3
(canal de alta desagregado) nunca pudo evaluarse."*

Verificada palabra por palabra contra `hitoD-R1_3-veredicto-v1_0.md §7`, que
contiene la misma frase, verbatim, como su propia "Propuesta: `E`" — no hay
divergencia entre lo pre-declarado y lo obtenido. Verificado también contra
§5-§6 del veredicto: Condición 1 (penetración) = 3.86%, IC95%=[3.23%,4.48%],
decisiva, sin reserva estadística declarada (a diferencia de `R5.2`/Nota 18);
Condición 2 (brecha) = 2.98pp, IC95%=[1.94pp,4.03pp], decisiva. Ninguna de las
dos condiciones matiza la frase pre-declarada (no hay caso límite que exigiera
una reserva escrita, como sí ocurrió con `R5.1`/`R5.2`/ADR-58(c)). Se escribe
sin ajuste.

## 3 · Cascada de contadores — derivada de T18, no tecleada

```
$ python3 tests/check.py 2>&1 | grep -E "T15|T18|FAIL · .*WARN"
  [ ok ]  T15 T-ADR-COUNT
  [ ok ]  T18 T-PASO2-EJECUCION
  18 FAIL · 95 WARN
```

Conteo real del bloque append-only tras añadir `R1.3` → `E` (mismo parser que
T18, `_VEREDICTO_CANONICO`): **13** fichas únicas (7D·2B·2A·2E por letra,
contando `R4.3` una sola vez como en el desglose vigente de `README:36`).
Propagado a `canon/estado-programa-v1_10.md` (§L5 línea 95, §7 líneas 122 y
196 — esta última es la que T18 lee) y `README.md` (líneas 36 y 89, con la
receta de sus propios comentarios HTML). Conteo de ADR (62→63) propagado a
`canon/gobernanza-v1_15.md:2` (cabecera) y `canon/estado-programa-v1_10.md:27,99`
— receta de T15. Fuera de perímetro de este acto, declarado como deuda igual
que ADR-58(e): `gobernanza:358,810` (narrativas internas de §4/§5) quedan en
"12 de 27" hasta el próximo acto con perímetro de cascada completa.

## 4 · Suite y remoto

```
$ python3 tests/check.py --baseline
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
$ git remote -v
origin  https://github.com/Josanoforo/Modelado-Mexicano (fetch)
origin  https://github.com/Josanoforo/Modelado-Mexicano (push)
```

Idéntico a la línea base previa al acto — el único cambio es el conteo de ADR
y de veredictos archivados, exactamente lo que este acto movía.
