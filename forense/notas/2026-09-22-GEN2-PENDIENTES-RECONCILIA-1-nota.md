# GEN2-PENDIENTES-RECONCILIA-1 — nota de cierre

## 1 · Tabla «21/sep → hoy» (P1, re-derivada por comando sobre el commit de arranque de este acto)

| métrica | 21/sep (inventario) | hoy (re-derivado) | comando |
|---|---|---|---|
| Firmas ABIERTA | 12 | 16 | `awk -F'\t' 'NR>1 && $6=="ABIERTA"{c++} END{print c}' forense/firmas-pendientes.tsv` |
| NC ABIERTA | 208 | 212 | `awk -F'\t' 'NR>1 && $10=="ABIERTA"{c++} END{print c}' forense/no-corrido.tsv` |
| Ramas en origin (no-main) | 5 → 0 (según el propio inventario, ya fusionadas #989/#987/#994/#988/#985) | **8** (nuevas: `acto/gen2-din-credito-escolaridad-2`, `acto/gen2-din-lote-c2-restringido-1`, `acto/gen2-tramite-firmas-6`, `claude/gen2-fp374-resello-1`, `claude/gen2-marco-m-consumidor-1`, `claude/gen2-marginales-adopcion-1`, `claude/gen2-pendientes-caja-1` [gemelo de este acto], `claude/gen2-pendientes-reconcilia-1` [este acto]) | `git ls-remote --heads origin` |
| N_corridas_selladas | 82 → 154 (según inventario) | 154 (sin cambio adicional) | `python3 tools/corrida0.py status` |
| N_resultados_gen2_pendientes_adopcion | 12 | 12 (mismas 12 filas de §1.4) | `python3 tools/corrida0.py status` |
| Encargos sin `## CONSUMIDO` (universo de §4.1) | 28 | 28/28 — **0 ejecutados** (verificado por objeto: ninguno tiene fila NC/FP posterior cuyo campo `acto`/`encargo` lo cite) | ver metodología P2 más abajo |

**Nota de universo**: `forense/no-corrido.tsv` tiene hoy 556 filas (212 ABIERTA), no las 544 (208 ABIERTA) que cita el inventario del 21/sep — el árbol creció ~12 filas nuevas desde el corte del inventario, casi todas de actos ya corridos el 21–22/sep (`GEN2-TUBERIA-*`, `GEN2-DIN-CREDITO-PREDICCION-2024-*`, `GEN2-LECTURAS-DE-MESA-Y-ROTULOS-1`). `forense/firmas-pendientes.tsv` pasó de 12 a 16 ABIERTA por la misma razón: nuevos encargos del 21/sep abrieron firmas nuevas más rápido de lo que mesa las firma.

No se re-derivaron por comando propio: WARN nuevas de la suite (46 en el inventario) y subcomandos sin implementar (`corrida0.py vigencia`, `corrida0.py go`) — correr `tests/check.py` completo no es parte del perímetro de este acto (eso lo hace `/acto` al cerrar); se cita el inventario para esos dos renglones sin re-verificarlos, y se declara así.

## 2 · Metodología

1. Se generaron las listas de ids ABIERTA actuales de `forense/no-corrido.tsv` (212) y `forense/firmas-pendientes.tsv` (16) por comando (`awk`).
2. Para 139 de esas 212 filas NC existe un generador previo del mismo día — `forense/analisis/senal-1/nc-abiertas-por-clase.tsv` (ACTO GEN2-SENAL-1, `tools/nc_por_clase.py`) — que ya hizo verificación por objeto (CALC, ADR, PR, sucesor) sobre esas filas y dejó una columna `verificado_por_producto_en_senal_1` para las 20 candidatas más probables de cierre: **cero de las 18 `SUCESOR-YA-FUSIONADO` resistieron la verificación** (todas quedaron `NO-RESUELTA`). Este acto reutiliza ese generador (D-14/latitud del encargo: "reutilizar el generador del inventario original si existe") en vez de repetir la verificación desde cero, y mapea su `clase` al vocabulario de seis palabras de este acto.
3. Para las 73 filas NC restantes (no cubiertas por senal-1, casi todas de actos del 17–22/sep), la clasificación usa el token A.14 ya escrito en la columna `razon` de `no-corrido.tsv` (`DECISION-DE-MESA-PENDIENTE`→DE-MESA, `PARO-PREMISA`→VENCIDO, `NO-VERIFICABLE-AQUI`/`PARO-ENTORNO`→revisadas fila por fila: solo 2 de 16 exigían de verdad corpus/microdato/red — las otras 14 eran falta de herramienta (`gh`, `scipy`) o presupuesto de sesión, y quedan VIGENTE, no DE-CAJA — `FUERA-DE-PERIMETRO`/`DIFERIDO-A`/`SUSTITUIDO-POR`/`DECLARADO`→VIGENTE por defecto).
4. Las 16 firmas ABIERTA se buscaron una por una en `data/corrida0/decisiones.tsv` (`grep -c <id>`): **0/16 tienen fila** — ninguna autorización de mesa consta ya en el repo para cerrarlas por otra vía. Las 16 quedan DE-MESA.
5. Las 12 filas de §1.4 (RESULT esperando adopción) se re-verificaron contra `corrida0.py status` (`N_resultados_gen2_pendientes_adopcion=12`, mismo conteo) — siguen DE-MESA porque adoptar es PARO c del encargo.
6. Las 21 filas de §1.5 (corridas selladas que no cuentan) se clasificaron por su `motivo`: las 4 `PENDIENTE-DE-MESA` → DE-MESA; las 17 restantes (regla E.1/cadena, o etiquetas de spec sin decisión pendiente) → VIGENTE, sin cambio de premisa detectado.
7. Las 28 filas de §4.1 (encargos sin `## CONSUMIDO`) se re-ubicaron primero (se movieron de `forense/encargos/` a `forense/encargos/cola/` entre el 21 y el 22/sep) y se verificó `## CONSUMIDO` por comando: **0/28 lo tienen**. Se buscó además, por objeto, si el nombre del encargo (p. ej. `GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO`) aparece como `acto` en alguna fila de `no-corrido.tsv` o como `encargo` en `firmas-pendientes.tsv` — **0/28 coincidencias**: no hay evidencia de que ninguno de los 28 haya corrido. Los 28 quedan VIGENTE.

## 3 · Resultado — seis veredictos

```
      2 DE-CAJA
     62 DE-MESA
      9 VENCIDO
    216 VIGENTE
```

**RESUELTO-NO-ASENTADO: 0.** Ningún ítem re-verificado por objeto resultó cerrable desde este acto — el mismo hallazgo que ya había dejado `GEN2-SENAL-1` unas horas antes para el subconjunto que cubrió (cero de 18 candidatas resistieron). No se cerró ninguna fila de `no-corrido.tsv`, no se marcó ninguna FP como FIRMADA, y no se añadió ningún `## CONSUMIDO — SUPERADO-POR` a los 28 encargos de §4.1: **no hay evidencia en el árbol que lo sostenga**, y este acto prefiere cero cierres a un cierre sin cita real.

**MAL-ROTULADO: 0.** Se revisaron las razones en prosa que aparecían fuera del universo ya cubierto por `senal-1`; solo una fila nueva (`NC-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`) tenía razón en prosa sin token A.14 reconocible, y no se encontró autorización correspondiente en `data/corrida0/decisiones.tsv` ni en un ADR — queda VIGENTE con su prosa intacta (no se editó su columna `razon`).

## 4 · Lista DE-MESA (62 ítems) — lo que dirección lleva a mesa

| id | sección | qué se pide (lenguaje RH) | qué desbloquea |
|---|---|---|---|
| NC-0061 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0061 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-0090 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0090 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-0111 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0111 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-0151 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0151 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-0153 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0153 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-0156 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0156 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-0159 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0159 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-0166 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-0166 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02 | no-corrido.tsv | forense/analisis/senal-1/nc-abiertas-por-clase.tsv:NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02 (clase=BANDEJA-TITULAR) | cierre de la fila de deuda citada |
| NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE | cierre de la fila de deuda citada |
| NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE | cierre de la fila de deuda citada |
| NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-3619-01 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: (a) adoptar el piso C2 no vencido (A-bis 6; champion_actual=C2 | cierre de la fila de deuda citada |
| NC-260921-GEN2-RELEVO-TANDA-4-dedd-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE | cierre de la fila de deuda citada |
| NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1-2707-01 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: el propio encargo declara que no tener gh no es PARO (§9); que | cierre de la fila de deuda citada |
| NC-260921-GEN2-MARCADOR-E-INFORME-1-48d4-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISION-DE-MESA-PENDIENTE: la firma F8 (FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-08) lo veda  | cierre de la fila de deuda citada |
| NC-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: mesa contesto «Sin destino por ahora» a la bifurcacion del §2; | cierre de la fila de deuda citada |
| NC-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: el encargo lo fija como sucesor (§10: «decision de mesa sobre  | cierre de la fila de deuda citada |
| NC-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: sería la quinta corrida y el CONTADOR del encargo «sella hasta | cierre de la fila de deuda citada |
| NC-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-03 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: exige recortar 2021 a 18-70 (población de 2012-2018 por diseño | cierre de la fila de deuda citada |
| NC-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-03 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE | cierre de la fila de deuda citada |
| NC-260921-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1-7ef3-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: dirección cita la fuente y el universo de «18 de 20» o la fras | cierre de la fila de deuda citada |
| NC-260921-GEN2-DUELO-ENVIPE2026-COMMIT-1-8796-04 | no-corrido.tsv | forense/no-corrido.tsv razon=`DECISIÓN-DE-MESA-PENDIENTE` — este acto no corre LLM (encargo §10); `L` entra al COMMIT-2 | cierre de la fila de deuda citada |
| NC-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-01 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: FP-398 FIRMADA opción (a) (instalar librerías en CI) con ejecu | cierre de la fila de deuda citada |
| NC-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02 con recomendación  | cierre de la fila de deuda citada |
| NC-260921-GEN2-CUADERNO-DE-MESA-1-b6dc-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE -- son preguntas de regla que gobernarian actos futuros, no cas | cierre de la fila de deuda citada |
| NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-01 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISION-DE-MESA-PENDIENTE: cambiarlo toca E.7 de las instrucciones ('toda corrida sellada | cierre de la fila de deuda citada |
| NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISION-DE-MESA-PENDIENTE: es una propiedad de la configuracion del repositorio en GitHub | cierre de la fila de deuda citada |
| NC-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-02 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: enlace del piso del núcleo a las celdas C1 del marcador. | cierre de la fila de deuda citada |
| NC-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-03 | no-corrido.tsv | forense/no-corrido.tsv razon=DECISIÓN-DE-MESA-PENDIENTE: fusionar #973 antes del sello de capturas, o fijar agregador | cierre de la fila de deuda citada |
| FP-260921-MOTOR-THETA-CONGELADA-1-e8fa-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-02 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-ENCIG-SERIE-Y-TENDENCIA-1-852f-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-02 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-03 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-04 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-TRAMITE-FIRMAS-5-958c-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-02 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260921-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1-7866-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| FP-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01 | 1.1-firmas-pendientes | Firmar o rechazar la propuesta ya escrita en el encargo citado (ver firmas-pendientes.tsv). | Que el acto que la abrió pueda cerrarse y sus contadores dejen de esperar. |
| RESULT-BANXICO-2024-AUT-ATRASO-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-BANXICO-2024-AUT-ATRASO-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-BANXICO-2024-HIP-ATRASO-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-BANXICO-2024-HIP-ATRASO-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-BANXICO-2024-NOM-ATRASO-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-BANXICO-2024-NOM-ATRASO-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-BANXICO-2024-PER-ATRASO-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-BANXICO-2024-PER-ATRASO-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-BANXICO-2024-TDC-ATRASO-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-BANXICO-2024-TDC-ATRASO-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-CTX-2019-P-ALTO | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-CTX-2019-P-ALTO` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-CTX-2021-P-ALTO | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-CTX-2021-P-ALTO` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-CTX-2023-P-ALTO | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-CTX-2023-P-ALTO` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-EDER-A-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-EDER-A-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-MOTRAL15-ENOE-P17-CON-ACCESO-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-MOTRAL15-ENOE-P17-CON-ACCESO-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-MOTRAL15-ENOE-P17-SIN-ACCESO-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-MOTRAL15-ENOE-P17-SIN-ACCESO-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| RESULT-MOTRAL15-P17-TOTAL-P | 1.4-resultados-gen2-pendientes-adopcion | Decidir si se adopta el resultado `RESULT-MOTRAL15-P17-TOTAL-P` (merge de mesa, E.2) o se veta como los otros dos ya vetados. | Que N_resultados_gen2_adoptados_activos suba y el resultado deje de estar sellado sin uso. |
| CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002--18e3c08247d5 | 1.5-corridas-no-cuentan | Decidir si `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002--18e3c08247d5` cuenta para GEN2 (cuenta_gen2) — etiqueta PENDIENTE-DE-MESA en la spec. | Que la corrida deje de estar sellada sin contar. |
| CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001--f22dc8014aec | 1.5-corridas-no-cuentan | Decidir si `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001--f22dc8014aec` cuenta para GEN2 (cuenta_gen2) — etiqueta PENDIENTE-DE-MESA en la spec. | Que la corrida deje de estar sellada sin contar. |
| CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002--cd853c64a584 | 1.5-corridas-no-cuentan | Decidir si `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002--cd853c64a584` cuenta para GEN2 (cuenta_gen2) — etiqueta PENDIENTE-DE-MESA en la spec. | Que la corrida deje de estar sellada sin contar. |
| CALC-WBES2023-PRECISION-INTERACCIONES-0001--7f2a0899f700 | 1.5-corridas-no-cuentan | Decidir si `CALC-WBES2023-PRECISION-INTERACCIONES-0001--7f2a0899f700` cuenta para GEN2 (cuenta_gen2) — etiqueta PENDIENTE-DE-MESA en la spec. | Que la corrida deje de estar sellada sin contar. |

## 5 · Lista DE-CAJA (2 ítems)

Archivada en `forense/notas/2026-09-22-PENDIENTES-CAJA-lista-v1_0.tsv` (sha256 `60acbe9d0c778a1d3a8c17a96cc63b7e1a06871156120aa55de6832ea9c69760`) — insumo de `GEN2-PENDIENTES-CAJA-1`. Se depuró de las 14 filas `NO-VERIFICABLE-AQUI`/`PARO-ENTORNO` originales a solo 2: las otras 12 no exigen corpus/microdato/red (exigen `gh` con credenciales, `scipy`, o más presupuesto de verificación de sesión) y quedan VIGENTE en el TSV de clasificación, listadas ahí con la cita de por qué se reclasificaron.

## 6 · Lo que quedó VIGENTE / VENCIDO

- **VIGENTE: 216.** La gran mayoría (139) hereda directamente la verificación por objeto de `GEN2-SENAL-1`, ya hecha el mismo día contra el árbol actual. El resto se clasificó por su propio token A.14 (`FUERA-DE-PERIMETRO`, `DIFERIDO-A`, `SUSTITUIDO-POR`, `DECLARADO`) o por búsqueda de objeto directa (28 encargos §4.1, 17 corridas §1.5).
- **VENCIDO: 9.** Filas NC cuya razón es `PARO-PREMISA` (la premisa del encargo que las abrió cambió y el encargo necesita reescribirse, no cerrarse) — se listan íntegras en el TSV de clasificación con su cita; no se les tocó el texto.

## 7 · Auditoría de la clasificación (por qué cero cierres es el resultado correcto y no una falla de este acto)

`GEN2-SENAL-1` corrió horas antes sobre prácticamente el mismo árbol y ya hizo la verificación de objeto más cara (18 candidatas de cierre revisadas a mano, cero sobrevivieron). Que este acto, corriendo después sobre un árbol apenas más grande, llegue al mismo resultado (cero cerrables) es la confirmación cruzada esperada, no evidencia de que faltó buscar. Donde este acto sí aporta encima de `senal-1`: (a) cubre las 73 filas NC nuevas que `senal-1` no vio, (b) cubre las 16 FP, 12 RESULT, 21 corridas y 28 encargos que `senal-1` no tocaba, y (c) depuró la lista DE-CAJA de 14 candidatas a 2 reales.

## 8 · Vocabulario nuevo y `canon/registro-rotulos.tsv`

Se inspeccionó `canon/registro-rotulos.tsv` antes de escribir: su esquema (`espacio · valor · que_significa · donde_vive`) registra **habitantes de espacios de nombres** (IDs de actos por espacio C/GEN2/etc.), no un vocabulario de veredictos de clasificación. Forzar las seis palabras de este acto (`RESUELTO-NO-ASENTADO`, `VIGENTE`, `VENCIDO`, `MAL-ROTULADO`, `DE-MESA`, `DE-CAJA`) en ese archivo sería escribir en un sitio que no es el suyo — no se hizo. El vocabulario queda declarado en el encargo archivado y en esta nota; si dirección quiere un registro central de vocabularios de veredicto, es una pieza nueva, no esta.

## 9 · Entregables de este acto

- `forense/notas/2026-09-22-GEN2-PENDIENTES-RECONCILIA-1-clasificacion.tsv` — 289 filas, `seccion · id · veredicto · cita`.
- `forense/notas/2026-09-22-PENDIENTES-CAJA-lista-v1_0.tsv` — 2 filas, sha256 `60acbe9d0c778a1d3a8c17a96cc63b7e1a06871156120aa55de6832ea9c69760`.
- Esta nota.

## 10 · Auditoría de rigor extremo

No aplica — este acto afirma sobre el tablero del programa, no sobre México (§10 del encargo).
