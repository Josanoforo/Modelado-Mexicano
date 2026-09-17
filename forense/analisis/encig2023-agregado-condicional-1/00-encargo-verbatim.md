# GEN2-ENCIG2023-AGREGADO-CONDICIONAL-1

Encargo propuesto para Jonás · 16/sep/2026 · Codex CLI en CAJA, donde está el payload.
Repositorio: Josanoforo/Modelado-Mexicano. Base revisada: 85a2e77a. Ejecutar desde origin/main vigente.

## Producto y alcance de la autorización

Producir una **estimación descriptiva agregada**, reproducible y con universo explícito, a partir de ENCIG 2023 ya adquirido. Servirá para decidir si RES-0007/0008 pueden tener un consumidor sin canal. No constituye adopción de la opción B del modelo: no cambiar milpa ni afirmar que mesa ya la firmó. El lanzamiento autoriza este producto descriptivo y su universo definido abajo; la decisión sobre el consumidor queda posterior.

El PR #828, ya integrado, identifica el hueco: existen tasas por canal, pero los consumidores no declaran canal. No basta promediar las tasas presencial/digital ni escoger una. La entrega debe dar un agregado calculado con masas de expansión y mostrar cuánto cambia el universo al restringir a esos dos canales.

## Insumos mínimos

- `forense/produccion/sin-candidato-rutas-1/01-encig2023-correspondencia.md`.
- `data/corrida0/CALC-ENCIG-2023-0001-v1_1/`: spec, medidor, resultados y recibos; sólo lectura.
- La spec sellada referida por ese CALC: `forense/prereg-caja/ENCIG-MORDIDA-2023-spec-v1_0.md`, más su documentación de diseño.
- Manifiesto: objeto `encig23_base_datos_csv`; verificar SHA completo y miembros en CAJA. No volver a descargarlo.
- Reserva vigente F-8/NC-0222: distinguir cobertura de join de cobertura de observación del desenlace. No reabrir un incidente ya resuelto.
- Demanda y consumidores RES-0007/0008; RES-0001/0002 pertenecen a otra familia y quedan fuera.

## Estimando fijado antes del nuevo agregado

Primario: proporción ponderada de eventos de trámite con `P8_4=1` **entre eventos del universo observado con P8_4 válido {0,1}, unión acreditada y FAC_TRA positivo válido**, sin restringir al canal presencial/digital. Conservar la unidad evento y la convención primaria sin deduplicar de la familia B. Es una proporción condicional al flujo que hizo observable P8_4, no una tasa para toda la población ni para todo trámite.

Secundario descriptivo, anunciado desde la spec: la misma proporción dentro de la unión de canales PRE={1} y DIG={3,4,5} de P7_3. Mostrar por separado otros códigos/canal faltante dentro del universo primario. No seleccionar el primario después de observar cuál se parece al prior.

Para cada universo: `p=Σ(FAC_TRA·I[P8_4=1])/ΣFAC_TRA`, `q=1-p`. Descomponer numerador, denominador ponderado y n por canal de modo que las partes reconstruyan el agregado. Un NA fuera del flujo no cuenta como P8_4=0. No usar FAC_P18 en lugar de FAC_TRA.

## Ejecución

1. Revisar instrucciones y trabajos vivos. Si existe agregado equivalente con cadena suficiente, reutilizarlo y entregar la correspondencia; no repetir la medición. Buscar primero numeradores/denominadores sellados: si bastan, derivar desde ellos. Si no bastan, ejecutar sólo sobre el payload ENCIG autorizado.
2. En worktree propio, escribir y comprometer spec y código con fixtures sintéticos antes de abrir el nuevo agregado. Declarar que los resultados por canal ya son conocidos: no es una evaluación ciega ni una nueva prueba confirmatoria.
3. Crear un CALC sucesor independiente, sugerido `CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001`, comprobando unicidad. Reutilizar lógica acreditada sin editar los CALC previos. La llave primaria ID_TRA, el control compuesto y la multiplicidad deben coincidir con el contrato heredado. Si la unión falla sus invariantes, parar el cálculo afectado, no deduplicar sobre la marcha.
4. Emitir p/q, n, masas, cobertura efectiva del desenlace, cobertura de join y descomposición por canal. El ~19% documentado de cobertura observada no equivale a 100% de cobertura por join. Conservar CON-RESERVA aunque la unión funcione perfectamente.
5. Para incertidumbre, usar diseño EST_DIS/UPM_DIS y procedimiento de la familia cuando los insumos lo permitan: bootstrap de conglomerados dentro de estrato, 2 000 réplicas, PCG64 y semilla 20260915. Recalcular el cociente completo en cada réplica; no combinar IC de canales como independientes. Declarar tratamiento de estratos con UPM única y réplicas no estimables. No llamar automáticamente «cota inferior» a un IC incompleto sin justificación. Si falta información de diseño, entregar el punto y la limitación concreta; no fabricar un IC binomial.
6. Sellar y verificar el CALC con mecanismos existentes. Presentar comparabilidad para RES-0007/0008 como una decisión pendiente: agregado observado no demuestra equivalencia con el consumidor actual. No enlazar RESULT a milpa, no adoptar cifras y no tocar RES-0001/0002.

## Perímetro y paralelo

Permitidos: nuevo CALC, prueba focal, tabla/lectura en `forense/analisis/encig2023-agregado-condicional-1/`, encargo verbatim y nota de cierre propios. No alterar medidores o sellos anteriores, herramientas generales ni ningún archivo de ENCRIGE, F6 o relevo. Este encargo puede correr al mismo tiempo que el derivado ENVIPE: no comparten archivos de salida.

Excepción temporal de cascada al lanzar: diferir decisiones, firmas, no-corrido, hallazgos, gobernanza, estado, rótulos, manifiesto, tableros y contadores; no reservar numeración. Devolver las propagaciones necesarias para integración serial después de CAREO/TRÁMITE-4. No ejecutar cron, deriva, despacho o registros globales con escritura. No congelar baseline ni debilitar checks.

Opus conserva piloto celda-D, CAREO, TRÁMITE-4, crosswalk y edad. No abrir ENIF 2024 ni derivar localidad × edad, reservas de F6 o capturas nuevas del piloto. Cero adquisición y cero llamadas experimentales; no enviar solicitudes a terceros.

## Cierre suficiente

Fixtures mínimos: pesos desiguales que hagan fallar la media simple; P8_4 faltante que no se convierta en cero; canal fuera de PRE/DIG que pertenezca al primario; q e IC transformados; multiplicidad de unión inválida. Una ejecución real y verificación dirigida bastan. No convertir el encargo en una auditoría general ni explorar más desenlaces.

Producto final: resultado agregado principal y secundario con denominadores, incertidumbre tipada o impedimento, tabla por canal, cadena/sello, interpretación de una página y propuesta concreta de correspondencia para decidir. No contar la derivación como fuente estadística independiente de la medición anterior.

Sincronizar main antes del push final sin force ni limpieza de árboles ajenos; si sólo cambió documentación, no repetir microdato. Entregar PR, SHA base/final, comandos, pruebas, CI y reservas. Presupuesto: un payload local, un desenlace y los dos universos declarados; ninguna búsqueda de fuentes o modelo.

## Prompt de lanzamiento

> Ejecuta este encargo en CAJA desde origin/main y worktree propio. Autorizo medir el agregado descriptivo condicional de ENCIG 2023 definido aquí, usando el payload ya adquirido, con spec comprometida antes del cálculo, pruebas, CALC sucesor, commits, push y PR; fusión conmigo. Esta autorización es para producir evidencia, no para adoptar la opción B ni cambiar consumidores. Autorizo diferir la cascada compartida. No abras ENIF/F6 ni uses llamadas experimentales. Devuelve el agregado con sus denominadores y reservas, y la correspondencia concreta que aún tendría que decidir mesa.
