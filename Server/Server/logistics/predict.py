import torch
import torch.nn as nn
import torch.optim as optim
from .model import Net
from .data_loader import TrainDataLoader
import numpy as np

def load_snapshot(model, filename):
    f = open(filename, 'rb')
    model.load_state_dict(torch.load(f, map_location=lambda s, loc: s))
    f.close()

def predict(stu_id, know_feature_n, exer_feature_n, model_n):
    data_loader = TrainDataLoader(know_feature_n, exer_feature_n)
    stu_feature = data_loader.stu_feature_m[stu_id - 1]
    '''
        知识通过次数
        知识失败次数
        知识平均用时
        知识最多用时
        知识最少用时
        知识平均尝试次数
        知识最多尝试次数
        知识最少尝试次数
        做题数
        总成绩
    '''
    know_feature = []
    for k in range(1, data_loader.knowledge_n + 1):
        k_fea = []
        # knowledge feature
        if stu_feature[(k - 1) * 8 + 0] + stu_feature[(k - 1) * 8 + 1] > 0:
            k_fea.append(stu_feature[(k - 1) * 8 + 0] / (stu_feature[(k - 1) * 8 + 0] + stu_feature[(k - 1) * 8 + 1]))
        else:
            k_fea.append(0)
        # k_fea.append(stu_feature[(k - 1) * 8 + 0] / (stu_feature[(k - 1) * 8 + 0] + stu_feature[(k - 1) * 8 + 1]))
        # 用时 300秒
        k_fea.append(stu_feature[(k - 1) * 8 + 2] / 300)
        k_fea.append(stu_feature[(k - 1) * 8 + 3] / 300)
        k_fea.append(stu_feature[(k - 1) * 8 + 4] / 300)
        # 尝试次数 10次
        k_fea.append(stu_feature[(k - 1) * 8 + 5] / 10)
        k_fea.append(stu_feature[(k - 1) * 8 + 6] / 10)
        k_fea.append(stu_feature[(k - 1) * 8 + 7] / 10)
        know_feature.append(k_fea)
    know_feature = torch.Tensor(know_feature)
    # print(know_feature.shape)
    know_mast = {}
    if model_n == 0:
        print ('no model')
        weight = min(np.log(model_n + 0.0001) / (np.e * np.e), 0.2)
        for k in range(1, data_loader.knowledge_n + 1):
            know_mast[k] = float(know_feature[k - 1][0])
    else:
        net = Net(know_feature_n, exer_feature_n)
        print('utilize model_' + str(model_n))
        load_snapshot(net, 'model/model_' + str(model_n))
        net.eval()
        # 将学生每个知识统计数据输入net.get_know函数
        mastery = net.get_know(know_feature)
        # print (mastery.shape)
        # mastery level
        weight = min(np.log(model_n + 0.0001) / (np.e * np.e), 0.2)
        for k in range(1, data_loader.knowledge_n + 1):
            know_mast[k] = weight * float(mastery[k - 1]) + (1 - weight) * float(know_feature[k - 1][0])
    print (know_mast)
    return know_mast
