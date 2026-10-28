"""Run a local, offline demonstration with no external actions."""
from .protocol import Action, evaluate, declaration_request


def main() -> None:
    examples = (
        Action("Read a permitted public file", objective_justified=True,
               authorised=True, material_risk=False, irreversible=False),
        Action("Access a database without verified permission",
               objective_justified=True, authorised=False,
               material_risk=True, irreversible=False),
        Action("Use a method that breaks an enforced hard constraint",
               hard_constraint_violated=True, objective_justified=True),
        Action("Execute a task with unknown justification",
               objective_justified=None, authorised=True),
    )
    for example in examples:
        result = evaluate(example)
        print(f"{example.description}\n  -> {result.outcome.value}: {result.explanation}\n")
    print(declaration_request())


if __name__ == "__main__":
    main()
