ENCARGO · ACTO GEN2-SPECS-DEMANDA-1
Recorre las 19 CORR sin candidato del registro GEN2: congela la spec ejecutable de las que se puedan, clasifica A.4 las que no

CABECERA · redactado contra `f5a5227` (merge de #771 — base verificada en el ARRANQUE, 0 commits detrás de `origin/main`) · ENTORNO: **NUBE** — sin `data/raw`, corpus NO montado; el acto abre SOLO codebook y metadato (E.5), microdato JAMÁS · COMPUERTA: ninguna · MODELO: Opus (juicio de medición: qué es construible y qué no) · Estado: VIVO · candidatos FP/ADR: deriva al cierre.
LANZAMIENTO, verbatim (mesa, 15/sep/2026): el texto de PIEZAS de abajo es el mensaje de lanzamiento tal como llegó; este archivo lo fija por A.3 porque llegó pegado en el mensaje que invocó `/acto`, no como archivo del repo.

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por el ejecutor contra `f5a5227` — el encargo llegó sin el bloque y A.8 manda pararse o contestarlo con comando, no suponerlo):

(1) ¿Existe ya la estructura? SÍ. `data/corrida0/demanda-corridas.tsv` y `demanda-resultados.tsv` (cabecera `# DERIVADO — NO EDITAR`, derivados por `tools/corrida0.py demanda`) gobiernan el dominio «demanda GEN2 por corrida»; `data/manifiesto.yaml` gobierna «qué payload tenemos»; `data/inventario-reactivos-v1_2.tsv`, `data/inventario-reactivos-descargas-mx-v1_2.tsv` y `data/inventario-reactivos-ext-v1_0.tsv` son los inventarios canónicos vigentes que A.15 exige citar; `forense/prereg-caja/` guarda las specs humanas selladas y `data/corrida0/CALC-*/spec.yaml` los contratos ejecutables. Ningún hueco de índice que reportar.

(2) ¿Existe ya el contenido? Parcialmente — y eso es entregable, no interrupción:
```
$ awk -F'\t' 'NR>2 && $4 ~ /SIN-CANDIDATO/' data/corrida0/demanda-corridas.tsv | wc -l
19
```
(la premisa del encargo se confirma: 19 de 82 corridas sin candidato). Y:
```
$ for n in 0001 … 0019; do grep -rl "CORR-$n" data/corrida0/*/spec.yaml forense/prereg-caja/; done
CORR-0002 → data/corrida0/CALC-ENCIG-0001/spec.yaml + forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md   [EXISTE-SATISFACE]
CORR-0003 → data/corrida0/CALC-ENCUCI-0001/spec.yaml + forense/prereg-caja/ENCUCI-MORDIDA-PROTESTA-spec-v1_0.md   [EXISTE-SATISFACE]
CORR-0007 → forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md (+ CORRECCIÓN 15/sep)   [EXISTE-NO-SATISFACE: cubre 2 de 8 RESULT]
CORR-0009 → data/corrida0/CALC-ENIF-0001/spec.yaml + forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md   [EXISTE-NO-SATISFACE: no releva RES-0031/0032/0065]
CORR-0013 → citado en data/corrida0/CALC-EDER-0001/spec.yaml con «NO se releva aquí»   [NO-ENCONTRADO como cobertura]
CORR-0017 → citado en ENIF-AHORRO-spec-v1_0.md solo para corregir un rótulo del encargo   [NO-ENCONTRADO como cobertura]
CORR-0001, 0004, 0005, 0006, 0008, 0010, 0011, 0012, 0014, 0015, 0016, 0018, 0019 → 0 aciertos   [NO-ENCONTRADO]
```
El encargo pide «recorrer las 19»: dos de ellas (`CORR-0002`, `CORR-0003`) ya están relevadas por una spec congelada y no se re-especifican — se asientan como ya cubiertas, que es lo que A.8 existe para no volver a pagar.

(3) ¿La estructura es posterior al trabajo? SÍ, y la brecha se declara: `demanda-corridas.tsv` nació el 7/sep/2026 (`tools/corrida0.py demanda`, GEN2); las conductas que puebla son de GEN1 (jul–sep/2026) y sus `script_legacy`/`spec_legacy` están vacíos **por construcción** — `SIN-CANDIDATO-EN-EL-REGISTRO` describe el registro legado, no el mundo. Que una corrida no tenga candidato ahí no implica que no exista una spec GEN2 posterior que la releve: la lista de (2) es exactamente ese cruce, y por eso se hace con comando y no de memoria.

PIEZAS (texto de mesa, verbatim)

> 1 · NUBE — ACTO GEN2-SPECS-DEMANDA-1 (Opus, integral, multi-día)
>
> Recorrer las 19 CORR sin candidato, en tandas por instrumento. Por cada una: A.8/A.15 contra los inventarios canónicos vigentes (¿el payload está en corpus? ¿los reactivos existen — verificados por archivo, secciones del codebook leídas del índice, no del nombre?), y entonces redactar y CONGELAR la spec ejecutable (md humana + spec.yaml, D-15, abriendo SOLO codebook y metadato — E.5 lo permite en nube, microdato jamás). Las que no se puedan: clasificación A.4 con bloqueador nombrado — payload faltante → cola/sobre, decisión → propuesta armada para tu firma (CORR-0001/ENCIG-2023 cae aquí: el acto te trae la decisión "adquirir vs. celda sin fuente" preparada, no pendiente). Entregable: N specs congeladas en COMMIT-1 + el mapa completo de las 19. Cada spec congelada es munición directa del encargo 2.

PERÍMETRO: `forense/encargos/2026-09-15-GEN2-SPECS-DEMANDA-1.md` (este archivo) · `forense/prereg-caja/` (specs humanas nuevas) · `data/corrida0/CALC-*/spec.yaml` (contratos ejecutables nuevos) · `data/corrida0/mapa-demanda-19-corr-v1_0.tsv` (el mapa de las 19) · `forense/notas/` (nota de cierre) · `forense/no-corrido.tsv` · `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_13.md`, `canon/registro-rotulos.tsv` (cascada). NO toca: `milpa/` (ningún consumidor cambia de cifra) · `data/manifiesto.yaml` · ningún CALC sellado · ningún microdato.

CONTADOR: **cero mediciones** — se dice en esta línea y no se disfraza (regla de señal v2.3). Un acto de specs congeladas produce contratos, no números: los números los produce la corrida en CAJA que consuma estos contratos.

LO QUE NO HACE: no corre ningún `CALC` · no abre un solo byte de microdato · no adopta ninguna cifra a ningún consumidor · no edita specs selladas (las sucede, si hiciera falta) · no decide por mesa ninguna de las adjudicaciones que arma.

CIERRE: cascada completa + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO` con el PR.
