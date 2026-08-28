#!/usr/bin/env python3
import os
from zfs_utils import ZfsManager
import config
from cmd_runner import LocalCmdRunner
from kopia import KopiaManager
import lock

def MaybeDeleteExistingClones(zfs_manager, full_clone_name):

    print(f"Checking if there are existing clones for {full_clone_name}")

    clone_list = zfs_manager.GetDataset(full_clone_name)

    if not len(clone_list) == 0:
        filtered_clone_list = []
        for clone in clone_list:
            if not config.archive_clone_name_prefix in clone:
                clone_list.remove(clone)

    if not len(clone_list) == 0:
        for clone in clone_list:
            print(f"Found existing managed clone {clone}, deleting it")
            zfs_manager.Destroy(clone)
            print(f"Deleted {clone} successfully")
            return
    else:
        print(f"No existing managed clone found for {full_clone_name}")


def MaybeDeleteExistingSnapshots(zfs_manager, full_snapshot_name):

    print(f"Checking if there are existing snapshots for {full_snapshot_name}")

    snapshot_list = zfs_manager.GetSnapshot(full_snapshot_name)

    print(f"List = {snapshot_list}")

    if not len(snapshot_list) == 0:
        filtered_snapshot_list = []
        for snapshot in snapshot_list:
            if not config.archive_snapshot_name_prefix in snapshot:
                snapshot_list.remove(snapshot)

    if not len(snapshot_list) == 0:
        for snapshot in snapshot_list:
            print(f"Found existing managed snapshot {snapshot}, deleting it")
            zfs_manager.Destroy(snapshot)
            print(f"Deleted {snapshot} successfully")
            return
    else:
        print(f"No existing managed snapshot found for {full_snapshot_name}")


def main():

    ## Lock so only one instance of this script runs at time
    executable_name = os.path.basename(__file__)
    lock.Lock(executable_name)
    print()

    ## Helpers to run local and remote command via ssh
    local_cmd_runner  = LocalCmdRunner()

    ## zfs helper, takes a cmd runner
    zfs_local_manager  = ZfsManager(local_cmd_runner)

    ## kopia helper
    kopia_local_helper = KopiaManager(local_cmd_runner)

    for zpool, datasets in config.datasets.items():
        for dataset in datasets:
            if dataset in config.datasets_to_archive:

                ## Generate names
                full_dataset_name   = f"{zpool}/{dataset}"
                full_snapshot_name  = f"{full_dataset_name}@{config.archive_snapshot_name_prefix}"
                full_clone_name     = f"{full_dataset_name}_{config.archive_clone_name_prefix}"

                ## Prearchival tasks
                MaybeDeleteExistingClones(zfs_local_manager, full_clone_name)
                print()
                MaybeDeleteExistingSnapshots(zfs_local_manager, full_snapshot_name)
                print()

                zfs_local_manager.CreateSnapshot(full_snapshot_name)
                print(f"Created snapshot {full_snapshot_name}")
                print()

                ## Clone snapshot to a readonly clone, sometimes kopia cannot enumerate snapshot within .zfs directly
                zfs_local_manager.Clone(full_snapshot_name, full_clone_name)
                print(f"Cloned {full_snapshot_name} to {full_clone_name}")
                print()
                zfs_local_manager.MarkReadOnly(full_clone_name)
                print(f"Marked {full_clone_name} as read only")
                print()


                ## Archival task
                print(f"Going to archive {full_clone_name}")
                print()
                ## Kopia takes filesystem path as parameter
                kopia_local_helper.CreateSnapshot(f"/{full_clone_name}")

                ## Post archival task
                MaybeDeleteExistingClones(zfs_local_manager, full_clone_name)   
                print()
                MaybeDeleteExistingSnapshots(zfs_local_manager, full_snapshot_name)
                print()

    lock.Unlock()

if __name__ == "__main__":
    main()
