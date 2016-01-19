### WIP!

Goals:

	- To make something like rundeck that's easy to use, manage, deploy and backup

	- Should be all pip-installable, modular and portable (via sqlite exports)

	- Should easily plug into ChefServer and PuppetDB APIs to generate dyanmic instance catalogues

	- User signup via organization (google OAuth or invites)

	- ACLs manageable via admin interface (User and Group Permissions)

	- Modular task models, should support chained execution

	- Secure storage and easy management of multiple private keys

Done:

	- Proof of concept

Todo:

	- User Auth

	- Expose TaskRunner state transitions via API

	- Frontend Interface @_@

## Fundeck

A clone of Rundeck that emphasizes fun over agony

Setup:

Fact!  Fundeck recommends using Virtual Environments: http://docs.python-guide.org/en/latest/dev/virtualenvs/

`mkvirtualenv fundeck`

`pip install -r requirements.txt`

`python ./manage.py syncdb`


Development:

`python ./manage.py runserver`

`celery -A fundeck worker -l debug`

Production:

`gunicorn fundeck.wsgi -w 4 --bind=0.0.0.0:80` (Starts 4 workers binding to all interfaces on port 80)

`celery -A fundeck worker --autoscale=40,4`  (Autoscales between 4 and 40 task workers)

Also Fact!  Fundeck endorses Supervisord (http://supervisord.org/) to manage production services.
