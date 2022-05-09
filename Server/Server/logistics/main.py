from .train import train
from .predict import predict
from .recommend import recommend
import os
from django.http import HttpResponse, JsonResponse

with open(os.getcwd() + '/Server/logistics/config.txt') as i_f:
    i_f.readline()
    student_n, exer_n, knowledge_n = list(map(eval, i_f.readline().split(',')))

def config_model_n():
    filepath = os.getcwd() + '/Server/logistics/model'
    # print(filepath)
    files = os.listdir(filepath)
    # for fi in files:
    #     fi_d = os.path.join(filepath, fi)
    #     print (fi_d)
    return len(files)

def train_server(request):
    know_feature_n = 7
    exer_feature_n = 3
    log = train(know_feature_n, exer_feature_n, config_model_n())
    return HttpResponse(log)

def predict_server(request):
    know_feature_n = 7
    exer_feature_n = 3
    request.encoding = 'utf-8'
    if 'stu_id' in request.GET and request.GET['stu_id']:
        stu_id = int(request.GET['stu_id'])
        http_response = predict(stu_id, know_feature_n, exer_feature_n, config_model_n())
        http_response['stu_id'] = stu_id
        return JsonResponse(http_response)
    else:
        return HttpResponse('请指定stu_id，如：/predict?stu_id=2')

def record_server(request):
    print (123)

def recommend_server(request):
    if 'stu_id' in request.GET and request.GET['stu_id']:
        stu_id = int(request.GET['stu_id'])
        if 'exer_id' in request.GET and request.GET['exer_id']:
            # 指定题目
            know_id = int(request.GET['exer_id'])
            recommend(stu_id, know_id)
        # else:
            # 未指定题目，按照知识推荐
            # for k in range(knowledge_n):
            #     recommend(stu_id, k+1)
    else:
        return HttpResponse('请指定stu_id，如：/recommend?stu_id=2')

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
