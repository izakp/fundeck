import select
import sys
import time

from cStringIO import StringIO

import paramiko
from paramiko import SSHException

from fabric.io import output_loop, input_loop

from thread_handler import ThreadHandler

"""
http://docs.fabfile.org/en/1.10/api/core/operations.html#fabric.operations.run
Implementation: https://github.com/fabric/fabric/blob/5217b12f8aca3bc071206f7f4168e62c003509d1/fabric/operations.py#L721
"""

class RemoteCommand(object):
    def __init__(self, host, username, private_key, timeout=300, stdout=None, stderr=None):
        self.timeout = timeout
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        pkey = paramiko.RSAKey.from_private_key(StringIO(private_key))
        self.client.connect(host, username=username,
                               look_for_keys=False, pkey=pkey)

    def run(self, command):
        channel = self.client.get_transport().open_session()
        channel.input_enabled = True
        channel.exec_command(command)

        stdout_buf, stderr_buf = [], []

        workers = (
            ThreadHandler('out', output_loop, channel, "recv",
                capture=stdout_buf, stream=self.stdout, timeout=self.timeout),
            ThreadHandler('err', output_loop, channel, "recv_stderr",
                capture=stderr_buf, stream=self.stderr, timeout=self.timeout),
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

        return CommandResult((stdout_buf, stderr_buf, status))

    def write_file(self, filename, content, permissions):
        sftp_client = self.client.open_sftp()
        f = sftp_client.open(filename, 'w')
        f.write(content)
        f.close()
        sftp_client.chmod(filename, int(permissions))
        sftp_client.close()

    def delete_file(self, filename):
        sftp_client = self.client.open_sftp()
        sftp_client.unlink(filename)

class CommandResult(object):
    def __init__(self, result):
        stdout_buf, stderr_buf, status = result
        self.stdout = stdout_buf
        self.stderr = stderr_buf
        self.status = int(status)

    @property
    def succeeded(self):
        return self.status == 0

    @property
    def failed(self):
        return self.status != 0

    @property
    def result(self):
        if self.status != 0:
            return self.stderr
        return self.stdout

    @property
    def stdout_as_list(self):
        return self.stdout.splitlines()

    @property
    def stderr_as_list(self):
        return self.stderr.splitlines()

