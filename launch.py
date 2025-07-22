import subprocess
import threading
import time

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "main.py"], cwd="app")

# Lancer Streamlit en arrière-plan
threading.Thread(target=run_streamlit).start()

# Pause pour laisser le temps de démarrer Streamlit
time.sleep(3)

# Lance Tauri
subprocess.call(["npm", "run", "tauri", "dev"])
