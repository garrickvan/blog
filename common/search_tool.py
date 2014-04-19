'''
    This is a small search tool interface wrapper the whoosh.
    It has the master and slave index
'''

#coding=utf-8
from whoosh.index import create_in
from whoosh.fields import *
from os import path
from portal.models import Article
from jieba.analyse import ChineseAnalyzer
from whoosh.qparser import QueryParser
from django.utils.html import strip_tags
from django.utils.text import Truncator
import threading
import time
import os
import tempfile

IX_DIR = path.join(path.abspath(tempfile.gettempdir()), 'ix')
IX_MASTER_DIR = path.join(IX_DIR, 'master_dir')
IX_IDLE_DIR = path.join(IX_DIR, 'idle_dir')

_article_ix_manager = None


class IXManager(object):
    def __init__(self, master_ix, idle_ix):
        self._curr_ix = master_ix;
        self._master_ix = master_ix;
        self._idle_ix = idle_ix;
        self._update_locked = False;

    def get_curr_ix(self):
        return self._curr_ix

    def get_idle_ix(self):
        return self._idle_ix

    def switch_ix(self):
        tmp_ix = self._master_ix
        self._curr_ix = self._idle_ix
        self._master_ix = self._idle_ix
        self._idle_ix = tmp_ix


class WhooshIX(object):
    '''
        This is the whoosh index object mapping to portal Article table.
        it simple wap the whoosh api, make it easy to use.
    '''

    def __init__(self, name, dir, schema):
        self.name = name
        self.schema = schema
        _init_ix_dir(dir)
        if dir is not None:
            self.ix = create_in(dir, self.schema)
        else:
            raise NameError
        self.writer = self.ix.writer()

    def add_doc(self, **fields):
        if self.writer.is_closed:
            self.writer = self.ix.writer()
        self.writer.update_document(**fields)

    def commit(self):
        self.writer.commit()

    def search(self, filed, key_world):
        q = QueryParser(filed, schema=self.ix.schema).parse(key_world)
        return self.ix.searcher().search(q)


def _init_ix_dir(dir_name):
    if not os.path.isdir(IX_DIR):
        os.mkdir(IX_DIR)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)


def init_article_index_from_db():
    global _article_ix_manager
    if _article_ix_manager is None:
        schema = Schema(title=TEXT(stored=True), date=TEXT(stored=True),
                        short_content=TEXT(stored=True), id=ID(unique=True, stored=True),
                        type_intro=TEXT(stored=True), cover_name=TEXT(stored=True),
                        author_name=TEXT(stored=True), content=TEXT(analyzer=ChineseAnalyzer()),
                        type_name=TEXT(stored=True), cover_url=TEXT(stored=True))
        master_ix = WhooshIX('a', IX_MASTER_DIR, schema.copy())
        idle_ix = WhooshIX('b', IX_IDLE_DIR, schema.copy())
        _article_ix_manager = IXManager(master_ix, idle_ix)
    _update_article_index_from_db(_article_ix_manager.get_curr_ix())
    _launch_article_update_task()


def _update_article_index_from_db(ix):
    '''
        update the article from the article table.
    '''

    import math

    print 'start updating article index.'
    objs = Article.objects
    each_page = 50
    page_count = int(math.ceil(objs.count() / float(each_page)))
    for p in range(1, page_count + 1):
        start = (p - 1) * each_page
        end = p * each_page
        for article in objs.all()[start: end]:
            ix.add_doc(id=unicode(article.id),
                       title=unicode(article.title),
                       author_name=unicode(article.author.first_name),
                       short_content=unicode(Truncator(strip_tags(article.content)).chars(200)),
                       # cut off all html tags from the content
                       content=unicode(article.content),
                       type_name=unicode(article.type.name),
                       type_intro=unicode(article.type.intro),
                       date=unicode(str(article.publish_date)),
                       cover_url=unicode(article.cover.url),
                       cover_name=unicode(article.cover.name), )
    ix.commit()
    print 'finish updating article index.'


def search_article(key_world, start=0, end=10):
    '''
        key_world: the search key world.
        start: the search result page start index.
        end: the search result page end index.

        return: the result of search from the documents.
    '''

    global _article_ix_manager
    if _article_ix_manager is None:
        init_article_index_from_db()
    if not (start >= 0 and start >= end):
        start = 0
        end = 10
    results = _article_ix_manager.get_curr_ix().search('content', key_world)[start: end]
    return results


class UpdateIXTask(threading.Thread):
    def __init__(self, ix_manager, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        self.ix_manager = ix_manager
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            _update_article_index_from_db(self.ix_manager.get_idle_ix())
            self.ix_manager.switch_ix()
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True


def _launch_article_update_task():
    '''
        This well update the index from db each hours.
    '''
    global _article_ix_manager
    UpdateIXTask(_article_ix_manager, 60 * 60).start()