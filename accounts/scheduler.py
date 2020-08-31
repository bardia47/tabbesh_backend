import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    # read about cron in apscheduler document
    # --> https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html
    scheduler.add_job(daily_course_times, 'cron', hour=6, minute=30)
    scheduler.start()


def daily_course_times():
    from .models import Course_Calendar, Course
    import logging
    logger = logging.getLogger("django")
    # we cant import in top because account app not register when this code run ...

    now = datetime.datetime.now()
    courses = Course.objects.filter(end_date__gt=now)
    for course in courses:
        classes = Course_Calendar.objects.filter(course__id=course.id)
        # update all classes time
        for class_course_calender in classes:
            try:
                while class_course_calender.end_date < now:
                    class_course_calender.start_date += datetime.timedelta(days=7)
                    class_course_calender.end_date += datetime.timedelta(days=7)
                    if class_course_calender.end_date > course.end_date:
                        break
                    class_course_calender.save()
                    logger.error(course.title + "  is OK!")
            except Exception as e:
                logger.error("danger: " + e)
    classes = Course_Calendar.objects.filter(end_date__day=now.day, end_date__gt=now)
    scheduler = BackgroundScheduler()
    for clas in classes:
        scheduler.add_job(update_course_calenders, 'date', args=[clas.id], run_date=clas.end_date)
    scheduler.print_jobs()
    scheduler.start()


def update_course_calenders(*args):
    from .models import Course, Course_Calendar, User
    from .utils import EmailUtils, TextUtils
    from .enums import Email
    import logging
    logger = logging.getLogger("django")
    try:
        course_calendar = Course_Calendar.objects.get(id__in=args)
        course_calendar.start_date += datetime.timedelta(days=7)
        course_calendar.end_date += datetime.timedelta(days=7)
        if course_calendar.end_date < course_calendar.course.end_date:
            course_calendar.save()
            logger.error(course_calendar.course.title + "  is OK!")
        EmailUtils.sending_email(TextUtils.replacer(Email.schadulerTestText.value, [course_calendar.course.title])
                                 , Email.tethaEmail.value, Email.testEmail.value, Email.testPassword.value)
    except Exception as e:
        logger.error("danger: " + e)
    # print log when course calender update ...
#  print("course calenders update at " + str(now))
# we need log for this
