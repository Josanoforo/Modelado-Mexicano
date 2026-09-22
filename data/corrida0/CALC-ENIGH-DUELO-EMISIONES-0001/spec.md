# ENIGH-DUELO-EMISIONES · COMMIT-2 · especificación humana v1.0 — PREVISTO, NO CORRIDO

`ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P4. Congela el código que emitiría
el punto de 2024 y las cinco predicciones sobre él, **sin correrlo**: este
acto no abre `enigh2024_ns_csv.zip` (PARO (a) del encargo). `preflight`
(hash, no contenido) sí se corre y se pega crudo en `## 3`.

## 1. Qué hace, cuando alguien lo corra

`guardian.carga_hogares(zip, miembro, reservada=True)` lee solo
`folioviv, foliohog, factor, remesas, est_dis, upm` de `concentradohogar`
de ENIGH 2024 (`conjunto_de_datos_concentradohogar_enigh2024_ns/
conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2024_ns.csv` —
ruta obtenida listando miembros del zip, A.7: listar no es abrir).
`guardian.emite_bajo_reserva(marco, autoriza=True)` calcula la única celda
(`remesas > 0`, proporción de hogares, IC95 bootstrap UPM en estrato). En
paralelo, `enigh_duelo_nacional.predice()` calcula las cinco predicciones
de C-PISO/C-T2/C-T3/C-TS/C-MEDIA sobre la serie 2016-2022 — estas NO usan
2024, así que no cambian si se corren antes o después de abrir el zip; se
re-emiten aquí solo para que COMMIT-3 tenga todo en un lugar.

## 2. Probado, sin el zip real (D-22)

`tests/test_enigh_duelo_guardian.py` (6 casos, zip sintético) prueba la
única función (`carga_hogares`/`emite_bajo_reserva`) que este medidor
llama contra datos reales. El propio medidor se probó, en el scratchpad de
esta sesión —no en el árbol, no commiteado como prueba porque duplicaría
`test_enigh_duelo_guardian.py`— contra OTRO zip sintético fabricado con las
mismas 6 columnas, confirmando que produce los 12 RESULT declarados con
los tipos correctos.

## 3. Preflight — salida cruda (corrida sobre este árbol, ANTES de este commit, D-a1: se pega la del borrador porque el propio `spec.md` que se está leyendo es lo que cambia entre borrador y commit; el input real —el zip de 2024— y su hash COINCIDE no cambian)

```
PRE-FLIGHT CALC-ENIGH-DUELO-EMISIONES-0001   (data/corrida0/CALC-ENIGH-DUELO-EMISIONES-0001)
  [UNICOS] ids de resultados: 12 declarados
  [UNICOS] ids de inputs: 2 declarados
  [EXISTE] script data/corrida0/CALC-ENIGH-DUELO-EMISIONES-0001/medidor.py
              script_blob_sha256 = d4014092e24363742185372da3a2c73abbfae6d6d6d94dad514052c26f0d8965
  inputs declarados: 2
    [COINCIDE] enigh2024_nc_csv  origen=manifiesto  raiz=data_raw
              ruta_absoluta   = /home/pc0/mm-gen2-enigh2024-serie-y-commit-1/data/raw/enigh2024_ns_csv.zip
              sha256 esperado = 7cbf18fee02c58849356e5495fb851ae4d0330743e34d26e35973f9ad5a1155d
              sha256 actual   = 7cbf18fee02c58849356e5495fb851ae4d0330743e34d26e35973f9ad5a1155d
              tamano          = 103139139
    [COINCIDE] IN-CALC-B-0001-RESULTADOS  origen=repo  ruta=data/corrida0/CALC-B-0001/resultados.json
              sha256 real     = 87e20e5aa2923fcc4b206734fa13ec321d3b036d61edd48eb0efd5bd369f263d
              sha256 declarado= 87e20e5aa2923fcc4b206734fa13ec321d3b036d61edd48eb0efd5bd369f263d
  [ENDURECIDO] esquema de spec   (etiquetas.generacion = GEN2)
  Bloqueos en el borrador (antes de commitear, esperados y no un defecto):
  no_commiteado=spec.md · no_commiteado=spec.yaml · spec_md_sha256_discorda_arbol
  (el spec.yaml del borrador traía un PLACEHOLDER a propósito, corregido en
  el mismo commit que archiva este spec.md) · working_tree_dirty=SI (el
  árbol traía además este mismo archivo y DUELO-PROSPECTIVO-ENIGH2024-
  spec-v1_0.md sin commitear, ambos entran juntos).
  La identidad del ÚNICO input real de datos (`enigh2024_nc_csv`, el zip
  reservado) ya está verificada arriba: `[COINCIDE]`, sha256 completo, sin
  abrir el archivo (A.7 -- hashear no es abrir).
```

## 4. Qué NO hace este CALC en este acto

No corre `run`. No abre el zip. No decide `ola_nueva` distinta de 2024 (es
el único valor con sentido dado el diseño). No adjudica (COMMIT-3, otro
CALC, otro acto).
