from config import zfs
from config import snapshot_name_prefix
import subprocess

def getSnapshot(pool):
    try:
        list_snapshot_result = subprocess.run(
            [ zfs, "list", "-H", "-o", "name", "-t", "snapshot", pool, "-r"],
            capture_output=True,
            text=True,
            check=True
        )

        if list_snapshot_result.stderr == "no datasets available\n":
            return None
        
        else:
            snapshots_list=[]
            for line in list_snapshot_result.stdout.splitlines():
                if snapshot_name_prefix in line:
                    snapshots_list.append(line)
            
            if len(snapshots_list) == 0: 
                print("No existing managed snapshot found")
            
            return snapshots_list
    
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
        return None


def deleteSnapshot(snapshot_list):

    for snapshot in snapshot_list:
        try:
            delete_snapshot_result = subprocess.run(
                [ zfs, "destroy", snapshot ],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("Deleted managed snapshot : " + snapshot)
        
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(e.stderr)
    
    print("No managed snapshots left to delete")


def takeSnapshot(full_snapshot_name):
    try:
        take_snapshot_result = subprocess.run(
            [ zfs, "snapshot", full_snapshot_name],
            capture_output=True,
            text=True,
            check=True
        )

        if take_snapshot_result.stdout == "":
            print(f"Took snapshot {full_snapshot_name} successfully")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
        return None
    