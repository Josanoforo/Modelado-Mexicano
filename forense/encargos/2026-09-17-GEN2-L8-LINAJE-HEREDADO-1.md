# ENCARGO · GEN2-L8-LINAJE-HEREDADO-1

**Entorno:** Codex CLI o Claude Cloud, repo-only; no necesita CAJA ni microdatos.  
**Resultado:** un correctivo pequeño que clasifique honestamente el origen numérico del artefacto L8 y deje explícitos los usos admitidos de sus tres resultados. No es una nueva estimación ni una adopción.

## 1. El bloqueo real y su límite

`NC-0253` registra que `CALC-L8-CONVERSION-0001` reproduce tres valores, pero el único insumo numérico, `data/l8-resultados-tipo-boleta-v1_0.json`, queda fuera de las rutas reconocidas por el clasificador. Sus resultados reciben origen `INDETERMINADO` y no pueden usarse como medición GEN2.

Hay que resolver la procedencia, **no hacer que el candado dé verde a cualquier precio**. El JSON viene del trabajo L8 de septiembre 2, anterior a la envoltura GEN2, y el corte revisado ya permite usos con herencia declarada. La hipótesis respaldada es `HEREDADO`, no `NUEVO`. Si al verificar la cadena resulta otra cosa, documentar la contradicción y parar sólo la clasificación afectada; no elegir la categoría por la conveniencia de bajar contadores.

Referencias concretas:

- `forense/no-corrido.tsv`, fila NC-0253.
- `data/corrida0/CALC-L8-CONVERSION-0001/spec.yaml`, `spec.md`, `resultados.json`, `sello.json`, `sello.sha256`; sólo lectura.
- `data/l8-resultados-tipo-boleta-v1_0.json`, SHA declarado `30f3e16dd6ea770ad72ab957547159c5427788a97a24a0ef30f2765752ef8f99`.
- `forense/notas/2026-09-02-MAESTRA35-L8-spec.md`, referencia al artefacto en línea 216 del corte revisado; `tools/l8_amplia_tipo_boleta.py` únicamente para trazar su productor, no ejecutarlo.
- `forense/encargos/2026-09-02-MAESTRA35-N9-SELLA-L8-Y-FINANZAS.md`: sello y reservas de la línea.
- `tools/corrida0.py`: `INSUMOS_LEGACY_ARCHIVO`, `INSUMOS_LEGACY_DIRECTORIO`, clasificación de dependencias y propagación de origen (bloque alrededor de líneas 3290–3332 del corte).
- `milpa/src/linaje.py`: `USOS_CON_HERENCIA`, `aptitud_para_uso` (líneas 23–83). Leer, **no modificar**.

## 2. Contrato del correctivo

El lanzamiento autoriza acreditar **esta identidad concreta** como insumo heredado si la traza de productor/fecha/hash la confirma. No autoriza una lista blanca de resultados nuevos, una excepción a `MEDICION-GEN2` ni alterar categorías del programa.

1. Reproducir por las funciones/comandos existentes el caso de NC-0253 sobre el árbol base. La verificación de origen no necesita regenerar resultados globales ni ejecutar el panel L8. Capturar sólo el resultado de estos tres IDs y sus dependencias.
2. Verificar el SHA del input que la spec consume y su procedencia en los artefactos citados. Una spec que se autodenomina GEN2 no prueba origen nuevo; un sello REPRODUCE no prueba independencia. Distinguir el JSON numérico de la spec documental: la segunda no es una nueva fuente de medición.
3. Implementar la corrección mínima en el clasificador existente, normalmente una entrada exacta en `INSUMOS_LEGACY_ARCHIVO`. No acreditar `data/` entero, no clasificar por extensión `.json`, fecha suelta o parecido del nombre. Usar los mecanismos existentes de identidad y hashes; no crear otro registro de procedencia.
4. Comprobar propagación hasta `RESULT-L8CONV-A-P-MINIMO`, `RESULT-L8CONV-A-P-MAXIMO` y `RESULT-L8CONV-A-P-MEDIA`. Mantener valores, redondeo previo del ancla, sellos y resultados originales byte a byte. Si el verificador depende del SHA de infraestructura, declarar por separado cambio de contexto y reproducción numérica; no reseñar como IDENTICO lo que no lo sea ni reseñar como cambio de cifra lo que sólo sea contexto.
5. Emitir una tabla de aptitud usando la función real: `MEDICION-GEN2 → NO-APTA`; `CONFIRMACION-INDEPENDIENTE → NO-APTA`; `HISTORICO/BASELINE/DESCRIPTIVO/CALIBRACION → APTA-CON-HERENCIA-DECLARADA` sólo como aptitud de linaje. Este resultado **no acredita** compatibilidad del estimando, validez causal ni que mesa deba elegir esos usos.
6. Devolver una decisión concreta para mesa: conservar los tres como legado explícito bajo un uso permitido, o mantenerlos sin cita de consumo GEN2. No editar `milpa/tramite.yaml` ni registrar esa elección. No prometer que disminuyen las dependencias heredadas: reclasificar no produce tres datos nuevos.

## 3. Pruebas útiles

Usar el arnés de linaje ya existente. Añadir únicamente regresiones del defecto observado:

- La identidad exacta L8 se reconoce heredada y propaga su origen a los tres resultados.
- Ruta desconocida o JSON parecido sigue indeterminado; no obtiene aptitud por cercanía de nombre.
- Heredado no satisface medición GEN2 ni confirmación independiente; el uso descriptivo mantiene la etiqueta de herencia.
- Input con hash distinto sigue rechazado por el mecanismo de identidad existente; clasificación histórica nunca neutraliza esa guarda.
- Los tres valores y archivos sellados no cambian. La tabla de antes/después separa origen, aptitud, contador y valor; no confundirlos.

No hace falta reproducir el estimador electoral con su bootstrap, ampliar municipios ni corregir todas las rutas desconocidas del programa. No añadir tests de nomenclatura. Comparar con la base para no atribuir a este cambio fallos heredados.

## 4. Perímetro y aceptación

Permitidos:

- `tools/corrida0.py`: sólo clasificación exacta del insumo L8 y lo estrictamente necesario para propagarla por la ruta existente.
- Prueba específica dentro del arnés existente o `tests/test_l8_linaje_heredado.py` si no hay ubicación apropiada.
- `forense/analisis/l8-linaje-heredado-1/`: tabla breve antes/después y decisión pendiente, con evidencia mínima.
- Encargo verbatim y cierre propios.

Prohibidos: JSON L8, código productor del panel, CALC/spec/resultados/sellos previos, `milpa/`, `tests/check.py`, baseline, manifiesto y registros globales. Coordinar únicamente el archivo compartido `tools/corrida0.py` si otro trabajo nuevo lo modifica: integrar el cambio acotado y correr las pruebas pertinentes. WBES/ENCIG/ENVIPE consumen el runner sin editarlo.

Cierre suficiente: reproducción del defecto, correctivo demostrado, identidad numérica preservada y tabla de usos/decisión. Si el caso ya fue resuelto por un acto nuevo, comprobar el resultado existente y entregar su referencia, sin fabricar otro PR. Si la cadena contradice la clasificación heredada, entregar la evidencia precisa y no ampliar una whitelist por inferencia débil.

**Interpretación obligatoria del cierre:** NC-0253 puede tener resuelta su indeterminación técnica mientras la cita/adopción siga pendiente; no declarar cerrada toda la fila ni contabilizar un relevo nuevo por este acto.

## Autoridad, arranque y trabajo simultáneo

Encargo para lanzar por Jonás · emitido 17/sep/2026 UTC (la sesión en CDMX puede seguir fechada 16/sep). Repositorio: `Josanoforo/Modelado-Mexicano`. Base consultada: `main @ 4fff914f286021574ac0897273ee0e6971b38f04`. Las premisas descritas corresponden a ese corte; al ejecutar manda `origin/main` vigente. Este documento no es una firma ya registrada: su prompt final define lo autorizado al lanzarlo.

1. Lee este archivo completo, `AGENTS.md` y las instrucciones aplicables a los archivos del perímetro. Reporta worktree absoluto, rama, HEAD y `git status --short`. Haz fetch y consulta PR/ramas del rótulo para no duplicar una ejecución. Revalida sólo las premisas materiales.
2. **Puedes continuar en la misma sesión CLI.** Si su PR anterior fue fusionado, usa un worktree y una rama sucesora desde `origin/main` para este encargo. No reaproveches el nombre de una rama fusionada para esconder un acto nuevo. Si hay cambios posteriores sin publicar, consérvalos: determina con diff cuáles corresponden a este encargo y traslada sólo esos cambios con commits/parches explícitos, sin reset, limpieza ni stash de árboles ajenos. Si ya corre exactamente este encargo, continúa su rama y PR; no abras un duplicado. Un squash merge no acredita ancestralidad por sí solo: compara el contenido pertinente.
3. No ejecutes este encargo encima de otro todavía activo. Sincronizar cambios propios y resolver conflictos locales de implementación está autorizado; no interpretar una contradicción científica como conflicto de texto resoluble automáticamente.
4. Los corpus se resuelven con `tools/entorno.py`, las raíces existentes y `tools/prepara_corpus.py` según sus opciones reales. Un worktree sin `data/raw` no significa que falten archivos en CAJA. No copies microdatos a Git ni expongas rutas privadas, credenciales o identificadores individuales en entregables.
5. Al lanzar quedan autorizados los cambios delimitados, pruebas pertinentes, commits, push sin force y un PR por encargo. **Las fusiones quedan con Jonás.** No enviar correos, mensajes ni solicitudes a terceros. Cero llamadas de brazos experimentales a modelos; usar CLI para desarrollar no equivale a emitir L.

### Separación respecto del trabajo en curso

Opus conserva CAREO / CELDA-D-PILOTO-1 / TRÁMITE-4, firmas, crosswalk, corte de edad, θ y magnitud de G5. Las sesiones existentes conservan ENCIG2023-AGREGADO-CONDICIONAL-1 y ENVIPE-RES0028-DERIVADO-U4-1. No intervenir sus archivos ni rehacer sus resultados. F6 mantiene su preparación y sus reservas.

**No abrir ni derivar ENIF 2024 localidad × edad**, ni leer las capturas o resultados reservados del piloto. No leer desenlaces retenidos de MOCIBA/ISSP, ENCRIGE 2016 ni WBES 2026. Antes de correr comandos generales, comprobar que no abran/deriven esas reservas como efecto lateral. El corpus de los brazos L no se amplía.

Excepción temporal de cascada autorizada al lanzar: archivar el encargo verbatim con procedencia/consumo fuera del bloque y publicar su producto, pero diferir `decisiones.tsv`, `forense/no-corrido.tsv`, firmas, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar numeración ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --escribe`. Cada PR enumerará únicamente las propagaciones necesarias después del trámite de Opus, bajo **CIERRE COMPARTIDO DIFERIDO**. La excepción puntual para manifiesto, si existe, se indica en el perímetro específico.

Una modificación de SHA o un defecto de nomenclatura no detiene el producto. Resolver un bloqueo con uno o dos intentos razonables, una alternativa directa y una receta concreta; continuar las piezas independientes. No ampliar a auditoría general. Aproximadamente 20% del esfuerzo como máximo en control, salvo riesgo material de datos.

## Cierre y entrega comunes

Sincroniza `origin/main` antes del push final; revisa diff y ejecuta las verificaciones afectadas. No rehagas mediciones por cambios documentales. No debilites checks ni recongeles baseline. Compara fallos heredados con la base sólo cuando afecten la entrega; corrige dependencias declaradas del entorno antes de atribuir el fallo al código. Si CI exige una escritura compartida fuera de alcance, entrega el producto probado y el impedimento exacto para integración serial, sin fingir verde.

Devuelve: qué producto cambió y qué decisión permite; enlace al PR y artefactos; SHA base/final; comandos realmente ejecutados; pruebas/CI; reservas materiales y máximo tres decisiones pendientes con su objeto preciso. Distingue PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR o un sello no constituye adopción científica. Una tabla de planes sin ejecutar lo disponible no satisface el encargo.

Termina cuando exista el producto usable y siguiente acción clara; no refines por inercia. Explica en una frase si quedó más cerca una medición, explicación o decisión mejor.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-L8-LINAJE-HEREDADO-1 en CLI o Claude Cloud. Autorizo verificar la cadena y, si confirma el origen histórico documentado, registrar la identidad exacta del JSON L8 como heredada en el clasificador existente, con pruebas, commits, push y PR; fusión conmigo. No lo acredites como fuente nueva, no aflojes MEDICION-GEN2, no cambies valores/sellos/usos de milpa ni hagas adopciones. Aplica cascada diferida. Si la rama anterior ya se fusionó, continúa esta sesión sobre una rama sucesora desde origin/main conservando su trabajo previo. Devuelve el correctivo y la tabla real de aptitud, separando procedencia resuelta de consumo aún pendiente.

---

## Procedencia y consumo (fuera del texto verbatim)

Fuente local recibida de mesa: `/mnt/c/Users/PC0/Descargas MX/ENCARGO-GEN2-L8-LINAJE-HEREDADO-1.md`.
Archivado por el propio acto el 17 de septiembre de 2026 UTC (sesión iniciada el 16 de septiembre en America/Mexico_City). El bloque anterior se conserva verbatim; esta nota posterior registra únicamente procedencia y consumo. Estado: en ejecución en la rama `acto/gen2-l8-linaje-heredado-1`.
