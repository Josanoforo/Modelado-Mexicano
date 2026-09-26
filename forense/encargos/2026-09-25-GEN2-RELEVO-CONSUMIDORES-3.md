# ENCARGO · ACTO GEN2-RELEVO-CONSUMIDORES-3 · Ejecuta H1–H3 (FIRMAS-18): 8 coeficientes de procedencia y 42 lecturas del marco del duelo salen del contador como históricos; las 12 probabilidades siguen la regla del motor; los momentos M01–M07 y M23 se acotan o se declaran históricos con la regla de M08 — `legacy` de 123 hacia el residuo real

> ENTORNO: **NUBE** — escritor, `milpa/`, RESULT sellados. Hook imprime ENTORNO-DERIVADO.

CABECERA · SHA de redacción `aa36232a` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: mueve `dependencias_numericas_legacy_activas_por_consumidor__{procedencia,catalogo_de_momentos,marco_del_duelo}` hacia su residuo (histórico no es relevo, pero sale del contador de deuda por decisión firmada); `adoptados` sube por cada cita que el escritor materialice. Escribir `milpa/` es adopción: **merge de mesa**.

## 1 · OBJETIVO
(P1) **Procedencia**: las 8 entradas `asignados_coeficiente` → `estado: HISTÓRICO-SIN-RELEVO` con cita de H1 (por el escritor; el valor no cambia, deja de contar como deuda); las 12 `asignados_probabilidad` → misma regla que B1/B2: donde hay par GEN2 medido con conducta y disparador coincidentes, el escritor cita el RESULT; donde no, `rol_historico` con rótulo. (P2) **Catálogo**: M01–M07 y M23 por la regla de M08: cotejo PARCIAL → acotar el momento a la unidad medida con valor GEN2 + cita + `discrepancia_gen1` (contrato consistente desde #1115); NO-EQUIVALENTE → HISTÓRICO-SIN-RELEVO con cita de H2; redacción por momento rotulada PROPUESTO-POR-EJECUTOR con la fuente (cotejo documental, report). (P3) **Marco del duelo**: las 42 lecturas L/AGREGADO → HISTÓRICO-SIN-RELEVO por H3 y fuera del contador (`tipo_uso` que el contador excluye, como B3 hizo con las particiones). (P4) Tabla final por consumidor y `status` en árbol antes/después; lo que quede, NC con razón y sucesor.
«Hecho»: `status` en árbol: procedencia, catálogo y marco con los conteos que el derivador dé tras aplicar H1–H3 (esperado: procedencia ≤ 32, marco ≤ 1, catálogo ≤ 15; se pega) · `milpa/*.yaml` y el catálogo sin edición manual (escritor, diff seco) · tests por llave · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas (FIRMAS-18, 25/sep), verbatim
- **H1** «Mesa declara HISTÓRICO-SIN-RELEVO las 8 entradas asignados_coeficiente de milpa/procedencia.yaml; las 12 asignados_probabilidad siguen la regla de FIRMAS-16 B1/B2; ejecuta RELEVO-CONSUMIDORES-3.»
- **H2** «Para M01–M07 y M23 rige la regla de M08: acotar a la unidad medida donde el cotejo sea PARCIAL; HISTÓRICO-SIN-RELEVO donde sea NO-EQUIVALENTE; ejecuta RELEVO-CONSUMIDORES-3.»
- **H3** «Mesa declara HISTÓRICO-SIN-RELEVO las 42 lecturas L/AGREGADO de marco-M-sorteado-v1_3 y las saca del contador legacy; ejecuta RELEVO-CONSUMIDORES-3.»
- Vigentes: N (M08 unidad DELITO), B1/B2/B3/B4 (FIRMAS-16), D6, 4.1.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` legacy 123 a `aa36232a` (motor ya relevado). `[LEÍDO]` nota de RELEVO-CONSUMIDORES-2 (las tres FP con la lista exacta de entradas, momentos y lecturas); contratos en `forense/analisis/astra4-relevo/`; #1115 (contrato del catálogo y T-REPRO(c) consistentes). `[SUPUESTO]` que el contador legacy distingue `HISTÓRICO-SIN-RELEVO` por `tipo_uso`/`estado` (B3 lo hizo para particiones): si no, se extiende con test y se declara.

## 4 · YA HECHO / YA DECIDIDO
`git ls-remote --heads origin | grep -i relevo` → 0. `grep -c 'HISTÓRICO-SIN-RELEVO' milpa/procedencia.yaml` → reporta.

## 5 · PIEZAS
P1 procedencia → P3 marco → P2 catálogo (la que más redacción exige) → P4 tabla.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir ola reservada · b) editar `milpa/` a mano; reescribir sellos; cambiar un valor sin RESULT · c) mover contadores a mano · d) cambiar procedimiento congelado · e) —

## 8 · COMPUERTAS
«Escritor, diff seco, test por llave, merge de mesa» protege: **adoptar / congelar**. «HISTÓRICO solo con la firma citada por fila» protege: **borrar** (deuda).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `milpa/procedencia.yaml`, `milpa/catalogo-momentos-v0_1.tsv`, el archivo del marco (`marco-M-sorteado-v1_3`), `tools/escribe_relevo_consumo.py` + tests, el contador legacy (solo si exige distinguir HISTÓRICO), `forense/analisis/relevo-consumidores/`, TSV de gobierno, nota, L0, cascada. Ajeno: `tramite.yaml` (hecho), YAML de celdas-D, CALC. En vuelo: las unidades de caja de esta tanda (no tocan `milpa/`).

## 10 · LO QUE NO HACE · SUCESORES
No mide; no adopta lo de las unidades. Sucesor: `-4` para el residuo real (lecturas sin RESULT ni decisión).
