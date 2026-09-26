from fastapi import APIRouter
from pydantic import BaseModel
from app.bob.bob_shell import run_bob_task, reset_flaky_test
import os

router = APIRouter()

PROJECT_ROOT = os.path.expanduser("~/FlakyTestHunter")

class PipelineRequest(BaseModel):
    test_path: str = "sample-target/tests"

DETECTOR_PROMPT = """Act as a Flaky Test Detector subagent. Run the test suite in {path} 10 times in a row, activating the venv first as described in AGENTS.md.

For each test, report:
1. Test name
2. Pass/fail ratio across the 10 runs
3. Flag any test that did not return the same result every time

Do not diagnose or fix anything yet — just report the raw results."""

DIAGNOSIS_PROMPT = """Act as a Diagnosis subagent. Analyze the flaky test found in the previous step and the code it exercises.

Identify the root cause of the non-determinism. Explain in plain English why this test sometimes passes and sometimes fails, referencing the specific code causing it.

Do not fix the code yet — just diagnose."""

FIX_PROMPT = """Act as a Fix and Proof subagent. Based on the diagnosis, fix the flakiness by mocking the source of randomness to return a controlled, deterministic value.

After applying the fix, run the test 10 more times in a row and report the new pass/fail ratio. Confirm whether the test is now fully deterministic."""

@router.post("/run-pipeline")
def run_pipeline(req: PipelineRequest = PipelineRequest()):
    # Reset to original flaky state before each demo run
    reset_flaky_test(PROJECT_ROOT)

    detector_result = run_bob_task(DETECTOR_PROMPT.format(path=req.test_path), cwd=PROJECT_ROOT)
    diagnosis_result = run_bob_task(DIAGNOSIS_PROMPT, cwd=PROJECT_ROOT)
    fix_result = run_bob_task(FIX_PROMPT, cwd=PROJECT_ROOT)

    return {
        "detector": detector_result,
        "diagnosis": diagnosis_result,
        "fix_and_proof": fix_result,
    }

@router.get("/health")
def health():
    return {"status": "ok"}
