from config import kopia
import subprocess
import time

def archive(archive_path):
    try:

        # subprocess.run(
        #     [ kopia, "snapshot", "create", snapshot_path ],
        #     check=True,
        #     capture_output=True,
        #     text=True
        # )
    
        print(f"Inside kopia.archive, trying to run kopia snapshot create {archive_path}")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
