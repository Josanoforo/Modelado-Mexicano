# Mapa de series · congelado (COMMIT-1b, antes de que el medidor lea un valor)

ACTO GEN2-DONDE-CAMBIO-EL-MEXICANO-1 · spec `forense/prereg-caja/DONDE-CAMBIO-spec-v1_0.md`
(sellada en `9aea5a09`) · esquema `ESQUEMA.md` en este directorio.

Todo fragmento se regenera byte a byte con `PYTHONPATH=. python3 tools/series/mapa_<familia>.py`.
Verificación ciega sobre el conjunto (sin leer valores; cada dirección se resuelve dentro del
`resultados.json` del CALC de su fila): 31 063 filas · 82 CALC · 0 ids planos faltantes ·
88 377 direcciones `CELDA-DE-TABLA` que resuelven a exactamente una celda · 0 `(serie_id, ola)`
duplicados. Estados de par: COMPARABLE 21 273 · PRIMERA 7 780 · NO-COMPARABLE 1 157 ·
NO-DOCUMENTADO 852 · CAMBIO-DOCUMENTADO 1.

## Interpretaciones declaradas (PROPUESTO-POR-EJECUTOR, cláusula de autonomía 1–3)

1. **Celda de tabla.** Un `RESULT-*-TABLA` sellado (ENOE-PISOS, ENDIREH-PISOS, MOCIBA-PISOS) es un
   RESULT sellado: sus celdas se citan con `<RESULT-ID>#k=v&…/<campo>` (valor percent-encoded,
   campo `nombre` o `nombre[i]`) y se resuelven por `(calc, RESULT-ID)`. Sin esto ENOE, ENDIREH y
   MOCIBA quedarían fuera del universo del encargo.
2. **Fuera de escala.** Conductas cuya unidad no es proporción (horas/semana ENUT, pesos ENIGH, 13
   filas ENIF) entran con nota `FUERA-DE-ESCALA-(0,1)`; spec §2 las deja con `k = 0` → `SIN-SERIE`.
   ENOE `horas_ocupado` e `ingreso_ocupado_nominal` no entran (tabla de pisos, no conducta de catálogo).
3. **ENOE** sólo dentro de era (spec §3): el par que cruza era es `NO-COMPARABLE`
   (`ENOE-PERSISTENCIA-spec-v1_0.md`, `separar_eras: true`). Nota `SIN-COVARIANZA-LONGITUDINAL`.
4. **ENDIREH** no tiene tabla ni spec de comparabilidad por texto: todos sus pares
   `NO-DOCUMENTADO` (spec §2, A.15). Series unidas entre olas sólo por cadena idéntica
   `(resultado, eje, categoria, ventana)`; `ventana` distingue series.
5. **MOCIBA** 2016→2017 `NO-COMPARABLE` por `MOCIBA-PISOS-spec-v1_0.md` («SIN-HISTORIA-PARA-CALIBRAR»);
   2015 sin IC por celda, no entra.
6. **ENVIPE** no denuncia C1/U1: 15 olas 2011–2025 (`CALC-ENVIPE-SERIE-*`, `CALC-R-CIV-M-*` por su
   universo secundario homologado, `CALC-ENVIPE-0001` ya sellado); comparabilidad por la columna
   `comparabilidad` de `data/corrida0/envipe-serie-denuncia-v1_0.tsv` y `ENVIPE-SERIE-COMPLETA-spec`.
7. **ENUT** pares por regla de ancla del ESQUEMA contra `enut-comparabilidad-texto-v1_0.tsv`.

## Exposición declarada (A.13 / ADR-46)

Dos subagentes de construcción vieron, por error, cifras incrustadas como texto en columnas de
texto permitidas: la columna `unidad_escala` del catálogo (sufijo `(esperado N.NNNNNN)` en ~11 filas
ENIF/ENVIPE) y tres valores GEN1 de control citados en la prosa de
`R-ENVIPE-SERIE-DBF-spec-v1_0.md` §0. No los transmitieron a la sesión ejecutora; los scripts los
recortan y no aparecen en ningún TSV. La sesión ejecutora no ha visto ningún valor de serie.

## Hashes (sha256)

    d120993e692b0aa263011433e920e83d3ca38dc3bc3b6f67fabbe185eda51d81  forense/analisis/donde-cambio/mapa/encig.tsv
    244694e8fa7bfa90a94ff24d5ef4c6a2ac0b39c39a306c94585e185756089c73  forense/analisis/donde-cambio/mapa/enif.tsv
    e0968833a58baf70fd56f06ebcc2015dc36ff8c56e9c0a6e5d70c7767b23f805  forense/analisis/donde-cambio/mapa/enigh.tsv
    02d5e90ac93959b08cf381131fa63bed81fcefe35b63ca9008c439d4eedc7938  forense/analisis/donde-cambio/mapa/enut.tsv
    91389e2af62f2a7f713b9b088c05ee6a287e4afc2e3c5bd4de7c08b47576792b  forense/analisis/donde-cambio/mapa/envipe.tsv
    67e6f9c08209daf5ff9b149f6f9ec9227f05aa747b784de63d717e45c5ca1ab8  forense/analisis/donde-cambio/mapa/resto.tsv
    d8552feccd45d40bb73d4002723718292dfa6534e8049ff302da25a0989c1d69  tools/series/__init__.py
    dab3b0359d7dce7fa092423f5ce88370fab7422fd25798bf61fb65c9ca92c2e2  tools/series/calc_serie.py
    eb64500be1a33ec995b1c09da28ad763cc61ea6b84981bedbcbb3edada6614b0  tools/series/dictamen.py
    88a71c19eaff0fc265de759d7ad8aed982acd8d4199103051ff511125c409d41  tools/series/mapa_encig.py
    593587dcc06dd937b59450643c4f4c9b0b5aad19ae4f0ccd6861e8e685a9a372  tools/series/mapa_enif.py
    6f707815e291f26c0a1eac1b945e177823ad9d8c0238d017154331f2e39f42bc  tools/series/mapa_enigh.py
    0ffb915b410f4bc42e095f75c01718a6b74b12cd7a40bef38621f1ff4da468e0  tools/series/mapa_enut.py
    1608b1b7a7fa4f9dc93544863bbbea5bf9d6e84b98101f0840c96ac7b1f28956  tools/series/mapa_envipe.py
    2bdfda09703343484398f5d420e0a2dc08d9d588dac197d136f2e402d194b692  tools/series/mapa_resto.py
    91dadbcd8bc8b5f39dad709e167312042c6a09acbcf26a92401dd7318f884413  tests/test_donde_cambio_dictamen.py
    fca40da56f94ba44015a1ad2b07f86d3d4f437ef0da78312bb00584bba8cfefd  forense/analisis/donde-cambio/mapa/ESQUEMA.md
