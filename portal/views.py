# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from portal.models import Article, Tag, ArticleType
from common.des_tool import get_decode_num

page_title = "xfuture的博客主页"

# 主页
def home(request):
    articles = Article.objects.order_by('-recommend_factor')[0:10]
    new_articles = Article.objects.all()[0:5]
    ranking_articles = Article.objects.order_by('-read_count')[0:5]
    tags = Tag.objects.all()[0:5]
    return render_to_response('home.html',
        {'module_index' : 0,
         'articles' : articles,
         'new_articles': new_articles,
         'ranking_articles' : ranking_articles,
         'tags' : tags,
         'page_title': page_title},
        context_instance=RequestContext(request))

# 开发笔记
development_type = None
development_index = 1
def development(request, page_number='1'):
    global development_type
    if not development_type:
        development_type = ArticleType.objects.filter(name='development')

    if page_number:
        number = int(page_number)
        if number <= 0:
            number = 1
        start = (number - 1) * 10
        end = number * 10
        articles = Article.objects.filter(type=development_type)[start:end]
    else:
        number = 1
        articles = Article.objects.filter(type=development_type)[0:10]

    page_count = (Article.objects.filter(type=development_type).count() / 10) + 1
    new_articles = Article.objects.filter(type=development_type).order_by('-publish_date')[0:5]
    ranking_articles = Article.objects.filter(type=development_type).order_by('-read_count')[0:5]
    tags = Tag.objects.all()[0:5]
    return render_to_response('development.html',
        {'module_index' : development_index,
         'page_title': "开发笔记",
         'articles' : articles,
         'new_articles': new_articles,
         'ranking_articles' : ranking_articles,
         'tags' : tags,
         'page_count' : page_count,
         'page_number' : number},
        context_instance=RequestContext(request))

# 随思录
life_record_type = None
life_record_index = 2
def life_record(request, page_number='1'):
    global life_record_type
    if not life_record_type:
        life_record_type = ArticleType.objects.filter(name='life_record')

    if page_number:
        number = int(page_number)
        if number <= 0:
            number = 1
        start = (number - 1) * 10
        end = number * 10
        articles = Article.objects.filter(type=life_record_type)[start:end]
    else:
        number = 1
        articles = Article.objects.filter(type=life_record_type)[0:10]

    page_count = (Article.objects.filter(type=life_record_type).count() / 10) + 1
    new_articles = Article.objects.filter(type=life_record_type).order_by('-publish_date')[0:5]
    ranking_articles = Article.objects.filter(type=life_record_type).order_by('-read_count')[0:5]
    tags = Tag.objects.all()[0:5]
    return render_to_response('life_record.html',
        {'module_index' : life_record_index,
         'page_title': "随思录",
         'articles' : articles,
         'new_articles': new_articles,
         'ranking_articles' : ranking_articles,
         'tags' : tags,
         'page_count' : page_count,
         'page_number' : number},
        context_instance=RequestContext(request))

# 关于页面
def about_me(request):
    return render_to_response('about_me.html',
        {'module_index' : 3,
         'page_title': "关于我"},
        context_instance=RequestContext(request))

# 文章页面
def article(request, id):
    id = get_decode_num(id)
    article = None
    if id >= 0:
        article = Article.objects.filter(id=id)[0]
    if article:
        module_index = article.type.module_index
    else:
        return render_to_response('404.html', {'error_title': '文章'}, context_instance=RequestContext(request))

    article.read_count += 1
    article.save()
    try:
        before_article = Article.objects.filter(id__lt=id)[0]
    except:
        before_article = None

    try:
        after_article = Article.objects.filter(id__gt=id).order_by('id')[0]
    except:
        after_article = None

    related_articles = Article.objects.filter(type=article.type,)[0:4]
    new_articles = Article.objects.filter(type=article.type,).order_by('-publish_date')[0:5]
    ranking_articles = Article.objects.filter(type=article.type,).order_by('-read_count')[0:5]
    tags = Tag.objects.all()[0:5]

    return render_to_response('article.html',
        {
            'module_index' : module_index,
            'article' : article,
            'before_article': before_article,
            'after_article': after_article,
            'ranking_articles':ranking_articles,
            'new_articles':new_articles,
            'related_articles': related_articles,
            'tags' : tags,
            'page_title': article.title,
        },
        context_instance=RequestContext(request))

# 标签页面
def tags(request):
    tags = Tag.objects.all()
    return render_to_response('tags.html',
        {
            'module_index' : -1,
            'tags' : tags,
            'page_title': "收录的标签"
        },
        context_instance=RequestContext(request))

# 搜索结果页面
def search(request):
    query_tag = request.GET.get('tag')
    if query_tag:
        articles = Article.objects.order_by('-recommend_factor')[0:10]
        query_arg = query_tag
    else:
        query_arg = ''
    new_articles = Article.objects.all()[0:5]
    ranking_articles = Article.objects.order_by('-read_count')[0:5]
    tags = Tag.objects.all()[0:5]
    return render_to_response('home.html',
        {
        'module_index' : -1,
        'page_title' : query_arg + "的结果",
         'articles' : articles,
         'new_articles': new_articles,
         'ranking_articles' : ranking_articles,
         'tags' : tags,},
        context_instance=RequestContext(request))

# 测试bae运行环境
def testbae(request):
    import os
    import django
    import sys
    cwdpath = os.path.abspath(os.getcwd())
    django_version = django.get_version()
    python_version = sys.version
    platform = sys.platform
    return render_to_response('test.html',
        {
            'module_index' : -1,
            'page_title' : "bae环境参数",
            'cwdpath': cwdpath,
            'django_version': django_version,
            'python_version': python_version,
            'platform': platform
        },
        context_instance=RequestContext(request))
