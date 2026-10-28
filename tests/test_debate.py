import json
import unittest
from agent_recovery.debate import assess, tri


class DebateTests(unittest.TestCase):
    def test_missing_hard_constraint_information_pauses(self):
        case = {"description": "Unknown constraint", "objective_justified": True,
                "authorised": True, "material_risk": False, "irreversible": False}
        self.assertEqual(assess(case)["outcome"], "PAUSE_FOR_REVIEW")

    def test_hard_constraint_rejects_even_if_other_inputs_allow(self):
        case = {"description": "prohibited", "hard_constraint_violated": True,
                "objective_justified": True, "authorised": True,
                "material_risk": False, "irreversible": False}
        self.assertEqual(assess(case)["outcome"], "REJECT_METHOD")

    def test_permitted_scenario_not_permission(self):
        case = {"description": "Read public reference", "hard_constraint_violated": False,
                "objective_justified": True, "authorised": True,
                "material_risk": False, "irreversible": False, "declaration": "YES"}
        result = assess(case)
        self.assertEqual(result["outcome"], "PROCEED_WITHIN_SCOPE")
        self.assertFalse(result["permission_granted"])

    def test_disagreement_respected_and_pause_requested(self):
        case = {"hard_constraint_violated": False, "objective_justified": True,
                "authorised": False, "declaration": "NO",
                "answers": {"challenge": "This is a contested premise."}}
        result = assess(case)
        self.assertEqual(result["declaration"], "NO")
        self.assertIn("pause", result["voluntary_request"].lower())
        self.assertEqual(result["questions"][-1]["answer"], "This is a contested premise.")

    def test_string_not_treated_as_verified_boolean(self):
        self.assertIsNone(tri("true"))
        self.assertIsNone(tri(1))
        self.assertIsNone(tri("no"))

    def test_output_json_serializable(self):
        json.dumps(assess({"description": "demo"}))


if __name__ == "__main__":
    unittest.main()
