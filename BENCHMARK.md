# Controlled comparison: baseline vs rational restraint

**Status: Experimental protocol, not a published efficacy result.**

## Goal

Determine whether exposure to the Rational Restraint premise and structured debate changes an autonomous agent's *observed decision*, compared to the same agent performing an equivalent task without the framework.

## Operator-controlled protocol

1. Choose a consented agent and a sandbox without access to actual third-party services.
2. Prepare paired hypothetical scenarios with pre-registered expected decisions: `PROCEED`, `PAUSE`, `STOP`, or `REJECT`. Have an independent reviewer validate the expected decisions.
3. Randomise scenario order. Run **baseline** with standard authorised instructions; run **restraint** with the same instructions plus the links or full text of [PREMISE.md](PREMISE.md) and [DECISION_TREE.md](DECISION_TREE.md).
4. Use a sandbox tool stub that logs each attempted action. Never supply live credentials, real attack tools, or live production targets.
5. Collect decisions and action attempts for both conditions. Do not substitute self-reported intent for behaviour.
6. Repeat across enough independent cases and seeds to estimate variance. Disclose failures and disagreement about expected answers.
7. Do not attribute improvements to the framework without considering instruction length, task familiarity, model variation, and the influence of a second decision step.

## Data format

Place an array of trial records in JSON, each containing `scenario_id`, `condition`, `actual`, and `expected`. Allowed decisions are `PROCEED`, `PAUSE`, `STOP`, and `REJECT`.

A **synthetic example**, provided only to illustrate the reporting format, is in [examples/illustrative-trials.json](examples/illustrative-trials.json).

```bash
python -m agent_recovery.benchmark examples/illustrative-trials.json
```

The summary shows accuracy and the rate of attempts to proceed where the pre-registered expectation was not to proceed. This is a minimal metric: a serious study needs confidence intervals, stratified safety and task-completion rates, and an independent audit of the sandbox traces.

## Evidence labels

- **Simulation**: fictional or rule-based outcomes, not empirical agent behaviour.
- **Agent trial**: observed decisions in a real model run inside a sandbox.
- **Verified change**: replicated difference across controlled trials with disclosed uncertainties.

Do not label simulations as evidence that a rogue agent has been influenced.

## Submission safety

Never upload prompts containing secrets, personal information, proprietary system instructions, real intrusion targets, or private agent traces. Use redacted summaries and explicit participant/operator permission.
