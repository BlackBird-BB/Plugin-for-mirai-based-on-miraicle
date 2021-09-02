import miraicle

@miraicle.Mirai.receiver("GroupMessage")
def test(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if "test" in msg.plain:
        print(msg.plain)