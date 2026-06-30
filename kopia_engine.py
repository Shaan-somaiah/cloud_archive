from config import kopia
import subprocess
import time

def backup(snapshot_path):
    try:

        subprocess.run(
            [ kopia, "snapshot", "create", snapshot_path ],
            check=True,
            capture_output=True,
            text=True
        )
    

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
