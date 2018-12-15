#!/usr/bin/python3
import requests
import time
import datetime
import re
import json
import random

# get your cookies and unionid
f = open("./raw")
for line in f.readlines():
    line = line.strip('\n')
    if re.search("Cookie:",line):
        c=line.split('Cookie: ',1)
    if re.search(r'unionidDst',line):
        m=line.split('"')
f.close()

cookies=c[1]
myline=m[7]
wx_nickname=m[15]
wx_header=m[11]

# header for tool
aheaders={ 'postman-token': '74162342-d591-d89c-2f7b-b949454bef22',
            'cache-control': 'no-cache',
            'content-type': 'application/json' }

session = requests.Session()

# header for zhongxin
headers= {
     "Host": "s.creditcard.ecitic.com",
     "Content-type": "application/json",
     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN",
     'X-Requested-With': 'XMLHttpRequest',
     'Cookie' : cookies,
     'Referer' : 'https://servicewechat.com/wx13b9861d3e9fcdb0/11/page-frame.html'
}


applytype="zhuli"

zhulist = []
for i in range(0,8):
    listurl = "http://144.34.215.167/site/get-unionid2?pageIndex=%s&pageSize=20&qqNumber=758192" % (i)
    rep = session.post(url=listurl,headers=aheaders).json()
    for otherid in rep['data']:
         zhulist.append(otherid['unionid'])

def zhuli():
        if applytype == "zhuli":
            #f = open("unionid.txt")
            #line = f.readline()
            for line in zhulist:
                print (line)
                #line = line.strip('\n')
                datajson={"unionidDst":line,
                          "unionidSrc":myline,
                          "wx_header":wx_header,
                          "wx_nickname":wx_nickname}
                print (datajson)
                zhuliapply = session.post(url="https://s.creditcard.ecitic.com/citiccard/gwapi/winterpig/assistance/enjoy",data=json.dumps(datajson),headers=headers).text
                print (zhuliapply)


zhuli()
