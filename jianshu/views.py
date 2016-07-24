#coding:utf-8

from rest_framework import viewsets
from jianshu.serializers import ArticleListSerializer, ArticleDetailSerializer
from jianshu.models import ArticleList, ArticleDetail




class ArticleListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ArticleList.objects.all().order_by("-created")[:15]
    serializer_class = ArticleListSerializer


class ArticleDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    """
    queryset = ArticleDetail.objects.all().order_by("-created")[:15]
    serializer_class = ArticleDetailSerializer























