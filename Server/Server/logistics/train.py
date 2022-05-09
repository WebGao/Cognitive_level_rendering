import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from sklearn.metrics import roc_auc_score
from .data_loader import TrainDataLoader
from .model import Net

def train(topic, know_feature_n, exer_feature_n, model_n):
    log = ''
    data_loader = TrainDataLoader(topic, know_feature_n, exer_feature_n)
    # 初始化模型
    net = Net(know_feature_n, exer_feature_n)
    log += (str(net) + ' <br>')
    optimizer = optim.Adam(net.parameters(), lr=0.002)
    log += 'training model... <br>'

    loss_function = nn.NLLLoss()
    likelihood_value_old = 0
    epoch = 0
    while True:
        epoch += 1
        data_loader.reset()
        running_loss = 0.0
        batch_count = 0
        likelihood_value = 0
        while not data_loader.is_end():
            batch_count += 1
            know_feature, exer_feature, diff, labels = data_loader.next_batch()
            optimizer.zero_grad()
            output_1 = net.forward(know_feature, exer_feature, diff)
            output_0 = torch.ones(output_1.size()) - output_1
            output = torch.cat((output_0, output_1), 1)

            # grad_penalty = 0
            loss = loss_function(torch.log(output), labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if batch_count % 20 == 19:
                log += ('[epoch: %d batch: %d] loss: %.3f <br>' % (epoch, batch_count + 1, running_loss / 20))
                running_loss = 0.0
            likelihood_value += loss.item()
        likelihood_value /= batch_count
        if abs(likelihood_value - likelihood_value_old) <= 0.001:
            log += "training is ok <br>"
            break
        else:
            likelihood_value_old = likelihood_value
    # validate and save current model every epoch
    save_snapshot(net, os.getcwd() + '/Server/logistics/topic' + str(topic) + '/model/model_' + str(model_n + 1))
    log += ("model is saved as model_" + str(model_n + 1) + ' <br>')
    # print (log)
    return log


def save_snapshot(model, filename):
    f = open(filename, 'wb')
    torch.save(model.state_dict(), f)
    f.close()

