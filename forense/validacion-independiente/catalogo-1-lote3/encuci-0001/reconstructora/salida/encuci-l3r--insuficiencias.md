# Insuficiencias · RESULT-ENCUCI-B-P-RUR-AGR

1. **Protocolo inferencial R23 ausente.** La firma R26 subordina la receta IC «al protocolo que resulte de FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01» (sha256 `26746fee…`), y ese documento no está en el paquete. El IC se calculó con la receta P3 firmada, solo como reproducibilidad diagnóstica. No se comprobó que sea compatible con R23. Según la firma, no certifica cobertura del 95%.
2. **Singleton vs. `NO-IDENTIFICADA`.** P3 manda sortear el singleton y «marcar» IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA. CONTRATO-v3 dice que un bloqueo de inferencia se representa con `NO-IDENTIFICADA`. Ninguno de los dos aclara si la marca bloquea el IC. En esta llave no hubo impacto porque `n_singleton = 0`.
3. **Estado para denominador cero.** El documento del punto dice NO-ESTIMABLE-UNIVERSO-VACIO, y P3 dice «Y=0 es NO-ESTIMABLE». v3 ofrece DENOMINADOR-CERO. Se decidió usar DENOMINADOR-CERO con esa causa en `motivo`. No hubo impacto porque Y > 0.
4. **Pertenencia al marco de las filas sin pareja.** No se fija de forma literal si entran al marco. Se incluyeron con contribución cero. No hubo impacto porque hubo 0 filas sin pareja.
5. **Contenido de `hash_contrato`, `hash_entrada` y `hash_entorno`.** P3 nombra estas columnas pero no define qué contienen. La elección está en `diagnostico.json` → `decisiones`.
6. **`sha256_entrada`.** No se pudo verificar porque el .tar.gz no está en el paquete. Se copió tal como lo dio la instrucción de sesión.
7. **Relleno DBF de EST_DIS/UPM_DIS.** El campo C tiene 7 bytes y el FD documenta EST_DIS con largo 3. Solo se retiró el relleno derecho del formato, aunque P3 dice «sin trim implícito». Ese texto no cubre de forma explícita el relleno de almacenamiento.
