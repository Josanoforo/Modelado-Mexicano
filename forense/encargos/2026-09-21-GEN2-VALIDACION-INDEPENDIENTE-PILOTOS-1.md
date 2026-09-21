# ENCARGO · ACTO GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1 · LAS CIFRAS QUE SOSTIENEN EL PRODUCTO —LA REALIDAD Y EL PISO DE LOS TRES PILOTOS— SE RECALCULAN DESDE CERO, POR ALGUIEN QUE NO LEYÓ EL CÓDIGO QUE LAS PRODUJO

> ENTORNO: **CAJA** (corpus montado: ENIF 2021/2024, ENVIPE 2023–2025, ENCIG 2021–2025). Si el hook no dice CAJA, PARA en una línea. NO es NUBE.

CABECERA · SHA de redacción `fc13cdcc`; re-deriva al abrir · una sola sesión, rama `acto/gen2-validacion-independiente-pilotos-1` · MODELO: Opus · MODO: **ABIERTO** · **INDEPENDENCIA (es el punto del acto):** no abras `medidor.py`, `adjudicacion.py` ni ningún `.py` dentro de los seis CALC de §3, ni los tests que los ejercitan; trabajas desde la **spec humana**, el cuestionario y el descriptor. Si ya los tienes en contexto, PARA y dilo · CONTADOR: no sella corridas de programa ni adopta; produce una validación con veredicto · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación.** Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.
**NO CHOCAR CON TUBERÍA (acto en vuelo):** no edites `.github/workflows/verify.yml`, `tests/check.py`, `.gitattributes`, `.claude/commands/*.md`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `tools/estado_comun.py` ni `tools/digesto_tramite.py`. Tu test nuevo **no** se cablea a mano: el job de guardias lo ejecuta como huérfano (`tools/ci_guardias.py --ejecuta-huerfanos`) `[EJECUTADO por dirección: 56 ejecutados]`. Si tu cierre exige tocar uno de esos archivos, déjalo en NC con sucesor y dilo.

## 1 · OBJETIVO
La frase que el producto puede decir hoy descansa en 35 celdas: «el estimador adjudicado acierta a 1.5 pp y su intervalo contuvo el valor real en 18 de 20». Esas cifras **se reproducen** (mismo código, mismo resultado), pero reproducir no es validar: si el medidor lee mal un filtro, lo lee mal las dos veces. E.2 separa tres preguntas —¿se reproduce? ¿pasó validación independiente? ¿se adopta?— y la segunda no se ha hecho para los pilotos. Un comprador escéptico la va a pedir. Los tres cruces ya están abiertos: recalcularlos no gasta nada.
«Hecho» significa: para cada piloto, R por celda (punto e IC95) y C2 por celda (punto), recalculados con código propio escrito desde la spec, comparados contra lo sellado con la tolerancia del tipo · veredicto por piloto: `COINCIDE` · `COINCIDE-CON-DIFERENCIA-EXPLICADA` (dices la causa y cuánto mueve el error del piso) · `DISCREPA` · informe en `forense/validaciones/`.

## 2 · FIRMAS DE MESA — verbatim
Instrucciones E.2: «Tres preguntas que no se colapsan: ¿se reproduce? ¿pasó validación independiente? ¿se adopta?» Piso adjudicado (17/sep): «Un piso no vencido es el estimador adjudicado de su celda y se adopta salvo veto de mesa.» Decisión de mesa (21/sep): «"Error conocido" no se promete fuera de cruces.»
**Propuesta de dirección — el lanzamiento es el sello:** «La validación independiente de los pilotos no re-adjudica: si discrepa, el veredicto sellado no se toca y la discrepancia va a mesa como hallazgo, con su tamaño en pp.»

## 3 · LO QUE DIRECCIÓN SABE (contra `fc13cdcc`, sin corpus)
- `[EXISTE]` los seis CALC y sus specs humanas: piloto 1 — `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` y `…-ARBITRO-CRUCE-0001`, spec `forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_2.md` · piloto 2 — `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` y `…-ARBITRO-CRUCE-0001`, spec `TRA-evade-norma-sxd12-spec-v1_0.md` · piloto 3 — `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` y `…-ADJUDICACION-0001` (sellados hoy, ya en main `[EJECUTADO: sello.json presente]`), spec `GOB-gobierno-digital-exe15-spec-v1_1.md`. Los `resultados.json` sí los lees: son contra lo que comparas — **después** de tener tus números.
- `[EXISTE]` precedente de forma: `forense/validaciones/GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/` y `tools/valida_envipe_independiente.py` (ése sí puedes leerlo: es de otra cosa).
- `[LEÍDO: notas de cierre]` unidades distintas: persona (ENIF), delito con `FAC_DEL` (ENVIPE), trámite (ENCIG: quien pagó doce veces contribuye doce veces). Piloto 3: edad 60–96, código 97 fuera; 18-29 × hasta primaria fuera de soporte ex ante; universo `N_TRA == 01`.
- `[SUPUESTO]` que las tres specs humanas bastan para recalcular sin leer código. **Si una no basta, ése es el hallazgo más importante del acto**: una spec que no permite reproducir sin el código no es una spec; di qué le falta.

## 4 · YA HECHO
Por objeto («validación independiente», «pilotos», «recalcula») en `forense/validaciones/`, encargos y ramas: hay validación independiente de la serie ENVIPE y de parámetros activos; ninguna de los pilotos. **Repítela tú.**

## 5 · PIEZAS
**P1 · Tus números, a ciegas.** Por piloto: código propio desde spec + cuestionario + descriptor; R por celda con IC95 por el diseño que la spec declare; C2 por celda desde los marginales de la misma ola. Commit de tus resultados **antes** de abrir los `resultados.json` sellados: el orden del diff es la prueba de independencia.
**P2 · Comparación.** Celda por celda contra lo sellado; diferencia en pp; tolerancia: la del tipo para el punto; para el IC, declara la tuya y por qué (tu remuestreo no tiene que ser el mismo plan de réplicas).
**P3 · Causas.** Toda diferencia mayor que la tolerancia se explica hasta la línea de la spec que la origina (filtro, código de no respuesta, ponderador, banda), o se declara `SIN-EXPLICAR`.
**P4 · Lo que cambia para el producto.** Con tus números: error medio del piso por piloto y cobertura de su IC. ¿La frase «1.5 pp, 18 de 20» se sostiene, se matiza o se rompe? Una línea.

## 6 · LATITUD
Decides tú: lenguaje, librerías, método de varianza (decláralo). Si una spec es ambigua, toma la lectura literal, anota la alternativa y calcula las dos.

## 7 · PAROS — lista cerrada
a) leer el código de los seis CALC o sus tests antes de tener P1 commiteado · b) abrir cualquier cruce `RESERVADA` (en ENIF 2024 solo `localidad × edad`; en ENVIPE 2025 solo el par del piloto 2; en ENCIG 2025 solo `edad × escolaridad` de luz) · c) editar un sello o un veredicto · d) entorno equivocado.

## 8 · COMPUERTAS
«P1 commiteado y en `origin`» protege: la independencia — formalmente, **abrir dato** (los sellados).

## 9 · PERÍMETRO
Propio: `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/` (código, resultados, informe) · nota · cascada. Ajeno: todo lo demás. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE
No re-adjudica · no sella corridas del programa. Sucesor: el informe del programa cita este veredicto; si hay `DISCREPA`, mesa decide. Auditoría: no afirma nada nuevo sobre México; verifica que lo afirmado esté bien medido — y declara, por piloto, el universo real que encontró al leer el cuestionario, que es donde se cuelan los sesgos de clase (quién tiene el servicio a su nombre, quién es el adulto elegido). `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
