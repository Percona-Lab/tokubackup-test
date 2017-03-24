from backup.backup_calculation import CheckMySQLEnvironment
from os import makedirs
from os.path import join

class BackupRun(CheckMySQLEnvironment):
    def __init__(self, config):
        self.conf = config
        super().__init__(self.conf)


    def create_backup_directory(self, backup_dir):
        """
                Creating timestamped backup directory.
                :return: Newly created backup directory or Error.
                """
        # new_backup_dir = join(self.backupdir,
        #                       datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        new_backup_dir = join(self.backupdir, backup_dir)
        try:
            # Creating backup directory
            makedirs(new_backup_dir)
            return new_backup_dir
        except Exception as err:
            print("Something went wrong in create_backup_directory(): {}".format(err))


    def run_all(self, backup_dir):
        backupdir = self.create_backup_directory(backup_dir=backup_dir)
        self.run_backup(backup_dir=backupdir)