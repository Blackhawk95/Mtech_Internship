import pandas as pd
import numpy as np
import pickle


def sigmoid(x):
    return 1/(1+ np.exp(-x))

def dsigmoid(y):
    return y*(1.0-y)

class MLP_NN(object):

    #no of inputs, hidden layer and output
    def __init__(self,input,hidden,output):
        self.input = input
        self.hidden = hidden
        self.output = output

        #array for all
        self.ai = [1.0]*self.input
        self.ah = [1.0]*self.hidden
        self.ao = [1.0]*self.output

        #create random weights
        self.wi = np.random.randn(self.input, self.hidden)
        self.wo = np.random.randn(self.hidden,self.output)
        
        #for changes
        self.ci = np.zeros((self.input,self.hidden))
        self.co = np.zeros((self.hidden,self.output))

    def FF(self,inputs):
        if(len(inputs) != self.input):
            raise ValueError(" bad input")

        #input activation
        for i in range(self.input -1 ): 
            self.ai[i] = inputs[i]

        #hidden activations
        for j in range(self.hidden):
            sum = 0.0
            for i in range(self.input):
                sum += self.ai[i]*self.wi[i][j]
            self.ah[j] = sigmoid(sum)
   
        #output activations
        for k in range(self.output):
            sum = 0.0
            for j in range(self.hidden):
                sum += self.ah[j]*self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]    
    
    def backProp(self,targets, lr):
        if len(targets) != self.output:
            raise ValueError('Wrong number of targets')
    
        #calculate output error and delta
        output_deltas = [0.0] * self.output
        for k in range(self.output):
            error = -(targets[k] - self.ao[k])
            output_deltas[k] = dsigmoid(self.ao[k])*error

        #calculate error for hidden layer and delta
        hidden_deltas = [0.0] * self.hidden
        for j in range(self.hidden):
            error = 0.0
            #print(output_deltas)
            #print(self.wo)
            for k in range(self.output):
                error+=output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        #update the weights connecting hidden to out
        for j in range(self.hidden):
            for k in range(self.output):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] -= lr * change + self.co[j][k]
                self.co[j][k] = change
        
        #update the weights connecting input to hidden
        for i in range(self.input):
            for j in range(self.hidden):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] -= lr * change + self.ci[i][j]
                self.ci[i][j] = change

        #calculate MSE error
        error = 0.0
        for k in range(len(targets)):
            error += 0.5 * (targets[k] - self.ao[k]) ** 2

        return error    

    def train(self,X,Y, iterations = 3000, lr = 0.0002):
        for i in range(iterations):
            error = 0.0
            for j in range(len(X)):
                inputs = X[j]
                targets = Y[j]
                self.FF(inputs)
                error = self.backProp(targets,lr)
                if j % 1000 == 0:
                    print ('error ', error,)

    def predict(self,X):
        predictions = []
        for p in X:
            predictions.append(self.FF(p))
        return predictions

    def print_weight(self,weight_name_in,weight_name_out,header_name_in,header_name_out):
        fi = open(header_name_in,"w+")
        xi = "float " + str(weight_name_in)+ "={ "
        for i in self.wi:
            xi = xi + "{"
            for j in i:
                xi = xi + str(j) + ","
            xi = xi[:-1]
            xi = xi + "}, "
        xi = xi[:-2]
        xi = xi + " };"
        fi.write(xi)
        fi.close()
        #for outheader - to create {{.,...,.},...,{.,...,.}}
        fo = open(header_name_out,"w+")
        xo = "float " + str(weight_name_out)+ "={ "
        for i in self.wo:
            xo = xo + "{"
            for j in i:
                xo = xo + str(j) + ","
            xo = xo[:-1]
            xo = xo + "}, "
        xo = xo[:-2]
        xo = xo + " };"
        fo.write(xo)
        fo.close()

#for micro
file = 'dataset/microdataset.csv'

#read the data`
df = pd.read_csv(file)
#to swap

headers = list(df.columns.values)
#print(headers)
#normalising
for dfi in headers[:-1]:
    df[dfi] = pd.to_numeric(df[dfi], errors='coerce')
    #df[dfi] = (df[dfi] - df[dfi].min())/(df[dfi].max()-df[dfi].min())    

#to mix
df = df.sample(frac=1).reset_index(drop=True)
#df=(df-df.min())/(df.max()-df.min())    
df_train = df.sample(frac = 0.7).reset_index(drop = True)
df_test = df.drop(df_train.index).reset_index(drop = True)

Y_train = []

for feature in (df_train.values)[:,-1]:
    if( feature == "benignware"):
        Y_train.append([1,0])
    elif( feature == "malware"):
        Y_train.append([0,1])

X_train = (df_train.values)[:,0:-1]
X_test = (df_test.values)[:,0:-1]
Y_test = (df_test.values)[:,-1]


NN = MLP_NN(21,31,2)# 21 51 2 : #167 input, 200 hidden and 2 output

#print(len(X_train[1]))

NN.train(X_train,Y_train,iterations = 1000,lr = 0.0001)

Y_cap = NN.predict(X_test)

for a in range(len(Y_cap)):
    for b in range(len(Y_cap[0])):
        Y_cap[a][b] = round(Y_cap[a][b])

print(Y_cap)

correct = 0
wrong = 0
for a in range(len(Y_cap)):
    if(Y_cap[a] == [1,0]):
        print("benignware",Y_test[a])
        if(Y_test[a] == "benignware"):
            correct = correct+1
        else:
            wrong = wrong+1 
    elif(Y_cap[a] == [0,1]):
        print("malware",Y_test[a])
        if(Y_test[a] == "malware"):
            correct = correct+1
        else:
            wrong = wrong+1 

print("Accuracy = " + str(correct/(correct+wrong)) + " out of " + str(correct + wrong) + "test data")    

NN.print_weight("wi[21][11]","wo[11][2]","less_uwin.h","less_uwout.h")

#print(Y_cap)

#print(df_test)



