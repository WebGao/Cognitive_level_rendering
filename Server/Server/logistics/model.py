import torch
import torch.nn as nn

class Net(nn.Module):
    '''
    Model
    '''
    def __init__(self, know_feature_n, exer_feature_n):
        self.know_feature_n = know_feature_n
        self.exer_feature_n = exer_feature_n

        super(Net, self).__init__()

        # network structure
        self.know_linear = nn.Linear(self.know_feature_n, 1)
        self.disc_linear = nn.Linear(self.exer_feature_n, 1)

        # initialization
        for name, param in self.named_parameters():
            if 'weight' in name:
                nn.init.xavier_normal_(param)

    def forward(self, know_feature, exer_feature, diff):
        '''
        :param feature: [k, f] Tensor, k knowledge concepts, f features
        :param diff: [k, 1], Tensor, difficulty
        :return: y_pred, the probabilities of answering correctly
        '''
        master_of_k = torch.sigmoid(self.know_linear(know_feature))
        discrimination = torch.sigmoid(self.disc_linear(exer_feature)).unsqueeze(1)
        diff = diff.unsqueeze(1)
        y_pred = torch.mean(1 / (1 + torch.exp(-1.7 * (master_of_k - diff) * discrimination)), 0)
        # print(y_pred)
        return y_pred.unsqueeze(1)

    def get_know(self, feature):
        '''
        :param feature: [1, f] Tensor
        :return: k_pred, the probabilities of mastering knowledge k
        '''
        k_pred = torch.sigmoid(self.know_linear(feature))
        return k_pred
