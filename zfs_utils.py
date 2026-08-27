from cmd_runner import ICmdRunner
import subprocess

## This class provides methods to interact with zfs
## ICmdRunner is depedency injected to run local and remote commands abstractly

class ZfsManager():

    zfs_exec = "/usr/bin/zfs"


    def __init__(self, cmd_runner: ICmdRunner):
        self.cmd_runner = cmd_runner


    def GetSnapshot(self, full_dataset_name):

        command = [ self.zfs_exec, "list", "-H", "-o", "name", "-t", "snapshot", full_dataset_name ]
        
        try:
            result = self.cmd_runner.RunCmd(command)

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
