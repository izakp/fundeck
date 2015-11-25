class TaskResult(object):
    def __init__(self, result=None, error=None):
        assert (result and not error) or (error and not result), "result xor error are required"

        if result is not None:
            self.failed = False
            self.error = None
            stdout_buf, stderr_buf, status = result
            self.stdout = stdout_buf
            self.stderr = stderr_buf
            self.status = status

        if error is not None:
            self.failed = True
            self.error = error
            self.stdout = None
            self.stderr = None
            self.status = None

    def remote_command_failed(self):
        return self.status != 0

    def human_result(self):
        if self.failed:
            return self.error.splitlines()
        if self.status != 0:
            return self.stderr.splitlines()
        return self.stdout.splitlines()