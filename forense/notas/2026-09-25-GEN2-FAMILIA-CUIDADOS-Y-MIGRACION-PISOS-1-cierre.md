**Conductas con piso GEN2 por dominio (este acto; derivado por `python3 forense/analisis/familia-migracion/tabla_pisos_familia_migracion.py`): FAMILIA_CUIDADOS 6 · VEJEZ 9 · PAREJA 2 · MIGRACION 7 — 24 conductas, 3 CALC sellados, 0 adopciones.**

# Nota de cierre · ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1

25/sep/2026 · CAJA (Ubuntu/WSL2, corpus montado, `ENTORNO-DERIVADO = CAJA`; `data/raices.local.yaml`
apunta `descargas_mx` al espejo `mm-corpus/descargas_mx_espejo`) · Opus 5.5 · MODO AUTÓNOMO ·
rama `acto/gen2-familia-cuidados-y-migracion-pisos-1` · 0-bis `2a0ebb63` · base `origin/main`
`40058c09` (= SHA de redacción). Encargo: `forense/encargos/2026-09-25-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1.md`.

Secuencia: 0-bis `2a0ebb63` → COMMIT-1 `fcb8ad24` (lista cerrada, specs, medidores, test D-22;
preflight VERDE ×3; ningún valor de registro leído) → COMMIT-2a `95c3e5c4` (ENASIC) →
COMMIT-2b `bbee5d6a` (Pew) → COMMIT-2c `71bf988d` (ENADID) → cascada.

## 1 · Qué se midió

| CALC | olas abiertas | reservada | conductas | RESULT | verify aislado |
|---|---|---|---|---|---|
| `CALC-ENADID-FAMILIA-HOGARES-0001` | 2009, 2014, 2018 | 2023 | 11 (5 hogar, 6 persona) | 3 775 | REPRODUCE · IDENTICO, Δ máx 0.0 |
| `CALC-ENASIC-CUIDADOS-VEJEZ-0001` | 2022 (única; se abre) | — | 7 (2 hogar, 5 persona 60+) | 521 | REPRODUCE · IDENTICO, Δ máx 0.0 |
| `CALC-PEW-MIGRACION-MEX-0001` | 2013, 2015, 2017, 2018, 2023 | Spring 2025 | 6 | 766 | REPRODUCE · IDENTICO, Δ máx 0.0 |

Lista cerrada, textos y códigos: `forense/analisis/familia-migracion/lista-cerrada-familia-migracion-P1.md`
(ver §6, renombre). Estructura: `estructura-instrumentos.md`. Tabla conducta × segmento × ola
con el id de cada RESULT: `tabla-pisos-familia-migracion-v1_0.tsv` (867 filas, derivada de los
`resultados.json` sellados). Diagnósticos: hogares y personas con diseño válido = filas leídas
en las tres olas de ENADID (91 217 / 94 422 / 109 546 hogares; 343 887 / 348 450 / 385 978
personas; 0 personas sin hogar) y en ENASIC (6 508 hogares, 21 776 personas, 0 renglones de
cuidador sin pareo); Pew: 1 000 / 1 000 / 1 000 / 897 / 1 041 entrevistas en México.

**IC calibrado de persistencia** (ENADID sobre 2018; Pew sobre la última ola de cada pregunta
con ≥ 3 olas): `-ICC-LO/-HI` y `-TAU2` por (conducta, eje). Es el parámetro reutilizable del
encargo; no se evalúa contra ninguna R.

**Lo ya sellado se cita, no se re-mide (E.5):** unión por sexo y edad ENADID 2023
(`CALC-ENADID2023-UNION-SEXO-EDAD-0001..0004`) y `CALC-ENADID-0001`; primera unión por cohorte
(`CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001/0002`); cuidado por sexo y horas ENUT
(`CALC-ENUT-0001`, `-SERIE-2009-2014-NUCLEO-0001`, `-SERIE-DICTAMEN-0001`,
`CALC-ENUT2019-NUCLEO-EJES-0001`, `CALC-ENUT2024-DISTRIBUCION-HORAS-0001/0002`,
`-NUCLEO-EJES-0001`, `-PARTICIPACION-INTENSIDAD-0001`).

**Sellado en disco, no registrado.** Asientos E.7 de las tres corridas en
`forense/replay-evidencia.tsv`; la vista `corridas/resultados.tsv` no viaja en el PR
(derivados protegidos) → NC `-2a0e-01`.

## 2 · Controles externos

| afirmación | report / fuente | este acto | lectura |
|---|---|---|---|
| VEJEZ-002: 60+ = 12.3 % de la población, ENADID 2018 | *Vejez y cuidado* | PERSONA-60MAS 2018 = 12.3 % [12.1, 12.5] | COINCIDE (misma encuesta y ola: valida universo y factor) |

## 3 · Bloque C por report

Vocabulario: CONFIRMA / MATIZA / ROMPE; NO-COMPARABLE cuando escala, unidad o universo no
enlazan. Todas las cifras son RETROSPECTIVAS (pisos descriptivos contra afirmaciones ya
escritas); ninguna PROSPECTIVA. Unidad al lado de cada cifra: hogar o persona, nunca
promediadas. Evidencia: ENADID, ENASIC y Pew GAS son (a).

### *La familia mexicana como sistema psicológico*

- **FAM-025 «24.4 % ampliados, 12.4 % unipersonales» (Censo, hogares).** ENADID 2018: ampliados
  24.0 % [23.7, 24.4], estable 2009→2018 (τ² ≈ 0); unipersonales 11.7 % [11.5, 12.0], ICC
  [9.2, 14.8]. **CONFIRMA** el orden de magnitud con otro instrumento (encuesta de hogares vs
  censo; se declara, no se enlaza).
- **«Hogares con jefatura femenina: 40 % ampliados vs 28 % con jefatura masculina».** ENADID 2018:
  32.4 % [31.8, 33.1] vs 20.8 % [20.5, 21.2]. **MATIZA**: la brecha (≈ 11.6 pp) se sostiene y es
  estable en tres olas; los niveles del report son ~7–8 pp más altos (fuente no identificada en
  el report; no se atribuye).
- **FAM-042 / «edad de independización 28.9 y sigue aumentando»; «la corresidencia crece
  porque la vivienda se vuelve inaccesible».** Proxy medido: persona de 25–34 que es hija(o)
  del jefe del hogar = 31.9 % (2009) → 33.3 % (2018) [32.7, 33.9]. **MATIZA**: la dirección
  (más corresidencia) se ve, pero el alza es pequeña (1.4 pp en nueve años) y el gradiente es
  por escolaridad (superior 45.3 % vs hasta primaria 24.8 %) — consistente con estudios más
  largos y con precio de vivienda; el acto no identifica mecanismo y «vivienda inaccesible» no
  se prueba aquí. La edad media de salida no es este estimando.
- **«Familismo» como rasgo.** No medido: es evidencia (b) (§3); los pisos de estructura no lo
  corroboran ni refutan.

### *Vejez y cuidado intergeneracional*

- **VEJEZ-002** (arriba): **CONFIRMA** (COINCIDE).
- **VEJEZ-006 «16.8 % de hogares con adultos mayores eran unipersonales» (Censo 2020, hogar).**
  ENADID 2018, dos estimandos vecinos: hogares con jefe 60+ unipersonales 18.2 % [17.6, 18.8];
  personas 60+ que viven solas 11.3 % [11.0, 11.7], estable 2009→2018 (11.1 → 11.3). **MATIZA**:
  el orden de magnitud por hogar se sostiene; «los unipersonales de mayores crecen» no se ve en
  la proporción de personas 60+ que viven solas (τ² 0.0014, ICC [10.5, 12.2]); crece el número
  absoluto porque crece la población 60+ (9.9 % → 12.3 %).
- **VEJEZ-005/037 «hogar multigeneracional como colchón, y su erosión».** 60+ en hogar
  ampliado: 42.4 % (2009) → 41.4 % → 39.8 % (2018) [39.1, 40.6]. **CONFIRMA** una erosión lenta
  (−2.6 pp en nueve años), con la reserva de que ICC 2018 [37.2, 42.5] cubre 2009 cerca del
  borde.
- **VEJEZ-008 «cuidadora modal: mujer, hija o cónyuge».** ENASIC 2022, 60+ con cuidador
  principal en el hogar (n = 422): cuidadora mujer 68.4 % [63.6, 72.7]; cónyuge 49.3 %
  [42.5, 55.2]; hija 30.5 % [24.3, 37.0]. Por sexo del adulto mayor: a los hombres 60+ los cuida
  una mujer en 93.1 % [87.7, 97.1]; a las mujeres 60+, 46.8 % [39.0, 54.6]. Por edad, la hija
  pasa de 19.6 % (60–69) a 58.1 % (80+). **MATIZA**: «hija o cónyuge» se sostiene, pero la
  feminización es asimétrica — el cuidado de las mujeres mayores recae casi por mitad en
  hombres (sobre todo cónyuges); el 95.3 % de FAM-007 es de otro universo (cuidadores de toda
  edad, ENUT) y no se compara.
- **«74 % sin apoyo de terceros».** ENASIC: 60+ cuidados por alguien de otro hogar 7.8 %
  [6.5, 9.2]. NO-COMPARABLE (el 74 % es de un estudio clínico local sobre cuidadoras, otro
  universo); el piso nacional sugiere que el apoyo externo es raro, sin probarlo.
- **«El cuidado recae en la familia por ausencia de servicios».** ENASIC: sólo 15.6 %
  [12.8, 18.3] de los 60+ que viven acompañados recibieron cuidados de alguien del hogar la
  semana pasada (31.2 % a los 80+). No se puede leer como preferencia: sin medida de oferta
  al lado (§3).

### *Elegir, cortejar y amar* (PAREJA)

- **«Los mexicanos no dejan de emparejarse: retrasan y desformalizan».** ENADID: 15+ unidos
  58.3 % (2009) → 58.0 % (2018) [57.7, 58.2] (τ² 0.0006) — **CONFIRMA** «no dejan de
  emparejarse»; entre unidos, unión libre 22.7 % → 27.9 % → 31.2 % [30.8, 31.7]; entre unidos de
  15–29, 44.9 % → 62.9 %. **CONFIRMA** la desformalización, con fuerza.
- **«Doble raíz: unión libre tradicional (popular, rural) y moderna (clase media urbana)».**
  2018, unión libre entre unidos: < 2 500 hab. 34.7 % vs ≥ 100 mil 29.1 %; secundaria 35.8 %,
  media superior 34.6 %, superior 22.4 %. **MATIZA**: la raíz popular/rural domina el nivel;
  la «moderna» de clase media no aparece como mayoría en ningún corte — si crece, crece desde
  abajo. Sin cruce edad × escolaridad (un eje a la vez) no se separan las dos.
- PAREJA-032 (separación 3.4× en unión libre): no medido (historia de uniones) → citado a
  `CALC-ENADID2023-UNION-SEXO-EDAD-*`, que tampoco lo mide; queda abierto.

### *Psychology of Mexico–US Migration*

- **«La migración es un hecho estructural y familiar».** ENADID: hogares con algún migrante
  internacional en los últimos cinco años 1.9 % (2014) → 1.8 % (2018) [1.7, 1.9]; rurales
  (< 2 500) 3.1 % [2.8, 3.4]. Pew (a): 52.1 % [47.3, 57.0] tiene contacto regular con parientes o
  amigos en el extranjero (2017); 13.1 % [10.4, 15.9] recibe dinero de parientes en el
  extranjero (2018; 21.2 % en 2013). **MATIZA**: la exposición por redes es mayoritaria, la
  emigración reciente del hogar es rara (≈ 2 %) y concentrada en lo rural — «estructural» sí,
  «generalizada» no.
- **«La emigración masculina produce hogares de jefatura femenina de facto».** Hogares con
  migrante: jefa 2.3 % [2.1, 2.5] vs jefe 1.6 % [1.5, 1.7]. **CONFIRMA** la asociación
  (co-observación, no identificación: A-bis).
- **Aspiración.** Pew: «iría a vivir a EE. UU. si tuviera los medios» 36.6 % (2013) → 28.7 %
  (2018) [24.6, 32.9], ICC [22.5, 35.8]; entre quienes irían, sin autorización 39.5 % (2017) [33.7,
  45.6]; «en EE. UU. se vive mejor» 59.8 % (2023). El report no trae cifra de intención: sin
  contraste directo. Sirve de piso: la intención declarada cae entre 2013 y 2018 en todas las
  edades de 45+.
- **«Remesas como fondo salarial familiar».** NO-COMPARABLE: Pew mide recepción declarada, no
  destino del gasto.

## 4 · Módulo de auditoría (§5 de las instrucciones)

- **Contadores que movió este trabajo:** 3 CALC sellados con `cuenta_gen2: SI` (en disco, no
  registrados en la vista; NC-01); «conductas con piso GEN2 por dominio» 0 → 24 en los cuatro
  dominios del encargo; 0 adopciones; `celdas_validadas` 219 → 219 (Δ0).
- **¿Estructura confundida con cultura?** Hogar ampliado, corresidencia de jóvenes y cuidado
  por hijas se leen primero como vivienda, ingreso, mercado laboral y ausencia de oferta
  pública; ninguno se lee como «familismo» (que es (b)).
- **¿Sobre-generalización urbana?** ENADID trae TLOC en toda conducta; ENASIC no publica
  localidad (declarado); Pew no trae urbanidad armonizada (declarado) y es muestra
  cara a cara de n ≈ 1 000.
- **Unidades.** Hogar y persona nunca se promedian; «vive solo» (persona 60+) ≠ «unipersonal»
  (hogar); la comparación con VEJEZ-006 se hizo con los dos, rotulados.
- **Escalas.** Todas proporciones. Pew son disposiciones declaradas: no se comparan con flujos.
- **Evidencia débil con intuición fuerte.** `IRIA-SIN-AUTORIZACION` (ICC [17.8, 66.3]) y
  `RECIBE-DINERO` (ICC [3.6, 37.7]) tienen τ² grande: se marcan en la FP de Pew.
- **Pew 2013 y 2023 sin PSU**: IC sin efecto de diseño (más estrechos de lo real). Declarado.
- **PROSPECTIVA vs RETROSPECTIVA:** todo RETROSPECTIVO; nada se mezcla.
- **Firewall genético:** ningún eje étnico ni hereditario.
- **Cifra escrita a mano:** ninguna. Las de esta nota se leyeron de
  `tabla-pisos-familia-migracion-v1_0.tsv` en la sesión; las del report, del mapa o del report.

## 5 · Adopción por instrumento (F-ASTRA-5-4)

Tres FP abiertas, con ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR: `FP-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-01`
(ENADID; recomendada ADOPTAR: tres olas, diseño completo, COINCIDE con VEJEZ-002, τ² del TOTAL ≤ 0.02
en 9 de las 10 conductas con τ²; unión libre 0.050 por su tendencia), `-2a0e-02` (ENASIC; recomendada CON-RESERVA-DE-ANCHO: una ola, cuidador
principal con n = 422, sin localidad), `-2a0e-03` (Pew; recomendada CON-RESERVA-DE-ANCHO: sin
PSU en 2013/2023, n ≈ 1 000, τ² grande en remesas y sin autorización). Este acto no adopta nada.

## 6 · Declaraciones (INTERPRETACIÓN-DECLARADA y hallazgos)

1. **E.6 sobre ENADID:** la ola más reciente (2023) ya tenía aperturas parciales por CALC
   sellados; se reservó lo no derivado (todas las conductas de esta lista) y se citó lo
   derivado. Cláusula 2 de autonomía.
2. **VEJEZ como dominio:** el mapa no tiene dominio VEJEZ (sus filas están en FAMILIA_CUIDADOS);
   el conteo lo separa porque el encargo §1 lo nombra.
3. **Pew = (a):** GAS entrevista residentes de México en México; la cláusula (b) de la firma
   §3 v2.16 no aplica (se aplicaría a productos de Pew sobre mexicanos en EE. UU.).
4. **Renombre por T02 en el cierre:** `lista-cerrada-P1.md` colisionaba por nombre con la de
   SALUD (#1124); se renombró con `git mv` a `lista-cerrada-familia-migracion-P1.md`, contenido
   byte a byte idéntico (sha256 `668b1de4…3218d`). Las specs selladas del COMMIT-1 citan el
   nombre viejo y no se editan: la cita se resuelve por este párrafo y el hallazgo.
5. **EMIF:** NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO; receta en la lista cerrada §4 → NC.
6. **ENADID 2014 CSV `_PE`** no es la base completa (≈ 1/40 del tamaño): se usó el DBF.
7. **Catálogo v1.1 regenerado por comando (fuera de §9, declarado):** el job `guardias` falló en
   `tests/test_catalogo_v1_1.py::test_regenera_identico` porque las FP nuevas de este acto
   cambian un derivado del catálogo (MIGRACION pasa de MEDIBLE-EN-CORPUS-SIN-CALC a
   EN-MEDICIÓN, 1 pendiente de firma). Se regeneró con
   `python3 forense/analisis/catalogo/genera_catalogo_v1_1.py --sin-registro` (3 archivos:
   `canon/catalogo-del-mexicano-v1_1.md`, `cobertura-31.tsv`, `conteos.json`); nada se editó a
   mano. El catálogo es ajeno por el encargo §9: se toca sólo su salida derivada, cláusula 6
   («fuera de §9 sin declarar» es lo vedado).
