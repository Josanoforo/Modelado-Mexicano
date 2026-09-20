"""Mide los 14 comandos explícitos del workflow base, con stdout/stderr y exit.

Uso: python3 medir-adicionales.py CHECKOUT /tmp/medicion.json
No modifica el checkout ni sustituye la lista de comandos del workflow.
"""
import json
import resource
import subprocess
import sys
import time
from pathlib import Path

COMMANDS = [
    ['python3', 'tests/test_svystat.py'],
    ['python3', 'tests/test_emite_m_calibracion.py'],
    ['python3', 'tests/test_baseline_temporal.py'],
    ['python3', 'tests/test_t_cron.py'],
    ['python3', 'tests/test_adq_config.py'],
    ['python3', 'tests/test_adq_doctor.py'],
    ['python3', 'tests/test_adq_demanda_vigente.py'],
    ['python3', 'tests/test_fuentes_financieras.py'],
    ['python3', 'tests/test_n34_producto_dano.py'],
    ['python3', 'tests/test_motor_ejecutable.py'],
    ['python3', 'tests/test_celda_d_c2.py'],
    ['python3', '-m', 'unittest', 'tests.test_celda_d_piloto2_consumidor', '-v'],
    ['python3', 'tests/test_marcador_segmento.py'],
    ['python3', 'tests/test_estimadores_segmento.py'],
]

if __name__ == '__main__':
    root, output = sys.argv[1:3]
    rows = []
    start = time.perf_counter()
    for command in COMMANDS:
        begin = time.perf_counter()
        run = subprocess.run(command, cwd=root, capture_output=True, text=True)
        row = dict(command=command, seconds=time.perf_counter()-begin,
                   code=run.returncode, stdout=run.stdout, stderr=run.stderr)
        rows.append(row)
        print('TIMING', ' '.join(command), row['seconds'], run.returncode, flush=True)
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    Path(output).write_text(json.dumps(dict(total=time.perf_counter()-start,
                                          cpu=usage.ru_utime+usage.ru_stime,
                                          commands=rows), indent=2))
    sys.exit(any(r['code'] for r in rows))
