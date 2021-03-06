from tbtests.run_sysbench import SysbenchRun
from tbtests.run_backup import BackupRun
import click
import shlex
from time import sleep
import threading


@click.command()
@click.option(
    '--backup',
    is_flag=True,
    help="Take backup"
)
@click.option(
    '--prepare',
    is_flag=True,
    help="Run sysbench prepare")

@click.option(
    '--run',
    is_flag=True,
    help="Run sysbench run"
)
@click.option(
    '--slave',
    is_flag = True,
    help="Use this option if you want to run backup against slave server"
)
@click.option(
    '--defaults_file',
    default='/etc/tokubackup.conf',
    help="Read options from the given file")

def all_procedure(backup, prepare, run, defaults_file, slave):
    if (not prepare) and (not defaults_file) and (not run):
        print("ERROR: you must give an option, run with --help for available options")
    elif prepare and (not backup):
        obj = SysbenchRun(defaults_file)
        command_to_run = obj.create_sysbench_command(sysbench_action="prepare")
        obj.run_sysbench_prepare(command_to_run=shlex.split(command_to_run))
    elif prepare and backup:
        obj = SysbenchRun(defaults_file)
        command_to_run = obj.create_sysbench_command(sysbench_action="prepare")
        obj.run_sysbench_prepare(command_to_run=shlex.split(command_to_run))
        sleep(5)
        print("WARN: starting backup process. This is not a multithreaded run, it is in loop")
        if not slave:
            backup_obj = BackupRun(defaults_file)
            for i in range(int(obj.tb_thread)):
                backup_obj.run_backup_with_output(backup_dir="thread_" + str(i))
        else:
            backup_obj = BackupRun(defaults_file)
            for i in range(int(obj.tb_thread)):
                backup_obj.run_backup_with_output(backup_dir="thread_" + str(i), server_v=1)
    elif run:
        obj = SysbenchRun(defaults_file)
        command_to_run = obj.create_sysbench_command(sysbench_action="run")
        obj.run_sysbench_run(command_to_run=shlex.split(command_to_run))
        sleep(5)
        backup_obj = BackupRun(defaults_file)
        print("WARN: starting backup process. This is a multithreaded run")
        workers = [threading.Thread(target=backup_obj.run_all(backup_dir="thread_"+str(i)), name="thread_"+str(i))
                   for i in range(int(obj.tb_thread))]
        [worker.start() for worker in workers]
        [worker.join() for worker in workers]




if __name__ == "__main__":
    all_procedure()