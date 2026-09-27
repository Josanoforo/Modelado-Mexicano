"""Ataques materiales al transporte; no usa cifras ni productores."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location('lote2',ROOT/'tools/validacion/astra6_paquetes_lote2.py')
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
results = []
with tempfile.TemporaryDirectory(prefix='astra6-p3-negativos-') as temporary:
    for attack in ['valido','traversal','enlace','extra','duplicado','hash-alterado']:
        path = Path(temporary)/(attack+'.tar.gz')
        method = b'Metodo humano sin cifras\n'
        manifest = json.dumps({'paquete':'prueba','archivos':{'metodo.md':hashlib.sha256(method).hexdigest()}}).encode()
        items = [('metodo.md',method),('manifiesto.json',manifest)]
        if attack=='traversal': items.append(('../fuera',b'x'))
        if attack=='extra': items.append(('extra.md',b'x'))
        if attack=='duplicado': items.append(('metodo.md',method))
        if attack=='hash-alterado': items[0]=('metodo.md',b'cambio')
        with tarfile.open(path,'w:gz') as tar:
            for name,content in items:
                info=tarfile.TarInfo(name);info.size=len(content);tar.addfile(info,io.BytesIO(content))
            if attack=='enlace':
                info=tarfile.TarInfo('enlace');info.type=tarfile.SYMTYPE;info.linkname='/etc/passwd';tar.addfile(info)
        try:
            tool.archive(path,tool.sha(path),hashlib.sha256(manifest).hexdigest())
        except AssertionError as error:
            assert attack!='valido'
            results.append({'caso':attack,'rechazado':True,'causa':str(error)})
        else:
            assert attack=='valido'
            results.append({'caso':attack,'aceptado':True})
    reason=tool.permission({'id':'enif_2024_enif_2024_bd_csv'},{})
    assert reason=='ZIP-ENIF2024-INTEGRAL-NO-AUTORIZADO'
    results.append({'caso':'ZIP-ENIF2024','rechazado':True,'causa':reason})
    reviewed={'encodat2016_bd':{'tipo':'raw','estado_acceso':'ABIERTO','autorizacion':'misión histórica'}}
    assert tool.permission({'id':'encodat2016_bd'},reviewed)==''
    results.append({'caso':'ENCODAT-no-ENCO','aceptado':True})
    assert not tool.document_matches({},'fd-ENDUTIH2022.xlsx',{('ENIGH','2022')})
    assert not tool.document_matches({},'fd-ENIGH2022.pdf',{('ENIGH','2020')})
    results.append({'caso':'FD-instrumento-o-ola-ajenos','rechazado':True})
    try:
        tool.materialize('bloqueado',Path(temporary)/'no-debe-existir',[],{})
    except AssertionError as error:
        assert not (Path(temporary)/'no-debe-existir').exists()
        results.append({'caso':'bloqueado-sin-escritura','rechazado':True,'causa':str(error)})
    else:
        raise AssertionError('Materializó bloqueado')
    source=Path(temporary)/'sintetico.csv'
    source.write_bytes(b'variable\nsynthetic\n')
    item={'id':'sintetico','archivo':'sintetico.csv','sha256':tool.sha(source)}
    delivery={'sintetico':({'manifiesto.json':b'{}'},[(item,source)],{'estado':'LISTO-PARA-SESION-NUEVA'})}
    receipt=tool.materialize('sintetico',Path(temporary)/'copia-sintetica',[],delivery)
    assert receipt['version']=='v2' and receipt['estado']=='MATERIALIZADO-SIN-RECALCULO'
    assert tool.sha(Path(temporary)/'copia-sintetica/raw/sintetico/sintetico.csv')==item['sha256']
    results.append({'caso':'transporte-sintetico-hash-recibo-v2','aceptado':True})
    newer={'sintetico':(delivery['sintetico'][0],delivery['sintetico'][1],{'estado':'LISTO-PARA-SESION-NUEVA','version_entrada':5})}
    assert tool.materialize('sintetico',Path(temporary)/'copia-sintetica-v5',[],newer)['version']=='v5'
    assert receipt['version']=='v2'
    results.append({'caso':'transporte-v5-preserva-v2','aceptado':True})
    link=Path(temporary)/'parent-link'
    link.symlink_to(Path(temporary)/'copia-sintetica',target_is_directory=True)
    try:
        tool.materialize('sintetico',link/'nuevo',[],delivery)
    except AssertionError as error:
        results.append({'caso':'destino-parent-symlink','rechazado':True,'causa':str(error)})
    else:
        raise AssertionError('Aceptó ancestor symlink')
    try:
        tool.archive(path,'0'*64,hashlib.sha256(manifest).hexdigest())
    except AssertionError as error:
        results.append({'caso':'hash-contenedor','rechazado':True,'causa':str(error)})
    else:
        raise AssertionError('Aceptó hash contenedor alterado')
out=Path(__file__).with_name('p3-pruebas-negativas.json')
out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False))
