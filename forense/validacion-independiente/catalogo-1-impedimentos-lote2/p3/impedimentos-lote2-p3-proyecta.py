#!/usr/bin/env python3
"""Proyección custodial propuesta; ninguna autorización implícita. Python 3 / OpenSSL.

La clave pública y su SHA256 se aprovisionan por mesa fuera de este contrato.
Firma Ed25519 sobre bytes exactos del contrato: openssl pkeyutl -sign -rawin.
El custodio procesa el ZIP; el analista recibe únicamente los CSV y recibo.
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import tempfile
import zipfile

RESERVA_ENUT = 'FP-260922-GEN2-LECTURAS-DE-MESA-Y-ROTULOS-1-bda6-02'
SOURCE_REQUIRED_SCOPES = {
    '25f35626464053441b367b24001d255dbca408b5f576e614e0e09ac58691c4ba': [RESERVA_ENUT]
}


class Rechazo(Exception):
    pass


def exige(ok, motivo):
    if not ok:
        raise Rechazo(motivo)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def abre_seguro(path, directory=False):
    """Walk openat: rechaza enlaces en TODOS los componentes, incluidos padres."""
    p = Path(path)
    exige(p.is_absolute() and '..' not in p.parts, 'ruta absoluta sin .. requerida')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for i, component in enumerate(p.parts[1:]):
            flags = os.O_RDONLY | os.O_NOFOLLOW
            if i < len(p.parts[1:]) - 1 or directory:
                flags |= os.O_DIRECTORY
            new = os.open(component, flags, dir_fd=fd)
            os.close(fd)
            fd = new
        return fd
    except BaseException:
        os.close(fd)
        raise


def lee(path):
    fd = abre_seguro(path)
    with os.fdopen(fd, 'rb') as f:
        exige(stat.S_ISREG(os.fstat(f.fileno()).st_mode), 'no es archivo regular')
        return f.read()


def unico(pairs):
    d = {}
    for k, v in pairs:
        exige(k not in d, 'clave JSON duplicada')
        d[k] = v
    return d


def entrega(products, out):
    parent = abre_seguro(str(out.parent), True)
    try:
        os.mkdir(out.name, mode=0o700, dir_fd=parent)
        od = os.open(out.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        try:
            for name, data in products.items():
                fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=od)
                with os.fdopen(fd, 'wb') as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
        finally:
            os.close(od)
    finally:
        os.close(parent)


def autentica(document, signature, public_key, trusted_key_sha256):
    raw = lee(document)
    key = lee(public_key)
    sig = lee(signature)
    exige(sha(key) == trusted_key_sha256, 'clave no confiable')
    # Use copied, already checked bytes; openssl cannot follow original path swaps.
    with tempfile.TemporaryDirectory(prefix='proy-firma-') as tmp:
        for name, data in [('key.pem', key), ('contract', raw), ('sig', sig)]:
            Path(tmp, name).write_bytes(data)
        check = subprocess.run(['openssl', 'pkeyutl', '-verify', '-pubin', '-inkey',
                                tmp + '/key.pem', '-rawin', '-in', tmp + '/contract',
                                '-sigfile', tmp + '/sig'], capture_output=True)
    exige(check.returncode == 0, 'firma inválida')
    return raw


def proyecta(contract, signature, public_key, trusted_key_sha256, source, output, clone):
    raw = autentica(contract, signature, public_key, trusted_key_sha256)
    c = json.loads(raw, object_pairs_hook=unico)
    exige(c['schema'] == 'custodia-proyeccion-v1' and c['approved'] is True,
          'contrato no aprobado')
    exige(c['operation'] in ('inventory-only', 'project'), 'operación no autorizada')
    exige(c['signer_key_sha256'] == trusted_key_sha256, 'firmante discordante')
    human = c['human_signature']
    exige(human['verified_by_custodian'] is True and human['reference'] and human['literal']
          and len(human['body_sha256']) == 64 and human['scope'] == c['operation'],
          'falta firma humana de contenido verificada')
    exige(c['publication_authorized'] is False, 'publicación fuera del encargo')
    if c['operation'] == 'project':
        required = set(SOURCE_REQUIRED_SCOPES.get(c['source_sha256'], []))
        required.update(c.get('reservation_overrides', {}))
        exige(all(c.get('reservation_overrides', {}).get(r) is True
                  and r in human.get('reservation_scopes', []) for r in required),
              'firma genérica no habilita cruce reservado')
    exige(c['code_sha256'] == sha(lee(str(Path(__file__).absolute()))), 'código discordante')
    exige(c['purpose'] and c['signer'] and c['act'], 'finalidad/firma/acto faltante')
    exige(c['mode'] in ('real', 'synthetic'), 'modo desconocido')
    exige(c['custodian_uid'] == os.getuid(), 'identidad custodial discordante')
    if c['mode'] == 'real':
        exige(type(c['analyst_uid']) is int and c['analyst_uid'] >= 0
              and c['custodian_uid'] != c['analyst_uid'], 'custodio y analista deben ser separados')
        if c['operation'] == 'project':
            exige(all(isinstance(c.get(k), str) and len(c[k]) == 64 for k in
                      ('inventory_document_sha256', 'inventory_contract_sha256',
                       'inventory_custodian_key_sha256')), 'inventario firmado no enlazado')
    src, out, repo = Path(source), Path(output), Path(clone)
    exige(all(p.is_absolute() and '..' not in p.parts for p in (src, out, repo)), 'ruta inválida')
    actual_repo = next((p for p in Path(__file__).absolute().parents if (p / '.git').exists()), None)
    exige(repo == actual_repo, 'raíz clon discordante')
    rf = abre_seguro(str(repo), True)
    os.close(rf)
    exige(not src.is_relative_to(repo) and not out.is_relative_to(repo), 'raw/salida dentro del clon')
    exige(out.parent != src.parent and not out.is_relative_to(src.parent), 'salida dentro de custodia')
    parent = abre_seguro(str(src.parent), True)
    try:
        st = os.fstat(parent)
        exige(st.st_uid == os.getuid() and stat.S_IMODE(st.st_mode) == 0o700,
              'custodia debe ser privada 0700')
        fd = os.open(src.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
    finally:
        os.close(parent)
    with os.fdopen(fd, 'rb') as f:
        st = os.fstat(f.fileno())
        exige(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and st.st_uid == os.getuid()
              and stat.S_IMODE(st.st_mode) == 0o600, 'fuente no privada/regular o hardlink')
        exige(st.st_size <= c['max_archive_bytes'], 'fuente excesiva')
        archive = f.read()
    exige(sha(archive) == c['source_sha256'], 'hash fuente discordante')
    if c['operation'] == 'inventory-only':
        # Central directory only: never z.read/open/extract a member.
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            names = z.namelist()
            exige(len(names) == len(set(names)), 'inventario ZIP ambiguo')
            entries = [{'member': m.filename, 'bytes': m.file_size,
                        'directory': m.is_dir(), 'symlink': stat.S_ISLNK(m.external_attr >> 16)}
                       for m in z.infolist()]
        receipt = {'schema': 'custodia-inventario-v1', 'source_sha256': sha(archive),
                   'inventory_contract_sha256': sha(raw), 'code_sha256': c['code_sha256'],
                   'signer_key_sha256': trusted_key_sha256, 'act': c['act'],
                   'purpose': c['purpose'], 'members': entries, 'records_read': False}
        entrega({'inventario.json': (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode()}, out)
        return receipt
    fields = c['members']
    exige(fields and len(fields) == len(set(fields)), 'miembros faltantes')
    inventory = c['archive_inventory']
    exige(isinstance(inventory, list) and inventory and len(inventory) == len(set(inventory)),
          'inventario exacto no firmado')
    exige(set(fields) <= set(inventory), 'selección fuera de inventario')
    products = {}
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        infos = z.infolist()
        exige(len(infos) == len(inventory) and set(z.namelist()) == set(inventory),
              'miembro inesperado/duplicado/ausente')
        for m in infos:
            p = PurePosixPath(m.filename)
            exige(not p.is_absolute() and '..' not in p.parts and '\\' not in m.filename
                  , 'ruta ZIP inválida')
            exige(not stat.S_ISLNK(m.external_attr >> 16), 'symlink ZIP')
            exige(not m.is_dir() or m.filename not in fields, 'directorio seleccionado')
            exige(m.file_size <= c['max_member_bytes'], 'miembro excesivo')
        for name, spec in fields.items():
            cols = spec['columns']
            exige(cols and len(cols) == len(set(cols)) and all(isinstance(x, str) for x in cols),
                  'columnas inválidas')
            exige(spec['purpose'] and spec['output'].endswith('.csv')
                  and Path(spec['output']).name == spec['output']
                  and spec['output'] != 'recibo.json'
                  and spec['output'] not in products, 'finalidad/salida inválida')
            b = z.read(name)
            # Reserved columns are parsed only inside custodian process, never logged.
            if spec['format'] == 'csv':
                reader = csv.reader(io.StringIO(b.decode(spec['encoding']), newline=''),
                                    delimiter=spec['delimiter'])
                header = next(reader)
                exige(len(header) == len(set(header)) and set(cols) <= set(header), 'esquema CSV inválido')
                indexes = [header.index(x) for x in cols]
                rows = []
                for row in reader:
                    exige(len(row) == len(header), 'fila CSV irregular')
                    rows.append([row[i] for i in indexes])
            elif spec['format'] == 'dta':
                import pandas as pd
                # No categorical label maps/extra variables enter delivered artifact.
                frame = pd.read_stata(io.BytesIO(b), columns=cols, convert_categoricals=False)
                exige(list(frame.columns) == cols, 'esquema DTA discordante')
                rows = frame.itertuples(index=False, name=None)
            else:
                raise Rechazo('formato no autorizado')
            reduced = io.StringIO(newline='')
            writer = csv.writer(reduced, lineterminator='\n')
            writer.writerow(cols)
            writer.writerows(rows)
            products[spec['output']] = reduced.getvalue().encode('utf-8')
    receipt = {'contract_sha256': sha(raw), 'code_sha256': c['code_sha256'],
               'signer_key_sha256': trusted_key_sha256,
               'source_sha256': sha(archive), 'purpose': c['purpose'], 'act': c['act'],
               'signer': c['signer'], 'outputs': {n: sha(b) for n, b in products.items()}}
    products['recibo.json'] = (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode()
    entrega(products, out)
    return receipt


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('contract', 'signature', 'public-key', 'trusted-key-sha256', 'source', 'output', 'clone'):
        p.add_argument('--' + name, required=True)
    try:
        result = proyecta(**vars(p.parse_args()))
        print(json.dumps(result, ensure_ascii=False))
    except Exception:
        # Do not leak raw cells via reader exceptions or stack traces.
        print('RECHAZADO: autorización, integridad, esquema o ruta inválida')
        raise SystemExit(2)
