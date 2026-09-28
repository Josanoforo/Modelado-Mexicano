# Revisión acotada a encargos Astra/Codex

Corte main: ffa1df15043befac6abdf0fdafdf2f86382f3186, observado después de la fusión #1229, 27/sep/2026 CDMX. No se revisan los PR abiertos de dirección/adquisición.

| PR | HEAD final | Estado y conclusión |
|---|---|---|
| #1221 | 831063f96de8c30839ded28ac670f083db04f9af | Fusionado; implementación portable recibible, mantiene NO-LANZAR-COMO-CIEGA en su entorno. No acredita sesión remota ni runtime científico. |
| #1222 | c6b0dfe9311a212f9a21b94124227c9b5eaeb4a2 | Fusionado; acta restaurada a VIVO en cuerpo inicial y CONSUMIDO solo al pie, reparación registrada. Diagnóstico ENOE y NO-LANZAR intactos. |
| #1229 | 6c6af88a8d06462fca012e212272d400ba6db9d8 | Fusionado; esquema v2 único, diagnósticos fuera de salida comparada y v1 preservados. Resuelve el rechazo de alias señalado. |

Revisión propia de la corrección #1229: lectura del generador, contrato de salida, correspondencia y prueba. Los hashes del adaptador/contrato fusionados coinciden con los fijados por la prueba del PR. Se ejecutaron aquí tres circuitos sintéticos de formatos corregidos (punto sin IC, IC calculado y no recalculable por spec): congelación/comparación satisfactoria. No se extrajeron/reprodujeron aquí los cuatro tar ni se reejecutaron los 12 circuitos sobre ellos; esos 12 y las 936 filas son evidencia declarada en el PR, leída, no ejecución propia de este pase.

Reserva concreta de integración: el comando documentado --adapter-ref origin/pr-1221 fija d8ef9f56, pero la rama final avanzó por integración. Los bytes consumidos siguen coincidiendo. Para reproducción usar --adapter-dir con adaptador/contrato de hashes verificados o el SHA histórico fijo; no interpretar el avance de HEAD como cambio de contrato. No requiere rehacer resultados.

Límite explícito de estados: denominador cero con spec suficiente no cabe como insuficiencia de spec. #1229 lo reconoce y detiene ese caso; 01 resuelve la representación con versión nueva antes de ejecución real. La fusión no firma contratos de edades/IC ni abre reservas.

C3: listado actual por homónimos, 31 originales y 17 v2. Se seleccionaron diez originales sin homónimo, con rutas/blob documentados en cada encargo. Se leyeron extractos iniciales para orientar revisiones, no se afirma haber auditado íntegros los diez reports en este pase.
