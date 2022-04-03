import miraicle
from miraicle.mirai import Mirai
import requests
import json
import time
import os

r18_g = {}
r18_p = {}

def get_img(url):
    name = "data/setu/" + \
        str(time.time()).replace(".", "_")+".jpg"
    os.system(
        f'''proxychains curl {url} --output {name}''')
    return name

@miraicle.Mirai.receiver("FriendMessage")
def setu_p(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.sender == 602198790 and msg.plain[:4] == 'set ':
        tar = int(msg.plain.split()[1])
        if tar not in r18_p.keys():
            r18_p[tar] = 0
        opt = int(msg.plain.split()[2])
        r18_p[tar] = opt
    elif msg.plain[:2] == '色图':
        print("[setu] Started")
        if msg.sender not in r18_p.keys():
            r18_p[msg.sender] = 0
        tag = msg.plain[3:].split()
        content = {
            'r18': r18_p[msg.sender],
            'tag': tag
        }
        res = requests.post(
            url="https://api.lolicon.app/setu/v2", json=content).json()
        if len(res['data']) == 0:
            bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain(
                "这个标签没找到色色的图片欸~(用英语或者换个标签吧)"), miraicle.Face.from_face_id(176)])
            bot.send_friend_msg(qq=msg.group, msg=[miraicle.Plain("什么？你非要冲？？？"), miraicle.Face.from_face_id(
                104), miraicle.Plain("那满足你吧"), miraicle.Face.from_face_id(101)])
            content = {'r18': r18_p[msg.sender], 'tag': []}
            res = requests.post(
                url="https://api.lolicon.app/setu/v2", json=content).json()
            
            data = f'''标题：{res['data'][0]['title']}\nUID: {res['data'][0]['uid']}\n作者: {res['data'][0]['author']}\ntags: {res['data'][0]['tags']}\n'''
            img = get_img(res['data'][0]['urls']['original'])
            bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain(data)])
            msg_id = bot.send_friend_msg(qq=msg.sender, msg=[Mirai.Image.from_file]).get('messageId', 0)
        else:
            data = f'''标题：{res['data'][0]['title']}\nUID: {res['data'][0]['uid']}\n作者: {res['data'][0]['author']}\ntags: {res['data'][0]['tags']}\n'''
            img = get_img(res['data'][0]['urls']['original'])
            print(img)
            bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain(
                data)])
            msg_id = bot.send_friend_msg(
                qq=msg.sender, msg=miraicle.Image.from_file(img)).get('messageId', 0)
        time.sleep(10)
        bot.recall(msg_id)

@miraicle.Mirai.receiver("GroupMessage")
def setu(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.plain[:8] == 'set r18 ' and msg.sender == 602198790:
        if msg.group not in r18_g.keys():
            r18_g[msg.group] = 0
        # 管理员管理r18
        r18_g[msg.group] = int(msg.plain[8:])
    elif msg.plain[:2] == '色图':
        # 色图
        if msg.group not in r18_g.keys():
            r18_g[msg.group] = 0
        tag = msg.plain[3:].split()
        content = {
            'r18': r18_g[msg.group],
            'tag': tag
        }
        res = requests.post(
            url="https://api.lolicon.app/setu/v2", json=content).json()
        if len(res['data']) == 0:
            bot.send_group_msg(group=msg.group, msg=[miraicle.Plain(
                    "这个标签没找到色色的图片欸~(用英语或者换个标签吧)"), miraicle.Face.from_face_id(176)])
            bot.send_group_msg(group=msg.group, msg=[miraicle.Plain("什么？你非要冲？？？"), miraicle.Face.from_face_id(
                    104), miraicle.Plain("那满足你吧"), miraicle.Face.from_face_id(101)])
            content = {'r18': r18_g[msg.group], 'tag': []}
            res = requests.post(
                url="https://api.lolicon.app/setu/v2", json=content).json()
            data = f'''标题：{res['data'][0]['title']}\nUID: {res['data'][0]['uid']}\n作者: {res['data'][0]['author']}\ntags: {res['data'][0]['tags']}\n'''
            img = get_img(res['data'][0]['urls']['original'])
            bot.send_group_msg(group=msg.group, msg=[miraicle.Plain(
                data)], quote=msg.id)
            msg_id = bot.send_group_msg(group=msg.group, msg=[
                miraicle.Image.from_file(img)], quote=msg.id).get('messageId', 0)
        else:
            data = f"标题：{res['data'][0]['title']}\nUID: {res['data'][0]['uid']}\n作者: {res['data'][0]['author']}\ntags: {res['data'][0]['tags']}\n"
            img = get_img(res['data'][0]['urls']['original'])
            msg_id = bot.send_group_msg(group=msg.group, msg=[miraicle.Plain(
                data)], quote=msg.id)
            msg_id = bot.send_group_msg(group=msg.group, msg=[
                miraicle.Image.from_file(img)], quote=msg.id).get('messageId', 0)
        time.sleep(10)
        bot.recall(msg_id)
                            



@miraicle.Mirai.receiver("GroupMessage")
@miraicle.Mirai.receiver("FriendMessage")
def joke(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.plain == '讲个笑话':
        # 讲笑话
        res = requests.post("https://api.vvhan.com/api/xh?type=json")
        res = json.loads(res.text)
        rel = res['joke']
        try:
            bot.send_group_msg(group=msg.group, msg=rel)
        except:
            bot.send_friend_msg(qq=msg.sender, msg=rel)


@miraicle.Mirai.receiver("GroupMessage")
@miraicle.Mirai.receiver("FriendMessage")
def ai(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if "2441825920" in msg.text:
        # 人工智障
        response = requests.get(
            "http://api.qingyunke.com/api.php?key=free&appid=0&msg="+msg.plain)
        rel = json.loads(response.text)
        rel = rel['content']
        try:
            bot.send_group_msg(group=msg.group, msg=rel)
        except:
            bot.send_friend_msg(qq=msg.sender, msg=rel)
