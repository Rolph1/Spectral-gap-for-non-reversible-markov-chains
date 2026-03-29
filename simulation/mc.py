### HELPER FUNCTIONS ### 
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

def take_step(x, y, p, N):
    generated_prob = np.random.random()

    if generated_prob > p:
        return x , (y+1)%N # prob. 1-p 
    else:
        return (x+1)%N, y # prob p
    
def compute_observed_tau(delta):
    big_tau = -10

    for k in range(len(delta)):
        delta_k = delta[k]
        const = (k+1)*(delta_k**2)*1/4
        if big_tau < const:
            big_tau = const 
    return big_tau

# try all combinations lol
def find_opt_int(N, p):
    L = int(np.floor(N**(1/3)))
    minimum = 10000
    min_m1, min_m2 = -1000, -1000
    for m_1 in range(0, N, 1):
        for m_2 in range(0, N, 1):
            if m_1 == 0 and m_2 == 0:
                continue
            diophan = ( 1 - p * np.cos(2*np.pi * m_1 / N) - (1-p) * np.cos(2*np.pi * m_2/N))**2 + (p * np.sin(2*np.pi * m_1 / N) + (1-p) * np.sin(2*np.pi * m_2/N))**2
            if diophan < minimum:
                minimum = diophan
                min_m1 = m_1
                min_m2 = m_2
    return min_m1, min_m2

def compute_delta_paper(N, p, m_1, m_2, number_deltas, iteration_count):
    print(p)
    all_deltas = np.zeros((number_deltas, iteration_count))

    for j in range(number_deltas):
        # we want X_0 to be sampled from the stationary distribution, so we randomly draw initial x and y
        # this is how to simulate the stationary distribution!!!
        curr_x = np.random.randint(0, N)
        curr_y = np.random.randint(0, N)
        val_sin = 0
        val_cos = 0

        for i in range(iteration_count):
            # take a step, then compute f
            curr_x, curr_y = take_step(curr_x, curr_y, p, N)
            val_sin += np.sin(2*np.pi*(m_1*curr_x + m_2*curr_y)/N)
            val_cos += np.cos(2*np.pi*(m_1*curr_x + m_2*curr_y)/N)
            # compute empirical average of f after drawing i samples
            f_sum = val_sin**2 + val_cos**2 
            all_deltas[j, i] = f_sum/(i+1)**2

    delta_n = np.sqrt(np.mean(all_deltas, axis=0))
    return delta_n

### helper methods
# to go from and back to matrix indices based on a loop that goes through each element of the nodes once
def decode_index(idx, N):
    return idx % N, idx//N

def encode_index(x, y, N):
    return x + N*y

# construct the sparse matrices
def transition_positions(N, p):
    right_positions = []
    up_positions = []
    # going through every single node, and for each one adding the probability it goes right or up
    for node in range(N**2):
        x_1, y_1 = decode_index(node, N)
        x_2 = (x_1 + 1) % N
        y_2 = (y_1 + 1) % N

        right_node = encode_index(x_2, y_1, N)
        up_node = encode_index(x_1, y_2, N)

        right_positions.append((node, right_node))
        up_positions.append((node, up_node))

    # creating right, up, and identity sparse matrices to not kill my ram
    # data vector
    right_data = np.array([p]*len(right_positions))
    up_data = np.array([1-p]*len(up_positions))
    # data = np.concatenate((right_ps, up_ps), axis=None) 

    # separated the matrices into 3 to make debugging easier
    right_rows = np.array([k[0] for k in right_positions])
    right_cols = np.array([k[1] for k in right_positions])

    up_rows = np.array([k[0] for k in up_positions])
    up_cols = np.array([k[1] for k in up_positions])
    csr_right = csr_matrix((right_data, (right_rows, right_cols)), shape=(N**2,N**2))
    csr_up = csr_matrix((up_data, (up_rows, up_cols)), shape=(N**2,N**2))

    return csr_right, csr_up

# returns a matrix's second smallest singular value
def generator_sv(generator_matrix):
    u, s_min, vt = svds(generator_matrix, k=2, which="SM")
    abs_max = np.max(np.abs(s_min))
    return abs_max

# use helper functions above to do everything at once
def compute_tau(N, p):
    csr_right, csr_up = transition_positions(N, p)
    ones = np.ones(N**2)
    csr_identity = csr_matrix((ones, (range(N**2), range(N**2))))

    generator_matrix = csr_identity - (csr_right + csr_up)

    return 1/generator_sv(generator_matrix)