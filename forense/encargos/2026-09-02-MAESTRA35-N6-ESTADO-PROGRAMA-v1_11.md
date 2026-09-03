# ENCARGO · ACTO MAESTRA35-N6 · ESTADO-PROGRAMA-v1_11

SHA de redacción: 19770f2 (merge PR #481). Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR. COMPUERTA: ninguna. Un acto de CANON, no de reglas operativas (DE1 no aplica: no revisa reglas, refresca el documento que se declara «ÚNICA FUENTE DE ESTADO»). ENTORNO ASIGNADO: NUBE (`cloud_default`, repo-only). NO en UBUNTU. MODELO SUGERIDO: Opus (síntesis con lectura; nada se mide).

## Carriles

N5 (nube: cascada toca `estado-programa` L0 — re-aplica quien fusiona segundo; esperado: este acto fusiona DESPUÉS de N5 y de #480) · L4/L7/L8/A1 (caja: sus cascadas tocan L0). Este acto crea `canon/estado-programa-v1_11.md` y deja v1_10 como historia (política del programa: una versión viva por artefacto; `tests/check.py` T15/T20 leen la ruta — verifica qué tests citan `estado-programa-v1_10.md` con `grep -rn "estado-programa-v1_10" tests/ .claude/ canon/` y actualiza las citas en la MISMA cascada, o PARA si el conteo excede 15 sitios y repórtalo).

## Firmas de mesa — verbatim

El ejecutor propaga, no decide (SELLA-3).

* Mesa, 2/sep/2026: «necesito que hagas un tablero completo del avance del programa … creo que estamos listos para ese mapa» y «vamos con todo». El tablero (TABLERO-PROGRAMA-v1_0, §7 D1) encontró que `canon/estado-programa-v1_10.md` (fecha 4/ago) describe la era Hito D en §3 L1–L5, §4 y §7 y sólo L0 vive por cascada. Este acto es P8 del tablero.
* Regla de oro (v2): «Toda síntesis se construye leyendo, no recordando.» Cada afirmación de estado trae comando o cita de archivo:línea; ninguna cifra tecleada (v2.1); vocabulario A.4; estampa A.10 en la cabecera (SHA).
* Firma final: el archivo v1_11 queda `PROPUESTA — firma de mesa pendiente` en su cabecera hasta que mesa fusione; la fusión es la firma (regla 1 de maestra-34).

## Verificación de existencia (A.8) — contestada por dirección contra 19770f2

**(1) Estructura.** `canon/estado-programa-v1_10.md`: §0 nomenclatura (ADR-36) · §1 inventario verificado · §2 el estado en una frase · §3 estratos L0–L5 · §4 deudas S1–S5 + huecos de dato · §5 reglas que no se negocian · §6 trampas · §7 qué sigue. L0 recifrado por cascada (`T15`); T20 lee Hito D. Fuentes derivables: `tools/tablero_programa.py` (si N7 lo fusionó; si no, la columna «comando» del tablero), ADR 265–298, `milpa/tramite.yaml`, `forense/prereg-duelo-v2/`, `data/manifiesto.yaml`.

**(2) Contenido.** `grep -n "Hito D\|MILPA Fase 0\|3 de 10" canon/estado-programa-v1_10.md` → §3 L4 dice «MILPA Fase 0: 3 de 10 rules/*.yaml», L5 «Hito D … el estrato más problemático», §7 «HITO D — falsación sistemática». `grep -c "corredor\|Ola 5\|sorteado\|scoreboard" canon/estado-programa-v1_10.md` → contar y pegar (esperado ≈0 fuera de L0). → EXISTE-NO-SATISFACE.

**(3) Cobertura retroactiva.** v1_10 nace 4/ago; todo lo que describe mal es posterior; cubierto.

## Piezas

**P1 · v1_11**, sección por sección, conservando la estructura y el §0/§5/§6 casi íntegros (cámbialos sólo donde el árbol los contradiga, con cita):

* §2 · el estado en una frase, reescrito: motor de 10 reglas con 9 medidas y 1 sin dato (universo declarado); corredor v1_2 con L∩M∩R = N (deriva), Ola 6 no abierta (ADR-265) con N5 en cola; 1 040 payloads; instrucciones v2.12.
* §3 · L1 evidencia (31 + 6, sin cambio salvo conteo) · L2 síntesis (glosario v5_6, integrador) · L3 modelo (49 reglas, modelo-decision v4_0; 10 en el motor: lista) · L4 implementación: MILPA con `tramite.yaml` (10 reglas, 25+ conductas MEDIDO, enmiendas `_encig2025`, `_r2`, `_enif2024`, `_envipe2025`, `segmentacion_ejes_*`), `procedencia.yaml` (7 coeficientes sellados, 13 asignados con veredictos), emisor/motor en `milpa/src/`; el corredor M/L vs R (marco v1_2 34/14, R/M/L por comando, scoreboards) · L5 validación: Hito D como historia (26 de 27, T20) y el duelo como validación vigente; mediciones propias desde 4/ago (lista con ADR); refutaciones por dato (mordida, concurrencia electoral) · L0 por cascada (no lo toques a mano: T15).
* §4 · deudas: S1 «cero datos primarios propios» → RESUELTA (fecha y ADR de la primera medición); las S2/S3 que siguen abiertas se conservan verbatim con su casillero; se añaden las de hoy con dueño y FP: S1 tablero (coercitivo, universo declarado), dominio dinero (DIN-M-01 puntuable con reserva), FP-179/233/235/240, contaminación de sesión ciega (mitigada), numeración con ≥2 PR abiertos.
* §7 · qué sigue: la señal del tablero (S1–S7), N5·RE-EVALUA-OLA6 con criterios explícitos (firma 9), cívica L8, reglas activas L7, v2.13, y lo que es de mesa.

Cada cifra con su comando en comentario HTML (mismo patrón que README «Estado del modelo»).

**P2 · Cascada:** renombrar citas de `estado-programa-v1_10` → `v1_11` donde los tests y skills la lean (lista con conteo), correr `tests/check.py --baseline`: VERDE o PARO-reporta. v1_10 NO se borra (historia).

**P3 · Nota de cierre** con la tabla «afirmación de estado → comando/cita» completa, y lo que NO pudo derivarse (`NO-DERIVADO (razón)`), sin estimaciones.

## Perímetro y concurrencia

`canon/estado-programa-v1_11.md` (nuevo) · citas a la ruta en `tests/`, `.claude/commands/`, `canon/gobernanza-v1_15.md` cabecera, `README.md` (orden de lectura) · `forense/notas/` · `forense/hallazgos.md` · tablero · A.3 · cascada. NO toca `milpa/`, `data/`, `corridas-*`, `instrucciones-proyecto-*`, ni el cuerpo de `gobernanza`. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

## FP/ADR candidatos

Una fila (recibo: v1_11 propuesta, firma = fusión); primer libre al arrancar.

## Contador

Cero directo, declarado — canon de estado al día; ningún número del programa se mueve.

## Lo que este acto NO hace

No mide; no decide qué sigue (lo transcribe del tablero y de las firmas); no edita instrucciones ni gobernanza; no toca el tablero (es vista derivada, vive en N7).
