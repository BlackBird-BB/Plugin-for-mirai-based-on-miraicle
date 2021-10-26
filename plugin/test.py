import miraicle

@miraicle.Mirai.receiver("Message")
def test(bot: miraicle.Mirai, msg: miraicle.Message):
    if "test" in msg.plain:
        if msg.type == 'FriendMessage':
            bot.send_friend_msg(qq=602198790, msg=miraicle.Plain(r"好友消息"+str(msg.json)))
        elif msg.type == 'GroupMessage':
            bot.send_friend_msg(qq=602198790, msg=miraicle.Plain(r"群消息"+str(msg.json)))
