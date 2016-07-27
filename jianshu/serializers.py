#!/usr/bin/env python
# coding:utf-8

from models import ArticleList, ArticleDetail, HotArticle
from rest_framework import serializers

class ArticleListSerializer(serializers.ModelSerializer):
    """
        新上榜文章列表
    """
    class Meta:
        model = ArticleList
        fields = ('article_id', 'article_title', 'article_url', 'article_user', 'article_user_url') 


class ArticleDetailSerializer(serializers.ModelSerializer): 
    """
        新上榜文章详细信息
    """
    class Meta:
        model = ArticleDetail 
        fields = ('image', 'title', 'body', 'created', 'views', 'comments', 'likes', 'tip', 'article_abstract')


class HotArticleSerializer(serializers.ModelSerializer): 
    """
        热门文章详细信息
    """
    class Meta:
        model = HotArticle
        fields = ('article_id', 'article_url', 'article_user', 'article_user_url', 'article_image', 'article_title', 'article_body', 'article_time', 'article_views_count', 'public_comments_count', 'article_likes_count', 'total_rewards_count' )


