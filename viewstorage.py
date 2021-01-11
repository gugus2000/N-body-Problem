import numpy as np
import matplotlib.pyplot as plt
from classes import *

C_FILE='SAVE.npy'
C_FILE=input('Enter the name of the file you want to display')

with open(C_FILE, 'rb') as save:
    bodies=np.load(save, allow_pickle=True)

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
for body in bodies:
    plt.plot([body.trajectory[date][0] for date in range(len(body.trajectory))], [body.trajectory[date][1] for date in range(len(body.trajectory))])
plt.show()
