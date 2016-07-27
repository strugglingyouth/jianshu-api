#!/usr/bin/env python
# coding:utf-8


"""
    爬取简书新上榜的文章（首页 20 篇）
"""

__author__ = 'tianfeiyu'


import sys  
reload(sys)  
sys.setdefaultencoding('utf-8') 
from bs4 import BeautifulSoup
import requests
import MySQLdb
import time
from collections import OrderedDict
from colorama import init,Fore
from jianshu_api.settings import DATABASES



def get_details(mysql, base_url, domain_name, article_list_table, article_detail_table):
    """
        爬取文章并获取详细信息
    """
    article_list = OrderedDict()
    article_detail = OrderedDict()
    html = requests.get(base_url).content  

    # html 是网页的源码，soup 是获得一个文档的对象
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('li', class_="have-img")
    print Fore.YELLOW + "---------------all-------------------:",len(tags)
    ct = 1
    
    for tag in tags:
        image = tag.img['src'].split('?')[0]
        article_user = tag.p.a.get_text()

        article_user_url = tag.p.a['href']
        if article_user_url.startswith('/users/'):
            article_user_url = domain_name + article_user_url
        created = tag.p.span['data-shared-at']
        article_title = tag.h4.get_text(strip=True)
        article_title = article_title.replace('"', '\\"')
        article_url = tag.h4.a['href']
        article_id = article_url.split('/')[2]
        if article_url.startswith('/p/'):
            article_url = domain_name + article_url
        tag_a = tag.div.div.find_all('a')
        views = tag_a[0].get_text(strip=True)
        views = filter(str.isdigit, str(views))
        
        comments = tag_a[1].get_text(strip=True)
        comments = filter(str.isdigit, str(comments))

        tag_span = tag.div.div.find_all('span')
        likes = tag_span[0].get_text(strip=True)
        likes = filter(str.isdigit, str(likes))

        # 阅读，评论，喜欢一定存在，打赏不一定有
        try:
            tip = tag_span[1].get_text()
            tip = filter(str.isdigit, str(tip))
        except Exception as e:
            tip = 0

        body = get_body(article_url)
        article_list['article_id'] = article_id
        article_list['article_title'] = article_title
        article_list['article_url'] = article_url
        article_list['article_user'] = article_user
        article_list['article_user_url'] = article_user_url 

        article_detail['image'] = image
        article_detail['title'] = article_title
        article_detail['body'] = body
        article_detail['time'] = created
        article_detail['views_count'] = str(views)
        article_detail['public_comments_count'] = str(comments)
        article_detail['likes_count'] = str(likes)
        article_detail['total_rewards_count'] = str(tip)
        article_detail['article_abstract_id'] = article_id
        created_time = mysql.get_current_time()
        article_list['created'] = created_time
        article_detail['created'] = created_time
        
        print Fore.YELLOW + "----开始插入第 %s 条数据----" %ct
        for key,values in article_list.items():
            print key+':'+values

        result = mysql.insert_data(article_list_table, article_list)
        if result:
            print Fore.GREEN + "article_list_table：数据保存成功！" 
        else:
            print Fore.RED + "article_list_table：数据保存失败！" 
        
        result = mysql.insert_data(article_detail_table, article_detail)
        if result:
            print Fore.GREEN + "article_detail_table: 数据保存成功！" 
        else:
            print Fore.RED + "article_detail_table: 数据保存失败！"  
        ct += 1
def get_body(article_url):
    """
        获取文章内容
    """
    html = requests.get(article_url).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup('div', class_="show-content")
    body = str(tags[0])

    body = body.replace('"','\\"')
    return body

class Mysql(object):
    """
        保存文章到 mysql
    """
    def get_current_time(self):
        created_time = time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
        created_time = created_time.split('[')[1]
        created_time = created_time.split(']')[0]
        return created_time
    def __init__(self, host, user, passwd, db, port):
        try:
            self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset='utf8')
            self.cur = self.db.cursor()
        except MySQLdb.Error as e:
            print Fore.RED + '连接数据库失败'
            print Fore.RED + self.get_current_time(),'[%Y-%m-%d %H:%M:%S]',time.localtime(time.time())
                             
    def insert_data(self, table, my_dict):
        try:
            cols = ','.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            values = '"' + values + '"'
            try:
                sql = "insert into %s (%s) values(%s)" %(table, cols, values)
                result = self.cur.execute(sql) 
                self.db.commit()
                if result:
                    return 1
                else:
                    return 0 
            except MySQLdb.Error as e:
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                     print Fore.RED + self.get_current_time(), "数据已存在，未插入数据"
                else:
                    print Fore.RED + self.get_current_time(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
        except MySQLdb.Error as e:
            print Fore.RED + self.get_current_time(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':

    host = DATABASES['default']['HOST']
    user = DATABASES['default']['USER']
    passwd = DATABASES['default']['PASSWORD']
    db = DATABASES['default']['NAME']
    port = DATABASES['default']['PORT']

    # 保存文章所用到的表
    article_list_table = 'jianshu_articlelist' 
    article_detail_table = 'jianshu_articledetail'
    
    # 通过使用autoreset参数可以让变色效果只对当前输出起作用，输出完成后颜色恢复默认设置
    init(autoreset=True)
    domain_name = 'http://www.jianshu.com'
    base_url = 'http://www.jianshu.com/recommendations/notes'

    mysql = Mysql(host, user, passwd, db, port)
    get_details(mysql, base_url, domain_name, article_list_table, article_detail_table)

    




