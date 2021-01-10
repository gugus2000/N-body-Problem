import numpy as np
import matplotlib.pyplot as plt

C_FILE='SAVE.npy'

with open(C_FILE, 'rb') as file:
    print(np.load(file))
