# ENCARGO · GEN2-ESQUEMA-E1-CAPA-1 · EL ESTADO DE CADA θ, LEGIBLE POR MÁQUINA, EN SU CAPA SEPARADA

**SHA de redacción:** `402d1a3` (merge de #836); re-deriva al abrir. Al abrirse, `origin/main` estaba en `1e8cbc5`.
**Entorno asignado:** NUBE — cero microdato. NO caja.
**Estado:** VIVO
**Vehículo:** `/acto`

CABECERA · redactado contra `402d1a3` (merge de #836); re-deriva al abrir · ENTORNO: NUBE — cero microdato · COMPUERTA: ninguna (ADR-531 ya fijó "capa separada") · MODELO SUGERIDO: Opus (traducir el censo de E1 a tokens es juicio nombre por nombre) · FP/ADR/NC: deriva al cierre, no heredes (máximos hoy: FP-379, NC-0282, ADR-533; hay tres actos de nube y uno de caja corriendo — quien fusione después renumera) · vehículo: `/acto`.

FIRMA DE MESA que gobierna (verbatim, ya sellada — se cita, no se pide): ADR-531, rama B: "Esquema E1: capa separada." NC-0261 lo esperaba: "llenar el token exige decidir dónde vive el esquema (edición de procedencia.yaml sellado, o capa separada) y ese es alcance de mesa". Está decidido; este acto lo ejecuta.

## VERIFICACIÓN DE EXISTENCIA (A.8, dirección, contra `402d1a3`)

* (1) Estructura: `milpa/procedencia.yaml` (sellado, GEN1: valores no se reescriben — E.1), `milpa/src/theta.py` (lanza `ThetaNoDisponible` para todo nombre), `forense/theta-cargable-por-celda-diseno-e1-v1_0.md` §3 (el censo, campos `escala` · `universo` · `identificacion`; tokens `ARGUMENTO_EXPLICITO` / `ASOCIACION-MEDIDA·*` / `AUSENCIA_DECLARADA(A-bis 1/2)`), tablero. Cubren.
* (2) Contenido: `ls milpa/ | grep -i "theta\|esquema\|e1"` → 0 de 10 archivos; `find . -name "*esquema-e1*"` → 0: la capa NO-ENCONTRADA. NC-0261 `ABIERTA` (sucesor: "acto que edite el esquema … una vez mesa decida dónde vive"); NC-0263 `ABIERTA` (`procedencia.yaml:1244` escribe `G5_familismo_apoyo` como hija de `propuesta_de_esquema:` (:1228) y no de `coeficientes_generador_medidos:`, medido con `yaml.safe_load`). Ninguno de los actos vivos toca `procedencia.yaml` (E1 lo lee; EMISOR-ESTADO-1 toca `tramite.yaml`).
* (3) Cobertura retroactiva: E1 es del 16/sep; la capa nace hoy; nada anterior pudo pasar por ella.

## PIEZAS

P1 · La capa. `milpa/theta-esquema-e1-v1_0.yaml`, cabecera `# DERIVADO DEL CENSO E1 §3 — NO EDITAR VALORES DE procedencia.yaml`, una entrada por cada nombre que `theta.py` lanza (lista derivada por código, no copiada de la nota — reporta el conteo; E1 dice 43), con los tres campos y sus tokens exactamente como el censo los asigna: `escala` (declarada o `NO-DECLARADO-EN-CANON`), `universo` (poblacional / restringido a quién / `NO-DECLARADO`), `identificacion` (`ARGUMENTO_EXPLICITO: <método>` / `ASOCIACION-MEDIDA·marginal` / `ASOCIACION-MEDIDA·condicionada(eje)` / `AUSENCIA_DECLARADA(A-bis 1/2): <por qué>`), más `fuente` (`procedencia.yaml:<línea>` o `AUSENTE`) y `generacion` (GEN1/GEN2). Si el censo deja un nombre sin token, el campo lleva `NO-CENSADO` y se cuenta: no se adivina (A.15). Las 15 familias de distribución (ADR-28.d, `modelo-decision-v4_0.md:806`) entran como sección aparte `dispersion:` con `NO-DECLARADA` en cada una — es la enmienda que E1 §4.4 debía y que el careo dejó al primer acto que tocara θ.

P2 · La colocación (NC-0263). Mover la llave `G5_familismo_apoyo` de `propuesta_de_esquema:` a `coeficientes_generador_medidos:` en `procedencia.yaml` sin cambiar un solo valor: `yaml.safe_load` antes y después, y el diff de valores es vacío (pegar el comando y la salida). Si mover la llave cambia lo que `matriz.py`/`theta.py`/`corrida0.py demanda` leen (el acto lo prueba corriendo `demanda` antes y después y comparando conteos), PARA en P2 y repórtalo: la llave puede estar donde está a propósito.

P3 · Consumo. Un test: la capa cubre exactamente el conjunto de nombres de `theta.py` (ni uno más ni uno menos) y ningún nombre lleva `ARGUMENTO_EXPLICITO` (hoy debe ser 0; el test falla el día que uno lo alcance, para que se vea). NC-0261 y NC-0263 → CERRADAS citando este acto (o NC-0263 ABIERTA si P2 paró). Enmienda fechada in situ en E1 §4.4 ("90 parámetros" → "15 familias", con cita a ADR-531 y a la capa).

PERÍMETRO Y CONCURRENCIA: `milpa/theta-esquema-e1-v1_0.yaml` (nuevo) · `milpa/procedencia.yaml` (solo la llave de P2) · `tests/test_theta_esquema_e1.py` (nuevo) · `forense/theta-cargable-por-celda-diseno-e1-v1_0.md` (enmienda fechada §4.4) · nota de cierre · tablero al cierre + cascada. No toca `theta.py`, `matriz.py`, `tramite.yaml`, specs, resultados, el piloto ni el marcador. En paralelo: E1 piloto (caja), TRÁMITE-4, EMISOR-ESTADO-1, CORTE-EDAD-1 (nube) — sin archivo común salvo el tablero al cierre. Orden de fusión: después de TRÁMITE-4 y EMISOR-ESTADO-1, antes o después de CORTE-EDAD-1 indistinto. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

CONTADOR: cero mediciones, dicho sin disfraz; 43 (o los que sean) nombres de θ con estado legible por máquina; cierra dos NC de mesa. LO QUE NO HACE: no carga ninguna θ · no cambia valores · no decide la forma de G5 · no toca el piloto. SUCESOR: el rediseño del marcador (lee la capa para saber qué θ compiten) y el segundo piloto celda-D. CIERRE: cascada + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO`.
