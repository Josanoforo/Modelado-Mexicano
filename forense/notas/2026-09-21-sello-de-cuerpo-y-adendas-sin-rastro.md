# Nota de cierre · el sello del cuerpo, el verificador de sidecars, y las adendas que el repo no guarda

*ACTO `GEN2-TUBERIA-SIDECAR-CUERPO-1` · 21 de septiembre de 2026 · entorno NUBE ·
encargo archivado en `forense/encargos/2026-09-21-GEN2-TUBERIA-SIDECAR-CUERPO-1.md`
(0-bis `3d086c56`) · `cuenta_gen2 = NO` — este acto no mide ninguna celda del programa.*

---

## 0 · Contadores movidos (§5, auditoría v2.4)

Cero contadores del programa. Este acto es aparato: no abre microdato, no emite
ninguna celda, no adopta ni mueve ningún estimador. Lo que mueve es la capacidad
de auditar qué se pidió en un encargo, que hasta hoy se perdía en cuanto el acto
cerraba.

## 1 · Qué quedó

| Pieza | Resultado |
|---|---|
| `P-a` | `tools/sella_sha256.py --cuerpo` — sella y verifica el CUERPO con `N(texto)` (D-a1), candidatos por hash ante cualquier `^## ` más el archivo entero (D-a2 + D-a5), sidecar `X.cuerpo.sha256` (D-a3). Reporta cuál candidato casó. `WARN_ENCABEZADO_AJENO`, no FAIL, cuando lo que sigue abre con otro encabezado. Los tres estados y sus exit codes (0/2/3) intactos; el modo viejo **no cambia** — `tools/corrida0.py` y `tests/check.py` lo importan y ven lo mismo. |
| `P-b` | `.claude/commands/acto.md`, **exactamente** los dos sitios autorizados: sección `## 3 · 0-bis A.3` (el sello en el mismo commit, el texto de (a), la prohibición de re-sellar citando la advertencia del 7/sep del sellador, y la regla de adendas) y el paso 10 del `## 5 · CIERRE` (la frase de D-a6, verbatim). Ningún otro cambio. |
| `P-c` | `tools/verifica_sidecars.py` + `tests/test_verifica_sidecars.py` (11 casos, todos por mutación sobre fixtures salvo dos lecturas del repo real). Cableado en `.github/workflows/verify.yml`, job `adicionales`, en dos pasos: el test y el verificador sobre el árbol. |
| `P-d` | Sello de `#932` restaurado, **no recalculado**: `8a847600182d54be21ee712ecbde51d1ac0dc83214341020dd220d604c9652c0`, leído de `git show d4d472b7:…`. El `.sha256` retirado declaraba `b07f8ba3968f3914c59c6e6f1051f5ebd7ef3cac9b4490a4fb4c8e23ae52b250`. Es la única compuerta de este acto y se ejecutó en el mismo commit que crea el sustituto. |
| `P-e` | `forense/notas/ENCARGOS-GEN2-v1_5-aparato-antes-de-calcular-2026-09-08.md.cuerpo.sha256` = `1fc3d582deb6a0d8bdb30d423af9b5abc71914cabd451543833671e44ce692c9`, sobre el texto de hoy. El `.sha256` viejo (`8e9232f4…`) **intacto**, declarado TESTIGO VENCIDO EN ALCANCE (A.10) con su motivo escrito. El texto no se revierte. |
| `P-f` | Siete líneas en `forense/hallazgos.md`: las cinco que el encargo pide más dos que este acto midió (el huérfano codex y el costo de `sha256sum -c`). |
| `P-g` | La tabla de §3 de esta nota. |
| `P-h` | Huérfano codex declarado y asentado. **Corrección de premisa** — ver §4. |
| `P-i` | Este encargo es el primer encargo del repo que nace con sello de cuerpo: `b0f861aa2877bd14899228025cceabb704f11e798942af45d1a96c1744ba6894`, puesto antes de escribir una sola línea de cierre. El verificador lo cubre desde su primera corrida. |

El universo del verificador hoy: **12 sidecars** en `forense/encargos/` + `forense/notas/`
(A.13). Diez viejos, tres nuevos de cuerpo, uno retirado. `FAIL: 0`, `WARN: 0`.

## 2 · Verificación de la premisa central

La premisa que todo el acto soporta —que el sello del 0-bis de `#932` pasa hoy con
la regla firmada— se verificó **derivándola**, no citándola:

```
candidato                                            sha256
prefijo-antes-de-linea-137: ## NO-CORRIDO / RESERVAS  8a847600182d54be…   ← CASA, sin WARN
prefijo-antes-de-linea-148: ## CONSUMIDO              25b58e302778a386…
archivo-entero                                        ea54f0f05daa506c…
```

El sello del 0-bis casa exactamente con el prefijo anterior a `## NO-CORRIDO /
RESERVAS`, y el encabezado que sigue es uno de los dos de cierre: sin WARN. La
traza que dirección declaró (`d4d472b7` → `d3ac15a9` → `4893f53e` → `847d12b0`) se
sostiene entera.

## 3 · Adendas sin rastro — qué actos corrieron bajo un texto que el repo no guarda

Nada se archiva retroactivamente (firma «Semillas sin ejecutar»). Esta tabla existe
para que quede **escrito** el hueco, no para taparlo.

| Acto | Commits que la nombran | Dónde está el texto |
|---|---|---|
| `GEN2-MARCADOR-REDISENO-1` | `07794972` | **Pegada al encargo** tras el 0-bis. El texto existe; rompe el sello del cuerpo, y es justo el caso que la regla de hoy manda archivar como archivo propio. |
| `GEN2-TRAMITE-FIRMAS-3` | `00ac06e9` («Adenda de mesa: reserva:envipe2026») | **Aterrizó como archivo**: `forense/encargos/CUADERNO-DE-FIRMAS-2026-09-21.md`. |
| `GEN2-CELDA-D-PILOTO-3-P0` | `4d4131df` («Adenda de mesa del 20/sep: P0 deja de gatear el COMMIT-1») · `352c7aed` («Adenda de mesa punto 4») | **NO-ENCONTRADO.** No está en el encargo ni como archivo propio; sólo la nota del paro la refiere. |
| `GEN2-LIMPIEZA-RAMAS-LOCALES-3` | `2802e63b` («tras adenda de dirección») · `adbdb3c0` («hipótesis de dirección, adenda») | **NO-ENCONTRADO.** |

Descartado como falso positivo: `4fc8fcd1`. **No** son adendas `LIMPIEZA-RAMAS-LOCALES-4`
ni `-6`: ahí el INPUT DE MESA *es* el encargo.

**La diferencia se declara, no se estima.** Mesa reportó unas seis adendas; el repo
nombra **cuatro actos**, de los cuales **dos** conservan el texto y **dos** no. Las
dos que faltan para llegar a seis no se pueden nombrar desde el repo con ningún
universo que este acto haya podido examinar (6 refs del remoto, los 56 encargos
tocados del 19 al 21/sep): A.4 `NO-ENCONTRADO`, con el mecanismo declarado. No se
infiere cuáles pudieron ser. Asentado como
`NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-02`.

## 4 · Una premisa que cayó, y por qué la corrección importa

Dirección declaró `EJECUTADO` que el sello del insumo codex de
`forense/notas/insumos-externos/pisos-enif2021-0002-rama-codex/` «cita un `sello.json`
que no está junto a él» y que el verificador debía declararlo huérfano. Se sostiene
la cita rota; **no** se sostiene que el payload esté perdido. Medido aquí: el archivo
hermano `pisos-enif2021-0002-codex-2026-09-20-sello.json` tiene sha256
`96fd07bc97709c11c33cabad9e689698f9e75bdcfefa831b0c155e47faa821fb`, **exactamente** el
que el sidecar declara.

Eso obligó a una decisión de diseño que el encargo dejaba a latitud, y es la parte
que vale la pena: la primera versión del verificador caía al archivo hermano cuando
la cita no resolvía, y con esa regla el huérfano **desaparecía de la vista** como un
`CASA` limpio. Resolver una cita «por parecido» es exactamente cómo un verificador
deja de ver lo que existe para ver. La regla final le toma la palabra al sidecar: la
caída al hermano queda reservada al formato (3), el de hash pelado, donde no hay cita
que romper. Toca logística, no qué se mide: se replanteó, se siguió y se declara
(§2 de las instrucciones, v2.15). Asentado como
`NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-01`.

## 5 · Lo que este acto NO hace

No re-sella ningún otro encargo · no extiende el verificador a los 261 sidecars del
árbol · no archiva retroactivamente ninguna adenda · no toca
`forense/encargos/PLANTILLA-ENCARGO-v2_0.md` · no toca la renumeración ni el asignador
de `ADR` · no reabre la v2.15 · **no fusiona su propio PR** — se publica y queda
propuesto a mesa.

## 6 · Falsador (§9)

Si en tres meses `tools/verifica_sidecars.py` no ha emitido un solo FAIL ni un solo
WARN, se anota y se revisa si valía el aparato. Si el `WARN` de D-a5 salta en más de
uno de cada diez encargos nuevos, lo que no se está cumpliendo es la frase de D-a6
(«la sección de cierre se añade al final; nada por encima de ella se edita») y se
revisa `/acto`, **no** el verificador.
