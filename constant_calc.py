c_masses=[2e30, 3.3e23, 4.8e24, 6e24  , 5.4e23, 1.9e27, 568e24, 8.7e25, 102e23]
y_speeds=[0   , 47e3  , 35e3  , 29.8e3, 24e3  , 13e3  , 9.6e3 , 6.8e3 , 5.4e3 ]
x_positi=[0   , 28e9  , 108e9 , 150e9 , 227e9 , 778e9 , 1.4e12, 2.9e12, 4.5e12]

position_masses=0
speed_masses=0
masses=0
for i in range(len(c_masses)):
    position_masses+=c_masses[i]*x_positi[i]
    speed_masses+=c_masses[i]*y_speeds[i]
    masses+=c_masses[i]

print('Décalage du barycentre en x: '+str(position_masses/masses))
print('Translation du barycentre en y: '+str(speed_masses/masses))
