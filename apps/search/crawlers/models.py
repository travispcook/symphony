from django.db.models.loading import cache
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from search import Crawler, registry
from search.models import Document

from HTMLParser import HTMLParser

class TagStripper(HTMLParser):
    """ Convert markup to plain text. Use my convert method to just bung in data and get the desired results."""
    def __init__(self):
        self.reset()
        self.info = []
        
    def handle_data(self, d):
        self.info.append(d)
        
    def plaintext(self):
        return ' '.join(self.info)
        
    def clear(self):
        self.reset()
        self.info = []
        
    def convert(self, d):
        if str(d) == d and d.__contains__("<"):
            self.clear()
            self.feed(d)
            return self.plaintext()
        return d

class ModelCrawler(Crawler):
    """
    Crawls Django models.
    """
    def crawl(self):
        if not registry:
            print "No models registered to index."
        for opts in registry.values():
            ct = ContentType.objects.get_for_model(opts.model)
            for instance in opts.manager.all():
                values = []
                document, created = Document.objects.get_or_create(content_type=ct, object_id=instance.pk)
                if settings.DEBUG:
                    if created:
                        print "%s created" % document
                for field in opts.fields:
                    if field.has_key('is_title') and field['is_title']:
                        document.title = getattr(instance, field['field_name'])
                    if field.has_key('is_html') and field['is_html']:
                        values.append(TagStripper().convert(getattr(instance, field['field_name'])))
                    else:
                        values.append(getattr(instance, field['field_name']))
                document.body = "".join(values)
                document.save()
                self.indexer.add(document)
    