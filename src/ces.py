import numpy as np

class CES:
    ''' Implementation of a CES 
    '''

    def __init__(self, z0, x0, y0, rho):
        self.z0 = z0
        self.x0 = x0
        self.y0 = y0
        self.alpha_x = x0 / (x0 + y0)
        self.alpha_y = y0 / (x0 + y0)
        self.rho = rho
        self.elast = 1 / (1 - rho)

    def eval(self, x, y):
        return self.z0 * (
                    self.alpha_x * ((x / self.x0) ** self.rho)
                  + self.alpha_y * ((y / self.y0) ** self.rho)
                    ) ** (1/self.rho)

    def eval_rectangle(self, x, y):
        xn = np.tile(x, (y.size,1))
        yn = np.tile(y, (x.size,1)).T

        return self.z0 * (
                self.alpha_x * ((xn / self.x0) ** self.rho)
              + self.alpha_y * ((yn / self.y0) ** self.rho)
            ) ** (1/self.rho)

    def eval_derivative(self):
      ()