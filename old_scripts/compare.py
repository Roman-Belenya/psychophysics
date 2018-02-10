from psychopy import monitors

mon1 = monitors.Monitor('labDELL')
mon1.setCurrent('calib')
mon2 = monitors.Monitor('labDELL2')
mon2.setCurrent('calib')

print mon1.__dict__['calibNames']
print mon2.__dict__['calibNames']

with open('1.txt', 'wb') as f:
    for key, value in mon1.currentCalib.items():
        f.write('{}: {}\n\n'.format(key, value))

with open('2.txt', 'wb') as f:
    for key, value in mon2.currentCalib.items():
        f.write('{}: {}\n\n'.format(key, value))
