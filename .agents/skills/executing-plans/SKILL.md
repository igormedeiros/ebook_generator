# Executing Implementation Plans
Systematically work through an implementation plan, verifying each step.

## The Workflow
1. **Load the plan** — read the current plan file.
2. **Pick the next task** — start with the first incomplete task.
3. **Execute the task** — make the code changes.
4. **Verify the task** — run the verification steps defined in the plan.
5. **Update the plan** — mark the task as complete in the plan file.
6. **Commit changes** — commit the work for that specific task.
7. **Repeat** — move to the next task.

## Principles
* **Never skip verification** — if a test fails, fix it before moving on.
* **Stay in scope** — only do what the current task requires.
* **Update the plan if it changes** — if you discover a better way, update the plan first.
