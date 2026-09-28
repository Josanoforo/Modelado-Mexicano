#!/usr/bin/env python3
"""Cierre editorial C3 (GEN2-ASTRA-CONTINUIDAD-C3-1, P2): añade a cada report v2
el bloque del módulo de auditoría con las dos preguntas [v2.16] y el firewall
genético. Deriva, por report, los RESULT citados y su CALC/unidad desde los
sellos (data/corrida0/CALC-*/resultados.json + spec.yaml). No toca el cuerpo
del report: solo añade (o reemplaza) el bloque entre marcadores. Idempotente.

Uso: bloque_v216.py [--escribe]   (sin --escribe solo reporta; D-23)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
V2 = ROOT / 'corpus/reports-v2'
INI = '<!-- C3-V216:INICIO (GEN2-ASTRA-CONTINUIDAD-C3-1; generado por forense/analisis/reports-v2/continuidad-c3-1/bloque_v216.py) -->'
FIN = '<!-- C3-V216:FIN -->'
RX = re.compile(r'RESULT-[A-Z0-9][A-Z0-9_.+/-]*[A-Z0-9+]')


def indice_result():
    idx = {}
    for rj in sorted((ROOT / 'data/corrida0').glob('CALC-*/resultados.json')):
        try:
            d = json.loads(rj.read_text())
        except Exception:
            continue
        res = d.get('resultados', d) if isinstance(d, dict) else {}
        if not isinstance(res, dict):
            continue
        spec = rj.parent / 'spec.yaml'
        uni = 'no declarada en su spec.yaml como persona/hogar/delito/trámite: se lee en el CALC'
        if spec.exists():
            for m in re.finditer(r'^\s*unidad\w*:\s*(.+)$', spec.read_text(), re.M):
                v = m.group(1).strip().strip('"\'')
                if re.search(r'PERSONA|HOGAR|VIVIENDA|DELITO|TR[AÁ]MITE|INDIVIDUO', v, re.I):
                    uni = v
                    break
        for k in res:
            idx[k] = (rj.parent.name, uni)
    return idx


def bloque(ids, idx):
    hall = [(i, *idx[i]) for i in ids if i in idx]
    fal = [i for i in ids if i not in idx]
    calcs = {}
    for _, c, u in hall:
        calcs.setdefault(c, u)
    L = [INI, '', '## Módulo de auditoría · preguntas [v2.16] y firewall genético (cierre editorial C3)', '',
         '**¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA, y se mezclan en alguna frase?** '
         'Ninguna cifra de este report es PROSPECTIVA: ninguna fue emitida y sellada antes de '
         'existir la referencia contra la que se lee. Toda cifra aquí es RETROSPECTIVA '
         '(lectura de una ola ya vista o de una fuente publicada); ninguna frase mezcla las dos columnas.', '']
    if calcs:
        L.append(f'**¿Qué unidad tiene cada cifra y se promedia con otra?** Las cifras con `RESULT-` citado '
                 f'({len(hall)} ids, {len(calcs)} CALC sellados) llevan la unidad que declara su spec:')
        for c, u in sorted(calcs.items()):
            L.append(f'- `{c}` → unidad: {u}')
        L.append('Ninguna cantidad de unidad delito o trámite se promedia aquí con una de unidad persona u hogar.')
    else:
        L.append('**¿Qué unidad tiene cada cifra y se promedia con otra?** Este report no cita ningún '
                 '`RESULT-` sellado; sus cifras son externas y su unidad es la de la fuente citada '
                 '(persona, hogar, delito o trámite según la encuesta). No se promedian cantidades de unidades distintas.')
    if fal:
        L.append(f'Ids `RESULT-` citados sin sello localizable por este generador: {len(fal)} '
                 f'(p. ej. `{fal[0]}`); se leen como cifra sin sellado.')
    L += ['',
          '**Procedencia de cifras sin RESULT.** Toda cifra de este report que no cite un `RESULT-` '
          'sellado es **cifra sin sellado: no entra al canon**; su procedencia se clasifica como '
          '(a) dato primario en México, (b) muestra mexicano-americana o de diáspora (no es evidencia '
          'sobre México) o (c) marco teórico importado en la tabla de afirmaciones del expediente, '
          'enlazada desde `corpus/reports-v2/INDICE.md`.', '',
          '**Firewall genético (§3).** Prohibida la inferencia ascendencia → conducta de grupo. Nada en '
          'este report autoriza segmentar por ascendencia, origen étnico o componente genético; la única '
          'vía admitida es individual, molecular y de efecto pequeño (p. ej. alcohol, nicotina), nunca como segmentación.',
          '', FIN]
    return '\n'.join(L) + '\n'


def main():
    escribe = sys.argv[1:] == ['--escribe']
    idx = indice_result()
    n = 0
    for f in sorted(V2.glob('*.md')):
        if f.name == 'INDICE.md':
            continue
        t = f.read_text()
        if INI in t:
            t = t[:t.index(INI)].rstrip('\n') + '\n'
        cuerpo = t
        ids = sorted(set(RX.findall(cuerpo)))
        nuevo = cuerpo.rstrip('\n') + '\n\n' + bloque(ids, idx)
        hall = sum(i in idx for i in ids)
        print(f'{hall}/{len(ids)}\t{f.name[:60]}')
        if escribe and nuevo != f.read_text():
            f.write_text(nuevo)
        n += 1
    print(f'reports={n} escribe={escribe}')


if __name__ == '__main__':
    main()
