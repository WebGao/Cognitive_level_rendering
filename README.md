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
python manage.py runserver [port]
```

### 访问
此时命令行显示服务端地址（如：http://127.0.0.1:8000/ ），请求和参数使用如下：

- 存储学生做题记录（record）
```
http://127.0.0.1:8000/logistics/record

// 返回数据：存储日志（字符串）
```

- 训练模型（train）
```
http://127.0.0.1:8000/logistics/train

// 返回数据：训练日志（字符串）
```

- 渲染学情（predict）

请指定stu_id，如：/predict?stu_id=2，当前stu_id为整型（所有student、knowledge id都从1开始），若是用户名字符串，服务器端需要维系用户名字符串和排序映射。
```
http://127.0.0.1:8000/logistics/predict?stu_id=2

//返回数据：学生知识掌握水平（对象）
```

考虑到服务器环境和本地环境差异，若是遇到路径错误，可以使用```os.getcwd()```获取当前文件（```manage.py```）路径，基于此到达目标文件路径，如：```os.getcwd() + '/Server/logistics/model'```。

后端按需可以添加：删除模型、指定模型等服务。