import json
import torch
import numpy as np
import os

class TrainDataLoader(object):
    '''
    data loader for training
    '''
    def __init__(self, topic, know_feature_n, exer_feature_n):
        self.batch_size = 1 # 不可改
        self.ptr = 0
        self.data = []
        self.topic = topic
        self.know_feature_n = know_feature_n
        self.exer_feature_n = exer_feature_n

        data_file = os.getcwd() + '/Server/logistics/topic' + str(topic) + '/data/log.txt'
        with open(data_file) as f:
            self.data = f.readlines()
        with open(os.getcwd() + '/Server/logistics/topic' + str(topic) + '/config.txt') as i_f:
            i_f.readline()
            self.student_n, self.exer_n, self.knowledge_n = list(map(eval, i_f.readline().split(',')))
        # 计算每个学对于在不同题目、知识的统计数据
        self.stu_feature_m = self.stu_feature()
        # 标准化训练数据
        self.know_feature_m, self.exer_feature_m, self.diff, self.ys = self.cal_know_and_exer_feature()

        # print (self.know_feature_m)
        # print (len(self.know_feature_m))

    def next_batch(self):
        if self.is_end():
            return None, None, None, None
        know_feature, exer_feature, diff, ys = [], [], [], []
        for count in range(self.batch_size):
            know_feature = self.know_feature_m[self.ptr + count]
            exer_feature = self.exer_feature_m[self.ptr + count]
            diff = self.diff[self.ptr + count]
            ys.append(self.ys[self.ptr + count])
        self.ptr += self.batch_size
        return torch.Tensor(know_feature), torch.Tensor(exer_feature), torch.Tensor(diff), torch.LongTensor(ys)

    def is_end(self):
        if self.ptr + self.batch_size > len(self.data):
            return True
        else:
            return False

    def reset(self):
        self.ptr = 0

    def cal_know_and_exer_feature(self):
        know_features = []
        exer_features = []
        diff = []
        ys = []
        for log in self.data:
            k_fea_list = []
            e_diff_list = []
            log = log.rstrip('\n')
            user_id, exercise_id, exercise_diff, know_code, attempts, start_time, end_time, score = log.split(',')
            user_id = int(user_id.strip())
            exercise_id = int(exercise_id.strip())
            exercise_diff = float(exercise_diff.strip())
            know_code = know_code.strip().split(' ')
            attempts = int(attempts.strip())
            start_time = int(start_time.strip())
            end_time = int(end_time.strip())
            score = int(score.strip())
            '''
                feature与题目无关：
                当前知识通过率(通过次数、失败次数)
                当前知识关联题目平均用时
                当前知识关联题目最多用时
                当前知识关联题目最少用时
                当前知识关联题目平均尝试次数
                当前知识关联题目最多尝试次数
                当前知识关联题目最少尝试次数
            '''
            for k in know_code:
                k = int(k)
                k_fea = []
                # knowledge feature
                # if self.stu_feature_m[user_id-1][(k-1)*8+0] + self.stu_feature_m[user_id-1][(k-1)*8+1] > 0:
                #     k_fea.append(self.stu_feature_m[user_id-1][(k-1)*8+0] / (self.stu_feature_m[user_id-1][(k-1)*8+0] + self.stu_feature_m[user_id-1][(k-1)*8+1]))
                # else:
                #     k_fea.append(0)
                k_fea.append(self.stu_feature_m[user_id - 1][(k - 1) * 8 + 0] / (
                                self.stu_feature_m[user_id - 1][(k - 1) * 8 + 0] + self.stu_feature_m[user_id - 1][
                            (k - 1) * 8 + 1]))

                # 用时 300*1000毫秒
                k_fea.append(self.stu_feature_m[user_id - 1][(k - 1) * 8 + 2] / 300 / 1000)
                k_fea.append(self.stu_feature_m[user_id - 1][(k - 1) * 8 + 3] / 300 / 1000)
                k_fea.append(self.stu_feature_m[user_id - 1][(k - 1) * 8 + 4] / 300 / 1000)

                # k_fea.append(self.stu_feature_m[user_id-1][(k-1)*8+2] / np.max(self.stu_feature_m[:, (k-1)*8+2]))
                # k_fea.append(self.stu_feature_m[user_id-1][(k-1)*8+3] / np.max(self.stu_feature_m[:, (k-1)*8+3]))
                # k_fea.append(self.stu_feature_m[user_id-1][(k-1)*8+4] / np.max(self.stu_feature_m[:, (k-1)*8+4]))
                # 尝试次数 10次
                k_fea.append(self.stu_feature_m[user_id - 1][(k - 1) * 8 + 5] / 10)
                k_fea.append(self.stu_feature_m[user_id - 1][(k - 1) * 8 + 6] / 10)
                k_fea.append(self.stu_feature_m[user_id - 1][(k - 1) * 8 + 7] / 10)
                # k_fea.append(self.stu_feature_m[user_id-1][(k-1)*8+5] / np.max(self.stu_feature_m[:, (k-1)*8+5]))
                # k_fea.append(self.stu_feature_m[user_id-1][(k-1)*8+6] / np.max(self.stu_feature_m[:, (k-1)*8+6]))
                # k_fea.append(self.stu_feature_m[user_id-1][(k-1)*8+7] / np.max(self.stu_feature_m[:, (k-1)*8+7]))
                # exercise feature
                # e_fea.append(end_time-start_time)
                # e_fea.append(attempts)
                # e_fea.append(exercise_diff)
                k_fea_list.append(k_fea)
                e_diff_list.append(exercise_diff)
            know_features.append(k_fea_list)
            exer_features.append([end_time-start_time, attempts, exercise_diff])
            diff.append(e_diff_list)
            ys.append(score)

        return know_features, exer_features, diff, ys

    def stu_feature(self):
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
        stu_feature = np.zeros((self.student_n, 2+8*self.knowledge_n))
        for log in self.data:
            # user_id, exercise_id, exercise_diff, know_code, attempts, start_time, end_time, score
            log = log.rstrip('\n')
            user_id, exercise_id, exercise_diff, know_code, attempts, start_time, end_time, score = log.split(',')
            user_id = int(user_id.strip())
            exercise_id = int(exercise_id.strip())
            exercise_diff = float(exercise_diff.strip())
            know_code = know_code.strip().split(' ')
            attempts = int(attempts.strip())
            start_time = int(start_time.strip())
            end_time = int(end_time.strip())
            score = int(score.strip())
            for k in know_code:
                k = int(k)
                # 通过次数
                stu_feature[user_id-1][(k-1)*8+0] += score
                # 失败次数
                if score == 0:
                    stu_feature[user_id-1][(k-1)*8+1] += 1
                time_using = end_time - start_time
                # 知识次数
                know_count = stu_feature[user_id - 1][(k - 1) * 8 + 0] + stu_feature[user_id-1][(k-1)*8+1]
                # 平均用时
                stu_feature[user_id-1][(k-1)*8+2] = (stu_feature[user_id-1][(k-1)*8+2]*(know_count-1)+time_using) / know_count
                # 最多用时
                if time_using > stu_feature[user_id-1][(k-1)*8+3]:
                    stu_feature[user_id-1][(k-1)*8+3] = time_using
                # 最少用时
                if stu_feature[user_id-1][(k-1)*8+4] == 0:
                    stu_feature[user_id - 1][(k - 1) * 8 + 4] = time_using
                elif time_using < stu_feature[user_id-1][(k-1)*8+4]:
                    stu_feature[user_id-1][(k-1)*8+4] = time_using
                # 平均尝试次数
                stu_feature[user_id-1][(k-1)*8+5] = (stu_feature[user_id-1][(k-1)*8+5]*(know_count-1)+attempts) / know_count
                # 最多尝试次数
                if attempts > stu_feature[user_id-1][(k-1)*8+6]:
                    stu_feature[user_id-1][(k-1)*8+6] = attempts
                # 最少尝试次数
                if stu_feature[user_id-1][(k-1)*8+7] == 0:
                    stu_feature[user_id - 1][(k - 1) * 8 + 7] = attempts
                elif attempts < stu_feature[user_id-1][(k-1)*8+7]:
                    stu_feature[user_id-1][(k-1)*8+7] = attempts
            stu_feature[user_id-1][-2] += 1
            stu_feature[user_id-1][-1] += score
        return stu_feature
