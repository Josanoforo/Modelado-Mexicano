# GEN2-FRONT-2 · verificación de un tercero, de punta a punta

P3 del encargo. Simula a alguien sin contexto previo del repositorio ni de
esta sesión: un clon limpio, aparte de la copia de trabajo, siguiendo
únicamente `docs/verificar.md` tal como quedó antes de esta corrección.

## Entorno del clon

```
git clone --local --no-hardlinks . /tmp/.../scratchpad/clon-verificacion-tercero
```

(`--local` fue ignorado porque el repo de origen es superficial —
`shallow`—; git hizo una copia completa igual.) HEAD del clon:
`02eadbc6b3bd66f32acec71cc929652fb2a6f933` (rama
`claude/new-session-punbef`, al día con `origin`). El clon no comparte
proceso ni variables con la sesión que redactó los documentos: es una
copia de disco aparte, ejecutada con los mismos binarios de Python que
trae este contenedor de NUBE (sin paquetes previos de `numpy`/`pandas`;
ver más abajo).

## Paso 1 · `python3 tools/corrida0.py status` contra el README

Salida completa (recortada a las claves que el README cita):

```
N_corridas_selladas=246
N_resultados_gen2_sellados=66582
N_resultados_gen2_adoptados_activos=72
celdas_validadas=219
celdas_validadas_prospectiva=20
celdas_validadas_retrospectiva=59
N_resultados_gen2_pendientes_adopcion=10
```

Coincide dígito a dígito con la tabla "Estado derivado" del README y con
lo que esta misma sesión ya había obtenido en la copia de trabajo antes de
clonar — dos corridas independientes del mismo comando, mismo commit,
mismo resultado.

## Paso 2 · identidad de un CALC citado en una nota

`docs/verificar.md` remite a la nota del piloto de ahorro
(`forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md`), que cita
`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001`.

```
$ sha256sum data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001/{spec.yaml,resultados.json,sello.json}
12bf26d8a8f7c6a84cea3ac5f3152dcd8bbcfe07eefd5bf9015107da26374888  spec.yaml
69ec9c6a21d259a76ae5617f2cff801e6165c351c750121125cc77e642f2d8c1  resultados.json
f412f9036dc43e2e0964893b28793f7a791968bc5d4217d2cbb54e1774f2c5a9  sello.json
```

`sello.json` declara internamente:

```json
{
  "spec.yaml": "12bf26d8a8f7c6a84cea3ac5f3152dcd8bbcfe07eefd5bf9015107da26374888",
  "resultados.json": "69ec9c6a21d259a76ae5617f2cff801e6165c351c750121125cc77e642f2d8c1"
}
```

Los tres hashes calculados coinciden exactamente con los declarados
(`spec.yaml` y `resultados.json` contra `sello.json`; `sello.json` contra
su sidecar `sello.sha256`, también coincidente). El control de identidad
que promete "Lectura rápida" funciona tal como está escrito, sin tocar
`data/raw`.

## Paso 3 · `python3 tools/corrida0.py verify <CALC-ID>` sin corpus

```
VERIFY CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001
  [1/5 SELLO] COINCIDE
  [2/5 SPEC.YAML] IDENTICO
  [3/5 INPUT AUSENTE] enif2021_csv, enif2021_fd_zip, enif2024_csv, enif2024_fd_xlsx (manifiesto; actual=None)
  [4/5 CONTEXTO] DISTINTO (inputs ausentes; commit_informativo distinto, FP-358 no gatea)
  [5/5 RESULT] NO-EJECUTABLE — ModuleNotFoundError: No module named 'numpy'
VERIFY: NO-EJECUTABLE (CONTEXTO=DISTINTO · RESULTADO=NO-EJECUTABLE)
```

Hallazgo no documentado antes en `docs/verificar.md`: sin `numpy`
instalado, `[5/5 RESULT]` falla por import antes de que el motor llegue a
notar la ausencia real de corpus. `pip install --break-system-packages
numpy` lo destraba un paso; el mismo `medidor.py` vuelve a fallar con
`ModuleNotFoundError: No module named 'pandas'`. Con ambos instalados el
veredicto seguiría siendo `NO-EJECUTABLE` porque los cuatro inputs de
`data/raw` siguen ausentes en este contenedor — el hallazgo es que el
mensaje de error que ve alguien sin esas dos librerías no distingue
"falta una dependencia de Python" de "falta el corpus", aunque el paso
`[3/5 INPUT AUSENTE]` ya lo había dicho correctamente una línea antes.
`docs/verificar.md` queda corregido con esta distinción. No se tocó
`requirements.txt` (fuera del perímetro de este acto — `tools/corrida0.py`
y sus dependencias son de otro dueño); queda una NC para quien mantenga
esa lista.

## Paso 4 · sello externo

`forense/sellos/manifiesto-sellos-2026-09-23.tsv` existe (344 filas);
ningún `.ots` ni `.tsr` lo acompaña en este corte — coincide con lo que
`docs/sello-externo.md` ya declara: sin egress al sellar, sólo corre el
mecanismo (c) (firma GPG del merge). Las columnas `firma_gpg_estado` /
`firma_gpg_keyid` están pobladas en la muestra revisada. No hay nada que
corregir aquí; el documento ya se anticipó a este caso.

## Paso 5 · `python3 tests/check.py --baseline`

Ver el resultado crudo pegado abajo (corrida completa desde el clon,
misma sesión, después de los pasos 1–4).

## AUTOCORRECCIÓN (25/sep/2026, PR #1126 aún abierto)

Los párrafos de arriba (Paso 3, "Qué no se corrigió") afirman que
`requirements.txt` **no declara** `numpy`/`pandas`. **Es falso.**
`requirements.txt` sí los declara (sección "ASTRA5-U3-POLITICA", junto con
`pyreadstat`, para los medidores de ENCUP/LAPOP). El error fue de lectura
propia: esta sesión sólo había leído `head -20 requirements.txt` antes de
escribir esa afirmación, y nunca corrió `pip install -r requirements.txt`
en el clon de verificación — instaló `numpy`/`pandas` sueltos con `pip
install`, sin pasar por el archivo que ya los tenía. El texto original de
arriba **no se reescribe** (append-only, `CONTRIBUTING.md` §3); esta
sección es la corrección fechada.

Lo que sigue siendo cierto y útil de este hallazgo: alguien que clona el
repo y va directo a `python3 tools/corrida0.py verify <CALC-ID>` sin haber
corrido `pip install -r requirements.txt` primero ve el mismo
`ModuleNotFoundError` y puede confundirlo con "falta el corpus". La
corrección real en `docs/verificar.md` queda como "corre `pip install -r
requirements.txt`", no como una receta de `numpy`/`pandas` sueltos.
`NC-260924-GEN2-FRONT-2-d095-01` se corrigió y se cerró en el mismo acto
(`forense/no-corrido.tsv`, `canon/L0/ADR-260924-GEN2-FRONT-2-d095-01.md`).

## Qué se corrigió

`docs/verificar.md`: enlace al reto público en la navegación; párrafo
nuevo bajo "Reproducción numérica" que distingue `NO-EJECUTABLE` por
dependencia de Python ausente de `NO-EJECUTABLE` por corpus ausente, con
la receta de instalación y esta nota como fuente.

## Qué no se corrigió (y por qué)

`requirements.txt` no declara `numpy` ni `pandas` aunque al menos un
`medidor.py` los importa. Es un defecto real, pero de otro dueño
(`tools/corrida0.py`, `requirements.txt`: ajeno a este acto, §9). Queda
registrado como NC con sucesor abierto, no se repara aquí.
