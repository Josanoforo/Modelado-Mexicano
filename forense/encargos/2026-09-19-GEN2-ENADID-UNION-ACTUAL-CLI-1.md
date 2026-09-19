# GEN2-ENADID-UNION-ACTUAL-CLI-1

## Mandato y resultado

Completa la operación analítica sucesora ENADID 2023 de `familia.union.libre`, ordenada por F-10 de `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-2.md`. Entrega mediciones reproducibles de situación conyugal actual, total y por edad, con denominadores explícitos y una propuesta de correspondencia para RES-0043/0044. El resultado es una CALC nueva con evidencia suficiente para decidir su uso; no una nueva lista de pendientes ni sólo una spec.

El principal defecto que hay que resolver es sustantivo: el consumidor llama `primera_union` a la situación, presenta un punto como prevalencia bruta, describe un denominador condicionado a casada(o)/unión libre y denomina `matrimonio_directo` a su complemento. EDER 2017 mide tipo de primera unión; ENADID 2023 mide situación actual. No intercambies esos objetos ni ajustes el estimador para reproducir 0.1905.

La revisión se hizo contra main `843a5f977e024ef5d74863e95856c763bee9e58d`. Revalida premisas materiales al abrir. Rama propuesta: `codex/gen2-enadid-union-actual-cli-1`.

## Inicio y fuentes

Lee AGENTS.md, instrucciones vigentes y 00-LANZAMIENTO.md. Reporta worktree absoluto, rama, HEAD y estado. Revisa ramas/worktrees/PR relacionados para no duplicar una sucesora ya iniciada. Conserva todo trabajo ajeno. Usa un worktree nuevo desde main; no reutilices la carpeta sucia del antiguo 03.

Lee únicamente lo necesario:

- `milpa/tramite.yaml`, regla `familia.union.libre`, y la entrada correspondiente de `milpa/tramite-ola5-propuesta-v0.yaml`.
- F-10; NC-0194/NC-0254 y las enmiendas firmadas vigentes, distinguiendo la firma de una propuesta.
- `data/corrida0/demanda-resultados.tsv` y `relevo-usos-v1_0.tsv`, RES-0043/0044; spec de `CALC-EDER-0003` para delimitar la diferencia, sin volver a medir EDER.
- `data/manifiesto.yaml`, `data/diseno-muestral.yaml`, FD y cuestionario ENADID 2023. Identidades candidatas: `enadid2023_base_datos_csv` y `enadid2023_fd_xlsx`; confírmalas.

Localiza los bytes en las raíces configuradas, descargas y worktrees conocidos; comprueba hash, tamaño, edición y miembros. Ausencia en `data/raw` de este worktree no significa ausencia del payload. Si no existe, recupera la misma edición desde la fuente pública oficial en una ruta propia; conserva URL y hash. No sustituyas edición ni aceptes contratos o acceso con identidad ajena. Un archivo inaccesible se declara como problema de acceso, no como inexistencia del estimando.

## Diseño completo antes del cálculo

Antes de leer valores de personas, permite sólo hash/miembros, FD, cuestionario y metadatos. Reconstruye tabla, llave, edad, situación conyugal, códigos válidos, saltos y factor del nivel persona. `p3_27_ag` es una pista del consumidor, no una codificación acreditada. No uses por costumbre el factor de mujeres del módulo ni confundas UPM de enlace con UPM de diseño. Confirma `EST_DIS` frente a `ESTRATO` y `UPM_DIS` frente a `UPM` en la tabla real.

Congela en COMMIT-1 la spec y el código efectivo, incluyendo helpers que puedan cambiar el número. Usa fixtures sintéticos para desarrollar. La spec debe predeclarar:

1. Distribución completa de situación conyugal actual entre personas de 15+ con respuesta válida. Publica cada categoría documental; unión libre es una de ellas. El complemento de unión libre se llama “no unión libre”, nunca “matrimonio directo”.
2. Proporción en unión libre **entre personas actualmente casadas o en unión libre**, con su complemento “actualmente casadas”. Mantén este denominador separado del anterior.
3. Ambos estimandos por edad: 15–17, 18–29, 30–44, 45–59 y 60+, además del total 15+. El tramo 15–17 evita perder población al reconciliar el total con el perfil 18+. Si el universo documental contradice este recorte, conserva la discrepancia y resuelve el recorte antes del cálculo; no cambies categorías después de ver puntos.
4. Edad o situación no especificada, pesos inválidos y pérdida de enlace: sus conteos y masas, sin convertirlos en respuestas negativas. Llaves duplicadas o muchos-a-muchos abortan el enlace afectado.
5. Método de punto, varianza de diseño, dominios sobre muestra completa, tratamiento de singleton, grados de libertad, nivel y construcción de IC; FPC sólo si está acreditada. Un estrato con una UPM no equivale a varianza cero demostrada. Si el diseño no permite precisión defendible, conserva puntos y publica IC/EE no disponibles con causa, sin sustitución iid/Kish silenciosa.

No agregues cruces exploratorios, cohortes retrospectivas, causalidad, comparaciones de olas ni perfiles elegidos por significación. Estas salidas son dominios y transformaciones de una operación, no muestras independientes. Declara que ya existen cifras legacy: la congelación es prospectiva para esta ejecución, no una pretensión de cegamiento histórico.

## Ejecución y controles

En COMMIT-2 ejecuta la spec congelada. Cada resultado incluye identidad de fuente y universo, categoría/edad, n expuesto y válido, n/masa desconocida, numerador y denominador ponderados, punto, EE/IC/df o causa de ausencia. Publica también flujo de exclusiones y verificaciones de diseño.

Comprueba que categorías exhaustivas cierren en uno dentro del mismo denominador; que los componentes por edad reconstruyan los totales mediante masas, no promedios simples; y que unión libre bruta y condicional se obtengan de los totales adecuados. El control independiente no importa el medidor ni sus funciones de recorte: verifica al menos ambos puntos nacionales y los denominadores de todos los grupos, y precisión si se publica.

Después de sellar, compara con legacy en una tabla: resultado, universo, punto anterior, punto nuevo, comparabilidad y causa de discrepancia. Sólo calcula delta cuando coinciden evento, población, unidad y denominador. La tabla debe resolver expresamente si 0.1905 era bruto o condicional y si 0.8095 admite el nombre histórico. Una diferencia no autoriza retocar códigos. No declares que la composición actual prueba el mecanismo de baja garantía institucional.

Reproduce desde los inputs sellados en otro directorio temporal. No incluyas en resultados funciones del estado vivo del árbol, la hora o la existencia de artefactos posteriores: evita repetir NC-0313.

## Perímetro y publicación

Puedes crear spec, medidor, pruebas necesarias, una nueva CALC y `forense/analisis/enadid-union-actual-cli-1/` con encargo, nota y tablas. El nombre de CALC debe comprobarse libre antes de asignarse. Reutiliza utilidades existentes sin refactorizar el registro global. Si recuperas fuentes, conserva un manifiesto local a la operación con referencias canónicas y hash; no pises el manifiesto compartido mientras A trabaja.

No editas motor, `milpa/tramite.yaml`, árbitro, celdas-D, θ, adopción, firmas, decisiones ni NC. Entrega una propuesta explícita de consumidor/RESULT compatible para Claude y B; no la presentes como consumo activo. Los sellos históricos quedan intactos.

Sigue la publicación serial de 00-LANZAMIENTO: cuando A/B estén integrados, incorpora main y publica sólo tus nuevos asientos y vistas mediante escritores canónicos. Verifica sellos, replay propio y que no cambien evidencias ajenas. No fuerces el guardia ni marques `cuenta_gen2=SI` por defecto cuando haga falta clasificación; usa el estado pendiente soportado y declara la decisión. Si la dependencia aún no llegó, abre el PR con medición terminada y publicación pendiente explícita, para terminarla en la misma rama.

## Entrega y aceptación

Entrega commits de congelación y ejecución, PR contra main sin fusionar, rutas de CALC/RESULT, receta de replay y nota sustantiva breve con los números y su lectura. El PR debe permitir revisar los dos universos y todas las categorías, no sólo afirmar “tests pasan”. Incluye:

- tabla nacional y por edad con precisión disponible y límites;
- correspondencia RES-0043/0044: compatible, incompatible o requiere renombre, con razón;
- evidencia del control independiente y reproducción;
- estado separado de medición, sello, publicación y adopción;
- bloqueador residual exacto únicamente si persiste tras intentar las vías autorizadas.

Una discrepancia legacy bien resuelta es un resultado válido. La falta de acceso no justifica inventar un valor, y una restricción sobre adopción no justifica dejar sin ejecutar la medición autorizada. Dedica el esfuerzo a producirla; no conviertas la tarea en auditoría general.
