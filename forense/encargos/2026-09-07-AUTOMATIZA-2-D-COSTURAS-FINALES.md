ENCARGO · CIERRE-AUTOMATIZA-2 · COSTURAS FINALES
MODELO SUGERIDO
Claude Sonnet Ultracode
NATURALEZA
Micro-PR de cierre.
No abre `AUTOMATIZA-3`.
No rediseña arquitectura.
No busca nuevas automatizaciones.
Corrige únicamente dos defectos concretos encontrados en la revisión post-fusión de AUTOMATIZA-2:

1. orden imposible/inconsistente del cierre directo de `/acto`;
2. verificación incompleta del contenido del sidecar en `tools/sella_sha256.py`.

0 · AUTORIDAD Y ARRANQUE
`origin/main` vigente es la autoridad.
El último SHA observado por dirección durante la revisión fue posterior a #585/#586, pero NO se hereda como base de ejecución.
Al arrancar:

```bash
git fetch origin main
git rev-parse origin/main

```

Crear rama fresca desde ese SHA.
Re-derivar mediante las herramientas vigentes:

```bash
python3 tools/cierre_acto.py

```

No heredar ADR, FP ni rótulos de este encargo.
Aplicar `/acto` vigente y su cascada.
No fusionar el PR. Mesa fusiona.
1 · OBJETIVO
Cerrar dos costuras pequeñas que quedaron visibles después de fusionar:

* `AUTOMATIZA-2-A · BLINDA-HEAD-PR`;
* `AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR`;
* `AUTOMATIZA-2-C · SELLA-SIDECAR`.

La revisión confirmó que A/B/C funcionan y están fusionados.
No se reabre su diseño.
El objetivo es:

```text
AUTOMATIZA-2 funcional
        ↓
dos defectos concretos residuales
        ↓
microfix
        ↓
campaña cerrada

```

2 · PERÍMETRO
Archivos esperados
Primariamente:

```text
.claude/commands/acto.md
tools/sella_sha256.py

```

Y un test dirigido para el segundo defecto, preferentemente:

```text
tests/test_sella_sha256.py

```

si no existe ya una prueba equivalente utilizable.
Además de los archivos mecánicos que `/acto` obligue a tocar en su propia cascada:

* gobernanza;
* estado-programa;
* encargo archivado;
* T25 sólo si el test real lo exige.

No tocar

* corpus;
* `data/raw`;
* `descargas_mx`;
* browser `Downloads`;
* manifiesto;
* adquisición;
* relaciones;
* motor;
* scoring;
* tablero;
* cron;
* `tests/baseline.json` mediante freeze;
* CI;
* GitHub Actions;
* branch protection.

No corregir defectos incidentales fuera de este perímetro.
ELEMENTO 1 · CORRIGE EL ORDEN DEL CIERRE DIRECTO DE `/acto`
3 · DEFECTO OBSERVADO
El guard final de HEAD introducido por AUTOMATIZA-2-A quedó correctamente cableado.
Pero `/acto` conserva una contradicción previa en su camino directo.
Hoy conceptualmente dice:

```text
8. añadir ## CONSUMIDO citando el PR
9. push y abrir el PR
10. guard final de HEAD

```

El número del PR no existe todavía en el paso 8.
Por tanto el ejecutor tiene que inferir una secuencia distinta a la que la skill declara.
`/despacha` ya resuelve correctamente este problema mediante dos fases:

```text
trabajo cerrado
→ push
→ abrir PR
→ obtener número
→ escribir CONSUMIDO
→ commit
→ push final
→ baseline
→ guard HEAD

```

El camino directo de `/acto` debe declarar la misma lógica.
4 · RESULTADO REQUERIDO
Reordenar únicamente la sección de cierre/entrega de:

```text
.claude/commands/acto.md

```

para que el camino directo quede explícito.
Secuencia objetivo:

```text
1. completar trabajo sustantivo
2. ejecutar cascada mecánica
3. commit
4. push de la rama
5. abrir UN PR
6. obtener número real del PR
7. añadir ## CONSUMIDO citando ese número
8. commit final de cierre
9. push final
10. tests/check.py --baseline después del último commit
11. tools/verifica_head_remoto.py
12. sólo si PR_HEAD_SINCRONIZADO → PR listo para mesa

```

No inventar número de PR.
No abrir segundo PR.
No fusionar.
5 · CAMINO BAJO `/despacha`
Conservar la excepción actual:
cuando `/acto` corre bajo `/despacha`:

* `/despacha` conserva propiedad de push;
* `/despacha` abre el PR;
* `/despacha` escribe estado/bitácora/`## CONSUMIDO`;
* `/despacha` corre el guard final.

No duplicar esos pasos desde `/acto`.
No modificar `.claude/commands/despacha.md` salvo que la inspección de `main` demuestre una contradicción real provocada por el cambio.
Por defecto:
cero cambios a `/despacha`.
6 · LÍMITE
Esto es una corrección de secuencia documental-operativa.
No:

* crear otro helper;
* modificar `verifica_head_remoto.py`;
* añadir workflow;
* tocar API de GitHub;
* automatizar apertura del PR;
* cambiar quién tiene autoridad de merge.

ELEMENTO 2 · ENDURECE `sella_sha256.py --verifica`
7 · DEFECTO OBSERVADO
`tools/sella_sha256.py` declara como contrato del sidecar:

```text
<64 hex minúsculas><dos espacios><basename>\n

```

una sola línea exacta.
Pero `--verifica` actualmente lee únicamente:

```python
linea = f.readline()

```

Por tanto un sidecar como:

```text
<HASH-CORRECTO>  spec.md
BASURA

```

puede aceptar la primera línea e ignorar contenido adicional.
Eso contradice el formato que la propia herramienta promete verificar.
La herramienta sella bien.
El defecto está únicamente en la validación.
8 · RESULTADO REQUERIDO
`--verifica` debe validar el contenido completo del sidecar.
Aceptar únicamente si el archivo es exactamente:

```text
<64 hex minúsculas><dos espacios><basename>\n

```

y nada más.
Debe rechazar como `SELLO_NO_COINCIDE`:

* segunda línea adicional;
* bytes/texto después del newline;
* falta de newline final;
* formato distinto;
* basename distinto;
* hash distinto;
* hash malformado.

No hace falta introducir nuevos exit codes.
Conservar:

```text
0 SELLO_COINCIDE
1 entrada rechazada
2 SIDECAR_AUSENTE
3 SELLO_NO_COINCIDE

```

9 · IMPLEMENTACIÓN MÍNIMA
Preferir leer el contenido completo:

```python
contenido = f.read()

```

y validar el contrato exacto.
Una solución simple puede:

1. calcular el basename esperado;
2. calcular el SHA real;
3. construir la línea canónica esperada:


```python
esperado = f"{sha_real}  {basename}\n"

```

4. comparar el contenido completo contra esa representación;

pero el diagnóstico actual distingue:

* formato;
* basename;
* hash;

y conviene conservar diagnósticos útiles si se puede hacer sin complejidad.
No hace falta construir un parser general.
10 · UNA PRUEBA PERMANENTE JUSTIFICADA
A diferencia del encargo original de C, ahora sí apareció un defecto concreto.
Por tanto se justifica una prueba dirigida permanente.
Debe proteger como mínimo:

```text
sidecar con primera línea correcta
+
segunda línea basura
→ SELLO_NO_COINCIDE

```

También conviene, si cabe en el mismo test sin inflarlo:

```text
línea correcta sin newline final
→ SELLO_NO_COINCIDE

```

No crear una batería exhaustiva.
Los casos ya verificados por C no necesitan reproducirse todos de nuevo salvo que el test actual ya los agrupe barato.
11 · NO CAMBIAR EL CONTRATO DE C
Conservar:

* sidecar = reemplazo de la última extensión;
* no `.md.sha256`;
* fuente explícita;
* no glob;
* no caminar directorios;
* no sellado recursivo;
* rechazo de directorios;
* rechazo de `.sha256` como fuente;
* escritura atómica;
* `--verifica` sólo lectura;
* no integración automática a `/acto`.

No convertirlo en sistema de firmas.
12 · COMMITS
Hacer idealmente dos commits.
COMMIT 1

```text
fix acto: ordena PR → CONSUMIDO → push final → guard HEAD

```

Sólo la costura del workflow directo.
COMMIT 2

```text
fix sella_sha256: valida el sidecar completo

```

Incluye la prueba dirigida.
Un único PR.
No dividirlo en dos PR porque ambas piezas son microfixes residuales de la misma revisión de cierre.
13 · VERIFICACIÓN
A. `/acto`
Releer el bloque resultante y comprobar que no existe ninguna instrucción que necesite el número de PR antes de abrirlo.
La secuencia debe ser inequívoca.
No hace falta test automatizado de Markdown.
B. Sellador
Correr al menos:

```bash
python3 tools/sella_sha256.py --verifica \
  forense/prereg-caja/S7-L17-spec-v1_1.md

```

Debe seguir produciendo:

```text
SELLO_COINCIDE

```

Elegir un segundo sidecar real como control.
Después ejecutar la prueba dirigida nueva.
C. Suite

```bash
python3 tests/check.py --baseline

```

Debe quedar sin regresión nueva.
D. Entrega
Después del último commit/push:

```bash
python3 tools/verifica_head_remoto.py

```

Debe producir:

```text
PR_HEAD_SINCRONIZADO
local=<sha>
remote=<mismo-sha>

```

Sólo entonces declarar el PR listo para mesa.
14 · NOTAS QUE NO DEBEN CONVERTIRSE EN TRABAJO
Durante la revisión aparecieron varias notas.
NO abrir trabajo por ellas:
Dictamen faltante en sesiones A/B/C
No material.
Las precisiones del dictamen terminaron implementadas en el producto.
No reconstruir trazabilidad histórica.
Reporte final prometido por C
No crear documento nuevo.
La revisión post-fusión ya verificó el producto final.
`RENUMERA-DIAGNÓSTICO`
Sigue descartado.
Sin código.
Sin nota.
E4 corrida natural
La prueba end-to-end del cron queda para la ventana natural del:

```text
1–3 octubre 2026

```

No descargar varios GB para verificar este microfix.
PR #586
El marcador huérfano del tablero era preexistente y ya fue retirado.
No pertenece a este acto.
15 · PARO
PARO si:

* corregir el orden de `/acto` exige modificar arquitectura de `/despacha`;
* aparece un segundo mecanismo de apertura de PR que vuelva ambigua la secuencia;
* validar el sidecar exacto rompe sidecars reales que no cumplen el formato declarado.

En este último caso:

1. no normalizar automáticamente;
2. listar los sidecars reales afectados;
3. determinar si el formato real difiere del contrato;
4. reportar a dirección antes de ampliar el cambio.

No convertir un caso inesperado en una migración masiva.
16 · CRITERIO DE ÉXITO
Costura `/acto`
Antes:

```text
CONSUMIDO necesita PR
↓
PR todavía no existe

```

Después:

```text
PR existe
↓
CONSUMIDO cita número real
↓
push final
↓
guard confirma HEAD remoto

```

Sidecar
Antes:

```text
primera línea correcta + basura
→ posible aceptación

```

Después:

```text
sidecar completo != formato canónico exacto
→ SELLO_NO_COINCIDE

```

17 · REGLA DE PARADA
Después de fusionar este micro-PR:
AUTOMATIZA-2 queda cerrada.
No buscar automáticamente otra pieza.
No abrir `AUTOMATIZA-3`.
El siguiente objetivo estratégico vuelve a trabajo de modelo.
Dirección ha señalado como siguiente frente sustantivo:

```text
M-POR-CELDA

```

porque el emisor del duelo todavía no convierte directamente las reglas medidas en movimiento del marcador por celda.
Ese trabajo tiene prioridad sobre cualquier nueva automatización preventiva.
REPORTE DEL PR
El cuerpo debe indicar:

1. los dos defectos concretos corregidos;
2. archivos exactos tocados;
3. prueba dirigida del sidecar;
4. resultado de `tests/check.py --baseline`;
5. evidencia final `local == remote`;
6. qué notas revisadas se declararon no materiales;
7. declaración explícita:


```text
AUTOMATIZA-2: CERRADA

```

No fusionar.
Mesa fusiona.
