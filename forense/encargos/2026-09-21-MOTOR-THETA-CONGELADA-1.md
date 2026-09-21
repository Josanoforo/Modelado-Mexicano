# ENCARGO · ACTO MOTOR-THETA-CONGELADA-1 · el código y la documentación del motor dicen en voz alta que `matriz.g` no es camino de emisión vigente

> ENTORNO: **NUBE** — el hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.
> ENTORNO que **NO**: CAJA (este acto no abre microdato ni necesita corpus).

CABECERA · SHA de redacción: `a61dd0004b055f701f3e65bf2751266e61ec69e6` · una sola sesión, rama
`motor/theta-congelada-1` · MODELO SUGERIDO: **Sonnet** (aplica un diff ya escrito y probado;
no mide) · MODO: **ABIERTO** · CALC-id reservado: ninguno
CONTADOR · mueve: nada numérico. **NO debe moverse**: ningún contador de adopción, ninguna
cifra, ningún sello. `cuenta_gen2 = NO` (no mide).

## 1 · OBJETIVO

Que nadie —lector del código, sesión nueva o comprador— pueda leer que el motor compone por
segmento hoy. Al cerrar: el mensaje de `ThetaNoDisponible` cita ADR-531 y no BARRIDO-2; la
spec del motor declara el estado vigente; el único test que llama a `g()` con un θ inventado
lo dice.
«Hecho» significa: el diff de §5 está en `main`, los seis tests de §8 salen 0, y
`git diff --name-only` del PR no contiene `matriz.py`, `motor.py`, `celdas.py` ni
`procedencia.yaml`.

## 2 · FIRMAS DE MESA

Verbatim, 21/sep/2026 (carril libre y guardrail):
«Carril libre. Cambiar el mensaje de `theta.py` para que cite ADR-531 en lugar de BARRIDO-2.
Poner en SALIDA y en la documentación del motor la línea «`matriz.g` no es camino de emisión
vigente». Marcar los tests que la asumen ejecutable. Proponer a dirección una θ candidata como
retador para un piloto futuro.
Guardrail. `g()` no emite por defecto. `matriz.py` y `procedencia.yaml` no se borran.
Ninguna frase de producto dice «el motor compone por segmento». Cualquier edición a
`matriz.py`, `motor.py` o `celdas.py` se declara, porque mueve el contexto de replay de dos
sellos.»

## 3 · LO QUE DIRECCIÓN SABE

- [EJECUTADO] Sobre `a61dd000`: `Theta.desde(procedencia.cargar())` → 43 entradas; `valor()`
  lanza `ThetaNoDisponible` en 43/43.
- [LEÍDO] `milpa/src/matriz.py:193`: `g()` llama `theta.valor(nombre, celda)`; es el único
  consumidor de θ en `milpa/src/`.
- [EJECUTADO] `grep` sobre los 122 archivos de `tests/`: solo dos tocan `g()` o
  `theta.valor`. `test_motor_matriz.py` usa un θ inventado (≡1); `test_theta_esquema_e1.py`
  asevera que `valor()` sigue lanzando. **Ningún test asume que `g()` emite con la θ real.**
- [EJECUTADO] `milpa/src/theta.py` aparece en `data/corrida0/` solo en `corridas.tsv`
  (`CORR-0086`, DEMANDA, PENDIENTE, sin spec) y en las dos vistas de demanda. En ningún sello.
  Editarlo no mueve contexto de replay.
- [EJECUTADO] Diff de §5 aplicado en rama local sobre `a61dd000`: seis tests del motor verdes
  (§8). Diff total: 3 archivos, +19 −3.
- [LEÍDO] `milpa/src/motor.py:20` y `:129` también citan BARRIDO-2. **No se tocan** (§10).

## 4 · YA HECHO / YA DECIDIDO

Dirección buscó por objeto «mensaje de ThetaNoDisponible / estado de matriz.g» en ramas vivas,
`forense/encargos/` y `forense/no-corrido.tsv`: ningún acto previo cambia ese mensaje; el
precedente es NC-0239 (`theta.valor` lanza 43/43) y el diseño E1
(`forense/theta-cargable-por-celda-diseno-e1-v1_0.md`), que no tocó `theta.py`.
Al ejecutor: repítela con tu acceso. Si `main` ya contiene alguna de las tres ediciones, se
aplica solo lo que falte y se dice.

## 5 · PIEZA ÚNICA · el diff, inline (A.3)

Aplícalo tal cual. sha256 del parche completo del que sale este diff:
`d756c129d299d121e3fc645d432eadd37b1dfde1ee7fd305ba1d81eeb123000e` (commit local
`6889837d` sobre `a61dd000`; ese commit no existe en el remoto, por eso el diff va aquí).

```diff
diff --git a/milpa/milpa-spec-v0_2.md b/milpa/milpa-spec-v0_2.md
index 2693e0c8..ad16d1e6 100644
--- a/milpa/milpa-spec-v0_2.md
+++ b/milpa/milpa-spec-v0_2.md
@@ -26,6 +26,8 @@
 
 ## 1. Vista general
 
+> **Estado vigente, 21/sep/2026 (ACTO MOTOR-THETA-CONGELADA-1, ADR-531):** `matriz.g` no es camino de emisión vigente. `theta.valor()` lanza para las 43 entradas de `milpa/procedencia.yaml`; ninguna celda emite por composición `B·θ(x)`. Lo que el motor emite hoy sale del emisor (`milpa/src/emisor.py`) y de los estimadores adjudicados por celda. El diagrama de abajo describe la arquitectura diseñada, no la que corre.
+
 ```
    DATOS                MOTOR                        SALIDA
 ┌───────────┐    ┌────────────────────────┐    ┌──────────────┐
diff --git a/milpa/src/theta.py b/milpa/src/theta.py
index a125bb17..28560b53 100644
--- a/milpa/src/theta.py
+++ b/milpa/src/theta.py
@@ -9,6 +9,12 @@ En E0 este módulo NO estima nada. Lee lo ya adjudicado en
 `procedencia.py`: una `MEDIDO·NACIONAL` no se segmenta, una `MEDIDO·PARCIAL(x)`
 sólo por sus `x`, y una `ASIGNADO` devuelve punto sin banda con su deuda a la
 vista.
+
+ESTADO VIGENTE (ACTO MOTOR-THETA-CONGELADA-1, 21/sep/2026): `valor()` lanza
+para las 43 entradas, y por eso `matriz.g` no es camino de emisión vigente.
+No es un defecto a parchar: bajo `ADR-531` la matriz compone, no estima, y
+compite como candidato de una celda solo cuando esa celda la adjudica por
+contrato celda-D (`ADR-68`). Mientras ninguna lo haga, lanzar es lo correcto.
 """
 
 from dataclasses import dataclass
@@ -48,9 +54,11 @@ class Theta:
             for eje, _ in celda.coordenadas:
                 segmentar(e, eje)
         raise ThetaNoDisponible(
-            f"`{nombre}` está registrada como {e.clase.value} pero E0 no "
-            f"construye su distribución: eso es calibración (E1+), que espera "
-            f"el cierre de BARRIDO-2. Ley de mesa vigente."
+            f"`{nombre}` está registrada como {e.clase.value} pero no hay "
+            f"distribución cargable: `matriz.g` no es camino de emisión "
+            f"vigente. Bajo ADR-531 la matriz compone, no estima, y solo "
+            f"compite en una celda que la adjudique por contrato celda-D "
+            f"(ADR-68). No se sustituye por un default."
         )
 
     def segmentable(self, nombre, eje):
diff --git a/tests/test_motor_matriz.py b/tests/test_motor_matriz.py
index aeb849fb..7dee4ad5 100644
--- a/tests/test_motor_matriz.py
+++ b/tests/test_motor_matriz.py
@@ -50,6 +50,12 @@ def main():
         lanza(SinMagnitud, M.g, B, object(), None)
 
     def test_g_acotada_a_generadores_computa_g1_pese_a_g5():
+        # MARCA (ACTO MOTOR-THETA-CONGELADA-1, 21/sep/2026): este test usa un
+        # θ INVENTADO (≡1) para verificar la ARITMÉTICA de la composición.
+        # NO demuestra que `g()` emita: con la θ real, `theta.valor()` lanza
+        # en 43/43 y `matriz.g` no es camino de emisión vigente (ADR-531).
+        # Su contrato gemelo con la θ real vive en
+        # tests/test_theta_esquema_e1.py::test_la_capa_no_carga_ninguna_theta.
         # `ADR-531` (`ACTO GEN2-M1-ALCANCE-1`, firma de mesa del 17/sep/2026
         # sobre `M1`): el estimador es de la celda; la matriz COMPONE. `G1` no
         # depende de `G5 × familismo_obligacion` en ninguna lectura del modelo,
```

Si `main` se movió y el diff no aplica limpio (contexto desplazado), **no es PARO**: aplícalo a
mano con el mismo texto, línea por línea, y decláralo. Lo que no puede cambiar es el texto de las
líneas añadidas.

## 6 · LATITUD

Decides tú: cómo aplicarlo (`git apply`, `git am` con el parche, o a mano), el mensaje de commit,
y remover obstáculos reversibles y baratos. Un defecto adyacente de ≤ 10 líneas que te impida
terminar, lo arreglas y lo declaras — **salvo** en `matriz.py`, `motor.py` o `celdas.py`:
ahí no hay latitud (§7-c y §10).
Pregunta a mesa, siguiendo con lo demás: si algún test del motor falla por causa ajena a este
diff.

## 7 · PAROS — lista cerrada

a) abrir o derivar dato de una ola reservada (ENVIPE 2026 está RESERVADA desde el 21/sep)
b) borrar, forzar o reescribir algo sellado; **borrar `matriz.py` o `procedencia.yaml`**
c) editar `matriz.py`, `motor.py` o `celdas.py` (mueve el contexto de replay de dos sellos;
   no está autorizado en este acto)
d) cualquier cambio que haga que `theta.valor()` o `g()` devuelvan un número con la θ real
e) entorno equivocado
f) el objetivo dejó de ser alcanzable

## 8 · COMPUERTAS

- «`git diff --name-only` sin `matriz.py|motor.py|celdas.py|procedencia.yaml`» **protege:
  adoptar.**
- «Estos seis salen 0: `test_motor_matriz`, `test_theta_esquema_e1`,
  `test_motor_ejecutable`, `test_motor_holdout`, `test_motor_procedencia`,
  `test_motor_clases` (con `PYTHONPATH=.:tests`)» **protege: adoptar.**

## 9 · PERÍMETRO

Propio: `milpa/src/theta.py`, `milpa/milpa-spec-v0_2.md`, `tests/test_motor_matriz.py`.
Ajeno que no se toca: `matriz.py`, `motor.py`, `celdas.py` (replay) · `procedencia.yaml` ·
CI e ids (TUBERÍA) · el texto de SALIDA (lo lleva mesa; la línea está en §10).
Si te encuentras escribiendo fuera de esta lista, PARA.
PERÍMETRO DE CIERRE, permanente: cascada de `/acto`, hallazgos, NC y FP propios.

## 10 · LO QUE NO HACE · SUCESORES · CIERRE

No hace: no edita `motor.py:20` ni `:129`, que también citan BARRIDO-2 — se asienta en
`## NO-CORRIDO` como `DECISIÓN-DE-MESA-PENDIENTE`: coherencia de dos líneas que exige declarar
el movimiento de replay. No calibra ninguna θ. No propone el retador `justicia-policía`: eso es
propuesta de MOTOR a dirección, fuera de este acto.
Línea para SALIDA, que mesa lleva (no la escribe este acto): «`matriz.g` no es camino de
emisión vigente. Lo que el motor emite hoy sale del emisor y de los estimadores adjudicados por
celda; no compone por segmento.»
Auditoría de rigor extremo: no aplica — no afirma nada sobre México.
Cierre: `## NO-CORRIDO / RESERVAS` («Ninguno." si no hubo) antes de `## CONSUMIDO`, con este
encargo archivado verbatim y marcado con su PR.

## NO-CORRIDO / RESERVAS

- **qué:** `motor.py:20` y `:129`, que también citan `BARRIDO-2` (§10 de este encargo).
  **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` — el encargo los excluye a propósito del
  perímetro (editar `motor.py` mueve el contexto de replay de dos sellos, PARO c/§7).
  **impacto:** `motor.py:20`/`:129` siguen citando `BARRIDO-2` en vez de `ADR-531`;
  ningún contador de adopción de este acto se mueve por esto.
  **sucesor:** `SIN-ASIGNAR` (acto sucesor con permiso explícito de mesa para tocar
  `motor.py`) — fila `NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01`.

- **qué:** compuerta de "seis tests salen 0" (§8 de este encargo).
  **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` — `test_motor_holdout::test_c_roles_sellados_antes_que_todo_resultado`
  sale `FAIL`, verificado ajeno a este diff: `git log` sobre `matriz.py`/`motor.py`/`celdas.py`
  no muestra ningún commit de este acto y el fallo es anterior a `PR #883` (ADR-68, "el
  catálogo y el motor entraron en el MISMO commit"). Los otros cinco — `test_motor_matriz`
  (10/10), `test_theta_esquema_e1` (7/7), `test_motor_ejecutable` (6/6),
  `test_motor_procedencia` (8/8), `test_motor_clases` (10/10) — salen 0.
  **impacto:** la compuerta de adopción de este acto se apoya en 5/6, no 6/6; ningún
  contador de adopción propio se mueve por esto.
  **sucesor:** `SIN-ASIGNAR` (acto que resuelva el `commit_declaracion` de ADR-68 para el
  catálogo/motor) — fila `NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-02` y firma pendiente
  `FP-260921-MOTOR-THETA-CONGELADA-1-e8fa-01`.

**Defecto de secuencia propio, declarado:** el commit que archiva este encargo verbatim
(0-bis A.3) llegó *después* del commit que aplicó el diff de §5, no antes como exige el
orden del Bloque D de `/acto`. No afecta el contenido verbatim del encargo ni las
compuertas — se declara aquí por transparencia, no se corrige reescribiendo historia.

## CONSUMIDO

Ejecutado por PR https://github.com/Josanoforo/Modelado-Mexicano/pull/947, rama
`claude/untitled-session-anhykf`. Diff de §5 aplicado limpio con `git am` sobre
`9bb5396` (main se había movido desde el SHA de redacción `a61dd000`; no fue PARO).
Cinco de seis tests de §8 verdes; el sexto (`test_motor_holdout`) con un FAIL ajeno,
declarado arriba en `## NO-CORRIDO / RESERVAS` junto con `motor.py:20`/`:129`, no
editados. Cascada de cierre: `ADR-582` (`canon/gobernanza-v1_15.md`), L0 recifrado
(`canon/estado-programa-v1_14.md`), `canon/registro-rotulos.tsv`, excepción T25 en
`tests/check.py`, `NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01/02`,
`FP-260921-MOTOR-THETA-CONGELADA-1-e8fa-01`. `python3 tests/check.py --baseline
--parallel`: LÍNEA BASE VERDE, 0 FAIL nuevos frente a `tests/baseline.json`. **NO
FUSIONAR** hasta que mesa se pronuncie sobre `FP-260921-MOTOR-THETA-CONGELADA-1-e8fa-01`.
