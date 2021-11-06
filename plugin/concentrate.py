import miraicle
import pickle
from miraicle.message import GroupMessage
from miraicle.mirai import Mirai

def group_str(msg):
    return f'{msg._time} GroupMessage #{msg.id} {msg.group_name}({msg.group})' \
        f' - {msg.sender_name}({msg.sender}): {msg.plain}'

def friend_str(msg):
    return f'{msg._time} FriendMessage #{msg.id}' \
        f' - {msg.sender_name}({msg.sender}): {msg.plain}'

def storage(msg):
    try:
        with open("/home/git/bot/Plugin-for-mirai-based-on-miraicle/data/concentrate/today.pkl", 'rb') as f:
            msgsToday = pickle.load(f)
    except:
        msgsToday = []
    msgsToday.append(msg)
    with open("/home/git/bot/Plugin-for-mirai-based-on-miraicle/data/concentrate/today.pkl", 'wb') as f:
        pickle.dump(msgsToday, f)

@miraicle.Mirai.receiver('GroupMessage')
@miraicle.Mirai.receiver('FriendMessage')
@miraicle.Mirai.receiver('TempMessage')
def concentrate(bot: miraicle.Mirai, msg):
    print(msg.json)
    print(msg.plain)
    flag=0
    if '[AtAll]' in msg.text:
        flag=1
        print("[con strated]")
        con = f"Master~ {msg.sender_name}({msg.sender}) in {msg.group_name}({msg.group}) have sent a [AtAll] message at {msg.time}. Here's the content:\n\n{msg.plain}\n\nAnd I've saved it for you."

    elif '[At:2441825920]' in msg.text or '[At:602198790]' in msg.text:
        flag=1
        print("[con strated]")
        con = f"Master~ {msg.sender_name}({msg.sender}) in {msg.group_name}({msg.group}) have sent a [AtYou] message at {msg.time}. Here's the content.\n\n{msg.plain}\n\nAnd I've saved it for you."
    
    elif '[Tell BB]' in msg.plain:
        flag=1
        print("[con strated]")
        con = f"Master~ {msg.sender_name}({msg.sender}) sent you a message. Hereis the content\n\n{msg.plain}."
    if flag==1:
        storage(msg)
        bot.send_friend_msg(qq=602198790, msg=con)


@miraicle.scheduled_job(miraicle.Scheduler.every().day.at('22:00'))
def remind(bot: miraicle.Mirai):
    with open("/home/git/bot/Plugin-for-mirai-based-on-miraicle/data/concentrate/today.pkl", 'rb') as f:
        msgsToday = pickle.load(f)
    bot.send_friend_msg(qq=602198790, msg=[miraicle.Plain(
        "Master~ It's 22:00. Have you handled all messages about you? Here's a reminder~")])
    for i in msgsToday:
        if i.type == 'GroupMessage':
            con = group_str(i)
        elif i.type == 'FriendMessage' or i.type == 'TempMessage':
            con = friend_str(i)
        bot.send_friend_msg(qq=602198790, msg=con)
    msgsToday = []
    with open("/home/git/bot/Plugin-for-mirai-based-on-miraicle/data/concentrate/today.pkl", 'wb') as f:
        pickle.dump(msgsToday, f)

