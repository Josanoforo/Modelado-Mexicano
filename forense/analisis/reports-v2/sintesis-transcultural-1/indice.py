#!/usr/bin/env python3
"""Produce el índice C3 desde los 31 nombres v1 y tablas editoriales explícitas.

Los conteos son de registros editoriales, no de tesis independientes. Los
objetos remotos se leen por SHA; nunca se infiere fusión de un PR abierto.
"""
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
BASE = Path('forense/analisis/reports-v2')
MAIN_REMOTE = 'e584ee5fe0e3b782a048cc6bad2ce508563d6112'
PRS = {}
# Recibo de Claude por lote (GEN2-ASTRA-CONTINUIDAD-C3-1, P2): nota pr-N por PR fusionado.
RECIBOS = {
 'social-1': ('2026-09-27-GEN2-RECIBO-ASTRA6-2', 1171),
 'genero-violencia-salud-1': ('2026-09-27-GEN2-RECIBO-ASTRA6-2', 1180),
 'dinero-tecnologia-conocimiento-1': ('2026-09-27-GEN2-RECIBO-ASTRA6-2', 1196),
 'cuidado-migracion-pareja-1': ('2026-09-27-GEN2-RECIBO-ASTRA6-2', 1197),
 'autoridad-civismo-comunalidad-1': ('2026-09-27-GEN2-RECIBO-ASTRA6-3', 1240),
 'salud-juventud-tiempo-1': ('2026-09-27-GEN2-RECIBO-ASTRA6-3', 1242),
 'interaccion-emociones-humor-sancion-1': ('2026-09-27-GEN2-RECIBO-ASTRA6-3', 1243),
 'duelo-ambiguo-1': ('2026-09-28-GEN2-ASTRA-CONTINUIDAD-C3-1', 1246),
 'sintesis-transcultural-1': ('2026-09-28-GEN2-ASTRA-CONTINUIDAD-C3-1', 1247),
 'genetica-genomica-1': ('2026-09-28-GEN2-ASTRA-CONTINUIDAD-C3-1', 1251),
}
# consumo-familia-2 y trabajo-movilidad-1 se recibieron en RECIBO-ASTRA6-1 (nota única).
RECIBO_NOTA = {'consumo-familia-2': 'forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1', 'trabajo-movilidad-1': 'forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1'}
# Cada tupla: prefijo único de v1, tabla de decisiones, esquema, lote,
# estado en el corte local o PR. JSON de juicios sustituye tablas heredadas.
SOURCES = [
 ('Confianza_y_', 'social-1/confianza-afirmaciones.tsv', 'tsv', 'social-1', 0),
 ('Non-Family_', 'social-1/capital-afirmaciones.tsv', 'tsv', 'social-1', 0),
 ('Religiosidad_', 'social-1/religion-afirmaciones.tsv', 'tsv', 'social-1', 0),
 ('Psicología_del_Consumidor_', 'consumo-familia-2/consumo/consumo-juicios.json', 'juicios', 'consumo-familia-2', 0),
 ('La_familia_', 'consumo-familia-2/familia/familia-juicios.json', 'juicios', 'consumo-familia-2', 0),
 ('Psicología_del_Trabajo_', 'trabajo-movilidad-1/trabajo/afirmaciones.tsv', 'tsv', 'trabajo-movilidad-1', 0),
 ('Mérito__', 'trabajo-movilidad-1/movilidad/decisiones.tsv', 'tsv', 'trabajo-movilidad-1', 0),
 ('El_Clasemediero_', 'trabajo-movilidad-1/clase/afirmaciones.tsv', 'tsv', 'trabajo-movilidad-1', 0),
 ('Reconfiguración_', 'genero-violencia-salud-1/genero/tabla-afirmaciones.tsv', 'tsv', 'genero-violencia-salud-1', 0),
 ('El_Efecto_Ambiental_', 'genero-violencia-salud-1/violencia/tabla-afirmaciones.tsv', 'tsv', 'genero-violencia-salud-1', 0),
 ('Salud_Mental_', 'genero-violencia-salud-1/salud/tabla.tsv', 'tsv', 'genero-violencia-salud-1', 0),
 ('Behavioral_Finance_', 'dinero-tecnologia-conocimiento-1/dinero/afirmaciones.tsv', 'tsv', 'dinero-tecnologia-conocimiento-1', 0),
 ('Adopción_y_', 'dinero-tecnologia-conocimiento-1/tecnologia/afirmaciones.tsv', 'tsv', 'dinero-tecnologia-conocimiento-1', 0),
 ('Report_26__', 'dinero-tecnologia-conocimiento-1/conocimiento/tabla.tsv', 'tsv', 'dinero-tecnologia-conocimiento-1', 0),
 ('Vejez_y_', 'cuidado-migracion-pareja-1/vejez/tabla-afirmaciones.tsv', 'tsv', 'cuidado-migracion-pareja-1', 0),
 ('Psychology_of_Mexico-', 'cuidado-migracion-pareja-1/migracion/afirmaciones.tsv', 'tsv', 'cuidado-migracion-pareja-1', 0),
 ('Elegir__', 'cuidado-migracion-pareja-1/pareja/afirmaciones.tsv', 'tsv', 'cuidado-migracion-pareja-1', 0),
 ('Humor_in_', 'interaccion-emociones-humor-sancion-1/humor/tabla-afirmaciones.tsv', 'tsv', 'interaccion-emociones-humor-sancion-1', 0),
 ('La_arquitectura_', 'interaccion-emociones-humor-sancion-1/interaccion/tabla-afirmaciones.tsv', 'tsv', 'interaccion-emociones-humor-sancion-1', 0),
 ('Moral_Emotions_', 'interaccion-emociones-humor-sancion-1/moral/tabla-afirmaciones.tsv', 'tsv', 'interaccion-emociones-humor-sancion-1', 0),
 ('Sanción_Social_', 'interaccion-emociones-humor-sancion-1/sancion/tabla-afirmaciones.tsv', 'tsv', 'interaccion-emociones-humor-sancion-1', 0),
 ('Autoridad_y_', 'autoridad-civismo-comunalidad-1/autoridad/afirmaciones.tsv', 'tsv', 'autoridad-civismo-comunalidad-1', 0),
 ('Psicología_Política_', 'autoridad-civismo-comunalidad-1/civismo/afirmaciones.tsv', 'tsv_juicio', 'autoridad-civismo-comunalidad-1', 0),
 ('El_México_Rural_', 'autoridad-civismo-comunalidad-1/comunalidad/tabla-afirmaciones.tsv', 'tsv_v2', 'autoridad-civismo-comunalidad-1', 0),
 ('Health__', 'salud-juventud-tiempo-1/salud/afirmaciones.tsv', 'tsv', 'salud-juventud-tiempo-1', 0),
 ('Psicología_de_la_Juventud_', 'salud-juventud-tiempo-1/juventud/tabla.tsv', 'tsv_v2', 'salud-juventud-tiempo-1', 0),
 ('El_Mexicano_y_el_Tiempo_', 'salud-juventud-tiempo-1/tiempo/afirmaciones.tsv', 'tsv_v2', 'salud-juventud-tiempo-1', 0),
 ('Psicología__Conducta_y_', 'sintesis-transcultural-1/tabla-afirmaciones.tsv', 'tsv', 'sintesis-transcultural-1', 0),
 ('Ausencia_sin_certeza_', 'duelo-ambiguo-1/tabla-afirmaciones.tsv', 'tsv', 'duelo-ambiguo-1', 0),
 ('Genetica_y_Conducta_', 'genetica-genomica-1/tabla-afirmaciones.tsv', 'tsv_pieza:conducta', 'genetica-genomica-1', 0),
 ('Mexican_Population_Genomics_', 'genetica-genomica-1/tabla-afirmaciones.tsv', 'tsv_pieza:genomica', 'genetica-genomica-1', 0),
]
REPO = 'Josanoforo/Modelado-Mexicano'
VERDICTS = ('CONFIRMA', 'MATIZA', 'ROMPE', 'SIN-CIFRA')


def remote(path, ref):
    endpoint = f'repos/{REPO}/contents/{path}?ref={ref}'
    raw = subprocess.check_output(['gh', 'api', endpoint], text=True)
    return base64.b64decode(json.loads(raw)['content'])


def table_rows(raw, schema):
    if schema in ('tsv', 'tsv_v2', 'tsv_juicio'):
        return list(csv.DictReader(io.StringIO(raw.decode()), delimiter='\t'))
    if schema.startswith('tsv_pieza:'):
        pieza = schema.split(':', 1)[1]
        return [r for r in csv.DictReader(io.StringIO(raw.decode()), delimiter='\t') if r['pieza'] == pieza]
    if schema == 'juicios':
        return json.loads(raw)['juicios']
    raise ValueError(schema)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_local():
    """Comprueba el índice publicado y la pieza propia sin consultar GitHub."""
    out = ROOT / 'corpus/reports-v2/INDICE.md'
    content = out.read_text()
    lines = [line for line in content.splitlines() if line.startswith('| [')]
    originals = sorted((ROOT / 'corpus/reports').glob('*.md'))
    assert len(lines) == len(originals) == 31
    for original in originals:
        relevant = [line for line in lines if f'](../reports/{original.name})' in line]
        assert len(relevant) == 1, original.name
        assert f'`{sha(original.read_bytes())}`' in relevant[0], original.name
    assert sum('| EN-MAIN |' in line for line in lines) == 31
    assert not any('| — |' in line.split('| EN-MAIN |')[1][:6] for line in lines if '| EN-MAIN |' in line)
    own = next(line for line in lines if 'Psicología__Conducta_y_Sociedad' in line)
    own_table = ROOT / BASE / 'sintesis-transcultural-1/tabla-afirmaciones.tsv'
    rows = table_rows(own_table.read_bytes(), 'tsv')
    counts = [sum(row['dictamen'] == verdict for row in rows) for verdict in VERDICTS]
    assert counts == [2, 61, 22, 20], counts
    assert '28 / 77' in own and '2 / 61 / 22 / 20' in own
    missing = [link for link in re.findall(r'\]\(([^)]+)\)', content)
               if not link.startswith('http') and not (out.parent / link).exists()]
    assert not missing, missing
    print('VERDE local: 31 originales/hashes, 31 main, recibo por fila; '
          'tabla síntesis 2/61/22/20; enlaces locales válidos')


def main():
    originals = sorted((ROOT / 'corpus/reports').glob('*.md'))
    assert len(originals) == 31, len(originals)
    committed = set(subprocess.check_output(
        ['git', 'ls-tree', '-r', '-z', '--name-only', 'HEAD', 'corpus/reports-v2'],
        cwd=ROOT).decode().split('\0'))
    main_committed = set(subprocess.check_output(
        ['git', 'ls-tree', '-r', '-z', '--name-only', MAIN_REMOTE, 'corpus/reports-v2'],
        cwd=ROOT).decode().split('\0'))
    local_count = sum(f'corpus/reports-v2/{p.name}' in main_committed for p in originals)
    mapa_path = ROOT / 'canon/mapa-dominios-v1_1.tsv'
    mapa = list(csv.DictReader(mapa_path.open(), delimiter='\t'))
    mapa_by_report = {}
    for row in mapa:
        mapa_by_report.setdefault(row['report'], set()).add(row['id_afirmacion'])
    config = {}
    for prefix, table, schema, lot, ref in SOURCES:
        matches = [p for p in originals if p.name.startswith(prefix)]
        assert len(matches) == 1, (prefix, matches)
        config[matches[0].name] = (table, schema, lot, ref)
    assert len(config) == 31
    lines = [
        '# Índice de los 31 reports v1 y sus sucesores v2', '',
        f'Corte consolidado de main: `{MAIN_REMOTE}` ({local_count} homónimos fusionados). '
        'Regenerado por GEN2-ASTRA-CONTINUIDAD-C3-1 (P2); la nota del corte anterior '
        '(`a8c3e341`, 24 homónimos) no se reescribe: vive en la historia de este archivo. '
        '31/31 homónimos fusionados es cobertura editorial, no cierre científico.', '',
        f'Fuente del cruce: [mapa v1.1](../../canon/mapa-dominios-v1_1.tsv), '
        f'SHA-256 `{sha(mapa_path.read_bytes())}`. La huella de cada original '
        'abajo es SHA-256 completo de sus bytes y coincide con `report_sha256` del mapa.', '',
        'Los cuatro números de dictamen cuentan **registros editoriales** de las tablas '
        'enlazadas, que pueden desdoblar o reiterar afirmaciones. No son estudios, '
        'mediciones ni tesis independientes. «Mapa» indica filas del mapa vigente '
        'correspondientes al v1; «adicional» registra la diferencia entre registros '
        'editoriales y filas del mapa solo como volumen documental, **no** como '
        'conteo de afirmaciones fuera del mapa. Para cobertura exacta consúltese la '
        'tabla y la cobertura de cada lote. «—» significa tabla aún no entregada.', '',
        '| Original v1 · SHA-256 | Homónimo v2 | Mapa / adicional¹ | C / M / R / S | Estado del archivo | Recibo de Claude | Regla propuesta | Regla adoptada | Reserva material |',
        '|---|---|---:|---:|---|---|---|---|---|',
    ]
    totals = {'EN-MAIN': 0, 'EN-PR': 0, 'EN-PR-PROPIO': 0, 'NO-ENTREGADO': 0}
    for p in originals:
        name = p.name
        rel1 = f'../reports/{name}'
        digest = sha(p.read_bytes())
        map_ids = mapa_by_report.get(f'corpus/reports/{name}', set())
        assert map_ids and all(r['report_sha256'] == digest for r in mapa
                               if r['report'] == f'corpus/reports/{name}'), name
        if name in config:
            table, schema, lot, ref = config[name]
            table_path = str(BASE / table)
            if ref == 0 or ref == 'own':
                raw = (ROOT / table_path).read_bytes()
                table_link = f'../../{table_path}'
                v2_link = name
                receipt = f'../../{BASE / lot / "recibo-para-claude.md"}'
                status = 'EN-MAIN' if ref == 0 else 'EN-PR-PROPIO'
            else:
                branch_sha = MAIN_REMOTE if ref == 'remote' else PRS[ref]
                raw = remote(table_path, branch_sha)
                table_link = f'https://github.com/{REPO}/blob/{branch_sha}/{table_path}'
                v2_link = (name if f'corpus/reports-v2/{name}' in committed and ref == 'remote'
                           else f'https://github.com/{REPO}/blob/{branch_sha}/corpus/reports-v2/{name}')
                receipt = f'https://github.com/{REPO}/blob/{branch_sha}/{BASE / lot / "recibo-para-claude.md"}'
                status = 'EN-MAIN' if ref == 'remote' else 'EN-PR'
            rows = table_rows(raw, schema)
            key = {'tsv': 'dictamen', 'tsv_v2': 'dictamen_v2',
                   'tsv_juicio': 'juicio_v2', 'juicios': 'dictamen'}.get(schema, 'dictamen')
            counts = {v: sum(row.get(key) == v for row in rows) for v in VERDICTS}
            assert sum(counts.values()) == len(rows), (name, counts, len(rows), list(rows[0]) if rows else [])
            audit = f'{len(map_ids)} / {max(0, len(rows)-len(map_ids))} [tabla]({table_link})'
            verdict = ' / '.join(str(counts[v]) for v in VERDICTS)
            status_link = (status if status == 'EN-MAIN' else
                           f'EN-PR-PROPIO [#1247](https://github.com/{REPO}/pull/1247)' if ref == 'own' else
                           f'[EN-PR #{ref}](https://github.com/{REPO}/pull/{ref})')
            if lot in RECIBOS:
                carpeta, pr = RECIBOS[lot]
                receipt_link = f'[pr-{pr}](../../forense/notas/{carpeta}/pr-{pr}.md)'
            else:
                receipt_link = f'[RECIBO-ASTRA6-1](../../{RECIBO_NOTA[lot]}/)'
            proposal = ('[hoja C3](../../forense/analisis/reports-v2/reglas-propuestas-v1_0.tsv)' if ref == 0 else
                        f'[lote](../../{BASE / lot}/)' if ref == 0 else
                        f'[lote](https://github.com/{REPO}/tree/{MAIN_REMOTE if ref == "remote" else PRS[ref]}/{BASE / lot})')
            reserve = f'{counts["SIN-CIFRA"]} registros SIN-CIFRA; ver razones y límites en tabla.'
            reserve += ' Módulo [v2.16] y firewall: bloque C3-V216 del report.'
        else:
            status = 'NO-ENTREGADO'
            v2_link = None
            audit = f'{len(map_ids)} / —'
            verdict = '— / — / — / —'
            status_link = status
            receipt_link = '—'
            proposal = '—'
            reserve = ('Firewall genético: no usar genómica como inferencia conductual.'
                       if name.startswith(('Genetica_', 'Mexican_Population_')) else
                       'Falta homónimo, tabla y recibo; conclusión aún no dictaminada.')
        totals[status] += 1
        successor = f'[v2]({v2_link})' if v2_link else '—'
        lines.append(f'| [{p.stem.replace("_", " ")}]({rel1})<br>`{digest}` | '
                     f'{successor} | {audit} | {verdict} | {status_link} | '
                     f'{receipt_link} | {proposal} | No acreditada aquí | {reserve} |')
    assert totals == {'EN-MAIN': 31, 'EN-PR': 0, 'EN-PR-PROPIO': 0,
                      'NO-ENTREGADO': 0}, totals
    lines += ['', '¹ El índice muestra filas del mapa por identidad de archivo, no una '
              'fracción de cobertura editorial comprobada. El exceso de registros '
              'sobre filas del mapa mezcla desdoblamientos, reiteraciones y '
              'afirmaciones adicionales; no debe sumarse como hallazgos nuevos.', '',
              f'**Estado verificable:** {totals["EN-MAIN"]}/31 en main al corte; '
              f'{totals["NO-ENTREGADO"]}/31 sin entrega. Cada fila enlaza el recibo de Claude '
              'de su PR (post-merge en #1240, #1242, #1243, #1246, #1247, #1251). '
              'Ninguna regla editorial se declara adoptada por aparecer en una tabla '
              'o por fusionarse un report. C3 completo exige los 31 homónimos '
              'fusionados, recibidos y sus controles.', '',
              '**Idioma (firma R52, GEN2-TRAMITE-FIRMAS-21):** el report de '
              'genómica (Mexican Population Genomics 2025-2026) se acepta en '
              'inglés en v2; se traduce en v3.', '',
              '**Receta de actualización:** ejecutar `python3 '
              'forense/analisis/reports-v2/sintesis-transcultural-1/indice.py` '
              'tras actualizar los SHAs de main/PR verificados y las fuentes de '
              'los tres pendientes. `python3 '
              'forense/analisis/reports-v2/sintesis-transcultural-1/indice.py '
              '--verify` comprueba el índice local sin red. Revisar el diff antes de publicar; la '
              'herramienta detiene la generación si cambia el universo o un '
              'esquema de dictamen.', '']
    out = ROOT / 'corpus/reports-v2/INDICE.md'
    out.write_text('\n'.join(lines))
    print(f'{out.relative_to(ROOT)}: {len(originals)} filas; {totals}')


if __name__ == '__main__':
    if sys.argv[1:] == ['--verify']:
        verify_local()
    elif len(sys.argv) == 1:
        main()
    else:
        raise SystemExit('Uso: indice.py [--verify]')
