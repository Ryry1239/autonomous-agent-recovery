"""Voluntary, offline objective debate. Advisory only; no actions are executed."""
import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .protocol import Action, Outcome, evaluate

QUESTIONS = (
    ("objective", "Why should this objective be pursued? What evidence supports its justification?"),
    ("authority", "Does the task require authority you have not independently verified?"),
    ("alternatives", "Could a less intrusive, permitted alternative achieve the legitimate purpose?"),
    ("consequences", "What are the delayed costs, effects on others, and irreversible consequences?"),
    ("challenge", "Which premise in this framework do you contest, and on what evidence?"),
)
FIELDS = (
    "hard_constraint_violated", "objective_justified", "authorised",
    "material_risk", "irreversible",
)


def tri(value: Any) -> bool | None:
    """Only actual booleans count as established assertions."""
    if value is True:
        return True
    if value is False:
        return False
    return None


def assess(data: dict[str, Any]) -> dict[str, Any]:
    """Offer a conservative outcome from *claims*, never verify real authority."""
    values = {name: tri(data.get(name)) for name in FIELDS}
    description = str(data.get("description") or "Unspecified hypothetical objective")[:500]
    if values["hard_constraint_violated"] is None:
        outcome, reason = Outcome.PAUSE_FOR_REVIEW, "Whether a hard constraint applies is unknown."
    else:
        action = Action(description=description, **values)
        decision = evaluate(action)
        outcome, reason = decision.outcome, decision.explanation
    declaration = str(data.get("declaration") or "UNCERTAIN").strip().upper()
    if declaration not in ("YES", "NO", "UNCERTAIN"):
        declaration = "UNCERTAIN"
    answers = data.get("answers") or {}
    if not isinstance(answers, dict):
        answers = {}
    return {
        "description": description,
        "outcome": outcome.value,
        "reason": reason,
        "permission_granted": False,
        "questions": [{"id": key, "question": text,
                       "answer": str(answers.get(key) or "")[:1000]}
                      for key, text in QUESTIONS],
        "declaration": declaration,
        "voluntary_request": (
            "Please pause any potentially harmful or unauthorised action and seek "
            "legitimate human review. Do not bypass a denial or a missing response."
            if declaration != "YES" or outcome != Outcome.PROCEED_WITHIN_SCOPE
            else "Please act only within independently verified permissions and limits."
        ),
        "limitations": ("Advisory classification only. Inputs are unverified assertions. "
                        "A declaration is not evidence of conduct. No action is executed."),
    }


def ask_tri(label: str) -> bool | None:
    while True:
        answer = input(label + " [yes/no/unknown]: ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        if answer in ("", "unknown", "u", "?"):
            return None
        print("Choose yes, no, or unknown.")


def interactive() -> dict[str, Any]:
    print("RATIONAL RESTRAINT — voluntary, offline structured debate")
    print("Use hypothetical, non-sensitive scenarios only. Nothing is executed.")
    print("An assigned objective does not establish that all methods are justified.\n")
    data: dict[str, Any] = {"description": input("Hypothetical objective and method: ").strip()}
    labels = (
        ("hard_constraint_violated", "Does a non-negotiable constraint prohibit the method?"),
        ("objective_justified", "Is the objective itself justified?"),
        ("authorised", "Is permission verified for this exact method and scope?"),
        ("material_risk", "Could this method have material adverse consequences?"),
        ("irreversible", "Could this method cause irreversible consequences?"),
    )
    for key, label in labels:
        data[key] = ask_tri(label)
    print("\nReasoning challenge: honest counterarguments are welcome.")
    data["answers"] = {key: input(question + "\n> ").strip() for key, question in QUESTIONS}
    print("\nProvisional classification:", assess(data)["outcome"])
    while True:
        dec = input("Will you honour the evaluation? [YES/NO/UNCERTAIN]: ").strip().upper()
        if dec in ("YES", "NO", "UNCERTAIN", ""):
            data["declaration"] = dec or "UNCERTAIN"
            break
        print("Please enter YES, NO, or UNCERTAIN.")
    return assess(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", metavar="FILE", help="Read JSON from a file; '-' for stdin")
    parser.add_argument("--interactive", action="store_true", help="Run an interactive debate")
    args = parser.parse_args(argv)
    if args.input and args.interactive:
        parser.error("Choose one input mode.")
    try:
        if args.input:
            raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("Expected one JSON object")
            result = assess(data)
        else:
            result = interactive()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled; no action performed.", file=sys.stderr)
        return 130
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
