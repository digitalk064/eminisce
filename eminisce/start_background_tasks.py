import subprocess, os, sys
import shlex

def main():
    print(sys.executable)
    process_tasks_cmd = sys.executable + " manage.py crontab add"
    process_tasks_subprocess = subprocess.Popen(process_tasks_cmd, env=os.environ.copy())


if __name__ == '__main__':
    main()