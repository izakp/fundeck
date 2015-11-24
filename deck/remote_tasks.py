from fabric.api import task, run, parallel

@task
@parallel
def whoami():
    return run("ls -la")
