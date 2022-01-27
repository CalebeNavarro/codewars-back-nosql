from apscheduler.schedulers.blocking import BlockingScheduler
import os


sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=1.5)
# def timed_job():
#     os.system("flask routine codewars")

@sched.scheduled_job('cron', hour='12')
def scheduled_job():
    os.system("flask routine codewars")

sched.start()