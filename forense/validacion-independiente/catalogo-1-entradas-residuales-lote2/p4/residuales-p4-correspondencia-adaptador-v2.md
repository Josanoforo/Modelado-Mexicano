# Correspondencia de salida · contenedores residuales v2 ↔ adaptador #1221

Contrato externo verificado: PR #1221 HEAD `d8ef9f56ef80ec1cd7867779489beb0ce7e4cfe9`, `adaptador.py` SHA-256 `228d2897b0e2a85f3a64c107e4f0691ef26ff44086fbb87f9e03a92d14593fd2`, `contrato-v2.json` SHA-256 `78a44e2ab1b8cb07c8374e3e3ef265fa827d0b3af291f0cf06089a4402c6f19d`. #1221 sigue siendo propuesta; esta correspondencia no adopta su contrato ni autoriza un nuevo intento real. Si su HEAD cambia, se revisa de nuevo antes de entregar entradas.

| Origen en el paquete v2 | Campo comparado #1221 | Regla previa a referencia |
|---|---|---|
| Nombre de `*.tar.gz` sin sufijo | `identidad.paquete` | Igual al `sucesor` del manifiesto P4. |
| Versión del contenedor | `identidad.version_entrada` | Literal `residuales-documentales-v2`. |
| Bytes del `*.tar.gz` entregado | `identidad.sha256_entrada` | SHA-256 calculado por el orquestador; no se incrusta en el propio tar. |
| `esquema-identidades.tsv:llave` | `filas[].llave` | Identificador RESULT sin cifra, copiado literalmente para comparar con referencia. |
| `esquema-identidades.tsv:unidad` | `filas[].unidad` | Literal, sin escala convertida; discrepancia de unidad detiene comparación. |
| Estimador reconstruido | `filas[].punto` | Número decimal finito solo con `estado=RECONSTRUIDO`. |
| IC calculado por P3 | `filas[].ic95_inf`, `ic95_sup` | Ambos numéricos ordenados, `estado_ic=CALCULADO`. |
| Punto sin IC | `filas[].estado_ic=SIN-IC` | Extremos ausentes, distintos de null y del silencio. |
| Insuficiencia de spec/diseño | `filas[].estado=NO-RECALCULABLE-DESDE-SPEC`, `motivo` | Sin `punto` ni extremos; causa específica antes de referencia. |

`entrada_id`, conducta, eje y segmento localizan la entrada humana y no son llaves de comparación. `n_valido`, peso, exclusiones, SE, réplicas, semilla, marco, cuantiles, hashes por fila y otros diagnósticos de P3 no entran en el JSON comparado. Si se producen, van en `diagnosticos-ic-v1.tsv` exterior, sellado junto al JSON original antes de revelar referencias. `ic_lo`, `ic_hi`, `IC95_inf` e `IC95_sup` no se emiten: se usan exactamente los alias `ic95_inf` e `ic95_sup` aceptados por el adaptador. No se transforman valores, no se ajustan tolerancias y ningún diagnóstico reinterpreta la comparación tras abrir la referencia.

El contrato #1221 no define un estado específico para un denominador cero observado bajo spec suficiente. La prueba `no_estimable` usa la categoría válida de insuficiencia de diseño, con motivo explícito; no afirma que el denominador cero tenga esa causa. Si aparece una condición distinta no representable sin mentir con los estados vigentes, se detiene esa fila antes de la congelación y se requiere una versión nueva del adaptador/contrato. No se reetiqueta a posteriori.

Prueba funcional reproducible desde el worktree: `git fetch origin pull/1221/head:refs/remotes/origin/pr-1221` seguido de `python3 tools/validacion/astra6_entradas_residuales/prueba_salida_v2.py --adapter-ref origin/pr-1221`. La herramienta exige el HEAD y hashes exactos arriba, extrae solo adaptador/contrato y usa cifras sintéticas. Para cada una de cuatro cohortes construye tres JSON estrictos, congela con el tar real, verifica el sello externo, crea la referencia sintética **después** de congelar y compara; rechaza un campo auxiliar antiguo. Evidencia: `residuales-p4-prueba-salida-v2.json`. Es prueba de transporte, no validación científica ni ceguera.
