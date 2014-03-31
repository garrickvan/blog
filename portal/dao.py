# coding=utf-8
from common.cache_tool import get_cache
from portal.models import *

from common.log_tool import get_logger

def load_from_cache(key, time):
    '''
    返回key对应的缓存，time是缓存的有效时间，秒为单位，如果不存在就调用fun函数获取
    '''
    def __fun_deco(fun):
        def __fun_arg_deco(*args, **kwargs):
            cache = get_cache()
            suffix = kwargs.pop('suffix', None)
            if suffix:
                key_str = ''.join(key).join(str(suffix))
            else:
                key_str = str(key)
            val = cache.get(key_str)
            get_logger().debug('Getting cache by key(%s)' %(key_str))
            if not val:
                val = fun(*args)
                cache.set(key_str, val, time)
            return val
        return __fun_arg_deco
    return __fun_deco

## 获取前五个标签
#@load_from_cache('tags', 300)
def get_tags():
    return Tag.objects.all()[0:5]

## 获取home页面的数据
#@load_from_cache('home_articles', 120)
def get_home_articles():
    return Article.objects.order_by('-recommend_factor')[0:10]

#@load_from_cache('home_new_articles', 120)
def get_home_new_articles():
    return Article.objects.all()[0:5]

#@load_from_cache('home_ranking_articles', 120)
def get_home_ranking_articles():
    return Article.objects.order_by('-read_count')[0:5]

## 获取development页面的数据
#@load_from_cache('development_articles', 120)
def get_development_articles(type, start, end, suffix='1'):
    return Article.objects.filter(type=type)[start:end]

#@load_from_cache('development_articles_page_count', 60)
def get_development_articles_page_count(type):
    return (Article.objects.filter(type=type).count() / 10) + 1

#@load_from_cache('development_new_articles', 120)
def get_development_new_articles(type):
    return Article.objects.filter(type=type).order_by('-publish_date')[0:5]

#@load_from_cache('development_ranking_articles', 120)
def get_development_ranking_articles(type):
    return Article.objects.filter(type=type).order_by('-read_count')[0:5]

#@load_from_cache('development_type', 0)
def get_development_type():
    return ArticleType.objects.filter(name='development')[0]

## 获取life_record页面的数据
#@load_from_cache('life_record_type', 0)
def get_life_record_type():
    return ArticleType.objects.filter(name='life_record')[0]

#@load_from_cache('life_record_articles', 0)
def get_life_record_articles(type, start, end, suffix='1'):
    return Article.objects.filter(type=type)[start:end]

#@load_from_cache('life_record_page_count', 60)
def get_life_record_page_count(type):
    return (Article.objects.filter(type=type).count() / 10) + 1

#@load_from_cache('life_record_new_articles', 120)
def get_life_record_new_articles(type):
    return Article.objects.filter(type=type).order_by('-publish_date')[0:5]

#@load_from_cache('lief_record_ranking_articles', 120)
def get_life_record_ranking_articles(type):
    return Article.objects.filter(type=type).order_by('-read_count')[0:5]

## 文章页面的数据
#@load_from_cache('articles', 120)
def get_article(id, suffix=''):
    return Article.objects.filter(id=id)[0]

#@load_from_cache('before_article', 120)
def get_before_article(id, suffix=''):
    try:
        before_article = Article.objects.filter(id__lt=id)[0]
    except:
        before_article = None
    return before_article

#@load_from_cache('after_article', 120)
def get_after_article(id, suffix=''):
    try:
        after_article = Article.objects.filter(id__gt=id).order_by('id')[0]
    except:
        after_article = None
    return after_article

#@load_from_cache('related_articles', 120)
def get_related_articles(type, suffix=''):
    return Article.objects.filter(type=type)[0:4]

#@load_from_cache('new_articles', 60)
def get_new_articles(type, suffix=''):
    return Article.objects.filter(type=type).order_by('-publish_date')[0:5]

#@load_from_cache('ranking_articles', 60)
def get_ranking_articles(type, suffix=''):
    return Article.objects.filter(type=type).order_by('-read_count')[0:5]

## 搜索页面
#@load_from_cache('search_articles', 120)
def get_search_tag_articles(query_arg, start, end, suffix=''):
    tag = Tag.objects.filter(name=query_arg)
    return Article.objects.filter(tags__in=tag)[start:end]

#@load_from_cache('search_articles', 120)
def get_search_tag_articles_page_count(query_arg, suffix=''):
    tag = Tag.objects.filter(name=query_arg)
    return (Article.objects.filter(tags__in=tag).count() / 10) + 1