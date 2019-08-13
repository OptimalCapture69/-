def pyramid_calc(BALLS_SIDE=4):
    BALL_DIAMETER = 100
    xyz_list = []
    sqrt2 = 2**(0.5)
    for h in range(BALLS_SIDE):
        for i in range(BALLS_SIDE-h):
            for j in range(BALLS_SIDE-h):
               print