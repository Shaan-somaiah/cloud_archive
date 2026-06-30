from config import zfs
from config import snapshot_name_prefix, clone_name_prefix
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


def getClone(pool):
    try:
        list_clone_result = subprocess.run(
            [ zfs, "list", "-H", "-o", "name", pool, "-r"],
            capture_output=True,
            text=True,
            check=True
        )

        if list_clone_result.stderr == "no datasets available\n":
            return None
        
        else:
            clone_list=[]
            for line in list_clone_result.stdout.splitlines():
                if clone_name_prefix in line:
                    clone_list.append(line)
            
            if len(clone_list) == 0: 
                print("No existing managed clones found")
            
            return clone_list
    
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
        return None

def destroy(dataset_list):

    # for snapshot in snapshot_list:
    #     print(f"Inside deleteSnapshot, trying to delete {snapshot}")
    for dataset in dataset_list:
        try:
            delete_dataset_result = subprocess.run(
                [ zfs, "destroy", dataset ],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("Deleted managed dataset : " + dataset)
        
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(e.stderr)
    
    print("No managed dataset left to delete")


def createSnapshot(full_snapshot_name):

    # print(f"Inside takeSnapshot, trying to take snapshot {full_snapshot_name}")

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
    
def cloneSnapshot(full_snapshot_name, full_clone_name):

    # print(f"Inside cloneSnapshot, trying to clone {full_snapshot_name} to {full_clone_name}")
    try:
        clone_snapshot_result = subprocess.run(
            [ zfs, "clone", full_snapshot_name, full_clone_name],
            capture_output=True,
            text=True,
            check=True
        )

        print(f"Cloned snapshot {full_snapshot_name} to {full_clone_name} successfully")


        ## mark cloned dataset as read only
        mark_snapshot_read_only_result = subprocess.run(
            [ zfs, "set", "readonly=on", full_clone_name],
            capture_output=True,
            text=True,
            check=True
        )

        print(f"Marked clone {full_clone_name} as read only successfully")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
        return None
    