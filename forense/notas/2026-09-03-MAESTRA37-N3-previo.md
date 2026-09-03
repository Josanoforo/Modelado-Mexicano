# ACTO MAESTRA37-N3 · SELLA-CIVICA-COERCITIVO-Y-PROPAGA — COMMIT-1, estado previo

«El primer resultado que produzca este procedimiento es el que se reporta.»

## Conteo de reglas del motor (previo)

`grep -cE '^ - id: ' milpa/tramite.yaml` → **16** (regex sin indentación, no calza;
el motor usa dos espacios: `grep -cE '^  - id: ' milpa/tramite.yaml` → **16**,
verificado línea por línea contra las 16 entradas listadas por
`grep -nE '^\s*- id: ' milpa/tramite.yaml`).

## Smoke del emisor sobre las 16 reglas actuales (previo)

```
python3 -c "
import sys; sys.path.insert(0,'.')
from milpa.src.emisor import cargar_reglas, emitir_binaria
reglas = cargar_reglas()
print('n reglas:', len(reglas))
for r in reglas:
    for s in r.entonces:
        p = emitir_binaria(r, s.conducta)
        print(r.id, s.conducta, 'OK')
"
```
→ `n reglas: 16`; las 16 reglas y sus 44 salidas `entonces` emiten `EMITE`
sin excepción (0 errores). Salida completa capturada en el commit de este acto.

## Entrada `tramite.gobierno_digital.coercitivo` — líneas 193-285 de `milpa/tramite.yaml` (previo, verbatim)

Ver bloque congelado abajo (líneas exactas, sin edición):

```yaml
  - id: tramite.gobierno_digital.coercitivo
    situacion: le_ofrecen_servicio_gobierno_digital
    si:
      disparadores: {cobertura_formal: false}
      contexto_producto: {coercitivo: true, riesgo_fiscal_percibido: true}
    entonces:
      # SIN DATO POR DEFECTO DE LA FUENTE -- EXISTE-NO-SATISFACE en ENCIG 2025 (ACTO MAESTRA34-L5 P0/P2, ADR-287): ninguna de 483 columnas de 2025 ni ~100 000 de cinco olas distingue obligatoriedad del canal; P7_3=7 es fracaso, no rechazo; cobertura_formal:false selecciona fuera del universo (sección VII solo la contesta quien hizo el trámite). No se propone sucesor en ENCIG. Queda como único prior ASIGNADO vigente sin dato al cierre de MAESTRA35-N1.
      - {conducta: rechaza_servicio, p: 0.91, clase: ASIGNADO}
      - {conducta: adopta, p: 0.09, clase: ASIGNADO}
    porque: {generador: [G1], mecanismo: "la utilidad predice adopción; la coerción con riesgo fiscal la mata"}
    tier: MEDIA-FUERTE          # corregido en v0.2.0 · el motor §3.3 dice MEDIA-FUERTE, no FUERTE
    alcance: "gobierno digital ÚNICAMENTE (cambio 11 del modelo v2)"
    falsable_si: "Si un servicio coercitivo con riesgo fiscal lograra adopción masiva, la regla se rompe"
    fuente: ["validacion:CoDi", "report:tecnologia"]
    nota_validacion: "Backtest: CoDi = 3.09M cuentas con >=1 transacción en 6 años."
    sin_dato_universo_examinado:
      # firma c1 (mesa, 2/sep/2026, CORREGIDA sobre su primera redaccion), sobre
      # ACTO MAESTRA35-L6 -- ADR-299. La regla SIGUE SIN DATO y el contador S1
      # SIGUE EN 1. p y tier NO se tocan (ASIGNADO 0.91/0.09, MEDIA-FUERTE) y el
      # backtest CoDi se queda. NO se declara "hueco de mundo": se declara un
      # universo EXAMINADO con su veredicto, y nada sobre el que no se examino.
      declarado_por: "firma c1 (mesa, 2/sep/2026) -- ACTO MAESTRA35-L6 · FUENTE-COERCITIVO-Y-PUENTE"
      firma_verbatim: >
        la regla sigue SIN DATO y el contador S1 sigue en 1. Clasificacion con
        universo declarado (A.4/A.10): NO-ENCONTRADO en encuestas de hogares del
        corpus -- ENCIG 2011-2025 (ADR-287), ENDUTIH 2023/2024/2025, ENIF 2024,
        ENCUCI 2020, serie CoDi (este acto: 7 piezas, 7 veredictos con refutador
        independiente) -- por defecto de universo de ESAS fuentes: la situacion
        solo se observa donde la conducta ya ocurrio. NO-ACCESIBLE en las dos
        fuentes que si tendrian denominador de obligacion (SAT: obligados vs
        cumplidores de buzon tributario/e.firma; CNGF), sondeadas y sin respuesta
        desde la caja. No se afirma nada sobre el universo no examinado.
      adr: [ADR-287, ADR-299]
      veredicto: NO-ENCONTRADO
      universo_examinado_encuestas_de_hogares:
        # SIETE instrumentos. Cada linea dice que se abrio y con que se conto.
        - {instrumento: "ENCIG 2011-2025 (8 olas)", adr: ADR-287, examinado: "483 columnas de 2025 y ~100 000 de cinco olas", veredicto: EXISTE-NO-SATISFACE}
        - {instrumento: "ENDUTIH 2023", adr: ADR-299, examinado: "FD 1 099 filas + tic_2023_usuarios.DBF, 229 variables, N=58 922", veredicto: EXISTE-NO-SATISFACE}
        - {instrumento: "ENDUTIH 2024", adr: ADR-299, examinado: "FD 477 variables en 5 tablas + 5 DBF, N=58 080", veredicto: EXISTE-NO-SATISFACE}
        - {instrumento: "ENDUTIH 2025", adr: ADR-299, examinado: "FD 8 hojas + ti25usu.dbf, 239 variables, N=57 810", veredicto: EXISTE-NO-SATISFACE}
        - {instrumento: "ENIF 2024", adr: ADR-299, examinado: "cuestionario 32 pag./2 534 lineas + FD 398 variables + TMODULO.csv, 13 502 personas 18+", veredicto: EXISTE-NO-SATISFACE}
        - {instrumento: "ENCUCI 2020", adr: ADR-299, examinado: "FD_ENCUCI2020.pdf 4 006 lineas/422 073 caracteres + 5 DBF, 458 campos (54+164+156+50+34), 21 519 personas", veredicto: NO-ENCONTRADO}
        - {instrumento: "serie CoDi/Banxico", adr: ADR-299, examinado: "cuentas_validadas_x_mil_hab_trimestral.xlsx 3 hojas 2022-T1..2026-T1 + HTML de avances", veredicto: "EXISTE-NO-SATISFACE (serie agregada: unidad cuenta, no persona)"}
      defecto_de_universo_de_esas_fuentes: >
        Uno solo: la SITUACION solo se observa donde la CONDUCTA ya ocurrio. En
        ENCIG, la seccion VII solo la contesta quien hizo el tramite (ADR-287
        iii). En ENDUTIH, P7_36_1 -- "declaracion de impuestos" por internet,
        el unico item de tramite fiscal explicito del corpus -- esta
        autoseleccionado al 100 % a quien ya interactuo con el gobierno en
        linea, medido por cruce sobre el DBF entero: 16 362/16 362 en 2025,
        15 557 en 2024, 15 083 en 2023. En ENIF, P5_15_2 esta gateado DOS veces
        (tener el producto Y haberlo comparado), asi que la adopcion vale 1 en
        todo su universo. En ENCUCI 2020, cero aciertos de fiscal|impuest|SAT|
        contribuy|RFC sobre las 4 006 lineas del FD, con control positivo
        confian=79. Y un faltante propio de ENDUTIH que ADR-287 no tenia: NO HAY
        DENOMINADOR DE OBLIGACION FISCAL -- ni RFC, ni regimen, ni condicion de
        contribuyente en 239 variables --, asi que P7_36_1=2 mezcla "rechaza el
        canal" con "no esta obligado a declarar". Es "fracaso != rechazo" un
        nivel mas arriba: NO OBLIGADO != RECHAZA.
      no_accesible:
        veredicto: NO-ACCESIBLE
        fuentes: >
          Las dos que SI tendrian denominador de obligacion: SAT (obligados vs
          cumplidores de buzon tributario / e.firma) y CNGF.
        sondas_con_codigo_crudo:
          # Se reportan crudas porque el codigo por si solo enganiaria: las dos
          # dieron 200 y ninguna de las dos entrego contenido legible desde la
          # caja, que es exactamente lo que hace el veredicto NO-ACCESIBLE.
          - {url: "https://www.sat.gob.mx", http_code: 200, curl_exit: 0, cuerpo: "1 477 bytes: shell de una SPA SvelteKit, SIN <title> y SIN texto; todo se renderiza por JavaScript"}
          - {url: "https://www.inegi.org.mx/programas/cngf/", http_code: 200, curl_exit: 0, cuerpo: "321 bytes: stub de redireccion por JavaScript; el programa vive en /programas/cngf/2025/ y su unidad de analisis son INSTITUCIONES, no personas (ficha RNM 1145)"}
          - {url: "https://datos.gob.mx (CKAN)", http_code: 404, curl_exit: 35, cuerpo: "1/sep/2026; NO se reintento -- el encargo ordena no reintentar sin ruta nueva"}
      universo_no_examinado: >
        No se afirma NADA sobre el. Este veredicto cubre exactamente los siete
        instrumentos de arriba y las tres sondas; fuera de ahi, el acto no
        midio y no opina.
      siguiente_universo_declarado: >
        Fuentes ADMINISTRATIVAS (SAT/CNGF), por navegador o por solicitud de
        transparencia -- no por sonda desde la caja, que ya se agoto. Receta
        para mesa en data/cola-adquisicion-v1_0.tsv, filas INEGI_CNGF y
        SAT_MEXICO (ACTO MAESTRA35-L6, P3).
      tablero: >
        "S1 = 1 · NO-ENCONTRADO en 7 instrumentos + 2 NO-ACCESIBLE" (firma c1).
        NO se dice "hueco de mundo" y NO se dice "S1 = 0": el contador no se
        mueve, y lo que se gana es el universo declarado del negativo.
      estampa_A10: >
        Describe el corpus del 2/sep/2026. ENDUTIH publica cada anio y ENIF cada
        tres: una ola futura puede anadir el reactivo que falta y este veredicto
        caduca. Lo que caduca es el veredicto sobre la fuente, no el defecto de
        diseno que lo produce.
      falsador_de_reapertura: >
        Si aparece una fuente con DENOMINADOR DE OBLIGACION (SAT, CNGF, o una
        ola futura de encuesta de hogares que lo traiga), la regla se reabre.

```

## Propuesta — `civico.participacion.concurrencia_presidencial_conversion` (línea 2889, previo: `situacion: PROPUESTA-DE-CARGA`)

`grep -n concurrencia_presidencial_conversion milpa/tramite-ola5-propuesta-v0.yaml` → línea 2889.
`grep -c concurrencia_presidencial milpa/tramite.yaml` (motor) → **0** (confirmado: no está en el motor antes de este acto).

## Propuesta — MPS-2012, dos entradas (previo)

`civico.clientelismo.vote_change_mps2012` (línea 2775) y `civico.clientelismo.prevalencia_lista_mps2012`
(línea 2830), ambas con `situacion: PENDIENTE-DE-MESA` (líneas 2778 y 2833 respectivamente).

## Tablero — filas a tocar (previo)

FP-255, FP-257, FP-261, FP-262, FP-263, FP-264, FP-265, FP-266, FP-269, FP-270 todas en estado
`ABIERTA` antes de este acto (verbatim capturado arriba, sección VERIFICACIÓN DE EXISTENCIA del
encargo archivado en `forense/encargos/2026-09-03-MAESTRA37-N3-SELLA-CIVICA-COERCITIVO-Y-PROPAGA.md`).
FP-267 y FP-268: `ABIERTA`, no se tocan (sin letra de mesa / esperan recuento de L1).

## ADR máximo (previo)

`grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1` → **319**.
Candidato: **ADR-320**.

## `canon/registro-rotulos.tsv` — A.13, negativo del encargo no reproducido

El encargo declara `grep -n 'EXT.OF.05' canon/registro-rotulos.tsv` → `0`. Reproducido en este
árbol (`8f49eab8`): `grep -n 'EXT.OF.05' canon/registro-rotulos.tsv | wc -l` → **3** (líneas 92,
112, 147 — menciones en prosa de `EXT_OF_05`/`EXT-OF-05` dentro del perímetro narrado de
MAESTRA33-A3, MAESTRA34-N6 y MAESTRA36-A2; ninguna es un rótulo `EXT-OF-05` propio, y
`canon/registro-rotulos.tsv` censa rótulos de ACTO, no ids de fuente). El cero que el encargo
afirma no se reproduce con ese comando exacto; A.13 obliga a declararlo aquí, sin editar la firma
de dirección (verbatim, A.3). No cambia la propagación de D5 (la colisión de ids
`EXT-OF-05`/`EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` es real y vive en `relaciones.tsv:204-205`,
no en `registro-rotulos.tsv`).
