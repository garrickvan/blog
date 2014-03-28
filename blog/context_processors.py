# coding=utf-8
import settings

# 设置全局模板变量
def global_value(request):
    return {
        'Bootstrap_css' : settings.STATIC_URL + 'css/bootstrap.min.css',
        'Bootstrap_js' : settings.STATIC_URL + 'bootstrap/js/bootstrap.js',
        'JQuery_js' : 'http://libs.baidu.com/jquery/1.10.0/jquery.min.js',
        'UI_to_top_js': settings.STATIC_URL + 'js/jquery.ui.totop.js',
        'project_name' : 'xfuture的博客',
    }