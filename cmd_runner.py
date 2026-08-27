import subprocess
import sys
from abc import ABC, abstractmethod


## ICommandRunner provides an interface to call both local command runner and remote command runner (via ssh)
## Force all child classes to implement atleast RunCmd() via abstractmethod
class ICmdRunner(ABC):

    @abstractmethod
    def RunCmd(self, command: list[str]) -> subprocess.CompletedProcess :
        pass


## Run commands on the machine which invokes the methods
class LocalCmdRunner(ICmdRunner):

## No need for explict constructor
    def RunCmd(self, command: list[str]) -> subprocess.CompletedProcess:

        return subprocess.run (
            command,
            capture_output=True,
            text=True,
            check=True
        )


## Run commands on a remote machine via ssh
class RemoteCmdRunner(ICmdRunner):

    ssh_exec = "/usr/bin/ssh"

    def __init__(self, remote_host, username = "shaan"):

        if remote_host == "":
            print(f"Remote host not supplied, panic!")
            sys.exit(3)

        self.remote_host = remote_host
        self.username = username


    def RunCmd(self, command: list[str]) -> subprocess.CompletedProcess:

        return subprocess.run (
            [ self.ssh_exec, f"{self.username}@{self.remote_host}", *command ],
            capture_output=True,
            text=True,
            check=True
        )
