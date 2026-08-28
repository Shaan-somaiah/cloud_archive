from cmd_runner import ICmdRunner
import subprocess

class KopiaManager():

    kopia_exec = "/usr/bin/kopia"

    def __init__(self, cmd_runner: ICmdRunner):
        self.cmd_runner = cmd_runner

    def CreateSnapshot(self, full_snapshot_path):

        command = [ self.kopia_exec, "snapshot", "create", full_snapshot_path ]

        try:
            result = self.cmd_runner.RunCmd(command)

            if result.returncode == 0:
                return True

            return False

        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(e.stderr)
            return False
