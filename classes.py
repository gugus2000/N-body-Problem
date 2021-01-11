# IMPORTS
import numpy as np

# CONSTANTS
C_V0=15.567317523246935
C_X0=1284919574.6478384
C_G=6.67e-11
C_PERIOD=2
C_SMALL_STEP=3600

# CLASSES DEFINIION
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

    def getForce(self, body):
        coordinate=self.position-body.position
        coordinate=coordinate.ToSpherical()
        return SphericalCoordinate(-C_G*(body.mass*self.mass)/(coordinate.first**2), coordinate.second, coordinate.third)

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

class OptiStorage:
    """Optimize storage to speed up the algorithm"""
    def __init__(self, bodies):
        self.storage={}
        for body in bodies:
            self.storage[body.name]={}

    def Optimize(self, body, bodies):
        force=CartesianCoordinate(0,0,0)
        for other_body in bodies:
            if other_body.name!=body.name:
                if body.name not in self.storage[other_body.name]:
                    temp_force=body.getForce(other_body)
                    self.storage[body.name][other_body.name]=temp_force
                    force+=temp_force
                else:
                    force-=self.storage[other_body.name][body.name]
        return force

