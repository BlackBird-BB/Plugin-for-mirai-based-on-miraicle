import miraicle
import requests
import json

r18 = {}


@miraicle.Mirai.receiver("GroupMessage")
@miraicle.Mirai.receiver("FriendMessage")
def setu(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.plain[:8] == 'set r18 ' and msg.sender == 602198790:
        if msg.group not in r18.keys():
            r18[msg.group] = 0
        # 管理员管理r18
        r18[msg.group] = int(msg.plain[8:])
    elif msg.plain[:2] == '色图':
        # 色图
        if msg.group not in r18.keys():
            r18[msg.group] = 0
        tag = msg.plain[3:].split()
        content = {
            'r18': r18[msg.group],
            'tag': tag
        }
        res = requests.post(
            url="https://api.lolicon.app/setu/v2", json=content).json()
        if len(res['data']) == 0:
            try:
                bot.send_group_msg(group=msg.group, msg=[miraicle.Plain(
                    "这个标签没找到色色的图片欸~(用英语或者换个标签吧)"), miraicle.Face.from_face_id(176)])
                bot.send_group_msg(group=msg.group, msg=[miraicle.Plain("什么？你非要冲？？？"), miraicle.Face.from_face_id(
                    104), miraicle.Plain("那满足你吧"), miraicle.Face.from_face_id(101)])
            except:
                bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain(
                    "这个标签没找到色色的图片欸~(用英语或者换个标签吧)"), miraicle.Face.from_face_id(176)])
                bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain("什么？你非要冲？？？"), miraicle.Face.from_face_id(
                    104), miraicle.Plain("那满足你吧"), miraicle.Face.from_face_id(101)])
            content = {'r18': r18[msg.group], 'tag': []}
            res = requests.post(
                url="https://api.lolicon.app/setu/v2", json=content).json()
            data = f"标题：{res['data'][0]['title']}\nUID: {res['data'][0]['uid']}\n作者: {res['data'][0]['author']}\ntags: {res['data'][0]['tags']}\n"
            try:
                bot.send_group_msg(group=msg.group, msg=[miraicle.Plain(
                    data), miraicle.Image.from_url(res['data'][0]['urls']['original'])], quote=msg.id)
            except:
                bot.send_friend_msg(qq=msg.sender, msg=[miraicle.Plain(
                    data), miraicle.Image.from_url(res['data'][0]['urls']['original'])], quote=msg.id)

        else:
            data = f"标题：{res['data'][0]['title']}\nUID: {res['data'][0]['uid']}\n作者: {res['data'][0]['author']}\ntags: {res['data'][0]['tags']}\n"
            bot.send_group_msg(group=msg.group, msg=[miraicle.Plain(
                data), miraicle.Image.from_url(res['data'][0]['urls']['original'])], quote=msg.id)


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
