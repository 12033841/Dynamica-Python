from src.animals import nervous_system
import numpy as np
np.set_printoptions(precision=3, suppress=True)

x_list = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
y_list = [[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]]

# and, or, xor

input_size = 2
hidden_size = 5
output_size = 3
learning_rate = 0.2
num_epochs = 10000
weight_init = [0, 0.5]

net = nervous_system.NeuralNetwork(input_size, hidden_size, output_size, learning_rate, weight_init)

for i in range(num_epochs):
    epoch_cost = 0
    for j in range(len(x_list)):
        x = np.array(x_list[j], float)
        y = np.array(y_list[j], float)
        h, o = net.feedforward(x)
        o_cost = net.calc_cost(y, o)
        net.backpropogation(x, o, h, o_cost)
        epoch_cost += (o_cost**2).sum()
        if i % 100 == 0:
            print("Cost:", epoch_cost)

for i in range(len(x_list)):
    x = np.array(x_list[i], float)
    y = np.array(y_list[i], float)
    h, o = net.feedforward(x)
    o_cost = net.calc_cost(y, o)
    print("x:", x, " | y:", y, " | o:", '{}'.format(o), " | cost:", '{:0.3f}'.format((o_cost**2).sum()))


