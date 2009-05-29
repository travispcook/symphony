
from django.conf import settings
from django.core.management import BaseCommand
from django.core.exceptions import ImproperlyConfigured

class Command(BaseCommand):
    
    def load_crawlers(self, indexer):
        crawlers = []
        for crawler_path in settings.SEARCH_CRAWLERS:
            try:
                dot = crawler_path.rindex(".")
            except ValueError:
                raise ImproperlyConfigured, "%s isn't a crawler module" % crawler_path
            crawler_module, crawler_classname = crawler_path[:dot], crawler_path[dot+1:]
            try:
                mod = __import__(crawler_module, {}, {}, [""])
            except ImportError, e:
                raise ImproperlyConfigured, 'Error importing crawler module %s: "%s"' % (crawler_module, e)
            try:
                crawler_class = getattr(mod, crawler_classname)
            except AttributeError:
                raise ImproperlyConfigured, 'Middleware module "%s" does not define a "%s" class' % (crawler_module, crawler_classname)
            crawlers.append(crawler_class(indexer))
        return crawlers
        
    def load_indexer(self):
        backend = settings.SEARCH_BACKEND
        try:
            dot = backend.rindex(".")
        except ValueError:
            raise ImproperlyConfigured, "%s isn't a backend module" % backend
        backend_path, backend_module = backend[:dot], backend[dot+1:]
        indexer_name = "%sIndexer" % backend_module.capitalize()
        try:
            mod = __import__(backend, {}, {}, indexer_name)
            mod = getattr(mod, indexer_name)
        except ImportError, e:
            raise ImproperlyConfigured, 'Error importing indexer module %s: "%s"' % (backend, e)
        return mod
            
    def handle(self, *args, **options):
        from search import Indexer
        crawlers = self.load_crawlers(Indexer())
        for crawler in crawlers:
            crawler.crawl()
