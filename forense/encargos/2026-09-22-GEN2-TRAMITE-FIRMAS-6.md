# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-6 · Las firmas abiertas del 21–22/sep, contestadas por mesa, entran al tablero en bloque; ninguna se inventa

> ENTORNO: **NUBE**. Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` (re-deriva: este acto se lanza **después** de que mesa conteste, y E1–E4 pueden haber fusionado y consumido algunas filas) · una sola sesión · MODELO: **Sonnet** (propagación con textos dados) · MODO: **ABIERTO** · CONTADOR: cero mediciones; FP `ABIERTA` a la baja (reportado) · ids raíz de acto.

## 1 · OBJETIVO
Que cada firma abierta con respuesta de mesa quede FIRMADA con su verbatim en `decisiones.tsv`, que las filas ya consumidas por E1–E4 se citen y no se dupliquen (A.12: la firma que viaja en un encargo la asienta ese acto), y que lo que mesa no contestó siga ABIERTA sin tocar. «Hecho» = `digesto --mesa` sin ninguna de las FP contestadas en ABIERTA; `decisiones.tsv` con una fila por firma contestada, objeto = id de la FP; cero filas duplicadas (`sort | uniq -d` vacío sobre `objeto`).

## 2 · FIRMAS DE MESA — propuestas de dirección; **mesa borra las líneas que no firma y edita las que quiera; lo que queda es la firma**
- `MOTOR-THETA-CONGELADA-1-e8fa-01`: «`test_c_roles_sellados…` es causa ajena declarada (ADR-68); no bloquea la adopción de este acto; se resuelve por separado.»
- `ENCIG-SERIE-Y-TENDENCIA-1-852f-01`: «(a) sin piso de tendencia en marginales ENCIG; (b) TENDENCIA-SERIE entra como retador en el duelo ENVIPE 2026 **si su spec aún no está congelada** — si lo está, queda para el siguiente duelo; (c) la regla de «conducta sin serie» como la nota la escribe.»
- `DIN-LOTE-ENIF2024-A-a98a-02`: «Opción A: ENIF 2018 no entra como segunda ola histórica mientras el lote 2024 no cierre.»
- `ARBITRO-MARGINALES-1-ed7d-01`: «Se ratifica `cuenta_gen2 = SI` de `CALC-ARBITRO-PERSISTENCIA-ERROR-0001`.»
- `DIN-LOTE-ENIF2024-COMMIT-1-6c10-03` (Q3): «#973 fusionó; el agregador de L es `tools/agrega_l_v1_0.py`; la pieza cierra por superación.» `…6c10-04`/`6c10-02` (Q2, Q1): «Q1 queda resuelta por E2 (C2-restringido); Q2: rige el régimen ARBITRO-2024 para todo lo que se compare contra el árbitro, y el de PILOTO-1 solo dentro de sus celdas-D ya selladas.»
- `DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-01`: «No se corre L1/L2 con presupuesto sobre los 14 cruces: sería RETROSPECTIVA sobre reserva consumida y L perdió 8/8 en DIN.»
- `DIN-CREDITO-PREDICCION-2024-COMMIT-1-7866-01`: «Se ratifica K6-P-TENEDORES (unidad P).»
- `DIN-CREDITO-HISTORIA-1-ff56-01`: «Opción (a): sucesor con el mismo medidor genérico sobre ENIF 2021 con recorte 18-70, CALC nuevo.»
- **Consumidas por otros actos si fusionaron antes (citar, no re-asentar):** `…95ec-01` (E1), `…8e53-02` (E2), `…ff56-02` (E3), `…ed7d-02` (E4), `…958c-01` (FP374-RESELLO-1).
- **No se proponen aquí:** `ENUT-PISOS-Y-SERIE-1-308c-01` (dirección la trae con la nota leída), `CORPUS-INTEGRIDAD-3d56-01` (física: mesa nombra el destino).

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` 17 FP `ABIERTA` en `firmas-pendientes.tsv` al 22/sep (ids arriba). `[LEÍDO]` cada `qué_se_firma`. `[SUPUESTO]` #973 fusionó (aparece en los merges de main del 21/sep como `acto/gen2-l-desde-capturas-1`); si el acto no lo confirma por `git log`, la Q3 queda ABIERTA.
- ADJUNTOS: ninguno; las firmas van embebidas en este §2 y el sello del cuerpo las cubre (A.3).

## 4 · YA HECHO / YA DECIDIDO
Por id de FP: `grep -c "<id>" data/corrida0/decisiones.tsv` antes de asentar; si > 0, se cita y no se duplica. Ramas vivas al abrir: declarar cuáles de E1–E4 están en vuelo.

## 5 · PIEZAS
- **P1** una fila en `decisiones.tsv` por firma de §2 que sobreviva al lanzamiento (objeto = id FP; verbatim; fecha del lanzamiento).
- **P2** FP → FIRMADA con cita; NC ligadas (las que cada FP nombra en `gatea`) reciben enmienda fechada con el sucesor que la firma nombra; ninguna se cierra si su sucesor es un acto que no ha corrido.
- **P3** nota con la tabla: firma · fila · lo que desbloquea · quién lo ejecuta.

## 6 · LATITUD
DECIDES TÚ: orden, formato. PREGUNTAS A MESA: una firma cuyo objeto ya cambió (p. ej. el duelo ENVIPE 2026 congelado antes de (b)) — ¿asentar con la condición escrita (recomendado) o dejar ABIERTA? NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) editar una firma ya sellada · c) adoptar (E4 adopta; este acto solo asienta) · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
Ninguna que proteja las cuatro cosas. Orden sugerido: lanzar cuando E1–E4 hayan arrancado, para citar en vez de duplicar.

## 9 · PERÍMETRO
Propio: `data/corrida0/decisiones.tsv` · `forense/firmas-pendientes.tsv` · `forense/no-corrido.tsv` (enmiendas fechadas) · nota · `canon/L0/<raíz>.md`. Ajeno: todo lo demás. Otro acto en vuelo: E1–E4 y FP374-RESELLO-1 tocan `firmas-pendientes.tsv` — ids con raíz, sin renumerar; quien fusione después re-aplica. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No decide, no adopta, no mide. Sucesor: ninguno propio. Auditoría: no aplica. Cierre por /acto.
