import numpy as np

class CES:
    ''' Implementation of a CES 
    '''

    def __init__(self, alpha1, alpha2, rho):
      self.alpha1 = alpha1
      self.alpha2 = alpha2
      self.rho = rho
      self.elast = 1 / (1 - rho) if rho != 0 else None


    def eval(self, x, y):
      if self.rho != 0:
        return (
                self.alpha1 * (x ** self.rho)
              + self.alpha2 * (y ** self.rho)
                ) ** (1/self.rho)
      else:
        return 1

    def eval_rectangle(self, x, y):
        xn = np.tile(x, (y.size,1)).astype(np.float32)
        yn = np.tile(y, (x.size,1)).astype(np.float32).T
        res = self.eval(xn, yn)

        if self.rho != 0:
          return res
        else:
          return np.ones(xn.shape) 

    def eval_derivative(self):
      ()


class ControlProblem:
  def __init__(self, p1, p2, alpha1, alpha2):
    self.p1 = p1
    self.p2 = p2
    self.alpha1 = alpha1
    self.alpha2 = alpha2

    self.model = Problem.build_model()

  @classmethod
  def build_model(cls,p1, p2, alpha1, alpha2):
    return 0