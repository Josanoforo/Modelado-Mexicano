# Bloque candidato de adopción de reglas · 1 · ACTO GEN2-REGLAS-Y-RESULT-1

28/sep/2026 · derivado de `canon/reglas-contrastadas-v1_0.tsv` (162 reglas) · **candidato, no adoptado**: si mesa lo decide, el merge del PR que traiga el bloque es la adopción (E.2). Todo RETROSPECTIVO: ninguna regla se valida prospectivamente aquí.

## 1 · Conteo por dictamen (derivado: `python3 forense/analisis/reglas-y-result-1/p4_ensambla.py`)

| dictamen | reglas |
|---|---|
| CONFIRMA | 2 |
| MATIZA | 4 |
| MATIZA-SIN-CRUCE | 6 |
| ROMPE | 0 |
| INCOMPARABLE | 0 |
| SIN-CIFRA-GEN2 | 150 (143 NO-CONSTRUIBLE: prescriptivas, de mecanismo o sin reactivo; 7 con instrumento identificado) |

Solo (b)/(c): 39 reglas marcadas y fuera del bloque. Firewall genético: 12 reglas del dominio genética lo respetan; ninguna lo viola.

## 2 · El bloque (CONFIRMA · tier evidenciado ≥ media · procedencia (a))

| regla_id | regla (resumen) | RESULT · punto [IC95] · unidad | tier evid. | qué implica para el motor y el catálogo |
|---|---|---|---|---|
| RG-afa48731c6 | SI hogares de menor ingreso ENTONCES reservan más gasto a alimentos (probar precio/presentación/costo por canasta) | `RESULT-ENIGH-CONSUMO-PISOS-PART-ALIMENTOS-2022-DECIL-D01-P` 0.511 [0.483, 0.539] vs D10 0.283 [0.260, 0.308] · proporción del gasto, hogar | fuerte | Sin consumidor en `tramite.yaml`; entraría como regla descriptiva de CONSUMO con piso ENIGH 2022. El «probar precios…» es recomendación: sólo se adopta el SI→conducta (Engel); el driver es estructura, no preferencia (§3 oferta antes que preferencia). |
| RG-33ece9e072 | SI se segmenta por escolaridad la asistencia a comités ENTONCES no suponer gradiente educativo monótono | `RESULT-LAPOP-PISOS-CS-ASISTE-COMITE-MEJORAS-2019-ESCOLARIDAD-SECUNDARI…` 0.108 [0.081, 0.138] (primaria 0.169 [0.126, 0.212], superior 0.144) · persona | media | Sin consumidor. Regla de lectura (anti-gradiente), rotulada PROPUESTO-POR-EJECUTOR por Codex en C3-1; confirma solo la no-monotonía descriptiva; los IC se traslapan en parte. |

Reservas: ninguna de las dos identifica el PORQUE; se adoptaría la conducta descriptiva, no el mecanismo. Ninguna se basa en muestras de clase media urbana solamente (ENIGH y LAPOP nacionales).

## 3 · ROMPE — correcciones propuestas a reports
Ninguna regla ROMPE: no hay corrección que proponer a reports v3 desde este bloque.

## 4 · MATIZA (fuera del bloque; alimentan reports v3 y cruces)
RG-56f645220c (horizonte de ahorro × seguridad social), RG-97bd27956f (mordida presencial 14.1% vs digital 3.0%, unidad trámite), RG-55c7a10915 (denuncia de robo de vehículo × seguro, unidad delito), RG-6f79d79dc1 (vacunación: razón logística). MATIZA-SIN-CRUCE: RG-a4ed0259ce, RG-3d4669ddc0, RG-1bd7c23d10, RG-cc7bc4ae1a, RG-a215c82838, RG-806ce20ffa — piden el cruce que el SI condiciona.

---

# Hoja para mesa (lenguaje RH)

**Qué se decide.** Si dos reglas de conducta, ya respaldadas por cifras selladas, pasan de «propuesta» a «adoptada».

**Lo que hay.** De 162 reglas que el programa tiene escritas, solo 2 se sostienen hoy con una cifra sellada en la misma unidad; 10 se matizan; ninguna queda desmentida; 150 no tienen cifra (la mayoría son recomendaciones o mecanismos que ninguna encuesta mide).

**Opciones.**
1. **Adoptar el bloque (2 reglas)** — recomendada: son descriptivas, con IC que separa, datos nacionales (a); costo cero para el motor (ninguna tiene consumidor todavía).
2. Adoptar por dominio (CONSUMO sí, CAPITAL_SOCIAL después) — si mesa quiere más traslape de IC resuelto en la de comités.
3. Esperar cruces — si mesa prefiere un bloque más grande con las 6 MATIZA-SIN-CRUCE medidas en caja.

**Texto de firma listo:** «Mesa adopta el bloque candidato 1 de GEN2-REGLAS-Y-RESULT-1 (RG-afa48731c6, RG-33ece9e072) como reglas descriptivas, sin adoptar su PORQUE.» · Fila: `FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01`.
