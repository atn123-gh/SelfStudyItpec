"""itp_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.views import defaults as default_views
from django.views.generic import TemplateView

# from quiz.views import quiz_sitemap
# from django.contrib.sitemaps.views import sitemap
# sitemaps = {
#     'quiz': quiz_sitemap,
# }
    


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('home/',include('home.urls')),
    path('quiz/',include('quiz.urls')),
    # path('learn/',include('learn.urls')),
    path('',RedirectView.as_view(url='home/',permanent=True)),
    path('sitemap/', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml'), name='sitemap-redirect'),

    # path("sitemap.xml", sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
    # if "debug_toolbar" in settings.INSTALLED_APPS:
    #     import debug_toolbar

    #     urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns


from django.urls import path

def trigger_error(request):
  division_by_zero = 1 / 0

  urlpatterns = [
    path('sentry-debug/', trigger_error),
    # ...
  ]