import numpy as np 
import matplotlib.pyplot as plt

# constants
# length of each dimension of the Taurus 
N = 16
# transition probability 
p = np.sqrt(1/2)
iteration_count = 400

# stationary distribution 
stat_dist = np.array([1/(N**2)]*(N**2))
initial_dist = np.array([2/N**2]*int(N**2/2))
initial_dist = np.append(initial_dist, np.zeros(int(N**2/2)))

# spectral gap upper bound (only valid if p=0.5)
upper_bounds = [np.sqrt(N)/2 * np.exp(-(np.pi**2) * n / (2 * N**2)) for n in range(iteration_count)]

# helper functions:
# input: index
# output: index modulo N (x), index // N (y)
def decode_index(idx):
    return idx % N, idx//N

def encode_index(x, y):
    return x + N*y

# transition matrix construction
transition_matrix = np.zeros((N**2, N**2))
for node in range(N**2):
    x_1, y_1 = decode_index(node)
    x_2 = (x_1 + 1) % N
    y_2 = (y_1 + 1) % N

    right_node = encode_index(x_2, y_1)
    up_node = encode_index(x_1, y_2)

    transition_matrix[node][right_node] = p
    transition_matrix[node][up_node] = 1-p

# plotting tools
x = np.array(range(iteration_count))

# simulate chain 
def simulate_chain(dist, P, iterations):
    y = np.array([])
    for i in range(iterations):
        dist = P.dot(dist)
        #print(dist)
        y = np.append(y, d_TV(dist, stat_dist))
    print(dist)
    return dist, y

# check total variation distance
def d_TV(curr, stat_dist):
    return 0.5 * np.sum(np.abs(curr - stat_dist))

final_dist, y = simulate_chain(initial_dist, transition_matrix, iteration_count)

plt.plot(x, y, c="r", label="Total variation distance")
#plt.plot(x, upper_bounds, label="Upper bound")
plt.legend()
plt.savefig("graphs\in")
plt.show()