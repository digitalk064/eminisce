from django.apps import AppConfig

import subprocess, os, sys

class EminisceAppConfig(AppConfig):
    name = 'eminisce'
    verbose_name = "Eminisce"
    def ready(self):
        if 'runserver' not in sys.argv and 'makemigrations' not in sys.argv and 'migrate' not in sys.argv: # Don't run on local because Windows does not have cron
            print("Starting crontab jobs")
            #subprocess.Popen([sys.executable, os.getcwd() + '/eminisce/start_background_tasks.py'], env=os.environ.copy(),)
            process_tasks_cmd = sys.executable + " manage.py crontab add"
            process_tasks_subprocess = subprocess.Popen(process_tasks_cmd, env=os.environ.copy())