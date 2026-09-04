# MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1 — resultados Lote 1 (COMMIT-2)

Spec congelada: `forense/notas/2026-09-03-MAESTRA38-A1-spec-lote-1.md`. Las
cuatro candidatas del Lote 1 (ENADIS, ENCO, ENCRIGE, MOTRAL) quedan
**sondeadas, descargadas y registradas** contra el criterio congelado
ahí — sin ampliarlo ni estrecharlo después de leer el FD.

## (a) Sonda de alcanzabilidad (v2.2)

Portal reachable (host responde, `curl -s -o /dev/null -w %{http_code}`) para
las cuatro: ENADIS 200, ENCO 200, ENCRIGE 200, MOTRAL 200. **Advertencia
medida en el propio proceso**: el sitio de INEGI es una SPA (React) que
devuelve `HTTP 200` con el shell de la app para casi cualquier ruta —
`no alcanzable` / `sin el dato` / `nadie corrió el mecanismo` no se
distinguen por código HTTP aquí; cada candidato de descarga se verificó por
**firma de bytes** (`PK\x03\x04` para zip, `%PDF` para PDF vía
`curl -r 0-4 | xxd`), no por código de estado — un 200 con
`3c21444f...` (`<!DO`) es el shell falso, no el archivo.

Para las cuatro, la ruta de FD/cuestionario se resolvió vía el catálogo RNM
de INEGI (`inegi.org.mx/rnm/index.php/catalog/<id>/related-materials`, que
sí es servido por el servidor, a diferencia del portal react) y verificó
real por firma de bytes. La ruta de microdato para ENADIS y ENCRIGE se
resolvió por el patrón `datosabiertos/conjunto_de_datos_<slug>_<año>_csv.zip`
(deducido de entradas ya existentes en el manifiesto para otros programas
INEGI). Para ENCO y MOTRAL, ese patrón **no** existía — todos los intentos
devolvían el shell SPA. Se agotó sondeo directo (curl, WebSearch, crawl del
catálogo RNM) sin resultado; se delegó un sub-agente (Sonnet) dedicado a
buscar más, que encontró el mecanismo real: el sitio expone un JSON REST
en `inegi.org.mx/app/descarga/componente/descargamasiva/lista/archivoscompaginacion`
parametrizado por `idBiinegi` (id numérico interno leíble sin ejecutar JS,
desde un sidecar `pestanaData.js` de cada programa) — **hallazgo
reutilizable para cualquier acto de adquisición INEGI futuro** que tope con
el mismo shell SPA; candidato a nota corta en `forense/hallazgos.md`.

## (b)+(c) Fetch de FD y descarga de microdato, con veredicto A.4

| candidata | FD/cuestionario | microdato | A.4 (contra criterio congelado) |
|---|---|---|---|
| ENADIS | 3 PDF reales (`_fd`, `_cuestionario_general`, `_cuestionario_opinion`) | zip real, 2369 archivos, testzip OK | **NO-ENCONTRADO** para N15/deferencia — verificado byte a byte en ambos cuestionarios: cero ítems de deferencia dada (obedecer/no-contradecir autoridad), sólo discriminación recibida y demografía de jefe/jefa de hogar |
| ENCRIGE | 1 PDF real | zip real, 392 archivos, testzip OK | **EXISTE-NO-SATISFACE** para N18/`tramite.evasion.norma_inutil_sancion_improbable` (una de las 9 NO-ENCONTRADO de E18-P2) — cobertura parcial fuerte: Sección VIII trae requisitos/costos excesivos, sanciones/clausuras injustificadas, batería de motivos de cumplimiento (evitar multas/inspecciones); no trae ítem directo de inutilidad percibida ni de probabilidad de sanción |
| MOTRAL | 2 PDF reales (2012, 2015) | 2 zip reales (DBF), testzip OK | **EXISTE-NO-SATISFACE** para N35 — confirmado contra el DBF real (tabla `empleos`, 13651 filas persona-empleo 2007-2012: `SALARIO` + formalidad `P8` IMSS/ISSSTE/privada/no-asegurado por empleo) y contra el cuestionario completo (ítems 1-10 trayectoria + 11-23 AFORE/ahorro): disparador y desenlace factual presentes, ningún ítem de preferencia/trade-off. Mismo veredicto que `forense/notas/2026-09-03-mapeo-ola6-N5.md` (hueco de instrumento, no de dato) — ahora confirmado desde una fuente distinta |
| ENCO | 1 PDF real (básico) | zip real (DBF, agosto 2026), testzip OK | **NO-ENCONTRADO** para `dinero.consumo.estatus_mediado_por_credito` — confirmado contra el DBF real (`encocb`, 15 ítems P1-P15): ninguno sobre modalidad de pago ni marca; el instrumento no toca la regla en absoluto |

Ninguna requirió cuenta ni solicitud — las cuatro son públicas. Ninguna
pieza paró.

## (c) Registro por las tres capas

- **Manifiesto** (`--escanea descargas_mx --grupo '<subcarpeta>/*' --promueve`,
  por fuente, dos veces cada una — API de línea de comandos aplica un solo
  `--url` por invocación y regenera `staging` completo, así que un segundo
  `--escanea` sin promover antes pierde la asignación del primero; patrón
  correcto: escanea→promueve→escanea siguiente, dos rondas — la primera
  antes de que el sub-agente resolviera los microdatos de MOTRAL/ENCO, la
  segunda después): **1233 → 1245** entradas (+12: 1 microdato + 3 FD de
  ENADIS, 1 microdato + 1 FD de ENCRIGE, 2 microdatos + 2 FD de MOTRAL, 1
  microdato + 1 FD de ENCO). Doble descarga + hash SHA-256 coincidente +
  `testzip` limpio para los 5 microdatos; FD con hash único (no token, no
  requiere doble descarga por A.7). *(Corrección aritmética 3/sep/2026: la
  redacción original de esta nota citaba `1233 → 1242` — el tally de la
  primera ronda de registro, escrito antes de que el sub-agente resolviera
  MOTRAL/ENCO y antes de la segunda ronda que sumó esas 3 entradas. El
  total final del acto (1233 → 1256, +23) sí era correcto en la cabecera
  del ADR-328; el error estaba en cómo se repartía entre lotes. Recontado
  contra `git log` sobre `data/manifiesto.yaml` — ver ADR-328.)*
- **Cola** (`tools/curador_registro/tsv_crudo.py`, sin módulo `csv` —
  preserva bytes de las 112 filas existentes): +4 filas, las cuatro
  `OBTENIDO` (MOTRAL y ENCO pasaron de `OBTENIDO-PARCIAL` a `OBTENIDO` tras
  el hallazgo del sub-agente). Vista `data/cola-adquisicion-v1_0.tsv`
  regenerada (112→116 filas, `tools/vista_cola_adquisicion.py`).
- **Alta de fuente (GUÍA §32)**: sólo para las dos con `clasificacion_relacion
  CANDIDATA` que sí tocan una regla/necesidad activa — MOTRAL→N35, ENCRIGE→N18
  (`tramite.evasion_norma`, confirmado el mismo id que
  `tramite.evasion.norma_inutil_sancion_improbable` de E18-P1). ENADIS y ENCO
  quedan **fuera** de esta alta: su A.4 es NO-ENCONTRADO, el instrumento no
  toca la regla hipotetizada en absoluto — registrar una relación ahí sería
  inflar el contador de candidatas sin sustento (criterio explícito de
  COMMIT-1: NO-ENCONTRADO no registra relación, EXISTE-NO-SATISFACE sí).
  `relaciones.tsv` 219→221, `evidencias.tsv` 220→222, `utilidad-modelo.tsv`
  219→221 (proyección 1:1 conservada), `aliases-fuentes.tsv` 15→17.
  `data/curacion-registro/baseline.json` regenerado a mano (no hay script
  que lo escriba — confirmado en el propio texto de §32) y `baseline.py`
  corre en **VERDE** (`"ok": true`, cero errores) contra las tres invariantes.

## Corrección a la premisa A.8 (ver spec-lote-1) — reafirmada

Pew (Lote 3) tiene fetch parcial previo (FP-29); las cuatro de este lote
sí eran SIN-FETCH limpio, confirmado sin excepción.

## Anti-PR#77

Los 12 payloads nuevos quedan en `descargas_mx/UNIVERSO-2026-09/<fuente>/`
(corpus compartido, NO en el worktree de esta sesión) — verificado
(`ls -la` sobre la ruta absoluta de `descargas_mx`, fuera de este worktree).

## Contador movido por este lote

Candidatas sondeadas: 0 → 4 (de 12). Veredictos A.4 con FD: 0 → 4. Payloads:
+12 (dos rondas de registro, ver corrección arriba). Fuentes en cola: +4. Relaciones nuevas (CANDIDATA): +2. Reglas
NO-ENCONTRADO con candidata: 9 → 8 (N18/ENCRIGE deja de estar sin candidata;
sigue sin cerrar — EXISTE-NO-SATISFACE, no EXISTE-SATISFACE).
