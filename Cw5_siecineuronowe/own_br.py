import numpy as np
import matplotlib.pyplot as plt

hidden_layer_neurons=0
ITERATIONS=150
wsp=0.05

b=np.random.rand(2).tolist()

p = [2,8] #Mikolaj Roszczyk: 318482, Iga Bernat: 318468

L_BOUND = -5
U_BOUND = 5

def J(x):
    return float(np.sin(x*np.sqrt(p[0]+1))+np.cos(x*np.sqrt(p[1]+1)))

def sigmoid(x):
    return float(1/(1+np.exp(-x)))

def d_sigmoid(x):
    s = float(1/(1+np.exp(-x)))
    return s * (1-s)

def nloss(y_out, y):
    return (y_out - y) ** 2

def d_nloss(y_out, y):
    return 2*( y_out - y)

x = np.linspace(L_BOUND, U_BOUND, 100).tolist()
y=[]
for i in range(len(x)):
    y.append(J(x[i]))

class Neuron:
    def __init__(self, inputs, wages):
        self.wages_vector=wages
        self.inputs_vector=inputs

    def adder(self):
        sum=0
        for i in range(len(self.inputs_vector)):
            sum=sum+self.inputs_vector[i]*self.wages_vector[i]
        sum=sum+self.wages_vector[len(self.inputs_vector)]
        return sum
    
    def output(self):
        return sigmoid(self.adder())
    


class NeuralNetwork:
    def __init__(self, inputs, hidden_layer_size):
        self.inputs=inputs
        self.hidden_layer=[]
        self.hidden_layer_outputs=[]
        self.hidden_layer_size=hidden_layer_size
        for i in range(hidden_layer_size):
            wages=np.random.rand(len(self.inputs)).tolist()
            wages.append(b[0])
            self.hidden_layer.append(Neuron(self.inputs, wages))
            self.hidden_layer_outputs.append(self.hidden_layer[i].output())
        self.output_layer=[]
        self.outputs_vector=[]
        for i in range(len(inputs)):
            wages=np.random.rand(hidden_layer_size).tolist()
            wages.append(b[1])
            self.output_layer.append(Neuron(self.hidden_layer_outputs, wages))
            self.outputs_vector.append(self.output_layer[i].adder())

    def feedforward(self, wages_hidden, wages_output):
        self.hidden_layer=[]
        self.hidden_layer_outputs=[]
        for i in range(self.hidden_layer_size):
            self.hidden_layer.append(Neuron(self.inputs, wages_hidden[i]))
            self.hidden_layer_outputs.append(self.hidden_layer[i].output())
        self.output_layer=[]
        self.outputs_vector=[]
        for i in range(len(self.inputs)):
            self.output_layer.append(Neuron(self.hidden_layer_outputs, wages_output[i]))
            self.outputs_vector.append(self.output_layer[i].adder())

    def backpropagation(self, wsp):
        #UPDATE OUTPUT LAYER WAGES:
        update_wages_output=[]
        for i in range(len(self.output_layer)):
            update_wages_neuron=[]
            dtotal_dout=d_nloss(self.outputs_vector[i], y[i])
            for j in range(len(self.hidden_layer)):
                update_wages_neuron.append(self.output_layer[i].wages_vector[j]-wsp*dtotal_dout*self.hidden_layer_outputs[j])
            update_wages_neuron.append(b[0])
            update_wages_output.append(update_wages_neuron)

        #UPDATE HIDDEN LAYER WAGES:
        update_wages_hidden=[]
        for i in range(len(self.hidden_layer)):
            update_wages_neuron=[]
            e_total_out=0
            for j in range(len(self.output_layer)):
                e_total_out=e_total_out+d_nloss(self.outputs_vector[j],y[j])*self.output_layer[j].wages_vector[i]
            for j in range(len(self.output_layer)):
                update_wages_neuron.append(self.hidden_layer[i].wages_vector[j]-wsp*e_total_out*d_sigmoid(self.hidden_layer_outputs[i])*self.inputs[j])
            update_wages_neuron.append(b[1])
            update_wages_hidden.append(update_wages_neuron)

        return update_wages_output, update_wages_hidden




def train(nn):
    for i in range(ITERATIONS):
        update_wages_output, update_wages_hidden = nn.backpropagation(wsp)
        nn.feedforward(update_wages_hidden, update_wages_output)
    return nn


nn=NeuralNetwork(x, hidden_layer_neurons) #inicjalizacja sieci neuronowej
nn=train(nn)

plt.plot(x,nn.outputs_vector, '-')
plt.plot(x,y, '-')
plt.grid()
plt.show()

loss_sum=0
loss_sum_d=0
for i in range(len(x)):
    loss_sum=loss_sum+nloss(nn.outputs_vector[i],y[i])
    loss_sum_d=loss_sum_d+d_nloss(nn.outputs_vector[i],y[i])
mean_1=loss_sum/len(x)
mean_d=loss_sum_d/len(x)
print("nloss mean:   ", mean_1)
print("d_nloss mean: ", mean_d)
    