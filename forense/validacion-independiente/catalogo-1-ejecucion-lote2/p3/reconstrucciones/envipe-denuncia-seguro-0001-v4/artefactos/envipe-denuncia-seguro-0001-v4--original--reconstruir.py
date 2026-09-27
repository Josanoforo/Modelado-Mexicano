#!/usr/bin/env python3
"""Reconstrucción independiente; sólo entradas preservadas y payloads declarados."""
import csv
import hashlib
import io
import json
import platform
from pathlib import Path
import sys
import zipfile
import numpy as np

BASE = Path(__file__).resolve().parent
ENTRADA = BASE / 'entrada'
RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/raw')
MIEMBRO = 'tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def guardar(nombre, objeto):
    (BASE / nombre).write_text(json.dumps(objeto, ensure_ascii=False, indent=2) + '\n')

def main():
    manifest_bytes = (ENTRADA / 'manifiesto.json').read_bytes()
    manifiesto = json.loads(manifest_bytes)
    entradas = []
    for nombre, esperado in manifiesto['archivos'].items():
        contenido = (ENTRADA / nombre).read_bytes()
        observado = sha(contenido)
        if observado != esperado:
            raise ValueError(f'Entrada alterada: {nombre}')
        entradas.append(dict(archivo=nombre, sha256=observado, bytes=len(contenido)))
    tolerancia = json.loads((ENTRADA / 'tolerancia.json').read_text())
    assert tolerancia['tipo'] == 'flotante' and tolerancia['abs'] >= 0
    texto = (ENTRADA / 'estimandos.tsv').read_text()
    escapado = '\t' not in texto and r'\t' in texto
    if escapado:
        # Decodificación limitada a separadores; no unicode_escape sobre texto UTF-8.
        texto = texto.replace(r'\r\n', '\n').replace(r'\t', '\t')
    estimandos = list(csv.DictReader(io.StringIO(texto), delimiter='\t'))
    inventario = []
    errores = []
    for insumo in json.loads((ENTRADA / 'insumos.json').read_text()):
        ruta = RAW / insumo['id'] / insumo['archivo']
        ficha = dict(insumo, ruta=str(ruta))
        try:
            contenido = ruta.read_bytes()
            ficha.update(sha256_observado=sha(contenido), bytes=len(contenido))
            ficha['verificacion'] = 'COINCIDE' if sha(contenido) == insumo['sha256'] else 'NO-COINCIDE'
            if ficha['verificacion'] != 'COINCIDE':
                errores.append(f"Hash distinto: {insumo['id']}")
        except OSError as exc:
            ficha['verificacion'] = 'BLOQUEADO-POR-ACCESO'
            errores.append(f"Sin acceso a {ruta}: {exc}")
        inventario.append(ficha)
    guardar('inventario_insumos.json', inventario)
    recibo = dict(manifiesto_sha256=sha(manifest_bytes), entradas=entradas,
                  resultados_esperados_accedidos=False, revelacion_solicitada=False,
                  estimandos_separadores_escapados=escapado,
                  python=platform.python_version(), numpy=np.__version__,
                  tolerancia=tolerancia)
    guardar('recibo.json', recibo)
    campos = ['llave','calc','result_id','estado','motivo','unidad','estimacion',
              'ee','ic_025','ic_975','naturaleza_ic','n','numerador','denominador']
    salida = []
    # Asignaciones literales de la tabla de metodo.md; no inferencia de códigos.
    identidades = {
        'RESULT-ENVIPE-SEG-CON-P-DENUNCIA': ('1','1'),
        'RESULT-ENVIPE-SEG-CON-P-NO-DENUNCIA': ('1','2'),
        'RESULT-ENVIPE-SEG-SIN-P-DENUNCIA': ('2','1'),
        'RESULT-ENVIPE-SEG-SIN-P-NO-DENUNCIA': ('2','2'),
    }
    if not errores:
        with zipfile.ZipFile(RAW / 'envipe2025_csv/envipe2025_csv.zip') as z:
            guardar('inventario_zip.json', [dict(entrada=i.filename, bytes=i.file_size,
                                               crc32=f'{i.CRC:08x}') for i in z.infolist()])
            contenido = z.read(MIEMBRO)
        lector = csv.DictReader(io.StringIO(contenido.decode('utf-8-sig'), newline=''))
        requeridos = {'BPCOD','BP2_1','BP1_20','FAC_DEL','EST_DIS','UPM_DIS'}
        if not requeridos <= set(lector.fieldnames):
            raise ValueError(f'Faltan nombres literales: {requeridos - set(lector.fieldnames)}')
        datos = list(lector)
        dominio = [r for r in datos if r['BPCOD'] == '01']
        # Diseño sobre el dominio de delitos 01, antes de separar cobertura.
        grupos = {}
        for r in dominio:
            h,u = r['EST_DIS'],r['UPM_DIS']
            if not h or not u:
                raise ValueError('Llave de diseño vacía')
            grupos.setdefault(h, {}).setdefault(u, np.zeros(6, dtype=np.float64))
            w = int(r['FAC_DEL'])
            if w <= 0:
                raise ValueError('FAC_DEL no positivo')
            if r['BP2_1'] in ('1','2'):
                j = 0 if r['BP2_1'] == '1' else 3
                grupos[h][u][j] += w
                if r['BP1_20'] == '1':
                    grupos[h][u][j+1] += w
                elif r['BP1_20'] == '2':
                    grupos[h][u][j+2] += w
        matrices = [np.array([grupos[h][u] for u in sorted(grupos[h])]) for h in sorted(grupos)]
        totales = sum((m.sum(axis=0) for m in matrices), np.zeros(6))
        rng = np.random.Generator(np.random.PCG64(20260915))
        replicas = np.zeros((2000,6))
        # Orden fijo: réplica, estrato textual, UPM textual; m_h sorteos por estrato.
        for b in range(2000):
            for m in matrices:
                replicas[b] += m[rng.integers(0,len(m),size=len(m))].sum(axis=0)
        if np.any(replicas[:,[0,3]] == 0):
            raise ValueError('Réplica con denominador cero; no se omite silenciosamente')
        proporciones = replicas[:,[1,2,4,5]] / replicas[:,[0,0,3,3]]
        unica = sum(len(m) == 1 for m in matrices)
        naturaleza = 'IC-CON-ESTRATOS-DE-UPM-UNICA' if unica else 'IC-BOOTSTRAP-PERCENTIL'
        # Control independiente, usando ambos numeradores contados.
        sumas = [(totales[j+1]+totales[j+2])/totales[j] for j in (0,3)]
        guardar('diagnostico.json', dict(miembro=MIEMBRO, miembro_sha256=sha(contenido),
                filas_archivo=len(datos), filas_dominio=len(dominio),
                filas_cobertura_no_1_2=sum(r['BP2_1'] not in ('1','2') for r in dominio),
                estratos=len(matrices), upm=sum(len(m) for m in matrices),
                estratos_upm_unica=unica, replicas=2000,
                sumas_probabilidades=sumas,
                control_suma_uno=[bool(abs(s-1)<=tolerancia['abs']) for s in sumas],
                replicas_denominador_cero=0))
        with (BASE / 'replicas.tsv').open('w') as f:
            escritor = csv.writer(f, delimiter='\t', lineterminator='\n')
            escritor.writerow(['replica'] + list(identidades))
            for b,p in enumerate(proporciones,1):
                escritor.writerow([b] + [format(x,'.17g') for x in p])
    for e in estimandos:
        fila = {k:e[k] for k in ('llave','calc','result_id')}
        if errores:
            fila.update(estado='BLOQUEADO-POR-ACCESO', motivo='; '.join(errores))
        elif e['llave'] not in identidades or e['result_id'] != e['llave']:
            fila.update(estado='NO-RECALCULABLE-DESDE-SPEC', motivo='Identidad no especificada literalmente')
        else:
            cobertura, desenlace = identidades[e['llave']]
            j = 0 if cobertura == '1' else 3
            k = j + int(desenlace)
            pos = list(identidades).index(e['llave'])
            p = proporciones[:,pos]
            limites = np.percentile(p, [2.5,97.5], method='linear')
            fila.update(estado='RECONSTRUIDO', motivo='', unidad='proporcion',
                estimacion=format(totales[k]/totales[j],'.17g'),
                ee=format(np.std(p,ddof=1),'.17g'),
                ic_025=format(limites[0],'.17g'), ic_975=format(limites[1],'.17g'),
                naturaleza_ic=naturaleza, n=sum(r['BP2_1']==cobertura for r in dominio),
                numerador=int(totales[k]), denominador=int(totales[j]))
        salida.append(fila)
    with (BASE / 'reconstruccion.tsv').open('w') as f:
        escritor = csv.DictWriter(f,fieldnames=campos,delimiter='\t',lineterminator='\n')
        escritor.writeheader()
        escritor.writerows(salida)

if __name__ == '__main__':
    main()
