from backup.backup_calculation import CheckMySQLEnvironment
from os import makedirs
from os.path import join
import shlex
import subprocess

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

    def run_backup_with_output(self, backup_dir):
        backupdir = self.create_backup_directory(backup_dir=backup_dir)
        """
            Running actual backup command to MySQL server.
            :param backup_dir:
        """

        backup_command_connection = '{} -u{} --password={} --host={}'
        backup_command_execute = ' -e "set tokudb_backup_dir=\'{}\'"'

        try:

            if hasattr(self, 'mysql_socket'):
                backup_command_connection += ' --socket={}'
                backup_command_connection += backup_command_execute
                new_backup_command = backup_command_connection.format(
                        self.mysql,
                        self.mysql_user,
                        self.mysql_password,
                        self.mysql_host,
                        self.mysql_socket,
                        backupdir)
            else:
                backup_command_connection += ' --port={}'
                backup_command_connection += backup_command_execute
                new_backup_command = backup_command_connection.format(
                        self.mysql,
                        self.mysql_user,
                        self.mysql_password,
                        self.mysql_host,
                        self.mysql_port,
                        backupdir)
            # Do not return anything from subprocess
            print(
                "Running backup command => %s" %
                (''.join(new_backup_command)))

            status, output = subprocess.getstatusoutput(new_backup_command)
            if status == 0:
                print("Backup completed!")
            else:
                print("Backup failed!")
                print(output)

        except Exception as err:
            print("Something went wrong in run_backup(): {}".format(err))
