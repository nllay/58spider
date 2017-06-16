# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#初始化
def startSpider():
    htmlHead ='''
        <html>
            <head>
                <style type="text/css">
                    .tab{border-top:1px solid #000;border-left:1px solid #000;text-align:center}
                    .tab td{border-bottom:1px solid #000;border-right:1px solid #000;}
                </style>
            </head>
            <body>
                <table class="tab" cellspacing="0" cellpadding="0" width="100%" >
    '''

    fo = open('result.html','w+')
    fo.write(htmlHead)
    fo.close()

    header = {'title':u'标题','money':u'价格','payType':u'付款方式','time':u'时间','from':u'来自','phone':u'电话','link':u'链接','body':u'详细描述'}
    toHtml(header)


#结束
def endSpider():
    htmlend ='''
                </table>
            </body>
        </html>
    '''

    fo = open('result.html','a+')
    fo.write(htmlend)
    fo.close()

#数据封装,并输出到文件
def toHtml(body):
    bodyText = '<tr><td>'+body['title']+'</td><td>'+body['money']+'</td><td>'+body['payType']+'</td><td width="100px">'+body['time']+'</td><td>'+body['from']+'</td><td>'+body['phone']+'</td><td><a href=\''+body['link']+'\' >链接地址</a></td><td width="500px">'+body['body']+'</td></tr>'
    fo = open('result.html','a+')
    fo.write(bodyText)
    fo.close()

#解析详情页面，获取信息
def getHomeAbout(url):
    htmlCode = getHtmlCode(url)
    soup = BeautifulSoup(htmlCode,'lxml')
    #             标题/       价格/      付款方式/     时间/     来自/     电话/       链接/   详细描述
    homeAbout = {'title':'','money':'','payType':'','time':'','from':'','phone':'','link':'','body':''}
    try:
        homeAbout['title'] = soup.select('.f20')[0].text
        homeAbout['money'] = soup.select('.f36')[0].text
        homeAbout['payType'] = soup.select('.f16 .c_333')[0].text
        homeAbout['time'] = soup.select('.house-update-info')[0].text
        homeAbout['from'] = soup.select('.c_000')[0].text
        try:
            homeAbout['phone'] = soup.select('.phone-num')[0].text
        except IndexError:
            homeAbout['phone'] = u'该用户选择隐私保护'
        homeAbout['link'] =url
        homeAbout['body'] = soup.select('.a2')[0].text
    except IndexError:
        print u'访问过于频繁，无法获取到数据,程序中断'
        sys.exit(1)
    return homeAbout

#解析主列表页面，提取信息
def getIndexAbout(url):
    
    htmlCode = getHtmlCode(url)
    soup = BeautifulSoup(htmlCode,'lxml')
    #标题   h2 a   解析结果short开头表示置顶，jxjump地址开头表示加精
    homeList = soup.select('h2')

    links = []
    for link in homeList:
        links.append(link.a['href'])
    return links
    
#获取页面源码
def getHtmlCode(url):
    urlCode = requests.get(url)
    urlCode.encoding = 'utf-8'
    urlCode = urlCode.text
    return urlCode

#主函数
def main():
    startSpider()

    print 'go...'
    #wh：武汉     hongshan：洪山      pn3：第三页    http://wh.58.com/hongshan/chuzu/pn3/
    
    startSpider()
    for i in range(0,10):
        url = 'http://wh.58.com/hongshan/chuzu/pn'+ str(i) +'/'

        indexLinks = getIndexAbout(url)
        print u'第'+ str(i+1) +'页列表解析完毕...'
        #延迟1秒请求，防止验证码
        time.sleep(1)
        for indexLink in indexLinks:
            #延迟1秒请求，防止验证码
            time.sleep(1)
            homeAbout = getHomeAbout(indexLink)
            #录入数据
            toHtml(homeAbout)
        print u'第'+ str(i+1) +'详细数据录入完毕...'
    
    endSpider()


if __name__ == "__main__":
    main()
