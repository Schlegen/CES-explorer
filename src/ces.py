import numpy as np
import control as ct
import control.optimal as obc
import scipy.optimize as sciop

from math import isnan

class CES:
    ''' Implementation of a CES 
        y = (alpha1 (x1 ** rho) + alpha2 (x2 ** rho)) ** (1/rho)
    '''

    def __init__(self, alpha1, alpha2, x10, x20, p1, p2, rho):
      self.alpha1 = alpha1
      self.alpha2 = alpha2
      self.x10 = x10
      self.x20 = x20
      self.p1 = p1
      self.p2 = p2
      self.rho = rho
      self.elast = 1 / (1 - rho) if rho != 1 else 'inf'

    @classmethod
    def from_alphas(cls, alpha1, alpha2, rho):
      x10 = 1
      x20 = 1
      p1 = 1
      p2 = 1
      return cls(alpha1, alpha2, x10, x20, p1, p2, rho)

    @classmethod
    def from_initial_conditions(cls, x10, x20, p1, p2, rho):
      alpha1 = x10 * p1 / (x10 * p1 + x20 * p2)
      alpha2 = x20 * p2 / (x10 * p1 + x20 * p2)
      return cls(alpha1, alpha2, x10, x20, p1, p2, rho)

    # EVALUATION FUNCTIONS
    def eval(self, x1, x2):
      if self.rho != 0:
        return (
                self.alpha1 * ((x1 / self.x10) ** self.rho)
              + self.alpha2 * ((x2 / self.x20) ** self.rho)
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
        denom = self.alpha1 * ((x1 / self.x10) ** self.rho) + self.alpha2 * ((x2 / self.x20) ** self.rho)

        return (res_eval / x1) * self.alpha1 * ((x1/self.x10) ** self.rho) / denom, (res_eval / x2) * self.alpha2 * ((x2 / self.x20) ** self.rho) / denom

      else:
        return 0

    def eval_derivatives_rectangle(self, x1, x2):
      x1n = np.tile(x1, (x2.size,1)).astype(np.float32)
      x2n = np.tile(x2, (x1.size,1)).astype(np.float32).T

      if self.rho != 0:
        res_eval = self.eval(x1n, x2n)
        denom = self.alpha1 * ((x1n / self.x10) ** self.rho) + self.alpha2 * ((x2n/self.x20) ** self.rho)
        return self.alpha1 * (res_eval / x1n) * self.alpha1 * ((x1n / self.x10) ** self.rho) / denom, self.alpha2 * (res_eval / x2n) * self.alpha1 * ((x2n/self.x20) ** self.rho) / denom
      else:
        return np.ones(x1n.shape), np.ones(x2n.shape) 

    # EVALUATION FUNCTIONS

    def update_function(self,t,x,u,params):
        p1 = params.get('p1')
        p2 = params.get('p2')
        x1_0 = params.get('x1_0')
        x2_0 = params.get('x2_0') 
  
        dydx1, dydx2 = self.eval_derivatives(x[0] + x1_0, x[1] + x2_0)
        
        if isnan(dydx1):
            dydx1 = 0
        if isnan(dydx2):
            dydx2 = 0

        dx1dt, dx2dt = u[0] / p1, u[1] / p2

        return np.array([dx1dt, dx2dt, (dydx1 * dx1dt + dydx2 * dx2dt)])
    
    def output_function(self,t,x,u,params):
      x1_0 = params.get('x1_0')
      x2_0 = params.get('x2_0')
      y_0 = params.get('y_0') 
      # Todo: set initial conditions for x[2] 
      return np.array([x[0] + x1_0, x[1] + x2_0, x[2] + y_0])

class ControlProblem:
    def __init__(self, rho=-2, q0=np.array([1.,1.]), p=np.array([1.,1.]), calib_mode='quantities', I=1., Tf=10):
        """
        """

        # initial value of y is always 1 (because of x normalisation and alpha1 + alpha2 = 1)
        self.x0 = np.array([q0[0],
                          q0[1],
                          1])
        self.p = p

        self.params = {
            'p1': p[0],
            'p2': p[1],
            'x1_0' : q0[0],
            'x2_0' : q0[1],
            'y_0' : 1
        }

        if 'quantities' in  calib_mode.lower():
          self.ces = CES.from_initial_conditions(self.x0[0], self.x0[1], 1, 1, rho)
        elif 'investments' in calib_mode.lower():
          self.ces = CES.from_initial_conditions(self.x0[0], self.x0[1], p[0], p[1], rho)
        else :
          raise ValueError(f"calib_mode.lower() should contain \'quantities\' or \'money\' current value is {calib_mode.lower()}")

        self.dynamic =  ct.NonlinearIOSystem(
              self.ces.update_function, 
              self.ces.output_function,
              states=3, name='investment',
              inputs=('i1', 'i2'), outputs=('x1','x2','y'), params=self.params)
    
        self.I = I
        self.Tf = Tf
    
        self.constraints = [obc.input_range_constraint(self.dynamic, [0.0, 0.0], [self.I, self.I]),
                           sciop.LinearConstraint(np.array([0, 0, 0, p[0], p[1]]),  0, self.I)]
    
        self.cost = obc.quadratic_cost(self.dynamic, Q=np.diag([0,0,-1]), R=np.diag([0,0])) # 0 0 1 0 0
        
        self.timepts = np.linspace(0, Tf, 11, endpoint=True)
           
    def solve(self):
        self.result = obc.solve_ocp(
             self.dynamic,
             timepts=self.timepts,
             X0=0, # bug : x0 seems not to be taken in account
             initial_guess=np.array([self.I/2, self.I/2]),
             cost=self.cost,
             trajectory_constraints=self.constraints,
             )

        self.t = self.result.time

        self.x1 = self.result.states[0] + self.x0[0]
        self.x2 = self.result.states[1] + self.x0[1]
        self.y = self.result.states[2] + self.x0[2]

        self.i1 = self.result.inputs[0]
        self.i2 = self.result.inputs[1]