#/usr/bin/env python
# -*- coding:utf-8 -*-
#BETA 1.0

from bs4 import BeautifulSoup
import urllib2
import datetime
import time
import codecs
import cookielib
import random
import threading
import os,sys


def getInfo(max_index_user=5):
    stock_news_site = "http://www.8btc.com/sitemap?pg="
 
    my_userAgent = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)']
    index = 1
    max_index = max_index_user
    num = 1
    temp_time = time.strftime("[%Y-%m-%d]-[%H-%M]", time.localtime())

    store_filename = "StockNews-%s.log" % temp_time
    f = codecs.open(store_filename, 'wb', 'utf-8')

    while index <= max_index:
        #random_choice_one_header
        user_agent = random.choice(my_userAgent)
        # print user_agent
        company_news_site = stock_news_site + str(index)
        # content = urllib2.urlopen(company_news_site)
        headers = {'User-Agent': user_agent, 'Host': "www.8btc.com", 'DNT': '1',
                   'Accept': 'text/html, application/xhtml+xml, */*', }
        req = urllib2.Request(url=company_news_site, headers=headers)
        resp = None
        raw_content = ""
        resp = urllib2.urlopen(req, timeout=30)
        raw_content = resp.read()
        resp.close()
        raw_content1 = BeautifulSoup(raw_content, "html.parser")
        article_links = raw_content1.find_all("a", hidefocus="hidefocus")
        for url in article_links:
            url_href = url.get('href')
            article_url = "http://www.8btc.com/sitemap" + url_href
            #article_title = url.get('title')
            #f.write("No.%s \n\t%s \n\t---> %s \n\n" %(str(num),article_title, article_url))
            
            #get_single_article
            article = ""
            article_page = urllib2.Request(url = article_url, headers = headers)
            article_page2 = urllib2.urlopen(article_page, timeout=30)
            article = article_page2.read()
            article_page2.close()
            article_content = BeautifulSoup(article, 'html.parser')
            Art_title = article_content.h1.string
            Art_content = article_content.find_all('div', class_="article-content")
            #Art_title = art_title.decode('unicode-escape')
            #Art_content = art_content.decode('unicode-escape')(
            #for tit in Art_title.
            print Art_title
            print Art_content
            f.write("No.%s \n\t%s  \n\t %s \n\n" %(str(num), Art_title, Art_content))

            
            
            
            
            
            num = num + 1
        



        index = index + 1
    f.close()






""" 
        try:
            resp = urllib2.urlopen(req, timeout=30)

        except urllib2.HTTPError as e:
            e.fp.read()
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                print "error code %d" % e.code
            elif hasattr(e, 'reason'):
                print "error reason %s " % e.reason

        finally:
            if resp:
                raw_content = resp.read()
                time.sleep(2)
                resp.close()

        soup = BeautifulSoup(raw_content, "html.parser")
        all_content = soup.find_all("span", "time")

        for i in all_content:
            news_time = i.string
            node = i.next_sibling
            str_temp = "No.%s \n%s\t%s\n---> %s \n\n" % (str(num), news_time, node['title'], node['href'])
            #print "inside %d" %num
            #print str_temp
            fOpen.write(str_temp)
            num = num + 1

        #print "index %d" %index
        index = index + 1

    fOpen.close()
"""

def execute_task(n=60):
    period = int(n)
    while True:
        print datetime.datetime.now()
        getInfo(3)
        
        time.sleep(60 * period)
        


if __name__ == "__main__":

    # dir_file_manager
    sub_folder = os.path.join(os.getcwd(), "stock")
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    os.chdir(sub_folder)

    start_time = time.time()  # user can change the max index number getInfo(10), by default is getInfo(5)
    if len(sys.argv) <2:
        n = raw_input("How often checking articles of this script ?(min) \n")
    else:
        n=int(sys.argv[1])
    execute_task(n)
    end_time = time.time()
    print "Total time: %s s." % str(round((end_time - start_time), 4))

