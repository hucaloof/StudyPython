# _*_ coding:utf-8 _*_

from lxml import etree
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def search(keyword):
   	url = 'http://www.mp4ba.com/search.php?keyword=%s' % keyword
   	page = requests.get(url)
   	html = etree.HTML(page.text)
   	selector = html.xpath('//*[@id="data_list"]/tr[starts-with(@class,"alt")]')
   	infolist = []
   	for each in selector:
   		info = {}
   		info['title'] = each.xpath('td[@style="text-align:left;"]')[0].xpath('string(.)').replace('\r', '').replace('\n', '').replace(' ', '')
   		info['link'] = 'http://www.mp4ba.com/' + each.xpath('td[@style="text-align:left;"]/a/@href')[0]
		info['size'] = each.xpath('td[4]/text()')[0]
		infolist.append(info)
	return infolist

def getDownurl(link):
    page = requests.get(link)
    html = etree.HTML(page.text)
    for each in html:
        links = each.xpath('//*[@id="magnet"]/@href')[0]
    return links

if __name__=='__main__':
    mname = raw_input('请输入要搜索的电影名:')
    # mname = '冰与火之歌'
    result = search(mname)
    if not result:
        print u'没有搜索到结果'
    print u'搜索到%d部电影:'%len(result)
    for r in result:
        downurl = getDownurl(r['link'])
        print '''
电影名：%s
大小：%s
磁力链接：%s\n''' % (r['title'], r['size'], downurl)