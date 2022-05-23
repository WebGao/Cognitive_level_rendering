from .exer_know import exer_know
import os
import json
from .data_loader import TrainDataLoader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend(topic, stu_id, exer_id, response):
    know_feature_n = 7
    exer_feature_n = 3
    # 题目和知识关联
    exer_know_dic = exer_know(topic)
    know_id = exer_know_dic[str(exer_id)]
    # 推荐题库
    with open(os.getcwd() + '/Server/logistics/topic' + str(topic) + '/data/exercise.json', encoding='utf8') as i_f:
        recom_exer = json.load(i_f)

    # 根据学情推荐，需要限制，学生未做过被推荐题目
    recom_exer_dic = {
        'stu_id': stu_id,
        'current_exer_id': exer_id,
        'current_know_id': know_id,
        'response': response,
    }
    if not response:
        # 若是当前题目做错，需要练习对应知识：
        # strategy 1：推荐当前题目关联知识的其他题目
        exer_list_stra1 = []
        for e in recom_exer:
            for k in e['know_id']:
                if k in know_id:
                    exer_list_stra1.append(e['exer_id'])
        recom_exer_dic['strategy_1'] = list(set(exer_list_stra1))
        # strategy 2：推荐当前题目关联知识的前驱知识对应题目（夯实基础），未提供知识关系
        recom_exer_dic['strategy_2'] = []
    elif response:
        # 若是当前题目做对，可以夯实基础：
        # strategy 3：推荐与stu_id做题记录相似的学生在当前知识上做错的题
        data_loader = TrainDataLoader(topic, know_feature_n, exer_feature_n)
        stu_log = data_loader.data
        stu_feature_m = data_loader.stu_feature_m
        # current_feature = np.array(list(stu_feature_m[stu_id - 1][0: -2]) * stu_feature_m.shape[0]).reshape(stu_feature_m.shape[0], -1)

        current_feature = np.array([stu_feature_m[stu_id - 1][0: -2]])
        sim = cosine_similarity(current_feature, stu_feature_m[:, 0: -2])[0]
        recom_exer_dic['strategy_3'] = []
        for s in range(len(sim)):
            if sim[s] >= 0.5 and not (stu_id == s+1):
                # 建议后续可以增量更新
                for stu_l in stu_log:
                    stu_l = stu_l.replace('\n', '').replace(' ', '').split(',')
                    if int(stu_l[0]) == s+1 and int(stu_l[-1]) == 0 and int(stu_l[1]) not in recom_exer_dic['strategy_3']:
                        recom_exer_dic['strategy_3'].append(int(stu_l[1]))
        # strategy 4：推荐与stu_id做题记录相似的学生在当前题目关联知识的前驱知识对应易错题目（夯实基础），未提供知识关系
        recom_exer_dic['strategy_4'] = []
    return recom_exer_dic