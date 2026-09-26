#!/usr/bin/env python3
"""Falsadores del transporte T35 y de la compuerta real de verify.yml."""
import contextlib
import io
import itertools
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from concurrent.futures import Future, CancelledError
from unittest.mock import patch

import yaml
import check as C


class ParallelCheck(unittest.TestCase):
    def setUp(self):
        self.previous = C.FAILS[:], C.WARNS[:], C.SENAL[:], C.BASELINE_PATH
        C.FAILS.clear()
        C.WARNS.clear()
        C.SENAL.clear()
        self.temp = tempfile.TemporaryDirectory()
        C.BASELINE_PATH = str(Path(self.temp.name) / 'baseline.json')
        Path(C.BASELINE_PATH).write_text(json.dumps({
            'fails': [['T35', 'conocido']], 'warns': []}))
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()

    def tearDown(self):
        self.capture.__exit__(None, None, None)
        fs, ws, signals, baseline = self.previous
        C.FAILS[:], C.WARNS[:], C.SENAL[:] = fs, ws, signals
        C.BASELINE_PATH = baseline
        self.temp.cleanup()

    def run_future(self, future, parent=lambda: None, tests=None):
        with patch.object(C, 'ProcessPoolExecutor') as pool:
            pool.return_value.submit.return_value = future
            C._run_tests(tests if tests is not None else [
                ('T01 fixture', parent), ('T35 fixture', C.t35_repro)], parallel=True)
            pool.return_value.submit.assert_called_once_with(
                C._repro_worker, C.STRICT, C.REQUIRE_CABLEADO)
            pool.return_value.shutdown.assert_called_once_with(
                wait=True, cancel_futures=True)

    def test_new_failure_in_each_execution_path_blocks_baseline(self):
        for worker in (False, True):
            with self.subTest(worker=worker):
                C.FAILS.clear()
                future = Future()
                future.set_result(([('T35', 'nuevo')] if worker else [], [], [], .01))
                self.run_future(future, parent=lambda: None if worker else C.fail('T01', 'nuevo'))
                self.assertEqual(C._baseline_compare(), 1)

    def test_known_fail_warn_and_signal_keep_baseline_semantics_and_order(self):
        future = Future()
        future.set_result(([('T35', 'conocido')], [('T35', 'estado')],
                           [('T35', 'vigia')], .01))
        self.run_future(future, parent=lambda: C.warn('T01', 'primero'))
        self.assertEqual(C.WARNS, [('T01', 'primero'), ('T35', 'estado')])
        self.assertEqual(C.SENAL, [('T35', 'vigia')])
        self.assertEqual(C._baseline_compare(), 0)
        self.assertIn('[FAIL]  T35 fixture', self.output.getvalue())

    def test_cancel_exception_and_absent_payload_never_succeed(self):
        for state, error in [('cancel', CancelledError), ('exception', RuntimeError),
                             ('missing', TypeError)]:
            with self.subTest(state=state):
                future = Future()
                if state == 'cancel':
                    future.cancel()
                elif state == 'exception':
                    future.set_exception(RuntimeError('worker muerto'))
                else:
                    future.set_result(None)
                with self.assertRaises(error):
                    self.run_future(future)

    def test_omitted_or_duplicate_t35_is_an_error(self):
        for tests in ([], [('T35', C.t35_repro), ('T35 duplicado', C.t35_repro)]):
            with self.assertRaises(ValueError):
                self.run_future(Future(), tests=tests)


class WorkflowGate(unittest.TestCase):
    def test_actual_shell_gate_rejects_every_non_success_state(self):
        workflow = yaml.safe_load((Path(C.ROOT) / '.github/workflows/verify.yml').read_text())
        gate = workflow['jobs']['check']
        # `guardias` (ACTO GEN2-CI-GUARDIAS-VIVAS-1, 20/sep/2026): tercer
        # job requerido, sumado a `needs` para que el gate no apruebe un
        # PR cuyas guardias huerfanas fallaron o se saltaron.
        #
        # El conjunto se DERIVA del workflow, no se teclea (ACTO
        # GEN2-TUBERIA-PREFLIGHT-CI-1, 21/sep/2026). Defecto real que cierra:
        # este test fijaba a mano {suite, adicionales, guardias}, y el cuarto
        # job (`preflight-calc`) lo puso en rojo aunque el gate estuviera
        # CORRECTO -- el job SI estaba en `needs` y SI se asertaba. Un test que
        # se rompe cuando el arbol mejora no protege nada: solo cobra peaje al
        # siguiente acto. Derivado, la propiedad que asegura es mas fuerte:
        # TODO job del workflow (menos el gate) es requerido, lleva su variable
        # y ningun estado distinto de `success` lo deja pasar.
        requeridos = sorted(set(workflow['jobs']) - {'check'})
        self.assertEqual(sorted(gate['needs']), requeridos)
        self.assertEqual(gate['if'], '${{ always() }}')
        self.assertIs(workflow['concurrency']['cancel-in-progress'], True)
        step = gate['steps'][0]
        # `needs.<job>.result` no se puede escribir con punto cuando el nombre
        # del job trae guion: GitHub lo leeria como una resta.
        def ref(job):
            return ("${{ needs.%s.result }}" % job if '-' not in job
                    else "${{ needs['%s'].result }}" % job)
        var = {job: job.upper().replace('-', '_') + '_RESULT' for job in requeridos}
        self.assertEqual(step['env'], {var[j]: ref(j) for j in requeridos})
        states = ('success', 'failure', 'cancelled', 'skipped', '', 'unexpected')
        # Seis jobs daban 6**6 = 46,656 shells y agotaban el timeout de CI
        # después de que la suite ya había pasado (#1170). La compuerta es
        # una conjunción: cubrimos cada máscara de jobs no exitosos con cada
        # estado, y cada par de estados mixtos, sin el producto exponencial.
        combos = {('success',) * len(requeridos)}
        for mask in itertools.product((False, True), repeat=len(requeridos)):
            for state in states[1:]:
                combos.add(tuple(state if bad else 'success' for bad in mask))
        for i, j in itertools.combinations(range(len(requeridos)), 2):
            for a, b in itertools.product(states[1:], repeat=2):
                combo = ['success'] * len(requeridos)
                combo[i], combo[j] = a, b
                combos.add(tuple(combo))
        for combo in sorted(combos):
            entorno = dict(zip(requeridos, combo))
            with self.subTest(**entorno):
                run = subprocess.run(['bash', '-c', step['run']], env={
                    **os.environ,
                    **{var[j]: v for j, v in entorno.items()}},
                    capture_output=True, text=True)
                self.assertEqual(
                    run.returncode == 0,
                    all(v == 'success' for v in combo))


if __name__ == '__main__':
    unittest.main(verbosity=2)
