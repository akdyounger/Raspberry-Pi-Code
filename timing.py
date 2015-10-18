from apscheduler.scheduler import Scheduler
import datetime

# Start the scheduler
sched = Scheduler()
sched.start()

def job_function():
    print "Hello World"

# Schedules job_function to be run every minute
# sched.add_cron_job(job_function, minute=1)
#sched.add_cron_job(job_function, second=10, start_date=datetime.datetime.now())
sched.add_interval_job(job_function, seconds=10, start_date=datetime.datetime.now())

sched.print_jobs()