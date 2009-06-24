# Create your views here.

from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseRedirect
from library.models import Piece, Composer, Arranger, Performance
from settings import URL_PREFIX, MEDIA_URL
import random
from library.modelsearch import *

extra = {'random_list': Piece.objects.order_by('?')[0:5], 'URL_PREFIX': URL_PREFIX}

# Listing Views. These views wrap the object_list generic view.
# Probably best to conglomerate all of these into one smart view.

def group_list(request, group_name):
	queryset = Piece.objects.filter(drawer__cabinet__group__shortname = group_name).order_by('composer__last_name')
	return object_list(request=request, queryset=queryset, template_name="library/group_piece_list.html", paginate_by=10, allow_empty=False, extra_context = extra)

def cabinet_list(request, group_name, cabinet_id):
	queryset = Piece.objects.filter(drawer__cabinet__group__shortname = group_name).filter(drawer__cabinet__number = cabinet_id).order_by('composer__last_name')
	return object_list(request=request, queryset=queryset, template_name="library/cabinet_piece_list.html", paginate_by=10, allow_empty=False, extra_context = extra)

def drawer_list(request, group_name, cabinet_id, drawer_id):
	queryset = Piece.objects.filter(drawer__cabinet__group__shortname = group_name).filter(drawer__cabinet__number = cabinet_id).filter(drawer__number = drawer_id).order_by('composer__last_name')
	return object_list(request=request, queryset=queryset, template_name="library/drawer_piece_list.html", paginate_by=10, allow_empty=False, extra_context = extra)

def composer_list(request, composer_id):
	queryset = Piece.objects.filter(composer = composer_id).order_by('title')
	extra['composer'] = Composer.objects.get(pk=composer_id)
	return object_list(request=request, queryset=queryset, template_name="library/composer_piece_list.html", paginate_by=10, allow_empty=False, extra_context = extra)

def arranger_list(request, arranger_id):
	queryset = Piece.objects.filter(arranger = arranger_id).order_by('title')
	extra['arranger'] = Arranger.objects.get(pk=arranger_id)
	return object_list(request=request, queryset=queryset, template_name="library/arranger_piece_list.html", paginate_by=10, allow_empty=False, extra_context = extra)

# End listing views.

def object_random(request, object):
	objects = {'piece': Piece, 'composer': Composer,'arranger': Arranger}
	return HttpResponseRedirect(random.choice(objects[object].objects.all()).get_absolute_url())

def piece_nextprev(request, id, nextprev):
	id = int(id)
	if nextprev == 'next':
		try: redirect = Piece.objects.filter(id__gt=id).order_by('pk')[0]
		except IndexError: return HttpResponseNotFound()
	elif nextprev == 'prev':
		try: redirect = Piece.objects.filter(id__lt=id).order_by('-pk')[0]
		except IndexError: return HttpResponseNotFound()
	return HttpResponseRedirect(redirect.get_absolute_url())

def performance_nextprev(request, id, nextprev):
	id = int(id)
	if nextprev == 'next':
		try: redirect = Performance.objects.filter(id__gt=id).order_by('pk')[0]
		except IndexError: return HttpResponseNotFound()
	elif nextprev == 'prev':
		try: redirect = Performance.objects.filter(id__lt=id).order_by('-pk')[0]
		except IndexError: return HttpResponseNotFound()
	return HttpResponseRedirect(redirect.get_absolute_url())

def search_pieces(request):
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		
		entry_query = get_query(query_string, ['title', 'subtitle'])
		
		found_entries = Piece.objects.filter(entry_query)

	render_dict = {'query_string': query_string, 'object_list': found_entries, 'MEDIA_URL': MEDIA_URL}
	render_dict.update(extra)
	
	return render_to_response(
		'library/piece_search.html',
		render_dict,
#		context_instance=RequestContext(request)
	)

