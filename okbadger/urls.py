from django.conf.urls import patterns, include, url
import okbadger.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','okbadger.views.home'),
    url(r'^issuer/?', 'okbadger.views.issuer'),
    url(r'^badge/?','okbadger.views.badge'),
    url(r'^badge/?/criteria','okbadger.views.badge_criteria'),
    url(r'^badge/?/issue/?','okbadger.views.issued_badge'),

)
