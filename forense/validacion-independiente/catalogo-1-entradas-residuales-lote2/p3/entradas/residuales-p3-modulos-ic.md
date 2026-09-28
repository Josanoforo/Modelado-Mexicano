# RESIDUALES-P3-MODULOS-IC-v1 · PROPUESTO-POR-EJECUTOR

Estos cuatro módulos aplican RESIDUALES-P3-IC-v1 sin adoptar estimandos ni cambiar filtros históricos. Las identidades finales las fija el esquema humano entregado; requieren contrato de punto suficiente. Sin esa spec, no se ejecuta la identidad aunque la receta IC esté completa.

| Módulo | Unidad, base, peso | Diseño y unión | Ámbito |
|---|---|---|---|
| ENBIARE2021 | Persona elegida18+, TENBIARE; FAC_ELE>0 finito | EST_DIS/UPM_DIS opacos; TSDEM por FOLIO+VIV_SEL+HOGAR+N_REN, único | Escalas0..10 medias; demás conductas proporciones; marco persona elegida18+ previo al filtro de conducta/eje |
| ENCODAT2016–2017 | Persona12..65 de Individual; ponde_ss>0 finito | est_var/code_upm de Hogar, id_pers primeros20 caracteres=id_hogar único | Conservar sexo, edad y escolaridad18+ conforme spec; marco conjunto base12..65, no reducido a mayores18 para eje educativo; no ENCODAT2025 |
| ENCUCI2020 | Persona seleccionada 15+; A: FAC_SEL de SEC_4_5; B protesta: FAC_SEL de SEC_6_7_8; peso>0 finito | EST_DIS/UPM_DIS de tabla base; B: SEC_6_7_8 base unida a SEC_4_5 por ID_PER único, sin reordenar; no sustituir ni promediar pesos | Familia A dominio contacto/respuestas; B protesta×DOMINIO×agravio; marco completo personas15+ con diseño antes de contacto, agravio o rural; ruralR, urbanoU/C, sin sensibilidad como primaria |
| ENIGH2022 | Hogar concentradohogar; factor>0 finito | est_dis/upm; folioviv+foliohog único | remesas>0 y complemento remesas=0 directo; nulos remesas provocan NO-ESTIMABLE-NULOS-INESPERADOS; marco completo hogares con diseño; no ENIGH2024 |

Semilla común20260923 y marco completo son elecciones NUEVAS del contrato diagnóstico; no restauran semillas históricas20260924/20260909/20260915. B2000 y percentiles2.5/97.5 preservan familia de recetas, no equivalencia histórica. ENBIARE/ENCODAT referían receta común que es código productor; no se abrió ni se convierte en fuente humana. Los diseños oficiales describen la encuesta y métodos Taylor, no esta realización bootstrap.

La retención de UPM con contribución cero evita redefinir la ley al filtrar dominios. El uso de semilla común permite un estándar diagnóstico; se reinicia por identidad para no depender del orden del catálogo. El bootstrap no reescalado se conserva por compatibilidad con la propuesta común previa; no se recomienda para afirmar cobertura poblacional sin justificación adicional. Conservar ponderadores finales respeta estimandos humanos, pero condiciona inferencia a su calibración. Los singleton quedan explícitamente no identificados.
