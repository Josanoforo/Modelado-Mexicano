# GEN2-ISSP-APOYO-MONETARIO-DESCRIPTIVO-CLI-1

## Mandato nuevo y frontera científica

Completa una operación descriptiva sobre ISSP México 2017, **ZA6980 v2.0.0, v26/Q8a**, que pregunta a quién o dónde acudiría primero la persona para pedir prestada una gran suma de dinero. Entrega la distribución completa de respuestas, total y por sexo, con fuente integrada acreditada, código, spec, resultados sellados, control independiente y PR.

**Este encargo, al ser lanzado por la mesa, autoriza esa medición descriptiva nueva.** No afirma que F-16 o las tarjetas F6 la hubieran autorizado. El cierre de `GEN2-F6-FACTIBILIDAD-PREPARACION-1` documentó exposición previa del objetivo y desalineación con M: recepción efectiva de dinero familiar para vejez no es intención de pedir un préstamo, y “familiares o amigos cercanos” no separa familiares de amigos.

No ejecutas F6, M, L ni comparaciones predictivas. No llamas modelos, no adoptas parámetros y no declaras validación independiente del modelo. La reserva de ZA5900/ISSP 2012, otros módulos y v21–v25/v27–v30 de ZA6980 permanece cerrada. No abras sus valores ni tabulados. SEX/edad/país/peso y las variables de diseño estrictamente necesarias sí están dentro del perímetro.

Base revisada: main `843a5f977e024ef5d74863e95856c763bee9e58d`. Rama propuesta: `codex/gen2-issp-apoyo-monetario-cli-1`.

## Inicio y adquisición dirigida

Lee AGENTS.md, instrucciones vigentes y 00-LANZAMIENTO.md. Reporta worktree absoluto, rama, HEAD y estado. Revisa únicamente trabajo vivo relacionado para no duplicarlo. Usa un worktree propio desde main y preserva ramas/cambios ajenos.

Fuentes mínimas:

- `forense/notas/2026-09-16-GEN2-F6-FACTIBILIDAD-PREPARACION-1-cierre.md`;
- `forense/produccion/mociba-flujo-documental-1/tarjetas-sucesoras.yaml`, sólo la sección R09, para entender las restricciones; no abras payloads MOCIBA;
- `data/manifiesto.yaml` e inventario de reactivos de descargas, identidades ZA6980;
- cuestionario mexicano `ZA6980_q_mx.pdf`, documentación de variables de contexto `ZA6980_backgroundvar_mx.pdf` y documentación de la versión integrada.

Localiza ZIP y documentos por configuración y raíces reales, no sólo `data/raw` de tu worktree. Verifica edición, hash, país, miembros y correspondencia entre `.dta`/`.sav`. Trabaja sobre copia de lectura o acceso compartido inmutable; usa caché propia. No reconfigures el corpus que usa pisos.

**Resuelve el bloqueo documental dentro de este encargo.** La pregunta nacional y el nombre `v26` por separado no acreditan sus códigos en el archivo integrado. Busca codebook integrado de la versión exacta en corpus y repositorio oficial GESIS. También puedes leer exclusivamente metadatos/etiquetas embebidas del archivo integrado con una interfaz que no materialice filas. Acredita que corresponden a México y a Q8a; conserva evidencia y versión. No deduzcas la correspondencia sólo por semejanza de nombre.

La recuperación de documentos o datos públicos de la misma edición está autorizada; no aceptar términos personales, registrarse ni enviar solicitudes a terceros. Si la fuente exige ese paso, entrega su identificación exacta y completa todo lo demás ejecutable; no reintentes indefinidamente ni uses otra edición sin declararlo.

## Contrato congelado

Antes de abrir valores de respuestas, congela spec y código efectivo en COMMIT-1. Puedes leer documentación, etiquetas y hashes, y usar fixtures sintéticos. No presentes esta operación como ciega: el objetivo tiene exposición histórica documentada.

Fija documentalmente país, universo adulto, unidad, ponderador, códigos y tratamiento de no respuesta. La lectura candidata del formulario nacional es: 1 familiares o amigos cercanos; 2 otras personas; 3 compañías privadas; 4 servicios públicos; 5 organizaciones sin fines de lucro o religiosas; 6 otras organizaciones; 7 ninguna persona u organización; 8 no puedo elegir. Confirma todos contra la versión integrada, incluidos 9/system missing u otros códigos que efectivamente documente. “Ninguna persona u organización” es respuesta sustantiva, no faltante. “No puedo elegir” se informa aparte y no se recodifica como ausencia de apoyo.

Lista de salidas cerrada:

1. Distribución de las siete respuestas sustantivas entre respuestas válidas, para total México adulto, hombres y mujeres: **21 proporciones potenciales**.
2. Para esos mismos dominios, n/masa de población elegible, válidos, no puede elegir, no respuesta y peso inválido. Publica cobertura ponderada de respuesta válida para interpretar el denominador.
3. Contraste descriptivo mujeres menos hombres de la categoría conjunta familiares/amigos. No separa los dos vínculos ni identifica un efecto de género.

Si el documento integrado cambia esa partición, resuelve y congela la lista exacta antes de calcular; no fuerces siete categorías por cumplir un conteo. No agregues cruces urbanos, nuevas preguntas de apoyo, otros países u olas. Son dominios de una sola muestra, no tres estudios.

Especifica selección de columnas, llaves, pesos, punto, tratamiento de extremos/denominador nulo y diseño. Las tarjetas anteriores sólo acreditaban WEIGHT, no PSU/estrato. Busca la documentación de México y verifica si existe diseño ejecutable. Si existe, congela método de varianza, dominios, df, singleton y fórmula del contraste con su covarianza. Si no existe, **publica puntos ponderados y EE/IC no disponibles por diseño no acreditado**. No sustituyas por iid, Kish o bootstrap de personas para simular precisión poblacional; no sumes varianzas de dominios suponiendo independencia. La falta de IC no impide producir el descriptivo acotado.

## Cálculo y resultado útil

Después del COMMIT-1, lee únicamente las columnas autorizadas. Evita interfaces que impriman o exploren todas las preguntas. Si una librería recorre internamente el contenedor, no materialices ni analices variables reservadas. Filtra México usando códigos documentados; no uses sólo etiquetas de archivo o la cifra histórica de muestra como filtro.

En COMMIT-2 calcula distribución, cobertura y contraste. Cada fila lleva CALC/RESULT, instrumento, versión, país, universo, dominio, código y texto acreditado, denominador, n, masas ponderadas, punto y precisión/causa. Conserva categorías con cero eventos y denominadores nulos como estados explícitos, sin suprimirlas por poca conveniencia.

Controles materiales:

- partición sustantiva que suma uno dentro de cada denominador válido;
- reconciliación de elegibles = válidos + exclusiones clasificadas, sin duplicación;
- reconstrucción del total a partir de dominios y de cualquier sexo no clasificable, con masas y no promedios simples;
- control independiente de puntos y denominadores sin importar el medidor; se permite un script pequeño separado, no una segunda plataforma;
- preservación de “familiares o amigos” como categoría conjunta y del carácter hipotético de la pregunta.

La distribución histórica de apertura puede compararse sólo después de obtener los resultados nuevos; no es un oráculo para elegir recortes. Documenta diferencias de denominador y ponderación. No copies esa tabla dentro de una envoltura GEN2 ni la llames nueva medición.

Sella y reproduce desde inputs identificados en un directorio temporal distinto. Los resultados no dependen del estado vivo del árbol. Redacta una interpretación breve: qué fuentes de apoyo se mencionan y cómo varía su composición por sexo; qué no permite decir sobre recepción efectiva, apoyo familiar exclusivo, causalidad o México en otra fecha.

## Perímetro y entrega

Puedes crear una spec descriptiva, medidor, tests sintéticos materiales, CALC nueva y `forense/analisis/issp-apoyo-monetario-cli-1/` con evidencia y tablas. Confirma IDs libres. No alteres tarjetas F6 selladas, sus gates, archivos históricos, motor, marcador, adopción, crosswalk, θ, canon ni firmas/NC de B. Conserva la nueva autorización en el encargo archivado, sin fabricar una firma histórica.

La propuesta de utilidad se entrega como evidencia para FAM y como distinción de constructos. No inventes una ranura del motor para justificar el cálculo. La decisión posterior de integrar/adoptar será explícita y separada.

Tras A/B y C integrados, incorpora main y publica tus propios asientos de replay y vistas mediante escritores canónicos, según 00-LANZAMIENTO. Si todavía no están integrados, abre el PR con la operación completa y publicación global pendiente claramente identificada; termina esa fase en la misma rama al disponer de la base. No cambies evidencia ajena ni uses `--lote` como permiso general. No asignes clasificación contable por inercia.

Entrega un PR sin fusionar con: prueba de códigos integrados; congelación y ejecución separadas; tabla nacional/sexo; cobertura/no respuesta; contraste; precisión acreditada o ausencia explícita; control independiente; receta de reproducción y estado real de publicación. El resumen debe mostrar el resultado sustantivo y sus límites, no sólo números de tests. No cierres NC-0161/0162 ni presentes el descriptivo como F6 resuelto.
