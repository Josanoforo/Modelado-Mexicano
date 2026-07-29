# Auditoría de perímetro: T07–T10 solo ven corpus/reports/

**Fecha:** 29 de julio de 2026
**Estado de la suite al momento:** 18 FAIL · 107 WARN (`check.py`, HEAD 09bfb05)

---

## 0. Contexto de la corrida

- Los 18 FAIL se reprodujeron hoy en Windows 11, Python 3.14, contra la corrida original en contenedor Linux. Primera verificación independiente. El desglose por test coincide exacto.
- La suite no llegaba al final: `CONTRIBUTING.md` tenía un byte 0xC3 truncado en pos 2149 que rompía T03 con `UnicodeDecodeError`. Corregido en 09bfb05. `check.py` aborta la corrida entera ante un archivo mal codificado en vez de reportarlo.

---

## 1. Perímetro real de la suite

De los 13 tests de `check.py`, los tests T07, T08, T09 y T10 operan exclusivamente sobre `corpus/reports/*.md`. No revisan `canon/`, `corpus/forense/`, `forense/` ni `milpa/`.

| Test | Qué valida | Archivos que cubre | Archivos que NO cubre |
|---|---|---|---|
| T07 | Vocabulario de tiers | `corpus/reports/*.md` | `canon/`, `corpus/forense/`, `forense/`, `milpa/`, raíz |
| T08 | Mapa de evidencia por report | `corpus/reports/*.md` | ídem |
| T09 | Marco importado (c) usado como causa | `corpus/reports/*.md` | ídem |
| T10 | Muestra de diáspora (b) sin marcar | `corpus/reports/*.md` | ídem |

El motor (`canon/modelo-decision-v3_2.md`) solo lo revisan T04 (diagonal en ENTONCES) y T12 (conteos). Ningún test valida vocabulario de tiers, marcas de procedencia ni lenguaje causal dentro del motor, el glosario ni el integrador.

---

## 2. T09 — ampliar no gana señal

Se verificaron los 26 disparos que T09 produciría si cubriera `canon/` y `forense/` además de `corpus/reports/`. Se clasificó cada uno con cita textual.

**Conteo verificado:**

| Clasificación | Ya atrapado (reports/) | Nuevo (canon/ + forense/) | Total |
|---|---|---|---|
| USO CAUSAL REAL | 5 | 0 | 5 |
| MENCIÓN CRÍTICA | 2 | 16 | 18 |
| FALSO POSITIVO (co-ocurrencia) | 1 | 2 | 3 |
| **Total** | 8 | 18 | 26 |

Los 5 usos causales reales de Hofstede/PDI/UAI están todos en `corpus/reports/` y T09 ya los atrapa. Los 18 disparos nuevos son todos mención crítica o falso positivo por co-ocurrencia en líneas largas.

**Conclusión:** ampliar T09 a `canon/` y `forense/` no produciría señal nueva.

---

## 3. T10 — 4 defectos de medida + 1 defecto real

Se verificaron los 45 disparos nuevos que T10 produciría si cubriera `canon/` y `forense/`. De los 45, 39 son contexto de auditoría, 1 falso positivo, y 5 están en `canon/integrador-psicologia-mexicano.md`. Se analizó cada uno de los 5 con su bloque completo.

### 3.a — Cuatro defectos de medida de T10

En estos cuatro casos, el integrador marca la procedencia de diáspora pero no usa el marcador formal `(b)` ni la palabra "diáspora". T10 busca literalmente `(b)` o el regex `diáspora|no es evidencia sobre México`, y no encuentra las convenciones locales del integrador.

**L28** (`integrador:28`):
> *Casi todas las escalas (Sabogal, Lugo Steidel, Knight) se validaron con mexicano-americanos en EE.UU.*

Marca en la misma línea: cabecera `[Fuerte, con caveat US]` y "mexicano-americanos en EE.UU.". Reforzada en L164 (`integrador:164`): *"Caveat US fuerte: escalas de Sabogal, Lugo Steidel, Knight validadas con mexicano-americanos en contextos migratorios."*

**L30** (`integrador:30`):
> *Machismo ≠ caballerismo (dos dimensiones, Arciniega 2008). Precisión que el report de género exige: el machismo se asocia a ansiedad y hostilidad cínica (HCHS/SOL)*

Sin marca en la línea. Marca en L175 (`integrador:175`, mismo Patrón 4): *"Caveat US: Arciniega, Castillo, Wheeler y HCHS/SOL son de población latina en EE.UU."*

**L40** (`integrador:40`):
> *usa constructos de muestras US-hispanas (simpatía, Acevedo 2020; Ramírez-Esparza 2009) sin marcarlas consistentemente*

La línea dice "muestras US-hispanas" pero en contexto de diagnóstico del defecto, no como cita. T10 no distingue uso de mención crítica.

**L225** (`integrador:225`):
> *la simpatía se midió en muestras **US-hispanas** (Acevedo 2020; Ramírez-Esparza)*

"US-hispanas" está en la línea (`integrador:225`) pero no en la forma `(b)` ni "diáspora".

### 3.b — Un defecto real del integrador: L174

**Cita textual (L174):**
> **Evidencia a favor.** **Sólido**: machismo ≠ caballerismo (Arciniega 2008); marianismo-autosilenciamiento→malestar y barrera de búsqueda de ayuda (Castillo 2010); patrón demanda-retirada (Wheeler 2010)

**Cita textual del caveat (L175):**
> **Evidencia en contra / límites.** [...] *Caveat US: Arciniega, Castillo, Wheeler y HCHS/SOL son de población latina en EE.UU.*

Arciniega 2008, Castillo 2010 y Wheeler 2010 son estudios con muestras mexicano-americanas en EE.UU. L174 los presenta como "Evidencia a favor" con tier **Sólido** sin ninguna marca de procedencia. El caveat existe en L175, pero vive en la sección "Evidencia en contra / límites" — la sección opuesta. El tier se asigna sin la marca; la marca llega como limitación.

Este es el mecanismo que `forense/curaduria-archivos.md:23` ya documentó: *"convirtió un `[MEDIO], muestra mexicano-americana` en un `Fuerte` pelón"*. El integrador separa la afirmación positiva (con tier, sin marca) de la limitación (con marca, sin tier). Quien lea o cite la fila del tier no ve la marca.

**Clasificación: DEFECTO REAL del integrador.** La marca no viaja con el tier.

---

## 4. Convenciones de procedencia paralelas

El integrador usa al menos tres convenciones para marcar muestras de diáspora:

- `[Fuerte, con caveat US]` (L28)
- `Caveat US:` seguido de lista de autores (L164, L175)
- `muestras US-hispanas` / `muestras mexicano-americanas` (L40, L225)

Ninguna usa el marcador formal `(b)` del protocolo definido en el motor (`modelo-decision-v3_2.md §0.1`). T07 ya reprueba vocabularios paralelos de tier en `corpus/reports/`; esto es el mismo patrón en marcas de procedencia. La regla del protocolo es que la marca viaja con el dato; una convención local no viaja.

---

## 5. Error de estimación previa

La estimación inicial de disparos nuevos fue 22 para T09 y 46 para T10. La verificación exhaustiva arrojó 26 para T09 (8 ya atrapados + 18 nuevos) y 111 para T10 (66 ya atrapados + 45 nuevos). La estimación falló.

---

## 6. Discrepancia T03

T03 (referencias colgantes) produce 41 WARN, no 44. El total de WARN de la suite es 107, no 110. La diferencia de 3 está toda en T03. El 44 no tiene artefacto que lo respalde y no se puede reconstruir.
