import miraicle


my_qq = 602198790           # 你的 QQ 号


@miraicle.Mirai.filter('GroupSwitchFilter')
def group_switch(bot: miraicle.Mirai, msg: miraicle.GroupMessage, flt: miraicle.GroupSwitchFilter):
    if msg.sender == my_qq:
        if msg.plain == '启用所有组件':
            flt.enable_all(group=msg.group)
            bot.send_group_msg(group=msg.group, msg='已在群内启用所有组件', quote=msg.id)
        elif msg.plain == '禁用所有组件':
            flt.disable_all(group=msg.group)
            bot.send_group_msg(group=msg.group, msg='已在群内禁用所有组件', quote=msg.id)
        elif msg.plain[:6]=='unload':
            func = msg.plain[7:]
            flt.disable(msg.group, func)
            bot.send_group_msg(group=msg.group, msg=f"已在该群内禁用{func}", quote=msg.id)
        elif msg.plain[:4]=='load':
            func = msg.plain[5:]
            flt.enable(msg.group, func)
            bot.send_group_msg(group=msg.group, msg=f"已在该群内启用{func}", quote=msg.id)
        elif msg.plain == 'func_list':
            fun = flt.funcs_info(msg.group)
            data = ""
            for i in fun:
                data = data + f"{i['func']}: {i['enabled']}\n"
            bot.send_group_msg(group=msg.group, msg=data, quote=msg.id)
