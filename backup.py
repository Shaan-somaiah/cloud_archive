import zfs_snapshot

def main():

    print("Checking if there are existing managed snapshots")
    snapshot_list = zfs_snapshot.getSnapshot()

    if snapshot_list is not None:
        print("Existing managed snapshots found, deleting them : " + str(snapshot_list))
        zfs_snapshot.deleteSnapshot(snapshot_list)

    print("No existing managed snapshots found")


main()