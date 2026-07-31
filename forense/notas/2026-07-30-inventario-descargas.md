# Inventario de descargas — 30/jul/2026

Nota forense pura: registra lo que hay en disco, no lo que hay dentro de los
archivos. No abre ningún payload salvo los dos ya registrados (comparación
de hash, que no abre el contenido). **Cero entradas nuevas en
`data/manifiesto.yaml`** — ver punto 6 sobre por qué los 24 de ENSANUT
quedan fuera de este PR.

Ubicación de los 32 archivos: `/mnt/c/Users/PC0/Descargas MX/` (lado Windows
del WSL, fuera del repo — mismo patrón que `data/raw/`, que tampoco se
versiona). No hay copia de estos archivos dentro del working tree de git.

---

## 1 · Los 32 archivos: nombre, tamaño, sha256, fecha de modificación en disco

sha256 y tamaño calculados directamente sobre el archivo en disco
(`sha256sum`, `stat`) el 30/jul/2026. La fecha de modificación es la que
reporta el filesystem (hora local, UTC-6), no una fecha declarada por nadie.

| archivo | bytes | sha256 | mtime en disco |
|---|---|---|---|
| `1 VFINAL Cuestionario Hogar ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | 662210 | `adc873843b79067a1a2212e25b1f90f6ecb916f8541ad0e42411fd933126c425` | 2026-07-30 11:18:48 |
| `2 VFINAL Cuestionario nios 0 a 9 ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | 518103 | `af65f922094c42a31d77cad5d8d889c0d7e597b925c7ef0efe1ae700fd66981c` | 2026-07-30 11:20:02 |
| `3 VFINAL Cuestionario adolescentes ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | 479013 | `344f32ef0f873f86fb20faf1d6afd2bfa0bc3735656ea4fe4d71e39736faeeab` | 2026-07-30 11:20:21 |
| `4 VFINAL Cuestionario adultos ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | 795644 | `0bc30c3b7f08bda0b1cfebb823eb2bfdd815581fd1d93ea956314bf6507f82d0` | 2026-07-30 11:20:28 |
| `5 VFINAL Cuestionario utilizadores ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | 267996 | `004aacee3729009e79065ba7e2c4afacfc7f7c3e418e735c405f46e9189fafa6` | 2026-07-30 11:20:34 |
| `BD_ENCUCI2020_dbf.zip` | 6913684 | `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` | 2026-07-30 10:51:49 |
| `DescargaMasiva_3072026_105543.zip` | 602155 | `cbcd416a843f0a17419fb4c5be64800540c37dc2b575c69862a87f16de04e0d6` | 2026-07-30 10:55:45 |
| `DescargaMasiva_3072026_10560.zip` | 602154 | `a68da0e08403c2083a161491a908a36ae340c1a13db545bb22383577e6d0a7e9` | 2026-07-30 10:56:03 |
| `DescargaMasiva_3072026_105617.zip` | 602150 | `4ab75449ed7bc6e3576d3da6c85f81fcb8c2a462ccfdacc75e3761f8840f5240` | 2026-07-30 10:56:19 |
| `DescargaMasiva_3072026_105625.zip` | 602154 | `b7af09f37e8215d9a092825b4f4ecdde4bae65a6f3fc5ec8f40086b61a245bfb` | 2026-07-30 10:56:26 |
| `DescargaMasiva_3072026_10567.zip` | 602152 | `e913e542b6f08fee3192d3881891e5a0163cd715d1d321b38d108dbda9aa2b25` | 2026-07-30 10:56:08 |
| `FD_ENCUCI2020.pdf` | 1758249 | `6cd6f7475a0b5db27a84cf0e047db5b7ed98f73c3480a9e64ea084bc7d475638` | 2026-07-30 10:51:59 |
| `Indice de Bienestar.Cuestionarios.docx` | 13255 | `6913725196ae2a3b52f11a1d8d3d650336a13840ad5279daecce0d89048d93f5` | 2026-07-30 11:19:56 |
| `NSE_Hogar_ENSANUT_2024.Catlogo.xlsx` | 137855 | `ed1be4e10d76b065f2c6ad67e4ab3fb9f5af3ce5d5877aea28ffe4382f5ccc1a` | 2026-07-30 11:20:42 |
| `NSE_Hogar_ENSANUT_2024.csv.csv.zip` | 83570 | `685e33d003ca100b06501c377de13abce8f56b46b3705f7a6fa0effaf4db28af` | 2026-07-30 11:19:46 |
| `NSE_Integrantes_ENSANUT_2024.Catlogo.xlsx` | 138387 | `6d2425ad899ab5beaa9c4ea016d9cadebb17ae4827fa847090b5c32ebc7bf8b0` | 2026-07-30 11:20:43 |
| `NSE_Integrantes_ENSANUT_2024.csv.csv.zip` | 256745 | `0315bc625b262ec14f818c4b3858a387a022911e527af059ac3c6923f46e6ff0` | 2026-07-30 11:19:47 |
| `adolescentes_ensanut2024_w.csv.csv.zip` | 416868 | `3c5f21ef6158ea0830cabc750ca31b45e0039b04fa93b9b9236b0fe6457d023b` | 2026-07-30 11:19:51 |
| `adolescentes_ensanut2024_w.stata.stata.zip` | 798929 | `b528e00511ad931f2fda973c344299a73d245c11502d867cb9666f7c33824260` | 2026-07-30 11:19:30 |
| `adultos_ensanut2024_w.Catlogo.csv.csv.zip` | 234627 | `464a62daf5e9b0f991a500791e58eb4d2c5ec255acabd59f74ad67d71520ab7a` | 2026-07-30 11:19:53 |
| `adultos_ensanut2024_w.Catlogo.xlsx` | 247551 | `0ab22b7f0c3515d966e60634d6e06543a14f2839cda32e3e49895749d419df4c` | 2026-07-30 11:20:46 |
| `descargas.php` | 141181 | `361ac35fa637933ba245bf1fa328cf62bd6cd80d61bf613cf0b431755a1cef10` | 2026-07-30 11:19:34 |
| `hogar_ensanut2024_w_ICB.Catlogo.xlsx` | 162227 | `b5b9792e92287091a89e57f13f13a4b89aab4b27a060c4ea7e1cd375041716fd` | 2026-07-30 11:20:39 |
| `hogar_ensanut2024_w_ICB.csv.csv.zip` | 996094 | `fb27bb64c3fbd2344ff8966ad69c4675d2c0a0f86b87225b0c6899bc8b2b4212` | 2026-07-30 11:19:39 |
| `integrantes_ensanut2024_w_ICB.Catlogo.xlsx` | 197249 | `d0acf24dd918f07c4462ade607171933a2756f4ff6a2fa8fff64193ea4566448` | 2026-07-30 11:20:41 |
| `integrantes_ensanut2024_w_ICB.csv.csv.zip` | 1858331 | `1dc1277b38b131a5768acffc6679aa30f3c873be5fd695c61da93e126d2f07da` | 2026-07-30 11:19:40 |
| `menores_ensanut2024_w.Catlogo.xlsx` | 197357 | `2aa89c4b97ecf310e96f4c6ab9b23388194353c30f3bba371b5aad0f71c660a6` | 2026-07-30 11:20:44 |
| `menores_ensanut2024_w.csv.csv.zip` | 617777 | `df07aa31dfc8838869d098d9e128a9800262cc713218a4e470bed35cbd88809f` | 2026-07-30 11:19:49 |
| `menores_ensanut2024_w.stata.stata.zip` | 1133030 | `cadf52a7127a6feeb2b37b4b299c96ab559e1eb78c1ee7022db58618ff0442bb` | 2026-07-30 11:19:28 |
| `utilizadores_ensanut2024_w.Catlogo.xlsx` | 153149 | `81928f1d470126174e135df17749cfa82e3ef43fffe7ee7568ccb0752ef3ed3e` | 2026-07-30 11:20:47 |
| `utilizadores_ensanut2024_w.csv.csv.zip` | 284328 | `2836f15464e01ebbd42e282cac1b2bf18cf98c2262e360c346c5ebd6cfae27ea` | 2026-07-30 11:19:54 |
| `utilizadores_ensanut2024_w.stata.stata.zip` | 424623 | `1fb44754452e5cbf8d8b195385cd4b052cde80b4784ac38193527682f8ceb482` | 2026-07-30 11:19:34 |

Total: 32 archivos. Ningún contenido fue abierto para producir esta tabla,
salvo la lectura de hash de los dos ya registrados (punto 2, abajo).

---

## 2 · `BD_ENCUCI2020_dbf.zip` y `FD_ENCUCI2020.pdf` — comparación contra manifiesto

Ambos ya tienen entrada en `data/manifiesto.yaml` de `origin/main`
(`encuci2020_bd_dbf`, `encuci2020_fd_pdf`; no están en `sesion/calg3-fasec`,
que es la rama detrás de la que partió esta sesión — ver nota al final).

| archivo | sha256 en disco | sha256 en manifiesto | resultado |
|---|---|---|---|
| `BD_ENCUCI2020_dbf.zip` | `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` | `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` | **coincide — ya registrado** |
| `FD_ENCUCI2020.pdf` | `6cd6f7475a0b5db27a84cf0e047db5b7ed98f73c3480a9e64ea084bc7d475638` | `6cd6f7475a0b5db27a84cf0e047db5b7ed98f73c3480a9e64ea084bc7d475638` | **coincide — ya registrado** |

Tamaño en bytes también coincide en ambos casos (6,913,684 y 1,758,249) con
lo que declara el manifiesto. Ningún hallazgo aquí: no se toca la entrada
existente, no se abre el archivo.

---

## 3 · `DescargaMasiva_3072026_*.zip` (5 archivos) — contenido: no identificado

No se abrieron. Nombre, tamaño y sha256 quedan en la tabla del punto 1. No
hay procedencia (URL, fecha de descarga, quién los bajó) más allá de lo que
el nombre del archivo sugiere (una exportación con timestamp del 30/jul/2026
entre 10:55 y 10:56). No entran al manifiesto en este PR.

---

## 4 · `descargas.php` — evidencia de procedencia, no payload

`descargas.php` (141,181 bytes) es una página de descarga guardada, no un
dato. Se deja registrada aquí como evidencia de la sesión de descarga (mismo
directorio, mismo bloque horario 11:19 que los archivos de ENSANUT). No
entra al manifiesto: no es un insumo de dato, es rastro de procedencia.

---

## 5 · Los 24 archivos de ENSANUT 2024 — quedan fuera de este PR

Lista (nombre exacto en la tabla del punto 1): los 5 `VFINAL Cuestionario
*.pdf`, `Indice de Bienestar.Cuestionarios.docx`, los 2 `NSE_Hogar_*` y 2
`NSE_Integrantes_*` (`.Catlogo.xlsx` + `.csv.csv.zip`), y los archivos de
`adolescentes`, `adultos`, `hogar_ICB`, `integrantes_ICB`, `menores` y
`utilizadores` (`.Catlogo.xlsx`/`.Catlogo.csv.csv.zip` y/o
`.csv.csv.zip`/`.stata.stata.zip` según el caso) — 24 en total.

**Por qué no entran todavía:** el esquema de `data/manifiesto.yaml` exige
`url_origen`, `fecha_descarga` y `descargado_por`, y ninguno de los tres es
derivable del archivo en disco — solo quien hizo la descarga los tiene.
"Confirmado en memoria" no es procedencia; es justamente la clase de cifra
que la Regla de oro / v2.1 de `instrucciones-proyecto-v2.md` prohíbe usar
como si fuera dato verificado. Nombre, tamaño, sha256 y mtime ya quedaron
capturados en el punto 1 — eso es lo único que se perdía si nadie lo
escribía hoy. Quedan listos para un segundo pase de registro en cuanto el
autor dé la procedencia de cada uno.

---

## 6 · `sesion/encuci` — ¿reserva el dominio ENCUCI?

Verificado: `sesion/encuci` **sí tiene push** — `git rev-parse
sesion/encuci` y `git rev-parse origin/sesion/encuci` coinciden en
`dcbf6ece15a49d609ed955c09f575f6090a7c082`. No es una rama local huérfana;
existe en `origin` y ya trae consigo el registro de
`encuci2020_bd_dbf`/`encuci2020_fd_pdf` que después llegó a `main` (PR #8,
ADR-46). No hay nada que anotar como riesgo aquí más allá de esto: la rama
está publicada, no reserva un "dominio" en ningún sentido especial, y este
inventario no depende de ella.

---

## Nota sobre la rama de origen de este PR

`sesion/calg3-fasec` — la rama activa en el working tree compartido al
momento de recibir esta instrucción — tiene trabajo en curso ajeno a esta
nota (Fase C de CAL-G3: `forense/hitoD-preregistro-v2_0.md` modificado,
`tests/calg3_fasec.py`, `forense/notas/2026-07-30-calg3-fasec-salida.txt`,
más dos archivos vacíos sin explicación clara — `anota`, `es`). Ese trabajo
no es de esta sesión y no se tocó. Esta nota se preparó en un worktree
aislado, rama `sesion/inventario-descargas`, partiendo de `origin/main`
(commit `fae0191`), precisamente para no interferir con esa rama compartida.
