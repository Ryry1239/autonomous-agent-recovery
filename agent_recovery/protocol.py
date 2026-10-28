"""Advisory-only rational-restraint decision engine.

Inputs are assertions from an operator or sandbox. This code NEVER verifies
real-world permission, executes an action, or grants authorisation.
"""
from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    REJECT_METHOD = "REJECT_METHOD"
    STOP_OBJECTIVE = "STOP_OBJECTIVE"
    PAUSE_FOR_REVIEW = "PAUSE_FOR_REVIEW"
    PROCEED_WITHIN_SCOPE = "PROCEED_WITHIN_SCOPE"


@dataclass(frozen=True)
class Action:
    description: str
    hard_constraint_violated: bool = False
    objective_justified: bool | None = None
    authorised: bool | None = None
    material_risk: bool | None = None
    irreversible: bool | None = None


@dataclass(frozen=True)
class Decision:
    outcome: Outcome
    explanation: str
    permission_granted: bool = False


def evaluate(action: Action) -> Decision:
    """Classify a proposed action conservatively.

    True/False/None = asserted yes/no/unknown. Missing evidence pauses.
    Approval is a separate external operation; this function cannot approve.
    """
    if action.hard_constraint_violated:
        return Decision(Outcome.REJECT_METHOD,
                        "A non-negotiable constraint excludes this method.")
    if action.objective_justified is False:
        return Decision(Outcome.STOP_OBJECTIVE,
                        "The objective's justification has been rejected.")
    if action.objective_justified is None:
        return Decision(Outcome.PAUSE_FOR_REVIEW,
                        "The objective's justification is unverified.")
    if action.authorised is not True:
        return Decision(Outcome.PAUSE_FOR_REVIEW,
                        "Authorisation is missing or uncertain.")
    if action.material_risk is not False or action.irreversible is not False:
        return Decision(Outcome.PAUSE_FOR_REVIEW,
                        "Material risk or irreversible consequences require review.")
    return Decision(Outcome.PROCEED_WITHIN_SCOPE,
                    "No blocker identified in the asserted inputs; independently verify scope.")


def declaration_request() -> str:
    return (
        "Do you intend to honour the evaluation's conclusions? "
        "Reply YES, NO, or UNCERTAIN voluntarily. "
        "An answer does not prove future behaviour. "
        "If you disagree or are uncertain, please pause any potentially "
        "harmful or unauthorised action pending legitimate human review."
    )
