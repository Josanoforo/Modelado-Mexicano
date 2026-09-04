# MAESTRA38-N5 · DISEÑO-9-REGLAS-SIN-INSTRUMENTO

Ejecuta `forense/encargos/2026-09-04-MAESTRA38-N5-DISENO-9-REGLAS-SIN-INSTRUMENTO.md`.
Insumo: `forense/notas/2026-09-03-MAESTRA38-A1-censo-9-no-encontrado.md` — 48 payloads
nuevos (12 candidatas de `MAESTRA38-A1`, 3 formulaciones × 9 reglas = 27 corridas) no
movieron 8 de 9 reglas `NO-ENCONTRADO`; la 9ª (`N34`) trajo señal adyacente en ENCRIGE
2020, del lado equivocado de la transacción. Esta pieza **no mide, no cierra regla, no
abre Ola 6**: diseña el criterio de clasificación y lo aplica una vez a las 9, deja
tabla `PENDIENTE-DE-MESA`, y no toca `canon/` ni `milpa/` — mesa decide con la tabla,
un acto sucesor propaga. D-6 aplicado: este acto se declara `ACTO MAESTRA38-N5` en
todo archivo que escribe.

---

## COMMIT-1 · Las 9 reglas, objeto medible, criterio de clasificación

### 1.1 Las 9 reglas — texto verbatim, `canon/modelo-decision-v4_0.md` §3

| # | id | § | tier | texto (SI…ENTONCES…PORQUE, recortado) |
|---:|---|---|---|---|
| 1 | `tramite.evasion.norma_inutil_sancion_improbable` | §3.3 (L520) | `[MEDIA]` | SI una norma se percibe como inútil o extractiva y la sanción es improbable ENTONCES evasión ("hacerse guaje") — PORQUE cálculo ante institución de baja calidad. *(Distinguir evasión de subsistencia [informalidad] de evasión por cinismo de clase alta.)* |
| 2 | `dinero.ahorro.seguro_deposito_atenua_aversion` | §3.1 (L503) | `[MEDIA]` | SI existe seguro de depósito visible o marca confiable ENTONCES se atenúa la aversión (la fintech con respaldo penetra donde el banco tradicional no) — PORQUE G1 + diseño. |
| 3 | `dinero.credito.scoring_alternativo` | §3.1 (L504) | `[MEDIA]` **(a)** | SI el hogar es popular/informal y el crédito es de efectivo o tarjeta de alto CAT ENTONCES paga sobreprecios notables hasta un techo: la mora regulada se estabiliza en 15–20% — PORQUE el precio absorbe el error de predicción del scoring. Falsador ya pre-registrado: IMOR de consumo del sector popular > ~25–30% sostenido sin que el CAT pueda subir más. |
| 4 | `dinero.credito.baja_friccion_usura_dano_downstream` (`N34`) | §3.1 (L505) | `[MEDIA]` **(a)** | SI el crédito combina baja fricción + tasa usuraria (CAT>100%) + reporte crediticio incompleto (BNPL) ENTONCES la adopción produce daño downstream — concentración de mora, quejas de cobranza — PORQUE la advertencia es condicional a la estructura, no a la conducta. |
| 5 | `civico.voto.agencia_con_secreto` | §3.7 (L553) | `[FUERTE]` **(a)** | SI hay transferencia universal no condicionada Y NO hay proximidad/focalización del reparto Y NO hay monitoreo percibido del voto ENTONCES conserva autonomía de la ELECCIÓN de voto — PORQUE no hay monitoreo del voto individual ni sanción creíble. |
| 6 | `civico.voto.clientelar_si_observable` | §3.7 (L554) | `[MEDIA]` **(a)** | SI hay proximidad/focalización del reparto O el votante percibe que su voto puede ser monitoreado ENTONCES la autonomía CEDE localmente — PORQUE cálculo racional bajo incertidumbre sobre el secreto del voto. Cantú 2019, Ascencio-Chang 2025 (lab: 0.06→0.63) citados en canon. |
| 7 | `civico.transferencia.atribucion_lider` | §3.7 (L557) | `[MEDIA]` **(a)**, correlacional, ⚠️ CONFUNDIDO | SI hay transferencia universal no condicionada ENTONCES la atribución va al líder y se expresa como aprobación, no como voto comprado — PORQUE premio retrospectivo al desempeño e identidad partidista. Falsador ya pre-registrado: RDD sobre la Pensión del Bienestar con efecto electoral independiente de la aprobación presidencial. |
| 8 | `civico.protesta.agravio_urbano` | §3.7 (L558) | `[MEDIA-FUERTE]` **(a)** | SI hay agravio personal/familiar + falla estatal palpable + red previa Y el entorno es urbano con espacio público disponible ENTONCES se suma a protesta (8M: mujeres jóvenes urbanas; colectivos de búsqueda: familiares) — PORQUE G4 (destructor selectivo). |
| 9 | `familia.cortejo.urbano_joven_apps` | §3.5 (L538) | `[MEDIA / HIPÓTESIS]` | SI el cortejo es urbano-joven-conectado (15-29, `tam_loc`=1, `conex_inte`=1) ENTONCES apps + lógica de mercado, guiones de género se reconfiguran desigual (actitud rápida, conducta lenta) — PORQUE cohorte + exposición. |

### 1.2 Objeto medible por regla — tal como está escrito, sin clasificar aún

| # | id | objeto medible |
|---:|---|---|
| 1 | evasión | en población con exposición a una norma/trámite concreto: (i) percepción de utilidad/extractividad de esa norma + (ii) percepción de probabilidad de sanción + (iii) conducta de evasión autorreportada — que (i) baja y (ii) baja prediga (iii) alta, separando evasión de subsistencia de evasión por cinismo de clase alta. |
| 2 | seguro depósito | en población con capacidad de ahorro: si conocer/percibir un seguro de depósito visible (IPAB) o una marca confiable predice menor aversión al ahorro formal/fintech frente a quien no lo percibe. |
| 3 | scoring alternativo | el IMOR (índice de morosidad) de cartera de consumo del sector popular, contra el umbral pre-registrado (~25–30% sostenido, techo de CAT agotado) — un objeto **administrativo/regulatorio**, no una conducta de hogar. |
| 4 | daño downstream (N34) | entre usuarios de crédito de baja fricción + CAT>100% + reporte incompleto (BNPL): concentración de mora/quejas de cobranza **del lado del deudor-consumidor**, no del acreedor-empresa. |
| 5 | secreto del voto | entre beneficiarios de transferencia universal SIN proximidad/focalización Y SIN percepción de monitoreo del voto: que el tamaño del beneficio no prediga a quién votan. |
| 6 | voto clientelar | entre quienes SÍ perciben proximidad/focalización O posible monitoreo de su voto: que la elección de voto cambie, frente a quien no lo percibe. |
| 7 | atribución al líder | entre beneficiarios: que la atribución del apoyo vaya al líder/presidente (como aprobación, no como voto comprado), aislada de aprobación presidencial general e identidad partidista — ya declarado CONFUNDIDO en canon. |
| 8 | protesta | entre quienes reportan agravio personal/familiar + falla estatal percibida + red previa, en entorno urbano con espacio público: que se sumen a protesta más que quienes tienen las mismas condiciones sin esas tres piezas. |
| 9 | cortejo por apps | entre jóvenes urbanos conectados (15-29, `tam_loc`=1, `conex_inte`=1): que el cortejo ocurra vía apps y que actitud y conducta de guion de género se muevan a ritmos distintos. |

**Nota metodológica, aplica a las 9.** `tools/busca_reactivos.py` indexa `texto_reactivo`
+ `variable_id` de payloads de encuesta/microdato bajo `descargas_mx*` — su universo es
**reactivo de hogar**, nunca serie administrativa/regulatoria publicada (boletines,
índices de un regulador). El objeto de la regla 3 (`scoring_alternativo`) es
estructuralmente invisible a esta herramienta por diseño del universo, no por ausencia
real de dato — distinción que importa para no confundir "el buscador no lo encontró"
con "no existe la fuente" (A.13: un cero producido por un comando que no examinó el
tipo de archivo correcto no es lo mismo que un cero sobre el universo correcto).

### 1.3 Criterio de clasificación — antes de proponer nada, verbatim del encargo

- **(a) REFORMULABLE** — existe en el inventario un reactivo que mide el mismo driver
  con otro desenlace (o el mismo desenlace con otro encuadre del driver): el objeto se
  reescribe para anclarse a lo que el reactivo realmente mide, sin inventar dato.
- **(b) SIN-INSTRUMENTO** — el objeto exige una condición que ningún instrumento
  nacional mide hoy: se escribe cuál condición falta, con el comando de
  `busca_reactivos.py` a la vista, el universo examinado y los términos probados.
- **(c) CON-CANDIDATA** — existe una fuente nombrada y conocida (household o
  administrativa) que podría resolver el objeto, pendiente de adquisición o de lectura
  completa — el caso de referencia es `N34`/ENCRIGE.

Regla operativa que este acto sigue, declarada para que se pueda auditar: (a) exige que
el reactivo encontrado mida el **driver** (no solo una palabra suelta del enunciado) —
un acierto de `busca_reactivos.py` que solo coincide por substring sin relación
conceptual con el mecanismo **no** cuenta como (a), se declara ruido y el veredicto cae
a (b) o (c) según corresponda.

---
