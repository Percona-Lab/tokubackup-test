from subprocess import Popen, getstatusoutput
from readconfig import config_reader


class SysbenchRun(config_reader.ConfigReader):

    def __init__(self, config):
        self.conf = config
        super().__init__(self.conf)

    def create_sysbench_db(self):
        backup_command_connection = '{} -u{} --password={} --host={}'
        execute = " -e 'create database {}'"
        if hasattr(self, 'sysbench_db'):
            new_command = backup_command_connection.format(
                            self.mysql,
                            self.mysql_user,
                            self.mysql_password,
                            self.mysql_host) + execute.format(self.sysbench_db)
            status, output = getstatusoutput(new_command)

            if status == 0:
                print("Database Created!")
                return True
            else:
                print("Failed to create specified database!")
                print(output)
                return False
        else:
            new_command = backup_command_connection.format(
                self.mysql,
                self.mysql_user,
                self.mysql_password,
                self.mysql_host) + execute.format('sbtest')
            status, output = getstatusoutput(new_command)

            if status == 0:
                print("Database Created!")
                return True
            else:
                print("Failed to create specified database!")
                print(output)
                return False





    def create_sysbench_command(self, sysbench_action):
        command = "sysbench  %s" \
                          " --mysql-db=%s " \
                          " --mysql-user=%s --mysql-password=%s --db-driver=mysql " \
                          " --max-requests=0  --mysql-socket=%s %s"
        general_command = (command) % (self.sysbench_options, self.sysbench_db,
                                       self.mysql_user, self.mysql_password,
                                       self.mysql_socket, sysbench_action)
        return general_command

    def run_sysbench(self, command_to_run):

        if self.create_sysbench_db():
            process = Popen(
                command_to_run,
                stdin=None,
                stdout=None,
                stderr=None)

