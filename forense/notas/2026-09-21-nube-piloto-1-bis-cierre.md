# ACTO GEN2-NUBE-PILOTO-1-bis · nota de cierre (21/sep/2026)

Encargo: `forense/encargos/2026-09-20-GEN2-NUBE-PILOTO-1.md` (archivado verbatim por 0-bis A.3 en el commit rescatado `91b1e9fd`; sha256 `ed67f208d41058fec391e1059ba267b3451ddde368d25cb6df3aae90d0bb3fc3`). SHA de redacción declarado: `bd9ed213`. Base real: `d582506` — main se movió dos veces durante el acto y se re-derivó las dos, sin PARO.

MODO: `RÍGIDO`. No se tocó `spec.yaml`, `medidor.py` ni ningún `sello.*` de `CALC-ENIF-0001`, ni ninguno de los dos archivos que `PR #930` congeló.

---

## 1 · Resultado, en una línea

`RESULTADO = REPRODUCE` · `CONTEXTO = DISTINTO` (razón `dependencias_distintas`), en `milpa-inegi`, sobre un payload que bajó **el descargador rescatado**, con su fila en `forense/replay-evidencia.tsv` en este mismo acto. **«Hecho» según el encargo: satisfecho.**

**No generaliza** — verbatim, como mesa pidió: *un `REPRODUCE` sobre un payload de 3.1 MB en un host no demuestra que 18.4 GB en 200 hosts funcionen. El piloto prueba que el carril existe, nada más.*

---

## 2 · Por qué existe un `-bis`, y qué reemplaza

El encargo se intentó dos veces y ninguna llegó a main:

- **`PR #930`** (rama `claude/new-session-lvyz4s`) entregó la **pieza 1 entera y congelada** y paró por **PARO (e)**: corrió en `cloud_default` con el egreso a INEGI bloqueado. Su propia nota lo declara y lo mide por dos vías.
- **`PR #931`** ejecutó el encargo completo en `milpa-inegi` con una pieza 1 **distinta**. Sus cuatro rótulos —`ADR-569`, `FP-402`, `NC-0423`, `NC-0424`— quedaron **todos ocupados en main** por otros actos en cuestión de horas.

Mesa decidió (21/sep/2026, sobre opciones presentadas por esta sesión) que **este acto reemplaza a `PR #931`** y que la pieza 1 que vive es la de `PR #930`. Los dos PR se cierran como `SUSTITUIDO-POR` éste (política de cero ramas, A.14).

---

## 3 · ARRANQUE (salida cruda del hook, A.2 en tres partes)

Primera corrida del acto, **antes** de tocar nada:

```
ENTORNO-DERIVADO = CAJA
senal-corpus: montado=SI archivos_examinados=1
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: PERMITIDA (http_code=200, http_connect=200, x_deny_reason=ausente, via_proxy=SI)
```

`red: PERMITIDA` → **no hay PARO (e)**, que es la mitad de la compuerta que mesa nombra explícitamente. Pero `ENTORNO-DERIVADO` dice `CAJA` y el encargo declara `NUBE`, que es la otra mitad. **No se paró, y la razón está medida, no supuesta:** el único archivo en `data/raw` era el payload de ENIF 2024 que el acto sustituido (`PR #931`) había bajado en este mismo worktree horas antes. Apartándolo, el mismo contenedor, la misma red y la misma variable dan:

```
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=VACIO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: PERMITIDA (http_code=200, http_connect=200, x_deny_reason=ausente, via_proxy=SI)
```

Es decir: **la caja es NUBE; lo que se había volteado era la señal.** Va como hallazgo, no como nota al pie — §7.

`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sigue diciendo `cloud_default` dentro de `milpa-inegi`, como dirección advirtió: la variable no discrimina el entorno.

---

## 4 · El rescate — verificado, no supuesto

Injertados sobre `origin/main` exactamente dos commits de `claude/new-session-lvyz4s`:

- `91b1e9fd` — 0-bis A.3, archiva el encargo verbatim.
- `ca194d3f` — COMMIT-1, congela `tests/manifiesto.py --descarga` y su arnés.

**No** se trajeron `625ea17e` ni `111e9ff6`: su cierre lleva `ADR-569`, `NC-0423` y `FP-402`, los tres ya ocupados en main.

Los dos aplicaron limpios y el congelamiento sobrevivió:

```
f1030b8bbd3d9d6a626f038514c09b97609397891fe0663ba65e643b0942e753  tests/manifiesto.py
45ba0e1cb8932cf9e788dd0d3442c838715b286af72a081bac73349587715e01  tests/test_descarga_manifiesto.py
```

— idénticos a los que dirección declara. Se re-verificaron **después de cada commit posterior** de esta rama, incluido el merge de `origin/main` que resolvió un conflicto en `.github/workflows/verify.yml`, y no cambiaron.

Arnés sobre la base nueva: `python3 tests/test_descarga_manifiesto.py` → **26 PASS · 0 FAIL**.

**Lo único que se le añadió a la pieza 1, en commit aparte:** el paso de CI que D-21 exige. Aquel acto no lo puso porque paró por PARO (e) antes del cierre, y un test que nadie corre es decoración (NC-0331). El conflicto de merge con `origin/main` —que había añadido su propio paso en el mismo punto— se resolvió **conservando los dos**, no eligiendo uno.

---

## 5 · Pieza 2 · el piloto

Descarga, con el descargador rescatado, salida cruda:

```
enif_2024_enif_2024_bd_csv [data_raw]: DESCARGADO-AHORA -- 3131148 bytes desde
  www.inegi.org.mx, sha256 verificado contra el manifiesto antes de entrar a
  'data_raw' -> enif_2024_bd_csv.zip
    raíz resuelta: AUSENTE -> data_raw (cabecera de data/manifiesto.yaml)
```

Sin redirección: **no hay host nuevo que reportar a mesa** (firma 1).

**Decisión declarada:** `data/raw` ya tenía ese payload, bajado por el acto sustituido con **otro** descargador. El encargo excluye de «hecho» un verify sobre un payload traído a mano y exige que lo baje la pieza 1, así que se apartó el archivo —reversible, `data/raw` es gitignorado y nada sellado se tocó— y se volvió a bajar con el que vive. **A.7:** las dos copias son byte-idénticas (`cmp`), `sha256 00e4b0b4…f039` las dos veces.

Verify, **dos ejes por separado** (E.3) — salida cruda íntegra en `forense/evidencia-replay-nube-2026-09-21.txt`:

```
[1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
[2/5 SPEC.YAML] IDENTICO
[3/5 INPUT COINCIDE] enif_2024_enif_2024_bd_csv (manifiesto)
[3/5 INPUT COINCIDE] IN-ENIF-SPEC-SELLADA (repo)
[4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO (FP-358: no gatea)
                parametros=IDENTICO  seed=IDENTICO  dependencias=DISTINTO
CONTEXTO: DISTINTO  razon: dependencias_distintas
VERIFY: REPLICA-RESULTADO · CONTEXTO-DISTINTO   (CONTEXTO=DISTINTO · RESULTADO=REPRODUCE)
```

**188 `RESULT REPRODUCE`, 0 discordantes.** `numpy` es la única `dependencias_materiales` que la spec sellada declara; estaba ya instalado en esta caja por el acto sustituido, e instalarlo es latitud explícita del encargo. No se parcheó nada congelado. `NO-EJECUTABLE` no se escribe como `NO-REPRODUCE` (E.3).

**E.7 y el contador.** Fila nueva en `forense/replay-evidencia.tsv` en el mismo acto, texto plano `split`/`join` (ADR-123(h)), 14 columnas verificadas. La fila heredada de 2026-09-09 no se editó ni se borró. **146 → 147 filas de datos**, como el encargo declara — ver la corrección de §7. `cuenta_gen2` **no se movió**.

---

## 6 · Pieza 3 · FP-404, con los dos lados medidos

`FP-404`, `ABIERTA`. Acota `FP-67` a su universo medido (A.10) por firma 6. **La fila `FP-67` no se editó**: sigue `CERRADA` y sigue mandando mientras mesa no firme.

Lo nuevo es que ahora **los dos lados están medidos**, por dos sesiones distintas del mismo encargo, y cada uno entra con su origen citado:

- **(a) CONFIRMA `FP-67` para `cloud_default`** — medición **rescatada** de `PR #930` (`forense/notas/2026-09-21-nube-piloto-1-cierre.md` §2 de esa rama): `red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente, via_proxy=SI)` por el hook, y el descargador dando `NO-OBTENIDO` con `Tunnel connection failed: 403 Forbidden`, por dos vías independientes. **No se reprodujo aquí**: se incorpora citando su origen, como dirección instruyó.
- **(b) VENCE EN ALCANCE** para nube con red `Custom` — medido en este acto.

Aquella sesión también separó, bien, los tres hallazgos que §2 prohíbe colapsar: lo suyo fue **«no pude alcanzar la fuente»** (el CONNECT del proxy devuelve 403 antes de que haya respuesta de INEGI), no «la fuente no tiene el dato» ni «nadie corrió el mecanismo».

---

## 7 · Hallazgos — dos nuevos, tres conservados

Nuevos de este acto:

1. **`ENTORNO-DERIVADO` se voltea solo.** Medido arriba (§3). La señal de corpus no distingue «corpus compartido montado» de «un payload que este mismo acto acaba de bajar», y la derivación de entorno cuelga de ella. Un acto de nube que descargue algo y vuelva a evaluar su compuerta de entorno —o cualquier acto posterior en el mismo worktree— lee `CAJA`. Hoy, de las tres partes de A.2, la única que aguanta un acto que descarga es la sonda de red.
2. **Contar líneas por filas convierte una premisa correcta en una premisa «refutada», y la refutación se hereda.** La nota de `PR #930` da por caída la premisa del contador: «ya tenía **147** líneas, no 146 — la premisa del contador estaba una fila atrás». Re-derivado sobre `origin/main`: **147 líneas = 1 cabecera + 146 filas de datos**, el archivo termina en salto de línea. **La premisa del encargo era correcta.** Regla de oro (§2): una cifra reportada por otra sesión es del tipo (3) y se re-deriva antes de entrar al canon, aunque venga de un acto propio y de la misma semana. El costo de no hacerlo habría sido publicar una corrección inexistente en un ADR.

Conservados íntegros de `PR #930`, con su origen marcado en la propia línea: la regla de clasificación sobre `urlsplit(url).path` y no sobre la URL cruda (los nueve `banxico_sie_*`); el censo de `raiz` (**1 013** ausente · 335 `descargas_mx` · 277 `data_raw` · 4 `reserva_respondentes` · **0** con valor nulo); y la autocrítica de aquel acto por haber corrido una sonda de red **antes** del `COMMIT-1` que la compuerta protege.

---

## 8 · Lo que dirección pidió declarar

**`NC-0343`** — la fila que `PR #930` añadía es de `GEN2-FAM-UNION-ESTIMANDO-1` (`PR #880`), acto ajeno y fuera del perímetro de §9. **Se deja fuera**, por dos razones que no se colapsan: (a) **ya existe en `origin/main`** con su dueño y `estado = ABIERTA` — re-añadirla duplicaría la deuda de otro acto; (b) este acto no produjo **ninguna evidencia** que la cierre, y una fila ajena que uno no puede cerrar no se adopta, se deja donde está. Tampoco se toca.

**«Cuatro líneas de hallazgos»** — la instrucción de dirección las da por cuatro. El diff de `forense/hallazgos.md` entre `origin/main` y `origin/claude/new-session-lvyz4s` trae **tres** (universo: ese diff completo, A.13). Las tres se conservan íntegras. La cuarta corrección de aquella sesión —la del contador— vivía sólo en su nota, nunca llegó a `hallazgos.md`, y es justamente la que resultó equivocada (§7.2).

**La fila de no-corrido de `PR #930`** se marca `SUSTITUIDO-POR` esta PR, pero no en su sitio: aquella fila era `NC-0423` **en su rama**, nunca llegó a main, y ese número hoy pertenece a `GEN2-RELEVO-RECONCILIA-1`. Se absorbe como **`NC-0433`**, `CERRADA` por este acto, enumerando qué absorbe (la pieza 2 entera y la pieza 3) y qué queda huérfano (**nada**).

---

## 9 · Contadores movidos

- `forense/replay-evidencia.tsv`: **146 → 147** filas de datos.
- `forense/firmas-pendientes.tsv`: **+1** (`FP-404`, `ABIERTA`).
- `forense/no-corrido.tsv`: **+3** (`NC-0433` CERRADA, `NC-0434` y `NC-0435` ABIERTAS).
- `cuenta_gen2`: **sin mover**, como el encargo veda. `N_corridas_selladas` +0. Cero adopciones.
- Mediciones sobre México producidas por este acto: **0** — verifica un carril, no afirma nada sobre México. Por eso el módulo de auditoría de rigor extremo no aplica.
