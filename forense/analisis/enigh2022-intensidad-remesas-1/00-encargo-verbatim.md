# ENCARGO · GEN2-ENIGH2022-INTENSIDAD-REMESAS-1

**Entorno:** Codex CLI / CAJA. **Prioridad:** primera de esta tanda. **Producto:** una medición descriptiva nueva de montos y participación de las remesas en el ingreso corriente de hogares receptores de ENIGH 2022, con incertidumbre tipada cuando el diseño lo permita.

## 1. Pregunta y diferencia respecto de lo medido

CALC-ENIGH-0001 ya mide hogares con remesas > 0 y su complemento; #835 aplica el veredicto F-3. Ninguno de esos productos, en el perímetro consultado, entrega la distribución de montos ni cuánto pesan las remesas dentro del ingreso de quienes las reciben.

Pregunta: **entre los hogares receptores, cuánto reciben y qué fracción de su ingreso corriente representan las remesas?** Contrastar promedio de participaciones por hogar y razón de masas de ingreso: son estimandos distintos. El término “dependencia” será sólo una descripción de participación contable, nunca dependencia causal, pérdida contrafactual de ingreso o capacidad de aseguramiento.

Consumidor analítico: interpretación de `familia.seguro.volatilidad_ausencia_estado` (R5.1). Una sección transversal sobre recepción e ingreso no identifica volatilidad, ausencia de Estado, respuesta a choques ni efecto protector. No cambia el parámetro ni el tier de esa regla. La prevalencia conocida se usa sólo como control de reproducción, no se vende como resultado nuevo.

## 2. Insumos exactos

- `data/corrida0/CALC-ENIGH-0001/`: spec, medidor, resultados y sellos, sólo lectura.
- `forense/prereg-caja/ENIGH-REMESAS-R51-spec-v1_0.md`, contrato de identidad, ponderación y códigos.
- `data/manifiesto.yaml`: `enigh2022_nc_csv`, SHA-256 `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`.
- Único miembro estadístico permitido: `conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2022_ns.csv`.
- Diccionario del mismo paquete: `conjunto_de_datos_concentradohogar_enigh2022_ns/diccionario_de_datos/diccionario_datos_concentradohogar_enigh2022_ns.csv`, y metadatos correspondientes. Confirmar rutas con el índice ZIP, sin abrir otros miembros estadísticos.
- Variables inventariadas: `remesas`, `ing_cor`, `factor`, `folioviv`, `foliohog`, `est_dis`, `upm`. No hace falta abrir población, ingresos individuales, trabajos ni gastos. No medir otras olas.

Primero acreditar documentalmente definición de remesas, composición de ing_cor, unidad monetaria, periodo de referencia/normalización y si ing_cor incluye remesas. El inventario acredita nombres, no esas equivalencias. Si falta una pieza, adquirir hasta dos documentos oficiales de ENIGH 2022 indispensables. No deflactar ni anualizar por intuición; si ambas variables no comparten unidad/periodo, detener su cociente y conservar las piezas identificables.

## 3. Contrato estadístico acotado

Congelar contrato antes de leer las columnas monetarias reales para este análisis. Se conoce la prevalencia previa: el estudio no es ciego ni confirmatorio. Usar todos los hogares del archivo para el marco muestral, peso factor y llave folioviv+foliohog; exigir una fila por hogar y códigos documentados. No tratar nulos/negativos como cero.

Con w=factor, r=remesas, y=ing_cor:

- Dominio receptor: r > 0 documentado y válido. Informar n no ponderado y masa ponderada; comparar su prevalencia contra CALC-ENIGH-0001.
- Montos entre receptores: media ponderada de r y mediana ponderada (inversa de la función de distribución ponderada, regla de empate declarada), con unidad/periodo en encabezado.
- Dominio de participación: receptores con y > 0, finito y documentado. Reportar exclusiones por motivo y masa; no ocultar que cambia el denominador.
- Participación media por hogar: `sum(w*r/y)/sum(w)` en ese dominio.
- Participación agregada: `sum(w*r)/sum(w*y)` sobre exactamente el mismo dominio. No es la media anterior y no se calcula promediando porcentajes sin peso.
- Proporción de esos hogares con `r/y >= 0.5`. El 50% es un umbral descriptivo fijado ahora; no es corte de pobreza o riesgo ni se optimiza después.

Si documentación acredita r como componente no negativo de y, verificar r <= y dentro de tolerancia monetaria predefinida. Si hay excepciones, mostrar n/masa y causa identificable; no truncar a 1 ni eliminar extremos para hacer válida la identidad. Si la documentación revela un total neto que permite cocientes >1, fijar su interpretación antes del cálculo y no llamarlo automáticamente proporción acotada. Una incompatibilidad material suspende únicamente los estimandos afectados.

No winsorizar, no crear deciles, no escoger subgrupos después de los resultados, no añadir un índice de vulnerabilidad. No publicar montos como moneda constante ni valores anuales si las fuentes no lo sostienen.

## 4. Incertidumbre y ejecución

**COMMIT 1:** spec humana/mecánica, código y fixtures sintéticos. Sucesor sugerido `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`; no modificar el padre ni su sello. Reutilizar lectura/validaciones existentes cuando corresponda, sin acoplar a archivos mutables de otras ramas.

Precisar el diseño de encuesta que sustenta cualquier IC: estratos y UPM como identidades de texto, universo completo para los remuestreos y contribuciones cero fuera del dominio. No filtrar primero a receptores y presentar ese subconjunto como toda la muestra. Si procede bootstrap de UPM en estrato, fijar antes de ejecutar 2,000 réplicas, generador/semilla y política de estratos singleton; recalcular los cocientes completos en cada réplica.

IC95 prioritarios: participación media, participación agregada y proporción >=50%; montos pueden quedar como descriptores sin IC si añadir su incertidumbre no cambia la decisión presente. No fabricar IC binomial independiente de diseño. No heredar del padre la afirmación de que el tratamiento singleton produce una cota inferior garantizada. Documentar supuestos y etiquetar la aproximación. Si falta diseño operativo, entregar puntos y limitación concreta; no bloquear toda la medición ni repetir la investigación general de diseño.

**COMMIT 2:** ejecución real y verificación focal; tabla de cinco estadísticos principales, n/masas de cada dominio, reservas e IC donde acreditados. Una figura compacta de participaciones es opcional; si se hace, mostrar unidades y no mezclar pesos monetarios con pesos de hogares.

Pruebas del riesgo: media de razones distinta de razón de sumas en fixture con pesos desiguales; ceros/no receptores; ingreso cero y faltantes; duplicación de hogar rechazada; dominio mantiene la estructura de muestreo; regla documentada de cuantiles; control de prevalencia del padre. Una comprobación analítica independiente pequeña basta, sin suite estadística nueva.

## 5. Entrega y perímetro

En `forense/analisis/enigh2022-intensidad-remesas-1/`: tabla CSV/TSV, lectura de máximo dos páginas, recibo de reproducción y contrato de unidades/periodo. Incluir inserción lista para el informe de familia: qué añade a la prevalencia, cómo difieren ambas participaciones y qué NO sostiene sobre aseguramiento/causalidad. No editar el informe canónico aún.

Permitidos: ese directorio, CALC sucesor, pruebas propias, hasta dos adiciones documentales de manifiesto. Prohibido editar milpa, canon, padre, F-3, herramientas de relevo/registro, paneles, otras olas y datos originales. No adoptar cifras ni aumentar contadores por iniciativa propia.

Si los insumos sostienen los cinco estadísticos, calcular y entregar; no cerrar con una propuesta de cálculo. Si una parte no se identifica, publicar las otras y señalar la razón precisa. Evidencia suficiente para una lectura descriptiva, sin vender una nueva validación independiente.

## Ejecución, autoridad y concurrencia comunes

Preparado el 17/sep/2026 UTC contra `main @ 402d1a3d0e96f6d159e5c4763bbd93c01f234295` de `Josanoforo/Modelado-Mexicano`. Al ejecutar manda origin/main vigente. Este archivo autoriza su perímetro cuando Jonás lo lanza; no constituye una firma ya registrada ni una adopción científica.

1. Leer el encargo completo, AGENTS.md e instrucciones del perímetro. Reportar worktree absoluto, rama, HEAD y git status --short. Hacer fetch y comprobar si este mismo encargo ya corre o ya está integrado; continuar el trabajo existente si corresponde, sin duplicarlo. Revalidar sólo premisas materiales.
2. Una tarea/worktree/rama/PR. Se puede continuar en la misma conversación CLI. Si la rama anterior fue fusionada, abrir sucesora desde origin/main; preservar cualquier trabajo posterior mediante commits/parches explícitos. No reset/clean/force ni stash de árboles ajenos. No confundir squash merge con falta de integración: comparar contenido pertinente.
3. Resolver corpus mediante tools/entorno.py, raíces locales y las opciones reales de tools/prepara_corpus.py. Ausencia de data/raw en un worktree no demuestra ausencia del corpus. No incorporar microdatos, identificadores individuales, rutas privadas o secretos a Git.
4. Autorizados al lanzar: cambios delimitados, pruebas focales, commits, push sin force y un PR. **Fusiones con Jonás.** Cero comunicaciones externas, cuentas, compras o llamadas experimentales a modelos. CLI para desarrollar no equivale a emitir L.
5. Sincronizar antes del push final, revisar diff/perímetro y ejecutar sólo las verificaciones afectadas. No debilitar checks, no recongelar baseline ni ampliar la tarea a reparar fallos heredados sin efecto material. Si una compuerta exige escribir fuera del perímetro, entregar el producto probado y el impedimento preciso para integración serial. Resolver defectos propios de nomenclatura sin alterar el contenido del encargo archivado.

### Perímetros vivos y reserva

CAREO #827, ENCO #834, remesas/F-3 #835 y ENCRIGE-carga #836 están fusionados al corte. Precisión WBES #837 está abierto: su contenido no se trata como consolidado. ENVIPE-U4-2013-2015, ENCIG2023-FLUJO-Y-ESTIMANDO-1 y MOCIBA-FLUJO-DOCUMENTAL-1 se consideran en curso aunque todavía no aparezca un PR. MEDICION-DEMANDA-3 conserva su dueño.

Opus conserva PILOTO-1/TRÁMITE-4, firmas, corte de edad, crosswalk, θ y adopciones del piloto. **No abrir ni derivar ENIF 2024 localidad × edad**, ni leer sus capturas/resultados reservados. No abrir respuestas MOCIBA/ISSP/ENCO ni olas retenidas de F6. El merge de CAREO no levanta reservas. No ampliar corpus L ni ejecutar herramientas generales que consuman reservas incidentalmente.

Excepción temporal de cascada autorizada por el lanzamiento: archivar este encargo verbatim en el directorio propio, con metadatos de procedencia/consumo fuera del bloque, y entregar producto; diferir decisiones.tsv, no-corrido.tsv, firmas-pendientes.tsv, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar números ADR/NC/FP. No correr /tramite, /despacha, /deriva, cron ni registro --escribe. Sólo F-2 autoriza regenerar su vista específica mediante el escritor canónico; eso no autoriza una cascada global.

Manifiesto: ENIGH admite hasta dos documentos metodológicos nuevos y ENAPROCE hasta seis documentos instrumentales. Son adiciones por identidad, no regeneración completa. Preservar las adiciones concurrentes de ENCIG/MOCIBA/WBES y no duplicar un documento ya registrado. F-2 no toca manifiesto. Cada encargo tiene salidas propias.

### Cierre

Devuelve primero producto, por qué importa y decisión que habilita; después PR y rutas, SHA base/final, comandos realmente ejecutados, pruebas/CI, reservas materiales y máximo tres decisiones pendientes precisas. Distinguir PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR no adopta una cifra; un nuevo CALC no crea una fuente independiente.

Incluir **CIERRE COMPARTIDO DIFERIDO** con únicamente las propagaciones necesarias después del trámite de Opus. No convertirlo en otro inventario general. Aproximadamente 20% máximo del esfuerzo en control, salvo riesgo material de datos. Dos intentos razonables, una alternativa directa y receta concreta por bloqueo; continuar piezas independientes. Terminar con producto usable y siguiente acción clara, sin refinamiento por inercia.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-ENIGH2022-INTENSIDAD-REMESAS-1 en CAJA. Autorizo verificar unidad/periodo/composición de remesas e ing_cor, adquirir hasta dos documentos oficiales imprescindibles, congelar contrato/código y medir los cinco estadísticos descritos sobre el concentrado de hogares ENIGH 2022. Estima precisión sólo con diseño y supuestos explícitos; conserva puntos si falta esa precisión. No midas otras olas ni cambies parámetros, tiers o padres. Autorizo pruebas, commits, push y PR; fusión conmigo. Aplica cascada diferida y no interpretes participación contable como efecto causal de aseguramiento.
