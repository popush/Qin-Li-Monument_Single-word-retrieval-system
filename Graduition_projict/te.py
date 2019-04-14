from Graduition_projict import golbal as gv
t_list = []

def search(info):

    temp_result = gv.get_laber_key(gv.ch, info)
    print(temp_result)
    if temp_result[0] != 'false':
        # print(temp_result)
        for i in gv.final_label.keys():
            temp = gv.final_label[i]
            # print(temp)
            if int(temp_result) == temp[0]:
                print(i)
                t_list.append(i)
        print(t_list)

    else:
        print('error')


search("湘")