#!/usr/bin/env python
# coding:utf-8

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8') 

from bs4 import BeautifulSoup
import requests
import re

pattern = re.compile(r'.*?(\d+).*?')

domain_name = 'http://www.jianshu.com'
base_url = 'http://www.jianshu.com/recommendations/notes'

html = requests.get(base_url).content

# html 是网页的源码，soup 是获得一个文档的对象
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

def get_article():
    links = soup.find_all('h4')
    for link in links:
        print link.a.get_text()
        href = link.a['href']
        if href.startswith('/p/'):
            print domain_name + href

def get_digit(var):
    var = filter(str.digit, str(var))
    return var
def get_details():
    """
        阅读，评论，喜欢一定存在，打赏不一定有
    """
    tags = soup.find_all('li', class_="have-img")
    print "all:",len(tags)
    for tag in tags:
        image = tag.img['src']
        user = tag.p.a.get_text()

        user_url = tag.p.a['href']
        if user_url.startswith('/users/'):
            user_url = domain_name + user_url
        created = tag.p.span['data-shared-at']
        article = tag.h4.get_text(strip=True)
        article_url = tag.h4.a['href']
        if article_url.startswith('/p/'):
            article_url = domain_name + article_url
        print 'image:',image
        print 'user:',user
        print 'user-url:',user_url
        print 'time:',created
        print 'article:',article
        print 'article-url:',article_url


        tag_a = tag.div.div.find_all('a')
        views = tag_a[0].get_text(strip=True)
        views = filter(str.isdigit, str(views))
        
        comments = tag_a[1].get_text(strip=True)
        comments = filter(str.isdigit, str(comments))

        tag_span = tag.div.div.find_all('span')
        likes = tag_span[0].get_text(strip=True)
        likes = filter(str.isdigit, str(likes))
        res = pattern.search(views)
        print 'views:',views
        print 'comments:',comments
        print 'likes:',likes

        try:
            tip = tag_span[1].get_text()
            tip = filter(str.isdigit, str(tip))
        except Exception as e:
            tip = 0
        print 'tip:', tip

if __name__ == '__main__':
    #get_article()
    get_details()

