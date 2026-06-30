import zfs_snapshot
from config import zpools, snapshot_name_prefix
import lock
from datetime import datetime
import kopia


def main():
    lock.lock()

    try:
        for pool,datasets in zpools.items():
            print(f"Checking if there are existing managed snapshots for pool {pool}")
            snapshot_list = zfs_snapshot.getSnapshot(pool)

            if snapshot_list:
                print(f"Existing snapshots found: {snapshot_list}")
                zfs_snapshot.deleteSnapshot(snapshot_list)

        archive_paths = []

        for pool,datasets in zpools.items():
            for dataset in datasets:
                ## Not including timestamp in snapshot name as it creates a seperate chain in kopia
                snapshot_name = f"{snapshot_name_prefix}_{dataset}"
                full_dataset_path = f"{pool}/{dataset}"
                full_snapshot_name = f"{full_dataset_path}@{snapshot_name}"
                full_clone_name = f"{pool}/clone_{snapshot_name_prefix}_{dataset}"
                zfs_snapshot.takeSnapshot(full_snapshot_name)

                ## There seems to be some bug within kopia/zfs where kopia cannot enumerate the contents of snapshot directory within .zfs virual filesystem
                ## on the first attempt, this causes kopia to miss items during archival. Cloning the snapshot to a read only dataset will evade this issue as
                ## a read only dataset is mounted as a regular zfs filesystem

                zfs_snapshot.cloneSnapshot(full_snapshot_name, full_clone_name)
                archive_paths.append(f"/{full_clone_name}")
        

        for archive_path in archive_paths:
            kopia.archive(archive_path)

    finally:
        lock.unlock()

main()
