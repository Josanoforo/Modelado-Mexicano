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
- **2026-07-30** · El checkout compartido de Ubuntu tiene un origin/main que ninguna sesión refresca: tres ramas del día (PR #17, PR #18, y el chequeo de sesion/encuci) nacieron de fae0191 con main ya en 85c64e2, produciendo diffs con miles de borrados ajenos y una premisa falsa sobre una rama viva. Detectado al comparar git rev-parse contra git ls-remote. No impidió medir.
- **2026-07-30** · La ficha `CAL-G3` se pre-registró sin declarar a qué categorías ocupacionales aplica su instrumento: `TB33` nunca interroga a los códigos 1 y 2 de `tb32p` (campesino en parcela propia, trabajador familiar sin retribución), 730 jefes con cero respuestas. Verificado contra el codebook de la ola 2 al corregir una afirmación previa —mía y de la sesión de chat— que atribuía la exclusión al cuenta propia; esa era falsa: el cuenta propia sí contesta (380 de 773, 49.2%) y es el 15.8% de la muestra analítica. Misma familia que las dos premisas que Fase B tumbó. No impidió medir. Cierra el pendiente que `hitoD-preregistro-v2_0.md` `Nota 10` (k)(1) dejó declarado.
- **2026-07-31** · Reconstruyendo el desglose de los 90 `params_base` desde `milpa/procedencia.yaml` (`resumen.delta_v1_v2`) para cruzarlo contra el catálogo de fuentes: 14 de los 15 parámetros por perfil quedan identificables por nombre (el vector de 6 de `confianza_institucional`, el par `familismo_apoyo`/`familismo_obligacion`, y los 6 restantes ya nombrados en `asignados_coeficiente.detalle`); el 15º no tiene identidad legible en el archivo — se infiere su existencia por aritmética (15×6=90) pero no su nombre. No impidió medir esta sesión (se excluyeron sus 6 números del conteo candidata/sin-candidata, marcados "no derivable").
- **2026-07-31** · El cruce del catálogo de fuentes contra `hitoE-campana-medicion-v2_0.md` §11 emitió SIN CANDIDATA para `horizonte_temporal` teniendo el instrumento nombrado en el mismo bloque que ya se había leído — `milpa/procedencia.yaml`, `asignados_coeficiente.unico_calibrable_hoy` declara `ENOE` como única elasticidad calibrable con dato público, y `ENOE` está en `data/catalogo-fuentes-v1_0.md` como operable sin bajar. Detectado en revisión, no por esta sesión. Corregido en el mismo archivo antes de mergear: 14 filas pasan de 9/5 a 10/4 candidata/sin-candidata, y la cola priorizada se reordena. No impidió avanzar.
