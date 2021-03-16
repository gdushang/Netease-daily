# -*- coding: utf-8 -*-
import requests
import random
import hashlib
import json

false = False
null = None
true = True
cookie = None

user = ''  # 账号
pwd = ''  # 密码
fast_url = 'http://music.20mua.com'  # 打卡网址
url = [fast_url + '/api.php?do=login', fast_url + '/api.php?do=sign', fast_url + '/api.php?do=daka']  # api


def message(pwd):
    h1 = hashlib.md5()
    h1.update(pwd.encode('utf-8'))
    return h1.hexdigest()


data = {
    'uin': user,
    'pwd': message(pwd),
    'r': random.random()
}  # uin是账号，pwd是密码 md5加密，r推测是密钥之类的，没有r值不行，r值貌似确实没用，他就是生成了一个随机数
hade = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


def start(date):
    a = 0
    for i in range(3):
        user_start = requests.post(url=url[i], data=date, headers=hade)  # 循环api
        if i == 0:
            hade['cookie'] = user_start.headers.get('Set-Cookie')  # 获取并设置cookie
            login = json.loads(user_start.text)
            a += 1
            if login is not None:
                print('密码或者账号错误')
                break
            else:
                login = login.get('profile').get('nickname')
        elif i == 1:
            qiandao = json.loads(user_start.text).get('code')
            if qiandao is not None:
                qiandao = '签到成功'
            else:
                qiandao = json.loads(user_start.text).get('msg')
            a += 1
        # 获取签到结果
        elif i == 2:
            daka = str(json.loads(user_start.text).get('count'))  # 获取打卡结果  就是那个310首音乐
            a += 1
    if a == '3':
        pr = "用户：" + login + '\n' + qiandao + '\n' + '增加了：' + daka
        u = ''  # 推送日志
        # rizhi = requests.get(url=u)
        return pr


def main_handler(event, context):
    a = start(data)
    return a


#main_handler(123, 231)
#本地运行把上一行的#删掉
