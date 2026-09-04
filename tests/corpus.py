#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/corpus.py — archivo -> entrada: el hueco que ningún test cubría.

`tests/manifiesto.py --verifica` comprueba la dirección entrada -> archivo:
para cada entrada del manifiesto con payload, recomputa sha256/tamaño del
archivo que declara. Nada comprobaba la dirección inversa, archivo ->
entrada. Ese es el defecto de PR #77: seis payloads quedaron en un
data/raw local sin entrada de manifiesto y nadie lo notó en dos actos.
El encargo de DESC-1 (2026-08-05, PR #142) declaró explícitamente que
ese defecto "no lo atrapa ningún test". Este script existe para que deje
de ser cierto.

Tres comprobaciones, todas dirigidas por data/manifiesto.yaml:

  C1 · HUÉRFANO             archivo bajo data/raw que ninguna entrada
                             declara.
  C2 · DUPLICADO POR CONTENIDO  dos entradas con el mismo sha256 bajo ids
                             distintos. Se lee del YAML, no del disco.
  C3 · ENTRADA SIN ARCHIVO   entrada cuyo archivo/raíz no resuelve.
                             Solapa con `manifiesto.py --verifica` (que
                             reporta esto como AUSENTE): se reporta aquí
                             también, declarado como solape, no como
                             hallazgo nuevo. La diferencia es de mecanismo,
                             no de cobertura -- C3 solo comprueba
                             existencia (os.path.exists), --verifica además
                             rehashea para detectar contenido corrupto o
                             cambiado; ninguna de las dos cuenta aparte.

LÍMITE DECLARADO DE C1 (ADDENDUM TC-1, 2026-08-06), textual:
    C1 no ve las raíces no integradas. Un resultado limpio de C1 no
    significa corpus sin huérfanos: significa data_raw sin huérfanos.
C1 barre únicamente la raíz `data_raw` (repo/data/raw/, integrada por
código). NO ve `descargas_mx` ni ninguna otra raíz declarada en
data/raices.local.yaml (gitignorado, por máquina) -- por ejemplo, la
carpeta Windows Downloads/Descargas MX donde DESC-1 encontró la canasta
nacional correcta. Un archivo huérfano bajo esas raíces es invisible
para C1 tal como está escrito. Precedente: T20 (tests/check.py) declara
igual de explícito que "no ve sitios sin marca" -- un test con límite
escrito vale; uno que aparenta cubrir todo y no lo hace, no.

ENMIENDA (ACTO INV-DESCMX, 2026-08-13): el límite de arriba ya NO aplica
tal cual -- queda como registro histórico del defecto que motivó su
escritura, no como descripción del código vigente. C1 ahora barre TODAS
las raíces que `M.raices_configuradas()` declare (más RAIZ_INTEGRADA),
cada una emparejada solo contra las entradas que declaran esa misma
`raiz` -- un archivo bajo `descargas_mx` ya no se da por cubierto porque
exista una entrada con ese contenido bajo `data_raw` (duplicado físico
entre raíces, no lo mismo que "cubierto"; ver C2 para duplicados por
contenido dentro del manifiesto). Excepción deliberada, no reintroduce
el defecto: sobre raíces en `M.RAICES_QUE_EXIGEN_GRUPO` (`downloads`),
el barrido se acota a `M.EXTENSIONES_DATO_RAICES_NO_CURADAS` -- mismo
filtro que MAP-1b aplicó a mano y que --escanea ya reusa, no uno nuevo
-- y el reporte da solo la CUENTA, nunca nombres: esa raíz es el
destino por defecto del navegador, no una carpeta curada del proyecto
(`descargas_mx` sí lo es y no lleva filtro ni redacción de nombres,
ver ENCARGO INV-DESCMX §0(a)/(b)). Un huérfano de `downloads` sigue
siendo un hecho sobre la tabla, no una lista de nombres personales en
un commit permanente.

ENMIENDA 2 (FP-259(iii), MAESTRA37-INFRA-2, 2026-09-03): la ENMIENDA de
arriba (2026-08-13) dejaba "duplicado físico entre raíces" y "contenido
nunca registrado" en una sola lista plana de huérfanos, sin distinguirlos.
Ya no: C1 ahora SÍ hashea (M.sha256_de), pero solo el subconjunto de
archivos que ya falló la comprobación por ruta declarada (rel not in
declarados) -- un archivo cuya ruta relativa SÍ está en `declarados` para
esa raíz nunca se abre; no se rehashea el árbol completo. Ese sha256 se
compara contra `_indice_por_sha_y_raiz(entradas)`, el índice de TODAS las
entradas ya cargadas en memoria (sin I/O nuevo: `entradas` ya viene de
`cargar()`). Cada huérfano se reclasifica en dos categorías:

  · presente_bajo_otra_raiz  el sha256 SÍ está registrado, bajo una
                              declaración de `raiz` DISTINTA a la que se
                              está barriendo ahora -- duplicado físico
                              entre raíces, tal como ya decía la ENMIENDA
                              de 2026-08-13, ahora con nombre y raíz
                              declarante citables en vez de quedar
                              disuelto dentro de "huérfano" sin más.
  · sin_registro              todo lo demás: ningún sha256 igual en el
                              manifiesto, O el único sha256 igual está
                              declarado bajo la MISMA raíz que se está
                              barriendo. Este segundo caso (duplicado
                              DENTRO de la misma raíz) es a propósito
                              `sin_registro`, NUNCA `presente_bajo_otra_raiz`:
                              que dos copias físicas convivan en la misma
                              raíz no dice que ESTE archivo/ruta esté
                              declarado -- `presente_bajo_otra_raiz`
                              responde "¿este contenido ya vive en OTRA
                              raíz registrada?", no "¿existe en algún lado
                              un gemelo de este contenido?". Confirmado
                              contra el corpus real de este repo: 3 casos
                              (ADQ15_OMCA_conflictos_agua/omca_consulta.html.2a,
                              ennvih_diseno/calculo-de-factores-de-expansion.pdf,
                              eder2025/889463930242.pdf) tienen sha256 ya
                              registrado bajo `data_raw` -- la MISMA raíz en
                              la que el propio archivo huérfano vive -- y
                              quedan `sin_registro`, no
                              `presente_bajo_otra_raiz`. El total C1 (suma
                              de ambas categorías) es numéricamente idéntico
                              al que la versión anterior (lista plana)
                              reportaba: esta ENMIENDA reclasifica, no
                              recuenta.

Las tres comprobaciones emiten WARN; ninguna emite FAIL. Decisión de
diseño central de este script (ENCARGO TC-1, 2026-08-05/06): un hallazgo
del corpus no debe poder gatear el push de un acto ajeno -- CONF-17 quedó
detenido una vez por carpetas que no creó y un bug que no introdujo, y
cualquier redacción de C1/C2/C3 que emitiera FAIL reproduciría exactamente
ese modo de falla para el próximo acto que toque data/raw.

Este script es independiente de tests/check.py: no importa check.py, no
participa en su cuenta de FAIL/WARN, no lee ni escribe tests/baseline.json,
no tiene --freeze. Reusa exclusivamente las funciones de resolución de
tests/manifiesto.py (repo_root, rutas, leer_manifiesto, resolver_raiz,
RAIZ_INTEGRADA) -- lectura pura, sin efectos secundarios.

Uso: python3 tests/corpus.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M  # noqa: E402


def cargar(root):
    manifiesto_path, raw_dir = M.rutas(root)
    _, entradas = M.leer_manifiesto(manifiesto_path)
    return entradas, raw_dir


def _indice_por_sha_y_raiz(entradas):
    """{sha256: [(entrada, raiz_declarada), ...]} sobre TODAS las entradas
    con payload ya cargadas en memoria -- sin I/O nuevo, `entradas` ya viene
    de `cargar()`. `raiz_declarada` sigue la misma convención que el resto
    de este módulo y de manifiesto.py: `entrada.get("raiz", M.RAIZ_INTEGRADA)`
    (raíz ausente = data_raw). Usado por c1_huerfanos() para distinguir
    'presente_bajo_otra_raiz' de 'sin_registro' -- ver ENMIENDA 2 en la
    cabecera de este archivo."""
    indice = {}
    for e in entradas:
        sha = e.get("sha256")
        if not sha:
            continue
        raiz_declarada = e.get("raiz", M.RAIZ_INTEGRADA)
        indice.setdefault(sha, []).append((e, raiz_declarada))
    return indice


def c1_huerfanos(root, entradas, raw_dir):
    """Archivo bajo una raíz configurada que ninguna entrada del manifiesto
    declara PARA ESA RAÍZ, reclasificado por contenido (sha256) en dos
    categorías -- ver ENMIENDA 2 en la cabecera de este archivo.

    Barre RAIZ_INTEGRADA (data_raw) más todo lo que M.raices_configuradas()
    devuelva (descargas_mx, downloads -- lo que este entorno tenga en
    data/raices.local.yaml). Cada raíz se compara primero por RUTA contra
    las entradas que declaran esa raíz (`raiz` ausente = data_raw por
    convención); un archivo cuya ruta relativa ya está declarada para esa
    raíz nunca se hashea (no es candidato, no hay I/O nuevo para el caso ya
    cubierto). Solo el resto -- ruta no declarada para esta raíz -- se
    hashea (M.sha256_de) y se busca en `_indice_por_sha_y_raiz(entradas)`:

      · presente_bajo_otra_raiz  si algún entry con ese sha256 declara una
                                  `raiz` DISTINTA a `nombre_raiz` (la raíz
                                  que se está barriendo). Duplicado físico
                                  entre raíces: el contenido SÍ está en el
                                  manifiesto, bajo otra raíz.
      · sin_registro              en cualquier otro caso -- incluido el caso
                                  en que el único entry con ese sha256
                                  declara la MISMA raíz que se está
                                  barriendo (duplicado DENTRO de la misma
                                  raíz: no cuenta como 'presente_bajo_otra_
                                  raiz', la ENMIENDA 2 existe exactamente
                                  para no confundir ambos casos). Cuando
                                  aplica este sub-caso se anota (no cambia
                                  el conteo/bucket) con
                                  'sin_registro_pero_duplica_contenido_de(<id>)'.

    Sobre raíces en M.RAICES_QUE_EXIGEN_GRUPO se acota por extensión con
    M.EXTENSIONES_DATO_RAICES_NO_CURADAS (mismo filtro que --escanea, no
    reinventado) -- ver ENMIENDA 2026-08-13 en la cabecera de este archivo;
    ese filtro se aplica IDÉNTICO a ambas sublistas (acota qué se camina,
    antes de clasificar -- eso no cambió).

    Devuelve {nombre_raiz: {"presente_bajo_otra_raiz": [(rel, [otras_raices]), ...],
                             "sin_registro": [(rel, anotacion_o_None), ...]}}
    con ambas sublistas ordenadas por `rel`.
    """
    raices = {M.RAIZ_INTEGRADA: raw_dir}
    raices.update(M.raices_configuradas(root))
    indice_sha = _indice_por_sha_y_raiz(entradas)

    resultado = {}
    for nombre_raiz, ruta_raiz in raices.items():
        declarados = set()
        for e in entradas:
            if "sha256" not in e:
                continue
            if e.get("raiz", M.RAIZ_INTEGRADA) != nombre_raiz:
                continue
            archivo = e.get("archivo")
            if not archivo:
                continue
            declarados.add(os.path.normpath(archivo))

        acotar_extension = nombre_raiz in M.RAICES_QUE_EXIGEN_GRUPO
        presente_bajo_otra_raiz = []
        sin_registro = []
        if ruta_raiz and os.path.isdir(ruta_raiz):
            for dirpath, _dirnames, filenames in os.walk(ruta_raiz):
                for fn in filenames:
                    if acotar_extension:
                        ext = os.path.splitext(fn)[1].lower()
                        if ext not in M.EXTENSIONES_DATO_RAICES_NO_CURADAS:
                            continue
                    ruta_abs = os.path.join(dirpath, fn)
                    rel = os.path.normpath(os.path.relpath(ruta_abs, ruta_raiz))
                    if rel in declarados:
                        continue

                    sha_real = M.sha256_de(ruta_abs)
                    coincidencias = indice_sha.get(sha_real, [])
                    otras_raices = sorted({r for (_e, r) in coincidencias if r != nombre_raiz})
                    if otras_raices:
                        presente_bajo_otra_raiz.append((rel, otras_raices))
                    else:
                        mismas_raiz = [e.get("id", "?") for (e, r) in coincidencias if r == nombre_raiz]
                        anotacion = (
                            f"sin_registro_pero_duplica_contenido_de({mismas_raiz[0]})"
                            if mismas_raiz else None
                        )
                        sin_registro.append((rel, anotacion))
        resultado[nombre_raiz] = {
            "presente_bajo_otra_raiz": sorted(presente_bajo_otra_raiz, key=lambda t: t[0]),
            "sin_registro": sorted(sin_registro, key=lambda t: t[0]),
        }
    return resultado


def c2_duplicados_por_contenido(entradas):
    """Dos entradas del manifiesto con el mismo sha256 bajo ids distintos.
    Puramente sobre el YAML ya cargado -- no toca disco."""
    por_hash = {}
    for e in entradas:
        sha = e.get("sha256")
        if not sha:
            continue
        por_hash.setdefault(sha, []).append(e.get("id", "?"))
    return {sha: sorted(ids) for sha, ids in por_hash.items() if len(ids) > 1}


def c3_entradas_sin_archivo(root, entradas, raw_dir):
    """Entrada cuyo archivo/raíz no resuelve. Solapa con --verifica (AUSENTE);
    igual que --verifica, una raíz no configurada en esta máquina se omite
    -- 'no configurada' no es el mismo hecho que 'archivo ausente'."""
    sin_archivo = []
    for e in entradas:
        if "sha256" not in e:
            continue
        archivo = e.get("archivo")
        if not archivo:
            continue
        nombre_raiz = e.get("raiz", M.RAIZ_INTEGRADA)
        base_dir = M.resolver_raiz(nombre_raiz, root, raw_dir)
        if base_dir is None:
            continue
        ruta = os.path.join(base_dir, archivo)
        if not os.path.exists(ruta):
            sin_archivo.append((e.get("id", "?"), nombre_raiz, archivo))
    return sin_archivo


def distribucion_raices(entradas):
    """Cuántas entradas declaran cada raíz, y cuántas no declaran ninguna
    (ausente = data_raw por convención) -- crudo, sin resolver nada."""
    con_payload = [e for e in entradas if "sha256" in e]
    conteo = {}
    sin_campo = 0
    for e in con_payload:
        r = e.get("raiz")
        if r is None:
            sin_campo += 1
        else:
            conteo[r] = conteo.get(r, 0) + 1
    return con_payload, conteo, sin_campo


def main():
    root = M.repo_root()
    entradas, raw_dir = cargar(root)

    print("=" * 76)
    print("  CORPUS: archivo -> entrada (complemento de manifiesto.py --verifica)")
    print("=" * 76)

    con_payload, conteo_raices, sin_campo = distribucion_raices(entradas)
    print(f"  manifiesto: {len(entradas)} entradas totales, "
          f"{len(con_payload)} con payload (sha256)")
    partes = [f"{nombre}={n}" for nombre, n in sorted(conteo_raices.items())]
    partes.append(f"SIN CAMPO raiz (=data_raw por convención)={sin_campo}")
    print("  por raíz, tal cual declarado: " + " · ".join(partes))
    print(f"  raíces visibles a C1 (RAIZ_INTEGRADA + configuradas en "
          f"data/raices.local.yaml): {M.RAIZ_INTEGRADA}, "
          f"{', '.join(sorted(M.raices_configuradas(root))) or '(ninguna configurada en esta máquina)'}")
    print()

    warn_total = 0

    huerfanos_por_raiz = c1_huerfanos(root, entradas, raw_dir)
    total_huerfanos = sum(
        len(v["presente_bajo_otra_raiz"]) + len(v["sin_registro"])
        for v in huerfanos_por_raiz.values()
    )
    etiqueta = f"[warn]  C1 huérfanos  ({total_huerfanos} warn)" if total_huerfanos \
        else "[ ok ]  C1 huérfanos"
    print("  " + etiqueta + "  -- alcance: todas las raíces configuradas, ver ENMIENDA en cabecera")
    for nombre_raiz in sorted(huerfanos_por_raiz):
        clasif = huerfanos_por_raiz[nombre_raiz]
        otra_raiz = clasif["presente_bajo_otra_raiz"]
        sin_registro = clasif["sin_registro"]
        if not otra_raiz and not sin_registro:
            continue
        if nombre_raiz in M.RAICES_QUE_EXIGEN_GRUPO:
            # ENMIENDA 2026-08-13: raíz no curada -- solo CUENTA, nunca nombres.
            print(f"    · [{nombre_raiz}]: {len(otra_raiz)} presente(s) bajo otra raíz · "
                  f"{len(sin_registro)} sin registro -- solo cuenta, sin nombres "
                  f"(raíz no curada, ver ENMIENDA 2026-08-13)")
        else:
            for rel, otras in otra_raiz:
                print(f"    · [{nombre_raiz}] {rel} -- presente bajo otra raíz "
                      f"({' · '.join(otras)})")
            for rel, anotacion in sin_registro:
                sufijo = f" -- {anotacion}" if anotacion else ""
                print(f"    · [{nombre_raiz}] {rel} -- ningún id del manifiesto lo "
                      f"declara para esta raíz (sin_registro){sufijo}")
            print(f"    · [{nombre_raiz}]: {len(otra_raiz)} presente(s) bajo otra raíz · "
                  f"{len(sin_registro)} sin registro")
    warn_total += total_huerfanos

    dups = c2_duplicados_por_contenido(entradas)
    print(f"  [warn]  C2 duplicado por contenido  ({len(dups)} warn)" if dups
          else "  [ ok ]  C2 duplicado por contenido")
    for sha, ids in sorted(dups.items()):
        print(f"    · sha256 {sha[:16]}... bajo ids distintos: {' · '.join(ids)}")
    warn_total += len(dups)

    sin_archivo = c3_entradas_sin_archivo(root, entradas, raw_dir)
    print(f"  [warn]  C3 entrada sin archivo  ({len(sin_archivo)} warn, "
          f"solapa con manifiesto.py --verifica)" if sin_archivo
          else "  [ ok ]  C3 entrada sin archivo")
    for id_, nombre_raiz, archivo in sin_archivo:
        print(f"    · {id_} [{nombre_raiz}]: {archivo} no resuelve "
              f"(mismo hecho que AUSENTE en --verifica)")
    warn_total += len(sin_archivo)

    print()
    print(f"  {warn_total} WARN  (C1={total_huerfanos} · C2={len(dups)} · "
          f"C3={len(sin_archivo)})")
    print("  Ninguna comprobación de este script emite FAIL: no gatea nada,")
    print("  no toca tests/baseline.json, no tiene --freeze.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
