from tbtests.run_sysbench import SysbenchRun
import click
import shlex


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
        obj.run_sysbench(command_to_run=shlex.split(command_to_run))
    elif run:
        obj = SysbenchRun(defaults_file)
        command_to_run = obj.create_sysbench_command(sysbench_action="run")
        obj.run_sysbench(command_to_run=shlex.split(command_to_run))



if __name__ == "__main__":
    all_procedure()