from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from DevLabs4.views import home,home2,like, dislike
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DevLabs4.views.home', name='home'),
    # url(r'^DevLabs4/', include('DevLabs4.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^hey/',home2),
    url(r'^like/',like),
    url(r'^dislike/',dislike),
)
