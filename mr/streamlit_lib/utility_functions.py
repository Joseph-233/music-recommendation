import subprocess
import logging

def run_script(script_path):
    result = subprocess.run(
        ["python", script_path], capture_output=True, text=True
    )
    return (result.stdout, result.stderr) if result.returncode == 0 else (None, result.stderr)

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="a",
        format="%(name)s - %(levelname)s - %(message)s"
    )