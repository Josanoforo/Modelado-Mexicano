# AMAI: contrato humano completo de sucesor

PROPUESTO-POR-EJECUTOR. Requiere firma por contenido; ENIF2024 AMAI requiere
autorización propia de tablas/columnas aparte de la apertura de ahorro.
No adopta el procedimiento ni valida los históricos. Fuente humana:
forense/prereg-caja/AMAI-NSE-spec-v1_0.md §§1–5, métodos humanos de las entradas
#1185 ENIF0001/0002, ENDUTIH2023 y definiciones de familiares-vejez. Es D-15 que
la spec histórica remita a helpers para conductas/EE. Lo escrito abajo es la
propuesta cerrada que resuelve ese vacío para un sucesor, no una atribución al
código congelado. Los porcentajes nacionales publicados AMAI y sus veredictos
de comparación se excluyen del paquete de reconstrucción: comparación aparte.

Unidad NSE hogar; una jefatura por hogar; llave/join no único devuelve error.
CSV/DBF conserva texto en llaves. Código numérico equivalente se normaliza solo
en reactivos; blanco/NS/NR no se imputa. Datos válidos de los seis componentes
obligatorios; hogar incompleto SIN-NSE, contado. Sumar puntos:

| Componente | Código o valor → puntos |
|---|---|
| educa_jefe | 01,02→0;03→6;04→11;05→12;06→18;07→23;08→27;09→36;10→59;11→85 |
| baños completos | 0→0;1→24;2+→47 |
| autos | 0→0;1→22;2+→43 |
| internet | no→0;sí→32 |
| ocupados | 0→0;1→15;2→31;3→46;4+→61 |
| dormitorios | 0→0;1→8;2→16;3→24;4+→32 |

Niveles: E=[0,47];D=(47,94];D+=(94,115];C−=(115,140];C=(140,167];
C+=(167,201];A/B>201. BAJO=E,D,D+;MEDIO=C−,C;ALTO=C+,A/B. Cero se incluye
en E y su masa se informa. Variables de cantidad deben ser enteros>=0;
códigos fuera del cuestionario detienen; no truncar negativos ni faltantes.

ENIGH2022: concentradohogar une hogares por folioviv+foliohog y viviendas por
folioviv; exigir unicidad en la tabla correspondiente y cobertura completa.
educa_jefe/ocupados/factor/est_dis/upm del concentrado; conex_inte=1 internet,
=2 no; autos=num_auto+num_van+num_pickup de hogares; baños=bano_comp y
dormitorios=cuart_dorm de viviendas. Hogares de la misma vivienda comparten
componentes, conservando cada factor de hogar. remesas>0 recibe, ==0 no;
remesas negativa/nula/no finita fuera, contada. Pisos hogar por grupo NSE.

ENIF2024: TVIVIENDA por LLAVEVIV, THOGAR por LLAVEHOG, roster por hogar y
persona, TMODULO por LLAVEMOD; el descriptor debe acreditar enlace y unicidad
antes de materializar. Jefatura PAREN=1. NIVEL/GRADO: 00→educa01;01→02;
02 primaria grado<6→03,>=6→04;03 secundaria grado<3→05,>=3→06;
04 normal básica y05 técnica secundaria→06;06 preparatoria grado<3→07,
>=3→08;07 técnica preparatoria→08;08 licenciatura grado<4→09,>=4→10;
09 especialidad,10 maestría,11 doctorado→11. 99/blanco SIN-NSE. Baños=P0_3,
dormitorios=P0_1; P0_4_1=2 autos0,=1 autosP0_4_1A; internet sí si
P0_4_2=1 yP0_4_2A=1;no siP0_4_2=2 oP0_4_2A=2;resto inválido.
Ocupados=P2_8 entero0..90;>90 faltante. NSE distribución con FAC_HOG,
pisos personas elegidas EDAD_V18..98 con FAC_PER>0; diseño EST_DIS/UPM_DIS.
Ocupados remunerados sin corte14+ constituye aproximación declarada.

ENDUTIH2023: llave hogar UPM,VIV_SEL,HOGAR; roster completo para jefatura
PAREN=1 NIVEL/GRADO con regla anterior; ocupados cuenta residentes EDAD14..97
con P3_10 en1,2 o P3_11 en1,2,3. Auto binario P1_5_3=1/2. Internet hogar
sí siP4_4=1 yP4_5 en1,3;no siP4_4=2 oP4_5=2. No imputar respuestas inválidas.
Donante ENIGH2022 requiere los seis componentes válidos y factor>0; definir
A=puntos(baños)+puntos(dormitorios)+puntos(autos). Media ponderada de A en
celda educa_jefe,internet,min(ocupados,4),con_auto; si n<30 usar
educa_jefe,internet,con_auto;si n<30 usar con_auto. Si última celda vacía,
SIN-NSE; no completar desde otro universo. Donación determinista sin redondear
media antes de cortar NSE. Donante se congela una vez; no reimputar por réplica:
inferencia condicional al donante, no incertidumbre completa de imputación.
Hogar factor FAC_HOG; personas usuarios+usuarios2 por UPM,VIV_SEL,HOGAR,NUM_REN
exigiendo1:1 completo, EDAD>=6,FAC_PER>0,EST_DIS/UPM_DIS. Faltantes fuera.

| Conducta ENDUTIH2023 | Universo válido | y=1; y=0 |
|---|---|---|
| internet | P7_1 en1,2 | P7_1=1;=2 |
| celular | P8_1 en1,2 | P8_1=1;=2 |
| actividad_mensajes | P7_1=1,P7_12_3 en1,2 | =1;=2 |
| actividad_tramite | P7_1=1,P7_35_4 en1,2 | =1;=2 |
| no_internet_acceso/costo/preferencia | P7_1=2,P7_2 en1..8 | P7_2=1/4/3 respectivamente;otros1..8 |
| no_celular_costo/preferencia/cobertura | P8_1=2,P8_2 en1..8 | P8_2=1/2/3 respectivamente;otros1..8 |

Actividad empleo no entra. Mensajes/internet tres meses, trámites12meses;
sus dominios son usuarios actuales. SALTO/NR/NS contados, nunca negativos.

| Conducta ENIF2024 | Universo y desenlace |
|---|---|
| formal_cualquiera F | Toda persona18+;1 si algúnP5_6_1..9=1;0 si ninguno;blanco estructural sin cuenta no aporta1;otros inválidos se cuentan |
| informal_cualquiera I | Toda persona18+;1 si algúnP5_1_1..6=1;0 si ninguno;8/9/inválidos contados, no convertidos a1 |
| ambas_vias,solo_formal,solo_informal,no_ahorra | Mismo universo: F∧I,F∧¬I,¬F∧I,¬F∧¬I; partición conjunta, no independencia |
| tiene/no_tiene_ahorros | F∨I; complementario, mismo universo; no usar P4_10=1 para inferir ausencia |
| horizonte_corto/no_corto_sin_ss | P3_13=7,P4_10 en1..5; corto1,2;no_corto3,4,5 |
| horizonte_corto/no_corto_con_ss | P3_13 en1..4,P4_10 en1..5; corto1,2;no_corto3,4,5 |
| horizonte_corto_no_trabaja | P3_8=8 oP3_9=7,P4_10 en1..5;1 si1,2;0 si3..5; no equivale a P3_13 blanco |
| desconfia_conoce/no_conoce_proteccion | P5_20 en01..10 yP5_23=1/2 respectivamente;1 siP5_20=03;0 resto01..10; cualquier P5_23 blanco invalida el eje |
| recibe/no_recibe_dinero_familiares_para_vejez | FILTRO_S9_1=2,EDAD_V<71,P9_9_4 en1,2;=1 recibe;=2 no_recibe |

Propuesta de regla explícita para F/I: códigos válidos1/2 y blanco estructural
de P5_6; un inválido no estructural con ninguna respuesta1 deja F/I desconocido
y sale del denominador de las particiones, contado; con alguna1 es evento
observado. Esta convención conservadora requiere firma y no se atribuye a los
helpers históricos. Las 49 identidades ENIF se conservan en su mapa; el contrato
no amplía a celdas no presentes. P4_10=1 mezcla sin ahorros y menos de semana;
P5_20=03 mezcla desconfianza y mal servicio. Asociaciones, no causalidad.

Por conducta y grupo: d=universo válido∩grupo; p=sum(w*d*y)/sum(w*d).
Marcos completos de cada tabla con peso/diseño válidos; UPM fuera de dominio
aportan cero. Suprimir si n<200,UPMdominio<2 o dispersión réplicas nula.
Plan1000réplicas de UPM con reposición por estrato;PCG64(20260924);estratos/UPM
texto orden lexicográfico; iteración réplica luego estrato, m_h extracciones
uniformes por estrato; multiplicidad sobre w; plan común a grupos/conductas de
la misma tabla. Cuantiles lineales tipo7 0.025/0.975; réplica sin denominador
=>VARIANZA-NO-ESTIMABLE en esa celda, no eliminarla silenciosamente.
Singleton aporta cero, se cuenta/rotula, sin afirmar cota garantizada.
Salidas por identidad: punto,IC,n,masa,UPM,estado; distribución siete niveles
con ponderador hogar y denominador hogaresNSEválido; masaSIN-NSE separada.
No transportar valores de validación externa AMAI ni objetivos históricos.
