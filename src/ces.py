import numpy as np

class CES:
    ''' Implementation of a CES 
    '''

    def __init__(self, alpha1, alpha2, rho):
      self.alpha1 = alpha1
      self.alpha2 = alpha2
      self.rho = rho
      self.elast = 1 / (1 - rho) if rho != 0 else None

    def eval(self, x1, x2):
      if self.rho != 0:
        return (
                self.alpha1 * (x1 ** self.rho)
              + self.alpha2 * (x2 ** self.rho)
                ) ** (1/self.rho)
      else:
        return 1

    def eval_rectangle(self, x1, x2):
      x1n = np.tile(x1, (x2.size,1)).astype(np.float32)
      x2n = np.tile(x2, (x1.size,1)).astype(np.float32).T
      res = self.eval(x1n, x2n)

      if self.rho != 0:
        return res
      else:
        return np.ones(x1n.shape) 

    def eval_derivatives(self, x1, x2):
      if self.rho != 0:
        res_eval = self.eval(x1,x2)
        denom = self.alpha1 * (x1 ** self.rho) + self.alpha2 * (x2 ** self.rho)

        return self.alpha1 * (res_eval / x1) * self.alpha1 * (x1 ** self.rho) / denom, self.alpha2 * (res_eval / x2) * self.alpha1 * (x2 ** self.rho) / denom

      else:
        return 0

    def eval_derivatives_rectangle(self, x1, x2):
      x1n = np.tile(x1, (x2.size,1)).astype(np.float32)
      x2n = np.tile(x2, (x1.size,1)).astype(np.float32).T

      if self.rho != 0:
        res_eval = self.eval(x1n, x2n)
        denom = self.alpha1 * (x1n ** self.rho) + self.alpha2 * (x2n ** self.rho)
        return self.alpha1 * (res_eval / x1n) * self.alpha1 * (x1n ** self.rho) / denom, self.alpha2 * (res_eval / x2n) * self.alpha1 * (x2n ** self.rho) / denom
      else:
        return np.ones(x1n.shape), np.ones(x2n.shape) 

    def eval_cheaper(self, x1, x2, ratio_prices):
      derivatives = self.eval_derivatives_rectangle(x1,x2)
      return derivatives[0] / ratio_prices > derivatives[1]

    def eval_cheaper_rectangle(self, x1, x2, ratio_prices):
      derivatives = self.eval_derivatives_rectangle(x1,x2)
      return derivatives[0] / ratio_prices > derivatives[1]

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