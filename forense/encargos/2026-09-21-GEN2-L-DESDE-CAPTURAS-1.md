# ENCARGO · ACTO GEN2-L-DESDE-CAPTURAS-1 · LAS CIFRAS DEL LLM EN EL DUELO SE MIDEN DESDE SUS CAPTURAS SELLADAS, CON EL AGREGADOR QUE LA SPEC DECLARA, Y QUEDA EL MÓDULO QUE EL LOTE Y LOS DUELOS VAN A USAR

> ENTORNO: **NUBE** (cualquiera): las capturas están en el repo; no abre microdato ni llama a ningún modelo. NO es CAJA.

CABECERA · SHA de redacción `fc13cdcc`; re-deriva al abrir · una sola sesión, rama `acto/gen2-l-desde-capturas-1` · MODELO: Opus (mide) · MODO: **ABIERTO** hasta el COMMIT-1; desde ahí RÍGIDO · CONTADOR: sella una corrida (o una por variante); `cuenta_gen2 = SI` (§2); **no pinea y no adopta**: legacy no debe moverse en este acto · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación.** Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.
**NO CHOCAR CON TUBERÍA (acto en vuelo):** no edites `.github/workflows/verify.yml`, `tests/check.py`, `.gitattributes`, `.claude/commands/*.md`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `tools/estado_comun.py` ni `tools/digesto_tramite.py`. Tu test nuevo **no** se cablea a mano: el job de guardias lo ejecuta como huérfano (`tools/ci_guardias.py --ejecuta-huerfanos`) `[EJECUTADO por dirección: 56 ejecutados]`. Si tu cierre exige tocar uno de esos archivos, déjalo en NC con sucesor y dilo.

## 1 · OBJETIVO
En el marco del duelo, las lecturas del LLM (campo L) siguen siendo GEN1: 9 de ellas quedaron rotuladas «rehecho con diferencia» porque GEN1 agregó con la **media** y la spec sellada declara la **mediana**, y porque GEN2 re-extrae desde las 224 capturas completas mientras GEN1 usó otro conjunto. Mesa firmó: gobierna la mediana declarada, GEN1 es historia, y el relevo de L exige un CALC propio que mida desde las capturas. Nadie lo tomó. Además, el lote ENIF 2024 y los duelos ENVIPE y ENIGH van a sellar capturas nuevas de LLM: necesitan **un** agregador probado, no tres.
«Hecho» significa: CALC sellado que produce L por celda y por variante (solo / con corpus) desde `corridas-L-completa-v1_0`, con mediana, dispersión entre repeticiones e intervalo · tabla de diferencias contra GEN1, con la parte que explica el agregador y la que explica el conjunto de extracción, **separadas** · módulo de agregación reutilizable con su test · lista para mesa de qué lecturas L quedarían pineables, sin pinear ninguna.

## 2 · FIRMAS DE MESA — verbatim
4.1 (21/sep) `[LEÍDO: forense/encargos/2026-09-21-GEN2-RELEVO-TANDA-3.md:8]`: «Una lectura sale de legacy solo por una de dos vías: (i) su cifra la produce código GEN2 desde un insumo crudo con hash —microdato o capturas selladas—; o (ii) […]. Ingerir un número GEN1 como insumo, con hash o sin él, no cuenta nunca.» Los 9 L (21/sep, FIRMADA por `#959`): «Gobierna la mediana que la spec sellada declara; la media de GEN1 queda como historia (E.1). El relevo de L exige un CALC propio que mida desde las capturas. Los 9 se re-rotulan para que no parezcan candidatos a pin.» FP-228: «L-v1_2: mesa corre PAQUETE-L-v1_2 (14 celdas x 2 variantes x k=8 = 224 llamadas) por CLI con sesion de claude.ai, sin ANTHROPIC_API_KEY». D-22 ampliada (21/sep): «Congelado exige: `preflight` VERDE sobre el commit final con main fusionado; que `_valida_outputs` acepte la salida de cada rama terminal del procedimiento, incluida la de celda rara, sobre sintético y sobre oro; que todo id que el código pueda emitir nulo por lectura estática esté declarado; y ningún input con hash sobre un archivo vivo.»
**Propuesta de dirección — el lanzamiento es el sello:** «La corrida de GEN2-L-DESDE-CAPTURAS-1 cuenta (`cuenta_gen2 = SI`): mide desde capturas selladas con hash, que es la vía (i) de 4.1. No pinea: los pines de L los firma mesa con la lista de este acto.»

## 3 · LO QUE DIRECCIÓN SABE (contra `fc13cdcc`)
- `[EJECUTADO: git ls-files]` `forense/prereg-duelo-v2/corridas-L-completa-v1_0/` → 224 archivos (= 14 × 2 × 8 de FP-228); `forense/prereg-duelo-v2/corridas-L/` → 731; `…/F5-documental-v1_0/capturas/` → 32. `tools/extrae_l_v1_3.py` y `extrae_l_v1_1.py`.
- `[EXISTE]` `forense/analisis/relevo-tanda-3/P6-los-9-L-con-diferencia-v1_0.md` (el análisis de los 9) y el sucesor de rótulo que dejó `#959`. `[REPORTADO por #942]` son dos diferencias, no una: agregador y conjunto de extracción.
- `[EXISTE]` precedente de agregación sellada para M: `CALC-AGG-marco-M-sorteado-v1_3-ola-v3`.
- `[SUPUESTO]` que las 224 capturas traen hash y que la spec sellada de L nombra ese conjunto como el vigente. **Verifícalo antes de congelar; si el conjunto vigente es otro, dilo y usa el que la spec nombre.**

## 4 · YA HECHO
Por objeto («L desde capturas», «mediana», «agrega L», «extrae_l») en encargos, `data/corrida0/` y ramas: existe el extractor v1.3 y el análisis de los 9; no hay CALC que mida L en GEN2. **Repítela tú.**

## 5 · PIEZAS
**P1 · Inventario con hash.** Qué conjunto de capturas declara vigente la spec sellada; 224 de 224 presentes e íntegras; modelo, versión y fecha de cada una según lo que la captura misma registre.
**P2 · COMMIT-1.** Spec humana con sidecar (universo: las 14 celdas del duelo; unidad y escala de cada una; agregador = mediana, con la regla para respuestas no numéricas, rangos y negativas a contestar, **escrita antes de mirar** cuántas hay) + `spec.yaml` + medidor. «Congelado» es D-22 ampliada; oro: sobre un subconjunto sintético con respuesta conocida, el módulo devuelve lo esperado; ramas terminales: celda con todas las repeticiones inválidas, celda con una sola válida.
**P3 · COMMIT-2.** `corrida0 run`; sello; vista y replay.
**P4 · Diferencias contra GEN1, descompuestas.** Por celda: GEN1 (media, su conjunto) → mediana sobre su conjunto, si es reconstruible → mediana sobre las 224. Lo no reconstruible se dice, no se estima.
**P5 · Módulo y lista.** El agregador queda importable (archivo nuevo en `tools/`, con test) para que lote y duelos lo usen tal cual. Lista para mesa: qué lecturas L del marco quedarían pineables por la vía (i), con el RESULT que citarían.

## 6 · LATITUD
Decides tú: una corrida o dos, nombres, forma de la tabla. Replantea y sigue ante main movido.

## 7 · PAROS — lista cerrada
a) llamar a cualquier modelo o generar capturas nuevas · b) escribir un pin o mover legacy · c) editar una captura, el análisis `v1_0` de los 9 o una spec sellada · d) fijar la regla de respuestas inválidas después de contarlas · e) `corrida0 run` no sella → no se parcha.

## 8 · COMPUERTAS
«COMMIT-1 en `origin`» protege: **congelar spec** (la regla de inválidas queda fijada antes de medir).

## 9 · PERÍMETRO
Propio: CALC nuevo y spec · módulo agregador nuevo en `tools/` y su test · tabla de diferencias · lista para mesa · filas propias de vista y replay · nota · cascada. Ajeno: `pines-de-mesa.tsv` · `tools/pines_mesa.py` · `tools/extrae_l_v1_*.py` (léelos, no los edites) · la lista de TUBERÍA. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE
No pinea · no corre LLM · no juzga si el LLM «sabe» de México. Sucesores: firma de mesa sobre los pines de L · el paquete L del lote ENIF usa este módulo. Auditoría: lo que un LLM contesta sobre México es, en buena parte, el sesgo de su corpus —clase media urbana, fuentes en inglés, muestras de diáspora—: el acto mide qué dijo, no si tiene razón; el duelo nacional es RETROSPECTIVO para el LLM y así se rotula toda cifra que salga de aquí. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
