# ENCARGO · ACTO GEN2-ASTRA5-U2-ENDIREH-CIERRE-1 · La cascada de cierre que #1093 no trajo: ADR con raíz, fragmento L0, registro-rótulos, asientos y NO-CORRIDO, sobre lo que ya está en main, sin re-medir nada

> ENTORNO: **NUBE** — cero microdato; lee lo que #1093 y #1099 ya sellaron. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `c12a0d87` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-astra5-u2-endireh-cierre-1` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta (las adopciones ENDIREH ya están firmadas en T y las ejecuta ADOPCION-2); asienta en `replay-evidencia.tsv` lo que #1093 dejó sin asiento.

## 1 · OBJETIVO
La auditoría post hoc (`NC-…-AUDITORIA-POST-HOC-ASTRA-1-39d2-01`) encontró que #1093 (`codex/astra5-genero-endireh-1`) se fusionó auto-declarado borrador «hasta completar… ADR raíz», sin su cascada de cierre. R(a) de FIRMAS-15 ordena la cascada por acto sucesor. Este acto la produce: ADR con raíz de acto que cite los CALC de #1093 y #1099 por id y hash, fragmento L0, `registro-rotulos`, asientos de replay que falten, `## NO-CORRIDO / RESERVAS` con lo que la unidad dejó fuera, y el recibo de la unidad al estándar del 23/sep escrito por este acto (el que Codex no dejó).
«Hecho»: `canon/L0/ADR-260924-GEN2-ASTRA5-U2-ENDIREH-CIERRE-1-<hhhh>-01.md` existe y cita cada `CALC-ENDIREH-*` por id/hash · `grep -c ENDIREH forense/replay-evidencia.tsv` = número de CALC ENDIREH sellados (derivado, citado) · `forense/analisis/astra5-genero-endireh/recibo-para-claude.md` con los seis criterios del recibo contestados por comando · NC `39d2-01` cerrada · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
R(a) (FIRMAS-15, 24/sep): «…#1093 recibe su cascada de cierre por acto sucesor.» Las adopciones ENDIREH (T, `6a2c-01..05`) las ejecuta ADOPCION-2; aquí se citan.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` Auditoría (`forense/notas/2026-09-23-GEN2-AUDITORIA-POST-HOC-ASTRA-1-auditoria.md`): #1093 y #1085 son las únicas con documento de Codex; #1093 se auto-declara incompleto; cero REVERTIR. `[EJECUTADO]` #1093 y #1099 (sucesor, 6 sellos, recibo) en main.
- `[SUPUESTO]` que los CALC de #1093 tienen `sello.json` completo y `spec.yaml` con etiquetas; si a alguno le falta etiqueta, **no se edita el sello**: NC a Astra y el CALC queda `cuenta_gen2: PENDIENTE-DE-MESA`.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls canon/L0 | grep -ci endireh` → reporta (esperado: solo el de #1099 si existe). `ls forense/encargos | grep -c ENDIREH-CIERRE` → 0.

## 5 · PIEZAS
P1 · Inventario por comando de lo que #1093 y #1099 sellaron (ids, hashes, etiquetas, asientos). P2 · Recibo de la unidad (seis criterios). P3 · Cascada: ADR, L0, rótulos, asientos faltantes, NO-CORRIDO. P4 · Cierre de `39d2-01`.

## 6 · LATITUD
Formato del recibo: el de `RECIBO-ASTRA-PRODUCTO-N`. Pregunta a mesa: ninguna.

## 7 · PAROS — lista cerrada
a) abrir ENDIREH (no hace falta) · b) editar un sello o `spec.yaml` de Astra · c) adoptar · d) no aplica · e) CAJA · f) la cascada ya existe.

## 8 · COMPUERTAS
«Sellos de Astra intactos; lo que falte es NC, no edición» protege: **borrar/reescribir**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `canon/L0/<ADR>`, `canon/gobernanza-v1_15.md` (append de cabecera), `canon/registro-rotulos.tsv`, `forense/replay-evidencia.tsv` (append), `forense/analisis/astra5-genero-endireh/recibo-para-claude.md`, `no-corrido.tsv`, nota, cascada. Ajeno: CALC, `milpa/`, `decisiones.tsv` (ADOPCION-2). En vuelo: ADOPCION-2 (union en TSV), U0.

## 10 · LO QUE NO HACE · SUCESORES
No mide, no adopta. Sucesor: ninguno; si #1085 (tecnología) necesita lo mismo, `GEN2-ASTRA5-U4-TECNOLOGIA-CIERRE-1` con esta plantilla.
