import zfs_snapshot
from config import zpools, snapshot_name_prefix, clone_name_prefix
import lock
from datetime import datetime
import kopia


def main():
    lock.lock()
    print()

    try:

        created_snapshots_list = []
        created_clones_list = []
        
        for pool,datasets in zpools.items():
            print(f"Checking if there are existing managed clones for pool {pool}")
            clone_list = zfs_snapshot.getClone(pool)

            if clone_list:
                print(f"Existing clones found: {clone_list}")
                zfs_snapshot.destroy(clone_list)
        print()

        for pool,datasets in zpools.items():
            print(f"Checking if there are existing managed snapshots for pool {pool}")
            snapshot_list = zfs_snapshot.getSnapshot(pool)

            if snapshot_list:
                print(f"Existing snapshots found: {snapshot_list}")
                zfs_snapshot.destroy(snapshot_list)
        print()

        archive_paths = []

        for pool,datasets in zpools.items():
            for dataset in datasets:
                ## Not including timestamp in snapshot name as it creates a seperate chain in kopia
                snapshot_name = f"{snapshot_name_prefix}_{dataset}"
                full_dataset_path = f"{pool}/{dataset}"
                full_snapshot_name = f"{full_dataset_path}@{snapshot_name}"
                full_clone_name = f"{pool}/{clone_name_prefix}_{dataset}"
                zfs_snapshot.createSnapshot(full_snapshot_name)
                created_snapshots_list.append(full_snapshot_name)
                ## There seems to be some bug within kopia/zfs where kopia cannot enumerate the contents of snapshot directory within .zfs virual filesystem
                ## on the first attempt, this causes kopia to miss items during archival. Cloning the snapshot to a read only dataset will evade this issue as
                ## a read only dataset is mounted as a regular zfs filesystem

                zfs_snapshot.cloneSnapshot(full_snapshot_name, full_clone_name)
                created_clones_list.append(full_clone_name)
                archive_paths.append(f"/{full_clone_name}")
                print()
        
        results_vec = []

        for archive_path in archive_paths:
            result = kopia.archive(archive_path)
            results_vec.append(result)

            print(f"Done archiving {archive_path} in {result['time_elapsed']:.2f}s")
            print(f"Kopia stdout:\n{result['stdout']}")
            print()


    finally:

        if created_clones_list:
            zfs_snapshot.destroy(created_clones_list)
        print()
        
        if created_snapshots_list:
            zfs_snapshot.destroy(created_snapshots_list)
        print()

        lock.unlock()

main()
