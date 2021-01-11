# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from classes import *

# CONDITIONS INITIALES
Sun=Body('Sun', CartesianCoordinate(0-C_X0, 0, 0), CartesianCoordinate(0, 0, 0), CartesianCoordinate(0, 0, 0), 2e30, 696e6, C_SMALL_STEP)
Mercury=Body('Mercury', CartesianCoordinate(28e9-C_X0, 0, 0), CartesianCoordinate(0, 47e3, 0), CartesianCoordinate(0, 0, 0),3.3e23,2.5e6,C_SMALL_STEP)
Venus=Body('Venus', CartesianCoordinate(108e9-C_X0, 0, 0), CartesianCoordinate(0, 35e3, 0), CartesianCoordinate(0, 0, 0), 4.8e24,6e6,10*C_SMALL_STEP)
Earth=Body('Earth', CartesianCoordinate(150e9-C_X0, 0, 0), CartesianCoordinate(0, 29.8e3, 0), CartesianCoordinate(0, 0, 0), 6e24, 6.4e6, 24*C_SMALL_STEP)
Mars=Body('Mars', CartesianCoordinate(227e9-C_X0, 0, 0), CartesianCoordinate(0, 24e3, 0), CartesianCoordinate(0, 0, 0), 5.4e23,3.4e6,30*C_SMALL_STEP)
Jupiter=Body('Jupiter', CartesianCoordinate(778e9-C_X0, 0, 0), CartesianCoordinate(0, 13e3, 0), CartesianCoordinate(0, 0, 0), 1.9e27,70e6,50*C_SMALL_STEP)
Saturn=Body('Saturn', CartesianCoordinate(1.4e12-C_X0, 0, 0), CartesianCoordinate(0, 9.6e3, 0), CartesianCoordinate(0, 0, 0), 568e24,60e6,80*C_SMALL_STEP)
Uranus=Body('Uranus', CartesianCoordinate(2.9e12-C_X0, 0, 0), CartesianCoordinate(0, 6.8e3, 0), CartesianCoordinate(0, 0, 0), 8.7e25,25.6e6,140*C_SMALL_STEP)
Neptune=Body('Neptune', CartesianCoordinate(4.5e12-C_X0, 0, 0), CartesianCoordinate(0, 5.4e3, 0), CartesianCoordinate(0, 0, 0), 102e23,4.8e6,180*C_SMALL_STEP)

bodies=[Neptune, Uranus, Saturn, Jupiter, Mars, Earth, Venus, Mercury, Sun]

now=dt.datetime.now()

# CONSTANTS
C_FILE='SAVE_'+str(now.year)+'_'+str(now.month)+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)+'.npy'

# CALCULS
for temps in range(0, int(C_PERIOD*365.25*C_SMALL_STEP*24), C_SMALL_STEP):
    optimized_storage=OptiStorage(bodies)
    for index_body in range(len(bodies)):
        if temps%bodies[index_body].step==0: # On regarde si on doit calculer la position de cette planète (pas adaptatif)
            force=optimized_storage.Optimize(bodies[index_body], bodies)
            bodies[index_body].applyForce(force, temps)

end_now=dt.datetime.now()

# SAUVEGARDE
with open(C_FILE, 'wb') as save:
    np.save(save, np.array(bodies), allow_pickle=True)

# AFFICHAGE
print('le calcul a pris '+str(end_now-now))

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
for body in bodies:
    plt.plot([body.trajectory[date][0] for date in range(len(body.trajectory))], [body.trajectory[date][1] for date in range(len(body.trajectory))])
plt.show()
