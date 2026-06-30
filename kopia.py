from config import kopia
import subprocess
import time

def archive(archive_path):
    try:
        
        star_time = time.perf_counter()
        print(f"Starting archive of {archive_path}")

        archive_result = subprocess.run(
            [ kopia, "snapshot", "create", archive_path ],
            check=True,
            capture_output=True,
            text=True
        )

        end_time = time.perf_counter()      
    
        result_vec = {
            "dataset_name": archive_path,
            "time_elapsed": end_time - star_time,
            "stdout" : archive_result.stdout,
            "stderr" : archive_result.stderr,
            "returncode" : archive_result.returncode
        }

        return result_vec
        # print(f"Inside kopia.archive, trying to run kopia snapshot create {archive_path}")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
