from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Home page
    url(r'^$', 'taxapp.views.home'),

    # AJAX Request to pull county information on OpenLayers JS Code
    url(r'^get_county/(?P<county_name>.+)/$', 'taxapp.views.get_county'),
)

urlpatterns += patterns('',url(r'^staticfiles/(?P<path>.*)$',
    'django.views.static.serve', {'document_root':'data/www',
        'show_indexes':True}),)
