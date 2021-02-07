from django.apps import AppConfig


class ReportsConfig(AppConfig):
    name = 'rec_demo.reports'

    def ready(self):
        import rec_demo.reports.signals  # noqa
