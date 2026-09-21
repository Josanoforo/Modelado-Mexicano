# Nota de cierre · ACTO `GEN2-TUBERIA-RES-LLAVE-1` · 21/sep/2026

Encargo archivado (A.3): `forense/encargos/2026-09-21-GEN2-TUBERIA-RES-LLAVE-1.md`
(0-bis `557399fc`, raíz de acto `5573`).
Anexo: `forense/encargos/DISENO-RES-CORR-llave-logica-v1_1.md`,
sha256 `a7b5e3adc6c789b8067fa3a97ff6b50dc4307454ac1453d91f3ea2b670aa0f06`,
**verificado** contra el declarado en la cabecera del encargo.
Modo `ABIERTO`. Compuerta: ninguna. **El PR no se fusiona: mesa fusiona.**

> **Adenda fechada (21/sep/2026, tras fusionar `main` en `8535a977`).** `PR #948`
> (`GEN2-TUBERIA-PREFLIGHT-CI-1`) fusionó primero y llevó `main` hasta `ADR-585`.
> Este acto **renumera su ADR de `583` a `586` y luego a `587`** —regla de la casa, renumera
> quien fusiona segundo— y sus dos jobs de CI **conviven**: `preflight-calc`
> (de #948) y `guardas-res` (de éste), los dos con su propio clonado y los dos
> exigidos por `check`. **Los cinco criterios se re-verificaron contra el merge
> real** —no contra un re-derivado hipotético— y **ninguno cambió**: §3 trae la
> salida nueva, medida contra `origin/main` `8535a977`.

---

## 1 · Qué se entregó

| Pieza | Entregable |
|---|---|
| **P0** | Encargo y anexo verbatim en `forense/encargos/`. Duplicado por CONTENIDO: **7 ramas remotas examinadas**, 0 lo archivan (A.13). Firma de mesa del §1 asentada verbatim en `forense/firmas-pendientes.tsv` como `FP-260921-GEN2-TUBERIA-RES-LLAVE-1-5573-01`, NACE FIRMADA (A.12). |
| **P1** | Espacio `cortes-C1` en `tools/pines_mesa.py::_ESPACIOS`. La llave traduce **210/210** consumidores, antes 204/210, sin colisiones. |
| **P2** | `data/corrida0/registro-res.tsv` (sólo-añadir) + `corrida0.py numera-res --escribe`, único escritor. `_asigna_ids` sólo lee. |
| **P3** | Columna `llave_logica` en `demanda-resultados.tsv`. |
| **P4** | `tools/resuelve_citas.py` + `data/corrida0/pines-sellados-resueltos.tsv`, 166 filas. Resolvedor expuesto: `resuelve_citas.py que-nombraba <token> <commit\|fecha>`. |
| **P5** | Los 4 canales de `tools/relevo_usos.py` casan por llave; `CORR` deja de ser citable. |
| **P6** | `tools/ci_guardas_res.py` (G1..G6) + `tests/test_guardas_res.py` (18 casos, por mutación) + job `guardas-res` en `verify.yml` con su propio clonado (D-23). |
| **P7** | Los cinco criterios, con comando y salida cruda: §3. |
| **P8** | 7 líneas en `forense/hallazgos.md`. `NC-0213` y `NC-0343` CERRADAS. |

**Decisiones de latitud, declaradas** (D-19):

1. El subcomando se llama **`numera-res`**, no `registro`: ese nombre ya lo
   tenía la vista de usos (`corrida0.py registro --escribe`). El encargo decía
   «al estilo de `registro --escribe`», y el estilo se conserva.
2. La llave de `cortes-C1` **no repite el nombre de la tabla**:
   `cortes-C1::formalidad`, no `cortes-C1::CORTES_C1::formalidad`. Es lo que
   mesa firmó, y la absorción se declara en una tabla explícita
   (`_RESTO_REDUNDANTE`), no a ojo.
3. La tabla de P4 lleva **una fila por par `(CALC, token)`**, no por archivo:
   `spec.md` y `spec.yaml` son la misma spec. Con la otra granularidad salían
   269 filas; con ésta, 166, que es la forma en que el anexo cuenta (~160).
4. El **contenido inicial del registro se siembra del derivado commiteado**,
   no de una re-derivación. Ver §2: re-derivar para sembrar habría renumerado
   justo lo que el acto existe para congelar.
5. `git fetch --unshallow` sobre el clon de trabajo (latitud explícita de
   `/acto` §4.4). Sin eso, la medición histórica de P4 daba 0 divergencias.

---

## 2 · La premisa que cayó, y qué se hizo en su lugar (§2, D-19)

El encargo se redactó contra `a61dd000`. Al abrir, `main` estaba en `483eeeb`
y traía **un slot `celda-D` nuevo** —
`GOB.gobierno_digital.encig2025.edad_x_escolaridad`— **cuyo derivado
`demanda-resultados.tsv` nunca se regeneró**.

Medido en un worktree de `origin/main` **sin ningún cambio de este acto**:

```
$ git worktree add --detach /tmp/wt-main origin/main
$ cd /tmp/wt-main && python3 tools/corrida0.py demanda
N_resultados_activos = 211
N_corridas_requeridas = 87
$ python3 tools/corrida0.py status | head -6
N_corridas_requeridas=87
N_resultados_activos=211
dependencias_numericas_legacy_activas=150
```

Es decir: **la deriva que este acto viene a cerrar estaba ocurriendo en vivo**,
y el esquema posicional habría corrido **36 ids** (`RES-0175`…`RES-0210`) en el
próximo `demanda` que alguien corriera. Es `NC-0343` otra vez, el mismo día.

Consecuencias, todas declaradas y ninguna ajustada para que cuadre:

- La numeración que el registro congela es **la del derivado commiteado de
  `main`** — la que sostiene hoy los 149 literales del código y las 116 citas
  `RES` de specs selladas. **210/210 preservada.** El slot nuevo recibe
  `RES-0211` por el paso explícito, y **cero** números existentes se mueven.
- Los criterios 2 y 3 sólo son interpretables contra **`main` re-derivado**,
  que es la única comparación que aísla este acto. Contra el derivado viejo de
  `main`, `status` cambia — y cambia igual **sin** este acto. Asentado en
  `NC-260921-GEN2-TUBERIA-RES-LLAVE-1-5573-01` para que mesa lo decida al
  fusionar; no se ajustó nada para evitar el número.

---

## 3 · Los cinco criterios, por comando

### Criterio 1 · la numeración de hoy se preserva 210/210

```
$ python3 tools/corrida0.py numera-res --escribe | head -8
SEMILLA: 210 pares llave->RES leidos de data/corrida0/demanda-resultados.tsv --
  el contenido inicial del registro ES la numeracion de hoy, no una renumeracion
slots_en_la_demanda = 211
llaves_vigentes_en_el_registro = 0
numeros_sembrados_de_la_numeracion_de_hoy = 210
numeros_nuevos = 1
numeros_heredados_por_alias = 0
llaves_retiradas = 0
  NUEVO     RES-0211  celda-D::GOB.gobierno_digital.encig2025.edad_x_escolaridad::…
```

Contraste contra el derivado de `origin/main`, slot por slot:

```
slots antes 210 ahora 211
numeracion preservada 210 / 210
cambiados {}
nuevos {'…GOB.gobierno_digital.encig2025.edad_x_escolaridad…': 'RES-0211'}
```

**CUMPLIDO.** Y contra `main` re-derivado, 36 filas difieren **sólo** en
`resultado_id`: son exactamente las que el esquema viejo habría renumerado.

### Criterio 2 · la vista difiere sólo en las 6 filas CIV y en la de `NC-0213`

Comparación contra `main` **re-derivado** (211 filas contra 211): **12 filas
sustantivas**, y **0 veredictos cambian en las 211**.

**Las 6 filas CIV — dejan de proponer el CALC equivocado:**

| fila | `calc_candidato` antes | ahora |
|---|---|---|
| `marco-M::CIV-M-01::L::L+corpus` | `CALC-R-CIV-M-02` | *(vacío)* |
| `marco-M::CIV-M-02::L::L+corpus` | `CALC-R-CIV-M-04` | *(vacío)* |
| `marco-M::CIV-M-04::L::L+corpus` | `CALC-R-CIV-M-10` | *(vacío)* |
| `marco-M::CIV-M-10::L::L+corpus` | `CALC-R-CIV-M-12` | *(vacío)* |
| `marco-M::CIV-M-12::L::L+corpus` | `CALC-R-CIV-M-13` | *(vacío)* |
| `procedencia::asignados_probabilidad::tramite.gobierno_digital.util_sin_coercion` | `CALC-R-CIV-M-01` | *(vacío)* |

Las seis seguían y siguen en `SIN-CANDIDATO`: no había adopción equivocada,
había **atribución** equivocada a la vista de quien la leyera.

**Las 4 filas de `NC-0213` — reciben el crédito de cobertura que les tocaba**
(`CALC-ENVIPE-0001` se añade a `calc_candidato`; veredicto
`LISTADO-PARA-MESA`, sin cambio):
`civico.denuncia.con_seguro::denuncia` · `::no_denuncia` ·
`civico.denuncia.sin_seguro::denuncia` · `::no_denuncia`.

**Las 2 filas de más**, que cambian **sólo** en la columna informativa
`canales_observados` y conservan veredicto, `calc_candidato` y pin:
`marco-M::CIV-M-01::R` gana `C3-CORRIDA`, `marco-M::DIN-M-01::R` la pierde.
Causa: `CORR` se resuelve a los slots que el grupo tenía al escribirse (D-r2).
Asentado en `NC-260921-GEN2-TUBERIA-RES-LLAVE-1-5573-02` para mesa.

**Las 4 filas de claves cambiadas quedan IDÉNTICAS** gracias a los alias
(`RES-0005`, `RES-0006`, `RES-0059`, `RES-0060`). Sin leerlos —probado en
vivo— `RES-0006` caía de `VETADO-POR-DECISION` a `SIN-CANDIDATO`.

### Criterio 3 · `status` y el contador quedan idénticos

```
$ diff status-MAIN3-REDERIVADO.txt status-MERGE.txt
26c26
< no_corrido_abiertas=175
---
> no_corrido_abiertas=176
```

Medido contra `origin/main` `8535a977` (con `#948` dentro), re-derivado.
**La única línea que difiere es `no_corrido_abiertas`**, +1 por las NC que este
acto abre (3) y cierra (2). **`dependencias_numericas_legacy_activas` es
IDÉNTICO: 150 = 150.**

Contra el derivado **commiteado** de `main` sí hay diferencia (149 → 150), y
**es de `main`, no de este acto** — el mismo worktree de `origin/main`
**sin ningún cambio de este PR**, re-derivado, da 150:

```
$ grep dependencias_numericas_legacy_activas \
    status-MAIN3-COMMITEADO.txt status-MAIN3-REDERIVADO.txt status-MERGE.txt
status-MAIN3-COMMITEADO.txt:dependencias_numericas_legacy_activas=149
status-MAIN3-REDERIVADO.txt:dependencias_numericas_legacy_activas=150
status-MERGE.txt:dependencias_numericas_legacy_activas=150
```

**CUMPLIDO contra la única comparación que aísla el acto.** El salto que la
cifra publicada de `main` muestra es una corrección de derivado viejo, y por
eso **este acto no se fusiona solo**: §5 y `NC-…-5573-01`.

### Criterio 4 · el test de oro pasa sin tocar el registro

Verificado que una lectura con un slot sin número **falla en voz alta** en vez
de numerar en silencio, y que el registro **no cambia de bytes**:

```
$ sha256sum data/corrida0/registro-res.tsv   # antes
2c611b98…1a1c87
$ python3 tools/corrida0.py demanda          # con el registro mutilado
PARO · REGISTRO-RES-INCOMPLETO: 1 slot(s) de la demanda no tienen numero …
  celda-D::GOB.gobierno_digital.encig2025.edad_x_escolaridad::…
Asignar numero es un paso EXPLICITO (firma de mesa 21/sep/2026): correlo con
    python3 tools/corrida0.py numera-res --escribe
Ningun comando de lectura escribe el registro.
$ sha256sum data/corrida0/registro-res.tsv   # despues
2c611b98…1a1c87
```

Y `tests/test_guardas_res.py::test_el_registro_del_arbol_conserva_la_numeracion_de_la_demanda`
lo deja cableado: el registro y la demanda no pueden separarse sin que el CI lo
diga.

### Criterio 5 · G1..G5 y la de biyección están en CI

`.github/workflows/verify.yml`, job **`guardas-res`** (nuevo, con su propio
clonado que trae la rama base — D-23), y `check` no aprueba sin él.

```
$ python3 tools/ci_guardas_res.py --base refs/remotes/origin/base
[NO-VERIFICABLE-AQUI] G1
    no se pudo leer data/corrida0/registro-res.tsv en 'origin/main' …
[PASA] G2
[PASA] G3
[PASA] G4
[PASA] G5
[PASA] G6
guardas_corridas = 6 · fallas = 0
```

`G1` sale `NO-VERIFICABLE-AQUI` —**no `PASA`**— porque la base todavía no tiene
registro: lo crea este PR. Desde el primer PR posterior al merge corren
completas. Asentado en `NC-…-5573-03`. Las seis quedan probadas **por
mutación** contra repos de git sintéticos y contra el árbol real.

---

## 4 · Lo que este acto NO hace

No escribe pines · no adopta nada · **no quita la ceguera de los 37 slots**
(son `CALC-SIN-PIN`; eso es trabajo de pines de mesa, decisión de contenido) ·
**no mueve el contador** · no renumera ningún id existente · no crea archivo de
alias aparte · no toca la numeración de `ADR` fuera de este acto · no fusiona
su propio PR · no toca `NC-0393` ni `NC-0426` (§10 del encargo).

---

## 5 · Por qué el ejecutor NO fusiona, pese a la autorización (21/sep/2026)

Mesa autorizó, por excepción explícita, que el ejecutor fusionara `PR #949`
tras `PR #948`, **condicionada** a que no saltara ninguna de las líneas cerradas
de PARO. Re-verificado contra el merge real (`origin/main` `8535a977`), **dos de
esas líneas se cumplen sólo en sentido interpretado, no literal**:

1. **«que `dependencias_numericas_legacy_activas` o cualquier cifra de `status`
   cambie».** La cifra que `main` **publica** pasa de **149 a 150**. Está
   probado por comando que el salto **no es de este acto** —`origin/main` sin
   ningún cambio de este PR, re-derivado, da 150— pero la cifra publicada sí se
   mueve, y ésa es la que mesa lee.
2. **«que la vista re-derivada cambie en alguna fila fuera de las 6 CIV y las de
   `NC-0213`».** Hay **dos filas más** (`marco-M::CIV-M-01::R`,
   `marco-M::DIN-M-01::R`) que cambian **sólo** en la columna informativa
   `canales_observados`, conservando veredicto, `calc_candidato` y pin.

Las dos estaban ya asentadas, **antes** de la autorización, en
`NC-260921-GEN2-TUBERIA-RES-LLAVE-1-5573-01` y `-02`, precisamente como
decisiones de mesa. **Reinterpretarlas ahora a favor de fusionar sería el
ejecutor concediéndose la firma que el encargo reserva a mesa** — y §2 de las
instrucciones es explícito: una premisa que toca una firma de mesa **PARA y se
reporta; nunca se ajusta el procedimiento para que cuadre**.

Todo lo demás está listo: rama al día con `main` fusionado, `ADR-586`
renumerado, los cinco criterios re-verificados con salida cruda, línea base
VERDE y `PR_HEAD_SINCRONIZADO`. **El merge es de un clic de mesa**, y basta con
que mesa diga que las dos líneas de arriba se leen como se midieron.
