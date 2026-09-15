<!-- RESCATADO POR MESA 15/sep/2026, verbatim de su conversación ChatGPT de origen («Revisar integración GitHub», 8/sep/2026, archivos nombrados ~21:18 UTC). Verificado por dirección: la nota de ejecución (forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md) tiene exactamente 524 líneas, la cifra que NC-0058 declara. sha256 del adjunto: 6d4a53bce16dd456a4fe803818e829656dd56407f9dfebcc1ade2c0f2ad86e8d. Archivado bajo ACTO GEN2-SANEA-REGISTRO-Y-RESCATE, cierra NC-0058. -->
# ACTO GEN2-SONDA-CAJA-1 · CIERRA-RESERVAS-PR632

**ESTADO:** LISTO-CAJA  
**FECHA:** 2026-09-08  
**ENTORNO OBLIGATORIO:** UBUNTU LOCAL / CAJA  
**COMPUERTA:** PR #632 fusionado en `main`  
**PREDECESOR:** `ACTO GEN2-SONDA-2 · OPERACIONALIZA-SONDA-LATERAL`

## Objetivo

Cerrar únicamente las tres reservas materiales que PR #632 no pudo verificar por ejecutarse en NUBE sin `data/raw` y con política de egreso bloqueada.

Este acto no rediseña `/sonda`. Este acto prueba la capacidad recién instalada en el entorno que faltaba.

Los tres objetos son:

1. R5.4 / ENADID 2023: verificar `enadid2023:TMUJER1:conoce_1..6`.
2. RUPC: ejecutar realmente las tres rutas laterales que PR #632 dejó `SIN-FETCH`.
3. R7.9 / `civico.transferencia.atribucion_lider`: verificar la granularidad real de las fuentes administrativas de Bienestar identificadas por PR #632.

## 0. Autoridad y arranque

1. `git fetch --prune`
2. Trabajar desde `origin/main` vigente.
3. No asumir ningún SHA heredado; re-derivarlo.
4. Crear worktree/rama nueva desde `origin/main`.
5. Confirmar entorno CAJA, `data/raw` montado correctamente, `descargas_mx` disponible si alguna fuente existente la requiere y red real.
6. Correr:

```bash
python3 tests/check.py --baseline
```

No reproducir toda GitHub Actions salvo que el baseline local revele una regresión nueva. CI del PR #632 ya fue verde.

Nombre sugerido de rama:

```text
acto/gen2-sonda-caja-1-cierra-reservas-pr632
```

Nombre sugerido de PR:

```text
ACTO GEN2-SONDA-CAJA-1 · CIERRA-RESERVAS-PR632
```

## P1 · R5.4 / ENADID 2023

Problema heredado de PR #632:

```text
familia.cortejo.urbano_joven_apps
```

sigue `HIPÓTESIS-SIN-INSTRUMENTO`.

La sonda HERMANAS descubrió en el inventario nuevo:

```text
enadid2023:TMUJER1:conoce_1
...
enadid2023:TMUJER1:conoce_6
```

pero `texto_reactivo` estaba vacío y NUBE no tenía acceso al payload real.

### Tarea

1. Recuperar de `main` la definición VERBATIM vigente de R5.4. No reconstruirla de memoria.
2. Resolver ENADID 2023 contra `data/manifiesto.yaml` y el resolver vigente. No adivinar paths.
3. Abrir únicamente lo necesario: diccionario/codebook si contiene las etiquetas; si no basta, metadata del microdato real.
4. No explorar distribuciones ni resultados.
5. Para `TMUJER1:conoce_1..6`, extraer nombre de variable, etiqueta/pregunta real, categorías/value labels si ayudan y universo/filtro o skip relevante si está documentado.
6. Comparar exclusivamente contra la definición VERBATIM de R5.4.

### Veredictos permitidos

**A. `EXISTE-SATISFACE`** si mide realmente la condición requerida.

**B. `EXISTE-NO-SATISFACE`** declarando exactamente qué falta.

**C. `NO-ENCONTRADO-EN-ENADID2023`** si `conoce_1..6` fue un falso positivo nominal.

No modificar automáticamente R5.4, tier, `milpa/tramite.yaml`, canon ni ninguna spec.

Si satisface, entregar evidencia para decisión/mapeo posterior. Si no satisface, cerrar únicamente esta candidata.

## P2 · RUPC · SONDA LATERAL REAL

Problema heredado de PR #632:

```text
RUPC
NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)
```

PR #632 añadió a su fila tres rutas laterales candidatas pero no pudo ejecutarlas por bloqueo general de red NUBE.

### Tarea

1. Leer la fila RUPC actual de:

```text
data/curacion-registro/cola-adquisicion-registro.tsv
```

2. Leer la nota de PR #632.
3. Extraer de ahí las tres rutas laterales propuestas. No inventar otras antes de probar esas tres.
4. Ejecutar `/sonda` en modo LATERAL siguiendo `.claude/commands/sonda.md`.
5. Por cada ruta distinguir host alcanzable, landing alcanzable, API/catálogo real, objeto pertinente, payload real, agregado solamente, ruta muerta, credencial/costo y error técnico.

Un HTTP 200 no es éxito. Verificar identidad/contenido suficiente.

### Si aparece el payload exacto

No construir downloader propio.

Leer `/adquiere` vigente y, si permite apuntar de forma segura a RUPC y no existe lock/conflicto con el cron, usar el mecanismo existente.

Dejar que `/adquiere` haga A.7, payload al corpus, SHA, manifiesto, actualización de cola y vista.

Si la adquisición no es mecánica o exige decisión humana, no forzarla. Actualizar la fila con URL exacta, evidencia y receta concreta.

Si ninguna ruta funciona, mantener el negativo acotado a las rutas efectivamente probadas. Nunca escribir “RUPC no existe”.

## P3 · R7.9 / PADRÓN DE BIENESTAR

Problema heredado de PR #632:

Para:

```text
civico.transferencia.atribucion_lider
```

la sonda CONSTRUCTO concluyó que continuar buscando encuestas probablemente es el tipo de instrumento equivocado.

Hipótesis operativa:

```text
padrón de beneficiarios
        ×
resultado electoral por sección
```

PR #632 identifica como candidatos/parientes:

```text
PUB
PREP 2024
pub.bienestar.gob.mx
cpid.bienestar.gob.mx
```

pero NUBE no pudo verificar granularidad.

### Tarea

1. Recuperar la definición VERBATIM vigente de R7.9.
2. Revisar primero qué objetos PUB/PREP ya están realmente en corpus/manifiesto.
3. Sondear los endpoints/portales de Bienestar desde CAJA.
4. El objetivo no es descargar todo. Primero determinar esquema y granularidad.

Para el lado del padrón determinar, con evidencia real:

- unidad de observación;
- si existe registro por beneficiario;
- qué identificadores publica;
- campos geográficos;
- localidad/municipio/CP;
- sección electoral, si existe;
- domicilio/coordenadas u otra llave que permitiera derivar sección sin una inferencia epistemológicamente inadmisible;
- periodo/corte.

Para PREP determinar sólo lo necesario para confirmar la llave electoral disponible.

### Veredictos

**A. `ENLACE-POTENCIALMENTE-CONSTRUIBLE`** si existe una llave/secuencia de llaves defendible para sección electoral.

**B. `GRANULARIDAD-INSUFICIENTE`** si Bienestar sólo llega a un nivel demasiado agregado.

**C. `SIN-FETCH`** si CAJA tampoco puede comprobar el objeto.

No construir el join, no calcular asociación, no abrir un CALC y no cambiar R7.9.

Si se descubre una fuente pública concreta nueva que amerita adquisición, usar el handoff vigente de `/sonda` hacia la cola. No crear segunda cola.

## P4 · Validación de `/sonda` en CAJA

Este acto sirve además como primera ejecución de `/sonda` en el entorno local que faltaba.

No escribir tests nuevos sólo por eso.

Registrar únicamente si aparece un defecto material del contrato de `/sonda`, por ejemplo:

- cree que una fuente no existe cuando sí existe;
- duplica una fila de adquisición;
- no puede resolver el corpus;
- confunde bloqueo de red con negativo;
- rompe la vista de adquisición.

Si `/sonda` funciona como fue redactada, no modificarla.

## P5 · Escritura

Producto mínimo esperado:

```text
forense/notas/<fecha>-GEN2-SONDA-CAJA-1.md
```

Sólo tocar además:

- cola de adquisición + vista, si RUPC/Bienestar producen un handoff real;
- manifiesto, únicamente si `/adquiere` obtiene realmente un payload;
- `.claude/commands/sonda.md`, únicamente si la ejecución revela un defecto material de su contrato.

No tocar specs GEN2, resultados GEN2, medidores, `milpa/tramite.yaml`, canon sustantivo, reglas, cron, Despacha, Revisa, Trámite, Pulso ni GitHub Actions.

## P6 · Cierre

Correr al final:

```bash
python3 tests/check.py --baseline
```

Si la cola cambió:

```bash
python3 tools/vista_cola_adquisicion.py
```

y verificar que registro/vista son coherentes.

Si `/adquiere` obtuvo algo, correr únicamente sus verificaciones obligatorias vigentes.

Cerrar con una tabla:

| objeto | antes de CAJA | evidencia nueva | veredicto | cambio material |
|---|---|---|---|---|
| R5.4 / ENADID | ... | ... | ... | ... |
| RUPC | ... | ... | ... | ... |
| R7.9 / Bienestar | ... | ... | ... | ... |

Contadores:

```text
N_reservas_PR632 = 3
N_reservas_resueltas = k
N_candidatas_confirmadas = k
N_candidatas_descartadas = k
N_fuentes_adquiridas = k
N_handoffs_nuevos = k
```

## Criterio de éxito

No es necesario que aparezca una fuente útil.

Éxito significa que las tres reservas de PR #632 dejan de ser “no verificables por NUBE” y pasan a evidencia obtenida en CAJA, positiva o negativa.

Si una reserva sigue bloqueada incluso en CAJA, declarar exactamente por qué.

No abrir un PR separado por cada reserva.

## Regla de parada

Una vez que las tres reservas tengan veredicto suficientemente fundado, el baseline no tenga regresión material y cualquier handoff esté correctamente registrado, abrir un único PR pequeño y parar.

Terminar con:

```text
SIGUIENTE AVANCE:
<cuál de las tres vías, si alguna, quedó lista para convertirse en medición/adquisición real>
```
