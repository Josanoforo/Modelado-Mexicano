# P02 · ENNViH: obtener diseño oficial para cerrar RES-0029/0030

**Compuerta:** `DECISION-REQUERIDA` (titular/envío) y después respuesta externa.  
**Prioridad:** 2: reutiliza un expediente y payloads existentes; el bloqueo es documental, no de microdato.  
**No es:** adquisición de un paquete ni autorización para enviar correo desde este acto.

## 1. Resultado y consumidor

Entregar un CALC reproducible con punto e IC de diseño para:

- `RES-0029` → `milpa/tramite.yaml:dinero.ahorro.tiene_ahorros:tiene_ahorros`.
- `RES-0030` → `milpa/tramite.yaml:dinero.ahorro.tiene_ahorros:no_tiene_ahorros`.

Pregunta: prevalencia de tener/no tener ahorros en ENNViH/MxFLS olas 2–3 bajo el universo ya declarado, sin presentar un IC de sensibilidad como varianza oficial.

## 2. Entradas y disponibilidad

- Manifestados con sha256: `ennvih2_2005_hogar_dta`, `ennvih3_2009_hogar_dta`, `ennvih2_2005_ponderador_transversal`.
- Valor legacy existente: `0.174804/0.825196`; no acredita por sí solo la cadena GEN2.
- Bloqueador exacto: pesos replicados con contrato completo o servicio oficial de varianza para olas 2–3.
- Expediente reutilizable: `forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/03-ENNVIH-DIN-S6.md`, `LISTO-PARA-TITULAR; NO ENVIADO`.
- El texto actual cubre DIN/S6, pero no nombra `RES-0029/0030` ni `G3.horizonte_temporal`.

## 3. Cambio mínimo

Añadir al expediente un párrafo que pida la vía oficial de varianza para esos tres usos del mismo instrumento: `RES-0029`, `RES-0030` y `G3.horizonte_temporal`. El titular decide si envía con identidad real. Al recibir documentación o servicio operativo, congelar una sola spec para `RES-0029/0030`; no abrir ni volver a adquirir los payloads ya manifestados.

**Recomendación:** ampliar y enviar la solicitud existente. Es el mismo contacto y tiene costo marginal de canal casi cero; evita tres solicitudes inconexas. Si la respuesta confirma que no hay vía oficial, mesa decide explícitamente entre punto descriptivo sin IC oficial o mantener los slots sin relevo; no se inventa varianza.

## 4. Perímetro y entorno

Primera etapa: expediente de acceso y comprobante de envío/respuesta, ejecutada por titular. Segunda: prereg/spec y CALC en CAJA, con sólo los miembros ENNViH ya declarados. Dependencias: `NC-0156`; compatible con el piloto y MEDICION-DEMANDA-3. No lee ENIF 2024 localidad×edad, F6, ni resultados del piloto.

## 5. Terminado y secuencia

1. Titular aprueba el párrafo ampliado y envía; se conserva acuse.
2. Se archiva la respuesta/documentación con identidad y fecha.
3. Se verifica que método, pesos, réplicas, cobertura y grados de libertad aplican a olas 2–3 y al universo de hogar/persona usado.
4. Se congela spec antes del cálculo y se ejecuta en CAJA.
5. Verificación mínima: p y complemento comparten denominador, suman 1 al grano publicado, el IC usa el método oficial y el `RESULT` cita payloads/sha256.
6. `relevo_usos.py --json` fija un RESULT exacto para cada slot; no basta declarar la corrida cubierta.

No se presupuesta ninguna llamada a modelo. El único acto externo es la comunicación del titular, que esta ficha propone pero no autoriza ni ejecuta.
