from general_conf.generalops import GeneralClass
import configparser
import test


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