# DISEÑO EMISOR-M · DELTA v1.0 → v1.1 — las dos directivas de mesa, ejecutadas · 20/ago/2026

**Contra `origin/main = 8b73aee`. El v1.0 queda intacto (evidencia fechada); este delta sustituye sus §3, §4 y §6, y ajusta §2.1 y §8. Directivas de mesa, verbatim (20/ago, capturadas por widget): Q1 → *"benchmark web"* · Q2 → *"Las reglas en prosa nos mete en problemas encuentra otra solución"*.**

---

## Δ-§3 · El intervalo de M — resuelto por benchmark (sustituye §3 del v1.0)
El benchmark ordenado por mesa está corrido y archivado: `BENCHMARK-INTERVALO-CORREDOR-M-2026-08-20.md` (cuatro literaturas: Cooke, NUSAP, IPCC, ecoinvent). Veredicto, en una línea cada uno: O1 reprobada (calibración-0 = FP-83 del lado corredor) · O2-con-constantes reprobada (doctrina IPCC: la confianza no se interpreta probabilísticamente) pero **O2′-derivada aprobada como destino** (procedimiento ecoinvent/Ciroth: razones de incertidumbre por grupo de clase contra el grupo medido) · **O3 aprobada para el piloto, mejorada** · O4 compatible, OLA-5.

**La síntesis que sube a firma (Q1-bis):**
1. **M emite punto + clase-como-confianza** — dos lenguajes que no se mezclan (IPCC): el punto es lo que el modelo afirma; la clase viaja al lado como pedigree, jamás convertida a banda a mano.
2. **Intervalo solo donde hay EE real** (hoy: las 2 entradas `ic95` de procedencia; mañana: cada coeficiente que gradúe a MEDIDO). Campo `spread` reservado y **nulo por defecto** — NUSAP-conforme: pedigree alto no fabrica spread.
3. **El piloto gana el producto `CAL-ASIGNADO`** (estilo Cooke): con las semillas que ya existen — celdas `P0` de plomería + todo par asignado↔L-valor que la tubería produzca — se mide **qué fracción de los valores ASIGNADO del programa cae dentro del IC del árbitro**. Es un resultado científico de primera clase (¿está calibrada la práctica de asignación de mesa?) y se publica junto al marcador, mismo tamaño de letra. No sustituye a la calibración de intervalos de L/B/E: es su análogo honesto para un corredor puntual.
4. **Bandas por clase = destino v2, pre-registrado hoy**: se derivarán del propio CAL-ASIGNADO por el procedimiento ecoinvent (grupo por clase / grupo medido = factor), con mutabilidad declarada y el falsador escrito en el benchmark §4 (si el pedigree no predice el error, la banda por clase muere).
**Consecuencia técnica verificada:** nada del scoring ni de E se modifica — `interval_score`/`crps_normal_aprox` ya hablan punto+intervalo, y `combinar_continua` solo exige `valor_punto`.

## Δ-§4/§6 · La "otra solución" — el emisor NO compila prosa (sustituye §4 y §6 del v1.0)
Mesa rechazó las tres opciones sobre transcripción. La verificación de esta sesión encontró la salida en el árbol: **la capa cuantitativa del modelo ya es máquina**, y lo que no lo es, no hace falta transcribirlo — hace falta **declararlo**.

**Las tres fuentes-máquina, únicas y suficientes (el emisor no lee prosa jamás):**
- **`milpa/tramite.yaml`** — 5 reglas con `p`, dos niveles ya separados (`si.disparadores` globales · `si.contexto_*` palancas), la pareja completa del gate.
- **`milpa/procedencia.yaml`** — coeficientes y condicionales con clase, **y la capa de generadores ya parametrizada por desenlace** (verificado: `{gen: G1, coefs: {confianza_institucional: −0.60, radio_confianza: −0.35}...}` · `{gen: G5, ...}` · entradas `donde: civico.voto.* → desenlace`). Aquí vive lo que el duelo puede preguntar en números.
- **El Registro congelado de `modelo §7`** — tabla de 49 filas, IDs fijos que nunca se recomputan — **parseado, no re-transcrito**: un lector mecánico extrae `id · tier · enunciado` del canon mismo; la fidelidad es por construcción (el parser no puede inflar un tier: lo copia), y un test compara el parse contra el archivo en cada corrida. Sirve para metadatos del crosswalk (qué regla respalda qué), no para inventarle números a nadie.

**La regla que sustituye a toda migración:** lo que el modelo solo afirma en prosa **es `NO-EMITE` por construcción** — silencio honesto, contado y publicado. Y la promoción prosa→máquina **no es tarea del piloto**: es el mecanismo ordinario del canon, por acto propio con firma, exactamente como el propio `modelo §0` narra su numerador 9→12 (`norma_de_género`, `obligación_medida`, `confianza_institucional_generico` — tres promociones, tres actos, tres firmas). Si el duelo revela que una afirmación en prosa importa, la maestra lanza SU acto de promoción; el emisor la consumirá el día que sea máquina.

**R3.4 sin prosa nueva — las tres condiciones, mapeadas a lo que ya existe:** (A) y (B) encienden/apagan `riesgo_fiscal_percibido`/`coercitivo` — palancas que `tramite.yaml` ya trae, con su pareja anti-`NO_COVERAGE` restituida; (C) "apagar el canal de confianza personal" se implementa como **switch de generador `G1a`** en la capa que `procedencia.yaml` ya parametriza (poner a cero la contribución del canal en la combinación de generadores) — un interruptor del bucle, **no una regla nueva ni una edición**. El assert anti-`NO_COVERAGE` del harness queda igual que en v1.0 §5.

**ADR-68(a): la ambigüedad se disuelve, no se adjudica.** No se compila, no se transcribe, no se edita regla alguna; el emisor es un consumidor de tres archivos existentes más un parser de solo-lectura del canon. La pregunta Q2 del v1.0 muere sin necesitar firma — lo que sube a mesa es la arquitectura, no un permiso de excepción.

## Δ-§8 · Actos, ajustados
**ACTO EMISOR-M-1** (NUBE · Opus · gate: firma Q1-bis): `milpa/src/emisor.py` (bucle de dos niveles + switch de generador) · lector de las tres fuentes (cero archivos de reglas nuevos) · parser del Registro §7 con su test de fidelidad · `tests/aceptacion_r3_4.py` (A∧B∧C + anti-`NO_COVERAGE`) · esqueleto del crosswalk con `emisibilidad` (se espera `NO-EMITE` alto: es el dato que la saturación del marco necesita). Perímetro: `milpa/src/emisor.py` (nuevo) · `tests/` solo nuevos · crosswalk nuevo · nota/ADR/tablero/hallazgos/encargo. Los 6 `test_motor_*` y `--baseline` VERDES, sin `--freeze`. Contador: **R3.4 corrible**; medición sobre México: 0, dicho.
**ACTO EMISOR-M-2** (NUBE · Opus): crosswalk 60/60 · emisión M para todo lo `EMITE-*` con **hash al registry antes de R** · **producto CAL-ASIGNADO cableado** (denominador/numerador de Δ-§3.3, receta en el benchmark §3) · conteo `NO-EMITE` entregado a la fila de saturación (`FP-82`). Contador: **filas M comprometidas 0→n de 60**.
**Acto hermano (dueño hitoD, sin cambio):** FICHA-R3.4 con el límite de Nota 3 — sigue siendo condición para mover 13/27, y sigue dicho antes.

## Lo que este delta NO hace
No toca `ADV1-M5`, `⊕` ni `FP-91` (otra lane). No escribe código (espera Q1-bis). No promueve ninguna regla de prosa. No inventa una sola banda — esa es la línea que el benchmark acaba de volver doctrina citada.
