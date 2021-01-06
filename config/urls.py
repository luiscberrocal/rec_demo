from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from rec_demo import __version__ as current_version
from rec_demo.core.api.views import app_data

admin.site.site_header = _("REC Demo v{}".format(current_version))
admin.site.site_title = _("REC Demo Portal v{}".format(current_version))
admin.site.index_title = _("Welcome to REC Demo Portal")

urlpatterns = []
urlpatterns += i18n_patterns(
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("rec_demo.users.urls", namespace="users")),
    path("real-estate/", include("rec_demo.real_estate.urls", namespace="real_estate")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path('api/v1/app-data/', app_data, name='app_data'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
