from fabric.api import task, run, sudo, parallel

# http://docs.fabfile.org/en/1.10/api/core/operations.html#fabric.operations.run

@task
def run_command_sync(command):
    return run(command)

@task
@parallel
def run_command_parallel(command):
    return run(command)

@task
def sudo_run_command_sync(command):
    return sudo(command)

@task
@parallel
def sudo_run_command_parallel(command):
    return sudo(command)
