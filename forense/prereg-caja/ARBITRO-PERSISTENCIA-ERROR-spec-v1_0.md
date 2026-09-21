# ADJUDICACIÓN DE LA PERSISTENCIA · piso t-1 vs realidad GEN2 · 57 celdas marginales · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-ARBITRO-MARGINALES-1 · pieza 3 (21/sep/2026, CAJA). CALC:
`CALC-ARBITRO-PERSISTENCIA-ERROR-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-ARBITRO-MARGINALES-1.md`. **Rotulada
PROSPECTIVA:** cada piso (`CALC-PISOS-ENIF2021-EJES-0003`, `…-FORMALIDAD-0001`,
`…-ENVIPE2024-EJES-0002`, `…-ENCIG2023-EJES-0002`) se selló el 19-20/sep/2026,
antes de que GEN2 midiera R (`CALC-ARBITRO-MARGINALES-ENIF2024-0001`,
`…-ENVIPE2025-0001`, `…-ENCIG2025-0001`, 21/sep/2026).

## 1 · Qué estima (primera línea: universo, unidad, escala)

**Universo:** las 57 celdas marginales de `ARBITRO-MARGINALES-metadatos-v1_0.tsv`
(las `SOLO-PISO` del marcador en `55c8d57c`: ENIF 2024 ×32, ENVIPE 2025 ×15,
ENCIG 2025 ×10), cada una con piso y R sellados y enlazados 1:1 por `cell_id`.
**Unidad:** la de cada celda (persona / delito / trámite), que nunca se
mezcla entre encuestas. **Escala:** puntos porcentuales (d) y proporciones
(coberturas).

**Estimando, por celda:** `d = (R − piso)·100` pp; IC95 de d por simetría
normal desde los dos IC95 sellados, olas independientes
(`ee = (sup − inf)/(2·1.959964)`, `ee_d = sqrt(ee_R² + ee_piso²)`; misma
receta que `CALC-PISO-PERSISTENCIA-ERROR-0001`, con las mismas pérdidas
declaradas: asimetría del bootstrap y correlación por marco compartido);
`CLASE` = PERSISTE si el IC de d incluye 0, CAMBIA si lo excluye;
`R-EN-IC-PISO` = DENTRO si el punto R cae en el IC95 del piso, FUERA si no
(la **cobertura** que pide el encargo §1).
**Por encuesta, por encuesta×desenlace y por encuesta×eje** (nunca entre
encuestas): N, error medio con signo, MAE, máx |d|, N-DENTRO, cobertura =
N-DENTRO/N con IC95 binomial de Wilson, N-PERSISTE, N-CAMBIA.

**Hallazgo sobre GEN1 (no corrección):** por celda, `p` del árbitro GEN1
(`milpa/tramite-ola5-propuesta-v0.yaml`, sha `93dfa3f9…`, misma celda por
`MARG::…` del marcador) y `R − p_GEN1`, cotejo COINCIDE (|Δ| ≤ 5e-7, el
redondeo a 6 decimales del yaml) / DISCREPA; por grupo, N-COINCIDE y máx |Δ|.

**Cita de lo ya sellado en la ola nueva (no re-medición):** 28 celdas de
ENIF 2024 (`CALC-C2-COMPUESTO-IC-ENIF2024-0001`, `…-G-MARG-*`) y 8 de
ENCIG 2025 (`CALC-GOB-DIGITAL-EXE-EMISIONES-0002`, `…-2025-MARGINAL-{EDAD,ESC}-*`):
`R − sellado`, máx |Δ| en los límites del IC, cotejo COINCIDE (≤ 1e-6) /
COINCIDE-1E-3 (≤ 1e-3) / DISCREPA, con el id citado. Mapa explícito de ids
en el medidor (`MAPA_C2IC_*`, `MAPA_GOB_EJE`), cada lado por su archivo.
ENVIPE 2025 no tiene marginal sellado con `P` por piloto (el C2-IC de
ENVIPE sólo selló deltas de control): no se cita nada.

## 0 · Exposición declarada

Todos los insumos son RESULT sellados o tablas versionadas, leídos por
sha256; ningún microdato. Esta sesión midió los tres R y vio sus valores
antes de congelar esta spec: lo que congela es la aritmética, no una
cifra esperada. Umbrales (5e-7, 1e-6, 1e-3, z95) fijados aquí antes de
correr; no se ajustan.

## 2 · Nulos y ramas

Ninguna: toda celda enlazada tiene piso y R con punto e IC finitos (los tres
R sellaron con 0 null; los pisos, con `B-VALIDAS = 10 000`). Si un lado
faltara, `medir()` falla con `KeyError` y la corrida no sella (PARO f: se
diagnostica, no se parcha). Determinista: `seed.aplica = false`; tolerancia
flotante 1e-10.

## 3 · B-bis, escrito antes de correr

Por encuesta: si la mayoría de celdas `PERSISTE` y la cobertura ≥ 0.5 con
IC que no excluye 0.95, la persistencia t-1 queda corroborada como piso a
esa brecha (los retadores tienen poco margen). Si la mayoría `CAMBIA` o la
cobertura excluye 0.5 por abajo, el piso es débil a esa brecha: ahí un
retador rinde. Si ambas lecturas caben por eje, manda la lectura por eje y
se dice al cerrar. ENCIG (brecha 2 años, unidad trámite) ya mostró 0/10
persistentes contra el R GEN1: aquí se vuelve a leer con R GEN2, sin
promediar con ENIF (3 años, persona) ni ENVIPE (1 año, delito).

## 4 · Lo que NO hace

No corrige el yaml GEN1 · no adopta · no compara contra el MAE de C2 en
cruces (otro estimando) · no toca `CALC-PISO-PERSISTENCIA-ERROR-0001`
(queda como la lectura contra GEN1; ésta es la lectura contra GEN2).
