from django.conf.urls.defaults import *

from library.models import Piece, Composer, Arranger, Performance
random_list = Piece.objects.order_by('?')[0:5]
extra_context = {
	'random_list': random_list,
}

piece_dict = {
	'queryset': Piece.objects.all(),
	'paginate_by': 50,
	'extra_context': extra_context,
}

composer_dict = {
	'queryset': Composer.objects.order_by('last_name'),
	'paginate_by': 50,
	'extra_context': extra_context,
}

arranger_dict = {
	'queryset': Arranger.objects.order_by('last_name'),
	'paginate_by': 50,
	'extra_context': extra_context,
}

piece_detail = {
	'queryset': Piece.objects.all(),
	'extra_context': extra_context,
}

performance_list = {
	'queryset': Performance.objects.all(),
	'paginate_by': 50,
	'extra_context': extra_context,
}

performance_detail = {
	'queryset': Performance.objects.all(),
	'extra_context': extra_context,
}

urlpatterns = patterns('django.views.generic.list_detail',
	# URLs for listing. Directly access the list_detail generic views.

	# Homepage. Lists all pieces. Paginated.
	url(r'^$',
		'object_list',
		piece_dict,
		name='piece_list'
	),
	
	# Shows detailed information on a specific piece.
	url(r'^piece/(?P<object_id>\d+)/$',
		'object_detail',
		piece_detail,
		name='piece_detail'
	),
	
	# Lists all composers.
	url(r'^composer/$',
		'object_list',
		composer_dict,
		name='composer_list'
	),

	# Lists all arrangers.
	url(r'^arranger/$',
		'object_list',
		arranger_dict,
		name='arranger_list'
	),

	# List all performances.
	url(r'^performance/$',
		'object_list',
		performance_list,
		name='performance_list'
	),

	# Show information on a specific performance.
	url(r'^performance/(?P<object_id>\d+)/$',
		'object_detail',
		performance_detail,
		name='performance_detail'
	),
)

urlpatterns += patterns('library.views',
	# Some of these URLs wrap the list_detail generic views.

	# List all pieces filed in a specific cabinet group.
	url(r'^(?P<group_name>\w{1,5})/$',
		'group_list',
		name='group_list'
	),

	# List all pieces filed in a specific cabinet group and cabinet.
	url(r'^(?P<group_name>\w{1,5})/(?P<cabinet_id>\d+)/$',
		'cabinet_list',
		name='cabinet_list'
	),

	# List all pieces filed in a specific cabinet group, cabinet, and cabinet drawer.
	url(r'^(?P<group_name>\w{1,5})/(?P<cabinet_id>\d+)/(?P<drawer_id>\d+)/$',
		'drawer_list',
		name='drawer_list'
	),

	# List all pieces by a specific composer.
	url(r'^composer/(?P<composer_id>\d+)/$',
		'composer_list',
		name='composer_piece_list'
	),

	# List all pieces by a specific arranger.
	url(r'^arranger/(?P<arranger_id>\d+)/$',
		'arranger_list',
		name='arranger_piece_list'
	),
	
	# Go to the next or previous piece by ID number.
	url(r'^piece/(?P<id>\d+)/(?P<nextprev>(next|prev))$',
		'piece_nextprev',
		name='piece_nextprev'
	),

	# Go to the next or previous performance by date..
	url(r'^performance/(?P<id>\d+)/(?P<nextprev>(next|prev))$',
		'performance_nextprev',
		name="performance_nextprev"
	),
	
	# Select a random object of various kinds.
	url(r'^(?P<object>(piece|composer|arranger))/random$',
		'object_random',
		name='object_random'
	),

	# Search all pieces by title.
	url(r'^search/title$',
		'search_pieces',
		name='search_pieces'),
	
	# Search all composers by name.
	url(r'^search/composer$',
		'search_composers',
		name='search_composers'
	),
	
	url(r'^lys-backup.json.gz$',
		'backup',
		name='backup'
	),
)

urlpatterns += patterns('',
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
