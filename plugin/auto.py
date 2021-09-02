import miraicle
import requests
import json

r18 = 0    

@miraicle.Mirai.receiver('FriendMessage')
def hello_to_friend(bot: miraicle.Mirai, msg: miraicle.FriendMessage):
    bot.send_friend_msg(qq=msg.sender, msg='Hello world!')


@miraicle.Mirai.receiver('GroupMessage')
def hello_to_group(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    global r18
    if msg.text in ['Hello', 'hello']:
        bot.send_group_msg(group=msg.group, msg=[miraicle.Plain('Hello world!'),
                                                 miraicle.Face().from_face_id(74),
                                                 miraicle.At(qq=msg.sender)])
    elif msg.plain == '草':
        # 草，图片回复
        bot.send_group_msg(
            msg.group, [miraicle.Image.from_file('/home/blackbird/mcl/python_miraicle/data/cao.jpg')])
    elif msg.plain == '麻了':
        # 麻了，是全麻么？
        bot.send_group_msg(group=msg.group, msg='是全麻嘛？')
    elif msg.plain == '笑死':
        # 笑死，根本笑不死
        bot.send_group_msg(group=msg.group, msg='根本笑不死')
    elif msg.plain == '讲个笑话':
        # 讲笑话
        res = requests.post("https://api.vvhan.com/api/xh?type=json")
        res = json.loads(res.text)
        bot.send_group_msg(group=msg.group, msg=res['joke'])
    elif "2441825920" in msg.text:
        # 人工智障
        response = requests.get("http://api.qingyunke.com/api.php?key=free&appid=0&msg="+msg.plain)
        rel = json.loads(response.text)
        rel = rel['content']
        bot.send_group_msg(group = msg.group, msg = rel)