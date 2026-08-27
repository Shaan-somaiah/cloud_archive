## Env
zpools = [
    "dump"
]

dataset_root = "main"

datasets = {
    zpools[0] : {
        f"{dataset_root}/common",
        f"{dataset_root}/kube_vol",
        f"{dataset_root}/pbs_archive",
        f"{dataset_root}/pbs"
    }
}

datasets_to_archive   = [
    f"{dataset_root}/common",
    f"{dataset_root}/kube_vol",
    f"{dataset_root}/pbs"
]


datasets_to_replicate = [
    f"{dataset_root}/common",
    f"{dataset_root}/kube_vol",
    f"{dataset_root}/pbs",
    f"{dataset_root}/pbs_archive"
]

source_nas        = "nas"
destination_nas   = "nas-node2"

## Common naming prefixes
archive_name_prefix             = "archive"
archive_snapshot_name_prefix    = f"{archive_name_prefix}_managed_snapshot"
archive_clone_name_prefix       = f"{archive_name_prefix}_managed_clone"


replication_name_prefix                 = "replication"
replication_snapshot_name_prefix        = f"{replication_name_prefix}_managed_snapshot"
replication_snapshot_base_name_prefix   = f"{replication_snapshot_name_prefix}_base"
replication_snapshot_new_name_prefix    = f"{replication_snapshot_name_prefix}_new"
