#!/usr/bin/env python
# coding:utf-8

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8') 

from bs4 import BeautifulSoup
import requests
import MySQLdb
import time
from collections import OrderedDict


domain_name = 'http://www.jianshu.com'
base_url = 'http://www.jianshu.com/recommendations/notes'

html = requests.get(base_url).content

# html 是网页的源码，soup 是获得一个文档的对象
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

def get_details():
    """
        获取文章详细信息
    """
    article_list = OrderedDict()
    article_detail = OrderedDict()
    tags = soup.find_all('li', class_="have-img")
    print "all:",len(tags)
    for tag in tags:
        image = tag.img['src'].split('?')[0]
        article_user = tag.p.a.get_text()

        article_user_url = tag.p.a['href']
        if article_user_url.startswith('/users/'):
            article_user_url = domain_name + article_user_url
        created = tag.p.span['data-shared-at']
        article_title = tag.h4.get_text(strip=True)
        article_url = tag.h4.a['href']
        article_id = article_url.split('/')[2]
        if article_url.startswith('/p/'):
            article_url = domain_name + article_url
        #print 'image:',image
        #print 'user:',article_user
        #print 'user-url:',article_user_url
        #print 'time:',created
        #print 'article:',article_title
        #print 'article-url:',article_url
        #print 'article-id:',article_id


        tag_a = tag.div.div.find_all('a')
        views = tag_a[0].get_text(strip=True)
        views = filter(str.isdigit, str(views))
        
        comments = tag_a[1].get_text(strip=True)
        comments = filter(str.isdigit, str(comments))

        tag_span = tag.div.div.find_all('span')
        likes = tag_span[0].get_text(strip=True)
        likes = filter(str.isdigit, str(likes))
        #print 'views:',views
        #print 'comments:',comments
        #print 'likes:',likes

        #阅读，评论，喜欢一定存在，打赏不一定有
        try:
            tip = tag_span[1].get_text()
            tip = filter(str.isdigit, str(tip))
        except Exception as e:
            tip = 0
        #print 'tip:', tip

        body = get_body(article_url)
        article_list['article_id'] = article_id
        article_list['article_title'] = article_title
        article_list['article_url'] = article_url
        article_list['artile_user'] = article_user
        
        article_detail['image'] = image
        article_detail['title'] = article_title
        article_detail['body'] = body
        article_detail['time'] = created
        article_detail['views'] = views
        article_detail['comments'] = comments
        article_detail['likes'] = likes
        article_detail['tip'] = tip
        for key,values in article_list.items():
            print key+':'+values
        for key,values in article_detail.items():
            print key,values
        break
    return article_list,article_detail
def get_body(article_url):
    """
        获取文章内容
    """
    html = requests.get(article_url).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup('div', class_="show-content")
    body = tags[0]
    print 'body:',body
    #print 'img:', tags[0].img['src']
    #body = ""
    #for p in tags[0].find_all('p'):
    #     body += '\n    ' + p.get_text()
    #print body.decode()
    return body
def save_data():
    """
        保存数据到 mysql
    """
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='jianshu', port=3306)
        cur = conn.cursor()
        conn.select_db('jianshu')
    except MySQLdb.error as e:
        print 'Error in mysql:', e


class Mysql:

    def get_current_time(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    def __init__(self, host, user, passwd, db, port):
        try:
            self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port)
            self.cur = self.db.cursor()
        except MySQLdb.error as e:
            print self.get_current_time(),'[%Y-%m-%d %H:%M:%S]',time.localtime(time.time())
                             
    def insert_data(self, table, my_dict):
        try:
            cols = ','.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            sql = "insert into %s (%s) values(%s)" %(table, cols, '"'+values+'"')
            try:
                result = self.cur.execute(sql) 
                insert_id = self.db.insert_id()
                self.db.commit()
                if result:
                    return insert_id
                else:
                    return 0 
            except MySQLdb.error as e:
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                     print self.getCurrentTime(), "数据已存在，未插入数据"
                else:
                    print self.getCurrentTime(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
        except MySQLdb.error as e:
            print self.get_current_time(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':

    host = '127.0.0.1'
    user = 'root'
    passwd = '123456'
    db = 'jianshu'
    port = 3306
    article_list_table = 'jianshu_artilcelist' 
    article_detail_table = 'jianshu_artilcedetail'
    
    article_list,article_detail = get_details()

    mysql = Mysql(host, user, passwd, db, port)
    mysql.insert_data(article_list_table, article_list)
    mysql.insert_data(article_detail_table, article_detail)
    




