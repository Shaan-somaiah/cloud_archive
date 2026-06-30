import zfs_snapshot
from config import zpools, snapshot_name_prefix
import lock
from datetime import datetime
import kopia_engine


def main():
    lock.lock()

    try:
        for pool,datasets in zpools.items():
            print(f"Checking if there are existing managed snapshots for pool {pool}")
            snapshot_list = zfs_snapshot.getSnapshot(pool)

            if snapshot_list:
                print(f"Existing snapshots found: {snapshot_list}")
                zfs_snapshot.deleteSnapshot(snapshot_list)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshots_to_backup = []

        for pool,datasets in zpools.items():
            for dataset in datasets:
                snapshot_name = f"{snapshot_name_prefix}_{dataset}_{current_time}"
                full_dataset_path = f"{pool}/{dataset}"
                full_snapshot_name = f"{full_dataset_path}@{snapshot_name}"
                zfs_snapshot.takeSnapshot(full_snapshot_name)
                snapshots_to_backup.append(f"/{full_dataset_path}/.zfs/snapshot/{snapshot_name}")

        for snapshot_path in snapshots_to_backup:
            kopia_engine.backup(snapshot_path)

    finally:
        lock.unlock()

main()
