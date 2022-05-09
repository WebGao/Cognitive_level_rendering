import pandas as pd
import os
import re
import json

def exer_know(topic):
    data_file = os.getcwd() + '/Server/logistics/topic' + str(topic)
    if os.path.exists(data_file + '/data/exer_know.json'):
        print ('使用题目和知识关联文件exer_know.json')
        with open(data_file + '/data/exer_know.json', encoding='utf8') as i_f:
            exer_know_dic = json.load(i_f)
    else:
        print('初始化题目和知识关联文件exer_know.json')
        filepath = data_file + '/exercise/'
        exer_know_file = os.listdir(filepath)[0]
        topic_exer = pd.read_csv(filepath + exer_know_file)
        know = topic_exer['问题对应知识点']
        exer_know_dic = {}
        exer = 0
        for i in range(len(know)):
            if 'nan' not in str(know[i]):
                exer += 1
                exer_know_dic[exer] = re.findall(r"\d+\.?\d*", str(know[i]))
        with open(data_file + '/data/exer_know.json', 'w', encoding='utf8') as output_file:
            json.dump(exer_know_dic, output_file, indent=4, ensure_ascii=False)
    return exer_know_dic


# topic_exer = pd.read_csv('topic1/exercise/主题1知道点相关问题.csv')
# print (topic_exer['问题'])
# print (topic_exer['问题对应知识点'])
#
# exer = topic_exer['问题']
# know = topic_exer['问题对应知识点']
# exer_list = []
# know_list = []
# for i in range(len(know)):
#     if 'nan' not in str(know[i]):
#         know_list.append(str(know[i]))
#
# import re
# for i in range(len(know_list)):
#     print (know_list[i], re.findall(r"\d+\.?\d*", know_list[i]))



