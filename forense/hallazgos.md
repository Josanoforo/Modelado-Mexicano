# Hallazgos · R0

*Abierto el 30 de julio de 2026 por ADR-48. Vacío a propósito.*

**La regla, entera:**

> **Cada sesión produce una medición o produce nada.**
> **Defecto que no impide medir:** una línea aquí, y sigue.
> **Defecto que impide medir:** para y reporta.

Una línea es una línea: fecha, qué se vio, dónde. Sin campos, sin ID
correlativo, sin `casos`, sin estado, sin ADR. Si algo necesita un ID, la
convención es `D-AAAAMMDD-HHMM` o un hash corto — nunca un correlativo
derivado de contar este archivo (ADR-48, cierra I-13).

Lo que había antes de R0 está congelado en
`forense/hallazgos-congelados-2026-07-30.yaml` y no se le añaden entradas.

---

- **2026-07-30** · El paquete de catálogo traía `data/inventarios/README.md`, que colisiona con el `README.md` de la raíz bajo el nombre normalizado de `T02` y ponía la línea base en ROJO. Renombrado a `README-inventarios.md` al aterrizarlo. Impedía medir; se paró, se corrigió y se siguió.
- **2026-07-30** · Este PR mezcla trabajo de instrumento (R0, ADR-48) con trabajo de evidencia (el catálogo de fuentes), contra la prohibición 1 del protocolo. Aceptado por decisión del autor, sin ADR: la prohibición existe para poder atribuir un movimiento de la línea base a un cambio concreto, y aquí la línea base no se movió — 19 FAIL · 84 WARN antes y después, con diez inventarios y un catálogo nuevos. El riesgo que la regla previene no se materializó; separarlos costaba trabajo y no compraba nada medible.
- **2026-07-30** · `data/catalogo-fuentes-v1_0.md` declara "Operables ya en `data/manifiesto.yaml`: 6" y "Operables NO bajadas: 32". Ninguno de los dos scripts los imprime — salen de restar a mano el listado del catálogo contra las 38 operables. Se verificaron por fuera al aterrizar (dan 6 y 32, y los 6 acrónimos están en el manifiesto), pero la receta declarada `catalogo.py && dedup.py` no los reproduce sola. No impide medir. **Cerrado el mismo día:** `tests/dedup.py` deriva ahora el cruce contra `data/manifiesto.yaml` e imprime las dos cifras; corrido en la raíz da 6 y 32, iguales a la tabla, y el catálogo no se regeneró porque no hacía falta.
