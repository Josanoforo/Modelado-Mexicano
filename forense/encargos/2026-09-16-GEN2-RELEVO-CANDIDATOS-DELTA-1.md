# ENCARGO · GEN2-RELEVO-CANDIDATOS-DELTA-1

Fecha: 16 de septiembre de 2026. Repositorio: `Josanoforo/Modelado-Mexicano`.
Base consultada: `9dffd6455c67e2ca99740e79f90be59a13f250e1`; ejecución desde `origin/main` vigente.
Ejecutor: Codex CLI; Claude Cloud también sirve, sin corpus.
Producto: comparaciones reproducibles y bloque de decisiones sobre relevos existentes.

## Resultado encargado

Resolver NC-0255 en su alcance técnico: producir las comparaciones admisibles y las listas de decisión de los slots que hoy tienen `CANDIDATO-GEN2`. Los números ya existen; falta determinar qué relevo permitirían. **No adoptar ni editar consumidores en este acto**: la preparación debe poder correr sin cambiar el snapshot de M que Opus y F6 necesitan.

Comprobación al emitir, `python3 tools/relevo_usos.py`: 12 candidatos, sobre 207 slots. Son RES-0025, 0026, 0028, 0031, 0032, 0033, 0034, 0053, 0054, 0055, 0056 y 0066. Es una referencia, no una aserción fija. Los 12 se distribuyen entre evasión de norma, denuncia, ahorro, apoyo familiar y derivados de vías/horizonte. No invadas LISTADO-PARA-MESA, conflictos o vetados para aumentar el lote.

## Insumos mínimos

- `forense/no-corrido.tsv`: NC-0255 y NC-0085; sólo lectura.
- `forense/notas/2026-09-16-GEN2-PINS-REPRODUCE-1-cierre.md`, P2.
- `forense/encargos/2026-09-15-GEN2-RELEVO-USOS-1-ADENDA-REGLA-ADOPCION-EN-BLOQUE.md`, texto firmado íntegro y enmienda.
- `tools/relevo_usos.py`, `tools/delta_comparacion.py` y CLI `corrida0 delta`.
- `data/corrida0/relevo-usos-v1_0.tsv`, demanda y resultados; specs/sellos y consumidores sólo de los slots seleccionados.
- `forense/notas/2026-09-15-GEN2-E11-RES0028-PARTICION-cierre.md` y la ficha que cita: RES-0028 ya tiene trabajo sustantivo que no debe perderse.

## Ejecución

### P1 · Selección actual, sin escritura global

Corre `tools/relevo_usos.py --json` sin `--escribe`; captura salida fuera de los registros. Selecciona por valor de `veredicto`, no por posición ni por el número 12. Si lees TSV derivados, respeta los comentarios que preceden al encabezado. Guarda SHA efectivo y lista de IDs. Separa cualquier slot ya resuelto por un merge concurrente; no fuerces el universo viejo.

La derivación es un índice de candidatos, **no una demostración de equivalencia**. Para cada pareja acredita consumidor, fuente legacy anterior a adopción, CALC, RESULT, sello, generación y las ocho dimensiones exigidas por GEN2-DELTA-1. Una cifra cercana no acredita el mismo evento o universo. Lee los sellos y resultados publicados, sin volver a correr medidores o abrir respondentes.

### P2 · Contrato y comparación efectiva

Genera contratos con la infraestructura existente, filtrados a la lista vigente, hacia el directorio propio. Puedes importar `deriva()`/`contrato()` y utilizar sus representaciones, pero revisa que las familias soporten estas parejas. Si el generador omite una familia, completa únicamente la correspondencia de esa pareja con fuentes y citas precisas en el contrato propio; no inventes equivalencia para satisfacer el esquema ni modifiques el motor compartido de comparación.

Ejecuta el CLI vigente de `corrida0 delta` sobre cada pareja admisible y guarda JSON/TSV/lectura breve. Los valores y hashes los lee el script desde sus fuentes; no copies números a mano al comparador. Si ya existe el mismo delta bajo el mismo contrato/fuentes, reutilízalo con identidad verificable. Ante una incompatibilidad material, publica `NO-COMPARABLE` y la dimensión, **sin delta numérico interpretado**. No ocultes exclusiones: una fila final por cada slot seleccionado.

### P3 · Aplicar la regla firmada, no una tolerancia inventada

Cita la regla vigente al clasificar. Diferencia la materialidad numérica que devuelve una herramienta del **bin de autorización** que manda la firma:

- Bin 1 sólo con todas sus condiciones acreditadas: signo, cláusula `se_mueve_si` o IC legacy y ausencia de las categorías obligatoriamente materiales.
- Bin 2 incluye reglas con p medida, coeficientes y marcador aunque el delta sea cero. Las seis filas `conducta_p_medido` del corte inicial no se vuelven bin 1 por reproducir seis decimales. Una etiqueta de columna no sustituye leer la función real del consumidor.
- Bin 3 cuando no hay criterio o la pareja no admite comparación; conserva la razón y no rellenes una diferencia inválida. No convierte una ruptura de universo en adopción autorizable por mayoría.

RES-0028 requiere la partición/universo documentados en su ficha sucesora: no rebautizar un complemento como una conducta distinta. Para las cuatro vías de ahorro, verifica partición y suma en el conjunto de resultados publicados; para cualquier derivado, conserva su dependencia explícita. Es un control material de consistencia, no un nuevo cálculo con microdato.

### P4 · Devolver una decisión lista

Entrega `decisiones-propuestas.md`: bloque bin 1 que podría entrar por merge posterior, renglones bin 2 con el cambio real y el motivo de decisión individual, bloque bin 3 con lo que falta. Redacta el texto de resolución que mesa podría aprobar, **sin firmarlo**. Si todos requieren decisión, dilo; no prometas reducción del contador. El producto termina en comparación y propuesta, no en adopción.

## Perímetro de escritura

- `forense/relevo-usos/candidatos-delta-1/`: selección, contratos, resultados de comparación y decisiones propuestas.
- `tools/relevo_candidatos_delta.py`: sólo si hace falta un envoltorio pequeño; reutiliza las funciones existentes y acepta destino explícito.
- `tests/test_relevo_candidatos_delta.py`: sólo si se incorpora código y existe una regresión material que proteger (p.ej. omisión silenciosa de slots o tratar p medida como bin 1).
- Encargo y nota de cierre exclusivos de este rótulo, en `forense/encargos/` y `forense/notas/`.

No editar `tools/relevo_usos.py`, `tools/corrida0.py`, `tools/delta_comparacion.py` ni las vistas canónicas. No necesitas corpus; CLI o Claude Cloud sirven.

## Cierre suficiente

Cada ID seleccionado aparece exactamente una vez, con pareja acreditada o rechazo explícito; ningún delta publicado cruza escalas/universos incompatibles; bins derivados de la firma y no del redondeo. Comprueba resultados por los comandos existentes, sin duplicar toda la validación científica. Fuentes y consumidores sin cambios; una tabla con slot, consumidor, estimando/universo, referencia legacy, CALC/RESULT, delta admisible, bin, decisión y siguiente acción.

El PR debe dejar claro: **cero adopciones y cero cambio del snapshot de M**; el beneficio es poder resolver el relevo de un bloque concreto.

## Autoridad, arranque y concurrencia — parte integral del encargo

Este archivo es un encargo propuesto por ChatGPT para Jonás. Su prompt de lanzamiento autoriza su ejecución; no atribuyas a mesa una firma nueva por la mera existencia del archivo. Al lanzarlo se autorizan trabajo en el perímetro, pruebas pertinentes, commits, push sin force y un PR; **fusión con Jonás**. No enviar correos ni solicitudes a terceros, comprar, aceptar contratos o efectuar llamadas experimentales a modelos. El agente CLI puede implementar normalmente.

1. Lee `AGENTS.md` y este encargo completo. Localiza el clon existente, reporta ruta absoluta, rama, HEAD y estado; fetch de `origin/main`, consulta de ramas, worktrees y PR del mismo objeto. Un PR ausente no demuestra que una sesión no esté trabajando: considera los encargos ya lanzados de esta conversación. No dupliques una ejecución viva.
2. Usa un worktree propio desde `origin/main` vigente. No cambies de rama, hagas stash, limpies o descartes archivos de otra sesión. No alteres el árbol que ejecuta el cron ni el del piloto de Opus. Si el SHA avanzó, revalida únicamente las premisas materiales; la variación de conteos no es causa automática de paro.
3. Archiva este texto verbatim en `forense/encargos/2026-09-16-GEN2-RELEVO-CANDIDATOS-DELTA-1.md`, con procedencia/consumo fuera del bloque original. Publica temprano la rama para visibilizar el trabajo; los commits técnicos pueden seguir antes de abrir el PR final.
4. **Excepción temporal de cascada, autorizada por el prompt de lanzamiento:** no escribir `decisiones.tsv` (ninguno), `no-corrido.tsv`, firmas, hallazgos, PARA, canon/gobernanza, canon/estado, registro de rótulos, índices generales, tableros, colas, manifiesto, rutinas, contadores o baseline. No reservar ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --verifica --escribe`. Esta excepción difiere su integración serial; no elimina permanentemente las reglas del proyecto ni autoriza debilitar checks.
5. Opus conserva CAREO, TRÁMITE-4, CELDA-D-PILOTO-1, corte de edad, crosswalk y firmas. F6-FACTIBILIDAD-PREPARACION-1 conserva MOCIBA/ISSP; DIGESTO-CORRECTIVO-1 conserva su generador y pruebas. **No leer ni derivar ENIF 2024 localidad × edad**, ni capturas/resultados nuevos del piloto; no abrir microdatos ni desenlaces reservados de F6. Ningún script, test o verificación masiva puede hacerlo incidentalmente. Lectura de resultados históricos ya públicos sólo donde este encargo la necesita; nunca reconstruir con ellos el cruce reservado.
6. No editar `milpa/`, motor, theta, G5, contratos sellados, medidores ajenos, scripts de adquisición o archivos de los otros encargos. Si una pieza exige una decisión material, completa las independientes y devuelve esa decisión concreta; no abandones el producto por numeraciones, nombres o cascada diferida.
7. Antes del push final, incorpora `origin/main` por un procedimiento que preserve historial compartido. Revisa diff y pruebas afectadas. No reejecutes una medición ya sellada sólo porque avanzó documentación: usa su verify dirigido si procede. CI heredado se compara con baseline bajo el mismo entorno; nunca `--freeze`, exenciones nuevas o cifras inventadas. Si un gate requiere un archivo excluido, entrega PR con producto y bloqueo exacto para integración serial.
8. Entrega SHA base/final, producto, comandos reales, pruebas/CI y reservas. En el PR: `CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4`; lista sólo propagaciones necesarias, sin números reservados. Un PR listo no equivale a integrado, adoptado, validado o desplegado.

Auditoría y documentación auxiliar: aproximadamente 20% del esfuerzo. La definición del estimando y la verificación de escala/universo son parte sustantiva del resultado. Una o dos comprobaciones razonables ante fallo; alternativa directa y bloqueo preciso. Termina con un producto usable o con la causa material y la siguiente acción exacta, sin auditoría general.

## Prompt de lanzamiento

> Ejecuta íntegramente ENCARGO-GEN2-RELEVO-CANDIDATOS-DELTA-1.md desde origin/main vigente en worktree propio. Autorizo comparaciones sobre resultados publicados, archivos y script del perímetro, pruebas pertinentes, commits, push y un PR; fusión conmigo. Autorizo diferir la cascada compartida. No adoptes, no edites milpa, no abras microdatos ni datos/capturas reservados. Entrega las parejas y deltas admisibles por script, las tres listas conforme a la regla firmada y las decisiones listas para resolver. No clasifiques p medida como bin 1 por tener delta pequeño. El piloto de Opus y F6 conservan su snapshot.

---

## Procedencia y consumo — fuera del bloque original

El bloque anterior se archivó verbatim desde
`/mnt/c/Users/PC0/Descargas MX/ENCARGO-GEN2-RELEVO-CANDIDATOS-DELTA-1.md`,
recibido como prompt de lanzamiento el 16/sep/2026; SHA-256 del original:
`1c2308099cacba55f01e501fbf5cd6ad497ae122963f5a34a7016f1f2f18bb16`.

Consumo técnico: rama `acto/gen2-relevo-candidatos-delta-1`, base
`9dffd6455c67e2ca99740e79f90be59a13f250e1`, PR `#829`. Producto y cierre en
`forense/relevo-usos/candidatos-delta-1/` y
`forense/notas/2026-09-16-GEN2-RELEVO-CANDIDATOS-DELTA-1-cierre.md`.
La cascada compartida queda diferida por la excepción temporal del encargo;
este consumo no es firma, adopción ni fusión.
