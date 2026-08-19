# Nota del acto · ACTO FP61-ADJUDICA — ficha-puente Bloque C → `ref.A.04`

**Fecha:** 19/ago/2026 · **Encargo:** `forense/encargos/2026-08-19-FP61-ADJUDICA.md` · **Origen:** `FP-61` (`ACTO REFUTACIONES-SIN-OBJETO`, `ADR-117`, `PR #283`) — el gate que ese ADR pidió antes de adjudicar `ref.A.04`.

---

## 0 · ARRANQUE

1. **REPO.** Clon existente, `/home/user/Modelado-Mexicano`. `git log -1`: `e25f2bd3dd7cd5e218aead27a3d400013a5330a5` — Merge PR #289, `ACTO U2-EV1`. `git status` al arrancar: limpio, rama `claude/credito-popular-corpus-adjudica-2btjpd`.
2. **SHA.** Encargo dice `e25f2bd`. Igual — no se movió.
3. **`data/raw`.** No se toca. Este acto es repo-only; no lee ni escribe microdato.
4. **ENTORNO.** `echo ${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}` → `cloud_default` — variable cruda, sin sonda, firma correcta de NUBE (el encargo asigna NUBE, prohíbe UBUNTU).
5. **ESPEJO / INSUMO ADJUNTO.** El adjunto obligatorio (`compass_artifact_wf-e29a28d4-…_text_markdown.md`) **no llegó en el primer turno** — verificado por `find / -iname "*compass*e29a28d4*"` → 0 resultados en todo el filesystem, y `git ls-files | grep -c e29a28d4` → 0 en el repo. Por regla explícita del propio encargo ("si el adjunto no llega o llega vacío, PARA y repórtalo"), el acto se detuvo y lo reportó **sin tocar nada** antes de continuar. El adjunto llegó en el turno siguiente, verificado no vacío (124 líneas, contenido completo con TL;DR/Key Findings/Tabla/Síntesis/Recommendations/Anexo). Archivado en `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md` — verbatim, verificado por `diff` contra el archivo subido: única diferencia, el salto de línea final. Este es el "gate" que `ADR-117`/`FP-61` exigían.

---

## 1 · Veredicto agregado del informe (Bloque C) sobre la forma fuerte del mito

`ref.A.04` dice: *"Los pobres no pagan o no quieren pagar"* (`milpa/refutations.yaml:208`, tier `FUERTE`). El informe evaluó **11 casos independientes** con datos mayoritariamente `AUDITADA` (CNBV/BMV/SEC/dictaminados): **0 CONFIRMA** la forma fuerte (conductual pura); el veredicto agregado que el propio informe declara es **ROMPE/MATIZA**, mayoritario entre los 11 (§B, §TL;DR). Ningún caso con dato auditado sostiene que el segmento popular "no paga" — donde la mora reportada es baja es porque el mecanismo (no la confianza) hace el trabajo, y donde el precio es alto (CAT de dos-tres dígitos) es porque el modelo precarga una pérdida esperada de 6%–20%, no porque el deudor sea virtuoso.

## 2 · Las tres quiebras, como riesgo del EMISOR — mapeadas a los dos atributos de la enmienda

El borrador de enmienda a `ADR-35` (`forense/notas/2026-08-19-adr35-enmienda-borrador.md`) propone exactamente dos atributos para la entidad `prestamista`: `fondeo` y `gobierno_corporativo`. Las tres quiebras que el informe analiza caen en esos dos, no en un tercero:

- **Famsa (2020) → `gobierno_corporativo`.** Revocación por partes relacionadas (Ps. 8,589 M en pasivos con partes relacionadas) registradas para evadir reservas; ICAP bajo mínimo. Autopréstamo, no impago del cliente.
- **Crédito Real (2022) → `fondeo`.** Muro de refinanciamiento en bono CHF 170 M (cross-default ~US$1.9 mil M) — descalce de fondeo mayorista y duración/FX. El ~47% de portafolio en interés capitalizado es, a la vez, la señal contable que ocultó el problema de fondeo real (menos caja de la que el balance sugería), no una causa aparte.
- **AlphaCredit (2021) → `gobierno_corporativo`.** Reexpresión de derivados, falla de control contable (~Ps. 4,100 M de deterioro). Fallo de supervisión interna, no de cobranza.

Las cuatro etiquetas que el informe usa ("fondeo, partes relacionadas, gobierno, contabilidad") colapsan sobre los dos atributos declarados: **partes relacionadas y contabilidad son formas de falla de `gobierno_corporativo`** (autodealing y fallas de control/divulgación, respectivamente); **`fondeo`** es el atributo propio de Crédito Real. Ninguna de las tres quiebras exige un tercer atributo — coincidencia exacta con el alcance mínimo que el borrador de enmienda ya propone, ni más ni menos.

## 3 · Taxonomía de mecanismos (informe §B, §Recommendations-3)

El informe separa tres mecanismos y advierte no mezclarlos bajo la palabra "pagan":

1. **Cobro involuntario en la fuente** (nómina: Crédito Real ~1.2–1.5%, AlphaCredit) → la conducta del deudor es irrelevante; el descuento ocurre antes de que el trabajador cobre.
2. **Colateral líquido** (empeño: Nacional Monte de Piedad ~90% redención, FirstCash inventario añejo 1–2%) → la conducta es irrelevante; la prenda hace el trabajo.
3. **Presión social/grupal sin garantía física** (Compartamos, tandas) → única evidencia de pago genuinamente voluntario, y aun así con castigo precargado (Compartamos: Ps. 2,406 M castigados en un solo trimestre de 2025, CAT de tres dígitos).

## 4 · Regla operativa de alarma (informe §Recommendations-2)

**Umbral declarado por el informe:** si `IMOR-ajustado > 2.5 × IMOR-simple`, la institución sanea por castigo y el IMOR simple es cosmético. El informe cita cuatro casos como cumpliendo el patrón: Banco Azteca, BanCoppel, Financiera Independencia y CAME.

**Nota de tensión interna, re-derivada de la propia tabla del informe (§A), no tecleada:** con los pares de cifras que el informe mismo reporta en la misma fila de tabla, solo Financiera Independencia cruza claramente el umbral declarado —

| Institución | IMOR simple | IMOR ajustado | Razón (ajustado / simple) | ¿Cruza 2.5×? |
|---|---|---|---|---|
| Banco Azteca | 5.35% (jun 2025) | ~10.7% (2025) | ≈2.0× | **No**, por la propia tabla |
| BanCoppel | 8.4% (3T24) | 15.7% (3T24) | ≈1.9× | **No**, por la propia tabla |
| Financiera Independencia | 6.1–6.3% (4T23–24) | ~20% (4T24) | ≈3.2–3.3× | Sí |
| CAME | *(no reportado en la tabla)* | 34.0% cartera vencida ajustada (2023) | no calculable con lo dado | Sin dato pareado |

Esto no invalida la regla como heurística de alarma —sigue siendo una advertencia metodológica sana: nunca leer un IMOR simple del sector popular sin su castigo— pero la lista de "cuatro casos que la cumplen" que trae el propio §Recommendations-2 no reconcilia aritméticamente con la propia tabla de §A para Azteca y BanCoppel, y CAME no trae el par de cifras necesario para verificarse. Se cita así, sin corregir el informe (doctrina `FP-57`, no se retoca) y sin ocultar la discrepancia (doctrina ESPEJO del propio encargo).

## 5 · Ficha B-bis de `ref.A.04` — benchmarks de reversión ("qué cambiaría el veredicto")

Registrados verbatim del informe, §Recommendations-5, como pre-registro de falsación (Bloque B-bis) para el veredicto agregado de §1:

- **(a) → movería hacia CONFIRMA (versión débil).** Un microdato auditado de cumplimiento de tandas/cundinas que muestre default voluntario **<5%** sin garantía. Hoy: **no existe** en fuente auditada (el informe marca la tasa de default de tandas como `NO ENCONTRADO` en SciELO, Sociológica UAM, Forbes, Banco Mundial — §C, caso 8a).
- **(b) → movería hacia CONFIRMA (versión fuerte).** Un estudio que aísle la mora **conductual pura** de la cartera popular —controlando cobro en fuente y colateral— **por encima** de la mora de tarjetas de clase media (referencia de control del propio informe: IMOR ajustado de tarjeta banca múltiple **13.7%**, jun 2025). Hoy: **no existe** en fuente auditada.

Mientras ninguno de los dos benchmarks se satisfaga con fuente auditada nueva, el veredicto agregado de §1 (`ROMPE/MATIZA`, N=11, 0 `CONFIRMA` la forma fuerte) es el que esta ficha registra como vigente para alimentar la adjudicación de `ref.A.04`.

---

## 6 · Compuerta de firma (T3) — verificada, no satisfecha

El mensaje que lanzó este acto se leyó completo, buscando la cadena exacta `FIRMO FP-61: (a) / (b) / (c)`. **No aparece en ninguna forma** — el mensaje describe la compuerta y las tres opciones (T4), pero no trae la firma misma. Por regla explícita del propio encargo (T3): *"Sin cadena: cierras con T1+T2 hechos, fila anotada 'material listo, firma pendiente', y eso NO es fracaso."*

**Consecuencia:** T4 no se ejecuta. `canon/modelo-decision-v4_0.md` y `milpa/refutations.yaml` no se tocan en este acto — quedan exactamente como `ADR-117` los dejó (entidad `prestamista` sin abrir; `ref.A.04` con `tipo`/`mito`/`evidencia_contraria`/`tier`/`falla_si` sin cambio). `forense/firmas-pendientes.tsv`, fila `FP-61`: permanece `ABIERTA`, columnas `dónde` y `encargo` anotadas con el gate cumplido y el resultado de este acto — detalle en `forense/hallazgos.md` y en el ADR de cierre.

---

## 7 · Cierre

- `corpus/forense/compass-4-e29a28d4-credito-popular-2026.md`: nuevo, verbatim + cabecera de procedencia (T1).
- Esta nota (T2): ficha-puente completa, con Ficha B-bis (§5).
- `forense/firmas-pendientes.tsv`: fila `FP-61` anotada, estado sin cambio (`ABIERTA`).
- T4: **no ejecutado** — sin cadena de firma.
- `canon/gobernanza-v1_15.md`: ADR corto de cierre (número derivado al escribir, a re-derivar al fusionar).
- `canon/estado-programa-v1_10.md`: solo cascada de cabecera/WARN.
- `forense/hallazgos.md`: una línea.
- `forense/encargos/2026-08-19-FP61-ADJUDICA.md`: archivado, `CONSUMIDO`.
- Contadores de medición sobre México movidos: **0** — este acto no corre microdato ni mueve `tipo`/`tier` de ninguna refutación; la única cuenta que se mueve es de higiene de tablero (una fila anotada, no adjudicada).
- Gate de cierre: `python3 tests/check.py --baseline` → **21 FAIL · 122 WARN**, `LÍNEA BASE: VERDE`, sin `--freeze` — mismas cifras que el árbol antes de este acto (dos FAIL nuevos, T14 y T15, aparecieron y se corrigieron dentro de este mismo commit: cascada de `estado-programa` §1 tras el archivo nuevo de `corpus/forense/`, y marca `{cita-historica}` en `ADR-121` tras bumpear el conteo de ADR).
