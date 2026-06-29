## Create zfs snapshot of my datasets and backup to kopia

import subprocess

datasets = ["pbs", "kube_vol", "common"]
dataset_root_path = "/dump/main/"
kopia = "/usr/bin/kopia"
rclone = "/usr/bin/rclone"
zfs = "/usr/sbin/zfs"

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
            print("No snapshots found")
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


