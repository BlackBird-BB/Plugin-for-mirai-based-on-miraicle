import miraicle

@miraicle.Mirai.receiver('GroupMessage')
@miraicle.Mirai.receiver('FriendMessage')
def help(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if 'help' in msg.plain:
        con = '''你好~我是BB Master的有限状态姬。这里是我的食用方式：
    我可以讲笑话（“讲个笑话”）、对特定的话做出反应，还可以发色图（“色图 [tag]”）哦~
    如果你想看更加色色的那种，可以联系我的主人给你设置。
    如果你还想要我的早晚安也要联系我的主人呀，只有主人允许了我才可以给你发
    
    对了对了！！！如果你想联系主人，在你给我发送的消息前面加上“[Tell BB]”，我便会将后面的内容告诉我的主人~（标签仅当前一条消息有效哦'''
        bot.send_friend_msg(qq=msg.sender, msg=con)