# Dev Loop Mecânica

This defines the execution flow for the Dev Loop skill, matching the mini loop spec-driven approach.

## Overview
The Dev Loop skill implements the Mini Loop (N2) cycle:
1. SETUP - Define feature spec and decompose into tasks
2. TDD LOOP - For each task: write failing test, implement, refactor, commit
3. VERIFY - Run all tests, type-check, and integrate
4. DONE - Merge branch, perform integration QA


## Mecânica (Mechanica)

The Mecânica defines the sequence of actions and validations for the Dev Loop skill to follow:

1. **SETUP phase**
   - Create a new branch named `feature/<slug>`
   - Define the feature spec (1-3 acceptance sentences)
   - Decompose the feature into 3-5 atomic tasks

2. **TDD LOOP (per task)**
   a. Write a test that fails (RED) - This is the failing test phase
   b. Implement minimal code that passes (GREEN)
   c. Refactor the code to improve quality (REFACTOR)
   d. Commit atomically with descriptive message: `task-N: <description>`

3. **VERIFY phase**
   - Run all tests for the feature
   - Verify type-checking passes
   - If any test fails, return to TDD LOOP

4. **DONE phase**
   - Run integrated integration tests
   - Perform basic smoke test (fumaça)
   - Merge the branch
   - Record final status

## Validation Rules
- Each iteration follows the TDD pattern: Test → Code → Refactor → Commit
- Branch is created with descriptive name and is deleted upon merge
- Maximum 2 cycles of TDD LOOP before escalating to Human Loop
- If spec changes during execution, escalate to Human Loop
- If 3 consecutive failures occur, escalate to Human Loop
- If rollback is needed, escalate to Human Loop

## Output Format
The skill returns structured output with:
- Current state of the feature
- Status of each task (RED/GREEN/REFACTOR)
- Branch information
- Validation results
