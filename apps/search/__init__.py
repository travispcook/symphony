
from base import Crawler
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings 

try:
    backend = settings.SEARCH_BACKEND
    try:
        dot = backend.rindex(".")
    except ValueError:
        raise ImproperlyConfigured, "%s isn't a backend module" % backend
    backend_path, backend_module = backend[:dot], backend[dot+1:]    
    
    indexer_name = "%sIndexer" % backend_module.capitalize()
    try:
        mod = __import__(backend, {}, {}, indexer_name)
        Indexer = getattr(mod, indexer_name)
    except ImportError, e:
        raise ImproperlyConfigured, 'Error importing indexer module %s: "%s"' % (backend, e)
        
    searcher_name = "%sSearcher" % backend_module.capitalize()
    try:
        mod = __import__(backend, {}, {}, searcher_name)
        Searcher = getattr(mod, searcher_name)
    except ImportError, e:
        raise ImproperlyConfigured, 'Error importing searcher module %s: "%s"' % (backend, e)
        
except AttributeError:
    from base import Searcher, Indexer



registry = {}

class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass

class ModelSearchOptions(object):
    def __init__(self, model, fields, manager=None):
        self.model = model
        self.fields = fields
        self.manager = manager or model._default_manager

def register(model, *args, **kwargs):
    opts = model._meta
    #if str(opts) in registry:
    #    raise AlreadyRegistered("The model %s has already been registered." % model.__name__)
    registry[str(opts)] = ModelSearchOptions(model, *args, **kwargs)