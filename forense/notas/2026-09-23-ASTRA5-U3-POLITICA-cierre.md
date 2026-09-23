# Cierre de preparación · ASTRA5-U3-POLITICA

**Base:** `origin/main` = `8e41f72fa8b00a20e83f28c92f6b2964e66b0081`;
worktree `/home/pc0/mm-astra5-politica-1`, rama `codex/astra5-politica-1`.
Encargo verbatim SHA256 `bc255836ca9e8ed7a32c578961e302d99a79e7b855eb809ba4863660aa6bc679`;
0-bis `df0db6e2`. Entorno CAJA WSL2, corpus montado; LAPOP de respaldo
`descargas_mx` con hash y tamaño COINCIDE contra manifiesto. No se abrió
ENCO, ENVIPE 2026, la última ola ENOE ni otra ola reservada.

## EJECUTADO / LEÍDO / REPORTADO

- **EJECUTADO:** `CALC-INE-PISOS-2024-0001` (9 773 730 filas,
  numerador/denominador administrativos), `CALC-ENCUP-PISOS-2012-0002`
  (primer resultado parcialmente NO-ESTIMABLE conservado intacto en
  `forense/historico/ASTRA5-U3-POLITICA/CALC-ENCUP-PISOS-2012-0002.tar`,
  SHA256 `17f1121fb33b43e2b2b40d0607b00ca880eb7ea1831116e7b0e00a6dd6648213`,
  sello COINCIDE tras extracción), sucesor `0003`
  (recodificación de etiquetas) y `CALC-LAPOP-PISOS-2019-0001` (dos
  proporciones con IC de diseño aproximado). Cada spec y medidor fueron
  commiteados antes del run de su microdato. El intento ENCUP `0001` falló
  antes de sello por nombres de cabecera; no se ocultó.
- **LEÍDO:** manifiesto por id/archivo/alias, descriptor INE, cuestionario
  ENCUP 2012, codebook LAPOP 2019, reporte GEN1 y CALC GEN2 preexistente.
  Los 45 IDs `ine_*` quedan clasificados por objeto y razón de uso.
- **REPORTADO:** tres tablas sin mezclar personas y secciones, origen
  numérico NUEVO por CALC, notas U0, límites, falsadores y reporte de
  auditoría de rigor extremo. No se produce serie ni retador.

**Contador inicial/final:** vista `corridas.tsv` de base: 146 `SELLADA` con
`cuenta_gen2=SI`; vista final no movida: 146. En disco se añaden tres CALC
activos sellados con etiqueta SI y adopta NO, pendientes de registro/adopción,
y un cuarto en archivo histórico con sello idéntico.
`celdas_validadas` no se tocó. El canal vigente de publicación es el job
del push a main (`registro --verifica --escribe --lote` derivado de los
asientos); este PR no modifica las vistas globales. La colisión propia de
IDs ENCUP 0002/0003 se resolvió archivando 0002 sin alterar bytes ni sello.
`corrida0 status --json` deriva sin error. Estado de los tres activos:
**sellada en disco, no registrada** hasta el canal de `main`.

## NO-CORRIDO / RESERVAS

- `NC-260923-ASTRA5-U3-POLITICA-df0d-01` **CERRADA**: `ID-DUPLICADO`
  de dos RESULT ENCUP; 0002 preservado en archivo histórico y sello
  verificado. `corrida0 status --json` volvió a derivar.
- `NC-260923-ASTRA5-U3-POLITICA-df0d-02`: IC poblacional ENCUP; falta peso,
  estrato y UPM verificables. Se deja descriptivo; sucesor obtiene descriptor
  y fija un CALC nuevo si los campos existen.
- `NC-260923-ASTRA5-U3-POLITICA-df0d-03`: serie LAPOP 2004–2023; textos,
  versiones, modos y diseño no dictaminados para estos dos estimandos.
  Sucesor hace dictamen por ola antes de congelar nuevas mediciones.
- `NC-260923-ASTRA5-U3-POLITICA-df0d-04`: vistas globales no escritas por
  este PR; el canal de push a `main` debe consumir los tres asientos de
  replay. Si detecta drift ajeno, sigue el ADR de canal vigente.

## CONSUMIDO

El encargo `forense/encargos/2026-09-23-ASTRA5-U3-POLITICA.md` se preparó
en esta rama; se consigna el PR y recibo Codex al abrirlo. La adopción y
fusión corresponden a mesa.
