# ENVIPE · precisión de la unidad de remuestreo antes de habilitar R · v1.0

Acto `GEN2-ASTRA6-C2-EJECUCION-1` · 28/sep/2026 · CAJA · 0-bis `e897d3df`.
Familias: `ENVIPE-DENUNCIA-U4` y `ENVIPE-EVASION-NORMA` (una sola apertura, un solo plan de réplicas). Cara mecánica: `enmienda-firmas-c2-envipe-v1_0.yaml`.

**Contadores movidos: cero.** No modifica el código congelado (`tools/familias-2027/envipe/medidor.py`, commit `f59b1b90`), ni `spec-v1_3.md`, ni `spec.yaml`, ni `emision.json`, ni `sello.json`. Precisa el texto de la spec humana **hacia** lo que el código ya hace, por la opción firmada.

## 1 · Firma de mesa que se ejecuta (verbatim)

Mesa, 28/sep/2026, «firmado» sobre la línea «… B4 las tres · … · E3 1 · E4 1 …» (`forense/encargos/2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-1.md`). Texto firmado, B4-(iii) = E4 opción 1 (`hoja-c2-para-mesa-v1_0.md` l.27):

> «Para ENVIPE, la frase singleton contribuyente se precisa así: se usa la unidad del marco completo de remuestreo, conforme al código congelado, y el soporte del dominio se conserva como diagnóstico. No se modifica ningún sello. Antes de habilitar R se añade la medida de exclusión por oferta junto al marginal.»

FP que resuelve: `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06` (B4) y `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-15` (E4).

## 2 · La ambigüedad y cómo queda fijada

- **Spec humana** (`forense/prereg-caja/FAMILIA-2027-ENVIPE-DENUNCIA-U4-spec-v1_3.md` §Dictamen, punto 2; igual en EVASION-NORMA): «Cualquier singleton que contribuya al estimando implica `NO-ESTIMABLE` …». Admite dos lecturas: un estrato con una sola UPM **dentro del dominio** de la familia, o un estrato con una sola UPM **en el marco de remuestreo**.
- **Código congelado** (`tools/familias-2027/envipe/medidor.py`, LEÍDO):
  - l.88–96: el marco son todas las personas de `tper_vic2` con `EST_DIS`, `UPM_DIS` y `FAC_ELE` válidos.
  - l.168–180: el remuestreo se hace por estrato **del marco**. Si el estrato tiene una sola UPM, se suma con multiplicidad fija y cuenta en `single`.
  - l.191, l.195–198: `estimable` exige `single == 0`, además de soporte, estratos, UPM y réplicas.
  - l.149: `singleton_soporte`, el singleton de dominio, sólo se reporta y no entra a la compuerta.
- **Fijado (opción 1 firmada):** «singleton contribuyente» = estrato con una sola UPM **en el marco completo `tper_vic2`** (`singleton_marco`). Cualquiera mayor que 0 → `NO-ESTIMABLE`, como ya hace el código. El singleton de dominio (`singleton_soporte`) queda como **diagnóstico** y no habilita ni bloquea: una UPM que es única en el dominio sigue variando en las réplicas dentro de su estrato completo.

## 3 · Qué dice el oro histórico con esta unidad (LEÍDO, `astra6-envipe/diagnostico.json`, ENVIPE 2025, ola vista)

```
diseno: estratos_marco=746 · upm_marco=13742 · singleton_marco=0 · replicas_comunes=2000
DENUNCIA_U4:   n=13023 · estratos=725 · upm=7830  · singleton_soporte=83 · estimable=True
EVASION_NORMA: n=40280 · estratos=739 · upm=10694 · singleton_soporte=23 · estimable=True
```

Son RETROSPECTIVA (diagnóstico de soporte sobre una ola vista), no acierto futuro. Con la unidad fijada, los 83 y 23 singletons de dominio no bloquean. Si la ola 2027 trae algún estrato con una sola UPM en el marco, el dictamen es `NO-ESTIMABLE`: no se relaja tras R.

## 4 · «Medida de exclusión por oferta junto al marginal»

Mesa, 28/sep/2026, a pregunta de este acto: la medida va con **ENIF ahorro** («ENIF ahorro (Recomendado)»), no con la denuncia ENVIPE. Razón: la pieza nace en `1178-ENIF-NC-F` y en `interpretacion-y-oferta.md` («junto a cada marginal de ahorro o canal»), y v2.16 §3 la exige para la conducta de mercado. El texto firmado la redactó dentro de la frase de ENVIPE. Ver `astra6-enif/enmienda-firmas-c2-v1_0.md` §4. **Para ENVIPE no se añade medida nueva**: el motivo de no denuncia ya es el estimando (C2 = {01, 02, 06, 08}), y una partición nueva del mismo reactivo sería un contendiente más.

## 5 · Módulo de auditoría v2.16

- Unidades: DENUNCIA-U4 es persona víctima con al menos un delito U1; EVASION-NORMA es **delito**. No se promedian entre sí.
- PROSPECTIVA: sólo las emisiones selladas del 26/09. El diagnóstico de §3 es RETROSPECTIVA. Ninguna frase las mezcla.
- Riesgo de lectura simplista: leer «no denuncia por miedo o desconfianza» o «evasión» como rasgo cultural. Son tasas condicionadas a victimización y a oferta institucional (§3 de las instrucciones).
