import numpy as np 
import matplotlib as plt 

# constants 
p = np.sqrt(0.5)
N = 5
iteration_count = 100 
x, y = 0, 0

def iterate_chain(x, y):
    generated_prob = np.random.random()

    if generated_prob > p:
        return (x+1) % N, y 
    else:
        return x, (y+1) % N 

for i in range(iteration_count):
    x, y = iterate_chain(x, y)
    print(f"({x}, {y})")

