**SHA de redacción:** `959006a` (merge #206, ENASIC-SPLIT) — coincide con `origin/main` real al abrir este acto, no hizo falta refrescar.
**Entorno asignado:** CAJA con red. NO en nube (403 `host_not_allowed` contra dominios de datos). NO en los dos.
**Estado:** CONSUMIDO — ver `forense/notas/2026-08-13-gdelt-ucdp-recon.md` (Commit 1 + Commit 2 + registro), `forense/hallazgos.md`.

---

ENCARGO B · GDELT-UCDP-RECON (relanzado) — caracterizar, no bajar
Entorno: CAJA con red. NO en nube (403 host_not_allowed contra dominios de datos). NO en los dos.

§0 · Qué cambió desde la versión anterior de este encargo

Mesa decidió: "bajamos lo necesario para identificar en qué consisten." Eso no es un lote de descarga: es una caracterización. El objetivo es saber qué recorte a México es posible y a qué costo, no llenar disco.

Tres premisas de la versión anterior ya están contestadas y salen del encargo:

(1) El sondeo de override ya no hace falta. VERIFICA-PUERTAS (#205) las midió el 13/ago y están en data/acceso-puertas-2026-08-13.tsv:

puerta    http_sin_override    quien_puede    cabecera diagnóstica    sirve
GDELT_RawDataFiles    206    AGENTE    content-range: bytes 0-0/55068, server: GDELT    N17, N27
UCDP_Downloads_GED    206    AGENTE    content-range: bytes 0-0/138078, server: Microsoft-IIS/10.0, CC BY 4.0 declarado    N17, N27

Las dos son alcanzables sin override. Léelo de ese TSV; no repitas el sondeo de acceso. Lo que sí sondeas es la estructura, que es otra cosa.

(2) Su clasificación EXISTE-NO-SATISFACE es correcta y sigue vigente. Responden, son libres, y son globales — sin recorte a México definido. Este acto no la cambia: la resuelve o confirma que no se puede.

(3) Cada una tiene DOS filas en el puntero — la real, sondeada contra portal, y una gap_mapeo_map_b marcada NO_PROBADO con universo interno. No es contradicción sin resolver: RECONCILIA-PUERTAS (#208) dejó la regla de precedencia propuesta. Usa la fila con sondeo de portal y dilo; no toques la vieja.

Sobre la infraestructura de agentes que mesa mencionó: no aparece en tools/ ni en tests/ de este repo. Localízala y decláralala en el ARRANQUE si existe fuera; si no la encuentras, dilo y procede con curl. No la des por supuesta — una restricción supuesta se hereda igual que una cifra supuesta, y es peor porque nadie la audita.

§1 · PERÍMETRO

ESCRIBE: el corpus compartido (/home/pc0/mm-corpus/raw, no solo el worktree) · data/manifiesto.yaml (por su vía, §4.2) · data/universo-puertas-2026-08-12.tsv (solo filas nuevas de adquisición; las de sondeo no se editan) · forense/notas/2026-08-13-gdelt-ucdp-recon.md · forense/encargos/2026-08-13-GU-gdelt-ucdp-recon.md (A.3, con prefijo) · hallazgos (union, merge local).

NO ESCRIBE: data/curacion-registro/** · data/cola-adquisicion-*.tsv · data/acceso-puertas-2026-08-13.tsv · canon/** · milpa/** · tools/** · tests/**.

Carga: ALTA. Es el único acto que llena disco. No lo corras junto a otro acto de microdato pesado. Medido 13/ago: 15 GiB + 4 GiB de swap; el límite es el pico por acto, no el número de sesiones.

§2 · ARRANQUE

1 · REPO · 2 · SHA (base 959006a; refresca y reporta, no es PARO) · 5 · ESPEJO — como siempre.

3 · data/raw Y CORPUS COMPARTIDO. Este acto descarga: enlaza, no crees local. ln -s /home/pc0/mm-corpus/raw data/raw y readlink -f data/raw. Copia data/raices.local.yaml si el worktree no lo hereda. ⚠️ Al cerrar, verifica PR#77 con ls -la directo sobre /home/pc0/mm-corpus/raw/, no sobre el symlink. Ningún test lo atrapa. Es el patrón que P·LOTE-2 aplicó bien.

4 · ENTORNO. echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]" → sin variable · curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.gdeltproject.org/data.html → esperado 200/206. NUNCA curl -I. Si 403 host_not_allowed: PARA.

4-bis · pwd antes de cada bloque de comandos de repositorio, y git -C <ruta> en vez de cd si miras otro árbol. Un cd sin volver produjo el 13/ago una afirmación falsa sobre el repo que se sintió verificada porque el comando devolvió salida.

§3 · COMMIT 1 — el techo y el criterio, congelados antes de bajar nada
El techo de descarga, en bytes, por fuente: ≤ 500 MB. Si caracterizar exige más, se para y se reporta cuánto haría falta. No se negocia en vuelo.
Qué archivo mínimo caracteriza la estructura — índice, manifiesto de archivos, un solo día de datos, o el codebook. Nombra el archivo antes de bajarlo.
El mecanismo de recorte candidato, por fuente y escrito antes de mirar: ¿hay filtro por país en el nombre de archivo, en una columna, o en un endpoint? Las tres tienen costos muy distintos y hay que decir cuál se espera.
El criterio de veredicto, cerrado: RECORTE-VIABLE (mecanismo existe y se puede ejercer con lo que hay) · VIABLE-CON-PARSER-NUEVO (existe pero exige código que no está) · NO-SEPARABLE (no hay forma de aislar México sin bajar todo).
Pre-registro de falsación (B-bis) — la fila que suele faltar. NO-SEPARABLE es un resultado válido y probablemente el más útil: cierra por evidencia una pregunta que hoy está abierta, y evita que un lote futuro gaste la caja en peso muerto. Y RECORTE-VIABLE obliga a decir el volumen estimado del recorte mexicano con el comando que lo estima — sin esa cifra, "viable" no significa nada operativamente.
La reserva de A.4 que este acto no puede saltarse: EXISTE-NO-SATISFACE es la clasificación vigente y correcta de ambas. Solo cambia si este acto demuestra el recorte. Un 200 en la portada no es satisfacción.

Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

§4 · COMMIT 2 — la caracterización

No edita el commit 1. Si la especificación estaba mal, un tercer commit lo dice; nunca se corrige hacia atrás.

Por fuente:

4.1 · Estructura real, verificada byte a byte. No te creas la portada: SONDA-1 encontró en INEGI un contentUrl señuelo a prueba.pdf, soft-404 de 2,263 bytes fijos, y P·LOTE-2 se topó con el mismo en CNGMD. GET -r 0-0 y compara el tamaño real contra lo declarado.

4.2 · ¿México es separable, y cómo? Columna, código de país, archivo aparte, parámetro de endpoint. Con el comando que lo demuestra, no con la documentación del portal.

4.3 · Volumen del recorte mexicano, estimado con su comando. Si es una extrapolación desde un día de datos, dilo y da el factor.

4.4 · Veredicto de §3.4. Si es VIABLE-CON-PARSER-NUEVO: el parser NO se escribe aquí. Va como propuesta en la nota, con el diff exacto, citando la ventana de ADR-70(d) —"el mantenimiento del aparato previo a la apertura del piloto queda permitido únicamente con ADR que lo selle"— para que mesa decida el acto de motor.

4.5 · Registro por la vía completa de lo que sí se bajó: sha256 al manifiesto por su vía, fila de puerta de adquisición, y verificación PR#77.

⚠️ La trampa de mecanismo, medida y heredada: tests/manifiesto.py --registra solo resuelve contra data/raw/. Para otra raíz, la única vía que funciona es --escanea <raiz> --grupo + --promueve inmediatos, en pares por grupo — nunca N --escanea seguidos de un --promueve al final. Y valores de más de 78 caracteres disparan el defecto de plegado YAML del staging: se parchan importando escribir_manifiesto() del propio script, nunca a mano.

⚠️ Y el criterio que NO aplica, porque es estructuralmente insatisfacible. El molde de adquisición exigía "decisión de adquisición por la vía del motor". P·LOTE-2 leyó decide_acquisition.py completo y demostró que su esquema no tiene acción para una fuente recién adquirida — solo NO_ADQUIRIR_AHORA y BUSQUEDA_DIRIGIDA, y ninguna aplica. Marca EN-ESPERA-DE-VÍA y sigue. No edites el TSV a mano. No lo cuentes como fallo del acto.

§5 · CONTADOR

Dos veredictos de separabilidad donde hoy hay dos EXISTE-NO-SATISFACE sin resolver. Y, si alguno es RECORTE-VIABLE, el volumen estimado del recorte mexicano — la cifra que convierte una decisión de ingeniería aplazada en un lote firmable.

§6 · NO HACE

No baja las bases completas. No escribe parser nuevo. No cambia la clasificación A.4 sin demostrar el recorte. No toca relaciones.tsv ni la cola. No retira las filas viejas del puntero. No promete que alguna sea viable — NO-SEPARABLE cierra la pregunta y eso es el entregable.
