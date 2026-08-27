zpools_archive = {
    "dump/main": [
        "common",
        "kube_vol",
        "pbs_archive"
    ]
}

zpools_replicate = {
    "dump/main": [
        "common",
        "kube_vol",
        "pbs_archive",
        "pbs"
    ]
}

kopia = "/usr/bin/kopia"
rclone = "/usr/bin/rclone"
zfs = "/usr/sbin/zfs"

snapshot_name_prefix = "kopia_managed"
clone_name_prefix = "clone_kopia_managed"

replicate_name_prefix = "replicate_managed"
