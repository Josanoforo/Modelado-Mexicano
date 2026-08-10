import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
repo_root = next(parent for parent in root.parents if (parent / 'tools/curador_registro/produce.py').is_file())
sys.path.insert(0, str(repo_root))
from tools.curador_registro.produce import execute

if __name__ == '__main__':
    result = execute(root / 'especificacion-recibida.json', root)
    print(json.dumps({'ok': True, **result}, ensure_ascii=False, indent=2, sort_keys=True))
