import select
import sys
import time

import paramiko

from fabric.thread_handling import ThreadHandler
from fabric.io import output_loop, input_loop


"""
TODO

Look into fabric/operations.py._execute for paramiko implementation

Thread Pool for stdin,stdout,stderr - pipe via Redis  LPUSH/RPOP?

http://docs.fabfile.org/en/1.10/api/core/operations.html#fabric.operations.run

Implementation: https://github.com/fabric/fabric/blob/5217b12f8aca3bc071206f7f4168e62c003509d1/fabric/operations.py#L721

No parallel operations (no forking within multiprocessign if possible)

"""

def run_paramiko(command, host, username, timeout=300, stdout=None, stderr=None):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    client.connect(host, username=username)

    channel = client.get_transport().open_session()
    channel.exec_command(command)

    # stdout/stderr redirection
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr

    stdout_buf, stderr_buf = [], []

    workers = (
        ThreadHandler('out', output_loop, channel, "recv",
            capture=stdout_buf, stream=stdout, timeout=timeout),
        ThreadHandler('err', output_loop, channel, "recv_stderr",
            capture=stderr_buf, stream=stderr, timeout=timeout),
        ThreadHandler('in', input_loop, channel, False)
    )

    while True:
        if channel.exit_status_ready():
            break
        else:
            for worker in workers:
                worker.raise_if_needed()
        try:
            time.sleep(paramiko.io_sleep)
        except KeyboardInterrupt:
            channel.send('\x03')

        rl, wl, xl = select.select([channel], [], [], 0.0)
        if len(rl) > 0:
            buf = channel.recv(1024)
            stdout_buf.append(buf)

    status = channel.recv_exit_status()
    for worker in workers:
        worker.thread.join()
        worker.raise_if_needed()

    channel.close()

    stdout_buf = ''.join(stdout_buf).strip()
    stderr_buf = ''.join(stderr_buf).strip()

    return stdout_buf, stderr_buf, status
