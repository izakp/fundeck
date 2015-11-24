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
