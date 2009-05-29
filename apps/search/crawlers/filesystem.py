from search import Crawler
from search.models import Document
from django.conf import settings

from os.path import exists, isdir, join
from os import listdir, walk

from search.models import Document

FS_CRAWL_DIRECTORIES = settings.FS_CRAWL_DIRECTORIES
FILE_EXTENSIONS_TO_SEARCH = ['html', 'txt', 'body', 'toc']
FS_CRAWL_RECURSIVE = False


class FileSystemCrawler(Crawler):
    """
    Crawls given directories
    """
    def crawl(self):       
        for directory in FS_CRAWL_DIRECTORIES:
            if exists(directory) and isdir(directory):
                for root, dirs, files in walk(directory):
                    for listed_item in files:
                        filenameparts = listed_item.split('.')
                        if len(filenameparts) > 2:
                            filename = filenameparts[:len(filenameparts)-1]
                            extension = filenameparts[-1:]
                        else:
                            filename = filenameparts[0]
                            extension = filenameparts[1]
                        if extension in FILE_EXTENSIONS_TO_SEARCH:
                            print "Crawling: %s%s.%s" % (root, filename, extension)
                            fp = open(directory+listed_item, "r")
                            data = fp.readlines()
                            fp.close()
                            data = ''.join(data)
                            document = Document.objects.create(body=data, title=filename)
                            self.indexer.add(document)