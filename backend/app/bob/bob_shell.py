import subprocess
import os

BOB_PATH = "bob"

ORIGINAL_FLAKY_TEST = '''from app import process_order

def test_process_order_succeeds():
    result = process_order(101)
    assert result["status"] == "success"
'''

def reset_flaky_test(project_root: str):
    """Resets the sample test file to its original flaky state before each pipeline run."""
    test_file_path = os.path.join(project_root, "sample-target", "tests", "test_app.py")
    with open(test_file_path, "w") as f:
        f.write(ORIGINAL_FLAKY_TEST)

def run_bob_task(prompt: str, cwd: str, timeout: int = 300) -> dict:
    try:
        result = subprocess.run(
            [BOB_PATH, "run", "--accept-license", prompt],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": "Bob task timed out"}
    except Exception as e:
        return {"success": False, "output": "", "error": str(e)}
