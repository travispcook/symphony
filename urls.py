from django.conf.urls.defaults import *
from settings import MEDIA_ROOT, DEVELOPMENT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Enable Admin
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/(.*)', admin.site.root, name="admin"),

	# My URLS:
	(r'^', include('library.urls')),
)

if DEVELOPMENT:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve',	{'document_root': MEDIA_ROOT}),
	)

