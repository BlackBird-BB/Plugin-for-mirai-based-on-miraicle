import datetime
import json
import os
import re
import sys
import time
from http import cookiejar

import miraicle
import requests
from bs4 import BeautifulSoup
from lxml import etree

my_bot = None
my_msg = None
my_cx = None


# 超星登录


class chaoXinglogin(object):

    def __init__(self, school_id):
        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar(
            filename=f'data/chaoxing/core/{school_id}.txt')
        self.login_headers = {
            'Origin': 'http://passport2.chaoxing.com',
            'Referer': 'http://passport2.chaoxing.com/login?loginType=3&newversion=true&fid=-1&refer=http%3A%2F%2Fi.chaoxing.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'passport2.chaoxing.com',
        }
        # 登录完成的请求头
        self.login_complete_headers = {
            'Host': 'mooc1-2.chaoxing.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        }
        self.login_check_headers = {
            'Host': 'i.chaoxing.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        }
        self.account_url = 'http://passport2.chaoxing.com/unitlogin'
        # 机构登录data
        self.account_data = {
            'fid': '学校id',
            'uname': '',
            'numcode': '',
            'password': '',
            'refer': 'http%3A%2F%2Fi.chaoxing.com',
            't': 'true',
        }
        self.phone_url = 'http://passport2.chaoxing.com/fanyalogin'
        # 手机号登录data
        self.phone_data = {
            'fid': '-1',
            'uname': '',
            'password': '',
            'refer': 'http%3A%2F%2Fi.chaoxing.com',
            't': 'true',
            'forbidotherlogin': '0',
        }
        self.QR_code_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Host': 'passport2.chaoxing.com',
            'Referer': 'http://passport2.chaoxing.com/login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers = self.login_headers

    # 图片展示
    @staticmethod
    def show_img(file_name):
        my_bot.send_friend_msg(qq=my_msg.sender, msg=[miraicle.Image.from_file(file_name)])

    # 检查cookies
    def check_cookies(self):
        self.session.headers = self.login_check_headers
        try:
            # 加载cookies
            self.session.cookies.load(ignore_discard=True)
            url = "http://i.chaoxing.com/"
            response = self.session.get(url=url, allow_redirects=True)
            if response.status_code == 200:
                # print(response.text)
                return True
            else:
                return False
        except FileNotFoundError:
            return "无cookie文件"

    # 扫码登入所需的uuid,enc
    def get_uuid_enc(self):
        url = 'http://passport2.chaoxing.com/login'
        params = {
            'fid': '',
            'newversion': 'true',
            'refer': 'http://i.chaoxing.com',
        }
        response = self.session.get(url=url, params=params)
        text = response.text
        self.uuid = re.findall('<input.*?value="(.*?)".*?"uuid"/>', text)[0]
        self.enc = re.findall('<input.*?value="(.*?)".*?"enc"/>', text)[0]

    def QR_png(self):
        self.log(self, '二维码获取中......')
        self.get_uuid_enc()
        url = 'http://passport2.chaoxing.com/createqr'
        params = {
            'uuid': self.uuid,
            'fid': '-1',
        }
        self.session.headers = self.QR_code_headers
        response = self.session.get(url=url, params=params)
        if response.status_code == 200:
            self.log(self, '二维码获取成功')
            content = response.content
            # 这里照片数据为bytes形式，所以为'wb'
            with open('data/chaoxing/core/QR.png', 'wb') as f:
                f.write(content)
            self.log(self, '二维码保存成功')
            self.show_img(file_name='data/chaoxing/core/QR.png')
        else:
            self.log(self, '抱歉,获取二维码失败\n'
                           '程序将自动终止，请重新打开程序')
            sys.exit()

    # 扫码登录状态获取
    def getauthstatus(self):
        count = 0
        while True:
            getauthstatus_url = 'http://passport2.chaoxing.com/getauthstatus'
            data = {
                'enc': self.enc,
                'uuid': self.uuid,
            }
            response = self.session.post(url=getauthstatus_url, data=data)
            text = response.text
            if '未登录' not in text:
                dic = response.json()
                if not dic['status']:
                    self.uid = dic['uid']
                    self.nickname = dic['nickname']
                    self.log(self, '用户==》{}《==请您确认登录'.format(self.nickname))
                elif dic['status']:
                    self.log(self, '用户==》{}《==您已确认登录'.format(self.nickname))
                    return True
            else:
                self.log(self, '不要让人家苦苦等待嘛,请您扫一下二维码')
            # 请求50次，二维码将刷新一次
            count += count
            if count == 150:
                return False
            time.sleep(1)

    # 扫码登录
    def QR_code_sign(self):
        self.QR_png()
        while True:
            judge_info = self.getauthstatus()
            if judge_info:
                break
            else:
                self.QR_png()
        return ''

    # 登录入口
    def login(self):
        b = self.check_cookies()
        if b==True:
            self.log(self, '超星cookie有效')
        else:
            if b==False:
                self.log(self, '超星cookies失效')
            else:
                self.log(self, '没有超星cookie文件')
            self.session.headers = self.login_headers
            self.QR_code_sign()
            self.session.headers = self.login_check_headers
            url = "http://i.chaoxing.com/"
            response = self.session.get(url=url, allow_redirects=True)
            if response.status_code == 200:
                print('登录成功')
                self.session.cookies.save()
                print('cookie保存成功')
        self.session.headers = self.login_complete_headers
        return self.session

    @staticmethod
    def log(self, txt):
        print(f"[Chaoxing] {txt}")


def certain_eles(all_view, key):
    soup = BeautifulSoup(all_view.text, "lxml")
    all_eles = soup.find_all("a")
    cer_eles = []
    for i in all_eles:
        if i.has_attr("href") and key in i.attrs["href"]:
            cer_eles.append(i.attrs["href"])
    return cer_eles


def get_work(work_view):
    soup = BeautifulSoup(work_view.text, "lxml")
    all_eles = soup.find_all("div")
    work_eles = []
    for i in all_eles:
        if i.has_attr("class") and i.attrs["class"] == ["titTxt"]:
            work_eles.append(i)

    works = []
    for i in work_eles:
        work_str = i.text
        work_str = work_str.strip().replace(" ", "")
        work_list = work_str.split()

        st_time = datetime.datetime.strptime(work_list[1][5:], '%Y-%m-%d%H:%M')
        ed_time = work_list[2][5:].replace(" ", "")
        if ed_time != "":
            ed_time = datetime.datetime.strptime(
                work_list[2][5:], '%Y-%m-%d%H:%M')
        work = {
            "title": work_list[0],
            "start_time": st_time,
            "end_time": ed_time,
            "statue": work_list[-1]
        }
        works.append(work)
    return works


def get_all_work(authed_session):
    classes_header = {
        'Host': 'fycourse.fanya.chaoxing.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    }
    classes_term_view = authed_session.get(
        "http://fycourse.fanya.chaoxing.com/courselist/study", headers=classes_header)
    classes_term = certain_eles(classes_term_view, "/courselist/opencourse")

    classes_all_view = authed_session.get(
        "http://mooc1-2.chaoxing.com/visit/courses")
    classes_all = certain_eles(classes_all_view, "/visit/stucoursemiddle")

    print(f"[LOG] {len(classes_all)} classes in all!!!")
    print(f"[LOG] {len(classes_term)} classes this term!!!")

    url_base = "https://mooc1-2.chaoxing.com"
    rel = []
    for i in range(0, len(classes_term)):
        class_work = ""
        url = url_base + classes_all[i * 2]
        class_view = authed_session.get(url)
        class_view = etree.HTML(class_view.text)
        class_name_ele = class_view.xpath(
            r"/html/body/div[4]/div/h1/span[1]/a")
        if not len(class_name_ele):
            class_name_ele = class_view.xpath(
                r"/html/body/div[2]/div/h1/span[1]/a")
            if not len(class_name_ele):
                continue
        class_name = class_name_ele[0].text.replace("\n", "").replace("\t", "")
        work_ele = class_view.xpath(
            r"/html/body/div[4]/div/div/div[2]/ul/li[6]/a")
        works_url = url_base + work_ele[0].attrib["data"]
        works_view = authed_session.get(works_url)
        works = get_work(works_view)
        if len(works) != 0:
            class_work = f"{class_name}:\n"
            for work in works:
                class_work = class_work + f'''    {work["title"]}\n    开始时间:{work["start_time"]}\n    截止时间:{work["end_time"]}\n    {work["statue"]}\n'''
        rel.append(class_work)
    return rel

def downloadimg(url, path):
    rep = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'})
    with open(path, 'wb') as f:
        f.write(rep.content)


def get_notification(authed_session):
    notif_header = {
        'Host': 'notice.chaoxing.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    }
    notis_all_url = "https://notice.chaoxing.com/pc/notice/getNoticeList"
    notis_all_view = authed_session.get(
        notis_all_url, data={"type": "2"}, headers=notif_header)
    notis_all = json.loads(notis_all_view.text)
    notis_all = notis_all["notices"]["list"]
    contents = []
    for noti in notis_all:
        if not noti["redDot"]:
            imgs = noti["imgs"]
            main_str = f'''{noti["title"]}\n{noti["createrName"]}\n{noti["content"]}\n{noti["sendTime"]}'''
            authed_session.post(
                f'''https://notice.chaoxing.com/pc/notice/{noti["idCode"]}/detail''', data={"sendTag": 0},
                headers=notif_header)
            names = []
            for i in range(len(imgs)):
                img = imgs[i]
                name = f"data/chaoxing/noti/{noti['idCode']}/{i}.jpg"
                if not os.path.isdir(f"data/chaoxing/noti/{noti['idCode']}"):
                    os.mkdir(f"data/chaoxing/noti/{noti['idCode']}")
                downloadimg(img['imgUrl'], f"data/chaoxing/noti/{noti['idCode']}/{i}.png")
                names.append(name)
            content = {
                "str": main_str,
                "imgs": names
            }
            contents.append(content)
    return contents


@miraicle.Mirai.receiver("FriendMessage")
def chaoxing(bot: miraicle.Mirai, msg: miraicle.FriendMessage):
    global my_bot
    global my_msg
    global my_cx
    my_bot = bot
    my_msg = msg
    if msg.plain[:8] == "chaoxing":
        tmp = msg.plain.split()
        school_id = tmp[1]
        cmd = tmp[2]
        cx = chaoXinglogin(school_id)
        my_cx = cx
        cx.log(cx, "Started")
        auth_session = cx.login()
        if cmd == "Getwork":
            contents = get_all_work(auth_session)
            for i in contents:
                bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain(i)])
            bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain("目前就这些作业啦~")])
        elif cmd == "Getnoti":
            contents = get_notification(auth_session)
            bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain("这些是未读通知哦~")])
            for content in contents:
                bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain(content["str"])])
                for name in content["imgs"]:
                    bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Image.from_file(name)])
        else:
            bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain("参数错误哦~")])
