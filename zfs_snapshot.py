from config import zfs
from config import snapshot_name_prefix
import subprocess

def getSnapshot():
    try:
        list_snapshot_result = subprocess.run(
            [ zfs, "list", "-t", "snapshot"],
            capture_output=True,
            text=True,
            check=True
        )

        list_snapshot_results = [list_snapshot_result.stdout, list_snapshot_result.stderr]

        if list_snapshot_results[1] == "no datasets available\n":
            return None
        
        else:
            snapshots_list=[]
            lines = list_snapshot_results[0].splitlines()
            for line in lines:
                if "dump" in line and "@" in line:
                    snapshot_name = line.split()
                    snapshots_list.append(snapshot_name[0])
            
            return snapshots_list
    
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
        return None


def deleteSnapshot(snapshot_list):

    for snapshot in snapshot_list:
        try:
            if "@" not in snapshot or snapshot_name_prefix not in snapshot:
                print(f"Refusing to destroy unmanaged snapshot: {snapshot}")
                continue
            delete_snapshot_result = subprocess.run(
                [ zfs, "destroy", snapshot ],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("Deleted " + snapshot)
        
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(e.stderr)
    