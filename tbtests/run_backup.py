from backup.backup_calculation import CheckMySQLEnvironment

class BackupRun(CheckMySQLEnvironment):
    def __init__(self, config):
        self.conf = config
        self.conf = config
        super().__init__(self.conf)

    def run_all(self):
        backupdir = self.create_backup_directory()
        self.run_backup(backup_dir=backupdir)
