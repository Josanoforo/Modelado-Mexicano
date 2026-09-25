# Pisos por segmento ENCODAT 2016–2017 (alcohol, tabaco, drogas) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1`, 24/sep/2026, CAJA, rama
`acto/gen2-salud-y-bienestar-pisos-1`, 0-bis `6d56f7ff`. Encargo:
`forense/encargos/2026-09-24-GEN2-SALUD-Y-BIENESTAR-PISOS-1.md` (P3). CALC:
`CALC-ENCODAT-PISOS-SUSTANCIAS-0001`. Congelada en el COMMIT-1, **antes** de ejecutar su
medidor sobre ENCODAT. **El primer resultado que produzca este procedimiento es el que se
reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` ENCODAT en el manifiesto: 2016–17 (individual, integrantes, hogar,
  catálogos, cuestionarios) y **2025**, cuyos 3 payloads de microdato llevan
  `RESERVADA-NO-ABIERTA-NO-INDEXAR-L`. E.6 del encargo: con dos olas en corpus, la última
  (2025) queda reservada; se abre 2016–17. Sin IC de persistencia: una ola abierta no tiene Δ.
- `[EJECUTADO]` Estructura por metadatos: `forense/analisis/salud-bienestar/estructura-encodat.md`
  (8/8 sha256 COINCIDE) y verificación propia de `id_pers`, `ponde_ss`, `ds2`, `ds3`,
  `ds9` (Individual) e `id_hogar`, `estrato`, `est_var`, `code_upm` (Hogar). Los `.dta`
  exigen `encoding="UTF-8"`.
- No existe variable de región (8 regiones) ni de tamaño de localidad en ningún archivo
  (informe §A–B, búsqueda sobre 1 715 + 48 + 20 variables): la afirmación regional del
  mapa (SALUD-017) es NO-CONSTRUIBLE aquí.

## 1 · Unidad, universo, diseño

Unidad: **persona** de 12 a 65 años (`ds3` ∈ [12, 65]) que respondió el cuestionario
individual; ponderador `ponde_ss`. El diseño vive en Hogar: estrato de varianza `est_var`,
UPM `code_upm`, estrato rural/urbano/metropolitano `estrato`. **Llave declarada:** los 20
primeros caracteres de `id_pers` (ancho 22) = `id_hogar` (ancho 20); el catálogo no la
documenta, la carátula del cuestionario sí nombra el folio del hogar. Sólo se usan
`id_hogar` únicos; los no pareados se cuentan (`G-JOIN-SIN-HOGAR`) y quedan fuera por
diseño inválido (`G-FILAS-DISENO-VALIDO`). Si la llave no parea, el conteo lo dice: no se
prueba otra llave después de abrir el dato.

## 2 · Conductas (por texto)

Tabla en `forense/analisis/salud-bienestar/lista-cerrada-P1.md` §2 (ENCODAT), parte de esta
spec. Saltos: quien nunca bebió (`al1` = 2) vale 0 en ALCOHOL-12M; quien no bebió en 12
meses (`al1` = 2 o `al4` = 2) vale 0 en ALCOHOL-30D y ALCOHOL-EXCESIVO-12M; FUMA-ACTUAL sin
dato y `tb05` = 2 (nunca fumó) vale 0. ALCOHOL-EXCESIVO-12M con `al11` (mayor número de
copas en un solo día, 12 meses): hombres 5+ (códigos 1–4), mujeres 4+ (1–5); `ds2` 1 =
hombre, 2 = mujer (sin etiqueta de valor en el `.dta`; el cuestionario lo marca así).
«Alguna vez» de drogas: 1 si algún ítem = 1; 0 si todos = 2; si no, fuera. La segunda
ronda (`di1a2`…, `dm1a2`…) no se usa (declarado).

## 3 · Ejes (uno a la vez)

TOTAL · SEXO · EDAD 12–17 / 18–34 / 35–65 · ESTRATO (1 RURAL, 2 URBANO, 3 METROPOLITANO) ·
ESCOLARIDAD (`ds9`, sólo 18+): HASTA-PRIMARIA {1, 2}, SECUNDARIA {3, 4}, MEDIA-SUPERIOR
{5, 6}, SUPERIOR {7, 8, 9}; 99 fuera.

## 4 · Estimación

Igual que la spec ENSANUT §4 (razón ponderada; bootstrap de UPM dentro de `est_var`,
certeza para UPM única, `PCG64(20260924)`, 2 000 réplicas, percentiles 2.5/97.5, contrato
conservador), con la receta común por sha256. Sin IC de persistencia.

## 5 · Controles, secuencia

Sintético con todas las ramas (hogar no pareado, conducta sin soporte, fuera de universo) en
`tests/test_salud_pisos_gen2.py`. Oro: no hay piso GEN2 previo de ENCODAT (`ls data/corrida0
| grep -c ENCODAT` = 0 al COMMIT-1). Ninguna ejecución diagnóstica.

## 6 · Auditoría (afirma sobre México)

**Escala:** proporciones de personas 12–65. **Firewall genético:** consumo de alcohol y
tabaco se describe por segmento social (sexo, edad, escolaridad, estrato), nunca por
ascendencia; ningún eje es étnico. **Oferta antes que preferencia:** CONSULTO-PROFESIONAL-POR-CONSUMO
mide contacto con servicios, no necesidad; su universo es el del filtro del cuestionario y se
reporta con N. **Declaración ≠ consumo:** son autorreportes; el subreporte en drogas ilegales
y en mujeres es conocido y no se corrige. **Comparación con 2025:** no se hace; 2025 está
reservada. **Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
