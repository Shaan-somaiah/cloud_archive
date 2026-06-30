import zfs_snapshot
import lock
import time


def main():
    lock.lock()

    try:
        print("Checking if there are existing managed snapshots")
        snapshot_list = zfs_snapshot.getSnapshot()

        if snapshot_list:
            print(f"Existing snapshots found: {snapshot_list}")
            zfs_snapshot.deleteSnapshot(snapshot_list)

    finally:
        lock.unlock()

main()
