import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.orchestrator import run_orchestration

if __name__ == "__main__":
    run_orchestration()
