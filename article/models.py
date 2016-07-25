# coding:utf-8

from __future__ import unicode_literals

from django.db import models


class article(models.Model):
    """

    """

    article_id = models.CharField('ID', primary_key=True, max_length=100)
    article_url = models.URLField('文章URL')
    article_user = models.CharField('作者', max_length=100)
    article_user_url = models.URLField('作者URL')
    article_image = models.URLField('图片URL' )
    article_title = models.CharField('文章标题', max_length=100)
    article_body = models.TextField('文章内容', null=True)
    article_time = models.CharField('发表时间' , max_length=100, null=True)
    article_views = models.CharField('阅读数', max_length=100)
    article_comments = models.CharField('评论数', max_length=100)
    article_likes = models.CharField('喜欢', max_length=100)
    article_tip = models.CharField('打赏', max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', ]

    def __unicode__(self):
        return self.article_title
    def __str__(self):
       return self.article_title


