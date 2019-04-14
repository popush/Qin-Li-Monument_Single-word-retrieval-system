import re

import codecs


fr = open(r'C:\graduation_project\颜勤礼碑单字版\颜真卿-勤礼碑.txt', 'r')
# 读取文件所有行
content = fr.readlines()
contentLines = ''
symbol = ['，','。','/','、','《','》','：','”','；','‘','【','】','{','}']
characers = []
stat = {}


for line in content:
    line = line.strip()
    if len(line) == 0:
        continue
    contentLines = contentLines + line
    punctuation = """！？｡，。/；’【】《》？：“.{}、，。/；‘【】?、《》？：”{}||＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
    re_punctuation = "[{}]+".format(punctuation)
    line = re.sub(re_punctuation, "", line)

    for x in range(0, len(line)):
        if not line[x] in characers:
            characers.append(line[x])

stat = sorted(stat.items(), key=lambda e: e[1], reverse=True)

f = codecs.open('chinese_labels.txt','w','utf-8')
for i in range(0,len(characers)):
    print(characers[i])
    f.write(characers[i]+"\n")
f.close()

print('全文共有%d个字' % len(contentLines))
print('一共有%d个不同的字' % len(characers))
fr.close()
