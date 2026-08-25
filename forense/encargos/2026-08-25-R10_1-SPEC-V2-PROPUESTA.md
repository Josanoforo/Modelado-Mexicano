# ENCARGO · ACTO SPEC-R10.1-v2 — la versión 2 del experimento de la fila de espera (FP-108, GO de mesa 24/ago)

- **SHA de redacción:** contra `origin/main` al redactar, sesión 25/ago/2026.
- **Entorno asignado:** **NUBE**. No Ubuntu.
- **Estado:** `EJECUTADO` — 25/ago/2026, produce `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md`, fila de tablero `FP-128`, esta nota y este encargo.
- **CONTADOR DECLARADO: cero.** Redacta una PROPUESTA; correrla y sellarla son actos posteriores (v2.1 corrida, v2.3 sello).

---

## Texto completo tal como se lanzó

EXISTENCIA (dirección): `FP-108` (FIRMADA el 24/ago) autoriza la spec sucesora con cuatro piezas nombradas en la propia fila de tablero: codificación pragmática · segundo codificador · la arista medido-sin-potencia desemboca en `C` · techo de `n` declarado. La spec v1 defectuosa y su defecto `D-08` ("replicable no es replicado") viven en la ficha `R10.1` del preregistro y en la tabla de notas al calce (`hitoD-preregistro:313`).

TAREAS:
1. Redactar `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md` con las cuatro piezas, escala de falsación completa (incluida la fila de no-refutación `B-bis`: corroborada/acotada/falsador débil, con precedencia), universo, unidad, y qué exactamente contaría como `C`.
2. La spec declara qué entorno y qué insumo necesita la corrida (¿campo?, ¿corpus?) — sin adivinar disponibilidad: veredicto `A.4` por insumo.
3. Fila de tablero nueva: "mesa sella la spec v2 de R10.1" (`ABIERTA`).
4. Nota corta.

PERÍMETRO: `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md` (nuevo) · tablero · gobernanza · estado · nota · encargo. NO toca la ficha vieja ni el bloque append-only.

---

## Lo que este acto hizo, verificado contra el propio encargo

1. **La spec** (`hitoD-R10_1-spec-v2_0-PROPUESTA.md`) cubre las cuatro piezas de `FP-108` en §2–§5, reproduce la escala completa con el bloque `B-bis` y su precedencia en §6, fija universo/unidad y la condición exacta de `C` en el mismo §6, y declara los cuatro insumos con veredicto `A.4` en §7 (dos `EXISTE`, uno `NO-ACCESIBLE` heredado, uno `POR-ASIGNAR` — sin adivinar disponibilidad del segundo codificador, que es decisión de mesa/dirección, no un hecho de corpus).
2. **Tablero:** `FP-128` nueva, `ABIERTA`, cita el archivo nuevo en `dónde` (satisface T22(b): el marcador de decisión de mesa que trae la spec queda cubierto por esta fila).
3. **Gobernanza:** `ADR-159` en `canon/gobernanza-v1_15.md` registra el acto (ver más abajo por la colisión de numeración verificada al redactar).
4. **Estado:** `canon/estado-programa-v1_10.md` no requiere recifrado de contador de Hito D — este acto no adjudica ninguna ficha ni mueve `18 de 27`; se limita a anotar la nueva `FP-128` en la línea de WARN de T22 si el conteo de `tests/check.py` lo refleja al cerrar.
5. **Nota:** `forense/notas/2026-08-25-r10-1-spec-v2-propuesta-cierre.md`.

No se tocó `hitoD-R10_1-especificacion-v1_0.md`, `hitoD-R10_1-veredicto-v1_0.md`, `hitoD-R10_1-defecto-spec-v1_0.md` ni el bloque append-only de `hitoD-preregistro-v2_0.md`.
