import os
import sys

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(PROJECT_FOLDER, "backend"))
sys.path.insert(0, os.path.join(PROJECT_FOLDER, "frontend"))

import setup_check
setup_check.run_all_checks()

import frontend
frontend.run_app()