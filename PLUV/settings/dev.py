from .base import *

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


def show_toolbar(request):
    """
    Function determins whether toolbar is shown or not
    """
    return False


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
