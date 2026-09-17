# ACTO GEN2-ESQUEMA-E1-CAPA-1 · nota de cierre

**Fecha:** 17/sep/2026 · **Entorno:** NUBE `cloud_default`, Opus, sin corpus
montado (`tools/entorno.py`: `acceso_corpus.montado=NO`,
`archivos_examinados=0`), cero microdato, cero red, **cero medición** ·
**Encargo:** `forense/encargos/2026-09-17-GEN2-ESQUEMA-E1-CAPA-1.md`
(archivado verbatim por 0-bis A.3) · **COMPUERTA:** ninguna, declarada por el
encargo — `ADR-531` rama B ya fijó la decisión que este acto ejecuta ·
**Base:** declarada `402d1a3`, real re-derivada al abrir `1e8cbc5`
(`git rev-list --count HEAD..origin/main` → `0`).

## 0 · Lo que este acto hace y lo que no

Hace **una** cosa: convierte el censo E1 §3 —que era prosa— en un archivo que
una máquina puede leer, y de paso mueve una llave que estaba en la sección
equivocada. **No carga ninguna θ**, no cambia ningún valor, no decide la forma
de `G5`, no toca el piloto. `theta.valor()` sigue lanzando `ThetaNoDisponible`
para los 43 nombres, y hay un test que lo comprueba.

## 1 · A.8 · verificación de existencia, re-derivada contra `1e8cbc5`

| # | qué | comando | resultado |
|---|---|---|---|
| 1 | estructura | `ls milpa/src/theta.py milpa/procedencia.yaml` | existen |
| 2 | la capa | `ls milpa/ \| grep -i "theta\|esquema\|e1"` · `find . -name "*esquema-e1*"` | **0** y **0** — `NO-ENCONTRADA` |
| 2 | `NC-0261` / `NC-0263` | `awk -F'\t' '$1=="NC-0261"\|\|$1=="NC-0263"' forense/no-corrido.tsv` | ambas `ABIERTA` |
| 3 | cobertura retroactiva | E1 es del 16/sep; la capa nace hoy | nada anterior pudo pasar por ella |

## 2 · P1 · la capa

`milpa/theta-esquema-e1-v1_0.yaml`. Los nombres se **derivan por código**, no
se copian de la nota:

```
python3 -c "import sys;sys.path.insert(0,'milpa')
from src.procedencia import cargar; from src.theta import Theta
print(len(Theta.desde(cargar()).entradas))"
→ 43
```

**43**, la cifra que E1 §3 decía — confirmada contra el árbol, no heredada. Las
43 líneas de `fuente` (`milpa/procedencia.yaml:<línea>`) se verificaron una por
una contra el archivo; las 43 son distintas y ninguna quedó `AUSENTE`.

### 2.1 · A.15 se ejecuta, no se cita

El censo no asigna token a todo. Donde describe el campo pero **declina**
tokenizarlo —«ausencia declarada de facto … **pero sin token**»— la capa
escribe `NO-CENSADO` y lo **cuenta**. No se adivina:

| contador | valor |
|---|---|
| `nombres_theta` | 43 |
| `campos_totales` | 129 (43 × 3) |
| **`argumento_explicito`** | **0** |
| `ausencia_declarada` | 12 |
| `asociacion_medida` | 7 |
| `declarado_verbatim` | 25 |
| **`no_censado`** | **24** |
| `no_declarado_en_canon` | 36 |
| `no_declarado` | 25 |
| `mediciones_de_este_acto` | **0** |

La regla de traducción está escrita en la cabecera del propio archivo, y cada
entrada arrastra el veredicto del censo **verbatim** en `*_segun_censo`: la
traducción es auditable fila por fila sin tener que creerle al ejecutor.

### 2.2 · `dispersion:` — la enmienda que E1 §4.4 debía

Los **15 pares `gen×coef`**, todos `NO-DECLARADA`, derivados por código de
`asignados_coeficiente.detalle` (no transcritos). La deuda de `ADR-28.d` **no
se salda** —el check de varianza intra-celda sigue sin poder correr— pero se
cuenta bien: no son «90 parámetros» (cifra de la tabla de perfiles) sino 15
familias, `canon/modelo-decision-v4_0.md:806`, con el cambio de forma de la
deuda explicado en `:307` y `:671`. Enmienda fechada in situ en el censo, sin
reescribir nada de lo anterior.

## 3 · P2 · la colocación (`NC-0263`), con la prueba pegada

`G5_familismo_apoyo` es una entrada `MEDIDO·β̂` completa que vivía como llave
hija de `propuesta_de_esquema:` — un bloque de **prosa** sobre un campo
propuesto (`descripcion`, `ejemplo`, `efecto`), no una sección de mediciones.
Movida a `coeficientes_generador_medidos:` **sin tocar un solo valor**.

**Diff de valores por `yaml.safe_load`, antes contra después:**

```
valores escalares antes: 722  despues: 722
VALORES QUE CAMBIARON : 0 {}
SOLO ANTES            : 0 {}
SOLO DESPUES          : 0 {}
```

**Llaves de cada sección después del movimiento:**

```
coeficientes_generador_medidos: ['G1_radio_confianza', 'G1_confianza_institucional',
  'G3_familismo_apoyo', 'G4_exposicion_violencia',
  'G4_confianza_institucional_justicia', 'G3_horizonte_temporal', 'G5_familismo_apoyo']
propuesta_de_esquema         : ['descripcion', 'ejemplo', 'efecto']
```

**La condición de PARO que el encargo puso en P2 se probó y no se disparó:**

```
python3 tools/corrida0.py demanda > DESPUES.txt
diff ANTES.txt DESPUES.txt   → sin diferencias (exit 0)

entradas: 46 | consumibles: 44 | nombres theta: 43
contador_condicionales_medidas: 12          (idénticos antes y después)
```

**Evidencia independiente de que la colocación estaba mal**, encontrada al
derivar y no buscada: `coeficientes_generador_sellados` ya citaba
`coeficientes_generador_medidos.G5_familismo_apoyo` en su `fuente:`, y
`tools/corrida0.py:348-351` resuelve esa cita contra la sección. Antes del
movimiento **colgaba**; ahora resuelve:

```
G5.familismo_apoyo -> medidos[G5_familismo_apoyo] RESUELVE
```

Es decir: el archivo ya se contradecía a sí mismo, y la reubicación es la
lectura que lo hace consistente — no una preferencia de estilo.

### 3.1 · La forma más fuerte de la prueba: el registro generado

`diff` sobre la **salida** de `demanda` ya daba vacío. Se comparó además el
**registro en seco que `demanda` escribe**, generado dos veces: una con
`milpa/procedencia.yaml` exactamente como está en `origin/main`, otra con la
llave movida.

```
diff reg-corridas.MAIN.tsv   data/corrida0/demanda-corridas.tsv    → SIN DIFERENCIAS
diff reg-resultados.MAIN.tsv data/corrida0/demanda-resultados.tsv  → SIN DIFERENCIAS
```

**Byte a byte idéntico.** La condición de PARO de `P2` («si mover la llave
cambia lo que `matriz.py`/`theta.py`/`corrida0.py demanda` leen») queda probada
negativa por la vía más directa que hay: el artefacto que esos lectores
producen no cambia.

### 3.2 · Un hallazgo colateral, medido al montar esa prueba (`NC-0297`)

Los dos TSV **se reescriben al correr `demanda` aunque no se cambie nada**: con
`procedencia.yaml` idéntico al de `origin/main`, `git status` los marca como
modificados. Aparece una fila `CORR` nueva (un consumidor de
`milpa/src/motor.py`) y todos los ids `CORR`/`RES` posteriores se recorren. El
registro en seco versionado **no describe el árbol actual**.

Es **preexistente y ajeno a este acto** —se reprodujo con el archivo sin
tocar— y **no contamina P2**, precisamente porque la comparación de §3.1 es
entre dos salidas generadas en la misma corrida de hoy, no contra el TSV
commiteado. `data/corrida0/` está fuera de perímetro: los dos archivos se
usaron como evidencia y se revirtieron con `git checkout`. Va a `NC-0297`, con
la rutina `/deriva` como dueña.

## 4 · P3 · consumo

`tests/test_theta_esquema_e1.py`, **7 pruebas, todas en verde**. Las dos que
importan:

- **`test_cobertura_exacta`** — la capa cubre el conjunto de `theta.py` ni uno
  más ni uno menos, en los dos sentidos por separado (son defectos distintos).
- **`test_ninguna_theta_alcanza_argumento_explicito`** — hoy **0**. Este test
  **falla el día que una θ lo alcance, a propósito**. No es un candado contra
  la identificación: es el aviso de que ese día llegó y alguien tiene que
  mirarlo, en vez de que la primera θ identificada del programa entre sin que
  nadie se entere. Si falla, **no se edita la capa para acallarlo**.

Y `test_la_capa_no_carga_ninguna_theta`, que comprueba que escribir este
archivo no cargó nada: los 43 siguen lanzando `ThetaNoDisponible`.

## 5 · Cuatro defectos nuevos, medidos al derivar y ninguno corregido aquí

Todos fuera de perímetro, todos con `NC` y sucesor. El primero es serio:

**`NC-0294` · colisión de llave `0`.** `consumibles()` devuelve **44** entradas
pero `Theta.desde()` las indexa por llave pelada en un `dict` y entrega **43**:
la llave `0` colisiona entre `evidencia_experimental_terceros.0` y
`coeficientes_generador_sellados.0`, y la segunda **pisa** a la primera. La
pisada es la única entrada `EVIDENCIA_EXPERIMENTAL_TERCEROS` del archivo (RCT
de Compartamos, sellada por `ADR-204`) y **la única que el censo marcó `LISTO`
por identificación real**. Queda inalcanzable por nombre desde `theta.py` **sin
que se emita un solo error** — la misma clase de defecto que `NC-0263`, pero en
código en vez de en datos. `milpa/src/theta.py` está fuera de perímetro por
mandato explícito del encargo, así que se declara y no se toca.

**`NC-0295` · el censo declara `universo` presente donde el árbol no trae el
campo.** Medido con `yaml.safe_load`: sólo **3 de las 6** llaves de
`coeficientes_generador_medidos` traen campo `universo:`, y **ninguna** entrada
de `condicionales_*` lo trae — el universo vive repartido en `fuente:` +
`n_util:`. La capa lo deriva de ahí y **lo declara** en `universo_origen`, en
vez de fingir un campo que no existe.

**`NC-0296` · `fuente:` colgante del sellado `G3.horizonte_temporal`.** Su
`fuente` es una ruta de nota, y el parseo de `tools/corrida0.py` obtiene la
cadena `"md"`, que no existe en la sección. Hoy cae en el respaldo y **no mueve
ninguna cifra** (verificado: `diff` vacío); es una referencia colgante latente.

**`NC-0297` · el registro en seco commiteado está desfasado del árbol.** Ver
§3.2. Preexistente, ajeno a este acto y sin efecto sobre P2.

**`NC-0293` · los 24 campos `NO-CENSADO`**, sucesor explícito del residuo de
`NC-0261` — para que cerrar `NC-0261` no entierre la deuda que quedaba debajo.

## 6 · Perímetro

Escrito: `milpa/theta-esquema-e1-v1_0.yaml` (nuevo) ·
`milpa/procedencia.yaml` (**sólo** la llave de P2) ·
`tests/test_theta_esquema_e1.py` (nuevo) ·
`forense/theta-cargable-por-celda-diseno-e1-v1_0.md` (enmienda fechada §4.4) ·
esta nota · cascada (`canon/gobernanza-v1_15.md`,
`canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv`,
`forense/no-corrido.tsv`, `tests/check.py` por `T25`) · encargo archivado.

**No tocado:** `milpa/src/theta.py`, `milpa/src/matriz.py`, `milpa/tramite.yaml`,
specs, resultados, piloto, marcador.

`tests/check.py` se edita **sólo** por el paso 5 de `/acto` (exención `T25` del
rótulo pelado `E1`, que aquí no es rótulo sino la **etapa** del programa que
`theta.py` nombra en su propio docstring). El encargo verbatim no se edita para
complacer el test (A.3).

## 7 · Contador

**Cero mediciones**, dicho sin disfraz. Cero θ cargadas, cero valores
cambiados, cero decisiones sobre la forma de `G5`, cero microdato, cero red.
43 nombres de θ con estado legible por máquina; 15 familias de dispersión
enumeradas; dos `NC` de mesa cerradas (`NC-0261`, `NC-0263`) y **cinco**
abiertas (`NC-0293`…`NC-0297`).

**Sucesor:** el rediseño del marcador (lee la capa para saber qué θ compiten) y
el segundo piloto celda-D.
