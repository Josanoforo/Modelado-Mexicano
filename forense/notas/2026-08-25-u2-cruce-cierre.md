# Nota · ACTO U2-CRUCE — la primera validación externa material del programa

> | | |
> |---|---|
> | **ENCARGO** | `forense/encargos/2026-08-25-U2-CRUCE.md` (dirección, 24/ago/2026) — **CONSUMIDO** |
> | **FIRMA QUE EJECUTA** | `FP-70` opción **(a)** (`ADR-155(d)`) por su fila sucesora `FP-125` |
> | **FICHA CONGELADA** | `bbis-u2-cruce-v1_0.md` — Commit 1, `df3eeeb`, **sin un solo número estimado en su diff** |
> | **ADR** | `ADR-165` |
> | **VEREDICTO** | **Fila 1 de la escala `B-bis` — `PIPELINE CORROBORADO`**, propuesto, no firmado |
> | **EN UNA LÍNEA** | El pipeline reproduce a INEGI **exactamente**: los dos totales al peso, y los dos errores estándar de diseño a la **novena** cifra decimal |

---

## §0 · ARRANQUE — los cinco puntos, crudos

**1 · REPO.** Clon existente, `/home/pc0/Modelado-Mexicano`. Caja nueva: worktree `/home/pc0/mm-u2-cruce`, rama `u2-cruce`.

**2 · SHA, refrescado y reportado.** Al arrancar, `origin/main = 7848b97` (PR #331, `EVAL-COMPARTAMOS-LLAVE3`, 24/ago 23:56). Refrescado antes de escribir nada: **`origin/main = bd70166`** (PR #333, `BIBLIOTECARIO-56`, 25/ago 00:09) — la caja se reasentó ahí antes del Commit 1, y el candidato de ADR se re-derivó en consecuencia (§8).

**3 · `data/raw`.** Enlazado al corpus compartido, no descargado: `data/raw -> /home/pc0/mm-corpus/raw`, cubierto por `.gitignore:6`. **Cero descargas en todo el acto.**

**4 · ENTORNO, las tres partes de `A.2`, sin colapsar:**

| parte | comando | salida |
|---|---|---|
| variable | `${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE+x}` | **`sin_variable`** (no definida) → **UBUNTU local**. `uname`: `Linux 6.18.33.2-microsoft-standard-WSL2` |
| sonda de red | `curl … https://www.inegi.org.mx/` | **`HTTP 200` en 0.579609 s** |
| corpus montado | `ls data/raw/ 2>/dev/null \| head -1` | **`2005trim1_csv.zip`** · 321 entradas → **no vacío, no hay `PARO`** |

La sonda se corrió porque `A.2` la exige como firma, **no** porque el acto la use: no hay descarga (§3, y `FP-70` lo dice — el insumo ya está adquirido).

**5 · ESPEJO.** Nada del espejo.

**Concurrencia.** `origin/main` se movió **dos veces** durante este acto: `7848b97 → bd70166` en el arranque (§ARRANQUE 2) y `bd70166 → 8aff7cb` mientras se escribía el cierre (`ACTO SELLA-AGO25-E`, `PR #334`), lo que obligó a fusionar y renumerar — ver §8. `pgrep -af claude` sólo ve el propio shell de esta sesión — ya está medido que no detecta sesiones de agente concurrentes. El detector que sí sirve es el remoto: `origin/main` se movió **una vez** durante el arranque (`7848b97 → bd70166`), y `PR #330` (`ADV1-M3`, `codex/scoring-adv1-m3`) sigue abierto. Colisión de `ADR`/fila esperada y tratada por la regla de la casa: renumera quien fusiona segundo.

---

## §1 · Verificación de existencia — los tres insumos, `A.1`, una invocación por `--id`

Las tres respuestas de `tests/manifiesto.py` se mantienen separadas (`AUSENTE` · raíz-no-configurada · hash-discordante): **ninguna aplica**, las tres son `COINCIDE`.

```
$ python3 tests/manifiesto.py --verifica --id enasic2022_ipe_cv_ee_ic
enasic2022_ipe_cv_ee_ic [data_raw]: COINCIDE -- sha256 y tamaño (51724 bytes) verificados contra data/manifiesto.yaml
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0

$ python3 tests/manifiesto.py --verifica --id enasic2022_bd_csv_zip
enasic2022_bd_csv_zip [data_raw]: COINCIDE -- sha256 y tamaño (2289078 bytes) verificados contra data/manifiesto.yaml
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0

$ python3 tests/manifiesto.py --verifica --id enasic2022_fd_xlsx
enasic2022_fd_xlsx [data_raw]: COINCIDE -- sha256 y tamaño (266488 bytes) verificados contra data/manifiesto.yaml
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

`FP-70` se leyó **íntegra** del tablero antes de nada, con lector de 9 columnas, y su fila sucesora también. Estado al arrancar: las dos `FIRMADA` con `ejecutada_en` **vacío**.

**Defecto de referencia encontrado al leerlas, y corregido en este acto.** El campo `firmada_en` de `FP-70` dice, verbatim, *«Fila sucesora `FP-124` abierta `FIRMADA`…»*. **Hoy `FP-124` es otra fila** — la del `GO` sobre las cinco fuentes de eventos (`F5`), y además ya está `ejecutada_en = ADR-158`. La sucesora real de `FP-70` es **`FP-125`**, única fila del tablero que se declara *«Sucesora de FP-70»*: nació como `FP-124` en `299e2e8` (`SELLA-AGO24-C-v2`) y la cascada de renumeración por colisión la corrió a `FP-125`, sin actualizar el texto de `FP-70`. `ADR-155(d)` sí dice `FP-125`, correcto. Quien hubiera escrito a ciegas donde el texto de la fila apunta habría pisado una fila cerrada de otro acto. Se corrige el texto de `FP-70` (§7).

---

## §2 · La ficha congelada — qué se cerró antes de estimar

Todo el diseño vive en `bbis-u2-cruce-v1_0.md`, Commit 1, `df3eeeb`. Lo que este acto necesita repetir aquí es sólo lo que la corrida usa:

* **Estimandos.** `U2-E1` = `Población total` y `U2-E2` = `Sí requirió apoyo o cuidados`, hoja `INDICADORES` filas 2 y 3 del IPE oficial (§1 de la ficha los cita celda por celda). Los dos con `Unidad_Obs = Población`, `Parametro = Total`, `Niv_Conf = 90`.
* **Reserva (i), resuelta.** Se convierte el **lado oficial** con `IC95 = Estimación ± 1.9599639845400536 × ErrorEst`. Congelados en la ficha: `U2-E1` → `[125 341 905.029395 , 132 372 870.970605]`; `U2-E2` → `[56 751 384.429881 , 60 437 557.570119]`.
* **Reserva (ii), resuelta.** Factor **`FAC_HOG` de `TCSDEMPO.csv`**, sin reescalar. Lo que fija la unidad no es el nombre del factor sino la unidad de fila del archivo — y el descriptor etiqueta *«FACTOR HOGAR DE EXPANSIÓN»* también a `FAC_ELE`, que es de persona elegida y tiene otro rango, así que la etiqueta no sirve de oráculo.
* **Universo.** `TCSDEMPO.csv` menos los renglones con `EDAD = '99'` (*«No sabe, en personas menores de 15 años»*, el único código que corresponde a la exclusión que el renglón oficial declara).
* **Criterio, uno solo.** **El punto propio cae dentro del `IC95` oficial.**
* **Escala `B-bis`,** cinco desenlaces con precedencia: `REFUTADO` manda sobre todos, luego `PRUEBA DÉBIL`, luego `NO CONCLUYENTE POR OPERACIONALIZACIÓN`, luego `CORROBORADO · DISCREPANCIA ACOTADA`, y por último `CORROBORADO`.
* **Diagnóstico que no adjudica:** razón `|EE_propio − EE_oficial| / EE_oficial` contra `0.15`, umbral **heredado** del pre-registro de `U2/EV-1` §5, no inventado aquí.
* **Comprobación (a), pre-declarada con valor exacto:** la diferencia entre sumar todos los renglones y sumar el universo debe dar **`21 090`**.

---

## §3 · La vía — y la desviación respecto de `produce.py`, medida y no supuesta

`produce.py::taylor_distribution` **no puede** producir este estimando: su salida es una distribución de **proporciones**, y linealiza la varianza de una **razón** centrando cada conglomerado por `p` (`psu_z += w × (1[y=c] − p)`, líneas 105-107). Un total no es una razón. Se usó por tanto el **mismo estimador de conglomerados últimos** en su forma de total — única diferencia `w·y` en vez de `w·(1[y=c] − p)`; misma partición por `EST_DIS`, mismos conglomerados `UPM_DIS`, mismo factor `m/(m−1)`, mismo trato de estratos con una sola UPM.

El script vive en `scratchpad` (dentro del perímetro; `tools/` está fuera). Para que no dependa del scratchpad, va **verbatim**, y su `sha256` es `3b36e1c46bf06985490182f10cea05a13b8dd676ef8eff6d53d693fe5ea81884`:

```python
#!/usr/bin/env python3
"""U2-CRUCE · estimador de TOTAL bajo diseno estratificado por conglomerados ultimos.

Congelado por forense/bbis-u2-cruce-v1_0.md (Commit 1, df3eeeb). Unica diferencia
con tools/curador_registro/produce.py::taylor_distribution: donde produce.py
acumula w*(1[y=c] - p) porque estima una RAZON, aqui se acumula w*y porque el
estimando es un TOTAL. Particion, factor m/(m-1) y trato de estratos con una sola
UPM se conservan identicos.

Convenciones fijadas en la ficha, no aqui:
  1. m_h y el conjunto de UPM se cuentan sobre la muestra COMPLETA del archivo,
     no sobre el dominio; una UPM sin miembros del dominio aporta z = 0.
  2. Estratos con una sola UPM se reportan con lista y conteo, no se colapsan.
  3. Sin correccion por poblacion finita, sin recalibracion, sin recorte de pesos.
"""
import csv, io, math, sys, zipfile
from collections import defaultdict

Z95 = 1.9599639845400536   # cuantil normal exacto de dos colas al 95 %
ZIP = "/home/pc0/mm-corpus/raw/enasic2022/enasic_2022_bd_csv.zip"
BANDERAS_E2 = ("PN_CDISC", "PN_C0005", "PN_C0617", "PN_C60MA", "PN_CETEM")


def leer(miembro):
    with zipfile.ZipFile(ZIP) as z, z.open(miembro) as raw:
        return list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig",
                                                    errors="strict", newline="")))


def total_con_diseno(filas, y_de, w="FAC_HOG", h="EST_DIS", i="UPM_DIS"):
    """Total ponderado y su EE por conglomerados ultimos.

    `filas` es la muestra COMPLETA (convencion 1); `y_de(fila)` devuelve 0.0
    para lo que queda fuera del dominio.
    """
    Y = 0.0
    z = defaultdict(float)                 # (estrato, upm) -> suma w*y
    upms = defaultdict(set)                # estrato -> {upm}  (muestra completa)
    for f in filas:
        peso = float((f.get(w) or "").strip())
        est = (f.get(h) or "").strip()
        upm = (f.get(i) or "").strip()
        if not est or not upm or not math.isfinite(peso) or peso <= 0:
            raise ValueError("DISENO_O_PESO_INVALIDO")
        upms[est].add(upm)
        yv = y_de(f)
        if yv:
            Y += peso * yv
            z[(est, upm)] += peso * yv

    var, singleton = 0.0, []
    for est, ups in upms.items():
        m = len(ups)
        if m < 2:
            singleton.append(est)
            continue
        vals = [z[(est, u)] for u in ups]
        media = sum(vals) / m
        var += (m / (m - 1)) * sum((v - media) ** 2 for v in vals)
    ee = math.sqrt(max(0.0, var))
    return {
        "Y": Y, "EE": ee,
        "CV_pct": (ee / Y * 100.0) if Y else float("nan"),
        "ic95": (Y - Z95 * ee, Y + Z95 * ee),
        "n_estratos": len(upms),
        "n_upm": sum(len(u) for u in upms.values()),
        "singleton": sorted(singleton),
    }
```

*(el resto del archivo es `main()`: aplica `y1`/`y2` según §6 de la ficha, imprime los dos estimandos contra los oficiales y las comprobaciones (a) y (b). Su salida íntegra es §4.)*

---

## §4 · La corrida — salida verbatim, primera y única

```
TCSDEMPO.csv: 21776 renglones-persona · THOGAR.csv: 6508 renglones-hogar

n(U, EDAD != '99')            = 21775 renglones-persona   (excluidos por EDAD=='99': 1)
n(U2-E2, dominio 'requirio')  = 9864 renglones-persona
estratos = 148 · UPM = 896 · estratos con una sola UPM = 0 

===== U2-E1 · Poblacion total =====
  PROPIO   Y = 128,836,298.000000   EE = 1,793,474.858412   CV = 1.3920571192 %
           IC95 propio  = [125,321,151.870334 , 132,351,444.129666]
  OFICIAL  Y = 128,857,388   EE = 1,793,646.719192   CV = 1.3919626550 %
           IC95 oficial = [125,341,905.029395 , 132,372,870.970605]
  CRITERIO punto propio dentro del IC95 oficial: SI
  dif absoluta punto = -21,090.000000   dif relativa = -0.0163669312 %
  (c) razon EE = |1,793,474.858412 - 1,793,646.719192| / 1,793,646.719192 = 0.0000958164  contra 0.15 -> DENTRO

===== U2-E2 · Si requirio apoyo o cuidados =====
  PROPIO   Y = 58,594,471.000000   EE = 940,367.570352   CV = 1.6048742386 %
           IC95 propio  = [56,751,384.429881 , 60,437,557.570119]
  OFICIAL  Y = 58,594,471   EE = 940,367.570352   CV = 1.6048742386 %
           IC95 oficial = [56,751,384.429881 , 60,437,557.570119]
  CRITERIO punto propio dentro del IC95 oficial: SI
  dif absoluta punto = +0.000000   dif relativa = +0.0000000000 %
  (c) razon EE = |940,367.570352 - 940,367.570352| / 940,367.570352 = 0.0000000000  contra 0.15 -> DENTRO

===== comprobaciones estructurales (no adjudican) =====
  (a) Sigma FAC_HOG todos = 128,857,388.000000
      Sigma FAC_HOG en U  = 128,836,298.000000
      excluido            = 21,090.000000   esperado pre-declarado = 21090   dif = +0.000000
  (b) Sigma FAC_HOG sobre THOGAR = 38,785,744.000000 hogares
      personas/hogares = 3.322287   rango pre-declarado 3.3-3.8 -> DENTRO
```

**Ninguna segunda corrida, ninguna variante.** La cláusula §12 de la ficha se cumple literalmente: éste es el primer resultado del procedimiento y es el que se reporta.

**Ampliación de la comprobación (a), que no es una segunda corrida.** La comprobación (a) ya calculaba el total sobre **todos** los renglones; la corrida sólo imprimía su punto. Un script auxiliar importa el estimador **sin tocarlo** (`sha256` idéntico) e imprime los campos restantes **del mismo objeto ya calculado**:

```
=== comprobacion (a), campos completos: total sobre TODOS los renglones ===
  Y  = 128,857,388.000000      oficial = 128,857,388      dif = +0.000000
  EE = 1,793,646.719192269   oficial = 1,793,646.719192270   dif = -0.000000001
  CV = 1.3919626550 %   oficial = 1.3919626550 %   dif = +0.000000000018
  IC95 propio = [125,341,905.029395 , 132,372,870.970605]
  razon EE = 0.000000000000

=== el unico renglon con EDAD=='99' ===
  LLAVESDE=27603103  EST_DIS=0037  UPM_DIS=00276  FAC_HOG=21090
  SEXO=2  PAREN=3  EDAD='99'
  banderas de la Seccion 4: PN_CDISC='2' · PN_C0005='' · PN_C0617='' · PN_C60MA='' · PN_CETEM=''
  -> entra al dominio U2-E2? NO

=== distribucion de EDAD en los codigos de no-respuesta ===
  EDAD=='98': 12 renglones · suma FAC_HOG = 118,305
  EDAD=='99': 1 renglones · suma FAC_HOG = 21,090
```

---

## §5 · Qué dicen estos números

### 5.1 · El criterio pre-declarado, aplicado

| estimando | punto propio | `IC95` oficial | ¿dentro? | dif. relativa | diagnóstico (c) EE |
|---|---|---|---|---|---|
| **`U2-E1`** Población total | `128 836 298` | `[125 341 905.03 , 132 372 870.97]` | **SÍ** | **−0.0164 %** | `0.0000958` ≤ 0.15 · **dentro** |
| **`U2-E2`** Sí requirió apoyo o cuidados | `58 594 471` | `[56 751 384.43 , 60 437 557.57]` | **SÍ** | **+0.0000000000 %** | `0.0000000` ≤ 0.15 · **dentro** |

**Los dos satisfacen el criterio. Los dos diagnósticos de `EE` caen dentro del umbral heredado.** Por la escala `B-bis` de la ficha, eso es la **fila 1 · `PIPELINE CORROBORADO`**, salvo que una fila de mayor precedencia aplique. Se revisan las tres, una por una, en §5.4.

### 5.2 · Lo que el número exacto significa, y es más fuerte que el criterio

El criterio pedía caer dentro de un intervalo de ±2.7 %. Lo que ocurrió es de otro orden:

* **`U2-E2` reproduce al peso.** Nuestro total es `58 594 471` y el oficial es `58 594 471`. **Diferencia: cero.** Y el error estándar propio es `940 367.570352` contra `940 367.570351719` — **coincide en las seis decimales publicadas**.
* **`U2-E1`, bajo el universo de la comprobación (a), reproduce al peso y el `EE` a la novena decimal.** `128 857 388.000000` contra `128 857 388`, diferencia cero; `EE = 1 793 646.719192269` contra `1 793 646.719192270`, diferencia **`−1 × 10⁻⁹`** — ruido de punto flotante, no discrepancia.

Reproducir el punto es reproducir una suma. **Reproducir el error estándar de diseño a nueve decimales es otra cosa:** significa que el estimador de varianza de este programa —partición por `EST_DIS`, conglomerados últimos `UPM_DIS`, factor `m/(m−1)`, sin corrección por población finita, sin ajuste por calibración— **es exactamente el que el INEGI usó** para publicar esas cifras. Eso no se podía saber antes de correr: §10 de la ficha lo listaba explícitamente como una de las cuatro cosas que el acto *no* podría concluir, porque *«el archivo oficial publica el número, no la fórmula»*. La coincidencia a nueve decimales la resuelve por identificación numérica, que es más fuerte que la cita que faltaba.

### 5.3 · El hallazgo material: la etiqueta del renglón oficial no describe el número que publica

Esto es lo que la comprobación (a) atrapó, y es un defecto **del archivo oficial**, no del pipeline:

* El renglón `U2-E1` se titula, verbatim: *«Población total **(Se excluyen 21,090 casos que no especificaron la edad de la población menor de 15 años)**»*.
* La suma sobre el universo que esa exclusión define —`EDAD ≠ '99'`— da **`128 836 298`**.
* La suma **sin** excluir nada da **`128 857 388`**, que es **exactamente** la cifra publicada.
* La diferencia es **`21 090.000000`**, **exactamente** el valor pre-declarado en la ficha antes de correr.

Es decir: **el `Población total` publicado incluye los casos que su propia etiqueta declara excluidos.** Y hay un segundo dato que la ampliación de (a) deja a la vista: los *«21 090 casos»* del texto oficial **no son 21 090 registros — son uno solo**, `LLAVESDE 27603103`, cuyo `FAC_HOG` vale precisamente `21 090`. El archivo oficial llama *«casos»* a un conteo **expandido**, no muestral. Las dos cosas juntas explican por qué la etiqueta se lee mal: describe una exclusión en escala de población que, además, no está aplicada.

Para `U2-E2` la etiqueta es **inocua**: el único renglón afectado trae `PN_CDISC = '2'` y las otras cuatro banderas en blanco, así que no entra al dominio de `U2-E2` bajo ninguna lectura — de ahí que `U2-E2` reproduzca exacto tanto excluyéndolo como sin excluirlo.

**Lo que este hallazgo NO es.** No es una corrección al INEGI ni una impugnación de sus cifras: `128 857 388` es un total poblacional coherente con el resto de su publicación, y la discrepancia está enteramente en la glosa del renglón. Este acto lo registra porque **cualquiera que use ese archivo como referencia de precisión reproducirá 128 836 298 si obedece la etiqueta**, y creerá que su pipeline falla. Es exactamente el defecto que una validación externa existe para encontrar.

### 5.4 · Las tres filas de mayor precedencia, descartadas una por una

**Fila 4 · `REFUTADO · DEFECTO DE PIPELINE`** — exige `Ŷ₁` **fuera** de su `IC95` oficial. Está dentro, con holgura de dos órdenes de magnitud (`−0.0164 %` contra un semiancho de `±2.73 %`). **No aplica.**

**Fila 5 · `PRUEBA DÉBIL`** — exige descubrir, al correr, que el criterio **no podía fallar**. No es el caso, y se justifica en vez de afirmarse: lecturas plausiblemente equivocadas del mismo ZIP caen fuera del intervalo por órdenes de magnitud, no por poco — `THOGAR`/`FAC_HOG` da `38 785 744` (hogares, comprobación (b)), `TPER_ELE`/`FAC_ELE` expande sólo personas elegidas de 15 a 60 años, y `TVIVIENDA`/`FAC_VIV` expande viviendas. El criterio discrimina. **No aplica** — pero ver la reserva de §5.5, que es real y no se tapa.

**Fila 3 · `NO CONCLUYENTE POR OPERACIONALIZACIÓN`** — exige `Ŷ₂` fuera. Está dentro, y además **exacto**. Eso resuelve por la vía de los hechos la reserva que §6 de la ficha había dejado escrita: la operacionalización derivada de `U2-E2` —disyunción de las cinco banderas `PN_CDISC`/`PN_C0005`/`PN_C0617`/`PN_C60MA`/`PN_CETEM`— **es** la definición del INEGI para *«Sí requirió apoyo o cuidados»*. Un total que coincide al peso sobre `9 864` renglones-persona de `21 776` no es compatible con una operacionalización distinta. **No aplica.**

**Fila 2 · `CORROBORADO · DISCREPANCIA ACOTADA`** — exige razón de `EE` > `0.15` en al menos uno. Las dos razones son `0.0000958` y `0.0000000`. **No aplica.**

→ **Veredicto propuesto: fila 1 · `PIPELINE CORROBORADO`.**

### 5.5 · La reserva, escrita y no maquillada — el criterio elegido fue más laxo que la evidencia

El criterio de §7 de la ficha **absorbió sin inmutarse una discrepancia determinista de 21 090 personas** en `U2-E1`: la dio por buena porque caía dentro de un intervalo de ±3.5 millones. Quien leyera sólo el criterio concluiría *«reprodujo»* y no vería nada más. Lo que localizó la discrepancia —y la explicó entera— fue la **comprobación (a)**, que la ficha había declarado explícitamente como *«no adjudica»*.

Es una lección sobre elección de criterio, y se escribe aquí porque el acto la pagó: **contra un valor publicado con `CV` de 1.4 %, un criterio de pertenencia a intervalo es del orden de 170 veces más laxo que la precisión que el propio procedimiento alcanza.** Las tres razones que la ficha dio para elegirlo (§7) siguen siendo correctas —es el más exigente de los dos que el encargo ofrecía, aísla el confundido metodológico de la varianza, y sí puede fallar—, pero las tres razonaban contra la *otra* opción del encargo, no contra un criterio de reproducción exacta que el encargo no ofrecía. El criterio **no se cambia** ahora: adjudicar con un criterio elegido después de ver el dato es precisamente lo que el pre-registro existe para impedir. Se adjudica con el criterio congelado, y la reserva queda escrita para el acto que fije el criterio de la siguiente validación externa.

**Contraparte de `A-bis`, aplicada.** El veredicto es **propuesto**, no firmado por el ejecutor. Y se anota el dato que la exige: **nuestro `IC95` propio de `U2-E1` no está contenido** en el oficial (`[125 321 151.87 , 132 351 444.13]` contra `[125 341 905.03 , 132 372 870.97]` — se traslapan casi enteramente, pero el propio está desplazado 20 753 a la izquierda, que es el mismo `21 090` de §5.3 propagado). Bajo el universo de la comprobación (a) los dos intervalos **coinciden a la sexta decimal**.

---

## §6 · Escalas y universo, como la ficha los declaró

Todas las cantidades de §4 y §5 están en **personas** (`Ŷ`, `EE`) o son **adimensionales** (`CV` en %, razón de `EE`); `n` está en **renglones-persona**. **Nada de este acto se compara contra la θ sellada de `familismo_obligacion`** (0.6933, una proporción sobre `TPER_ELE`): escalas distintas, sin función de enlace declarada — `A-bis` regla 3.

**Estampa de universo (`A.10`).** Universo de la medición: `TCSDEMPO.csv` del ZIP `sha256 8a5e8c5e…`, 21 776 renglones-persona, 181 columnas, 148 estratos, 896 UPM distintas (idéntica estructura de diseño en `THOGAR.csv` y `TVIVIENDA.csv`, verificado: los tres traen exactamente el mismo conjunto de UPM), 0 estratos con una sola UPM. Universo de la comparación: las **2** filas con contenido de las 337 de la hoja `INDICADORES` del IPE oficial — el archivo entero, no una muestra.

**`A.13` — los negativos de este acto, con los archivos que el comando examinó.** Son dos, y los dos van con su conteo: *(1)* «`produce.py` no puede producir un total» — derivado de leer **1 archivo**, `tools/curador_registro/produce.py`, 279 líneas, función `taylor_distribution` completa (líneas 56-151); no es un `grep` que no encontró algo, es la lectura de la única función candidata. *(2)* «ningún estrato tiene una sola UPM» — derivado del barrido de los **21 776 renglones** de `TCSDEMPO.csv`, 148 estratos evaluados, lista de singletons vacía e impresa como tal en §4.

---

## §7 · Cascada

**`forense/firmas-pendientes.tsv`:**

* **`FP-125`** → `ejecutada_en = ADR-165`. Es la fila que este acto ejecuta.
* **`FP-70`** → `ejecutada_en = ADR-165` (el encargo lo pide por nombre), **y** corrección del texto de su `firmada_en`: la referencia a la fila sucesora decía `FP-124` y la sucesora real es `FP-125` (§1). Se corrige la referencia, no el contenido de la firma.
* **Fila nueva `FP-135`, `ABIERTA`** (`A.12`): el veredicto de §5.4 es **propuesto** y mueve un contador; la firma de mesa que pide es la de archivarlo y la de qué hacer con el hallazgo de §5.3.

**`canon/gobernanza-v1_15.md`:** `ADR-165`, con el veredicto, el hallazgo y la reserva de criterio.

**`canon/estado-programa-v1_10.md`:** conteo de `ADR` `163 → 164` (`L0`); contador nuevo **`Validaciones externas materiales: 1 de 1`**, población de conteo propia que nace con este acto tal como el encargo la declara bajo `v2.3`; recifrado de la suite.

**Contadores de medición sobre México que este acto mueve: cero.** No archiva ninguna corrida del Hito D (`18 de 27` no se mueve), no estima ningún coeficiente (`0/15` no se mueve), no re-etiqueta ningún resultado sellado, no toca `milpa/` ni el pre-registro del Hito D.

**Fuera de perímetro, declarado y no ejecutado.** `forense/hallazgos.md` **no** está en el `PERÍMETRO` del encargo, y el encargo dice *«Fuera de la lista: PARA»*. Los dos hallazgos de este acto —la etiqueta del renglón oficial (§5.3) y la referencia obsoleta a `FP-124`, ya corregida en el propio tablero (§1)— viven por tanto en esta nota y en `ADR-165`, **no** en el registro de hallazgos. Queda nombrado como deuda de un acto sucesor con ese archivo en su perímetro, no como omisión silenciosa.

---

**Suite, medida y no supuesta — y re-medida tras la fusión.** Base de la caja **antes de escribir una sola línea**, sobre `bd70166`: `19 FAIL · 147 WARN`, `LÍNEA BASE: VERDE` — coincidía exactamente con lo que `canon/estado-programa-v1_10.md` declaraba al arrancar, así que este acto no heredó desfase. Sobre esa base el acto cerró en `19 FAIL · 146 WARN`. Después `origin/main` volvió a moverse (`ACTO SELLA-AGO25-E`, `PR #334`, que palomea seis filas del tablero y baja el `WARN` de `T22` por su cuenta), se fusionó, y la cifra se **volvió a medir** en vez de aritmetizarse:

```
════════════════════════════════════════════════════════════════════════
  19 FAIL · 140 WARN
════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
  (5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
────────────────────────────────────────────────────────────────────────
```

El **`−1` de WARN sobre el árbol fusionado (141 → 140) es de este acto y de una sola causa**: `T22` — dos WARN menos porque `FP-70` y `FP-125` reciben `ejecutada_en`, uno más porque nace `FP-135` `ABIERTA`, que es exactamente lo que `A.12` existe para hacer visible. `T03` no se mueve (55). **`FAIL` sin cambio, y las seis categorías son las mismas** (`T09:8 · T05:5 · T02:2 · T06:2 · T08:1 · T11:1`).

**Los `FAIL` que este acto sí produjo, y cerró dentro de sí mismo** — se declaran en vez de omitirse, porque el neto en cero los haría invisibles. Fueron cuatro, de tres clases:

1. **`T15`, antes de la fusión** — el recifrado de `ADR` deja desincronizadas las citas vivas de `canon/`; se resincronizaron las dos vivas y la tercera, que dejó de ser vigente, recibió su marca de cita histórica.
2. **`T25`, dos veces** — las dos por rótulos pelados de la familia que `D-6`/`ADR-128` prohíbe. La primera por los rótulos de la ficha (§9). **La segunda porque el bloque que narraba esa misma corrección los reproducía verbatim**: un test de rótulos no distingue narrar un rótulo de usarlo, y la corrección volvió a crear lo que corregía.
3. **`T15` otra vez y `T16` una vez, después de la fusión** — la renumeración a `ADR-165` dejó dos citas de conteo desfasadas (una en `estado §Registro de artefactos`, otra dentro de la propia cascada de este ADR), y la cifra de suite que `ACTO SELLA-AGO25-E` había escrito **correcta al escribirse** quedó superada por este acto: recibió `{cita-historica}`, que es el mecanismo previsto, en vez de reescribirse — sobreescribirla falsearía lo que ese acto midió.

Cifra declarada = núcleo sin `T16` (`CHECK_SELFCHECK_CHILD=1 python3 tests/check.py`), sin `--freeze` en ningún momento.

---

## §8 · Numeración — la colisión anunciada ocurrió, dos veces

`ADR` y `FP` se candidatearon contra el máximo re-derivado **por regex sobre el árbol** (`grep -oE '^\*\*ADR-[0-9]+' | grep -oE '[0-9]+' | sort -n -u`), **no** por `sort -t- -k2 -n`, que en este archivo parte en el primer guion y devuelve un máximo falso. Sobre `bd70166`: máximo `163`, 163 únicos, sin huecos → candidato `ADR-164`; máximo de tablero `134` → `FP-135`.

**Y la colisión ocurrió.** `ACTO SELLA-AGO25-E` (`PR #334`) fusionó primero y tomó `ADR-164`. Por la regla de la casa —*renumera quien fusiona segundo*— este acto pasa a **`ADR-165`**, re-verificado sobre el árbol ya fusionado: **165 únicos, máximo 165, sin duplicados ni huecos**. `FP-135` **no** colisionó: ese acto abrió hasta `FP-134`, y el tablero fusionado tiene 137 filas, 9 columnas cada una, sin ids duplicados y con el conteo de comillas dobles cuadrando exactamente (`87` mías + `88` suyas sobre una base de `87` → `88`), es decir cero corrupción.

**La renumeración se hizo con anclas, no con buscar-y-reemplazar.** Un `ADR-164` global habría pisado las referencias del acto ajeno, que ahora vive en el mismo archivo: el renombrado se acotó al rango de líneas del bloque propio y a las tres filas propias del tablero, y se verificó después que **ninguna** fila ajena cambiara (`ADR-164` en el tablero: `0` antes de la fusión en `origin/main` y `0` después — ese acto no lo cita ahí).

**`origin/main` se movió dos veces durante este acto** (`7848b97 → bd70166` en el arranque, `bd70166 → 8aff7cb` mientras se escribía el cierre). Es el detector real de concurrencia de esta caja: `pgrep -af claude` sólo ve el propio shell.

---

## §9 · Enmienda del Commit 3 — la ficha estaba mal en un punto

**El defecto.** La ficha del Commit 1 nombró sus dos estimandos con la letra `E` seguida de un dígito, sin prefijo de espacio. Eso es un rótulo **pelado** de una familia que `D-6` (`ADR-128`, `ACTO SELLA-ADV`, 20/ago/2026) prohíbe crear desde ese día, y `T25` marcó `FAIL` los dos archivos nuevos de este acto — que es exactamente para lo que ese test existe. El defecto es del ejecutor y de la ficha, no del encargo.

**Cómo se corrige.** Con un tercer commit que **lo dice**, tal como el encargo lo previó (*«Si la ficha estaba mal: tercer commit que lo diga; nunca hacia atrás»*), no arreglándolo en silencio dentro del Commit 2. Los rótulos pasan a **`U2-E1`** y **`U2-E2`**, prefijo de espacio del propio acto. Nada más cambia: ni un estimando, ni un intervalo, ni el criterio, ni la escala, ni una cifra.

**Por qué no viola §12 ni la congelación de la ficha.** La cláusula protege contra mover la *especificación* después de ver el resultado. Un rótulo no es especificación, y `D-6` es canon: manda sobre la auto-congelación de una ficha. Los rótulos viejos no se reproducen en su forma pelada en ningún archivo de este acto, a propósito — para un test de rótulos, mención y uso no se distinguen, así que escribirlos volvería a crear el defecto.

**Trazabilidad, y es la parte que importa.** El script imprimía los rótulos en **cuatro** cadenas. Se produjo una `v2` que cambia **sólo esas cuatro** (`sha256 3b36e1c46bf06985490182f10cea05a13b8dd676ef8eff6d53d693fe5ea81884` → `f25e84a995e264313aa5835bf283b6b570772b3802ce770d10142a8703988bc0`) y se volvió a correr. El diff entre las dos salidas es **de tres líneas, todas de rótulo**:

| # | línea de la corrida 2, **verbatim** | qué cambió respecto de la corrida 1 |
|---|---|---|
| 1 | `n(U2-E2, dominio 'requirio')  = 9864 renglones-persona` | el token del rótulo, y dos espacios de alineación |
| 2 | `===== U2-E1 · Poblacion total =====` | el token del rótulo |
| 3 | `===== U2-E2 · Si requirio apoyo o cuidados =====` | el token del rótulo |

*(El diff se presenta así, y no pegado, por la misma razón que la enmienda declara: las líneas eliminadas contienen los rótulos viejos en su forma pelada, y pegarlas volvería a disparar `T25` sobre esta nota — mención y uso no se distinguen para un test de rótulos. El diff crudo, con sus tres pares de líneas, vive en `scratchpad` junto a las dos salidas.)*

Y normalizando los rótulos, `cmp` las declara **idénticas byte a byte**. La transcripción de §4 es la de esta segunda corrida, verbatim. **Ninguna cifra reportada cambia**, así que lo que se reporta sigue siendo el primer —y único— resultado del procedimiento.

---

## §10 · El párrafo a mesa

**¿El pipeline reproduce al INEGI, sí o no, y con qué holgura?** **Sí, y no con holgura: con identidad.** Los dos totales oficiales de ENASIC 2022 se reprodujeron **al peso** —`58 594 471` contra `58 594 471`, y `128 857 388` contra `128 857 388`— y los dos errores estándar de diseño se reprodujeron **a la novena cifra decimal**, con una diferencia de `10⁻⁹` que es ruido de punto flotante. Eso significa que la maquinaria que este programa usa para ponderar y para calcular precisión —el mismo estimador de conglomerados últimos que produjo el `IC95` de la única θ sellada del programa— **es la misma que usó el INEGI**, y no una aproximación parecida: coincide en la fórmula, en el factor `m/(m−1)`, en no aplicar corrección por población finita y en no ajustar por calibración de los factores. Hasta hoy eso era un supuesto declarado que ningún tercero había contrastado; ahora está identificado numéricamente. Dos cosas que mesa debe leer junto al sí. **La primera:** el criterio que el encargo hizo elegir —punto dentro del `IC95` oficial— resultó unas 170 veces más laxo que la precisión realmente alcanzada, y por sí solo habría dado por buena una discrepancia determinista de 21 090 personas sin verla; quien fije el criterio de la próxima validación externa debería exigir reproducción exacta, no pertenencia a intervalo. **La segunda:** el cruce encontró un defecto, y no es nuestro — el renglón `Población total` del archivo oficial de precisión publica una cifra que **incluye** los casos que su propia etiqueta declara excluidos, y llama *«21 090 casos»* a lo que es **un solo registro muestral con factor de expansión 21 090**. Cualquiera que obedezca esa etiqueta obtendrá `128 836 298`, no reproducirá la cifra publicada, y concluirá que su pipeline falla. El nuestro no falla: la etiqueta miente. Eso, y no el «sí», es lo que hace que esta validación externa haya valido lo que costó.
