#coding:utf-8

from rest_framework import viewsets
from jianshu.serializers import ArticleListSerializer, ArticleDetailSerializer, HotArticleSerializer, SearchArticleSerializer
from jianshu.models import ArticleList, ArticleDetail, HotArticle, SearchArticle




class ArticleListViewSet(viewsets.ReadOnlyModelViewSet):
    """
        新上榜文章列表
    """
    queryset = ArticleList.objects.all().order_by("-created")[:18]
    serializer_class = ArticleListSerializer


class ArticleDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
        新上榜文章详细信息
    """
    queryset = ArticleDetail.objects.all().order_by("-created")[:18]
    serializer_class = ArticleDetailSerializer

class HotArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
        热门文章详细信息
    """
    queryset = HotArticle.objects.all().order_by("-created")[:18]
    serializer_class = HotArticleSerializer

class SearchArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
        搜索到文章的详细信息
    """
    queryset = SearchArticle.objects.all().order_by("-created")[:10]
    serializer_class = SearchArticleSerializer























