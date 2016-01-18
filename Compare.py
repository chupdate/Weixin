#coding=utf-8
author='__Han Chen__'
#对比old与new两个文件
import codecs

if __name__=='__main__':
    f_old=codecs.open('D:\\WeixinResult\\userInfo_old.txt','r',encoding='utf-8')
    f_new=open('D:\\WeixinResult\\userInfo_new.txt','r',encoding='utf-8')
    f_compare=codecs.open('D:\\WeixinResult\\userInfo_compare.txt','w',encoding='utf-8')
    dict_old={}
    dict_new={}
    for line in f_old.readlines():
        itemlist=line.split('\t')
        dict_old[itemlist[0]]=line
    for line in f_new.readlines():
        itemlist=line.split('\t')
        dict_new[itemlist[0]]=line
    for key in dict_old:
        if key not in dict_new:f_compare.write(dict_old[key])

