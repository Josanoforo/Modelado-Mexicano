Contadores movidos: «estimadores en catálogo con RESULT» → 35 070 (`jq .estimadores forense/analisis/catalogo/v1_1/conteos.json`); «dominios MEDIDOS» → 8 dominios del mapa U0, en 9 de 31 reports (`jq '.dominios_medidos, .reports_medidos, .reports' …/conteos.json`). Cero mediciones, cero adopciones.

# Cierre · ACTO GEN2-CATALOGO-V1-1-1 · catálogo del mexicano v1.1

Encargo: `forense/encargos/2026-09-24-GEN2-CATALOGO-V1-1-1.md` (sello de cuerpo `66493e33…`, 0-bis `afe161a7`). Entorno NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus montado=NO, archivos examinados=0; el acto no toca microdato ni red). Base `9632a880` = SHA de redacción (`git rev-list --count HEAD..origin/main` → 0). Rama `claude/new-session-4q2juk` (fijada por la plataforma). MODO AUTÓNOMO.

## Productos

- `canon/catalogo-del-mexicano-v1_1.tsv` y `.md`, generados por `python3 forense/analisis/catalogo/genera_catalogo_v1_1.py`; tablas derivadas en `forense/analisis/catalogo/v1_1/`.
- `tests/test_catalogo_v1_1.py` (5 pruebas, VERDE; huérfano censado en `forense/analisis/ci-guardias/censo-tests.tsv`).
- `docs/catalogo.md` apunta a v1.1. `canon/catalogo-del-mexicano-v1_0.*` sin diff (`git diff --stat origin/main -- canon/catalogo-del-mexicano-v1_0.*` → vacío).

## Premisas: verificación

- `[EJECUTADO]` `status`: 81 adoptados / 219 validadas — **se sostiene** (`python3 tools/corrida0.py status`: `N_resultados_gen2_adoptados_activos=81`, `celdas_validadas=219`). «266 corridas» no se re-derivó: status imprime «417 corridas · 82612 resultados · 231 usos». Es logística y no toca el entregable.
- `[EJECUTADO]` «v1.0 con tabla de cobertura; verificar que ADENDA-2 la incorporó» — **no la incorporó.** v1.0 cuenta filas por cinco áreas. Tampoco hay un archivo ADENDA-2 de ASTRA-4 en el repo: solo `MISION-ASTRA-4-ADENDA-1.md`. La firma F-A4 (`GEN2-TRAMITE-FIRMAS-12-ADENDA-1.md:24`) la nombra como «cobertura de 31 dominios en el catálogo». P3 la crea, como el encargo prevé.
- **INTERPRETACIÓN-DECLARADA (cláusula 2): «31 dominios».** El mapa U0 (`canon/mapa-dominios-v1_0.tsv`) tiene 28 ids de dominio, no 31. El 31 es el número de reports de `corpus/reports/` (README: «31 reports temáticos», derivado por `rg --files corpus/reports -g '*.md' | wc -l`). La tabla P3 tiene una fila por report, con el dominio primario de `report-a-dominio-v1_0.tsv`.
- **Vocabulario de P3.** Se añade `MEDIBLE-EN-CORPUS-SIN-CALC` porque el mapa dictamina afirmaciones MEDIBLE-EN-CORPUS que nadie corrió. Fundirlas en MEDIBLE-CON-ADQUISICIÓN colapsaría «nadie corrió el mecanismo» con «la fuente no está» (§2). Un report (`SIN-AFIRMACIONES-EN-MAPA`) no tiene afirmaciones en el mapa con su dominio.
- `[SUPUESTO]` «PISOS-GEN2-2 no habrá cerrado» — **se sostiene**: la rama `acto/gen2-pisos-gen2-2` sigue viva y no hay merge en main. Los pisos legacy salen por el censo de `GEN2-ENCIG-PISOS-GEN2-1` (`forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv`, 36 filas HEREDADO-DE-LEGACY): 20 de ellas eran adoptados activos del marcador (DIN LxE y TRA SxD) y no entran, con la nota «re-medición en curso, rama acto/gen2-pisos-gen2-2». Las 16 de ENCIG ADJ-0001 ya habían salido del consumo.
- **FIRMAS-16 no ha fusionado.** Las FP `6d56-01..03` (ENSANUT, ENCODAT, ENBIARE) y `e773-01` (NSE) están ABIERTAS. No entran y quedan en «pendiente de firma». No es PARO (§2 del encargo).
- **Estimadores sin FP citable.** 13 RESULT que `status` cuenta como adoptados activos (cuentan por la etiqueta de su spec, E.2) no tienen FP firmada, ni fila de mesa en `decisiones.tsv` para su CALC, ni firma de encargo en su pin. El catálogo no les inventa firma: van a «pendiente de firma» y a `FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01`.
- Homónimo descartado: `GEN2-CATALOGO-CONTRATO-Y-TEST-1` trata el esquema de cita de `milpa/procedencia.yaml`, no este catálogo.

## Qué es «adoptado» aquí (regla mecánica del generador)

Una fila entra si su RESULT está en un CALC con sello válido, hay una firma citada por id que lo adopta y su piso no es HEREDADO-DE-LEGACY. Las firmas válidas son: una FP FIRMADA en `forense/firmas-pendientes.tsv`, una fila de `decisiones.tsv` cuyo objeto es el CALC con `cuenta_gen2=SI` o que adopta un bloque, o la firma verbatim de un encargo archivado citada por el pin de mesa del uso. Fuentes: adoptados activos de `corrida0` (misma vista que `status`), marginales EVALUADA del marcador adoptadas por instrumento (ENVIPE 2025; ENIF 2024 con reserva de ancho), pisos de la Firma T (ENOE, ENDIREH ×4, ENDUTIH, MOCIBA) y bloque ENIGH de la Firma M.

**PROPUESTO-POR-EJECUTOR:** la asignación de dominio (ids del mapa U0) por prefijo de regla y por CALC, declarada en el generador. La columna `oferta_exclusion` en DINERO: la exclusión por oferta sellada existe solo para crédito ENIF 2012–2021, y ninguna fila DINERO de v1.1 es crédito, así que cada una declara la ausencia.

## Reglas (P2)

v1.0 regla 1 (ENCIG, canal): CONFIRMA, mismos RESULT. v1.0 regla 2 (remesas): MATIZA, con serie 2016–2022 adoptada. Ocho reglas nuevas en trabajo, género, tecnología, dinero y seguridad. El tier FUERTE se da solo a la frecuencia sostenida por RESULT; cada PORQUE lleva su propio tier.

## NC y FP

NC `afe1-01..05` en `forense/no-corrido.tsv`; FP `afe1-01` en `forense/firmas-pendientes.tsv`.
