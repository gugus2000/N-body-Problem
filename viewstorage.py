import numpy as np
import matplotlib.pyplot as plt
from classes import *

C_FILE='SAVE.npy'
C_FILE=input('Enter the name of the file you want to display')

with open(C_FILE, 'rb') as save:
    print(np.load(save))
