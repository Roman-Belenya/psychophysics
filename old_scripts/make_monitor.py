from psychopy import monitors

# mon = monitors.Monitor('labLG')

# calib, = mon.__dict__['calibs'].keys()

# mon.__dict__['calibs'][calib]['distance'] = 70
# mon.__dict__['calibs'][calib]['sizePix'] = [1920.0, 1080.0]
# mon.__dict__['calibs'][calib]['width'] = 48.0

# mon.saveMon()


mon = monitors.Monitor('labBENQ')

calib, = mon.__dict__['calibs'].keys()

mon.__dict__['calibs'][calib]['distance'] = 70
mon.__dict__['calibs'][calib]['sizePix'] = [1920.0, 1080.0]
mon.__dict__['calibs'][calib]['width'] = 53.13

mon.saveMon()