import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    # read about cron in apscheduler document
    # --> https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html
    scheduler.add_job(update_course_calenders, 'cron', hour=6, minute=30)
    scheduler.start()


def update_course_calenders():
    from .models import Course, Course_Calendar
    # we cant import in top because account app not register when this code run ...
    now = datetime.datetime.now()
    courses = Course.objects.filter(end_date__gt=now)
    for course in courses:
        classes = Course_Calendar.objects.filter(course__id=course.id)
    # update all classes time
        for class_course_calender in classes:
            while class_course_calender.end_date < now:
                class_course_calender.start_date += datetime.timedelta(days=7)
                class_course_calender.end_date += datetime.timedelta(days=7)
                if  class_course_calender.end_date>course.end_date :
                    break
                class_course_calender.save()
    # print log when course calender update ...
  #  print("course calenders update at " + str(now))
# we need log for this 
