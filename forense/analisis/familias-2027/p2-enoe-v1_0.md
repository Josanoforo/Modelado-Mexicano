# P2 · ENOE-INFORMALIDAD · singleton y consulta a INEGI · v1.0

Acto: GEN2-ASTRA-CONTINUIDAD-C2-1 · pieza P2 · HEAD de redacción `ba6ccd23` · entorno nube (sin data/raw; no se abrió microdato).
Contadores movidos por este trabajo: cero.

## 1 · Reproducción del conteo singleton

EJECUTADO: `python3 forense/analisis/familias-2027/reproduce_singleton_enoe.py` (stdlib, solo lectura). Salida cruda:

```
artefacto: forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json
sha256 calculado: 3493f3a82dad3642e30b20b4806bf47d3665aaf3d7498ff5d14e5f5ddce0851a
sha256 registrado: 3493f3a82dad3642e30b20b4806bf47d3665aaf3d7498ff5d14e5f5ddce0851a -> COINCIDE
id oro: enoe_2024_4t_microdatos · archivo_sha256 oro: 817f28d20a43fa4fed08195e62df58bf320b31c323a3049fe09b5194a1677305
grupo 1: singleton=39 (lista) · estratos=1210
grupo 2: singleton=39 (lista) · estratos=1210
union=39 interseccion=39 suma_sin_deduplicar=78
singleton_union declarado=39 -> COINCIDE
singleton_detalle upm_todas==1: 39 · igual a union: True
marcos (filtrados, informativo): {'todas': 39, 'entrevistadas': 39, 'edad': 39, 'ocupados': 40, 'SEX1': 41, 'SEX2': 61}
VEREDICTO: REPRODUCE
```

- EJECUTADO: los dos grupos (SEX 1 y 2) listan los mismos 39 códigos EST_D_TRI; unión = intersección = 39; «78» solo sale sumando sin deduplicar.
- EJECUTADO: el sha del artefacto coincide con `enoe-producto.sha256` (línea de `diagnostico/enoe-auditoria.json`).
- LEÍDO (`diagnostico/diagnostico.md`, tabla de marcos): los marcos filtrados SEX1/SEX2 dan 41/61 porque el filtro de dominio elimina UPM de contribución cero; el lector histórico las conserva, por eso el conteo que gobierna es 39. El script lo imprime como informativo, no lo adjudica.

**Límite de procedencia (obligatorio).** Derivado del artefacto `forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json`, no del diseño muestral; el diseño (microdato `ENOE_SDEMT424.csv`, id `enoe_2024_4t_microdatos`) no está en el corpus de esta sesión. Es una verificación de coherencia interna del agregado, no una re-medición independiente.

**Receta para CAJA (≈1 minuto, re-medición desde el diseño):**
```
python3 tools/familias-2027/enoe_inferencia_1/enoe_diagnostico.py \
  --oro data/raw/enoe_microdatos_post2019/enoe_2024_trim4_csv.zip \
  --salida /tmp/enoe-auditoria-recalc.json
sha256sum data/raw/enoe_microdatos_post2019/enoe_2024_trim4_csv.zip   # debe dar 817f28d2…7305
jq '.singleton_union, (.grupos|map_values(.singleton|length))' /tmp/enoe-auditoria-recalc.json
python3 forense/analisis/familias-2027/reproduce_singleton_enoe.py     # sobre el artefacto commiteado
```
(LEÍDO: comando de reproducción en `diagnostico/diagnostico.md`, último párrafo. Para validación independiente E.2, contar `EST_D_TRI` con un solo `UPM` distinto por `ENT+EST_D_TRI` en todas las filas del SDEM sin leer ese código.)

## 2 · Veredicto

**NO-LANZAR-TODAVIA** (ENOE-INFORMALIDAD, 2027T4). LEÍDO: `enoe-hoja-decision.md` §1 y `frontera-disposiciones.json` (motivo «39 estratos singleton sin regla de inferencia acreditada»).

Razón: en los 39 estratos con m=1 la fórmula oficial de conglomerados últimos m/(m−1) no identifica el componente de varianza; con SE_taylor = null por grupo, la potencia/MDE queda null (no cero) y la regla de decisión exige ambos grupos con SE finita y positiva. Asignar cero, promedio o colapso inventado sería una hipótesis ausente de la documentación, elegida después de ver potencia.

**Alcance del veredicto.** No es veto a toda cifra ENOE: los puntos p0 por sexo (0.5396 / 0.5515, LEÍDO en `enoe-auditoria.json`) se conservan y los pisos ENOE sellados siguen vigentes. El bloqueo es solo sobre inferencia (SE, IC, potencia) de esta familia con este oro y este diseño, hasta que llegue el insumo de diseño.

## 3 · PROPUESTA de consulta a INEGI

> **BORRADOR · NO ENVIADO · no equivale a autorización** (ni de mesa para enviarlo, ni para abrir ola alguna). Mesa decide si se envía y por qué canal.

Asunto: Consulta técnica sobre estimación de varianza en ENOE, cuarto trimestre de 2024 (ENOE_SDEMT424)

Estimado equipo de la Dirección de Encuestas de Hogares / Atención a usuarios de microdatos del INEGI:

Trabajamos con los microdatos públicos de la ENOE correspondientes al cuarto trimestre de 2024 (tabla SDEM, archivo ENOE_SDEMT424.csv) y estimamos proporciones por sexo con el método de conglomerados últimos descrito en la documentación metodológica (linealización de razón con factor m/(m−1) por estrato, usando EST_D_TRI como estrato, UPM como conglomerado y FAC_TRI como factor de expansión).

Al aplicarlo encontramos 39 valores de EST_D_TRI que en el archivo tienen una sola UPM (podemos enviar la lista de códigos). En esos estratos el factor m/(m−1) no está definido. Agradeceríamos nos indicaran:

1. El tratamiento oficial para estimar la varianza en estratos con una sola UPM en esta ola: si se trata de unidades de inclusión forzosa (certeza), el indicador y las probabilidades de inclusión de primera etapa y cómo se trata la variación de etapas posteriores; o, si no lo son, la regla oficial de agrupación o colapso de estratos para varianza, o pesos de réplica compatibles con FAC_TRI.
2. El significado de los códigos UPM que aparecen en más de un estrato (532 en el archivo): si identifican la misma unidad física o unidades distintas, y la llave correcta de conglomerado (por ejemplo ENT + EST_D_TRI + UPM, o su relación con CD_A).
3. Si existe un documento o programa de cálculo (por ejemplo en SAS, Stata o R) que INEGI utilice para los errores estándar publicados de la ENOE y que podamos consultar.

No necesitamos información confidencial ni datos de otras olas; con cualquiera de las rutas del punto 1 es suficiente. Muchas gracias por su atención.

(Redacción basada en LEÍDO: `enoe-hoja-decision.md` §«Insumo específico para decidir» y `diagnostico.md`; conteos 39 y 532 EJECUTADO/LEÍDO de `enoe-auditoria.json` `.singleton_union` y `.colisiones.upm_en_multiples_estratos`.)

## NO-CORRIDO / RESERVAS
- Re-medición del singleton desde el diseño muestral: NO-VERIFICABLE-AQUÍ (microdato ausente en nube); sucesor: receta de §1 en CAJA.
- Envío de la consulta: DECISIÓN-DE-MESA-PENDIENTE.
