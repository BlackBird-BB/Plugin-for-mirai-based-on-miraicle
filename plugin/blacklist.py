import miraicle

my_qq = 602198790           # 你的 QQ 号

@miraicle.Mirai.filter('BlacklistFilter')
def blacklist(bot: miraicle.Mirai, msg: miraicle.GroupMessage, flt: miraicle.BlacklistFilter):
    if msg.sender == my_qq:
        if msg.plain == '拉黑我':
            flt.append(msg.sender)
            bot.send_group_msg(group=msg.group, msg="满足你~")
        elif msg.plain == '我错了':
            flt.remove(msg.sender)
            bot.send_group_msg(group=msg.group, msg="哼~")
        elif msg.plain[:2] == '拉黑':
            try:
                id = int(msg.plain[2:])
                flt.append(id)
                bot.send_group_msg(group=msg.group, msg=f"已拉黑{id}", quote=msg.id)
            except:
                pass
            
        elif msg.plain[:2] == '放过':
            try:
                id = int(msg.plain[2:])
                flt.remove(id)
                bot.send_group_msg(group=msg.group, msg=f"已放出{id})", quote=msg.id)
            except:
                pass
        elif msg.plain == '大赦天下':
            flt.clear()
        elif msg.plain == '监狱名单':
            bot.send_group_msg(group=msg.group, msg=str(flt.show()), quote=msg.id)