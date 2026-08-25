# `ACTO 2 · SERIE-HOMOGENEA-CODI` — encargo archivado

| campo | valor |
|---|---|
| **SHA de redacción** | `7f26983` (tip de `ACTO PURGA-EJECUTA`, que fusiona `origin/main` `14a7b42`) |
| **Entorno asignado** | **UBUNTU** — abre PDF del corpus (`data/raw/R3.4_Banxico_CoDi_SPEI/`). NO nube: sin corpus montado no hay bytes que barrer |
| **ESTADO** | **CONSUMIDO** — 25/ago/2026, rama `serie-homogenea-codi` |
| **Fila que ejecuta** | `FP-142` · **Fila que actualiza** `FP-104` |

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2)

**Estructura.** Todo lo que el encargo cita existe en el árbol al SHA de redacción:
`forense/ficha-r34-conda-v2-spec.md` (266 líneas, §1-§9), `forense/firmas-pendientes.tsv` (filas `FP-142` y
`FP-104` presentes), `canon/gobernanza-v1_15.md` (`ADR-37`, `ADR-146`, `ADR-168`), `milpa/src/emisor.py`
(`UMBRAL_A_RAZON = 0.10`), y los 20 payloads de `data/raw/R3.4_Banxico_CoDi_SPEI/`.

**Contenido.** Dos premisas del encargo **no reproducen** y se corrigen en el acto, no en silencio: (i) el encargo
enumera «cuentas SPEI o personas CoDi» y las dos son `NO-ENCONTRADO` — la unidad que sí existe, `operaciones`, el
encargo no la nombra; (ii) el encargo dice «22 payloads» y son **20** en el directorio y **20** en
`data/manifiesto.yaml`.

**Cobertura retroactiva.** Ningún acto anterior había barrido los Informes IdMF por constructo homogéneo: la ficha
los cita (§3) para el constructo (ii) del lado CoDi y para el de personas del lado SPEI, que es justamente la
mezcla que `FP-142` existe para deshacer.

## ARRANQUE (A.2, tres partes)

`sin_variable` (entorno sin variable de clave de proveedor) · sonda
`curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → **200** ·
`ls data/raw/ | head -1` → `2005trim1_csv.zip` (**321** entradas; vacío habría sido PARO).
`pgrep -af claude` → sólo el propio shell.

## Texto del encargo, verbatim

> **ACTO 2 · SERIE-HOMOGENEA-CODI — ejecuta FP-142 (L3-b) y deja R3.4 a una re-corrida (Opus; contador: cero
> directo — arma el 19 de 27)**
>
> EXISTENCIA (dirección): los Informes Anuales de Infraestructura Banxico 2019-2024 y el xlsx de cuentas validadas
> YA están en corpus (EXPLORA-2, 22 payloads); la ficha r34-conda-v2-spec quedó enmendada por #338 con L4-a
> (término textual, «activas» retirada). Lo que falta —textual de FP-142— es una serie misma-unidad: cuentas SPEI
> (para cuenta↔cuenta) o personas CoDi (para persona↔persona). TAREAS: (1) barre los Informes en corpus (páginas
> de SPEI y de CoDi) por el constructo homogéneo, con doble extractor y cita página exacta; veredicto A.4 por
> candidato; (2) si EXISTE-SATISFACE: enmienda fechada en la ficha declarando el par re-especificado en esa
> unidad, y re-corre el par bajo la spec enmendada (dos commits: enmienda-spec primero, corrida después; «el
> primer resultado…» aplica a la re-corrida); veredicto de la condición A propuesto → FP-104 actualizada, lista
> para tu firma; (3) si NO-ENCONTRADO tras agotar los Informes: la fila lo registra con universo (páginas
> examinadas) y FP-104 queda con la rama A3 que L3 dejó como salida — también es cierre. PERÍMETRO:
> forense/ficha-r34-conda-v2-spec.md (enmienda) · tablero (FP-142, FP-104) · gobernanza · estado · nota
> 2026-08-25-serie-homogenea.md · encargo · scratchpad. NO toca milpa/ ni el preregistro.

**Reglas comunes del pack, verbatim.**

> 🚫 --freeze · pgrep -af claude · iconv -f utf-8 -t utf-8 -c · ⚠️ [v2.11] A.13 en todo negativo · nada del espejo
> · ADR re-derivado, renumera si colisiona · recifrado con punto fijo · suite VERDE con tail · encargo CONSUMIDO ·
> fuera del perímetro: PARA.

## CONSUMIDO — resumen de ejecución

Rama `serie-homogenea-codi`, **dos commits** en el orden exigido: `a23fda6` (enmienda-spec congelada **antes** de
correr) y el commit de la corrida. Resultado: **`EXISTE-SATISFACE`** por la vía (2) — la serie homogénea es
**número de operaciones**, no cuentas ni personas. Condición A re-especificada: **veredicto propuesto `A1`
(satisfecha), NO sellado**; falta que mesa firme la sustitución de la cláusula «con enlace firmado» por «sobre
unidad homogénea, sin enlace» (`§10.7`). `R3.4` sigue **sin veredicto** (B y C con base medida 0 de 2). Perímetro
respetado al pie: `forense/hallazgos.md` **no** se tocó por no estar en la lista, aunque el acto produjo un
hallazgo que lo merece (contención `CoDi ⊂ SPEI`) — queda declarado en la nota y en `ADR-170`. Detalle:
`forense/notas/2026-08-25-serie-homogenea.md`.
