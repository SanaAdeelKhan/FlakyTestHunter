from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
import os
import shutil
from app.bob.bob_shell import run_bob_task

router = APIRouter()

DETECTOR_PROMPT = """Act as a Flaky Test Detector subagent. The file to analyze is at {path}.

Run any tests in this file 10 times in a row if it contains pytest tests. If it's a standalone script with no tests, analyze it for potential non-determinism instead (unseeded random calls, time-based branching, network calls without mocking, etc).

Report:
1. What you found
2. Whether it's flaky/non-deterministic and why

Do not fix anything yet — just report."""

DIAGNOSIS_PROMPT = """Act as a Diagnosis subagent. Analyze the file at {path} based on the previous step's findings.

Identify the exact root cause of any non-determinism, referencing specific line numbers and code.

Do not fix the code yet — just diagnose."""

FIX_PROMPT = """Act as a Fix and Proof subagent. Based on the diagnosis, fix the file at {path} to eliminate any non-determinism (e.g. by mocking randomness, seeding, or removing uncontrolled external dependencies).

After applying the fix, re-run any tests 10 times if applicable and report the pass/fail ratio. Confirm the fix worked."""

@router.post("/upload-and-fix")
async def upload_and_fix(file: UploadFile = File(...)):
    if not file.filename.endswith(".py"):
        return JSONResponse(status_code=400, content={"error": "Only .py files are supported."})

    tmp_dir = tempfile.mkdtemp(prefix="flaky_upload_")
    file_path = os.path.join(tmp_dir, file.filename)

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        detector_result = run_bob_task(DETECTOR_PROMPT.format(path=file_path), cwd=tmp_dir)
        diagnosis_result = run_bob_task(DIAGNOSIS_PROMPT.format(path=file_path), cwd=tmp_dir)
        fix_result = run_bob_task(FIX_PROMPT.format(path=file_path), cwd=tmp_dir)

        fixed_content = None
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                fixed_content = f.read()

        return {
            "detector": detector_result,
            "diagnosis": diagnosis_result,
            "fix_and_proof": fix_result,
            "fixed_file_content": fixed_content,
            "fixed_filename": file.filename,
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
