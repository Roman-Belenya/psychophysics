from psychopy import core
my_clock = core.Clock()
for frame in range(60):  # 0.5 secs on 120Hz
    my_clock.reset()
    stim.pos += 0.01
    stim.ori *= 0.01
    stim.draw()
    #win.flip()
    response = event.getKeys()
    print 'processing for this frame took', my_clock.getTime() * 1000, 'ms'