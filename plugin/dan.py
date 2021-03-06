import miraicle
import requests
import datetime
import json

from .nudgefunc import get_yiyan, get_dmoe

group_list = [679371905]
friend_list = [602198790, 2446770095, 2363157552]

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

@miraicle.scheduled_job(miraicle.Scheduler.every().day.at('7:30'))
def morning(bot: miraicle.Mirai):
    now = datetime.datetime.now()
    time = now.strftime("%Y年%m月%d日")
    
    dmoe = get_dmoe()
    yiyan = get_yiyan()
    
    data = "早安，"+time+"\n\n"+yiyan
    reply = [miraicle.Plain(data),
             miraicle.Image.from_url(dmoe)]

    for i in group_list: 
        bot.send_group_msg(group=i, msg=reply)
    for i in friend_list:
        bot.send_friend_msg(qq=i, msg=reply)


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

