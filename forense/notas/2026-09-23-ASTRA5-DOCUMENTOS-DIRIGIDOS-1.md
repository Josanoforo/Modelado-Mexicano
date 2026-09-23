# ASTRA5-DOCUMENTOS-DIRIGIDOS-1 · Recibo documental para #1079

Fecha: 2026-09-23. Entorno: NUBE, sin apertura de microdatos. Base: `origin/main` `a6ed79a9d374d7af8029ab8803367261e423167a`. Encargo consumidor: [#1079](https://github.com/Josanoforo/Modelado-Mexicano/pull/1079), `forense/analisis/dominios/hoja-adquisicion.md` en la rama `codex/astra5-mapa-dominios-1`.

La instrucción del usuario de esta sesión autoriza registrar documentos en `data/manifiesto.yaml` y supera para este acto el perímetro de solo lectura del encargo U0. No se modificó #1079 ni se abrió dato reservado.

## Entradas nuevas: cinco PDF, cero microdatos

| Consumidor y fila | id de manifiesto | archivo en corpus compartido | SHA256 recalculado | verificación |
|---|---|---|---|---|
| U1 / ENOE-001..003 | `enoe_n_diseno_muestral_pdf` | `enoe_n_diseno_muestral.pdf` | `42eaa300fcbd4bec98c2a38f3edb5912bcc2208fe69a54a0c1103b75a85dbd09` | COINCIDE |
| U4 / TEC-001 | `endutih2024_cuestionario_pdf` | `endutih2024/CENDUTIH2024.pdf` | `95514c5fe0a000bfaf29062a9cf9225ec64674dbb83df6a44a3dceda13187800` | COINCIDE |
| U4 / TEC-001 | `endutih2024_diseno_muestral_pdf` | `endutih2024/endutih2024_diseno_muestral.pdf` | `97ee8088cd12d3112e1d0f3bf4bafb1bb11a9175b93b3dfb9bab61e08833b612` | COINCIDE |
| U2 / GEN-001 | `endireh2021_cuestionario_a_pdf` | `endireh2021/endireh2021_cuestionario_a.pdf` | `d2de0f03b8d347b298f7355312953d772a94edf21443bded042dd2a2ec487ae1` | COINCIDE |
| U2 / GEN-001 | `endireh2021_diseno_muestral_pdf` | `endireh2021/889463907183.pdf` | `16d023f62b69942d3ffe3646817a2406d942bacc6461b3389913ecd7cd367692` | COINCIDE |

U3 / POL-001: el reporte técnico LAPOP 2023 **ya estaba registrado** en `origin/main` como `abmex2023_technical_report_v4_0_final_eng_231117`, SHA `f12f33d7c957f2020eb3e7a2c49e9bc21fe0372b501f753fcbfcb929541e4b05`. `tests/manifiesto.py --compara-sha` contra el PDF documental leído en `/tmp` dio `COINCIDE`; la raíz `descargas_mx` no está configurada en este worktree. No se duplicó el id ni se bajó el dataset LAPOP.

## Fuente y condiciones leídas

Los cinco PDF INEGI proceden de las URLs primarias consignadas en sus entradas. Se leyeron los [Términos de Libre Uso](https://www.inegi.org.mx/inegi/terminos.html): permiten copiar y distribuir información conservando metadatos, exigen crédito a INEGI y distinguir las transformaciones propias de las del Instituto. Cada entrada porta esa condición. Para LAPOP, el [acceso y cita actuales de CGD](https://www.vanderbilt.edu/cgd/data-access/) piden citar la versión y no compartir archivos de datos directamente; este acto solo comparó el PDF técnico.

## Comandos y alcance

`python3 tests/manifiesto.py --verifica --id enoe_n_diseno_muestral_pdf --id endutih2024_cuestionario_pdf --id endutih2024_diseno_muestral_pdf --id endireh2021_cuestionario_a_pdf --id endireh2021_diseno_muestral_pdf` devolvió **data_raw: coincide=5, no_coincide=0, ausente=0, sin_configurar=0**. El manifiesto pasó de 1652 a 1657 entradas. El comando también imprimió avisos de procedencia derivados de entradas ajenas; no son fallos de estas cinco. Se verificó `abmex2023_technical_report_v4_0_final_eng_231117` con `--compara-sha` y devolvió `COINCIDE`.

## NO-CORRIDO / RESERVAS

No se descargó, abrió ni duplicó microdato. No se abrieron olas reservadas; el registro documental no cambia sus permisos. ENDIREH B/C/General siguen fuera de la solicitud concreta GEN-001; si U2 persigue el agregado 70.1%, debe precisar y registrar esas piezas por su propio contrato. LAPOP requiere comprobar en CAJA la raíz `descargas_mx` y la licencia aplicable al dataset antes de abrirlo.

## CONSUMIDO

Hoja de adquisición de #1079, commit `ade8ded3` en `codex/astra5-mapa-dominios-1`. La transferencia de estos ids se completa mediante el commit de este acto, que U0/U1/U2/U3/U4 deberán leer por SHA antes de actualizar sus cortes.
