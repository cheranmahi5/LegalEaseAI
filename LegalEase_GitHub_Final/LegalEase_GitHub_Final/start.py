import os
import subprocess
import sys
import time

root = os.path.dirname(os.path.abspath(__file__))
backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"], cwd=root)
time.sleep(1)
try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], cwd=root, check=False)
finally:
    backend.terminate()
