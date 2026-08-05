# ENCARGO M-2: adjudica ADR-61 con el veredicto de W1-P y cierra cuatro cabos

Mesa #20, 4/ago/2026 (TZ America/Mexico_City, verificado con `TZ=America/Mexico_City
git log -1 --date=local`). Ejecutor: sesión Claude Code, entorno de nube
(`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`). Contador: cero, no mide —
sella lo que ya se midió (`W1-P`, Encargo X) y corrige dos cifras del ejecutable.

## 0 · ARRANQUE

Clon existente en `/home/user/Modelado-Mexicano` (no home), rama
`claude/encargo-m2-adr60e-qu1nim` ya creada y con árbol limpio (`git status`).
`HEAD` == `origin/main` == `2bc613b` (merge de PR #111,
`claude/censo-estimabilidad-6qok9w`, el remate de `E-CE`) — **`main` se movió**
respecto del `612571d` (PR #110, W1-P) que el encargo declara: entre `612571d` y
`2bc613b` solo hay el merge de PR #111 (`ca883a3`, 2 archivos:
`forense/censo-estimabilidad-coeficientes-v1_0.md` y `milpa/procedencia.yaml`) —
exactamente la rama que el encargo exige fusionar antes de lanzar. No es PARO:
refrescado (`git fetch origin main`), la rama de este acto ya contenía ese merge
(`git diff --stat` entre `HEAD` y `origin/main` vacío — cero divergencia). `data/raw`:
ausente, no aplica — este acto no lo usa. Entorno: `cloud_default`, valor correcto
para nube (ADR-59(b)); sonda saltada. Ningún número de este acto sale del espejo del
proyecto — todo comando corrido contra el clon de (1), pegado crudo abajo.

**Concurrencia viva, derivada, no de memoria.** `mcp__github__list_pull_requests`
(estado `open`) y `search_pull_requests` sobre
`repo:Josanoforo/Modelado-Mexicano is:pr is:open`: **cero PR abiertos** al momento
de este arranque. `git ls-remote --heads origin` solo expone `refs/heads/main` desde
este entorno (firma normal del proxy de este entorno, no evidencia de que `R1.3` no
exista). El encargo declara que `R1.3` corre en paralelo en Ubuntu, perímetro
`tests/`, `forense/notas/(r1-3)`, `hitoD-preregistro` y `hallazgos.md` — el único
archivo compartido con este acto es `forense/hallazgos.md`; esta nota se apendiza al
final del archivo (última línea verificada antes de escribir, `wc -l` +
lectura de la última entrada) para minimizar colisión de mérge.

## 1 · ADR máximo — derivado, no la constante 61

```
$ grep -ohE '^\*\*ADR-([0-9]+)' canon/*.md | grep -oE '[0-9]+' | sort -n | uniq -c
```
Devuelve 1..60, cada uno exactamente una vez, sin huecos — máximo = **60**, único.
Este acto sella **ADR-61** (máximo + 1, derivado).

## 2 · Verificación de las cuatro premisas de §1

1. **ADR máximo = 60, derivado con la receta de T15** (arriba). ✓
2. **W1-P en `main`.** `forense/notas/2026-08-04-w1-p-policial.md` existe, §8 trae el
   veredicto; `milpa/procedencia.yaml → coeficientes_generador_medidos.
   G1_radio_confianza.eje_policial` existe (líneas 687-708 al abrir este acto). ✓
3. **ADR-60(e) existe** (`gobernanza-v1_15.md:695`) y deja `radio_confianza` en
   `ASIGNADO · SIGNO BAJO PRUEBA`, apuntando explícitamente a `W1-P` como acto de
   resolución (verbatim: *"condición de resolución escrita: el resultado del acto
   `W1-P`"*). ✓
4. **`gobernanza-v1_15.md:714` declara la discrepancia de §4.1 "no corregida aquí"**
   — verbatim: *"La corrección de ese titular y su propagación a `procedencia.yaml`
   está asignada al commit 3 de `W1-P` (perímetro de ese acto, no de este)"*. `W1-P`
   v2 (§0, `2026-08-04-w1-p-policial.md` líneas 12-19) reasignó ese commit 3 fuera de sí misma
   por contaminación — el cabo llega huérfano a este acto. ✓

Las cuatro premisas sostienen. Continúa.

## 3 · Cláusula (b) — comparación en razón de riesgos, receta y salida

Tabla RR transcrita literal de `2026-08-04-w1-p-policial.md` §8 (columna `RR`/`IC95%(RR)`,
tabla "por ítem × estrato"). Receta: ¿el punto RR central de un estrato cae dentro
del IC95% del otro estrato? (criterio simétrico, aplicado a los dos sentidos).

```python
rows = [
    ("AP5_1_1", "policial",    0.821, 0.691, 0.975),
    ("AP5_1_1", "no_policial", 1.160, 0.899, 1.498),
    ("AP5_1_2", "policial",    0.836, 0.698, 1.001),
    ("AP5_1_2", "no_policial", 1.025, 0.745, 1.410),
    ("AP5_1_3", "policial",    0.817, 0.691, 0.966),
    ("AP5_1_3", "no_policial", 0.919, 0.707, 1.195),
]
# por ítem: ¿rr_pol dentro de [lo_np,hi_np]? ¿rr_np dentro de [lo_pol,hi_pol]?
# "distingue" = ni uno ni el otro cae dentro del IC del contrario
```

Salida:

```
Ítem         RR pol   RR pol ∈ IC no-pol?   RR no-pol   RR no-pol ∈ IC pol?   Distingue
AP5_1_1      0.821    False                  1.160      False                 True
AP5_1_2      0.836    True                   1.025      False                 False
AP5_1_3      0.817    True                   0.919      True                  False

2 de 3 ítems SIN distinción (el punto de un estrato cae dentro del IC95% del otro)
1 de 3 ítems SÍ distinguen los dos estratos en razón de riesgos
```

Confirmado: **solo `AP5_1_1` distingue** los dos estratos en RR; en `AP5_1_2` y
`AP5_1_3` el punto policial cae dentro del IC95% no-policial. Adicional, magnitud
de lo que "no distinguible" significa en puntos porcentuales sobre la base chica:

```
base_no_policial = 5.35%  (w1-p-policial.md §8, tabla de prevalencia)
RR típico policial ≈ 0.82 (mediana de los tres ítems: 0.821/0.836/0.817)
Δpp = base * (1 - RR) = 5.35 * 0.18 = 0.96pp ≈ "cerca de 1 punto porcentual"
```

Script completo: `/tmp/.../rr_comparacion.py` (efímero, receta reproducida arriba
íntegra — no depende de rutas de sesión).

## 4 · Cláusula (c) — recuento re-derivado de §4.1, con validación

**Receta:** parser de texto sobre las tres tablas de
`forense/notas/2026-08-04-x-condicionamiento-y-forma.md` §4.1 (regex ancla a filas
`| Formalidad|Edad|Ingreso | Nivel | n1 | n0 | β̂ | IC95% |`, extrae signo de β̂ y si
el IC95% excluye cero) — ajeno a la prosa del titular, cuenta directo sobre las 39
filas de datos.

```python
row_re = re.compile(
    r"^\|\s*(Formalidad|Edad|Ingreso)\s*\|\s*([^|]+?)\s*\|\s*([\d\s]+)\s*\|\s*([\d\s]+)\s*\|"
    r"\s*\*{0,2}([+\-−][\d.]+)\*{0,2}\s*\|\s*\[\s*\*{0,2}([+\-−][\d.]+)\*{0,2}\s*,"
    r"\s*\*{0,2}([+\-−][\d.]+)\*{0,2}\s*\]", re.M)
# positiva: beta > 0 · significativa: IC95% no cruza cero (lo>0 o hi<0)
```

Salida:

```
AP5_1_1: n=13 positivas=11 negativas=2  significativas=2
AP5_1_2: n=13 positivas=9  negativas=4  significativas=2
AP5_1_3: n=13 positivas=13 negativas=0  significativas=5

TOTAL: n=39 positivas=33 negativas=6 significativas=9
```

**Validación contra caso conocido** (contado a mano antes de confiar en la receta):
fila `AP5_1_1` / Edad / `18-29`, literal del archivo — `| Edad | 18-29 | 1 777 |
1 535 | **+0.0398** | [+0.0015, +0.0782] |`. A mano: β̂=+0.0398 (positivo), IC95%
= [+0.0015, +0.0782], ambos límites positivos → no cruza cero → significativa. El
parser extrae exactamente `beta=0.0398, lo=0.0015, hi=0.0782`, marca positiva=Sí,
significativa=Sí — coincide. Aserción del propio script (`assert`) confirma que
ninguna celda significativa tiene signo no-positivo — consistente con la lectura
cualitativa original.

**33 de 39 positivas, 9 de 39 significativas (las nueve positivas)** — coincide,
por una vía de derivación independiente, con la cifra que `ADR-60(f)`
(`gobernanza-v1_15.md:701-712`) ya había recontado por su propio método ("fila por
fila sobre las tres tablas de §4.1"). Dos parsers distintos, mismo resultado: no es
casualidad, es que la aritmética de la tabla es inequívoca — el titular original
("28 de 39... 12... distinguibles") es el que no reproduce.

La conclusión cualitativa **no cambia y se refuerza**: cero celdas con IC95% que
excluye cero tienen signo negativo, en los tres ítems y los tres ejes.

## 5 · Cláusula (d) — cronología verificada del censo `E-CE` contra `B-3` (PR #109)

```
$ TZ=America/Mexico_City git log --date=local --format="%h %cd %s" <sha>
```

| Hora (huso Mesa) | SHA | Evento |
|---|---|---|
| 20:41:02 | `8cdabcb` | Merge PR #106 — la "foto" del corpus contra la que `E-CE` se derivó |
| 21:11:53 | `0db6d1d` | Censo `E-CE` escrito (commit inicial); reparto `RUTA-A=3·RUTA-I=1·RUTA-C=2·SIN-RUTA=9` |
| 21:14:21 | `65302f7` | Merge PR #107 (ENASEM, 6 payloads) — **2m28s después** del commit del censo; primera vencida |
| 21:34:54 | `482ab20` | Merge PR #108 — la rama de `E-CE` (censo + fix de huso) llega a `main` |
| 21:37:56 | `ca883a3` | Remate `E-CE` (2 archivos): declara la foto (`8cdabcb`) y la primera vencida (ENASEM/PR#107), nombra ENASEM/MHAS candidato v1.1; declara explícitamente no haber cruzado `B-3` ("`git grep`... cero resultados al cierre de este acto") |
| 22:02:02 | `dff4877` | Merge PR #109 (`B-3`) — 10 instrumentos nuevos a `data/manifiesto.yaml`, entre ellos `enfih2019_bd_csv_zip` y `ensafi2023_bd_csv_zip` — **24m6s después** del remate de `E-CE`, sin cruzar |
| 22:20:20 | `2bc613b` | Merge PR #111 (rama de `E-CE`, con su remate) a `main` — **18m18s después** de que `B-3` ya hubiera movido el corpus |

Verificado por grep, no asumido: `grep -in "enfih\|ensafi" forense/censo-
estimabilidad-coeficientes-v1_0.md` → **cero resultados**. El censo nunca vio
ENFIH ni ENSAFI, ni en su commit inicial ni en su remate — ambos entraron al
manifiesto **después** de que el remate ya estuviera escrito.

`data/manifiesto.yaml` (diff `482ab20..dff4877`), entradas nuevas relevantes:

- `enfih2019_bd_csv_zip` — *"ENFIH 2019 (Encuesta Nacional sobre las Finanzas de
  los Hogares, Banxico+INEGI)... Candidata a credito-ahorro-finanzas-hogar."*
- `ensafi2023_bd_csv_zip` — *"ENSAFI 2023 (Encuesta Nacional sobre Salud
  Financiera)..."*

Ambas tocan directamente dominio de dinero (`G1`/`G3`/`G5`, mismos generadores que
`radio_confianza`/`familismo_apoyo`/`horizonte_temporal` citan en el propio censo).

**Es la segunda vez que este censo se vence antes de ser leído por el programa**:
la primera (ENASEM/PR#107) la atrapó su propio remate; esta segunda (ENFIH/ENSAFI/
PR#109) nadie la había atrapado hasta este acto.

## 6 · Barrido de la cascada (crudo)

```
$ grep -n "^\*\*ADR-" canon/gobernanza-v1_15.md | tail -3
671:**ADR-60 · ...**

$ grep -n -E '[0-9]+ ?ADR\b' canon/*.md
canon/estado-programa-v1_10.md:27: ... 60 ADR, protocolo de cambio ...
canon/estado-programa-v1_10.md:99: ... 60 ADR, protocolo de cambio ...
canon/gobernanza-v1_15.md:2: ... **60 ADR**

$ grep -n "SIGNO BAJO PRUEBA" milpa/*.yaml canon/*.md
milpa/procedencia.yaml:702  (eje_policial, prosa histórica de W1-P — no se toca)
milpa/procedencia.yaml:784  (rutas_estimabilidad_coeficiente.detalle, VIGENTE — se actualiza)
canon/gobernanza-v1_15.md:695  (ADR-60(e), sellado — no se edita)
canon/gobernanza-v1_15.md:718  (Reversión de ADR-60(e), histórico — no se edita)
```

| Sitio | Valor viejo | Valor nuevo | Vigente/histórico |
|---|---|---|---|
| `gobernanza-v1_15.md:2` | 60 ADR | 61 ADR | Vigente — se actualiza |
| `estado-programa-v1_10.md:27` | 60 ADR | 61 ADR | Vigente — se actualiza |
| `estado-programa-v1_10.md:99` | 60 ADR (+ cadena hasta ADR-60) | 61 ADR (+ entrada ADR-61) | Vigente — se actualiza |
| `procedencia.yaml:665` (eje_condicionante) | 28 de 39 / 12 sig. | 33 de 39 / 9 sig. | Vigente — se actualiza |
| `procedencia.yaml:685` (adr57_a) | 28 de 39 | 33 de 39 | Vigente — se actualiza |
| `procedencia.yaml:784` (rutas_estimabilidad_coeficiente) | "SIGNO BAJO PRUEBA (ADR-60 e), pendiente W1-P" | rótulo nuevo (a), cita ADR-61 | Vigente — se actualiza |
| `gobernanza-v1_15.md:695` (ADR-60(e)) | condición abierta | — | **Histórico, sellado — no se edita** (ADR-60 append-only) |
| `gobernanza-v1_15.md:714` (discrepancia declarada) | "no corregida aquí" | + adenda "cerrada por ADR-61" | Se anota cierre, sin editar el texto original (mismo criterio que ADR-58(e)/ADR-60) |
| `procedencia.yaml:702` (eje_policial, prosa de W1-P) | cita histórica de la condición ADR-60(e) | sin cambio | Histórico — correcto tal como está, no se edita |
| `gobernanza-v1_15.md:619` (ADR-57(a), cifra 28/12) | — | — | **Histórico, sellado — no se edita** (ADR-57 append-only) |

Contadores verificados sin mover: `0 de 15` (coeficientes en escala del modelo,
`README`/`estado §L5`), `12 de 27` (Hito D, `hitoD-preregistro`), `9 de 14`
(condicionales), `4 de 144`. Ninguno cambia — este acto sella interpretación de
resultados ya medidos, no mide nada nuevo.

## 7 · Cierre

`python3 tests/check.py --baseline` corrido tras verificar cero marcadores de
conflicto (`grep -c '^=======$' forense/hallazgos.md` y sobre `canon/`,
`milpa/procedencia.yaml` = 0 antes de escribir). Resultado y detalle de T15/T16 en
la sección de cierre de `gobernanza-v1_15.md`/PR. Perímetro de este acto:
`canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`,
`milpa/procedencia.yaml`, esta nota, `forense/hallazgos.md` (una línea, al final).
No se tocó `tests/`, `data/`, `canon/modelo-decision-v4_0.md`,
`forense/hitoD-preregistro-v2_0.md`, `ADR-57`, `ADR-60`, ni ninguna nota forense
previa. No se abrió `data/raw/` ni microdato. No se mueve ningún contador. No se
declara `radio_confianza` validado ni refutado. Sesión LIMPIA.
