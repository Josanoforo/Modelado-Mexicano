# P3 · criterios previos

PROPUESTO-POR-EJECUTOR. Se escribe antes de ejecutar el cálculo. No adopta
umbrales ni modifica emisiones previas. Fuente: encargo ASTRA6-C2-FRONTERA-1,
P3 y ADENDA-1 C2. Todas las cantidades de escenario son supuestos de diseño,
no RESULT ni estimaciones extraídas de una ola.

1. Error familiar bilateral 0.05; Bonferroni por grupos × olas objetivo,
   válido aun con dependencia. Potencia exigida 0.80.
2. Una conclusión es informativa si el IC simultáneo del cambio queda entero
   dentro de la banda de equivalencia, o entero por encima o debajo de ella.
   Un IC que toca/cruza un límite es inconcluso. Informativa no significa
   predicción acertada: es capacidad de discriminar después de medir.
3. Lanzar requiere oro ejecutado/comparable, lector validado y probabilidad
   informativa ≥0.80 bajo estabilidad y cambio material, en cada grupo y en
   escenario temporal adverso. Si falta calibración histórica: no lanzar
   todavía; una frontera de factibilidad no sustituye el oro.
4. Separar varianza muestral histórica y futura de dispersión temporal.
   Para proporciones de escenario se usa p=.5 (cota conservadora), n efectivo
   500/2000/10000 por grupo/ola, rho muestral 0/.5/.8, desviación temporal
   0/.01/.03. Son escenarios, no tamaños reales ni covarianzas estimadas.
5. Cambio material de diseño: dos veces la semibanda; estabilidade: cero.
   Semibanda .05: propuesta de persistencia local de P2 para ENSU,
   fijada antes del oro; no se estima a partir del dato futuro.
   MDE se obtiene resolviendo potencia bilateral exacta normal ≥.80.
6. El intervalo usa solo error muestral; la probabilidad prospectiva integra
   separadamente la dispersión temporal normal asumida. Las réplicas del oro
   solo pueden calibrar error muestral, nunca variación temporal futura.
7. ENOE: rho entre oro y objetivo solo se usa si realmente comparten panel;
   si están separados por más de la rotación, rho=0. Varias olas cercanas
   comparten hogares y requieren covarianza agrupada por hogar/UPM. No sumar
   tamaños como independientes. ENSU/otras: rho no se presume del calendario.
8. Subgrupos comparten diseño y factores calibrados: Bonferroni evita asumir
   independencia; no se multiplican sus probabilidades. La probabilidad
   conjunta se acota por max(0,1−Σ(1−P_i)), conservador sin covarianzas.

Cero retadores. Estos cálculos son una frontera condicional de planificación,
no una corrida ni una emisión congelada. Sin simulación aleatoria: integración
normal analítica reproducible, sin semilla.

Selección recibida antes del cálculo: ENSU CD01, BP1_1=2 sobre códigos 1/2/9,
18+, dos grupos SEXO y una ola objetivo 2027T4, oro 2025T4. Para ENSU se
reportará rho=0 como caso conservador; rho positivo solo sensibilidad, jamás
ganancia de precisión acreditada sin covarianza histórica. No se reutilizarán
oro ni incertidumbre de ENSU para los otros instrumentos.

Extensión antes de cálculo ENOE: candidato marginal informalidad EMP_PPAL=1
entre ocupados 15–98, grupos SEX1/2, oro2024T4→2027T4. Mismos alpha/banda/
criterios por familia; no se afirma control .05 conjunto de ambas familias.
La separación de tres años no demuestra independencia de UPM. Se usa rho=0
conservador, y el SE futuro=SE oro sigue siendo supuesto. ENOE no reutiliza
réplicas ni n efectivos de ENSU. La rotación no convierte el estimando marginal
en seguimiento de la misma persona. Se mantiene escenario temporal adverso
.03 aunque haga fallar informatividad; nunca se lo ajusta después del oro.

Distinción de estimandos de inferencia: p0 emitido es el número histórico fijo.
Evaluar el futuro respecto a ese número usa solo SE futuro; el script lo
reporta como `conditional_fixed_p0_*`. El dictamen científico conservador
adicional pregunta por cambio físico entre poblaciones de ambas olas e incluye
SE del oro. No cambia p0 ni las reglas del paquete. Informatividad principal
de P3 se refiere explícitamente a ese cambio físico, no a una emisión nueva.
