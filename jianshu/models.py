# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.db import models

class ArticleList(models.Model):
    """
        文章概要信息
    """
    article_id = models.CharField('ID', primary_key=True, max_length=100)
    article_title = models.CharField('文章标题', max_length=100)
    article_url = models.URLField('文章URL')
    user = models.CharField('作者', max_length=100)
    user_url = models.URLField('作者URL')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', ]

    def __unicode__(self):
        return self.article_title
    def __str__(self):
        return self.article_title


class ArticleDetail(models.Model):
    """
        文章详细信息
    """
    image = models.URLField('图片URL' )
    title = models.CharField('文章标题', max_length=100)
    body = models.TextField('文章内容', null=True)
    time = models.CharField('发表时间' , max_length=100, null=True)
    views = models.PositiveIntegerField('阅读数', default=0)
    comments = models.PositiveIntegerField('评论数', default=0)
    likes = models.PositiveIntegerField('喜欢', default=0)
    tip = models.PositiveIntegerField('打赏', default=0)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    article = models.ForeignKey('ArticleList', verbose_name='文章摘要')
     
    class Meta:
        ordering = ['-created', ]
    
    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title
    




