import miraicle
import io
import base64
import sqlite3
import jieba
import wordcloud
import matplotlib.pyplot as plt
from collections import defaultdict


@miraicle.Mirai.receiver('GroupMessage')
def word_cloud(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.plain == '本群词云':
        connect = sqlite3.connect(r'/home/blackbird/mcl/python_miraicle/data/word_cloud.db')
        cursor = connect.cursor()
        bot.send_group_msg(msg.group, '正在生成本群词云', quote=msg.id)
        execute_text = 'SELECT msg FROM msgs WHERE group_id = ?'
        content = (msg.group,)
        results = cursor.execute(execute_text, content).fetchall()
        results = [r[0] for r in results]

        counts = defaultdict(int)
        for result in results:
            words = jieba.cut(result, cut_all=True)
            for word in words:
                if word and not word.isspace():
                    counts[word] += 1

        cloud = wordcloud.WordCloud(background_color='white', repeat=True, font_path='simhei.ttf')
        cloud.generate_from_frequencies(counts)
        figure = plt.figure(figsize=(16, 9))
        plt.axis('off')
        plt.imshow(cloud, interpolation='bilinear')
        
        with io.BytesIO() as buffer:
            figure.canvas.print_png(buffer)
            binary_data = buffer.getvalue()
            base64_data = base64.b64encode(binary_data)
        bot.send_group_msg(msg.group, [miraicle.Image.from_base64(base64_data)], quote=msg.id)

    elif msg.plain:
        connect = sqlite3.connect(r'/home/blackbird/mcl/python_miraicle/data/word_cloud.db')
        cursor = connect.cursor()
        execute_text = 'INSERT INTO msgs(time, sender_id, group_id, msg) VALUES(?, ?, ?, ?)'
        content = (msg.time, msg.sender, msg.group, msg.plain)
        cursor.execute(execute_text, content)
        connect.commit()
