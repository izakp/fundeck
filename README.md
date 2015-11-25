### WIP!

Goals:

	- To make something like rundeck that's easy to use, manage, deploy and backup

	- Should be all pip-installable, modular and portable (via sqlite exports)

	- Should easily plug into ChefServer and PuppetDB APIs to generate dyanmic instance catalogues

	- Should uspport static host definitions

	- User signup via organization (google OAuth or invites)

	- ACLs manageable via admin interface (User and Group Permissions)

	- Modular task models, should support chained execution

	- Secure storage and easy management of multiple private keys

Done:

	- Proof of concept

Todo:

	- Finish model structure

	- Build task execution strategies / context guards (FSM)

	- User Auth

	- Expose TaskRunner state transitions via API

	- Frontend Interface @_@

	- Swap Fabric for underlying Paramiko method calls

	- Work around https://github.com/celery/celery/issues/1709


## Fundeck

A clone of Rundeck that emphasizes fun over agony

`mkvirtualenv fundeck`

`pip install -r requirements.txt`

`python ./manage.py syncdb`

`python ./manage.py runserver`

`PYTHONOPTIMIZE=1 celery -A fundeck worker -l info`

Caveat: https://github.com/celery/celery/issues/1709

"AssertionError: daemonic processes are not allowed to have children"

`export PYTHONOPTIMIZE=1` (Skips assertions at Runtime)
