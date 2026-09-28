# Hoja C2 para mesa · v1.1 · 28/sep/2026

De `GEN2-ASTRA6-C2-EJECUCION-1`. Sucede a `hoja-c2-para-mesa-v1_0.md`: B4, E3 y E4 ya se firmaron y se ejecutaron, así que salen de aquí.

## Lo que ya no te toca

Cinco de las ocho familias 2027 quedaron **listas para abrirse cuando INEGI publique su ola 2027**. Ya no esperan ninguna firma tuya: la única espera es el dato. Cuando llegue una ola, el acto de apertura (COMMIT-3) cotejará identidades y correrá una sola vez.

## Lo que sigue esperando una decisión tuya (sin cambio respecto a v1.0; re-verificado en `firmas-pendientes.tsv` el 28/sep)

1. **ENOE-INFORMALIDAD (`FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01`, ABIERTA).** En 39 estratos hay una sola UPM y no se puede calcular error. La familia no se lanza hasta que firmes cómo tratarlos. Texto listo en `forense/analisis/recibo-astra6-3/hoja-para-mesa-recibo-astra6-3.md`.
2. **ENSU-CAMPECHE y frontera (`FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01`, ABIERTA).** Con la banda de ±5 pp la prueba casi no informa. El texto de firma, que no lanza ENSU ni ENOE y conserva los diagnósticos, está en `hoja-c2-para-mesa-v1_0.md` l.23.
3. **ENCIG-PAGO-DIGITAL.** Sigue suspendida por tu firma del 26/sep. Reactivarla exige una enmienda nueva del gate de residuo antes del dato. Nadie la ha redactado: si la quieres, es un encargo.
4. **Tablero C2 (`FP-260928-GEN2-ASTRA-CONTINUIDAD-C2-1-ba6c-01`, ABIERTA).** Si MOCIBA y ENSANUT entran, si ENSU dic/2025 está abierta o reservada, y cómo se declara «consumido» por cruce.
5. **Permisos parciales C1 (`FP-260926-GEN2-ASTRA6-C1-PAQUETES-2-9c9e-01`, ABIERTA).** La v1.0 la heredó como reserva de las dos familias ENIF («ACCESO-AUTORIZADO»). Se conserva, pero no bloquea hasta que llegue ENIF 2027.

## Lo que no es tuyo pero conviene que sepas

- **Atestación externa (`.ots`).** Sigue siendo de mesa (SELLO-EXTERNO-2). Ninguna fila está ATESTIGUADA-EXTERNAMENTE.
- **Hallazgo de proceso.** El encargo pedía COMMIT-1 y COMMIT-2 de las cinco familias, pero ya existían desde el 26/09: lo que bloqueaban B4/E3/E4 era el COMMIT-3. No se selló nada nuevo para no crear un segundo contendiente (regla 6). Tu respuesta del 28/sep («YA-HECHO: verificar») está en la nota del acto.
- **NC `NC-260926-GEN2-RECIBO-ASTRA6-N-996b-03`.** La v1.0 proponía cerrarla con E3. Este acto verificó la identidad de la enmienda ENCIG (4/4 sha contra el inventario), pero no corrió `cierre.py --verifica` de ENCIG sobre el commit fusionado, que es lo que la fila pide. Se deja ABIERTA para el acto de caja post-merge que ella misma nombra.
