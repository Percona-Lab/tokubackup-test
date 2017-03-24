from backup.backup_calculation import CheckMySQLEnvironment
from os import makedirs
from os.path import join
from datetime import datetime
from threading import Lock

class BackupRun(CheckMySQLEnvironment):
    def __init__(self, config):
        self.conf = config
        super().__init__(self.conf)
        self.mutex = Lock()

    def create_backup_directory(self):
        """
                Creating timestamped backup directory.
                :return: Newly created backup directory or Error.
                """
        new_backup_dir = join(self.backupdir,
                              datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        try:
            # Creating backup directory
            makedirs(new_backup_dir)
            return new_backup_dir
        except Exception as err:
            print("Something went wrong in create_backup_directory(): {}".format(err))


    def run_all(self):
        self.mutex.acquire(1)
        backupdir = self.create_backup_directory()
        self.run_backup(backup_dir=backupdir)
        self.mutex.release()