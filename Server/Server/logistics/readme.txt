log.txt：user_id, exercise_id, exercise_diff, know_code, attempts, start_time, end_time（提交时间）, score

每次达到batch数据或者做完某个主题题目（发送signal），更新一次模型（每次都运行epoch轮,重新训练，因为归一化范围不同），同时把数据存进log.txt，把模型存到本地。

每次初始化时，加载模型，若是没有模型就随机初始化模型参数。

模型给出的预测值权重随着训练次数n增加，最多只占0.2（即，min(log(n)/e^2, 0.2)）

每次预测时找最新的模型

训练和预测独立

需要维系题目和知识关联文件exer_know.json，运行pyhton exer_know.py
