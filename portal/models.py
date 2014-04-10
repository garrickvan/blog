# coding=utf8
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=20)
    intro = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

# 文章类型表
class ArticleType(models.Model):
    name = models.CharField(max_length=20)
    intro = models.CharField(max_length=60)
    module_index = models.IntegerField()

    def __unicode__(self):
        return self.name

# 图片文件表
class ImgFile(models.Model):
    name = models.CharField(max_length=120)
    url = models.CharField(max_length=250)
    upload_date = models.DateTimeField()
    upload_user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

# 文章表
class Article(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    read_count = models.IntegerField()
    publish_date = models.DateTimeField()
    author = models.ForeignKey(User)
    type = models.ForeignKey(ArticleType)
    tags = models.ManyToManyField(Tag, blank=True)
    cover = models.ForeignKey(ImgFile, blank=True, null=True,)
    recommend_factor = models.IntegerField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-publish_date',)

# 资讯Key_Value表
class KVInfo(models.Model):
    key = models.CharField(max_length=32)
    val = models.TextField()
    order = models.IntegerField()

    def __unicode__(self):
        return self.key

    class Mate:
        ordering = ('order', 'key', )