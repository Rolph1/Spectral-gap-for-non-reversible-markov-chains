import numpy as np 
import matplotlib.pyplot as plt

# constants
# length of each dimension of the Taurus 
N = 200
# transition probability 
p = np.sqrt(1/2)
iteration_count = 100

# stationary distribution 
stat_dist = np.array([1/(N**2)]*(N**2))
initial_dist = np.array([4/N**2]*int(N**2/4))
initial_dist = np.append(initial_dist, np.zeros(int(3 * N**2/4)))

#random_array = np.random.rand(N**2)
# normalize so it's a distribution
#initial_dist = random_array / np.linalg.norm(random_array)
print(np.linalg.norm(initial_dist))
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
    dist_sum = dist
    # matrix where each row corresponds to the empirical mean vector  
    dist_emp_avg = np.empty([iteration_count, N**2])
    dist_emp_avg[0] = np.array([dist_sum])

    # running the chain
    for i in range(iterations):
        dist = P.dot(dist)
        dist_sum += dist 
        dist_emp_avg[i] = np.array([dist_sum/(i+1)])
        y = np.append(y, d_TV(dist, stat_dist))
        print(dist)
    return dist, y, dist_emp_avg

# check total variation distance
def d_TV(curr, stat_dist):
    return 0.5 * np.sum(np.abs(curr - stat_dist))

final_dist, y, dist_emp_avg = simulate_chain(initial_dist, transition_matrix, iteration_count)
empirical_variance = np.array([])

for distribution in dist_emp_avg:
    empirical_variance = np.append(empirical_variance, np.var(distribution))

#plt.plot(x, y, c="r", label="Total variation distance")
plt.plot(x, empirical_variance, c="r", label="Δ_n")
#plt.plot(x, upper_bounds, label="Upper bound")
plt.legend()
plt.savefig("graphs\in")
plt.show()