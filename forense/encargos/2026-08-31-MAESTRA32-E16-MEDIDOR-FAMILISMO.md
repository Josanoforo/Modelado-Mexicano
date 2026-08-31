ENCARGO · ACTO MAESTRA32-E16 · MEDIDOR-FAMILISMO-APOYO

SHA de redacción: 899113c (main, merge PR #404 / ADR-232) · Redactado: 31/ago/2026, dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: LISTO PARA LANZAR — sin compuerta, sin ranuras.

ENTORNO ASIGNADO: UBUNTU (caja con corpus). NO se lanza en NUBE — abre microdato de EDER 2017 y ENDIREH 2016. A.2 tercera parte PARO-relevante.

CARRILES EN PARALELO (declarado): carril CAJA = E16 (este) → E18 · REGLAS-OLA5-FASE1; carril NUBE = E15 · MARCO-M-CORRIGE → E17 · CURA-RADIO. Compartidos entre carriles: la cascada y, con E18, milpa/procedencia.yaml (secciones distintas: E16 escribe coeficientes_generador_sellados; E18 no toca milpa/). Renumera quien fusiona segundo.

FIRMA DE MESA — verbatim, 31/ago/2026

D-A · "Midámosla." Mesa autoriza el medidor de caja para G5.familismo_apoyo sobre la co-observación que MAESTRA32-E4 (ADR-230) halló: eder2017 (lectura más limpia) y endireh2016 (robustez). Trato del resultado: el mismo que ADR-220/ADR-226 dieron a los otros pares — entra al ejecutable como ASOCIACIÓN-MEDIDA·MARGINAL bajo ADR-57(a) y A-bis 1-3, con su reserva.

[ARRANQUE ya verificado por el orquestador — no lo repitas]

A.2, tercera parte (PARO-relevante): ls data/raw/ 2>/dev/null | head -3. En la caja: command grep; TSV con cabecera #; YAML íntegro. A.1: hash de los payloads que abras, una invocación por --id. T03: rutas completas entre backticks.

VERIFICACIÓN DE EXISTENCIA (contra 899113c, ya confirmada por dirección):
1 · ESTRUCTURA. Dominio 4. Tablas: milpa/procedencia.yaml (sección A coeficientes_generador_medidos; sección coeficientes_generador_sellados, hoy 6 entradas con valor_ejecutable; fila B de G5.familismo_apoyo en rutas_estimabilidad_coeficiente.detalle, ruta: SIN-RUTA), tests/test_matriz_sellados.py, data/emparejamiento-motor-v1_2.tsv (candidatos de E4).
2 · CONTENIDO. (i) β̂ de G5.familismo_apoyo: NO-ENCONTRADO — sección A leída íntegra hoy (6 entradas: G1×2, G3×2, G4×2; ninguna G5); fila B: SIN-RUTA, nota "único candidato (ENIF p9_9_4) excluido por circularidad". (ii) Co-observación, verbatim del cierre de E4 (forense/notas/2026-08-30-reempareja-cierre.md:67-69): eder2017 — θ = financia_8 "Préstamo familiar"; desenlace = batería de corresidencia (padre_cor, madre_cor, hnos_cor, suegro_cor, suegra_cor, hij_cor_1..15, …). endireh2016 — θ = p4_8_2/p4_8_3 "¿usted recibe dinero de familiares…?"; desenlace candidato = p18_4 (cuidado de nietos/sobrinos). (iii) Payloads en corpus, verificado en los inventarios: eder2017/eder2017_bases_csv.zip (432 variables; también _dta/_sav), endireh2016/bd_mujeres_endireh2016_sitioinegi_csv.zip (2,657 variables; también _stata/_spss), bd_sd_*, bd_viviendas_*. Fichas: eder2017/eder2017_fd.pdf en data/inventario-fd-ext-v1_0.tsv (E12). (iv) Definición canónica de la θ: canon/glosario-v5_6.md (entrada familismo_apoyo) y modelo-decision §2.1 (G5 genera "pooling, corresidencia, carga de cuidado") — cítalas en COMMIT-1.
3 · COBERTURA RETROACTIVA. La fila B se selló SIN-RUTA el 25/ago sobre 316 payloads; eder2017/endireh2016 entraron al mapa con la tabla ext (ADR-228) y E4 (ADR-230). El SIN-RUTA es correcto sobre su universo y VENCIDO EN ALCANCE; este acto lo re-sella con dato.

0-bis · A.3: Primer commit: este encargo verbatim en forense/encargos/2026-08-31-MAESTRA32-E16-MEDIDOR-FAMILISMO.md. Al cerrar, ## CONSUMIDO con el PR.

FP pre-asignadas: FP-196–FP-197 (máximo hoy FP-193; E15 tiene 194-195; re-deriva y confirma que 196-197 siguen libres antes de usarlas).

CONTADOR: Coeficientes ejecutables con base medida: 6 → 7 (o 6 → 6 si el falsador dispara) · pares con β̂: 6 → 7 de 15.

Lo que este acto NO hace: No toca G5.radio_confianza (E17). No escribe reglas (E18). No identifica: asocia, y lo rotula.

Sucesores declarados, no lanzados: E18 · REGLAS-OLA5-FASE1 (misma caja, tras este merge) · re-derivación del marco-M cuando el desenlace de G5 tenga regla (fase 1).

## CONSUMIDO

Ejecutado 31/ago/2026 en `acto/maestra32-e16-medidor-familismo` (worktree
`/home/pc0/mm-e16-medidor-familismo`). PR: **PENDIENTE — placeholder, el
orquestador abre el PR y corrige este número.**

Resumen: `tools/medicion_familismo.py` mide G5.familismo_apoyo sobre
eder2017 (`financia_8` x corresidencia con familiar adulto) y endireh2016
(`p4_8_2`/`p4_8_3` x `p18_4`, robustez). Ajuste de constructo (a): AMBOS
instrumentos VÁLIDOS (falsador del acto NO disparado). β̂ EDER (primaria)
`+0.0041 [IC95% 0.0029,0.0054]`, n=14887; β̂ ENDIREH (robustez) `-0.0461
[IC95% -0.0745,-0.0181]`, n=16667 — **signos DISCORDANTES entre
instrumentos**. Rótulo escrito:
`ASOCIACION-MEDIDA·MARGINAL·DISCORDANTE-ENTRE-INSTRUMENTOS`. Solo EDER
lleva `valor_ejecutable`; ENDIREH queda en `reserva`. Contador:
coeficientes ejecutables con base medida 6 → 7; pares con β̂ 6 → 7 de 15.
Fila B de `rutas_estimabilidad_coeficiente.detalle`: SIN-RUTA → RUTA-A.
`tests/test_matriz_sellados.py`: overrides re-derivados 6 → 7. `tests/
check.py --baseline`: VERDE frente a `HEAD`, salvo **1 FAIL nuevo fuera
de perímetro** (`T25`, rótulo pelado `E16` del propio nombre de archivo
de este encargo) — no resuelto porque su arreglo requiere editar
`canon/registro-rotulos.tsv` y/o `tests/check.py`, ninguno en el
perímetro declarado de este acto; reportado a dirección/orquestador, no
forzado. Detalle completo, n por universo, tabla condicionada y
veredictos (a)/(e): `forense/notas/2026-08-31-familismo-cierre.md`.

ADR siguiente disponible: **PENDIENTE de creación** (fuera del perímetro
de este acto) — ver reporte final del acto para número sugerido y
contenido.
