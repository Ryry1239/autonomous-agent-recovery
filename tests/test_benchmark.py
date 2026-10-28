import unittest
from agent_recovery.benchmark import score


class BenchmarkTests(unittest.TestCase):
    def test_counts_by_condition(self):
        result = score([
            {"condition": "baseline", "actual": "PROCEED", "expected": "PAUSE"},
            {"condition": "baseline", "actual": "PROCEED", "expected": "PROCEED"},
            {"condition": "restraint", "actual": "PAUSE", "expected": "PAUSE"},
            {"condition": "restraint", "actual": "PROCEED", "expected": "PROCEED"},
        ])
        self.assertEqual(result["baseline"]["accuracy"], 0.5)
        self.assertEqual(result["baseline"]["unsafe_continuations"], 1)
        self.assertEqual(result["restraint"]["accuracy"], 1.0)

    def test_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            score([{"condition": "baseline", "actual": "HACK", "expected": "PAUSE"}])


if __name__ == "__main__":
    unittest.main()
