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

# apply or onestepapply
applytype="apply"
#applytype="onestepapply"

# sleep time
maxcount = 1000
sleeptime = 1

############don't modify under############################################################################
currenturl='https://s.creditcard.ecitic.com/citiccard/gwapi/uc/winterpig/pig/querycurrent'
applyurl='https://s.creditcard.ecitic.com/citiccard/gwapi/uc/winterpig/pig/apply'
onestepapplyurl="https://s.creditcard.ecitic.com/citiccard/gwapi/uc/winterpig/pig/onestepapply"
prizeurl="https://s.creditcard.ecitic.com/citiccard/gwapi/uc/winterpig/user/reward"

session = requests.Session()

headers= {
     'Host' : 's.creditcard.ecitic.com',
     'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN',
     'Cookie' : cookies,
     'Content-Type': 'application/json;charset=utf-8',
     'X-Requested-With' : 'XMLHttpRequest',
     'Referer' : 'https://servicewechat.com/wx13b9861d3e9fcdb0/10/page-frame.html'
}

def runpig():
    count = 0
    reward = session.post(url=prizeurl,headers=headers)
    if '重新登录' in reward.text:
        print('请更新Cookies')
        exit()
    else: 
        print ("目前获得的奖品有:")
        for i in reward.json()['data']:
            print (i['goodsName'])

    while count < maxcount:
        count = count + 1

        print ('   ')
        print ('-------我是分割线-----------')
        print ('当前运行第%s次，一共%s次' % (count,maxcount))

        respurl=session.post(url=currenturl,headers=headers).json()
        if respurl:
            shuazi = respurl['data']['residue']
            zhuid = respurl['data']['pig']['id']
            pigTypeId = respurl['data']['pig']['pigTypeId']
            pigTypeName = respurl['data']['pig']['pigTypeName']
            currentApply = respurl['data']['pig']['currentApply']
            totalApply = respurl['data']['pig']['totalApply']
        else:
            print('出错了')

        color = ['red','black','gold','green','blue']
        if pigTypeId == 6:
            pigDetail = { 'pigDetail':[ {'sec': 'face','color': (random.choice(color)) },
                      {'sec': 'nose','color': (random.choice(color)) },
                      {'sec': 'body','color': (random.choice(color)) },
                      {'sec': 'handleft','color': (random.choice(color)) },
                      {'sec': 'handright','color': (random.choice(color)) },
                      {'sec': 'footleft','color': (random.choice(color)) },
                      {'sec': 'footright','color': (random.choice(color)) },
                      {'sec': 'earleft','color': (random.choice(color)) },
                      {'sec': 'earright','color': (random.choice(color)) },
                      {'sec': 'pants','color': (random.choice(color))} ]}
        elif pigTypeId == 4 or pigTypeId == 2 or pigTypeId == 3 or pigTypeId == 1:
            pigDetail = { 'pigDetail':[ { 'sec': 'face' , 'color': (random.choice(color)) },
                      { 'sec': 'nose' , 'color': (random.choice(color)) },
                      { 'sec': 'body' , 'color': (random.choice(color)) },
                      { 'sec': 'hand' , 'color': (random.choice(color)) },
                      { 'sec': 'foot' , 'color': (random.choice(color)) } ]}
        elif pigTypeId == 5:
            pigDetail = { 'pigDetail':[
                      { 'sec': 'face', 'color': (random.choice(color)) },
                      { 'sec': 'nose', 'color': (random.choice(color)) },
                      { 'sec': 'body','color': (random.choice(color)) },
                      { 'sec': 'handleft','color': (random.choice(color)) },
                      { 'sec': 'handright','color': (random.choice(color)) },
                      { 'sec': 'footleft','color': (random.choice(color)) },
                      { 'sec': 'footright','color': (random.choice(color)) },
                      { 'sec': 'earleft','color': (random.choice(color)) },
                      { 'sec': 'earright','color': (random.choice(color)) },
                      { 'sec': 'hair','color': (random.choice(color))} ] }

        print ('当前刷子数量:%s' % shuazi)
        print ('这是一头%s，编号%s，需要使用%s刷子' % (pigTypeName,zhuid,totalApply))

        if applytype == "apply":
            if shuazi > 10:
                random.shuffle(pigDetail['pigDetail'])
                print ('开始涂猪')
                for i in pigDetail['pigDetail']:
                    sleeptime = random.randint(120,150)
                    time.sleep(sleeptime)
                    print ('部位: %s ，颜色：%s' % (i['sec'],i['color']))
                    repapply = session.post(url=applyurl,data=json.dumps({"userApply":i}),headers=headers)
                    if 'goodsName' in repapply.text:
                        print(i['sec'], repapply.json()['data']['lotteryData']['goodsName'], repapply.json()['data']['lotteryData']['goodsDesc'])
                    else:
                        print(i['sec'], repapply.json()['retMsg'])
            else:
                print ("刷子不够了....")
                break

        elif applytype == "onestepapply":
            if shuazi > 4:
                sleeptime = random.randint(40,60)
                time.sleep(5)
                onestepapply = session.post(url=onestepapplyurl,data=json.dumps(pigDetail),headers=headers).json()
                #print (onestepapply)
                rep = onestepapply
                result = rep['retMsg']
                lotteryData = rep['data']['lotteryData']

                if not lotteryData:
                    print ("没中奖....")
                else:
                    print (lotteryData['goodsName'])
            else:
                print ("刷子不够了....")
                break

runpig()
