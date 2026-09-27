# Dictamen y encargos ASTRA6 · tanda3 · 26/sep/2026 CDMX

Corte sustantivo inicial: `57a3f2a4f55178d02d8b0e3c165502014ca48efa`; main final verificado con ambos PR tardíos fusionados: `0304bf211798d29740d7a50649ea81dbcea7a943`. Se incorporaron los dos PR tardíos:1188 HEAD76ee2240e44e27dd6545f896596ba4d9be8e669b;1189 HEAD6a08745a0cb7da46e106e33ff670c43a530a2dc5. Al cierre se verificó que ambos ya están fusionados, sobre los mismos HEAD revisados. Son dictámenes de esta revisión, no comentarios publicados ni recibos formales concedidos.

## Recomendación de integración

1. **#1189 ya fusionado; conforme por contenido documental.** Se leyeron el dictamen completo y la captura de identidades. Sus cifras/estados coinciden con los objetos revisados: integración distinta de recibo/adopción,685 puntos distintos frente a1873IC y11publicabilidad,11reports de31. Declara que no ejecutó microdatos. No necesita otra integración ni crea dependencia de nuevas autorizaciones.
2. **#1188 ya fusionado; queda una reserva de integridad reproducida.** Leer abajo. La compactación normal y su uso por los consumidores revisados son coherentes; probar/restringir la pérdida parcial de metadata y acreditar recibo sobre HEADfinal. No abrir otro encargo de CI: devolver ese ajuste acotado a la misma sesión. Resolver por un sucesor acotado y publicar derivados por el canal existente; no deshacer la compactación normal. La tanda sustantiva puede arrancar sin esperar esa publicación, consultando objetos por identidad.
3. **#1175 no usar como snapshot vigente.** Sigue abierto y declara corte4f125e70, anterior a los avances actuales. Antes de fusionar una actualización de derivados, regenerar por el canal autorizado contra main vigente; no priorizarlo sobre ciencia/producto ni añadir una sesión de mantenimiento a esta tanda.

## Hallazgos materiales de las seis entregas

| PR | Estado revisado | Dictamen e implicación |
|---|---|---|
| [1179](https://github.com/Josanoforo/Modelado-Mexicano/pull/1179) | Fusionado | Consumo/familia ya corrigió dictámenes por cláusula y las cinco falsas ROMPE por ausencia; no reenviar la corrección original. Recibo sobre sucesor final, no usar1178 como aceptación. |
| [1180](https://github.com/Josanoforo/Modelado-Mexicano/pull/1180) | Fusionado | Tres reports nuevos; separación de constructos y límites. C1 obliga a cotejar dependencias afectadas, no a detener/retractar el lote entero. |
| [1181](https://github.com/Josanoforo/Modelado-Mexicano/pull/1181) | Fusionado, HEAD62832424 | MOV034a y MOVEX02 pasaron aMATIZA; se separó MOVEX02-C causal SIN-CIFRA. Adjudicación de exposición ENIGH2024_RR.pdf sigue PROPUESTO. No restaurar ceguera ni autorizar por haber retirado contenido. |
| [1182](https://github.com/Josanoforo/Modelado-Mexicano/pull/1182) | Fusionado, HEAD70e7ea19 | Cierre material útil: inventario portable ENIF y cobertura del lector sucesor, identidad de enmiendas/drivers. Seis emisiones/tres olas, cinco con soporte; pago digital suspendido. Sin COMMIT3 ni atestación externa verificada. El NO-FUSIONAR previo revisó7f0c4370, no el HEADfinal. |
| [1184](https://github.com/Josanoforo/Modelado-Mexicano/pull/1184) | Fusionado, HEAD3effe094 | Avance científico central:2561 reconstrucciones numéricas,685 puntos distintos,1873IC distintos con punto coincidente,11publicabilidad y799spec insuficientes. Adjudicar causa y efecto; no sustituir productor por validador. |
| [1185](https://github.com/Josanoforo/Modelado-Mexicano/pull/1185) | Fusionado en57a3f2a4, HEADc9593f46 | 59sucesores:11/425 preparados;48/32347 impedidos. Se revisaron materializador, revisión semántica, disponibilidad, propuestas y delta. Preparación no acredita validación; adaptar comparación a hashes sucesores antes de revelar. |

### C1: qué significan las cifras

Los3371 diagnósticos de lote1 se reconcilian en3COINCIDE+2569DISCREPA+799NO-RECALCULABLE. Las2569DISCREPA son685punto+1873soloIC+11publicabilidad. Las2561cifras reconstruidas son685punto diferente+1876punto coincidente. No son3371 cifras efectivamente recalculadas ni2569 defectos probados del productor. Cobertura numérica histórica2561/36143=7.09%; no representa la cobertura del catálogo actual. Los9paquetes comparten2olas; no son9pruebas independientes.

Hay evidencia más fuerte que una mera discrepancia en el código de edad2021:98/99 son desconocidos en FD, pero el productor los clasifica60+. La reconstrucción diferencia global/etario de otra manera; la magnitud exacta aún exige contraste controlado. Máxima diferencia puntual reportada del lote33.25pp. No normalizarla como ruido de bootstrap.

IC: tolerancia absoluta histórica1e-10 no es un ensayo de equivalencia estadística. Diferencia de marcoUPM y dominio puede ser sustantiva, aunque dos puntos coincidan. Las once supresiones están cerca de reglasCV/ancho; no atribuirlas automáticamente al azar ni suavizar umbral después de verlas.

Las799insuficiencias incluyen767ventanas temporales sin llave semántica,31recodificaciones educativas y1confusión entre leyes/servicios. Un nuevo contrato no borra este hallazgo ni convierte una reconstrucción posterior en el primer intento ciego.

Reservas de lote1 a conservar: etiquetas originales de exposición, aislamiento efectivo frente a nombres de rutas root, normalización de estado comunitaria, primer launcher con fallo y salidas preservadas; lectura administrativa de esperados por orquestador no ciego antes del comparador. Git prueba orden, no ceguera cognitiva. No repetir lanzamientos para borrar esas reservas.

### Preparación: dónde está el trabajo grande

ENOE26273 es el mayor bloque de los48; separar punto deIC puede precisar el impedimento sin inventar semilla/ordenUPM. ENIF/ENUT/ENSANUT y parejaENDIREH2021 requieren alcances de apertura concretos. Un programa proyector anunciado aún no es una herramienta probada. Las8tolerancias propuestas necesitan decisión previa a comparación.381exclusiones de lote2 y7045nuevas filasv1.2 requieren overlay por identidad; no reemplazar la cohorte original.

### #1188: revisión de código y reserva concreta

Se leyó el parche completo (8archivos) y las funciones de vista/corrida0, consulta/relevo y cadena del emisor del motor. Los ocho campos se compactan solo si son texto no vacío idéntico dentro de corrida con más de una fila; variables/vacíos reales quedaninline. Los lectores restauran antes de buscar por spec_id; el emisor pasa porjoin_resultado. Se ejecutó aquí un caso sintético de roundtrip e idempotencia: pasó. Las233428filas/48.44MiB son medición del autor leída, no ejecución propia de esta revisión. Margen al límite50MiB≈1.56MiB: suficiente al corte, limitado para crecimiento.

**Reserva reproducida:** `restaura_constantes_resultado` valida tipo/allowlist y mapa totalmente ausente, pero no integridad/completitud del mapa. Caso: compactar spec_id=S y sello=SI; reemplazar el mapa por el JSON válido `{"spec_id":"S"}`; restaurar conserva sello vacío y no falla. La prueba nueva de metadata ausente/inválida no cubre pérdida parcial. No demuestra corrupción de los datos actuales; limita la afirmación de fallo cerrado y arriesga lectura silenciosa si el par corridas/resultados queda incompleto o desalineado. Recomiendo agregar validación de la asociación exacta al mapa (hash/identidad de contrato por referencia o mecanismo equivalente) y regresión de borrado de una clave y mezcla de snapshots, sin perder la ganancia de tamaño. Alternativamente, acotar la garantía y documentar cómo el canal garantiza y verifica el par atómico con evidencia; no afirmar detección completa que el código no tiene.

No se ejecutó la suite integral, el registro de233428filas ni la publicación en este entorno. La compatibilidad revisada cubre los consumidores citados, no todos los scripts históricos del repo. Esto no pide refactor general.

## Recibos y decisiones de Claude/mesa

- Recibir1179,1180,1181,1182,1185 sobre HEADfinal.1184 tiene FUSIONABLE-CON-RESERVA sobre suHEADfinal; cerrar las reservas técnicas con evidencia, sin fingir replay de microdatos del revisor. SOCIAL N2 no se da por recibido sin localizar su acto.
- Resolver adjudicación de exposición1181: sesiones/objetos afectados, consecuencias y prohibición de reclasificar como ciego. Aclarar también el condicionamiento de CEEY en el recibo de movilidad; no inferir población nacional ni causalidad sin denominador comparable.
- C2: decidir contrato/control sucesor ENIF y enmiendas necesarias, interpretación ENVIPE de singleton/marco y mantener suspensión de pago digital. Atestación externa y aperturas son actos distintos.
- Firmar propuestas de acceso/tolerancias solo con objetos concretos;03 deja código/contratos terminados antes de pedir esas decisiones. No detener toda la tanda esperando firmas de una pieza.

## Alcance de esta revisión

Lectura de GitHub contra commits concretos, parches y documentos/código señalados; reconciliación aritmética de agregados y casos sintéticos de1188 ejecutados localmente. No se ejecutaron microdatos,9replaysCAJA,200réplicas por estimador, pruebas de aislamiento ni todos los tar; la evidencia de esos hechos proviene de entregas y recibos explícitos. La revisión no concede validación independiente global ni aceptación editorial automática. Las cifras de resumen se cotejaron entre informes/JSON, no se volvió a calcular el conjunto de3371filas desde microdatos.
