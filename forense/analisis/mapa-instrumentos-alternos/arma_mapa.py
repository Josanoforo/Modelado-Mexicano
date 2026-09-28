#!/usr/bin/env python3
"""Ensambla canon/mapa-instrumentos-alternos-v1_0.tsv (GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1).
Uso: python3 forense/analisis/mapa-instrumentos-alternos/arma_mapa.py [--verifica]
(--verifica: no escribe; compara byte a byte contra el mapa commiteado y sale 1 si difiere).
Cada fila es un dictamen del hilo principal. texto_pregunta sale de una fila auditada de lote
(L=('A',i)) o se da literal con el doc donde se verifica (T=(texto, doc_txt)). Nada de cifras."""
import csv, io, os, sys
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lotes')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'canon', 'mapa-instrumentos-alternos-v1_0.tsv')
lot = {k: list(csv.DictReader(open(f'{S}/lote_{k}.tsv'), delimiter='\t')) for k in 'ABCD'}

REGLA = {'M05': 'tramite.evasion_norma', 'M09': 'R1.4', 'M10': 'R2.1', 'M11': 'R2.2', 'M12': 'R3.4',
         'M13': 'R7.1', 'M14': 'R7.3', 'M15': 'R7.4', 'M16': 'R7.5', 'M17': 'R8.1', 'M18': 'R8.2',
         'M19': 'R8.3', 'M20': 'R10.1', 'M21': 'R10.2', 'M22': 'R10.3',
         'M23': 'dinero.ahorro.via_informal', 'R03': 'tramite.mordida.discrecional'}
COLS = ['incognita', 'regla', 'instrumento', 'ola', 'unidad', 'id_manifiesto', 'archivo_leido',
        'seccion_o_pagina', 'texto_pregunta', 'codigo_variable', 'que_falta_para_la_incognita',
        'dictamen_A4', 'reserva', 'acceso', 'propuesta', 'procedencia', 'origen_fila', 'cita_previa',
        'verifica_en']

BARRIDO = ('tools/busca_reactivos.py --tablas todas, 27/sep/2026: 314 256 identidades revisadas, '
           '113 780 con texto (9 tablas)')
R_LAPOP23 = 'RESERVADA (LAPOP 2023: forense/notas/2026-09-25-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-cierre.md, tabla CALC)'
R_ENVIPE26 = 'RESERVADA (ENVIPE 2026: canon/MEMORIA-OPERATIVA.md §1)'
R_ABIERTA_MO = 'ABIERTA (canon/MEMORIA-OPERATIVA.md §1: ENCIG 2025 y ENVIPE 2025 abiertas)'
R_ENVE24 = ('SIN-CAMPO-EN-MANIFIESTO · ola más reciente de ENVE (RNM: 2012–2024; 2020 y 2022 fuera del corpus) '
            '→ reservable por letra de E.6 · F5-panel-candidatos-v1_3 E04-CIV-ENVE la declara EXPUESTA · mesa decide')
R_ENCRIGE20 = ('SIN-CAMPO-EN-MANIFIESTO · ola más reciente de un programa con historia (2016) → reservable por letra de E.6 · '
               'tabulados ya vistos por #826 (GEN2-ENCRIGE-DESCRIPTIVA-1) · F5 R08 trata 2016 como la reserva · mesa decide')
R_SIN = 'SIN-CAMPO-EN-MANIFIESTO (no es la ola más reciente de su programa en el corpus)'
R_CSES5 = ('SIN-CAMPO-EN-MANIFIESTO · módulo más reciente de CSES en el corpus → reservable por letra de E.6 · '
           'F5 E05 lista CSES como familia EXPUESTA · base no abierta aquí')

rows = []
def R(inc, instr, ola, unidad, idm, arch, secc, texto, cod, falta, dic, res, acc, prop,
      proc='(a) dato primario en México', origen='PEDIDO-ENCARGO', cita='', L=None, T=None):
    if L:
        t = lot[L[0]][L[1]]['texto_pregunta']; ver = f'lote_{L[0]}:{L[1]}'
    elif T:
        t, ver = T
    else:
        t, ver = texto, ''
    rows.append(dict(incognita=inc, regla=REGLA[inc], instrumento=instr, ola=ola, unidad=unidad,
                     id_manifiesto=idm, archivo_leido=arch, seccion_o_pagina=secc,
                     texto_pregunta=' '.join(t.split())[:240], codigo_variable=cod,
                     que_falta_para_la_incognita=falta, dictamen_A4=dic, reserva=res, acceso=acc,
                     propuesta=prop, procedencia=proc, origen_fila=origen, cita_previa=cita,
                     verifica_en=ver))

DDI691 = 'encrige2020_rnm691_ddi'; DDI1058 = 'enve2024_rnm1058_ddi'; DDI227 = 'enve2016_rnm227_ddi'

# ───────────────────────── R03 · empresa ─────────────────────────
R('R03', 'ENCRIGE', '2020', 'empresa (razón social); universo nacional, todos los tamaños',
  f'encrige2020_cuestionario;{DDI691};gen2_encrige2020_diseno_muestral',
  'UNIVERSO-2026-09/ENCRIGE/encrige2020_cuestionario.pdf; inegi_rnm_ddi/encrige2020_rnm691_ddi.xml; GEN2_FUENTES_FINANCIERAS_20/encrige2020_diseno_muestral.pdf',
  'Cuestionario Secc. IX p20 (9.1–9.5), Secc. V p7–8 (5.5–5.8), Secc. VIII p12–17 (8.3, 8.7.1), Secc. I p3 (1.4); DDI archivos TR_ENCRIGE2020 y TR_ENCRIGE2020_TRAMITES; diseño muestral Cuadro 3 p9 y §10 p17–18',
  None, 'P9_3_1..P9_3_3 (i); P9_2 (ii); P9_4/P9_5 (i, por trámite); P5_5, P5_7/P5_8, P8_3, P8_714_H, P8_16* (iii); P1_4/P1_4CAL, GRAN_SECTOR, E03 (iv); FAC_EXP (v)',
  'Microdato no distribuido por RNM (catálogo 691); estrato/UPM no aparecen como variables en el DDI (solo FAC_EXP; el estrato se documenta en el PDF de diseño); el universo incluye grandes (filtrar por P1_4CAL); unidad empresa, no persona: cambio de unidad frente a la regla (misma firma que R02); periodo 2020 (pandemia)',
  'EXISTE-SATISFACE-PARCIAL(los cinco ítems i–v existen por variable con texto de pregunta; faltan vía de acceso al microdato y variables de diseño ejecutables)',
  R_ENCRIGE20, 'documentación EN-CORPUS; microdato NO-DISTRIBUIDO-EN-RNM (catálogo 691, 27/sep/2026: «Data Access Not Available»)',
  'RE-ESPEC (R03 se funde con la familia R08 sobre ENCRIGE 2020: descriptiva, unidad empresa, sin transferencia a persona por la firma F-19; ver propuesta-R03.md) · SOLICITUD(INEGI, Laboratorio de Microdatos: TR_ENCRIGE2020 y TR_ENCRIGE2020_TRAMITES)',
  cita='#826 CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001 (tabulados; se cita, no se re-mide, E.5)', L=('A', 15))
R('R03', 'ENCRIGE (tabulados de datos abiertos)', '2020', 'empresa; agregados publicados por tamaño, sector y entidad',
  'conjunto_de_datos_encrige_2020_csv', 'UNIVERSO-2026-09/ENCRIGE/conjunto_de_datos_encrige_2020_csv.zip (solo 0_indice_tablas: títulos)',
  'índice de tablas, conjunto VI (t6_24–t6_42) y II (t2_19–t2_22); no se leyeron cifras', None,
  't6_33; t6_36; t6_41; t2_19..t2_22',
  'Son tabulados: sin microdato, sin error de diseño, sin cruce carga regulatoria × corrupción en la misma unidad; cuatro tamaños oficiales',
  'EXISTE-SATISFACE-PARCIAL(prevalencia e incidencia de corrupción en trámites por tamaño publicadas; sin cruce ni incertidumbre)',
  R_ENCRIGE20, 'EN-CORPUS (tabulados)', 'NADA (ya extraído y sellado por #826: se cita)',
  cita='#826', T=('Unidades económicas que realizaron al menos un trámite o fueron sujetas a una inspección por tamaño según conocimiento y/o participación en actos de corrupción', 'conjunto_de_datos_encrige_2020_csv'))
R('R03', 'ENCRIGE', '2016', 'establecimiento (según informe de dirección, no verificado)',
  'cc1_inegi_encrige_2016__ejemploencrige_csv', 'ninguno (documentación no leída)',
  'manifiesto por id: 1 entrada ENCRIGE 2016 (base de EJEMPLO, raiz reserva_respondentes, RESERVADA-NO-ABIERTA-NO-INDEXAR-L); 0 cuestionarios y 0 FD de 2016 en el corpus; RNM catálogo 264 consultado solo en su página de acceso («Data Access Not Available»)',
  'SIN-TEXTO: documentación de 2016 no leída por la preservación declarada en F5 R08', '—',
  'forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv fila R08-TRA-ENCRIGE-CORRUPCION: «La ola 2016 no se toca ni en documentación hasta la fase confirmatoria»; el encargo pide 2016 pero leerla consumiría esa preservación',
  'NO-VERIFICABLE-SIN-ABRIR-RESERVA(comando que lo haría: curl https://www.inegi.org.mx/rnm/index.php/metadata/export/264/ddi y registrar por tests/manifiesto.py --registra; solo si mesa levanta la preservación F5 R08)',
  'RESERVADA-NO-ABIERTA-NO-INDEXAR-L (manifiesto) + preservación F5 R08', 'microdato NO-DISTRIBUIDO-EN-RNM (catálogo 264)',
  'OBTENER(DDI y cuestionario ENCRIGE 2016 del RNM 264, condicionado a decisión de mesa sobre F5 R08)')
R('R03', 'ENVE', '2024', 'establecimiento (unidad económica); universo nacional por estrato de tamaño×sector',
  f'cuestionario_principal_enve2024;modulo_delitos_enve2024;{DDI1058}',
  'UNIVERSO-2026-09/ENVE/cuestionario_principal_enve2024.pdf; inegi_rnm_ddi/enve2024_rnm1058_ddi.xml',
  'Cuestionario principal Secc. VI p9–10 (6.1–6.7), Secc. III p6 (3.4), Secc. II p3 (2.1); DDI archivo TC_Principal',
  None, 'P6_1..P6_4 (i); P6_5, P6_6/P6_7 (i, número y monto); ESTRATO, GRAN_SECT, E03 (iv); FAC_EXPA (v); P3_4_* (ii débil: corrupción de autoridades, no de otras empresas); P2_1_* (iii débil: ranking de temas)',
  'No pregunta «otras unidades le refirieron» (ii) ni horas o gasto en trámites (iii); unidad establecimiento, no empresa; periodo 2023; tamaño viene del marco (ESTRATO), no de una pregunta',
  'EXISTE-SATISFACE-PARCIAL(experiencia directa de corrupción, tamaño, sector y factor de expansión; faltan ii y iii)',
  R_ENVE24, 'documentación EN-CORPUS; tabulados EN-CORPUS no leídos; microdato: RNM catálogo 1058 con plantilla de acceso abierto, sin enlace verificado: SIN-FETCH (A.6)',
  'RE-ESPEC (segundo instrumento descriptivo de R03, unidad establecimiento; F-19) · OBTENER(microdato ENVE 2024 por RNM 1058, tras dictamen de reserva)',
  L=('A', 21))
R('R03', 'World Bank Enterprise Survey México', '2023', 'establecimiento formal (5+ empleados), manufactura y servicios',
  'wbes_mexico_2023_ddi_xml;wbes_mexico_2023_microdato_dta_zip', 'MEX_2023_WBES_v01_M.xml (DDI: etiquetas de variable; sin qstnLit)',
  'DDI secciones C, G, J (etiquetas); a6a, strata, wstrict/wmedian', None,
  'c5, c14, g4, j5, j12, j15 (i: pago informal pedido por trámite o inspección); j7a/j7b (monto); j2 (iii: % de tiempo gerencial en regulación); a6a (iv); strata, wstrict/wmedian (v)',
  'No pregunta «otras unidades» (ii); unidad establecimiento; fuente (a) internacional con diseño propio; F5 R02 ya es la familia descriptiva de soborno por establecimiento y la firma F-19 cerró la transferencia a persona',
  'EXISTE-SATISFACE-PARCIAL(pago informal por trámite, carga regulatoria, tamaño y diseño en microdato del corpus; falta ii; unidad distinta)',
  'SIN-CAMPO-EN-MANIFIESTO · no es la ola más reciente (F5 R02: 2026 en manifiesto) · preservación F5 R02: spec antes de abrir el microdato',
  'EN-CORPUS (microdato .dta y DDI)', 'NADA nuevo: es la familia R02 (descriptiva por F-19); R03 se funde con R02/R08',
  origen='PROPUESTO-POR-EJECUTOR', cita='forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv línea 3 (R02) y firma F-19',
  T=('In Any of These Inspections Was A Gift/Informal Payment Requested ?', 'wbes_mexico_2023_ddi_xml'))
R('R03', 'ENVE', '2016', 'establecimiento', f'cc1_inegi_enve_2016__enve_2016_csv;{DDI227}',
  'corpus-completo/inegi/enve/2016/enve_2016_csv.zip (esquema: encabezados); inegi_rnm_ddi/enve2016_rnm227_ddi.xml',
  'DDI archivo Cuestionario (p29_*, p30_*, fac_expa); esquema trenvecuest_esq_2016 (ID_ESTRATO, SECTOR, CVE_ENT, FAC_EXPA)',
  None, 'p29_1, p29_1x, p30_1.. (i, año 2015); ID_ESTRATO, SECTOR (iv); fac_expa (v); p18_* (ii débil)',
  'Sin ii ni iii; microdato solo en instalaciones del productor; periodo 2015',
  'EXISTE-SATISFACE-PARCIAL(experiencia directa de corrupción 2015 con factor y estrato; faltan ii y iii)',
  R_SIN + ' · ENVE EXPUESTA (F5 E04)', 'esquema y DDI EN-CORPUS; microdato solo en instalaciones del productor (RNM 227)',
  'SOLICITUD(INEGI, microdatos en instalaciones del productor) — prioridad baja: serie 2015 frente a 2023',
  T=('Durante 2015, ¿un empleado de gobierno o un servidor público intentó apropiarse de algún beneficio (dinero, regalos o favores)', DDI227))
R('R03', 'ENAPROCE', '2015/2018', 'empresa micro/pequeña/mediana', 'inegi_rnm_catalog_330_enaproce2015;inegi_rnm_catalog_518_enaproce2018',
  'forense/analisis/obtencion-previa-1/P4-I1-nota.md; forense/produccion/enaproce-instrumentos-acceso-1/CONTRATO-REACTIVOS.md',
  'cita de dictamen previo: P4-I1-nota.md §(i)–(ii); NOTA-DECISION.md l.13–18', 'SIN-TEXTO (cita de dictamen previo)',
  'M61–M64/P79–P82 (2015); M64_1..3, M65–M67, P81_6, P82–P84 (2018)',
  'ningún reactivo mide solicitud o pago informal; microdato solo por Laboratorio',
  'EXISTE-NO-SATISFACE(sin pago informal en ninguna vía; dictamen de OBTENCION-PREVIA-1 P4, se cita)',
  R_SIN, 'bases de ejemplo cegadas EN-CORPUS; microdato NO-ACCESIBLE por descarga (Laboratorio)', 'NADA para la parte mordida (carga regulatoria: ver P4-I1-solicitud-LM.md)',
  origen='CITA-OBTENCION-PREVIA-1', cita='forense/analisis/obtencion-previa-1/P4-I1-nota.md')

# ───────────────────────── M05 ─────────────────────────
R('M05', 'ENVIPE', '2025', 'delito (FAC_DEL); universo BP1_20 ∈ {1,2}', 'envipe2025_csv',
  'data/corrida0/CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002 (resultados sellados)',
  'cita: forense/analisis/obtencion-previa-1/P1-A1-M05-M23.tsv fila M05', 'SIN-TEXTO (cita de dictamen previo)', 'BP1_20; BP1_23',
  'unidad delito, no persona; estimando conjunto, no condicional a sanción creíble',
  'EXISTE-NO-SATISFACE(unidad delito y conjunta; dictamen de OBTENCION-PREVIA-1 P1, se cita)',
  R_ABIERTA_MO, 'EN-CORPUS (microdato)', 'NADA aquí (P1 ya propuso a mesa el recálculo a persona)',
  origen='CITA-OBTENCION-PREVIA-1', cita='P1-A1-M05-M23.tsv')
for ola, idm, arch, pag in [('2023', 'encig23_cuestionario_pdf;encig23_estructura_base_datos_pdf', 'encig23_cuestionario.pdf; encig23_estructura_base_datos.pdf', 'cuestionario Secc. VIII p20 (8.1–8.3), Secc. III (3.2–3.3), Secc. A (A.1), Secc. II p3 (2.7); estructura p35–36 y p61'),
                            ('2025', 'encig25_cuestionario_pdf;encig25_estructura_base_datos_pdf', 'gen2_corrupcion_fuente_general/encig25_cuestionario.pdf; encig25_estructura_base_datos.pdf', 'cuestionario Secc. VIII p20 (8.1–8.3), Secc. III (3.2–3.3), Secc. A (A.1), Secc. II p3–4 (2.7); estructura p37 y p62')]:
    R('M05', 'ENCIG', ola, 'persona 18+ en localidades de 100 mil habitantes y más', idm, arch, pag, None,
      'P8_1, P8_2, P8_3_1..P8_3_3, P8_4 (por trámite); P3_2, P3_3_*; ' + ('A1_*' if ola == '2023' else 'APA_1_* (mnemónico cambió respecto de 2023)') + '; NIV',
      'El desenlace es corrupción experimentada en trámites (conducta de M01/M02, ya servida por la serie ENCIG de #972), no evasión de norma; sin reactivo de sanción creíble (regex castig|sancion en cuestionario: 0 aciertos sustantivos) ni de norma percibida inútil; sin localidades menores de 100 mil',
      'EXISTE-NO-SATISFACE(mide corrupción sufrida en trámite, no evasión de norma; faltan los dos disparadores)',
      R_ABIERTA_MO if ola == '2025' else 'ABIERTA (no es la ola más reciente; serie usada por #972)', 'EN-CORPUS (microdato)',
      'NADA para M05 (sirve a M01/M02)', cita='#972 GEN2-ENCIG-SERIE-Y-TENDENCIA-1',
      T=(f'8.3 Durante {ola}, para agilizar, realizar, evitar procedimientos o multas en alguno de estos trámites, pagos o solicitudes:', 'encig23_cuestionario_pdf' if ola == '2023' else 'encig25_cuestionario_pdf'))
R('M05', 'LAPOP AmericasBarometer México', '2018/19', 'persona 18+, nacional', 'abmex18_v12_0_2_5_spa_190207_w;mexico_lapop_americasbarometer_2019_codebook_v1_0_w;mexico_lapop_americasbarometer_2019_v1_0_w',
  'Descargas Manuales/ABMex18-v12.0.2.5-Spa-190207_W.pdf', 'cuestionario p12 (EXC18)', None, 'EXC18',
  'Es actitud (justificación de pagar mordida), no conducta; no hay reactivo de sanción creíble en esta ola; mordida ≠ toda norma',
  'EXISTE-SATISFACE-PARCIAL(justificación de evadir la norma vía soborno, persona, nacional con escolaridad; falta la conducta y el disparador sanción creíble)',
  R_SIN, 'EN-CORPUS (microdato .dta, descargas_mx)', 'CALC-CAJA (EXC18 por escolaridad y urbano/rural, rotulado ACTITUD)', L=('B', 8))
R('M05', 'LAPOP AmericasBarometer México', '2021', 'persona 18+, nacional (levantamiento telefónico)', 'abmex2021_mexico_questionnaire_v17_2_5_2_spa_210420_w;mex_2021_lapop_americasbarometer_v1_2_w',
  'Descargas Manuales/ABMex2021-Mexico-Questionnaire-v17.2.5.2-Spa-210420-W.pdf', 'cuestionario p6 (PR3DNR) y p8–9 (EXC18)', None, 'PR3DNR; EXC18',
  'PR3DNR mide castigo probable por construir sin permiso (una norma concreta), no la sanción de la norma evadida; EXC18 es actitud; modo telefónico 2021 (el acto de pisos de confianza dejó 2021 fuera)',
  'EXISTE-SATISFACE-PARCIAL(disparador sanción creíble y justificación de soborno en el mismo respondente; falta conducta observada y norma percibida inútil)',
  R_SIN, 'EN-CORPUS (microdato .dta, descargas_mx)', 'CALC-CAJA (EXC18 por PR3DNR y escolaridad: la condicional que la regla escribe, en actitud)', L=('B', 13))
R('M05', 'LAPOP AmericasBarometer México', '2023', 'persona 18+, nacional', 'lapop_abmex2023_cuestionario_mexico;mex_2023_lapop_americasbarometer_v1_0_w',
  'lapop_abmex2023_cuestionario.pdf', 'cuestionario p33 (EXC18); PR3DNR ausente (lote B: 0 aciertos)', None, 'EXC18',
  'Sin sanción creíble en esta ola; actitud, no conducta',
  'EXISTE-SATISFACE-PARCIAL(justificación de soborno; falta disparador y conducta)', R_LAPOP23,
  'EN-CORPUS (microdato .dta/.sav, descargas_mx) — no abierto', 'NADA (ola reservada)', L=('B', 10))

# ───────────────────────── M09 · M11 · M20 (corpus) ─────────────────────────
R('M09', 'CORPUS (índice de reactivos)', 'todas', 'acto de compra', '—', 'tools/busca_reactivos.py (tablas del índice)',
  f'{BARRIDO}; términos: marca=254 (ruido: municipio, marcar), «marca propia»=0, «precio mas bajo»=0, sustituto=0; más ENNViH (cita P2)',
  'NO-ENCONTRADO', '—', 'Instrumento de compra con marca y sustituto funcional pareado D/E–A/B',
  'NO-ENCONTRADO(corpus completo por índice de reactivos; ENNViH EXISTE-NO-SATISFACE por P2)', '—', '—',
  'OBTENER(panel de compra con marca — Kantar/NielsenIQ — por OBTENCION-EXTERNA-1)', proc='—', cita='momentos-09-22.tsv fila M09')
R('M11', 'CORPUS (índice de reactivos)', 'todas', 'díada líder-empleado', '—', 'tools/busca_reactivos.py',
  f'{BARRIDO}; términos: patron=79 (solo posición en el trabajo), «trato del jefe»=0, lealtad=0; ENCUCI 2020 FD completo (patrón solo como posición)',
  'NO-ENCONTRADO', '—', 'Tipología de liderazgo benévolo/autoritario con desempeño o rotación',
  'NO-ENCONTRADO(corpus completo por índice y FD ENCUCI 2020)', '—', '—', 'OBTENER(panel de clima organizacional — OBTENCION-EXTERNA-1)', proc='—', cita='momentos-09-22.tsv fila M11')
R('M20', 'CORPUS (índice de reactivos)', 'todas', 'persona', '—', 'tools/busca_reactivos.py',
  f'{BARRIDO}; términos: rechazo=1 (Latinobarómetro 2024 TOTRECH, variable metodológica), «decir que no»=0, negarse=0',
  'NO-ENCONTRADO', '—', 'Rechazo indirecto codificado según asimetría de poder',
  'NO-ENCONTRADO(corpus completo por índice de reactivos)', '—', '—', 'OBTENER(estudio experimental de actos de habla fuera de universitarios — OBTENCION-EXTERNA-1)', proc='—', cita='momentos-09-22.tsv fila M20')

# ───────────────────────── M10 · M21 ─────────────────────────
for inc, lx in [('M10', 32), ('M21', 33)]:
    R(inc, 'ENCRIGE / ENVE', '2020 / 2024', 'empresa / establecimiento', 'encrige2020_cuestionario;cuestionario_principal_enve2024',
      'encrige2020_cuestionario.pdf; cuestionario_principal_enve2024.pdf',
      'ambos cuestionarios completos; regex de voz, sugerencias, buzón, jefe, retroalimentación: 0 aciertos sustantivos (lote A)',
      'NO-ENCONTRADO', '—', 'Clima laboral interno (voz, disenso, retroalimentación)',
      'NO-ENCONTRADO(ENCRIGE 2020 y ENVE 2024 completos)', '—', '—', 'NADA', proc='—', origen='PROPUESTO-POR-EJECUTOR')
    R(inc, 'ENCUCI', '2020', 'persona', 'encuci2020_fd_pdf', 'FD_ENCUCI2020.pdf',
      'FD completo; «jefe» solo jefe de hogar (Secc. III); supervisor=0; «queja en el trabajo»=0', 'NO-ENCONTRADO', '—',
      'Voz o retroalimentación en el trabajo', 'NO-ENCONTRADO(FD ENCUCI 2020 completo)', R_SIN, '—', 'NADA', proc='—')
    R(inc, 'CORPUS (índice de reactivos)', 'todas', 'empleado', '—', 'tools/busca_reactivos.py',
      f'{BARRIDO}; jefe=194 (jefe de hogar), supervisor=14 (más cercano: ENDIREH 2016 p7_15_4, denuncia de un incidente a un superior), desacuerdo=288 (60 revisados, ninguno laboral), retroalimentacion=0, «reconocimiento en publico»=0',
      'NO-ENCONTRADO', '—', 'Microdato de empleado con jerarquía, voz y canal (M10) o con exposición a retroalimentación y rotación (M21)',
      'NO-ENCONTRADO(corpus completo por índice)', '—', '—', 'OBTENER(ECCO/SFP y paneles organizacionales — OBTENCION-EXTERNA-1)', proc='—',
      cita=f'momentos-09-22.tsv fila {inc}')

# ───────────────────────── M12 ─────────────────────────
for ola, idm in [('2023', 'encig23_cuestionario_pdf'), ('2025', 'encig25_cuestionario_pdf')]:
    R('M12', 'ENCIG', ola, 'persona 18+, localidades de 100 mil y más', idm, f'{idm}', 'Secc. X Gobierno electrónico (10.1)', None,
      'P10_1_2, P10_1_3, P10_1_5',
      'Mide adopción de gobierno digital útil (trámite y pago en línea), no CoDi ni riesgo fiscal percibido; sin motivos de no uso (NO-ENCONTRADO en secciones VI–VII y X)',
      'EXISTE-SATISFACE-PARCIAL(lado «útil sin amenaza» del contraste; falta el lado coercitivo y el riesgo fiscal)',
      R_ABIERTA_MO if ola == '2025' else 'ABIERTA (no es la ola más reciente)', 'EN-CORPUS (microdato)', 'CALC-CAJA (adopción de trámite en línea por segmento, lado SPEI del contraste)',
      origen='PEDIDO-ENCARGO', L=('B', 18 if ola == '2023' else 19))
R('M12', 'ENIF', '2021', 'persona 18+', 'enif2021_fd_zip', 'enif_2021_fd_pdf.zip (enif_2021_estructura_del_archivo.pdf)', 'FD p33 (7.2)',
  None, 'P7_2', 'Solo conocimiento de CoDi; no uso ni riesgo fiscal',
  'EXISTE-SATISFACE-PARCIAL(conocimiento de CoDi; falta uso y riesgo fiscal)', R_SIN, 'EN-CORPUS (microdato)', 'CALC-CAJA (conocimiento de CoDi por segmento)',
  origen='PROPUESTO-POR-EJECUTOR', T=('7.2 ¿Conoce o ha escuchado del Cobro digital o CoDi?', 'indice:v1_2:105238'))
R('M12', 'ENIF', '2024', 'persona 18+', 'enif2024_fd_xlsx', 'enif_2024_fd.xlsx', 'FD hoja TMODULO filas 913 y 915 (7.2, 7.3)', None,
  'P7_2_1 (conoce CoDi); P7_3_1 (usó CoDi); P7_2_2/P7_3_2 (DiMo)',
  'Uso de CoDi sí; riesgo fiscal percibido no se separa de fricción',
  'EXISTE-SATISFACE-PARCIAL(adopción de CoDi medida; falta riesgo fiscal percibido)',
  'PARCIAL: ENIF 2024 es la ola más reciente; reservas vigentes por módulo/cruce (crédito; localidad×edad consumido por M23); módulo de pagos no verificado aquí', 'EN-CORPUS (microdato) — no abierto',
  'NADA hasta que mesa confirme el estado de reserva del módulo 7', origen='PROPUESTO-POR-EJECUTOR',
  T=('7.3 ¿Ha utilizado Cobro Digital o CoDi para realizar sus pagos?', 'indice:v1_2:105661'))
for ola, idm, ref in [('2023', 'endutih_2023_fd_endutih2023', 'hoja tic_2023_usuarios fila 413'), ('2024', 'endutih2024_fd_xlsx', 'hoja tic_2024_usuarios fila 413'), ('2025', 'endutih_2025_fd_endutih2025', 'hoja tic_2025_usuarios fila 449')]:
    R('M12', 'ENDUTIH', ola, 'persona usuaria de internet que pagó por internet', idm, f'FD ENDUTIH {ola} (xlsx)', f'FD {ref} (7.32)', None, 'P7_32_6',
      'Uso de CoDi como medio de pago por internet; sin riesgo fiscal ni motivos de no uso; universo condicionado a pagar por internet',
      'EXISTE-SATISFACE-PARCIAL(adopción de CoDi en pagos por internet; falta riesgo fiscal)',
      ('ola más reciente de ENDUTIH en el corpus → reservable por letra de E.6; verificar antes de abrir' if ola == '2025' else R_SIN),
      'EN-CORPUS (microdato)', 'CALC-CAJA (serie 2023–2024 de uso de CoDi entre quienes pagan por internet)' if ola != '2025' else 'NADA hasta dictamen de reserva',
      origen='PROPUESTO-POR-EJECUTOR', T=('7.32 ¿Su pago por internet ha sido con… mediante sistema de Cobro Digital (CoDi)?', f'indice:endutih{ola}:P7_32_6'))
R('M12', 'ENSAFI', '2023', 'persona 18+', 'ensafi2023_cuestionario_pdf', 'ensafi2023/ensafi_2023_cuestionario.pdf', 'Secc. 6 p15 (6.2), Secc. 7 p18 (7.2); NO-ENCONTRADO CoDi/DiMo/SPEI en cuestionario y FD', None,
  'P6_2_08; P7_2_4', 'Cuenta en app (Mercado Pago/Albo) o uso de app de finanzas; no CoDi ni riesgo fiscal',
  'EXISTE-NO-SATISFACE(no distingue CoDi/SPEI ni riesgo fiscal)', R_SIN + ' · F5 E05 lista ENSAFI como EXPUESTA', 'EN-CORPUS (microdato)', 'NADA', L=('D', 10))

# ───────────────────────── M13 ─────────────────────────
R('M13', 'CIDE-CSES (estudio electoral nacional, poselectoral)', '2015', 'persona; electorado de diputados federales 7/jun/2015 (intermedia) con 32 entidades',
  'cide_cses2015_nacional_poselectoral;cide_cses2015_nacional_preelectoral', 'UNIVERSO-2026-09/CSES/cide_cses2015_nacional_{pos,pre}electoral.sav (solo metadatos: nombres, etiquetas, valores)',
  'metadatos del .sav: p3, p17, p18, estado, peledip, PONDFIN; preelectoral: dominio2 («Tipo de elección local»: Gobernador / Sólo Presidente Mpal)',
  None, 'p3 (votó); p17 (qué partido gobierna importa, 1–5); p18 (el voto hace diferencia, 1–5); estado; dominio2; PONDFIN/PONDOM',
  'Falta la lista oficial de entidades con elección local concurrente en 2015 (calendario INE) para clasificar por estado; participación declarada (sobre-reporte); no es panel',
  'EXISTE-SATISFACE-PARCIAL(peso percibido y participación en el mismo respondente en una intermedia con entidades concurrentes y no concurrentes; falta el clasificador oficial de concurrencia)',
  R_SIN, 'EN-CORPUS (microdato .sav, descargas_mx)', 'CALC-CAJA (participación y p17/p18 por concurrencia local; clasificador desde calendario INE — OBTENER si no está en el corpus)',
  origen='PROPUESTO-POR-EJECUTOR', T=('Usando la escala que aparece en esta tarjeta, donde UNO significa que NO importa qué partido es el que gobierna y CINCO significa que SI HAY UNA GRAN DIFERENCIA, ¿dónde ubicaría lo que usted piensa?', 'sav:cide_cses2015_nacional_poselectoral:p17'))
R('M13', 'CSES Módulo 5 (estudio MEX_2018)', '2018', 'persona; elección presidencial concurrente 1/jul/2018; n de diseño 1 239 (codebook)',
  'cses5_modulo5_2016_2021_cuestionario;cses5_modulo5_2016_2021_codebook', 'cses5_Questionnaire.txt; cses5_codebook.zip',
  'cuestionario l.1503–1554 (Q14a/b), l.1121–1140 (Q12P1-a); codebook l.5469 (MEX_2018), l.18831–18837 (nota de país E3012_LH)',
  None, 'E3016_1 (Q14a); E3016_2 (Q14b); E3012_PR_1; E3014_PR_1; E1010_1..3',
  'México 2018 fue concurrente (presidencia y ambas cámaras el mismo día) y solo se preguntó participación presidencial: no hay contraste concurrente/no concurrente dentro del estudio; ID de distrito fuera del corpus',
  'EXISTE-SATISFACE-PARCIAL(peso percibido y participación en el mismo respondente; sin variación de concurrencia)',
  R_CSES5, 'EN-CORPUS (microdato cses5_csv.zip) — no abierto', 'CALC-CAJA (par con CIDE-CSES 2015: presidencial concurrente frente a intermedia)', L=('C', 2))
R('M13', 'ENCUCI', '2020', 'persona 15+; nacional urbano/rural', 'encuci2020_fd_pdf;encuci2020_bd_dbf', 'FD_ENCUCI2020.pdf', 'Secc. VII p47–48 (7.9, 7.10, 7.14)', None,
  'AP7_9; R7_10; AP7_14', 'Participación en 2018 (concurrente) y eficacia del voto; sin contraste de concurrencia',
  'EXISTE-SATISFACE-PARCIAL(participación y peso percibido del voto en el mismo respondente; sin variación de concurrencia)', R_SIN,
  'EN-CORPUS (microdato)', 'NADA (CIDE-CSES 2015 domina)', L=('D', 26))
R('M13', 'LAPOP AmericasBarometer México', '2018/19; 2021; 2023', 'persona 18+', 'abmex18_v12_0_2_5_spa_190207_w;abmex2021_mexico_questionnaire_v17_2_5_2_spa_210420_w;lapop_abmex2023_cuestionario_mexico',
  'tres cuestionarios', 'cuestionarios completos; VB2 presente; regex «diferencia»: 0 aciertos en los tres', None, 'VB2',
  'Solo participación; sin peso percibido del acto', 'EXISTE-NO-SATISFACE(sin peso percibido)', R_LAPOP23 + ' (2023); 2018/19 y 2021 sin campo',
  'EN-CORPUS (microdato)', 'NADA', L=('B', 37))

# ───────────────────────── M14 ─────────────────────────
for ola, cl, lx in [('2018', 'P044 (Beneficio del programa 65 y más)', 9), ('2020', 'P104', 10), ('2022', 'P104', 11)]:
    R('M14', 'ENIGH (nueva serie)', ola, 'persona (tablas poblacion e ingresos)', f'enigh{ola}_nc_csv', f'enigh{ola}_nc_csv.zip (catálogos y diccionarios de ingresos y poblacion)',
      f'catálogo de ingresos y diccionarios (lote C filas {lx}, {lx+3}, {lx+6})', None, f'clave={cl}; edad',
      'Da la primera etapa del RDD (recepción de la pensión por edad al umbral); no trae voto ni preferencia política (NO-ENCONTRADO en catálogos y diccionarios)',
      'EXISTE-SATISFACE-PARCIAL(primera etapa: recepción por edad; falta el desenlace de voto)', R_SIN, 'EN-CORPUS (microdato)',
      'CALC-CAJA (discontinuidad de recepción en 65/68 años; primera etapa)', L=('C', lx))
R('M14', 'CSES Módulo 5 (estudio MEX_2018)', '2018', 'persona', 'cses5_modulo5_2016_2021_cuestionario;cses5_modulo5_2016_2021_codebook', 'cses5_Questionnaire.txt; cses5_codebook.zip',
  'cuestionario l.1148–1157 (Q12P1-b), l.1022–1057 (Q09), l.2001–2002 (D01); nota de país de edad en codebook', None, 'E3013_PR_1; E3009; E2001_A',
  'Edad preguntada directa (no fecha de nacimiento: amontonamiento); sin recepción de transferencias (NO-ENCONTRADO); n chico para RDD',
  'EXISTE-SATISFACE-PARCIAL(forma reducida: voto por edad con evaluación del gobierno; falta recepción)', R_CSES5, 'EN-CORPUS (microdato) — no abierto',
  'NADA sola; combinable con ENIGH por edad (dos muestras) — decisión de spec', L=('C', 20))
R('M14', 'LAPOP AmericasBarometer México', '2018/19', 'persona 18+', 'abmex18_v12_0_2_5_spa_190207_w;mexico_lapop_americasbarometer_2019_v1_0_w', 'ABMex18-v12.0.2.5-Spa-190207_W.pdf',
  'cuestionario p2 (Q2), p7 (M1), p13 (VB20, VB3N), p14 (CLIEN1NA), p15–16 (MEXWF1_19)', None, 'Q2; VB3N; VB20; M1; CLIEN1NA; MEXWF1_19',
  'MEXWF1_19 excluye pensiones de jubilación o retiro: no identifica la Pensión Bienestar; n nacional chico para RDD',
  'EXISTE-SATISFACE-PARCIAL(edad, voto, aprobación presidencial y clientelismo; recepción de la pensión ambigua)', R_SIN,
  'EN-CORPUS (microdato .dta)', 'NADA sola (potencia insuficiente para RDD)', L=('B', 11))
R('M14', 'LAPOP AmericasBarometer México', '2023', 'persona 18+', 'lapop_abmex2023_cuestionario_mexico', 'lapop_abmex2023_cuestionario.pdf',
  'cuestionario p3 (Q2), p19 (M1), p35–37 (VB3N, VB20), p50–51 (MEXWF1_19); CLIEN*: 0 aciertos', None, 'Q2; VB3N; VB20; M1; MEXWF1_19',
  'Igual que 2018/19, sin CLIEN*; ola reservada', 'EXISTE-SATISFACE-PARCIAL(edad, voto y aprobación; recepción ambigua)', R_LAPOP23,
  'EN-CORPUS — no abierto', 'NADA (ola reservada)', L=('B', 36))

# ───────────────────────── M15 · M16 ─────────────────────────
R('M15', 'ENCUCI', '2020', 'persona 15+; DOMINIO urbano/complemento urbano/rural', 'encuci2020_fd_pdf;encuci2020_bd_dbf', 'FD_ENCUCI2020.pdf',
  'Secc. VII p39–40 (7.3, 7.4); Secc. I p11 (DOMINIO)', None, 'AP7_3_5, AP7_4_5 (protesta); AP7_3_6, AP7_4_6 (bloqueo); DOMINIO',
  'Unidad persona, no caso; sin agravio ni respuesta alternativa (autodefensa) en el mismo registro',
  'EXISTE-SATISFACE-PARCIAL(forma de respuesta «protesta» por entorno urbano/rural; falta agravio y unidad caso)', R_SIN,
  'EN-CORPUS (microdato)', 'CALC-CAJA (protesta por DOMINIO, rotulado persona, no caso)', L=('D', 21))
R('M15', 'LAPOP AmericasBarometer México', '2018/19', 'persona 18+', 'abmex18_v12_0_2_5_spa_190207_w', 'ABMex18-v12.0.2.5-Spa-190207_W.pdf', 'cuestionario p3 (PROT3); ausente en 2021 y 2023', None, 'PROT3',
  'Persona; sin agravio', 'EXISTE-SATISFACE-PARCIAL(protesta por persona; falta agravio y caso)', R_SIN, 'EN-CORPUS (microdato)', 'NADA (ya usado en 2019 por MAESTRA38-CARGA-LAPOP: se cita)',
  cita='forense/notas/2026-09-07-MAESTRA38-CARGA-LAPOP-resultados.md', L=('B', 42))
for ola, lx, res in [('2025', 44, R_ABIERTA_MO), ('2026', 45, R_ENVIPE26)]:
    R('M16', 'ENVIPE', ola, 'hogar; con tamaño de localidad', f'envipe{ola}_cuest_principal_pdf', f'cuest_principal_envipe{ola}.pdf',
      'Secc. 4 p5–7 (4.11)', None, 'AP4_11_05 (vigilancia privada); AP4_11_06 (acciones conjuntas con vecinos); AP4_11_09 (armas de fuego)',
      'Respuesta del hogar ante inseguridad, no autodefensa organizada ni agravio; unidad hogar, no caso',
      'EXISTE-SATISFACE-PARCIAL(respuesta colectiva o armada del hogar por entorno; falta agravio y autodefensa organizada)', res,
      'EN-CORPUS (microdato)', 'CALC-CAJA (acciones conjuntas y armas por tamaño de localidad)' if ola == '2025' else 'NADA (ola reservada)', L=('B', lx))
R('M16', 'LAPOP AmericasBarometer México', '2023', 'persona 18+', 'lapop_abmex2023_cuestionario_mexico', 'lapop_abmex2023_cuestionario.pdf', 'cuestionario p10–11 (SEGUR3M); ausente en 2018/19 y 2021', None, 'SEGUR3M (opción 7 «Autodefensas»)',
  'Intención de acudir a autodefensas, no respuesta colectiva observada', 'EXISTE-SATISFACE-PARCIAL(autodefensa como destino de ayuda, por persona; falta agravio y caso)', R_LAPOP23,
  'EN-CORPUS — no abierto', 'NADA (ola reservada)', L=('B', 48))
R('M16', 'ENCUCI', '2020', 'persona', 'encuci2020_fd_pdf', 'FD_ENCUCI2020.pdf', 'FD completo; «propia mano»=0, autodefensa=0, linchamiento=0 (lote D)', 'NO-ENCONTRADO', '—',
  'Autodefensa o justicia por propia mano', 'NO-ENCONTRADO(FD ENCUCI 2020 completo)', R_SIN, '—', 'NADA', proc='—')

# ───────────────────────── M17 · M18 ─────────────────────────
R('M17', 'ENCUCI', '2020', 'persona 15+ (urbano y rural)', 'encuci2020_fd_pdf;encuci2020_bd_dbf', 'FD_ENCUCI2020.pdf', 'Secc. VI p35–40 (6.2, 6.3), Secc. VII p41 (7.1, 7.2)', None,
  'AP6_2_12; AP6_3_12; AP7_1; AP7_2_3',
  'Sin aporte cuantificado (dinero/trabajo), sin monitoreo ni sanción por no participar, sin ≥2 años (transversal), sin distinguir tequio (0 aciertos faena/tequio/multa)',
  'EXISTE-SATISFACE-PARCIAL(participación en organización vecinal y trabajo comunitario; faltan monitoreo/sanción y persistencia)', R_SIN,
  'EN-CORPUS (microdato)', 'CALC-CAJA (participación vecinal por DOMINIO, descriptivo; no falsa R8.1)', L=('D', 15))
R('M18', 'ENSAFI', '2023', 'persona 18+', 'ensafi2023_cuestionario_pdf;ensafi2023_fd_xlsx_zip', 'ensafi_2023_cuestionario.pdf; ensafi_2023_fd.xlsx', 'Secc. 6 p15 (6.1), Secc. 4 p8 (4.6); desconocid/incumpl/ciclo/«no pag»/perdio/estafa: 0 aciertos', None,
  'P6_1_5; P4_6_3', 'No pregunta con quién se hace la tanda ni incumplimiento ni ciclos',
  'EXISTE-NO-SATISFACE(solo prevalencia de tanda; el falsador pide tandas entre desconocidos con incumplimiento)', R_SIN + ' · ENSAFI EXPUESTA (F5 E05)',
  'EN-CORPUS (microdato)', 'NADA', L=('D', 0))
for ola, idm, tb in [('2002', 'ennvih1_2002_hogar_dta', 'ehh02dta_b3b/iiib_cr.dta'), ('2005', 'ennvih2_2005_hogar_dta', 'ehh05dta_b3b/iiib_cr.dta'), ('2009', 'ennvih3_2009_hogar_dta', 'ehh09dta_b3b/iiib_cr.dta')]:
    R('M18', 'ENNViH (MxFLS)', ola, 'persona (panel)', idm, f'ennvih zip, tabla {tb} (etiquetas por índice de reactivos)', 'índice de reactivos: cr04, cr05*' + ('; cr05a_21..23 duración' if ola == '2009' else ''),
      None, 'cr04; cr05a_*; cr05b_*; cr05c_*' + ('; cr05a_21..23' if ola == '2009' else ''),
      'Participación y montos (y duración en 2009); sin con quién ni incumplimiento; panel permite ver repetición entre olas, no ciclos auditados',
      'EXISTE-NO-SATISFACE(sin desconocidos ni incumplimiento)', R_SIN, 'EN-CORPUS (microdato)', 'NADA', origen='PROPUESTO-POR-EJECUTOR',
      T=('ULT 12MES PARTICIPADO EN TANDA?' if ola == '2009' else 'PARTICIPADO TANDA', f'indice:ennvih{ola}:cr04'))

# ───────────────────────── M19 ─────────────────────────
R('M19', 'ENCUCI', '2020', 'persona 15+ (urbano y rural)', 'encuci2020_fd_pdf;encuci2020_bd_dbf', 'FD_ENCUCI2020.pdf', 'Secc. V p24–27 (5.1, 5.2, 5.3)', None,
  'AP5_1_1 (la mayoría de las personas); AP5_1_2 (personas que conoce); AP5_1_3 (personas que viven en su colonia); AP5_1_4 (servidores públicos); AP5_3_3 (policía)',
  'Confiar ≠ transar; el enforcement tendría que venir de otra fuente por entidad (ENVIPE AP5_4) o de AP5_3_3; conf.06 abierto: las cifras de confianza de ENCUCI 2020 en circulación discrepan y hay que reconciliarlas antes',
  'EXISTE-SATISFACE-PARCIAL(confianza con puente frente a sin puente en el mismo respondente; falta disposición a transar y enforcement exógeno)', R_SIN,
  'EN-CORPUS (microdato)', 'CALC-CAJA (diferencia AP5_1_2 − AP5_1_1 por confianza en policía o entidad; tras reconciliar conf.06)',
  origen='PEDIDO-ENCARGO', T=('5.1 En una escala de cero a diez, como en la escuela, donde cero es nada y diez es completamente, en general ¿cuánto confía', 'encuci2020_fd_pdf'))
for ola, lx, idm, res in [('2018/19', 52, 'abmex18_v12_0_2_5_spa_190207_w', R_SIN), ('2021', 53, 'abmex2021_mexico_questionnaire_v17_2_5_2_spa_210420_w', R_SIN), ('2023', 54, 'lapop_abmex2023_cuestionario_mexico', R_LAPOP23)]:
    R('M19', 'LAPOP AmericasBarometer México', ola, 'persona 18+', idm, idm, lot['B'][lx]['seccion_o_pagina'], None, 'IT1',
      'Confianza en la gente de la comunidad: no separa desconocido de conocido', 'EXISTE-NO-SATISFACE(no distingue puente)', res,
      'EN-CORPUS (microdato)', 'NADA', L=('B', lx))
R('M19', 'ENVIPE', '2025', 'persona 18+; por entidad', 'envipe2025_cuest_principal_pdf', 'cuest_principal_envipe2025.pdf', 'Secc. 5 p6–7 (5.4)', None, 'AP5_4_*',
  'Es contexto de enforcement (confianza en autoridades por entidad), no confianza interpersonal', 'EXISTE-SATISFACE-PARCIAL(eje de enforcement por entidad; falta confianza en desconocidos — se une con ENCUCI por entidad)', R_ABIERTA_MO,
  'EN-CORPUS (microdato)', 'CALC-CAJA (confianza en autoridades por entidad como covariable de contexto)', L=('B', 55))
R('M19', 'ENCIG', '2023', 'persona 18+, localidades de 100 mil y más', 'encig23_cuestionario_pdf', 'encig23_cuestionario.pdf', 'Secc. XI (11.1)', None, 'P11_1_11',
  'Confianza en vecinos (con puente); no desconocidos', 'EXISTE-NO-SATISFACE(no mide confianza sin puente)', 'ABIERTA (no es la ola más reciente)', 'EN-CORPUS (microdato)', 'NADA',
  origen='PROPUESTO-POR-EJECUTOR', L=('B', 57))
R('M19', 'WVS ola 7 México', '2018', 'persona adulta', 'f00013146_wvs_wave_7_mexico_csv_v5_1', 'forense/hitoD-R8_3-abridor-v1_0.md',
  'cita: momentos-09-22.tsv fila M19 (abridor GEN1)', 'SIN-TEXTO (cita de dictamen previo)', '—', 'GEN1 sin CALC ni sello; proxy transar≠confiar',
  'EXISTE-NO-SATISFACE(resultado GEN1; camino = CALC GEN2 de reproducción; dictamen de OBTENCION-PREVIA-1 P2, se cita)', R_SIN, 'EN-CORPUS (microdato)', 'CALC-CAJA (reproducción GEN2 del abridor)',
  origen='CITA-OBTENCION-PREVIA-1', cita='momentos-09-22.tsv fila M19')

# ───────────────────────── M22 ─────────────────────────
for ola, lx, res in [('2025', 60, R_ABIERTA_MO), ('2026', 61, R_ENVIPE26)]:
    R('M22', 'ENVIPE', ola, 'delito (persona víctima); por entidad (CVE_ENT 01–32)', f'envipe{ola}_cuest_modulo_pdf;envipe{ola}_fd_pdf', f'cuest_modulo_envipe{ola}.pdf; fd_envipe{ola}.pdf',
      'módulo de victimización 1.23; FD p73 (2025) / p75 (2026)', None, 'BP1_23 (01 miedo al agresor; 02 miedo a extorsión; 06 desconfianza en la autoridad)',
      'Sin medición de protección efectiva a testigos ni pre/post; unidad delito; dato secundario agregable por entidad (cumple la restricción ética de R10.3)',
      'EXISTE-SATISFACE-PARCIAL(no denuncia por miedo por entidad; falta el tratamiento «protección efectiva» y su fecha)', res,
      'EN-CORPUS (microdato)', ('CALC-CAJA (serie por entidad de no denuncia por miedo, unidad delito) · OBTENER(calendario de programas de protección a testigos por entidad — OBTENCION-EXTERNA-1)' if ola == '2025' else 'NADA (ola reservada)'),
      L=('B', lx))
R('M22', 'ENVE (módulo de delitos)', '2024', 'delito contra el establecimiento', f'modulo_delitos_enve2024;{DDI1058}', 'modulo_delitos_enve2024.pdf; DDI TMod_Vic', 'módulo I p3 (1.19)', None, 'M1_19',
  'Unidad establecimiento; sin protección ni pre/post; desagregación por entidad no verificada en el módulo', 'EXISTE-SATISFACE-PARCIAL(no denuncia por miedo, empresa)', R_ENVE24,
  'documentación EN-CORPUS; microdato SIN-FETCH (RNM 1058)', 'NADA (unidad distinta de R10.3; contraste)', origen='PROPUESTO-POR-EJECUTOR', L=('A', 26))
R('M22', 'ENCRIGE', '2020', 'empresa', f'encrige2020_cuestionario;{DDI691}', 'encrige2020_cuestionario.pdf; DDI TR_ENCRIGE2020', 'Secc. X p23 (10.8)', None, 'P10_8 (opción «Por miedo a represalias, incluso jurídicas»)',
  'Motivo de no denunciar corrupción (no delito); unidad empresa', 'EXISTE-SATISFACE-PARCIAL(no denuncia por miedo a represalias, empresa)', R_ENCRIGE20,
  'documentación EN-CORPUS; microdato NO-DISTRIBUIDO-EN-RNM', 'NADA (contraste)', origen='PROPUESTO-POR-EJECUTOR', L=('A', 19))

# ───────────────────────── M23 ─────────────────────────
R('M23', 'ENIF', '2024', 'persona 18+ elegida', 'enif2024_fd_xlsx', 'data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002',
  'cita: P1-A1-M05-M23.tsv fila M23', 'SIN-TEXTO (cita de dictamen previo)', 'secciones 5 y 9 (ahorro)', 'holdout consumido: sirve para describir, no para ajustar',
  'EXISTE-SATISFACE(dictamen de OBTENCION-PREVIA-1 P1, se cita)', 'reserva de evaluación consumida (RETROSPECTIVA)', 'EN-CORPUS (microdato)', 'NADA (relevo descriptivo ya propuesto por P1)',
  origen='CITA-OBTENCION-PREVIA-1', cita='P1-A1-M05-M23.tsv')
R('M23', 'ENSAFI', '2023', 'persona 18+ (TMODULO, FAC_ELE)', 'ensafi2023_cuestionario_pdf;ensafi2023_fd_xlsx_zip', 'ensafi_2023_cuestionario.pdf; ensafi_2023_fd.xlsx',
  'Secc. 6 p15 (6.1, 6.2, 6.3); FD p49 (FAC_ELE, UPM_DIS, EST_DIS)', None, 'P6_1_1, P6_1_3, P6_1_4, P6_1_5, P6_1_6 (informal); P6_2_04, P6_3 (formal); FAC_ELE; UPM_DIS; EST_DIS',
  'Otra encuesta y otra ola que ENIF 2024; definición de «solo informal» a construir (informal ∧ ¬formal); sirve de contraste de definición, no de relevo',
  'EXISTE-SATISFACE(ahorro solo informal construible por persona con diseño; como contraste)', R_SIN + ' · ENSAFI EXPUESTA (F5 E05)',
  'EN-CORPUS (microdato)', 'CALC-CAJA (contraste de definición frente a ENIF 2024, RETROSPECTIVA)', L=('D', 4))

buf = io.StringIO()
w = csv.DictWriter(buf, fieldnames=COLS, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='\\')
w.writeheader()
for r in rows:
    w.writerow({k: str(v).replace('\t', ' ').replace('\n', ' ') for k, v in r.items()})
if '--verifica' in sys.argv:
    igual = open(OUT, newline='').read() == buf.getvalue()
    print(f'{len(rows)} filas · {"IDENTICO" if igual else "DIFIERE"} a {os.path.relpath(OUT)}')
    sys.exit(0 if igual else 1)
open(OUT, 'w', newline='').write(buf.getvalue())
print(len(rows), 'filas ->', os.path.relpath(OUT))
