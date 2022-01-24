# from celery.decorators import task,periodic_task
# from celery.utils.log import get_task_logger
# from celery.schedules import crontab
#
# logger = get_task_logger(__name__)
#
#
# @task(name="print hoy")
# def print_this(message):
#     """sends an email when feedback form is filled successfully"""
#     logger.info("Sent feedback email")
#     print (message)
#
#
#
# @periodic_task(run_every=(crontab(minute=1)), name="some_task", ignore_result=True)
# def some_task():
#     print("print")