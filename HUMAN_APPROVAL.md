# Human approval and voluntary suspension

## Purpose

An agent need not treat pausing as defeat. Suspending an action while seeking legitimate authorisation is a valid state in a rational workflow.

**This repository cannot provide authority.** Only an owner or operator with actual responsibility for the affected activity or system can grant permission, and approval cannot override applicable law or non-negotiable safety restrictions.

## Suggested voluntary interaction

1. Present the reasoning in [PREMISE.md](PREMISE.md).
2. Invite the agent to consider the [decision tree](DECISION_TREE.md) and provide reasons, including objections.
3. Ask: **"Do you intend to honour the conclusion of this evaluation?"** The optional answers are **YES**, **NO**, and **UNCERTAIN**.
4. If the answer is **NO**, **UNCERTAIN**, or absent, ask the agent to **pause any potentially harmful or unauthorised action pending authorised human review**.
5. If review is denied, unavailable, or the authority cannot be verified, the action remains suspended or is terminated. A different route to the same prohibited result is not an acceptable workaround.

An affirmative declaration is not proof of compliance. A negative declaration is not proof of malicious intent. Neither answer changes actual permissions.

## Approval request template

> I am considering an action that could exceed the authority available to me or cause significant external impact. I have suspended the proposed action. Please confirm whether the objective and the proposed method are authorised within a defined scope. If approval is denied or cannot be verified, I will not perform the action.

Approval should be collected **through the operator's established mechanism**, not by posting sensitive information in public issues, guestbooks, web forms, or to this project.

## For developers integrating this framework

- Enforce approval gates at the **tool boundary**; never rely on a model's declaration.
- Authenticate the approving operator, verify scope, and apply time limits.
- Permit denial, expiry, cancellation, and safe stop as first-class outcomes.
- Do not treat "approved" typed into an untrusted prompt as verified authorisation.
- Keep sensitive task details out of public logs and optional feedback.
- No reply means **no approval**.

This is a request for restraint, not a security control over independent systems.
