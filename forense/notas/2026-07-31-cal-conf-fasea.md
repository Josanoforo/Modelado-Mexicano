# CAL-CONF Fase A — inventario de instrumento para `confianza_institucional`

*31 de julio de 2026. Responde al encargo de la misma fecha: para cada uno de
los 6 componentes del vector `confianza_institucional` (`canon/modelo-decision-v3_4.md`
§1.3, ADR-28.b), ¿hay reactivo ESPECÍFICO de esa institución? ¿hay corte
formal/informal en el mismo instrumento para asignar perfil?*

**Firewall respetado.** Se abrieron descriptores/diccionarios de variables y
cuestionarios (nombres de variable, etiquetas de pregunta, códigos de valor,
estructura de tablas). No se abrió ni una fila de microdato, ni frecuencia, ni
distribución, ni cruce. Extracción vía `pdftotext -layout` (PDF) y un parser
propio sobre el XML crudo de `xlsx` (sin librerías externas — `openpyxl`/
`pandas` no están instalados en este entorno); los `.txt` derivados viven en
el scratchpad de la sesión, no en el repo.

## Instrumentos abiertos

| Encuesta | Archivo(s) | Dónde | Nota |
|---|---|---|---|
| ENVIPE | `fd_envipe2025.pdf` | `Modelado-Mexicano-descarga-dirigida/data/raw` | edición 2025 (más reciente disponible) |
| ENCUCI | `FD_ENCUCI2020.pdf` | `Modelado-Mexicano/data/raw` | única edición existente |
| ENIF | `enif_2024_fd.xlsx` + `enif_2024_cuestionario.pdf` | `Modelado-Mexicano-descarga-dirigida/data/raw` | edición 2024 |
| ENSANUT 2024 | `adultos_ensanut2024_w.Catlogo.xlsx`, `hogar_ensanut2024_w_ICB.Catlogo.xlsx`, `utilizadores_ensanut2024_w.Catlogo.xlsx` + cuestionarios "adultos" y "utilizadores" | `Descargas MX` | **parcial**: 3 de ~9 instrumentos del paquete (no se abrieron niños/adolescentes/menores/integrantes/NSE — ver "Límite declarado") |
| ENCIG | `encig21_estructura_base_datos.pdf` + `encig21_cuestionario.pdf` | `Modelado-Mexicano-descarga-dirigida/data/raw` | **sin FD 2023** (no localizado, ver `forense/hallazgos.md` 2026-07-31); se usa la edición 2021, la más reciente con descriptor en disco |

## Los 6 componentes (`modelo` §1.3)

seguridad-fuerzas armadas · educación · salud · electoral-partidos ·
justicia-policía · financiera.

## Resultado por componente

| Componente | Reactivo específico | Instrumento(s) / variable / cita | Corte formal/informal (mismo instrumento) |
|---|---|---|---|
| **Seguridad-fuerzas armadas** | **SÍ** | ENVIPE `AP5_4_08` Ejército, `AP5_4_09` Fuerza Aérea, `AP5_4_10` Marina, `AP5_4_04` Guardia Nacional (`fd_envipe2025.pdf`, sección 5.4, pp. 33-34 del texto extraído) · ENCUCI `AP5_3_4` "Ejército y Marina", `AP5_3_5` "Guardia [Nacional]" (`FD_ENCUCI2020.pdf`, pregunta 5.3, p. 27) · ENCIG ítem 20 "Guardia Nacional", ítem 21 "Ejército y Marina" (`encig21_cuestionario.pdf`, sección XI, pregunta 11.1, p. 22) | **SÍ**, vía ENCUCI: `AP3_15_4` "¿tenía... derecho a servicios públicos de salud (IMSS, ISSSTE u otro)?" en el trabajo de la semana pasada — proxy estándar de formalidad laboral (`FD_ENCUCI2020.pdf`, pregunta 3.15, p. 15), en la misma tabla que `AP5_3_4`/`AP5_3_5` |
| **Educación** | **SÍ** | ENCUCI `AP5_2_6` "Universidades" (`FD_ENCUCI2020.pdf`, pregunta 5.2, p. 26) · ENCIG ítem 1 "Universidades públicas", ítem 16 "Escuelas públicas de nivel básico" (`encig21_cuestionario.pdf`, sección XI, p. 22) | **SÍ**, vía ENCUCI: mismo `AP3_15_4`, misma tabla que `AP5_2_6` |
| **Salud** | **SÍ, pero de un solo instrumento** | ENCIG ítem 3 "Hospitales públicos" (`encig21_cuestionario.pdf`, sección XI, p. 22). Ni ENVIPE ni ENCUCI ni ENIF traen batería de confianza institucional para salud. ENSANUT (3 instrumentos revisados: hogar/adultos/utilizadores) **no trae reactivo de confianza en instituciones de salud** — la única mención de "confianza" encontrada es `05 Falta de confianza`, un motivo entre varios ("no hay dónde atenderse", "es caro", "tratan mal"...) dentro de la pregunta 10.7 sobre por qué no recibió tratamiento — condicional a tener un diagnóstico, no un reactivo de confianza institucional autónomo. No cuenta como específico. | **NO**. ENCIG no tiene módulo de prestaciones laborales (contrato, aguinaldo, derecho a servicios médicos por el trabajo) — solo "posición en la ocupación" (jornalero/empleado/cuenta propia/patrón/sin pago, pregunta 2.10), que es un eje distinto de formal/informal, no un corte limpio |
| **Electoral-partidos** | **SÍ** | ENCUCI `AP5_2_5` "Partidos" (p. 26), `AP5_3_6` "Senadores federales", `AP5_3_7` "Diputados", `AP5_3_8` "Instituto [Nacional Electoral]" (p. 27-28) · ENCIG ítem 12 "Cámaras de Diputados y Senadores", ítem 14 "Institutos electorales", ítem 19 "Partidos políticos" (p. 22) | **SÍ**, vía ENCUCI: mismo `AP3_15_4` |
| **Justicia-policía** | **SÍ** | ENVIPE `AP5_4_01/02/03/05` (policía de tránsito/preventiva/estatal/ministerial), `AP5_4_06` Ministerio Público, `AP5_4_07` Fiscalía General, `AP5_4_11` Jueces (pp. 29-34) · ENCUCI `AP5_3_1` Jueces, `AP5_3_3` Policía (p. 27) · ENCIG ítem 2 "Policías", ítem 17 "Jueces y Magistrados", ítem 22 "Ministerio Público" (p. 22) | **SÍ**, vía ENCUCI: mismo `AP3_15_4` |
| **Financiera** | **SÍ** | ENIF, Sección 11 "Confianza y protección de personas usuarias de servicios financieros", `P11_1_1`-`P11_1_5` (`enif_2024_fd.xlsx`, hoja `TMODULO`; `enif_2024_cuestionario.pdf`, p. 28) — ver nota "de paso" abajo sobre por qué cuenta como específico y no condicionado a uso | **SÍ**, en el mismo instrumento: `P3_13` "Por parte de su trabajo, ¿usted tiene derecho a los servicios médicos... del Seguro Social (IMSS)?" (hoja `TMODULO`; cuestionario p. 7) |

## El número: de 36

36 = 6 componentes × 6 perfiles del modelo (la misma cuenta que usa
`forense/hitoE-campana-medicion-v2_0.md:262-266` para `confianza_institucional`).
Cada componente aporta sus 6 celdas de perfil enteras a un solo balde, según
su estatus de instrumento — el estatus no varía por perfil, varía por
componente:

- **Con reactivo Y corte: 30** (5 componentes × 6 — seguridad-fuerzas
  armadas, educación, electoral-partidos, justicia-policía, financiera)
- **Con reactivo, sin corte: 6** (1 componente × 6 — salud)
- **Sin nada: 0**

**30 + 6 + 0 = 36.** Los seis componentes tienen reactivo específico en al
menos un instrumento de los cinco abiertos; cinco de los seis además tienen,
en el mismo instrumento que trae el reactivo, un corte utilizable para
formal/informal. Solo salud queda con reactivo pero sin corte propio en la
misma fuente (ENCIG no trae módulo de prestaciones laborales).

## De paso: ¿ENIF trae confianza en instituciones financieras sin condicionar a uso/tenencia?

**Sí.** La Sección 11 (`P11_1_1`-`P11_1_5`) se formula en modo hipotético
para toda persona entrevistada, sin importar si tiene cuenta o producto
financiero: *"11.1 Si usted tuviera que solicitar los servicios de un banco o
cualquier otra institución financiera, ¿considera que…"* — recibiría la
información necesaria / resolverían su problema económico / estaría seguro
su dinero / resolverían quejas / protegerían sus datos (`enif_2024_cuestionario.pdf`,
p. 28). Verificado el flujo del cuestionario: el único filtro de edad
cercano (línea "FILTRO 1: ¿TIENE 71 AÑOS O MÁS?", que salta a Sección 10)
no salta la Sección 11 — todo entrevistado adulto la contesta,
independientemente de si usa o tiene productos financieros. No es un
reactivo condicionado a tenencia ni a uso.

**Esto tumba el veredicto SIN INSTRUMENTO** que `forense/hitoE-campana-medicion-v2_0.md:370-371`
declara para el componente financiero de `confianza_institucional`
("financiera | SIN INSTRUMENTO | —"). Esta nota no edita ese archivo — es
otra sesión, y el requisito de salida de ADR-40/ADR-34 sobre forma canónica
de veredicto no aplica aquí (esto no es un veredicto `RX.Y` de Hito D, es
inventario de Fase A) — se deja registrado para que quien mantenga `hitoE`
lo revise y decida si corrige la fila.

## Límite declarado

- **ENCIG sin FD 2023.** `encig23_estructura_base_datos.pdf` está registrado
  en `data/manifiesto.yaml` con sha256/tamaño pero no se localizó en disco
  en ninguno de los tres worktrees vivos ni en las carpetas de descarga
  (hallazgo aparte en `forense/hallazgos.md`, 2026-07-31). Se usó la edición
  **2021** como sustituto (instrucción del encargo: "sin FD, usa lo que
  haya"). La batería de confianza institucional de ENCIG parece estable
  entre ediciones (mismo formato de pregunta 11.1 en versiones que sí se
  han visto en otras sesiones), pero esta nota no verifica que los 24 ítems
  y sus claves `P11_1_x` sean idénticos en 2023 — es una lectura de la
  edición 2021, no de la vigente.
- **ENSANUT parcial.** Solo se abrieron 3 de los ~9 instrumentos del
  paquete 2024 (catálogos y cuestionarios de hogar, adultos y
  utilizadores). No se revisaron niños 0-9, adolescentes, ni los catálogos
  de menores/integrantes/NSE. El veredicto "ENSANUT no trae reactivo de
  confianza en salud" se sostiene sobre esos 3, no sobre el paquete
  completo — no cambia el número de 36 (salud ya tiene reactivo vía ENCIG),
  pero no se puede afirmar con la misma certeza que ENSANUT esté vacío en
  esto si alguien necesita esa afirmación específica más adelante.
- **Corte de ENCIG marcado NO, no "parcial".** ENCIG sí trae "posición en la
  ocupación" (jornalero/empleado/cuenta propia/patrón/sin pago), pero ese
  eje no equivale a formal/informal sin una prestación o afiliación
  adicional que ENCIG no pregunta — se contó como NO por criterio estricto,
  no por no haber mirado.
