<!-- RESCATADO POR MESA 15/sep/2026, verbatim de su conversación ChatGPT de origen («Revisar integración GitHub», 8/sep/2026, encargo ~20:02 UTC). Verificado por dirección contra base d48014ed y merge a800f299 (PR #632), que existen y coinciden. sha256 del adjunto: 2e8cab983ea935da00ddd29011902d6bd5f04c6ec820658023f93d0ca61c3c42. Archivado bajo ACTO GEN2-SANEA-REGISTRO-Y-RESCATE, cierra NC-0054. Sufijo
`-ENCARGO` en el nombre de archivo por T02 (tests/check.py): el nombre
limpio sin sufijo colisiona por normalización de nombre con la nota de
ejecución `forense/notas/2026-09-08-GEN2-SONDA-2-operacionaliza-sonda-lateral.md`,
ya viva en el árbol; son documentos distintos (encargo vs. nota de cierre
de #632) y el contenido de este archivo, tras esta cabecera, es verbatim
del adjunto rescatado. -->
# ACTO GEN2-SONDA-2 · OPERACIONALIZA-SONDA-LATERAL

**ESTADO:** CONSUMIDO — PR #632  
**FECHA:** 2026-09-08  
**ENTORNO DE EJECUCIÓN:** NUBE  
**BASE USADA POR EL ACTO:** `d48014ed8da3879459aeb234de2addd5a8a83ad3`  
**PR:** #632  
**MERGE:** `a800f29999028f25ed830215e5ed2180f04a57a7`

## Objetivo

Convertir en una capacidad reusable del proyecto la metodología de SONDA que ya fue ejecutada con éxito en actos anteriores.

No diseñar una metodología nueva. No abrir otra capa de gobernanza. No construir otro sistema de adquisición.

El producto principal es una interfaz reusable `/sonda` que permita que un `NO-ENCONTRADO`, una fuente bloqueada o un instrumento faltante no se conviertan accidentalmente en una afirmación global de inexistencia.

La sonda debe buscar fuera del universo inmediato examinado, registrar qué universo adicional exploró y entregar candidatas o handoffs concretos sin decidir por mesa ni modificar specs/modelo.

## 0. Autoridad y arranque

La autoridad es siempre `origin/main`.

Antes de diseñar nada:

1. `git fetch --prune`
2. Registrar el SHA vigente de `origin/main`.
3. Crear worktree/rama nueva desde ese SHA.
4. Leer el estado actual, sin heredar cifras ni estados del encargo.
5. Correr la línea base vigente antes de modificar archivos.

Nombre sugerido de rama:

```text
acto/gen2-sonda-2-operacionaliza-sonda-lateral
```

Nombre sugerido de PR:

```text
ACTO GEN2-SONDA-2 · OPERACIONALIZA-SONDA-LATERAL
```

Este acto es preferentemente NUBE:

- no requiere corpus;
- no abre microdato;
- no ejecuta CALC;
- no descarga payloads.

Si la red del entorno impide comprobar una candidata externa, declarar `SIN-FETCH` o equivalente vigente y continuar. Un bloqueo de NUBE no autoriza a concluir que la fuente no existe.

No gatear el acto esperando CAJA salvo que aparezca un bloqueo material que impida construir o validar la interfaz reusable.

## 1. Precedentes obligatorios

Antes de escribir `/sonda`, reconstruir brevemente la conducta ya demostrada por estos precedentes. No hace falta una auditoría exhaustiva ni revalidar cada URL histórica.

### A. PR #197 · `ACTO SONDA-1`

Patrón a extraer:

- fuentes que sólo habían sido contrastadas contra tablas internas;
- sondeo contra portal/fuente real;
- distinguir barrera, ausencia y falta de obtención;
- no descargar por defecto.

### B. PR #524 · `ACTO MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1`

Patrón a extraer:

- explorar explícitamente el “Universo desconocido”;
- buscar fuentes candidatas fuera de las ya inventariadas;
- separar `EXISTE-SATISFACE`, `EXISTE-NO-SATISFACE`, `NO-ENCONTRADO`, `PENDIENTE`/`SIN-FETCH` según el vocabulario vigente.

### C. Segunda ronda del PR #524 · `SONDA-LATERAL-PENDIENTES`

Patrón a extraer:

- una ruta oficial fallida no agota una fuente;
- buscar vías hermanas/laterales: repositorios institucionales, APIs, archivos históricos, mirrors, replication packages, formatos alternos y endpoints de datos subyacentes;
- verificar que el objeto encontrado sea realmente el instrumento/dato buscado, no sólo una página HTTP 200.

### D. PR #542 · `ACTO MAESTRA38-N12 · SONDA-INSTRUMENTOS-DE-PERCEPCION`

Patrón a extraer:

- partir de un instrumento/constructo faltante;
- explorar fuentes candidatas distintas;
- si NUBE no puede abrir una candidata, no convertirlo en negativo;
- handoff a adquisición/CAJA cuando proceda.

No copiar ceremonias particulares de esos actos. Extraer sólo comportamiento reusable.

## 2. Estado vigente que debe reutilizarse

Leer al menos:

```text
.claude/commands/mapea.md
.claude/commands/adquiere.md
tools/arbitra.py
tools/curador_registro/tsv_crudo.py
tools/curador_registro/registra_cola_adquisicion.py
tools/curador_registro/alta_relacion.py
tools/vista_cola_adquisicion.py
```

y cualquier archivo que esos módulos indiquen como SSOT actual.

Verificar, no suponer:

- SSOT de adquisición;
- escritor canónico;
- vista generada;
- vocabulario A.4/A.5 vigente;
- mecanismo vigente de aliases;
- forma vigente de regenerar la vista.

Hechos conocidos a comprobar en `main`:

- `data/cola-adquisicion-v1_0.tsv` es una vista generada.
- `tools/curador_registro/registra_cola_adquisicion.py` es migración legacy, no el escritor normal.
- Existe `tsv_crudo.upsert_fila(...)` como mecanismo canónico usado por `tools/arbitra.py`.
- Existe `tools/curador_registro/alta_relacion.py` para altas transaccionales de relaciones cuando corresponda.

Si `main` cambió estas interfaces, seguir `main`.

## 3. Decisión de diseño

No crear:

```text
tools/sonda_encola.py
```

No crear un segundo registro de candidatas, una segunda cola, una rutina/CRON nueva, una ontología paralela si sólo renombra el universo examinado/desconocido, un duplicado de `/adquiere` ni un descargador dentro de `/sonda`.

Producto principal:

```text
.claude/commands/sonda.md
```

y los cambios mínimos para que `/mapea` pueda recomendarla cuando un negativo material lo justifique.

Si para el handoff a adquisición hace falta escritura, reutilizar la interfaz canónica actual.

Antes de añadir cualquier helper nuevo, demostrar que no existe ya una vía suficiente.

## 4. Contrato de `/sonda`

Interfaz sugerida:

```text
/sonda <codigo> <definicion-verbatim> [modo]
```

Modos conceptuales:

### A. CONSTRUCTO

Pregunta: ¿Qué otras fuentes/instrumentos podrían medir esta definición que el universo actual no contiene?

Sirve para `NO-ENCONTRADO`, `HIPÓTESIS-SIN-INSTRUMENTO` y constructos que no aparecen en el inventario conocido. Debe buscar familias de fuente distintas y no sólo sinónimos dentro del mismo inventario.

### B. HERMANAS

Pregunta: ¿Existe otra ola, módulo, edición, repositorio, release, replication package o miembro de la misma familia que resuelva el hueco?

Sirve cuando existe la fuente/familia pero la ola presente no contiene la variable, hay cobertura temporal incompleta o existe un estudio adyacente que podría contener el instrumento.

### C. LATERAL

Pregunta: La fuente es conocida. ¿Existe otra vía legítima para llegar al mismo objeto?

Puede explorar API oficial, endpoint de descarga, metadata/JSON-LD, formato alterno, repositorio institucional, Dataverse/DSpace, replication package, archivo histórico, mirror legítimo, endpoints que alimenten visualizaciones públicas y documentación/codebook que revele la ubicación real.

Los modos pueden compartir una sola secuencia si eso resulta más simple. No forzar tres motores distintos sólo por conservar los nombres.

## 5. Disciplina del negativo

`/sonda` nunca puede transformar `no apareció en X` en `no existe` sin declarar qué universo adicional agotó.

Toda conclusión negativa debe incluir explícitamente:

- definición buscada;
- universo examinado;
- fuentes/familias exploradas;
- formulaciones o rutas usadas;
- qué no pudo abrirse;
- qué queda fuera del sondeo.

Usar el vocabulario vigente del repo. No inventar un vocabulario paralelo si A.4/A.5 ya expresa la situación.

Distinguir ninguna candidata satisfactoria, candidata existente pero insuficiente, candidata localizada pero no abierta, barrera técnica, barrera de credencial/costo, fuente pendiente de adquisición y ausencia comprobada sólo dentro del universo sondeado.

Un fallo HTTP, TLS, Cloudflare, WAF, login de interfaz o navegador no prueba inexistencia. Un HTTP 200 tampoco prueba existencia del payload.

## 6. Relación con `/mapea`

Hacer un cambio mínimo en `.claude/commands/mapea.md`. No reescribir `/mapea`.

Conservar su función actual: buscar reactivos dentro del universo indexado y proponer, no decidir.

Cuando el resultado sea materialmente `NO-ENCONTRADO`, o sólo haya `EXISTE-NO-SATISFACE`, y la ausencia pueda cambiar una medición, spec, regla o parámetro, la recomendación debe poder terminar en algo equivalente a:

```text
SONDA-RECOMENDADA:
ejecutar /sonda sobre <código> <definición verbatim>,
porque el negativo sólo agota <universo examinado>.
```

No disparar SONDA por cualquier cero irrelevante. No convertir cada `NO-ENCONTRADO` histórico en una nueva tarea.

## 7. Handoff a adquisición

`/sonda` no reemplaza `/adquiere`.

```text
/mapea
   ↓
negativo material en universo conocido
   ↓
/sonda
   ↓
candidata concreta
   ├─ ya disponible/indexada → reportarla
   ├─ necesita adquisición → handoff a cola vigente
   ├─ requiere CAJA/manual → PENDIENTE/SIN-FETCH + receta
   └─ no aparece → negativo limitado al universo sondeado
```

Si `/sonda` descubre una fuente concreta que requiere adquisición:

1. A.8 contra manifiesto/registro antes de crear nada.
2. Resolver alias con el mecanismo vigente.
3. Evitar duplicados.
4. Si procede encolar, escribir en el SSOT actual mediante el escritor canónico.
5. Regenerar la vista con el mecanismo vigente.
6. Dejar procedencia suficiente para saber qué sonda la descubrió, qué definición intentaba cubrir, URL/fuente candidata, por qué es candidata y qué falta verificar.

El alta en la cola no significa `EXISTE-SATISFACE`, relación `CONFIRMADA` ni resultado adoptado. Sólo significa que vale la pena intentar adquirir/verificar la candidata.

## 8. Piloto real

Después de construir `/sonda`, seleccionar como máximo tres huecos materiales reales vigentes en `origin/main` y re-derivarlos en ese momento.

Buscar candidatos entre no-corrido vigente, specs GEN2 bloqueadas por variable/instrumento, `HIPÓTESIS-SIN-INSTRUMENTO`, `NO-ENCONTRADO` que todavía afecte algo del modelo y huecos de ola/familia que impidan un CALC o parámetro.

Diversificar el piloto si es posible: 1 CONSTRUCTO, 1 HERMANAS, 1 LATERAL. Si no existen tres casos honestos, usar los que existan.

Por piloto registrar código, definición verbatim, estado previo, universo previo examinado, modo de sonda, fuentes/rutas adicionales exploradas, candidatas nuevas, resultado A.4/A.5, handoff creado y qué decisión o medición podría cambiar.

## 9. Medición del acto

```text
N_huecos_sondeados
N_candidatas_nuevas
N_candidatas_ya_conocidas_redescubiertas
N_handoffs_adquisicion
N_negativos_que_siguieron_negativos
N_negativos_reclasificados_por_nueva_evidencia
```

No inflar estos números con URLs alternativas del mismo objeto.

## 10. Salida estándar de `/sonda`

```text
### SONDA · <código>
Definición: "<verbatim>"

Estado de entrada:
<qué había concluido el mecanismo previo y sobre qué universo>

Modo:
CONSTRUCTO | HERMANAS | LATERAL

Universo adicional sondeado:
<fuentes/familias/repositorios/rutas realmente examinados>

| candidata | fuente/familia | evidencia de existencia | cobertura aparente | acceso | A.4/A.5 | siguiente paso |
| ... |

NEGATIVO ACOTADO:
<si aplica, qué se agotó exactamente y qué NO fue examinado>

HANDOFF:
- NINGUNO
- adquisición: <fuente / fila / estado>
- CAJA/manual: <receta concreta>
- volver a /mapea con <nuevo universo>, si aplica.

RECOMENDACIÓN:
una sola frase. Propone, no decide.
```

## 11. Archivos y perímetro

Perímetro esperado:

```text
.claude/commands/sonda.md
.claude/commands/mapea.md
forense/notas/<fecha>-GEN2-SONDA-2-*.md
```

Y sólo si los pilotos producen handoffs reales:

```text
data/curacion-registro/cola-adquisicion-registro.tsv
data/cola-adquisicion-v1_0.tsv
```

Sólo tocar código Python si se demuestra que falta una operación mínima para usar el escritor ya existente.

No tocar specs/resultados GEN2, medidores, `milpa/tramite.yaml`, canon sustantivo, crosswalks, microdato, configuración de rutinas, GitHub Actions, Despacha, Revisa, Trámite ni Pulso.

## 12. Pruebas

Correr la línea base vigente al inicio y al cierre.

No añadir una batería nueva de tests por la existencia de `/sonda`. Sólo añadir/modificar prueba si aparece un defecto material y estable cuya repetición cambiaría un negativo por positivo, una fila de adquisición, una identidad de fuente, una decisión o una medición.

Validación funcional mínima:

1. `/sonda` puede ejecutarse conceptualmente sobre los pilotos sin inventar universo ni estado.
2. Un fallo de fetch no termina como “no existe”.
3. Una candidata pendiente puede producir handoff sin duplicar cola.
4. `/mapea` sigue proponiendo, no decidiendo.
5. `/sonda` tampoco decide ni adopta nada.

## 13. Criterios de aceptación

El acto está terminado si existe `/sonda` reusable y autocontenida; está basada explícitamente en #197, #524 y #542; no duplica `/adquiere`; no crea segunda cola ni segundo escritor; `/mapea` deriva a SONDA sólo ante negativos materiales; los negativos quedan acotados al universo realmente examinado; se corrieron hasta 3 pilotos reales vigentes; cualquier candidata de adquisición usa el SSOT/escritor vigente; no se abrió microdato; no se modificaron specs/resultados GEN2; baseline queda sin regresión material nueva; queda una nota corta con la medición; y el PR es pequeño y fusionable.

## 14. Lo que no hace este acto

No crea SONDA como idea nueva, no reaudita todas las fuentes históricas, no vuelve a ejecutar PR #197/#524/#542, no intenta resolver todos los `NO-ENCONTRADO`, no convierte la sonda en crawler general, no crea un índice universal de internet, no decide causalidad, no diseña nuevas specs, no adopta resultados, no crea sucesores CALC, no arregla CALC-0003, no crea una rutina llamada SONDA y no añade otro robot supervisor.

## 15. Cierre esperado

El PR debe explicar primero:

1. qué capacidad quedó reusable;
2. qué negativos reales se sondearon;
3. qué candidatas/handoffs nuevos aparecieron;
4. qué decisión o medición futura desbloquean.

PRISMA de cierre:

```text
base origin/main usada
N_huecos_sondeados
N_candidatas_nuevas
N_handoffs_adquisicion
N_negativos_reclasificados
archivos tocados
baseline final
bloqueos materiales restantes
```

Terminar con:

```text
SIGUIENTE AVANCE:
una frase sobre el resultado sustantivo que ahora puede producirse gracias a la sonda.
```

Regla de parada: si `/sonda` funciona, el puente con `/mapea` funciona, los pilotos producen evidencia interpretable y no hay regresión material, abrir PR y parar.

---

## Recibo de ejecución

Consumido por **PR #632**, fusionado a `main`.

Resultado sustantivo:

- `/sonda` quedó instalada con modos CONSTRUCTO/HERMANAS/LATERAL.
- `/mapea` recibió el puente mínimo `SONDA-RECOMENDADA`.
- Se ejecutaron tres pilotos reales.
- Se produjo un handoff real sobre RUPC sin duplicar la cola.
- Quedaron tres reservas que requieren CAJA:
  1. leer `ENADID 2023 / TMUJER1:conoce_1..6`;
  2. probar las tres rutas laterales de RUPC;
  3. verificar granularidad administrativa del padrón de Bienestar para R7.9.
