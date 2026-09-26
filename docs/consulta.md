---
title: Contrato de consulta
---

# Contrato de consulta · v1.0

[Portada]({{ '/' | relative_url }}) · [Consultar]({{ '/consultar.html' | relative_url }}) · [Ejemplos]({{ '/ejemplos.html' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }}) · [Reto público]({{ '/reto.html' | relative_url }})

Acto `GEN2-PRODUCTO-CONSULTA-1` (26/sep/2026). Este texto es la spec humana (D-15): basta para reimplementar la consulta sin leer `tools/benchmark.py`. Si no basta, ése es el hallazgo.

**Qué es.** Una pregunta «¿cuánto X en el segmento S?» y una respuesta citable: el **piso** adoptado que el catálogo vigente publica para esa conducta y ese segmento, con su intervalo, su unidad, su ola, su origen y la cadena `RESULT → CALC → sello` para verificarlo. La consulta **no recomienda retadores, no predice y no promete cambios entre olas** (firma D2; regla 6): devuelve pisos. Donde no hay piso, dice por qué.

## 1 · Fuente única: el catálogo vigente por puntero

- La consulta lee **solo** la tabla del catálogo vigente: `canon/catalogo-del-mexicano-v1_N.tsv` con el `N` mayor presente en el árbol (hoy `v1_1`, 36 143 filas <!-- deriva: python3 tools/benchmark.py puntero -->). Cuando otro acto publique `v1_2`, la consulta la toma sin editar código; el `N` viaja en toda salida (`catalogo`).
- Cada cifra devuelta es una fila del catálogo y **debe ser idéntica** al valor del `RESULT` sellado que cita, leído de `data/corrida0/<calc>/resultados.json` tras verificar `sello.sha256 → sello.json → resultados.json`. Regla de localización: si `celda` es un entero `i`, el valor es el registro `i` de la tabla sellada `resultados[result_id]` (campo `punto`, o `p` en ENDIREH; IC en `ic95_lo/ic95_hi` o `ic95[0..1]`); si no, es `resultados[result_id]`. Una fila que no reproduce su RESULT no se devuelve (PARO c del encargo); el test de equivalencia la busca sobre **todo** el catálogo.
- Ninguna otra tabla aporta cifras. Las tablas auxiliares solo aportan texto: hashes (`forense/analisis/catalogo/v1_1/calcs.tsv`), exclusiones (`…/excluidos.tsv`), cobertura de dominios (`…/cobertura-31.tsv`), reglas SI-ENTONCES (`milpa/tramite.yaml`), olas reservadas (ids de `data/manifiesto.yaml` con `estado_reserva: RESERVADA*`; se leen ids, nunca payloads).

## 2 · Entrada

| campo | obligatorio | forma |
|---|---|---|
| `conducta` | sí (uno de los dos) | id exacto del catálogo (columna `conducta`, p. ej. `actividad_mensajes`) |
| `texto` | sí (uno de los dos) | palabras; casan si **todas** aparecen (sin acentos ni mayúsculas) en `conducta`, `dominio`, `instrumento` o `llave` |
| `segmento` | no | `eje=valor`, repetible. `eje` ∈ {`sexo`, `edad`, `escolaridad`, `localidad`, `formalidad`, `region`, `nse`, `nacional`}; `valor` se compara sin acentos ni mayúsculas contra la columna `segmento`: **exacto** si algún segmento de esa familia de eje es igual al valor; si ninguno lo es, por subcadena (enmienda v1.0-a del mismo acto, antes de fusionar: `superior` casaba también `media_superior`) |
| `instrumento` | no | p. ej. `ENIF` (exacto, sin mayúsculas) |
| `ola` | no | p. ej. `2024` (exacto) |

Familias de eje (la columna `eje` del catálogo trae la grafía de cada CALC; la consulta las agrupa y **no** reinterpreta categorías):

| eje de la consulta | columnas `eje` del catálogo |
|---|---|
| `sexo` | `sexo`, `SEXO` |
| `edad` | `edad`, `EDAD` |
| `escolaridad` | `escolaridad`, `ESCOLARIDAD`, `ESC`, `escolaridad_proxy` |
| `localidad` | `localidad`, `TLOC`, `ESTRATO`, `dominio_urbano_rural` |
| `formalidad` | `formalidad` (seguridad social). `cuenta_formal` es inclusión financiera y se pide como `formalidad=cuenta` |
| `region` | `entidad`, `ENT` (entidad federativa). Las regiones del eje regional v1.0 no están adoptadas: no se contestan |
| `nse` | `NSE` (aproximación rotulada, con reserva de instrumento) |
| `nacional` | `nacional`, `TOTAL` |

## 3 · Salida — una respuesta por fila del catálogo que casa

| campo | contenido |
|---|---|
| `llave` | llave del catálogo |
| `conducta`, `dominio`, `instrumento`, `ola` | de la fila |
| `eje`, `segmento` | de la fila, sin recodificar |
| `punto` | del catálogo = del RESULT sellado (§1) |
| `ic95` | `[inf, sup]` o `null` si no identificado (vacío **no** es cero) |
| `tipo_ic` | `diseno` (IC95 de diseño o bootstrap UPM) · `calibrado` (IC de persistencia; ancho a propósito, no se llama cobertura) · `ic-con-r` (IC de la spec sin calibración contra R, o muestral de la ola t−1) · `sin-ic` — y `naturaleza_ic` verbatim |
| `unidad` | verbatim; una cifra de unidad delito o trámite no se compara con una de unidad persona u hogar |
| `temporalidad` | `PROSPECTIVA` o `RETROSPECTIVA` (hoy todo el catálogo es RETROSPECTIVA) |
| `origen_piso` | `NUEVO` o `HEREDADO-DE-GEN2` |
| `estado_adopcion`, `alcance`, `firma` | de la fila (`firma_fp`) |
| `result`, `celda`, `calc` | la cita |
| `sha256_resultados`, `sha256_sello` | de `calcs.tsv`; la consulta los re-verifica contra el disco |
| `oferta` | columna de oferta: medida de exclusión por oferta o su ausencia declarada (§3 de las instrucciones: oferta antes que preferencia) |
| `regla` | si la fila es `PARAMETRO-DE-REGLA` y la regla está en `milpa/tramite.yaml`: `id`, `tier`, `falsable_si`; si no, `null` |
| `reserva` | verbatim |
| `terminos` | «Términos: uso no comercial libre con atribución; uso comercial por acuerdo; contacto = correo de CITATION.cff.» (F-FRONT-2) |

Envoltura: `{catalogo, consulta, n, respuestas[], no_contesta[], terminos}`. La salida humana muestra lo mismo en texto.

## 4 · Qué no puede contestar — `no_contesta`

Si ninguna fila casa, o además de las que casan, la consulta declara con vocabulario cerrado:

| razón | cuándo |
|---|---|
| `SEGMENTO-NO-ESTIMABLE` | la conducta existe pero hay celdas excluidas del catálogo por `CELDA-SUPRIMIDA*` / `CELDA-NO-ESTIMABLE*` (n insuficiente) — se cita la causa de `excluidos.tsv` |
| `FUERA-POR-REGLA` | celdas excluidas por firma, legacy, NSE fuera de reserva o marginal no adoptada — causa verbatim |
| `DOMINIO-NO-MEDIDO` | el texto casa con un dominio de `cobertura-31.tsv` cuyo estado no es `MEDIDO` |
| `OLA-RESERVADA` | `instrumento`+`ola` pedidos corresponden a un payload `RESERVADA*` del manifiesto: la ola no se abre ni se consulta |
| `EJE-NO-DISPONIBLE` | el eje pedido no está en la tabla de §2 (p. ej. región del eje regional, religiosidad, migración) |
| `SIN-COINCIDENCIA` | nada casa y ninguna de las anteriores aplica: nadie midió esto en el catálogo vigente (no «no existe»: el universo es el catálogo `v1_N`) |

## 5 · Verificación — `verificar <llave|RESULT>`

Reproduce la cadena hasta el sello sin abrir microdato: (1) `sha256(sello.json)` = `sello.sha256`; (2) `sello.json["resultados.json"]` = `sha256(resultados.json)`; (3) valor localizado por §1 = `punto` del catálogo; (4) hashes = `calcs.tsv`; (5) `spec.yaml` y `ejecucion.json` presentes. Veredicto: `CADENA-VERIFICADA` o `CADENA-ROTA:<paso>`. No recalcula el estimando (para eso: `python3 tools/corrida0.py verify <CALC>`, que necesita el corpus).

## 6 · Formas de acceso

- **CLI:** `python3 tools/benchmark.py consulta --conducta … | --texto … [--segmento eje=valor] [--instrumento …] [--ola …] [--json] [--limite N]`; `python3 tools/benchmark.py verificar <llave>`; `python3 tools/benchmark.py exporta` (deriva el JSON de Pages); `python3 tools/benchmark.py puntero`.
- **Página estática:** [Consultar]({{ '/consultar.html' | relative_url }}) carga `docs/data/catalogo-v1_N.json` (derivado por `exporta`; no se edita a mano) y aplica este mismo contrato del lado del cliente, sin servidor ni dependencias externas.

## 7 · Lo que el contrato no hace

No sirve API (D-14). No devuelve retadores ni la matriz. No promete lo que INEGI no preguntó. No promedia filas: si varias casan, devuelve todas.
