import miraicle

@miraicle.Mirai.receiver('GroupMessage')
@miraicle.Mirai.receiver('FriendMessage')
def help(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.plain == 'help':
        con = '''你好~我是BB Master的有限状态姬。'''