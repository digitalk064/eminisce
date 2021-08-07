from django.apps import AppConfig

import subprocess, os, sys
import shlex

class EminisceAppConfig(AppConfig):
    name = 'eminisce'
    verbose_name = "Eminisce"
    def ready(self):
        if True: #if 'runserver' not in sys.argv and 'makemigrations' not in sys.argv and 'migrate' not in sys.argv: # Don't run on local because Windows does not have cron
            print("Starting crontab jobs")
            #subprocess.Popen([sys.executable, os.getcwd() + '/eminisce/start_background_tasks.py'], env=os.environ.copy(),)
            process_tasks_cmd = "python manage.py crontab add"
            process_tasks_args = shlex.split(process_tasks_cmd)
            process_tasks_subprocess = subprocess.Popen(process_tasks_args)