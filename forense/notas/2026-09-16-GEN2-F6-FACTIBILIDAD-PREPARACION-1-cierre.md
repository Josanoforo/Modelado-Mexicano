# Cierre · GEN2-F6-FACTIBILIDAD-PREPARACION-1

Base: `origin/main` = `9dffd6455c67e2ca99740e79f90be59a13f250e1`.
Worktree: `/home/pc0/mm-gen2-f6-factibilidad-preparacion-1`. Rama:
`acto/gen2-f6-factibilidad-preparacion-1`.

Estado del producto: **PREPARADA-PARA-MESA · NO AUTORIZA EMISIONES NI R**.
Cero llamadas, cero emisiones, cero estimaciones R, cero microdatos abiertos,
cero cambios al motor y cero escrituras a la cascada compartida.

## Resultado

| Candidata | Definición acreditada | M elegible | Reserva preservada | Preparación técnica | Falta para correr |
| --- | --- | --- | --- | --- | --- |
| R01 · MOCIBA 2021/2022 | **NO** · `FILTRO-NO-ACREDITADO`; `P12_5`, 1/2, `FACTOR`, `UPM_DIS` y `EST_DIS` sí están documentados, pero no el flujo que hace aplicable P12 | **NO** · la razón de no denuncia por miedo/desconfianza entre no denunciantes no produce denuncia total de ciberacoso | **SÍ** · sólo FD; no BD/R | `python3 tools/f6_factibilidad_prepara.py --cards forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/tarjetas.yaml --json` → 2/2 celdas rechazadas con causas explícitas | cuestionario/manual con flujo P12 y enlace predictivo de M firmado antes de R; ambos, no uno inferido del otro |
| R09 · ISSP ZA6980 | **CONDICIONADA** · Q8a nacional y etiqueta `v26` acreditadas por piezas separadas; falta codebook integrado de etiquetas de valor | **NO** · recepción efectiva de dinero familiar para vejez no es intención hipotética de acudir a familiares o amigos | **NO para cegamiento** · exposición incidental de distribución `v26` ya versionada; no se reproduce aquí | mismo comando → 2/2 celdas rechazadas por definición, M y exposición | excluir del duelo ciego actual; para uso descriptivo, codebook integrado y contrato distinto. La exposición no se cura con firma |

Dos olas o dos dominios siguen siendo una familia. El resultado material son
**cero familias/celdas elegibles** para ejecución, no cuatro réplicas de
evidencia ni dos familias confirmatorias.

## Evidencia documental y exposición

- MOCIBA FD 2021: SHA-256
  `375bf7c1bcdbcc9b0716cd3b63fe940906a97783a3b69f2afad35f35950b1e25`;
  hoja `TMOCIBA`, filas físicas 38, 2306, 2503–2504, 2531, 2542–2543,
  2576–2578.
- MOCIBA FD 2022: SHA-256
  `923fa85a665219200d6c87d1f5af25090870bf91957d16f1008726e78edc396e`;
  hoja `TMociba`, filas 38, 2510, 2728–2730, 2765, 2776–2777,
  2810–2812.
- ISSP cuestionario México: SHA-256
  `61bc0c80415521965ec1b2546fbe3b2400cfacb2e6b0b542583304821544f2ed`;
  PDF p.3 / impresa p.2, Q8a. Background `SEX`: SHA-256
  `6004c300ca1331bfd15f163c4deaa726c71b66b46ae9e05361f40ae8cc26ca5f`.
- No se encontraron cuestionario/manual MOCIBA 2021/2022 ni codebook
  integrado ZA6980 entre los documentos adquiridos tras dos búsquedas
  acotadas; no se adquirió nada.
- La búsqueda textual sobre el árbol mostró incidentalmente una distribución
  de `v26` en `data/apertura-issp-variables-2026-08-13.tsv`. La cifra no se
  copia a spec/tarjetas/dieta. R09 queda `EXPUESTA-OBJETIVO` y pierde su
  pretensión de evaluación ciega en este procedimiento.

## Artefactos

- `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/spec.md`:
  definición, dieta, orden, comparación, presupuesto y decisión de mesa.
- `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/tarjetas.yaml`:
  lista cerrada de cuatro celdas y sus gates.
- `forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/fixtures/SINTETICO-NO-MEDICION.json`:
  casos sin datos reales.
- `tools/f6_factibilidad_prepara.py`: preflight de sólo tarjetas y funciones
  sintéticas mínimas; reutiliza el validador numérico y la excepción de
  `tools/calcula_f5_sin_fugas.py` sin modificar F5.
- `tests/test_f6_factibilidad_prepara.py`: nueve regresiones específicas.

## Pruebas y baseline

Comandos ejecutados:

```text
python3 tools/f6_factibilidad_prepara.py --cards forense/prereg-duelo-v2/F6-factibilidad-preparacion-v1_0/tarjetas.yaml --json
python3 -m unittest tests.test_f6_factibilidad_prepara
python3 -m unittest tests.test_f5_sin_fugas
TZ=UTC python3 tests/check.py --baseline
```

Resultados:

- preflight: 2 familias, 4 celdas,
  `DEFINICION_O_CANDIDATO_INSUFICIENTE=4`, autorización `false`, payloads
  abiertos `false`, modelos llamados `false`, escrituras canónicas `false`;
- pruebas nuevas: **9/9 OK**;
- interfaz heredada F5 sobre fixtures: **23/23 OK**;
- baseline final: **ROJO, 6 FAIL · 4,351 WARN; 2 entradas nuevas frente al
  baseline**. La material es T25 por el rótulo pelado “M uno” dentro del encargo
  verbatim, que no puede editarse; T16 aporta dos FAIL derivados porque
  gobernanza todavía declara 3 y la corrida real da 4 antes del propio
  self-check. Los FAIL heredados T06×2 y T08×1 y los 4,351 WARN no son de este
  acto. Por la excepción explícita, no se editaron `tests/check.py`, baseline,
  registro de rótulos ni gobernanza. La única propagación realmente necesaria
  al cierre serial es censar/eximir el rótulo verbatim del encargo y recifrar
  T16 por el mecanismo compartido vigente.

## Presupuesto recalculado

Nominal contrafactual si cuatro celdas fueran elegibles: 32 posiciones
`L_SOLO`, 4 M, hasta 4 R, B=0; con dos reintentos técnicos, hasta 96 intentos.
Viable con las tarjetas actuales: **0 posiciones, 0 intentos, 0 turnos, 0
unidades facturadas, 0 M, 0 R y 0 B**. Coste monetario pendiente de modelo,
modalidad, tarifa y conteo verificables; no se hicieron llamadas para
estimarlo.

## Decisiones materiales para mesa

1. R01: exigir flujo documental de P12 y un enlace M pre-R, o rechazarla.
2. R09: excluirla del duelo ciego; decidir sólo si conserva valor descriptivo
   no ciego bajo otro contrato.
3. Llamadas: autorizar cero bajo esta versión. Una ejecución requiere spec
   sucesora y firma explícita de identidad, presupuesto y alcance.

Texto sugerido, **no firmado ni registrado como adoptado**. Se incluye porque
el encargo lo exige; no crea una ranura nueva en el tablero: el mismo encargo
prohíbe escribir `firmas-pendientes.tsv` y ordena llevar la decisión al PR.

> TEXTO DE FIRMA SUGERIDO F6-FACTIBILIDAD-PREPARACION-1 — autoridad y fecha por completar:
> se adopta la lectura de factibilidad de la spec y sus tarjetas; R01 queda
> condicionada al flujo documental de P12 y a un enlace M pre-R; R09 se excluye
> de evaluación ciega por exposición y desalineación de constructo. Se
> autorizan cero llamadas, cero emisiones M/L/B y cero aperturas R. Toda
> ejecución futura exige spec sucesora, identidad de modelo/cliente,
> presupuesto recalculado y autorización explícita.

## Cierre compartido diferido

**CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4.** No se
asignaron IDs ni se escribieron decisiones, firmas, hallazgos, gobernanza,
estado, rótulos, tableros, rutinas, manifiesto, colas o contadores. Propagación
serial concreta: resolver sólo el rótulo “M uno” que aparece dentro del encargo
verbatim y el recifrado T16 que ese FAIL deriva. El producto F6 no depende de
esa contabilidad auxiliar.
