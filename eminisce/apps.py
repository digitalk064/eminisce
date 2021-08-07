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
        # if 'runserver' not in sys.argv and 'makemigrations' not in sys.argv and 'migrate' not in sys.argv and 'crontab' not in sys.argv: 
        #     print("Starting crontab jobs")
        #     subprocess.Popen([sys.executable, 'manage.py', 'crontab', 'add'], env=os.environ.copy(),)
        #     # process_tasks_cmd = "python manage.py crontab add"
        #     # process_tasks_args = shlex.split(process_tasks_cmd)
        #     # process_tasks_subprocess = subprocess.Popen(process_tasks_args)

        # UPDATE: Good news, background_tasks actually works here!
        print(sys.argv)
        if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv and 'process_tasks' not in sys.argv: 
            print("Starting background tasks")
            from eminisce.tasks import auto_update_loans
            print("Executing 'auto updating loans status' task")
            auto_update_loans(repeat=1) # Repeat every second because why not
            subprocess.Popen([sys.executable, 'manage.py', 'process_tasks'], env=os.environ.copy(),)