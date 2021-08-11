from django.apps import AppConfig
import subprocess, os, sys
import shlex
import psutil

class EminisceAppConfig(AppConfig):
    name = 'eminisce'
    verbose_name = "Eminisce"
    def ready(self):
        # Use cron to do background tasks
        # We need a lot of checks to prevent this from being stuck in a loop since manage.py will call ready every time
        # Don't run on local because Windows does not have cron
        # if 'runserver' not in sys.argv and 'makemigrations' not in sys.argv and 'migrate' not in sys.argv and 'crontab' not in sys.argv: 
        #     print("Starting crontab jobs")
        #     subprocess.Popen([sys.executable, 'manage.py', 'crontab', 'add'], env=os.environ.copy(),)
        #     # process_tasks_cmd = "python manage.py crontab add"
        #     # process_tasks_args = shlex.split(process_tasks_cmd)
        #     # process_tasks_subprocess = subprocess.Popen(process_tasks_args)
        # UPDATE: Herooku does not have cron either :( and I'll die before I use their scheduler

        # UPDATE: Good news, background_tasks actually works here!
        # This is a really bad idea but it gets the job done
        print(f"{sys.argv} {os.environ.get('RUN_MAIN', None)}")
        if os.environ.get('RUN_MAIN', None) != 'true': # Don't execute on the autoreload thread           
            if 'collectstatic' not in sys.argv and 'makemigrations' not in sys.argv and 'migrate' not in sys.argv and 'process_tasks' not in sys.argv:
                startTasks = True
                
                if (os.environ.get("DYNO")): # If running on heroku, make sure to only run on 1 process
                    print("Running on Heroku, running process check")
                    #check WEB_CONCURRENCY exists and is more than 1
                    web_concurrency = os.environ.get("WEB_CONCURRENCY")
                    if (web_concurrency):
                        mypid = os.getpid()
                        print("[%s] WEB_CONCURRENCY exists and is set to %s" % (mypid, web_concurrency))
                        gunicorn_workers = int(web_concurrency)
                        if (gunicorn_workers > 1):
                            maxPid = self.getMaxRunningGunicornPid()
                            if (maxPid == mypid):
                                startTasks = True
                            else:
                                startTasks = False
                
                if startTasks:
                    print("Starting background tasks")
                    from eminisce.tasks import auto_update_statuses, cleanup_completed_tasks_db
                    from background_task.models import Task
                    Task.objects.all().delete() #Clean the tasks database 
                    print("Executing 'auto updating loans status' task")
                    auto_update_statuses(repeat=60) # Repeat every minute because heroku can't take it
                    cleanup_completed_tasks_db(repeat=300) # For some reason this stupid plugin clutters up the database so we need to cleanup continuously
                    subprocess.Popen([sys.executable, 'manage.py', 'process_tasks'], env=os.environ.copy(),)

    # HEROKU/GUNICORN ONLY =================================================================================
    def getMaxRunningGunicornPid(self):
            running_pids = psutil.pids()
            maxPid = -1
            for pid in running_pids:
                proc = psutil.Process(pid)
                proc_name = proc.name()
                if (proc_name == "gunicorn"):
                    if (maxPid < pid):
                        maxPid = pid
            print("Max Gunicorn PID: %s", maxPid)
            return maxPid
