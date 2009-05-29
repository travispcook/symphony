
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Document(models.Model):
    content_type = models.ForeignKey(ContentType, null=True, blank=True) # allow these to be null
    object_id = models.PositiveIntegerField(null=True, blank=True)       # so we can store other
    object = generic.GenericForeignKey()                                 # crawler's output here too
    title = models.CharField(null=True, blank=True, max_length=255)
    body = models.TextField()
    
    class Admin:
        pass
    
    def __unicode__(self):
        if self.object:
            return unicode(self.object)
        elif self.title:
            return unicode(self.title)
        else:
            return u'Document'

class Word(models.Model):
    string = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.string
        
    class Admin:
        pass

class WordPosition(models.Model):
    document = models.ForeignKey(Document, related_name="words")
    word = models.ForeignKey(Word, related_name="locations")
    position = models.PositiveIntegerField()
    
    class Admin:
        pass
    
    def __unicode__(self):
        return self.word.string