# GEN2-DIGESTO-CORRECTIVO-1 · cierre técnico

Fecha: 2026-09-16

Rama: `acto/gen2-digesto-correctivo-1`

Base de arranque: `origin/main @ 9dffd6455c67e2ca99740e79f90be59a13f250e1`

## Resultado

Se corrigió el defecto reproducido por PR #816 sin tocar T22/T25 ni las
fuentes administrativas. La sección H neutralizaba cada celda antes de
armar su fila Markdown, pero la unión de dos celdas podía crear por primera
vez el patrón T22(b): `PROPUESTA` al final de la copia vigente de `sucesor`
y `mesa` en la copia anterior del mismo campo. El caso real fue `NC-0076`
en `main @ 84bd7fdd4a85f31960334ba932783b6914c66726`.

El correctivo vuelve a neutralizar la fila justo después de ensamblarla.
Cuando la alternativa que coincide empieza por `PROPUESTA`, sustituye sólo
ese token por `«marcador-T22-b»` y conserva el resto de la frase. El ID, los
dos valores del campo, la decisión pendiente y la procedencia
`forense/no-corrido.tsv` siguen visibles.

## Evidencia antes / después

| Evidencia | Resultado real |
|---|---|
| Corte histórico sin parche | `python3 tools/digesto_tramite.py --fecha 2026-09-16 --stdout --sin-suite` sobre `84bd7fd` → rc=2, stdout=0 bytes; T22(b) sobrevivió |
| Localización | salida diagnóstica no verificada: sección H, fila `NC-0076`, patrón creado entre las columnas `sucesor` y `campos modificados` |
| Mismo corte con generador corregido | generador de esta rama con `--raiz /tmp/mm-digesto-historico-84bd` → rc=0, 55 neutralizaciones, salida completa de 68,150 bytes |
| Fixture contra generador anterior | `t_neutralizacion_al_ensamblar_columnas_preserva_contenido` → 2 fallos esperados: marcador sobreviviente y contenido no preservado |
| Fixture corregido | `tests/test_digesto_nc.py` → 22/22 casos, 0 fallos |
| Corte vigente, diagnóstico | `--stdout --sin-suite` → rc=0 |
| Corte vigente, sin truncar | `--stdout --sin-suite --tope-texto 0` → rc=0, 94,539 bytes |
| Vista de mesa | `--mesa --stdout` → rc=0, 69 filas, 0 vencidas |
| Generación completa | `--stdout`, suite y verificación activas → rc=0 |
| Escritura externa completa | `--salida /tmp/gen2-digesto-correctivo-1-output/DIGESTO-2026-09-16.md` con suite y verificación activas → rc=0; `sha256:f0a1265cd9bfbbe1267620153162bf0ac97e95832b8e9442c962a773ed3eb57d` |
| Escritura completa o ninguna | `t_hash_referencia_incongruente_detiene_diff`, incluido en los 22 casos: ante rc=2 conserva byte a byte el archivo previo; la escritura exitosa externa contiene cabecera, pie y fin de línea y `verifica()` devuelve `[]` |
| Repetición | dos corridas consecutivas con `--stdout --sin-suite` → contenido idéntico, `sha256:496e028f8c0cb4e52b83d7f7f25542a585e4861a0c45b43a163ae178e144d14a` |

Pruebas dirigidas adicionales:

- `python3 tests/test_digesto_candidatas.py` → rc=0.
- `python3 tests/test_digesto_fecha.py` → rc=0.
- `python3 tests/test_digesto_mesa.py` → 10/10 casos, rc=0.
- `python3 tests/check.py --baseline` → rc=0, línea base VERDE; 3 FAIL y
  4351 WARN heredados, sin entrada nueva.

## Cero escritura de fuentes

Los hashes del árbol de trabajo después de todas las corridas coinciden con
`HEAD`:

| Registro | SHA-256 |
|---|---|
| `forense/firmas-pendientes.tsv` | `b9d0f0ae9a599995ed5cd00f7c978a087fa8e279bf2a105b79a25c37f5a30cd9` |
| `forense/no-corrido.tsv` | `a248b13b925153e8b3a6697092e93b6fcda4a33dfd55773d0ad4800722d9a852` |
| `forense/rutinas.tsv` | `23c5ad1d360becdf2b42aa52fdb28d6885f6383ebe74bbaa45b65cd60ddb9a8a` |
| `data/curacion-registro/cola-adquisicion-registro.tsv` | `55b4c8e726d782b5509e0d82939387bdbbe9146b34a195db1e6f19ffef39a011` |

## Límites y paso posterior

- Digesto canónico publicado: **NO**; diferido hasta que CAREO/TRÁMITE-4 y
  este correctivo estén integrados.
- Rutina automática acreditada: **NO**; todas las comprobaciones fueron
  manuales y locales.
- Cascada compartida, scheduler, cron, firmas, decisiones, numeraciones,
  gobernanza, tableros, rutinas y manifiestos: **sin cambios**.
- CI remoto: pendiente de observar en el PR.

Después de las integraciones, el responsable de publicación debe actualizar
su worktree y seguir el runbook vigente `.claude/commands/tramite.md`. Para
reponer el incidente histórico, el comando exacto del generador existente es:

```bash
python3 tools/digesto_tramite.py --fecha 2026-09-16
```

Ese comando sí escribe `forense/digesto/DIGESTO-2026-09-16.md`; no se ejecutó
en este acto. Una publicación de otro día debe usar su fecha real y el SHA ya
integrado, mediante la misma rutina `/tramite`, sin crear otro publicador.
