from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'
    verbose_name = 'داشبورد'
    # # run scheduler when app is ready
    # def ready(self):
    #     scheduler.start()
