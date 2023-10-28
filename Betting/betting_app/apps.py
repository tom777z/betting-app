from django.apps import AppConfig

class BettingAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "betting_app"

    def ready(self):
        import betting_app.signals