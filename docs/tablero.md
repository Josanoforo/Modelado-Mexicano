---
title: Tablero del programa
---

# Tablero del programa

[Portada]({{ '/' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }})

Este bloque lo escribe únicamente el job `guardias` de CI
(`.github/workflows/verify.yml`) sobre `origin/main`, en el mismo commit
`[deriva]` que actualiza
[`forense/tablero/TABLERO-PROGRAMA.md`](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/tablero/TABLERO-PROGRAMA.md).
Esta página es una copia, no una segunda fuente: la escribe el mismo
comando (`tools/tablero_programa.py --actualiza`), en el mismo commit,
sobre el mismo árbol. Ver
[`docs/PROTOCOLO-TABLERO.md`](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/docs/PROTOCOLO-TABLERO.md)
para qué hacer (y qué no hacer) con lo que sigue.

<!-- TABLERO-DERIVADO:BEGIN -->
## Estado vivo derivado

- **Celdas validadas (métrica rectora, firma de mesa 20/sep/2026).** `219` celdas con predicción emitida antes de ver el dato y error sellado contra R (cruce `162` + persistencia `57`). **No es «N aciertos»: es N celdas con error CONOCIDO.** Tres clases, sin fundir:
  - *cruce vs R* · `DIN.ahorro_solo_informal.enif2024.localidad_x_edad` · n `8` · champion `C2` · error mediano `1.011` pp (máx `4.278` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PROPORCION` · `data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k1.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `4.747` pp (máx `4.747` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k2_automotriz.enif2024.marginal16` · n `15` · champion `PERSISTENCIA` · error mediano `0.341` pp (máx `0.341` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k2_departamental.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `2.584` pp (máx `2.584` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k2_nomina.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `1.016` pp (máx `1.016` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k3.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `2.218` pp (máx `2.218` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k5.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `2.232` pp (máx `2.232` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k6_p_tenedores.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `4.462` pp (máx `4.462` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `GOB.gobierno_digital.encig2025.edad_x_escolaridad` · n `15` · champion `C2` · error mediano `2.861` pp (máx `12.282` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/resultados.json`
  - *cruce vs R* · `GOB.gobierno_digital.encig2025.edad_x_sexo` · n `8` · champion `C2` · error mediano `0.922` pp (máx `1.806` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-ENCIG-DUELO-2025-ADJUDICACION-0002/resultados.json`
  - *cruce vs R* · `GOB.gobierno_digital.encig2025.escolaridad_x_sexo` · n `8` · champion `C2` · error mediano `0.868` pp (máx `2.014` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-ENCIG-DUELO-2025-ADJUDICACION-0002/resultados.json`
  - *cruce vs R* · `TRA.evade_norma.envipe2025.escolaridad_x_dominio` · n `12` · champion `C2` · error mediano `1.224` pp (máx `5.436` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002/resultados.json`
  - *persistencia t−1 vs R* · `ENCIG 2025 · encig2025_04_sec_7.csv · unidad = TRÁMITE (quien pagó doce veces contribuye doce veces)` · n `10` · error mediano `11.826` pp (máx `13.358` pp) · **brecha `2` años** · PERSISTE `0` / CAMBIA `10`
  - *persistencia t−1 vs R* · `ENIF 2024 · TMODULO.csv · unidad = PERSONA elegida 18+` · n `32` · error mediano `2.145` pp (máx `5.196` pp) · **brecha `3` años** · PERSISTE `16` / CAMBIA `16`
  - *persistencia t−1 vs R* · `ENVIPE 2025 · tmod_vic (conjunto_de_datos) · unidad = DELITO` · n `2` · error mediano `2.767` pp (máx `3.849` pp) · **brecha `1` años** · PERSISTE `2` / CAMBIA `0`
  - *persistencia t−1 vs R* · `ENVIPE 2025 · tmod_vic · unidad = DELITO` · n `13` · error mediano `2.34` pp (máx `5.361` pp) · **brecha `1` años** · PERSISTE `6` / CAMBIA `7`
  - *duelo de tres, nacional* · n `12` · MAE `M` `4.987` pp · `L_SOLO` `3.957` pp · `L_CORPUS` `3.889` pp · veredicto `SIN-GANADOR-UNICO` · NO se suma a las otras dos clases (otro universo, otro estimando) · `CALC-TRIADA-0002/resultados.json`
  - *sub-cifra del dominio DINERO* · cruce n `8` (error mediano `1.011` pp) · persistencia n `32` (error mediano `2.145` pp) · ENIF 2024; la brecha de persistencia es de 3 años y no se promedia con las de 1 y 2 años de ENVIPE/ENCIG
  - *NO cuentan* · `89` filas `IDENTICO` (M == R porque `EMISOR=ARBITRO`: el mismo número copiado, no una predicción contrastada) · `2` celdas de `formalidad` con piso y sin `error_piso_pp` (su error es un CALC sucesor) · universo examinado: 327 filas de data/corrida0/marcador-segmento.tsv + 3 CALC sellados
- **Procedencia.** SHA `35017cfc8` · fecha del commit `2026-09-29` · ¿árbol == origin/main? `True`.
- **Motor.** reglas totales `25` · reglas con dato (>=1 conducta MEDIDO*) `24` · reglas sin dato `1` · conductas MEDIDO* `58` · tiers `{'FUERTE': 20, 'MEDIA': 5}`.
- **Marcador por segmento.** filas por estado: ADOPTADO-POR-FIRMA `52` · CONSUMIDA-SIN-PILOTO `1` · DIAGNOSTICO `8` · EVALUADA `57` · IDENTICO `89` · MEDIDA-POR-NSE `52` · MEDIDA-POR-NSE-APROXIMACION `24` · MEDIDA-POR-NSE-APROXIMACION-CIRCULAR `6` · NO-COMPARABLE `2` · RESERVADA `19` · SIN-PISO `15` · SUPRIMIDA-N `2` (total `327`) · cobertura de piso `111 / 327` · valor añadido / evaluadas `0 / 52` · celdas `emision = EMITIDA-SIN-EVALUAR` `13 / 327` · `veto_pisos_activo` `True`.
- **Corridas selladas que no cuentan todavía.** por `cuenta_gen2`: `False` 1 · `NO` 18 · `NO-DERIVACION-CONTEXTUAL` 1 · `NO-SIN-FIRMA-DE-OBJETO` 1 · `PENDIENTE-DE-CASCADA-DIFERIDA` 2 · `PENDIENTE-DE-INTEGRACION-SERIAL` 2 · `PENDIENTE-DE-MESA` 15 · `SI` 219 (selladas total `259`) · `PENDIENTE-DE-MESA`:
  - `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002--18e3c08247d5`: `NO-VERIFICADO`
  - `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001--f22dc8014aec`: `NO-VERIFICADO`
  - `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002--cd853c64a584`: `NO-VERIFICADO`
  - `CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001--8cf894b01d4b`: `REPRODUCE`
  - `CALC-ENIGH2016-INTENSIDAD-REMESAS-0001--db3e1d99cc39`: `REPRODUCE`
  - `CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001--268b0658db7c`: `REPRODUCE`
  - `CALC-ENIGH2016-REMESAS-CONTEXTO-0001--d1a27b7d702b`: `REPRODUCE`
  - `CALC-ENIGH2018-INTENSIDAD-REMESAS-0001--f0d2fa594560`: `REPRODUCE`
  - `CALC-ENIGH2018-PERFIL-ESTRUCTURAL-0001--0a3f34eaea63`: `REPRODUCE`
  - `CALC-ENIGH2018-REMESAS-CONTEXTO-0001--4604b387eeb2`: `REPRODUCE`
  - `CALC-ENIGH2020-INTENSIDAD-REMESAS-0001--d41b466457b6`: `REPRODUCE`
  - `CALC-ENIGH2020-PERFIL-ESTRUCTURAL-0001--ff84ff36db65`: `REPRODUCE`
  - `CALC-ENIGH2020-REMESAS-CONTEXTO-0001--0fcfbe663035`: `REPRODUCE`
  - `CALC-RELEVO-ENCIG23-P83-0001-v1_1--66cfff97600b`: `REPRODUCE`
  - `CALC-WBES2023-PRECISION-INTERACCIONES-0001--7f2a0899f700`: `NO-VERIFICADO`
- **Corredor LEGACY (eje x = ∅, GO-MARCADOR).** el marcador por segmento es la línea de arriba. marco vigente `marco-M-v1_3` sorteado / `marco-M-v1_2` congelado (derivado del árbol) · celdas sorteadas `14` · celdas con M `14` · con R `14` · con L `14` · celdas puntuables (M∩R∩L) `14` · celdas sin cobertura completa `0`.
- **Corpus lógico.** entradas del manifiesto `7198` · filas de registro de curación `953` · filas de relaciones `231` · filas del inventario de reactivos v1.2 `178247`.
- **Gobernanza operativa.** ADR máximo del espacio numérico CERRADO `593` · FP máximo del mismo espacio `409` · ids con raíz de acto (época vigente) `{'ADR': 208, 'FP': 281, 'NC': 656}` · FP abiertas: FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01, FP-260923-GEN2-FRONT-1-4296-01, FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01, FP-260926-GEN2-FRONT-3-PORTADA-1-8914-03, FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12, FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-20, FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-26, FP-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01, FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-01, FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-02, FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01, FP-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01, FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01, FP-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-01, FP-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-02, FP-260928-GEN2-TUBERIA-3-f18c-01, FP-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01, FP-260928-GEN2-CIERRE-Y-PRODUCTO-3-3c2e-01, FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01, FP-260928-GEN2-PENDIENTES-4-12d9-03, FP-260928-GEN2-PENDIENTES-4-12d9-04, FP-260928-GEN2-PENDIENTES-4-12d9-05, FP-260928-GEN2-PENDIENTES-4-12d9-06, FP-260928-GEN2-PENDIENTES-4-12d9-07, FP-260928-GEN2-PENDIENTES-4-12d9-08, FP-260928-GEN2-PENDIENTES-4-12d9-09, FP-260928-GEN2-PENDIENTES-4-12d9-10, FP-260928-GEN2-PENDIENTES-4-12d9-11, FP-260928-GEN2-PENDIENTES-4-12d9-12, FP-260928-GEN2-PENDIENTES-4-12d9-13, FP-260928-GEN2-PENDIENTES-4-12d9-14, FP-260928-GEN2-PENDIENTES-4-12d9-15, FP-260928-GEN2-PENDIENTES-4-12d9-16, FP-260928-GEN2-PENDIENTES-4-12d9-17, FP-260928-GEN2-PENDIENTES-4-12d9-18, FP-260928-GEN2-PENDIENTES-4-12d9-19, FP-260928-GEN2-PENDIENTES-4-12d9-20, FP-260928-GEN2-PENDIENTES-4-12d9-21, FP-260928-GEN2-PENDIENTES-4-12d9-22, FP-260928-GEN2-PENDIENTES-4-12d9-23, FP-260928-GEN2-PENDIENTES-4-12d9-24 · encargos archivados `855` (consumidos `766`) · instrucciones vigentes `v2.16` · cola de encargos (solo estados != CONSUMIDO; consumidos `77`):
  - `2026-09-07-ENCARGOS-GEN2-en-orden.md`: GATED
  - `2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md`: LISTO
  - `2026-09-10-GEN2-POST-685/00-LEEME-LANZAMIENTO-POST-685.md`: GATED
- **NC abiertas por razón (token A.14, prefijo exacto).** abiertas `283` · por token: `DECISIÓN-DE-MESA-PENDIENTE` 35 · `DIFERIDO-A` 104 · `FUERA-DE-PERÍMETRO` 35 · `NO-VERIFICABLE-AQUÍ` 56 · `PARO-ENTORNO` 6 · `PARO-PREMISA` 18 · `SUSTITUIDO-POR` 1 · prosa (sin token reconocible) `28`.
- **GEN2 (derivado de `corrida0 status`, valores EN ÁRBOL; vistas del árbol distintas de HEAD: `data/corrida0/corridas.tsv, data/corrida0/resultados.tsv, data/corrida0/pines-sellados-resueltos.tsv, data/corrida0/usos.tsv, data/corrida0/demanda-corridas.tsv, data/corrida0/demanda-resultados.tsv`).** adoptados activos `138` · pendientes de adopción `0` · corridas selladas `326` / requeridas `0` · resultados sellados `240946` / activos `236` · pendientes `63` · dependencias numéricas legacy activas `82` · validación independiente `5933` · diferencias materiales `0` · NC- abiertas `283` · replays LEGACY-GEN1 sellados `5` (no cuentan). El `0 / N` es la lectura correcta: el aparato se construyó antes que las corridas.
- **Legacy activas por consumidor (desglose aditivo del contador de arriba).** motor `13` · procedencia `30` · catalogo de momentos `17` · marco del duelo `1` · celdas D `21` · otro `0` — suman `82`, el total. Los cinco consumidores son RELEVABLES: ninguno se declara fuera del contador. Cuántos de ellos ya tienen medición GEN2 sellada que la vista no enlaza se deriva en `forense/analisis/relevo-reconcilia-1/reconcilia-173-v1_0.tsv`.
- **Relevadas por pin de mesa, por vía (firma 4.1, 21/sep/2026 — las clases NO se funden).** vía (i) desde insumo crudo con hash `14` · vía (ii) lectura de una conducta ya GEN2 `13`. Marco del duelo, lo que sigue legacy por campo: R `0` · M `1` · L `0` · AGREGADO `0`. Celdas M todavía legacy, **nombradas**: `DIN-M-01` — `DIN-M-01` es el recordatorio de que `tiene_ahorros` espera el acceso a ENNViH. El canal vive en `data/corrida0/pines-de-mesa.tsv` y cada fila pasa las cuatro guardas de 4.1 antes de mover el contador (`T32-quater T-PINES-MESA`).
- **GEN2 · medición vs. adopción (ACTO GEN2-PRE-E5 · P3).** sellados `216924` · pendientes de adopción (citados en la propuesta, ningún consumidor activo aún) `0` · vetados por decisión vigente (sellados, pero una firma prohíbe adoptarlos: no son cola) `813` · adoptados por un consumidor activo `138`. Sellar un RESULT no mueve `dependencias_numericas_legacy_activas` por sí solo: solo el consumidor activo que lo adopta la baja.
- **Fuentes.** `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`, `milpa/procedencia.yaml`, `forense/prereg-duelo-v2/` (marcos y corridas M/R/L), `data/manifiesto.yaml`, `data/curacion-registro/cola-adquisicion-registro.tsv`, `data/curacion-registro/relaciones.tsv`, `data/inventario-reactivos-v1_2.tsv`, `canon/gobernanza-v1_15.md`, `forense/firmas-pendientes.tsv`, `forense/encargos/*.md`, `forense/encargos/cola/*.md`.

**Protocolo vigente.** La actualización factual de este bloque se hace con:

```
git fetch origin
python3 tools/tablero_programa.py --actualiza
python3 tests/check.py --baseline
```

El humano solo actualiza la interpretación (las tablas curadas §2.1-2.5 y la narrativa) cuando hay una decisión o un hallazgo que valga la pena registrar. Las recetas antiguas del snapshot histórico (p. ej. `git branch -r` o `awk '$6=="ABIERTA"'`) NO gobiernan esta actualización -- son historia, no el mecanismo vigente.

<!-- TABLERO-DERIVADO:END -->

## Carriles — qué falta para medir cada tema

<!-- TABLERO-UNICO:CARRILES:BEGIN -->
_Derivado con `python3 tools/tablero_carriles.py` (mismo `derivar()`), sin escribir aparte. Un carril es un report temático del corpus. Los umbrales del semáforo y la precedencia de la siguiente acción viven en un solo sitio, la cabecera de `tools/tablero_carriles.py`; las versiones del catálogo, las reglas y las familias se resuelven del puntero `docs/data/catalogo-vigente.json` o de la serie más alta del árbol, y la cadena de procedencia del pie dice cuáles leyó. Este bloque sustituye a `TABLERO-CARRILES.md` y a su página web._

#### Cómo leer

Umbrales (único sitio: cabecera de `tools/tablero_carriles.py`): núcleo = dominio con peso ≥ 0.2 (más el de mayor peso) · VERDE exige cifra adoptada en todo el núcleo y reglas con dictamen ≥ 0.5 · NARANJA = núcleo cubierto por cifra adoptada o piso sellado registrado en la vista pendiente de adopción (visibilidad, no adopción) · GRIS = dominio principal en GENETICA, GENOMICA o NO-MEDIBLE-POR-DISEÑO > 0.5 · a lo más 5 stoppers listados por categoría ⟨S⟩

Precedencia de la siguiente acción: FIRMA > RESERVA > ADQUISICION > NC-PARO > CALC > EDITORIAL. Cada línea con un número lleva `⟨F…⟩`: el archivo del que sale, con su blob y su lector en «Cadena de procedencia». `S` = regla del script. El catálogo no trae `report`: la unión carril ↔ cifra pasa por dominio × instrumento. Firmas, reservas, NC, CALC, actos en vuelo y validación casan con los instrumentos del núcleo y se ordenan por relevancia. ⟨S⟩

#### Resumen

Carriles 31: 🔴 ROJO 3 · 🟡 AMARILLO 23 · 🟠 NARANJA 1 · 🟢 VERDE 1 · ⚪ GRIS 3 ⟨F1 F2 F3 S⟩

| carril | report | semáforo | afirm. | núcleo con cifra | reglas con dictamen | stoppers | siguiente acción | ⟨⟩ |
|---|---|---|---:|---:|---:|---:|---|---|
| CARRIL-02 | Ausencia sin certeza · duelo y pérdida ambigua en familias d | 🔴 ROJO | 41 | 0/1 | 0% de 4 | 3 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-09` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-13 | Humor in Mexican Psychological Life · 2023-2026 Update | 🔴 ROJO | 34 | 0/1 | 0% de 3 | 2 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-16` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-17 | Moral Emotions in Mexico · Declared Dignity · Relational Fac | 🔴 ROJO | 31 | 0/1 | 0% de 2 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-24 | Psicología del Trabajo en México · Un Mapa Basado en Evidenc | 🟡 AMARILLO | 57 | 1/1 | 0% de 3 | 5 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-15 | La familia mexicana como sistema psicológico · entre el afec | 🟡 AMARILLO | 51 | 1/1 | 0% de 3 | 4 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-09 | El México Rural e Indígena en sus Propios Términos · Comunal | 🟡 AMARILLO | 49 | 1/1 | 0% de 3 | 2 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-07 | El Efecto Ambiental de la Violencia Crónica en México · Cómo | 🟡 AMARILLO | 48 | 1/1 | 0% de 4 | 4 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-09` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-10 | Elegir · Cortejar y Amar en el México de Hoy · Díada de Pare | 🟡 AMARILLO | 46 | 2/2 | 0% de 4 | 8 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-11` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-14 | La arquitectura invisible de la interacción social en México | 🟡 AMARILLO | 45 | 1/2 | 0% de 2 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-01 | Adopción y Resistencia Tecnológica en México · La Paradoja d | 🟡 AMARILLO | 43 | 1/1 | 0% de 3 | 3 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-06 | El Clasemediero Mexicano · Identidad · Ansiedad de Estatus y | 🟡 AMARILLO | 43 | 1/1 | 0% de 2 | 5 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-20 | Psicología Política y Comportamiento Cívico del Mexicano Con | 🟡 AMARILLO | 43 | 1/1 | 40% de 10 | 8 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-09` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-25 | Psychology of Mexico-US Migration · Identity · Family · Aspi | 🟡 AMARILLO | 42 | 1/1 | 0% de 3 | 2 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-19` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-12 | Health · Body · Food and Substance Use in Mexico · The Behav | 🟡 AMARILLO | 39 | 1/1 | 0% de 3 | 7 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-19` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-29 | Salud Mental en México · Prevalencia · Estigma y la Brecha e | 🟡 AMARILLO | 39 | 1/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-08 | El Mexicano y el Tiempo · Estructura · no Cultura · en la Pl | 🟡 AMARILLO | 38 | 1/1 | 29% de 7 | 4 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-22` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-18 | Mérito · Movilidad Social y Desigualdad en México · Actualiz | 🟡 AMARILLO | 38 | 1/1 | 0% de 4 | 7 | FIRMA: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-23 | Psicología del Consumidor Mexicano · Patrones · Contradiccio | 🟡 AMARILLO | 38 | 2/2 | 40% de 5 | 3 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-22` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-27 | Religiosidad y Psicología del Mexicano Contemporáneo · Moral | 🟡 AMARILLO | 38 | 1/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-28 | Report 26 · The Contemporary Mexican and Knowledge · Experti | 🟡 AMARILLO | 38 | 2/2 | 44% de 9 | 4 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-31 | Vejez y Cuidado Intergeneracional en México · El Debilitamie | 🟡 AMARILLO | 38 | 1/1 | 25% de 4 | 3 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-19` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-04 | Behavioral Finance Mexicano · Estructura · Adaptación Racion | 🟡 AMARILLO | 35 | 1/1 | 33% de 3 | 2 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-22` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-05 | Confianza y Desconfianza en México · Anatomía Psicológica de | 🟡 AMARILLO | 33 | 1/1 | 0% de 4 | 7 | FIRMA: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-26 | Reconfiguración de los Guiones de Género en México · Masculi | 🟡 AMARILLO | 33 | 2/2 | 0% de 3 | 8 | FIRMA: `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-03 | Autoridad y jerarquía en el México contemporáneo · anatomía  | 🟡 AMARILLO | 30 | 1/1 | 0% de 3 | 6 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-16` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-21 | Psicología · Conducta y Sociedad en el México Contemporáneo  | 🟡 AMARILLO | 28 | 2/2 | 0% de 0 | 6 | RESERVA: `mapa:reserva_v1_1` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-22 | Psicología de la Juventud Mexicana Contemporánea · Gen Z y M | 🟠 NARANJA | 32 | 0/1 | 0% de 4 | 6 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-07` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-19 | Non-Family Social Capital in Mexico · Cooperation · Trust ·  | 🟢 VERDE | 42 | 1/1 | 67% de 9 | 6 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-09` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-11 | Genetica y Conducta del Mexicano Contemporaneo · Canal Indiv | ⚪ GRIS | 38 | 0/1 | 0% de 3 | 1 | ADQUISICION: `SIN-UNION` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-16 | Mexican Population Genomics · 2025-2026 Scientific and Marke | ⚪ GRIS | 33 | 0/1 | 0% de 2 | 4 | FIRMA: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |
| CARRIL-30 | Sanción Social Horizontal en México · Chisme · Envidia y Mal | ⚪ GRIS | 22 | 1/1 | 0% de 2 | 3 | FIRMA: `FP-260928-GEN2-PENDIENTES-4-12d9-10` | ⟨F1 F2 F3 F4 F5 F7 F8 F9⟩ |

#### Adquisición — global

Cola de adquisición: 952 filas; por estado A4/A5 (primer token, tal cual): OBTENIDO 879 · OBTENIDO-PARCIAL 20 · SOLICITUD-PREPARADA 13 · NO-ACCESIBLE 10 · NO-OBTENIDO-POR-ESTE-AGENTE 8 · NO-ENCONTRADO 6 · CERRADA 4 · CERRADA-PREEXISTENTE 4 · SUPERADA-POR 4 · SIN-FETCH 2 · DIFERIDO-A 1 · NO-ADQUIRIDA-POR-COSTO 1 ⟨F5⟩

Manifiesto: 7198 payloads; con `estado_reserva`: RESERVADA-NO-ABIERTA-NO-INDEXAR-L 173 · DOCUMENTACION-ESTRUCTURAL-NO-RESPUESTAS 45 · RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR 4; licencia ausente o NO-DECLARADA: 220 ⟨F6⟩

Vocabulario de instrumentos: 150 tokens; tokens de la cola citados por los reports y fuera del vocabulario: ninguno ⟨F12 F2 F1 F5 S⟩

Fuentes pendientes en la cola (quién la pide, por la regla QUIEN_PIDE):

| fuente | estado A4/A5 | prioridad | quién la pide | ⟨F5⟩ |
|---|---|---|---|---|
| `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` | OBTENIDO-PARCIAL | 20 | caja (completa el payload) | ⟨F5 S⟩ |
| `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` | OBTENIDO-PARCIAL | 21 | caja (completa el payload) | ⟨F5 S⟩ |
| `OECD` | OBTENIDO-PARCIAL | 36 | caja (completa el payload) | ⟨F5 S⟩ |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | OBTENIDO-PARCIAL | 38 | caja (completa el payload) | ⟨F5 S⟩ |
| `REGISTRO_DE_TANDAS_Y_REPUTACION` | OBTENIDO-PARCIAL | 39 | caja (completa el payload) | ⟨F5 S⟩ |
| `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` | SOLICITUD-PREPARADA | 40 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENAFIN` | OBTENIDO-PARCIAL | 49 | caja (completa el payload) | ⟨F5 S⟩ |
| `MERCER_GPTW_CLIMA_DESEMPENO` | NO-ADQUIRIDA-POR-COSTO | general-9 | mesa (costo) | ⟨F5 S⟩ |
| `SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_CANDIDATA` | NO-ENCONTRADO | fp190-6 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ENJUVE` | OBTENIDO-PARCIAL | sin-prioridad-asignada | caja (completa el payload) | ⟨F5 S⟩ |
| `REUTERS_DNR` | OBTENIDO-PARCIAL | sin-prioridad-asignada | caja (completa el payload) | ⟨F5 S⟩ |
| `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` | OBTENIDO-PARCIAL | 3 | caja (completa el payload) | ⟨F5 S⟩ |
| `RUPC` | OBTENIDO-PARCIAL(RUPC historico 2019 via datamx.io | a6-reconciliacion | caja (completa el payload) | ⟨F5 S⟩ |
| `ENSAFI_TANDAS_PARTICIPACION_R8_2_N29` | OBTENIDO-PARCIAL | — | caja (completa el payload) | ⟨F5 S⟩ |
| `CONDUSEF_CNBV_TANDAS_FUERA_DE_PERIMETRO` | NO-ENCONTRADO | — | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ROSCA_ACADEMICO_MEXICO_BUSQUEDA` | NO-ENCONTRADO | — | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ENNVIH_DIN_M_01_DISENO_INFERENCIAL` | SOLICITUD-PREPARADA | GEN2-E09-DIN | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXI` | OBTENIDO-PARCIAL | 0 | caja (completa el payload) | ⟨F5 S⟩ |
| `MPS2012_35024_0001_DATA_DTA` | SOLICITUD-PREPARADA | 18 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `OECD_TRUST_PUM_2021_2023_2025` | SOLICITUD-PREPARADA | 36 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENJUVE_MICRODATOS_2000_2005_2010` | SOLICITUD-PREPARADA | sin-prioridad-asignada | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENVIPE_ROSTER_UPM_O_SERVICIO_VARIANZA` | SOLICITUD-PREPARADA | 0 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENCIG_TASA_NACIONAL_PAGO_INFORMAL_POR_CANAL` | SOLICITUD-PREPARADA | 0 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `ENSAFI_TANDAS_REPUTACION_INCUMPLIMIENTO` | NO-ENCONTRADO | 39 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `CFPB_BNPL_UNSECURED_DEBT_2025` | OBTENIDO-PARCIAL | 3 | caja (completa el payload) | ⟨F5 S⟩ |
| `ENPOL_2016_MICRODATOS_CSV` | OBTENIDO-PARCIAL | 60 | caja (completa el payload) | ⟨F5 S⟩ |
| `ENAPROCE_2015_2018_MICRODATO_COMPLETO` | NO-ACCESIBLE | F6-R03 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `CONDUSEF-REDECO_SERIE` | OBTENIDO-PARCIAL | 3 | caja (completa el payload) | ⟨F5 S⟩ |
| `EMOVI_2011` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `EMOVI_2023` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ENAFI_SIN-OLA` | NO-ENCONTRADO | 3 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `ENEM_2024` | NO-OBTENIDO-POR-ESTE-AGENTE(4 intentos) | 3 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `EQD-PANEL_2018` | NO-OBTENIDO-POR-ESTE-AGENTE(3 intentos) | 3 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `IFPS-MEXICO_2020-2021` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `INEGI-MMP_2024` | NO-OBTENIDO-POR-ESTE-AGENTE(4 intentos) | 3 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `MCPS_SIN-OLA` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `WVS-EEUU-JAPON_7` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `WVS-LONGITUDINAL_1981-2022` | NO-ACCESIBLE | 3 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ENAPROCE_2015_2018_MICRODATO_COMPLETO` | NO-ACCESIBLE | F6-R03 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ECRIGE_CDMX_2019` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `ECRIGE_CDMX_2019_FD` | NO-OBTENIDO-POR-ESTE-AGENTE(10) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `ENVE_2012_2022_DATOS_ABIERTOS_Y_DOCUMENTACION` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `ENVE_2012_2014_DATOS_ABIERTOS` | NO-OBTENIDO-POR-ESTE-AGENTE(4) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `ENVE_2020_2022_BASE_EJEMPLO` | NO-OBTENIDO-POR-ESTE-AGENTE(4) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `ENVE_MICRODATO_COMPLETO_2012_2024` | NO-ACCESIBLE | OBTENCION-EXTERNA-1 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `ENCRIGE_2016_MICRODATO_COMPLETO` | NO-ACCESIBLE | OBTENCION-EXTERNA-1 | mesa con identidad (acceso/registro) | ⟨F5 S⟩ |
| `IECM_SEPCOPP_RESULTADOS_2011_2025` | NO-OBTENIDO-POR-ESTE-AGENTE(11) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `IECM_COPACO_2020_2023_RESULTADOS_E_INTEGRACION` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `MECANISMO_PROTECCION_INFORMES_ESTADISTICOS` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `JEMS_47_6_REPLICAS_3X1_Y_REMESAS_VIGILANTISMO` | NO-ENCONTRADO | OBTENCION-EXTERNA-1 | acto de nube (/sonda) | ⟨F5 S⟩ |
| `BANXICO_ESTUDIOS_EFECTIVO_Y_BILLETES` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `PROFECO_QQP` | OBTENIDO-PARCIAL | OBTENCION-EXTERNA-1 | caja (completa el payload) | ⟨F5 S⟩ |
| `ECCO_SFP_CLIMA_CULTURA_ORGANIZACIONAL` | NO-OBTENIDO-POR-ESTE-AGENTE(13) | OBTENCION-EXTERNA-1 | acto de nube (reintento) o caja | ⟨F5 S⟩ |
| `SANDOVAL_2026_LATIN_AMERICAN_POLICY` | SIN-FETCH | OBTENCION-EXTERNA-1 | acto de nube (abrir la fuente) | ⟨F5 S⟩ |
| `PELLEGRINI_SCANDURA_2008_JOM` | SIN-FETCH | OBTENCION-EXTERNA-1 | acto de nube (abrir la fuente) | ⟨F5 S⟩ |
| `BANXICO_CODI_TAG_RESEARCH_ESTUDIO` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `SEGOB_MECANISMO_INCORPORACIONES_E_INCIDENTES_2012_2026` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `FELIX_BRASDEFER_ROLE_PLAYS_CODIFICADOS` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `FIU_DELANEY_2021_MICRODATO` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |
| `WORLDPANEL_NUMERATOR_CONVENIO_ACADEMICO` | SOLICITUD-PREPARADA | OBTENCION-EXTERNA-1 | mesa con identidad (solicitud preparada) | ⟨F5 S⟩ |

#### Frente 2027 ⟨F11⟩

| familia | ola | estado | gate faltante | firma que lo abre | carriles que alimenta | ⟨⟩ |
|---|---|---|---|---|---|---|
| ENIF-AHORRO-FORMAL | enif_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-ASTRA6-C1-PA | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-04, CARRIL-05, CARRIL-08, CARRIL-15, CARRIL-23 | ⟨F11 F1⟩ |
| ENIF-HORIZONTE-AHORRO | enif_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-ASTRA6-C1-PA | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-04, CARRIL-05, CARRIL-08, CARRIL-15, CARRIL-23 | ⟨F11 F1⟩ |
| ENCIG-PAGO-DIGITAL | encig_2027 | SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01) | CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-dato del re | FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01 (FIRMADA: suspender); FP-2609 | CARRIL-05, CARRIL-07, CARRIL-18, CARRIL-20 | ⟨F11 F1⟩ |
| ENCIG-SOLICITUD-MORDIDA | encig_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-05, CARRIL-07, CARRIL-18, CARRIL-20 | ⟨F11 F1⟩ |
| ENVIPE-DENUNCIA-U4 | envipe_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-02, CARRIL-05, CARRIL-07, CARRIL-19, CARRIL-20, CARRIL-30 | ⟨F11 F1⟩ |
| ENVIPE-EVASION-NORMA | envipe_2027 | LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | DATO-2027-AUSENTE | FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06 + FP-260927-GEN2-TRAMIT | CARRIL-02, CARRIL-05, CARRIL-07, CARRIL-19, CARRIL-20, CARRIL-30 | ⟨F11 F1⟩ |
| ENOE-INFORMALIDAD | 2027T4 | NO-LANZAR-TODAVIA | CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(FP-260927-G | FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01; FP-260926-GEN2-AST | CARRIL-06, CARRIL-08, CARRIL-10, CARRIL-12, CARRIL-15, CARRIL-18, CARRIL-21, CARRIL-22, CARRIL-24, CARRIL-26, CARRIL-28, CARRIL-31 | ⟨F11 F1⟩ |
| ENSU-CAMPECHE-INSEGURIDAD | 2027T4 | NO-LANZAR-TODAVIA | CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA(FP-260926- | FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01 | CARRIL-07, CARRIL-14, CARRIL-30 | ⟨F11 F1⟩ |

#### Carriles

##### 🔴 CARRIL-02 · Ausencia sin certeza · duelo y pérdida ambigua en familias de personas desaparecidas en México ⟨F1 F14⟩

- **Semáforo ROJO** — núcleo con cifra adoptada 0/1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 41**: medible en corpus 3 · con adquisición 24 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: DUELO 33 (80%) núcleo · CONFIANZA 1 (2%) · FAMILIA_CUIDADOS 1 (2%) · GENERO 1 (2%) · MIGRACION 1 (2%) · RELIGIOSIDAD 1 (2%) · SALUD 1 (2%) · SALUD_MENTAL 1 (2%) · SANCION_SOCIAL 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCUCI 3 · ENNVIH 1 · ENVIPE 1; sin instrumento reconocido: 36 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENVIPE 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: DUELO ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · FAMILIA_CUIDADOS 1449 · GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · SALUD 800 · SALUD_MENTAL 2758 · SANCION_SOCIAL 9 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 4 · PASA 147 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 9 / 23 / 3 / 20): EN-MAIN · recibo pr-1246 · regla adoptada: No acreditada aquí · reserva material: 20 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): SIN-UNION 24 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-09` (por ENVIPE) — [D11 · ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato] Opciones: (a) Confirmar para ENVIP → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 24 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL ×13, ASTRA5-MESA-DOCUMENTAL ×6, ASTRA5-U5 ×5 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md` ⟨F13⟩
- **Frente 2027**: ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-09` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🔴 CARRIL-13 · Humor in Mexican Psychological Life · 2023-2026 Update ⟨F1 F14⟩

- **Semáforo ROJO** — núcleo con cifra adoptada 0/1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 34**: medible en corpus 1 · con adquisición 19 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 1 ⟨F1⟩
- **Dominios**: HUMOR 28 (82%) núcleo · SALUD_MENTAL 4 (12%) · GENERO 2 (6%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): LATINOBAROMETRO 3; sin instrumento reconocido: 31 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): LATINOBAROMETRO 3 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: HUMOR ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): GENERO 7304 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 68 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 3 / 15 / 0 / 17): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 17 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · SIN-UNION 17 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F7⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-16` (por LATINOBAROMETRO) — [D18 · Latinobarómetro 2024: levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 17 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-CULTURA ×5, ASTRA5-MESA-CULTURA / ASTRA5-MESA-DOCUMENTAL ×3, ASTRA5-U4 ×3 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-16` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🔴 CARRIL-17 · Moral Emotions in Mexico · Declared Dignity · Relational Face · and Residual Catholic Guilt ⟨F1 F14⟩

- **Semáforo ROJO** — núcleo con cifra adoptada 0/1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 31**: medible en corpus 7 · con adquisición 15 · no medible por diseño 8 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 2 ⟨F1⟩
- **Dominios**: EMOCIONES_MORALES 22 (71%) núcleo · CONFIANZA 3 (10%) · RELIGIOSIDAD 2 (6%) · FAMILIA_CUIDADOS 1 (3%) · RURAL_INDIGENA 1 (3%) · SALUD_MENTAL 1 (3%) · VIOLENCIA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): LATINOBAROMETRO 2 · CCPV 1 · CONEVAL 1 · ENADIS 1 · ENASEM 1 · ENASIC 1 · ENBIARE 1 · ENCUCI 1 · ENDIREH 1 · WVS 1; sin instrumento reconocido: 21 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CONEVAL 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: EMOCIONES_MORALES ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · FAMILIA_CUIDADOS 1449 · RELIGIOSIDAD 404 · RURAL_INDIGENA 77 · SALUD_MENTAL 2758 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: ningún RESULT de sus instrumentos o núcleo ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 19 / 0 / 15): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 15 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 14 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 14 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-INTERACCION ×8, ASTRA5-MESA-SALUD ×2, ASTRA5-MESA-GENERO ×2 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-INTERACCION ×8, ASTRA5-MESA-SALUD ×2, ASTRA5-MESA-GENERO ×2 ⟨F1 F5 F6⟩

##### 🟡 CARRIL-24 · Psicología del Trabajo en México · Un Mapa Basado en Evidencia ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 57**: medible en corpus 5 · con adquisición 34 · no medible por diseño 18 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 4 ⟨F1⟩
- **Dominios**: TRABAJO 38 (67%) núcleo · CONFIANZA 4 (7%) · GENERO 4 (7%) · JUVENTUD 3 (5%) · CONOCIMIENTO 2 (4%) · RURAL_INDIGENA 2 (4%) · CONSUMO 1 (2%) · POLITICA 1 (2%) · SALUD_MENTAL 1 (2%) · TIEMPO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENOE 5 · OECD 3 · CONEVAL 1 · WVS 1; sin instrumento reconocido: 48 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENOE 3 · OECD 2 · CONEVAL 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - TRABAJO (núcleo): 26409 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENOE* 26409 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · CONOCIMIENTO 408 · CONSUMO 4470 · GENERO 7304 · POLITICA 124 · RURAL_INDIGENA 77 · SALUD_MENTAL 2758 · TIEMPO 78 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 134 · PASA 2 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 49 / 2 / 94): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 94 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 31 ⟨F1 F5 F6⟩
- **Stoppers** (5): ⟨F1 F5 F6 F8 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 31 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U1 ×31 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 2; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 2; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENOE) — PARO-PREMISA · P3 → MESA-ACCION (2026-10-05) · antes: FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-20-ADQ-ENOE-PRE2019.md`, `2026-09-23-ASTRA5-U1-TRABAJO-ENOE.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

##### 🟡 CARRIL-15 · La familia mexicana como sistema psicológico · entre el afecto · la obligación y la adaptación económica ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 51**: medible en corpus 8 · con adquisición 32 · no medible por diseño 9 · no construible 2; citan un CALC/RESULT en `gen2_existente`: 9 ⟨F1⟩
- **Dominios**: FAMILIA_CUIDADOS 23 (45%) núcleo · DINERO 6 (12%) · SALUD_MENTAL 5 (10%) · GENERO 4 (8%) · JUVENTUD 4 (8%) · TRABAJO 4 (8%) · CAPITAL_SOCIAL 2 (4%) · RURAL_INDIGENA 1 (2%) · SALUD 1 (2%) · VIOLENCIA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIGH 3 · ENOE 3 · ENUT 3 · CCPV 2 · CONEVAL 2 · OECD 2 · SHF 2 · BANXICO 1 · ECCO 1 · EDR 1 · ENASIC 1 · ENDIREH 1 · ENIF 1 · ENSAFI 1 · INTERCENSAL 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CCPV 2 · ENUT 2 · CONEVAL 1 · ENASIC 1 · ENSAFI 1 · OECD 1 · SHF 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - FAMILIA_CUIDADOS (núcleo): 611 · 838 · 0 · 0 — por instrumento (* = el carril lo cita): CCPV* 640, EDER 2, ENADID 679, ENASIC* 98, ENIF* 3, ENIGH* 26, ENUT* 1 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CAPITAL_SOCIAL 661 · DINERO 124 · GENERO 7304 · RURAL_INDIGENA 77 · SALUD 800 · SALUD_MENTAL 2758 · TRABAJO 26409 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 420 · NO-PASA 229 · PASA 257 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 49 / 1 / 70): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 70 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 4 · PROGRAMA-OBTENIDO-EN-COLA 6 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F8⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-FAMILIA ×9, ASTRA5-MESA-SALUD ×4, ASTRA5-U1 ×2 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 2; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 2; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-13-ENASIC-SPLIT.md`, `2026-09-19-GEN2-ENSAFI-ESTRATEGIAS-CONJUNTAS-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-FAMILIA ×9, ASTRA5-MESA-SALUD ×4, ASTRA5-U1 ×2 ⟨F1 F5 F6⟩

##### 🟡 CARRIL-09 · El México Rural e Indígena en sus Propios Términos · Comunalidad · Autoridad y Reciprocidad como Sistemas con Lógica Propia ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 49**: medible en corpus 7 · con adquisición 23 · no medible por diseño 19 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 5 ⟨F1⟩
- **Dominios**: RURAL_INDIGENA 38 (78%) núcleo · SALUD 5 (10%) · MIGRACION 3 (6%) · RELIGIOSIDAD 2 (4%) · GENERO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENUT 4 · CONEVAL 2 · ENIGH 2 · CAAS 1 · ENADID 1 · ENASEM 1 · ENASIC 1 · ENDIREH 1 · ENSANUT 1; sin instrumento reconocido: 38 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENUT 3 · CONEVAL 2 · ENASEM 1 · ENASIC 1 · ENIGH 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - RURAL_INDIGENA (núcleo): 0 · 77 · 0 · 0 — por instrumento (* = el carril lo cita): ENADID* 51, ENUT* 26 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · SALUD 800 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 19 · NO-PASA 2 · PASA 1 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 5 / 21 / 2 / 32): EN-MAIN · recibo pr-1240 · regla adoptada: No acreditada aquí · reserva material: 32 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F8⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U5 ×18, ASTRA5-MESA-RURAL ×2 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-13-ENASIC-SPLIT.md` ⟨F13⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-U5 ×18, ASTRA5-MESA-RURAL ×2 ⟨F1 F5 F6⟩

##### 🟡 CARRIL-07 · El Efecto Ambiental de la Violencia Crónica en México · Cómo el Miedo Reorganiza la Conducta Psicológica de la Población ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 48**: medible en corpus 14 · con adquisición 21 · no medible por diseño 12 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 8 ⟨F1⟩
- **Dominios**: VIOLENCIA 22 (46%) núcleo · DINERO 8 (17%) · CONFIANZA 5 (10%) · SALUD_MENTAL 5 (10%) · GENERO 4 (8%) · MIGRACION 2 (4%) · AUTORIDAD 1 (2%) · POLITICA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENVIPE 7 · ENSU 5 · SESNSP 2 · BANXICO 1 · ENCIG 1 · ENCOAP 1 · ENVE 1 · LATINOBAROMETRO 1 · OECD 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENVIPE 5 · ENSU 3 · SESNSP 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - VIOLENCIA (núcleo): 138 · 12667 · 0 · 0 — por instrumento (* = el carril lo cita): ENSU* 12634, ENVIPE* 171 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): AUTORIDAD 142 · CONFIANZA 2007 · DINERO 124 · GENERO 7304 · MIGRACION 126 · POLITICA 124 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12109 · NO-PASA 525 · PASA 151 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 9 / 25 / 2 / 104): EN-MAIN · recibo pr-1180 · regla adoptada: No acreditada aquí · reserva material: 104 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 18 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-09` (por ENVIPE) — [D11 · ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato] Opciones: (a) Confirmar para ENVIP → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 18 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-VIOLENCIA ×14, ASTRA5-MESA-MIGRACION ×2, ASTRA5-U2 ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENSU) — PARO-PREMISA · P3 → MESA-ACCION (2026-10-05) · antes: FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md` ⟨F13⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENSU-CAMPECHE-INSEGURIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA() · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-09` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-10 · Elegir · Cortejar y Amar en el México de Hoy · Díada de Pareja · Apps de Citas y Cambio en los Guiones de Género ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 46**: medible en corpus 5 · con adquisición 25 · no medible por diseño 16 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 6 ⟨F1⟩
- **Dominios**: PAREJA 30 (65%) núcleo · VIOLENCIA 12 (26%) núcleo · GENERO 1 (2%) · MIGRACION 1 (2%) · RELIGIOSIDAD 1 (2%) · SALUD 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): EMAT 6 · ENDIREH 4 · ENADID 2 · ENDISEG 2 · ENOE 2 · CCPV 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): EMAT 6 · ENDIREH 4 · ENDISEG 2 · ENOE 2 · ENADID 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - PAREJA (núcleo): 0 · 3304 · 0 · 0 — por instrumento (* = el carril lo cita): EMAT* 3304 ⟨F2⟩
  - VIOLENCIA (núcleo): 138 · 12667 · 0 · 0 — por instrumento (* = el carril lo cita): ENSU 12634, ENVIPE 171 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · SALUD 800 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12879 · NO-PASA 535 · PASA 3332 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 24 / 2 / 48): EN-MAIN · recibo pr-1197 · regla adoptada: No acreditada aquí · reserva material: 48 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 4 · PROGRAMA-OBTENIDO-EN-COLA 6 · SIN-UNION 15 ⟨F1 F5 F6⟩
- **Stoppers** (8): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (5) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-11` (por ENDIREH, PAREJA) — [D13 · Firma de contenido de los sucesores ENDIREH 2006 y 2016] Opciones: (A) Firmar por separado las tres lín → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` (por ENDIREH) — ACOTAR RESULT-ENDIREH2016-PF-TABLA#4 y #50 (edad 60+, vida y desde oct-2015) en catálogo v1.4 con rótulo «60+  → mesa firma; encargo 2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-03` (por ENDIREH) — [D1 · Régimen de aislamiento de la sesión ciega de C1 (767 identidades ENDIREH 2021)] Opciones: (a) Extender R → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-05` (por ENDIREH) — [D4 · Publicabilidad frágil de 10 celdas ENDIREH del lote 1] Opciones: (a) Dejar las 10 en ACOTADA de forma pe → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-19` (por ENADID) — [D21 · ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?] Opciones: (A) Reservarlas por escrito (fila reserva:*  → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 15 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-PAREJA ×10, ASTRA5-U2 ×4, ASTRA5-MESA-GENERO ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-03` (por ENDIREH) — PARO-PREMISA: · ENTORNO · ENDIREH 2021 → DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) · antes: GEN2-ASTRA6-C1-LOTE-4 (767 ENDI ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENOE) — PARO-PREMISA · P3 → MESA-ACCION (2026-10-05) · antes: FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-20-ADQ-ENOE-PRE2019.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md`, `2026-09-23-ASTRA5-U1-TRABAJO-ENOE.md`, `2026-09-23-ASTRA5-U2-GENERO-ENDIREH.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-11` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-14 · La arquitectura invisible de la interacción social en México ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 45**: medible en corpus 2 · con adquisición 30 · no medible por diseño 13 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: INTERACCION 14 (31%) núcleo · TRABAJO 9 (20%) núcleo · SALUD_MENTAL 6 (13%) · GENERO 3 (7%) · JUVENTUD 3 (7%) · VIOLENCIA 3 (7%) · EMOCIONES_MORALES 2 (4%) · AUTORIDAD 1 (2%) · CONFIANZA 1 (2%) · HUMOR 1 (2%) · POLITICA 1 (2%) · SANCION_SOCIAL 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENASIC 1 · ENNVIH 1 · ENSU 1 · LAPOP 1 · WVS 1; sin instrumento reconocido: 41 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ninguno ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - TRABAJO (núcleo): 26409 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENOE 26409 ⟨F2⟩
  - núcleo sin filas en el catálogo: INTERACCION ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): AUTORIDAD 142 · CONFIANZA 2007 · GENERO 7304 · POLITICA 124 · SALUD_MENTAL 2758 · SANCION_SOCIAL 9 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 134 · PASA 2 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 26 / 1 / 22): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 22 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · SIN-UNION 28 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 28 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-INTERACCION ×9, ASTRA5-MESA-SALUD ×5, ASTRA5-U1 ×3 ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-23-ASTRA5-U1-TRABAJO-ENOE.md` ⟨F13⟩
- **Frente 2027**: ENSU-CAMPECHE-INSEGURIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA() ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-INTERACCION ×9, ASTRA5-MESA-SALUD ×5, ASTRA5-U1 ×3 ⟨F1 F5 F6⟩

##### 🟡 CARRIL-01 · Adopción y Resistencia Tecnológica en México · La Paradoja de la Baja Confianza Institucional ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 43**: medible en corpus 16 · con adquisición 15 · no medible por diseño 12 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 12 ⟨F1⟩
- **Dominios**: TECNOLOGIA 38 (88%) núcleo · CONFIANZA 2 (5%) · RURAL_INDIGENA 1 (2%) · SALUD 1 (2%) · TRABAJO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENDUTIH 11 · LATINOBAROMETRO 2 · ENADID 1 · OECD 1 · WVS 1; sin instrumento reconocido: 28 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENDUTIH 11 · OECD 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - TECNOLOGIA (núcleo): 1827 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENDUTIH* 1578, MOCIBA 249 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · RURAL_INDIGENA 77 · SALUD 800 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: ningún RESULT de sus instrumentos o núcleo ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 7 / 42 / 7 / 74): EN-MAIN · recibo pr-1196 · regla adoptada: No acreditada aquí · reserva material: 74 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · SIN-UNION 14 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 14 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U4 ×9, ASTRA5-U3_U4 ×4, ASTRA5-U3 ×1 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 1; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 1; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-23-ASTRA5-U4-TECNOLOGIA.md` ⟨F13⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-U4 ×9, ASTRA5-U3_U4 ×4, ASTRA5-U3 ×1 ⟨F1 F5 F6⟩

##### 🟡 CARRIL-06 · El Clasemediero Mexicano · Identidad · Ansiedad de Estatus y el Miedo Racional a Caer ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 43**: medible en corpus 4 · con adquisición 24 · no medible por diseño 15 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 4 ⟨F1⟩
- **Dominios**: MOVILIDAD 25 (58%) núcleo · POLITICA 5 (12%) · CONOCIMIENTO 4 (9%) · SALUD_MENTAL 4 (9%) · DINERO 3 (7%) · CONSUMO 1 (2%) · TRABAJO 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENBIARE 3 · ENIGH 3 · CEEY_EMOVI 1 · CNBV 1 · CONEVAL 1 · ENOE 1 · IECM 1 · MMSI 1; sin instrumento reconocido: 31 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIGH 3 · ENBIARE 2 · CEEY_EMOVI 1 · CONEVAL 1 · MMSI 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MOVILIDAD (núcleo): 172 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENASEM 14, MMSI* 158 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONOCIMIENTO 408 · CONSUMO 4470 · DINERO 124 · POLITICA 124 · SALUD_MENTAL 2758 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 1): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 425 · NO-PASA 6 · PASA 1 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 15 / 4 / 41): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 41 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 3 · PROGRAMA-OBTENIDO-EN-COLA 3 · SIN-UNION 16 ⟨F1 F5 F6⟩
- **Stoppers** (5): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (4) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 16 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-MOVILIDAD ×7, ASTRA5-MESA-CONOCIMIENTO ×4, ASTRA5-U3 ×3 ⟨F1 F5 F6⟩
    - `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` — estado OBTENIDO-PARCIAL; prioridad 3; afirmaciones 1; origen MAESTRA38-N6 (propaga FP-298, disena MAESTRA38-N5 #3 dinero. → caja (completa el payload) ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

##### 🟡 CARRIL-20 · Psicología Política y Comportamiento Cívico del Mexicano Contemporáneo · Una Lectura Anti-Esencialista desde Abajo · 2026 ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 40% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 43**: medible en corpus 18 · con adquisición 14 · no medible por diseño 11 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 17 ⟨F1⟩
- **Dominios**: POLITICA 40 (93%) núcleo · CONFIANZA 2 (5%) · VIOLENCIA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENVIPE 8 · ENCIG 6 · ENEM 3 · LAPOP 2 · LATINOBAROMETRO 2 · WVS 2 · CSES 1 · MMSI 1; sin instrumento reconocido: 21 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENVIPE 7 · ENCIG 6 · ENEM 3 · LATINOBAROMETRO 2 · CSES 1 · LAPOP 1 · MMSI 1 · WVS 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - POLITICA (núcleo): 14 · 110 · 2 · 0 — por instrumento (* = el carril lo cita): CIDE-CSES 4, ENCUCI 2, ENVIPE* 12, LAPOP* 38, LATINOBAROMETRO* 68 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (10; encabezados excluidos 0): MATIZA 3 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 6; con dictamen distinto de SIN-CIFRA-GEN2 40% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 230 · PASA 157 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 6 / 16 / 4 / 34): EN-MAIN · recibo pr-1240 · regla adoptada: No acreditada aquí · reserva material: 34 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · SIN-UNION 13 ⟨F1 F5 F6⟩
- **Stoppers** (8): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (4) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-09` (por ENVIPE) — [D11 · ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato] Opciones: (a) Confirmar para ENVIP → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-16` (por LATINOBAROMETRO) — [D18 · Latinobarómetro 2024: levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `CSES 2016` — manifiesto estado_reserva: RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO ×1; afirmaciones que la citan: 1 → E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito ⟨F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 13 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×13 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
    - `NC-260923-GEN2-CONTADORES-CONSUMO-2-749c-01` (por ENCIG) — PARO-PREMISA · P3 (canal completo): 16 celdas de GOB.gobierno_digital.encig2025.edad_x_sexo + . → CANAL (derivados/auto-*) · antes: cerrable al fusionar el [deriva] o su acto: EN-CURSO [ca ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md`, `2026-09-23-ASTRA5-U3-POLITICA.md` ⟨F13⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-09` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-25 · Psychology of Mexico-US Migration · Identity · Family · Aspiration · and Wellbeing in 2025 ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 42**: medible en corpus 4 · con adquisición 17 · no medible por diseño 20 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: MIGRACION 42 (100%) núcleo ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENADID 7 · BANXICO 2 · ENIGH 2 · PEW 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENADID 7 · BANXICO 2 · ENIGH 2 · PEW 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MIGRACION (núcleo): 0 · 126 · 0 · 0 — por instrumento (* = el carril lo cita): PEW* 126 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 55 · NO-PASA 2 · PASA 105 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 19 / 1 / 48): EN-MAIN · recibo pr-1197 · regla adoptada: No acreditada aquí · reserva material: 48 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 15 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F7⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-19` (por ENADID) — [D21 · ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?] Opciones: (A) Reservarlas por escrito (fila reserva:*  → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 15 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-MIGRACION ×15 ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` ⟨F13⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-19` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-12 · Health · Body · Food and Substance Use in Mexico · The Behavioral Layer of Decisions · Environment and Structure ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 39**: medible en corpus 11 · con adquisición 22 · no medible por diseño 6 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 4 ⟨F1⟩
- **Dominios**: SALUD 32 (82%) núcleo · CONSUMO 7 (18%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENSANUT 13 · ENCODAT 7 · CONEVAL 1 · ENADID 1 · ENCUCI 1 · ENOE 1 · LAPOP 1; sin instrumento reconocido: 16 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENSANUT 11 · ENCODAT 7 · CONEVAL 1 · ENADID 1 · ENCUCI 1 · ENOE 1 · LAPOP 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - SALUD (núcleo): 2 · 798 · 0 · 0 — por instrumento (* = el carril lo cita): ENCODAT* 130, ENSANUT* 670 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONSUMO 4470 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 400 · PASA 99 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 15 / 0 / 35): EN-MAIN · recibo pr-1242 · regla adoptada: No acreditada aquí · reserva material: 35 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): PROGRAMA-OBTENIDO-EN-COLA 10 · SIN-UNION 12 ⟨F1 F5 F6⟩
- **Stoppers** (7): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-19` (por ENADID) — [D21 · ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?] Opciones: (A) Reservarlas por escrito (fila reserva:*  → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **RESERVA** (4) ⟨F12 F6 F15⟩
    - `ENCODAT 2025` — manifiesto estado_reserva: DOCUMENTACION-ESTRUCTURAL-NO-RESPUESTAS ×5; RESERVADA-NO-ABIERTA-NO-INDEXAR-L ×3; afirmaciones que la citan: 7 → E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito; expediente forense/prereg-aperturas/ENCODAT-2025 (CODIGO-CONGELADO del expediente ENCODAT-) ⟨F6⟩
    - `ENOE 2026` — manifiesto estado_reserva: RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO ×2; RESERVADA-NO-ABIERTA-NO-INDEXAR-L ×1; afirmaciones que la citan: 1 → familia 2027 ENOE-INFORMALIDAD; expediente forense/prereg-aperturas/ENOE-2026T2 (CODIGO-CONGELADO del expediente ENOE-202) ⟨F6⟩
    - `ENOE 2026T2` — tabla-final olas_reservadas_al_entrar; afirmaciones que la citan: 1 → familia 2027 ENOE-INFORMALIDAD; expediente forense/prereg-aperturas/ENOE-2026T2 (CODIGO-CONGELADO del expediente ENOE-202) ⟨F12⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 12 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-SALUD ×12 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENOE) — PARO-PREMISA · P3 → MESA-ACCION (2026-10-05) · antes: FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-08-20-ADQ-ENOE-PRE2019.md`, `2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md`, `2026-09-17-GEN2-ADQ-HANDOFF-RESULTADO-Y-SALUD-1-ENCARGO.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` … y 1 más ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-19` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-29 · Salud Mental en México · Prevalencia · Estigma y la Brecha entre Necesidad y Atención ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 39**: medible en corpus 6 · con adquisición 23 · no medible por diseño 9 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 5 ⟨F1⟩
- **Dominios**: SALUD_MENTAL 22 (56%) núcleo · GENERO 3 (8%) · JUVENTUD 3 (8%) · MIGRACION 2 (5%) · RELIGIOSIDAD 2 (5%) · TECNOLOGIA 2 (5%) · VIOLENCIA 2 (5%) · EMOCIONES_MORALES 1 (3%) · FAMILIA_CUIDADOS 1 (3%) · RURAL_INDIGENA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENSANUT 4 · EDR 2 · ENDUTIH 2 · ENIGH 2 · ENCOVID 1 · ENNVIH 1; sin instrumento reconocido: 28 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): EDR 2 · ENSANUT 2 · ENCOVID 1 · ENIGH 1 · ENNVIH 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - SALUD_MENTAL (núcleo): 180 · 2578 · 0 · 0 — por instrumento (* = el carril lo cita): EDR* 2578, ENBIARE 180 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): FAMILIA_CUIDADOS 1449 · GENERO 7304 · MIGRACION 126 · RELIGIOSIDAD 404 · RURAL_INDIGENA 77 · TECNOLOGIA 1827 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 541 · NO-PASA 6 · PASA 2291 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 36 / 2 / 68): EN-MAIN · recibo pr-1180 · regla adoptada: No acreditada aquí · reserva material: 68 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-SALUD ×15, ASTRA5-MESA-GENERO ×2, ASTRA5-U0 ×1 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-SALUD ×15, ASTRA5-MESA-GENERO ×2, ASTRA5-U0 ×1 ⟨F1 F5 F6⟩

##### 🟡 CARRIL-08 · El Mexicano y el Tiempo · Estructura · no Cultura · en la Planeación y el Compromiso Temporal ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 29% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 12 · con adquisición 12 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 7 ⟨F1⟩
- **Dominios**: TIEMPO 18 (47%) núcleo · TRABAJO 4 (11%) · DINERO 3 (8%) · MOVILIDAD 3 (8%) · VIOLENCIA 3 (8%) · INTERACCION 2 (5%) · CONFIANZA 1 (3%) · CONSUMO 1 (3%) · GENERO 1 (3%) · JUVENTUD 1 (3%) · SALUD 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIF 1 · ENOE 1 · ENUT 1; sin instrumento reconocido: 35 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIF 1 · ENUT 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - TIEMPO (núcleo): 0 · 78 · 0 · 0 — por instrumento (* = el carril lo cita): ENUT* 78 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · CONSUMO 4470 · DINERO 124 · GENERO 7304 · MOVILIDAD 172 · SALUD 800 · TRABAJO 26409 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (7; encabezados excluidos 2): MATIZA 1 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 5; con dictamen distinto de SIN-CIFRA-GEN2 29% ⟨F3⟩
- **Validación ciega**: PASA 12 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 10 / 5 / 29): EN-MAIN · recibo pr-1242 · regla adoptada: No acreditada aquí · reserva material: 29 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 5 · SIN-UNION 7 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-22` (por ENIF) — [D24 · Anexo A del lote ENIF 2024 archivado con otro sha256] Opciones: (a) Mesa aporta el Anexo A original byt → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 2) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 7 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U1 ×7 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-22` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-18 · Mérito · Movilidad Social y Desigualdad en México · Actualización 2025-2026 ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 6 · con adquisición 22 · no medible por diseño 6 · no construible 4; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: MOVILIDAD 22 (58%) núcleo · CONFIANZA 5 (13%) · DINERO 3 (8%) · JUVENTUD 2 (5%) · TRABAJO 2 (5%) · CONSUMO 1 (3%) · GENERO 1 (3%) · MIGRACION 1 (3%) · POLITICA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): CEEY_EMOVI 8 · ENCIG 3 · ENIGH 3 · MMSI 3 · ENOE 2 · BANXICO 1 · ENADIS 1 · LATINOBAROMETRO 1 · OECD 1 · WVS 1; sin instrumento reconocido: 15 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CEEY_EMOVI 8 · MMSI 3 · ENIGH 2 · ENADIS 1 · LATINOBAROMETRO 1 · WVS 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MOVILIDAD (núcleo): 172 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENASEM 14, MMSI* 158 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · CONSUMO 4470 · DINERO 124 · GENERO 7304 · MIGRACION 126 · POLITICA 124 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 245 · NO-PASA 2 · PASA 1 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 3 / 26 / 0 / 54): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 54 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 7 · EN-MANIFIESTO 3 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 10 ⟨F1 F5 F6⟩
- **Stoppers** (7): ⟨F1 F5 F6 F7 F12 F15⟩
  - **FIRMA** (3) ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-16` (por LATINOBAROMETRO) — [D18 · Latinobarómetro 2024: levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 2) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 10 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-MOVILIDAD / ASTRA5-MESA-DOCUMENTAL ×4, ASTRA5-U1 ×2, ASTRA5-MESA-ECONOMIA ×2 ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 7; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 7; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩

##### 🟡 CARRIL-23 · Psicología del Consumidor Mexicano · Patrones · Contradicciones y Estrategia ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 40% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 5 · con adquisición 23 · no medible por diseño 10 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 6 ⟨F1⟩
- **Dominios**: CONSUMO 25 (66%) núcleo · DINERO 9 (24%) núcleo · TECNOLOGIA 2 (5%) · CONFIANZA 1 (3%) · JUVENTUD 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIF 3 · ENDUTIH 2 · ENIGH 2 · BANXICO 1 · WVS 1; sin instrumento reconocido: 29 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIF 3 · ENIGH 2 · BANXICO 1 · ENDUTIH 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CONSUMO (núcleo): 0 · 4470 · 0 · 0 — por instrumento (* = el carril lo cita): ENGASTO 330, ENIGH* 4140 ⟨F2⟩
  - DINERO (núcleo): 76 · 48 · 0 · 0 — por instrumento (* = el carril lo cita): ENFIH 2, ENIF* 105, ENNVIH 1, ENSAFI 16 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · TECNOLOGIA 1827 ⟨F2⟩
- **Reglas del report** (5; encabezados excluidos 1): CONFIRMA 1 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 40% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 6 · NO-PASA 3 · PASA 23 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 69 / 0 / 144): EN-MAIN · recibo RECIBO-ASTRA6-1 · regla adoptada: No acreditada aquí · reserva material: 144 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 20 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6 F7 F12 F15⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-22` (por ENIF) — [D24 · Anexo A del lote ENIF 2024 archivado con otro sha256] Opciones: (a) Mesa aporta el Anexo A original byt → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `ENDUTIH 2025` — manifiesto estado_reserva: RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO ×1; afirmaciones que la citan: 1 → E.6: la levanta el código congelado de una prueba pre-registrada o mesa por escrito; expediente forense/prereg-aperturas/ENDUTIH-2025 (SOLO-MESA-POR-ESCRITO (sin contendiente ) ⟨F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 20 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-CONSUMO ×14, ASTRA5-MESA-DINERO ×3, ASTRA5-MESA-DIGITAL ×1 ⟨F1 F5 F6⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-22` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-27 · Religiosidad y Psicología del Mexicano Contemporáneo · Moral · Afrontamiento · Consumo e Identidad en Transformación ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 4 · con adquisición 22 · no medible por diseño 9 · no construible 3; citan un CALC/RESULT en `gen2_existente`: 0 ⟨F1⟩
- **Dominios**: RELIGIOSIDAD 28 (74%) núcleo · CONSUMO 3 (8%) · POLITICA 3 (8%) · SALUD_MENTAL 2 (5%) · GENERO 1 (3%) · MIGRACION 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): PEW 5 · CCPV 2 · TEPJF 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): PEW 5 · CCPV 2 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - RELIGIOSIDAD (núcleo): 0 · 404 · 0 · 0 — por instrumento (* = el carril lo cita): LATINOBAROMETRO 34, PEW* 237, WVS 133 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONSUMO 4470 · GENERO 7304 · MIGRACION 126 · POLITICA 124 · SALUD_MENTAL 2758 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 451 · NO-PASA 227 · PASA 6 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 106 / 4 / 47): EN-MAIN · recibo pr-1171 · regla adoptada: No acreditada aquí · reserva material: 47 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 19 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 19 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-RELIGION ×16, ASTRA5-MESA-MIGRACION ×1, ASTRA5-MESA-SALUD ×1 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-RELIGION ×16, ASTRA5-MESA-MIGRACION ×1, ASTRA5-MESA-SALUD ×1 ⟨F1 F5 F6⟩

##### 🟡 CARRIL-28 · Report 26 · The Contemporary Mexican and Knowledge · Expertise · Education and Information as Decision Behavior ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 44% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 3 · con adquisición 19 · no medible por diseño 16 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: CONOCIMIENTO 17 (45%) núcleo · SALUD 8 (21%) núcleo · CONFIANZA 6 (16%) · TECNOLOGIA 3 (8%) · TRABAJO 3 (8%) · RURAL_INDIGENA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): OECD 4 · ENPECYT 3 · ENSANUT 3 · PISA 3 · ENDUTIH 2 · ENOE 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 24 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): OECD 4 · ENPECYT 3 · PISA 3 · ENSANUT 2 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CONOCIMIENTO (núcleo): 0 · 408 · 0 · 0 — por instrumento (* = el carril lo cita): ENIGH 128, ENPECYT* 280 ⟨F2⟩
  - SALUD (núcleo): 2 · 798 · 0 · 0 — por instrumento (* = el carril lo cita): ENCODAT 130, ENSANUT* 670 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · RURAL_INDIGENA 77 · TECNOLOGIA 1827 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (9; encabezados excluidos 0): CONFIRMA 1 · MATIZA 2 · MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 5; con dictamen distinto de SIN-CIFRA-GEN2 44% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 450 · PASA 90 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 5 / 28 / 2 / 99): EN-MAIN · recibo pr-1196 · regla adoptada: No acreditada aquí · reserva material: 99 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · EN-MANIFIESTO 2 · PROGRAMA-OBTENIDO-EN-COLA 9 · SIN-UNION 7 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 7 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-CONOCIMIENTO ×5, ASTRA5-MESA-CONOCIMIENTO / ASTRA5-MESA-DOCUMENTAL ×1, ASTRA5-MESA-SALUD ×1 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 1; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 1; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md`, `2026-09-17-GEN2-ADQ-HANDOFF-RESULTADO-Y-SALUD-1-ENCARGO.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

##### 🟡 CARRIL-31 · Vejez y Cuidado Intergeneracional en México · El Debilitamiento del Seguro Familiar ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 25% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 9 · con adquisición 24 · no medible por diseño 5 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 6 ⟨F1⟩
- **Dominios**: FAMILIA_CUIDADOS 15 (39%) núcleo · TRABAJO 5 (13%) · DINERO 4 (11%) · SALUD 4 (11%) · SALUD_MENTAL 4 (11%) · MIGRACION 2 (5%) · CONSUMO 1 (3%) · GENERO 1 (3%) · RURAL_INDIGENA 1 (3%) · TIEMPO 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENASEM 5 · ENOE 3 · CCPV 2 · ENUT 2 · CONEVAL 1 · ENADID 1 · ENIGH 1; sin instrumento reconocido: 23 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CCPV 2 · ENADID 1 · ENIGH 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - FAMILIA_CUIDADOS (núcleo): 611 · 838 · 0 · 0 — por instrumento (* = el carril lo cita): CCPV* 640, EDER 2, ENADID* 679, ENASIC 98, ENIF 3, ENIGH* 26, ENUT* 1 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONSUMO 4470 · DINERO 124 · GENERO 7304 · MIGRACION 126 · RURAL_INDIGENA 77 · SALUD 800 · SALUD_MENTAL 2758 · TIEMPO 78 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): MATIZA 1 · SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 25% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 420 · NO-PASA 229 · PASA 101 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 42 / 0 / 86): EN-MAIN · recibo pr-1197 · regla adoptada: No acreditada aquí · reserva material: 86 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 6 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 16 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6 F7 F12 F15⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-19` (por ENADID) — [D21 · ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?] Opciones: (A) Reservarlas por escrito (fila reserva:*  → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 16 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-VEJEZ ×13, ASTRA5-MESA-SALUD ×3 ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-19` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-04 · Behavioral Finance Mexicano · Estructura · Adaptación Racional y Cultura en el Ahorro · Crédito y Riesgo ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 33% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 35**: medible en corpus 18 · con adquisición 6 · no medible por diseño 10 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 11 ⟨F1⟩
- **Dominios**: DINERO 30 (86%) núcleo · CONFIANZA 3 (9%) · CONSUMO 1 (3%) · GENERO 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENIF 10 · ENAFI 1; sin instrumento reconocido: 25 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENIF 9 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - DINERO (núcleo): 76 · 48 · 0 · 0 — por instrumento (* = el carril lo cita): ENFIH 2, ENIF* 105, ENNVIH 1, ENSAFI 16 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · CONSUMO 4470 · GENERO 7304 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): MATIZA-SIN-CRUCE 1 · SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 33% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 1 · NO-PASA 1 · PASA 12 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 24 / 5 / 64): EN-MAIN · recibo pr-1196 · regla adoptada: No acreditada aquí · reserva material: 64 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): SIN-UNION 6 ⟨F1 F5 F6⟩
- **Stoppers** (2): ⟨F1 F5 F6 F7⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-22` (por ENIF) — [D24 · Anexo A del lote ENIF 2024 archivado con otro sha256] Opciones: (a) Mesa aporta el Anexo A original byt → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 6 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-DINERO ×6 ⟨F1 F5 F6⟩
- **Frente 2027**: ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-22` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-05 · Confianza y Desconfianza en México · Anatomía Psicológica de una Sociedad Dual ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 33**: medible en corpus 6 · con adquisición 17 · no medible por diseño 7 · no construible 3; citan un CALC/RESULT en `gen2_existente`: 7 ⟨F1⟩
- **Dominios**: CONFIANZA 19 (58%) núcleo · CAPITAL_SOCIAL 4 (12%) · DINERO 4 (12%) · AUTORIDAD 3 (9%) · GENERO 1 (3%) · JUVENTUD 1 (3%) · TRABAJO 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCIG 4 · WVS 3 · ENVIPE 2 · LAPOP 2 · OECD 2 · BANXICO 1 · CNBV 1 · ENIF 1 · ENSI 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 18 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENCIG 4 · WVS 3 · ENVIPE 2 · OECD 2 · ENSI 1 · LAPOP 1 · LATINOBAROMETRO 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CONFIANZA (núcleo): 59 · 1948 · 13 · 0 — por instrumento (* = el carril lo cita): ENCIG* 1113, ENCRIGE 27, ENCUCI 40, ENVE 9, ENVIPE* 14, INSTRUMENTO-NO-IDENTIFICADO 4, LATINOBAROMETRO* 323, WVS* 477 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): AUTORIDAD 142 · CAPITAL_SOCIAL 661 · DINERO 124 · GENERO 7304 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 72 · PASA 156 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 150 / 6 / 201): EN-MAIN · recibo pr-1171 · regla adoptada: No acreditada aquí · reserva material: 201 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 3 · PROGRAMA-OBTENIDO-EN-COLA 3 · SIN-UNION 11 ⟨F1 F5 F6⟩
- **Stoppers** (7): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (4) ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-09` (por ENVIPE) — [D11 · ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato] Opciones: (a) Confirmar para ENVIP → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-16` (por LATINOBAROMETRO) — [D18 · Latinobarómetro 2024: levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 11 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×8, ASTRA5-MESA-CONFIANZA ×1, ASTRA5-U2 ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260923-GEN2-CONTADORES-CONSUMO-2-749c-01` (por ENCIG) — PARO-PREMISA · P3 (canal completo): 16 celdas de GOB.gobierno_digital.encig2025.edad_x_sexo + . → CANAL (derivados/auto-*) · antes: cerrable al fusionar el [deriva] o su acto: EN-CURSO [ca ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md` ⟨F13⟩
- **Frente 2027**: ENCIG-PAGO-DIGITAL (SUSPENDIDA(FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01); gate CONTEXTO(gate vigente; soporte_acreditado=False)+CONTRATO-FIRMADO(enmienda pre-d) · ENCIG-SOLICITUD-MORDIDA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENIF-AHORRO-FORMAL (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENIF-HORIZONTE-AHORRO (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE; reserva heredada de v1.0: ACCESO-AUTORIZADO(FP-260926-GEN2-AS) · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩

##### 🟡 CARRIL-26 · Reconfiguración de los Guiones de Género en México · Masculinidades · Feminidades y Violencia a través de Clase · Generación y Región ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 33**: medible en corpus 9 · con adquisición 18 · no medible por diseño 6 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 10 ⟨F1⟩
- **Dominios**: GENERO 12 (36%) núcleo · VIOLENCIA 7 (21%) núcleo · TRABAJO 5 (15%) · POLITICA 3 (9%) · FAMILIA_CUIDADOS 2 (6%) · MIGRACION 1 (3%) · PAREJA 1 (3%) · RURAL_INDIGENA 1 (3%) · TECNOLOGIA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENOE 3 · ENCUCI 2 · ENDIREH 2 · ENUT 2 · SESNSP 2 · ENADID 1 · ENADIS 1 · ENCUP 1 · ENDUTIH 1 · ENNVIH 1 · LAPOP 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 20 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENDIREH 2 · SESNSP 2 · ENADIS 1 · ENCUCI 1 · ENCUP 1 · LAPOP 1 · LATINOBAROMETRO 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - GENERO (núcleo): 7304 · 0 · 7 · 689 — por instrumento (* = el carril lo cita): ENDIREH* 6880, ENDISEG 424 ⟨F2⟩
  - VIOLENCIA (núcleo): 138 · 12667 · 0 · 0 — por instrumento (* = el carril lo cita): ENSU 12634, ENVIPE 171 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): FAMILIA_CUIDADOS 1449 · MIGRACION 126 · PAREJA 3304 · POLITICA 124 · RURAL_INDIGENA 77 · TECNOLOGIA 1827 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12582 · NO-PASA 535 · PASA 160 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 8 / 16 / 1 / 93): EN-MAIN · recibo pr-1180 · regla adoptada: No acreditada aquí · reserva material: 93 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 2 · SIN-UNION 15 ⟨F1 F5 F6⟩
- **Stoppers** (8): ⟨F1 F5 F6 F7 F8 F12 F15⟩
  - **FIRMA** (5) ⟨F7⟩
    - `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` (por ENDIREH) — ACOTAR RESULT-ENDIREH2016-PF-TABLA#4 y #50 (edad 60+, vida y desde oct-2015) en catálogo v1.4 con rótulo «60+  → mesa firma; encargo 2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-03` (por ENDIREH) — [D1 · Régimen de aislamiento de la sesión ciega de C1 (767 identidades ENDIREH 2021)] Opciones: (a) Extender R → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-05` (por ENDIREH) — [D4 · Publicabilidad frágil de 10 celdas ENDIREH del lote 1] Opciones: (a) Dejar las 10 en ACOTADA de forma pe → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-11` (por ENDIREH) — [D13 · Firma de contenido de los sucesores ENDIREH 2006 y 2016] Opciones: (A) Firmar por separado las tres lín → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-16` (por LATINOBAROMETRO) — [D18 · Latinobarómetro 2024: levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 15 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U2 ×7, ASTRA5-MESA-GENERO ×4, ASTRA5-U3 ×2 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-03` (por ENDIREH) — PARO-PREMISA: · ENTORNO · ENDIREH 2021 → DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) · antes: GEN2-ASTRA6-C1-LOTE-4 (767 ENDI ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-23-ASTRA5-U2-GENERO-ENDIREH.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` → mesa firma; encargo 2026-09-28-GEN2-ASTRA6-C1-LOTE-3.md ⟨F7⟩

##### 🟡 CARRIL-03 · Autoridad y jerarquía en el México contemporáneo · anatomía psicológica de un sistema dual ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 1/1; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 30**: medible en corpus 9 · con adquisición 10 · no medible por diseño 11 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: AUTORIDAD 29 (97%) núcleo · POLITICA 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCUCI 3 · LATINOBAROMETRO 2 · CEEY_EMOVI 1 · WVS 1; sin instrumento reconocido: 23 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENCUCI 3 · LATINOBAROMETRO 2 · CEEY_EMOVI 1 · WVS 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - AUTORIDAD (núcleo): 0 · 142 · 0 · 0 — por instrumento (* = el carril lo cita): ENCUCI* 142 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): POLITICA 124 ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 1): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 68 · PASA 3 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 16 / 1 / 41): EN-MAIN · recibo pr-1240 · regla adoptada: No acreditada aquí · reserva material: 41 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · EN-MANIFIESTO 1 · SIN-UNION 8 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F7⟩
  - **FIRMA** (3) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-16` (por LATINOBAROMETRO) — [D18 · Latinobarómetro 2024: levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por WVS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por WVS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 8 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×6, ASTRA5-MESA-MOVILIDAD ×1, ASTRA5-MESA-EMPRESA ×1 ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-16` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟡 CARRIL-21 · Psicología · Conducta y Sociedad en el México Contemporáneo · Análisis Transcultural y Estructural ⟨F1 F14⟩

- **Semáforo AMARILLO** — núcleo con cifra 2/2; reglas con dictamen 0% (umbral 50%) ⟨F1 F2 F3 S⟩
- **Afirmaciones 28**: medible en corpus 1 · con adquisición 21 · no medible por diseño 4 · no construible 2; citan un CALC/RESULT en `gen2_existente`: 1 ⟨F1⟩
- **Dominios**: MOVILIDAD 4 (14%) núcleo · SALUD_MENTAL 4 (14%) núcleo · CONOCIMIENTO 3 (11%) · INTERACCION 3 (11%) · TRABAJO 3 (11%) · GENERO 2 (7%) · RURAL_INDIGENA 2 (7%) · CONFIANZA 1 (4%) · DINERO 1 (4%) · EMOCIONES_MORALES 1 (4%) · FAMILIA_CUIDADOS 1 (4%) · MIGRACION 1 (4%) · POLITICA 1 (4%) · VIOLENCIA 1 (4%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENOE 2 · CCPV 1 · CEEY_EMOVI 1 · CONEVAL 1 · ENUT 1 · OECD 1 · SESNSP 1; sin instrumento reconocido: 21 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): CEEY_EMOVI 1 · CONEVAL 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - MOVILIDAD (núcleo): 172 · 0 · 0 · 0 — por instrumento (* = el carril lo cita): ENASEM 14, MMSI 158 ⟨F2⟩
  - SALUD_MENTAL (núcleo): 180 · 2578 · 0 · 0 — por instrumento (* = el carril lo cita): EDR 2578, ENBIARE 180 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · CONOCIMIENTO 408 · DINERO 124 · FAMILIA_CUIDADOS 1449 · GENERO 7304 · MIGRACION 126 · POLITICA 124 · RURAL_INDIGENA 77 · TRABAJO 26409 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (0; encabezados excluidos 0): ninguna; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 708 · NO-PASA 4 · PASA 2290 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 61 / 22 / 20): EN-MAIN · recibo pr-1247 · regla adoptada: No acreditada aquí · reserva material: 20 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 1 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 17 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F12 F15⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (5) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 17 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-SALUD ×3, ASTRA5-MESA-INTERACCION ×2, ASTRA5-MESA-FAMILIA ×2 ⟨F1 F5 F6⟩
    - `EMOVI_2011` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-SINT-008 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `EMOVI_2023` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-AUTOR-016;ASTRA5-U0-MER-013;ASTRA5-U0-ME → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 1; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 1; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [RESERVA]: `mapa:reserva_v1_1` → E.6 (reserva declarada en el mapa) ⟨F1⟩

##### 🟠 CARRIL-22 · Psicología de la Juventud Mexicana Contemporánea · Gen Z y Millennials Jóvenes como Cohorte Divergente ⟨F1 F14⟩

- **Semáforo NARANJA** — núcleo con cifra adoptada 0/1 y piso sellado registrado pendiente de adopción en 1 ⟨F1 F2 F3 S⟩
- **Afirmaciones 32**: medible en corpus 9 · con adquisición 14 · no medible por diseño 8 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 8 ⟨F1⟩
- **Dominios**: JUVENTUD 10 (31%) núcleo · POLITICA 4 (12%) · TRABAJO 4 (12%) · GENERO 3 (9%) · SALUD_MENTAL 3 (9%) · AUTORIDAD 2 (6%) · FAMILIA_CUIDADOS 2 (6%) · TECNOLOGIA 2 (6%) · PAREJA 1 (3%) · RELIGIOSIDAD 1 (3%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): EDER 3 · ENADID 3 · ENOE 3 · ENDUTIH 2 · OECD 2 · EDR 1 · ENCODAT 1 · ENDISEG 1 · ENSANUT 1 · LATINOBAROMETRO 1; sin instrumento reconocido: 14 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): EDER 3 · ENADID 3 · OECD 1 ⟨F1 F12 S⟩
- **Pisos del núcleo pendientes de adopción** — registrados en la vista: JUVENTUD: CALC-MC2-ENOE-0001; sellados en disco, no registrados (E.7): ninguno ⟨F16 F17 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - núcleo sin filas en el catálogo: JUVENTUD ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): AUTORIDAD 142 · FAMILIA_CUIDADOS 1449 · GENERO 7304 · PAREJA 3304 · POLITICA 124 · RELIGIOSIDAD 404 · SALUD_MENTAL 2758 · TECNOLOGIA 1827 · TRABAJO 26409 ⟨F2⟩
- **Reglas del report** (4; encabezados excluidos 0): SIN-CIFRA-GEN2 4; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 8 · PASA 96 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 10 / 4 / 26): EN-MAIN · recibo pr-1242 · regla adoptada: No acreditada aquí · reserva material: 26 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · EN-MANIFIESTO 4 · PROGRAMA-OBTENIDO-EN-COLA 1 · SIN-UNION 7 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F7 F12 F15⟩
  - **FIRMA** (2) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-07` (por EDER) — [D8 · EDER 2025 (JUV-001/002): levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6  → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-19` (por ENADID) — [D21 · ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?] Opciones: (A) Reservarlas por escrito (fila reserva:*  → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **RESERVA** (1) ⟨F12 F6 F15⟩
    - `mapa:reserva_v1_1` — C4 FIRMAS-16: boletín ENOE 2026T1 consumido; ninguna afirmación de informalidad puede usar (afirmaciones: 1) → E.6 (reserva declarada en el mapa) ⟨F1⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 7 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-U3 ×3, ASTRA5-MESA-JUVENTUD ×2, ASTRA5-MESA-GENERO ×1 ⟨F1 F5 F6⟩
    - `OECD` — estado OBTENIDO-PARCIAL; prioridad 36; afirmaciones 2; origen cola-adquisicion-2026-08-12.tsv:36 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `OECD_TRUST_PUM_2021_2023_2025` — estado SOLICITUD-PREPARADA; prioridad 36; afirmaciones 2; origen NC-0061;NC-0151; GEN2-CRON-DEMANDA-A-DATO-Y-PRODUCCION → mesa con identidad (solicitud preparada) ⟨F1 F5 F6⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-19-EDER-PRIMERA-UNION-SEXO-COHORTE.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1-CONTINUACION.md`, `2026-09-19-GEN2-ENADID-UNION-ACTUAL-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENOE-INFORMALIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(regla de inferencia para 39 estratos singleton)+FIRMA-DE-MESA(F) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-07` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### 🟢 CARRIL-19 · Non-Family Social Capital in Mexico · Cooperation · Trust · and Collective Action Beyond Kinship ⟨F1 F14⟩

- **Semáforo VERDE** — núcleo con cifra 1/1; reglas con dictamen 67% ≥ 50% ⟨F1 F2 F3 S⟩
- **Afirmaciones 42**: medible en corpus 13 · con adquisición 13 · no medible por diseño 16 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 11 ⟨F1⟩
- **Dominios**: CAPITAL_SOCIAL 24 (57%) núcleo · RURAL_INDIGENA 5 (12%) · AUTORIDAD 3 (7%) · DINERO 3 (7%) · CONFIANZA 2 (5%) · RELIGIOSIDAD 2 (5%) · VIOLENCIA 2 (5%) · TECNOLOGIA 1 (2%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENCUCI 5 · ENVIPE 3 · CAAS 1 · CONDUSEF 1 · ENADIS 1 · ENSAFI 1 · ENUT 1 · LAPOP 1; sin instrumento reconocido: 29 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENCUCI 5 · ENSAFI 1 · ENUT 1 · ENVIPE 1 · LAPOP 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - CAPITAL_SOCIAL (núcleo): 0 · 661 · 0 · 0 — por instrumento (* = el carril lo cita): ENVIPE* 47, LAPOP* 614 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): AUTORIDAD 142 · CONFIANZA 2007 · DINERO 124 · RELIGIOSIDAD 404 · RURAL_INDIGENA 77 · TECNOLOGIA 1827 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (9; encabezados excluidos 0): CONFIRMA 2 · MATIZA 1 · MATIZA-SIN-CRUCE 3 · SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 67% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 4 · PASA 306 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 0 / 5 / 0 / 83): EN-MAIN · recibo pr-1171 · regla adoptada: No acreditada aquí · reserva material: 83 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 1 · SIN-UNION 12 ⟨F1 F5 F6⟩
- **Stoppers** (6): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-09` (por ENVIPE) — [D11 · ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato] Opciones: (a) Confirmar para ENVIP → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (3) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 12 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-RURAL ×6, ASTRA5-MESA-CAPITAL_SOCIAL ×3, ASTRA5-U3 ×2 ⟨F1 F5 F6⟩
    - `CONDUSEF-REDECO_SERIE` — estado OBTENIDO-PARCIAL; prioridad 3; afirmaciones 1; origen ASTRA5-U0 ASTRA5-U0-CRFAC-005 → caja (completa el payload) ⟨F1 F5 F6⟩
    - `CONDUSEF_CNBV_TANDAS_FUERA_DE_PERIMETRO` — estado NO-ENCONTRADO; prioridad —; afirmaciones 1; origen gen2-universo-c → acto de nube (/sonda) ⟨F1 F5 F6⟩
  - **NC-PARO** (2) ⟨F8⟩
    - `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` (por ENUT) — PARO-PREMISA: · P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcad → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
    - `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` (por ENVIPE) — PARO-PREMISA: · P1 → DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) · antes: (decidida por delegación: decididas- ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-ENVIPE-RES0028-DERIVADO-U4-1.md`, `2026-09-19-GEN2-ENSAFI-ESTRATEGIAS-CONJUNTAS-CLI-1.md` ⟨F13⟩
- **Frente 2027**: ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-09` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

##### ⚪ CARRIL-11 · Genetica y Conducta del Mexicano Contemporaneo · Canal Individual vs · Estructura ⟨F1 F14⟩

- **Semáforo GRIS** — dominio GENETICA fuera por firewall genético ⟨F1 F2 F3 S⟩
- **Afirmaciones 38**: medible en corpus 0 · con adquisición 35 · no medible por diseño 3 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 0 ⟨F1⟩
- **Dominios**: GENETICA 38 (100%) núcleo ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ninguno del vocabulario; sin instrumento reconocido: 38 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ninguno ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4**: ningún dominio del carril tiene filas en el catálogo ⟨F2⟩
- **Reglas del report** (3; encabezados excluidos 0): SIN-CIFRA-GEN2 3; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: ningún RESULT de sus instrumentos o núcleo ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 4 / 22 / 8 / 9): EN-MAIN · recibo pr-1251 · regla adoptada: No acreditada aquí · reserva material: 9 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · SIN-UNION 34 ⟨F1 F5 F6⟩
- **Stoppers** (1): ⟨F1 F5 F6⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 34 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-GENETICA / ASTRA5-MESA-DOCUMENTAL ×34 ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [ADQUISICION]: `SIN-UNION` → propietario en el mapa: ASTRA5-MESA-GENETICA / ASTRA5-MESA-DOCUMENTAL ×34 ⟨F1 F5 F6⟩

##### ⚪ CARRIL-16 · Mexican Population Genomics · 2025-2026 Scientific and Market Opportunity Update ⟨F1 F14⟩

- **Semáforo GRIS** — dominio GENOMICA fuera por firewall genético ⟨F1 F2 F3 S⟩
- **Afirmaciones 33**: medible en corpus 0 · con adquisición 26 · no medible por diseño 6 · no construible 1; citan un CALC/RESULT en `gen2_existente`: 0 ⟨F1⟩
- **Dominios**: GENOMICA 33 (100%) núcleo ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): MCPS 2 · PEW 1; sin instrumento reconocido: 30 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): MCPS 2 · PEW 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4**: ningún dominio del carril tiene filas en el catálogo ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 44 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 2 / 14 / 4 / 15): EN-MAIN · recibo pr-1251 · regla adoptada: No acreditada aquí · reserva material: 15 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): COLA-PENDIENTE 2 · SIN-UNION 24 ⟨F1 F5 F6⟩
- **Stoppers** (4): ⟨F1 F5 F6 F7⟩
  - **FIRMA** (2) ⟨F7⟩
    - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` (por MCPS) — Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩
    - `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` (por MCPS) — [E1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS → mesa firma (plazo 2026-09-29); encargo 2026-09-27-GEN2-TRAMITE-NC-DECISIONES-1.md ⟨F7⟩
  - **ADQUISICION** (2) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 24 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-GENOMICA ×11, ASTRA5-MESA-LEGAL ×6, ASTRA5-MESA-MERCADO ×4 ⟨F1 F5 F6⟩
    - `MCPS_SIN-OLA` — estado NO-ACCESIBLE; prioridad 3; afirmaciones 2; origen ASTRA5-U0 ASTRA5-U0-GENBEH-010 → mesa con identidad (acceso/registro) ⟨F1 F5 F6⟩
- **Frente 2027**: SIN-UNION (ningún instrumento citado es de una familia 2027) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` → mesa firma (plazo 2026-09-29); encargo 2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md ⟨F7⟩

##### ⚪ CARRIL-30 · Sanción Social Horizontal en México · Chisme · Envidia y Mal de Ojo como Mecanismos de Nivelación ⟨F1 F14⟩

- **Semáforo GRIS** — NO-MEDIBLE-POR-DISEÑO 64% > 50% ⟨F1 F2 F3 S⟩
- **Afirmaciones 22**: medible en corpus 3 · con adquisición 5 · no medible por diseño 14 · no construible 0; citan un CALC/RESULT en `gen2_existente`: 3 ⟨F1⟩
- **Dominios**: SANCION_SOCIAL 11 (50%) núcleo · INTERACCION 2 (9%) · TRABAJO 2 (9%) · CONFIANZA 1 (5%) · DINERO 1 (5%) · GENERO 1 (5%) · JUVENTUD 1 (5%) · MIGRACION 1 (5%) · RURAL_INDIGENA 1 (5%) · VIOLENCIA 1 (5%) ⟨F1 S⟩
- **Instrumentos citados** (afirmaciones): ENADID 1 · ENSU 1 · ENVE 1 · ENVIPE 1 · LATINOBAROMETRO 1 · MOCIBA 1; sin instrumento reconocido: 16 ⟨F1 F12 S⟩
- **Instrumentos del núcleo** (casan stoppers y validación): ENSU 1 · ENVE 1 · MOCIBA 1 ⟨F1 F12 S⟩
- **Cifras del catálogo v1.4 por dominio** (adoptadas · con reserva de ancho · suspendidas · acotadas en validación ciega) ⟨F2⟩
  - SANCION_SOCIAL (núcleo): 0 · 9 · 0 · 0 — por instrumento (* = el carril lo cita): ENSU* 9 ⟨F2⟩
  - dominios secundarios con cifra (adoptadas + con reserva de ancho): CONFIANZA 2007 · DINERO 124 · GENERO 7304 · MIGRACION 126 · RURAL_INDIGENA 77 · TRABAJO 26409 · VIOLENCIA 12805 ⟨F2⟩
- **Reglas del report** (2; encabezados excluidos 0): SIN-CIFRA-GEN2 2; con dictamen distinto de SIN-CIFRA-GEN2 0% ⟨F3⟩
- **Validación ciega**: CONCUERDA-NO-APROBADA 12105 · NO-PASA 525 · PASA 4 ⟨F10 F2⟩
- **Editorial v2** (C/M/R/S 1 / 11 / 0 / 18): EN-MAIN · recibo pr-1243 · regla adoptada: No acreditada aquí · reserva material: 18 registros SIN-CIFRA; ver razones y límites en tabla. Módulo [v2.16] y firewall: bloque C3-V216 del report. ⟨F4⟩
- **Adquisición del carril** (afirmaciones con adquisición): EN-MANIFIESTO 1 · SIN-UNION 4 ⟨F1 F5 F6⟩
- **Stoppers** (3): ⟨F1 F5 F6 F7 F8⟩
  - **FIRMA** (1) ⟨F7⟩
    - `FP-260928-GEN2-PENDIENTES-4-12d9-10` (por MOCIBA) — [D12 · Familia F6 (transferencia de M): retirar o reactivar] Opciones: (a) Retirar F6 por decisión de mesa: NC → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩
  - **ADQUISICION** (1) ⟨F1 F5 F6⟩
    - `SIN-UNION` — afirmaciones 4 sin instrumento del vocabulario → propietario en el mapa: ASTRA5-MESA-RURAL ×2, ASTRA5-MESA-ESTATUS ×1, ASTRA5-MESA-INTERACCION ×1 ⟨F1 F5 F6⟩
  - **NC-PARO** (1) ⟨F8⟩
    - `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` (por ENSU) — PARO-PREMISA · P3 → MESA-ACCION (2026-10-05) · antes: FP-260928-GEN2-VALIDACION-Y-2027-1-f926-04 ⟨F8⟩
- **Actos en vuelo** (sin CONSUMIDO, por nombre): `2026-09-16-GEN2-MOCIBA-FLUJO-DOCUMENTAL-1.md` ⟨F13⟩
- **Frente 2027**: ENSU-CAMPECHE-INSEGURIDAD (NO-LANZAR-TODAVIA; gate CONTRATO-FIRMADO(contrato nuevo; potencia insuficiente banda 5pp)+FIRMA-DE-MESA() · ENVIPE-DENUNCIA-U4 (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) · ENVIPE-EVASION-NORMA (LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA; gate DATO-2027-AUSENTE) ⟨F11⟩
- **Siguiente acción** [FIRMA]: `FP-260928-GEN2-PENDIENTES-4-12d9-10` → mesa firma; encargo 2026-09-28-GEN2-PENDIENTES-4.md ⟨F7⟩

#### Cadena de procedencia

Todo número de arriba sale de estos archivos por `python3 tools/tablero_carriles.py --json`; «blob» es el `git hash-object` del contenido leído (la salida no depende de HEAD ni de la fecha). El crosswalk F14 se escribe con `--crosswalk` y `--verifica` lo compara.

| clave | archivo | blob | lector | filas leídas |
|---|---|---|---|---:|
| F1 | `canon/mapa-dominios-v1_2.tsv` | `14210b7f869a` | lee_tsv (csv.DictReader), filas con report corpus/reports/* | 1396 |
| F2 | `canon/catalogo-del-mexicano-v1_4.tsv` | `58fc05037173` | lee_tsv, agrega por (dominio, instrumento, estado_adopcion) | 65480 |
| F3 | `canon/reglas-contrastadas-v1_2.tsv` | `69d9c19b267d` | lee_tsv, report = basename(fuentes) | 162 |
| F4 | `corpus/reports-v2/INDICE.md` | `cf3d1a1fa04d` | indice(): filas de la tabla markdown | 31 |
| F5 | `data/cola-adquisicion-v1_0.tsv` | `e96592d42f57` | lee_tsv (salta líneas #) | 952 |
| F6 | `data/manifiesto.yaml` | `d8ac4943b224` | manifiesto(): campos id y estado_reserva por línea | 7198 |
| F7 | `forense/firmas-pendientes.tsv` | `be51c3cb1bc7` | lee_tsv, estado ABIERTA* | 678 |
| F8 | `forense/no-corrido.tsv` | `ffdaf1817da3` | lee_tsv, estado ABIERTA*, razón PARO-PREMISA*/PARO-ENTORNO* | 1103 |
| F9 | `data/corrida0/demanda-dictamen-v1_0.tsv` | `59ab68b09e08` | lee_tsv, dictamen SIN-BASE-GEN2 / ESPERA-* | 341 |
| F10 | `data/corrida0/validaciones-independientes.tsv` | `2864d908be14` | lee_tsv, join resultado_id → catálogo.result_id | 21282 |
| F11 | `forense/analisis/familias-2027/familias-2027-estado-v1_2.tsv` | `871c4dfe05cd` | lee_tsv | 8 |
| F12 | `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` | `4a647dd37503` | lee_tsv, programa y olas_reservadas_al_entrar | 146 |
| F13 | `forense/encargos/*.md` | `e187a602071e (lista)` | glob; en vuelo = sin línea «## CONSUMIDO» | 820 |
| F15 | `data/corrida0/aperturas-pendientes-v1_0.tsv` | `4c7f99590390` | lee_tsv, (programa, año de ola) -> expediente y qué la abre | — |
| F16 | `forense/analisis/*/*dictamenes.tsv` | `0abe6bf6c772 (lista)` | pisos_pendientes(): glob; filas con dominio · calc · resultado_id | 90 |
| F17 | `data/corrida0/resultados.tsv` | `46e376c11e08` | pisos_pendientes(): conjunto de resultado_id registrados (salta líneas #) | — |
| F14 | `canon/crosswalk-carriles-v1_0.tsv` | `77878ff2f4d5` | crosswalk() (misma derivación; --verifica compara con el archivo) | 31 |
| S | `tools/tablero_carriles.py` | `cebf99425a43` | constantes de la cabecera | — |
<!-- TABLERO-UNICO:CARRILES:END -->

## Pendientes del programa — de quién es cada cosa

<!-- TABLERO-UNICO:PENDIENTES:BEGIN -->
_Derivado con `python3 tools/nc_por_clase.py --json` (`derivar()`, que no escribe) y `forense/firmas-pendientes.tsv`; universo de la deuda: 283 filas ABIERTA de 1103 en forense/no-corrido.tsv. La clase de cada fila es la del clasificador, sin reinterpretar. No toca el libro ni cierra nada. Este bloque sustituye al inventario `PENDIENTES-PROGRAMA` que ya no se publica aparte._

#### P.1 · Firmas de mesa abiertas: 41

Ordenadas por plazo y después por cuántos carriles frenan. «Vence» se compara con la fecha del commit del corte (2026-09-29). Solo cuentan como freno las firmas que gatean un instrumento, una ola o un payload del núcleo (una firma sobre el aparato no frena ningún carril).

| firma | qué se firma | plazo | carriles que frena | creada |
|---|---|---|---|---|
| `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | Acceso con solicitud o términos para seis objetos (EMOVI 2023/2011 CEEY, WVS ola 7 EE.UU./Japón y longitudinal, IFPS México, MCPS). Recomendación: el… | **2026-09-29 · vence** | 03, 05, 16, 18, 20 | 2026-09-24 |
| `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-12` | [E·1] 6 fuentes de microdato (EMOVI 2023/2011 de CEEY, WVS ola 7 EE.UU./Japón, WVS longitudinal 1981-2022, IFPS México 2020-2021, MCPS) siguen bloque… | **2026-09-29 · vence** | 03, 05, 16, 18, 20 | 2026-09-27 |
| `FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` | Destino del respaldo del corpus (P3 del encargo, §2): disco externo que mesa conecte (recomendada) · nube de mesa cifrada · las dos. El 21/sep mesa c… | **2026-09-29 · vence** | — | 2026-09-21 |
| `FP-260923-GEN2-FRONT-1-4296-01` | Activar GitHub Pages desde main/docs y decidir DOI Zenodo cuando el frente sea fusionado / NOTA (ADENDA-2 de GEN2-TRAMITE-FIRMAS-14, direccion, 23/se… | **2026-09-29 · vence** | — | 2026-09-23 |
| `FP-260926-GEN2-FRONT-3-PORTADA-1-8914-03` | Aplicar metadatos del repo (descripción, topics, homepage) y subir docs/assets/social-preview.png como vista previa social; receta de un minuto en la… | **2026-09-29 · vence** | — | 2026-09-26 |
| `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-20` | [F2] El respaldo del corpus (19.8 GB, 1914 archivos, restauración VERDE) sigue en el MISMO disco físico que el corpus (/home/pc0/mm-respaldo-corpus/2… | **2026-09-29 · vence** | — | 2026-09-27 |
| `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-26` | [H3] El respaldo del corpus fuera de sitio sigue pendiente de que mesa reformatee un disco duro propio; la fecha límite fijada por mesa el 23/sep ('e… | **2026-09-29 · vence** | — | 2026-09-27 |
| `FP-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01` | Pegar instrucciones v2.17 en el proyecto de Claude (bloque de gobierno/PEGAR-EN-PROYECTO-v2_17.md) y PLANTILLA-ENCARGO-v2_2 en el conocimiento; conte… | **2026-09-29 · vence** | — | 2026-09-28 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-16` | [D18 · Latinobarómetro 2024: levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de Latinobarómetro 2024 solo para HUM-006… | — | 03, 05, 13, 18, 20, 26 | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-09` | [D11 · ENVIPE 2026: leer sus documentos de instrumento sin abrir microdato] Opciones: (a) Confirmar para ENVIPE 2026 el mismo alcance de lectura que… | — | 02, 05, 07, 19, 20 | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-19` | [D21 · ENADID 2023 y Pew GAS Spring 2025: ¿reservadas?] Opciones: (A) Reservarlas por escrito (fila reserva:* en decisiones.tsv + estado_reserva en e… | — | 10, 12, 22, 25, 31 | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-22` | [D24 · Anexo A del lote ENIF 2024 archivado con otro sha256] Opciones: (a) Mesa aporta el Anexo A original byte a byte (si lo conserva); un acto NUBE… | — | 04, 08, 23 | 2026-09-29 |
| `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` | ACOTAR RESULT-ENDIREH2016-PF-TABLA#4 y #50 (edad 60+, vida y desde oct-2015) en catálogo v1.4 con rótulo «60+ incluye EDAD=98 (edad no especificada,… | — | 10, 26 | 2026-09-28 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-03` | [D1 · Régimen de aislamiento de la sesión ciega de C1 (767 identidades ENDIREH 2021)] Opciones: (a) Extender R32 a la sesión de las 767 con la receta… | — | 10, 26 | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-05` | [D4 · Publicabilidad frágil de 10 celdas ENDIREH del lote 1] Opciones: (a) Dejar las 10 en ACOTADA de forma permanente, sin regla nueva · (b) Firmar… | — | 10, 26 | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-11` | [D13 · Firma de contenido de los sucesores ENDIREH 2006 y 2016] Opciones: (A) Firmar por separado las tres líneas del dictamen: (1) ENDIREH2006-PAREJ… | — | 10, 26 | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-07` | [D8 · EDER 2025 (JUV-001/002): levantar la reserva E.6] Opciones: (A) Mesa levanta por escrito la reserva E.6 de EDER 2025 solo para JUV-001/002 (col… | — | 22 | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-10` | [D12 · Familia F6 (transferencia de M): retirar o reactivar] Opciones: (a) Retirar F6 por decisión de mesa: NC-0161 y NC-0162 pasan a CERRADA con cit… | — | 30 | 2026-09-29 |
| `FP-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01` | Margen de equivalencia y control simultáneo para IC reimplementados de C1 (R23: «se fijarán por mesa antes del siguiente conjunto sin revelar»). Opci… | — | — | 2026-09-28 |
| `FP-260928-GEN2-CIERRE-Y-PRODUCTO-3-3c2e-01` | ADOPCION POR BLOQUE (merge) de las cifras del catálogo v1.4: 16 CALC sellados el 27–28/sep, propuesta por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO… | — | — | 2026-09-28 |
| `FP-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01` | qué tope de sesiones pesadas de caja rige ahora que existe la caché Parquet: (a) 3 con patrón CSV y hasta 6 en total si las adicionales declaran tool… | — | — | 2026-09-28 |
| `FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-01` | [B1] dinero.ahorro.tiene_ahorros (RES-0029/0030): usa la ola 3 de ENNViH, hoy reservada; recomendación (a) HISTÓRICO-SIN-RELEVO como sus celdas (FP-3… | — | — | 2026-09-28 |
| `FP-260928-GEN2-DEMANDA-DICTAMEN-1-c133-02` | [B2] M·03 (gobierno digital coercitivo) dictaminado SIN-ESTIMANDO-RECONSTRUIBLE contra la regla del encargo (AJUSTE sin RESULT → DECIDIBLE); recomend… | — | — | 2026-09-28 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-04` | [D2 · Contratos nuevos de C1: escolaridad NIV-terminal-v1 y P14_22_14] Opciones: (a) Firmar por bloque NIV-terminal-v1 y P14_22_14 como contrato NUEV… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-06` | [D6 · ITER del Censo 2020: levantar la reserva E.6] Opciones: (A) Levantar por escrito la reserva completa del Censo 2020 ITER, volver a congelar el… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-08` | [D9 · ENCO (ahorro percibido): medir P10 y aceptar un puente] Opciones: (a) Autorizar las tres piezas: medición descriptiva de P10, puente con dinero… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-12` | [D14 · G1-B: partir resultados.tsv ya sin objeto] Opciones: (a) Retirar G1-B como SIN-OBJETO, citando el tamaño de hoy y la guarda de 50 MB; si la gu… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-13` | [D15 · Guarda 4.1: relevo de champion compuesto que ingiere resultados ajenos] Opciones: (a) Firmar un criterio nuevo para champions compuestos: se p… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-14` | [D16 · Solicitud de microdato ENCRIGE 2020 al Laboratorio de INEGI] Opciones: (a) Solicitar al Laboratorio de Microdatos de INEGI (procesamiento remo… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-15` | [D17 · Legado explícito de RESULT-L8CONV en tramite.yaml] Opciones: (a) Citar RESULT-L8CONV-A-P-MINIMO, -MAXIMO y -MEDIA en milpa/tramite.yaml como l… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-17` | [D19 · M·12, M·14, M·15, M·16 y M·17: fecharlos o dejarlos sin fecha (R08 b)] Opciones: (a) Mantener «sin fecha» (R08 b) como estado estable: la NC s… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-18` | [D20 · Cuarta condición del bin 1 de la regla de adopción en bloque] Opciones: (a) Sellar la 4ª condición del bin 1: «(iv) ningún sellado ni firma vi… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-20` | [D22 · Adendas de mesa sin rastro (19–21/sep): archivo retroactivo] Opciones: (a) Mantener la firma: el texto no se archiva. El hueco queda escrito e… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-21` | [D23 · Sidecar del insumo codex que cita un archivo ausente] Opciones: (a) Quien envió la rama codex re-envía el paquete con la cita corregida; entra… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-23` | [D25 · Envoltura por celda de emite_m.py (regla de ola previa estricta)] Opciones: (a) No cablear: las dos funciones quedan puras y probadas; NC-0026… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PENDIENTES-4-12d9-24` | [D26 · [COLA] y [ADQ]: ¿categoría exenta o excepción rotulada aparte?] Opciones: (a) Mantenerlas como EXCEPCIÓN EXPLÍCITA rotulada aparte, sin tocar… | — | — | 2026-09-29 |
| `FP-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-01` | [P2 · F4] Ratificar la INTERPRETACIÓN-DECLARADA de «congele el marcador-segmento vigente»: la constancia de CALC-PISO-PERSISTENCIA-ERROR-0002 es el m… | — | — | 2026-09-28 |
| `FP-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-02` | [P3 · F3 3(a) literal] ¿Se añade reserva_respondentes a RAICES_ESCANEABLES (tests/manifiesto.py:358) y a raices.local.yaml de cada caja, para que man… | — | — | 2026-09-28 |
| `FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01` | Bloque candidato de adopción de reglas SI-ENTONCES (adoptar el bloque · adoptar por dominio · esperar cruces) | — | — | 2026-09-28 |
| `FP-260928-GEN2-TUBERIA-3-f18c-01` | P4 · el [deriva] no se fusiona solo: (a) automerge-rutinas.yml gana schedule (cada 15 min) que fusiona PR derivados/auto-* con su último SHA verde y… | — | — | 2026-09-28 |
| `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | §5-bis · regla del semáforo de tools/tablero_carriles.py (GEN2-TUBERIA-TABLERO-INSUMOS-1; dirección propone, mesa decide). SIN-UNION cuenta como stop… | — | — | 2026-09-29 |

#### P.2 · Deuda abierta por dueño: 283 filas

| dueño | filas | qué la mueve |
|---|---:|---|
| MESA-DECISION | 42 | mesa elige una opción de la hoja de decisiones |
| MESA-ACCION | 41 | mesa hace algo con su identidad (acceso, envío, recibo) |
| DIRECCION-ENCARGO | 152 | dirección revisa y lanza un encargo ya redactado |
| CANAL | 23 | que se fusione el `[deriva]` en cola |
| APERTURA | 17 | que se abra una ola reservada (pre-registro o mesa por escrito, E.6) |
| ADQUISICION | 7 | que llegue el payload que nombra la solicitud |
| CAJA | 1 | que caja corra un encargo ya archivado |
| **total** | **283** | |

#### P.3 · El detalle, fila por fila, por dueño

**MESA-DECISION · 42**

| id | pieza | qué le falta | evidencia derivada |
|---|---|---|---|
| `NC-0026` | ADENDA precision 1 -- la envoltura por celda de tools/emite_m.py que consuma la regla de ola previa… | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D25) | — |
| `NC-0161` | Fase 4 B -- Transferencia o generalizacion de M | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D12) | — |
| `NC-0162` | Evaluacion de un M renovado | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D12) | — |
| `NC-0170` | P3 (censo de fichaje) | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D26) | — |
| `NC-0253` | P1/NC-0243 resto -- bin 1 de RES-0050/0051/0052 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D17) | — |
| `NC-0290` | P2(c) -- pasos 2 y 3 de la tabla de propagacion de la regla de adopcion en bloque | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D20) | — |
| `NC-0318` | GEN2-ENCO-DOS-OLAS-RESERVADAS-1 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D9) | — |
| `NC-0324` | GEN2-MOCIBA-FLUJO-DOCUMENTAL-1 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D12) | — |
| `NC-260921-GEN2-ADQUIERE-ENVIPE2026-ENIGH2024-1-dd08-01` | P2/P3 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D11) | — |
| `NC-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-04` | P0 · el sha256 declarado del Anexo A | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D24) | — |
| `NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-01` | P-h · Huérfano dentro del universo — el sello del insumo codex cita un objetivo que no está junto a… | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D23) | — |
| `NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-02` | P-g · Adendas del 19 al 21/sep cuyo texto el repo no guarda | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D22) | — |
| `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-09` | P2 relevo por lectura | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D5) | — |
| `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-10` | P2 relevo por lectura | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D5) | — |
| `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-15` | P2 relevo por lectura | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D10) | — |
| `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-16` | P2 relevo por lectura | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D10) | — |
| `NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-07` | ola más reciente **reservada** (E.6) | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D21) | — |
| `NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-06` | P5 residuo celdas_D | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D15) | — |
| `NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-07` | P5 residuo celdas_D | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D15) | — |
| `NC-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-03` | P3/P4 · Aislamiento antes de ejecución futura | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D1) | — |
| `NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02` | P2 · Decisiones conceptuales | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D13) | — |
| `NC-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-03` | P3 · D-15 y contratos sucesores | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D2) | — |
| `NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-02` | P2 catálogo M·03 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D5) | — |
| `NC-260927-GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1-4b11-03` | P2 · confirmación en base | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D16) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-07` | P3 · publicabilidad | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D4) | — |
| `NC-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01` | P1 · PASA y contador | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D3) | — |
| `NC-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-04` | P2 · Reserva de aislamiento | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D1) | — |
| `NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-04` | P3 · IC | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D3) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-01` | M·12 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D19) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-02` | M·14 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D19) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-03` | M·15 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D19) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-04` | M·16 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D19) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-05` | M·17 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D19) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-09` | R03 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D16) | — |
| `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-01` | P1/P2 · pieza LATINOBAROMETRO (HUM-006, AUTOR-026) | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D18) | — |
| `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-02` | P1/P2 · pieza CPV2020-ITER (TIME-027, RURAL-026/027, FAM-037, AUTOR-021) | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D6) | — |
| `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-03` | P1 · EDER 2025 (JUV-001, JUV-002) | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D8) | — |
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-10` | P1 · ceguera v2 | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D1) | — |
| `NC-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-03` | P4 · criterio de CONFIRMA | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D7) | — |
| `NC-260928-GEN2-TUBERIA-Y-CURACION-1-247d-01` | P1 (G1-B) | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D14) | — |
| `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` | P5 · opción de auto-merge del [deriva] (FP f18c-01) | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D27) | — |
| `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-02` | §5-bis · regla del semáforo de tools/tablero_carriles.py | dueño MESA-DECISION (forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md#D28) | — |

**MESA-ACCION · 41**

| id | pieza | qué le falta | evidencia derivada |
|---|---|---|---|
| `NC-0056` | P1(c)/P1(d)/P2(a) | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0061` | P3 (timbre de tandas) + timbre OECD (P6 de ACTO GEN2-CIERRES-GRUPO-A) | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0111` | UNIVERSO | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0151` | D17 / FP-314 y accesos pendientes | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0153` | Fase 4 -- demanda de tasa general ENCIG | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0156` | VIA-OFICIAL-DE-VARIANZA | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0159` | Fase 3 -- acreditar el diseno completo para el uso inferencial | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0166` | EXPERIMENTO-MEXICANO-PAQUETE-REPRODUCIBLE | dueño MESA-ACCION (2026-10-05) | — |
| `NC-0278` | P1 -- las tres fuentes externas de Astra | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` | P3 -- «copia al destino de mesa; verificacion por hash en destino» | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-04` | IC predictivo calibrado y prueba de cambio entre olas | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260923-ASTRA5-U2-ENDIREH-6a2c-01` | ENDIREH 2003 pareja residente | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-01` | ENCUP: busca y verifica peso/diseño de la base 2012 en documentación existente | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260923-GEN2-CORPUS-RESPALDO-EJECUCION-1-a307-01` | P1-P4 (copia, verificacion, aplicar 4 propuestas de manifiesto, firma de FP -3d56-01) | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260923-GEN2-FRONT-1-4296-02` | PLAN-VISIBILIZACION | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260923-GEN2-TRAMITE-FIRMAS-14-9556-05` | P1·H | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260923-GEN2-TUBERIA-SELLO-EXTERNO-1-cfce-01` | P2(a)/P2(b) | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` | P3 · fuentes con solicitud, términos o comité: EMOVI 2023, EMOVI 2011, WVS ola 7 EE.UU./Japón, WVS… | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-03` | P3 · CONDUSEF REDECO, cortes anteriores a 30/09/2025 | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260924-GEN2-TUBERIA-TABLERO-EN-CANAL-1-3726-02` | P3: verificar que Pages sirve docs/tablero.md y docs/PROTOCOLO-TABLERO.md | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-03` | PEW *Religion in Latin America* | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260925-GEN2-CORPUS-COMPLETO-1-7813-02` | P2 / P4 | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-02` | [SUPUESTO] que EMIF (COLEF) se obtuvo; si no, `/adquiere` o NO-OBTENIDO con receta | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260926-GEN2-ASTRA6-C2-CIERRE-MATERIAL-1-ad01-02` | C2 | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01` | P5 · Calendario, atestación y hoja de firma | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260926-GEN2-ASTRA6-C2-ENVIPE-1-7045-01` | P5 | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260926-GEN2-ASTRA6-C3-TRABAJO-MOVILIDAD-1-ed83-03` | Movilidad / condicionamiento CEEY | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260926-GEN2-PRODUCTO-CONSULTA-1-dcde-01` | P3 página estática | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260926-GEN2-RECIBO-ASTRA6-N-996b-03` | #1172 · recibo | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260927-ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1-3a1f-01` | Recibo técnico y firma de contenido | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260927-GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1-4b11-01` | P1 · adjuntos | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-08` | P1 · ceguera | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260927-GEN2-TRAMITE-FIRMAS-20-96f9-02` | P3 · E (8914-03) | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260928-GEN2-ASTRA-CONTINUIDAD-C3-1-26bb-01` | P0 · transfer | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-01` | P2(iii) | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-04` | P2(iv) | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-06` | P3 | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-07` | P4 | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260928-GEN2-TRAMITE-INSTRUCCIONES-V217-1-3e59-01` | P4 · commit 2 | dueño MESA-ACCION (2026-09-29) | — |
| `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-03` | P3 | dueño MESA-ACCION (2026-10-05) | — |
| `NC-260929-GEN2-TUBERIA-TABLERO-UNICO-1-22ee-01` | P5 · asiento de FP-260928-GEN2-CIERRE-Y-PRODUCTO-3-3c2e-01 | dueño MESA-ACCION (2026-10-05) | — |

**DIRECCION-ENCARGO · 152**

| id | pieza | qué le falta | evidencia derivada |
|---|---|---|---|
| `NC-0037` | P3(c) -- las 10 filas VIVAS del cruce FP-343/FP-286 (HOMESCAN, PANEL_DE_COMPRA_DE_HOGARES, REGISTRO… | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-0048` | «P5 · delta -- la primera comparacion GEN2<->GEN1, despues de medir y por script (E.1)» | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-0055` | «B1 · Reemplazar el cuerpo curado por la version v2.3» | dueño DIRECCION-ENCARGO (GEN2-PRODUCTO-CANON-2) | — |
| `NC-0136` | P3 (hallazgo ampliado al contestar el gate D-14 de NC-0123) | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-0164` | N34 · producto/costo y dano del lado consumidor | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-0218` | incorpora el sello de D-A cuando exista, sin esperarlo | dueño DIRECCION-ENCARGO (GEN2-PRODUCTO-CANON-2) | — |
| `NC-0246` | consumo del overlay recuperado · ninguna celda ni CORR lo usa todavia | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-0260` | las 2368 filas irrecuperables por construccion siguen en el denominador de NC-0136 | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-0272` | A.8 -- el universo de declaraciones vencidas de M·1 | dueño DIRECCION-ENCARGO (GEN2-TRAMITE-ARCHIVO-2) | — |
| `NC-0285` | P1(b) -- registro de CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001, y su encargo fuera del directorio ca… | dueño DIRECCION-ENCARGO (GEN2-TRAMITE-ARCHIVO-2) | — |
| `NC-0287` | P1(a) -- forma de cierre del carril Codex | dueño DIRECCION-ENCARGO (GEN2-TRAMITE-ARCHIVO-2) | — |
| `NC-0292` | P1(d) -- defecto propio del generador de digesto, encontrado al regenerarlo | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-0298` | P2 -- NC nueva (aparato): `escala` se lee por REGLA, no por salida | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-0299` | P1 -- NC nueva (registro): las citas `origen:` del emisor al arbitro estan DESFASADAS | dueño DIRECCION-ENCARGO (GEN2-TRAMITE-ARCHIVO-2) | — |
| `NC-0303` | PERIMETRO -- los tres consumidores de CORTES_C1 que el sello desalinea, todos fuera de la lista | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-0307` | P2/COMMIT-2 -- «C3 ... con intervalo de 80 % declarado por L» (diseno v1.1 §2/§4) | dueño DIRECCION-ENCARGO (GEN2-CALC-ALTERNOS-LOTE-2) | — |
| `NC-0332` | P4/NC-0331 -- cablear tests/test_marginales_una_variable.py (15 casos) a .github/workflows/verify.y… | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-0339` | Cascada de gobernanza -- ADR-545, anotacion L0 y los tres contadores mecanicos de canon/estado-prog… | dueño DIRECCION-ENCARGO (GEN2-TRAMITE-ARCHIVO-2) | — |
| `NC-0346` | P4 | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-0381` | P1 -- cableado de tests/test_c2_ic_enif2024_guardia.py en CI | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-0385` | LO QUE NO HACE -- error de persistencia de estas 6 celdas (CALC nuevo, sucesor de CALC-PISO-PERSIST… | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-0395` | P3 -- causa raiz de los DOS usos legacy que aparecen solo despues de la adopcion | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-0396` | P1 -- censo, FALLA-DE-VERDAD | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-0398` | P1 -- censo, FALLA-DE-VERDAD | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-0403` | P1 -- censo, FALLA-DE-VERDAD | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-0413` | P1/P4 -- unidad | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-0418` | P5 · falsador | dueño DIRECCION-ENCARGO (GEN2-FALSADOR-PLANTILLA-V22-1) | — |
| `NC-0438` | Pieza 2, paso 3 — codigo de salida de `corrida0.py verify` | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-0439` | Perimetro de cierre permanente (D-21) · censo de CI regenerado por este acto | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-0448` | P3 (3D) — demanda declarada | dueño DIRECCION-ENCARGO (GEN2-CALC-ALTERNOS-LOTE-2) | — |
| `NC-0449` | perimetro de cierre -- enlace de la tabla de identidad de credito al marcador | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-0450` | CI · job guardias tras fusionar #942 | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260921-GEN2-ADQUIERE-ENVIPE2026-ENIGH2024-1-dd08-02` | P3 | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-03` | §10 sucesor · «leer la cobertura de la persistencia con n grande» | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-02` | P4 «todo id anulable declarado por lectura estática y, si corrida0 ensayo ya existe, también por he… | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260921-GEN2-DUELO-ENVIPE2026-COMMIT-1-8796-06` | `tests/test_duelo_prospectivo.py` cableado en CI. | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260921-GEN2-ENCIG-SERIE-Y-TENDENCIA-1-852f-02` | P3 -- insumo 2025 del origen movil (ADENDA-1 de mesa) | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-03` | Perímetro de cierre D-21 · el test del conducto en CI | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260921-GEN2-MARCADOR-E-INFORME-1-48d4-03` | P4 (ii) -- cobertura del IC95 por candidato, «por piloto y juntos» | dueño DIRECCION-ENCARGO (GEN2-PRODUCTO-CANON-2) | — |
| `NC-260921-GEN2-MARCADOR-E-INFORME-1-48d4-04` | P4 (ii) -- «con intervalo binomial» | dueño DIRECCION-ENCARGO (GEN2-PRODUCTO-CANON-2) | — |
| `NC-260921-GEN2-TUBERIA-CIERRE-RAPIDO-1-baca-02` | P-B | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260921-GEN2-TUBERIA-CIERRE-RAPIDO-1-baca-03` | P-C | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-02` | P3 · tests/check.py (lista unica de registro de tests) | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01` | §6 -- sucesor: que /revisa lea la clase del resumen en vez de deducirla | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02` | §9 · no arregla el chequeo 0.c de `acto.md` (queda en NC para dirección) | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-07` | careo GEN2-TUBERIA-CAREO-1 · P3 · falsabilidad 2 · censo de consumidores de ORDEN por id (en el exp… | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260921-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1-7ef3-01` | P2 -- IC de C2 celda por celda, pilotos 1 y 2 | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260921-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1-7ef3-03` | P3 -- precisión de spec del piloto 3 sobre el universo de los marginales de C2 | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-06` | Test propio en CI (tests/test_enif_persistencia_ic_calibrado.py) | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-02` | COMMIT-2 · los 21 marginales con IC; registro y asiento | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260922-GEN2-ENUT-NUCLEO-CELDAS-1-9f24-03` | P3 · enut-comparabilidad-texto-v1_0.tsv enmendado por (a) (fila C2×2019); marcador re-derivado por… | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260922-GEN2-LECTURAS-DE-MESA-Y-ROTULOS-1-7357-02` | P4 -- detalle por celda y ΔMAE/IC del backtest de credito 2021->2024 en el informe v1.2 §2.3 | dueño DIRECCION-ENCARGO (GEN2-PRODUCTO-CANON-2) | — |
| `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-02` | P2 · NC-0270: consecuencia de la confirmacion | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-04` | firma de mesa 22/sep sobre FP-260922-GEN2-PENDIENTES-CAJA-1-c09b-01, opcion (b) | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260922-GEN2-TRAMITE-COLA-VIEJA-1-0eca-02` | 14 archivos de cola/ sin CONSUMIDO fuera de la tabla PENDIENTES-PROGRAMA §4.1 | dueño DIRECCION-ENCARGO (GEN2-TRAMITE-ARCHIVO-2) | — |
| `NC-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-02` | criterio de hecho: grep -c PENDIENTE-DE-MESA data/corrida0/corridas.tsv menor en exactamente 4 | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-02` | transición individual formal/informal | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-03` | cuidados específicos e ingreso real | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260923-ASTRA5-U2-ENDIREH-6a2c-02` | Serie temporal ENDIREH 2006-2021 | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260923-ASTRA5-U2-ENDIREH-6a2c-03` | Agregado U0 70.1 por cualquier violencia | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-02` | INE: dicta los objetos restantes pertinentes al encargo | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-03` | INE: dicta los objetos restantes pertinentes al encargo | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260923-GEN2-ASTRA-ENVIPE-ADJUDICACION-1-970c-01` | P0/P1/P2 (spec en dos capas, cuatro corridas, nota) -- el encargo entero | dueño DIRECCION-ENCARGO (GEN2-REPLAYS-Y-RECIBOS-CAJA-1) | — |
| `NC-260923-GEN2-AUDITORIA-POST-HOC-ASTRA-1-39d2-03` | P3 -- corroboracion externa en el anexo | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-01` | P1 | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260923-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-c6f4-02` | P3 | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260924-ASTRA5-U0-MAPA-DOMINIOS-63db-02` | diez contratos con RESULT sellado que mide exactamente su componente (ENOE-001..003, TEC-001/005/00… | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-04` | catalogación de los 782 payloads nuevos (inventario de reactivos y de FD); mesa eligió en la sesión… | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-05` | P4 · 14 NO-ACCESIBLE, 41 NO-ENCONTRADO y 14 EXISTE-NO-SATISFACE desde caja | dueño DIRECCION-ENCARGO (GEN2-PRODUCTO-CANON-2) | — |
| `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-06` | P1 · constancias: 16 NO-ENCONTRADO, ENIGH 2024 (ola reservada) y copias no conservadas en el repo | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-260924-GEN2-CLASE-AMAI-1-e773-03` | ENDUTIH 2023–2025: actividad_empleo | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-02` | P3: series ENDIREH dictaminables | dueño DIRECCION-ENCARGO (GEN2-MARCADOR-Y-SERIES-2) | — |
| `NC-260924-GEN2-ENCIG-PISOS-GEN2-1-19a3-02` | el resolvedor de linaje (`tools/corrida0.py::_propaga_envuelto`) no ve números tecleados en `parame… | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |
| `NC-260924-GEN2-ENCIG-PISOS-GEN2-1-19a3-06` | `tests/test_encig_pisos_gen2.py` en CI | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260924-GEN2-PISOS-GEN2-2-2518-04` | D-22 en CI | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-17` | P2 relevo por lectura | dueño DIRECCION-ENCARGO (GEN2-RELEVO-TRAMITE-CAJA-2) | — |
| `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-18` | P2 relevo por lectura | dueño DIRECCION-ENCARGO (GEN2-RELEVO-TRAMITE-CAJA-2) | — |
| `NC-260924-GEN2-RELEVO-MOTOR-34-1-a157-19` | P2 relevo por lectura | dueño DIRECCION-ENCARGO (GEN2-RELEVO-TRAMITE-CAJA-2) | — |
| `NC-260924-GEN2-REPLAY-NO-VERIFICADOS-1-822a-03` | «Hecho»: `corridas.tsv` (en el siguiente `[deriva]`) sin `NO-VERIFICADO` para esos seis ids. | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-02` | microdato ENSANUT (2018, 2020 continua, 2021, 2022, 2023 …) | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-03` | (P1) … las afirmaciones de esos dominios con dictamen MEDIBLE | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260925-GEN2-CATALOGO-V1-1-1-afe1-02` | P3 · MEDIBLE-CON-ADQUISICIÓN | dueño DIRECCION-ENCARGO (GEN2-PRODUCTO-CANON-2) | — |
| `NC-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-07` | LAPOP … (módulo EXC) | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-03` | segmentación (sexo, edad, escolaridad, localidad, formalidad, región, NSE donde A4 lo autorizó) | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-05` | P3 pisos por segmento con IC de diseño (control externo de la spec §5) | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-10` | test D-22 (tests/test_consumo_pisos_gen2.py) | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260925-GEN2-CORPUS-COMPLETO-1-7813-01` | §1 «Hecho» / CONTADOR | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260925-GEN2-CORPUS-COMPLETO-1-7813-03` | P2 · E.6 | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-03` | fecundidad deseada vs observada | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260925-GEN2-MAPA-DOMINIOS-V1-1-1-3cf7-01` | P2 | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-10` | P5 residuo catalogo_de_momentos | dueño DIRECCION-ENCARGO (GEN2-RELEVO-TRAMITE-CAJA-2) | — |
| `NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-01` | P1 · Resolver por componente y materialidad | dueño DIRECCION-ENCARGO (GEN2-TRAMITE-ARCHIVO-2) | — |
| `NC-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-03` | P3 · Aperturas precisas y herramienta terminada | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-02` | P2 · Once decisiones de publicabilidad | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260926-GEN2-ASTRA6-C2-CIERRE-MATERIAL-1-ad01-04` | C2 | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260926-GEN2-ASTRA6-C2-ENVIPE-1-7045-02` | P5 | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-260926-GEN2-ASTRA6-C3-CONSUMO-FAMILIA-2-9d28-01` | Nuevo recibo técnico independiente de Claude | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260926-GEN2-ASTRA6-C3-CONSUMO-FAMILIA-2-9d28-02` | Validación numérica independiente de RESULT | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260926-GEN2-ASTRA6-C3-CONSUMO-FAMILIA-2-9d28-03` | Coeficientes y cifras históricas externas retiradas del v1 sin fuente efectivamente accesible | dueño DIRECCION-ENCARGO (GEN2-REPLAYS-Y-RECIBOS-CAJA-1) | — |
| `NC-260926-GEN2-ASTRA6-C3-TRABAJO-MOVILIDAD-1-ed83-01` | Revisión humana y recibo externo | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260926-GEN2-CIERRE-SEMANAL-1-dea2-03` | «la columna de oferta de DINERO-SERIES junto a cada piso de crédito/ahorro» | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260926-GEN2-COLA-COMPLETA-1-0d4a-02` | (a) las ~30 filas restantes … FAMILIA/ENOE … pisos por segmento | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260926-GEN2-COLA-COMPLETA-1-0d4a-03` | (b) las 135 afirmaciones NO-VERIFICADO-AQUÍ … texto de pregunta contra cuestionario/FD | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260926-GEN2-COLA-COMPLETA-1-0d4a-04` | (a) RELIGIOSIDAD/CCPV | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260926-GEN2-COLA-LOTE-1-3a49-02` | La verificación de texto se asienta en `forense/analisis/dominios/verificaciones-texto-v1_1.tsv` …… | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260926-GEN2-COLA-LOTE-1-3a49-03` | P-EMAT / P-EDR: conductas por texto (tasas que citan PAREJA-002, FAM-023, JUV-011, SALMEN-015/016) | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260926-GEN2-COLA-LOTE-1-3a49-06` | test D-22 (tests/test_cola_lote_1_pisos.py) | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260926-GEN2-DINERO-SERIES-CNBV-BANXICO-1-8dbe-01` | P2 · constancias CNBV (R16 por institución e IMORA; boletín SOFIPO; BDIF) | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260926-GEN2-DINERO-SERIES-CNBV-BANXICO-1-8dbe-02` | P2 · constancias Banxico (SIE CF297, RIB tarjetas y personales) | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260926-GEN2-DINERO-SERIES-CNBV-BANXICO-1-8dbe-03` | P4 · columna de oferta | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260926-GEN2-RECIBO-ASTRA6-N-996b-08` | corrida0 verify | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-03` | P2 catálogo M·05, M·23 | dueño DIRECCION-ENCARGO (GEN2-RELEVO-TRAMITE-CAJA-2) | — |
| `NC-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-02` | serie 2013–2025 por conducta y ciudad | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-03` | nota CONFIRMA / MATIZA / ROMPE contra cada report | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-04` | serie 2013–2025 por conducta y ciudad | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260927-GEN2-CIERRE-SEMANAL-2-facd-02` | P1 | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-04` | P2 · 685 puntos | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-06` | P2 · 1 873 IC | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-05` | P1 · #1199 adjudicación de puntos | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-09` | P1 · #1203 reempaqueta ventana | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-11` | P1 · #1171 C3 social | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-13` | P1 · #1180 C3 género-violencia-salud | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-15` | P1 · #1196 C3 dinero-tecnología-conocimiento | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-17` | P1 · #1197 C3 cuidado-migración-pareja | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260927-GEN2-TUBERIA-CI-TIEMPO-1-c6d9-06` | COMMIT-cierre | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260928-GEN2-ASTRA-CONTINUIDAD-C3-1-26bb-03` | P3 · hoja de reglas | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-03` | ENTORNO · ENDIREH 2021 | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260928-GEN2-ASTRA6-C2-EJECUCION-1-e897-04` | D-21 · test propio en CI | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-01` | P1 · R28 re-comparación | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-02` | P2 · R25 sucesores | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-03` | P1 · ENBIARE escalas | dueño DIRECCION-ENCARGO (GEN2-C1-SUCESORES-2011-2021-1) | — |
| `NC-260928-GEN2-C1-SUCESORES-Y-LOTE-3-2385-06` | P2 · R33 CALC | dueño DIRECCION-ENCARGO (GEN2-RELEVO-TRAMITE-CAJA-2) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-07` | M·19 | dueño DIRECCION-ENCARGO (GEN2-CALC-ALTERNOS-LOTE-2) | — |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-08` | M13-p17p18 | dueño DIRECCION-ENCARGO (GEN2-CALC-ALTERNOS-LOTE-2) | — |
| `NC-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01` | P2 · ENIF 2024 | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-03` | Test en CI | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260928-GEN2-CORPUS-LICENCIAS-1-1997-02` | (i) registro de la página de términos INEGI | dueño DIRECCION-ENCARGO (GEN2-CURACION-CORPUS-2) | — |
| `NC-260928-GEN2-CORPUS-LICENCIAS-1-1997-03` | clave derivada en status | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260928-GEN2-DEMANDA-DICTAMEN-1-c133-02` | hallazgo 1 de la nota | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260928-GEN2-DEMANDA-DICTAMEN-1-c133-04` | §1 P1-P4 (63 RESULT que siguen pendientes) | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-08` | §5 | dueño DIRECCION-ENCARGO (GEN2-ADQUISICION-DOCUMENTAL-1) | — |
| `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-04` | P1 · TIME-001 (ENIF 2024), RURAL-041, SALMEN-032, TRAB-022, AUTOR-004 (WVS) | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-2) | — |
| `NC-260928-GEN2-PISOS-DOMINIOS-Y-REGLAS-1-7cd0-06` | P3 · RG-7c6dd83a03 | dueño DIRECCION-ENCARGO (GEN2-PISOS-DOMINIOS-Y-REGLAS-3) | — |
| `NC-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-03` | P3 · F3 3(a) literal | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-05` | P1 · esquema | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-06` | P2 · trazabilidad | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-08` | P1 · muestra | dueño DIRECCION-ENCARGO (GEN2-REPLAYS-Y-RECIBOS-CAJA-1) | — |
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-12` | P1 · archivo 01 | dueño DIRECCION-ENCARGO (GEN2-CORRECCION-C3-1) | — |
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-13` | P1 · replay oro | dueño DIRECCION-ENCARGO (GEN2-REPLAYS-Y-RECIBOS-CAJA-1) | — |
| `NC-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-03` | P1 · re-censo de tests | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1) | — |
| `NC-260928-GEN2-TUBERIA-3-f18c-01` | P4 | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-CORRIDA0-2) | — |
| `NC-260928-GEN2-TUBERIA-Y-CURACION-1-247d-02` | P6 (F1-a), mitad -- test_01/test_01b | dueño DIRECCION-ENCARGO (GEN2-TUBERIA-TESTS-Y-CHECK-2) | — |

**CANAL · 23**

| id | pieza | qué le falta | evidencia derivada |
|---|---|---|---|
| `NC-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-04` | Sella el primer resultado y registra replay | dueño CANAL (derivados/auto-*) | — |
| `NC-260923-GEN2-CONTADORES-CONSUMO-2-749c-01` | P3 (canal completo): 16 celdas de GOB.gobierno_digital.encig2025.edad_x_sexo + .escolaridad_x_sexo | dueño CANAL (derivados/auto-*) | — |
| `NC-260924-GEN2-CONTADORES-CONSUMO-2-749c-03` | «Hecho» de §1: el siguiente PR derivados/auto-* publica el marcador | dueño CANAL (derivados/auto-*) | — |
| `NC-260924-GEN2-ENCIG-PISOS-GEN2-1-19a3-05` | E.7 | dueño CANAL (derivados/auto-*) | — |
| `NC-260924-GEN2-PISOS-GEN2-2-2518-01` | E.7 · vista publicada | dueño CANAL (derivados/auto-*) | — |
| `NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01` | «Hecho»: ≥ 3 CALC sellados … con `verify` REPRODUCE y asiento | dueño CANAL (derivados/auto-*) | — |
| `NC-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-01` | «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento | dueño CANAL (derivados/auto-*) | — |
| `NC-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-01` | «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento | dueño CANAL (derivados/auto-*) | — |
| `NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-01` | «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento | dueño CANAL (derivados/auto-*) | — |
| `NC-260926-GEN2-COLA-COMPLETA-1-0d4a-01` | «Hecho»: … mapa re-derivado · verify y asiento (E.7) | dueño CANAL (derivados/auto-*) | — |
| `NC-260926-GEN2-COLA-LOTE-1-3a49-01` | «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento | dueño CANAL (derivados/auto-*) | — |
| `NC-260926-GEN2-DINERO-SERIES-CNBV-BANXICO-1-8dbe-05` | publicación en la vista corridas/resultados.tsv | dueño CANAL (derivados/auto-*) | — |
| `NC-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-01` | «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento | dueño CANAL (derivados/auto-*) | — |
| `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-12` | P1 · #1171 C3 social | dueño CANAL (derivados/auto-*) | — |
| `NC-260927-GEN2-TUBERIA-CI-TIEMPO-2-a387-01` | P3 · drenaje | dueño CANAL (derivados/auto-*) | — |
| `NC-260927-GEN2-TUBERIA-RESUMEN-SUITE-1-6127-01` | P1 | dueño CANAL (derivados/auto-*) | — |
| `NC-260928-GEN2-ASTRA-CONTINUIDAD-C2-1-ba6c-02` | P1 · ENVIPE emisiones | dueño CANAL (derivados/auto-*) | — |
| `NC-260928-GEN2-PISOS-Y-ADENDAS-1-fa42-04` | E.7 · vista | dueño CANAL (derivados/auto-*) | — |
| `NC-260928-GEN2-RELEVO-TRAMITE-CAJA-1-e2f9-02` | «Hecho»: RESULT con sello.json y fila en la vista | dueño CANAL (derivados/auto-*) | — |
| `NC-260928-GEN2-TABLERO-CARRILES-1-e2eb-01` | «Hecho»: el canal lo publica | dueño CANAL (derivados/auto-*) | — |
| `NC-260928-GEN2-TUBERIA-3-f18c-04` | P1/P2/P3 · prueba de campo | dueño CANAL (derivados/auto-*) | — |
| `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-05` | P3 | dueño CANAL (derivados/auto-*) | — |
| `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-03` | P2 · resumen de la suite en main | dueño CANAL (derivados/auto-*) | — |

**APERTURA · 17**

| id | pieza | qué le falta | evidencia derivada |
|---|---|---|---|
| `NC-260922-GEN2-DUELO-ENVIPE2026-MARGINALES-2-0f2c-01` | civico.denuncia.con_seguro nacional | dueño APERTURA (ENVIPE 2026 · con_seguro nacional, firma pendiente) | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01` | 2026T1 última ola del corpus, ambas rutas ZIP | dueño APERTURA (ENOE 2026T1; FP: FP-260923-GEN2-TRAMITE-FIRMAS-12-9087-03) | FP-260923-GEN2-TRAMITE-FIRMAS-12-9087-03 [FIRMADA] |
| `NC-260923-ASTRA5-U4-TECNOLOGIA-1f30-01` | MOCIBA 2019 | dueño APERTURA (MOCIBA 2019, reserva confirmatoria R01-F6, letra 5; FP: FP-260928-GEN2-TRAMITE-PENDIENTES-2-3… | FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01 [FIRMADA] |
| `NC-260923-ASTRA5-U4-TECNOLOGIA-1f30-02` | MOCIBA 2020 | dueño APERTURA (MOCIBA 2020, reserva confirmatoria R01-F6, letra 5; FP: FP-260928-GEN2-TRAMITE-PENDIENTES-2-3… | FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01 [FIRMADA] |
| `NC-260923-ASTRA5-U4-TECNOLOGIA-1f30-03` | MOCIBA 2021 | dueño APERTURA (MOCIBA 2021, RESERVA-PILOTO-P12 de R01-F6, letra 5; FP: FP-260928-GEN2-TRAMITE-PENDIENTES-2-3… | FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01 [FIRMADA] |
| `NC-260923-ASTRA5-U4-TECNOLOGIA-1f30-04` | MOCIBA 2022 | dueño APERTURA (MOCIBA 2022, RESERVA-PILOTO-P12 de R01-F6, letra 5; FP: FP-260928-GEN2-TRAMITE-PENDIENTES-2-3… | FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01 [FIRMADA] |
| `NC-260923-ASTRA5-U4-TECNOLOGIA-1f30-05` | MOCIBA 2023 | dueño APERTURA (MOCIBA 2023, firma pendiente: acto futuro con permiso y delimitacion frente a TIC-10) | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260923-ASTRA5-U4-TECNOLOGIA-1f30-06` | MOCIBA 2024 | dueño APERTURA (MOCIBA 2024, TIC-11 y fase confirmatoria R01-F6, letra 5; FP: FP-260928-GEN2-TRAMITE-PENDIENT… | FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01 [FIRMADA] |
| `NC-260923-ASTRA5-U4-TECNOLOGIA-1f30-07` | MOCIBA 2025 | dueño APERTURA (MOCIBA 2025, reserva confirmatoria R01-F6, letra 5; FP: FP-260928-GEN2-TRAMITE-PENDIENTES-2-3… | FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01 [FIRMADA] |
| `NC-260925-GEN2-CONSUMO-Y-GASTO-PISOS-1-2d37-02` | ENGASTO 28 payloads | dueño APERTURA (ENGASTO 2013, firma pendiente; GEN2-CONSUMO-Y-GASTO-PISOS-2 no archivado) | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260926-GEN2-ASTRA6-C2-ENVIPE-1-7045-03` | P4 | dueño APERTURA (ENVIPE 2027, firma pendiente) | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-04` | P4 | dueño APERTURA (olas 2026/2027 de las familias frontera-1; FP: FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01) | FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01 [FIRMADA] |
| `NC-260926-GEN2-RECIBO-ASTRA6-N-996b-04` | #1174 · recibo | dueño APERTURA (ENIF 2027, COMMIT-3, firma pendiente) | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260928-GEN2-APERTURAS-PREREGISTRADAS-1-68b3-01` | P2 · «códigos por texto de pregunta del cuestionario de esa ola (permitido: cuestionario y FD sí se… | dueño APERTURA (los 17 expedientes de forense/prereg-aperturas: preflight documental en caja al abrir cada ol… | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260928-GEN2-CALC-ALTERNOS-LOTE-1-795b-06` | M·13 | dueño APERTURA (CSES módulo 5 MEX_2018, el más reciente del corpus: reservable por E.6, base no abierta, firm… | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-02` | P2 · olas reservadas | dueño APERTURA (envipe2026, enigh2024, endutih2025: firma pendiente; encrige2020: R02 FIRMADA, la abre su cod… | SIN-FP: el dueño no nombra la firma que abriría la ola |
| `NC-260928-GEN2-VALIDACION-Y-2027-1-f926-02` | P2 | dueño APERTURA (lote 4 de C1: ENIF 2024, ENUT 2024 y ENSANUT 2024; firma de apertura por módulo pendiente en… | SIN-FP: el dueño no nombra la firma que abriría la ola |

**ADQUISICION · 7**

| id | pieza | qué le falta | evidencia derivada |
|---|---|---|---|
| `NC-0258` | NC-0235, segunda mitad: adquisicion de los 55 grupos REQUIERE-FD-EN-CORPUS | dueño ADQUISICION (FD INEGI encig 2015-2025, 6 de 55 grupos REQUIERE-FD; A4/A5: OBTENIDO; solicitud: cola:ENC… | cola:ENCIG_2015 [OBTENIDO] · cola:ENCIG_2017 [OBTENIDO] · cola:ENCIG_2019 [OBTENIDO] · cola:ENCIG_2021 [OBTEN… |
| `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-02` | P3 · INEGI pobreza multidimensional 2024 (programas y bases), ENEM 2024, EQD panel 2018 | dueño ADQUISICION (INEGI MMP 2024, ENEM 2024 y EQD panel 2018; A4/A5: NO-OBTENIDO-POR-ESTE-AGENTE(4 intentos) | cola:INEGI-MMP_2024 [NO-OBTENIDO-POR-ESTE-AGENTE(4 intentos)] · cola:ENEM_2024 [NO-OBTENIDO-POR-ESTE-AGENTE(4… |
| `NC-260928-GEN2-CORPUS-LICENCIAS-1-1997-01` | L1–L5 · página de términos y regla por portal | dueño ADQUISICION (licencias de 111 payloads: mesa amplía el acceso de red del entorno de nube a los hosts de… | SIN-SOLICITUD: el dueño no nombra su solicitud |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-02` | P1 | dueño ADQUISICION (ECRIGE-CDMX 2019 FD, ENVE 2012/2014 datos abiertos, ENVE 2020/2022 base de ejemplo; A4/A5:… | cola:ECRIGE_CDMX_2019_FD [NO-OBTENIDO-POR-ESTE-AGENTE(10)] · cola:ENVE_2012_2014_DATOS_ABIERTOS [NO-OBTENIDO-… |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-03` | §3 | dueño ADQUISICION (ECCO SFP/SABG bases; A4/A5: NO-OBTENIDO-POR-ESTE-AGENTE(13) | cola:ECCO_SFP_CLIMA_CULTURA_ORGANIZACIONAL [NO-OBTENIDO-POR-ESTE-AGENTE(13)] |
| `NC-260928-GEN2-OBTENCION-EXTERNA-1-81e1-05` | P3 | dueño ADQUISICION (Banxico estudios de efectivo otras ediciones, Profeco QQP previos a 2024 y réplica JEMS 47… | cola:BANXICO_ESTUDIOS_EFECTIVO_Y_BILLETES [OBTENIDO-PARCIAL] · cola:PROFECO_QQP [OBTENIDO-PARCIAL] · cola:JEM… |
| `NC-260928-GEN2-OBTENCION-PREVIA-1-8e6a-03` | P2/P3 · portales fuera de INEGI y RNM/calendario | dueño ADQUISICION (ECCO SFP/SABG bases, calendario INEGI sin fila; A4/A5: NO-OBTENIDO-POR-ESTE-AGENTE(13) | cola:ECCO_SFP_CLIMA_CULTURA_ORGANIZACIONAL [NO-OBTENIDO-POR-ESTE-AGENTE(13)] |

**CAJA · 1**

| id | pieza | qué le falta | evidencia derivada |
|---|---|---|---|
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-03` | P2 · broker | dueño CAJA (forense/encargos/2026-09-27-ASTRA6-C1-EJECUTOR-AISLADO-3.md) | — |
<!-- TABLERO-UNICO:PENDIENTES:END -->
