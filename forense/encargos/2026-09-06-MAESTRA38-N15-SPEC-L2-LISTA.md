ENCARGO · ACTO MAESTRA38-N15 · SPEC-L2-LISTA — nube, Sonnet (patrón N7)
SHA: a5350e59 · COMPUERTA: ninguna · no toca red ni corpus · ENTORNO: NUBE · MODELO: Sonnet · Estado: VIVO

Escribe forense/prereg-caja/S10-L2-LISTA-spec-v1_0.md + .sha256: universo (list::mexico, 1 004,
sin ponderar), estimandos (prevalencia por diferencia de medias tratamiento−control con IC;
prevalencia directa mex.direct; contraste lista−directa; heterogeneidad por mex.wealth/mex.urban/
mex.loyal; participación verificada × directa), fila B-bis (qué significa que la lista no supere a
la directa), escala declarada (proporciones), universo declarado, se_mueve_si. Reutiliza §1.2 de
S2-L2 verbatim donde aplique. PERÍMETRO: sólo la spec y su sha; tablero (recibo). FP candidato:
siguiente libre. CONTADOR: specs de caja 8 → 9 · medición: cero.

PENDIENTE ICPSR (alta prioridad) · HALLAZGO WB 6667 · OPCIONES PARALELAS A MPS-2012
dirección (Fable) · 6/sep/2026 · contra origin/main = a5350e59 · en caja: A4 y LOTE-LAPOP corriendo ·
ENSANUT gateado a LAPOP · A5-PDN gateado a A4

## 0 · Procedencia (A.10)

Tipo (1) repo a5350e59: fila 6 de la cola (IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016,
PENDIENTE-DE-MESA, nota «NO-BAJAR-PORQUE… no responde N15/G6.deferencia aunque se accediera»);
24 payloads adq15_wb6667_* del 18/ago; MEX_2016_APIPIE_v01_M_Stata.zip no registrado (grep -c → 0);
FP-263 ABIERTA; S2-L2-spec-v1_0.md §1.1–1.2 (R7.3 = W2_P39B×W2_P8 | W2_P36C; R7.6 = W2_P40×W2_P8 |
W2_P36C; P3 = P35A/B, W2_P35A/B).

Tipo (1-externo), abierto byte a byte hoy: github.com/SensitiveQuestions/list @ e088e5f (16/ene/2024),
data/mexico.tab, sha256 fe101499b591d90d9e2122f439e26306fcdeab443e42d14f9455e9efa1c04488, 1 004
filas × 25 variables, man/mexico.Rd con el texto del ítem.

Tipo (búsqueda, SIN-FETCH): ICPSR 35024 «Public and restricted versions… Restricted Data Use
Agreement» sólo para la restringida; mexicopanelstudy.mit.edu → acceso a datos por correo
(zqueen@mit.edu); Harvard Dataverse doi:10.7910/DVN/27083 (Imai/Park/Greene 2014, réplica sobre el
experimento de lista de la ola 2) y doi:10.7910/DVN/VOB5JL (Greene 2024, compra de participación,
México).

## 1 · Pendiente de mesa — solicitud ICPSR 35024 (alta prioridad, fecha objetivo 7–8/sep)

Fila para forense/firmas-pendientes.tsv (columnas: id · qué_se_firma · dónde · creado · gatea ·
estado · firmada_en · ejecutada_en · encargo). Rótulo candidato FP-316 (A4 reclama 312-313, LAPOP
314-315; re-deriva quien la commitee):

FP-316	ACCION DE MESA, ALTA PRIORIDAD: solicitud manual a ICPSR del microdato 35024-0001-Data.dta
(Mexico Panel Study 2012). Firma verbatim 6/sep: «Necesito registrar la opcion 2 como pendiente de
alta prioridad, lo haria manana o pasado manana». Antes de llenar el formulario, una verificacion de
un clic: el catalogo declara version PUBLICA y RESTRINGIDA; solo la restringida exige Restricted
Data Use Agreement. Si la publica baja con la cuenta ya creada (D6), no hay solicitud que hacer. Si
solo la restringida trae W2_P39B/W2_P40/W2_P36C/W2_P8/P35A-B, se solicita la restringida. Se reporta
cual de las dos se intento y que respondio (A.5). Vencimiento informativo 12/sep (D8: una fecha es
limite, nunca compuerta).	mesa (navegador) · icpsr.umich.edu/web/RCMD/studies/35024	2026-09-06	L2
rama MEDICION (sucesor L2-bis si el .dta llega despues de que L2 corra TEXTO)	ABIERTA			este
documento

Quién la commitea: el agente de fondo de trámite (D-13) o el primer acto de nube que abra el
tablero; una línea, un PR de trámite, sin ADR. No la añade LAPOP ni A4 (fuera de su perímetro).

## 2 · Hallazgo para forense/hallazgos.md (una línea, no se cataloga)

6/sep: la petición de descarga manual «WB 6667» a mesa cubrió 24 archivos; 23 ya estaban en corpus
desde el 18/ago (adq15_wb6667_*) y sólo MEX_2016_APIPIE_v01_M_Stata.zip faltaba. Petición derivada
sin cruzar el manifiesto (A.8 contra la página del catálogo, no contra manifiesto.yaml). Mismo
defecto que la cola del 13/ago. Depósito: sólo el .zip, en
Descargas MX\ADQ15_WB6667_Tutores_Pedagogicos_Moviles_2016\; lo promueve el [CENSO] (lunes 07:30, o
./tools/adquiere_cron.sh a mano). Reserva vigente de §2.1 del 3/sep: el instrumento no trae reactivo
de deferencia ni desenlace laboral — hoy no mueve N15; se abre con veredicto sólo si un acto de nube
lo cruza por texto contra G6.

## 3 · Opciones paralelas a MPS-2012, por lo que cada una cubre

| # | Fuente | Cubre | Estado | Ruta | Costo |
|---|---|---|---|---|---|
| A | list::mexico (subconjunto MPS-2012 ola 2, CRAN/GitHub) | P3 completo: lista vs directa, mismo n; participación (declarada y verificada) × pregunta directa; partido, riqueza, urbano | ABIERTO byte a byte hoy | git clone https://github.com/SensitiveQuestions/list desde la caja (espejo académico, ruta iv) → registro con sha del commit y del .tab | minutos + una spec |
| B | Dataverse DVN/27083 (Imai/Park/Greene) y DVN/VOB5JL (Greene 2024) | posiblemente más variables de la ola 2 (voto por partido, más covariables); Greene 2024 puede traer 2018 | SIN-FETCH | /adquiere con la API de Dataverse: https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/27083 (y VOB5JL); sin cuenta para archivos públicos | minutos |
| C | ICPSR 35024 versión pública | desconocido hasta abrir; podría traer W2_P39B/P40/P36C/P8 | SIN-FETCH, ver §1 | cuenta D6 ya creada; un clic | minutos de mesa |
| D | Cuestionarios ya en corpus: ENCUP 2012 (base xlsx + cuestionario), CIDE-CSES 2015 (3 .sav), Latinobarómetro 2024, LAPOP 2019/2021/2023 | candidatos para R7.3/R7.6 por constructo: beneficiario de programa × voto, «le condicionaron», secreto percibido | bytes en corpus; texto sin cruzar contra estos tres constructos | tools/inventario_reactivos.py + cruce de texto (patrón N12), nube, Sonnet, sin red | una sesión de nube |
| E | Mexico 2000 (ICPSR 03380) y 2006 Panel Studies | mismos constructos en otros años (Oportunidades/Progresa × voto en 2000 y 2006) | SIN-FETCH; misma vía de correo/ICPSR | después de §1 | igual que ICPSR |

Lo que A no hace, dicho antes de que alguien lo lea como cierre: no mueve R7.3 ni R7.6 (0 de sus
variables); no trae ponderador (sin ponderar, declarado); es un subconjunto (1 004 de ~1 555 de la
ola 2) — se declara universo restringido (A-bis 4). Lo que sí hace: convierte P3 de «PROPUESTA de
medición» a medición de primera mano, y su texto de ítem («Exchange your vote for a gift, favor, or
access to a service», ítem c sólo en tratamiento) satisface por texto la condición de entrada de
§1.2 — en inglés; el cuestionario en español está en corpus (ICPSR_35024/35024-Questionnaire-spanish.pdf)
y L2 rama TEXTO lo lee.

## A.8 · `tools/ya_medido.py` — citas ilustrativas de `R7.3`/`R7.6` en este encargo

Este encargo cita `R7.3`/`R7.6` sólo en la Procedencia (§0, heredado de `S2-L2 §1.1–1.2`) como
contexto de por qué `list::mexico` NO las mueve — no las clasifica, no las pre-registra, no las
carga ni las sella. `T-YAMEDIDO` exige la salida igual:

```
$ python3 tools/ya_medido.py R7.3
=== ya_medido: R7.3 ===
  resuelto por canon: R7.3 -> id `civico.voto.agencia_con_secreto`
MEDIDA-EN: L11, L12, L9, N6, S2, S4, canon§7, tramite-ola5-propuesta-v0.yaml

$ python3 tools/ya_medido.py R7.6
=== ya_medido: R7.6 ===
  resuelto por canon: R7.6 -> id `civico.voto.clientelar_si_observable`
MEDIDA-EN: L11, L12, L9, S4
```

Ambas `MEDIDA-EN` — confirma lo que este encargo y `S10-L2-LISTA` ya declaran: `list::mexico` no las
mueve (0 de sus variables), y `S2-L2`/futuras L2 corren sobre el `.dta` de ICPSR 35024, no aquí.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N15 · SPEC-L2-LISTA`, rama
`claude/s10-l2-lista-spec-rpaf1j`. Ver PR que fusiona esta rama contra
`main` para el commit final.
