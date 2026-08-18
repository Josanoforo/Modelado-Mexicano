# COND-ATRIB — condicionamiento por atributos del β̂ marginal PENDIENTE (`confianza_institucional_generico_servidores_publicos`)

*18 de agosto de 2026.*

Encargo `forense/encargos/2026-08-18-COND-ATRIB-condicion-por-atributos.md` (VIVO, tras fusión de `gate-durable-v7`, PR #260, `6178bf9`). Worktree `/home/pc0/Modelado-Mexicano-barrido2`, rama `cond-atrib` desde `origin/main` (`6178bf9`, ancestro de `68a3466` confirmado por `git merge-base --is-ancestor`).

## 0 · C0 — derivación propia de la lista de entradas afectadas, contra la instrucción explícita de no heredar "3"

`grep -n "marginal\|PENDIENTE.*condicional" milpa/procedencia.yaml` devuelve 4 líneas de `clase:` candidatas:

| Línea | Entrada | Familia | `clase:` literal |
|---|---|---|---|
| 310 | `condicionales_escalares_confianza_generica.confianza_institucional_generico_servidores_publicos` | `condicionales_escalares_*` (mide θ del propio reactivo) | `"PENDIENTE -- medición condicional por atributos NO CORRIDA en este acto"` |
| 805 | `coeficientes_generador_medidos.G1_radio_confianza` | `coeficientes_generador_medidos` (mide β̂ reactivo→desenlace) | `"MEDIDO·β̂(diferencia de proporciones), por ítem, marginal (sin condicionar sobre atributos)"` |
| 854 | `coeficientes_generador_medidos.G1_confianza_institucional` | ídem | `"MEDIDO·β̂(diferencia de proporciones), un ítem, marginal, TRUNCADO"` |
| 886 | `coeficientes_generador_medidos.G3_familismo_apoyo` | ídem | `"MEDIDO·β̂(diferencia de proporciones), un ítem, marginal"` |

**Verificación de existencia, contra el propio contenido de las tres últimas — resultado: EXCLUIDAS de la deuda, no forman parte del denominador.** Las tres tienen campo `eje_condicionante: "EJECUTADO (Encargo X, forense/notas/2026-08-04-x-condicionamiento-y-forma.md §4.1/§4.2/§4.3)..."` con resultados por celda ya escritos: 33/39 celdas invierten signo (W1), reversión completa en 4/4 celdas (W2), inversión en celdas mayoritarias (W3). Estas tres son, verbatim, **el precedente que A-bis Regla 1 (`instrucciones-proyecto-v2_10.md` §81) cita como su propio caso fundador**: *"Verificado el 4/ago: los tres coeficientes estimados marginalmente invirtieron el signo al estratificar -- en uno de ellos, las cuatro celdas del único eje disponible, todas significativas, todas opuestas al marginal."* La palabra "marginal" que sobrevive en su `clase:` describe el `beta_hat` oficialmente reportado (el punto marginal, con la reserva `adr57_a` escrita al lado) -- no significa "condicionamiento no corrido". Condicionarlas de nuevo repetiría trabajo ya hecho y violaría la frase ritual ("el primer resultado que produzca este procedimiento es el que se reporta" -- ya hay un resultado).

**`G1_confianza_institucional` (854) lleva además la palabra `TRUNCADO` -- verificado que tampoco es una tarea ejecutable pendiente.** Su propio `eje_condicionante` declara *"sigue TRUNCADO en ingreso/ruralidad, no resuelto aquí"*. `forense/notas/2026-08-04-w-coeficientes-generador-paso1.md` línea 101 (tabla C4 de P2) ya estableció, para ENCIG: *"1 eje estricto (edad), 4 laxos, **sin ingreso ni ruralidad en ningún régimen**"* -- ausencia estructural del instrumento, no una tarea sin ejecutar. Verificado independientemente en esta sesión (§0.1 abajo): ENCIG 2023 no trae `ingreso` en ninguna de las 6 tablas registradas en `data/manifiesto.yaml` (`encig23_base_datos_csv`), y la restricción de universo a ciudades de 100 000+ habitantes (ver §1.2) elimina la variación de ruralidad por diseño del instrumento, no por omisión de este o de ningún acto. **No hay nada ejecutable ahí.**

**Denominador del acto: 1, no ≥3.** Única entrada con conditioning genuinamente `NO CORRIDA`: `confianza_institucional_generico_servidores_publicos` (línea 309-321). Su propia nota interna ya lo distingue de las tres anteriores: *"Solo existe el β̂ MARGINAL de este reactivo, ya registrado en `coeficientes_generador_medidos.G1_confianza_institucional`... este bloque registra el reactivo y su estado de cobertura, no lo condiciona sobre atributos"* -- el ítem que registra (`P11_1_23`) es el MISMO instrumento/reactivo que `G1_confianza_institucional`, pero mide una cosa distinta: `G1_confianza_institucional` mide β̂(P11_1_23 → `tramite.mordida.discrecional`) -- ya condicionado (Encargo X, edad). Esta entrada mide θ(P11_1_23 | x) -- la prevalencia del propio reactivo, condicionada por atributos poblacionales -- análogo exacto al patrón ya sellado por sus hermanas de la misma familia `condicionales_escalares` (`radio_confianza` línea 252, `familismo_apoyo` línea 272, ambas `MEDIDO·PARCIAL(x)`), que nadie corrió para este reactivo. Nunca se corrió -- ni por `CAL-CONF Fase B posición 8` (`forense/notas/2026-08-04-cal-conf-faseb-pos8-encig-battxi.md`, que solo hizo cobertura de instrumento, cero microdato abierto, §4 de esa nota) ni por Encargo X (que condicionó la asociación con `mordida`, no la prevalencia del reactivo mismo).

Barrido exhaustivo adicional (`grep -n "PENDIENTE" milpa/procedencia.yaml`, todo el archivo): la única otra ocurrencia de clase distinta a comentarios de cabecera es línea 1043 (`G5.familismo_obligacion`, tabla `detalle`, "SIN-RUTA", "forma PENDIENTE") -- problema de clase distinta (sin magnitud asignada, sin ruta), fuera de perímetro, no tocado.

Búsqueda de encargo previo (`grep -rln "COND-ATRIB\|condicional por atributos" forense/encargos/`): **NO-ENCONTRADO** -- confirma que este es el primer acto que escribe este procedimiento.

### 0.1 · Verificación independiente de la ausencia de ingreso/ruralidad/migración/acceso-digital en ENCIG 2023

Diccionario `encig23_estructura_base_datos.pdf` (`sha256 eb89820c...`, coincide contra `data/manifiesto.yaml:61`) revisado con `pdftotext -layout`, dirigido (no íntegro) a: encabezados de sección de las 6 tablas, bloque "Campos empleados para el diseño muestral" de cada tabla, sección "II. INTEGRANTES DEL HOGAR..." (sociodemográficos), sección "IX." (P9, corrupción/denuncia) y "X. GOBIERNO ELECTRÓNICO" (P10). Ningún ítem de ingreso (monto, rango, nivel socioeconómico) localizado en ninguna de las 6 tablas. `AREAM` (área metropolitana) tiene "00 = Resto de ciudades de 100 mil [habitantes y más]" como categoría residual -- confirma que el marco muestral de ENCIG está restringido a ciudades de 100 000+ habitantes; no existe escala graduada de tamaño de localidad ni estrato rural. `P10_1_*` ("¿ha consultado páginas de internet del gobierno...?") es un ítem de uso/conducta de gobierno electrónico, no de tenencia de acceso digital (`celular`/`conex_inte`, la definición de `canon/modelo-decision-v4_0.md:121`) -- no es sustituto válido, no se usa. Ninguna variable de lugar de nacimiento/residencia previa localizada. **Los cuatro ejes -- urbanización/tamaño de localidad, ingreso, migración, acceso digital -- se declaran NO DISPONIBLES en ENCIG 2023, no forzados.**

## 1 · Especificación — congelada antes de abrir el desenlace condicionado

**⚠️ Declaración de desviación de protocolo, hecha aquí y no escondida.** Antes de escribir esta especificación, en la fase de reconocimiento de instrumento, se abrieron sin `unshare -Urn` (violación de la letra de "red cero durante apertura de microdato"): cabeceras + fila 2 de `encig2023_01_sec_11.csv` y cabecera de `encig2023_01_sec1_A_3_4_5_8_9_10.csv` (lectura local de zip, sin llamada de red intentada -- riesgo de exfiltración: nulo, verificado por inspección del código ejecutado), y una prueba de unión (`sec11.merge(sec02...)`) que expuso las distribuciones marginales de `P11_1_23` (1907/18383/12531/5024/1101/20 en códigos 1..5,9) y de `SEXO` (17612 H/21354 M) y confirmó unión 1:1 perfecta (38966/38966). **No se vio ninguna relación condicional (reactivo × eje) ni ninguna celda del diseño que sigue.** Se declara como defecto de proceso, no se oculta; el resto de esta apertura y todo cómputo corre bajo `unshare -Urn` desde este punto.

**Instrumento y payload:** `encig23_base_datos_csv.zip` (`data/manifiesto.yaml:28-52`, id `encig23_base_datos_csv`), `sha256 af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d` -- **Coincide**, verificado en este worktree. Tablas: `encig2023_01_sec_11.csv` (batería XI, ítem `P11_1_23`, diseño `EST_DIS`/`UPM_DIS`/`EST`, ponderador `FAC_P18`) unida por `ID_PER` a `encig2023_02_residentes_sec_2.csv` (roster de hogar, trae `SEXO`, `EDAD`, `NIV`, `POS`) -- unión verificada 1:1, 38966/38966, cero pérdida (§0.1 y prueba de unión declarada arriba). Diccionario: `encig23_estructura_base_datos.pdf`, `sha256 eb89820cd58af0d8799387a376b9e60b062ed59daea74cdbea7ff3b4ee13a906` -- **Coincide**.

**Universo:** todas las personas de 18+ entrevistadas de ENCIG 2023 (n=38966, universo completo de la tabla `sec_11`, sin restricción adicional -- mismo patrón que `condicionales_escalares.radio_confianza`: "Universo completo, sin no-aplicabilidad estructural") con `P11_1_23` válido: código ∈ {1,2,3,4} (dicotomizable), excluidos código 5 ("No aplica", n=20) y código 9 ("No sabe/no responde", n=1101) -- universo efectivo n=37845. Restringido a ciudades de 100 000+ habitantes por diseño del propio instrumento ENCIG (§0.1) -- no se reconcilia contra un marginal nacional de otra fuente (A-bis regla 4).

**Ponderador:** `FAC_P18` -- "Factor de expansión para la [población de] 18 años y más" (`encig23_estructura_base_datos.pdf`, líneas 2954/3951/4455 del texto extraído), el mismo que `data/manifiesto.yaml:55` nombra para este propósito. **Diseño:** estrato = `EST_DIS`, UPM = `UPM_DIS` (ambos en `encig2023_01_sec_11.csv`).

**θ:** `P11_1_23` dicotomizado confía={1,2} / no confía={3,4} -- **mismo corte que `coeficientes_generador_medidos.G1_confianza_institucional`** (procedencia.yaml:853), para comparabilidad de escala (no se compara la magnitud entre las dos entradas -- miden cosas distintas, regla 3 -- pero comparten la definición del reactivo).

**Ejes de condicionamiento disponibles, derivados del diccionario, un eje a la vez (patrón `Encargo X`):**

| Eje | Variable | Niveles | Estatus |
|---|---|---|---|
| Edad | `EDAD` (roster) | 18-29 / 30-44 / 45-59 / 60+ (excluye 98/99 "no especificada"; buckets del propio `canon`/convención del proyecto, p.ej. `G4_exposicion_violencia`, no derivados de la distribución) | Eje "estricto" (canónico, §1.1.A) -- el único que `Encargo X` corrió para este mismo reactivo (sobre el desenlace distinto `mordida`) |
| Formalidad | `POS` (roster) | 1 jornalero(a) · 2 empleado(a)/obrero(a) · 3 cuenta propia · 4 patrón(a) · 5 sin pago -- blanco (`POS` no aplicable a quien no trabajó la semana de referencia) EXCLUIDO de este eje, declarado, no forzado | Eje "laxo" (proxy de formalidad, §1.1.A eje 1) -- disponible pero no probado por `Encargo X` |
| Sexo | `SEXO` (roster) | 1 Hombre · 2 Mujer | Fuera del vector canónico de 6 ejes -- disponible, sugerido por el propio encargo, sin blancos declarados |
| Escolaridad | `NIV` (roster) | Recodificado 3 cubetas por definición estándar de nivel educativo (no por distribución): Básica-o-menos {0,1,2,3} · Media-superior/técnica {4,5,6} · Superior {7,8,9} | Fuera del vector canónico -- disponible, sugerido por el propio encargo |
| Estrato | `EST` (`encig2023_01_sec_11.csv`) | 1-4, sin descripción sustantiva más allá de "Estrato" en el diccionario -- se reporta por nivel, no se interpreta sustantivamente (mismo trato que `ESTRATO` en `G4_exposicion_violencia`, procedencia.yaml:919) | Variable de diseño, disponible |

**Declarados NO DISPONIBLES, no forzados (§0.1):** urbanización/tamaño de localidad, ingreso, migración, acceso digital.

**Estimador y escala -- reusa `tests/svystat.py::diff_ultimate_cluster` (sin modificar), mismo procedimiento y mismo cuantil (1.959963985) que `Encargo X`/`Encargo W`.** Para cada eje, para cada nivel ℓ: grupo T = filas de ese nivel, grupo C = filas de los demás niveles VÁLIDOS del mismo eje (mismo universo restringido de arriba). Devuelve `p_T` (= θ̂(ℓ), la proporción ponderada que confía dentro del nivel -- mismo estimando que la clase `MEDIDO·PARCIAL(x)` de las hermanas `radio_confianza`/`familismo_apoyo`) y `d_hat = p_T - p_C` (**la diferencia de proporciones que pide C1(5) del encargo, regla 3 -- nivel contra el resto del mismo eje, NO contra el marginal global**, elegido así porque nivel-vs-marginal-global no son grupos disjuntos y el marginal incluye al propio nivel -- `diff_ultimate_cluster` exige T/C disjuntos y da la varianza correcta para ese caso; nivel-vs-marginal violaría la condición "grupos disjuntos, independientes" que el propio método de `Encargo W` declara como supuesto). IC95% con 1.959963985 unidades de `se`. Umbral de soporte: n≥30 por celda T (mismo criterio que `G4_exposicion_violencia`, procedencia.yaml:919); celdas bajo el umbral se reportan igual (`diff_ultimate_cluster` no filtra) pero se marcan **SIN SOPORTE**, no se usan para adjudicar.

**(6) Qué significa cada desenlace -- declarado antes, adaptando el molde del encargo a una medición univariada (declarado explícitamente, no forzado a la plantilla del β̂ de dos variables):**

Para un eje con partición exhaustiva de 2 niveles (Sexo), `d_hat` de ambos niveles es necesariamente antisimétrico (`d_hat(B) = -d_hat(A)` exacto) -- **no es un hallazgo de "signo estable/discordante", es una propiedad mecánica de la partición binaria**, y se declara así, no se interpreta como corroboración ni como reversión.

Para ejes con 3+ niveles (Edad, Formalidad, Escolaridad, Estrato) -- que NO están forzados a suma cero de la misma manera (cada nivel se compara contra un "resto" distinto) -- la lectura declarada es: (a) el rango de θ̂ entre niveles del eje y si es sustantivo dado los IC95% que lo acompañan; (b) cuántos niveles tienen `d_hat` distinguible de cero al 95% (IC no cruza cero) y en qué dirección; (c) si hay un patrón ordenado/monótono (p.ej. por edad o por escolaridad) o disperso sin patrón -- sin adjudicar mecanismo. Un punto que cruza umbral con IC que no lo despeja no adjudica -- se reporta como propuesta con la reserva escrita (A-bis, contraparte). Ninguna lectura causal ni de intervención (A-bis regla 2) -- asociar ≠ identificar. Universo restringido a ENCIG (ciudades 100 000+) -- no se reconcilia contra un marginal de otra fuente ni otro universo (A-bis regla 4).

**El contador (auditoría, declarado antes de correr):** este acto mide México. Mueve la entrada de C0 de `PENDIENTE` a `MEDIDO·PARCIAL(x)` (la clase que corresponde a su familia `condicionales_escalares`, no `MEDIDO·β̂` -- esta entrada nunca tuvo un β̂ propio, tenía cero número). No toca el contador de coeficientes de generador en escala del modelo (hoy 0 de 15): esta medición es una condicional θ(x) sobre un ítem que no es un componente nombrado del vector de `ADR-28.b` (declarado por `ADR-57(e)`, procedencia.yaml:293-307) -- sigue sin alimentar ningún generador con nombre. Sigue siendo asociación condicionada, no identificación (A-bis regla 1-2); el primero de la lista de 15 sigue reservado a FP-11.

**El primer resultado que produzca este procedimiento es el que se reporta.**

## 2 · Resultados — primera y única corrida

**Nota de proceso, antes de los números.** Al escribir el script se cometió un defecto de código (no de especificación): la variable de agregación de diseño `EST_DIS` (~347 estratos de diseño, rango 001-999) se reasignó por error también a la variable del eje sustantivo "Estrato" (`eje_est`), que la especificación de §1 nombra correctamente como `EST` (1-4). El primer intento de ejecución produjo ~347 niveles espurios para ese eje -- detectado por inspección directa del output (recuento de líneas y valores de nivel fuera de {1,2,3,4}) antes de escribir cualquier resultado en este archivo o en `procedencia.yaml`. Corregido (`eje_est = df["EST"]`, no `df["est"]`) y re-ejecutado una sola vez más antes de reportar. Esto no es "corregir la especificación hacia atrás" (§1 siempre dijo `EST`): es una corrección de una implementación que no seguía lo ya congelado, hecha antes de que ningún resultado circulara. Se declara para que conste, no se oculta.

Comando: `unshare -Urn -- python3 cond_atrib_run.py` (script idéntico a lo congelado en §1, salvo la línea `eje_est` corregida como se explica arriba), ejecutado desde la raíz de este worktree contra `/home/pc0/mm-corpus/raw/encig23_base_datos_csv.zip`.

```
universo efectivo (P11_1_23 valido, excl. 5 y 9): n=37845

MARGINAL GLOBAL (contexto, no referencia de diferencia): p_hat=0.5135 IC95%=[0.5052,0.5218] n=37845 n_estratos=347 singleton=0

=== EJE: Edad (n=37670 de 37845, niveles=['18-29', '30-44', '45-59', '60+']) ===
  18-29: n_T=8207 (con soporte) n_C=29463 | p_hat(nivel)=0.5469 | d_hat=+0.0443 IC95%=[+0.0251,+0.0635] se=0.0098 | n_estratos=347 singleton=0 n_upm=8916
  30-44: n_T=11387 (con soporte) n_C=26283 | p_hat(nivel)=0.4798 | d_hat=-0.0471 IC95%=[-0.0643,-0.0299] se=0.0088 | n_estratos=347 singleton=0 n_upm=8916
  45-59: n_T=9747 (con soporte) n_C=27923 | p_hat(nivel)=0.4904 | d_hat=-0.0318 IC95%=[-0.0499,-0.0136] se=0.0092 | n_estratos=347 singleton=0 n_upm=8916
  60+: n_T=8329 (con soporte) n_C=29341 | p_hat(nivel)=0.5504 | d_hat=+0.0459 IC95%=[+0.0257,+0.0661] se=0.0103 | n_estratos=347 singleton=0 n_upm=8916

=== EJE: Formalidad (POS) (n=26502 de 37845, niveles=['cuenta-propia', 'empleado-obrero', 'jornalero', 'patron', 'sin-pago']) ===
  cuenta-propia: n_T=6812 (con soporte) n_C=19690 | p_hat(nivel)=0.4725 | d_hat=-0.0382 IC95%=[-0.0606,-0.0158] se=0.0114 | n_estratos=347 singleton=0 n_upm=8776
  empleado-obrero: n_T=18370 (con soporte) n_C=8132 | p_hat(nivel)=0.5116 | d_hat=+0.0352 IC95%=[+0.0143,+0.0561] se=0.0107 | n_estratos=347 singleton=0 n_upm=8776
  jornalero: n_T=282 (con soporte) n_C=26220 | p_hat(nivel)=0.5161 | d_hat=+0.0151 IC95%=[-0.0774,+0.1075] se=0.0472 | n_estratos=347 singleton=0 n_upm=8776
  patron: n_T=788 (con soporte) n_C=25714 | p_hat(nivel)=0.4372 | d_hat=-0.0659 IC95%=[-0.1207,-0.0110] se=0.0280 | n_estratos=347 singleton=0 n_upm=8776
  sin-pago: n_T=250 (con soporte) n_C=26252 | p_hat(nivel)=0.6569 | d_hat=+0.1572 IC95%=[+0.0726,+0.2418] se=0.0432 | n_estratos=347 singleton=0 n_upm=8776

=== EJE: Sexo (n=37845 de 37845, niveles=['Hombre', 'Mujer']) ===
  Hombre: n_T=17254 (con soporte) n_C=20591 | p_hat(nivel)=0.5038 | d_hat=-0.0180 IC95%=[-0.0345,-0.0015] se=0.0084 | n_estratos=347 singleton=0 n_upm=8919
  Mujer: n_T=20591 (con soporte) n_C=17254 | p_hat(nivel)=0.5218 | d_hat=+0.0180 IC95%=[+0.0015,+0.0345] se=0.0084 | n_estratos=347 singleton=0 n_upm=8919

=== EJE: Escolaridad (NIV) (n=37845 de 37845, niveles=['Basica-o-menos', 'Media-superior-tecnica', 'Superior']) ===
  Basica-o-menos: n_T=14762 (con soporte) n_C=23083 | p_hat(nivel)=0.5196 | d_hat=+0.0101 IC95%=[-0.0074,+0.0277] se=0.0090 | n_estratos=347 singleton=0 n_upm=8919
  Media-superior-tecnica: n_T=9278 (con soporte) n_C=28567 | p_hat(nivel)=0.5254 | d_hat=+0.0162 IC95%=[-0.0039,+0.0362] se=0.0102 | n_estratos=347 singleton=0 n_upm=8919
  Superior: n_T=13805 (con soporte) n_C=24040 | p_hat(nivel)=0.4973 | d_hat=-0.0246 IC95%=[-0.0420,-0.0072] se=0.0089 | n_estratos=347 singleton=0 n_upm=8919

=== EJE: Estrato (EST) (n=37845 de 37845, niveles=['1', '2', '3', '4']) ===
  1: n_T=561 (con soporte) n_C=37284 | p_hat(nivel)=0.5307 | d_hat=+0.0176 IC95%=[-0.0487,+0.0838] se=0.0338 | n_estratos=347 singleton=0 n_upm=8919
  2: n_T=16975 (con soporte) n_C=20870 | p_hat(nivel)=0.5082 | d_hat=-0.0097 IC95%=[-0.0265,+0.0071] se=0.0086 | n_estratos=347 singleton=0 n_upm=8919
  3: n_T=13965 (con soporte) n_C=23880 | p_hat(nivel)=0.5187 | d_hat=+0.0079 IC95%=[-0.0093,+0.0251] se=0.0088 | n_estratos=347 singleton=0 n_upm=8919
  4: n_T=6344 (con soporte) n_C=31501 | p_hat(nivel)=0.5151 | d_hat=+0.0019 IC95%=[-0.0186,+0.0225] se=0.0105 | n_estratos=347 singleton=0 n_upm=8919
```

Verificación de totales por eje contra el universo declarado (n=37845): Edad suma 37670 (175 excluidos, código EDAD 98/99 no especificada) · Formalidad suma 26502 (11343 excluidos, blanco estructural = no trabajó la semana de referencia, declarado en §1) · Sexo suma 37845 (cero excluidos) · Escolaridad suma 37845 (cero excluidos) · Estrato suma 37845 (cero excluidos) -- todos reconcilian contra lo esperado en §1, ningún eje pierde filas fuera de lo ya declarado.

## 3 · Interpretación

Aplicando exactamente la regla declarada en §1(6), sin adjudicar mecanismo y sin lectura causal (A-bis regla 2):

**Sexo (2 niveles -- propiedad mecánica declarada, no hallazgo de robustez).** `d_hat` antisimétrico exacto: Hombre −0.0180 [−0.0345,−0.0015], Mujer +0.0180 [+0.0015,+0.0345] -- ambos apenas distinguibles de cero (el límite superior/inferior roza 0.0015). Brecha pequeña (3.6pp) pero detectable: mujeres marginalmente más confiadas que hombres en este universo.

**Edad (4 niveles).** Rango de `p_hat`: 0.4798 (30-44, mínimo) a 0.5504 (60+, máximo) -- 7.1pp de recorrido. **4 de 4 niveles con `d_hat` distinguible de cero al 95%**: 18-29 y 60+ positivos (por encima del resto del eje), 30-44 y 45-59 negativos. Patrón: forma de U, no monótono -- adultos jóvenes y adultos mayores confían más en "servidores públicos genéricos" que adultos de edad media; sustantivo dado que las cuatro celdas tienen IC95% que no cruzan cero.

**Formalidad/POS (5 niveles).** Rango de `p_hat`: 0.4372 (patrón, mínimo) a 0.6569 (sin-pago, máximo) -- 22pp de recorrido, el más amplio de los cinco ejes. **4 de 5 niveles con `d_hat` distinguible de cero** (jornalero es la excepción, IC95%=[−0.0774,+0.1075], cruza cero pese a n=282≥30 -- celda con soporte pero sin señal). Sin patrón ordenado limpio por "formalidad": sin-pago (trabajo familiar sin remuneración) es el nivel más confiado con diferencia amplia (+15.7pp), patrón es el menos confiado (−6.6pp); empleado/obrero positivo (+3.5pp), cuenta propia negativo (−3.8pp). No se lee como escala de formalidad creciente o decreciente -- disperso, con dos extremos marcados.

**Escolaridad/NIV (3 niveles).** Rango de `p_hat`: 0.4973 (Superior, mínimo) a 0.5254 (Media-superior-técnica, máximo) -- 2.8pp, modesto. **Solo 1 de 3 niveles distinguible de cero**: Superior, negativo (−2.5pp) -- quienes tienen escolaridad superior confían algo menos que el resto en este reactivo; Básica-o-menos y Media-superior-técnica no se distinguen de cero. No hay patrón monótono limpio (Básica 0.5196 → Media 0.5254 → Superior 0.4973, sube y luego baja) -- señal débil, concentrada en un extremo.

**Estrato/EST (4 niveles).** Rango de `p_hat`: 0.5082 (nivel 2, mínimo) a 0.5307 (nivel 1, máximo) -- 2.3pp, el más chico de los cinco ejes. **0 de 4 niveles distinguible de cero.** Sin patrón -- efectivamente plano; el diccionario no da significado sustantivo a los cuatro niveles de `EST` más allá de "Estrato" (§1), así que no se interpreta más allá de "sin señal aquí".

**Ningún punto de este acto se adjudica sin IC que lo despeje** (A-bis, contraparte) -- jornalero (Formalidad), y los tres niveles no marcados arriba en Escolaridad y los cuatro de Estrato, cruzan cero y se reportan como propuesta sin adjudicación. Ninguna lectura causal ni de intervención. Universo restringido a ENCIG (ciudades de 100 000+ habitantes) -- no se reconcilia contra un marginal de otra fuente ni otro universo (A-bis regla 4). Ningún número de esta sección se compara en magnitud contra el β̂ de `coeficientes_generador_medidos.G1_confianza_institucional` (−0.0645) -- mismo reactivo, escala y desenlace distintos (A-bis regla 3).
