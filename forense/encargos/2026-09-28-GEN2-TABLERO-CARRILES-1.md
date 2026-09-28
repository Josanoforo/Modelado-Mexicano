# ENCARGO · ACTO GEN2-TABLERO-CARRILES-1 · Un tablero de control central organizado por los 31 reports del mexicano —un carril por report— que diga, derivado por comando y sin una cifra a mano, cómo está cada carril (afirmaciones medibles y medidas, cifras GEN2 adoptadas que lo sostienen, reglas con y sin cifra, validación ciega, estado editorial v2), qué lo detiene (firmas pendientes, olas reservadas, datos por adquirir, NC materiales, CALC en cola) y cuál es la siguiente acción que lo desbloquea; con una vista de adquisición por carril y global, y el frente 2027. Se deriva en CI y lo publica el canal, como el tablero actual

> ENTORNO: **NUBE** — lee tablas del repo; escribe una herramienta, dos derivados y un test. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `98f80cc7` (re-deriva al abrir) · una sesión, rama propia; PR por pieza si prefieres · MODELO: **Opus** (la unión report ↔ dominio ↔ instrumento ↔ catálogo exige juicio; el resto es derivación) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto · D-21 aplica.
CONTADOR: cero mediciones; no adopta; no mueve contadores. Todo número del tablero es `derivado_de = <archivo>, <comando>`; el tablero no tiene línea que un humano teclee salvo el bloque «Lectura de dirección», rotulado como opinión y fechado.

## 1 · OBJETIVO
(P1) **Crosswalk report ↔ dominio ↔ instrumento.** `canon/mapa-dominios-v1_1.tsv` ya tiene `report` (1 396 afirmaciones, 31 reports) e `instrumento_ola`; `canon/catalogo-del-mexicano-v1_3.tsv` tiene `dominio` (28) e `instrumento`; `canon/reglas-contrastadas-v1_0.tsv` tiene `origen` (report) y `dominio_catalogo`; `corpus/reports-v2/INDICE.md` tiene los 31 con C/M/R/S y recibo. La herramienta deriva y **registra** `canon/crosswalk-carriles-v1_0.tsv` (report · dominios del catálogo · instrumentos que sus afirmaciones citan · familias 2027 que lo alimentan), con la regla de unión declarada en el archivo; donde un report toque varios dominios se lista con peso por número de afirmaciones; donde no case, `SIN-UNION (razón)`, nunca a mano.
(P2) **`tools/tablero_carriles.py` → `forense/tablero/TABLERO-CARRILES.md` y `docs/tablero-carriles.html`** (misma data; el HTML para Pages, estático, sin cifra que no esté en el md). Por carril, una tarjeta con:
- **Evidencia**: afirmaciones por `clase` (medible en corpus / con adquisición / no medible / no construible); cifras GEN2 adoptadas del catálogo v1.3 en sus dominios e instrumentos (n, por instrumento; suspendidas y acotadas aparte); reglas del report: CONFIRMA / MATIZA / ROMPE / SIN-CIFRA; validación ciega: RESULT de sus instrumentos con PASA / NO-PASA / CONCUERDA-NO-APROBADA (`validaciones-independientes.tsv`); estado editorial v2 (INDICE: C/M/R/S, recibo, reserva material).
- **Semáforo** con regla declarada en la cabecera del script y probada: VERDE = al menos una cifra adoptada por dominio del carril y ≥ 50 % de sus reglas con dictamen distinto de SIN-CIFRA; AMARILLO = cifras adoptadas pero reglas mayoritariamente sin cifra, o al revés; ROJO = sin cifra adoptada; GRIS = carril no medible por diseño (GENETICA/GENOMICA por firewall, y lo que el mapa marque). Los umbrales viven en un solo sitio y el tablero los imprime.
- **Stoppers**, cada uno con id y sucesor: firmas ABIERTAS cuyo objeto nombra un instrumento o dominio del carril (`firmas-pendientes.tsv`); olas que sus afirmaciones necesitan y están RESERVADA o sin decidir (manifiesto, campo `reserva`); datos por adquirir (afirmaciones `MEDIBLE-CON-ADQUISICIÓN` cuya fuente no está OBTENIDO en `data/cola-adquisicion-v1_0.tsv`, con su estado A4/A5 y si hay solicitud preparada en OBTENCION-EXTERNA-1); NC ABIERTAS con razón PARO-PREMISA o PARO-ENTORNO que citen sus instrumentos; CALC pendientes en `demanda-dictamen-v1_0.tsv` (SIN-BASE-GEN2, ESPERA-*) y actos en vuelo (encargos archivados sin CONSUMIDO) que lo tocan.
- **Siguiente acción**: derivada del stopper de mayor precedencia (firma > reserva > adquisición > CALC > editorial), con el id del objeto y el acto sucesor declarado en su fila; si no hay stopper, «listo para catálogo v1.4» o «esperando ola 2027 (familia X, gate Y)».
(P3) **Adquisición.** Sección global: cola por estado (OBTENIDO / PARCIAL / SOLICITUD-PREPARADA / NO-ACCESIBLE / NO-ENCONTRADO), payloads del manifiesto por reserva, licencias sin resolver; sección por carril: qué fuente falta, qué la bloquea, quién la pide (mesa con identidad / acto de nube / caja) y en qué encargo o solicitud está. Nada de «no existe»: vocabulario A.4 tal cual viene de la cola.
(P4) **Frente 2027 y cadena.** Por carril, las familias 2027 que lo alimentan con su gate (expediente v1.x); y un pie con la cadena de procedencia de cada sección (archivo, commit, comando). Integración: el job del canal que hoy deriva `TABLERO-PROGRAMA.md` deriva también este; `README`/`docs/index.md` lo enlazan; test huérfano que falla si un carril queda sin semáforo o si aparece un número sin `derivado_de`.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: `python3 tools/tablero_carriles.py --actualiza` regenera md y html idénticos a los commiteados (`git diff` vacío) · 31 tarjetas, cada una con semáforo, ≥ 1 línea de evidencia, stoppers (o «ninguno») y siguiente acción · `crosswalk-carriles-v1_0.tsv` registrado en INFRAESTRUCTURA con 31 filas y 0 celdas vacías sin `SIN-UNION` · el canal lo publica (un `[deriva]` con el tablero nuevo, run_id en la nota) · test huérfano verde · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
Mesa, 28/sep/2026, verbatim: «al final del día la revisión es sobre los "31" reportes del mexicano, y me gustaría entender como estamos en cada carril, qué información nos falta descargar para alimentar al modelo … cuáles son los "stoppers" qué necesitamos para desbloquearlos y como vamos en descargas … un tablero de control central, que nos de visibilidad». D-14: defecto real → mesa decide firmas, descargas y prioridades por memoria y por transfers, con un tablero que solo cuenta GEN1→GEN2; costo → dos semanas creyendo que faltaban datos que estaban (ENCRIGE 2020, ENVE 2024, CSES) y cerrando letras por «no hay dato». E.4 (derivado, no reportado), E.7 (lo publica el canal), D-21, A.4/A.16 (tokens en campo). Sin firma nueva: el tablero no decide nada.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `98f80cc7` · columnas: mapa (`report`, `clase`, `procedencia_evidencia`, `instrumento_ola`, `pregunta_textual_codigo_respuestas`), catálogo v1.3 (63 706 filas: `dominio`, `instrumento`, `ola`, `estado_adopcion`, `alcance`), reglas (162: `origen`, `dominio_catalogo`, `dictamen`, `resultado_id`), cola de adquisición (952: `fuente_canonica`, `estado_A4A5`, `prioridad`, `ids_manifiesto`), familias 2027 (8: `gate_faltante`, `firma_que_lo_abre`, `estado`), demanda-dictamen (341: `dictamen`, `sucesor`), INDICE (31 filas: C/M/R/S, recibo, reserva material). 28 dominios en mapa; 31 reports: la unión no es 1:1 (P1 la deriva).
- [EJECUTADO] `tools/tablero_programa.py` y `tablero_vista.py` existen; el tablero actual tiene 9 secciones de programa, ninguna por report. Mesa lo llama «relativamente bien» para GEN1→GEN2.
- [LEÍDO] Informe v1.5: 17 de 28 dominios con estimador adoptado (`cifra_v1_5.py mapa11_dominios_medidos`): esa función es candidata a reutilizar por carril.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'TABLERO-CARRILES\|TABLERO-REPORTS\|CONTROL-CENTRAL'` → 0. Homónimos: TABLERO-SENAL-1, TABLERO-EN-CANAL, TABLERO-PROGRAMA (programa, no carriles: se reutiliza su cableado al canal y su test de «cifra derivada»); REGLAS-Y-RESULT-1 y MAPA-INSTRUMENTOS-ALTERNOS-1 (fuentes). En vuelo: TUBERIA-3 (canal: coordina por archivo si tocas el job de derivados; que sea una línea), PISOS-DOMINIOS, CALC-ALTERNOS, C1-SUCESORES (caja: sus cifras entran al tablero cuando el canal las publique).

## 5 · PIEZAS
P1 → P2 → P3 → P4. Rama prevista: report sin dominio casable → carril GRIS con `SIN-UNION` y la afirmación que más se acerque; instrumento citado por el mapa que no está en el manifiesto → stopper «adquisición» automático; catálogo sin `report` explícito → la unión pasa por dominio × instrumento y el tablero lo dice en el pie.

## 6 · LATITUD — amplia
Diseño visual del md/html, orden de tarjetas (sugerido: por semáforo y luego por número de afirmaciones), agrupación, nombres: tuyos. Puedes ajustar los umbrales del semáforo si los datos lo justifican, siempre en el único sitio y declarado. PREGUNTA A MESA: ninguna. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) editar una vista a mano, el catálogo, el mapa, sellos · c) adoptar; teclear una cifra; mover un contador · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Ninguna cifra sin `derivado_de`» protege **adoptar** (E.4) · «Lo publica el canal» protege **borrar** (E.7) · «Vocabulario A.4 tal cual» protege **borrar** (deuda escondida como «no existe»).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `tools/tablero_carriles.py` + test huérfano, `canon/crosswalk-carriles-v1_0.tsv` (registrado), `forense/tablero/TABLERO-CARRILES.md`, `docs/tablero-carriles.html`, enlaces en README y `docs/index.md`, una línea en el job de derivados, nota, L0, cascada. Ajeno: `TABLERO-PROGRAMA.md` (se enlaza, no se edita), vistas de `data/corrida0/`, `canon/catalogo-*`, `canon/mapa-*`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no adopta, no descarga, no cierra stoppers (los muestra con su sucesor). Sucesores: cada corte semanal lo regenera por el canal; `TABLERO-CARRILES-2` si mesa pide vistas nuevas tras usarlo una semana. Sin módulo de auditoría (no afirma sobre México: muestra el estado del programa). El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-TABLERO-CARRILES-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

| qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| «el canal lo publica (un `[deriva]` con el tablero nuevo, run_id en la nota)» | DIFERIDO-A: primer run del job derivados tras el merge de mesa (el job corre en el push a `main`; antes del merge no hay run que citar) | el tablero regenera idéntico en la rama (`--verifica` CASA) pero ningún `[deriva]` lo ha publicado todavía | GEN2-TABLERO-CARRILES-2 o el `/tramite` siguiente asienta el run_id · `NC-260928-GEN2-TABLERO-CARRILES-1-e2eb-01` |

## CONSUMIDO

Consumido por el PR #1300 (rama `claude/new-session-9hwjgo`), ACTO GEN2-TABLERO-CARRILES-1, ADR `ADR-260928-GEN2-TABLERO-CARRILES-1-e2eb-01`, nota `forense/notas/2026-09-28-GEN2-TABLERO-CARRILES-1-cierre.md`. Sin adendas.
