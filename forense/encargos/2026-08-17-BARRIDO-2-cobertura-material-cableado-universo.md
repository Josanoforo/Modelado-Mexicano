# ENCARGO BARRIDO-2 · cobertura material, cableado e integración fail-closed

- **SHA de redacción:** `f3873c25d12ec3e26730901dc257788011e5ceea`.
- **Entorno asignado:** caja Ubuntu/WSL2; todo proceso que abre, indexa, caracteriza o cura material corre bajo `unshare -Urn`. Git/GitHub quedan fuera del namespace material.
- **Entorno NO asignado:** checkout Windows divergido, `/home/pc0/Modelado-Mexicano-curador` y cualquier raíz distinta de `data_raw` / `descargas_mx`.
- **Estado:** `VIVO`.
- **Base real al lanzamiento:** `origin/main=f3873c25d12ec3e26730901dc257788011e5ceea`; coincide con la base verificada al redactar.
- **Worktree/rama:** `/home/pc0/Modelado-Mexicano-barrido2` · `codex/barrido-2`.
- **Raíces materiales autorizadas:** `data_raw=/home/pc0/mm-corpus/raw` · `descargas_mx=/mnt/c/Users/PC0/Descargas MX`. `Downloads` y otras carpetas quedan fuera.
- **Aislamiento verificado:** `unshare -Urn -- true` terminó 0; la conexión de control a `1.1.1.1:53` dentro del namespace falló con `PermissionError: [Errno 1] Operation not permitted`.

## Verificación de existencia · A.8

### 1 · Estructura

Leído contra `data/INFRAESTRUCTURA-v1_0.md` en la base real:

- Dominio 1 gobierna manifiesto/payload; BARRIDO-2 contabiliza pero no descarga.
- Dominio 3 gobierna snapshot, universo, inspección y ledger; BARRIDO-2 crea la sucesión multirraíz y E0/E1/E2 sin sobrescribir staging histórico.
- Dominio 4 gobierna propuestas e integración; BARRIDO-2 conserva `integrate.py` como vía fail-closed y no convierte cableado en credencial de escritura.
- Dominio 7 gobierna el ADR y su cascada.
- Dominio 8 gobierna este encargo y las notas.
- `INFRAESTRUCTURA-v1_0.md` no cubre todavía cableado BARRIDO-2; la decisión de mesa ordena actualizarlo al cierre, después de observar los mecanismos reales.

### 2 · Contenido

Comando ejecutado antes de crear o editar productos:

```text
forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md  NO-ENCONTRADO
.barrido2                                                                  NO-ENCONTRADO
data/cableado-universo-v1_0.tsv                                            NO-ENCONTRADO
data/curacion-universo/ledger-inspecciones-barrido2.tsv                    NO-ENCONTRADO
data/curacion-universo/reportes-inspeccion-barrido2-v1_0.tsv               NO-ENCONTRADO
data/curacion-universo/baseline-material-barrido2.json                     NO-ENCONTRADO
tools/curador_registro/build_cableado.py                                   NO-ENCONTRADO
```

Los objetos históricos `data/manifiesto.yaml`, `data/curacion-universo/snapshot-t0.json`, `data/curacion-registro/{relaciones,evidencias,utilidad-modelo,bootstrap-semantico}.tsv` e `INFRAESTRUCTURA-v1_0.md` sí existen. Se consumen como antecedentes o baseline; no satisfacen los productos BARRIDO-2.

### 3 · Cobertura retroactiva

Fechas de alta derivadas con `git log --diff-filter=A --follow`:

- manifiesto: 2026-07-29;
- relaciones/evidencias/utilidad-modelo: 2026-08-07;
- snapshot T0 y bootstrap semántico: 2026-08-10;
- índice de infraestructura: 2026-08-12.

BARRIDO-2 nace después de todas esas tablas. Por tanto, ausencia en ellas no demuestra ausencia material; W0 recensa las dos raíces y conserva por separado declaración, representación y contenido.

## Decisiones de mesa propagadas

1. **Privacidad:** adenda vigente, límite durable de 160 caracteres, prohibición de valores individuales/PII, `[REDACTADO-PRIVACIDAD]` y preservación de filas/estado constituyen política suficiente.
2. **M-APERTURA:** `SUPERADO POR BARRIDO-2 · decisión de mesa 2026-08-17`; sus 17 aperturas y entregables sobreviven como subconjunto obligatorio post-E2.
3. **Mantenimiento BARRIDO-2:** lista cerrada bajo ADR-70(d): snapshot multirraíz, inspección E2, validación offline, sincronización mecánica de bootstrap y vía fail-closed de capa 4. La vía de altas solo se implementa si aparece al menos una `PROPUESTA_ALTA` validada. T-CABLEADO pertenece a tests.
4. **FP-24:** sigue `ABIERTA`; la dependencia se determina propuesta por propuesta por necesidad real de resolver la regla pendiente de pares, nunca por pertenencia a los 20 IDs históricos.

## Verificación del archivo

Tras materializar este archivo, C0 ejecuta:

```bash
test -f forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md
rg -n '^# ENCARGO FINAL · ACTO BARRIDO-2$|^¿El proyecto quedó más cerca' forense/encargos/2026-08-17-BARRIDO-2-cobertura-material-cableado-universo.md
```

Resultado exigido y comprobado por el propio checkpoint: `EXISTE-SATISFACE`.

---

## Texto completo del encargo, verbatim

# ENCARGO FINAL · ACTO BARRIDO-2
## Cobertura material total + observación ciega E0/E1/E2 + cableado durable
## + absorción de M-APERTURA + capa 4 real + integración fail-closed

Fecha de redacción: 2026-08-17.
Base verificada al redactar:
origin/main = f3873c25d12ec3e26730901dc257788011e5ceea.

La base anterior es referencia, no constante. Al arrancar, haz fetch y deriva
el HEAD real. Si main avanzó, clasifica la deriva y actualiza el perímetro
antes de editar.

Este encargo autoriza crear worktree/rama, editar dentro del perímetro,
hacer commits por fases, empujar checkpoints validados y abrir un PR
borrador. NO autoriza fusionar el PR.

════════════════════════════════════════════════════════════════════════
0 · DECISIONES DE MESA INCORPORADAS EN ESTE LANZAMIENTO
════════════════════════════════════════════════════════════════════════

DECISIÓN MESA PRIVACIDAD BARRIDO-2:

La adenda vigente de BARRIDO-2, el límite durable de 160 caracteres,
la prohibición de valores individuales/PII, la redacción explícita
[REDACTADO-PRIVACIDAD] y la regla de preservar filas/estado constituyen
política operativa suficiente para este acto.

DECISIÓN MESA M-APERTURA:

M-APERTURA queda SUPERADO POR BARRIDO-2. Sus 17 aperturas y sus entregables
se conservan como subconjunto obligatorio de aceptación dentro de
BARRIDO-2. No se ejecuta un acto separado.

La información de que esos objetos pertenecen al subconjunto histórico
de M-APERTURA NO se entrega a los inspectores materiales ciegos. El
subconjunto se recupera y consume únicamente después del gate E2, durante
la fase semántica.

En el primer commit, propaga esta decisión al encargo vivo que contiene
M-APERTURA y marca específicamente su §6 como:

SUPERADO POR BARRIDO-2 · decisión de mesa 2026-08-17.

No borres su texto ni sus gates históricos.

DECISIÓN MESA MANTENIMIENTO BARRIDO-2:

Bajo la ventana vigente de ADR-70(d), se autoriza una lista cerrada de
mantenimiento estrictamente necesaria:

1. snapshot multirraíz;
2. inspección E2;
3. validación offline;
4. sincronización mecánica de bootstrap;
5. vía fail-closed de capa 4.

La vía de alta de relaciones nuevas solo se implementará si BARRIDO-2
produce al menos una PROPUESTA_ALTA validada.

T-CABLEADO pertenece a tests y no amplía esta lista.

La actualización documental de INFRAESTRUCTURA no es precondición para
abrir material. Se hace al cierre, después de observar qué mecanismos
terminaron existiendo realmente.

Antes de editar tools/curador_registro/, re-deriva contra el árbol si la
ventana de ADR-70(d) sigue abierta. Propaga esta decisión al siguiente ADR
disponible, sin anticipar su número. Si la ventana ya cerró de forma que
esta autorización no resulte suficiente, PARA y reporta la contradicción.

DECISIÓN MESA FP-24 · POLÍTICA DE PARES:

FP-24 sigue ABIERTA. Este acto NO adjudica la política pendiente.

La cifra histórica de 20 corresponde exclusivamente al conjunto que
ENLACE-2 dejó pendiente bajo su snapshot y su perímetro.

NO es denominador, máximo ni población congelada de BARRIDO-2.

Antes de integración semántica, BARRIDO-2 re-deriva desde el registro
vigente qué propuestas, si alguna, requieren materialmente la política
de pares aún no firmada.

Una propuesta queda bloqueada por FP-24 SOLO si su aceptación depende
de decidir la regla pendiente sobre pares.

No queda bloqueada únicamente porque:

- pertenezca a uno de los 20 IDs históricos;
- comparta necesidad_id con otra relación;
- exista otra fila de la misma fuente;
- históricamente haya sido llamada "gemela".

Si evidencia nueva permite adjudicar una relación de forma
fuente/objeto-específica sin invocar la política pendiente, se procesa
por la vía ordinaria.

Si para adjudicarla sí hace falta escoger cómo tratar el par, termina
como:

PROPUESTA_CAMBIO / REQUIERE_DECISION_FP24

y nunca como INTEGRADA mientras FP-24 siga ABIERTA.

El número final puede ser 0, menor que 20, 20 o mayor que 20.

Lo produce BARRIDO-2. No se preescribe.

Ningún script, prueba, schema o lista de tareas debe contener como regla
los 20 IDs históricos.

════════════════════════════════════════════════════════════════════════
1 · RESULTADO BUSCADO
════════════════════════════════════════════════════════════════════════

BARRIDO-2 debe producir:

1. cobertura material completa de data_raw y descargas_mx;
2. contabilización de todas las declaraciones del manifiesto;
3. E0/E1/E2 de toda representación físicamente disponible;
4. índice E2 neutral completo, local y auditable;
5. reportes neutrales durables y depurados;
6. cableado payload/representación/contenido ↔ N1-N33;
7. propuestas semánticas estructuradas y supervisadas;
8. absorción efectiva de las 17 aperturas de M-APERTURA;
9. capa 4 escrita por una vía real y fail-closed;
10. integración transaccional de propuestas aceptadas;
11. censo de explotación actualizado;
12. fuera-de-disco;
13. PRISMA material y semántico;
14. T-CABLEADO;
15. PR borrador, nunca fusionado por iniciativa del ejecutor.

No calcula coeficientes.
No modifica cifras del modelo.
No exige descubrir relaciones nuevas.
No descarga fuentes.
No usa red durante la apertura o curación del material.

Una salida válida puede contener cero PROPUESTA_ALTA.

════════════════════════════════════════════════════════════════════════
2 · ARRANQUE OBLIGATORIO
════════════════════════════════════════════════════════════════════════

Antes de editar, reporta:

1. ruta absoluta del clon base;
2. origin/main actual;
3. PR abiertos;
4. ruta absoluta del worktree nuevo;
5. rama;
6. HEAD;
7. git status --short;
8. estado de data/raw;
9. configuración de las dos raíces;
10. firma de entorno y aislamiento de red.

No uses el checkout Windows actual como base: su main está divergido.

No reutilices /home/pc0/Modelado-Mexicano-curador: contiene trabajo ajeno.

Comandos iniciales:

set -euo pipefail

B2_BASE=/home/pc0/Modelado-Mexicano
B2_WT=/home/pc0/Modelado-Mexicano-barrido2
B2_BRANCH=codex/barrido-2
B2_DATE="$(date +%F)"

cd "$B2_BASE"
git fetch origin --prune
git rev-parse origin/main
git status --short --branch

Consulta los PR abiertos mediante GitHub o gh. Si existe un PR que toca:

- data/manifiesto.yaml;
- data/curacion-registro/relaciones.tsv;
- data/curacion-registro/evidencias.tsv;
- data/curacion-registro/utilidad-modelo.tsv;
- data/curacion-registro/bootstrap-semantico.tsv;
- data/curacion-universo/**;
- tools/curador_registro/**;

declara la colisión y no abras material hasta delimitarla.

Crea un worktree nuevo:

test ! -e "$B2_WT"
git worktree add -b "$B2_BRANCH" "$B2_WT" origin/main
cd "$B2_WT"

cp "$B2_BASE/data/raices.local.yaml" data/raices.local.yaml

git log -1 --format='%H %s'
git status --short --branch

Verifica:

- data_raw = /home/pc0/mm-corpus/raw
- descargas_mx = /mnt/c/Users/PC0/Descargas MX

No incluyas Downloads ni otras carpetas.

Lee completos:

- AGENTS.md;
- instrucciones-proyecto vigente;
- ADR-66;
- ADR-70(d);
- ADR-84/85/86 vigentes;
- forense/encargos/convencion.md;
- forense/firmas-pendientes.tsv;
- encargo histórico de M-APERTURA;
- data/lista-apertura-enlace2-2026-08-14.tsv;
- data/INFRAESTRUCTURA-v1_0.md;
- herramientas que realmente vas a modificar.

No abras una auditoría general.

════════════════════════════════════════════════════════════════════════
3 · ARCHIVO DEL ENCARGO Y PRIMER CHECKPOINT
════════════════════════════════════════════════════════════════════════

Antes de abrir cualquier payload:

1. archiva este encargo completo, verbatim, en:

   forense/encargos/<fecha>-BARRIDO-2-cobertura-material-cableado-universo.md

2. incluye:
   - SHA de redacción;
   - entorno;
   - estado VIVO;
   - base real;
   - bloque de existencia A.8;
   - decisiones de mesa anteriores;
   - verificación de existencia del archivo;

3. propaga M-APERTURA como SUPERADO POR BARRIDO-2;

4. añade .barrido2/ a .gitignore si todavía no está protegido;

5. congela los schemas y contratos, sin abrir datos;

6. revisa el diff y ejecuta pruebas documentales relevantes;

7. crea el primer commit;

8. empújalo inmediatamente:

git push -u origin codex/barrido-2

Commit validado = checkpoint remoto.

No mantengas días de trabajo pesado únicamente en la caja.

Staging, texto completo, índices E2 locales, microdatos y logs nunca entran
al commit ni al push.

No abras todavía el PR si solo existe el archivo del encargo. Ábrelo como
borrador después del primer resultado material útil, preferentemente W0.

════════════════════════════════════════════════════════════════════════
4 · IDENTIDADES: NO COLAPSAR TRES OBJETOS
════════════════════════════════════════════════════════════════════════

Se mantienen tres identidades distintas:

payload_id:

- es id_manifiesto;
- identifica la declaración registrada;
- para un físico no declarado es NO-APLICA;
- no se inventa a partir de ruta o hash.

representacion_id:

- identifica una representación física;
- se deriva establemente de:

  root_id + ruta_relativa + sha256_observado

- formato recomendado: REP-<hash estable>.

sha256:

- identifica el contenido byte a byte;
- permite reutilización entre representaciones idénticas.

Para las representaciones físicas no declaradas:

payload_id = NO-APLICA

hasta que exista un alta legítima en el manifiesto.

Si una representación no declarada resulta semánticamente útil:

1. el inspector solo la caracteriza;
2. el supervisor propone PROPUESTA_ALTA_MANIFIESTO;
3. el líder valida procedencia, ruta, hash, tamaño y privacidad;
4. se registra por la vía legítima del manifiesto;
5. se actualizan manifest_sha y baseline material mediante una transición
   registrada;
6. recién entonces recibe payload_id real y puede integrar semántica.

No registres automáticamente las representaciones no declaradas.

════════════════════════════════════════════════════════════════════════
5 · POBLACIONES QUE DEBEN CERRAR
════════════════════════════════════════════════════════════════════════

Las cifras observadas al redactar son referencias preliminares:

- 631 entradas de manifiesto;
- 627 con archivo+sha;
- 4 sin archivo+sha;
- 672 representaciones físicas;
- 95 representaciones físicas no declaradas;
- 49 declaraciones fuera de disco.

No uses estas cifras como constantes de aceptación. Rederívalas en W0.

Deben cerrar por separado:

A. todas las declaraciones del manifiesto, incluidas las que no tienen
   archivo+sha;

B. todas las entradas con archivo+sha: población del censo explotable;

C. todas las representaciones físicas, declaradas o no;

D. todos los contenidos SHA únicos;

E. todos los objetos lógicos de cada representación abierta.

Las cuatro declaraciones sin archivo+sha deben aparecer con estado
administrativo terminal en T0/PRISMA aunque no pertenezcan al censo
explotable.

Las representaciones no declaradas reciben E0/E1/E2 igual que las demás.
Ninguna desaparece por carecer de payload_id.

════════════════════════════════════════════════════════════════════════
6 · RED CERO
════════════════════════════════════════════════════════════════════════

Git fetch, consultas GitHub, push y creación del PR ocurren fuera del
namespace material.

Antes de interpretar un fallo de conexión como aislamiento correcto,
demuestra primero que unshare funciona:

unshare -Urn -- true || {
  echo "ERROR: no se pudo crear namespace aislado" >&2
  exit 40
}

Después demuestra que el namespace no tiene salida:

if unshare -Urn -- python3 -c \
  "import socket; socket.create_connection(('1.1.1.1',53),2)"
then
  echo "ERROR: namespace permite red" >&2
  exit 41
fi

Todo proceso que abra, indexe, caracterice o cure material corre dentro
de unshare -Urn.

No pases --network.
No falsifiques network_habilitada.
La validación BARRIDO-2 debe exigir network_habilitada=false.

════════════════════════════════════════════════════════════════════════
7 · PRECONDICIONES TÉCNICAS ANTES DE W0
════════════════════════════════════════════════════════════════════════

Implementa solamente lo que desbloquea el engrane material:

1. snapshot_universe.py multirraíz;
2. respeto efectivo del campo raiz del manifiesto;
3. identidad separada payload/representación/contenido;
4. inspect_assets.py con E2 real;
5. validación material offline;
6. ledger reanudable;
7. partición disjunta de olas;
8. protección de staging y privacidad;
9. pruebas dirigidas de lo anterior.

No implementes todavía:

- sincronización de bootstrap;
- matching semántico;
- altas de relaciones;
- transformador de altas;
- integración semántica completa.

Bootstrap se implementa antes del gate semántico.

La vía de altas se implementa solo si después de supervisión existe al
menos una PROPUESTA_ALTA validada.

build_cableado.py no existe hoy. Si se crea, será ensamblador y validador
determinista. Está prohibido que decida semántica o haga matching
automático entre reportes y N1-N33.

Después de validar este commit:

git push

════════════════════════════════════════════════════════════════════════
8 · CONTRATO E0/E1/E2
════════════════════════════════════════════════════════════════════════

E0 · CONTABILIZACIÓN E INTEGRIDAD

Para cada declaración y representación:

- raíz;
- ruta relativa;
- existencia;
- tamaño;
- SHA-256 completo;
- extensión;
- magic bytes;
- legibilidad;
- integridad de contenedor;
- coincidencia con manifiesto;
- duplicación byte a byte;
- estado administrativo.

Estados mínimos:

PRESENTE-INTEGRO
PRESENTE-HASH-DIVERGENTE
PRESENTE-TAMANO-DIVERGENTE
FUERA-DE-DISCO
RAIZ-NO-CONFIGURADA
RUTA-INVALIDA
CORRUPTO
CIFRADO
FORMATO-NO-SOPORTADO
NO-DETERMINADO

E0 no cuenta como apertura.

E1 · APERTURA ESTRUCTURAL COMPLETA

Debe enumerar todos los objetos lógicos aplicables:

- miembros ZIP;
- contenedores anidados;
- hojas;
- tablas;
- columnas;
- páginas;
- secciones;
- formularios;
- diccionarios;
- value-label collections.

Cada objeto recibe objeto_logico_id estable basado en:

sha256 + localizador interno normalizado

Cada payload E1 termina en:

- estructura completa, o
- excepción específica por objeto.

E2 · CARACTERIZACIÓN NEUTRAL COMPLETA

E2 conserva, cuando exista:

- nombre de variable;
- etiqueta;
- texto de reactivo;
- definición;
- categorías;
- value labels;
- unidad;
- periodo;
- población;
- hoja/tabla/página;
- relación estructural entre objetos;
- frontera de inspección.

E2 no conoce N1-N33.

E2 no exporta:

- filas;
- valores individuales;
- PII;
- combinaciones individualizantes;
- conclusiones semánticas;
- extractos sensibles innecesarios.

Por formato:

ZIP:
- todos los miembros;
- detección zip-slip;
- central directory;
- expansión;
- anidados;
- una inspección por SHA.

PDF:
- todas las páginas, no las primeras cinco.

XLS/XLSX:
- todas las hojas;
- todas las tablas/diccionarios relevantes.

CSV/TSV:
- encabezado, esquema y conteo;
- no persistir filas.

DTA/SAV:
- variables, etiquetas, tipos, formatos, value labels y metadatos;
- no persistir observaciones.

DOCX:
- secciones, párrafos y tablas.

JSON/XML/HTML:
- estructura completa.

TXT/PHP/sin extensión:
- clasificación segura como texto o excepción.

════════════════════════════════════════════════════════════════════════
9 · ÍNDICE E2 COMPLETO Y REPORTE DURABLE
════════════════════════════════════════════════════════════════════════

La inspección produce dos capas distintas.

A. Índice E2 neutral completo, local y auditable:

.barrido2/private/e2-neutral-index.jsonl

- no versionado;
- solo lectura para curadores;
- sin filas individuales ni PII;
- conserva nombres, etiquetas, reactivos, categorías, páginas, tablas,
  localizadores y fronteras;
- incluye hashes de cada registro/lote;
- es suficiente para evitar falsos negativos por compactación.

B. Reporte neutral durable compacto:

data/curacion-universo/reportes-inspeccion-barrido2-v1_0.tsv

- versionable;
- texto máximo 160;
- privacidad aplicada;
- referencias al índice completo mediante IDs/hashes, nunca mediante ruta
  local durable;
- evidencia suficiente para auditoría compacta.

El curador recibe ambos:

- índice E2 completo, en solo lectura;
- reporte durable compacto.

No recibe microdatos crudos.

Está prohibido curar únicamente desde la versión recortada a 160 caracteres.

════════════════════════════════════════════════════════════════════════
10 · OLAS: PARTICIÓN, NO ETIQUETAS SOLAPADAS
════════════════════════════════════════════════════════════════════════

Primero clasifica cada representación aplicando esta precedencia:

W4 si es pesada o tiene riesgo de expansión;
si no, W3 si es ZIP;
si no, W2 si es PDF/XLS/XLSX/CSV/TSV/DTA/SAV/DOCX;
si no, W1.

W5 no es una clase inicial. Solo recibe excepciones/reintentos.

Una representación pertenece exactamente a una ola inicial.

El ledger debe demostrar:

- intersección de W1/W2/W3/W4 = vacío;
- unión W1∪W2∪W3∪W4 = universo físico de T0;
- W5 contiene únicamente referencias a representaciones ya asignadas.

Orden operativo recomendado:

1. W1 ligeros;
2. W2 documentos/tabulares;
3. W3 ZIP ordinarios;
4. W4 pesados/riesgosos;
5. W5 excepciones.

Concurrencia:

- W1: máximo 3;
- W2: máximo 3, PDF/XLS máximo 2;
- W3: máximo 2;
- W4: 1;
- W5: según formato, máximo 3.

Protecciones:

- leer central directory antes de extraer;
- no extraer ZIP completos por inercia;
- streaming por miembro;
- temp máximo min(50 GiB, 10% del espacio libre);
- miembro >8 GiB requiere excepción;
- ratio >200:1 requiere revisión;
- timeout;
- límite de memoria;
- una sola tarea pesada simultánea.

════════════════════════════════════════════════════════════════════════
11 · AGENTES Y CEGAMIENTO
════════════════════════════════════════════════════════════════════════

Usa agentes por etapas, con máximo cuatro slots totales.

ETAPA MATERIAL:

- líder;
- hasta tres inspectores ciegos.

Los inspectores reciben únicamente:

- representacion_id;
- payload_id o NO-APLICA;
- raíz/ruta;
- SHA;
- formato;
- profundidad;
- presupuesto;
- contrato neutral.

No reciben:

- N1-N33;
- necesidad_id;
- relacion_id;
- clasificaciones;
- términos semánticos;
- lista M-APERTURA;
- lista histórica de 20 FP-24.

Escriben únicamente en staging asignado.

ETAPA SEMÁNTICA, después del gate E2:

- líder;
- hasta tres curadores;
- supervisor semántico.

Los curadores reciben:

- índice E2 neutral completo;
- reportes durables;
- N1-N33;
- relaciones vigentes;
- evidencia vigente;
- subconjunto M-APERTURA;
- reglas de propuestas.

No editan baseline ni cableado.

El supervisor:

- reabre evidencia;
- comprueba propuesta↔reporte↔tarea;
- determina dependencia real de FP-24;
- valida/rechaza.

El integrador no interpreta contenido.

════════════════════════════════════════════════════════════════════════
12 · MUESTRA ADVERSARIAL
════════════════════════════════════════════════════════════════════════

Por ola:

max(3, ceil(5% de representaciones completadas)), máximo 20.

Si la ola tiene menos de 3, revisa todas.

Prioriza:

- primer lote de cada inspector;
- baja confianza;
- formato complejo;
- excepción;
- frontera inesperada;
- contenido semánticamente rico;
- promociones;
- negativos;
- propuestas FP-24.

Una evidencia inventada:

1. rechaza el lote;
2. pone en cuarentena inspector/parser;
3. amplía muestra;
4. repite el lote;
5. no invalida todo salvo contaminación general demostrada.

════════════════════════════════════════════════════════════════════════
13 · PRODUCTOS MATERIALES
════════════════════════════════════════════════════════════════════════

Obligatorios:

data/censo-explotacion-<fecha>.tsv
data/fuera-de-disco-v1_0.tsv
data/curacion-universo/ledger-inspecciones-barrido2.tsv
data/curacion-universo/reportes-inspeccion-barrido2-v1_0.tsv
data/curacion-universo/baseline-material-barrido2.json
PRISMA material

El censo es sucesor del de 2026-08-13.

Conserva primero sus columnas vigentes y añade al final:

sha256_observado
representacion_id
estado_e0
grado_inspeccion
objetos_logicos
frontera_inspeccion
reporte_neutral_ref
contrato_sha256
reporte_sha256

Población del censo explotable:

entradas vigentes de manifiesto con archivo+sha.

Las otras declaraciones aparecen en T0/PRISMA administrativo.

Los físicos no declarados aparecen en ledger/T0, tengan o no alta posterior.

fuera-de-disco lleva:

id_manifiesto
raiz
archivo
sha256_declarado
tamano_declarado
estado_observado
universo_busqueda
mecanismo
fecha
razon

No uses “no existe”.

Después de W0:

1. revisa;
2. ejecuta pruebas;
3. commit;
4. push;
5. abre PR borrador;
6. no lo fusiones.

════════════════════════════════════════════════════════════════════════
14 · REUTILIZACIÓN
════════════════════════════════════════════════════════════════════════

Reutiliza solo si coinciden:

- SHA completo;
- contrato;
- contract_sha256;
- parser;
- build/version;
- profundidad;
- frontera;
- report_sha256;
- privacidad;
- expediente verificable.

E2 satisface E1/E0.
E1 no satisface E2.

Representaciones con el mismo SHA comparten inspección, pero cada una
conserva su procedencia y representacion_id.

El T0 heredado y aperturas anteriores son candidatos de reutilización,
no verdad automática.

════════════════════════════════════════════════════════════════════════
15 · GATE MATERIAL Y DERIVA DE MAIN
════════════════════════════════════════════════════════════════════════

El gate material exige:

- todas las declaraciones en estado terminal;
- todas las representaciones en estado terminal;
- todo objeto E1 en E2 o excepción;
- muestra adversarial aprobada;
- índice E2 completo;
- reportes durables;
- privacidad;
- ledger consistente;
- partición exacta de olas;
- PRISMA reconciliado;
- red deshabilitada.

Congela baseline-material-barrido2.json con:

- SHA base;
- manifest_sha;
- roots config;
- inventario representación+SHA;
- parsers;
- contratos;
- reportes;
- excepciones;
- conteos;
- red=false.

Después de cerrar E2 y antes de semántica:

git fetch origin --prune

Compara:

BASE_MATERIAL..origin/main

Clasifica los cambios:

A. Cambió manifiesto/raíces/parser/contrato E2:
   invalida y reejecuta solo representaciones/formatos afectados.

B. Cambió relaciones/evidencias/N1-N33/canon semántico:
   conserva material por SHA y refresca baseline semántico.

C. Cambió algo ajeno:
   registra NO-INVALIDA y continúa.

No repitas 7.8 GB por un ADR ajeno.

Como la rama ya tiene checkpoints empujados, no rebasees ni reescribas
historial compartido.

Integra main mediante merge local:

git merge --no-edit origin/main

Si hay conflicto material, PARA.

Valida y empuja el merge:

git push

════════════════════════════════════════════════════════════════════════
16 · BOOTSTRAP ANTES DE SEMÁNTICA
════════════════════════════════════════════════════════════════════════

Ahora implementa sincronización mecánica de bootstrap.

Rederiva bootstrap-semantico.tsv completo desde el registro vigente.

No parches únicamente 48 filas.

Preserva vocabulario.

Añade una prueba dirigida y barata de sincronía en
tools/curador_registro/tests/.

Gate:

bootstrap derivado ↔ bootstrap versionado = 0 discrepancias.

No hace falta crear otro T numerado global.

Commit validado y push.

════════════════════════════════════════════════════════════════════════
17 · PROPUESTAS SEMÁNTICAS, NO MATCHER MÁGICO
════════════════════════════════════════════════════════════════════════

Flujo obligatorio:

E2 neutral completo
→ curadores
→ propuestas semánticas estructuradas
→ supervisor semántico
→ propuestas validadas
→ integrate.py
→ decisiones de integración
→ cableado final

No se permite:

reportes + N1-N33 → matching automático → cableado

Los curadores producen:

data/curacion-registro/ejecucion-semantica/barrido2/
propuestas-barrido2.tsv

Cabecera mínima:

propuesta_id
tarea_id
reporte_id
payload_id
representacion_id
sha256
objeto_logico_id
necesidad_id
reactivo_id
accion_propuesta
relacion_id_actual
veredicto_a4
evidencia_ref
frontera_semantica
confianza
requiere_decision_mesa
decision_mesa_id
dependencia_fp24
razon_gate
estado_supervision
supervisor_id
fecha

accion_propuesta:

ALTA
CAMBIO
SIN_CAMBIO
TERMINAL

Para cada propuesta:

requiere_decision_mesa = SI/NO
decision_mesa_id = FP-24/NO-APLICA
dependencia_fp24 = SI/NO
razon_gate = texto concreto o NO-APLICA

Consistencia:

dependencia_fp24=SI
si y solo si:
requiere_decision_mesa=SI
y decision_mesa_id=FP-24.

No se deriva FP-24 por pertenencia a lista histórica.

El supervisor debe escribir la prueba específica que justifica
dependencia_fp24=SI:

“aceptar esta propuesta exige decidir <regla pendiente de pares>”.

Si puede decidirse por evidencia fuente/objeto-específica, la dependencia
es NO aunque la relación pertenezca a los 20 IDs históricos.

════════════════════════════════════════════════════════════════════════
18 · ABSORCIÓN SEMÁNTICA DE M-APERTURA
════════════════════════════════════════════════════════════════════════

Solo después de E2:

1. lee data/lista-apertura-enlace2-2026-08-14.tsv;
2. deriva exactamente las 17 filas con payload ya disponible;
3. une por identidad vigente, no por subcadena;
4. comprueba que todas recibieron E2 o excepción;
5. asigna tareas semánticas a curadores;
6. produce propuesta/veredicto por cada una;
7. corrige capa4 al estado ganado por evidencia;
8. ninguna puede cerrar conservando INDEXADO-NO-DESCARGADO si el payload
   fue observado;
9. produce el PRISMA específico de estas 17;
10. conserva el vínculo al encargo histórico de M-APERTURA.

Los inspectores materiales nunca reciben la lista.

El número 17 sí es un subconjunto histórico de aceptación expresamente
absorbido por decisión de mesa; no es una regla general de FP-24.

════════════════════════════════════════════════════════════════════════
19 · INTEGRADOR: PROPUESTAS, NO CABLEADO
════════════════════════════════════════════════════════════════════════

No hagas que integrate.py consuma cableado-universo.tsv como orden de
mutación.

Conserva el diseño fail-closed actual:

- propuestas;
- reportes;
- tareas;
- snapshot;
- schemas;
- hashes;
- expediente verificable.

Interfaz lógica:

propuestas-barrido2.tsv
+ propuestas supervisadas
+ reportes
+ tareas
+ snapshot
+ baseline
→ integrate.py
→ decisiones/resultados de integración

El cableado es una proyección durable de decisiones y conocimiento.
No es credencial de escritura.

Antes de modificar integrate.py, lee su CLI y schemas reales. No inventes
flags sin implementar ni probar.

Implementa en esta fase la vía fail-closed de capa4.

Solo si existe al menos una PROPUESTA_ALTA validada:

- implementa high path;
- crea relación determinista;
- actualiza relaciones/evidencias/utilidad/baseline;
- añade pruebas;
- integra o rechaza fail-closed.

Si hay cero PROPUESTA_ALTA:

- no construyas high path;
- registra “0 altas propuestas”;
- continúa.

No existe requisito de producir relaciones nuevas.

Toda PROPUESTA_ALTA que exista debe terminar:

INTEGRADA
RECHAZADA_FAIL_CLOSED
CONFLICTO_MATERIAL
REQUIERE_DECISION_FP24, si aplica.

════════════════════════════════════════════════════════════════════════
20 · TRANSACCIÓN DE INTEGRACIÓN
════════════════════════════════════════════════════════════════════════

Para relaciones existentes/capa4:

1. validar propuesta↔reporte↔tarea↔snapshot;
2. verificar baseline y hashes;
3. escribir candidatos en staging;
4. validar todos juntos;
5. crear journal de hashes anteriores/nuevos;
6. aplicar reemplazos con rollback;
7. releer;
8. ejecutar baseline;
9. emitir decisiones de integración;
10. segunda ejecución con diff cero.

Para altas, si existen:

- relacion_id estable;
- duplicado rechazado;
- relaciones.tsv;
- evidencias.tsv;
- utilidad-modelo.tsv;
- bootstrap-semantico.tsv;
- baseline.json;
- todo coherente.

via_capa2.py sigue siendo la vía de promociones capa2/capa3.
T21 debe estar verde antes y después.

No editar TSV manualmente como sustituto.

════════════════════════════════════════════════════════════════════════
21 · CABLEADO DURABLE
════════════════════════════════════════════════════════════════════════

build_cableado.py, si se crea, solo:

- ensambla;
- proyecta decisiones;
- incorpora terminales;
- valida;
- ordena determinísticamente;
- escribe.

No decide correspondencias semánticas.

Producto:

data/cableado-universo-v1_0.tsv

Cabecera exacta:

payload_id
representacion_id
sha256_12
sha256
fuente_canonica
objeto_logico_id
necesidad_id
reactivo_id
texto_reactivo_recortado
grado_inspeccion
afirmacion_tipo
veredicto_a4
evidencia
frontera_inspeccion
reporte_neutral_ref
propuesta_id
relacion_id
semrun_id
requiere_decision_mesa
decision_mesa_id
dependencia_fp24
razon_gate
estado_integracion
cegamiento_roto
fecha
razon

Reglas:

- ninguna celda vacía;
- NO-APLICA / NO-DETERMINADO / [REDACTADO-PRIVACIDAD];
- texto durable ≤160;
- sha256 de 64 caracteres;
- sha256_12 es prefijo;
- una fila por representación/objeto/afirmación;
- bytes iguales conservan representaciones separadas;
- físicos no declarados: payload_id=NO-APLICA;
- si adquieren alta legítima, regenerar con payload_id real;
- cero cuotas;
- cero obligación de altas nuevas.

veredicto_a4:

EXISTE-SATISFACE
EXISTE-NO-SATISFACE
NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO
NO-ACCESIBLE
NO-DETERMINADO

estado_integracion:

NO_APLICA_TERMINAL
PROPUESTA_ALTA
PROPUESTA_CAMBIO
VALIDADA
INTEGRADA
RECHAZADA_FAIL_CLOSED
CONFLICTO_MATERIAL
REQUIERE_DECISION_FP24
NO_DETERMINADO

SIN-DEMANDA-CONFIRMADO exige:

- E2 completo;
- revisión N1-N33;
- universo/frontera;
- cero excepción material abierta;
- supervisor aprobado.

E1 nunca produce negativos semánticos.

════════════════════════════════════════════════════════════════════════
22 · T-CABLEADO
════════════════════════════════════════════════════════════════════════

Deriva el siguiente número T disponible. No heredes T23 de memoria.

T-CABLEADO normal queda inactivo antes de existir el producto.

El cierre usa --require-cableado.

FAIL por:

- archivo inexistente bajo --require-cableado;
- solo cabecera;
- payload_id ausente;
- representacion_id ausente;
- SHA inválido;
- sha256_12 incorrecto;
- celda vacía;
- texto >160;
- evidencia requerida ausente;
- reporte neutral no dereferenciable;
- negativo sin frontera;
- SIN-DEMANDA-CONFIRMADO sin E2;
- INTEGRADA con relacion_id inexistente;
- INTEGRADA sin decisión verificable de integrate.py;
- propuesta/reporte/tarea sin join;
- físico no declarado con payload_id inventado;
- inconsistencia entre requiere_decision_mesa, decision_mesa_id y
  dependencia_fp24;
- propuesta con dependencia_fp24=SI e INTEGRADA mientras FP-24 esté
  ABIERTA;
- cualquiera de las 17 aperturas absorbidas que conserve
  INDEXADO-NO-DESCARGADO teniendo payload observado.

T-CABLEADO no conoce:

- los 20 IDs históricos;
- un denominador esperado de FP-24;
- una cuota de relaciones;
- una cuota de altas.

Añade una prueba negativa que demuestre:

- una relación del conjunto histórico de 20, decidible por evidencia
  específica y dependencia_fp24=NO, puede integrarse ordinariamente;

y otra que demuestre:

- cualquier propuesta, histórica o nueva, con dependencia_fp24=SI no
  puede quedar INTEGRADA mientras FP-24 esté ABIERTA.

WARN únicamente por conteos:

- CONFLICTO_MATERIAL;
- NO_DETERMINADO;
- REQUIERE_DECISION_FP24;
- propuestas no integradas.

No fallar por tener 0, 5, 20 o 30 propuestas FP-24. Solo importa la
consistencia individual.

════════════════════════════════════════════════════════════════════════
23 · PRISMA
════════════════════════════════════════════════════════════════════════

PRISMA material:

- declaraciones totales;
- con archivo+sha;
- sin archivo+sha;
- representaciones físicas;
- SHA únicos;
- declaradas;
- no declaradas;
- fuera de disco;
- divergentes;
- corruptas;
- cifradas;
- no soportadas;
- reutilizadas;
- abiertas E1;
- caracterizadas E2;
- excepciones;
- objetos lógicos;
- reportes.

PRISMA semántico:

- objetos revisados;
- propuestas;
- ALTA;
- CAMBIO;
- SIN_CAMBIO;
- TERMINAL;
- EXISTE-SATISFACE;
- EXISTE-NO-SATISFACE;
- negativos;
- SIN-DEMANDA-CONFIRMADO;
- dependencia_fp24=SI;
- FP-24 integrables ordinariamente;
- validadas;
- integradas;
- rechazadas fail-closed;
- conflictos;
- no determinadas.

PRISMA M-APERTURA absorbido:

- 17 esperadas;
- observadas E2;
- propuestas;
- capa4 corregida;
- excepciones;
- pendientes.

Toda cifra declara denominador y comando.

════════════════════════════════════════════════════════════════════════
24 · PRIVACIDAD
════════════════════════════════════════════════════════════════════════

Versionable:

- censo compacto;
- fuera-de-disco;
- ledger compacto;
- reportes neutrales compactos;
- propuestas depuradas;
- decisiones;
- cableado;
- PRISMA;
- schemas;
- hashes;
- pruebas;
- expedientes de integración depurados.

Local, auditable, gitignored:

- índice E2 completo;
- contratos por tarea;
- reportes completos;
- texto extraído;
- inventarios internos;
- muestras adversariales;
- logs;
- mapas privados de supervisión.

Efímero:

- miembros extraídos;
- cachés;
- temporales.

Prohibido:

- filas de microdatos;
- valores individuales;
- PII;
- combinaciones individualizantes;
- credenciales;
- rutas absolutas durables;
- snippets sensibles innecesarios.

Nunca elimines una fila por privacidad.
Conserva estado y usa [REDACTADO-PRIVACIDAD].

════════════════════════════════════════════════════════════════════════
25 · COMMITS Y PUSHES
════════════════════════════════════════════════════════════════════════

No congeles una cantidad fija de commits. Usa fases coherentes.

Secuencia recomendada:

C0:
- A.3;
- decisiones;
- M-APERTURA SUPERADO;
- contratos/schemas;
- privacidad;
- .gitignore.

C1:
- multirraíz;
- identidades;
- E2;
- offline;
- ledger;
- partición de olas;
- pruebas materiales.

C2:
- W0;
- censo;
- fuera-de-disco;
- baseline material preliminar;
- PRISMA W0.

C3:
- W1-W5;
- índice E2;
- reportes;
- excepciones;
- PRISMA material;
- baseline material congelado.

C4:
- merge de origin/main si avanzó;
- bootstrap sync;
- tareas semánticas;
- propuestas;
- supervisión;
- FP-24 derivado;
- M-APERTURA absorbido.

C5:
- capa4 fail-closed;
- high path solo si hay PROPUESTA_ALTA validada;
- integración;
- decisiones;
- idempotencia.

C6:
- cableado final;
- T-CABLEADO;
- PRISMA total;
- INFRAESTRUCTURA actualizada;
- cierre.

Puede haber commits adicionales por formato, ola o corrección material.
No comprimas artificialmente cambios grandes.

Después de CADA commit coherente y validado:

git push

No empujes staging ni datos sensibles.

Abre PR borrador después de W0 o del primer resultado material sustantivo.
Manténlo borrador.
Nunca lo fusiones.

Antes de cada commit:

- git diff;
- pruebas relevantes;
- privacidad;
- perímetro;
- git diff --check.

════════════════════════════════════════════════════════════════════════
26 · PRUEBAS MÍNIMAS
════════════════════════════════════════════════════════════════════════

Pruebas dirigidas:

- snapshot multirraíz;
- raiz respetada;
- payload_id vs representacion_id vs SHA;
- cuatro declaraciones sin payload;
- físico no declarado;
- ruta duplicada/dos SHA;
- fuera de disco;
- olas disjuntas y exhaustivas;
- reuse exacto;
- invalidación por parser/contrato;
- E2 por formato;
- ZIP anidado/riesgoso/corrupto/cifrado;
- privacidad;
- red cero;
- índice E2 completo;
- compactación durable;
- bootstrap sync;
- propuestas↔reportes↔tareas;
- ensamblador sin matching semántico;
- FP-24 dinámico;
- M-APERTURA 17;
- capa4 fail-closed;
- high path condicional;
- transacción/rollback;
- idempotencia;
- T-CABLEADO.

Cierre:

python3 -m unittest discover \
  -s tools/curador_registro/tests \
  -p 'test_*.py'

python3 tests/check.py --baseline
python3 tests/check.py --require-cableado
git diff --check
git status --short

No recongeles tests/baseline.json hasta haber derivado la nueva salida real
y comprobar que los cambios provienen de este acto.

════════════════════════════════════════════════════════════════════════
27 · CRITERIOS DE PARADA
════════════════════════════════════════════════════════════════════════

PARA si:

- falta una raíz;
- unshare no funciona;
- el namespace tiene red;
- aparece PII;
- cambia material concurrentemente;
- un parser no puede declarar frontera;
- bootstrap no sincroniza;
- integrate.py requiere saltarse joins/hashes/schemas;
- capa4 solo puede escribirse manualmente;
- un alta necesita inventar identidad;
- una propuesta depende de FP-24 pero alguien intenta integrarla;
- el baseline cambia durante la transacción;
- una prueba de privacidad falla;
- hay conflicto con otro PR o acto.

No pares porque:

- main avanzó con cambios ajenos;
- data/raw es symlink;
- aparecen cero relaciones nuevas;
- aparecen cero dependencias FP-24;
- existen WARN conocidos;
- alguna propuesta es rechazada fail-closed.

════════════════════════════════════════════════════════════════════════
28 · CRITERIOS DE CIERRE
════════════════════════════════════════════════════════════════════════

BARRIDO-2 cierra únicamente cuando:

1. todas las declaraciones están contabilizadas;
2. todas las representaciones están terminales;
3. todos los objetos E1 tienen E2 o excepción;
4. el índice E2 completo existe localmente y está hasheado;
5. reportes durables pasan privacidad;
6. el censo reconcilia;
7. fuera-de-disco reconcilia;
8. PRISMA reconcilia;
9. bootstrap tiene cero deriva;
10. todas las 17 aperturas absorbidas terminaron;
11. toda propuesta semántica terminó;
12. toda PROPUESTA_ALTA existente terminó:
    INTEGRADA / RECHAZADA_FAIL_CLOSED / CONFLICTO_MATERIAL /
    REQUIERE_DECISION_FP24;
13. cero obligación de producir altas;
14. FP-24 se aplicó por dependencia real, no por lista histórica;
15. capa4 se escribió mediante vía real;
16. integración es idempotente;
17. cableado tiene filas reales;
18. T-CABLEADO está verde;
19. tests/check.py --baseline está verde;
20. checkpoints están empujados;
21. PR borrador existe;
22. nadie fusionó el PR.

Si quedan propuestas con REQUIERE_DECISION_FP24, el cierre puede ser:

COBERTURA-MATERIAL-COMPLETA
INTEGRACION-ORDINARIA-COMPLETA
DECISIONES-FP24-PENDIENTES=<n derivado>

No uses “integración semántica total” hasta que esas decisiones estén
adjudicadas.

════════════════════════════════════════════════════════════════════════
29 · COMUNICACIÓN FINAL
════════════════════════════════════════════════════════════════════════

Reporta primero:

1. qué cobertura nueva se produjo;
2. por qué importa;
3. qué decisiones habilita;
4. qué falta para usarla;
5. pruebas;
6. reservas materiales;
7. PRISMA;
8. FP-24 derivado;
9. resultado de las 17 aperturas;
10. propuestas altas y su destino;
11. commits/checkpoints;
12. URL del PR borrador.

No presentes volumen de trabajo como avance.

La pregunta final es:

¿El proyecto quedó más cerca de producir una explicación, medición,
decisión o modelo mejor?

Si la respuesta es no, no cierres.
