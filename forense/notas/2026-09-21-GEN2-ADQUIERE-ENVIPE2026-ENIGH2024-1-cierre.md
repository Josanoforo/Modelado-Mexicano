# ACTO GEN2-ADQUIERE-ENVIPE2026-ENIGH2024-1 · nota de sesión

Encargo: `forense/encargos/2026-09-21-GEN2-ADQUIERE-ENVIPE2026-ENIGH2024-1.md`
(0-bis `dd08dc47`, sello de cuerpo `8d34a66c…`). Rama
`acto/gen2-adquiere-envipe2026-enigh2024-1`. SHA de redacción `b86c40e0`
(PR #963); base real al abrir `c441c9d0` (main se movió 39 commits desde la
redacción) y `a126914e` al cerrar (48 commits más durante el acto;
fusionado dos veces sin conflicto). Entorno `CAJA` (corpus montado, 422
archivos; `sin_variable`; red 200 a INEGI). `data/raw` enlazada a
`mm-corpus/raw`; `raices.local.yaml` escrita a mano (worktree nuevo,
`descargas_mx` no se usó -- todo bajó por red directa).

Vehículo: `/adquiere` dentro de `/acto`. Contador: ninguno numérico
(adquisición, no medición); `cuenta_gen2 = NO-APLICA`.

## 0 · Premisas verificadas (§3 del encargo)

- `[EJECUTADO]` `python3 tools/adq_doctor.py --selecciona` antes de P1:
  **ELEGIDOS (0)**, `ENVIPE_2026`/`ENIGH_2024_NC` excluidas por
  `SOLICITUD-PRE-CONFIRMADA` fuera de contrato. ✔ (confirma la premisa)
- `[EJECUTADO]` `grep -c envipe2026 data/manifiesto.yaml` / `enigh2024` →
  0 y 0 al abrir. ✔
- `[LEÍDO]` `#968` merge commit `de35a0d8`, confirmado ancestro de
  `origin/main` por `git merge-base --is-ancestor` **antes** de P1 (no
  sólo `grep` de log -- A.13/ADR-277). El encargo lo declaraba condicional
  a P4; resultó ya cumplido desde el arranque.

## 1 · P1 -- habilitar la cola

`upsert_fila` (escritor canónico): `ENVIPE_2026`/`ENIGH_2024_NC`
`SOLICITUD-PRE-CONFIRMADA` → `PENDIENTE`, nota con la reserva de §2
verbatim. `adq_doctor.py --selecciona` → **ELEGIDOS (2)**, nada más.

## 2 · P2 -- ENVIPE 2026

Vía (i) URL directa, mismo patrón que 2025 (`.../envipe/2026/datosabiertos/
conjunto_de_datos_ENVIPE_2026_csv.zip`), confirmada contra control negativo
2263 B en `/contenidos/`. Doble descarga + sha256 idéntico en los cuatro
payloads (zip 20 258 782 B, FD, cuestionario principal, cuestionario de
módulo); ZIP `testzip()=None` sobre 662 miembros sin extraer (envoltura
autorizada por §2); PDF con `%%EOF`. Diseño muestral: `NO-ENCONTRADO` por
patrón de nombre (misma familia de intentos fallidos que 2025, que
tampoco tiene esa entrada en el manifiesto) -- el FD ya trae los campos
de diseño (`EST_DIS`/`UPM_DIS`/factor de expansión).

Registrados: `envipe2026_csv`, `envipe2026_fd_pdf`,
`envipe2026_cuest_principal_pdf`, `envipe2026_cuest_modulo_pdf`. Fila →
`OBTENIDO`.

## 3 · P3 -- ENIGH 2024

El patrón de nombre de 2022 (`conjunto_de_datos_enigh_ns_2022_csv.zip`) NO
aplica a 2024: el orden año/`ns` se invirtió
(`conjunto_de_datos_enigh2024_ns_csv.zip`), confirmado contra control
negativo. Descarga de 103 139 139 B en dos tramos por timeout de red
(`curl -C -` para reanudar); verificada A.7 contra una segunda descarga
fresca e independiente: sha256 idéntico. ZIP `testzip()=None` sobre 346
miembros -- solo trae diccionarios CSV por tabla, ningún documento
embebido.

Documentación localizada por el catálogo RNM 1116 (ENIGH 2024, pestaña
`related-materials`, 13 recursos completos) en vez de seguir adivinando
patrones de `/doc/` que fallaban: descripción de la base, diseño
muestral, y los seis módulos de cuestionario + manual del entrevistador
(diez payloads). Nota técnica: `NO-ENCONTRADO` -- la lista del catálogo
es completa y no la trae (a diferencia de 2022, que sí publicó una). Tres
documentos metodológicos adicionales del mismo catálogo (diseño
conceptual, criterios de validación, documento operativo de campo,
descripción del cálculo de indicadores con R) se localizaron pero **no**
se registraron -- fuera del alcance de P3 (que pide descriptor + nota
técnica + cuestionario), quedan citados aquí como sucesor si mesa los
pide.

Registrados: `enigh2024_nc_csv`, `enigh2024_descripcion_base_pdf`,
`enigh2024_diseno_muestral_pdf`, `enigh2024_cuest_hogares_pdf`,
`enigh2024_cuest_personas_mayores_pdf`,
`enigh2024_cuest_personas_menores_pdf`,
`enigh2024_cuest_negocios_hogar_pdf`, `enigh2024_cuest_gastos_hogar_pdf`,
`enigh2024_cuest_gastos_diarios_pdf`, `enigh2024_entrevistador_pdf`. Fila
→ `OBTENIDO`.

Los 14 payloads: `readlink -f` confirma que viven en el corpus compartido
(`/home/pc0/mm-corpus/raw`), no en el worktree (defecto PR #77); los 14
`COINCIDEN` con `tests/manifiesto.py --verifica`.

## 4 · P4 -- congelar el duelo

`#968` en `origin/main` (verificado §0). `python3 tools/corrida0.py
preflight CALC-DUELO-ENVIPE2026-EMISIONES-0001`: `BLOQUEADO
input_manifiesto_AUSENTE=envipe2026_csv` → **VERDE** (5 inputs COINCIDEN,
`spec_md_sha256` EN-MAIN-COINCIDE, árbol LIMPIO). Ninguna otra edición a
los CALC. `CALC-DUELO-ENVIPE2026-ADJUDICACION-0001` sigue `BLOQUEADO`,
sólo por `input_repo_ausente=emisiones_selladas` (cadena 3a; nace del
COMMIT-2, que este acto no corre) -- exactamente el remanente que la NC
preveía, no un bloqueo nuevo.

COMMIT-1 del duelo ENVIPE 2026 **CONGELADO** según D-22 ampliada:
requisito 1 cumplido hoy; requisitos 2-4 ya demostrados en `#968`. Cierra
`NC-260921-GEN2-DUELO-ENVIPE2026-COMMIT-1-8796-01` (estado `CERRADA`) y
actualiza su columna sucesor: sólo queda la sesión del COMMIT-2 (F3, otra
sesión, plazo 31/oct).

## 5 · Hallazgo (una línea, `forense/hallazgos.md`)

`tools/actualiza_reactivos_contexto.py --objeto <payload nuevo no
indexado>` sobrescribe el overlay **completo** con 0 filas en vez de
fusionar -- se corrió por error para `envipe2026`/`envipe2026_fd_pdf` y
borró 43 020 filas + 6 091 grupos residuales acumulados de
`envipe/ennvih/encuci/enif/ensafi`; revertido con `git checkout --` antes
de comitear, nunca llegó a `git add`. §5.4 de `/adquiere` queda
`NO-CORRIDO` para los payloads de este acto (añadir `envipe2026` a las
tablas de fuentes es trabajo de `tools/`, ajeno a este acto).

## 6 · Cierre

`python3 tools/adq_doctor.py --selecciona` antes: **ELEGIDOS (0)**
(bloqueadas por estado fuera de contrato). Después de P1: **ELEGIDOS
(2)**. Después de P2/P3: **ELEGIDOS (0)** (caminata vacía, no selección
equivocada). `python3 tools/cierre_acto.py --encargo <este encargo>`:
suite `tests/check.py --baseline --parallel` **VERDE** (código 0);
`HEAD deriva de origin/main: True` tras el segundo merge.

**Qué rompería revertirlo.** Las dos filas de la cola volverían a
`SOLICITUD-PRE-CONFIRMADA` sin caminata posible; el duelo ENVIPE 2026
volvería a `BLOQUEADO input_manifiesto_AUSENTE`, deteniendo el COMMIT-2
(plazo 31/oct); los 14 payloads desaparecerían del manifiesto (aunque el
corpus físico, gitignorado, sobreviviría hasta el próximo `--escanea`).

`## NO-CORRIDO / RESERVAS`: ver encargo archivado.
