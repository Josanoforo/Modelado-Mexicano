# Nota · 26/ago/2026 — Cierre de `ACTO MAESTRA30-E10 · R21-ADJUDICA`

**Encargo:** `forense/encargos/2026-08-26-E10-R21-ADJUDICA.md` (dirección, maestra-30, 26/ago/2026, redactado contra `main=3bc28b1`). Entorno asignado: **NUBE** (`cloud_default`, repo-only). Cero red, cero microdato.

## §1 · Arranque

1. **Repo.** Clon existente en `/home/user/Modelado-Mexicano`. `git log -1` al arrancar: `efd443b Merge pull request #378 from Josanoforo/acto/e7-r-scoring`. `git status` limpio, rama `claude/r21-adjudica-veredicto-0pufc0` ya existente localmente y en `origin`.
2. **SHA.** El encargo se redactó contra `main=3bc28b1`; `origin/main` ya se había movido a `efd443b` (mismo commit que `HEAD` de la rama de trabajo — la rama parte de `main` post-movimiento) al arrancar este acto. No es PARO: el perímetro del encargo (la ficha `R2.1`, su censo, el bloque de registro) no depende de qué PR aterrizó entre `3bc28b1` y `efd443b`; se verificó contra el árbol vivo, no de memoria.
3. **`data/raw`.** Ausente en este clon (esperado, gitignorada). Este acto no la toca — cero microdato.
4. **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (confirma NUBE). Este acto no toca red ni microdato — la sonda de conectividad (`curl` a INEGI) se omite por regla explícita del propio encargo ("Si este acto no toca microdato ni red, dilo y salta este punto"); cero archivos examinados por esa sonda, cero declarados.
5. **Espejo.** No se usó el espejo del proyecto. Todas las cifras de esta nota vienen del clon de (1), comandos a la vista abajo.

## §2 · Compuerta cero

Ranura de mesa **presente** en el encargo (RANURA M-R21, precargada, mismo patrón que R1.4/ADR-187). Verificación de la firma contra el árbol:

- **Línea del censo, pegada verbatim:** `forense/R21-censo-fuentes-v1_0.md:4` — *"Cero candidatas alcanzan EXISTE-SATISFACE... Se propone archivar D..."*
- **Ausencia de veredicto, con conteo (`grep` del bloque de emisiones antes de este acto):** de las 25 líneas canónicas `` `RX.Y` → veredicto `Z` `` que existían en `forense/hitoD-preregistro-v2_0.md` antes de este acto, ninguna cita `R2.1`. Contador previo: **25 de 27**, `13D·4B·4A·2E·2C`.

## §3 · Derivación de la letra

La ficha `R2.1` (post-`ADR-190`) trae **dos** escalas: `v1` (par organizacional, letras `A-D` clásicas — techo histórico, intacto) y `v2` (append `B-bis`, cuatro filas nombradas: `A-corr`, `Corrobora`, `Acota`, `Demasiado débil`). El desenlace medido por el censo es "ninguna fuente ejecuta el falsador `v2`" — de 12 candidatas examinadas (`forense/R21-censo-fuentes-v1_0.md`), **cero** alcanzan `EXISTE-SATISFACE`: 9 `EXISTE-NO-SATISFACE`, 1 `EXISTE-NO-SATISFACE (SÓLO como MARCO)`, 1 `NO-ENCONTRADO`. Ninguna candidata trae, a la misma unidad, el indicador de jerarquía/tipo de organización cruzado con voz ascendente y los cuatro confusores declarados (canal, sector, tamaño, escolaridad) — la candidata más próxima, HSOPS/HSOPSC mexicano, mide reporte voluntario de errores con dimensión jerárquica (α=0.88) pero sobre hospitales, no sobre firmas familiar/plana, y no declara pareo de canal.

Ese desenlace cae, literal, en la fila **`Demasiado débil`** de la escala `(d)` del append: *"el microdato disponible no permite controlar los cuatro confusores declarados... el falsador no corre, no se declara ni corroboración ni refutación"*. La escala **sí contempla** el desenlace — no es un caso B-bis (hueco), y no hace falta parar. En la nomenclatura de archivo del programa (`ADR-55`/`ADR-56`, ya aplicada a `R2.2`/`R10.2`/`R1.4`/`R8.1`/`R7.4`/`R7.5`), esa fila es letra **`D`** — y el propio censo la propone verbatim: *"Se propone archivar D"* (`forense/R21-censo-fuentes-v1_0.md:4`). La letra no se inventó: se derivó de la escala de la propia ficha, y coincide con lo que el censo, redactado tres días antes de este acto, ya había anticipado.

## §4 · Escritura

- **Emisión canónica** al bloque `## Registro de veredictos archivados` de `forense/hitoD-preregistro-v2_0.md`: `` `R2.1` → veredicto `D` ``, con firma verbatim de la RANURA, estampa `A.10` (censo + cruce `#363` + pase `#361`/gemelo), reserva estructural ("el ataque correlacional a nivel empleado nunca corrió — `D` no es juicio sobre la regla, es juicio sobre las fuentes"), `v1` intacto, tres reaperturas VENCIBLE EN ALCANCE.
- **Enmienda fechada** en la sección de la ficha `R2.1` (tras el §"Origen y procedencia del censo", :117 en adelante), cerrando la espera del 25/ago (`ADR-196`) con el mismo texto y la misma derivación de letra.
- **Contador re-derivado por parser** (`python3 tests/check.py`, T18/T20): **26 de 27**, `14D·4B·4A·2E·2C` — propagado a `README.md:36`, `canon/estado-programa-v1_10.md` (§L0/§L5 y Paso 2), `canon/gobernanza-v1_15.md` (ADR-37 y §5 deuda declarada) y `canon/modelo-decision-v4_0.md` (dos citas vivas que T20 exigía).
- **`forense/firmas-pendientes.tsv`:** fila `FP-167` nueva, `FIRMADA`/`ejecutada_en=ADR-208`, citando la RANURA precargada del encargo y este mismo acto (T22).
- **`canon/registro-rotulos.tsv`:** fila `E10` nueva — colisiona con la referencia previa "E10 · EL SIMULADOR" (`forense/encargos/2026-08-14-ENLACE-2-adjudicacion-68-y-19.md:51`), resuelto vía D-6: el acto se declara `ACTO MAESTRA30-E10` en todo archivo que escribe, sin reclamar el token pelado (T25). `tests/check.py`: `_T22_ARCHIVOS_CONOCIDOS`/`_T25_ARCHIVOS_CONOCIDOS` ganan las dos entradas del encargo/nota de este acto — extensión mínima de perímetro por desviación mecánica del CI del propio acto, mismo precedente que `ADR-202`/`ADR-204`/`ADR-207`.

## §5 · ADR

Candidateó `ADR-208` contra el máximo re-derivado por conteo entero sobre el árbol al arrancar (`grep -c '^\*\*ADR-[0-9]\+' canon/gobernanza-v1_15.md` → `207`, sin huecos) → `208`. Sin colisión detectada al escribir contra `E8`/`E9` (concurrentes declarados por el encargo).

## §6 · Perímetro cerrado

`forense/hitoD-preregistro-v2_0.md` (emisión + enmienda de ficha `R2.1`) · `README.md:36` · `canon/estado-programa-v1_10.md` (§L0/§L5, Paso 2) · `canon/gobernanza-v1_15.md` (ADR-37, §5 deuda declarada, este ADR) · `canon/modelo-decision-v4_0.md` (dos citas T20) · `forense/firmas-pendientes.tsv` (FP-167) · `canon/registro-rotulos.tsv` (E10) · `tests/check.py` (whitelist T22/T25) · `forense/encargos/2026-08-26-E10-R21-ADJUDICA.md` (A.3 + CONSUMIDO) · esta nota.

**No tocado:** `R10.3` ni ninguna otra ficha; ningún archivo fuera de la lista anterior. El tier `[FUERTE]`/`v2` `[FUERTE como correlación]` de `R2.1` no se movió. El censo no se reabrió.

## §7 · Verificación final

```
python3 tests/check.py --baseline
```
`--baseline`: **VERDE** — sin entradas nuevas frente a `tests/baseline.json` más allá de las ya presentes al arrancar (T16 pre-existente por drift de FAIL/WARN vigente, ajeno a este acto).

## §8 · Contador

Hito D: **25 de 27 → 26 de 27**, re-derivado por parser (`_VEREDICTO_CANONICO`, T18/T20), `14D·4B·4A·2E·2C`. `R10.3` queda como la 27ª, deliberadamente sin tocar — cierre ético del programa.
