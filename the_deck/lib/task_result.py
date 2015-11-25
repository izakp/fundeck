class TaskResult(object):
    def __init__(self, task_id=None, result=None, error=None):
        assert (result and not error) or (error and not result), "result xor error are required"

        self.task_id = task_id

        if result is not None:
            self.succeeded = True
            self.failed = False
            self.error = None
            stdout_buf, stderr_buf, status = result
            self.stdout = stdout_buf
            self.stderr = stderr_buf
            self.status = status

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
    def human_result(self):
        if self.failed:
            return self.error.splitlines()
        if self.status != 0:
            return self.stderr.splitlines()
        return self.stdout.splitlines()

    def get_stdout(self):
        return self.stdout.splitlines()

    def get_stderr(self):
        return self.stderr.splitlines()
