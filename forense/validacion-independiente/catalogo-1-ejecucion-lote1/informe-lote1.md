# C1 · primer lote independiente: resultado y límites

EJECUTADO sobre CAJA, worktree `/home/pc0/mm-astra6-c1-validacion-lote1-1`, rama `codex/astra6-c1-validacion-lote1-1`. Inicio de main `1eeb855272b933642177e3f32d51adc89f1009a0`; cierre incorpora main `3aacda232b3b03f158950738f31aa4ea509d3162`. Universo histórico: `4f125e709d3b3830078fe749c82068b3d55e6e70`, `canon/catalogo-del-mexicano-v1_1.tsv`, SHA-256 `11e35bfc5b371f45aa3219f8f08c185bc00a299e891e6ddf498992c95951b6b7`. No se sustituye por v1.2: vigencia.tsv coteja identidades separadamente.

Se entregaron nueve paquetes a nueve sesiones efectivas nuevas, sin historial del orquestador ni acceso al clon. Cada salida se congeló y se recibió antes de la comparación. Todas las 3371 identidades tienen dictamen; no hay NO-EVALUADO ni bloqueo de acceso dentro del lote. Hay 2561 llaves con cifras reconstruidas (75.97% del lote y 7.09% del universo histórico). La evaluación de 3371 identidades incluye diagnósticos de spec; no equivale a ese número de recálculos numéricos.

Los puntos: 1876 coinciden y 685 discrepan. Coinciden punto e IC en 3 casos; 1873 coinciden en punto pero difieren en IC bajo la tolerancia preexistente. El dictamen completo es 3 COINCIDE, 2569 DISCREPA, 799 NO-RECALCULABLE-DESDE-SPEC. DISCREPA incluye 11 supresiones de publicabilidad: hubo ejecución y una celda publicada originalmente quedó suprimida, no una spec imposible.

| Paquete | Identidades | COINCIDE punto+IC | DISCREPA | NO-RECALCULABLE |
|---|---:|---:|---:|---:|
| endireh-pisos-2011-modulos-0001 | 1894 | 3 | 1891 | 0 |
| endireh-pisos-2021-ayuda-0001 | 117 | 0 | 116 | 1 |
| endireh-pisos-2021-comunitaria-0001 | 100 | 0 | 0 | 100 |
| endireh-pisos-2021-decisiones-0001 | 138 | 0 | 138 | 0 |
| endireh-pisos-2021-discriminacion-0001 | 286 | 0 | 263 | 23 |
| endireh-pisos-2021-escolar-0001 | 96 | 0 | 0 | 96 |
| endireh-pisos-2021-familiar-0001 | 50 | 0 | 50 | 0 |
| endireh-pisos-2021-laboral-0001 | 100 | 0 | 0 | 100 |
| endireh-pisos-2021-nofisica-bc-0001 | 590 | 0 | 111 | 479 |

Las nueve sesiones comparten dos olas y muestras, no nueve pruebas estadísticas independientes. El lote se seleccionó por preparación disponible; no se extrapola su tasa al catálogo. Los otros paquetes y estimadores del universo permanecen fuera de esta entrega. C1 global no está cerrado. Coincidencia numérica, validez del estimando, adopción y capacidad predictiva son estados distintos; este lote solo contesta reproducción e identifica defectos.

## Hallazgos y decisiones que permiten

EJECUTADO: `efectos-discrepancias.tsv` conserva cada discrepancia y su componente; `hallazgos-spec.tsv` cada imposibilidad de identificación/método. `discrepancias-2011.md` documenta los filtros, desconocidos, denominador de instituciones, permisos y selección de columnas tras congelar. `discrepancias-nofisica.md` documenta EDAD 98/99 en ayuda y denuncia 60+. Se comprobó exposición literal en piso/catálogo; no se demostró cambio de una conclusión o regla consumidora. No se ejecutaron contrafactuales para atribuir completamente las magnitudes.

Los motivos D-15 se dividen en identidad temporal vida/reciente ausente, recodificación educativa ausente y conflicto semántico de razon_14. No se asignaron índices por semejanza con los esperados. Las tablas semánticas sin asignar de comunitaria, escolar y laboral se conservaron como cálculos provisionales separados, sin trasladarlas a las llaves. Un nuevo intento con spec aclarada será otro objeto; no valida retroactivamente este primer intento.

Las diferencias de IC no se convierten en error de punto ni en prueba de inequivalencia inferencial. La spec no fija completamente RNG, orden de UPM/extracciones, marco, percentil o convención de CV. No se ajustaron tolerancias ni semillas a los valores revelados. La investigación de 2011 identifica además diferencia de marco UPM, no solo realización aleatoria. Se necesita una comparación inferencial explícita antes de declarar cobertura equivalente.

PROPUESTO-POR-EJECUTOR: mesa recibe este diagnóstico y encarga sucesores para las discrepancias de punto/publicabilidad y las specs insuficientes. Prioridad: denominador de instituciones y denuncia externa 2011, códigos de edad no especificada y definición de negativos/desconocidos. No retirar ni adoptar automáticamente un resultado; hasta corregir, no presentar esas identidades como independientemente corroboradas. Los sellos históricos y la adopción vigente se preservan. No se ofrecen parámetros culturales o predicciones nuevos.

## Separación y orden observado

EJECUTADO: Bubblewrap montó únicamente entrada allowlist, raw autorizado, work nuevo, binarios/bibliotecas genéricos y credencial de API. `/home`, `/mnt`, `/root` y clon ausentes; CODEX_HOME nuevo, sin config, rules, skills, historial ni resume. `sesion-sin-outputs-raw` (nombre físico por paquete) conserva un único mensaje operativo y contexto de entorno genérico, comandos y hash del transcript local; excluye cuenta, credenciales y outputs de lecturas raw. El orquestador es NO CIEGO y los auxiliares de archivo/efectos tampoco calculan como validadores.

Algunos validadores conservaron rótulo NO-CIEGA porque el perfil interior dice lectura de raíz. Se conserva literalmente su recibo. INTERPRETACIÓN-DECLARADA del orquestador: la raíz interior es el filesystem de Bubblewrap, no el host; prueba de mounts, guard y comandos acreditan separación efectiva respecto del clon. La prueba local no demuestra independencia cognitiva absoluta ni atestación externa; se solicita a Claude dictaminar esta evidencia, no se concede recibo propio.

El primer intento no conectó con la API y no produjo cálculo. El segundo creó el commit original de comunitaria; el shell retornó 2 después de concluir Codex porque se editó el launcher durante su ejecución. Se preservan salida y commit, y su replay posterior es idéntico. Los ocho lanzamientos restantes usan una versión estable cuyo SHA se registró antes de cada entrega; todos finalizaron con código 0. El ajuste de launcher agrega el host de herramientas genérico y escritura en work; no modifica entrada ni procedimiento. El primer estado FALTANTE_HORIZONTE_EN_LLAVE se tradujo a NO-RECALCULABLE-DESDE-SPEC en archivo/commit adicional antes de comparar, con original y ambos commits conservados; no se cambiaron cifras.

INTERPRETACIÓN-DECLARADA: el materializador congelado llama a verify y lee el snapshot con esperados para comprobar integridad antes de entregar. Se reutilizó como ordena P1, sin exponerlo al validador. `revelacion_utc` significa inicio del comparador posterior a recepción/congelación, no primera lectura administrativa del snapshot por el orquestador conocido. El orden se acredita para la sesión de recálculo y para la comparación; esta reserva queda visible para recibo.

## Repetición y comprobación

Sin raw: `python3 tools/validacion/astra6_lote1/verifica_lote.py`, después `resume.py` y `efectos.py` en esa misma carpeta de herramientas. Verificador comprueba hashes de paquetes, llaves únicas y completas, fechas, sesión nueva, bytes en commit mediante prueba portable y estados con evidencia. Conserva estados mecánicos del comparador y dictámenes de publicabilidad aparte. `rutas-originales` mapea nombres físicos únicos a los nombres del commit; renombrar la copia archivada no altera sus bytes ni sus identificadores Git. El tar de documentos conserva bytes y nombres recibidos; no se ejecutaron los otros cuatro encargos.

Con corpus autorizado y Bubblewrap: `python3 tools/validacion/astra6_lote1/replay.py endireh-pisos-2021-ayuda-0001 --destino /tmp/astra6-replay-ayuda-nuevo`. Destino debe ser nuevo. Materializa solo ese paquete, restaura los nombres del código congelado y ejecuta en filesystem aislado sin red; no necesita API. Es replay del código independiente, no otra validación ciega. Los nueve replays fueron EJECUTADOS y reprodujeron byte a byte reconstruccion.tsv; constancias en replay-reconstrucciones.json. Dependencias registradas por cada validador: Python 3.14.4, NumPy 2.3.5; pandas 2.3.3 cuando se usa. Para otro intento ciego, se necesita un paquete/sesión nueva y un destino nuevo; no reanudar ni reutilizar work/config.

Las salidas, código, pruebas de pertenencia al commit, recibos, hashes y tiempos están en reconstrucciones/ y entregas.json. Las pruebas Git solo incluyen código y tablas agregadas: no incluyen blobs raw ni PDF aunque el primer commit local externo los contenía. No se cambiaron productores, sellos, paquetes congelados, catálogo, universo, registros globales, CI ni reservas. No se abrió ninguna ola futura.

## Auditoría de alcance

Unidad: proporciones ponderadas por mujer; diferencias en la misma escala, sin mezclar hogares/trámites. Datos mexicanos primarios (a), retrospectivos; frecuencia no equivale a mecanismo o causalidad. Segmentos se conservan por identidad, sin generalizar a un mexicano homogéneo. No se atribuyen desconocidos, exclusión, violencia o estructura a cultura. No se transporta evidencia de diáspora o marcos extranjeros. El universo excluye/limita población según cada instrumento; no se extiende a rural/indígena fuera de soporte. Evidencia débil: identidad ausente, incertidumbre de diseño y consumidores por alias no auditados. Lectura peligrosa: llamar validado a todo el catálogo, convertir ausencia de cifra en refutación, adoptar la reconstrucción o tratar olas compartidas como pruebas independientes. Falsador: un sucesor con spec explícita y reconstrucción congelada que resuelva cada identidad, sin alterar este primer intento. Contadores globales y adopciones movidos por este acto: ninguno; evidencia local nueva, sin atestación externa ni capacidad predictiva acreditada.

## Comprobación de cierre ejecutada

`python3 -m pytest -q tests/test_astra6_paquetes.py tools/validacion/astra6_lote1/test_verifica_lote.py`: 10 pasan. `verifica_lote.py`: 3371/3371, nueve objetos Git comprobados, sin llaves faltantes. Sello normalizado del encargo: SELLO_COINCIDE. `python3 tests/check.py --baseline --rapido`: 0 FAIL, 576 WARN preexistentes/registradas; línea base VERDE, sin congelar otra base. Log local `/tmp/astra6-c1-check-final-2.log`. Se comprobó además el replay de ayuda tras reorganizar nombres físicos: salida idéntica, SHA `e67839d2a4d9cb6bd710ffcfbc56a3a403838fca2cebdf65ae61d7f5fbc5c451`; no sustituye el replay ni salida originales.

Los TSV se archivan con `-text` local para conservar CRLF originales y hashes; el campo final vacío es parte del formato tabular, no se recorta. La regla de whitespace solo afecta TSV de esta entrega.
