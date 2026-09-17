# ENCARGO · GEN2-RELEVO-REMESAS-F3-1

**Entorno:** Codex CLI o Claude Cloud; repo-only. No requiere microdatos ni llamadas experimentales.  
**Producto:** el escritor de relevos aplica F-3 a RES-0035, conserva el veredicto anterior como SUPERADO y deja de presentar como indecisión una cuestión ya firmada por mesa. No modifica el valor ni la cita adoptada del consumidor.

## 1. Evidencia y alcance exacto

Base revisada: `main e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`.

- `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-2.md`, F-1 y F-3, y su apartado NO-CORRIDO: mesa ya firmó que gobierna el veredicto más reciente sellado para `recibe_remesas`, con el grano del consumidor; el anterior se conserva SUPERADO. La firma original está registrada, no hay que volver a pedirla.
- `forense/no-corrido.tsv`, NC-0216: la escritura se dejó al escritor canónico; su enmienda del 16/sep identifica una implementación pendiente, no una firma pendiente.
- `tools/relevo_usos.py`, construcción de `veredicto_sellado` alrededor de líneas 404–422: cuando encuentra dos valores diferentes emite CONFLICTO-ENTRE-VEREDICTOS sin aplicar F-3.
- Veredicto anterior: `CALC-B-0001/RESULT-B-ADOPCION-P3`, NO-ADOPTABLE-POR-GRANO.
- Veredicto que F-3 manda considerar vigente: `CALC-ENIGH-0001/RESULT-ENIGH-A-ADOPCION`, LISTADO-PARA-MESA-REPRODUCE.
- Consumidor: `familia.seguro.volatilidad_ausencia_estado:recibe_remesas`, RES-0035. Leer la ruta efectiva que declare la demanda y su grano; no editar `milpa/`.

Esta autorización es **por esa pareja, ese consumidor y esa firma**. No convertir «el más reciente gana» en una política universal: una corrida posterior puede medir otro universo, grano o cantidad. NC-0244/RES-0047/0049, RES-0005/F-2 y los casos nuevos ENVIPE/ENCIG quedan fuera de esta adjudicación.

## 2. Ejecución

1. Reproducir la fila RES-0035 en la base con el productor, modo lectura/JSON. Leer los sellos y artefactos de ejecución de las dos corridas; comprobar identidad y orden de ejecución sellada. No usar mtime, fecha del último commit del archivo, orden lexicográfico del nombre ni fecha de re-verificación como sustitutos de cronología científica.
2. Contrastar fuente, unidad, universo, periodo, variable/transformación y grano necesarios para saber que se está aplicando la firma al caso correcto. Reutilizar la equivalencia ya documentada; no auditar ENIGH completo. Si la definición o las cifras cambiaron materialmente desde F-3, aislar esa contradicción y no extender la firma por analogía.
3. Implementar una resolución acotada y legible en `tools/relevo_usos.py`. Reutilizar lector de decisiones y sello si existe; si no existe, una regla exacta documentada con referencia a F-3 basta. No crear un registro general de adjudicaciones. La resolución debe exigir la identidad de RES/consumidor, la pareja de CALC/RESULT y sellos válidos; si falta una condición, conservar el conflicto y su causa explícita.
4. La salida vigente debe citar el veredicto de ENIGH y conservar una referencia inequívoca `CALC-B-0001/RESULT-B-ADOPCION-P3 = SUPERADO -> CALC-ENIGH-0001/RESULT-ENIGH-A-ADOPCION`. Usar columnas explicativas existentes si bastan. No borrar el valor histórico ni cambiar el RESULT que el consumidor ya cita. Resolver un veredicto no supone intercambiar automáticamente la fuente numérica de esa cita.
5. No recalcular ni reescribir el contenido del veredicto sellado. F-1 distingue grano de adopción y tolerancia de reproducción: aplicar el contrato vigente del consumidor para comprobar la resolución, nunca comparar flotantes usando un epsilon elegido para que pase. Si hay desacuerdo material, emitir el caso concreto para mesa.
6. Regenerar `data/corrida0/relevo-usos-v1_0.tsv` **exclusivamente con su escritor canónico**. Ésta es una excepción explícita y estrecha a la cascada diferida. No ejecutar `corrida0 registro --escribe`, no rederivar decisiones/corridas/resultados/usos, no editar a mano la tabla y no mover milpa ni contadores.
7. Para atribuir cambios, comparar salida del productor anterior y modificado sobre los mismos insumos vigentes. Sólo RES-0035 debe cambiar por la política nueva. La diferencia contra la vista versionada puede incluir ofertas ya fusionadas que estaban pendientes de regeneración: identificar esos cambios derivados, conservarlos si el escritor vigente los produce y no confundirlos con nuevas adopciones. Si un writer paralelo también publica la vista, sincronizar, regenerar sobre el árbol combinado y conservar la derivación; no elegir un lado del TSV manualmente.
8. Entregar tabla antes/después de RES-0035: referencias, veredicto vigente, antecedente superado, cita del consumidor, valor y grano. Explicar qué bloqueo técnico desaparece y qué no cambia. No prometer que ya hay una medición nueva ni que toda NC-0217 está resuelta.

## 3. Pruebas mínimas del defecto observado

Usar `tests/test_relevo_candidatos_delta.py` cuando corresponda, o una prueba propia pequeña:

- La pareja real satisface F-3 y conserva ambas referencias, con ENIGH vigente.
- Un sello inválido/ausente, fecha no acreditable o pareja distinta no obtiene la excepción.
- La misma fecha en dos veredictos incompatibles no se resuelve por el nombre del archivo.
- Otro consumidor con conflicto conserva su conflicto; especialmente no decidir RES-0047/0049 por esta regla.
- El grano del consumidor y la tolerancia de reproducción siguen siendo conceptos separados.
- Valor, cita y bytes de los dos CALC sellados permanecen intactos.

No ejecutar las mediciones históricas para probar el selector. No ampliar el arnés a todo el programa ni modificar tests/check.py o baseline.

## 4. Perímetro y terminado

Permitidos: `tools/relevo_usos.py`, prueba focal existente o `tests/test_relevo_remesas_f3.py`, vista `data/corrida0/relevo-usos-v1_0.tsv` escrita por el productor, `forense/analisis/relevo-remesas-f3-1/`, encargo y cierre propios.

No editar `tools/corrida0.py` ni `milpa/src/linaje.py`: L8 trabaja el primero y este acto no necesita ninguno. Tampoco modificar firmas, no-corrido, sellos, capturas, CALC, catálogo de momentos o motor.

Cierre: comando de lectura y vista canónica presentan correctamente la resolución firmada; prueba focal acredita que no alcanza otros conflictos; PR pequeño y listo para revisión. Si un sucesor ya lo resolvió, comprobar su efecto y citarlo sin fabricar otro correctivo. La propagación administrativa a NC-0216 se difiere al trámite serial; el producto operativo no espera ese trámite.

## Autoridad, arranque y trabajo simultáneo

Encargo para lanzar por Jonás · emitido 17/sep/2026 UTC (la sesión en CDMX puede seguir fechada 16/sep). Repositorio: `Josanoforo/Modelado-Mexicano`. Base consultada: `main @ e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`. Las premisas descritas corresponden a ese corte; al ejecutar manda `origin/main` vigente. Este documento no es una firma ya registrada: su prompt final define lo autorizado al lanzarlo.

1. Lee este archivo completo, `AGENTS.md` y las instrucciones aplicables a los archivos del perímetro. Reporta worktree absoluto, rama, HEAD y `git status --short`. Haz fetch y consulta PR/ramas del rótulo para no duplicar una ejecución. Revalida sólo las premisas materiales.
2. **Puedes continuar en la misma sesión CLI.** Si su PR anterior fue fusionado, usa un worktree y una rama sucesora desde `origin/main` para este encargo. No reaproveches el nombre de una rama fusionada para esconder un acto nuevo. Si hay cambios posteriores sin publicar, consérvalos: determina con diff cuáles corresponden a este encargo y traslada sólo esos cambios con commits/parches explícitos, sin reset, limpieza ni stash de árboles ajenos. Si ya corre exactamente este encargo, continúa su rama y PR; no abras un duplicado. Un squash merge no acredita ancestralidad por sí solo: compara el contenido pertinente.
3. No ejecutes este encargo encima de otro todavía activo. Sincronizar cambios propios y resolver conflictos locales de implementación está autorizado; no interpretar una contradicción científica como conflicto de texto resoluble automáticamente.
4. Los corpus se resuelven con `tools/entorno.py`, las raíces existentes y `tools/prepara_corpus.py` según sus opciones reales. Un worktree sin `data/raw` no significa que falten archivos en CAJA. No copies microdatos a Git ni expongas rutas privadas, credenciales o identificadores individuales en entregables.
5. Al lanzar quedan autorizados los cambios delimitados, pruebas pertinentes, commits, push sin force y un PR por encargo. **Las fusiones quedan con Jonás.** No enviar correos, mensajes ni solicitudes a terceros. Cero llamadas de brazos experimentales a modelos; usar CLI para desarrollar no equivale a emitir L.

### Separación respecto del trabajo en curso

Opus conserva CAREO / CELDA-D-PILOTO-1 / TRÁMITE-4, firmas, crosswalk, corte de edad, θ y magnitud de G5. WBES2023-DESCRIPTIVA-1, ENCO-DOS-OLAS-RESERVADAS-1 y L8-LINAJE-HEREDADO-1 están corriendo por indicación de Jonás. L8 conserva tools/corrida0.py; ENCO sus nuevas entradas de manifiesto y reserva; WBES su CALC y análisis. ENCIG2023-AGREGADO-CONDICIONAL-1 (#831) y ENVIPE-RES0028-DERIVADO-U4-1 (#830) ya están integrados en este corte: reutilizar sus resultados sin repetirlos. F6 mantiene su preparación y reservas.

**No abrir ni derivar ENIF 2024 localidad × edad**, ni leer las capturas o resultados reservados del piloto. No leer desenlaces retenidos de MOCIBA/ISSP, ENCRIGE 2016 ni WBES 2026. Antes de correr comandos generales, comprobar que no abran/deriven esas reservas como efecto lateral. El corpus de los brazos L no se amplía.

Excepción temporal de cascada autorizada al lanzar: archivar el encargo verbatim con procedencia/consumo fuera del bloque y publicar su producto, pero diferir `decisiones.tsv`, `forense/no-corrido.tsv`, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --escribe`. Cada PR enumerará únicamente las propagaciones necesarias después del trámite de Opus, bajo **CIERRE COMPARTIDO DIFERIDO**. La única excepción adicional en esta tanda es la vista derivada de relevos para F-3, delimitada en su propio perímetro. No autoriza registro global ni ediciones de manifiesto.

Una modificación de SHA o un defecto de nomenclatura no detiene el producto. Resolver un bloqueo con uno o dos intentos razonables, una alternativa directa y una receta concreta; continuar las piezas independientes. No ampliar a auditoría general. Aproximadamente 20% del esfuerzo como máximo en control, salvo riesgo material de datos.

## Cierre y entrega comunes

Sincroniza `origin/main` antes del push final; revisa diff y ejecuta las verificaciones afectadas. No rehagas mediciones por cambios documentales. No debilites checks ni recongeles baseline. Compara fallos heredados con la base sólo cuando afecten la entrega; corrige dependencias declaradas del entorno antes de atribuir el fallo al código. Si CI exige una escritura compartida fuera de alcance, entrega el producto probado y el impedimento exacto para integración serial, sin fingir verde.

Devuelve: qué producto cambió y qué decisión permite; enlace al PR y artefactos; SHA base/final; comandos realmente ejecutados; pruebas/CI; reservas materiales y máximo tres decisiones pendientes con su objeto preciso. Distingue PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR o un sello no constituye adopción científica. Una tabla de planes sin ejecutar lo disponible no satisface el encargo.

Termina cuando exista el producto usable y siguiente acción clara; no refines por inercia. Explica en una frase si quedó más cerca una medición, explicación o decisión mejor.


## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-RELEVO-REMESAS-F3-1 en CLI o Claude Cloud. Autorizo aplicar la firma F-3 existente a la pareja y consumidor exactos indicados, corregir tools/relevo_usos.py, probar y regenerar su vista canónica con el escritor, commits, push y PR; fusión conmigo. Es la excepción puntual de escritura derivada de este encargo; el resto de la cascada queda diferido. No alteres valores, citas de milpa, sellos ni tools/corrida0.py; no resuelvas otros conflictos por fecha. Continúa en rama sucesora desde origin/main si la anterior ya se fusionó, conservando cambios existentes. Entrega el generador funcionando y la vista correcta, no otra propuesta de firma.

---

## Procedencia y consumo — fuera del bloque original

El bloque anterior se archivó verbatim desde
`/mnt/c/Users/PC0/Descargas MX/ENCARGO-GEN2-RELEVO-REMESAS-F3-1.md`,
recibido como prompt de lanzamiento el 16/sep/2026 (CDMX); SHA-256 del
original: `213525a6e9777a393526517cd719c00000b54f9402dad2a3a555e364d0a962b0`.

Consumo técnico: rama `acto/gen2-relevo-remesas-f3-1`, base
`e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`. Producto en
`tools/relevo_usos.py`, `data/corrida0/relevo-usos-v1_0.tsv` y
`forense/analisis/relevo-remesas-f3-1/`; cierre y PR se completan en esta
ejecución. La cascada compartida queda diferida bajo **CIERRE COMPARTIDO
DIFERIDO**; este consumo no es una medición, una nueva firma ni una fusión.
