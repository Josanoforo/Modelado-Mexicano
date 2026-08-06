#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ENCARGO ÍNDICE-2. Conecta el índice huérfano de la Descarga Masiva del
5/ago (data/indice-descarga-masiva-2026-08-05.tsv, 7,930 URLs, artefacto
fechado que nadie consume) con el índice de las 5 canastas de hoy
(data/indice-canastas-2026-08-08.tsv) y con el sistema de reconciliación
que ya existe (tests/catalogo.py -> data/catalogo_derivado.json). Tres
funciones, nada más: universo unido, en_manifiesto refrescado contra el
manifiesto VIVO (no el valor congelado del TSV), cruce contra el catálogo.
Deriva e imprime; no escribe canon, no escribe manifiesto, no es compuerta
de CI."""
import csv, os, re, subprocess, sys, unicodedata
import yaml

RAIZ = os.environ.get('MM_RAIZ') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RAIZ, 'data')
IDX_5AGO = os.path.join(DATA, 'indice-descarga-masiva-2026-08-05.tsv')
IDX_CANASTAS = os.path.join(DATA, 'indice-canastas-2026-08-08.tsv')
MANIFIESTO = os.path.join(DATA, 'manifiesto.yaml')
ALIAS = os.path.join(DATA, 'inventarios', 'alias-fuentes.yaml')
MAPA_FUENTES = os.path.join(DATA, 'mapa-fuentes-2026-08-06.tsv')

for p in (IDX_5AGO, IDX_CANASTAS, MANIFIESTO, ALIAS):
    if not os.path.isfile(p):
        sys.exit(f"NO ENCONTRÉ {p} — este script se corre desde un clon del repo con los "
                  f"dos índices y el manifiesto en su sitio, o con MM_RAIZ apuntando a la raíz.")


def carga_indices():
    """Une los dos TSV. Cada fila queda etiquetada con su origen literal —
    nunca se funde la procedencia de una URL."""
    filas = []
    with open(IDX_5AGO, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            r['_origen'] = 'indice-2026-08-05'
            r['canasta'] = r.get('canasta') or 'descarga_masiva_5ago'
            filas.append(r)
    with open(IDX_CANASTAS, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            r['_origen'] = 'indice-canastas-2026-08-08'
            filas.append(r)
    return filas


# ============================================================
# FUNCIÓN 1 — universo unido
# ============================================================
def universo(filas):
    print("=" * 70)
    print("FUNCIÓN 1 · UNIVERSO UNIDO")
    print("=" * 70)
    n_5ago = sum(1 for r in filas if r['_origen'] == 'indice-2026-08-05')
    n_canastas = sum(1 for r in filas if r['_origen'] == 'indice-canastas-2026-08-08')
    print(f"filas indice-2026-08-05:        {n_5ago}")
    print(f"filas indice-canastas-2026-08-08: {n_canastas}")
    print(f"filas totales (con repetición):  {len(filas)}")

    por_url = {}
    for r in filas:
        por_url.setdefault(r['url'], []).append(r)
    unicas = len(por_url)
    solapadas = sum(1 for v in por_url.values() if len(v) > 1)
    print(f"\nURLs únicas en la unión:         {unicas}")
    print(f"URLs que aparecen en más de un índice/canasta: {solapadas}")
    if solapadas:
        ejemplo = next(u for u, v in por_url.items() if len(v) > 1)
        canastas_ej = sorted({v2['canasta'] for v2 in por_url[ejemplo]})
        print(f"  ejemplo: {ejemplo}  -> {canastas_ej}")

    print("\npor canasta (raw, sin deduplicar entre sí):")
    cont_canasta = {}
    for r in filas:
        cont_canasta[r['canasta']] = cont_canasta.get(r['canasta'], 0) + 1
    for k, v in sorted(cont_canasta.items(), key=lambda x: -x[1]):
        print(f"  {v:6d}  {k}")

    progs = {}
    for r in filas:
        p = (r.get('programa') or '').strip()
        progs[p] = progs.get(p, 0) + 1
    print(f"\nprogramas distintos (incluye '' = fuera de /programas/): {len(progs)}")
    print(f"URLs con programa vacío (canastas masiva/, investigacion/, etc.): {progs.get('', 0)}")

    return por_url


# ============================================================
# FUNCIÓN 2 — refresca en_manifiesto contra el manifiesto VIVO
# ============================================================
def refresca_manifiesto(por_url):
    print("\n" + "=" * 70)
    print("FUNCIÓN 2 · en_manifiesto REFRESCADO (manifiesto vivo, no el TSV congelado)")
    print("=" * 70)
    manifiesto = yaml.safe_load(open(MANIFIESTO, encoding='utf-8'))
    urls_manifiesto = {e['url_origen'] for e in manifiesto if e.get('url_origen')}
    archivos_manifiesto = {e['archivo'] for e in manifiesto if e.get('archivo')}
    print(f"entradas en manifiesto vivo: {len(manifiesto)}  "
          f"(url_origen únicos: {len(urls_manifiesto)}, archivo únicos: {len(archivos_manifiesto)})")

    urls = list(por_url.keys())
    match_url = sum(1 for u in urls if u in urls_manifiesto)
    print(f"\nCIFRA 1 — emparejamiento por URL EXACTA: {match_url} / {len(urls)}")

    def nombre(u):
        return u.rsplit('/', 1)[-1]

    match_nombre = sum(1 for u in urls if nombre(u) in archivos_manifiesto)
    print(f"CIFRA 2 — emparejamiento por NOMBRE DE ARCHIVO (no se colapsa con la 1): "
          f"{match_nombre} / {len(urls)}")
    solo_por_nombre = sum(1 for u in urls if nombre(u) in archivos_manifiesto and u not in urls_manifiesto)
    print(f"  de esos, cuántos NO tenían ya match por URL exacta (ganancia atribuible "
          f"solo al nombre, el emparejamiento que el proyecto ya pagó como defecto): {solo_por_nombre}")
    print("  ambas cifras se reportan aparte; ninguna reemplaza a la otra.")
    return match_url, match_nombre


# ============================================================
# FUNCIÓN 3 — cruce contra el catálogo unificado
# ============================================================
def cruza_catalogo(por_url):
    print("\n" + "=" * 70)
    print("FUNCIÓN 3 · CRUCE CONTRA EL CATÁLOGO UNIFICADO")
    print("=" * 70)
    print("regenerando data/catalogo_derivado.json (corriendo tests/catalogo.py)...")
    r = subprocess.run([sys.executable, os.path.join(RAIZ, 'tests', 'catalogo.py')],
                        cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"tests/catalogo.py falló (returncode={r.returncode}):\n{r.stderr}")
    print("  ok — catalogo.py corrió limpio, catalogo_derivado.json regenerado.")

    alias = yaml.safe_load(open(ALIAS, encoding='utf-8')) or []
    slug_a_canon = {e['slug_portal']: e['canonico'] for e in alias if e.get('slug_portal')}
    print(f"\nfuentes canónicas con slug_portal verificado (data/inventarios/alias-fuentes.yaml): "
          f"{len(slug_a_canon)} de {len(alias)}")

    # -- verificación de receta contra un caso de respuesta conocida --
    # el propio encargo cita la cifra de mesa: mapa-fuentes-2026-08-06.tsv
    # suma 3,754 en n_urls_portal. Se re-deriva aquí por dos caminos
    # independientes y se compara contra ese valor conocido antes de
    # confiar en el resto del cruce.
    mapa = list(csv.DictReader(open(MAPA_FUENTES, newline='', encoding='utf-8'), delimiter='\t'))
    suma_mapa = sum(int(r['n_urls_portal']) for r in mapa if r['n_urls_portal'].strip())
    filas_5ago = [r for u, vs in por_url.items() for r in vs if r['_origen'] == 'indice-2026-08-05']
    suma_propia = sum(1 for r in filas_5ago if (r.get('programa') or '').strip().lower() in slug_a_canon)
    print(f"\nVERIFICACIÓN DE RECETA contra caso conocido:")
    print(f"  mapa-fuentes-2026-08-06.tsv, suma de n_urls_portal:            {suma_mapa}")
    print(f"  re-derivado aquí (URLs del índice 5/ago cuyo programa cae en un slug_portal): {suma_propia}")
    if suma_mapa == suma_propia:
        print("  COINCIDEN. La receta es consistente — la cifra de mesa no estaba mal contada.")
        print("  Respuesta a la pregunta del encargo: el mapa cubre menos de la mitad porque "
              f"solo {len(slug_a_canon)}/{len(alias)} fuentes canónicas tienen slug_portal asignado "
              "(ENCARGO MAP-1 solo lo verificó donde el slug coincidía Y el contenido corroboraba "
              "— no por falta de aritmética), no porque la suma esté mal.")
    else:
        print("  NO COINCIDEN — la receta de este script diverge de la cifra citada. "
              "No se reporta la respuesta a la pregunta del encargo hasta resolver esto.")

    urls = list(por_url.keys())
    cubiertas = 0
    no_cubiertas = 0
    programas_no_explicados = {}
    for u, filas in por_url.items():
        rep = filas[0]
        programa = (rep.get('programa') or '').strip().lower()
        canasta = rep.get('canasta') or ''
        if programa in slug_a_canon:
            cubiertas += 1
        else:
            no_cubiertas += 1
            clave = programa if programa else f"(sin programa; canasta={canasta})"
            programas_no_explicados[clave] = programas_no_explicados.get(clave, 0) + 1

    print(f"\nURLs del índice unido bajo una fuente canónica del catálogo: {cubiertas} / {len(urls)}")
    print(f"URLs del índice unido que ninguna fuente canónica explica:   {no_cubiertas} / {len(urls)}")
    print(f"\nprogramas/canastas del índice que ninguna fuente del catálogo explica "
          f"({len(programas_no_explicados)} claves distintas, top 25 por volumen de URLs):")
    for k, v in sorted(programas_no_explicados.items(), key=lambda x: -x[1])[:25]:
        print(f"  {v:6d}  {k}")
    print("\n  (este es el conjunto de puertas que el catálogo no conoce — no se decide aquí "
          "si merecen entrar, solo se nombran)")
    return cubiertas, no_cubiertas, programas_no_explicados


def main():
    filas = carga_indices()
    por_url = universo(filas)
    refresca_manifiesto(por_url)
    cruza_catalogo(por_url)


if __name__ == '__main__':
    main()
