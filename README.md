# 爬取简书中的文章保存至 MySQL 并生成 API 

---

简书 API 测试地址 : [http://222.24.63.118:8080/](http://222.24.63.118:8080/)



### 1. 爬取前的准备

了解简书整个网站的结构以及分析网页源代码：[爬取简书全站文章并生成 API](http://www.jianshu.com/p/c546c175b763)


> ##### 简书各个目录代码格式相同，所以相同的方法也可以爬取简书其余几个分类目录。


### 2. 爬取简书全站

爬取简书“新上榜”，“热门”中的文章并保存在 MySQL 中。爬虫使用 **python** 的 **BeautifulSoup** 模块进行爬取，**BeautifulSoup** 模块的使用方法可以参照 [BeautifulSoup 模块使用指南](http://www.jianshu.com/p/2b783f7914c6)。爬取“热门”目录下所有能加载到的文章，最多可以加载 15 页，每一小时爬取一次。对于新上榜中的内容，每次只爬取当前页面中的所有文章，15 分钟爬取一次，不会递归爬取所有页。

代码中使用 **Django orm** 来生成所需要的数据库，若不熟悉 **Django**，请参阅官方文档 [ Django 官方文档 ](https://www.djangoproject.com/) 或者对应的 [中文翻译文档](http://python.usyiyi.cn/django/index.html)。S数据库设计代码参考 **jianshu** 目录下 `models.py` 文件，爬虫代码参考 `popular_articles_jianshu.py` 文件。 



### 3. 爬取搜索到的文章

此功能有待完善，由于本人对前端代码不太熟悉，所以只能分析出搜索到的首页链接，爬取也只能获得首页的 10 篇文章，如果有朋友知道怎样爬取，麻烦告知下，非常感谢！


### 4. 生成 API

将上面爬取到的文章保存到 **MySQL** 中，使用 **Django REST framework** 来生成 **API**，若对此功能不熟悉的请查 [ Django REST framework 官方文档 ](http://www.django-rest-framework.org/)。


![简书 API](http://cdn.tianfeiyu.com/jianshuapi.png)


### 5. 部署上线

* 使用 **nginx + uwsgi + django + supervisor** 进行环境部署

	或者

* 使用 **docker** 进行环境部署

> #### -_- 目前代码写的比较散乱，后面还会不断重构，如有任何建议，欢迎提 issue，欢迎 fork，pr，当然也别忘了 star 哦！

---
