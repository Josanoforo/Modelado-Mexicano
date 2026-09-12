# Cierre · GEN2 SHED 2025: BNPL, daño y universos correctos

Fecha de ejecución: 11/sep/2026. Entorno: CAJA Ubuntu/WSL2 con corpus
compartido. Objeto: `CALC-SHED2025-BNPL-DANO-0001`.

## 1 · Resultado útil

El corte transversal SHED 2025 permite medir cinco objetos descriptivos sin
mezclar sus bases. Los cuatro puntos principales son:

| Estimando | Universo válido | n positivo | masa válida (`weight`) | masa positiva | Punto ponderado |
|---|---:|---:|---:|---:|---:|
| Uso BNPL en el último año | 12,934 | 2,004 | 12,933.9866 | 2,132.7017 | 16.49% |
| Atraso entre usuarios BNPL | 2,004 | 487 | 2,132.7017 | 549.8174 | 25.78% |
| Cargo extra entre quienes afirmaron atraso | 487 | 302 | 549.8174 | 352.4910 | 64.11% |
| Sobregiro/NSF atribuido a BNPL entre usuarios que declararon sobregiro previo | 542 | 206 | 595.6078 | 230.9771 | 38.78% |

Los denominadores no son intercambiables. En particular, 38.78% no es una
prevalencia entre los 2,004 usuarios BNPL: es una proporción condicional entre
542 personas que además declararon haber pagado un cargo por sobregiro en el
último año y respondieron `BNPL1A`.

## 2 · Asequibilidad y atraso

Entre los 2,004 usuarios con `BNPL4_e` y `BNPL3` válidos:

| “Única forma de poder pagar” (`BNPL4_e`) | Sin atraso: n / masa | Con atraso: n / masa | Atraso ponderado |
|---|---:|---:|---:|
| No | 758 / 786.1960 | 85 / 94.4147 | 10.72% |
| Sí | 759 / 796.6883 | 402 / 455.4027 | 36.37% |

La diferencia descriptiva es **+25.65 puntos porcentuales** (sí menos no).
Es asociación transversal: el motivo de asequibilidad no es un tratamiento y
este cálculo no identifica efecto causal.

## 3 · Fuente, identidad y rutas

Los IDs de entrada se resolvieron por manifiesto y coincidieron contra disco:

| ID | objeto | bytes | SHA-256 |
|---|---|---:|---|
| `gen2_federal_reserve_shed_2025_public_csv` | ZIP con `public2025.csv` | 4,676,794 | `a4ab3f7d042f16d63626b1af9aeb6f0b8a0b39e412fa94b87265bc67fe26de14` |
| `gen2_federal_reserve_shed_2025_codebook` | codebook, actualización 4/sep/2026 | 849,070 | `3094d147be4fe60214b1c2550537d1b9d931559d3f804be7976b24e43e27311e` |
| `gen2_federal_reserve_shed_2025_appendix_a_questionnaire` | cuestionario oficial Appendix A | 159,382 | `219658415e2aee6abf6f480be83e4faeb54d2c439f447cb61662514db1982864` |

El cuestionario fija estas rutas:

- `BK1` pregunta si existe cuenta bancaria; `BK2_f` se muestra si `BK1=1` y
  pregunta por un cargo de sobregiro durante los últimos 12 meses.
- `BNPL1` se pregunta a todos; `BNPL3` si `BNPL1=1`.
- `BNPL3A` se pregunta si `BNPL3=1` o si se rechazó `BNPL3`.
- `BNPL1A` se pregunta si `BNPL1=1` y `BK2_f=1`.
- `BNPL4_e` se pregunta a usuarios BNPL y significa que BNPL fue la única
  forma en que podían pagar la compra.

En el CSV exacto, las 12,934 personas tienen `shedid` único y `weight` y
`weight_pop` positivos. El codebook muestra 1/0, pero el CSV usa `Yes`/`No`;
el medidor rechaza literales numéricos para impedir una mezcla de capas. No
hay rechazo ni no sabe observado en estos reactivos. La ruta de rechazo de
`BNPL3` aporta n=0 respuestas válidas a `BNPL3A`; se conserva explícitamente
separada y nunca entra en la tasa principal de cargo.

Las ausencias de `BNPL1A` se descomponen en 10,930 no usuarios BNPL, 116
usuarios sin cuenta bancaria (`BK1=No`) y 1,346 usuarios con cuenta pero sin
sobregiro previo (`BK2_f=No`). Las 542 personas elegibles respondieron.

## 4 · CALC/RESULT, agregados y comprobaciones

La spec se congeló en el commit `6c160f8` antes del cálculo. El preflight
resolvió los tres inputs, 66 RESULT únicos, 815 columnas, el script y el árbol
limpio. La corrida `CALC-SHED2025-BNPL-DANO-0001--6c160f8586f8` terminó con
exit 0 y sello coincidente.

Artefactos principales:

- `data/corrida0/CALC-SHED2025-BNPL-DANO-0001/`: spec, medidor,
  `ejecucion.json`, `resultados.json` y sello.
- `data/shed2025-bnpl-dano/estimandos-shed.csv`: numeradores, denominadores,
  masas, puntos, faltantes y definiciones.
- `data/shed2025-bnpl-dano/asequibilidad-atraso-2x2.csv`: las cuatro celdas.
- `data/shed2025-bnpl-dano/faltantes-por-ruta.csv`: ausencias por razón.
- `data/shed2025-bnpl-dano/resultados-legibles.md` y
  `grafico-bnpl.svg`: lectura humana con bases explícitas.
- `data/shed2025-bnpl-dano/ficha-uso-extranjero.md`: límites de uso.

El control independiente leyó el ZIP directamente, sin importar el medidor:
reprodujo uso (2,004/12,934; p=0.164891287269) y sobregiro condicional
(206/542; p=0.387800663457), y confirmó cero respuestas válidas por la ruta
de rechazo. Los tres falsadores dirigidos cubren denominador BNPL1A, mezcla
de códigos y exclusión del rechazo de `BNPL3` de la tasa de cargo.

Reproducción:

```bash
python3 tests/test_shed2025_bnpl_dano.py
python3 tools/corrida0.py verify CALC-SHED2025-BNPL-DANO-0001
python3 tools/publica_shed2025_bnpl_dano.py
python3 tools/verifica_shed2025_bnpl_independiente.py \
  --zip data/raw/GEN2_N34_PRODUCTO_DANO/shed_2025_public_csv.zip \
  --resultados data/corrida0/CALC-SHED2025-BNPL-DANO-0001/resultados.json \
  --salida data/shed2025-bnpl-dano/control-independiente.json
```

## 5 · Contraste y límites

Las frecuencias del codebook coinciden con los controles de identidad (12,934
personas; 2,004 usuarios; 487 atrasos; 302 cargos; 542 respuestas BNPL1A;
206 positivas). No se usa esa tabulación como contraste de puntos porque son
frecuencias no ponderadas, no el mismo estimando poblacional ponderado.

No se producen EE/IC: `weight` acredita postestratificación y el punto, pero
no todo el diseño requerido para una varianza oficial. No se inventan UPM,
bootstrap de filas ni precisión. La descarga duplicada del HTML difirió sólo
en el token dinámico final de Cloudflare; se registra el hash de la primera
instantánea completa y el cuerpo del cuestionario fue idéntico.

## 6 · Uso para N34 y entrega a 40

La relación `REL-85fc542cc3c6ac0bb4b0d34c`, objeto
`OE-6eb9c3712c56d21187da0e70`, queda fortalecida con una medición real y
reproducible del mecanismo estadounidense. El paquete 40 puede consumir los
puntos exactos, universos, RESULT y ruta del cuestionario de esta nota; retiene
la conciliación general y el cierre global de `NC-0164`.

Esta entrega no infiere ninguna tasa mexicana, no adopta un parámetro, no
modifica tiers y no cierra `NC-0164`: siguen faltando BNPL/crédito digital o
lender identificable en México, CAT/tasa o fricción objetiva, daño, negativos
y estrategia causal.
