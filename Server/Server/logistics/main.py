from .train import train
from .predict import predict
from .recommend import recommend
import os
from django.http import HttpResponse, JsonResponse
import logging
import random

# logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.INFO)
# handler = logging.FileHandler(os.getcwd() + '/Server/logistics/log/log.txt')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
#
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
#
# logger.addHandler(handler)
# logger.addHandler(console)

def config_model_n(topic):
    filepath = os.getcwd() + '/Server/logistics/topic' + str(topic) + '/model'
    # print(filepath)
    files = os.listdir(filepath)
    # for fi in files:
    #     fi_d = os.path.join(filepath, fi)
    #     print (fi_d)
    return len(files)

def train_server(request, topic):
    # logger.info("Post: start print log")
    know_feature_n = 7
    exer_feature_n = 3
    log = train(topic, know_feature_n, exer_feature_n, config_model_n(topic))
    return HttpResponse(log)

def predict_server(request, topic):
    know_feature_n = 7
    exer_feature_n = 3
    request.encoding = 'utf-8'
    if 'stu_id' in request.GET and request.GET['stu_id']:
        stu_id = int(request.GET['stu_id'])
        http_response = predict(topic, stu_id, know_feature_n, exer_feature_n, config_model_n(topic))
        http_response['stu_id'] = stu_id
        return JsonResponse(http_response)
    else:
        return HttpResponse('请指定stu_id，如：/predict?stu_id=2')

def record_server(request, topic):
    # log=3_10_0.6_1-5_3_213124_213330_0
    # 可以考虑加密和解密
    request.encoding = 'utf-8'
    if 'stu_log' in request.GET and request.GET['stu_log']:
        stu_log = request.GET['stu_log']
    stu_log = stu_log.replace('_', ', ').replace('-', ' ')
    stu_log += '\n'
    # 建议备份log，最起码要查重
    with open(os.getcwd() + '/Server/logistics/topic' + str(topic) + '/data/log.txt', 'a') as f:
        f.write(stu_log)
    return HttpResponse(stu_log)

def recommend_server(request, topic):
    if 'stu_id' in request.GET and request.GET['stu_id']:
        stu_id = int(request.GET['stu_id'])
        if 'exer_id' in request.GET and request.GET['exer_id']:
            know_id = int(request.GET['exer_id'])
            if 'response' in request.GET and request.GET['response']:
                # 指定题目
                # 若是当前题目做错：
                #（1）需要练习当前知识关联其他题目
                #（2）推荐当前题目关联知识的前驱知识对应题目（夯实基础），未提供知识关系
                # 若是当前题目做对，可以夯实基础：
                #（3）推荐与stu_id做题记录相似的学生在当前知识上做错的题
                #（4）推荐与stu_id做题记录相似的学生在当前题目关联知识的前驱知识对应易错题目（夯实基础），未提供知识关系
                response = int(request.GET['response'])
                recom_exer_dic = recommend(topic, stu_id, know_id, response)
            else:
                # （1）需要练习当前知识关联其他题目
                # （2）推荐当前题目关联知识的前驱知识对应题目（夯实基础），未提供知识关系
                # （3）推荐与stu_id做题记录相似的学生在当前知识上做错的题
                # （4）推荐与stu_id做题记录相似的学生在当前题目关联知识的前驱知识对应易错题目（夯实基础），未提供知识关系
                recom_exer_dic_correct = recommend(topic, stu_id, know_id, 1)
                recom_exer_dic = recommend(topic, stu_id, know_id, 0)
                recom_exer_dic['strategy_3'] = recom_exer_dic_correct['strategy_3']
                recom_exer_dic['strategy_4'] = recom_exer_dic_correct['strategy_4']
                print (recom_exer_dic)

        else:
            # 未指定题目，按照知识推荐
            # 学情
            know_feature_n = 7
            exer_feature_n = 3
            http_response = predict(topic, stu_id, know_feature_n, exer_feature_n, config_model_n(topic))['cognitive level']
            # print (http_response)
            # 知识覆盖度
            recom_exer_dic = {
                "stu_id": stu_id
            }
            with open(os.getcwd() + '/Server/logistics/topic' + str(topic) + '/config.txt') as i_f:
                i_f.readline()
                student_n, exer_n, knowledge_n = list(map(eval, i_f.readline().split(',')))
            for k in range(knowledge_n):
                if http_response[k + 1] >= 0.5:
                    response = 1
                else:
                    response = 0
                recom_exer_dic_know = recommend(topic, stu_id, k + 1, response)
                recom_exer_dic[str(k + 1)] = recom_exer_dic_know
        return JsonResponse(recom_exer_dic)
    else:
        return HttpResponse('请指定stu_id，如：/recommend?stu_id=2')

def stulog_server(request, topic):
    with open(os.getcwd() + '/Server/logistics/topic' + str(topic) + '/data/log.txt') as f:
        data = f.read()
    return HttpResponse(data.replace('\n', '<br>'))

if __name__ == '__main__':
    know_feature_n = 7
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
    exer_feature_n = 3
    '''
        feature与题目相关，计算区分度：
        当前题目用时
        当前题目尝试次数
        当前题目难度
    '''
    type = 'predict'
    if type == 'train':
        train(know_feature_n, exer_feature_n, config_model_n())
    if type == 'predict':
        stu_id = 2
        predict(stu_id, know_feature_n, exer_feature_n, config_model_n())
