from subprocess import Popen
from readconfig import config_reader


class SysbenchRun(config_reader.ConfigReader):

    def __init__(self, config):
        self.conf = config
        super().__init__(self.conf)


    def create_sysbench_command(self, sysbench_action):
        command = "sysbench  %s" \
                          " --mysql-db=%s " \
                          " --mysql-user=%s --mysql-password=%s --db-driver=mysql " \
                          " --max-requests=0  --mysql-socket=%s %s"
        general_command = (command) % (self.sysbench_options, self.sysbench_db,
                                       self.mysql_user, self.mysql_user,
                                       self.mysql_socket, sysbench_action)
        return general_command

    def run_sysbench(self, command_to_run):

        process = Popen(
            command_to_run,
            stdin=None,
            stdout=None,
            stderr=None)

