"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, patterns, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from test_project.base import views as base_views


from test_project.jingo_utils import install_jinja_translations
install_jinja_translations()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

base_urlpatterns = patterns(
    '',

    url(r'^$', base_views.index_view, name='index_view'),
    url(r'^django', base_views.django_view, name='django_view'),
    url(r'^jingo', base_views.jingo_view, name='jingo_view'),
)

urlpatterns += i18n_patterns(
    '',

    url(r'', include(base_urlpatterns)),
)
