"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from yg_cms import views as new_views
from django.conf import settings


urlpatterns = [
    url(r'^admin/d033e22ae348aeb5660fc2140aec35850c4da997', admin.site.urls),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^$', new_views.index, name='index'),
    url(r'^column/(?P<column_slug>[^/]+)/$', new_views.column_detail, name='column'),
    url(r'^yg_cms/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', new_views.article_detail, name='article'),
    url(r'^archive/(?P<archive_slug>[^/]+)/$', new_views.archive, name='archives'),
    url(r'^comments/', include('django_comments.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
