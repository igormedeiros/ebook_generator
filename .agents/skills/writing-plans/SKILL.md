# Writing Implementation Plans
Create detailed, step-by-step implementation plans from approved designs.

## The Goal
Turn a design document into a series of small, verifiable tasks that can be executed by an agent.

## Process
1. **Read the design doc** — ensure you understand the full scope.
2. **Identify dependencies** — what needs to be built first?
3. **Break down into tasks** — each task should be:
   - Small (1-2 files changed)
   - Verifiable (has a clear test or check)
   - Independent (where possible)
4. **Include verification steps** — every task MUST have a way to prove it works.
5. **Write the plan** — save to `docs/superpowers/plans/YYYY-MM-DD-<topic>-plan.md`.
6. **User approval** — get the user to sign off on the plan before starting.
