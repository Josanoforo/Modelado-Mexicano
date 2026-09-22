# ENCARGO · ACTO GEN2-ENUT-NUCLEO-CELDAS-1 · Las 21 celdas de cuidado del marcador, re-derivadas sobre el núcleo comparable para que el piso ENUT 2019 tenga contra qué enlazarse

> ENTORNO: **CAJA** — abre ENUT 2024 (marginales por eje sobre el núcleo; **ningún cruce**) y lee ENUT 2019 ya sellado. Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** desde COMMIT-1 · CONTADOR: +1 corrida sellada y registrada, `cuenta_gen2 = SI`, **no adopta**; 21 celdas pasan de `NO-CONSTRUIBLE` (ADR-557) a `SOLO-PISO` si el enlace queda (derivado) · CALC-id reservado: `CALC-ENUT2024-NUCLEO-EJES-0001` · ids raíz de acto.

## 1 · OBJETIVO
Ejecutar la decisión (b) de `FP-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-01`: medir las 21 celdas marginales del marcador (cuidado, ENUT 2024) **sobre la definición del núcleo** que `CALC-ENUT2019-NUCLEO-EJES-0001` usa —una variable por celda, mismos ejes—, con IC, para que el piso t−1 de 2019 y la R de 2024 midan el mismo evento. «Hecho» = `verify CALC-ENUT2024-NUCLEO-EJES-0001` REPRODUCE; 21 RESULT con `definicion = NUCLEO (ENUT2019-NUCLEO-EJES-0001)` en su spec; el marcador re-derivado muestra 21 celdas `SOLO-PISO` (o las que la spec derive) con `piso_fuente = CALC-ENUT2019-NUCLEO-EJES-0001`.

## 2 · FIRMAS DE MESA
*Propuesta de dirección (recomendación del ejecutor de ENUT-PISOS-Y-SERIE-1), mesa sella o edita:* «(a) El salto uniforme 2019→2024 del núcleo (−18 % a −35 % en las 14 celdas, mismo signo; CONCP 2024 ≈ NÚCLEO 2019) se lee como CAMBIO-DE-INSTRUMENTO: la fila C2×2019 de `data/enut-comparabilidad-texto-v1_0.tsv` pasa a CAMBIO-DE-INSTRUMENTO y la persistencia 2019→2024 del núcleo queda rotulada así, no NO-DECIDIBLE. (b) Las 21 celdas del marcador se miden sobre el núcleo en un sucesor de caja —este acto—; el cruce sigue RESERVADA. (c) `cuenta_gen2 = SI` para los tres CALC de ENUT-PISOS-Y-SERIE-1.» Sin texto → PARA (la medición sin (a) no tiene definición).

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` la FP (texto de arriba). `[EXISTE]` `CALC-ENUT2019-NUCLEO-EJES-0001`, `CALC-ENUT-SERIE-2009-2014-NUCLEO-0001`, `CALC-ENUT2024-DISTRIBUCION-HORAS-0001`, `data/enut-comparabilidad-texto-v1_0.tsv`; ADR-557 («los 17 marginales que nadie midió: el piso t−1 del reparto de cuidado (ENUT 2019) es NO-CONSTRUIBLE por…»). No sé la definición exacta del núcleo ni sus 14/21 celdas: **el acto la lee de la spec sellada de 2019 y la copia verbatim**.
- `[SUPUESTO]` Las 21 celdas del marcador son marginales por un eje (no cruces). Si alguna es cruce, queda RESERVADA y fuera de este acto (PARO a) para esa celda).
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-ENUT2024-NUCLEO*` → 0; `grep -c "ENUT2024-NUCLEO" data/corrida0/corridas.tsv` → 0. Ramas vivas: ninguna.

## 5 · PIEZAS
- **COMMIT-1:** spec congelada: definición del núcleo verbatim de la spec 2019 (ítems, ventana, unidad, ponderador), ejes y categorías idénticos al marcador, códigos 2024 **por texto** contra el FD (la fila C2×2019 rotulada por (a)), seed, tolerancias; D-22 sintético.
- **COMMIT-2:** los 21 marginales con IC; registro y asiento en el mismo acto.
- **P3:** `enut-comparabilidad-texto-v1_0.tsv` enmendado por (a) (fila C2×2019), `decisiones.tsv` con (a)(b)(c) verbatim, FP → FIRMADA; el marcador re-derivado por su tool (no a mano).

## 6 · LATITUD
DECIDES TÚ: orden, enlazar `data/raw`, dependencias, ≤ 10 líneas. PREGUNTAS A MESA: si el núcleo 2019 no es construible en 2024 para un ítem (texto cambiado), ¿celda NO-CONSTRUIBLE (recomendado) o núcleo reducido con ambas olas re-medidas? NO DECIDES: §7.

## 7 · PAROS
a) derivar cualquier cruce de ENUT 2024 · b) editar CALC sellados o forzar · c) adoptar · d) cambiar la definición del núcleo congelada · e) nube · f) inalcanzable · g) código congelado no corre.

## 8 · COMPUERTAS
«Firma (a)(b)(c) presente — protege: congelar spec.» «No hay otro acto de caja en vuelo — protege: borrar.»

## 9 · PERÍMETRO
Propio: `forense/prereg-caja/ENUT2024-NUCLEO-EJES-spec-v1_0.md` (+ sidecar, yaml) · `data/corrida0/CALC-ENUT2024-NUCLEO-EJES-0001/` · `data/enut-comparabilidad-texto-v1_0.tsv` (una fila) · `decisiones.tsv` · `firmas-pendientes.tsv` · derivados y marcador por comando · nota · `canon/L0/<raíz>.md`. Ajeno: los CALC de 2019 y 2024 existentes, `milpa/`. Otro acto en vuelo: ninguno verificado. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no evalúa retadores, no abre cruces. Sucesor: la adopción del piso ENUT por instrumento cuando el marcador lo evalúe (misma lógica que MARGINALES-ADOPCION-1). Auditoría: no aplica (mide; la lectura sobre cuidado la hace el informe con el módulo). Cierre por /acto.


