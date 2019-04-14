import os
import codecs

end_flag = False

rootdir = 'C:\\atest'  # 处理内容的放置位置


output_dir = 'C:\\atest'  # 输出内容的放置位置

img_cut = {}

forecast_label = {}

id1 = 0
id2 = 0

ch = {}

final_label = {}

recongnize_flag = False
def init_final_label():
    path = os.path.join(rootdir,'final_label.txt')
    if os.path.exists(path):
        fc = codecs.open(path, 'r', 'utf-8')
        for line in fc.readlines():
            linestr = line.strip()
            linestrlist = linestr.split(" ")
            temp = []
            if len(linestrlist) == 2:
                temp.append(int(linestrlist[1]))
                final_label[linestrlist[0]] = temp
            if len(linestrlist) == 3:
                temp.append(int(linestrlist[1]))
                temp.append(int(linestrlist[2]))
                final_label[linestrlist[0]] = temp
        fc.close()
        # print(forecast_label)
        flag = True
    else:
        fc = open(path,'w')
        fc.close()
        flag = False
    return flag

def final_append(img_path,res_list):
    final_label[img_path] = res_list
    path = os.path.join(rootdir,'final_label.txt')
    fc = codecs.open(path, 'a', 'utf-8')
    fc.write(img_path + " ")
    if len(res_list) == 1:
        fc.write(str(res_list[0]) + '\r\n')
    if len(res_list) == 2:
        fc.write(str(res_list[0]) + ' ' + str(res_list[1]) + '\r\n')
    fc.close()

def laber_help():
    fc = codecs.open('C:\graduation_project\LABER_HELP.txt', 'r', 'utf-8')
    # content.split(' ')
    for line in fc.readlines():
        linestr = line.strip()
        linestrlist = linestr.split(" ")
        ch[linestrlist[0]] = linestrlist[1]
    # print(ch['2'])

def get_laber_key(dict, value):
    if value in ch.values():
        return [k for k, v in dict.items() if v == value]
    else:
        return ['false']

def init_forecast_label():
    path = os.path.join(rootdir, 'forecast_label.txt')
    if os.path.exists(path):
        # 读取文件所有行
        fc = codecs.open(path, 'r', 'utf-8')
        for line in fc.readlines():
            linestr = line.strip()
            linestrlist = linestr.split(" ")
            temp = []
            if len(linestrlist) == 2:
                temp.append(int(linestrlist[1]))
                forecast_label[linestrlist[0]] = temp
            if len(linestrlist) == 3:
                temp.append(int(linestrlist[1]))
                temp.append(int(linestrlist[2]))
                forecast_label[linestrlist[0]] = temp
        fc.close()
        # print(forecast_label)
        flag = True
    else:
        fc = open(path,'w')
        fc.close()
        flag = False
    return flag

def forecast_append(img_path, res_list):
    forecast_label[img_path] = res_list
    path = os.path.join(rootdir, 'forecast_label.txt')
    fc = codecs.open(path, 'a', 'utf-8')
    fc.write(img_path + " ")
    if len(res_list) == 1:
        fc.write(str(res_list[0])+'\r\n')
    if len(res_list) == 2:
        fc.write(str(res_list[0])+' '+str(res_list[1])+'\r\n')
    fc.close()

def re_write_final_label():
    if len(final_label) == 0:
        return False
    else:
        path = os.path.join(rootdir, 'final_label.txt')
        if os.path.exists(path):
            fc = codecs.open(path, 'w', 'utf-8')
            for x in final_label:
                fc.write(x)
                fc.write(' ')
                if len(final_label[x]) == 1:
                    fc.write(str(final_label[x][0])+'\r\n')
                if len(final_label[x]) == 2:
                    fc.write(str(final_label[x][0])+' '+str(final_label[x][1]) + '\r\n')
            return True
        else:
            return False

def re_write_forecast_label():
    if len(forecast_label) == 0:
        return False
    else:
        path = os.path.join(rootdir, 'forecast_label.txt')
        if os.path.exists(path):
            fc = codecs.open(path, 'w', 'utf-8')
            for x in forecast_label:
                print(x)
                fc.write(x)
                fc.write(' ')
                if len(forecast_label[x]) == 1:
                    fc.write(str(forecast_label[x][0])+'\r\n')
                if len(forecast_label[x]) == 2:
                    fc.write(str(forecast_label[x][0])+' '+str(forecast_label[x][1]) + '\r\n')

            return True
        else:
            return False

# forecast_append('dsad',[8,9])
# init_forecast_label()
# laber_help()
# m = get_laber_key(ch,'东')
# print(m)

# init_final_label()
# re_write_final_label()
# init_forecast_label()
# re_write_forecast_label()