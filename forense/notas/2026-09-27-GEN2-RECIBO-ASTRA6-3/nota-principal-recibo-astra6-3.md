# Nota principal · ACTO GEN2-RECIBO-ASTRA6-3 · recibo de diez PR de Codex (7 post-merge + 3 pre-merge previstos)

Siete PR de P1 (#1221, #1222, #1226, #1229, #1232, #1237, #1243) se fusionaron sin recibo de Claude, en incumplimiento de FIRMAS-20 D. De los tres de P2, uno (#1240) se fusionó a mitad del recibo y pasó a post-merge. Quedan dos pre-merge: #1241 y #1242.

- Encargo: `forense/encargos/2026-09-27-GEN2-RECIBO-ASTRA6-3.md` (0-bis `8c5c8bc3`, sello de cuerpo `8232ad17…`). SHA de redacción `3ac3ab7d`, igual a la base al abrir. Al cerrar, origin/main está en `32b0d413` y se fusionó en la rama. Entorno NUBE, cero microdato.
- ADR: `ADR-260928-GEN2-RECIBO-ASTRA6-3-8c5c-01`. Modo AUTÓNOMO-AMPLIO. Lotes D-11, uno por subagente: A (#1241) · B (#1240, #1242) · C (#1221, #1229, #1222) · D (#1243, #1226, #1232, #1237). Todo va en un solo PR de recibo.
- Commits recibidos en las ramas abiertas: #1241 = `86d9ece7`; #1242 = `58bd0f71`. La rama de #1242 avanzó desde `f003edc6` con una corrección documental: mesa debe fusionar `58bd0f71` o re-pedir recibo.
- Fuera de universo: #1246 (`codex/astra6-c3-duelo-ambiguo-1`) se abrió después del 0-bis y además fusionó sin recibo (`32b0d413`). Va a RECIBO-ASTRA6-4.
- Conteos de archivos distintos a los del encargo: #1240 tiene 39, no 37, y #1242 tiene 35, no 32. Las dos ramas se movieron; está declarado en sus notas.

## Veredictos (EJECUTADO: `grep -h '^VEREDICTO' pr-*.md | sort | uniq -c` → 3 RECIBIDO-POST-MERGE · 5 RECIBIDO-POST-MERGE-CON-NC · 2 RECIBIDO-CON-NC)

| PR | modo | carril | rutas sensibles | veredicto | NC (sufijo 8c5c-NN) |
|---|---|---|---|---|---|
| #1241 | PRE | C1 ejecutor v3 | 0 | RECIBIDO-CON-NC | 01–03 |
| #1242 | PRE | C3 salud/juventud/tiempo | 0 | RECIBIDO-CON-NC | 06–07 |
| #1240 | POST (fusionó a mitad, `a8c3e341`) | C3 autoridad/civismo/comunalidad | 0 | RECIBIDO-POST-MERGE-CON-NC | 04–05 |
| #1221 | POST | C1 aislamiento v2 | 0 | RECIBIDO-POST-MERGE-CON-NC | 10 |
| #1229 | POST | C1 entradas residuales | 1: falso positivo (`p2/residuales-p2-decisiones.tsv`, no el archivo de decisiones de mesa) | RECIBIDO-POST-MERGE-CON-NC | 11–12 |
| #1222 | POST | C2 ENOE inferencia | 0 | RECIBIDO-POST-MERGE-CON-NC | 13 |
| #1243 | POST | C3 interacción/emociones/humor/sanción | 0 | RECIBIDO-POST-MERGE-CON-NC | 08–09 |
| #1226 | POST | tubería adq | 0 | RECIBIDO-POST-MERGE | — |
| #1232 | POST | revisión tanda 4 | 0 | RECIBIDO-POST-MERGE | — |
| #1237 | POST | archivo tanda 5 | 0 | RECIBIDO-POST-MERGE | — |

**PROPONER-REVERTIR: 0.** Ningún PR escribe en sellos, catálogo, `decisiones.tsv`, `milpa/`, tabla de piso, vistas, `verify.yml` ni `check.py`.

## Hallazgos que pesan
- **#1241 (C1):** ningún recálculo sin paquete archivado previo, porque no hay recálculo real: solo corridas sintéticas. El contrato v3 (`ea302f89`) precede al ejecutor y al comparador. El broker sigue sin provisionar, así que no se puede acreditar ceguera. Las pruebas fijan Python 3.14.4, y aquí dan 2 ERROR.
- **#1221 (C1):** es preparación, no una sesión ciega. `probe` da NO-LANZAR-COMO-CIEGA en los dos entornos.
- **#1229:** resuelve el hallazgo de pr-1214 de ASTRA6-2: la fuente 01 casa por sha. Pero la archivó fuera de la carpeta de la tanda 4.
- **#1222 (C2):** ninguna ola reservada. `enoe_2026_1t_microdatos` existe (`yq`), así que 2024T4 no es la más reciente. Receta antes del recálculo; cero retadores (regla 6).
- **C3 (#1240, #1242, #1243):** v1 sin diff. Muestra de 10 con semilla 20260928: 10/10 por forma; la fuente externa es NO-VERIFICABLE-AQUÍ (sin red). Faltas editoriales: firewall genético y preguntas [v2.16] en #1240, y firewall en Juventud en #1242.
- **A.12:** #1241 y #1243 abren decisiones de mesa en prosa sin fila FP (NC 02 y 09).

## P3 · Hoja para mesa
`forense/analisis/recibo-astra6-3/hoja-para-mesa-recibo-astra6-3.md` (renombrada desde `hoja-para-mesa.md` del encargo: T02 colisiona por nombre normalizado): 5 FP nuevas y 3 decisiones sin id, una línea de dictamen por cada una. La asienta FIRMAS-21.

## CONTADOR
Cero mediciones y cero adopciones. `validaciones-independientes.tsv`: sin filas nuevas, porque ningún lote recalculó contra un RESULT.
