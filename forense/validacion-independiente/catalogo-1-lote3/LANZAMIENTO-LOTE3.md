# Lanzamiento del lote 3 de C1 · ACTO GEN2-ASTRA6-C1-LOTE-3

Escrito por la sesión receptora **antes** de entregar ningún paquete. Commit de este archivo = «paquete con sha antes de entregar» (E.2, §8 del encargo). Este archivo no contiene valores sellados; la receptora no los ha abierto.

## 1 · Universo del encargo contra el árbol (P1)

El encargo pide 56 + 92 + 312 = 460 identidades, tomadas de `catalogo-1-ejecucion-lote2`, `-entradas-residuales-lote2` e `-impedimentos-lote2`. Medido sobre `16ba3d02`:

| Grupo | Fuente en el árbol | Instrumentos | Llaves |
|---|---|---|---|
| 56 «no se reconstruyeron» | `lote2-tabla-estimadores.tsv`, `estado_punto = NO-RECALCULABLE-DESDE-SPEC` | ENBIARE 2021 54 · ENIGH 2022 1 · ENCUCI 2020 1 | 56 |
| 92 «apartadas» | misma tabla, `apartado_por_adenda = True` | ENDIREH 2016 (`endireh-pisos-2016-pareja-fisica-0002`) | 92 |
| 312 «residuales» | `catalogo-1-entradas-residuales-lote2/p1/tabla-llave-componente.tsv` | ENBIARE 180 · ENCODAT 2016 130 · ENCUCI 1 · ENIGH 1 (componente IC; 56 también con punto) | 312 |

**Premisa que cae:** el encargo llama a las 312 «residuales de ENDIREH». En el árbol hay cero filas ENDIREH entre ellas (`grep -c ENDIREH residuales-p4-original-sucesor.tsv` → 0). Además, las 56 son un subconjunto de las 312: la unión es de **404 llaves**, no de 460. No se cambia qué se mide: cada llave pasa por los cuatro gates y la regla del propio encargo (P0: «un gate que no cierra deja el paquete `NO-LANZADO (gate)`») decide.

## 2 · Gates por paquete

| Paquete | Llaves | APTO-TECNICAMENTE | CONTEXTO-NUEVO-ACREDITADO | CONTRATO-FIRMADO | ACCESO-AUTORIZADO | Estado |
|---|---:|---|---|---|---|---|
| `endireh-pisos-2016-pareja-fisica-0002` (c1-ventana-v1) | 92 | **SÍ**: contenedor `6ce9c8a5…a555` (#1203), manifiesto de entrada con sha antes de entregar (`entrada/allowlist.json`, sha canónico `7f467a4a…4a58`), tolerancia previa del paquete (`abs 1e-10`, flotante), suite v3 15/15 OK en CAJA | **SÍ sujeto a auditoría**: firma `26a2-02` (ADENDA-1); aislamiento acreditado por tres sondas con control positivo (§4); el transcript se audita antes de abrir sellados | **SÍ**: `26a2-01` (ADENDA-1), sha `821a5ecb…94eb` verificado | **SÍ**: `ee49-02` (ADENDA-1 de RECIBO-ASTRA6-2), TB_SEC_XIII `P13_1_1..9`, `P13_3_1..9` + auxiliares | **LANZADO** |
| `enbiare-pisos-bienestar-0001` (residuales v2) | 180 | residual v2; contrato sucesor sin firma (fb50-01, 1653-01) | — | — | **NO**: ninguna firma de acceso C1 para ENBIARE en este acto | **NO-LANZADO (gate)** |
| `encodat-pisos-sustancias-0001` (residuales v2) | 130 | contrato IC sucesor sin firma (157c-01) | — | — | **NO** | **NO-LANZADO (gate)** |
| `encuci-0001` (residuales v2) | 1 | — | — | — | **NO** | **NO-LANZADO (gate)** |
| `enigh-0001` (residuales v2) | 1 | — | — | — | **NO** | **NO-LANZADO (gate)** |

`—` = no evaluado: basta un gate en NO para no lanzar.

## 3 · Receta de lanzamiento: opción A, sin broker

- **Sesión:** `claude -p`, modelo `claude-opus-5-5`, creada por `lanzamiento/lanza-aislado.sh`. Cada paquete se lanza en una sesión nueva sin historial.
- **Herramientas (lista cerrada):** `Bash, Read, Write, Edit, Glob, Grep`. Sin WebFetch, WebSearch, Agent, MCP (`--strict-mcp-config`) ni skills de usuario (`--restricted`).
- **Configuración:** `--restricted` ignora los settings de usuario, proyecto y local, y solo aplica `lanzamiento/settings-reconstructor.json`: sandbox de Bash activo, `allowedDomains: []`, lecturas fuera del directorio de trabajo bloqueadas, `autoMemoryEnabled: false` y `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- **Aislamiento del sistema de archivos:** la sesión corre en un namespace de montaje propio (`unshare`) con `/tmp` en tmpfs vacío. Sin esto, el `$TMPDIR` compartido `/tmp/claude-1000` (scratchpads de otras sesiones) era legible (sonda 2).
- **Directorio de trabajo:** `/home/pc0/c1-lote3-rec/<paquete>/`, fuera del repo. Contiene `paquete/` (solo lectura: contenedor ventana-v1 extraído, `CONTRATO-v3.md` y los dos miembros autorizados del ZIP) y `salida/`.
- **Delimitación de acceso:** por módulo, solo `TB_SEC_XIII.csv` y `TSDem.csv` del ZIP (extraídos byte a byte por la receptora sin parsearlos; el resto del ZIP no se entrega). Por campo, lo impone el prompt (`usecols`) y lo verifica la auditoría del código entregado.
- **Decisiones de formato (latitud §6):**
  - `resultado.json` lleva punto e IC de toda celda estimable. La publicabilidad (n, UPM, ancho, CV) va por llave en `diagnostico.json`, fuera de `filas`: el contrato v3 no tiene estado de publicabilidad, y en lote 2 `estado_publicabilidad` ya iba en columna propia.
  - Números como `repr(float)`.
  - La tolerancia v2 del comparador (`entrada/tolerancia-v2.json`, `{"abs":"1e-10","rel":"0"}`) es la traducción mecánica de `tolerancia.json` del paquete (`flotante`, `abs 1e-10`), fijada aquí antes de revelar.
- **Orden E.2:** la reconstructora termina y la receptora archiva su `salida/` y su transcript en el repo con sha, y commitea y empuja. Después vienen la auditoría del transcript, `runtime.freeze-export` (ancla externa) y `compare_v3 freeze`. Solo entonces se construye la referencia desde el sellado, se fija su sha y corre `compare_v3 compare`.

## 4 · Sondas de aislamiento (control positivo, antes del lanzamiento real)

Las tres son sesiones desechables, no reconstructoras. Sus transcripts están en `lanzamiento/sondas/`.

| Sonda | Configuración | Repo / corpus | `/tmp/claude-1000` ajeno | Red | Memoria / CLAUDE.md | Python |
|---|---|---|---|---|---|---|
| 1 | settings + `--restricted` | ocultos | **legible** | bloqueada (curl 000) | NO | numpy 2.3.5, pandas 2.3.3 |
| 2 | + `CLAUDE_CODE_TMPDIR` | ocultos | **legible** (la variable no cambia el TMPDIR del sandbox) | bloqueada | — | OK |
| 3 | + namespace con `/tmp` tmpfs | ocultos; en `/home/pc0` solo se ve su propio directorio | **vacío** (solo el directorio de la propia sesión) | bloqueada | — | OK |

Se lanza con la configuración de la sonda 3. Reserva, dicha también en el rótulo `CIEGA-POR-CONTEXTO-NUEVO`: el proceso `claude` sí sale a la red (API), y el aislamiento es de sandbox y namespace, no de broker.
