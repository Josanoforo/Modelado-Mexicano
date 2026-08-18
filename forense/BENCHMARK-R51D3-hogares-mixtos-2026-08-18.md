# BENCHMARK · R5.1-D3 — hogares mixtos (T y C bajo el mismo techo) en DiD de pensiones
**Motivo:** prompt D-1b de `MESA-19AGO` (18/ago/2026). Tres reglas candidatas en `forense/notas/2026-08-11-e4c-r5-1-d2-commit3-ajuste-preejecucion.md:84-92`; conteos: 1,312 hogares mixtos en 2018 (31.4% de los de ≥2 personas 65+) y 2,201 en 2022 (36.1%). "No lo decide el ejecutor. Queda para mesa."
**Universo de búsqueda declarado (A.4/A.10):** 5 consultas web el 18/ago/2026 vía buscador de esta sesión de dirección — *pension eligibility elderly living arrangements household treatment control members* · *Hamoudi Thomas endogenous coresidence pension South Africa* · *Galiani Gertler Bando 70 y Más Mexico eligibility household* · *Duflo 2003 pension eligible member household definition* (+1 variante). **Todo hallazgo proviene de abstracts/snippets de buscador — clase segunda-mano A.6, `SIN-FETCH`**: la receta manual de verificación es el URL de cada entrada; ninguna afirmación de abajo requiere el texto completo para el uso que se le da (mapear precedentes, no extraer cifras).

---

## §1 · Los cuatro hallazgos que deciden

**H1 · La composición del hogar es ENDÓGENA a la elegibilidad — el hallazgo que gobierna todo lo demás.**
Hamoudi & Thomas (2014), *Journal of Development Economics* 109:30-37, sobre la Old Age Pension sudafricana: los beneficiarios tienen mayor probabilidad de corresidir con adultos de menor capital humano medido por **estatura y educación — rasgos fijos en adultos**, de modo que no puede ser efecto del ingreso: es **re-arreglo selectivo de la corresidencia causado por la elegibilidad**. Conclusión textual del abstract: los hallazgos "resaltan la endogeneidad de los arreglos de vivienda". URL: `sciencedirect.com/science/article/abs/pii/S0304387814000327` · `pmc.ncbi.nlm.nih.gov/articles/PMC4138532`.
**Implicación directa para D-1b:** *ser hogar mixto* es en parte un desenlace del propio tratamiento (quién termina viviendo con quién). Cualquier regla que condicione en la composición realizada —incluida la exclusión— condiciona en algo que el tratamiento mueve. Es exactamente la advertencia de **A-bis regla 2** (colisionador/selección), ahora con cita externa.

**H2 · La regla de asignación de hogar con precedente es "≥1 miembro elegible ⇒ hogar expuesto" — no la del máximo ingreso.**
La tradición completa (Case & Deaton 1998; Duflo 2000/2003 *WBER* 17(1):1-25; Edmonds 2006; Bertrand, Mullainathan & Miller 2003) define la exposición del hogar/menor por **convivir con una persona elegible** ("living with an eligible female…", "more than a quarter of black children under five live with a pension recipient"). Ningún resultado del barrido asigna el hogar por *el* adulto mayor de mayor pensión contributiva. URL: `academic.oup.com/wber/article-abstract/17/1/1/1676291` · `jhr.uwpress.org/content/51/4/900`.

**H3 · Las restricciones de muestra para limpiar la comparación son práctica estándar y se declaran.**
Ambler (*JHR* 2016, 51(4):900-) restringe a adultos 50-75 y a hogares con menores de 15, siguiendo a Duflo y Edmonds; los RD de corresidencia (p. ej. PMC5642942, pensión china) construyen la muestra precisamente para *evitar* "la complicación de la formación endógena del hogar". Restringir universo es legítimo; lo que la literatura exige es **declararlo y acompañarlo de la estimación sin la restricción**.

**H4 · Nadie cuenta un hogar en T y en C a la vez.**
Cero resultados con doble conteo en los cinco barridos. La literatura mexicana del programa (Galiani, Gertler & Bando 2016 *Labour Economics* 38:47-58; Juárez & Pfutze 2015; Ávila-Parra et al. 2024 *Economic Inquiry*) usa cortes de edad/geografía sobre beneficiarios y hogares elegibles — nunca la misma unidad en ambos numeradores.

## §2 · Mapa a las tres reglas del commit3

| Regla | Precedente | Veredicto |
|---|---|---|
| **1 · Excluir mixtos** (solo desenlace de corresidencia; −1,312/−2,201) | Sí — restricción de muestra estándar (H3); mecánicamente trivial aquí (`grupo=None` aporta residual cero en `diff_ultimate_cluster`, contrato ya verificado) | **PRIMARIA — con dos condiciones no opcionales:** (i) universo **ACOTADO declarado** (A-bis r4: el estimando pasa a "hogares 65+ sin mezcla T/C" y el marginal se recalcula sobre ese mismo universo); (ii) **sensibilidad pre-declarada en COMMIT A** con la regla de H2, porque la exclusión condiciona en composición endógena (H1) — si el programa *causa* hogares mixtos (un beneficiario se muda con un pensionado), excluirlos **borra eventos de corresidencia inducidos por el tratamiento y sesga el DiD hacia cero**: conservador para `EJERCIDA`, y se dice en el acta con esa dirección |
| **2 · Asignar por P032-máx** | **No** — el precedente de universo completo es "≥1 elegible ⇒ hogar T" (H2), no el máximo contributivo. Además tiene **signo perverso**: un hogar con un 65+ de pensión alta y otro elegible quedaría en **C** aunque la transferencia del programa **entra a ese hogar** | **DESCARTADA como está escrita.** Su versión con precedente (any-member) entra como la **sensibilidad** de la regla 1 |
| **3 · Contar dos veces** | **No** (H4); además rompe la exclusividad mutua declarada en Commit 1 §2.2 y no es neutral para la varianza (la propia nota lo dice) | **DESCARTADA** |

**Nota de alcance:** todo esto aplica **solo al desenlace de corresidencia**. El de transferencia (`P040`) es persona-nivel y coherente sin regla de hogar — intocado, como el commit3 ya declara.

## §3 · Texto propuesto para el campo "Otro" del prompt D-1b
> Regla 1 como primaria: excluir mixtos solo del desenlace de corresidencia, con universo ACOTADO declarado (A-bis r4) y el marginal recalculado sobre ese universo. Sensibilidad obligatoria pre-declarada en COMMIT A: universo completo con "hogar T si tiene ≥1 persona 65+ en T" (precedente Duflo/Case-Deaton) — no la variante P032-máx, que queda descartada por falta de precedente y signo perverso. Regla 3 descartada. Al acta va la advertencia Hamoudi-Thomas 2014: la composición del hogar es endógena a la elegibilidad, la exclusión condiciona en composición realizada y sesga hacia cero — por eso la sensibilidad no es opcional. Fuente: BENCHMARK-R51D3-hogares-mixtos, archívese en forense/ y cítese en el ADR.

## §4 · Lo que este benchmark NO establece
No adjudica el DiD ni toca umbrales de §6 · no convierte los abstracts en evidencia de primera mano (todo `SIN-FETCH`; las URLs son la receta) · no decide por mesa — ordena los precedentes para que la decisión de 30 segundos sea la informada.
