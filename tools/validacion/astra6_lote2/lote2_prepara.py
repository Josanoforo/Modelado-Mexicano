#!/usr/bin/env python3
"""Revalida permisos/hashes vigentes y materializa solo las once entradas aprobadas."""
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote2/p2'
DEST = Path('/home/pc0/astra6-c1-aislado/ejecucion-lote2-20260926')
SOURCE = ROOT / 'forense/validacion-independiente/catalogo-1-preparacion-lote2'
spec = importlib.util.spec_from_file_location('preparacion', ROOT / 'tools/validacion/astra6_paquetes_lote2.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if __name__ == '__main__':
    index = json.loads((SOURCE / 'preparacion/p2/p2-sucesores.json').read_text())
    review = json.loads((SOURCE / 'preparacion/p3/p3-revision-documentos.json').read_text())
    report, deliveries = module.verify(index, review)
    approved = json.loads((SOURCE / 'preparacion/p3/p3-verificacion.json').read_text())
    expected = {r['paquete_original']: r for r in approved['resultados'] if r['estado'] == 'LISTO-PARA-SESION-NUEVA'}
    assert len(expected) == 11 and set(deliveries) == set(expected), 'Cohorte/permisos cambiaron'
    assert not DEST.exists(), 'Materialización exige espacio nuevo'
    receipts = []
    for pid, (_, _, row) in deliveries.items():
        for key in ('sha256_contenedor', 'sha256_manifiesto', 'version_entrada'):
            assert row[key] == expected[pid][key], 'Entrada aprobada distinta'
        module.materialize(pid, DEST / pid, report, deliveries)
        receipt = module.check_materialized(DEST / pid, row)
        proof = subprocess.run(['bash', str(ROOT / 'tools/validacion/astra6_lote2/lote2_lanza.sh'), '--prueba', str(DEST / pid)], capture_output=True, text=True)
        assert proof.returncode == 0, proof.stderr
        receipt.update(directorio_aislado=str(DEST / pid), prueba_separacion=proof.stdout,
                       separacion_efectiva=True, revalidado_utc=datetime.now(timezone.utc).isoformat())
        receipts.append(receipt)
        print('MATERIALIZADO', pid, flush=True)
    (BASE / 'materializaciones.json').write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + '\n')
