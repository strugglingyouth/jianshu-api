#!/usr/bin/env python
# coding:utf-8


"""
    爬取简书热门的所有文章，总共 300 条
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
from colorama import init, Fore
from jianshu_api.settings import DATABASES

ct = 1


def get_data_url(base_url, domain_name):
    """
        获取 data-url
    """

    html = requests.get(base_url).content
    # html 是网页的源码，soup 是获得一个文档的对象
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    result = soup.find_all('button', class_="ladda-button")
    if result:
        for url in result:
            data_url = url['data-url']
        data_url = domain_name + data_url
        return data_url
    else:
        return 0


def get_details(mysql, page, base_url, domain_name, article_table):
    """
        获取文章详细信息
        将文章id，url，user，user_url，title，image，body，time，views，comments，likes，tip 存入 article中
    """

    global ct
    article = OrderedDict()
    html = requests.get(base_url).content

    # html 是网页的源码，soup 是获得一个文档的对象
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

    tags = soup.find_all('li', class_="have-img")
    print Fore.YELLOW + "-------page:%s-------articles:%s-------------------" % (page, len(tags))

    for tag in tags:
        article['article_image'] = tag.img['src'].split('?')[0]
        article['article_user'] = tag.p.a.get_text()

        article_user_url = tag.p.a['href']
        if article_user_url.startswith('/users/'):
            article['article_user_url'] = domain_name + article_user_url

        article['article_time'] = tag.p.span['data-shared-at']
        article_title = tag.h4.get_text(strip=True)
        article['article_title'] = article_title.replace('"', '\\"')
        article_url = tag.h4.a['href']
        article['article_id'] = article_url.split('/')[2]
        if article_url.startswith('/p/'):
            article_url = domain_name + article_url
        article['article_url'] = article_url
        tag_a = tag.div.div.find_all('a')
        try:
            views = tag_a[0].get_text(strip=True)
            article['article_views_count'] = filter(str.isdigit, str(views))
        except Exception as e:
            article['article_views_count'] = '0'
        try:
            comments = tag_a[1].get_text(strip=True)
            article['public_comments_count'] = filter(str.isdigit, str(comments))
        except Exception as e:
            article['public_comments_count'] = '0'

        tag_span = tag.div.div.find_all('span')
        try:
            likes = tag_span[0].get_text(strip=True)
            article['article_likes_count'] = filter(str.isdigit, str(likes))
        except Exception as e:
            article['article_likes_count'] = '0'

        # 阅读，评论，喜欢一定存在，打赏不一定有
        try:
            tip = tag_span[1].get_text()
            article['total_rewards_count'] = filter(str.isdigit, str(tip))
        except Exception as e:
            article['total_rewards_count'] = '0'

        body = get_body(article_url)

        article['article_body'] = body
        created_time = mysql.get_current_time()
        article['created'] = created_time

        print Fore.YELLOW + "----开始插入第 %s 条数据----" % ct

        # for key,values in article.items():
        #    print key+':'+values
        print "article_title:", article['article_title']
        result = mysql.insert_data(article_table, article)
        if result:
            print Fore.GREEN + "article_table：数据保存成功！"
        else:
            print Fore.RED + "article_table：数据保存失败！"

        ct += 1

    data_url = get_data_url(base_url, domain_name)
    
    # 获取 data-url 中的 page
    page = data_url.split('&')[-1]
     

    # 爬取 data_url 中的内容
    if data_url:
        page = data_url.split('&')[-1]
        get_details(mysql, page, data_url, domain_name, article_table)
    else:
        print Fore.GREEN + "----------------------------简书热门所有文章爬取完毕，共有%s篇--------------------------",ct
        return

def get_body(article_url):
    """
        获取文章内容
    """
    html = requests.get(article_url).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup('div', class_="show-content")
    body = str(tags[0])
    body = body.replace('"', '\\"')
    body = body.replace("'","\\'")
    return body


class Mysql(object):

    def get_current_time(self):
        created_time = time.strftime(
            '[%Y-%m-%d %H:%M:%S]',
            time.localtime(
                time.time()))
        created_time = created_time.split('[')[1]
        created_time = created_time.split(']')[0]
        return created_time

    def __init__(self, host, user, passwd, db, port):
        try:
            self.db = MySQLdb.connect(
                host=host,
                user=user,
                passwd=passwd,
                db=db,
                port=port,
                charset='utf8')
            self.cur = self.db.cursor()
        except MySQLdb.Error as e:
            print Fore.RED + '连接数据库失败'
            print Fore.RED + self.get_current_time(), '[%Y-%m-%d %H:%M:%S]', time.localtime(time.time())

    def insert_data(self, table, my_dict):
        try:
            cols = ','.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            values = '"' + values + '"'
            try:
              #  print "table:%s,cols:%s,values:%s." %(table, cols, values)
                sql = "insert into %s (%s) values(%s)" % (table, cols, values)
              #  print "sql:",sql
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
    article_table = 'jianshu_hotarticle'

    t = 1
    # 通过使用autoreset参数可以让变色效果只对当前输出起作用，输出完成后颜色恢复默认设置
    init(autoreset=True)
    domain_name = 'http://www.jianshu.com'
    base_url = 'http://www.jianshu.com'
    page = 1

    mysql = Mysql(host, user, passwd, db, port)
    get_details(mysql, page, base_url, domain_name, article_table)
