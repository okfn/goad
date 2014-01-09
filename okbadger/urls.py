from django.conf.urls import patterns, include, url
import okbadger.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','okbadger.views.home'),
    url(r'^issuer/(?P<slug>[-\w]+)$', 'okbadger.views.issuer'),
    url(r'^revocation$', 'okbadger.views.revocation'), 
    url(r'^badge/(?P<slug>[-\w]+)$','okbadger.views.badge'),
    url(r'^badge/(?P<slug>[-\w]+)/criteria','okbadger.views.badge_criteria'),
    url(r'^badge/(?P<slug>[-\w]+)/instance/(?P<id>\d+)','okbadger.views.instance'),
    url(r'^claim/(?P<id>\d+)$','okbadger.views.claim'),

)
