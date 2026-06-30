import zfs_snapshot
from config import datasets, dataset_root_paths, snapshot_name_prefix
import lock
from datetime import datetime

def main():
    lock.lock()

    try:
        print("Checking if there are existing managed snapshots")
        snapshot_list = zfs_snapshot.getSnapshot()

        if snapshot_list:
            print(f"Existing snapshots found: {snapshot_list}")
            zfs_snapshot.deleteSnapshot(snapshot_list)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        for dataset_root_path in dataset_root_paths:
            for dataset in datasets:
                full_snapshot_name = f"{snapshot_name_prefix}_{dataset}_{current_time}"
                full_dataset = f"{dataset_root_path}{dataset}"
                print(f"Trying to take snapshot for dataset {full_dataset}")
                zfs_snapshot.takeSnapshot(full_dataset, full_snapshot_name)

    finally:
        lock.unlock()

main()
