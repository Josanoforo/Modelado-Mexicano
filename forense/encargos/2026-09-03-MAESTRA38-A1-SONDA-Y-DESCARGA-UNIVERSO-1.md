ENCARGO · ACTO MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1 — invoca /acto

SHA de redacción: 2e79d153 · COMPUERTA: ninguna (INFRA-1 corre en nube y no toca el contenido del manifiesto; si al arrancar el writer de cola existe en origin/main, se usa; si no, tsv_crudo.py y GUIA §32 — se declara cuál). ENTORNO ASIGNADO: UBUNTU con corpus y red, worktree propio; A.2 tres partes + data/raices.local.yaml con descargas_mx. NO en NUBE (mesa: «tiene que ser en ubuntu»). MODELO SUGERIDO: Opus (identidad de fuente y A.4 con FD a la vista); Sonnet no, porque decide qué bajar. CARRILES caja: éste primero; INFRA-2 y L2 después. Nadie más escribe data/manifiesto.yaml en caja mientras corre.

FIRMA DE MESA — verbatim: la de «Universo desconocido» en §0. Traducción: sondear y descargar en el mismo acto lo que sea público; lo que exija cuenta o solicitud, receta de un minuto y fila PENDIENTE-DE-MESA.

═══ A.8 contra 2e79d153 ═══ Las 12 candidatas del consolidado §3.2 salen NO-ENCONTRADO por comando sobre manifiesto (1 233) y cola (112), con frontera de palabra y nombre largo: ENADIS, ENCO, ENCRIGE, MOTRAL, CONEVAL, ENJUVE, ENVE, ENH, Intercensal 2015, CSES México, Reuters DNR México, Pew Global Attitudes México. Reglas/necesidades que las piden: N21 (R1.4, 0 payload), N34/N35 (0 relaciones), 9 reglas activas NO-ENCONTRADO (E18), 10 de Ola 6 sin instrumento; la tabla candidata→dominio del consolidado es la guía, no la conclusión. Ninguna fue abierta byte a byte: SIN-FETCH hasta este acto (A.6).

SPEC — lotes de 4 (D-11), tres lotes, dos commits por lote. COMMIT-1 del lote congela: candidatas, la pregunta de cada una (qué regla/necesidad), qué cuenta como «trae lo que se pide» (variables/temas esperados, escritos antes de abrir el FD), y la frase de sello. COMMIT-2: (a) sonda de alcanzabilidad de las cuatro rutas antes de leer contenido (v2.2, tres hallazgos distintos: no alcanzable / sin el dato / nadie corrió el mecanismo); (b) fetch real del FD/cuestionario y veredicto A.4 con texto; (c) descarga de microdato + FD cuando sea pública sin cuenta, A.7 con doble descarga y hash de contenido para zips con token, testzip, registro por las tres capas (manifiesto vía --escanea descargas_mx --grupo '<subcarpeta>/*' + --promueve; fila nueva en la cola; alta de fuente por §32/alta_relacion.py cuando exista), anti-PR#77 al cierre; (d) cuenta o solicitud → receta ≤1 min y fila PENDIENTE-DE-MESA. Depósito en descargas_mx/UNIVERSO-2026-09/<fuente>/. Lotes: 1 = ENADIS · ENCO · ENCRIGE · MOTRAL (INEGI, mayor rendimiento) · 2 = CONEVAL · ENJUVE · ENVE · ENH · 3 = Intercensal 2015 · CSES · Reuters DNR · Pew. Una pieza que PARA no tumba el lote. Al cierre: /mapea de las 9 reglas NO-ENCONTRADO contra los FD nuevos indexados (tools/inventario_reactivos.py --raiz descargas_mx sobre la subcarpeta), sólo como censo — cero veredictos de regla, eso es sucesor.

PERÍMETRO Y CONCURRENCIA. Toca: data/manifiesto.yaml (+N entradas) · data/manifiesto-staging.yaml (transitorio) · data/curacion-registro/{cola-adquisicion-registro,aliases-fuentes,relaciones,procedencias,utilidad-modelo}.tsv + baseline.json · vista T26 · data/inventario-reactivos-descargas-mx-v1_2.tsv (nuevo, v1_1 intacto) · forense/notas/2026-09-0X-MAESTRA38-A1-{spec-lote-n,resultados}.md · forense/notas/…PAQUETE-RECETAS-4.md · forense/hallazgos.md · tablero · INFRAESTRUCTURA · A.3 · cascada. NO toca: milpa/** · canon · tests/manifiesto.py · tools/curador_registro/*.py · filas existentes de la cola (A2) · forense/encargos/* (N9). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR: ADR-331 (deriva; con cuatro actos en vuelo, renumera quien fusiona segundo) · FP-290 recibo · FP-291 «mesa ejecuta recetas de cuenta/solicitud» (vence 7 días). CONTADOR: candidatas sondeadas 0 → 12 · veredictos A.4 con FD 0 → declara · payloads +N · fuentes en cola +N · reglas NO-ENCONTRADO con candidata 9 → declara · medición de modelo: cero (adquisición). Lo que NO hace. No mide p; no sella reglas; no da veredicto sobre Ola 6; no cierra filas de la cola de A2; no toca julio ni v2 de ENSANUT.

Orden de lanzamiento

Caja: MAESTRA38-A1 (hoy, en cuanto la caja quede libre) → INFRA-2 → L2 (con el .dta de ICPSR si mesa lo bajó, como medición de primera mano). Nube: INFRA-1 (corriendo) → N8 → A2; N9 en paralelo desde ya. Mesa, a mano (D6/D7, ≤10 min): cuentas ICPSR y WB, .dta de 35024, microdato WB 6667, PDN S1/S2/S6 → a descargas_mx/, y una línea aquí con los nombres; el [CENSO] de N6 los ve al día siguiente y el siguiente acto A los registra.

Contadores movidos por este documento: cero. Declarado.

## CONSUMIDO

Ejecutado por `PR #524` · rama `acto/maestra38-a1-sonda-y-descarga-universo-1` ·
`ADR-330` (renumerado desde 328: `MAESTRA37-N8` e `INFRA-2` tomaron 328/329
 al fusionar origin/main antes que este acto) · `FP-290` (recibo) / `FP-291`
 (recetas de cuenta/solicitud, vence 7
días) · 3/sep/2026, UBUNTU con corpus y red.

Commits: `3fa0975` (0-bis A.3) · `5e8cc73`/`5f1c53f` (Lote 1, COMMIT-1/COMMIT-2:
ENADIS · ENCO · ENCRIGE · MOTRAL) · `d2a2659`/`254e81b` (Lote 2, COMMIT-1/COMMIT-2:
CONEVAL · ENJUVE · ENVE · ENH) · `a6c775b`/`b108049` (Lote 3, COMMIT-1/COMMIT-2:
Intercensal 2015 · CSES · Reuters DNR · Pew) · `0cf0d59` (censo de cierre, 9 reglas
NO-ENCONTRADO) · `d776da9` (cascada: ADR-328 [luego renumerado a 330, ver
 `b55b8a1`], L0, registro-rotulos, suite VERDE) ·
`7120457` (corrección aritmética: manifiesto 1233→1256, no 1253 — declarada, no
silenciada).

Resultado: 8 de 12 candidatas con veredicto A.4 (4 verificados byte a byte contra
FD/microdato real: MOTRAL→N35, ENCRIGE→N18, ENVE→N16 — las tres EXISTE-NO-SATISFACE;
ENADIS→N15, ENCO→dinero.consumo.estatus_mediado_por_credito — ambas NO-ENCONTRADO;
4 exploratorias sin regla previa: ENH, CONEVAL, Intercensal 2015 obtenidas completas,
ENJUVE OBTENIDO-PARCIAL por hallazgo genuino de A.6). 3 PENDIENTE-DE-MESA (CSES,
Reuters DNR, microdato de Pew) con receta ≤1 min cada una. Manifiesto 1233→1256
(+23); cola 112→124 (+12 filas); tres relaciones CANDIDATA nuevas por GUÍA §32.

Desviación declarada, numeración: el encargo proponía `ADR-331`. Primera derivación
al cierre (contra `origin/main = ff68b9f`): candidato `328` — ninguno de los "cuatro
actos en vuelo" que el encargo citaba había tomado un ADR nuevo todavía. Segunda
derivación, real, al fusionar `origin/main` de nuevo para la enmienda de abajo:
`MAESTRA37-N8` e `INFRA-2` (`PR #525`) habían fusionado primero y tomado `328`/`329`
— candidato re-derivado `330`, mismo criterio que el propio encargo anticipaba
("renumera quien fusiona segundo").

## Enmienda post-cierre (mismo día, 3/sep/2026) — sonda lateral de las 3 PENDIENTE-DE-MESA

Encargo directo del usuario, no archivado por A.3 aparte (corre sobre el mismo
PR/rama, no abre encargo nuevo): "persigue todas las posibles [vías], usa tu
imaginación, formas y varias maneras de intentar la descarga" — sobre CSES,
Reuters DNR y el microdato de Pew. Detalle completo en
`forense/notas/2026-09-03-MAESTRA38-A1-sonda-lateral-pendientes.md`, `ADR-331`.

Commits: `a411227` (workflow de 4 agentes, registro por las tres capas) ·
`b55b8a1` (merge de `origin/main`/PR #525, resuelve la colisión de numeración
de arriba, reconstruye gobernanza/L0/registro-rótulos completos, no solo el
conflicto).

Resultado: `CSES` → `OBTENIDO` (Wayback Machine + CIDE, sin cuenta) · `Pew`
microdato → `OBTENIDO` (bypass del muro de cuenta vía la REST API pública de
WordPress del propio sitio, 7 olas con México confirmado) · `Reuters DNR` →
`OBTENIDO-PARCIAL` (9 tablas topline México vía gráficos Datawrapper públicos;
el microdato individual sigue on-request, sin cambio) · `ENJUVE` confirmado
punto muerto genuino (Wayback CDX completo de `/inmujeres/`, sin sucesor
gubernamental desde 2010), mismo estado, evidencia mucho más fuerte. Manifiesto
`1256 → 1281` (+25; total del acto completo, dos rondas: `1233 → 1281`, +48).
Sin alta `GUÍA §32` — mismo criterio que Lote 2/3, ninguna de las cuatro tiene
regla/necesidad hipotetizada en el repo.

Ningún dominio se abrió, ninguna regla se selló, Ola 6 no se tocó, la cola de A2
no se cerró, no se abrieron candidatas nuevas (siguen siendo las 12 del encargo
original) — exactamente lo que el encargo, y su enmienda, declaran que este acto
no hace.

## Enmienda 2026-09-04 — restauración de FP-291/FP-292, perdidas en el merge de PR #527

`FP-291` (recibo, «mesa ejecuta recetas de cuenta/solicitud», declarada arriba
y en `## CONSUMIDO`) y `FP-292` (recibo del resultado de esas recetas tras la
sonda lateral de la enmienda de arriba) no existían como filas en
`forense/firmas-pendientes.tsv` pese a estar declaradas por este encargo:
`grep -c '^FP-291' forense/firmas-pendientes.tsv` daba 0. Investigado contra
`git log --all -- forense/firmas-pendientes.tsv` y ambos padres del merge de
`PR #527` (`68ce2a8`, padres `7a3e2ab4`/`74e0c49a`): **ninguno de los dos
lados del merge tenía jamás esas filas** — no es un conflicto de merge que
las descartó, es que nunca se escribieron pese a que el encargo las declaró.
Restauradas el 2026-09-04 con el contenido que este mismo documento fija:
`FP-291` = recibo de las 3 recetas de cuenta/solicitud (CSES, Reuters DNR,
Pew); `FP-292` = recibo del resultado de esas recetas — `CSES` SUPERADA por
la sonda lateral (OBTENIDO sin cuenta, ver enmienda de arriba); `Pew`
microdato OBTENIDO (misma sonda); `Reuters DNR` microdato individual sigue
on-request → MESA-DECIDE solicitar o no. Contenido exacto de ambas filas no
recuperable del historial (nunca existieron); reconstruidas fielmente a lo
que este encargo y su enmienda ya declaraban, fecha `creado=2026-09-03`,
nota "perdidas en merge #527". Detalle del hallazgo (por qué `A.12` no las
atrapó) en `forense/hallazgos.md`, entrada `A.12`.
