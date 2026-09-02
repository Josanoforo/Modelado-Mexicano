ENCARGO · ACTO MAESTRA34-L3 · CORPUS-SANO-Y-CNGMD — invoca /acto (y /adquiere)
SHA de redacción: 3c3ab3a. Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: GATED a MAESTRA34-N6 fusionado (verifica por producto: `git show origin/main:tests/check.py | grep -c "data/raw"` dentro de T27 > 0 y tests/baseline.json recongelado después de c6a0d72). Sin N6, la cascada no puede dar VERDE en caja; si igual se lanza, reporta como A1 (ROJO-solo-T27) y no PARA.

ENTORNO ASIGNADO: UBUNTU (caja: corpus, red a inegi.org.mx e ine.mx por sonda A.2). NO se lanza en NUBE. MODELO SUGERIDO: Opus. Un solo acto de caja a la vez.
COMPUERTA: la de arriba.

FIRMAS DE MESA — verbatim, 1/sep/2026: «DT - … si es así entonces A. DN-a. DS-a.» (condición de DT verificada por dirección, ver N6). DS-a: estados para la pieza cívica = Coahuila y Estado de México (local 2023 no concurrente vs 2024 concurrente); mesa baja SICEE en navegador; este acto aporta el crosswalk.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 3c3ab3a ═══
(1) ESTRUCTURA: corpus compartido /home/pc0/mm-corpus/raw (symlink data/raw); Dominio 1 (manifiesto por tests/manifiesto.py); registro del curador por las tres capas (vía documentada por N6 en GUIA §alta); /adquiere §5 y §6.
(2) CONTENIDO:
  - Symlink autorreferente `/home/pc0/mm-corpus/raw/raw → /home/pc0/mm-corpus/raw` (12/ago, documentado, no reparado; A1 cierre §6, ×18) → EXISTE-NO-SATISFACE. Verifica con `ls -la /home/pc0/mm-corpus/raw | grep " raw ->"` y reporta.
  - CNGMD 2023: DescargaMasiva_192026_194559.zip en corpus trae DescargaMasivaOD.xml con 87 URLs `https://www.inegi.org.mx/contenidos/programas/cngmd/2023/datosabiertos/m<N>/<tabla>_cngmd2023_csv.zip` (m1 2 · m2 31 · m3 23 · m4 9 · m5 6 · m6 10 · m7 6), 0 descargadas (A1 pendientes-v2 §2) → EXISTE-NO-SATISFACE (orden de descarga sin datos).
  - Crosswalk sección electoral → municipio (INE): `grep -i "seccion\|crosswalk\|catalogo.*municip" data/manifiesto.yaml` → pega la salida; dirección lo clasifica NO-ENCONTRADO al 1/sep. Es lo que resolvería la granularidad municipal del PREP ya en corpus (A1 pendientes-v2 §4, hueco declarado en ficha R7.1).
  - SICEE local Coahuila/Edomex: lo baja mesa (DS-a); si ya está en Descargas MX al arrancar, regístralo aquí (misma vía que A1).
(3) COBERTURA RETROACTIVA: no aplica.

PIEZAS (un commit por pieza; ninguna estima)
P1 · SYMLINK (DT-a). Elimina el enlace `raw/raw` (solo el enlace, `rm` del symlink, nunca `rm -r`), verifica con `find /home/pc0/mm-corpus/raw -maxdepth 1 -type l` = 0 y que `find data/raw -type f | wc -l` baje al conteo real (reporta antes/después, A.13). Nota en hallazgos.md.
P2 · CNGMD 87 URLs. `/adquiere` lee el XML y baja por curl en este orden: m1 (2) → m3 (23) → m2, m4, m5, m6, m7 (62). Verifica estructura por ZIP (`zipfile.testzip()`), sha por `--registra` (una invocación por --id, A.1), `usado_para` = módulo y tabla, `url_origen` = la URL del XML. Cola del registro: CNGMD → OBTENIDO con los ids; regenera la vista. Si un host responde soft-404 (2263 B, ya documentado), estado NO-OBTENIDO-POR-ESTE-AGENTE(N) con salida cruda; no se inventa. Si el tiempo de sesión no alcanza para los 62 restantes, cierra con los que sí y deja la lista exacta de faltantes.
P3 · CROSSWALK SECCIÓN→MUNICIPIO. ≥4 rutas (portal INE de cartografía/estadística, datos.gob.mx CKAN, SICEE si expone catálogo, repositorio documental INE) con salida cruda por ruta; éxito → registro por las tres capas relacionado con R7.1 y la necesidad cívica; fallo → receta de navegador ≤1 min. Prohibido concluir nada sobre el portal desde memoria (A.5).
P4 · VEREDICTO A.4 Y SUCESOR. Con lo que P2/P3 traigan (y SICEE si mesa ya lo bajó): ¿existe ya, para Coahuila o Edomex, elección local 2023 + concurrente 2024 con lista nominal y votos por municipio? Si EXISTE-SATISFACE, deja REDACTADO (no lanzado) `MAESTRA34-L4 · CIVICA-CONCURRENTE` con la spec de L1-spec.md:502-508 y los estados/años exactos. Si no, nombra qué mitad falta.

PERÍMETRO Y CONCURRENCIA: corpus (symlink, payloads nuevos) · data/manifiesto.yaml (vía script) · data/curacion-registro/{cola-adquisicion-registro, aliases-fuentes, evidencias, relaciones, utilidad-modelo}.tsv (por la vía de N6) · data/cola-adquisicion-v1_0.tsv (regenerada) · forense/hallazgos.md · notas · forense/encargos/ (L4 redactado, sin encolar) · tablero · A.3 · cascada. En paralelo: nube (N3/N5 gateados). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar.
CONTADOR: payloads OBTENIDO +N (hasta 87) · crosswalk +1 si llega · symlink −1 · cero estimaciones.
LO QUE NO HACE: no mide; no carga reglas; no baja SICEE (es de mesa por navegador); no toca corridas ni el marco.
SUCESORES: MAESTRA34-L4 · CIVICA-CONCURRENTE (si P4 lo redacta) · N5 (Ola 6) recibe CNGMD como fuente de cívico/autoridad local.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA34-L3 · CORPUS-SANO-Y-CNGMD`, 1/sep/2026, entorno
UBUNTU, con la skill `/acto` (`ADR-237`). `ADR-280`. PR: ver la rama
`acto/maestra34-l3-corpus-sano-y-cngmd`.

Compuerta: **no se cumplía al arrancar** —`data/raw` dentro de
`t27_infraestructura` = 0, no `>0`, con control positivo `grep -c 'T27'` = 3 sobre
el mismo tramo— y se procedió por la cláusula que este mismo encargo escribe
(*«si igual se lanza, reporta como A1 (ROJO-solo-T27) y no PARA»*).
`MAESTRA34-N6` fusionó por `PR #456` a mitad de acto, con `P1`-`P4` ya completos
y antes de la cascada, así que la compuerta quedó cumplida y la cascada cerró en
**VERDE**, no en ROJO-solo-T27.

P1 símlink eliminado (remedio (c) de `FP-229`, que cierra con los dos remedios
aplicados) · P2 **87 de 87** payloads del CNGMD 2023 · P3 crosswalk
sección→municipio **encontrado** por la ruta (iv), vintage 2016 · P4 veredicto
**`EXISTE-NO-SATISFACE`**, `MAESTRA34-L4 · CIVICA-CONCURRENTE` **no redactado**
porque el encargo lo condicionaba a `EXISTE-SATISFACE`.

Detalle: `forense/notas/2026-09-01-MAESTRA34-L3-cierre.md`.
