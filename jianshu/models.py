# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.db import models

class ArticleDetail(models.Model):
    """
        文章详细信息
    """
    image = models.CharField('图片URL', max_length=100)
    title = models.CharField('文章标题', max_length=100)
    #content = models.TextField('文章内容')
    created = models.CharField('发表时间' , max_length=100)
    views = models.PositiveIntegerField('阅读数', default=0)
    comments = models.PositiveIntegerField('评论数', default=0)
    likes = models.PositiveIntegerField('喜欢', default=0)
    top = models.PositiveIntegerField('打赏', default=0)

     
    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title
    


class ArticleList(models.Model):
    """
        文章概要信息
    """
    article_title = models.CharField('文章标题', max_length=100)
    artilce_url = models.CharField('文章url', max_length=100)
    user = models.CharField('作者', max_length=100)
    user_url = models.CharField('作者url', max_length=100)
    article = models.ForeignKey('ArticleDetail', verbose_name='文章详细信息', null=True)

    def __unicode__(self):
        return self.article_title
    def __str__(self):
        return self.article_title




