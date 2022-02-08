from apscheduler.schedulers.blocking import BlockingScheduler
import os
from pytz import utc


def job_function():
    os.system("flask routine codewars")

sched = BlockingScheduler()

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
sched.add_job(job_function, 'cron', hour='18', timezone=utc)

sched.start()


# @sched.scheduled_job('cron', hour='12', timezone=utc)
# def scheduled_job():
#     os.system("flask routine codewars")

# @sched.scheduled_job('interval', minutes=60)
# def timed_job():
#     os.system("flask routine codewars")

# sched.start()