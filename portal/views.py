# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from portal.models import Article, Tag, ArticleType
from common.des_tool import get_decode_num
from portal.dao import *
from django.views.decorators.cache import cache_page

page_title = "xfuture的博客主页"

# 主页
@cache_page(60 * 3)
def home(request):
    articles = get_home_articles()
    new_articles = get_home_new_articles()
    ranking_articles = get_home_ranking_articles()
    tags = get_tags()
    return render_to_response('home.html',
                              {'module_index': 0,
                               'articles': articles,
                               'new_articles': new_articles,
                               'ranking_articles': ranking_articles,
                               'tags': tags,
                               'page_title': page_title},
                              context_instance=RequestContext(request))


# 开发笔记
@cache_page(60)
def development(request, page_number='1'):
    development_type = get_development_type()
    if page_number:
        number = int(page_number)
        if number <= 0: number = 1
    else:
        number = 1
    start = (number - 1) * 10
    end = number * 10
    articles = get_development_articles(development_type, start, end, suffix=page_number)
    page_count = get_development_articles_page_count(development_type)
    new_articles = get_development_new_articles(development_type)
    ranking_articles = get_development_ranking_articles(development_type)
    tags = get_tags()
    development_sub_nav_world = get_kv_info('development_sub_nav_world')[0].val
    return render_to_response('development.html',
                              {'module_index': development_type.module_index,
                               'page_module_name': development_type.name,
                               'page_module_suffix': '.html',
                               'page_title': "开发笔记",
                               'articles': articles,
                               'new_articles': new_articles,
                               'ranking_articles': ranking_articles,
                               'tags': tags,
                               'page_count': page_count,
                               'development_sub_nav_world': development_sub_nav_world,
                               'page_number': number},
                              context_instance=RequestContext(request))


# 随思录
@cache_page(60)
def life_record(request, page_number='1'):
    life_record_type = get_life_record_type()
    if page_number:
        number = int(page_number)
        if number <= 0: number = 1
    else:
        number = 1
    start = (number - 1) * 10
    end = number * 10
    articles = get_life_record_articles(life_record_type, start, end, suffix=page_number)
    page_count = get_life_record_page_count(life_record_type)
    new_articles = get_life_record_new_articles(life_record_type)
    ranking_articles = get_life_record_ranking_articles(life_record_type)
    tags = get_tags()
    life_record_sub_nav_world = get_kv_info('life_record_sub_nav_world')[0].val
    return render_to_response('life_record.html',
                              {'module_index': life_record_type.module_index,
                               'page_module_name': life_record_type.name,
                               'page_module_suffix': '.html',
                               'page_title': "随思录",
                               'articles': articles,
                               'new_articles': new_articles,
                               'ranking_articles': ranking_articles,
                               'tags': tags,
                               'page_count': page_count,
                               'life_record_sub_nav_world': life_record_sub_nav_world,
                               'page_number': number},
                              context_instance=RequestContext(request))


# 关于页面
@cache_page(60 * 60 * 24 * 365)
def about_me(request):
    about_me_info = get_kv_info('about_me_info')
    about_my_blog = get_kv_info('about_my_blog')
    personal_info = get_kv_info('personal_info')
    about_sub_nav_world = get_kv_info('about_sub_nav_world')[0].val
    return render_to_response('about_me.html',
                              {'module_index': 3,
                               'about_me_info': about_me_info,
                               'about_my_blog': about_my_blog,
                               'personal_info': personal_info,
                               'about_sub_nav_world': about_sub_nav_world,
                               'page_title': "关于我"},
                              context_instance=RequestContext(request))


# 文章页面
@cache_page(60)
def article(request, id):
    id = get_decode_num(id)
    article = None
    if id >= 0:
        article = get_article(id, suffix=id)
    if article:
        module_index = article.type.module_index
    else:
        return render_to_response('404.html', {'error_title': '文章'}, context_instance=RequestContext(request))
    before_article = get_before_article(id, suffix=id)
    after_article = get_after_article(id, suffix=id)
    related_articles = get_related_articles(article.type, suffix=id)
    new_articles = get_new_articles(article.type, suffix=article.type.name)
    ranking_articles = get_ranking_articles(article.type, suffix=article.type.name)
    tags = get_tags()
    return render_to_response('article.html',
                              {
                                  'module_index': module_index,
                                  'article': article,
                                  'before_article': before_article,
                                  'after_article': after_article,
                                  'ranking_articles': ranking_articles,
                                  'new_articles': new_articles,
                                  'related_articles': related_articles,
                                  'tags': tags,
                                  'page_title': article.title,
                              },
                              context_instance=RequestContext(request))


# 标签页面
@cache_page(60)
def tags(request):
    tags = Tag.objects.all()
    return render_to_response('tags.html',
                              {
                                  'module_index': -1,
                                  'tags': tags,
                                  'page_title': "收录的标签"
                              },
                              context_instance=RequestContext(request))


# 搜索结果页面
def search(request, page_number='1'):
    query_tag = request.GET.get('tag')
    if page_number:
        number = int(page_number)
        if number <= 0: number = 1
    else:
        number = 1
    start = (number - 1) * 10
    end = number * 10
    query_articles = None
    q_results = None
    page_count = 1
    if query_tag is not None:
        query_arg = query_tag.strip()
        cache_suffix = str(query_arg) + str(number)
        query_articles = get_search_tag_articles(query_arg, start, end, suffix=cache_suffix)
        page_count = get_search_tag_articles_page_count(query_arg)
    else:
        from common import search_tool

        query_arg = request.GET.get('q')
        if query_arg is not None:
            q_results = search_tool.search_article(query_arg)
            page_count = (len(q_results) / 10) + 1
        else:
            query_arg = ''

    new_articles = get_home_new_articles()
    ranking_articles = get_home_ranking_articles()
    tags = get_tags()
    return render_to_response('search.html', {'module_index': -1,
                                              'page_title': query_arg + "的结果",
                                              'page_module_name': 'search',
                                              'page_module_suffix': '?q=' + query_arg,
                                              'query_arg': query_arg,
                                              'articles': query_articles,
                                              'q_results': q_results,
                                              'new_articles': new_articles,
                                              'ranking_articles': ranking_articles,
                                              'tags': tags,
                                              'number': number,
                                              'page_count': page_count},
                              context_instance=RequestContext(request))


# 阅读计数
def read_counter(request):
    if request.method == "POST":
        id = get_decode_num(request.POST.get('id'))
        article = None
        if id >= 0:
            article = get_article(id, suffix=id)
            ## 添加阅读次数
            article.read_count += 1
            article.save()
    return HttpResponse()


# 测试bae运行环境
@cache_page(60 * 60 * 24 * 365)
def testbae(request):
    import os
    import django
    import sys
    import whoosh
    import jieba
    import tempfile

    cwdpath = os.path.abspath(os.getcwd())
    django_version = django.get_version()
    python_version = sys.version
    platform = sys.platform
    return render_to_response('test.html',
                              {
                                  'module_index': -1,
                                  'page_title': "bae环境参数",
                                  'cwdpath': cwdpath,
                                  'django_version': django_version,
                                  'python_version': python_version,
                                  'platform': platform,
                                  'whoosh_version': whoosh.versionstring(),
                                  'jieba_is_working': bool(jieba.cut('test')),
                                  'sys_temp_dir': tempfile.gettempdir(),
                              },
                              context_instance=RequestContext(request))
