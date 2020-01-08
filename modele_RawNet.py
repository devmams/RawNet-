import torch.nn as nn
import torch.nn.functional as F
import importlib
import torch
import torch.optim as optim
from modele_Data import RawNetData
import numpy as np

class RawNet(nn.Module):
    def __init__(self):
        super(RawNet, self).__init__()

        self.lrelu = nn.LeakyReLU()
        self.lrelu_keras = nn.LeakyReLU(negative_slope=0.3)

        self.first_conv = nn.Conv1d(in_channels = 1,#1
			out_channels = 128,#128
			kernel_size = 3,#3
                        padding = 0,
                        stride = 3
        )

        self.bn = nn.BatchNorm1d(num_features = 128)

    def forward(self, x):
        out = self.first_conv(x)
        out = self.bn(out)
        out = self.lrelu_keras(out)


        print("shape : ",out.shape)

        return out

def train(model, train_loader, optimizer, device):
    criterion = nn.CrossEntropyLoss()
    for batch_idx, (data,target) in enumerate(train_loader):

        print("-- type data : ",data.shape)
        print("-- type target : ",target.shape)
        print("-- data :", data)
        print("-- target : ",target)

        data = data.to(device)
        target = target.to(device)

        output = model(data)
        print("output : ", output)
        print("output shape : ", output.shape)
        optimizer.zero_grad()
        loss = criterion(output.squeeze(),target.long())
        print("loss :", loss)
        
        loss.backward()
        optimizer.step()



if __name__ == '__main__':

    DIRECTORY = "/info/home/larcher/ATAL/2019/voxceleb1/dev/wav"
    print(DIRECTORY)
    print("-----")
    dataset = RawNetData(DIRECTORY)
    print("test data dataset : ", type(dataset.__getitem__(0)[0]))
    print("test target dataset : ", type(dataset.__getitem__(0)[1]))

    data_loader = torch.utils.data.DataLoader(dataset,batch_size=120,shuffle=True,
                                               drop_last=True, num_workers=12)
    print(data_loader)
    print("-----")
    model = RawNet()
    print(model)
    
    cuda = torch.cuda.is_available()
    device = torch.device('cuda' if cuda else 'cpu')

    learning_rate = 0.001
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate,
                                 weight_decay=0.0001)
    print("-----ff")
    train(model,data_loader,optimizer,device)
