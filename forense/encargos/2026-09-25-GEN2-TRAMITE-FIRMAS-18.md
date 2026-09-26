# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-18 · Asienta las cuatro firmas de la hoja FIRMAS-17 (H1–H4) que mesa dio en chat, ejecuta H4, y nombra ejecutor para H1–H3

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `4f3713cb` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Sonnet · MODO: **AUTÓNOMO** (cláusula v1.0 `3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones. H4 hace explícitas cuatro adopciones que `status` ya cuenta (E.2 por etiqueta): ningún contador cambia; H1–H3 bajan `legacy` cuando su ejecutor las saque del contador.

## 1 · OBJETIVO
FIRMAS-17 (#1150) dejó las cuatro filas `e760-01/02/03` y `afe1-01` ABIERTA porque su §2 llegó sin firma, y preparó H4 (PR de fusión por CALC: #1091 para `CALC-ENIF-0001` y `CALC-R-DIN-M-01-v4`; #1128 para los derivados de ENCIG y ENCUCI; formato de fila en su nota). Este acto: (P1) marca las cuatro FIRMADA con el texto verbatim de §2 y `EJECUTA:`; (P2) asienta las cuatro filas de H4 en `data/corrida0/decisiones.tsv` con el PR de fusión citado; (P3) cierra las cuatro NC «decisión de mesa pendiente» de #1150 con `DECISIÓN-DADA`.
«Hecho»: `awk` sobre `firmas-pendientes.tsv`: `e760-01/02/03` y `afe1-01` FIRMADA · `grep -c` de los cuatro CALC en `decisiones.tsv` → 4 filas nuevas con PR citado · NC cerradas · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas el 25/sep/2026 en chat («firmo» sobre H1–H4 de la hoja FIRMAS-17), verbatim; viajan aquí y las asienta este acto
- **H1** «Mesa declara HISTÓRICO-SIN-RELEVO las 8 entradas asignados_coeficiente de milpa/procedencia.yaml; las 12 asignados_probabilidad siguen la regla de FIRMAS-16 B1/B2; ejecuta RELEVO-CONSUMIDORES-3.»
- **H2** «Para M01–M07 y M23 rige la regla de M08: acotar a la unidad medida donde el cotejo sea PARCIAL; HISTÓRICO-SIN-RELEVO donde sea NO-EQUIVALENTE; ejecuta RELEVO-CONSUMIDORES-3.»
- **H3** «Mesa declara HISTÓRICO-SIN-RELEVO las 42 lecturas L/AGREGADO de marco-M-sorteado-v1_3 y las saca del contador legacy; ejecuta RELEVO-CONSUMIDORES-3.»
- **H4** «Se asienta en decisiones.tsv una fila de adopción por cada CALC adoptado solo por etiqueta, citando el PR de fusión; ejecuta este trámite.»
Si mesa corrigió alguna letra al contestar, esa fila lleva el texto de mesa y se declara; si mesa **no** contestó, este acto no se lanza (el lanzamiento es la constancia de la firma).

## 3 · LO QUE DIRECCIÓN SABE
`[LEÍDO]` Reporte de #1150 (FIRMAS-17): filas ABIERTA apuntando a la hoja; H4 preparada; `acto.md` paso 11 ya exige `## CONSUMIDO`; dos líneas en `tests/check.py` para los ids `M01`–`M23` (declaradas). `[EJECUTADO]` main `4f3713cb`: FIRMAS-17 y MAPA v1.1 con PR abierto; un `[deriva]` del bot abierto (`auto-36189916805`). ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
Si #1150 no ha fusionado al abrir, este acto arranca sobre su rama fusionada localmente y lo declara (no espera). `grep -c 'FIRMAS-18' forense/firmas-pendientes.tsv` → reporta.

## 5 · PIEZAS
P1 filas FIRMADA → P2 H4 en `decisiones.tsv` → P3 NC.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0
1–7 verbatim. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) editar una fila FIRMADA previa · c) adoptar fuera de H4 · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«Texto verbatim; H4 cita el PR de fusión por CALC» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/firmas-pendientes.tsv`, `no-corrido.tsv`, `data/corrida0/decisiones.tsv`, nota, L0, cascada. Ajeno: todo lo demás. En vuelo: MAPA v1.1 (PR), `[deriva]`.

## 10 · LO QUE NO HACE · SUCESORES
No releva. Sucesor: `GEN2-RELEVO-CONSUMIDORES-3` (H1–H3; dirección lo escribe sobre este trámite fusionado).

## NO-CORRIDO / RESERVAS
Ninguno. (Premisa corregida y declarada en la nota: H4 cita PR #1093, no #1091, para CALC-ENIF-0001 y CALC-R-DIN-M-01-v4 — logística; la firma pide «el PR de fusión».)
