from pathlib import Path


datasets = [ "pbs",
             "kube_vol",
             "common"
            ]

dataset_root_path = Path("/dump/main/")

kopia = "/usr/bin/kopia"
rclone = "/usr/bin/rclone"
zfs = "/usr/sbin/zfs"

snapshot_name_prefix = "kopia_scheduled_"