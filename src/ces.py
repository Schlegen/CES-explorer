

class CES:
    ''' Implementation of a CES 
    '''

    def __init__(self, z0, x0, y0, rho):
        self.x0 = x0
        self.y0 = y0
        self.alpha_x = x0 / (x0 + y0)
        self.alpha_y = y0 / (x0 + y0)
        self.rho = rho
        self.elast = 1 / (1 - rho)


    def eval(self, x1, x2):
        return z0 * (self.alpha_1 * ((x1 / self.x0) ** self.rho)
                  + self.alpha_2 * ((x2 / self.x0) ** self.rho)
                    ) ** (1/self.rho)


