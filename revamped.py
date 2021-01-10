import numpy as np
import matplotlib.pyplot as plt
import celluloid as cel

class Body:
    """A body with enought mass to be considered in the system"""
    def __init__(self, name, position, speed, acceleration, mass, radius, step):
        self.name=name
        self.position=position
        self.speed=speed
        self.acceleration=acceleration
        self.mass=mass
        self.radius=radius
        self.trajectory=[self.position.saveAsPartTrajectory()]
        self.step=step

    def getForce(self, bodies):
        force=CartesianCoordinate(0, 0, 0)
        for body in bodies:
            if self.name!=body.name:
                coordinate=self.position-body.position
                coordinate=coordinate.ToSpherical()
                force+=SphericalCoordinate(-C_G*(body.mass*self.mass)/(coordinate.first**2), coordinate.second, coordinate.third)
        return force

    def applyForce(self, force):
        self.trajectory.append(self.position.saveAsPartTrajectory())
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

    def saveAsPartTrajectory(self):
        if self.system=='cartesian':
            return [self.first, self.second, self.third]
        else:
            return self.ToCartesian().saveAsPartTrajectory()

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

C_G=6.67e-11

Earth=Body('Earth', CartesianCoordinate(150e9, 0, 0), CartesianCoordinate(0, 29.8e3, 0), CartesianCoordinate(0, 0, 0), 6e24, 2.5e6)
Sun=Body('Sun', CartesianCoordinate(0, 0, 0), CartesianCoordinate(0, 0, 0), CartesianCoordinate(0, 0, 0), 2e30, 696e6)

bodies=[Earth, Sun]
temps=np.linspace(0, 2*365.25*3600*24, 1)

for index_temps in range(1, len(temps)):
    for index_body in range(len(bodies)):
        if temps[index_temps]%bodies[index_body].step==0: # On regarde si on doit calculer la position de cette planète (pas adaptatif)
            force=bodies[index_body].getForce(bodies)
            bodies[index_body].applyForce(force)

fig=plt.figure()
ax=fig.add_subplot(1,1,1)
camera=cel.Camera(fig)
for date in range(len(bodies[0].trajectory)):
    plt.scatter([body.trajectory[date][0] for body in bodies], [body.trajectory[date][1] for body in bodies])
    camera.snap()
anim=camera.animate(blit=True)
anim.save('test.mp4')

"""
for index_body in range(len(bodies)):
    plt.plot([position[0] for position in bodies[index_body].trajectory], [position[1] for position in bodies[index_body].trajectory])
plt.show()
"""
