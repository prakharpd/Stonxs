import os
import subprocess
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, ".venv")
REQUIREMENTS_FILE = os.path.join(PROJECT_DIR, "requirements.txt")

REQUIRED_FILES = [
    "app.py",
    "backend/tools.py",
    "backend/stock_agents.py",
    "backend/security.py",
]


def check_venv():
    if os.path.isdir(VENV_DIR):
        print("[OK] .venv found.")
    else:
        print("[SETUP] Creating .venv...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)


def check_requirements():
    if os.path.isfile(REQUIREMENTS_FILE):
        print("[SETUP] Installing requirements...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE],
            check=True,
        )


def check_project_files():
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(os.path.join(PROJECT_DIR, f))]
    if missing:
        raise FileNotFoundError(f"Missing files: {', '.join(missing)}")
    print("[OK] All required files found.")


def run_all_checks():
    print("Running startup checks...")
    check_venv()
    check_requirements()
    check_project_files()
    print("Startup checks complete.")