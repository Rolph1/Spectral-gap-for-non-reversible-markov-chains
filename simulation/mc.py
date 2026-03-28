### HELPER FUNCTIONS ### 
import numpy as np


def take_step(x, y, p, N):
    generated_prob = np.random.random()

    if generated_prob > p:
        return (x+1) % N, y 
    else:
        return x, (y+1) % N
    
def compute_tau(delta):
    big_tau = -10

    for k in range(len(delta)):
        delta_k = delta[k]
        const = k*(delta_k**2)*1/4
        if big_tau < const:
            big_tau = const 
    return big_tau