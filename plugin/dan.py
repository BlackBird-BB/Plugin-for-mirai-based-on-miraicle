import miraicle
import requests
import datetime
import json

group_list = [975952062, 679371905]
friend_list = [602198790, 1320896465, 2446770095, 2363157552]

def jinrishici():
    token = "a9QBS+SLL6qZ0uabxPOHZinf3l2VOVDL"
    head = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        'X-User-Token': token}
    response = requests.get(url="https://v2.jinrishici.com/sentence", headers = head)
    rel = json.loads(response.text)
    con = ""
    for i in rel['data']['origin']['content']:
        con = con+i+"\n"
    data = f'''〖标题〗{rel['data']['origin']['title']}
〖作者〗（{rel['data']['origin']['dynasty'].replace("代", "")}）{rel['data']['origin']['author']}
〖诗词〗
{con}
'''
    if rel['data']['origin']['translate'] != None:
        tra = ""
        for i in rel['data']['origin']['translate']:
            tra = tra+i+"\n"
        data = data + "\n〖翻译〗\n"+tra
    return data


def meirigeyan():
    response = requests.get(url="http://open.iciba.com/disapi")
    rel = json.loads(response.text)
    data = f"●今日格言\n{rel['note']}\n{rel['content']}"
    return data, rel['fenxiang_img']



@miraicle.scheduled_job(miraicle.Scheduler.every().day.at('7:30'))
def morning(bot: miraicle.Mirai):
    now = datetime.datetime.now()
    time = now.strftime("%Y年%m月%d日")
    
    data, img = meirigeyan()
    data = "早安，"+time+"\n\n"+data
    rep = [miraicle.Plain(data),
            miraicle.Image.from_url(img)]

    for i in group_list: 
        bot.send_group_msg(group=i, msg=rep)
    for i in friend_list:
        bot.send_friend_msg(qq=i, msg=rep)


@miraicle.scheduled_job(miraicle.Scheduler.every().day.at('23:30'))
def night(bot: miraicle.Mirai):
    now = datetime.datetime.now()
    time = now.strftime("%Y年%m月%d日")
    
    data = jinrishici()
    data = "晚安，"+time+"\n\n"+data

    for i in group_list: 
        bot.send_group_msg(group=i, msg=data)
    for i in friend_list:
        bot.send_friend_msg(qq=i, msg=data)

# @miraicle.scheduled_job(miraicle.Scheduler.every(10).seconds)               # 每隔 10s 触发一次
# def test(bot: miraicle.Mirai):
#     bot.send_group_msg(group=975952062, msg="test")

