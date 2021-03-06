from subprocess import Popen, getstatusoutput
from readconfig import config_reader


class SysbenchRun(config_reader.ConfigReader):
    def __init__(self, config):
        self.conf = config
        super().__init__(self.conf)

    def create_mysql_client_command(self, statement):
        """Creating mysql client command for executing sql statements"""
        command_connection = '{} -u{} --password={} --host={}'
        command_execute = ' -e "{}"'

        if hasattr(self, 'mysql_socket'):
            command_connection += ' --socket={}'
            command_connection += command_execute
            new_command = command_connection.format(
                self.mysql,
                self.mysql_user,
                self.mysql_password,
                self.mysql_host,
                self.mysql_socket,
                statement
            )
            return new_command
        else:
            command_connection += ' --port={}'
            command_connection += command_execute
            new_command = command_connection.format(
                self.mysql,
                self.mysql_user,
                self.mysql_password,
                self.mysql_host,
                self.mysql_port,
                statement
            )

        return new_command

    def check_sysbench_database(self):
        """Check if sysbench database exists or not"""

        execute = "SELECT count(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{}'"

        if hasattr(self, 'sysbench_db'):
            command = self.create_mysql_client_command(execute.format(self.sysbench_db))
            print(command)
            status, output = getstatusoutput(command)

            if status == 0 and "0" in output:
                print("There is no such database!")
                return 1
            elif status == 0 and "1" in output:
                print("The specified database already there!")
                return 2
            else:
                print("Error while checking database!")
                print(output)
                return False
        else:
            command = self.create_mysql_client_command(execute.format('sbtest'))
            status, output = getstatusoutput(command)

            if status == 0 and "0" in output:
                print("There is no such database!")
                return 1
            elif status == 0 and "1" in output:
                print("The specified database already there!")
                return 2
            else:
                print("Error while checking database!")
                print(output)
                return False


    def drop_sysbench_db(self, db):
        execute_drop = "drop database {}"
        command = self.create_mysql_client_command(execute_drop.format(db))
        status, output = getstatusoutput(command)

        if status == 0:
            print("Database Droppped!")
            return True
        else:
            print("Failed to drop specified database!")
            print(output)
            return False


    def create_sysbench_db(self):
        """Creating sysbench database; specified one or default 'sbtest'"""

        execute_create = "create database {}"
        status_db = self.check_sysbench_database()
        if status_db == 1:
            if hasattr(self, 'sysbench_db'):

                status, output = getstatusoutput(
                    self.create_mysql_client_command(execute_create.format(self.sysbench_db)))

                if status == 0:
                    print("Database Created!")
                    return True
                else:
                    print("Failed to create specified database!")
                    print(output)
                    return False
            else:
                status, output = getstatusoutput(
                    self.create_mysql_client_command(execute_create.format('sbtest')))

                if status == 0:
                    print("Database Created!")
                    return True
                else:
                    print("Failed to create specified database!")
                    print(output)
                    return False
        elif status_db == 2:
            if hasattr(self, 'sysbench_db'):
                # Droppping database before creating
                self.drop_sysbench_db(self.sysbench_db)

                status, output = getstatusoutput(
                    self.create_mysql_client_command(execute_create.format(self.sysbench_db)))

                if status == 0:
                    print("Database Created!")
                    return True
                else:
                    print("Failed to create specified database!")
                    print(output)
                    return False
            else:
                # Droppping database before creating
                self.drop_sysbench_db('sbtest')

                status, output = getstatusoutput(
                    self.create_mysql_client_command(execute_create.format('sbtest')))

                if status == 0:
                    print("Database Dropped!")
                    return True
                else:
                    print("Failed to drop specified database!")
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

    def run_sysbench_prepare(self, command_to_run):
        """Running sysbench with prepare"""
        print("The following command will be executed -> %s" % command_to_run)
        if self.create_sysbench_db():
            process = Popen(
                command_to_run,
                stdin=None,
                stdout=None,
                stderr=None)

    def run_sysbench_run(self, command_to_run):
        """Running sysbench with run"""
        print("The following command will be executed -> %s" % command_to_run)
        process = Popen(
            command_to_run,
            stdin=None,
            stdout=None,
            stderr=None)
