# REGION-ENIF-PORTAFOLIO · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta. Esta pieza agrega regionalmente siete desenlaces de ahorro ENIF 2024 ya enumerados por consumidores U1/milpa, sin clase AMAI. El estimador es de la **persona elegida 18+**, y su geografía son exclusivamente las seis regiones oficiales de diseño `REGION=1..6`; no se estima entidad. El insumo es `enif_2024_enif_2024_bd_csv` del manifiesto, miembro `TMODULO.csv`, sin datos reservados. La batería y factor son los mismos del piso `CALC-REGION-ENIF-2024-0001`; este bloque conserva ese universo y no lo confunde con la serie histórica 18–70.

## Desenlaces y denominador congelados

`I = alguna P5_1_1..P5_1_6 == '1'`; `F = alguna P5_6_1..P5_6_9 == '1'`. Denominador común: al menos una respuesta sustantiva `1/2` en la unión de ambas baterías. Los códigos distintos se excluyen de la definición de respuesta válida. En cada persona del denominador:

| Conducta | Numerador |
|---|---|
| `no_tiene_ahorros_enif2024` | `¬I ∧ ¬F` |
| `informal_cualquiera` | `I` |
| `formal_cualquiera` | `F` |
| `ahorra_solo_informal` | `I ∧ ¬F` |
| `ahorra_solo_formal` | `F ∧ ¬I` |
| `ahorra_ambas_vias` | `I ∧ F` |
| `no_ahorra` | `¬I ∧ ¬F` |

Los dos nombres del complemento comparten valor solo si se conserva este denominador; se publican como RESULT distintos para no inventar una cita. La batería formal puede estar gateada por tenencia de cuenta: una ausencia de `1` no prueba preferencia ni exclusión por sí sola. No se afirma que las categorías expliquen causalmente mecanismos. `I`, `F`, sus intersecciones y complementos son asociaciones descriptivas.

## Diseño, publicación y archivo

Factor `FAC_PER`; estrato `EST_DIS`; UPM `UPM_DIS`. Razón ponderada de masas por región; no media de porcentajes. Plan de 1 000 réplicas UPM estratificadas, compartido entre regiones dentro de cada conducta, con semilla PCG64 20260923 y módulo `marginales_reproduccion.py::replicas_compartidas` SHA256 `4df2c630179c194345594d959d012b7dd18d94ac93fab3f48b8f6683753dafd6`. El marco completo de `TMODULO` forma el plan antes de aplicar denominador y región. Estratos de UPM única reciben el tratamiento fijado en el módulo compartido; n<200, varianza degenerada, réplica inválida o falta de soporte producen punto/IC nulos, sin cambiar n ni región para recuperar filas. R1/R2 de mesa del 23/sep/2026 rigen íntegramente.

El `-JSON` de cada conducta conserva réplicas conjuntas de las seis regiones, sin IDs ni pesos individuales; los scalar RESULT incluyen punto, IC95 de diseño, n, Kish y estado por región. `cuenta_gen2: SI`, `adopta: NO`, temporalidad **RETROSPECTIVA**. No se produce IC predictivo calibrado ni cruce región×clase. El script efectivo y sus imports van fijados en el CALC. Las siete conductas se corren juntas para conservar el mismo contrato de batería y evitar selección por cifras.

## Auditoría de rigor extremo

ENIF 2024 no ofrece entidad actual en este módulo; una región oficial no equivale a una ciudad. La clasificación de ahorro puede cambiar con liquidez, oferta y acceso financiero. Nada aquí identifica clase AMAI, población indígena o una preferencia cultural. Celdas amplias pueden tener incertidumbre de diseño material aun con n≥200.
