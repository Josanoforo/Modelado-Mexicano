═══ ENCARGO E4 · ORDEN-SUPERIOR ═══

ENCARGO E4 · ORDEN-SUPERIOR — el curador escribió que esperaba una orden; esta es la orden

Dirección (maestra-31), 26/ago/2026 · Redactado contra main = 77fddf2 (clon propio, no espejo). No gated. #381, #382 y #384 fusionados.

ENTORNO ASIGNADO: UBUNTU. NO lanzar en NUBE — este acto abre el corpus completo y sin data/raw montada no tiene los bytes. No llama red ni API (FP-165). Rótulo: ACTO MAESTRA31-E4 (D-6). Token pelado E4 colisiona; se censa, no se reclama.

═══ VERIFICACIÓN DE EXISTENCIA — CONTESTADA por dirección (clon propio, 77fddf2, 26/ago/2026) ═══

Este bloque es el más importante del encargo. Dirección buscó activamente si esto ya estaba hecho, y encontró que está hecho al 80%. Lo que sigue es qué existe, qué no, y por qué el faltante es una orden y no una herramienta.

1 · ESTRUCTURA — la maquinaria EXISTE-SATISFACE. No se construye nada.

pieza | dónde | estado
extractor multiformato (olefile, openpyxl, zipfile, pdf_extract) | tools/curador_registro/inspect_assets.py, 581 líneas | existe y corrió
esquema de reporte con grado_inspeccion y criterio_parada parametrizados | materialize_inspection_contracts.py:19-22 · schemas/inspector-contract.schema.json | existe
universo declarado | data/curacion-universo/universo-declarado-t0.tsv | 35,708 activos
inspección corrida | data/curacion-universo/reportes-inspeccion.tsv | 1,527 filas · 509 activos
esquema de fila-por-reactivo | data/reapertura-52a-54-variables-2026-08-13.tsv (208) · abrir4-variables (28) · apertura-issp-variables (14) · apertura-enfih-ensafi-v1_0 (8) | existe, 258 filas en 4 tablas
emparejador variable↔regla por token exacto | construir_crosswalk, milpa/src/emisor.py (reparado por E8, ADR-208) | existe

2 · CONTENIDO — el faltante es exactamente un nivel de profundidad, y el propio curador lo dejó escrito.

Comando y salida cruda citados por dirección (VERIFÍCALOS TÚ MISMO contra el árbol real antes de seguir; corrígelos si no cuadran, con evidencia):

awk -F'\t' 'NR>1 && $14!=""{n++} END{print n" de "NR-1}' data/curacion-universo/reportes-inspeccion.tsv
  → 1527 de 1527   (campo siguiente_objeto_no_inspeccionado, poblado al 100%)

awk -F'\t' 'NR>1{print $14}' ... | sort -u
  → "contenido más allá de la frontera declarada"
  → "contenido fuera de la frontera"
  → "documentación semántica o contenido completo, SI UNA ORDEN SUPERIOR LO SOLICITA"

awk -F'\t' 'NR>1{print $12}' ... | sort | uniq -c | sort -rn | head -1
  → 646  "Se abrió el contenedor completo y se enumeró su directorio central; solo se leyeron encabezados de miembros CSV/TSV/TXT/DBF con compresión soportada, no el contenido completo de los demás miembros."

awk -F'\t' 'NR>1{print $9}' ... | grep -cE "P[0-9]+_[0-9]+|VAR[0-9]|variable"
  → 2      (de 1,527 filas: el inventario de reactivos NO existe)

El curador abrió 509 contenedores, enumeró lo que había dentro, declaró la frontera y qué había del otro lado, y se detuvo a esperar. Esa orden nunca se dio. Su docstring dice por qué: "Este módulo no contiene nombres de fuentes reales ni conclusiones semánticas" — el cegamiento es deliberado, no un defecto.

Resultado A.4 sobre el entregable de este acto: NO-ENCONTRADO — universo: árbol completo salvo .git y data/raw, 26/ago/2026, 2,157 archivos de texto examinados. Ninguna tabla del repo tiene una fila por reactivo sin filtro de demanda. Y fíjate en el esquema de las cuatro que existen: la columna necesidad va antes que variable_encontrada. Las 258 filas se llenaron demanda-primero. Solo contienen reactivos que alguien fue a buscar.

3 · COBERTURA RETROACTIVA. El curador y su universo T0 nacen antes que coef-universo (19/ago), el cruce (25/ago) y enlace-M (26/ago). Ninguno de esos tres pudo consultar un inventario de reactivos porque no existía; los tres resolvieron a mano lo que este acto haría consultable. Esa es la deuda que este acto paga, y es medible: siete actos de las últimas tres semanas (E1, R34-ENSAFI-CENSA, APERTURA-ENFIH-ENSAFI, REAPERTURA-52A-54, ABRIR-4, INDICE-NO-INEGI, BIBLIOTECARIO-56) tuvieron como sustancia abrir payloads a mano. Siete sesiones.

⚠️ Si al ejecutar encuentras que algo de lo anterior ya está hecho —una tabla de reactivos, un modo profundo del inspector ya corrido, una rama con esto— PARA y repórtalo. Descubrirlo es el rendimiento de este bloque, y este programa ya perdió jornadas por no hacerlo.

OBJETO

Dar la orden superior que el curador declaró esperar, acotada al universo conocido —lo que está descargado hoy, no lo declarado— y producir data/inventario-reactivos-v1_0.tsv: la primera tabla del programa con una fila por reactivo y sin columna de necesidad.

Por qué importa, sin adorno: tres actos en 48 horas preguntaron "¿qué instrumento satisface esta demanda?" y volvieron con 1 de 60, 0 de 49 y 0 de 8. Los tres van demanda → oferta, cuestan un acto cada uno, y devuelven cero porque el motor pregunta cosas que ningún instrumento formuló como reactivo. La dirección inversa —qué puede contestar lo que ya tenemos— nunca se ha corrido, y no se puede correr sin esta tabla.

Lo que este acto NO hace: no empareja contra el motor (eso es E5), no adquiere nada del universo desconocido, no decide qué hacer con la tabla, no toca milpa/.

PASOS

0-bis · A.3. Commitea este encargo íntegro y verbatim en forense/encargos/2026-08-26-MAESTRA31-E4-ORDEN-SUPERIOR.md antes de nada (usa exactamente el texto del encargo que te acabo de dar arriba, entre las marcas ═══ ENCARGO E4 ═══ y el final de "PROHIBIDO" y "CONTADOR" incluidos). ## CONSUMIDO al cerrar, con el número de PR (lo agregas al final, en el paso de Cierre).

1 · Deriva el universo conocido y su solape con lo ya inspeccionado. Con comando y salida cruda: cuántos payloads hay en data/raw · cuántas entradas tiene data/manifiesto.yaml (dirección contó 794 en el árbol; ACTO MAESTRA31-E1 contó 321 archivos en data/raw en esta misma caja — esas dos cifras no cuadran y reconciliarlas es parte del entregable) · cuántos de los descargados están entre los 509 ya inspeccionados. Los tres números, sin fusionarlos.

2 · COMMIT-1 — congela la especificación ANTES de abrir un solo archivo. Escribe un archivo de spec (elige ubicación razonable dentro de forense/ o data/, p.ej. forense/notas/2026-08-26-orden-superior-spec.md) que contenga, y nada más que esto:
- Qué cuenta como reactivo. Propuesta de dirección, a confirmar o refutar: un par (variable_id, texto) donde variable_id es un identificador de columna en un archivo de microdato o en un diccionario de datos, y texto es su descripción declarada. Un encabezado de CSV sin diccionario da variable_id con texto vacío — cuenta, y se marca SIN-TEXTO, porque el emparejador de E5 trabaja por token exacto de variable, no por texto.
- El esquema exacto, heredado de las cuatro tablas existentes menos necesidad: payload_id · sha256_12 · instrumento · ola · archivo_miembro · variable_id · texto_reactivo · metodo · universo_declarado.
- Los formatos que se atacan y los que no (ver regla de tope abajo: csv/tsv encabezados, xlsx vía openpyxl, dbf si el extractor ya lo soporta, sav/dta si el extractor ya los soporta — revisa qué soporta inspect_assets.py realmente; todo lo no soportado va a NO-EXTRAIDO con el formato nombrado).
- El denominador de cobertura y qué cuenta como payload cubierto.
- Qué pasa si el rendimiento es bajo (B-bis: la escala declara el desenlace de la no-refutación antes de correr). Declara explícitamente qué significaría un resultado por debajo del falsador (cobertura <50% de payloads descargados, o <258 filas totales), y qué significaría uno muy por encima.
- Cierra con la frase de sello verbatim: «El primer resultado que produzca este procedimiento es el que se reporta.»
Commitea este archivo en un commit separado ANTES de generar la tabla.

3 · Ejecuta el inventario real:
- Lee tools/curador_registro/inspect_assets.py para ver qué parámetros/modos ya existen (busca grado_inspeccion, profundo, olefile, openpyxl, zipfile, pdf_extract) SIN EDITARLO.
- REGLA DE TOPE (no negociable): CERO herramientas nuevas de extracción. Si inspect_assets.py ya tiene un modo que sirve, invócalo (como subproceso o import). Si necesitas un consumidor delgado para armar la tabla fila-por-reactivo a partir de su salida, escribe un script nuevo FUERA de tools/curador_registro/ (p.ej. en tools/ o en la raíz, o en un scratch), que IMPORTE/REUTILICE las funciones de extracción existentes de ese módulo o lo invoque como subproceso — NUNCA reimplementes parsing de zip/xlsx/ole/pdf/dbf desde cero. Si un formato exigiría un extractor nuevo, ese formato va a NO-EXTRAIDO con el nombre del formato — eso es entregable, no fracaso.
- CERO emparejamiento contra ninguna tabla de variables ni contra milpa/. CERO red/API.
- Corre sobre el universo conocido (payloads presentes en data/raw). Genera data/inventario-reactivos-v1_0.tsv con el esquema exacto de COMMIT-1.
- Ve con cuidado de tiempo: data/raw puede tener cientos de payloads pesados (zips grandes, xlsx grandes). Está bien limitar la profundidad/tiempo por archivo si es necesario, pero documenta el criterio de corte usado y NO falsifiques cobertura.

4 · COMMIT-2 — commitea data/inventario-reactivos-v1_0.tsv en un commit separado, sin editar el de COMMIT-1 (enmienda por adición si hace falta). Universo declarado en la cabecera del TSV (como comentario o primeras filas si el formato TSV lo permite razonablemente — usa tu juicio, p.ej. líneas que empiecen con # antes de la cabecera real, o un archivo .meta hermano si mezclar comentarios en el TSV complica el parseo): SHA (del commit o de un hash del propio universo), fecha, denominador, y el conteo de NO-EXTRAIDO por formato.

5 · Evalúa el falsador declarado en COMMIT-1: si cobertura <50% de payloads descargados, o si la tabla tiene <258 filas → LA VÍA SE ABANDONA: NO iteres, NO mejores el extractor, NO pruebes otro formato. Se conserva lo producido, se documenta en forense/hallazgos.md como hallazgo con esa palabra ("abandonada"). Si cae entre 50% y el techo, repórtalo como cae — no ajustes el criterio. Si supera todo limpiamente, repórtalo también con las cifras.

6 · Cierre:
- Nota forense/notas/2026-08-26-orden-superior-cierre.md con los conteos.
- forense/firmas-pendientes.tsv: agrega SOLO la fila FP-171 (no toques otras filas) con la cifra de cobertura ante mesa. Revisa el formato de las filas existentes primero.
- Línea en forense/hallazgos.md sobre la cola del curador que estuvo 22 días sin consumir (y sobre el falsador si se disparó).
- ADR: revisa canon/ para ver el máximo ADR actual re-derivado por conteo real contra el árbol (no aritmética de memoria — lista los archivos ADR-*.md o la sección correspondiente y toma max+1). Escribe el ADR nuevo documentando esta decisión, en el lugar donde viven los demás ADRs de este repo (busca dónde están, probablemente canon/ o forense/).
- Recifrado §L0 si aplica (busca qué es esto en canon/gobernanza o estado-programa — probablemente un hash/checksum de un bloque que hay que actualizar tras editar esos archivos; si no encuentras tal mecanismo tras buscar, anótalo y sigue).
- Censo de rótulo en canon/registro-rotulos.tsv (agrega fila para ACTO MAESTRA31-E4) y en tests/check.py SOLO si hay una lista tipo _T25_ARCHIVOS_CONOCIDOS que lo exige (revisa tests/check.py para T25 y ese nombre de constante).
- Corre `python3 tests/check.py --baseline` (NUNCA --freeze) y confirma VERDE. Si falla, arréglalo dentro del perímetro permitido (los archivos listados abajo) y vuelve a correr hasta VERDE, documentando qué arreglaste.
- Crea el PR con `gh pr create` desde la rama maestra31-e4-orden-superior contra main. NO hagas push --force ni merge.

PERÍMETRO (toca SOLO esto): forense/encargos/2026-08-26-MAESTRA31-E4-ORDEN-SUPERIOR.md · data/inventario-reactivos-v1_0.tsv (nuevo) · forense/notas/2026-08-26-orden-superior-cierre.md (nuevo) · forense/notas/2026-08-26-orden-superior-spec.md (nuevo, para COMMIT-1) · forense/firmas-pendientes.tsv (solo fila FP-171) · forense/hallazgos.md · canon/gobernanza-v1_15.md (o el archivo de gobernanza vigente que encuentres, para el ADR) · canon/estado-programa-v1_10.md (o el vigente) · canon/registro-rotulos.tsv · tests/check.py (SOLO la constante tipo _T25_ARCHIVOS_CONOCIDOS si aplica) · más algún script delgado nuevo fuera de tools/curador_registro/ para generar el inventario (puede vivir en tools/ o en un scratch, tu decisión, pero no lo pongas dentro de tools/curador_registro/).

NO TOQUES bajo ninguna circunstancia: tools/curador_registro/** (se invoca vía import o subprocess, NUNCA se edita) · milpa/** · data/curacion-universo/** · data/manifiesto.yaml · data/reapertura-52a-54-variables-2026-08-13.tsv · abrir4-variables (busca su nombre exacto) · apertura-issp-variables (busca su nombre exacto) · apertura-enfih-ensafi-v1_0 (busca su nombre exacto) · forense/prereg-duelo-v2/** · forense/hitoD-preregistro-v2_0.md · nada relacionado con R10.3.

PROHIBIDO: escribir un extractor nuevo · editar tools/curador_registro/** · emparejar contra el motor o contra cualquier demanda/tabla de variables existente · añadir columna necesidad o cualquier filtro de demanda a la tabla nueva · descargar cualquier cosa · red o API · adjudicar casilla/letra/tier (D-i vigente) · derivar cifra del espejo · escribir "no existe" sin comando y universo al lado · iterar tras un resultado bajo del falsador.

═══ FIN DEL ENCARGO ═══
