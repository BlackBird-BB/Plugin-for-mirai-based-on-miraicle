import miraicle
import requests
import json

def search_song(name, stype=1, offset=0, total='true', limit=60):
    # 搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
    url = 'http://music.163.com/api/search/get/web'
    data = {
            's': name,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': 60}
    rel = requests.post(url, data)
    rel = json.loads(rel.text)
    if len(rel['result'])==0:
        return -1
    else:
        return rel['result']['songs'][0]['id']


@miraicle.Mirai.receiver('GroupMessage')
@miraicle.Mirai.receiver("FriendMessage")
def group_switch(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.text[:3] == "点歌 ":
        music_name = msg.text[3:]
        music_id = search_song(music_name)
        if music_id == -1:
            bot.send_group_msg(group=msg.group, msg=[miraicle.Plain("没有找到这首歌呀"),miraicle.Face.from_face_id(176)])
        else:
            card = {'type': 'MusicShare', 
                    'kind': 'NeteaseCloudMusic', 
                    'title': music_name, 
                    'summary': f"[点歌] {msg.sender_name}", 
                    'jumpUrl': f"http://music.163.com/song/{music_id}", 
                    'pictureUrl': f"http://q1.qlogo.cn/g?b=qq&nk={msg.sender}&s=640", 
                    'musicUrl': f"http://music.163.com/song/media/outer/url?id={music_id}.mp3", 
                    'brief': f"[点歌] {music_name}"}
        callback = [card]
        try:
            bot.send_group_msg(group=msg.group, msg=callback)
        except:
            bot.send_friend_msg(qq=msg.sender, msg=callback)
