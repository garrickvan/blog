# coding=utf8
from portal.models import *
from django.contrib import admin

# 标签表的admin视图定义
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro',)

# 文章类型表的admin视图定义
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro', 'module_index')

# 图片文件表
class ImgFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'upload_user', 'upload_date',)

# 文章表的admin视图定义
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'read_count', 'publish_date', 'recommend_factor')
    class Media:
        css = {
            'all': ('/static/kindeditor/themes/default/default.css',)
        }
        js = (
            '/static/kindeditor/kindeditor-min.js',
            '/static/kindeditor/lang/zh_CN.js',
            '/static/kindeditor/config.js',
        )

# 注册表到admin
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ArticleType, ArticleTypeAdmin)
admin.site.register(ImgFile, ImgFileAdmin)