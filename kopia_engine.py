from config import kopia
import subprocess

def backup(snapshot):
    try:
        subprocess.run(
            [ kopia, "snapshot", "create", snapshot ],
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)