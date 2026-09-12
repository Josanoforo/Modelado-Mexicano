# Cierre · GEN2 · corpus compartido utilizable

## Resultado

El corpus compartido ya contenía todos los bytes del perímetro congelado. La
verificación dirigida obtuvo **24/24 `COINCIDE`**, tanto desde un worktree
nuevo como desde el clon operativo de adquisición. No hubo descarga,
sustitución ni duplicación de payloads.

El defecto real era de preparación local: un worktree nuevo no hereda
`data/raices.local.yaml` ni el enlace gitignorado `data/raw`. Se añadió
`tools/prepara_corpus.py` para instalar ese montaje desde una configuración
local ya autorizada y, si faltara un objeto conocido, recuperarlo desde una
raíz explícita. La previsualización es el modo por defecto; `--aplica` es
obligatorio para escribir. La herramienta opera sólo sobre los `--id`
pedidos, usa la identidad del manifiesto, nunca barre una raíz, conserva el
origen y publica una copia validada de forma atómica sin sobreescribir un
destino distinto.

## Corrección de la premisa de NC-0059

`git diff 51fec053^ 51fec053 -- data/manifiesto.yaml` demuestra que PR #635
añadió **un** payload, `rupc_datamx_json`, mediante 29 líneas YAML. La frase
histórica “29 payloads” confundía líneas añadidas con entradas. El conjunto
completo de #635 es por tanto 1/1, no 29/29. Ese objeto está en la raíz
compartida con 5,810,200 bytes y SHA-256
`2e6c98ed3e557b239b331b746dc31b73dadf62c802923a53a9a38e0204cb3ee9`.
Un lector JSON real abrió sus 18,298 registros.

El perímetro adicional pedido por el encargo se derivó por identidad, sin
fijar un total preconcebido:

- #635: 1 ID;
- ENSAFI: 5 inputs declarados por `CALC-ENSAFI-DISENO-0001` en PR #730;
- ENNViH/tandas: 13 inputs declarados por `CALC-TANDAS-ENNVIH-0001`;
- parámetros activos: 5 payloads originales que alimentan las 16 salidas
  directas GEN2 del snapshot v1.1 en PR #731.

Son 24 identidades únicas. La tabla completa con raíz lógica, ruta relativa,
SHA, estado en ambos árboles y consumidor está en
`data/corpus-compartido-perimetro-v1_0.tsv`. Todas declaran `data_raw`; no se
recorrieron Descargas personales ni raíces fuera del perímetro físico.

## Demostración desde árboles independientes

Worktree nuevo:

```text
worktree nuevo de la tarea
rama acto/gen2-corpus-compartido-utilizable
base inicial 9472223f6b463c31b6c9f3129bd26e95bf992b00
prepara_corpus PREVISUALIZA: 24 DESTINO_IDENTICO, aplicable=SI
prepara_corpus APLICA: 24 COINCIDE, config=LISTO, montaje=LISTO
manifiesto --verifica: data_raw coincide=24, no_coincide=0, ausente=0,
sin_configurar=0, fuera_de_perimetro=0
```

Clon operativo de adquisición, leído sin reiniciarlo ni editarlo:

```text
clon operativo de adquisición
HEAD 50e693d508b9191047039930f00d886c5d818188
config SHA-256 7d7ba2640e983940dad1c21cd59cba14787a6140c6bfa07803431d05893e2444
data/raw -> raiz compartida vigente
manifiesto --verifica: data_raw coincide=24, no_coincide=0, ausente=0,
sin_configurar=0, fuera_de_perimetro=0
```

Lectores sustantivos:

- RUPC: `json.loads`, 18,298 registros;
- ENSAFI: `corrida0 verify CALC-ENSAFI-DISENO-0001` en el worktree de PR
  #730, 5/5 inputs y `VERIFY: REPRODUCE (CONTEXTO=IDENTICO)`;
- ENNViH: `corrida0 verify CALC-TANDAS-ENNVIH-0001` desde el worktree nuevo,
  13/13 inputs y 39/39 resultados reproducidos;
- parámetros activos: el validador independiente de PR #731 abrió los cinco
  payloads y devolvió 16/16 `PASA` sin `--write`.

Los dos worktrees de PR #730/#731 tenían la misma configuración local y el
mismo destino compartido; no se modificaron.

## Automatización y pruebas

`tools/prepara_corpus.py` informa por ID raíz lógica, origen, destino y
estado. Si el destino ya coincide, no copia. Si falta y se proporciona
`--recupera-desde`, valida SHA/tamaño antes de una publicación atómica. Si el
destino existe con otro contenido, termina en `CONFLICTO_DESTINO` sin
sobreescribirlo. La repetición deja `LISTO`/`COINCIDE` y no descarga.

Comprobaciones:

```text
python3 tests/test_prepara_corpus.py
  OK -- 4 pruebas: preview sin escritura, aplicación idempotente,
  recuperación atómica conservando origen y conflicto sin sobreescritura

python3 -m py_compile tools/prepara_corpus.py tests/test_prepara_corpus.py
git diff --check
```

## Cierre y límites

`NC-0059` cierra porque se verificó todo su universo real (1/1) y quedó
corregida la premisa de 29. No se cierra `NC-0058`, que sigue pidiendo el texto
externo original de #635. No hay datos nuevos, adopción, cambio al motor,
cron, selector, F5, FP-371/372/373/374 ni acceso comercial. Contador
científico: cero.

La numeración candidata inicial ADR-483 se renumeró a ADR-486 al integrar
`origin/main=8f47fe62`, que ya contenía ADR-483/484/485 por PR #730/#731/#729.
