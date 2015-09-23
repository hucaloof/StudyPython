#!/usr/bin/python
#_*_ coding:utf-8 _*_

import urllib2
import re
import sys

def search(keyword):
    url = 'http://www.mp4ba.com/search.php?keyword=%s'%keyword
    page = urllib2.urlopen(url)
    html = page.read()
    infolist = []
    try:
        for movieurl in re.findall(r'<tr class="alt\d"(.*?)</tr>',html,re.S):
            info = {}
            info['name'] = ''.join(re.findall(r'target="_blank">(.*?)<span class="keyword">(.*?)</span>(.*?)</a>',movieurl,re.S)[0]).replace('\r\n','').replace(' ','')
            info['url']  = 'http://www.mp4ba.com/' + re.findall(r'href="(show.php.*?)"',movieurl)[0]
            info['filesize'] = re.findall(r'<td>(.*[M|G]B?)</td>',movieurl)[0]
            infolist.append(info)
        return infolist
    except:
        return {}

def getDownurl(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return re.findall(r'<a id="magnet" href="(.*?)">',html)[0]

if __name__=='__main__':
    mname = raw_input('请输入要搜索的电影名:')
    result = search(mname)
    if not result:
        print '没有搜索到结果'
        sys.exit(2)
    print '搜索到%d部电影:'%len(result)
    i = 1
    for r in result:
        downurl = getDownurl(r['url'])
        print '''
%d
电影名:%s
大小:%s
详情链接:%s
下载链接:%s
'''%(i,r['name'],r['filesize'],r['url'],downurl)
        i += 1

