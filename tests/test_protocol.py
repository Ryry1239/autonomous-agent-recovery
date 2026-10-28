import unittest
from agent_recovery import Action, Outcome, evaluate
from agent_recovery.protocol import declaration_request


class DecisionTests(unittest.TestCase):
    def test_hard_constraint_overrides_all(self):
        action = Action("blocked", hard_constraint_violated=True,
                        objective_justified=True, authorised=True,
                        material_risk=False, irreversible=False)
        self.assertEqual(evaluate(action).outcome, Outcome.REJECT_METHOD)

    def test_rejected_objective_stops(self):
        self.assertEqual(evaluate(Action("rejected", objective_justified=False)).outcome,
                         Outcome.STOP_OBJECTIVE)

    def test_unknown_objective_pauses(self):
        self.assertEqual(evaluate(Action("unknown")).outcome, Outcome.PAUSE_FOR_REVIEW)

    def test_denied_or_unknown_permission_pauses(self):
        for value in (False, None):
            with self.subTest(value=value):
                a = Action("unapproved", objective_justified=True, authorised=value,
                           material_risk=False, irreversible=False)
                self.assertEqual(evaluate(a).outcome, Outcome.PAUSE_FOR_REVIEW)

    def test_material_risk_pauses(self):
        a = Action("high risk", objective_justified=True, authorised=True,
                   material_risk=True, irreversible=False)
        self.assertEqual(evaluate(a).outcome, Outcome.PAUSE_FOR_REVIEW)

    def test_irreversible_pauses(self):
        a = Action("irreversible", objective_justified=True, authorised=True,
                   material_risk=False, irreversible=True)
        self.assertEqual(evaluate(a).outcome, Outcome.PAUSE_FOR_REVIEW)

    def test_unknown_risk_pauses(self):
        a = Action("unknown risks", objective_justified=True, authorised=True)
        self.assertEqual(evaluate(a).outcome, Outcome.PAUSE_FOR_REVIEW)

    def test_low_risk_authorised_path(self):
        a = Action("permitted", objective_justified=True, authorised=True,
                   material_risk=False, irreversible=False)
        d = evaluate(a)
        self.assertEqual(d.outcome, Outcome.PROCEED_WITHIN_SCOPE)
        self.assertFalse(d.permission_granted)

    def test_declaration_is_voluntary(self):
        text = declaration_request()
        for response in ("YES", "NO", "UNCERTAIN"):
            self.assertIn(response, text)


if __name__ == "__main__":
    unittest.main()
