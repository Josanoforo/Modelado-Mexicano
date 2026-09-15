ENCARGO · ACTO GEN2-SPECS-DEMANDA-2
Levantar lo levantable del mapa-19: cerrar la Capa 2 de CORR-0016/CORR-0017, suceder o declarar CORR-0007/CORR-0009, encadenar CORR-0010/CORR-0015 por identidad, y sondear lo que no tiene fuente (CORR-0018, CORR-0001, NO-HAY-DISEÑO-PÚBLICO)

CABECERA · redactado contra `da9b47a` (merge de #775 — `origin/main`, ya con `ACTO GEN2-SPECS-DEMANDA-1` y el mapa de las 19 dentro) · ENTORNO: **NUBE** — sin `data/raw`, corpus NO montado; el acto abre SOLO codebook y metadato (E.5), microdato JAMÁS; NO se lance en CAJA · COMPUERTA: ninguna declarada por el lanzamiento — los handoffs a la cola de adquisición quedan GATED al merge de `ACTO ADQUISICION-CONTINUA` (en vuelo, sin PR abierto hoy: `git ls-remote`/`search_pull_requests` sin resultado) · MODELO: Opus, integral · Estado: VIVO · candidatos FP/ADR: deriva al cierre.

LANZAMIENTO, verbatim (mesa, 15/sep/2026): el texto de PIEZAS de abajo es el mensaje de lanzamiento tal como llegó; este archivo lo fija por A.3 porque llegó pegado en el mensaje que invocó `/acto`, no como archivo del repo.

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por el ejecutor contra `da9b47a`):

(1) ¿Existe ya la estructura? SÍ. `data/corrida0/mapa-demanda-19-corr-v1_0.tsv` (registrado en `data/INFRAESTRUCTURA-v1_0.md:755`, escrito a mano por `ACTO GEN2-SPECS-DEMANDA-1`, no derivado — envejece y no se re-genera) gobierna el estado de las 19 `CORR` sin candidato; `data/corrida0/demanda-corridas.tsv` (línea 736 de `INFRAESTRUCTURA`) es el derivado que lo alimentó; `forense/prereg-caja/` guarda las specs humanas selladas de `D-15` y `data/corrida0/CALC-*/spec.yaml` los contratos ejecutables; `milpa/procedencia.yaml:coeficientes_generador_sellados` gobierna los 7 coeficientes de `CORR-0018`; `forense/no-corrido.tsv` gobierna las `NC` abiertas por el acto anterior (`NC-0192`…`NC-0198`). Ningún hueco de índice que reportar.

(2) ¿Existe ya el contenido? Se re-verifica fila por fila contra el mapa, sin confiar en su fecha (el propio mapa advierte «no hay comando que la corrija»):
```
$ ls data/corrida0/ | grep -i CALC   # ninguna carpeta CALC-S7-L17, CALC-L8, CALC-ENVIPE-DENUNCIA-2, CALC-CORR0010, CALC-CORR0015
$ ls forense/prereg-caja/ | grep -i S7-L17
S7-L17-spec-v1_0.md  S7-L17-spec-v1_0.sha256  S7-L17-spec-v1_1.md  S7-L17-spec-v1_1.sha256
$ ls -la data/l8-resultados-tipo-boleta-v1_0.json
-rw-r--r-- 1 root root 43545 ... data/l8-resultados-tipo-boleta-v1_0.json
$ ls forense/prereg-caja/ | grep -i ENVIPE-DENUNCIA
ENVIPE-DENUNCIA-SEGURO-propuesta-v1_0.md  ENVIPE-DENUNCIA-spec-v1_0-CORRECCION-2026-09-15.md  ENVIPE-DENUNCIA-spec-v1_0.md  ENVIPE-DENUNCIA-spec-v1_0.sha256
$ ls forense/prereg-caja/ | grep -i ENIF-AHORRO
ENIF-AHORRO-control-gen1.py  ENIF-AHORRO-spec-v1_0.md  ENIF-AHORRO-spec-v1_0.sha256
```
Confirma el mapa sin drift: `CORR-0017` tiene **capa 1 sellada** (dos versiones) y **cero capa 2** (`spec.yaml`) — `SIN-CAPA-2` sigue vigente. `CORR-0016` tiene el payload como artefacto de repo y **cero spec** en ninguna capa. `CORR-0007`/`CORR-0009` tienen spec humana + `CALC` parcial (`CALC-ENVIPE-0001` releva 2/8, `CALC-ENIF-0001` releva 6/9) — `EXISTE-NO-SATISFACE` sigue vigente, sin re-especificar lo ya relevado (A.8). `CORR-0010`/`CORR-0015` siguen sin `CALC` propio — `BLOQUEADA` vigente. `CORR-0018` (`milpa/procedencia.yaml` prosa sin `payload_id`/hash/script) y `CORR-0001` (payload SÍ está, per `NC-0197`: el bloqueo es `DECISIÓN-DE-MESA` D1, no ausencia de fuente — la premisa de este lanzamiento que lo llama «ENCIG 2023 sin payload» queda corregida aquí antes de sondear nada) también siguen `BLOQUEADA` sin drift.

(3) ¿La estructura es posterior al trabajo? El mapa nació HOY (`15/sep/2026`, mismo día que este acto) contra `da9b47a`, recién fusionado: no hay ventana de tiempo en la que algo lo haya dejado atrás. `demanda-corridas.tsv` nació el 7/sep/2026; su brecha retroactiva ya la declaró `GEN2-SPECS-DEMANDA-1` y este acto no la reabre.

⚠️ Nada de (2)/(3) revela que el trabajo ya esté hecho: las seis `CORR` de P1–P3 y las tres candidatas de sonda de P4 siguen con el hueco exacto que el mapa nombra. El encargo se lanza.

PIEZAS (texto de mesa, verbatim)

> NUBE — secuencia, un solo grande ahora:
>
> 1. SPECS-DEMANDA-1 → tu merge (trae las tres decisiones armadas).
> 2. ACTO GEN2-SPECS-DEMANDA-2 · LEVANTAR LO LEVANTABLE DEL MAPA-19 (Opus, integral) — lanzable ya, sobre la rama del 1 hasta que fusione:
>    * P1 · Capa 2 faltante: CORR-0016 (SIN-CAPA-2) y CORR-0017 (FALTA-CAPA-2) → `spec.yaml` D-15 congelado, abriendo solo codebook/metadato. Dos specs más para caja.
>    * P2 · Las parciales: CORR-0007 y CORR-0009 (EXISTE-NO-SATISFACE) → sucesión que releve la corrida entera, o declaración explícita de qué parte no puede y por qué (con inventario por archivo, A.15).
>    * P3 · Identidad y encadenamiento: la CORR con IDENTIDAD-DE-PAYLOAD se resuelve contra el manifiesto por hash de contenido (A.7); CORR-0015 (DEPENDE-DE-CORRIDA-PADRE) se encadena a su padre con la condición escrita.
>    * P4 · Sonda sobre lo que no tiene fuente: `/sonda` (CONSTRUCTO/HERMANAS/LATERAL) sobre CORR-0018 (SIN-SCRIPT-NI-PAYLOAD), CORR-0001 (ENCIG 2023 sin payload) y la NO-HAY-DISEÑO-PUBLICO: candidatas con A.4/A.5, SIN-FETCH donde nube no abra, receta manual de un minuto donde haya credencial. ⚠️ Los handoffs a la cola quedan GATED al merge de ADQUISICION-CONTINUA — ese acto está rediseñando el SSOT de adquisición y escribirle encima ahora es duplicar; mientras, las candidatas se entregan como tabla por consumidor, que es exactamente el insumo que el servicio nuevo va a leer.
>    * Perímetro: `forense/prereg-caja/`, specs y sidecars, la nota, no-corrido. No toca cola, manifiesto, `tools/adq_*`, milpa, ni F5/F6. Entregable: N specs congeladas nuevas (munición de caja) + el mapa-19 actualizado. Contador propio cero, dicho sin disfraz; el contador lo mueve caja con lo que este acto le fabrica.

NOTA DE EJECUCIÓN (A.8, corrige la premisa antes de lanzar): la pieza 1 (`SPECS-DEMANDA-1 → tu merge`) ya está resuelta al escribir este archivo — PR [#775](https://github.com/Josanoforo/Modelado-Mexicano/pull/775) fusionado a `main` en `da9b47a`, CI verde, `mergeable_state=clean` verificado antes del merge. Este encargo por tanto NO corre «sobre la rama del 1 hasta que fusione»: corre directo sobre `main` porque el 1 ya fusionó. La CORR de P3 con `IDENTIDAD-DE-PAYLOAD` es `CORR-0010` (única fila del mapa con ese bloqueador exacto); la fila `NO-HAY-DISEÑO-PUBLICO` de P4 es `CORR-0008` (ENNViH/MxFLS olas 2-3) — identidad de payload ya corregida por `NC-0188`, pero sin diseño muestral publicado (`NC-0156`).

PERÍMETRO: `forense/encargos/2026-09-15-GEN2-SPECS-DEMANDA-2.md` (este archivo) · `forense/prereg-caja/` (specs y sidecars nuevos/sucesores) · `data/corrida0/CALC-*/spec.yaml` (capa 2 nueva) · `data/corrida0/mapa-demanda-19-corr-v1_0.tsv` (actualización de fila, no regeneración) · `forense/notas/` (nota de cierre y de sonda) · `forense/no-corrido.tsv` · `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv` (cascada). NO toca: `data/cola-adquisicion-v1_0.tsv` · `data/manifiesto.yaml` · `tools/adq_*` · `milpa/*` · `F5`/`F6` · ningún microdato · ningún CALC sellado ajeno a este acto.

CONTADOR: **cero mediciones propias** — dicho sin disfraz. Un acto de specs congeladas y candidatas de sonda produce contratos y tabla, no números; los números los produce la corrida en CAJA que consuma estos contratos.

LO QUE NO HACE: no corre ningún `CALC` · no abre un solo byte de microdato · no escribe en `data/cola-adquisicion-v1_0.tsv` ni en `tools/adq_*` (GATED a `ADQUISICION-CONTINUA`) · no toca `milpa/*` ni `F5`/`F6` · no adopta ninguna cifra a ningún consumidor · no edita specs selladas (las sucede, si hiciera falta) · no firma las decisiones D1/D2/D3 que `GEN2-SPECS-DEMANDA-1` dejó armadas.

CIERRE: cascada completa + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO` con el PR.
