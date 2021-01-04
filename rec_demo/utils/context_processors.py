from django.conf import settings


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {
        "DEBUG": settings.DEBUG,
        'ENVIRONMENT_NAME': settings.ENVIRONMENT_NAME,
        'ENVIRONMENT_ADMIN_CSS': settings.ENVIRONMENT_ADMIN_CSS,
    }
