from django.conf.urls import patterns, include, url
import badger.urls_simple 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include(badger.urls_simple)),
    url(r'^admin/', include(admin.site.urls)),
)
