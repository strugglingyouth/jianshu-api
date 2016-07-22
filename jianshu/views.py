#coding:utf-8

from rest_framework import viewsets
from jianshu.serializers import ArticleListSerializer, ArticleDetailSerializer
from jianshu.models import ArticleList, ArticleDetail




class ArticleListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ArticleList.objects.all()
    serializer_class =  ArticleListSerializer


class ArticleDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ArticleDetail.objects.all()
    serializer_class = ArticleDetailSerializer























