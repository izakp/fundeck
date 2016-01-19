import select
import sys
import time

import traceback

import cStringIO

import paramiko

from fabric.io import output_loop, input_loop

from thread_handler import ThreadHandler

"""
TODO

Thread Pool for stdin,stdout,stderr - pipe via Redis  LPUSH/RPOP?

http://docs.fabfile.org/en/1.10/api/core/operations.html#fabric.operations.run

Implementation: https://github.com/fabric/fabric/blob/5217b12f8aca3bc071206f7f4168e62c003509d1/fabric/operations.py#L721

"""

class RemoteCommand(object):
    def __init__(self, command, host, username, pkey, timeout=300, stdout=None, stderr=None):
        self.command = command
        self.host = host
        self.username = username
        self.pkey = pkey
        self.timeout = timeout
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

    def run(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            pkey = paramiko.RSAKey.from_private_key(cStringIO.StringIO(self.pkey))
            client.connect(self.host, username=self.username,
                            look_for_keys=False, pkey=pkey)

            channel = client.get_transport().open_session()
            channel.input_enabled = True
            channel.exec_command(self.command)
        except paramiko.SSHException:
            e = traceback.format_exc()
            return CommandResult(error=e)

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

        return CommandResult(result=(stdout_buf, stderr_buf, status))


class CommandResult(object):
    def __init__(self, result=None, error=None):
        assert (result and not error) or (error and not result), "result xor error are required"

        if result is not None:
            self.succeeded = True
            self.failed = False
            self.error = None
            stdout_buf, stderr_buf, status = result
            self.stdout = stdout_buf
            self.stderr = stderr_buf
            self.status = int(status)

        if error is not None:
            self.succeeded = False
            self.failed = True
            self.error = error
            self.stdout = None
            self.stderr = None
            self.status = None

    @property
    def remote_command_failed(self):
        return self.status != 0

    @property
    def result(self):
        if self.failed:
            return self.error
        if self.status != 0:
            return self.stderr
        return self.stdout

    @property
    def result_as_list(self):
        return self.human_result.splitlines()

    @property
    def stdout_as_list(self):
        return self.stdout.splitlines()

    @property
    def stderr_as_list(self):
        return self.stderr.splitlines()

