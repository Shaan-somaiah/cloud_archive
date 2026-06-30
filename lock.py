import os
import sys
from pathlib import Path

lock_file = Path("/var/lock/kopia_backup.lock")

def lock():

    if not lock_file.exists():
        print(f"Backup script not running, locking run with PID {str(os.getpid())}")
        lock_file.write_text(str(os.getpid()))
        print("Run locked")
    
    else:
        current_pid = os.getpid()
        lock_file_pid = int(lock_file.read_text())

        if current_pid != lock_file_pid:
            if Path(f"/proc/{lock_file_pid}/").exists():
                if "kopia_backup.py" in Path(f"/proc/{lock_file_pid}/cmdline").read_text():
                    print(f"Backup script already running with {lock_file_pid}, exiting this instance")
                    sys.exit(3)
        
        print(f"Stale lock file with PID {lock_file_pid} detected, force locking")
        lock_file.write_text(str(current_pid))
        print("Run locked")
                

def unlock():

    if not lock_file.exists():
        print("Lock file missing, panic")
        sys.exit(3)

    lock_file_pid = int(lock_file.read_text())
    current_pid = os.getpid()
    if current_pid != lock_file_pid:
        print(f"Cannot unlock unknown PID {lock_file_pid}")
        sys.exit(1)
    
    lock_file.unlink()
    