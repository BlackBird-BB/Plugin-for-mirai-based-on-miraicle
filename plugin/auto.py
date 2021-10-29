import miraicle

# @miraicle.Mirai.receiver('FriendMessage')
# def hello_to_friend(bot: miraicle.Mirai, msg: miraicle.FriendMessage):
#     bot.send_friend_msg(qq=msg.sender, msg='Hello world!')


@miraicle.Mirai.receiver('GroupMessage')
@miraicle.Mirai.receiver('FriendMessage')
def hello_to_group(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    callback = None
    if msg.text in ['Hello', 'hello']:
        callback = [miraicle.Plain('Hello world!'),
                miraicle.Face().from_face_id(74),
                miraicle.At(qq=msg.sender)]
        
    elif msg.plain == '草':
        # 草，图片回复
        # callback = [miraicle.Image.from_file('/home/blackbird/mcl/python_miraicle/data/cao.jpg')]
        callback = [miraicle.Image.from_file(
            "/home/git/bot/Plugin-for-mirai-based-on-miraicle/data/cao.jpg")]
    elif msg.plain == '麻了':
        # 麻了，是全麻么？
        callback = '是全麻嘛？'
    elif msg.plain == '笑死':
        # 笑死，根本笑不死
        callback = '根本笑不死'
    
    if callback!=None:
        try:
                bot.send_group_msg(group=msg.group, msg=callback)
        except:
                bot.send_friend_msg(qq=msg.sender, msg=callback)
