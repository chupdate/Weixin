#coding=utf-8
author='__Han Chen__'

import urllib.request,urllib.parse
import json
import time
import codecs

def getpostdata(idlist):
    user_list=[]
    for openid in idlist:user_list.append({'openid':openid,'lang': 'zh-CN'})
    postdata=json.dumps({'user_list':user_list }).encode('utf-8')
    return(postdata)

def timestamp_datetime(value):
    format = '%Y-%m-%d'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

class getuserinfolist:

    #获取access_token
    def gettoken(self):
        #appid=input('账号：')
        #password=input('密码：')
        appid=''
        appsecret=''
        url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+appsecret
        page=urllib.request.urlopen(url)
        result=page.read().decode()
        result=json.loads(result)
        self.token=result['access_token']
        print(self.token)

    #获取用户openid
    def getopenid(self):
        self.openidlist=[]
        next_openid=''
        while True:
            url='https://api.weixin.qq.com/cgi-bin/user/get?access_token='+self.token+'&next_openid='+next_openid
            page=urllib.request.urlopen(url)
            result=page.read().decode()
            result=json.loads(result)
            if result['count']==0:break
            self.openidlist.extend(result['data']['openid'])
            next_openid=result['next_openid']

    #获取用户基本信息
    def getinfolist(self):
        #首先获取所有分组
        groups={}
        url='https://api.weixin.qq.com/cgi-bin/groups/get?access_token='+self.token
        page=urllib.request.urlopen(url)
        result=page.read().decode()
        result=json.loads(result)
        for group in result['groups']:groups[group['id']]=group['name']
        f=codecs.open('D:\\WeixinResult\\userInfo.txt','w','utf-8')
        user_info_list=[]
        wrongidlist=[]
        k=0
        while self.openidlist:
            k+=1
            #每次获取100条
            l=len(self.openidlist)
            if (l>100):
                openidlist_tmp=self.openidlist[:100]
                postdata=getpostdata(openidlist_tmp)
                self.openidlist=self.openidlist[100:]
            else:
                openidlist_tmp=self.openidlist
                postdata=getpostdata(openidlist_tmp)
                self.openidlist=[]
            try:
                req=urllib.request.Request(
                    url='https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token='+self.token,
                    data=postdata
                )
                page=urllib.request.urlopen(req)
                result=page.read().decode()
                result=json.loads(result)
                print(k,':',result)
                user_info_list.extend(result['user_info_list'])
            except Exception:
                print('列表获取错误')
                wrongidlist.extend(openidlist_tmp)
        for user in user_info_list:
            if user['subscribe']==1:
                f.write(user['openid']+'\t'+user['nickname']+'\t'+str(user['sex'])+'\t'+user['city']+'\t'+user['province']
                        +'\t'+timestamp_datetime(user['subscribe_time'])+'\t'+user['remark']+'\t'+groups[user['groupid']]+'\r\n')
        #解决wrong列表问题
        for openid in wrongidlist:
            url='https://api.weixin.qq.com/cgi-bin/user/info?access_token='+self.token+'&openid='+openid+'&lang=zh_CN'
            page=urllib.request.urlopen(url)
            result=page.read()
            try:
                result=result.decode()
                user=json.loads(result)
                if user['subscribe']==1:
                    f.write(user['openid']+'\t'+user['nickname']+'\t'+str(user['sex'])+'\t'+user['city']+'\t'+user['province']
                            +'\t'+timestamp_datetime(user['subscribe_time'])+'\t'+user['remark']+'\t'+groups[user['groupid']]+'\r\n')
            except Exception:
                print('输出错误',result)
        f.close()

if __name__=='__main__':
    ex_infolist=getuserinfolist()
    #ex_infolist.gettoken()
    ex_infolist.token=''
    ex_infolist.getopenid()
    ex_infolist.getinfolist()


