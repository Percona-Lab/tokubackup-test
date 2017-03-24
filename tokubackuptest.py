from tbtests.run_sysbench import SysbenchRun
from tbtests.run_backup import BackupRun
import click
import shlex
from time import sleep
import threading


@click.command()
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
    '--defaults_file',
    default='/etc/tokubackup.conf',
    help="Read options from the given file")

def all_procedure(prepare, run, defaults_file):
    if (not prepare) and (not defaults_file) and (not run):
        print("ERROR: you must give an option, run with --help for available options")
    elif prepare:
        obj = SysbenchRun(defaults_file)
        command_to_run = obj.create_sysbench_command(sysbench_action="prepare")
        obj.run_sysbench_prepare(command_to_run=shlex.split(command_to_run))
    elif run:
        obj = SysbenchRun(defaults_file)
        command_to_run = obj.create_sysbench_command(sysbench_action="run")
        obj.run_sysbench_run(command_to_run=shlex.split(command_to_run))
        sleep(5)
        backup_obj = BackupRun(defaults_file)
        workers = [threading.Thread(target=backup_obj.run_all(), name="thread_"+str(i)) for i in range(0,100)]
        [worker.start() for worker in workers]
        [worker.join() for worker in workers]




if __name__ == "__main__":
    all_procedure()