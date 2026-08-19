# `ACTO CORTE-EDAD-CONVENCION` — 19/ago/2026

Sesión NUBE, repo-only, no toca microdato. Ejecuta la mitad (c)-convención de la firma D-2 de `MESA-19AGO` (`ADR-110(b)`, fila `FP-53`). Base: `35c9c9f` (`origin/main`, `PR #278`/`LIMPIA-CAJA` ya fusionado).

## 1 · Re-derivación de los nueve sitios (no heredados del encargo)

```
grep -niE "corte PENDIENTE|Corte de .?edad.? PENDIENTE" canon/modelo-decision-v4_0.md
```

Contra `35c9c9f`: `:189` (descriptor 5) · `:215` (H-02) · `:219` (H-06) · `:220` (H-07) · `:355` (R1.4) · `:357` (R2.4) · `:361` (R5.4) · `:457` (regla operativa R2.4) · `:482` (regla operativa R5.4). Idénticos a los nueve que `FP-53` ya había derivado y validado (control positivo 9/9, control negativo contra `FP-02` — cero coincidencias con "cortes iniciales").

## 2 · Procedencia citada (ninguna vivía en el árbol antes de este acto)

- INEGI, *Panorámica de la población joven por condición de actividad* (ENOE) — corte oficial adoptado, 15-29 años: <https://www.inegi.org.mx/investigacion/pobjoven/>, consultado 19/ago/2026.
- Ley del Instituto Mexicano de la Juventud, art. 2 (DOF 06/ene/1999, reformas 02/abr/2015) — alterno declarado, no adoptado, 12-29 años: <https://www.diputados.gob.mx/LeyesBiblio/pdf/LIMJ.pdf>, consultado 19/ago/2026.

Ambas verificadas por búsqueda web en el momento de ejecutar (no de memoria, per la prohibición general de generar URLs sin verificar).

## 3 · Sustitución y re-conteo

Los nueve sitios se sustituyeron literalmente: la condición que el `SI`/la fila ya enunciaba ("joven urbano", "urbano-joven-conectado") no cambia, solo el corte que faltaba. Re-conteo, mismo comando que §1:

```
grep -niE "corte PENDIENTE|Corte de .?edad.? PENDIENTE" canon/modelo-decision-v4_0.md
```

→ **0 resultados.** El número honesto es el derivado, no el esperado.

## 4 · Qué desbloquea, sin re-adjudicar veredicto

- **Descriptor 5**: "Región definible", sin excepción de corte.
- **H-02**: pierde el bloqueo de corte; conserva su tier `[HIPÓTESIS]` (proxy nunca tuvo dato mexicano citado — razón ajena al corte).
- **H-06**: sigue `NO DETERMINABLE EN ESTE RÉGIMEN`, ahora por una sola razón (`sens_estatus` sin reactivo, búsqueda cerrada por límite de régimen — §1.1.F Paso 5), no por dos.
- **H-07**: conserva `forma PENDIENTE` — razón funcional (Latinobarómetro `P4NOIJ`, C-bis), no del corte de edad, que ya no la bloquea.
- **`R1.4`/`R2.4`/`R5.4`** (§1.6) y las dos reglas operativas de `R2.4`/`R5.4` (§3.2/§3.5): disparables sobre el atributo `edad` ya cortado, sin cambio de predicción — misma disciplina que las diez reglas traducidas de §1.6.

## 5 · Convención, no verdad final

`modelo §1.1.A` trae el aviso completo: `CORTE-EDAD-EMPIRICO` (acto gemelo, en cola, UBUNTU, dato mexicano propio) puede corregir este corte y su alcance puede vencer al de esta convención — mismo principio que la estampa de universo (`ADR-67(b)`/`ADR-78(e)`, `A.10`). `P1` no verificó partición canónica de `edad` en la semilla ENIGH (`modelo §1.1.F` Paso 3) y esa afirmación no cambia: el corte es una regla externa aplicada sobre la variable ya inventariada, no una partición descubierta en el microdato.

## 6 · Perímetro

No toca `milpa/*.yaml` ni `data/`. No re-adjudica ninguna hipótesis o regla — cambia estatus de determinabilidad, no veredicto. No abre fila de tablero nueva (`FP-61`): no se encontró colisión de id ni deuda nueva que la requiera. `FP-53` (`FIRMADA`) se actualiza en `ejecutada_en` para reflejar que solo su mitad-convención quedó ejecutada aquí; sigue `FIRMADA`, no `CERRADA`, hasta que `CORTE-EDAD-EMPIRICO` corra.

Cascada de ADR: candidato **114** al escribir contra `35c9c9f` (113 únicos, máximo 113, sin huecos). Primera colisión al fusionar `origin/main` (`318e233`): `PR #279`/`FP57-DECLARA` también candidateó `114` y llegó primero. Renumerado a `115`. Segunda colisión al re-fusionar `origin/main` (`976b31d`): `PR #282`/`FP10-PRECEDENCIA` también candidateó `115` y llegó primero. Renumerado a **`ADR-116`** — `ADR-114`/`ADR-115` ajenos quedan intactos — mismo protocolo que trece ADR previos de esta semana.

Contadores de medición sobre México movidos: **0**.
