"""Arma la hoja consolidada de firmas y su tabla máquina · ACTO GEN2-TRAMITE-HOJA-FIRMAS-21-1.

Fuente única: la lista RENGLONES de abajo. Escribe `decisiones-21.tsv` y
`hoja-para-mesa-firmas-21.md` en este directorio. `--verifica` corre los
criterios de «hecho» del encargo contra forense/firmas-pendientes.tsv y
data/manifiesto.yaml (lector CSV/YAML, nunca por línea física) y no escribe.
No firma, no asienta, no edita ninguna FP ni NC.
"""
import csv
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
P = "FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-"
AD = "FIRMADA-EN-CHAT (ADENDA-1 de este acto, mesa 28/sep: «firmado»)"
AD2 = "forense/encargos/2026-09-27-GEN2-RECIBO-ASTRA6-2-ADENDA-1.md"
NCD = "forense/analisis/nc-decisiones/hoja-2026-09-27.md"
MAPA = "forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md"
R2 = "forense/analisis/recibo-astra6-2/hoja-para-mesa-recibo-astra6-2.md"
R3 = "forense/analisis/recibo-astra6-3/hoja-para-mesa-recibo-astra6-3.md"
C1 = "forense/analisis/astra-continuidad-c1/hoja-mesa-c1-v1_0.md"
C2 = "forense/analisis/familias-2027/hoja-c2-para-mesa-v1_0.md"
C3 = "forense/analisis/reports-v2/continuidad-c3-1/hoja-para-mesa.md"
PE2 = "forense/analisis/pendientes-2/hoja-firmas-2026-09-28.md"
OE1 = "forense/analisis/obtencion-externa-1/solicitudes/"
OP1 = "OBTENCION-PREVIA-1 + MAPA-INSTRUMENTOS-ALTERNOS-1 (#1255) + OBTENCION-EXTERNA-1 (#1259)"
TRES = ["(1) firmar la fila tal cual la redactó el ejecutor", "(2) firmar con el cambio que propone el recibo", "(3) no firmar: la pieza queda parada"]

TIPOS = ["APERTURA-DE-DATO", "ADOPCION-VETO", "CONTRATO-PROCEDIMIENTO", "ACCION-CON-IDENTIDAD", "FORMA"]
TITULO_TIPO = {
    "APERTURA-DE-DATO": "Apertura de dato (reservas, HOLDOUT, lecturas de olas)",
    "ADOPCION-VETO": "Adopción o veto (recibir sin adoptar, contratos de medición)",
    "CONTRATO-PROCEDIMIENTO": "Contrato y procedimiento (tubería, catálogo, CALC)",
    "ACCION-CON-IDENTIDAD": "Acciones de mesa con identidad (solicitudes, registros, disco, cuentas)",
    "FORMA": "Forma (idioma, cifras editoriales, textos de trámite)",
}


def R(ids, objeto, tipo, fuente, situacion, pide, opciones, rec, req, hecha, texto, estado="PIDE-FIRMA"):
    return dict(ids=ids, objeto=objeto, tipo=tipo, fuente=fuente, situacion=situacion, pide=pide,
                opciones=opciones, rec=rec, req=req, hecha=hecha, texto=texto, estado=estado)


def firmada(letra, fp, objeto, tipo, opcion, texto_op, ejecutor):
    return R([P + fp], objeto, tipo, f"{NCD} §{letra}", f"Letra {letra} de NC-DECISIONES-1; firmada en chat el 28/sep.",
             "Nada: ya firmada. Se lista para que TRAMITE-FIRMAS-21 (o el acto ejecutor) la asiente.",
             [f"{letra} {opcion} (firmada)", "las demás opciones de la hoja NC-DECISIONES-1 (descartadas por la firma)"],
             f"de NC-DECISIONES-1: {opcion}", "NO", "no aplica",
             f"«firmado» (mesa, 28/sep/2026, maestra 54) sobre «{letra} {opcion}»: {texto_op}. Asienta: {ejecutor}.", AD)


RENGLONES = [
    # ---------------- P2 · decisiones nuevas al frente ----------------
    R(["(sin FP) HOLDOUT M09–M23"], "rol_calibracion=HOLDOUT de M09–M23 en milpa/catalogo-momentos-v0_1.tsv", "APERTURA-DE-DATO",
      f"{MAPA} §«Antes de firmar» aviso 1",
      "15 momentos (M09–M23) guardan su valor como prueba del modelo, no para ajustarlo. M23 ya se consumió (ENIF 2024, RESULT sellado). Cualquier CALC sobre M09–M22 gasta su papel de prueba, y A1/A2 proponen CALC que lo harían. [EJECUTADO] el expediente C2 (forense/analisis/familias-2027*, 181 archivos) no cita ningún M09–M23 ni «HOLDOUT»: hoy ninguna familia 2027 los usa como R.",
      "Una decisión, una vez, para todo el bloque: qué se hace con el papel de prueba de estos momentos.",
      ["(a) gastar todos ahora como pisos descriptivos RETROSPECTIVOS. Gana: cobertura del catálogo. Cuesta: se pierde la prueba de los 14 para siempre (E.6: un cruce visto no se relanza)",
       "(b) gastar solo los que ninguna familia 2027 vaya a usar como R. Hoy son los 14 (expediente C2: 0 menciones en 181 archivos), así que equivale a (a) salvo que C2 reclame alguno antes. Cuesta: igual que (a) en el estado actual; protege solo lo que C2 reclame",
       "(c) no gastar ninguno y medir con instrumentos que no son el momento («combinable» del mapa). Gana: la prueba sigue intacta. Cuesta: las respuestas quedan acotadas o indirectas",
       "(d) convertir cada momento en familia 2027 con emisión sellada antes de la ola. Gana: la prueba se vuelve PROSPECTIVA. Cuesta: un expediente por momento y esperar a 2027"],
      "ninguna del acto (el encargo la reserva a dirección). Nota de ejecutor: A1 (b) y A2 (b) del mapa presuponen (a) o (b) para M05, M13, M19, M22 y M23",
      "SI", f"hecha: {MAPA} (64 pares) y OBTENCION-PREVIA-1",
      "«Sobre el papel HOLDOUT de M09–M23 firmo la opción (__). Toda spec que consuma un HOLDOUT lo declara en su COMMIT-1; lo consumido se rotula RETROSPECTIVA y no vuelve a servir como prueba.»"),
]

OLAS = [
    ("ENCRIGE 2020", "conjunto_de_datos_encrige_2020_csv, encrige2020_cuestionario, gen2_encrige2020_diseno_muestral, obtencion_previa_1_d1_programas_encrige_2020, encrige2020_rnm691_ddi", "R03 (I1) y R08; sus tabulados ya los usó #826", "La ola 2016 la preserva F5 R08; la 2020 es la más reciente y ya se vio en tabulados."),
    ("ENVE 2024", "conjunto_de_datos_enve_2024_csv, cuestionario_principal_enve2024, modulo_delitos_enve2024, enve2024_rnm1058_ddi, oe1_enve_2024_rnm_1058_catalogo_html", "R03 (apoyo) y M22", "Es la más reciente (2020 y 2022 no están en el corpus); F5 la declara EXPUESTA."),
    ("CSES Módulo 5", "cses5_modulo5_2016_2021_csv, cses5_modulo5_2016_2021_codebook, cses5_modulo5_2016_2021_cuestionario", "M13 y M14", "Es el módulo más reciente del corpus."),
    ("ENDUTIH 2025", "endutih_2025_endutih2025_bd_dbf, endutih_2025_fd_endutih2025", "M12 (y contratos de tolerancia de fb50-04)", "Es la más reciente; el recibo -2 la da como «sigue reservada» en fb50-04."),
    ("ENIF 2024 módulo 7 (pagos)", "enif2024_csv, enif2024_fd_xlsx, enif2024_cuestionario_pdf, enif_2024_enif_2024_bd_csv, enif_2024_enif_2024_modelo_logico_pdf, enif2024_diseno_muestral_pdf", "M12; M23 ya consumió ENIF 2024 en otro módulo", "Hay reservas por módulo vigentes sobre ENIF 2024; el m7 no trae campo propio."),
]
for ola, ids_m, calc, porque in OLAS:
    n = len(ids_m.split(", "))
    RENGLONES.append(R(
        [f"(sin FP) RESERVA {ola}"], f"estado de reserva de la ola {ola} (manifiesto)", "APERTURA-DE-DATO", f"{MAPA} §«Antes de firmar» aviso 2",
        f"[EJECUTADO, lector YAML] {n} entradas del manifiesto ({ids_m}): ninguna trae el campo estado_reserva. {porque} Por la letra de E.6 podría estar reservada; mientras mesa no decida, el mapa la trata como no abierta.",
        f"Fijar por escrito el estado de {ola}. La necesitan: {calc}.",
        ["RESERVADA: solo la abre el código congelado de una prueba pre-registrada. Cuesta: los CALC descriptivos que la usan esperan a un pre-registro",
         "ABIERTA-COMO-VISTA: mesa por escrito; sirve para describir y calibrar, nunca como R. Cuesta: la ola ya no puede ser prueba prospectiva",
         "ABIERTA-PARCIAL: solo columnas nombradas (como las seis AMAI de ENIGH 2024). Cuesta: una lista de columnas por firmar y un guardia por columna"],
        "ninguna del acto (el encargo la reserva a dirección)", "SI", f"hecha: manifiesto leído por id en este acto ({n} ids, 0 con campo); {MAPA}",
        f"«La ola {ola} queda ________ (RESERVADA · ABIERTA-COMO-VISTA · ABIERTA-PARCIAL: columnas ____). El acto que la use registra el estado en el campo estado_reserva del manifiesto, citando esta firma.»"))

RENGLONES += [
    # ---------------- apertura de dato ----------------
    R([P + "01"], "catálogo de momentos: M05 (evadir normas) y M23 (ahorro solo informal)", "APERTURA-DE-DATO", f"{NCD} §A1 + {MAPA} §A1",
      "La recomendación vieja (HISTÓRICO-SIN-RELEVO) ya no se sostiene: M05 tiene respuesta de actitud en LAPOP 2021 (EXC18 × PR3DNR) y M23 tiene RESULT sellado de ENIF 2024 más ENSAFI 2023 como contraste.",
      "Elegir cómo se responden M05 y M23.",
      ["(a) HISTÓRICO-SIN-RELEVO para las dos. Cuesta: dos preguntas quedan sin respuesta aunque el corpus la tiene",
       "(b) M05 acotada a actitud con CALC-caja LAPOP 2021; M23 relevo descriptivo con el RESULT de ENIF 2024 (RETROSPECTIVA) y ENSAFI 2023 de contraste. Cuesta: dos CALC de caja; consume HOLDOUT de M23 (ya consumido)",
       "(c) M05 en unidad persona con ENVIPE 2025. Cuesta: mide victimización, no la norma; otra unidad"],
      "del mapa: (b)", "SI", f"hecha: {OP1}",
      "«Firmo A1 (b): M05 se acota a actitud y se encarga CALC-caja sobre LAPOP 2021 (EXC18 × PR3DNR × escolaridad); M23 recibe relevo descriptivo con el RESULT sellado de ENIF 2024, rotulado RETROSPECTIVA, y ENSAFI 2023 como contraste. Ambas specs declaran que consumen HOLDOUT.»"),
    R([P + "02"], "catálogo de momentos: M09–M22 (catorce incógnitas del motor)", "APERTURA-DE-DATO", f"{NCD} §A2 + {MAPA} §A2",
      "8 de 14 tienen vía parcial en el corpus (ENCUCI, CSES, CIDE-CSES, ENIGH, ENVIPE, ENSAFI, ENCIG, ENIF, ENDUTIH, LAPOP). La recomendación vieja (13 de 14 a estudio nuevo) ya no se sostiene.",
      "Elegir cuántos CALC descriptivos se encargan. Depende del renglón HOLDOUT.",
      ["(a) CALC descriptivo de caja para los 8 con vía parcial. Cuesta: gasta 8 HOLDOUT",
       "(b) CALC solo para M13 (CIDE-CSES 2015), M22 (ENVIPE 2025) y M19 (ENCUCI 2020, tras conf.06); los otros cinco quedan documentados sin fecha. Cuesta: gasta 3 HOLDOUT",
       "(c) 13 de 14 a estudio nuevo (recomendación vieja). Cuesta: ignora vías ya verificadas"],
      "del mapa: (b)", "SI", f"hecha: {OP1}",
      "«Firmo A2 (b): se encargan CALC-caja descriptivos para M13 (CIDE-CSES 2015 con clasificador de concurrencia del calendario INE), M22 (ENVIPE 2025, no denuncia por miedo por entidad) y M19 (ENCUCI 2020, tras reconciliar conf.06). Cada spec declara que consume el HOLDOUT de su momento. M12, M14, M15, M16 y M17 quedan con su vía documentada en el mapa, sin fecha.»"),
    R([P + "10"], "reserva de las olas únicas de CAAS 2015, ENG 2009, ENCRIGE 2016 y MIGRACIÓN 2002", "APERTURA-DE-DATO", f"{NCD} §D1 + {MAPA} §D1",
      "E.6 las reservó como «ola nueva». El mapa verificó que ENCRIGE no está descontinuada (RNM lista 2016 y 2020) y que F5 R08 preserva 2016 a propósito. Las otras tres no se revisaron.",
      "Decidir la reserva de las cuatro; ENCRIGE 2020 se decide en su renglón propio.",
      ["(a) levantar por escrito la reserva de CAAS, ENG y MIGRACIÓN; mantener la preservación de ENCRIGE 2016 (F5 R08). Cuesta: ninguno detectado",
       "(b) levantar las cuatro, ENCRIGE 2016 incluida. Cuesta: rompe el plan confirmatorio de R08",
       "(c) mantenerlas hasta verificar caso por caso que no hay sucesora. Cuesta: tres fuentes inútiles mientras tanto"],
      "de NC-DECISIONES-1 (a) para las cuatro; del mapa (a) para ENCRIGE. PROPUESTO-POR-EJECUTOR: la opción (a) de este renglón junta las dos", "SI", f"hecha: {OP1}",
      "«Firmo D1: se levanta por escrito la reserva E.6 de CAAS 2015, ENG 2009 y MIGRACIÓN 2002; ENCRIGE 2016 conserva la preservación de F5 R08. ENCRIGE 2020 sigue lo firmado en su renglón.»"),
    R([P + "29", "(sin FP) solicitud (g) OBTENCION-EXTERNA-1"], "R03 (carga regulatoria y mordida en la MIPYME) y el microdato ENAPROCE", "APERTURA-DE-DATO", f"{NCD} §I1 + {MAPA} §I1 + {OE1}g-inegi-lm-enaproce.md",
      "ENAPROCE solo se consigue en el Laboratorio de INEGI con titular acreditado. La mordida en la empresa sí se mide en el corpus: ENCRIGE 2020, ENVE 2024 y WBES 2023. F-19 ya decidió que una encuesta de empresas no se traslada a personas. La solicitud (g) quedó ARCHIVADA-NO-NECESARIA.",
      "Decidir si se tramita ENAPROCE o se funde R03 con R08.",
      ["(a) designar titular para el Laboratorio por ENAPROCE. Cuesta: trámite de identidad por un dataset marginal",
       "(b) cerrar ENAPROCE como NO-ACCESIBLE. Cuesta: R03 queda sin fuente",
       "(d) (b) más fundir R03 con R08 como familia descriptiva sobre ENCRIGE 2020, con ENVE 2024 y WBES 2023 de apoyo. Cuesta: depende del estado de ENCRIGE 2020 y ENVE 2024"],
      "del mapa: (d)", "SI", f"hecha: {OP1}",
      "«Firmo I1 (d): ENAPROCE queda NO-ACCESIBLE para R03; R03 se funde con R08 como familia descriptiva UNIDAD-DISTINTA-NO-TRANSFERENCIA sobre ENCRIGE 2020 (ENVE 2024 y WBES 2023 de apoyo), según propuesta-R03.md. La solicitud de microdato ENCRIGE 2020 al Laboratorio es opcional y la decide mesa aparte.»"),
    R(["FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-01"], "lectura ciega nueva de ENDIREH 2021 (C1)", "APERTURA-DE-DATO", f"{AD2}; {R2}",
      "Firmada el 27/sep (ADENDA-1 de RECIBO-ASTRA6-2) y todavía ABIERTA en el TSV.", "Nada.", TRES, "del recibo -2: (2)", "NO", "no aplica",
      "Ya firmada: ADENDA-1 de RECIBO-ASTRA6-2, «FIRMADA, delimitada». La asienta TRAMITE-FIRMAS-21.", f"YA-CUBIERTA-POR {AD2}"),
    R(["FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-02"], "lectura ciega nueva de ENDIREH 2016 (C1)", "APERTURA-DE-DATO", f"{AD2}; {R2}",
      "Firmada el 27/sep y todavía ABIERTA en el TSV.", "Nada.", TRES, "del recibo -2: (2)", "NO", "no aplica",
      "Ya firmada: ADENDA-1 de RECIBO-ASTRA6-2, «FIRMADA, delimitada». La asienta TRAMITE-FIRMAS-21.", f"YA-CUBIERTA-POR {AD2}"),
    R(["FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-02"], "exposición documental a ENADID 2023 (pieza vejez)", "APERTURA-DE-DATO", f"{AD2}; {C3} §b",
      "Firmada el 27/sep (excluir la fuente, mantener la reserva) y todavía ABIERTA en el TSV.", "Nada.", TRES, "del recibo -2: (1)", "NO", "no aplica",
      "Ya firmada: ADENDA-1 de RECIBO-ASTRA6-2. La asienta TRAMITE-FIRMAS-21.", f"YA-CUBIERTA-POR {AD2}"),
    R(["FP-260927-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1-b544-02"], "exposición documental a EDER2025, ENADID2023, ENCODAT2025 y publicaciones ENUT2024/ENIF2024/ENSU-dic2025 (#1242)", "APERTURA-DE-DATO", f"{R3}; {C2} (ba6c-01 c)",
      "El ejecutor declaró la exposición y la sacó del producto. E.6: un cruce visto se declara consumido. C2 pide que «consumido» se diga por cruce enumerado, no por ola (parte c de ba6c-01, contestada aquí).",
      "Adjudicar la exposición.",
      ["(1) firmar la fila tal cual (solo niega permiso retroactivo). Cuesta: no declara consumido lo visto", "(2) firmar con el cambio del recibo -3: consumido por cruce, solo retrospectiva", "(3) no firmar: el producto saneado no se recibe"],
      "del recibo -3: (2)", "NO", "no aplica",
      "«Recibo el producto saneado del PR #1242 y adjudico la exposición documental a EDER2025, ENADID2023, ENCODAT2025 y a las publicaciones ENUT2024/ENIF2024/ENSU-dic2025: lo visto queda excluido del producto, se declara consumido para esos cruces (E.6), enumerados uno por uno, y solo sirve en retrospectiva, rotulado así; no se autoriza ninguna lectura retroactiva ni futura de esas olas fuera del código congelado de una prueba pre-registrada.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C2-1-ba6c-01"], "universo del tablero C2 (MOCIBA, ENSANUT) y estado de ENSU dic/2025", "APERTURA-DE-DATO", C2,
      "C2 pregunta (a) si MOCIBA y ENSANUT entran al tablero, (b) si ENSU dic/2025 es ola abierta (oro de frontera-1) o reservada (incidente #1242), y (c) cómo se dice «consumido». La (c) se contesta en el renglón de b544-02.",
      "Contestar (a) y (b).",
      ["(a1) MOCIBA y ENSANUT entran al tablero C2 · (a2) quedan fuera hasta tener oro comparable (71cf-01 las difiere)",
       "(b1) ENSU dic/2025 ABIERTA-COMO-VISTA: sirve de oro de frontera-1, nunca como R · (b2) RESERVADA por el incidente #1242: frontera-1 pierde ese oro"],
      "PROPUESTO-POR-EJECUTOR: (a2) por coherencia con 71cf-01 ya firmada; (b1), porque la exposición de #1242 ya la consumió en retrospectiva (b544-02)", "NO", "no aplica",
      "«Hoja C2: (a) MOCIBA y ENSANUT ____ (entran / quedan fuera hasta oro comparable) al tablero C2; (b) ENSU dic/2025 queda ____ (ABIERTA-COMO-VISTA, nunca R / RESERVADA).»"),
    R(["FP-260926-GEN2-ASTRA6-C1-PAQUETES-2-9c9e-01"], "permisos parciales ENIF/ENUT/ENSANUT 2024 y tolerancias nuevas de C1", "APERTURA-DE-DATO", C2,
      "La fila junta permisos de lectura y tolerancias. C2 la lista por referencia: recomienda firmar solo como recepción.", "Decidir si se recibe.",
      ["(1) recibir la preparación; los permisos se firman después, uno por uno. Cuesta: un trámite por permiso", "(2) firmar los permisos en bloque. Cuesta: abre dato sin texto concreto por ola", "(3) no firmar"],
      "de la hoja C2: (1)", "NO", "no aplica",
      "«Recibo la preparación y sus impedimentos con el corte y hashes entregados; autorizaciones ENIF/ENUT y tolerancias nuevas sólo se adoptan mediante firmas separadas sobre sus textos concretos. No adopto resultados ni levanto otras reservas; la comparación se realiza después de sellar las reconstrucciones de sesiones nuevas.»"),
    R(["FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-03"], "inventario custodial de los ZIP de C1 y su proyección por fuente", "APERTURA-DE-DATO", R2,
      "Dos etapas: inventario de miembros (A.7: envoltura, no dato) y proyección por fuente/columna (sí abre). ENUT conserva su cruce reservado (FP-bda6-02).", "Autorizar la etapa 1 sola o las dos.",
      TRES, "del recibo -2: (2)", "NO", "no aplica",
      "«Autorizo únicamente la etapa 1 (inventario de miembros —nombre, CRC, tamaño— de los ZIP, A.7), con custodio distinto del analista. La etapa 2 requiere una FP por fuente con miembro, columna, finalidad y hash; ENUT conserva FP-bda6-02 y no se abre su cruce reservado.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-03", "(sin FP) recibo -3 #1241 «conservar la reserva»"], "reserva del lote 3 de C1", "APERTURA-DE-DATO", f"{C1} §d; {R3}",
      "El lote 3 de C1 necesita autorización por paquete. El recibo -3 la dejó sin fila (#1241); C1 la acuñó como 26a2-03.", "Fijar cómo se autoriza el lote 3.",
      ["(1) conservar la reserva y autorizar paquete por paquete con los cuatro gates", "(2) autorizar el lote 3 completo. Cuesta: abre sin gate por paquete", "(3) pausar C1"],
      "de C1 y del recibo -3: (1)", "NO", "no aplica",
      "«La reserva se conserva hasta que haya autorización por paquete y cohorte. El lote 3 de C1 se lanza paquete por paquete, y cada uno solo cuando tenga en SÍ los cuatro gates (APTO-TECNICAMENTE, CONTEXTO-NUEVO-ACREDITADO, CONTRATO-FIRMADO, ACCESO-AUTORIZADO). Esta firma no autoriza ningún paquete concreto.»"),

    # ---------------- adopción / veto ----------------
    R(["FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-01"], "reports C3 de cuidado, migración y pareja", "ADOPCION-VETO", f"{AD2}; {C3} §b",
      "Firmada el 27/sep (recibir sin adoptar) y todavía ABIERTA en el TSV.", "Nada.", TRES, "del recibo -2: (1)", "NO", "no aplica",
      "Ya firmada: ADENDA-1 de RECIBO-ASTRA6-2. La asienta TRAMITE-FIRMAS-21.", f"YA-CUBIERTA-POR {AD2}"),
    R(["FP-260926-ASTRA6-C3-DINERO-TECNOLOGIA-CONOCIMIENTO-1-9df0-01"], "reglas del lote C3 dinero, tecnología y conocimiento", "ADOPCION-VETO", f"{AD2}; {C3} §b",
      "Firmada el 27/sep (recibir sin adoptar) y todavía ABIERTA en el TSV.", "Nada.", TRES, "del recibo -2: (1)", "NO", "no aplica",
      "Ya firmada: ADENDA-1 de RECIBO-ASTRA6-2. La asienta TRAMITE-FIRMAS-21.", f"YA-CUBIERTA-POR {AD2}"),
    R(["FP-260926-GEN2-ASTRA6-C2-FRONTERA-1-71cf-01"], "paquete «frontera» de C2 (ENSU-Campeche, ENOE-informalidad, ENSANUT-CESD, MOCIBA)", "ADOPCION-VETO", f"{AD2}; {C2}",
      "Firmada el 27/sep (recibir sin adoptar). La hoja C2 dice que NO está firmada porque lee solo el TSV: el TSV sigue ABIERTA, la firma está en la ADENDA-1 de RECIBO-ASTRA6-2.", "Nada.", TRES, "del recibo -2 y de C2: (1)", "NO", "no aplica",
      "Ya firmada: ADENDA-1 de RECIBO-ASTRA6-2. La asienta TRAMITE-FIRMAS-21.", f"YA-CUBIERTA-POR {AD2}"),
    R(["FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-03"], "regla de publicabilidad sellada (CV ≤ .30, ancho ≤ .20)", "ADOPCION-VETO", AD2,
      "Firmada el 27/sep (conservar) y todavía ABIERTA en el TSV.", "Nada.", TRES, "del recibo -2: (1)", "NO", "no aplica",
      "Ya firmada: ADENDA-1 de RECIBO-ASTRA6-2. La asienta TRAMITE-FIRMAS-21.", f"YA-CUBIERTA-POR {AD2}"),
    R(["FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-04"], "recibo de Claude del PR #1194", "ADOPCION-VETO", f"{AD2}; {R2}",
      "La ADENDA-1 de RECIBO-ASTRA6-2 la cierra por producto: el recibo existe (ADR-260927-GEN2-RECIBO-ASTRA6-2-627e-01).", "Nada.", TRES, "del recibo -2: cubierta", "NO", "no aplica",
      "Cerrada por producto; no requiere firma. La asienta TRAMITE-FIRMAS-21.", "SUPERADA (ADR-260927-GEN2-RECIBO-ASTRA6-2-627e-01)"),
    R(["FP-260927-ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1-3a1f-01"], "reports C3 de autoridad, civismo y comunalidad (#1240)", "ADOPCION-VETO", R3,
      "Mismo patrón que 9df0-01 (recibir sin adoptar). Autoridad y México Rural no llevan firewall genético y ninguno responde las preguntas [v2.16].", "Recibirlos, con o sin condición editorial.",
      TRES, "del recibo -3: (2)", "NO", "no aplica",
      "«Recibo los tres reports v2 (autoridad, civismo, comunalidad) y sus reglas SI-ENTONCES como propuesta para revisión independiente, sin adopción en motor ni catálogo, condicionado a que una pasada editorial C3 añada firewall genético a Autoridad y México Rural y las preguntas [v2.16] del módulo de auditoría a los tres.»"),
    R(["FP-260927-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1-b544-01"], "diez reglas editoriales de salud, juventud y tiempo (#1242)", "ADOPCION-VETO", R3,
      "Diez reglas como propuesta para un catálogo sucesor, sin adopción (E.2).", "Recibirlas.", TRES, "del recibo -3: (1)", "NO", "no aplica",
      "«Recibo diez reglas editoriales de salud, juventud y tiempo como propuestas para catálogo sucesor; sin adopción en motor.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C3-1-26bb-01", "(sin FP) recibo -3 #1243 «9 reglas PROP-C3»"], "inventario reglas-propuestas-v1_0.tsv (107 reglas C3)", "ADOPCION-VETO", f"{C3} §a; {R3}",
      "107 reglas C3, todas PROPUESTA; 2 citan RESULT. Las 9 PROP-C3 de #1243 que el recibo -3 dejó sin fila entran en este inventario.", "Recibir el inventario.",
      ["(1) recibir sin adoptar ninguna", "(2) adoptar las 2 que citan RESULT. Cuesta: adopción fuera de bloque (E.2)", "(3) no recibir"],
      "de C3: (1)", "NO", "no aplica",
      "«Recibo reglas-propuestas-v1_0.tsv (107 reglas C3) como inventario de propuestas. Ninguna se adopta. Una regla pasa a adopción solo en un bloque de mesa con RESULT sellado y consumidor identificado.»"),
    R(["FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-01"], "contratos sucesores P1 de C1 (ENOE/B parciales, derivados, contrato inferencial árbitros/AMAI)", "ADOPCION-VETO", R2,
      "La parte inferencial depende del protocolo de 157c-01, que no tiene margen de equivalencia.", "Recibir sin adoptar o adoptar en bloque.", TRES, "del recibo -2: (2)", "NO", "no aplica",
      "«Recibo los contratos sucesores propuestos en impedimentos-lote2-hoja-decisiones.md (manifiesto 3d508f7e…1c50) sin adoptarlos. Cada contrato se firmará por identidad, opción y hash en un trámite posterior; el contrato inferencial de árbitros/AMAI espera la resolución de FP-…-157c-01. No cambio contratos ni sellos originales.»"),
    R(["FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02"], "dictámenes ENDIREH 2006/2016 y retiro de quince llaves ENVIPE 2015", "ADOPCION-VETO", R2,
      "Los dictámenes documentales pueden recibirse ya; retirar llaves del catálogo cambia producto y es de CIERRE-SEMANAL-2.", "Recibir dictámenes; decidir el retiro.", TRES, "del recibo -2: (2)", "NO", "no aplica",
      "«Recibo los dictámenes ENDIREH 2006 (separar MD postseparación del anual) y ENDIREH 2016 (bins NIV propios desde FD) como base de contratos sucesores, sin reescribir llaves ni sellos. El retiro de las quince llaves ENVIPE 2015 se propone al circuito de catálogo como PROPONER-SUSPENDER con sucesor por CALC nuevo; no se ejecuta por esta firma.»"),
    R(["FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-04"], "tolerancias por identidad ENDUTIH/MOCIBA", "ADOPCION-VETO", R2,
      "Ocho contratos de tolerancia fijados antes de revelar; ENDUTIH 2025 sigue sin estado de reserva decidido (renglón propio).", "Fijar las tolerancias.", TRES, "del recibo -2: (1)", "NO", "no aplica",
      "«Fijo las tolerancias por identidad ENDUTIH/MOCIBA: proporciones abs 1e-8 rel 0, enteros y estados exactos, pesos expandidos abs 1e-8 / rel 1e-12; el plan de IC va aparte. No abre reserva ni adopta.»"),
    R(["FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01"], "protocolo inferencial de C1 para un nuevo intento", "ADOPCION-VETO", R2,
      "Sin margen de equivalencia ni validación de diseño, solo acredita implementación.", "Aprobarlo como diagnóstico o como estimador.", TRES, "del recibo -2: (2)", "NO", "no aplica",
      "«Apruebo el protocolo como contrato DIAGNÓSTICO de reproducción de IC para intentos futuros; no es estimador de IC adoptable ni recertifica IC históricos. El margen de equivalencia y el control simultáneo se fijarán por mesa antes del siguiente conjunto sin revelar.»"),
    R(["FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-02"], "restauración documental de ventana en 767 identidades de C1", "ADOPCION-VETO", R2,
      "La hoja pide no mezclar el transporte con cambios de estimando; la exclusión de EDAD 98/99 se decide con 39de-01.", "Autorizar el transporte solo o junto con contratos nuevos.", TRES, "del recibo -2: (2)", "NO", "no aplica",
      "«Autorizo el carril de transporte: copiar la ventana literal del catálogo v1.2 a las 767 identidades, sin cambiar método ni el DISCREPA/NO-RECALCULABLE histórico. Los contratos nuevos (NIV-terminal-v1, P14_22_14 leyes, exclusión EDAD 98/99) quedan pendientes de firma por bloque; ninguno se presenta como equivalente del histórico.»"),
    R(["FP-260926-ASTRA6-C1-ADJUDICACION-PUNTOS-1-39de-01"], "retiro temporal de identidades con defecto, denominador institucional y elegibilidad nacional 99 (C1)", "ADOPCION-VETO", f"{R2}; {AD2}",
      "beee-02 ya cubre las seis identidades de instituciones 2011; queda el resto (elegibilidad nacional 99, sucesores).", "Firmar el resto.", TRES, "del recibo -2: (1) en lo no cubierto por beee-02", "NO", "no aplica",
      "«En lo no cubierto por FP-…-beee-02: autorizo el retiro temporal de identidades con defecto documental, el denominador institucional, la elegibilidad nacional 99 y la ejecución de sucesores nuevos, sin adopción automática.»"),
    R(["FP-260927-GEN2-ASTRA6-C1-ENTRADAS-LOTE2-RESIDUALES-1-1653-01"], "contrato ENBIARE de edades/CESD-7 y receta IC sucesora (C1)", "ADOPCION-VETO", R3,
      "La fila junta dos decisiones: el contrato ENBIARE cambia el denominador; la receta IC depende de 157c-01.", "Firmarlas por separado y atadas a hash.", TRES, "del recibo -3: (2)", "NO", "no aplica",
      "«(a) Apruebo para un nuevo intento, con identidades sucesoras, el contrato ENBIARE de edades/CESD-7 identificado por el SHA-256 de p2/specs/enbiare-edades-propuesta.md; EDAD=98 queda fuera de tramos y de CESD-7; reconozco el cambio de denominador. (b) Apruebo la receta IC sucesora identificada por los SHA-256 de p3/entradas/residuales-p3-contrato-ic.md y residuales-p3-modulos-ic.md, solo como reproducibilidad diagnóstica y subordinada al protocolo que resulte de FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01; no certifica cobertura del 95%. Ninguna modifica intentos previos.»"),
    R(["FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01"], "ENOE-informalidad 2027T4 y la regla de varianza de 39 estratos singleton", "ADOPCION-VETO", f"{R3}; {C2}",
      "39 estratos con una sola UPM: NO-LANZAR-TODAVÍA. La fila es vaga; hay que decir que no se adopta la receta sucesora.", "Recibir la hoja y autorizar la solicitud a INEGI.", TRES, "del recibo -3 y de C2: (2)", "NO", "no aplica",
      "«Recibo la hoja forense/analisis/familias-2027-enoe-inferencia-1/enoe-hoja-decision.md: ENOE-INFORMALIDAD 2027T4 queda NO-LANZAR-TODAVIA; autorizo enviar a INEGI la solicitud de regla de varianza para los 39 estratos singleton de ENOE 2024T4. No adopto la receta sucesora, ningún tratamiento alternativo de singleton, cifra de diagnóstico ni COMMIT-3; cualquier regla nueva requiere firma propia antes del dato.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01", "(sin FP) recibo -3 #1241 «CONTRATO-v3»"], "CONTRATO-v3.md de C1 (sha256 821a5ecb…94eb)", "CONTRATO-PROCEDIMIENTO", f"{C1} §b; {R3}",
      "Contrato de estados de C1. El recibo -3 lo dictaminó sin fila; C1 le dio la 26a2-01.", "Firmar el contrato.", TRES, "del recibo -3 y de C1: (2)", "NO", "no aplica",
      "«Mesa firma CONTRATO-v3.md con sha256 821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb como contrato de estados de C1. Esta firma no acredita contexto nuevo ni autoriza acceso: cualquier C1 real exige además CONTEXTO-NUEVO-ACREDITADO y ACCESO-AUTORIZADO por paquete. Una corrección material se hace en una versión sucesora con sello nuevo.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02", "(sin FP) recibo -3 #1241 «provisionar el broker»"], "reconstructor sin historial de C1 (sesión nueva o broker)", "CONTRATO-PROCEDIMIENTO", f"{C1} §a; {R3}",
      "Sin broker no hay separación verificable. Opción A da validación ya con rótulo propio; B espera el broker, que el recibo -3 pide provisionar.", "Elegir A o B.",
      ["(A) sesión nueva de Claude Code sin historial, con prompt, paquete y allowlist; transcript auditado; rótulo CIEGA-POR-CONTEXTO-NUEVO", "(B) pausar C1 hasta que exista el broker (recibo -3: provisionarlo antes de un C1 real)"],
      "de C1: (A), con B como meta", "NO", "no aplica",
      "«Autorizo el reconstructor de opción A para el lote 3 de C1: una sesión nueva de Claude Code, sin historial, con solo el prompt, el paquete y la lista cerrada de herramientas, con el transcript archivado y auditado antes de revelar. Sus resultados llevan el rótulo CIEGA-POR-CONTEXTO-NUEVO y no se presentan como aislamiento por broker. El broker sigue como meta.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-04"], "130 COINCIDE no ciegas del lote 2 de C1 (ENBIARE 126, ENCIG 4)", "ADOPCION-VETO", C1,
      "Coincidieron sin ceguera. Recuperables en el lote 3 con adaptador congelado.", "Re-comparar o rotular no ciegas para siempre.",
      ["(1) re-comparar en el lote 3 con adaptador congelado antes de revelar", "(2) rotularlas NO-CIEGA de forma permanente. Cuesta: se pierden 130 validaciones"],
      "de C1: (1)", "NO", "no aplica",
      "«Las 130 COINCIDE de ENBIARE/ENCIG del lote 2 quedan CONCUERDA-NO-APROBADA con rótulo NO-CIEGA-PENDIENTE; se re-comparan en el lote 3 con el adaptador v3 congelado antes de revelar.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-05"], "2 NO-PASA de remesas ENIGH 2020 bajo tolerancia 0.0", "CONTRATO-PROCEDIMIENTO", C1,
      "Δ de −4.4e-16 y −1.8e-12: redondeo, no desacuerdo. La tolerancia de una spec sellada no se enmienda hacia atrás.", "Decidir el trato.",
      ["(1) dejar el NO-PASA formal y abrir spec sucesora con tolerancia de coma flotante", "(2) dejar el NO-PASA sin sucesora"],
      "de C1: (1)", "NO", "no aplica",
      "«Queda el NO-PASA formal de los dos RESULT de remesas ENIGH2020. Autorizo una spec sucesora con tolerancia absoluta 1e-10 para su próxima validación; la spec sellada no se edita.»"),

    # ---------------- firmadas en chat (ADENDA-1) ----------------
    firmada("B1", "03", "3 filas NC de RECIBO-ASTRA-1 con estructura rota y guardia T-NC-CAMPOS", "CONTRATO-PROCEDIMIENTO", "(a)", "reparar las filas en PENDIENTES-2 (ya ejecutada por PENDIENTES-2: YA-CUBIERTA)", "TRAMITE-FIRMAS-21 con el PR de PENDIENTES-2"),
    firmada("B5", "07", "reescritura mecánica de filas desalineadas de no-corrido.tsv", "CONTRATO-PROCEDIMIENTO", "(a)+(c)", "ya ejecutada por PENDIENTES-2: YA-CUBIERTA", "TRAMITE-FIRMAS-21 con el PR de PENDIENTES-2"),
    firmada("B4", "06", "tres firmas de forma de CIERRE-MATERIAL-1 para Astra C2 (control ENIF, identidad ENCIG, singleton ENVIPE)", "CONTRATO-PROCEDIMIENTO", "las tres", "aprobar las tres como las redactó el ejecutor", "el acto C2 al ejecutar"),
    firmada("E3", "14", "envoltura de control ENIF y reconocimiento de identidad ENCIG", "CONTRATO-PROCEDIMIENTO", "(1)", "aprobar la envoltura y reconocer la identidad", "el acto C2 al ejecutar"),
    firmada("E4", "15", "unidad de remuestreo ENVIPE («singleton contribuyente»)", "CONTRATO-PROCEDIMIENTO", "(1)", "unidad del marco completo conforme al código congelado, fijada antes de habilitar R, con la medida de oferta al lado", "el acto C2 al ejecutar"),
    firmada("C1", "08", "caché de actions/cache en CI", "CONTRATO-PROCEDIMIENTO", "(a)", "no implementar la acción de marketplace", "TRAMITE-FIRMAS-21"),
    firmada("C2", "09", "prueba del auto-merge de rutinas", "CONTRATO-PROCEDIMIENTO", "(a)", "aceptar la evidencia de producción y citar el run real", "TRAMITE-FIRMAS-21"),
    firmada("D2", "11", "rótulo de ola de los 24 ids engasto_2012_* (son ENGASTO 2013)", "CONTRATO-PROCEDIMIENTO", "(a)", "corregir el rótulo 2012→2013 por herramienta, verificando antes que las dos olas estén en el manifiesto", "el acto de curación al ejecutar"),
    firmada("E2", "13", "recibo técnico de #1171", "CONTRATO-PROCEDIMIENTO", "(2)", "ya ejecutada por RECIBO-ASTRA6-2 (#1166, #1171, #1180): YA-CUBIERTA", "TRAMITE-FIRMAS-21"),
    firmada("E5", "16", "recibo técnico de #1180", "CONTRATO-PROCEDIMIENTO", "(2)", "ya ejecutada por RECIBO-ASTRA6-2: YA-CUBIERTA", "TRAMITE-FIRMAS-21"),
    firmada("E7", "18", "recibo técnico de #1166", "CONTRATO-PROCEDIMIENTO", "(2)", "ya ejecutada por RECIBO-ASTRA6-2: YA-CUBIERTA", "TRAMITE-FIRMAS-21"),
    firmada("F1", "19", "ejemplos congelados del motor (forense/ejemplos/GEN2-*, 4 fallas de test_consulta_gen2)", "CONTRATO-PROCEDIMIENTO", "(a)", "dueño y re-sello de los ejemplos", "TRAMITE-FIRMAS-21"),
    firmada("F3", "21", "cuatro ajustes del manifiesto del censo de integridad (raíz explícita, PDF MOCIBA, enco_*_reservado)", "CONTRATO-PROCEDIMIENTO", "1a 2a 3a", "ratificar; copiar los dos PDF de MOCIBA a data/raw; verificar por comando los cuatro archivos", "TRAMITE-FIRMAS-21"),
    firmada("F4", "22", "CALC-PISO-PERSISTENCIA-ERROR-0001 NO-EJECUTABLE contra libro vivo", "CONTRATO-PROCEDIMIENTO", "(a)", "CALC nuevo contra snapshot congelado", "TRAMITE-FIRMAS-21"),
    firmada("G1", "23", "resultados.tsv por encima de 100 MB en el canal [deriva]", "CONTRATO-PROCEDIMIENTO", "(B)", "marcador por rango; ningún consumidor asume archivo único", "el acto de tubería al ejecutar"),
    firmada("H1", "24", "parser de ids FP/ADR (gramática D-24)", "CONTRATO-PROCEDIMIENTO", "(a)", "parser ampliado con test", "el acto de tubería al ejecutar"),
    firmada("H2", "25", "conteo de FP de la vista --mesa (líneas físicas vs registros)", "CONTRATO-PROCEDIMIENTO", "(b)", "contar registros lógicos", "el acto de tubería al ejecutar"),
    firmada("H4", "27", "piso ENCIG de confianza institucional", "CONTRATO-PROCEDIMIENTO", "(a)", "alta de ENCIG-CONFIANZA-PISOS-1 (o lote de pisos)", "el acto ENCIG al ejecutar"),
    firmada("H5", "28", "docs/index.md en el git add del job de derivados", "CONTRATO-PROCEDIMIENTO", "(a)", "la línea en el job", "el acto de tubería al ejecutar"),
    firmada("I2", "30", "licencias del corpus, primer lote", "CONTRATO-PROCEDIMIENTO", "(a)", "los tres dominios mayores primero (ya ejecutada por CORPUS-LICENCIAS-1: YA-CUBIERTA)", "TRAMITE-FIRMAS-21"),
    R([P + "04", P + "05", "FP-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-05"], "alianza académica con laboratorio de microdatos (CIDE/ITAM), fecha 2026-10-15", "ACCION-CON-IDENTIDAD", f"{NCD} §B2 §B3",
      "B2 y B3 piden la misma fecha que c3fa-05 (MISMA-DECISIÓN: una firma, una fila). Firmadas en chat el 28/sep.", "Nada: ya firmada.",
      ["B2/B3 (a) confirmar 2026-10-15 (firmada)", "(b) otra fecha · (c) cerrar sin alianza (descartadas)"], "de NC-DECISIONES-1: (a)", "NO", "no aplica",
      "«firmado» (mesa, 28/sep/2026) sobre «B2 a · B3 a»: se confirma 2026-10-15 para la alianza académica; c3fa-05 pasa a FIRMADA con este texto. Asienta TRAMITE-FIRMAS-21.", AD),

    # ---------------- acciones con identidad ----------------
    R([P + "12", "FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01", "(sin FP) registros-con-identidad OBTENCION-EXTERNA-1"], "registros con identidad: EMOVI 2011/2023, WVS 7 EE.UU./Japón, WVS longitudinal, IFPS, MCPS, LAPOP completo", "ACCION-CON-IDENTIDAD",
      f"{NCD} §E1; {OE1}registros-con-identidad.md",
      "Seis fuentes piden una persona real que se registre y acepte términos. La firma venció dos veces (24 y 27/sep). OBTENCION-EXTERNA-1 dejó las URL comprobadas y la receta de un minuto. La ADENDA-1 dice que falta el día.", "Poner fecha y alcance.",
      ["(1) mesa se registra en EMOVI y las dos filas WVS esta semana (gratis, un minuto cada una)", "(2) (1) más IFPS y MCPS solo si una afirmación concreta los exige (MCPS pide convenio Oxford/UNAM)", "(3) ninguna: las 6 quedan NO-ACCESIBLE"],
      "de NC-DECISIONES-1: (1)", "SI", "hecha: OBTENCION-EXTERNA-1 (#1259), URL comprobadas el 27/sep",
      "«Firmo E1 (1): mesa presenta EMOVI 2011/2023 y las dos filas WVS antes del ____ (fecha); IFPS y MCPS esperan a que una afirmación los exija. Los archivos van a Descargas MX y los registra GEN2-OBTENCION-EXTERNA-2.»"),
    R([P + "20", P + "26", "FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01"], "respaldo del corpus fuera de la máquina (19.8 GB, 1 914 archivos)", "ACCION-CON-IDENTIDAD", f"{NCD} §F2 §H3",
      "Tres filas sobre el mismo objeto (MISMA-DECISIÓN). El respaldo verificado está en el mismo disco que el corpus. La fecha del 23/sep («esta semana») venció. La ADENDA-1 dice que falta ruta o fecha.", "Dar destino y fecha dura.",
      ["(a) disco propio: mesa da fecha calendario y avisa «montado en <ruta>»", "(b) nube cifrada de mesa, sin reformatear", "(c) aceptar el riesgo de disco único por un plazo largo y explícito"],
      "de NC-DECISIONES-1: (a) si el disco está listo; si no, (b)", "NO", "no aplica",
      "«Respaldo del corpus: opción (__) con fecha ____. Al recibir la ruta, se lanza GEN2-CORPUS-RESPALDO-EJECUCION-2 con --destino, reutilizando el staging ya verificado.»"),
    R(["(sin FP) solicitudes (a)–(f) OBTENCION-EXTERNA-1"], "paquete de seis solicitudes PREPARADAS, NO ENVIADAS (Banxico, IECM, Segob, Félix-Brasdefer, Delaney/FIU, Worldpanel)", "ACCION-CON-IDENTIDAD", f"{OE1}00-LEEME.md",
      "Siete solicitudes redactadas; la (g) ENAPROCE quedó ARCHIVADA-NO-NECESARIA (renglón I1). Las otras seis esperan que mesa las envíe con su identidad. Plazo legal PNT: 20 días hábiles (art. 134 LGTAIP).", "Decidir cuáles se envían.",
      ["(a) enviar las seis ya", "(b) enviar solo las tres por PNT (a, b, c): gratis y con plazo legal; las de correo y convenio (d, e, f) esperan a que una afirmación las exija", "(c) no enviar ninguna"],
      "PROPUESTO-POR-EJECUTOR: (b); el acto de origen no recomendó", "SI", f"hecha: {OE1} (redactadas y verificadas el 27/sep)",
      "«Envío las solicitudes ____ de OBTENCION-EXTERNA-1 con mi identidad; el acuse de cada una se registra por GEN2-OBTENCION-EXTERNA-2.»"),
    R(["FP-260923-GEN2-FRONT-1-4296-01", "FP-260926-GEN2-FRONT-3-PORTADA-1-8914-03"], "publicación del repo: GitHub Pages, DOI Zenodo, metadatos y vista previa social", "ACCION-CON-IDENTIDAD", "forense/firmas-pendientes.tsv (filas 4296-01, 8914-03)",
      "Dos filas sobre el mismo objeto (la cara pública del repo). Las dos vencieron el 27/sep; necesitan la cuenta de mesa en GitHub/Zenodo.", "Poner fecha o diferir.",
      ["(a) mesa las hace este fin de semana (receta de un minuto en FRONT-3 §P3)", "(b) diferir hasta que el catálogo tenga una regla adoptada", "(c) Pages y metadatos ahora; DOI después"],
      "PROPUESTO-POR-EJECUTOR: (c); las filas no traen recomendación nueva", "NO", "no aplica",
      "«Publicación: opción (__); fecha ____.»"),
    R(["(sin FP) NC-260928-GEN2-CORPUS-LICENCIAS-1-1997-01"], "licencia de 598 payloads sin licencia declarada (ENSANUT 149, UNAM 119, IETAM 46, …)", "ACCION-CON-IDENTIDAD", "forense/notas/nota-2026-09-28-gen2-corpus-licencias-1.md",
      "I2 ya se firmó y se ejecutó en su primer lote. Queda residual: el proxy de nube rechazó los 43 hosts, así que la licencia de 598 no se pudo leer. No hay licencias restrictivas halladas: hay licencias no leídas.", "Decidir cómo se leen.",
      ["(a) acto GEN2-CORPUS-LICENCIAS-2 en caja (con red)", "(b) no publicar esos payloads hasta tener licencia; no se busca activamente", "(c) mesa lee los términos a mano y los dicta"],
      "PROPUESTO-POR-EJECUTOR: (a); CORPUS-LICENCIAS-1 ya lo nombró sucesor", "SI", "pendiente: NO OBTENIDO POR CORPUS-LICENCIAS-1 (43 hosts, proxy)",
      "«Licencias residuales: opción (__).»"),

    # ---------------- forma ----------------
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C3-1-26bb-02"], "report de genómica en inglés (§3: todo en español)", "FORMA", C3,
      "El report entero está en inglés. Traducirlo ahora reescribe un report de Astra sin cifras nuevas.", "Aceptar en v2 o traducir.",
      ["(1) aceptarlo en v2 con nota en INDICE y traducir en v3", "(2) traducir ya"], "de C3: (1)", "NO", "no aplica",
      "«El report de genómica se acepta en inglés en v2, con nota en INDICE; se traduce en v3.»"),
    R(["FP-260928-GEN2-ASTRA-CONTINUIDAD-C3-1-26bb-03"], "cifra de cuerpos y CIE-11 en el report de duelo", "FORMA", C3,
      "L8 dice «más de 70 mil cuerpos»; DUEL-026 deja «más de 72 mil» (IBERO) como SIN-CIFRA. Dos ROMPE clínicos se apoyan solo en DSM-5-TR.", "Decidir la cifra y el cotejo.",
      ["(1) marcar la cifra «pendiente de cotejo de fuente y corte»; mantener los ROMPE con reserva «una sola fuente» y encargar el cotejo CIE-11 a un acto con red", "(2) publicar la cifra de L8 como está"],
      "de C3: (1)", "SI", "pendiente: cotejo CIE-11 y de la fuente de la cifra",
      "«Duelo: la cifra de L8 queda «pendiente de cotejo de fuente y corte»; los ROMPE clínicos llevan la reserva «una sola fuente»; el cotejo CIE-11 va a un acto con red.»"),
]

PEND2 = [
    ("NC-0164", "estimandos Banxico/SHED", "APERTURA-DE-DATO"), ("NC-0259", "emparejamiento revisado a mano (3 casos), ¿acreditable?", "ADOPCION-VETO"),
    ("NC-0290", "cuarta condición del bin 1 (adopción en bloque)", "CONTRATO-PROCEDIMIENTO"), ("NC-0318", "tres piezas antes de abrir R", "CONTRATO-PROCEDIMIENTO"),
    ("NC-0324", "enlace pre-R o encargo descriptivo", "CONTRATO-PROCEDIMIENTO"), ("NC-0335", "retirar de cola, cambiar estrategia o aceptar hueco", "CONTRATO-PROCEDIMIENTO"),
    ("NC-0346", "demanda por texto + blob del medidor, ¿reabre pisos?", "CONTRATO-PROCEDIMIENTO"), ("NC-0438", "rc de verify para REPLICA-RESULTADO·CONTEXTO-DISTINTO (0 o 1)", "CONTRATO-PROCEDIMIENTO"),
    ("NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-02", "acto que suba la fila NC-0270 al crosswalk de ejes", "CONTRATO-PROCEDIMIENTO"), ("NC-260922-GEN2-ESTADO-V15-1-7e23-03", "retirar la revisión manual de celdas_validadas (derivada por comando)", "FORMA"),
    ("NC-260922-GEN2-TRAMITE-COLA-VIEJA-1-0eca-02", "14 encargos de cola vieja: CONSUMIDO o HISTÓRICO", "FORMA"), ("NC-260923-GEN2-ESTADO-V16-1-fa47-02", "retiro real de g()/Theta.valor o HISTÓRICO-SIN-RETIRO", "CONTRATO-PROCEDIMIENTO"),
    ("NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-07", "vía (i) de E.3 (cuaderno §2.5)", "CONTRATO-PROCEDIMIENTO"), ("NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-11", "¿se retiran las 12 lecturas θ?", "ADOPCION-VETO"),
    ("NC-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-04", "serie ENSU por ciudad: medir o retirar", "CONTRATO-PROCEDIMIENTO"), ("NC-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-05", "segmentación ENSU = ENT/CIUDAD/SEXO/EDAD", "CONTRATO-PROCEDIMIENTO"),
    ("NC-260927-GEN2-TUBERIA-CI-TIEMPO-1-c6d9-01", "sustitución por COMMIT-D sin firma citada", "FORMA"), ("NC-260927-GEN2-TUBERIA-CI-TIEMPO-1-c6d9-02", "¿SIN-OBJETO por D-14?", "FORMA"),
    ("33 NC (letra 19)", "asignar dueño a 33 NC cuyo sucesor corrió sin producir lo pedido", "CONTRATO-PROCEDIMIENTO"),
]
for i, (nc, q, tipo) in enumerate(PEND2, 1):
    RENGLONES.append(R(
        [f"FP-260928-GEN2-TRAMITE-PENDIENTES-2-3fc6-01#{i}"], f"{nc}: {q}", tipo, f"{PE2} letra {i}",
        "PENDIENTES-2 la halló sin decidir al verificar por producto una NC cuyo sucesor ya corrió. La NC sigue ABIERTA. El acto de origen no dejó recomendación de fondo.",
        f"Decidir: {q}.",
        ["(a) decidir hoy con el sí/no de la pregunta, y que la ejecute el acto dueño de la ruta", "(b) mandarla a un acto que traiga opciones con costo (no se decide hoy)", "(c) cerrarla SIN-OBJETO con cita"],
        "PROPUESTO-POR-EJECUTOR: (b) salvo para las letras 17 y 18 (forma, cerrables con cita): el acto de origen dejó pregunta, no opciones, y firmar sin opciones es lo que mesa rechazó el 27/sep",
        "NO", "no aplica", f"«PENDIENTES-2 letra {i} ({nc}): opción (__).»"))


def serial(r):
    return {"renglon": r["n"], "ids_fundidos": " ; ".join(r["ids"]), "objeto": r["objeto"], "tipo": r["tipo"], "fuente": r["fuente"],
            "requiere_obtencion_previa": r["req"], "obtencion_hecha": r["hecha"], "estado": r["estado"],
            "opciones": " || ".join(r["opciones"]), "recomendacion": r["rec"], "texto_de_firma": r["texto"]}


COLS = ["renglon", "ids_fundidos", "objeto", "tipo", "fuente", "requiere_obtencion_previa", "obtencion_hecha", "estado", "opciones", "recomendacion", "texto_de_firma"]


def numera():
    orden = {t: i for i, t in enumerate(TIPOS)}
    pide = [r for r in RENGLONES if r["estado"] == "PIDE-FIRMA"]
    resto = [r for r in RENGLONES if r["estado"] != "PIDE-FIRMA"]
    frente = [r for r in pide if r["ids"][0].startswith(("(sin FP) HOLDOUT", "(sin FP) RESERVA"))]
    cuerpo = sorted([r for r in pide if r not in frente], key=lambda r: orden[r["tipo"]])
    todos = frente + cuerpo + resto
    for i, r in enumerate(todos, 1):
        r["n"] = f"R{i:02d}"
    return todos, frente, cuerpo, resto


def escribe():
    todos, frente, cuerpo, resto = numera()
    with open(AQUI / "decisiones-21.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in todos:
            w.writerow(serial(r))
    L = ["# Hoja de firmas para mesa · FIRMAS-21 · 28/sep/2026",
         "",
         "ACTO GEN2-TRAMITE-HOJA-FIRMAS-21-1. Junta en una hoja todo lo que hoy espera firma. **Contadores movidos: cero.** No firma, no asienta, no adopta. La tabla que recorre TRAMITE-FIRMAS-21 es `decisiones-21.tsv` (misma fuente: `arma_hoja.py`).",
         "",
         f"**En una línea.** {len(todos)} renglones: {len(frente)} decisiones nuevas al frente, {len(cuerpo)} que piden firma y {len(resto)} ya cubiertas o firmadas en chat (no se vuelven a pedir).",
         "",
         "Cómo leer cada renglón: situación · qué se te pide · opciones con su costo · recomendación (y de quién es) · obtención previa · texto de firma listo. Llena el hueco `(__)` con la letra que elijas.",
         "",
         "## 1 · Al frente: HOLDOUT y reserva de cinco olas",
         "",
         "Sin recomendación del acto: la añade dirección al recibir la hoja (encargo P2).",
         ""]
    def bloque(r):
        out = [f"### {r['n']} · {r['objeto']}", "", f"`{'` · `'.join(r['ids'])}` · fuente: {r['fuente']}", "",
               f"**Situación.** {r['situacion']}", "", f"**Qué se te pide.** {r['pide']}", "", "**Opciones.**"]
        out += [f"- {o}" for o in r["opciones"]]
        out += ["", f"**Recomendación.** {r['rec']}.", "",
                f"**Antes de firmar.** Requiere obtención previa: {r['req']} ({r['hecha']}).", "", f"**Texto de firma.** {r['texto']}", ""]
        return out
    for r in frente:
        L += bloque(r)
    L += ["## 2 · Decisiones que piden firma hoy", ""]
    for t in TIPOS:
        rs = [r for r in cuerpo if r["tipo"] == t]
        if rs:
            L += [f"## 2.{TIPOS.index(t) + 1} · {TITULO_TIPO[t]}", ""]
            for r in rs:
                L += bloque(r)
    L += ["## 3 · Ya cubiertas: no se vuelven a pedir", "",
          "Firmadas en chat (ADENDA-1 de este acto, 28/sep), firmadas el 27/sep (ADENDA-1 de RECIBO-ASTRA6-2) pero aún ABIERTA en el TSV, o cerradas por producto. Las asienta TRAMITE-FIRMAS-21 o el acto que las ejecuta (A.12: nunca las dos cosas sobre la misma fila).", "",
          "| renglón | ids | objeto | estado |", "|---|---|---|---|"]
    for r in resto:
        L.append(f"| {r['n']} | {' · '.join(r['ids'])} | {r['objeto']} | {r['estado']} |")
    L += ["", "## 4 · Conteo por tipo", "", "| tipo | pide firma | cubierta o firmada | total |", "|---|---|---|---|"]
    for t in TIPOS:
        a = sum(1 for r in frente + cuerpo if r["tipo"] == t)
        b = sum(1 for r in resto if r["tipo"] == t)
        L.append(f"| {t} | {a} | {b} | {a + b} |")
    L.append(f"| total | {len(frente) + len(cuerpo)} | {len(resto)} | {len(todos)} |")
    (AQUI / "hoja-para-mesa-firmas-21.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"escrito: {len(todos)} renglones")


def verifica():
    import yaml
    filas = list(csv.DictReader(open(AQUI / "decisiones-21.tsv", encoding="utf-8"), delimiter="\t"))
    fp = [x["id"] for x in csv.DictReader(open(RAIZ / "forense/firmas-pendientes.tsv", encoding="utf-8"), delimiter="\t") if x["estado"] == "ABIERTA"]
    ids = set()
    for x in filas:
        for i in x["ids_fundidos"].split(" ; "):
            ids.add(i.split("#")[0])
    sin = [i for i in fp if i not in ids]
    objs = [x["objeto"] for x in filas]
    dup = len(objs) - len(set(objs))
    malas = [x["renglon"] for x in filas if len(x["opciones"].split(" || ")) < 2 or not x["texto_de_firma"].strip()]
    frente = [x for x in filas if x["ids_fundidos"].startswith(("(sin FP) HOLDOUT", "(sin FP) RESERVA"))]
    man = yaml.safe_load(open(RAIZ / "data/manifiesto.yaml", encoding="utf-8"))
    por_id = {e["id"]: e for e in man if isinstance(e, dict)}
    olas_ok = True
    for _, ids_m, _, _ in OLAS:
        for i in ids_m.split(", "):
            if i not in por_id or "estado_reserva" in por_id[i]:
                olas_ok = False
    print(f"FP ABIERTA: {len(fp)} · ids sin renglón: {len(sin)} {sin}")
    print(f"renglones: {len(filas)} · duplicados por objeto: {dup}")
    print(f"renglones con <2 opciones o sin texto: {len(malas)} {malas}")
    print(f"decisiones P2 al frente: {len(frente)} (HOLDOUT + 5 olas) · estado de reserva por id coincide con la hoja: {olas_ok}")
    print(f"hoja existe: {(AQUI / 'hoja-para-mesa-firmas-21.md').exists()}")
    return 0 if not sin and not dup and not malas and len(frente) == 6 and olas_ok else 1


if __name__ == "__main__":
    sys.exit(verifica() if "--verifica" in sys.argv else escribe())
