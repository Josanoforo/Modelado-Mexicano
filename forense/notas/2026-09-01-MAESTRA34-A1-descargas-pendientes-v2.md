# Descargas pendientes — v2 (1/sep/2026)

Producido por `ACTO MAESTRA34-A1 · REGISTRA-Y-EVALUA-DESCARGAS-2`
(encargo `forense/encargos/2026-09-01-MAESTRA34-A1-REGISTRA-Y-EVALUA-DESCARGAS-2.md`,
P3). Sucede al recibo de `ACTO MAESTRA33-A4` («0 de 15 ejecutadas»,
1/sep/2026), que corrió antes de que mesa bajara nada.

**Derivado del registro, no de memoria.** Cada línea de abajo sale de
`data/curacion-registro/cola-adquisicion-registro.tsv` (estado real de la fila
tras este acto) y de `data/manifiesto.yaml` (los `id` de payload que
efectivamente existen). Los negativos salen de un barrido por nombre sobre la
raíz completa `descargas_mx`, con control positivo declarado.

**A.13 — universo examinado.** `find "/mnt/c/Users/PC0/Descargas MX" -type f`
= **160 archivos**; `-newermt 2026-08-14` = **38 nuevos**. Barrido por nombre
sobre los 160 para las recetas sin payload: `ssrn` 0 · `cenfri` 0 · `bauchet` 0
· `microinsurance` 0 · `compranet` 0 · `proveedor` 0 · `iepc` 0 · `computos` 0
· `sicee` 0 · `reune` 0 · `redeco` 0 · `condusef` 0 · `tanda` 0. **Control
positivo del mismo barrido**: `urgencias` 10 · `wbes` 12 · `prep` 1 — el
comando sí examinó archivos reales.

---

## 1 · Estado de las 15 recetas tras la pasada de mesa

| # | fila / fuente | estado tras este acto | qué falta |
|---|---|---|---|
| 1 | `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023` (10) | **CUMPLIDA** — `OBTENIDO` | nada |
| 2 | `MEXICO_PANEL_STUDY_2012` (19) | **PARCIAL** — solo documentación | el microdato (exige cuenta ICPSR e iniciar sesión) |
| 3 | `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` (22) | **NO ES DESCARGA** | decisión de mesa: solicitar a CNSF/AMIS |
| 4 | `CNGMD` (29) | **PARCIAL** — llegó el diseño, no el dato | las 87 URLs de datos abiertos (ver §2) |
| 5 | `PRICE_AND_INFORMATION_TYPE...` (39) | **NO EJECUTADA** — 0 rastro | abrir cenfri.org o SSRN en navegador |
| 6 | `REGISTRO_DE_TANDAS_Y_REPUTACION` (40) | **NO ES DESCARGA** | decisión de mesa: contacto con Tanda+ |
| 7 | `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` (41) | **NO ES DESCARGA** | misma familia que #6 |
| 8 | `CAPITAL_RETURNS_LEON_2005_2006` (57) | **CUMPLIDA** — `OBTENIDO` | nada |
| 9 | `CERO_DESABASTO` (60) | **CUMPLIDA Y EXCEDIDA** | nada — ver corrección en §3 |
| 10 | `OBSERVATORIO_DE_CUIDADOS...` (62) | **CUMPLIDA** — `OBTENIDO` | nada |
| 11 | `EXT_OF_07_CATALOGO_PROVEEDORES...` (63) | **NO EJECUTADA** — 0 rastro | localizar el dominio vigente de CompraNet |
| 12 | `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` (64) | **CUMPLIDA Y EXCEDIDA** | nada — llegó descriptor **y** microdato |
| 13 | `EXT_OF_03_PARTICIPACION_LOCAL_2024` (65) | **NO EJECUTADA** | elección local; ver §4 |
| 14 | `EXT_OF_11_REUNE_REDECO` (70) | **NO ES DESCARGA** | consulta uno-por-uno; requeriría transparencia |
| 15 | `EXT_OF_12_PREP_2024` (71) | **CUMPLIDA por la vía PREP** | los cómputos distritales; ver §4 |

**Cuenta: 6 cumplidas · 2 parciales · 3 no ejecutadas · 4 que nunca fueron
descargas** (son decisiones de mesa o consultas sin exportación masiva). El
paquete original las contaba a las 15 por igual; esa distinción es de este acto.

**Fuera del paquete:** mesa resolvió además la fila 9
(`MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010`, `NO-ACCESIBLE`
por muro de credencial WB870 confirmado dos veces), que **no tenía receta**. Y
trajo el módulo `WBES-OS Mexico 2026` (seguimiento sobre IA), que no tenía fila.

---

## 2 · Receta enmendada para CNGMD (#4) — las 87 URLs ya están en tus manos

`DescargaMasiva_192026_194559.zip` **no trae datos**: trae
`DescargaMasivaApp.exe`, `leeme.txt` y `DescargaMasivaOD.xml`. Ese XML es una
**orden de descarga** que declara `totalMb="159.08 MB"` y lista **87 URLs
reales** con esta forma:

```
https://www.inegi.org.mx/contenidos/programas/cngmd/2023/datosabiertos/m<N>/<tabla>_cngmd2023_csv.zip
```

Reparto por módulo: **m1** 2 · **m2** 31 · **m3** 23 · **m4** 9 · **m5** 6 ·
**m6** 10 · **m7** 6. Ninguna de las 87 se descargó (0 coincidencias de nombre
en los 160 archivos de la raíz).

Los dos módulos que el encargo pedía y que **no** llegaron como cuestionario
(módulo 1 Ayuntamientos, módulo 3 Seguridad pública) están completos en esa lista. Las 2 de
m1 y las 23 de m3, verbatim del XML:

```
m1/alcaldias_cngmd2023_csv.zip
m1/ayuntamientos_cngmd2023_csv.zip
m3/acade_insti_forma_poli_cngmd2023_csv.zip     m3/enfrentamientos_cngmd2023_csv.zip
m3/activ_estadis_geo_cngmd2023_csv.zip          m3/fortalec_polic_cngmd2023_csv.zip
m3/actuacion_dentro_sjp_cngmd2023_csv.zip       m3/infraestruc_segpub_cngmd2023_csv.zip
m3/asegura_armas_cngmd2023_csv.zip              m3/operat_polic_patru_remi_cngmd2023_csv.zip
m3/asocia_interinst_cngmd2023_csv.zip           m3/pers_func_segpub_cngmd2023_csv.zip
m3/atenc_victlocali_persdes_noloc_cngmd2023_csv.zip  m3/pers_lesi_fall_desa_noloc_cngmd2023_csv.zip
m3/bien_robado_recuperado_cngmd2023_csv.zip     m3/puesta_disposi_cngmd2023_csv.zip
m3/centro_aten_sist_telef_cngmd2023_csv.zip     m3/rec_presup_cngmd2023_csv.zip
m3/certificaciones_cngmd2023_csv.zip            m3/regimen_discip_cngmd2023_csv.zip
m3/comis_honor_just_cngmd2023_csv.zip           m3/sit_oper_ejec_func_segpub_cngmd2023_csv.zip
m3/dignificacion_servicio_cngmd2023_csv.zip     m3/transito_vialidad_cngmd2023_csv.zip
                                                m3/unidad_especializada_cngmd2023_csv.zip
```

**Receta, ≤1 minuto:** ejecutar `DescargaMasivaApp.exe` en Windows con conexión
(él baja las 87 solo), **o** pegar cualquiera de las URLs de arriba en el
navegador. La receta original decía «si el enlace sigue roto, usa Descarga
Masiva» — mesa la usó, pero descargó **el instalador**, no corrió la descarga.
Ese es el paso que falta, y es un clic.

*(Precedente: `descargamasiva_1382026_134046`, 13/ago/2026, es el mismo
instalador bajado y registrado sin correr. Es la segunda vez.)*

---

## 3 · Corrección a lo que mesa reportó de Cero Desabasto (#9)

Mesa reportó: *«#9 "Cero Desabasto csv" (18 KB, tabla del gráfico, falta base
histórica)»*. La primera mitad es exacta; **la segunda no**.

- `Cero Desabasto csv` (17 872 B) → sí es la tabla del gráfico: 538 filas,
  columnas `entidad, year, cuatrimestre, count`, 2019-2025, sin municipio.
- `Exportación pública de Insumos y reportes.xlsx` (732 571 B) → **es la base
  histórica**. Hoja `Registros históricos`, **11 036 filas** (reporte × insumo,
  7 914 reportes distintos), columnas `id del Insumo, Tipo de Medicina, Grupo,
  Componente, Presentacion, id del Reporte, Fecha de Registro, Tipo de
  informante, Padecimiento, Entidad, Institución, Institución 2, CLUES,
  Hospital o clínica`. `Fecha de Registro` 0 % nula, 2019-02-18 → 2024-09-03;
  `Entidad` 0.2 % nula; `Institución` 0.3 % nula; `Componente` 10.0 % nula.

Trae fecha, institución, entidad y medicamento a nivel de registro: es
exactamente el criterio que el encargo puso como umbral para `EXISTE-SATISFACE`
en la receta #9. Mesa no lo asoció a Cero Desabasto porque el nombre del archivo
no la nombra.

**No hace falta volver a bajar nada para #9.**

---

## 4 · Vías alternas vivas para la pieza cívica (#13 y #15)

Lo que hay hoy, verificado: `20240603_2005_PREP.zip` (corte `03/06/2024 20:05
(UTC-6)`), 3 paquetes federales — Diputaciones Federales 172 406 actas,
Presidencia 171 410, Senadurías 172 438 —, una fila por acta de casilla, con
columna `LISTA_NOMINAL` verbatim.

Lo que **falta** para el diseño concurrente/no concurrente:

1. **La mitad no concurrente.** Ninguna elección local está en el paquete: 0
   menciones de `local`/`estatal`/`municipal`/`ayuntamiento`/`gubernatura` en el
   `LEEME.txt` de INE, idéntico en los 3 paquetes. Hace falta una elección local
   **no concurrente** (2022 ó 2023) de algún estado.
2. **La granularidad municipal.** La geografía del PREP federal llega como
   `ID_ENTIDAD`/`ENTIDAD`, `ID_DISTRITO_FEDERAL`/`DISTRITO_FEDERAL` y `SECCION`
   — **no hay columna de municipio**. Es el mismo hueco que la ficha `R7.1`
   declara por escrito («granularidad municipal es hueco declarado»).

Vías, en orden de costo:

- **SICEE** (`https://sicee.ine.mx/`) — dado de alta como fuente por este acto
  (fila nueva en el registro del curador + `aliases-fuentes.tsv`). Su propia
  documentación declara cobertura de elecciones **locales desde 2015**, así que
  la ventana sirve para 2022/2023. Es una SPA: no entrega nada a un cliente sin
  navegador. **Receta vigente:
  `forense/notas/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md` l.183-198.**
  *(El encargo de este acto la citaba como «cierre l.165-195»; ese rango empieza
  a media frase del intento 4 y corta el paso 3 de la receta. La cita correcta
  es l.183-198.)*
- **OPLE del estado elegido** — p. ej. `https://www.iepac.mx/micrositios/resultados-electorales`.
  El archivo de un instituto estatal no comparte la ventana de cobertura de
  SICEE (INE es federal; el OPLE es el archivo del propio estado).
- **Cómputos distritales 2024** (`https://computos2024.ine.mx/`) — mesa reporta
  que **bloquea su IP**. Alterna: otra red, o la vía SICEE de arriba.
- **Crosswalk sección→municipio del INE** — resolvería (2) sobre el PREP que ya
  está en el corpus, sin bajar una elección nueva. No está en el corpus hoy.

**Decisión de mesa que sigue pendiente y bloquea #13:** *qué estado(s)
priorizar*. La receta #13 ya lo decía («Requiere decisión de mesa primero») y
sigue sin contestarse.

---

## 5 · Lo que este acto NO hizo

No descargó nada por red: el perímetro del encargo lo prohíbe («si falta algo,
receta, no `curl`»). Todo lo de arriba es receta para mesa o para un acto
sucesor, no un fallo de adquisición de este acto.
