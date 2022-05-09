# Cognitive_level_rendering

### 安装Django和[PyTorch](https://pytorch.org/get-started/locally/)
```
pip install django
pip install torch torchvision torchaudio
```

### 运行项目
```
cd Cognitive_level_rendering
cd Server
python manage.py runserver [port，默认是8080]
```

### 访问
此时命令行显示服务端地址（如：http://127.0.0.1:8000/ ），请求和参数使用如下：

- 存储学生做题记录（record）
```
请求：logistics/<int:topic>/record
例子：http://127.0.0.1:8000/logistics/1/record

// 返回数据：存储日志（字符串）
```

- 训练模型（train）
```
请求：logistics/<int:topic>/train
例子：http://127.0.0.1:8000/logistics/1/train
```
返回数据：训练日志（字符串） ，成功请求后返回训练日志：
```
Net( (know_linear): Linear(in_features=7, out_features=1, bias=True) (disc_linear): Linear(in_features=3, out_features=1, bias=True) ) 
training model... 
[epoch: 1 batch: 20] loss: 0.575 
[epoch: 1 batch: 40] loss: 0.469 
[epoch: 2 batch: 20] loss: 0.572 
[epoch: 2 batch: 40] loss: 0.466 
[epoch: 3 batch: 20] loss: 0.570 
[epoch: 3 batch: 40] loss: 0.464 
[epoch: 4 batch: 20] loss: 0.569 
[epoch: 4 batch: 40] loss: 0.462 
[epoch: 5 batch: 20] loss: 0.568 
[epoch: 5 batch: 40] loss: 0.460 
[epoch: 6 batch: 20] loss: 0.567 
[epoch: 6 batch: 40] loss: 0.459 
[epoch: 7 batch: 20] loss: 0.566 
[epoch: 7 batch: 40] loss: 0.458 
[epoch: 8 batch: 20] loss: 0.565 
[epoch: 8 batch: 40] loss: 0.457 
training is ok 
model is saved as model_3 
```

- 渲染学情（predict）

请指定stu_id，如：/predict?stu_id=2，当前stu_id为整型（student、knowledge、exercise id为正整数），若是用户名字符串，服务器端需要维系用户名字符串和排序映射。
```
请求：logistics/<int:topic>/predict
参数：stu_id
例子：http://127.0.0.1:8000/logistics/predict?stu_id=2
```

返回数据：学生知识掌握水平（对象） ，成功请求后将获取如下学情数据：
```
{
    "status": "utilize model_3",  // 当没训练模型时，"status": "no model"
    "cognitive level": {
        "1": 0.6643327294507112,
        "2": 0.6810259137487279,
        "3": 0.5373374949281567,"
        4": 0.5373374949281567,
        "5": 0.6235578979375332,
        "6": 0.6810259137487279,
        "7": 0.9682176991458987,
        "8": 0.3935884032614904,
        "9": 0.10591300964572893,
        "10": 0.9682176991458987
    },
    "stu_id": 2
}
```
若未指定stu_id，则返回字符串提示：
```
请指定stu_id，如：/predict?stu_id=2
```

- 推荐题目（recommend）
```
请求：logistics/<int:topic>/recommend
参数：stu_id
可选参数：exer_id、response
推荐策略：
  - 策略1：
  - 策略2：
  - 策略3：
  - 策略4：
```
根据参数提供不同使用方法：

参数：stu_id（暂时不支持，应当根据当前topic为学生提供专项练习）
```
例子：http://127.0.0.1:8000/logistics/1/recommend?stu_id=2
```

参数：stu_id、exer_id，为题目exer_id（不考虑做题是否正确）提供策略1、2、3、4推荐
```
例子：http://127.0.0.1:8000/logistics/1/recommend?stu_id=2&exer_id=3
```

参数：stu_id、exer_id、response=0，根据题目exer_id练习成绩（做错）提供策略1、2推荐
```
例子：http://127.0.0.1:8000/logistics/1/recommend?stu_id=2&exer_id=3&response=0
```

参数：stu_id、exer_id、response=1，根据题目exer_id练习成绩（做对）提供策略3、4推荐
```
例子：http://127.0.0.1:8000/logistics/1/recommend?stu_id=2&exer_id=3&response=1
```

### 说明
- 路径：考虑到服务器环境和本地环境差异，若是遇到路径错误，可以使用```os.getcwd()```获取当前文件（```manage.py```）路径，基于此到达目标文件路径，如：```os.getcwd() + '/Server/logistics/model'```。

- 后端按需可以添加：删除模型、指定模型等服务。

- 前端需要考虑请求后如何确认请求成功。

- exer_know.json文件处理。

- exercise.json用于推荐（未提供）。

- 可以考虑增量计算，同时把data_loader处理的数据保存，之后使用可以直接使用，省去计算时间。
