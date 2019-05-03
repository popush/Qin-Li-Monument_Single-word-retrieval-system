# Qin-Li-Monument_Single-word-retrieval-system
# 《勤礼碑》单字检索系统
## 本系统是本人的毕业设计，仅供学习交流和西安理工大学计算机学院老师的查阅

**使用前**    
1.下载繁体的楷体字体文件    


**使用步骤：**    
**在每一步操作前，务必将路径修改为自己的路径！！！**    
1.配置opencv，tensorlow 1.3    
2.运行make_chinese_label    
2.运行put_training_dataset    
3.运行put_org_chinese_labels     
**此时已经结束训练集和测试集的lable标签的生成**    
**接下来进行神经网络的训练**    
务必修改好文件路径，训练次数根据自己需要设置，自己有GPU可以修改AlexNet文件夹下面的文件。    
**训练好模型后，将模型所在文件夹地址写在sus_one_pic中**    

**不出意外，此使已经可以正常运行了。**     

