from general_conf.generalops import GeneralClass
import configparser


class ConfigReader(GeneralClass):
    def __init__(self, config):
        self.conf = config
        super().__init__(self.conf)

        con = configparser.ConfigParser()
        con.read(self.conf)

        ######################################################
        STRESS = con['Stress']
        if 'stress' in STRESS:
            self.stress = STRESS['stress']
        if 'tb_thread' in STRESS:
            self.tb_thread = STRESS['tb_thread']
        if 'sysbench_options' in STRESS:
            self.sysbench_options = STRESS['sysbench_options']
        if 'sysbench_db' in STRESS:
            self.sysbench_db = STRESS['sysbench_db']
        ######################################################
        SLAVE = con['Slave']
        if 'mysql' in SLAVE:
            self.mysql_slv = SLAVE['mysql']
        if 'user' in SLAVE:
            self.user_slv = SLAVE['user']
        if 'password' in SLAVE:
            self.password_slv = SLAVE['password']
        if 'port' in SLAVE:
            self.port_slv = SLAVE['port']
        if 'socket' in SLAVE:
            self.socket_slv = SLAVE['socket']
        if 'host' in SLAVE:
            self.host_slv = SLAVE['host']
        if 'datadir' in SLAVE:
            self.datadir_slv = SLAVE['datadir']