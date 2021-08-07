from django.apps import AppConfig

import subprocess, os, sys
import shlex

class EminisceAppConfig(AppConfig):
    name = 'eminisce'
    verbose_name = "Eminisce"
    def ready(self):
        # This is a really bad idea because I'm too lazy to install cron on heroku
        # We need a lot of checks to prevent this from being stuck in a loop since manage.py will call ready every time
        # Don't run on local because Windows does not have cron
        if 'runserver' not in sys.argv and 'makemigrations' not in sys.argv and 'migrate' not in sys.argv and 'crontab' not in sys.argv: 
            print("Starting crontab jobs")
            subprocess.Popen([sys.executable, 'manage.py', 'crontab', 'add'], env=os.environ.copy(),)
            # process_tasks_cmd = "python manage.py crontab add"
            # process_tasks_args = shlex.split(process_tasks_cmd)
            # process_tasks_subprocess = subprocess.Popen(process_tasks_args)