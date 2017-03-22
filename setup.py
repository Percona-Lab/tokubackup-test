from setuptools import setup

datafiles = [('/etc', ['readconfig/tokubackuptest.conf'])]

setup(
    name='tokubackuptest',
    version='1.0',
    packages=['readconfig', 'test'],
    py_modules=['tokubackuptest'],
    url='https://github.com/Percona-Lab/tokubackup-test',
    download_url='https://github.com/Percona-Lab/tokubackup-test/archive/v1.0.tar.gz',
    license='GPL',
    author='Shahriyar Rzayev',
    author_email='shahriyar.rzayev@percona.com',
    description='Commandline tool written in Python3 for using Percona TokuBackup test',
    entry_points='''
        [console_scripts]
        tokubackuptest=tokubackuptest:all_procedure
    ''',
    data_files=datafiles,
)
