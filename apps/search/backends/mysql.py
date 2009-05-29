
from search.base import Indexer, Searcher
from search.models import Document, Word, WordPosition

from django.db import connection

DEFAULT_IGNORE_WORDS = ("a", "and", "in", "is", "it", "the", "to",)

class MysqlIndexer(Indexer):
    def __init__(self, ignore_words=None):
        """
        Since we're letting mysql do the indexing, all we need to do here is set the index up.
        """
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE FULLTEXT INDEX document_fulltext_index on search_document(title, body);")
        except:
            pass
        return None
    
    def make_words(self, document):
        return ''
        
    def add(self, document):
        return ''
    
class MysqlSearcher(Searcher):
    def query(self, query):
        meta = Document._meta
        columns = ['title', 'body']
        full_names = ["%s.%s" % (connection.ops.quote_name(meta.db_table), connection.ops.quote_name(column)) for column in columns]
        fulltext_columns = ", ".join(full_names)
        match_expr = ("MATCH(%s) AGAINST (%%s)" % fulltext_columns)
        return Document.objects.extra(select={'relevance' : match_expr}, where=[match_expr], params=[query, query]).order_by('-relevance')