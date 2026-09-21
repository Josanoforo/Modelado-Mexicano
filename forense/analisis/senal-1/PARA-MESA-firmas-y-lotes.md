# NC abiertas: qué firma desbloquea qué, y qué lotes proponemos

**ACTO GEN2-SENAL-1 · P2 · 2026-09-21 · SHA de derivación `dcbb140`**

Derivado de `forense/analisis/senal-1/nc-abiertas-por-clase.tsv`, que a su vez se
deriva de `forense/no-corrido.tsv` y `forense/firmas-pendientes.tsv`. Cero cifras
tecleadas. **Universo: 159 filas ABIERTA de 418** (155 tras los dos cierres, más los 4 asientos A.14 de este acto).

Este acto **no redacta encargos** y **no cierra ninguna NC que espere firma**.

---

## 1 · Lo primero, porque cambia cómo se lee todo lo demás

El campo `sucesor` de `no-corrido.tsv` **no predice si la deuda está pagada.**

El clasificador marcó 18 filas como `SUCESOR-YA-FUSIONADO` leyendo ese campo.
Las verificamos **por producto, una por una**: *cero* resistieron. Las dos que sí
se pudieron cerrar estaban clasificadas en otra clase. La suposición con la que
salió el encargo —«una parte ya tiene su sucesor fusionado y nadie volvió a
cerrarlas»— resulta ser **casi enteramente falsa**, y eso es el entregable.

La razón, cuando se mira de cerca, es sistemática: la mayoría de esos sucesores
son *decisiones de mesa*, no trabajo de ejecución. Un PR que fusiona no toma una
decisión. Por eso fusionar no cierra la fila.

**Cerradas en este acto: 2.** `no_corrido_abiertas` **157 → 155 → 159**. Los dos tramos son de naturaleza distinta y no se colapsan: **−2 por los dos cierres verificados por producto** (NC-0379, NC-0390), que es el único movimiento que el encargo autoriza; **+4 por los asientos que A.14 obliga** (NC-0423..NC-0426), que no son deuda nueva descubierta sino las reservas de este mismo acto puestas por escrito. El neto sube, y se declara: el encargo previó que la cifra sólo bajara, y no contempló que cerrar un acto con reservas la suba por regla. **No es PARO** (la lista cerrada del §7 veda que cambien los otros contadores, y A.14 no es opcional); se declara para que mesa decida si quiere que el contador distinga asiento de deuda.
Ningún otro contador se movió.

| NC | Qué pedía | Producto verificado |
|---|---|---|
| NC-0379 | que `tests/test_pisos_enut2019.py` corriera en CI | el test existe, corre solo con exit 0, y el job `guardias` (PR #917) lo ejecuta — su fila en el censo da `CORRE-EN-CI` |
| NC-0390 | que `tests/test_c2_ic_envipe2025_guardia.py` corriera en CI | ídem, exit 0, censo `CORRE-EN-CI`, sin dependencia pendiente |

**Su gemela NO se cerró, y la diferencia importa.** NC-0381 pide lo mismo para
`tests/test_c2_ic_enif2024_guardia.py`. Ese test **sigue sin correr en CI**: el
job lo descubre pero lo **salta en voz alta** porque necesita `numpy`, y `numpy`
no está en `requirements.txt` (NC-0332, abierta). El PR fusionó; el producto no
existe. **Decisión que pedimos a mesa:** ¿se añade `numpy` a `requirements.txt`?
Es una línea, y desbloquea NC-0381, NC-0332 y parte de NC-0331 de una vez.

---

## 2 · Las 14 que esperan firma — qué desbloquea cada una

Ordenadas por cuántas filas destraba cada firma.

| Firma | Estado hoy | NC que destraba | Qué desbloquea, en llano |
|---|---|---|---|
| **FP-374** | ⚠️ **VENCIDA-EN-ALCANCE** | NC-0161, NC-0162, NC-0234, NC-0237 | **No es una firma pendiente: es un sello cuyo universo creció (A.10).** No se firma — se **re-sella**. Mientras tanto estas cuatro no tienen a quién esperar. Es la única fila de esta tabla que pide una acción distinta de firmar. |
| **FP-394** | ABIERTA | NC-0369, NC-0370, NC-0372 | Limpieza de ramas ajenas y el contador de 12–13 corridas que ya reproducen. Es higiene del repo más una firma de contador: barato y destraba tres. |
| **FP-395** | ABIERTA | NC-0380, NC-0383 | Bajo qué rótulo entra el IC ya sellado de ENIF 2024 al marcador, y si esa corrida cuenta. Hoy 136 emisiones tienen el IC calculado y guardado, y el marcador no lo muestra. |
| **FP-397** | ABIERTA | NC-0387, NC-0388 | Lo mismo para ENVIPE 2025: 38 emisiones con IC sellado que el marcador no publica. Gemela de FP-395; **conviene firmarlas juntas o quedan desalineadas.** |
| **FP-387** | ABIERTA | NC-0344 | `tier` admite un escalar y hace falta más de uno. Decisión de esquema, no de medición. |
| **FP-393** | ABIERTA | NC-0409 | Cómo se registra una celda-D cuya unidad es TRÁMITE. **Gatea el registro de la celda del piloto 3.** |
| **FP-396** | ABIERTA | NC-0385 | El error de persistencia de las 6 celdas de formalidad. **Esta firma tiene consecuencia directa en la métrica rectora:** esas 6 celdas tienen piso pero su error no está medido, así que hoy **no cuentan** como validadas. Firmarla es el camino para que cuenten. |

---

## 3 · Lotes propuestos para las 55 `SIN-ASIGNAR`

D-11: hasta cuatro piezas afines del mismo entorno = un encargo, un PR, un ADR.
**Son propuestas.** Este acto no redacta los encargos.

### Nube — aparato, baratos y desbloqueantes

- **Lote N1 · dependencia de CI que destraba tres deudas** — NC-0381, NC-0412
  (+ NC-0332 y NC-0331, hoy en otras clases). `numpy` a `requirements.txt` y los
  dos pasos de CI que faltan. *Es el lote de mayor razón desbloqueo/costo de toda
  la lista.*
- **Lote N2 · ocho tests que corren y fallan (1/2)** — NC-0396, NC-0397, NC-0398, NC-0399.
  Ya no son huérfanos: el job los detecta y los salta como `FALLA-DE-VERDAD`. Cada
  uno es un contenido roto distinto; conviene no mezclarlos con N3.
- **Lote N3 · ocho tests que corren y fallan (2/2)** — NC-0400, NC-0401, NC-0402, NC-0403.
- **Lote N4 · `corrida0.py` y contadores** — NC-0253, NC-0298, NC-0350, NC-0377.
  Mismo archivo, misma clase de cambio. **Colisiona con PR #928**: lanzar después
  de que fusione.
- **Lote N5 · marcador y celdas-D** — NC-0305, NC-0348, NC-0378, NC-0411.
- **Lote N6 · spec/prereg y motor** — NC-0307, NC-0392, NC-0107, NC-0299.

### Caja — exigen microdato montado

- **Lote C1** — NC-0246, NC-0259, NC-0308, NC-0327.
- **Lote C2** — NC-0374, NC-0375, NC-0376.

### No son lote: son decisiones de mesa

**20 filas** (NC-0033, NC-0037, NC-0038, NC-0039, NC-0164, NC-0213, NC-0217,
NC-0218, NC-0225, NC-0244, NC-0260, NC-0317, NC-0318, NC-0319, NC-0324, NC-0349,
NC-0358, NC-0359, NC-0371, NC-0415) no esperan ejecución: esperan que alguien
decida. Empaquetarlas como encargo no las movería. **Recomendación: una sola
sesión de mesa que las despache en bloque**, o bien aceptar explícitamente que
son reserva declarada y sacarlas del conteo de deuda activa — hoy inflan
`no_corrido_abiertas` en un 13 % sin que exista trabajo que hacer.

### Sin clasificar

**5 filas** (NC-0247, NC-0313, NC-0343, NC-0382, NC-0418) no dan objeto
verificable. Ver la columna `que_le_falta` del TSV.
