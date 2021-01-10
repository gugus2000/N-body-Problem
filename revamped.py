import numpy as np
import matplotlib.pyplot as plt

class Body:
    """A body with enought mass to be considered in the system"""
    def __init__(self, name, position, speed, acceleration, mass, radius, step):
        self.name=name
        self.position=position
        self.speed=speed
        self.acceleration=acceleration
        self.mass=mass
        self.radius=radius
        self.trajectory=[self.position.saveAsPartTrajectory(0)]
        self.step=step

    def getForce(self, bodies):
        force=CartesianCoordinate(0, 0, 0)
        for body in bodies:
            if self.name!=body.name:
                coordinate=self.position-body.position
                coordinate=coordinate.ToSpherical()
                force+=SphericalCoordinate(-C_G*(body.mass*self.mass)/(coordinate.first**2), coordinate.second, coordinate.third)
        return force

    def applyForce(self, force, t):
        self.trajectory.append(self.position.saveAsPartTrajectory(t))
        self.acceleration=force/self.mass # First Principle
        self.speed+=self.acceleration*self.step
        self.position+=self.speed*self.step

class Coordinate:
    """A 3D coordinate"""
    def __init__(self, system, first, second, third):
        self.system=system
        self.first=float(first)
        self.second=float(second)
        self.third=float(third)

    def saveAsPartTrajectory(self, t):
        if self.system=='cartesian':
            if t==0:
                return [self.first, self.second, self.third]
            else:
                return [self.first, self.second-C_V0*t, self.third]
        else:
            return self.ToCartesian().saveAsPartTrajectory(t)

    def __add__(self, coordinate):
        if self.system==coordinate.system and self.system=='cartesian':
            return CartesianCoordinate(self.first+coordinate.first, self.second+coordinate.second, self.third+coordinate.third)
        elif self.system=='cartesian':
            return self+coordinate.ToCartesian()
        elif coordinate.system=='cartesian':
            return self.ToCartesian()+coordinate
        else:
            return self.ToCartesian()+coordinate.ToCartesian()

    def __sub__(self, coordinate):
        if self.system==coordinate.system and self.system=='cartesian':
            return CartesianCoordinate(self.first-coordinate.first, self.second-coordinate.second, self.third-coordinate.third)
        elif self.system=='cartesian':
            return self-coordinate.ToCartesian()
        elif coordinate.system=='cartesian':
            return self.ToCartesian()-coordinate
        else:
            return self.ToCartesian()-coordinate.ToCartesian()

    def __mul__(self, number):
        if self.system=='cartesian':
            return CartesianCoordinate(self.first*number, self.second*number, self.third/number)
        else:
            return self.ToCartesian()*number

    def __truediv__(self, number):
        if self.system=='cartesian':
            return CartesianCoordinate(self.first/number, self.second/number, self.third/number)
        else:
            return self.ToCartesian()/number

    def __str__(self):
        return self.system+' ('+str(self.first)+', '+str(self.second)+', '+str(self.third)+')'


class SphericalCoordinate(Coordinate):
    """A 3D coordinate in a spherical system (r, theta, phi)"""
    def __init__(self, r, theta, phi):
        Coordinate.__init__(self, 'spherical', r, theta, phi)

    def ToCartesian(self):
        x=self.first*np.sin(self.second)*np.cos(self.third)
        y=self.first*np.sin(self.second)*np.sin(self.third)
        z=self.first*np.cos(self.second)
        return CartesianCoordinate(x, y, z)

class CartesianCoordinate(Coordinate):
    """A 3D coordinate in a cartesian system (x, y, z)"""
    def __init__(self, x, y, z):
        Coordinate.__init__(self, 'cartesian', x, y, z)

    def ToSpherical(self):
        r=np.sqrt(self.first**2+self.second**2+self.third**2)
        if r!=0:
            theta=np.arccos(self.third/r)
        else:
            theta=0
        if self.first!=0:
            phi=np.arctan2(self.second,self.first)
        else:
            phi=0
        return SphericalCoordinate(r, theta, phi)

# CONDITIONS INITIALES
Sun=Body('Sun', CartesianCoordinate(0-1.849e9, 0, 0), CartesianCoordinate(0, 0, 0), CartesianCoordinate(0, 0, 0), 2e30, 696e6, 3600)
Mercury=Body('Mercury', CartesianCoordinate(28e9-1.849e9, 0, 0), CartesianCoordinate(0, 47e3, 0), CartesianCoordinate(0, 0, 0),3.3e23,2.5e6,3600)
Venus=Body('Venus', CartesianCoordinate(108e9-1.849e9, 0, 0), CartesianCoordinate(0, 35e3, 0), CartesianCoordinate(0, 0, 0), 4.8e24,6e6,3600*10)
Earth=Body('Earth', CartesianCoordinate(150e9-1.849e9, 0, 0), CartesianCoordinate(0, 29.8e3, 0), CartesianCoordinate(0, 0, 0), 6e24, 6.4e6, 3600*24)
Mars=Body('Mars', CartesianCoordinate(227e9-1.849e9, 0, 0), CartesianCoordinate(0, 24e3, 0), CartesianCoordinate(0, 0, 0), 5.4e23,3.4e6,3600*30)
Jupiter=Body('Jupiter', CartesianCoordinate(778e9-1.849e9, 0, 0), CartesianCoordinate(0, 13e3, 0), CartesianCoordinate(0, 0, 0), 1.9e27,70e6,3600*50)
Saturn=Body('Saturn', CartesianCoordinate(1.4e12-1.849e9, 0, 0), CartesianCoordinate(0, 9.6e3, 0), CartesianCoordinate(0, 0, 0), 568e24,60e6,3600*80)
Uranus=Body('Uranus', CartesianCoordinate(2.9e12-1.849e9, 0, 0), CartesianCoordinate(0, 6.8e3, 0), CartesianCoordinate(0, 0, 0), 8.7e25,25.6e6,3600*140)
Neptune=Body('Neptune', CartesianCoordinate(4.5e12-1.849e9, 0, 0), CartesianCoordinate(0, 5.4e3, 0), CartesianCoordinate(0, 0, 0), 102e23,4.8e6,3600*30)

bodies=[Earth, Mercure, Sun]

masses=0
masses_vitesses=0
for body in bodies:
    if body.name!='Sun':
        masses+=body.mass
        masses_vitesses+=body.mass*body.speed.second
    else:
        masse_soleil=body.mass

# CONSTANTES
C_V0=masses_vitesses/(masses+masse_soleil)
C_G=6.67e-11
C_FILE="SAVE"

# CALCULS
for temps in range(0, int(165*365.25*3600*24), 3600):
    for index_body in range(len(bodies)):
        if temps%bodies[index_body].step==0: # On regarde si on doit calculer la position de cette planète (pas adaptatif)
            force=bodies[index_body].getForce(bodies)
            bodies[index_body].applyForce(force, temps)

# SAUVEGARDE
np.save(C_FILE, np.array(bodies), True)

# AFFICHAGE
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
for body in bodies:
    plt.plot([body.trajectory[date][0] for date in range(len(body.trajectory))], [body.trajectory[date][1] for date in range(len(body.trajectory))])
plt.show()
