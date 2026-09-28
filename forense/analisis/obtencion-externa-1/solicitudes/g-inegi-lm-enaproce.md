# (g) Laboratorio de Microdatos INEGI · ENAPROCE 2015/2018 para la parte PyME de R03 — CONDICIONADA

Estado: **CONDICIONADA — ni se envía ni se archiva como innecesaria todavía.**

## Por qué
- El encargo (P4-g) la ata a una conclusión ajena: «**solo** si MAPA-INSTRUMENTOS-ALTERNOS-1 concluye que ENCRIGE/ENVE no cubren la parte PyME de R03; si no, la solicitud de `P4-I1-solicitud-LM.md` se archiva como no necesaria y se dice por qué».
- [EJECUTADO, 27/sep/2026 ~21:10] Estado de ese acto contra origin: la rama `acto/gen2-mapa-instrumentos-alternos-1` existe con **un solo commit** (`4b11076a`, su 0-bis: encargo verbatim + sello); `gh pr list --search MAPA-INSTRUMENTOS-ALTERNOS` → ningún PR; `git ls-tree origin/main | grep mapa-instrumentos-alternos` → nada. **No hay conclusión que leer.** Ninguna de las dos ramas del encargo se puede tomar sin inventarla.
- Lo que sí está fusionado y cuenta para mesa (LEÍDO, `forense/analisis/obtencion-previa-1/P4-I1-nota.md`): «ningún reactivo mide solicitud o pago informal, así que la mitad `mordida` de R03 no tiene desenlace en ENAPROCE con ninguna vía de acceso». El Laboratorio sólo serviría para la mitad «carga regulatoria» (PyME, 2015, error estándar).

## Texto listo
El texto completo (campos del proyecto para pegar en el formato `Solicitud_Uso.pdf`, adjuntos y receta de un minuto) **ya existe y no se duplica**: `forense/analisis/obtencion-previa-1/P4-I1-solicitud-LM.md` (GEN2-OBTENCION-PREVIA-1, fusionado). Formato del LM en corpus [EJECUTADO, por sha]: id **`inegi_laboratorio_microdatos_solicitud_uso`** (`R2.1_R2.2_R10.2_RNM_microdato/inegi_laboratorio_microdatos_solicitud_uso.pdf`, sha256 `5a5d041d…15c19`). La ruta que cita esa nota (`data/raw/obtencion-previa-1/enaproce/inegi_lm_solicitud_uso_formato.pdf`) no es la registrada: el mismo sha ya estaba bajo este id, así que se cita por id.

## Regla de decisión para cuando MAPA cierre (la aplica quien lea su mapa; no requiere firma nueva)
- Si `canon/mapa-instrumentos-alternos-v1_0.tsv` dictamina que ENCRIGE 2020 y/o ENVE **cubren** carga regulatoria de PyME (unidad empresa, tamaño PyME) → esta solicitud se archiva como **no necesaria**, citando la fila del mapa.
- Si dictamina que **no la cubren** → mesa envía `P4-I1-solicitud-LM.md` tal cual, con las dos firmas previas que esa nota exige (R03 redefinida como «carga regulatoria»; unidad empresa aceptada).

## Receta de un minuto (mesa, cuando aplique)
1. Abrir `forense/analisis/obtencion-previa-1/P4-I1-solicitud-LM.md` → seguir su «Receta de un minuto» (5 pasos).
2. Anotar el folio en la fila `ENAPROCE_2015_2018_MICRODATO_COMPLETO` de la cola (hoy NO-ACCESIBLE; la solicitud no cambia su estado hasta que haya acceso).
