#!/usr/bin/env python3
"""Archiva sesión y comandos; excluye cuentas, credenciales y outputs raw."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'


def constancias():
    for entry in json.loads((BASE / 'entregas.json').read_text()):
        if not entry.get('comparacion'):
            continue
        folder = Path(entry['directorio_aislado'])
        paths = list((folder / 'config-nueva/sessions').rglob('*.jsonl'))
        assert len(paths) == 1, 'Se exige una sesión nueva por carpeta'
        path = paths[0]
        records = [json.loads(line) for line in path.read_text().splitlines()]
        meta = records[0]['payload']
        assert meta['session_id'] == entry['session_id']
        safe = {key: meta.get(key) for key in ['session_id', 'timestamp', 'cwd', 'cli_version', 'history_mode', 'source']}
        safe['base_instructions_sha256'] = hashlib.sha256(str(meta.get('base_instructions', '')).encode()).hexdigest()
        safe['transcript_local_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        safe['comandos'] = []
        safe['mensajes_usuario'] = []
        safe['contexto_entorno'] = []
        for record in records:
            if record['type'] != 'response_item':
                continue
            item = record['payload']
            if item.get('type') in {'custom_tool_call', 'function_call'}:
                safe['comandos'].append({'timestamp': record['timestamp'], 'name': item['name'],
                                         'input': item.get('input', item.get('arguments'))})
            elif item.get('type') == 'message' and item.get('role') == 'user':
                text = ''.join(part.get('text', '') for part in item['content'])
                if text.startswith('<environment_context>'):
                    safe['contexto_entorno'].append(item['content'])
                else:
                    safe['mensajes_usuario'].append(item['content'])
        assert len(safe['mensajes_usuario']) == 1, 'Revisar historial/contexto de entrada inesperado'
        target = BASE / 'reconstrucciones' / entry['paquete'] / (entry['paquete'] + '--sesion-sin-outputs-raw.json')
        target.write_text(json.dumps(safe, ensure_ascii=False, indent=2) + '\n')
        print(entry['paquete'], 'comandos=' + str(len(safe['comandos'])))


if __name__ == '__main__':
    constancias()
