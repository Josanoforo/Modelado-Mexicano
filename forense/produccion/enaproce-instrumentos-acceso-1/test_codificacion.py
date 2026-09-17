#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

from codificacion import classify_record


HERE = Path(__file__).resolve().parent


class ContractFixturesTest(unittest.TestCase):
    def test_fixtures(self):
        fixtures = json.loads((HERE / "fixtures-sinteticos.json").read_text(encoding="utf-8"))
        for fixture in fixtures:
            with self.subTest(fixture=fixture["name"]):
                observed = classify_record(**fixture["input"])
                for key, expected in fixture["expected"].items():
                    self.assertEqual(observed[key], expected)

    def test_2015_rejects_three_problem_codes(self):
        with self.assertRaisesRegex(ValueError, "longitud/repetición"):
            classify_record(
                wave=2015,
                instrument="micro",
                problem_codes=[1, 2, 6],
                procedure_code=13,
                fiscal_compliance_cost=None,
                monthly_procedure_hours=None,
            )

    def test_empty_and_exclusive_no_problem_are_invalid(self):
        common = {
            "wave": 2018,
            "instrument": "micro",
            "procedure_code": 13,
            "fiscal_compliance_cost": None,
            "monthly_procedure_hours": None,
        }
        with self.assertRaisesRegex(ValueError, "longitud/repetición"):
            classify_record(problem_codes=[], **common)
        with self.assertRaisesRegex(ValueError, "sin problemas"):
            classify_record(problem_codes=[16, 6], **common)

    def test_missing_is_not_zero_and_negative_is_invalid(self):
        missing = classify_record(
            wave=2018,
            instrument="pyme",
            problem_codes=None,
            procedure_code=None,
            fiscal_compliance_cost=None,
            monthly_procedure_hours=None,
        )
        self.assertIsNone(missing["monthly_procedure_hours"])
        self.assertFalse(missing["burden_observed"])
        with self.assertRaisesRegex(ValueError, "no negativo"):
            classify_record(
                wave=2018,
                instrument="micro",
                problem_codes=[6],
                procedure_code=4,
                fiscal_compliance_cost=10,
                monthly_procedure_hours=-1,
            )


if __name__ == "__main__":
    unittest.main()
