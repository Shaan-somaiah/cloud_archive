from cmd_runner import ICmdRunner
import subprocess

## This class provides methods to interact with zfs
## ICmdRunner is depedency injected to run local and remote commands abstractly

class ZfsManager():

    zfs_exec = "/usr/bin/zfs"


    def __init__(self, cmd_runner: ICmdRunner):
        self.cmd_runner = cmd_runner

###
    def GetSnapshot(self, full_dataset_name):

        command = [ self.zfs_exec, "list", "-H", "-o", "name", "-t", "snapshot", full_dataset_name ]
        
        try:
            result = self.cmd_runner.RunCmd(command)
            # print(result.stdout)

            if "dataset does not exist" in result.stderr:
                print(f"Dataset supplied does not exist!")
                return None

            snapshots_list=[]
            for line in result.stdout.splitlines():
                snapshots_list.append(line)

            if len(snapshots_list) == 0:
                print(f"No snapshots found for dataset {full_dataset_name}")
                return None

            return snapshots_list

        except subprocess.CalledProcessError as e:
            print(f"GetSnapshot failed for {full_dataset_name} with return code {e.returncode}")
            print(e.stderr)
            return None

###
    def GetDataset(self, zpool):

        command = [ self.zfs_exec, "list", "-H", "-o", "name", zpool, "-r" ]

        try:
            result = self.cmd_runner.RunCmd(command)
            # print(result.stdout)

            if "zpool does not exist" in result.stderr:
                print(f"zpool supplied does not exist!")
                return None

            dataset_list=[]
            for line in result.stdout.splitlines():
                dataset_list.append(line)

            if len(dataset_list) == 0:
                print(f"No datasets found for pool {zpool}")
                return None

            return dataset_list

        except subprocess.CalledProcessError as e:
            print(f"GetDatasets failed for {zpool} with return code {e.returncode}")
            print(e.stderr)
            return None

###
    def Destroy(self, full_dataset_name):

        command = [ self.zfs_exec, "destroy", full_dataset_name ]

        try:
            print(f"Destroying dataset {full_dataset_name} !!")
            result = self.cmd_runner.RunCmd(command)

            if result.returncode == 0:
                return True

            return False

        except subprocess.CalledProcessError as e:
            print(f"Destroy dataset {full_dataset_name} failed with return code {e.returncode}")
            print(e.stderr)
            return None


###
    def CreateSnapshot(self, full_snapshot_name):

        command = [ self.zfs_exec, "snapshot", full_snapshot_name ]

        try:
            result = self.cmd_runner.RunCmd(command)

            if result.returncode == 0:
                return True

            return False

        except subprocess.CalledProcessError as e:
            print(f"CreateSnapshot {full_snapshot_name} failed with return code {e.returncode}")
            print(e.stderr)
            return None

###
    def Clone(self, full_source_dataset_name, full_destination_dataset_name):

        command = [ self.zfs_exec, "clone", full_source_dataset_name, full_destination_dataset_name ]

        try:
            result = self.cmd_runner.RunCmd(command)

            if result.returncode == 0:
                return True

            return False

        except subprocess.CalledProcessError as e:
            print(f"Cloning {full_source_dataset_name} to {full_destination_dataset_name} failed with return code {e.returncode}")
            print(e.stderr)
            return None

###
    def Rename(self, full_source_dataset_name, full_destination_dataset_name):

        command = [ self.zfs_exec, "rename", full_source_dataset_name, full_destination_dataset_name ]

        try:
            result = self.cmd_runner.RunCmd(command)

            if result.returncode == 0:
                return True

            return False

        except subprocess.CalledProcessError as e:
            print(f"Renaming {full_source_dataset_name} to {full_destination_dataset_name} failed with return code {e.returncode}")
            print(e.stderr)
            return None

### Something to do send / recieve
