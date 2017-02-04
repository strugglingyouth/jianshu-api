#!/usr/bin/env python
# coding:utf-8


"""
    在简书中搜索相关文章
"""


__author__ = 'tianfeiyu'


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import time
from collections import OrderedDict
from colorama import init, Fore
from jianshu_api.settings import DATABASES
import requests


ct = 1

def get_pages(mysql, base_url, domain_name, article_table, search_name):

    """
        获取文章详细信息
        将文章id，url，user，user_url，title，image，body，time，views，comments，likes，tip 存入 article中
    """

    html = requests.get(base_url).content

    result = eval(html)

    type = result['type']

    endpages = result['total_pages'] + 1

    print "type:%s,endpages:%s" %(type,endpages)
    for page in range(1, endpages):
        base_url = 'http://www.jianshu.com/search/do?q=' + search_name + '&page=%s&type=%s' %(page, type)
        print base_url
        time.sleep(10)
        get_details(mysql, base_url, domain_name, article_table)

def get_details(mysql, base_url, domain_name, article_table ):
    """

    """

    global ct
    article = OrderedDict()
    #cmd = 'curl -s --connect-timeout 10 %s' % base_url
    #p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #res = p.stdout.readlines()
    html = requests.get(base_url).content
    result = eval(html)
    #result = eval(res[0])
    print result
    for tag in result['entries']:
        article['article_id'] = str(tag['id'])
        article['article_title'] = tag['title']
        article['article_url'] = domain_name + '/p/' + tag['slug']
        article['article_user'] = tag['user']['nickname']
        article['article_user_url'] = domain_name + '/users/' + tag['user']['slug']
        article['article_time'] = tag['first_shared_at']
        article['article_views_count'] = str(tag['views_count'])
        article['public_comments_count'] = str(tag['public_comments_count'])
        article['article_likes_count'] = str(tag['likes_count'])
        article['total_rewards_count'] = str(tag['total_rewards_count'])

        created_time = mysql.get_current_time()
        article['created'] = created_time

        print Fore.YELLOW + "----开始插入第 %s 条数据----" % ct

        for key,values in article.items():
            print key+':'+values
        result = mysql.insert_data(article_table, article)
        if result:
            print Fore.GREEN + "article_table：数据保存成功！"
        else:
            print Fore.RED + "article_table：数据保存失败！"

        ct += 1


class Mysql(object):

    def get_current_time(self):
        created_time = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(
                time.time()))
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
    article_table = 'jianshu_searcharticle'

    t = 1
    # 通过使用autoreset参数可以让变色效果只对当前输出起作用，输出完成后颜色恢复默认设置
    init(autoreset=True)

    search_name = 'python'
    domain_name = 'http://www.jianshu.com'
    base_url = 'http://www.jianshu.com/search/do?q=' + search_name

    mysql = Mysql(host, user, passwd, db, port)
    get_pages(mysql, base_url, domain_name, article_table, search_name)



