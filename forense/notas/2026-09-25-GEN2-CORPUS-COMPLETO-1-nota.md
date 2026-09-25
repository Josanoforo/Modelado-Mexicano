# GEN2-CORPUS-COMPLETO-1 · nota de cierre (25/sep/2026)

**Contadores.** Cero mediciones; no adopta; no abre microdato. Mueve el manifiesto: **4 574 payloads nuevos** (17.62 GB; ids `cc1_*`), 4 436 en `data_raw` y **138 en `reserva_respondentes`** con `estado_reserva: RESERVADA-NO-ABIERTA-NO-INDEXAR-L`. Mueve la cola: **716 filas** `CORPUS-COMPLETO-1:<PROGRAMA>_<OLA>`, las 716 en `OBTENIDO`. Mueve la hoja del mapa por derivador (columna nueva `instrumento_en_corpus`). Cifras derivadas por comando; ver §5.

## 1 · Entorno y sesión

- Rama `acto/gen2-corpus-completo-1`, worktree `~/mm-gen2-corpus-completo-1`, **CAJA** (`data/raw → /home/pc0/mm-corpus/raw`, payloads verificados en el corpus compartido). Opus 5.5, MODO AUTÓNOMO.
- La sesión se interrumpió por un apagón de la máquina después del 0-bis (`7813eb89`) y de un P1 parcial sin commitear; se retomó sobre el worktree intacto y el trabajo recuperado se commiteó primero (`8e6ef288`).
- Un ejecutor Sonnet (inventario de fuentes no INEGI), auditado por el supervisor: `catalogo.py --verifica` COINCIDE tras su entrega y sus filas se reclasificaron (CONEVAL: programas de cálculo y tablas, no microdato; ENSANUT: ya en corpus por U5; Banxico/CNBV: sin microdato individual).
- `ls /home/pc0/mm-corpus/raw | wc -l` → 510 (encargo §4).

## 2 · Discrepancias encargo↔repo (cláusula de autonomía, 1)

| Encargo | Repo / hallazgo | Resolución |
|---|---|---|
| `/adquiere` en tandas | La primera versión de la sesión (antes del apagón) bajaba del catálogo con un script propio, fuera de la cola. El titular lo señaló a mitad de sesión. | P2 se rehízo por el conducto: registro de la cola (`catalogo_a_cola.py`, escritor `upsert_fila`) → vista (`tools/vista_cola_adquisicion.py`) → caminante sobre la vista (`descarga.py`, sólo filas propias PENDIENTE/PARCIAL/NO-OBTENIDO) → manifiesto por apéndice (`registra.py`, mismo método que U5, sha y tamaño derivados con `tests/manifiesto.py`) → estado de cada fila (`cierra_cola.py`) → vista. La `/adquiere` interactiva camina 5 filas por invocación; 716 filas se caminaron con el caminante, hasta 9 procesos en paralelo por reparto de (programa, ola). |
| `hoja_a_cola.py` se reutiliza | Sus reglas normalizan el texto libre del mapa; el catálogo ya trae programa y ola normalizados | Se reutiliza su contrato (clave `fila_origen`, `upsert_fila`, A.8 por objeto: 9 objetos ya en cola de U5 u otros actos no se duplican); sus reglas no aplican. |
| «`grep -c 'estado_reserva: RESERVADA'` = número de programas con ola nueva (uno por programa)» | El manifiesto es por archivo: una ola reservada trae varios archivos (base, FD, catálogos) | INTERPRETACIÓN-DECLARADA: 19 programas con ola nueva reservada, 138 entradas. `grep -c` pasa de 31 (origin/main) a 169 = +138. |
| «las 768 MEDIBLE-CON-ADQUISICIÓN dejan de tener instrumento ausente» | La hoja derivada del mapa clasifica 605 de las 768 como `DOCUMENTACIÓN-SOLAMENTE` (prensa, informes, artículos): un catálogo de microdatos no las cubre. Sólo 163 son `ADQUIRIR`. | Se mide sobre las 163: **41** con instrumento y ola en corpus, **10** con el instrumento en otra ola, **112** sin instrumento en corpus. Va a NO-CORRIDO; el «Hecho» no se rebaja. El dictamen del mapa no cambia (§10: el acto no cambia dictámenes). |
| E.6 «ola más reciente de cada programa con historia» | Programas descontinuados (CAAS, ENG, ENCRIGE, MIGRACION 2002) tienen como «más reciente» una ola vieja que no estaba en corpus | Se reservó por la letra (conservador: reservar no abre). Mesa puede levantarlas por escrito. |

Reservadas al entrar (19): CAAS 2015, CNGF 2018, CNGMD 2019, CNPJ 2018, EIC 2025, EMAT 2024, ENBIARE 2025, ENCO 2026, ENCOAP 2025, ENCRIGE 2016, ENG 2009, ENOE 2026T2, ENSU 2026, ENVE 2018, INVESTIGACION 2024, MIGRACION 2002, MORTALIDAD 2022, NUPCIALIDAD 2022, SALUD 2025. De ellas sólo se leyó el directorio central del zip (A.7) o la firma de bytes; ningún tabulado ni comunicado.

## 3 · P1 · catálogo

`forense/analisis/corpus-completo/catalogo-v1_0.tsv` (`catalogo.py --verifica` COINCIDE): 5 056 filas, 148 programas (138 INEGI por la API `descargamasiva/lista/archivoscompaginacion`, `tipodocto=4`; 10 externos por inventario de portal). Columnas del encargo más `reserva_al_entrar`. `en_manifiesto` refleja el manifiesto antes del acto (excluye `cc1_*`). Siete páginas crudas eran bytes idénticos bajo otra URL (T02): se conserva una por grupo y `crudo/DUPLICADOS.tsv` mapea nombre retirado → conservado con su sha256.

## 4 · P2 · adquisición

Bitácora `bitacora-descargas.tsv` (append-only, un intento por fila): 4 724 OK, 18 FALLO, 9 RECHAZADO-ESTRUCTURA, 31 DESTINO-OCUPADO-OTRO-SHA, 1 A7-DIFIERE, todos resueltos en reintento salvo lo que ya estaba en otra fila. Defectos del caminante encontrados y corregidos en la sesión: `.xls` OLE2 y `.csv` rechazados por la verificación de estructura; rutas INEGI con espacio literal (CNPJE/CNIJE 2012); CONEVAL corta `http` y sirve `https`; homónimos entre módulos (`m2/`, `m5/`, `iltefm/` vs `ilm/`) que caían en el mismo destino. INEGI cortó TLS mientras la salida de red de la máquina era una VPN en EE. UU. (datacenter); con salida MX respondió; después limitó la velocidad por volumen (~5 KB/s por conexión nueva) sin cortar. 136 archivos del catálogo ya estaban en el manifiesto por sha bajo otro id: no se duplicaron.

## 5 · P3 · verificación y mapa

- `python3 tests/manifiesto.py --verifica` (salida en `verificacion-p3.txt`): de las 4 574 entradas `cc1_*`, **4 436 COINCIDE** en `data_raw`; las **138** de `reserva_respondentes` salen `FUERA_DE_PERIMETRO` por diseño y se verificaron por sha directo: **138 COINCIDE, 0 DISCORDANTE, 0 AUSENTE**.
- Mapa: `ensambla_mapa.py` lee `cobertura-mapa-v1_0.tsv` (derivada por `cobertura_mapa.py` de la cola OBTENIDO y el catálogo, sobre `instrumento_ola`, no sobre la pieza: la pieza nombra alternativas descartadas) y publica `instrumento_en_corpus` en `hoja-adquisicion-derivada-v1_0.tsv`. `ensambla_mapa.py --verifica` y `hoja_a_cola.py --verifica` pasan. El canon `mapa-dominios-v1_0.tsv` no cambia.

## 6 · P4 · tabla final

`tabla-final-v1_0.tsv` (`tabla_final.py --verifica` COINCIDE): 146 programas; 131 con olas adquiridas por este acto; 19 con ola reservada; 8 con NO OBTENIDO o NO-APLICA. NO OBTENIDO POR ESTE AGENTE EN 1 INTENTOS, con receta en la tabla: Latinobarómetro (login), LAPOP (cuenta Vanderbilt), WVS y EVS (formulario de términos), EMOVI 2011/2017/2023 (formulario CEEY), Pew Religion in Latin America 2014 (login y reto anti-bot). NO-APLICA: Banxico y CNBV no publican microdato individual. Ya en corpus por otros actos: ENSANUT (U5), Latinobarómetro 2023 (U5), WVS México y LAPOP (cola previa).
