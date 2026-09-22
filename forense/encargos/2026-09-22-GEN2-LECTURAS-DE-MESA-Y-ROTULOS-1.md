# ENCARGO · ACTO GEN2-LECTURAS-DE-MESA-Y-ROTULOS-1 · MESA CIERRA LA LECTURA DEL LOTE, ENUT Y EDER RECIBEN SU RÓTULO, Y EL INFORME DEL PROGRAMA SUBE A v1.2 CON EL LOTE ADENTRO

> ENTORNO: **NUBE**. NO es CAJA.
CABECERA · SHA de redacción `bda6b60c`; una sesión, rama `acto/gen2-lecturas-de-mesa-y-rotulos-1` · LOTE (D-11): cuatro piezas · MODO ABIERTO · CONTADOR: ninguno numérico se mueve a mano; el marcador puede cambiar de estados por rótulo (repórtalo por comando). **L0 de `canon/estado-programa-v1_14.md`: si choca, toma la de `main` y re-inserta solo tu anotación; `canon/L0/` existe.**
**MODELO: Sonnet por mandato de mesa.** Procedimiento congelado o receta; latitud logística; toda duda de procedimiento se pregunta a mesa en una línea con opciones.
NO tocar (TUBERÍA): `tests/check.py`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `.github/workflows/`, `.claude/commands/`. Cierre: `tests/check.py --rapido` antes de empujar; el CI corre la suite completa. Derivados («DERIVADO — NO EDITAR») no se commitean: los re-deriva el job de main.

## 1 · OBJETIVO
Tres cosas quedaron «para mesa» en las notas de esta noche y mesa las resolvió con dirección: la lectura del B-bis del lote (`NO-CAE-EN-NINGUNA-FILA`, «la lectura la cierra mesa»), las 11 celdas de ENUT 2024 `SIN-PISO` sobre una definición que 2024 ya no pregunta igual, y la tabla EDER de 4 filas (F7 del trámite 5). Además el informe v1.1 (`#969`) no contiene el lote, que hoy es la evidencia mayor. «Hecho»: tres firmas asentadas (A.12) con su efecto en el marcador; `canon/informe-programa-v1_2.md` (v1.1 no se edita) con cada cifra derivada por comando o citada por RESULT.

## 2 · FIRMAS — verbatim; el lanzamiento es el sello
**F-LOTE (lectura del B-bis):** «Lote ENIF 2024: veredicto `PROPUESTA-CON-RESERVA` para R2 (ΔMAE 0.48 pp, IC95 [0.10, 0.72]: despeja 0, no 0.5). Ninguna fila del B-bis cae porque la cobertura de C2 por par quedó en 75 % < 80 %: **el argumento de producto "sé cuánto me equivoco" queda acotado a los cruces vistos**, como la spec lo pre-registró. La lectura de mesa: el piso C2 sigue adjudicado (A-bis 6: nadie venció), su intervalo **subcubre** y así se dice; R2 cubre 88.6 % y yerra menos, y queda como propuesta con reserva; ninguna frase de producto cita 88.6 % sin decir que es el retador no adjudicado. Para la regla de salida de θ cuenta como "no venció" — segunda prueba de tres.»
**F-ENUT:** «Las 11 celdas de ENUT 2024 definidas sobre la conducta sellada C1 (`CAMBIO-DE-INSTRUMENTO` en 2024, `#976`) pasan a `SIN-PISO-POR-DISEÑO` con esa razón; se registran celdas hermanas sobre el núcleo común C2 (`ENUT-NUCLEO-ejes-spec-v1_0.md`), que sí tiene piso 2019 y R 2024 sellados. El cruce `reparto_hogar × sexo_edad` sigue RESERVADA.»
**F-EDER (trámite 5, F7):** «Adopto `SIN-PISO-POR-DISEÑO` en el vocabulario `status`. Un acto escribe la tabla EDER de 4 filas con el dictamen de #908 §2.2 como `metadata_source`. Resuelve NC-0377 y NC-0411.» — la firma ya está en el repo (`#981`); aquí se **ejecuta** la tabla.

## 3 · LO QUE DIRECCIÓN SABE (contra `bda6b60c`)
- `[LEÍDO: nota de #986 :19-44]` las cifras del lote; B-bis `NO-CAE-EN-NINGUNA-FILA`, `ADJUDICA-SOLO = NO`. `[LEÍDO: nota de #976]` C1 sellada `CAMBIO-DE-INSTRUMENTO` fuera de 2024; C2 núcleo `CAMBIO-MENOR`; serie 2009–2024 con 2014 ≈ 2019 y salto uniforme 2019→2024, dictamen `NO-DECIDIBLE`. `[EJECUTADO: marcador]` ENUT 2024: 11 `SIN-PISO`, 10 `IDENTICO`, 1 `RESERVADA`; EDER 2017: 4 `SIN-PISO`.
- `[EXISTE]` `canon/informe-programa-v1_1.md` (`#969`) y su forma: marcador en dos columnas, cobertura por candidato con binomial, lo que el producto puede y no puede afirmar, auditoría §5.
- Resultados nuevos desde v1.1 que el v1.2 incorpora, todos sellados: lote (`#986`), árbitro 1 y 2 (`#971`, `#989`: persistencia en marginales cubre 14/57; 24 reglas re-medidas), crédito backtest (`#987`: persistencia gana 7/9), ENCIG `SALTO-SIN-EXPLICAR` (`#972`), ENUT (`#976`), validación independiente (`#970`), origen móvil ENIGH (`#988`). **Ninguna cifra entra desde este encargo: se re-deriva.**

## 4 · YA HECHO
Informe v1.1; firmas F-EDER en el repo sin ejecutar; ninguna lectura del lote asentada. Repítela tú.

## 5 · PIEZAS
**P1 · F-LOTE.** Fila FP/decisión con el texto verbatim; el campo de lectura de mesa en la celda-D o registro que el lote dejó para ello (búscalo por objeto en la nota de `#986`); el marcador sigue mostrando `PROPUESTA-CON-RESERVA` para R2 y C2 adjudicado.
**P2 · F-ENUT.** Rótulo en las 11 celdas por la herramienta que escriba el marcador (no a mano); celdas hermanas sobre el núcleo registradas con su piso 2019 y R 2024 por RESULT; el contador de `SOLO-PISO`/`evaluadas` cambia por comando, repórtalo.
**P3 · Tabla EDER.** 4 filas, `metadata_source` = dictamen de #908 §2.2, NC-0377 y NC-0411 cerradas.
**P4 · Informe v1.2.** Sucesor de v1.1: (i) marcador honesto con el lote (dos columnas); (ii) cobertura por candidato: pilotos (26/35 C2), lote (C2 75 %, R2 88.6 %), marginales (persistencia 14/57), con intervalo binomial y la advertencia de dependencia dentro de ola; (iii) lo que enseñaron el lote, ENCIG y crédito: el piso simple aguanta; la interacción encogida es señal repetida (piloto 3 y lote) sin adjudicar; nadie explica saltos de nivel; (iv) qué puede afirmar hoy el producto y qué no (con F-LOTE); (v) lo que viene: duelo ENVIPE 2026 (tercera prueba de θ), crédito 2024, ENIGH; (vi) auditoría §5 completa, con las preguntas [v2.16].

## 6 · LATITUD · 7 · PAROS
Latitud: forma, orden, herramientas. PAROS: a) una cifra que no puedas derivar o citar → no entra · b) editar un sello, un veredicto, v1.1 o una spec · c) escribir un rótulo a mano en un derivado · d) alterar el texto verbatim de una firma. Compuertas: ninguna. Perímetro: filas de firma, celdas-D de ENUT (rótulo y hermanas), tabla EDER, `canon/informe-programa-v1_2.md`, NC propias, derivados por comando, nota, cascada. Fuera, PARA. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
