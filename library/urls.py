from django.conf.urls.defaults import *

from library.models import Piece, Composer, Arranger, Performance
from settings import URL_PREFIX
random_list = Piece.objects.order_by('?')[0:5]
extra_context = {
	'random_list': random_list,
	'URL_PREFIX': URL_PREFIX
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
	url(r'^$', 'object_list', piece_dict, name='homepage'),
	url(r'^piece/(?P<object_id>\d+)/$', 'object_detail', piece_detail, name='piece_detail'),
	(r'^composer/$', 'object_list', composer_dict),
	(r'^arranger/$', 'object_list', arranger_dict),
	(r'^performance/$', 'object_list', performance_list),
	url(r'^performance/(?P<object_id>\d+)/$', 'object_detail', performance_detail, name='performance_detail'),
)

urlpatterns += patterns('library.views',
	(r'^(?P<group_name>\w{1,5})/$', 'group_list'),
	(r'^(?P<group_name>\w{1,5})/(?P<cabinet_id>\d+)/$', 'cabinet_list'),
	(r'^(?P<group_name>\w{1,5})/(?P<cabinet_id>\d+)/(?P<drawer_id>\d+)/$', 'drawer_list'),
	(r'^composer/(?P<composer_id>\d+)/$', 'composer_list'),
	(r'^arranger/(?P<arranger_id>\d+)/$', 'arranger_list'),
	(r'^piece/(?P<id>\d+)/(?P<nextprev>(next|prev))$', 'piece_nextprev'),
	(r'^performance/(?P<id>\d+)/(?P<nextprev>(next|prev))$', 'performance_nextprev'),
	(r'^(?P<object>(piece|composer|arranger))/random$', 'object_random'),
	(r'^search/title$', 'search_pieces'),
	(r'^search/composer$', 'search_composers'),
)

