import miraicle
from plugin import *

qq = 2441825920              # 你登录的机器人 QQ 号
verify_key = 'fuckit'     # 你在 setting.yml 中设置的 verifyKey
port = 8082                 # 你在 setting.yml 中设置的 port (http)

bot = miraicle.Mirai(qq=qq, verify_key=verify_key, port=port)
bot.set_filter(miraicle.GroupSwitchFilter(r'config\group_switch.json'))
bot.set_filter(miraicle.BlacklistFilter(r'config\blacklist.json'))
bot.run()

# QQ face_ID: https://docs-v1.zhamao.xin/face_list.html